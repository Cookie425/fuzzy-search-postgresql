import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_resource_usage(df: pd.DataFrame, path: str):
    try:
        # Настройка стиля
        plt.style.use('seaborn-v0_8')
        plt.rcParams['font.family'] = 'DejaVu Sans'
        
        # Подготовка данных
        df = df.copy()
        df['index_used'] = df['index_used'].fillna(False).astype(bool)
        df['dataset_size'] = pd.Categorical(df['dataset_size'], 
                                          categories=[1000, 10000, 100000], 
                                          ordered=True)

        # Создаем 4 отдельных графика (2x2)
        fig, axes = plt.subplots(2, 2, figsize=(24, 16))
        
        # Функция для создания heatmap с адаптивной шкалой
        def create_heatmap(data, ax, title, cmap):
            # Находим min и max для текущих данных (исключая NaN)
            vmin = data.min().min()
            vmax = data.max().max()
            
            # Добавляем небольшой отступ для лучшей визуализации
            range_pad = (vmax - vmin) * 0.1
            vmin = max(0, vmin - range_pad)
            vmax = vmax + range_pad
            
            sns.heatmap(
                data,
                annot=True,
                fmt=".1f",
                cmap=cmap,
                ax=ax,
                cbar_kws={'label': 'Использование (%)', 'shrink': 0.8},
                vmin=vmin,
                vmax=vmax,
                annot_kws={"size": 11},
                linewidths=0.5,
                linecolor='lightgray',
                center=(vmin + vmax)/2  # Центрируем цветовую шкалу
            )
            ax.set_title(title, pad=15, fontsize=14)
            ax.set_xlabel('Размер датасета', labelpad=10)
            ax.set_ylabel('Метод', labelpad=10)

        # CPU с индексами
        cpu_indexed = df[df['index_used']].pivot_table(
            index='method', columns='dataset_size', values='cpu_usage')
        create_heatmap(cpu_indexed, axes[0,0], 
                      'Использование CPU (с индексами)', "YlOrRd")

        # CPU без индексов
        cpu_non_indexed = df[~df['index_used']].pivot_table(
            index='method', columns='dataset_size', values='cpu_usage')
        create_heatmap(cpu_non_indexed, axes[0,1], 
                      'Использование CPU (без индексов)', "YlOrRd")

        # Память с индексами
        mem_indexed = df[df['index_used']].pivot_table(
            index='method', columns='dataset_size', values='memory_usage')
        create_heatmap(mem_indexed, axes[1,0], 
                      'Использование памяти (с индексами)', "Blues")

        # Память без индексов
        mem_non_indexed = df[~df['index_used']].pivot_table(
            index='method', columns='dataset_size', values='memory_usage')
        create_heatmap(mem_non_indexed, axes[1,1], 
                      'Использование памяти (без индексов)', "Blues")

        # Общий заголовок
        fig.suptitle('Использование ресурсов системы', y=1.02, 
                    fontsize=16, fontweight='bold')

        # Регулировка отступов
        plt.tight_layout()

        # Сохранение
        os.makedirs(os.path.join(path, 'performance_metrics'), exist_ok=True)
        plt.savefig(os.path.join(path, 'performance_metrics', 'resource_usage_comparison.png'), 
                   bbox_inches='tight', dpi=300, facecolor='white')

    except Exception as e:
        print(f"Ошибка при построении графиков: {e}")
        raise
    finally:
        plt.close()