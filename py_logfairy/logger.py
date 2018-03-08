import logging

from logging.handlers import RotatingFileHandler


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
    logger = logging.getLogger() or base_logger
    log_name = logdir + filename + '-worker'
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
