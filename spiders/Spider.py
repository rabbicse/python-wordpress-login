from cStringIO import StringIO
import os
from logs.LogManager import LogManager
from spiders import config
import gc
import time
from utils.Regex import Regex

__author__ = 'Rabbi'

import urllib
import urllib2
import cookielib


class Spider:
    def __init__(self):
        self.logger = LogManager(__name__)
        self.opener = None
        self.mycookie = None

    def login(self, url, loginInfo, retry=0, proxy=None):
        """
        Login request for user
        url = '' Ex. http://www.example.com/login
        loginInfo = {} Ex. {'user': 'user', 'pass': 'pass'}
        """
        conn = ('Connection', 'keep-alive')
        ac = ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        ln = ('Accept-Language', 'en-us,en;q=0.5')
        if proxy is None:
            self.opener = self.createOpener([config.USER_AGENT, conn, ac, ln], self.createCookieJarHandler())
        else:
            self.opener = self.createOpener([config.USER_AGENT, conn, ac, ln], self.createCookieJarHandler(), proxy)
        urllib2.install_opener(self.opener)
        try:
            response = self.opener.open(url, urllib.urlencode(loginInfo))
            print 'Response from Server:'
            print 'Status: ', response.getcode()
            print response.info()
            self.logger.debug('Response from Server:')
            self.logger.debug('Status: ' + str(response.getcode()))
            self.logger.debug(response.info())
            redirected_url = response.url
            return redirected_url, response.read()
        except Exception, x:
            print x
            self.logger.error(x.message)
            if retry < config.RETRY_COUNT:
                print 'Retry again. Please wait 5 seconds...'
                time.sleep(5)
                self.login(url, loginInfo, retry + 1)
            else:
                print 'Failed to retrieve data after maximum %d retry!' % config.RETRY_COUNT
        return None, None

    def fetchData(self, url, parameters=None, retry=0):
        """
        Fetch data from a url
        url='' Ex. http://www.example.com, https://www.example.com
        parameters={} Ex. {'user': 'user', 'pass': 'pass'}
        """
        conn = ('Connection', 'keep-alive')
        ac = ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        ln = ('Accept-Language', 'en-us,en;q=0.5')

        myheaders = [config.USER_AGENT, conn, ac, ln]
        if self.opener is None:
            self.opener = self.createOpener(myheaders)
            urllib2.install_opener(self.opener)
        try:
            if parameters is None:
                response = self.opener.open(url, timeout=config.TIMEOUT)
                self.mycookie = response.headers.get('Set-Cookie')
                data2 = response.read()
                response.close()
                del response
                gc.collect()
                del gc.garbage[:]
                gc.collect()
                return data2
            else:
                response = self.opener.open(url, urllib.urlencode(parameters), timeout=config.TIMEOUT)
                if response is not None:
                    data = response.read()
                    response.close()
                    del response
                    gc.collect()
                    del gc.garbage[:]
                    gc.collect()
                    return data
                else:
                    if retry < config.RETRY_COUNT:
                        time.sleep(5)
                        self.fetchData(url, parameters, retry + 1)
        except Exception, x:
            print x
            self.logger.debug(x)
            if retry < config.RETRY_COUNT:
                time.sleep(5)
                self.fetchData(url, parameters, retry + 1)
        return None

    def createOpener(self, headers=None, handler=None, proxyHandler=None):
        """
        Create opener for fetching data.
        headers = [] Ex. User-agent etc like, [('User-Agent', HEADERS), ....]
        handler = object Ex. Handler like cookie_jar, auth handler etc.
        return opener
        """
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
                                      urllib2.HTTPHandler(debuglevel=0),
                                      urllib2.HTTPSHandler(debuglevel=0))
        if headers is not None:
            opener.addheaders = headers
        if handler is not None:
            opener.add_handler(handler)
        if proxyHandler is not None:
            opener.add_handler(proxyHandler)
        return opener

    def createCookieJarHandler(self):
        """
        Create cookie jar handler. used when keep cookie at login.
        """
        cookieJar = cookielib.LWPCookieJar()
        return urllib2.HTTPCookieProcessor(cookieJar)

    def downloadFile(self, url, downloadPath, proxyHandler=None):
        try:
            regex = Regex()
            opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
                                          urllib2.HTTPHandler(debuglevel=0),
                                          urllib2.HTTPSHandler(debuglevel=0))
            opener.addheaders = [
                config.USER_AGENT,
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Connection', 'keep-alive')]

            if proxyHandler is not None:
                opener.add_handler(proxyHandler)
            resp = urllib2.urlopen(url, timeout=30)
            contentLength = resp.info()['Content-Length']
            contentLength = regex.getSearchedData('(?i)^(\d+)', contentLength)
            totalSize = float(contentLength)
            directory = os.path.dirname(downloadPath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            dl_file = open(downloadPath, 'wb')
            currentSize = 0
            CHUNK_SIZE = 32768
            while True:
                data = resp.read(CHUNK_SIZE)
                if not data:
                    break
                currentSize += len(data)
                dl_file.write(data)

                print('============> ' + str(round(float(currentSize * 100) / totalSize, 2)) + '% of ' + str(
                    totalSize) + ' bytes')
                if currentSize >= totalSize:
                    dl_file.close()
                    return True
        except Exception, x:
            print x

        return False