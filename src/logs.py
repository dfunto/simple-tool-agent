import logging
from logging.config import dictConfig


def init_logger():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "fmt": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",

            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": "INFO"},
        },
    })

class LoggingMixin:
    """Convenience super-class to have a logger configured with the class name"""

    _log: logging.Logger | None = None

    @property
    def log(self) -> logging.Logger:
        """Returns a logger."""
        if self._log is None:
            self._log = logging.getLogger(self.__class__.__module__ + "." + self.__class__.__name__)
        return self._log
