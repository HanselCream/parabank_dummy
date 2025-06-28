import logging
import inspect


def custom_logger(loglevel=logging.DEBUG):
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    logger.setLevel(loglevel)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')

        # File handler
        fh = logging.FileHandler("automation.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Optional: Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

