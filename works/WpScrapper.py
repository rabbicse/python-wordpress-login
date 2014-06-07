__author__ = 'Rabbi'

from logs.LogManager import LogManager
from utils.Utils import Utils
from spiders.Spider import Spider
from utils.Regex import Regex
from bs4 import BeautifulSoup
import csv


class WpScrapper():
    def __init__(self, input_file, output_file):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.input_file = input_file
        self.output_file = output_file

    def scrapData(self):
        csv_writer = csv.writer(open(self.output_file, 'wb'), delimiter=';')
        with open(self.input_file, 'rb') as csvfile:
            csv_rows = csv.reader(csvfile, delimiter=';')
            rows = list(csv_rows)
            total = len(rows)
            counter = 0
            for row in rows:
                counter += 1
                print '---------------- Checking [%d] of [%d] records. ----------------------' % (counter, total)
                self.logger.debug('Checking %d of %d records.' % (counter, total))
                domain = 'http://' + row[0] + '/wp-login.php'
                https_domain = 'https://' + row[0] + '/wp-login.php'
                wp_admin = 'http://' + row[0] + '/wp-admin/'
                https_wp_admin = 'https://' + row[0] + '/wp-admin/'
                username = row[1]
                password = row[2]
                status = 0
                print 'Login Credential => Domain: ' + domain + ' User: ' + username + ' Password: ' + password
                self.logger.debug('Login Credential => Domain: ' + domain + ' User: ' + username + ' Password: ' + password)
                if self.onLogin(domain, https_domain, wp_admin, https_wp_admin, username, password) is True:
                    print 'Successfully logged in.'
                    self.logger.debug('Successfully logged in.')
                    status = 1
                else:
                    print 'Login failed!'
                    self.logger.debug('Login failed!')
                csv_writer.writerow([row[0], username, password, status])
                print '---------------- End of checking [%d] of [%d] records. ----------------------' % (counter, total)
                print '\n\n'


    def onLogin(self, url, https_url, wp_url, https_wp_url, username, password):
        '''
        Credentials are:
        action	login_access
        i
        p
        password	sdfsdf
        username	sdfsdf
        '''
        try:
            loginCredentials = {'log': username,
                                'pwd': password,
                                'redirect_to': wp_url}
            print 'Credentials', loginCredentials
            print 'Please wait...Try to login with your credentials.'
            redirected_url, loginData = self.spider.login(url, loginCredentials)
            print 'redirected url: ', redirected_url
            if loginData and len(loginData) > 0:
                loginData = self.regex.reduceNewLine(loginData)
                loginData = self.regex.reduceBlankSpace(loginData)
                print 'After login data: ', loginData
            if redirected_url is not None and redirected_url.strip() == wp_url.strip(): return True

            # if loginData and len(loginData) > 0:
            #     loginData = self.regex.reduceNewLine(loginData)
            #     loginData = self.regex.reduceBlankSpace(loginData)
            # soup = BeautifulSoup(loginData)
            # if soup.find('div', {'id': 'login_error'}):
            #     return False
            # else:
            #     return True
        except Exception, x:
            print x
            print 'There was an error when login with http'

        try:
            https_loginCredentials = {'log': username,
                                      'pwd': password,
                                      'redirect_to': https_wp_url}
            print 'Credentials', https_loginCredentials
            print 'Please wait...Try to login with your credentials.'
            https_redirected_url, https_login_data = self.spider.login(https_url, https_loginCredentials)
            if https_redirected_url is not None and https_redirected_url.strip() == https_wp_url.strip(): return True
        except Exception, x:
            print x
            print 'There was an error when login with https'
        return False