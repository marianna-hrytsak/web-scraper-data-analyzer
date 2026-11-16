import logging
import requests
from bs4 import BeautifulSoup

def fetch_page(url, articles_queue):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        text = soup.get_text(separator=' ', strip=True)
        articles_queue.put({'url': url, 'text': text})

        logging.info(f"Pobrano stronę {url} i dodano do kolejki artykułów.")

    except requests.ConnectionError as e:
        logging.error(f"Błąd połączenia podczas pobierania strony {url}: {e}")
    except requests.Timeout:
        logging.error(f"Przekroczono limit czasu podczas pobierania strony {url}")
    except requests.HTTPError as e:
        logging.error(f"Błąd HTTP podczas pobierania strony {url}: {e}")
    except Exception as e:
        logging.error(f"Nieoczekiwany błąd: {e}")