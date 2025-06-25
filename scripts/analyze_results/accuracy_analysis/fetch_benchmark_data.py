import traceback
from typing import List, Dict

def fetch_benchmark_data(conn, dataset_size: int = 100000) -> List[Dict]:
    """Получает данные бенчмарков из БД"""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    b.method,
                    b.query_text,
                    b.result_count,
                    b.is_typo,
                    b.error_type,
                    ber.expected_skus
                FROM search_benchmarks b
                JOIN benchmark_expected_results ber ON b.id = ber.benchmark_id
                WHERE b.dataset_size = %s
                ORDER BY b.method, b.is_typo
            """, (dataset_size,))
            
            columns = [desc[0] for desc in cur.description]
            data = [dict(zip(columns, row)) for row in cur.fetchall()]
            return data
            
    except Exception as e:
        print(f"Ошибка при получении данных из базы: {str(e)}")
        traceback.print_exc()
        raise