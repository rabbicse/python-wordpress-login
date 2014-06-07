__author__ = 'Rabbi'

## Common Config
FILE_NAME = 'spider.log'
BACKUP_COUNT = 20
ENCODING = None

## For Rotating File Handler
MODE = 'a'
MAX_BYTES = 2 * 1024 * 1024
DELAY = 0

## For Time Rotating File Handler
WHEN = 'H'
INTERVAL = 24

## For Log Format
LOG_FORMAT = '%(asctime)s <%(levelname)s> %(name)s : %(message)s'
TIME_FORMAT = '%Y-%m-%d %I:%M:%S %p'