import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "../Logs")

os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)  
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

train_logger = setup_logger("train", os.path.join(LOG_DIR, "train.log"))
eval_logger = setup_logger("evaluate", os.path.join(LOG_DIR, "evaluate.log"))
error_logger = setup_logger("error", os.path.join(LOG_DIR, "error.log"), level = logging.ERROR)

