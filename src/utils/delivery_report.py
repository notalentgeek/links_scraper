from src.utils.logger import setup_logger

# Logger
logger = setup_logger()


def delivery_report(err, msg):
    '''
    Callback for reporting the delivery status of a Kafka message.

    This function is triggered by the Kafka producer for each message.
    It logs whether the delivery was successful or failed.

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
