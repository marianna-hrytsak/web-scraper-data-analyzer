import csv
import logging


def save_to_csv(results, filename, keywords):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url'] + keywords
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()

            saved = 0
            while not results.empty():
                result = results.get()
                row = {"url": result["url"], **result["counts"]}
                writer.writerow(row)
                saved += 1
        logging.info(f"Zapisano {saved} wyników do pliku {filename}")
    except OSError as e:
        logging.error(f"Nie udało się zapisać pliku {filename}: {e}")