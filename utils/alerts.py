import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import getenv
from utils.logger import logger

def send_price_alert(product_name, old_price, new_price, product_url):
    sender_email = getenv('ALERT_EMAIL')
    sender_password = getenv('ALERT_EMAIL_PASSWORD')
    recipient_email = getenv('ALERT_RECIPIENT_EMAIL')

    subject = f"Price Drop Alert: {product_name}"
    body = f"""
    Good news! A product you are tracking has dropped in price.

    Product: {product_name}
    Old Price: ₦{old_price:,.2f}
    New Price: ₦{new_price:,.2f}
    Savings: ₦{old_price - new_price:,.2f}
    
    View Product: {product_url}
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            logger.info(f"Price alert sent for: {product_name}")
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")