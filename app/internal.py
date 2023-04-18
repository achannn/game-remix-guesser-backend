import logging

logging.basicConfig()

handle = "default"
logger = logging.getLogger(handle)
logging.getLogger().setLevel(logging.INFO)

def log_error(e):
    logger.error(e)

def log_info(i: str):
    logger.info(i)
