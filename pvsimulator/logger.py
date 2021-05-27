import os
import logging
import config as cfg
from logging import Formatter
from logging.handlers import RotatingFileHandler


def setup_logging(logger_name):
    """
        Creates a rotating log
    """
    log_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s"
    if not os.path.isdir(cfg.LOG_DIRECTORY):
        os.mkdir(cfg.LOG_DIRECTORY)
    log_file_path = os.path.join(cfg.LOG_DIRECTORY, cfg.LOG_NAME)

    file_handler = RotatingFileHandler(log_file_path, maxBytes=10 ** 6, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(Formatter(log_file_format))
    logging.basicConfig(format=log_file_format, level=logging.INFO, filename=log_file_path)
    main_logger = logging.getLogger(logger_name)
    main_logger.addHandler(file_handler)

    return main_logger
