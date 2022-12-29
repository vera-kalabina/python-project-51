import logging
import logging.config


ERROR_LOG_FILENAME = ".page-loader-errors.log"


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d "
                      "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "formatter": "default",
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOG_FILENAME,
            "backupCount": 2,
        },
        "verbose_output": {
            "formatter": "simple",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "page-loader-info": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
        "page-loader-error": {
            "level": "ERROR",
            "handlers": [
                "logfile",
            ],
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
log_error = logging.getLogger('page-loader-error')
log_info = logging.getLogger('page-loader-info')
