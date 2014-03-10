update-temp.py
==============

Grabs temperature/humidity data from arduino via http. 

Install
-------
1. Use make-rrd.py to create the rrd database
2. Run update-temp.py via cron every 5 minutes to grab latest data:
`*/5 * * * * python2 /path/to/update-temp.py -f /path/to/conf.yml`