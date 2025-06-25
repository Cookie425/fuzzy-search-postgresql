import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_performance(df: pd.DataFrame, path: str):
    try:        
        plt.style.use('seaborn-v0_8')
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        
        # Подготовка данных
        df = df.copy()
        df['index_used'] = df['index_used'].fillna(False).astype(bool)
        df['dataset_size'] = pd.Categorical(
            df['dataset_size'], 
            categories=[1000, 10000, 100000], 
            ordered=True
        )
        
        # Группируем данные для усреднения
        grouped = df.groupby(['method', 'dataset_size', 'index_used'])['execution_time_ms'].mean().reset_index()
        
        # Создаем фигуру с двумя подграфиками
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 8), sharey=True)
        
        # Цветовая палитра и стили линий
        palette = sns.color_palette("husl", len(grouped['method'].unique()))
        markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p']
        
        # График с индексами
        indexed = grouped[grouped['index_used']]
        if not indexed.empty:
            for i, method in enumerate(indexed['method'].unique()):
                method_data = indexed[indexed['method'] == method]
                ax1.plot(
                    method_data['dataset_size'].astype(str),
                    method_data['execution_time_ms'],
                    label=method,
                    marker=markers[i % len(markers)],
                    markersize=8,
                    linewidth=2,
                    color=palette[i]
                )
            
            ax1.set_title('Производительность методов (с индексами)', pad=15)
            ax1.set_xlabel('Размер датасета', labelpad=10)
            ax1.set_ylabel('Среднее время выполнения (мс)', labelpad=10)
            ax1.set_yscale('log')
            ax1.grid(True, linestyle=':', alpha=0.7)
            ax1.legend(
                title='Метод',
                bbox_to_anchor=(1.02, 1),
                loc='upper left',
                frameon=True,
                fontsize=10
            )
        
        # График без индексов
        non_indexed = grouped[~grouped['index_used']]
        if not non_indexed.empty:
            for i, method in enumerate(non_indexed['method'].unique()):
                method_data = non_indexed[non_indexed['method'] == method]
                ax2.plot(
                    method_data['dataset_size'].astype(str),
                    method_data['execution_time_ms'],
                    label=method,
                    marker=markers[i % len(markers)],
                    markersize=8,
                    linewidth=2,
                    color=palette[i]
                )
            
            ax2.set_title('Производительность методов (без индексов)', pad=15)
            ax2.set_xlabel('Размер датасета', labelpad=10)
            ax2.grid(True, linestyle=':', alpha=0.7)
            ax2.legend(
                title='Метод',
                bbox_to_anchor=(1.02, 1),
                loc='upper left',
                frameon=True,
                fontsize=10
            )
        
        # Общий заголовок
        fig.suptitle(
            'Сравнение производительности методов поиска\n(логарифмическая шкала времени)',
            y=1.02,
            fontsize=16,
            fontweight='bold'
        )
        
        # Регулировка отступов
        plt.tight_layout()
        
        # Сохранение
        os.makedirs(os.path.join(path, 'performance_metrics'), exist_ok=True)
        plt.savefig(
            os.path.join(path, 'performance_metrics', 'performance_comparison.png'),
            bbox_inches='tight',
            dpi=300,
            facecolor='white'
        )
        
    except Exception as e:
        print(f"Ошибка при построении графиков: {e}")
        raise
    finally:
        plt.close()