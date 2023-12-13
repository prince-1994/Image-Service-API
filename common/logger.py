from logging import Logger
import logging
import sys


class AppLogger(Logger):
    def __init__(self, name: str, level=0) -> None:
        super().__init__(name, level)
        # Initial construct.
        self.format = f"{name} | %(asctime)s | %(levelname)s | %(message)s"

        # Logger configuration.
        self.console_formatter = logging.Formatter(self.format)
        self.console_logger = logging.StreamHandler(sys.stdout)
        self.console_logger.setFormatter(self.console_formatter)

        # Complete logging config.
        self.addHandler(self.console_logger)
