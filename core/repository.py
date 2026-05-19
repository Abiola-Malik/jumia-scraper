from core.database import get_connection
from datetime import datetime
import psycopg2.extras
from utils.alerts import send_price_alert
from utils.logger import logger
def get_existing_product(product_url):
    conn = get_connection()
    logger.info(f"Checking if product exists: {product_url}")
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM products WHERE product_url = %s', (product_url,))
    result = cursor.fetchone()
    logger.info(f"Product found: {bool(result)}")
    cursor.close()
    conn.close()
    return result

def insert_product(product):
    conn = get_connection()
    is_existing = get_existing_product(product['product_url'])
    cursor = conn.cursor()
    if is_existing:
        if is_existing['current_price'] != product['current_price']:
            logger.info(f"Updating product price: {product['product_url']}")
            # update last_checked even if price is the same to track when it was last seen
            cursor.execute('''
                UPDATE products
                SET current_price = %s,
                    original_price = %s,
                    last_checked = %s,
                    status = 'active'
                WHERE product_url = %s
            ''', (
                product['current_price'],
                product['original_price'],
                datetime.now(),
                product['product_url']
            ))
            #send email alert here if price has dropped
            
            send_price_alert(
                 product['name'],
                 is_existing['current_price'],
                 product['current_price'],
                product['product_url']
            )
            
            
        else:
            logger.info(f"Product price unchanged: {product['product_url']}")
            cursor.execute('''
                UPDATE products
                SET last_checked = %s
                WHERE product_url = %s
            ''', (
                datetime.now(),
                product['product_url']
            ))
    else:   
        logger.info(f"Inserting new product: {product['product_url']}")
        cursor.execute('''
        INSERT INTO products (name, current_price, original_price, image_url, product_url, category, site, status, last_checked)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        product['name'],
        product['current_price'],
        product['original_price'],
        product['image_url'],
        product['product_url'],
        product['category'],
        product['site'],
        'active',
        datetime.now()
    ))
    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f"Product processed: {product['product_url']}")
    
    
