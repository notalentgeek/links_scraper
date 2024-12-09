import time

from src.core.producer import Producer
from src.utils.config import (
    KAFKA_BROKER,
    KAFKA_CLIENT_ID,
    KAFKA_TOPIC,
    URL_INTERVAL,
    URLS,
)
from src.utils.logger import setup_logger

# Logger
logger = setup_logger()


def producer_service():
    '''Entry point for the producer service.'''
    # Initialize the producer wrapper
    producer = Producer(
        KAFKA_BROKER,
        KAFKA_CLIENT_ID,
        KAFKA_TOPIC
    )

    logger.info(
        f'Starting URL producer, sending messages to topic: {KAFKA_TOPIC}')

    try:
        while True:
            for url in URLS:
                # Send the message
                producer.send_message(key='url', value=url)

                # Flush the producer buffer
                producer.flush()

                logger.info(f'Sent URL: {url}')

                time.sleep(URL_INTERVAL)  # Wait before the next message
    except KeyboardInterrupt:
        logger.info('Stopping URL producer...')
    finally:
        producer.flush()  # Ensure all messages are sent


if __name__ == '__main__':
    producer_service()
