from logs import config

__author__ = 'Rabbi'

import logging
from logging import handlers, Formatter

class LogManager(logging.Logger):
    """
    This class is used to manage logs
    """

    def __init__(self, logName):
        super(LogManager, self).__init__(logName, logging.DEBUG)
        self.addHandler(LogHandler().getTimeRotatingFileHandler())


class SingleRotatingFileHandler(handlers.RotatingFileHandler):
    """
    This class extends RotatingFileHandler. It's singleton.
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(SingleRotatingFileHandler, cls).__new__(cls, *args, **kwargs)
        return cls.instance


class SingleTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    This class extends TimeRotatingFileHandler. It's singleton.
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(SingleTimedRotatingFileHandler, cls).__new__(cls, *args, **kwargs)
        return cls.instance


class LogHandler:
    """
    This class will return Singleton RotatingFileHandler and Singleton TimeRotatingFileHandler.
    """
    def getRotatingFileHandler(self):
        handler = SingleRotatingFileHandler(config.FILE_NAME, config.MODE, config.MAX_BYTES,
            config.BACKUP_COUNT, config.ENCODING, config.DELAY)
        handler.setFormatter(Formatter(config.LOG_FORMAT, config.TIME_FORMAT))
        return handler

    def getTimeRotatingFileHandler(self):
        handler = SingleTimedRotatingFileHandler(config.FILE_NAME, when=config.WHEN, interval=config.INTERVAL,
            backupCount=config.BACKUP_COUNT)
        handler.setFormatter(Formatter(config.LOG_FORMAT, config.TIME_FORMAT))
        return handler