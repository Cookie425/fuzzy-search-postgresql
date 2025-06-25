import psycopg2
import os
from typing import Dict, List

from generate_product_data import generate_products


def get_test_queries_from_db():
    """Получаем тестовые запросы из таблицы test_queries"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT correct_term, typo_term FROM test_queries")
            return [{'correct_term': row[0], 'typo_term': row[1]} for row in cur.fetchall()]
    finally:
        conn.close()


def insert_into_database(products):
    """Вставка товаров в таблицу products"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    try:
        with conn.cursor() as cur:
            for product in products:
                cur.execute("""
                    INSERT INTO products (name, description, category, brand, sku)
                    VALUES (%(name)s, %(description)s, %(category)s, %(brand)s, %(sku)s)
                """, product)
        conn.commit()
    finally:
        conn.close()


def save_matches(matched_skus: Dict[str, List[str]]):
    """Связываем SKU товаров с запросами через query_product_matches"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    try:
        with conn.cursor() as cur:
            # 1. Получаем все запросы из БД
            cur.execute("SELECT id, correct_term FROM test_queries")
            query_mapping = {term: id for id, term in cur.fetchall()}
            
            # 2. Вставляем связи для каждого термина
            for term, skus in matched_skus.items():
                if term in query_mapping:
                    query_id = query_mapping[term]
                    try:
                        # Удаляем старую запись, если она есть
                        cur.execute("DELETE FROM query_product_matches WHERE query_id = %s", (query_id,))
                        # Вставляем новую запись с массивом SKU
                        cur.execute("""
                            INSERT INTO query_product_matches (query_id, sku)
                            VALUES (%s, %s)
                        """, (query_id, skus))
                    except psycopg2.Error as e:
                        print(f"Error inserting {query_id}: {e}")
            
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    # 1. Получаем запросы из БД в нужном формате
    test_queries = get_test_queries_from_db() 
    
    # 2. Генерация данных (передаем test_queries как есть)
    product_data, matched_skus = generate_products(100000, test_queries)
    
    # 3. Сохранение
    insert_into_database(product_data)
    save_matches(matched_skus)


    print(matched_skus.keys())

    for i, (term, skus) in enumerate(matched_skus.items()):
        if i >= 5:
            break
        print(f"\Запрос: {term}")
        print(f"Первые 5 SKU: {skus[:5]}")

