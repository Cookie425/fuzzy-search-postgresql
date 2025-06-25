import random
import uuid
from faker import Faker
from typing import Dict, List, Tuple
from introduce_typo import introduce_typo

fake = Faker()

categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports', 'Home', 'Toys']
brands = ['TechCorp', 'StyleBrand', 'FoodMaster', 'ReadMore', 'SportsPro', 'HomeComfort', 'FunToys']

def generate_products(
    count: int = 10000,
    test_queries: List[Dict] = None
) -> Tuple[List[Dict], Dict[str, List[str]]]:
    """Генерирует товары с учетом запросов"""
    products = []
    used_skus = set()
    query_skus = {q['correct_term']: [] for q in (test_queries or [])}
    
    # Получаем список терминов из запросов
    query_terms = [q['correct_term'] for q in (test_queries or [])]
    
    for _ in range(count):
        term = None
        
        # 1. С вероятностью 10% создаем товар с термином из запроса
        if query_terms and random.random() < 0.1:
            term = random.choice(query_terms)
            # Создаем название с термином
            name_normal = f"{fake.word().capitalize()} {term} {fake.word()}"
        else:
            while True:
                name_normal = fake.catch_phrase()
                # Проверяем, что в названии нет ни одного термина из запросов
                if not any(term.lower() in name_normal.lower() for term in query_terms):
                    break
        
        # 2. Добавляем опечатку (10% шанс)
        name = name_normal
        if random.random() < 0.1:
            name = introduce_typo(name_normal)
        
        # 3. Генерируем уникальный SKU
        while True:
            sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
            if sku not in used_skus:
                used_skus.add(sku)
                break
        
        # 4. Сохраняем товар
        products.append({
            'name': name,
            'description': fake.text(max_nb_chars=200),
            'category': random.choice(categories),
            'brand': random.choice(brands),
            'sku': sku
        })
        
        # 5. Если товар с термином - сохраняем связь
        if term is not None:
            query_skus[term].append(sku)
    
    return products, query_skus