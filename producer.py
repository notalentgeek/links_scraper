import time

from confluent_kafka import Producer

from utils.config import KAFKA_BROKER, KAFKA_CLIENT_ID, KAFKA_TOPIC, URL_INTERVAL, URLS
from utils.logger import setup_logger

# Logger
logger = setup_logger()

# Producer configuration
conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'client.id': KAFKA_CLIENT_ID,
}


def delivery_report(err, msg):
    '''Callback for reporting the delivery status of a Kafka message.

    This function is triggered by the Kafka producer for each message.
    It prints a message indicating whether the delivery was successful or
    failed.

    Args:
        err (Exception or None): An error object if delivery failed, or None
            if the delivery was successful.
        msg (KafkaMessage): The Kafka message object containing metadata like
            topic and partition.
    '''
    if err is not None:
        logger.error(f'Delivery failed for message: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def main():
    # Initialize Kafka Producer
    producer = Producer(conf)

    logger.info(
        f'Starting URL producer, sending messages to topic: {KAFKA_TOPIC}')

    try:
        while True:
            for url in URLS:
                # Produce message to Kafka topic
                producer.produce(
                    KAFKA_TOPIC,
                    key=url,
                    value=url,
                    callback=delivery_report
                )

                # Flush the producer buffer
                producer.flush()

                logger.info(f'Sent URL: {url}')

                time.sleep(URL_INTERVAL)  # Wait before the next message
    except KeyboardInterrupt:
        logger.info('Stopping URL producer...')
    finally:
        producer.flush()  # Ensure all messages are sent


if __name__ == '__main__':
    main()
