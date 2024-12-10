import threading
import time
from queue import Queue

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from src.core.consumer import Consumer
from src.core.producer import Producer
from src.utils.chrome_driver import setup_chrome_driver
from src.utils.config import (
    KAFKA_BROKER,
    KAFKA_CLIENT_ID,
    KAFKA_TOPIC,
    URL_TIMEOUT,
    URL_WAIT_TIMER,
)
from src.utils.logger import setup_logger
from src.utils.mongodb import setup_mongodb
from src.utils.string import get_domain

# Logger
logger = setup_logger()


def consumer_producer_service(same_domain_only):
    '''Entry point for the consumer-producer service.'''
    # Logger
    db = setup_mongodb()

    # Initialize the consumer and producer
    consumer = Consumer(
        KAFKA_BROKER,
        KAFKA_CLIENT_ID,
        KAFKA_TOPIC
    )

    producer = Producer(
        KAFKA_BROKER,
        KAFKA_CLIENT_ID,
        KAFKA_TOPIC
    )

    logger.info(
        f'Starting URL consumer, listening for messages on topic: '
        f'{KAFKA_TOPIC}'
    )
    logger.info(
        f'Starting URL producer, sending messages to topic: '
        f'{KAFKA_TOPIC}'
    )

    try:
        while True:
            # Poll for new messages from Kafka
            message = consumer.consume_message()

            if message:
                retrieved_url_bytes = message.get('value')
                if retrieved_url_bytes:
                    retrieved_url = retrieved_url_bytes.decode('utf-8')
                    # Process the URL and extract urls
                    found_urls = process_url(retrieved_url)

                    for found_url in found_urls:
                        # Determine if we need to check for the same domain
                        if same_domain_only and get_domain(found_url) not in retrieved_url:
                            logger.info(f'Skipping URL: {found_url}')
                        else:
                            # Log the action
                            logger.info(f'Sending URL: {found_url}')

                            # Send each URL to the producer
                            producer.send_message(
                                key='url', value=found_url)

                            # Ensure the message is sent
                            producer.flush()

                            # Record to database
                            db.insert_one(
                                {'retrieved_url': retrieved_url,
                                    'found_url': found_url}
                            )
            else:
                # Wait for 1 second before checking again
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info('Stopping URL consumer...')
        logger.info('Stopping URL producer...')
    finally:
        consumer.close()  # Close the consumer
        producer.flush()  # Ensure all messages are sent


def process_url(url):
    '''
    Process the given URL by visiting it with a Chrome WebDriver,
    extracting all valid hyperlinks, and returning them.

    This function uses a separate thread to load the URL, with a timeout
    to prevent the process from hanging on slow or unresponsive pages.
    Extracted URLs are retrieved using a queue and returned as a list.

    Args:
        url (str): The URL to process.

    Returns:
        list: A list of extracted URLs found on the page, or an empty list if:
            - The page fails to load within the specified timeout.
            - The URL fails to load due to an error.
            - No valid URLs are found.

    Behavior:
        - Uses a Chrome WebDriver to load the page.
        - Ensures the process stops gracefully if the timeout is exceeded.
        - Filters out invalid or non-HTTP URLs.
        - Logs each step of the process for traceability.
        - Handles potential exceptions such as stale element references or
          navigation errors.

    Notes:
        - This function requires a properly configured Chrome WebDriver.
        - The WebDriver instance and threading flag are initialized within
          the function scope for isolation.
        - The function captures redirected URLs and logs them for debugging.

    Example:
        >>> extracted_urls = process_url("https://example.com")
        >>> print(extracted_urls)
        ['https://example.com/page1', 'https://example.com/page2']
    '''
    # Chrome Driver
    driver = setup_chrome_driver()

    # A flag to indicate if the thread should stop
    stop_flag = threading.Event()

    logger.info(f'Processing URL: {url}')

    # Function to load the URL
    def load_url(queue):
        try:
            if not stop_flag.is_set():
                driver.get(url)
                time.sleep(URL_WAIT_TIMER)  # Allow some time for page to load
                # Capture the current URL after redirection
                current_url = driver.current_url
                if url != current_url:
                    logger.info(f'Redirected to: {current_url}')

                # Find all <a> tags and extract valid URLs
                url_elements = driver.find_elements(By.TAG_NAME, 'a')

                urls = set()
                for idx, element in enumerate(url_elements):
                    try:
                        href = element.get_attribute('href')
                        if href and href.startswith('http'):
                            urls.add(href)
                    except StaleElementReferenceException:
                        logger.warning(
                            f'Warning: Element at index {
                                idx} became stale and '
                            f'could not be accessed.'
                        )
                    except Exception as e:
                        logger.error(
                            f'Error: Failed to process element at index {idx} '
                            f'due to: {e}.'
                        )

                # Return URLs through the queue
                queue.put(list(urls))
            else:
                logger.info(f'Stop flag is set, not loading the URL: {url}')
        except Exception as e:
            logger.error(f'Error while loading {url}: {e}')
            queue.put([])  # Return an empty list on error

    # Create a queue to hold URLs extracted by the thread
    url_queue = Queue()

    # Create and start the thread to load the URL
    thread = threading.Thread(target=load_url, args=(url_queue,), name=url)
    thread.start()

    # Wait for the thread to complete, with a timeout
    try:
        thread.join(URL_TIMEOUT)  # Timeout after a specified duration
        if thread.is_alive():
            logger.warning(
                f'Timeout: The page at {url} took longer than {URL_TIMEOUT} '
                f'seconds to load.'
            )
            stop_flag.set()  # Signal the thread to stop
            thread.join()    # Ensure the thread finishes cleanly
            return []        # Return an empty
        else:
            stop_flag.clear()  # Reset the flag for the next URL
            # Retrieve the extracted URLs from the queue
            extracted_urls = url_queue.get()

            # Output all unique URLs
            logger.info('Extracted URLs:')
            for url in extracted_urls:
                logger.info(url)

            return extracted_urls

    except Exception as e:
        logger.error(f'Error: {e}')
        return []  # Return an empty list if any other error occurs

    logger.info('Processing next URL...')


if __name__ == '__main__':
    consumer_producer_service()
