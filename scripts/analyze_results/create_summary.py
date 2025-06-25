import pandas as pd
from typing import Dict

def create_summary_report(accuracy_results: Dict, performance_results: pd.DataFrame, save_path: str):
    """Создает сводный отчет в Excel"""
    try:
        # Создаем Excel writer
        writer = pd.ExcelWriter(f"{save_path}/summary_table.xlsx", engine='xlsxwriter')
        
        # Лист с метриками точности
        accuracy_data = []
        accuracy_data.append({'category': 'all', **accuracy_results['all']})
        accuracy_data.append({'category': 'clean', **accuracy_results['clean']})
        accuracy_data.append({'category': 'typos', **accuracy_results['typos']})
        
        for method, data in accuracy_results['by_method'].items():
            accuracy_data.append({'category': f'method_{method}', **data})
            
        for error_type, data in accuracy_results['by_error_type'].items():
            accuracy_data.append({'category': f'error_{error_type}', **data})
            
        pd.DataFrame(accuracy_data).to_excel(writer, sheet_name='Accuracy Metrics', index=False)
        
        # Лист с метриками производительности
        performance_results.to_excel(writer, sheet_name='Performance Metrics', index=False)
        
        # Сохраняем файл
        writer.close()
        print(f"Сводный отчет сохранен в {save_path}/summary_table.xlsx")
        
    except Exception as e:
        print(f"Ошибка при создании сводного отчета: {str(e)}")
        raise