import psycopg2
import os

from dotenv import load_dotenv

from accuracy_analysis.accuracy_analysis_start import accuracy_analysis
from performance_analysis.performance_analysis_start import performance_analysis

from create_summary import create_summary_report

load_dotenv()

save_path = "../../results/"
data_path = '../../data/benchmark_results.csv'


def get_db_connection():    
    """Создает подключение к PostgreSQL"""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        print("Успешное подключение к базе данных")
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {str(e)}")
        raise



if __name__ == "__main__":
    conn = get_db_connection()

    accuracy_results = accuracy_analysis(save_path, conn, 100000)
    performance_results = performance_analysis(save_path, data_path)

    create_summary_report(accuracy_results, performance_results, save_path)
    