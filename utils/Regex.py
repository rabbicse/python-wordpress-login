__author__ = 'Rabbi'

import re


class Regex:
    def __init__(self):
        pass

    def reduceNewLine(self, data):
        data = re.sub('(?i)\n+', ' ', data)
        return data

    def reduceBlankSpace(self, data):
        data = re.sub('(?i)\s+', ' ', data)
        return data

    def reduceNbsp(self, data):
        data = re.sub('(?i)&nbsp;', '', data)
        return data

    def getAllSearchedData(self, pattern, data):
        return re.findall(pattern, data)

    def getSearchedData(self, pattern, data):
        try:
            searchedData = re.search(pattern, data)
            if searchedData:
                return searchedData.group(1)
        except Exception, x:
            print x
        return ''

    def getSearchedDataGroups(self, pattern, data):
        return re.search(pattern, data)

    def isFoundPattern(self, pattern, data):
        try:
            matchedData = re.search(pattern, data)
            if matchedData:
                return True
        except Exception, x:
            print x
        return False

    def replaceData(self, pattern, replace, data):
        return re.sub(pattern, replace, data)


