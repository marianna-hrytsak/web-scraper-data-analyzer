from concurrent.futures import ThreadPoolExecutor, wait
import queue
import threading
import logging
import config

from storage import save_to_csv
from analyzer import consumer
from scraper import fetch_page
from config import FILENAME, KEYWORDS, URLS

NUM_OF_CONSUMERS = 3

def main():
    logging.info("Starting analysis...")
    articles_queue = queue.Queue()
    results_queue = queue.Queue()
    stop_event = threading.Event()

    max_workers = NUM_OF_CONSUMERS + len(URLS)

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            consumer_thread = [ executor.submit(consumer, articles_queue, results_queue, KEYWORDS, stop_event)
                            for _ in range(NUM_OF_CONSUMERS) ]
            producer_thread = [ executor.submit(fetch_page, url, articles_queue, stop_event) 
                            for url in URLS ]

            wait(producer_thread)
            articles_queue.join()
            stop_event.set()
            wait(consumer_thread)

            for future in producer_thread + consumer_thread:
                if future.exception():
                    logging.error(f"Wątek zakończył się błędem: {future.exception()!r}")
    except KeyboardInterrupt:
        logging.warning("Przerwano przez użytkownika - zamykanie wątków.")
        stop_event.set()

    save_to_csv(results_queue, FILENAME, KEYWORDS)
    logging.info("Finished!")

if __name__ == "__main__":
    main()