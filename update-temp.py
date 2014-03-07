import sys
import rrdtool
import re
import commands
import string
import os
import MySQLdb
import httplib

host = '10.47.0.80'
retry = 5

data = None
itemp = None
ihumid = None

while retry > 0:
    retry -= 1
    data = None
    
    try:
        tn = telnetlib.Telnet(host)
        tn.write("f")

        data = tn.read_until("\n")
        (temp, humid) = data.rstrip("\n").split(",")
    except:
        print "http error"
        data = None

    if data != None and len(data) > 0:
        retry += 1
        break

if data == None:
    print "data request failed"
    exit()
    
temp = int(itemp)
humid = int(ihumid)

temp = temp * 0.0625
vout = humid / 1023.0
humid = (vout - 0.16) / 0.0062
if itemp != "-9999":
    humid = humid / (1.0546 - 0.00216 * temp)
temp = (temp * 9 / 5) + 32

if itemp == "-9999":
    temp = ""
else:
    temp = str(temp)
humid = str(humid)
    
ret = rrdtool.update("/srv/http/temp-humid/temp-humid.rrd", "N:" + temp + ":" + humid)
if ret:
	print rrdtool.error()

if itemp == "-9999":
    temp = itemp
    
conn = MySQLdb.connect(host="localhost", user="smarthouse", passwd="", db="smarthouse")
cursor = conn.cursor()
try:
	cursor.execute("""INSERT INTO `point_data_float` (`ipid`, `timestamp`, `value`) VALUES (1, NOW(3), %s), (2, NOW(3), %s)""", (temp, humid))
	conn.commit()
except:
	print "err"
	conn.rollback();
cursor.close()
conn.close()
