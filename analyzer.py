import re
import queue

def count_words(text: str, keywords: list) -> dict:
    text_lower = text.lower()
    
    word_counts = {}
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        count = len(re.findall(pattern, text_lower))
        word_counts[keyword] = count
    return word_counts


def consumer(articles_queue, results_queue, keywords, stop_event):
    while not stop_event.is_set() or not articles_queue.empty():
        try:
            article = articles_queue.get(timeout=1)
        except queue.Empty:
            continue

        try:
            counts = count_words(article['text'], keywords)
            results_queue.put({'url': article['url'], 'counts': counts})
        finally:
            articles_queue.task_done()