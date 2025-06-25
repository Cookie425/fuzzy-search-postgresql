import random

def introduce_typo(text):
    """Генерация различных типов опечаток в тексте"""
    if len(text) < 2: return text
    
    typo_type = random.choice(['swap', 'delete', 'insert', 'replace'])
    pos = random.randint(0, len(text) - 2)
    
    if typo_type == 'swap':
        return text[:pos] + text[pos+1] + text[pos] + text[pos+2:]
    elif typo_type == 'delete':
        return text[:pos] + text[pos+1:]
    elif typo_type == 'insert':
        return text[:pos] + random.choice('abcdefghijklmnopqrstuvwxyz') + text[pos:]
    elif typo_type == 'replace':
        return text[:pos] + random.choice('abcdefghijklmnopqrstuvwxyz') + text[pos+1:]
    
    return text