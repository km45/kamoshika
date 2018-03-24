# -*- coding: utf-8 -*-

import logging


LOG_LEVEL_MAP = {
    "fatal": logging.FATAL,
    "error": logging.ERROR,
    "warn": logging.WARN,
    "info": logging.INFO,
    "debug": logging.DEBUG
}


def create_logger(log_level: int) -> logging.Logger:
    """Create logger instance

    Args:
        log_level: log level integer value [0, 100]

    Returns:
        logger instance
    """
    log_format = (
        '[%(asctime)s] [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logger
