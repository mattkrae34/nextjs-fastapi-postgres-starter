import logging
import logging.config


# formats all extra args provided by the context handler and adds it to the log
class CustomLogFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__(
            fmt="%(asctime)s %(levelname)s %(name)s [%(module)s:%(lineno)d] %(message)8s",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="%",
        )


# sets root logger with the set format and env
def setup_logging(output_file=None) -> None:
    log_level = "INFO"
    handlers = {
        "default": {
            "level": "INFO",
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
    }
    if output_file is not None:
        handlers["file"] = {
            "level": log_level,
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": output_file,
        }
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"()": CustomLogFormatter},
        },
        "handlers": handlers,
        "loggers": {
            "": {
                "handlers": ["default"] + (["file"] if output_file else []),
                "level": log_level,
            },
        },
    }

    logging.config.dictConfig(logging_config)
