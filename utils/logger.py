import logging

# Set up logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set default log level to INFO using the DIWEC code i created for hierarchy of levels
#format fot log messages

formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log to file and console and creating handlers for both
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
