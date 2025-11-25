import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from urllib.robotparser import RobotFileParser
from fake_useragent import UserAgent
from config import settings
from src import utils
import os

# Importaciones para rich
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import track
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

class ProfessionalScraper:
    def __init__(self):
        # Inicializar Sesión y Rotación de UA
        self.session = requests.Session()
        self.ua = UserAgent()
        self._rotate_user_agent()
        
        # Configurar Logging
        self._setup_logging()
        
        # Inicializar Parser de Robots.txt
        self.rp = RobotFileParser()
        self.rp.set_url(settings.BASE_URL + "robots.txt")
        self.robots_checked = False
        
        self.data = []

    def _setup_logging(self):
        log_dir = os.path.dirname(settings.LOG_FILE)
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(settings.LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        rich_handler = RichHandler(rich_tracebacks=True, markup=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[file_handler, rich_handler]
        )

    def _rotate_user_agent(self):
        try:
            new_ua = self.ua.random
            self.session.headers.update({"User-Agent": new_ua})
            logging.debug(f"User-Agent rotado a: {new_ua}")
        except Exception:
            # Fallback por si fake-useragent falla
            self.session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; ProScraper/1.0)"})

    def check_robots_txt(self, url):
        if not self.robots_checked:
            try:
                logging.info("Leyendo robots.txt...")
                self.rp.read()
                self.robots_checked = True
            except Exception as e:
                logging.warning(f"No se pudo leer robots.txt. Asumiendo permiso.")
                return True
        
        user_agent = self.session.headers["User-Agent"]
        return self.rp.can_fetch(user_agent, url)

    def fetch_page(self, url):
        if not self.check_robots_txt(url):
            logging.warning(f"⛔ Scraping no permitido por robots.txt en: {url}")
            return None

        sleep_time = random.uniform(*settings.DELAY_RANGE)
        time.sleep(sleep_time)
        self._rotate_user_agent()

        for attempt in range(settings.MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.content
            except requests.exceptions.RequestException as e:
                logging.error(f"⚠️ Error en {url} (Intento {attempt+1}): {e}")
                time.sleep(2)
        return None

    def parse_catalogue(self, html_content):
        """Obtiene URLs de los productos"""
        if not html_content: return []
        soup = BeautifulSoup(html_content, 'html.parser')
        product_elements = soup.select('article.product_pod')
        
        book_urls = []
        for item in product_elements:
            relative_url = item.h3.a['href']
            if "catalogue/" in relative_url:
                full_url = settings.BASE_URL + relative_url
            else:
                full_url = settings.BASE_URL + "catalogue/" + relative_url
            
            full_url = full_url.replace("com//", "com/") 
            book_urls.append(full_url)
        return book_urls

    def parse_book_detail(self, html_content, url):
        """Extrae datos reales (incluyendo Stock exacto)"""
        if not html_content: return

        soup = BeautifulSoup(html_content, 'html.parser')
        
        try:
            title = soup.select_one('.product_main h1').text
            raw_price = soup.select_one('.price_color').text
            price = utils.clean_price(raw_price)
            
            # Aquí extraemos el stock REAL
            raw_stock = soup.select_one('.instock.availability').text.strip()
            stock_qty = utils.clean_stock(raw_stock)
            
            self.data.append({
                'title': title,
                'price': price,
                'stock_qty': stock_qty,
                'url': url
            })
            
        except AttributeError as e:
            logging.warning(f"Error parseando detalle del libro {url}: {e}")

    def run(self):
        rprint(Panel.fit("[bold cyan]🚀 E-COMMERCE DEEP CRAWLER v2.0[/bold cyan]\n[yellow]Target:[/yellow] books.toscrape.com\n[dim]Mode: Full Detail Extraction[/dim]", border_style="blue"))
        
        raw_dir = "data/raw"
        os.makedirs(raw_dir, exist_ok=True)

        pages_range = range(1, 3) 
        
        for page_num in track(pages_range, description="[green]Escaneando Catálogo..."):
            
            # Construir URL del catálogo
            if page_num == 1:
                cat_url = settings.BASE_URL
            else:
                cat_url = settings.BASE_URL + f"catalogue/page-{page_num}.html"
            
            logging.info(f"📂 Procesando Catálogo Página {page_num}")
            
            html_catalog = self.fetch_page(cat_url)
            book_urls = self.parse_catalogue(html_catalog)
            
            if not book_urls:
                logging.warning("No se encontraron libros en esta página.")
                continue

            for book_url in track(book_urls, description=f"[cyan]   ↳ Extrayendo detalles (Pág {page_num})..."):
                
                html_book = self.fetch_page(book_url)
                if html_book:
                    
                    self.parse_book_detail(html_book, book_url)
                    time.sleep(0.5)

        # FINALIZAR
        self._save_data()
        self._show_summary()

    def _save_data(self):
        if not self.data: 
            logging.error("⚠️ No se extrajeron datos.")
            return
            
        df = pd.DataFrame(self.data)
        os.makedirs(os.path.dirname(settings.OUTPUT_FILE), exist_ok=True)
        df.to_csv(settings.OUTPUT_FILE, index=False)
        logging.info(f"💾 Archivo CSV generado: [underline]{settings.OUTPUT_FILE}[/underline]")

    def _show_summary(self):
        if not self.data: return
        
        df = pd.DataFrame(self.data)
        table = Table(title="📊 Resumen de Extracción (Deep Crawl)")

        table.add_column("Título", style="cyan", no_wrap=True)
        table.add_column("Precio (£)", style="green")
        table.add_column("Stock Real", justify="right", style="bold magenta")

        for _, row in df.head(5).iterrows():
            title_short = (row['title'][:30] + '...') if len(row['title']) > 30 else row['title']
            table.add_row(title_short, str(row['price']), str(row['stock_qty']))

        console.print("\n")
        console.print(table)
        console.print(f"\n[bold green]✨ Trabajo terminado.[/bold green] Total procesados: {len(df)}\n")
