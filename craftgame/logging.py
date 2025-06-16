import logging

from pythonjsonlogger import json

from craftgame.config import Settings


def configure_logging(config: Settings):
    log_format = "%(levelname)s:\t %(name)s - %(message)s"
    handler = logging.StreamHandler()
    level = logging.DEBUG

    logging.basicConfig(level=level, format=log_format, handlers=[handler])
