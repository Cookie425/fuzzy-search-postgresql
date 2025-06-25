import pandas as pd

from .plot_performance import plot_performance
from .plot_resource_usage import plot_resource_usage


def load_and_preprocess_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {path} не найден.")

    # Проверяем наличие минимально необходимых колонок
    required_columns = [
        'method', 'dataset_size', 'execution_time_ms',
        'cpu_usage', 'memory_usage', 'index_used'
    ]
    
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Отсутствует обязательная колонка: {col}")

    # Преобразуем булевы значения
    if 'index_used' in df.columns:
        df['index_used'] = df['index_used'].astype(bool)
    
    # Преобразуем размер датасета в категориальный тип
    df['dataset_size'] = df['dataset_size'].astype('category')
    
    return df


def performance_analysis(save_path: str, data_path: str):
    try:
        # Загрузка данных
        df = load_and_preprocess_data(data_path)

        # Построение графиков
        plot_performance(df, save_path)
        plot_resource_usage(df, save_path)
        
        print("Анализ завершен успешно. Все графики сохранены")
        return df  # Возвращаем данные для сводного отчета
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        raise