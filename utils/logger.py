import logging


def setup_logger(name=__name__):
    '''Set up a logger with the given class name.

    This function configures the logging system with a specific format and
    level. It returns a logger instance that can be used for logging messages
    throughout the application.

    Args:
        name (str): The name of the logger, usually set to the module or class
            name. Defaults to the current module's name.

    Returns:
        logging.Logger: A logger instance configured for use.
    '''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    return logging.getLogger(name)
