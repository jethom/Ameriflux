import urllib2
from datetime import datetime, timedelta
from buoyPlot import *

dateyest = datetime.now() - timedelta(days=1)


urlLD=dateyest.strftime('http://metobs.ssec.wisc.edu/pub/cache/mendota/buoy/ascii/v0/00/%Y/%j/MendotaBuoy_limnodata_%Y%m%d.dat')
ldptr=urllib2.urlopen(urlLD)
buoyLimnoPlot(ldptr)

urlMD=dateyest.strftime('http://metobs.ssec.wisc.edu/pub/cache/mendota/buoy/ascii/v0/00/%Y/%j/MendotaBuoy_metdata_%Y%m%d.dat')
mdptr=urllib2.urlopen(urlMD)
buoyMetPlot(mdptr)
