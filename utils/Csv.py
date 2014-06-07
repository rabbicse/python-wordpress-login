from logs.LogManager import LogManager

__author__ = 'Rabbi'

import csv

class Csv:
    def __init__(self, fileName=None):
        self.logger = LogManager(__name__)
        if fileName is not None:
            self.writer = csv.writer(open(fileName, 'ab'))

    def writeCsvRow(self, data):
        try:
            self.writer.writerow(data)
        except Exception, x:
            self.logger.error(x)

    def readCsvRow(self, fileName, rowIndex=-1):
        rows = []
        try:
            reader = csv.reader(open(fileName, 'rb'))
            if rowIndex > -1:
                for row in reader:
                    rows.append(row[rowIndex])
            else:
                for row in reader:
                    rows.append(row)

        except Exception, x:
            self.logger.error(x)
        return rows
