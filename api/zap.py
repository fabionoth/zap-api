from zapv2 import ZAPv2
from pprint import pprint
from database import Database
import sqlite3
import time
import sys
import re
import time



class Zap:
    ZAP_URL_HTTP = 'http://localhost:8080'
    API_KEY = 'SupriseMotherFucker'
    

    def __init__(self, target, debug=False):
        self.__debug = debug
        self.__target = target

        if not self.__is_valid_url(target):
            raise Exception("Not valid url")
        self.__name = 'report_{}.{}'.format(self.__target.replace(
            'http://', '').replace('https://', '').replace('/', ''), time.time())

        if self.__debug:
            print("DEBUG: target -> {}".format(self.__target))
            print("DEBUG: name -> {}".format(self.__name))

    def run(self):
        zap = ZAPv2(proxies={'http': self.ZAP_URL_HTTP}, apikey=self.API_KEY)
        zap.urlopen(self.__target)
        status = "Starting Analysys: target -> {}".format(self.__target)
        self.__update_database_status(status)
        if self.__debug:
            print(status)
        self.__spider(zap)
        self.__scanning(zap)
        self.__generate_report(zap)

    def __spider(self, zap):
        scanid = zap.spider.scan(self.__target)
        status = "Spidering: target -> {}".format(self.__target)
        if self.__debug:
            print(status)
        
        self.__update_database_status(status)
        time.sleep(2)

        while(int(zap.spider.status(scanid)) < 100):
            status = u"Spider progress: {}% ".format(zap.spider.status(scanid))
            if self.__debug:
                print(status)
            self.__update_database_status(status)
            time.sleep(5)

    def __scanning(self, zap):
        scanid = zap.ascan.scan(self.__target)
        status = "Scanning: target -> {}".format(self.__target)
        self.__update_database_status(status)
        time.sleep(2)
        if self.__debug:
            print(status)
        
        while (int(zap.ascan.status(scanid)) < 100):
            status = 'Scan Progress progress %:{} '.format(zap.ascan.status(scanid))
            self.__update_database_status(status)
            if self.__debug:
                print(status)
            time.sleep(5)

    def __generate_report(self, zap):
        pprint(zap.core.alerts())
        html = zap.core.htmlreport()
        with open('templates/reports/' + self.__name + '.html', 'a') as f:
            f.write(html)
        self.__update_database_status("Report done")

        

    def __update_database_status(self, status):
        d = Database(debug=self.__debug)
        d.update_status(name = self.__name, status=status)
        d.__exit__()

    @property
    def name(self):
        return self.__name

    @property
    def target(self):
        return self.__target

    def __is_valid_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url)
