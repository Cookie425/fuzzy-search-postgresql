import pandas as pd
import matplotlib.pyplot as plt
import os

from typing import Dict

def plot_metrics(metrics: Dict, path: str):
    """Визуализирует метрики"""
    try:
        os.makedirs(path, exist_ok=True)
        
        # График для методов
        methods_data = [{'method': method, **data} for method, data in metrics['by_method'].items()]
        plot_metric_comparison(
            pd.DataFrame(methods_data),
            x='method',
            metrics=['precision', 'recall', 'f1_score'],
            title='Метрики по методам поиска',
            save_path=f"{path}/methods_metrics.png"
        )
        
        # График для типов ошибок
        if metrics['by_error_type']:
            errors_data = [{'error_type': error_type, **data} for error_type, data in metrics['by_error_type'].items()]
            plot_metric_comparison(
                pd.DataFrame(errors_data),
                x='error_type',
                metrics=['precision', 'recall', 'f1_score'],
                title='Метрики по типам ошибок',
                save_path=f"{path}/errors_metrics.png"
            )
    except Exception as e:
        print(f"Ошибка при построении графиков: {str(e)}")
        raise

def plot_metric_comparison(df, x, metrics, title, save_path):
    """Строит графики сравнения метрик"""
    plt.figure(figsize=(12, 6))
    
    for i, metric in enumerate(metrics, 1):
        plt.subplot(1, len(metrics), i)
        plt.bar(df[x], df[metric])
        plt.title(metric)
        plt.xlabel(x)
        plt.ylabel('Значение')
        plt.xticks(rotation=45)
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
