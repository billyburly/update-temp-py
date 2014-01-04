import sys
import rrdtool
import re
import commands
import string
import os
import MySQLdb
import telnetlib

host = '10.47.0.80'
retry = 5

data = None
temp = None
humid = None

while retry > 0:
    retry -= 1
    data = None
    
    try:
        tn = telnetlib.Telnet(host)
        tn.write("f")

        data = tn.read_until("\n")
        (temp, humid) = data.rstrip("\n").split(",")
    except:
        print "telnet error"
        data = None

    if data != None and len(data) > 0:
        retry += 1
        break

if data == None:
    print "data request failed"
    exit()

if temp == "-9999":
    temp = ""
if humid == "-9999":
    humid = ""

ret = rrdtool.update("/srv/http/temp-humid/temp-humid.rrd", "N:" + temp + ":" + humid)
if ret:
	print rrdtool.error()

conn = MySQLdb.connect(host="localhost", user="smarthouse", passwd="", db="smarthouse")
cursor = conn.cursor()
try:
	cursor.execute("""INSERT INTO `point_data_float` (`ipid`, `timestamp`, `value`) VALUES (1, NOW(), %s), (2, NOW(), %s)""", (temp, humid))
	conn.commit()
except:
	print "err"
	conn.rollback();
cursor.close()
conn.close()
