import sys
import serial
import rrdtool
import re
import commands
import string
import os

retry = 5
data = None
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)

while retry > 0:
    retry -= 1
    
    ser.write("g")
    data = ser.read(25)

    if data != None and len(data) > 0:
        retry += 1
        break

if retry == 0:
    print "read failed"
    exit()

print data
m = re.match("T: (-?\d*\.\d*); H: (\d*\.\d*);", data)
if m:
    ret = rrdtool.update("/srv/http/temp-humid/temp-humid.rrd", "N:" + m.group(1) + ":" + m.group(2))
    if ret:
        print rrdtool.error()
else:
    print "regex fail"

    
#    else:
#        ret = rrdtool.graph("/srv/http/temp-humid/temp-humid.png", "--start", "-1d", "--vertical-label=Temperature F / % Humidity",  "--width=600", "--height=200",
# "DEF:temp=/srv/http/temp-humid/temp-humid.rrd:temperature:AVERAGE",
# "DEF:humid=/srv/http/temp-humid/temp-humid.rrd:humidity:AVERAGE",
# "AREA:humid#ccccff",
# "LINE1:humid#5555ff:Humidity\\r",
# "LINE2:temp#ee2200:Temperature F", 
# "COMMENT:\\r",
# "GPRINT:temp:LAST:Tempature \: %6.2lf %S F",
# "GPRINT:humid:LAST:Humidity \: %6.2lf %S %%\\r")
#        if ret:
#            print rrdtool.error()
 
