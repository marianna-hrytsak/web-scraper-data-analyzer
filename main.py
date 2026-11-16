from concurrent.futures import ThreadPoolExecutor, wait
import queue
import threading
import logging

from analyzer import consumer
from scraper import fetch_page
from config import NAME, INDEX_NUMBER, KEYWORDS, URLS

logging.info(f"Starting analysis for {NAME} (Index: {INDEX_NUMBER})")

def main():
    articles_queue = queue.Queue()
    results_queue = queue.Queue()
    stop_event = threading.Event()

    with ThreadPoolExecutor(max_workers=5) as executor:
        consumer_thread = [ executor.submit(consumer, articles_queue, results_queue, KEYWORDS, stop_event)
                           for _ in range(5) ]
        producer_thread = [ executor.submit(fetch_page, articles_queue, stop_event, url) 
                           for url in URLS ]

        wait(producer_thread)
        stop_event.set()
        wait(consumer_thread)