import structlog

from django.conf import settings



def drop_unwanted_fields(_, __, event_dict):
    """Remove sensitive/unneeded fields"""
    return {k: v for k, v in event_dict.items() if k not in settings.DISABLED_FIELDS_TO_LOG}


def configure_structlog():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            drop_unwanted_fields,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
            "console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "file": {
                "class": "logging.handlers.WatchedFileHandler",
                "filename": str(settings.LOG_DIR / settings.BACKEND_LOG_FILE_NAME),
                "formatter": "json",
            },
        },
        "loggers": {
            # Only capture what YOU want from Django
            "django": {
                "handlers": ["console"],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            # Your app logger (name depends on project)
            "app": {
                "handlers": ["console", "file"],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": settings.LOG_LEVEL,
        },
    }
