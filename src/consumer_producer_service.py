import threading
import time
from queue import Queue

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from core.consumer import Consumer
from core.producer import Producer
from utils.chrome_driver import setup_chrome_driver
from utils.config import (
    KAFKA_BROKER,
    KAFKA_CLIENT_ID,
    KAFKA_TOPIC,
    URL_INTERVAL,
    URL_TIMEOUT,
    URL_WAIT_TIMER,
)
from utils.logger import setup_logger

# Logger
logger = setup_logger()

# Chrome Driver
driver = setup_chrome_driver()

# A flag to indicate if the thread should stop
stop_flag = threading.Event()


def main():
    """Entry point for the consumer-producer service."""
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
        f"Starting URL consumer, listening for messages on topic: "
        f"{KAFKA_TOPIC}"
    )
    logger.info(
        f"Starting URL producer, sending messages to topic: "
        f"{KAFKA_TOPIC}"
    )

    try:
        while True:
            # Poll for new messages from Kafka
            message = consumer.consume_message()

            if message:
                url = message.get('value')
                if url:
                    # Process the URL and extract links
                    urls = process_url(url.decode('utf-8'))

                    for url in urls:
                        # Send each URL to the producer
                        producer.send_message(key='url', value=url)

                        # Ensure the message is sent
                        producer.flush()
            else:
                # Wait for 1 second before checking again
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping URL consumer...")
        logger.info("Stopping URL producer...")
    finally:
        consumer.close()  # Close the consumer
        producer.flush()  # Ensure all messages are sent


def process_url(url):
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
                link_elements = driver.find_elements(By.TAG_NAME, 'a')

                urls = set()
                for idx, element in enumerate(link_elements):
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
                logger.info(f"Stop flag is set, not loading the URL: {url}")
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
            logger.info('Extracted Links:')
            for url in extracted_urls:
                logger.info(url)

            return extracted_urls

    except Exception as e:
        logger.error(f'Error: {e}')
        return []  # Return an empty list if any other error occurs

    # Idle after processing each URL
    logger.info('Waiting before processing next URL...')
    time.sleep(URL_INTERVAL)


if __name__ == "__main__":
    main()
