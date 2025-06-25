import traceback

from typing import Dict

from .fetch_benchmark_data import fetch_benchmark_data
from .calculate_metrics import calculate_metrics

def analyze_all_metrics(conn, dataset_size: int = 100000) -> Dict[str, Dict]:
    """Анализирует метрики с упрощенной логикой"""
    try:
        benchmark_data = fetch_benchmark_data(conn, dataset_size)
        
        metrics = {
            'all': {'found_count': 0, 'expected_count': 0},
            'clean': {'found_count': 0, 'expected_count': 0},
            'typos': {'found_count': 0, 'expected_count': 0},
            'by_method': {},
            'by_error_type': {}
        }
        
        for row in benchmark_data:
            method = row['method']
            is_typo = row['is_typo']
            error_type = row['error_type']
            found_count = row['result_count']
            expected_count = len(row['expected_skus'])
            
            if not is_typo:
                metrics['clean']['found_count'] += found_count
                metrics['clean']['expected_count'] += expected_count
            else:
                metrics['typos']['found_count'] += found_count
                metrics['typos']['expected_count'] += expected_count
                
                if error_type not in metrics['by_error_type']:
                    metrics['by_error_type'][error_type] = {'found_count': 0, 'expected_count': 0}
                metrics['by_error_type'][error_type]['found_count'] += found_count
                metrics['by_error_type'][error_type]['expected_count'] += expected_count
            
            if method not in metrics['by_method']:
                metrics['by_method'][method] = {'found_count': 0, 'expected_count': 0}
            metrics['by_method'][method]['found_count'] += found_count
            metrics['by_method'][method]['expected_count'] += expected_count
        
        final_metrics = {
            'all': calculate_metrics(metrics['all']['found_count'], metrics['all']['expected_count']),
            'clean': calculate_metrics(metrics['clean']['found_count'], metrics['clean']['expected_count']),
            'typos': calculate_metrics(metrics['typos']['found_count'], metrics['typos']['expected_count']),
            'by_method': {
                method: calculate_metrics(data['found_count'], data['expected_count'])
                for method, data in metrics['by_method'].items()
            },
            'by_error_type': {
                error_type: calculate_metrics(data['found_count'], data['expected_count'])
                for error_type, data in metrics['by_error_type'].items()
            }
        }
        
        return final_metrics
        
    except Exception as e:
        print(f"Ошибка при анализе метрик: {str(e)}")
        traceback.print_exc()
        raise
