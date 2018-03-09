import logging
import structlog
import sys

from logging.handlers import RotatingFileHandler


def configure_structlog():
    structlog.configure(
        processors=get_processors(),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_processors():
    py27_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeEncoder(),
        structlog.processors.JSONRenderer(ensure_ascii=False)
    ]

    py3_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(ensure_ascii=False)
    ]

    if sys.version_info[0] < 3:
        return py27_processors
    else:
        return py3_processors


def get_logger(filename, max_bytes=None,
               encoding='utf-8', base_logger=None,
               backup_count=1, logdir='/var/log/',
               conf=None):
    """Return logger with attached handlers.

    Given an existing logger, attach multiple
    handlers to the logger. Creates an INFO,
    DEBUG, and ERROR level RotatingFileHandler
    for given logger.

    Args:
        filename: str, basename of log file
        max_bytes: int, optional max size for log file
                   before a new one is created
        base_logger: <logging.Logger>, optional existing
                     logger to attach RotatingFileHandlers
        encoding: str, optional encoding for log files
        backup_count: int, optional number of backups logs to create
        logdir: str, optional directory to write log files.
                Combines with filename to create log path.

    Returns:
        <logging.Logger>
    """
    configure_structlog()

    logger = structlog.get_logger()

    logger.setLevel(logging.INFO)

    log_name = logdir + filename
    max_bytes = max_bytes or 10*1024*1024 # 10 MiB

    conf = conf or {
        'maxBytes': max_bytes,
        'encoding': encoding,
        'backupCount': backup_count
    }

    InfoRotatingHandler = RotatingFileHandler(
        '{}-info.log'.format(log_name), **conf
    )
    InfoRotatingHandler.setLevel(logging.INFO)

    DebugRotatingHandler = RotatingFileHandler(
        '{}-debug.log'.format(log_name), **conf
    )
    DebugRotatingHandler.setLevel(logging.DEBUG)

    ErrorRotatingHandler = RotatingFileHandler(
        '{}-error.log'.format(log_name), **conf
    )
    ErrorRotatingHandler.setLevel(logging.ERROR)

    logger.addHandler(InfoRotatingHandler)
    logger.addHandler(DebugRotatingHandler)
    logger.addHandler(ErrorRotatingHandler)

    return logger
