import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    logger = logging.getLogger("rotational_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=20 * 1024 * 1024, backupCount=7)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

