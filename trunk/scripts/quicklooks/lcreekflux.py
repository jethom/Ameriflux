#
#
# make daily plots of the lost creek flux calculations
#
#
#-----------------------------------------------------
import matplotlib
import sys
import collections
from datetime import datetime, timedelta
import urllib2
from dataread import flux_read

plotvars=['cflux', 'qflux', 'tflux', 'ch4flux', 'cstor', 'qstor', 'tstor', 'ch4stor','NEE_CO2', 'LE', 'H', 'NEE_CH4', 'u*']
runmode = 'OPER'
if runmode == 'TEST':
# file directory
# TEST -------------------------------------------------------------------------------
    figdir='/Users/jthom/public_html/images/lostcreek/'
# TEST -------------------------------------------------------------------------------
else:
# OPERATIONAL ------------------------------------------------------------------------
    matplotlib.use('Agg')
    figdir='/home/jthom/public_html/images/lostcreek/'
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xray
from record2xray import record2xray

today=datetime.now()
tminus5=today-timedelta(5)

TsliceE=today.strftime('%Y-%m-%d')
TsliceB=tminus5.strftime('%Y-%m-%d')

filename=today.strftime('http://flux.aos.wisc.edu/data/lcreek-raw/%Y/flux/lcreek%Y_flux.txt')
flptr=urllib2.urlopen(filename)

data=flux_read(flptr)

flptr.close()

datax=record2xray(data)
for var in plotvars:
    datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    plt.savefig(figdir + var + '.png', dpi=100)
    plt.close()
