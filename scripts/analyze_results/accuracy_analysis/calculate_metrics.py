from typing import Dict


def calculate_metrics(found_count: int, expected_count: int) -> Dict[str, float]:
    """Упрощенный расчет метрик"""
    tp = min(found_count, expected_count)
    fp = max(0, found_count - expected_count)
    fn = max(0, expected_count - found_count)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1_score': round(f1, 4),
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn
    }