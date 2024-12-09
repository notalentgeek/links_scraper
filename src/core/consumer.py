from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError, KafkaException

from src.utils.logger import setup_logger


class Consumer:
    def __init__(self, broker, group_id, topic):
        '''
        Initialize the Kafka consumer.

        Args:
            broker (str): The Kafka broker address.
            group_id (str): The consumer group ID.
            topic (str): The Kafka topic to consume messages from.
        '''
        self.logger = setup_logger()
        self.topic = topic
        self.conf = {
            'bootstrap.servers': broker,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
        }
        self.consumer = KafkaConsumer(self.conf)
        self.consumer.subscribe([self.topic])

    def consume_message(self):
        '''
        Consume a message from the Kafka topic.

        Logs the message content and offset.

        Returns:
            dict: A dictionary with the message details, including key, value,
                and offset.
        '''
        try:
            # Poll for new messages with a timeout of 1 second
            message = self.consumer.poll(timeout=1.0)
            if message is None:
                self.logger.info('No message received within the timeout.')

                return None

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    # Log end of partition
                    self.logger.info(
                        f'End of partition reached {message.partition}, '
                        f'offset {message.offset()}'
                    )
                else:
                    raise KafkaException(message.error())
            else:
                self.logger.info(
                    f'Consumed message: {message.key()}: {message.value()}')

                return {
                    'key': message.key(),
                    'value': message.value(),
                    'offset': message.offset()
                }
        except Exception as e:
            self.logger.error(f'Failed to consume message: {e}')

            return None

    def close(self):
        '''Close the consumer and release resources.'''
        self.consumer.close()
        self.logger.info('Kafka consumer closed.')
