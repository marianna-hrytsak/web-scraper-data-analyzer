import re

def count_words(text: str, keywords: list) -> dict:
    text_lower = text.lower()
    
    word_counts = {}
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        count = len(re.findall(pattern, text_lower))
        word_counts[keyword] = count
    return word_counts