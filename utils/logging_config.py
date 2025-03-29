
import logging
import os

log_dir = os.path.expanduser("~/.file_encryption_logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "audit.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_event(message):
    logging.info(message)

def log_error(message):
    logging.error(message)
