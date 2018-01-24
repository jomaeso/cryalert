import logging
from logging.handlers import RotatingFileHandler

def logging_setup(name, path, maxBytes=2000, backupCount=5, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=maxBytes,
                                  backupCount=backupCount)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    return logger
