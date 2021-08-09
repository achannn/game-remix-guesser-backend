import logging

logging.basicConfig()

handle = "default"
logger = logging.getLogger(handle)

def log_error(e):
    print(e)
    logger.info(e)
