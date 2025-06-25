import time
import psutil
import json

def analyze_query_plan(conn, query_text):
    """Анализирует план выполнения SQL-запроса используя SQL-функцию"""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM analyze_query_plan(%s)", (query_text,))
        return cur.fetchall()  # Возвращает список кортежей с данными плана

def check_index_usage(plan_data):
    """Проверяет использование индексов в плане запроса"""
    if not plan_data:
        return False
    return any(row[1] is not None for row in plan_data)  # Проверяем column index_name

def get_relevant_skus(conn, query_term):
    """Получает список релевантных SKU для запроса"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT qpm.sku FROM query_product_matches qpm
            JOIN test_queries tq ON qpm.query_id = tq.id
            WHERE tq.correct_term = %s OR tq.typo_term = %s
        """, (query_term, query_term))
        result = cur.fetchone()
        return result[0] if result else []



def benchmark_method(conn, test_run_id, method_name, query_template, search_term, 
                    error_type, dataset_size, index_used=True):
    """Выполняет бенчмарк одного метода поиска"""
    with conn.cursor() as cursor:
        try:

            # Запоминаем исходное значение index_used (параметр функции)
            requested_index_usage = index_used

            # Отключаем индексы, если нужно
            if not index_used:
                cursor.execute("SET enable_indexscan = off; SET enable_bitmapscan = off;")

            # Создаем временное представление с подмножеством данных
            cursor.execute(f"DROP VIEW IF EXISTS products_subset")
            cursor.execute(f"CREATE TEMP VIEW products_subset AS SELECT * FROM products LIMIT {dataset_size}")
            
            # Измеряем ресурсы до выполнения
            cpu_before = psutil.cpu_percent(interval=0.1)
            mem_before = psutil.virtual_memory().percent
            
            # Выполняем запрос и получаем результаты
            start_time = time.time()
            cursor.execute(query_template.format(term=search_term))
            results = cursor.fetchall()
            execution_time = (time.time() - start_time) * 1000
            
            # Измеряем ресурсы после выполнения
            cpu_after = psutil.cpu_percent(interval=0.1)
            mem_after = psutil.virtual_memory().percent
            
            # Получаем релевантные SKU
            relevant_skus = get_relevant_skus(conn, search_term)
            
            # Анализируем план выполнения
            explain_result = analyze_query_plan(conn, query_template.format(term=search_term))
            index_used = check_index_usage(explain_result)
            
            # Определяем, является ли запрос с опечаткой
            is_typo = error_type is not None

            # Восстанавливаем настройки
            if not index_used:
                cursor.execute("SET enable_indexscan = on; SET enable_bitmapscan = on;")

            # Анализируем план выполнения
            plan_data = analyze_query_plan(conn, query_template.format(term=search_term))
            index_used = check_index_usage(plan_data)
            
            # Вставляем основную запись бенчмарка
            cursor.execute("""
                INSERT INTO search_benchmarks
                (method, dataset_size, query_text, execution_time_ms, result_count,
                            test_run_id, cpu_usage, memory_usage, total_relevant, error_type, index_used, is_typo, plan_analysis)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """, (method_name, dataset_size, search_term, execution_time, len(results),
                       test_run_id, (cpu_before + cpu_after)/2, (mem_before + mem_after)/2, 
                len(relevant_skus), error_type, requested_index_usage, is_typo, json.dumps(plan_data)))
            
            benchmark_id = cursor.fetchone()[0]

            # Вставляем ожидаемые результаты
            if results:
                cursor.execute("""
                INSERT INTO benchmark_expected_results
                (benchmark_id, expected_skus)
                VALUES (%s, %s)
                """, (benchmark_id, relevant_skus))
            
            conn.commit()
            return execution_time, len(results)
        except Exception as e:
            conn.rollback()
            raise e
