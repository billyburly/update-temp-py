import sys
import rrdtool
import commands
import string
import os
import MySQLdb
import httplib
import yaml

host = '10.47.0.80'
retry = 5

data = None
itemp = None
ihumid = None

conf = yaml.load(file('update-temp.yml', 'r'), Loader=yaml.CLoader)
if "host" in conf:
    host = conf["host"]
if "retry" in conf:
    retry = conf["retry"]

def calcData(itemp, ihumid):
    temp = int(itemp)
    humid = int(ihumid)

    if(humid != -9999):
       vout = humid / 1023.0
       humid = (vout - 0.16) / 0.0062
    if temp != -9999:
        temp = temp * 0.0625
        if humid != -9999:
            humid = humid / (1.0546 - 0.00216 * temp)
        temp = (temp * 9 / 5) + 32

    return (temp, humid)

while retry > 0:
    retry -= 1
    data = None
    
    try:
        c = httplib.HTTPConnection(host)
        c.request("GET","/")

        resp = c.getresponse().read().splitlines()
        data = {}

        for line in resp:
            line = line.split(':')
            rid = int(line[0])
            (itemp, ihumid) = line[1].split(',')
            data[rid] = { 'itemp': itemp, 'ihumid': ihumid }
    except:
        print "http error"
        data = None

    if data != None and len(data) > 0:
        retry += 1
        break

if data == None:
    print "data request failed"
    exit()

for (i, d) in data.iteritems():
    (temp, humid) = calcData(d['itemp'], d['ihumid'])
    st = str(temp) if temp != -9999 else ""
    sh = str(humid) if humid != -9999 else ""
    dev = conf['idMap'][i]

    ret = rrdtool.update("/srv/http/temp-humid/dev/" + dev + ".rrd", "N:" + st + ":" + sh)
    if ret:
	print rrdtool.error()

    conn = MySQLdb.connect(host="localhost", user="smarthouse", passwd="", db="smarthouse")
    cursor = conn.cursor()
    try:
	cursor.execute("""INSERT INTO `point_data_float` (`ipid`, `timestamp`, `value`) VALUES ((SELECT `ipid` FROM `points` WHERE `pid` = %s), NOW(3), %s), ((SELECT `ipid` FROM `points` WHERE `pid` = %s), NOW(3), %s)""", ("temp." + dev, st, "humid." + dev, sh))
	conn.commit()
    except:
	print "err"
	conn.rollback();
    cursor.close()
    conn.close()
