import getopt
import sys
from works.WpScrapper import WpScrapper

__author__ = 'Rabbi'


if __name__ == "__main__":
    spider = WpScrapper(sys.argv[1], sys.argv[2])
    spider.scrapData()

