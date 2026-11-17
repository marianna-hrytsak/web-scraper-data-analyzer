import os
import queue
import sys
import threading
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import consumer, count_words
KEYWORDS = ["Sport", "Polityka", "Zdrowie"]


def test_case_insensitive():
    assert count_words("SPORT Sport sPoRt", KEYWORDS)["Sport"] == 3


def test_no_matches_returns_zeros():
    assert count_words("nic tu nie ma", KEYWORDS) == {"Sport": 0, "Polityka": 0, "Zdrowie": 0}

def test_empty_text():
    assert count_words("", KEYWORDS) == {"Sport": 0, "Polityka": 0, "Zdrowie": 0}

def test_whole_words_only():
    assert count_words("sportowy transport sport", ["Sport"])["Sport"] == 1


def test_punctuation_is_word_boundary():
    assert count_words("Sport, sport. (sport) sport!", ["Sport"])["Sport"] == 4


def run_consumer(articles, keywords=KEYWORDS):
    articles_queue = queue.Queue()
    results_queue = queue.Queue()
    stop_event = threading.Event()

    for article in articles:
        articles_queue.put(article)

    thread = threading.Thread(
        target=consumer, args=(articles_queue, results_queue, keywords, stop_event)
    )
    thread.start()
    articles_queue.join()
    stop_event.set()
    thread.join(timeout=5)

    assert not thread.is_alive(), "Consumer thread did not finish in time"
    return results_queue

def drain_queue(q):
    items = []
    while not q.empty():
        items.append(q.get())
    return items

def test_consumer_processes_all_articles():
    articles = [{"url": f"http://{i}", "text": "polityka"} for i in range(10)]
    results = drain_queue(run_consumer(articles))
    assert sorted(r["url"] for r in results) == sorted(a["url"] for a in articles)

def test_consumer_survives_bad_article():
    articles = [{"url": "http://bad"}, {"url": "http://ok", "text": "sport"}]
    results = drain_queue(run_consumer(articles))
    assert [r["url"] for r in results] == ["http://ok"]


def test_consumer_stops_on_empty_queue():
    stop_event = threading.Event()
    stop_event.set()
    thread = threading.Thread(
        target=consumer, args=(queue.Queue(), queue.Queue(), KEYWORDS, stop_event)
    )
    thread.start()
    thread.join(timeout=5)
    assert not thread.is_alive()