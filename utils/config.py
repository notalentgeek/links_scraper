# Constants for Selenium WebDriver and URL processing
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'
URL_INTERVAL = 1  # Time to wait in seconds before processing the next URL
URL_TIMEOUT = 10  # Time to wait in seconds for loading the URL

# Need to be smaller than URL_TIMEOUT
URL_WAIT_TIMER = 5  # Time to wait in seconds for loading the web page

# List of URLs to process
URLS = ['https://shopee.tw', 'https://www.naver.com/']

# Kafka configuration
KAFKA_BROKER = 'kafka:9092'
KAFKA_CLIENT_ID = 'url-producer'
KAFKA_TOPIC = 'urls'
