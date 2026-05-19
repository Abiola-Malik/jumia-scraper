from core.database import create_table, init_db_pool
from core.scraper import Scraper
from utils.logger import logger
import schedule
import time
init_db_pool()
create_table()




def job():
    logger.info("Starting scheduled job: Scraping Jumia")
    SiteScraper = Scraper("https://www.jumia.com.ng/")

    results = SiteScraper.parse()
    logger.info(f"Scheduled job completed: {len(results)} products processed")
job()  
schedule.every(12).hours.do(job) 

while True:
    schedule.run_pending()
    time.sleep(60)