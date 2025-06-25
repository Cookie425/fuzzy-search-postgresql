import traceback
from psycopg2.extensions import connection as pg_connection

from .analyze_all_metrics import analyze_all_metrics
from .plot_metrics import plot_metrics



def accuracy_analysis(path: str, conn: pg_connection, dataset_size: int = 100_000):
    print("Запуск анализа точности...")
    try:
        print("Анализ данных для записей...")
        metrics = analyze_all_metrics(conn, dataset_size=dataset_size)
        
        print("Генерация графиков...")
        plot_metrics(metrics, f"{path}/accuracy_metrics")
        
        print("Анализ успешно завершен!")
        return metrics  # Возвращаем метрики для сводного отчета
    except Exception as e:
        print(f"\nКРИТИЧЕСКАЯ ОШИБКА: {str(e)}")
        print("Детали ошибки:")
        traceback.print_exc()
        raise
    finally:
        if conn:
            conn.close()
            print("Соединение с базой данных закрыто")
