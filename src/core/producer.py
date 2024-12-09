from confluent_kafka import Producer as KafkaProducer

from src.utils.delivery_report import delivery_report
from src.utils.logger import setup_logger


class Producer:
    def __init__(self, broker, client_id, topic):
        """
        Initialize the Kafka producer.

        Args:
            broker (str): The Kafka broker address.
            client_id (str): The client ID to identify this producer.
            topic (str): The Kafka topic to which messages will be sent.
        """
        self.logger = setup_logger()
        self.topic = topic
        self.conf = {
            'bootstrap.servers': broker,
            'client.id': client_id,
        }
        self.producer = KafkaProducer(self.conf)

    def send_message(self, key, value, callback=delivery_report):
        """
        Send a message to the Kafka topic.

        Args:
            key (str): The key for the Kafka message.
            value (str): The value for the Kafka message.
            callback (function): The delivery report callback function.
        """
        try:
            # Send the message to Kafka
            self.producer.produce(
                self.topic,
                key=key,
                value=value,
                callback=callback
            )
            self.logger.info(
                f"Message queued for key: {key} and value: {value}")
        except Exception as e:
            self.logger.error(f"Failed to produce message: {e}")

    def flush(self):
        """Flush the producer buffer."""
        self.producer.flush()
        self.logger.info("Producer buffer flushed.")
