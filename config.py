import logging

NAME = "Marianna Hrytsak"
INDEX_NUMBER = "47705"
KEYWORDS = ["Sport", "Polityka", "Kultura", "Nauka", "Zdrowie", "Edukacja", "Finanse"]
FILENAME = "results.csv"
URLS = ["https://www.onet.pl/", 
       "https://www.interia.pl/", 
       "https://www.gazeta.pl/0,0.html"]

logging.basicConfig(level=logging.INFO, format=f'%(asctime)s - {NAME} (Index: {INDEX_NUMBER}) - %(levelname)s - %(message)s')