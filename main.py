import threading
import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from utils.logger import setup_logger

CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'
URL_INTERVAL = 1  # Time to wait in second before processing the next URL.
URL_TIMEOUT = 10  # Time to wait in second for loading the URL.

# Need to be smaller than URL_TIMEOUT
URL_WAIT_TIMER = 5  # Time to wait in second for loading the web page.

# List of URLs to process
URLS = ['https://shopee.tw', 'https://www.naver.com/']

# Logging
logger = setup_logger()

# Configure ChromeDriver service.
chrome_service = Service(CHROME_DRIVER_PATH)

# Configure ChromeDriver options.
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# A flag to indicate if the thread should stop
# Check:
# https://stackoverflow.com/questions/9731291/how-do-i-set-the-selenium-webdriver-get-timeout
stop_flag = threading.Event()


def process_url(url):
    logger.info(f'Processing URL: {url}')

    # Function to load the URL
    def load_url():
        try:
            if not stop_flag.is_set():
                driver.get(url)
        except Exception as e:
            logger.error(f'Error while loading {url}: {e}')

    # Create a thread to load the URL
    thread = threading.Thread(target=load_url, name=url)
    thread.start()

    # Wait for the thread to complete, with a timeout of 60 seconds
    try:
        thread.join(URL_TIMEOUT)  # Timeout after 60 seconds
        if thread.is_alive():
            # If the thread is still running, set the stop flag
            logger.warning(
                f'Timeout: The page at {url} took longer than {URL_TIMEOUT} '
                f'seconds to load.'
            )
            stop_flag.set()  # Signal the thread to stop (checked in load_url)
            thread.join()    # Wait for the thread to finish cleanly
        else:
            stop_flag.clear()  # Reset the flag for the next URL
            # Allow for any redirection to complete
            time.sleep(URL_WAIT_TIMER)

            # Wait for a short while to ensure any redirection completes
            time.sleep(5)

            logger.info(f'Page loaded: {url}')
            # Capture the current URL after redirection
            current_url = driver.current_url
            if url != current_url:
                logger.info(f'Redirected to: {current_url}')

            # Find all <a> tags
            link_elements = driver.find_elements(By.TAG_NAME, 'a')

            # Extract and clean up links
            links = set()
            for idx, element in enumerate(link_elements):
                try:
                    # Try getting href before any exception occurs
                    href = element.get_attribute('href')
                    # Ensure it's a valid URL
                    if href and href.startswith('http'):
                        links.add(href)
                except StaleElementReferenceException:
                    logger.warning(
                        f'Warning: Element at index {idx} became stale and '
                        f'could not be accessed. Skipping this element.'
                    )
                except Exception as e:
                    logger.error(
                        f'Error: Failed to process element at index {idx} '
                        f'due to: {e}.'
                    )

            # Output all unique links
            links = list(links)
            logger.info('Extracted Links:')
            for link in links:
                logger.info(link)
    except Exception as e:
        logger.info(f'Error: {e}')

    # Idle after processing each URL
    logger.info('Waiting before processing next URL...')
    time.sleep(URL_INTERVAL)


try:
    while True:
        for url in URLS:
            process_url(url)
except KeyboardInterrupt:
    logger.info('\nInterrupted by user. Cleaning up...')
finally:
    driver.quit()
    logger.info('Driver closed. Exiting program.')
