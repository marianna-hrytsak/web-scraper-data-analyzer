import csv

def save_to_csv(results, filename, keywords):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url'] + keywords
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        while not results.empty():
            result = results.get()
            row = {"url": result["url"], **result["counts"]}
            writer.writerow(row)