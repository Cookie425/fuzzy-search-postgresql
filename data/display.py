import pandas as pd
import os
from pathlib import Path

def display_benchmark_results():
    # Получаем путь к текущей директории
    current_dir = Path(__file__).parent
    
    # Формируем путь к файлу benchmark_results.csv
    csv_path = current_dir / "benchmark_results.csv"
    
    # Проверяем существование файла
    if not csv_path.exists():
        print(f"Файл {csv_path} не найден!")
        return
    
    # Читаем CSV файл
    try:
        df = pd.read_csv(csv_path)
        
        # Выводим таблицу
        print("\nBenchmark Results Table:")
        print("=" * 80)
        print(df.to_string(index=False))
        print("=" * 80)
        
        # Дополнительная информация
        print(f"\nФайл: {csv_path}")
        print(f"Всего записей: {len(df)}")
        print(f"Колонки: {', '.join(df.columns)}")
        
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")

if __name__ == "__main__":
    display_benchmark_results()