import sys
import rrdtool

ret = rrdtool.create("/srv/http/temp-humid/temp-humid.rrd", "--step", "300", "--start", "0",
 "DS:temperature:GAUGE:600:40:120",
 "DS:humidity:GAUGE:600:0:100",
 "RRA:AVERAGE:0.5:1:600",
 "RRA:AVERAGE:0.5:6:700",
 "RRA:AVERAGE:0.5:24:775",
 "RRA:AVERAGE:0.5:288:797",
 "RRA:MAX:0.5:1:600",
 "RRA:MAX:0.5:6:700",
 "RRA:MAX:0.5:24:775",
 "RRA:MAX:0.5:288:797")

if ret:
    print rrdtool.error()
