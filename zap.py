
from zapv2 import ZAPv2
from pprint import pprint
import sqlite3
import time
import sys
import re
import time


conn = sqlite3.connect('running.db')
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS running (id integer primary key autoincrement, app text, status text)''')
conn.commit()

if len(sys.argv) is not 2:
    print('Too short arguments.')
    sys.exit(1)
target = sys.argv[1]
name = 'report_{}.{}'.format(target.replace(
    'http://', '').replace('https://', '').replace('/', ''), time.time())
print("generating report {}".format(name))
query = u"INSERT INTO running (app, status) VALUES(?,?)"
print(query)
c.execute(query, (name, ''))
conn.commit()


zap = ZAPv2(proxies={'http': 'http://localhost:8080'},
            apikey="SupriseMotherFucker")
zap.urlopen(target)
scanid = zap.spider.scan(target)
time.sleep(2)


print('Spidering target %s' % name)
while (int(zap.spider.status(scanid)) < 100):
    status = u"Spider progress: {}% ".format(zap.spider.status(scanid))
    print(status)
    c.execute("UPDATE running SET status = ? WHERE app like ?", (status, name))
    conn.commit()
    print(status)

    time.sleep(2)
print('Spider completed')

# Give the passive scanner a chance to finish
time.sleep(5)


print('Scanning target %s' % name)
scanid = zap.ascan.scan(target)
while (int(zap.ascan.status(scanid)) < 100):
    status = 'Scan progress %:{} '.format(zap.ascan.status(scanid))
    c.execute("UPDATE running SET status = ? WHERE app like ?", (status, name))
    conn.commit()

    print(status)
    time.sleep(5)


print('Hosts: ' + ', '.join(zap.core.hosts))
pprint(zap.core.alerts())
html = zap.core.htmlreport()
with open('templates/reports/' + name + '.html', 'a') as f:
    f.write(html)


status = "Scan completed"
c.execute("UPDATE running SET status = ? WHERE app like ?", (status, name))
conn.commit()
conn.close()
print(status)  # Report the results
