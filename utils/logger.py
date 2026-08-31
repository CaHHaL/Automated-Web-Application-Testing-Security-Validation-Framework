"""
utils/logger.py
---------------
Centralised logging configuration for the WebTestX framework.

Usage
-----
    from utils.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Test started")
    logger.error("Assertion failed: %s", detail)
"""

import logging
import os
from pathlib import Path

from utils.config import config


def _ensure_reports_dir() -> None:
    """Create the reports directory if it does not exist."""
    Path(config.REPORTS_DIR).mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger pre-configured with both a console handler
    and a rotating file handler.

    Parameters
    ----------
    name:
        Typically ``__name__`` of the calling module.

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers when the function is called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))

    # ------------------------------------------------------------------ #
    #  Formatter
    # ------------------------------------------------------------------ #
    fmt = logging.Formatter(
        fmt="%(asctime)s  [%(levelname)-8s]  %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ------------------------------------------------------------------ #
    #  Console handler
    # ------------------------------------------------------------------ #
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)

    # ------------------------------------------------------------------ #
    #  File handler
    # ------------------------------------------------------------------ #
    _ensure_reports_dir()
    log_file = os.path.join(config.REPORTS_DIR, "webtestx.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    # Do not propagate to the root logger to prevent duplicate output
    logger.propagate = False

    return logger
