# mock_api/src/logger.py
import logging
import sys
from typing import Optional


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """Setup and configure logger"""
    logger = logging.getLogger(name or "mock_api")

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Create a detailed formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Prevent logging from propagating to the root logger
        logger.propagate = False

    return logger


# Create default application logger
logger = setup_logger()
