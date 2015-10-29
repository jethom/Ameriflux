import urllib2
from datetime import datetime, timedelta
from buoyPlot import *

figdir='/home/jthom/public_html/images/buoy/'
dateyest = datetime.now()
#dateyest = datetime.now() - timedelta(days=1)
#dateyest= datetime.now() - timedelta(days=8)

urlLD=dateyest.strftime('http://metobs.ssec.wisc.edu/pub/cache/mendota/buoy/ascii/v0/00/%Y/%j/MendotaBuoy_limnodata_%Y%m%d.dat')

try:
    ldptr=urllib2.urlopen(urlLD)
    buoyLimnoPlot(ldptr,figdir)
except:
    print 'buoy Limnological file does not exist: ' + urlLD

urlMD=dateyest.strftime('http://metobs.ssec.wisc.edu/pub/cache/mendota/buoy/ascii/v0/00/%Y/%j/MendotaBuoy_metdata_%Y%m%d.dat')

try:
    mdptr=urllib2.urlopen(urlMD)
    buoyMetPlot(mdptr,figdir)
except:
    print 'buoy meteorology file does not exist: ' + urlMD

urlSD=dateyest.strftime('http://metobs.ssec.wisc.edu/pub/cache/mendota/buoy/ascii/v0/00/%Y/%j/MendotaBuoy_system_%Y%m%d.dat')

try:
    sdptr=urllib2.urlopen(urlSD)
    buoySysPlot(sdptr,figdir)
except:
    print 'buoy system file does not exist: ' + urlSD
