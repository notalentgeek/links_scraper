import logging


def setup_logger(name=__name__):
    """Set up a logger with the given class name."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    return logging.getLogger(name)
