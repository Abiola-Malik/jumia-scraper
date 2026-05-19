import requests 
from bs4 import BeautifulSoup
from utils.logger import logger
from core.repository import insert_product


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

class Scraper:
    def __init__(self, url):
        self.url = url
        self.headers = headers
        self.results = []

    def fetch(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            logger.info(f"Fetching URL: {self.url} - Status Code: {response.status_code}")
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {self.url}: {e}")
            return None

    def parse(self):
        self.results = []  # Clear previous results before parsing
        response = self.fetch()
        if not response:
            return []
        soup = BeautifulSoup(response, 'html.parser')
        for article in soup.find_all('article', class_='prd _box _hvr'):
            try:
                price_string = article.find('div', class_='prc').text.strip().replace('₦', '').replace(',', '')
                contains_range = ' - ' in price_string
                if contains_range:
                    price_string = price_string.split(' - ')[0].strip()
                is_tag = article.find('div', class_='prc').get('data-oprc')
                name = article.find('div', class_='name').text.strip()
                current_price = float(price_string)
                original_price = float(is_tag.strip().replace('₦', '').replace(',', '')) if is_tag else None
                image_url = article.find('img')['src']
                extracted_url = article.find('a', class_='core')['href']
                product_url = f"https://www.jumia.com.ng{extracted_url}"
                category = article.find('a', class_='core')['data-gtm-category']
                site = "jumia"
                self.results.append({
                    'name': name,
                    'current_price': current_price,
                    'original_price': original_price,
                    'image_url': image_url,
                    'product_url': product_url,
                    'category': category,
                    'site': site
                })
                insert_product(self.results[-1])
            except Exception as e:
                logger.error(f"Error processing product: {e}")
                continue
        return self.results

