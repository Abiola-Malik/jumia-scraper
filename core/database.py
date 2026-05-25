from os import getenv
from utils.logger import logger

from dotenv import load_dotenv
import psycopg2.pool
load_dotenv()

pool = None
 
def init_db_pool():
    global pool
    if pool is None:
        dbname = getenv('POSTGRES_DB')
        host = getenv('POSTGRES_HOST', 'db')
        user = getenv('POSTGRES_USER')
        password = getenv('POSTGRES_PASSWORD')
        port = getenv('POSTGRES_PORT')
        
        logger.info(f"Initializing database connection pool: {dbname} at {host}:{port} as user {user}")
        try:
            pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=20, 
                dbname=dbname,
                host=host,
                user=user,
                password=password,
                port=port
            )
            logger.info("Database connection pool established successfully")
        except Exception as e:
            logger.critical(f"Error initializing database connection pool: {e}")
            raise e

def get_connection(): 
    if pool is None:
        logger.error("Database connection pool is not initialized")
        raise Exception("Database connection pool is not initialized")
    return pool.getconn()

def release_connection(conn):
    pool.putconn(conn)


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
    release_connection(conn)
    logger.info("Products table created or already exists")
