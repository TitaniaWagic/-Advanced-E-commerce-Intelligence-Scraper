import os

#configuraciones para guardar archivos 

BASE_URL = "https://books.toscrape.com/" #Pueba con una web segura
OUTPUT_FILE = "data/processed/books_data.csv"
LOG_FILE = "logs/scraper.log"

#Headers para imitar un navegador real
HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

MAX_RETRIES = 3
DELAY_RANGE = (1, 3)