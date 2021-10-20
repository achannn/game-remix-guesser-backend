import logging

logging.basicConfig()

handle = "default"
logger = logging.getLogger(handle)

def log_error(e):
    print("Logger logging error")
    print(e)
    logger.info(e)
