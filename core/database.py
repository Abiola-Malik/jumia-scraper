from os import getenv
from utils.logger import logger

from dotenv import load_dotenv
import psycopg2
load_dotenv()


def get_connection(): 
    dbname = getenv('dbname')
    host = getenv('host')
    user = getenv('user')
    password = getenv('password')
    port = getenv('port')
    
    logger.info(f"Connecting to database: {dbname} at {host}:{port} as user {user}")
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            host=host,
            user=user,
            password=password,
            port=port
        )
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.critical(f"Error connecting to database: {e}")
        raise e
    conn = psycopg2.connect(
    dbname=dbname,
    host=host,
    user=user,
    password=password,
    port=port
    )
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    logger.info("Creating products table if it doesn't exist")
    cursor.execute('''
        DO $$ BEGIN
             CREATE TYPE status_enum AS ENUM ('active', 'paused', 'out_of_stock', 'error');
        EXCEPTION
             WHEN duplicate_object THEN NULL;
         END $$;
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            product_url VARCHAR(255) UNIQUE NOT NULL,
            current_price NUMERIC(10, 2) CHECK (current_price > 0),
            original_price NUMERIC(10, 2),
            last_checked TIMESTAMP,
            category VARCHAR(255),
            image_url VARCHAR(255),
            site VARCHAR(50) NOT NULL,
            status status_enum NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Products table created or already exists")
