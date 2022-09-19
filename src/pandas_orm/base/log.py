import logging


def get_logger():
    logger = logging.getLogger('PandasORMLogger')
    logger.setLevel(logging.DEBUG)
    return logger
