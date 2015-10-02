import urllib2
from datetime import datetime, timedelta
from buoyPlot import *

figdir='/Users/jthom/Documents/buoyfigs/'
dateyest = datetime.now() - timedelta(days=3)
#dateyest= datetime.now() - timedelta(days=8)

urlLD=dateyest.strftime('http://metobs.ssec.wisc.edu/pub/cache/mendota/buoy/ascii/v0/00/%Y/%j/MendotaBuoy_limnodata_%Y%m%d.dat')
ldptr=urllib2.urlopen(urlLD)
buoyLimnoPlot(ldptr,figdir)

urlMD=dateyest.strftime('http://metobs.ssec.wisc.edu/pub/cache/mendota/buoy/ascii/v0/00/%Y/%j/MendotaBuoy_metdata_%Y%m%d.dat')
mdptr=urllib2.urlopen(urlMD)
buoyMetPlot(mdptr,figdir)

urlSD=dateyest.strftime('http://metobs.ssec.wisc.edu/pub/cache/mendota/buoy/ascii/v0/00/%Y/%j/MendotaBuoy_system_%Y%m%d.dat')
sdptr=urllib2.urlopen(urlSD)
buoySysPlot(sdptr,figdir)
