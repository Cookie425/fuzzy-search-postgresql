import psycopg2
import time
import uuid
import pandas as pd
from dotenv import load_dotenv
import os
import psutil

from benchmark_method import benchmark_method

load_dotenv()

def get_db_connection():
    """Создает и возвращает соединение с БД"""
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'fuzzy_search_lab'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', ''),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )


def get_test_queries(conn, include_typos=True):
    """Получает тестовые запросы из БД"""
    with conn.cursor() as cur:
        if include_typos:
            cur.execute("SELECT correct_term, typo_term, error_type FROM test_queries")
            return [{'term': row[1], 'correct_term': row[0], 'error_type': row[2]} for row in cur.fetchall()]
        else:
            cur.execute("SELECT DISTINCT correct_term FROM test_queries")
            return [{'term': row[0], 'correct_term': row[0], 'error_type': None} for row in cur.fetchall()]





def run_benchmarks(dataset_sizes):
    """Основная функция для запуска всех тестов"""
    conn = get_db_connection()
    test_run_id = str(uuid.uuid4())
    
    methods = {
        'LIKE': "SELECT * FROM products_subset WHERE name LIKE '%%{term}%%'",
        'ILIKE': "SELECT * FROM products_subset WHERE name ILIKE '%%{term}%%'",
        'Trigram': "SELECT * FROM products_subset WHERE name % '{term}'",  
        'Levenshtein': "SELECT * FROM products_subset WHERE levenshtein(name, '{term}') <= 3",
        'Soundex': "SELECT * FROM products_subset WHERE soundex(name) = soundex('{term}')",
        'Metaphone': "SELECT * FROM products_subset WHERE metaphone(name, 10) = metaphone('{term}', 10)",
        'FTS': "SELECT * FROM products_subset, plainto_tsquery('english', '{term}') query WHERE search_vector @@ query"
    }
    
    results = []
    
    try:
        # Запускаем тесты для корректных терминов
        correct_queries = get_test_queries(conn, include_typos=False)

        for index_used in [True, False]:
            for size in dataset_sizes:
                for query in correct_queries:
                    for method_name, query_template in methods.items():
                        print(f"Testing {method_name} (indexes={'on' if index_used else 'off'}) with term '{query['term']}' on {size} records...")
                        try:
                            time_ms, count = benchmark_method(
                                conn, test_run_id, method_name, query_template, 
                                query['term'], query['error_type'], size, index_used
                            )
                        
                            # Получаем полные данные из БД
                            cursor = conn.cursor()
                            cursor.execute("""
                                SELECT method, query_text, execution_time_ms, result_count, 
                                        cpu_usage, memory_usage, total_relevant, is_typo, error_type, index_used
                                FROM search_benchmarks
                                WHERE test_run_id = %s AND query_text = %s AND method = %s
                                ORDER BY id DESC LIMIT 1
                                """, (test_run_id, query['term'], method_name))
                    
                            benchmark_data = cursor.fetchone()
                        
                            if benchmark_data:
                                results.append({
                                'method': benchmark_data[0],
                                'term': benchmark_data[1],
                                'execution_time_ms': benchmark_data[2],
                                'result_count': benchmark_data[3],
                                'cpu_usage': benchmark_data[4],
                                'memory_usage': benchmark_data[5],
                                'total_relevant': benchmark_data[6],
                                'is_typo': benchmark_data[7],
                                'error_type': benchmark_data[8],
                                'index_used': benchmark_data[9],
                                'dataset_size': size
                                })
                        except Exception as e:
                            print(f"Error: {e}")
                            continue
        
        # Запускаем тесты для терминов с опечатками
        typo_queries = get_test_queries(conn, include_typos=True)
        for index_used in [True, False]:  # Добавить этот цикл
            for size in dataset_sizes:
                for query in typo_queries:
                    for method_name, query_template in methods.items():
                        print(f"Testing {method_name} (indexes={'on' if index_used else 'off'}) with typo term '{query['term']}' on {size} records...")
                        try:
                            time_ms, count = benchmark_method(
                                conn, test_run_id, method_name, query_template, 
                                query['term'], query['error_type'], size, index_used
                            )
                        
                            # Аналогично получаем полные данные для опечаток
                            cursor = conn.cursor()
                            cursor.execute("""
                            SELECT method, query_text, execution_time_ms, result_count, 
                                cpu_usage, memory_usage, is_typo, error_type, index_used  
                            FROM search_benchmarks
                            WHERE test_run_id = %s AND query_text = %s AND method = %s
                            ORDER BY id DESC LIMIT 1
                            """, (test_run_id, query['term'], method_name))
                            benchmark_data = cursor.fetchone()
                        
                            if benchmark_data:
                                results.append({
                                'method': benchmark_data[0],
                                'term': benchmark_data[1],
                                'execution_time_ms': benchmark_data[2],
                                'result_count': benchmark_data[3],
                                'cpu_usage': benchmark_data[4],
                                'memory_usage': benchmark_data[5],
                                'is_typo': benchmark_data[6],
                                'error_type': benchmark_data[7],
                                'dataset_size': size,
                                'index_used': benchmark_data[8]
                                })
                        except Exception as e:
                            print(f"Error: {e}")
                            continue
        
        # Сохраняем результаты в CSV
        df = pd.DataFrame(results)
        os.makedirs('../../data', exist_ok=True)
        df.to_csv('../../data/benchmark_results.csv', index=False)
        print("Results saved to data/benchmark_results.csv")
    
    finally:
        conn.close()




if __name__ == "__main__":

    dataset_sizes = [1000, 10000, 100000]
    
    run_benchmarks(dataset_sizes)