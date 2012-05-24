import sys
import serial
import rrdtool
import re
import commands
import string
import os

#running = commands.getoutput("ps aux | grep -v grep | grep update-temp")
#if len(running) > 0:
#    for instance in string.split(running,"\n"):
#        instance = string.split(instance)
#        print "|" + instance[1] + "|"
#        print "|" + str(os.getpid()) + "|"
#        if instance[1] != str(os.getpid()):
#            print "hi"
#            k = commands.getoutput("kill " + instance[1])

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
ser.write("g")
data = ser.read(25)
print data
m = re.match("T: (-?\d*\.\d*); H: (\d*\.\d*);", data)
if m:
    ret = rrdtool.update("/srv/http/temp-humid/temp-humid.rrd", "N:" + m.group(1) + ":" + m.group(2))
    if ret:
        print rrdtool.error()
#    else:
#        print "success"
else:
    print "regex fail"
    print data
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
 
