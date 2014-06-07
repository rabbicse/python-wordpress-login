import urllib2
from logs.LogManager import LogManager
import os

__author__ = 'Rabbi'


class Utils:
    def __init__(self):
        self.logger = LogManager(__name__)

    def downloadFile(self, url, savePath):
        try:
            directory = os.path.dirname(savePath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            webFile = urllib2.urlopen(url)
            localFile = open(savePath, 'wb')
            localFile.write(webFile.read())
        except Exception, x:
            self.logger.error(x)