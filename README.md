# Jumia Scraper

A Python-based price tracking tool that scrapes product listings from [Jumia Nigeria](https://www.jumia.com.ng), stores them in a PostgreSQL database, and sends email alerts when prices drop.

## Features

- Scrapes product name, price, category, and image from Jumia
- Detects price changes and sends email alerts
- Stores and tracks products in a PostgreSQL database
- Runs on a schedule (every 12 hours by default)
- Fully Dockerized — app and database run in separate containers
- Structured logging to both console and file

## Project Structure

```
jumia-scraper/
├── core/
│   ├── database.py       # DB connection pool and table setup
│   ├── repository.py     # DB read/write operations
│   └── scraper.py        # Jumia scraper logic
├── models/
│   ├── product.py        # Pydantic product model
│   └── enums.py          # Product status enum
├── utils/
│   ├── alerts.py         # Email alert logic
│   └── logger.py         # Logging setup
├── main.py               # Entry point — scheduler lives here
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                  # Not committed — see setup below
```

## Requirements

- Docker & Docker Compose
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) for email alerts

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/abiolamalik/jumia-scraper.git
cd jumia-scraper
```

### 2. Create your `.env` file

Create a `.env` file in the project root with the following variables:

```env
# Database
host=db
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432

# Email alerts
ALERT_EMAIL=your_gmail@gmail.com
ALERT_EMAIL_PASSWORD=your_app_password
ALERT_RECIPIENT_EMAIL=recipient@gmail.com
```

> **Note:** For `ALERT_EMAIL_PASSWORD`, use a Gmail App Password, not your regular Gmail password. Generate one at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

### 3. Run with Docker

```bash
docker-compose up --build
```

This will:

- Build the Python scraper image
- Pull and start a PostgreSQL container
- Start scraping Jumia and saving products to the database

## How It Works

1. On startup, the scraper runs immediately and then every 12 hours
2. Each run fetches the Jumia homepage and parses all product listings
3. New products are inserted into the database
4. Existing products are checked for price changes
5. If a price drop is detected, an email alert is sent to `ALERT_RECIPIENT_EMAIL`

## Scheduling

The scraper runs every 12 hours by default. To change the interval, update this line in `main.py`:

```python
schedule.every(12).hours.do(job)
```

## Logging

Logs are written to both the console and `app.log` in the project root. Log level is set to `INFO` by default.

## Author

**Abiola Malik**
