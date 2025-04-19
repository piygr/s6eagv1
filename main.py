import logging
import sys
from client import start_agent
from agent import app

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[1;41m' # Bold Red Background
    }
    RESET = '\033[0m'

    def format(self, record):
        levelname = record.levelname
        msg = super().format(record)
        color = self.COLORS.get(levelname, '')
        return f"{color}{msg}{self.RESET}"

def setup_logging():
    formatter = ColorFormatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", "%H:%M:%S"
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    return root_logger

setup_logging()

start_agent(app_logic=app)