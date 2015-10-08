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

plotvars=['UST', 'NEE', 'FC', 'SFC', 'H', 'SH','LE','SLE','GPP','RE','ZL','NEEfilled']

runmode = 'OPER'
if runmode == 'TEST':
# file directory
# TEST -------------------------------------------------------------------------------
    figdir='/Users/jthom/public_html/images/sylvania/'
# TEST -------------------------------------------------------------------------------
else:
# OPERATIONAL ------------------------------------------------------------------------
    matplotlib.use('Agg')
    figdir='/home/jthom/public_html/images/sylvania/'
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
import numpy as np
import pandas as pd
import xray
from dataread import *
from record2xray import record2xray

today=datetime.now()
filename=today.strftime('http://flux.aos.wisc.edu/data/sylvania-raw/flux/sylvaniaflux_%Y.txt')

flptr=urllib2.urlopen(filename)


TsliceE=None
TsliceB=None


data=sylv_flux_read(flptr)

flptr.close()

datax=record2xray(data)

# get the last data point and figure out the time slice. 
# can add additional data variables to check if this does not work
for i in range(len(datax)-1,1,-1):
    if not (np.isnan(datax[i].sel(varname='UST')) and np.isnan(datax[i].sel(varname='FC'))):
       TEnd=datax.time[i]
       TBegin= TEnd - np.timedelta64(10,'D') 
       TsliceE=np.datetime_as_string(TEnd)
       TsliceB=np.datetime_as_string(TBegin)
       break

# if you can't find a point just plot the whole year. 
if TsliceE==None and TsliceB==None:
    TsliceE=today.strftime('%Y-%m-%d')
    TsliceB=today.strftime('%Y-01-01')


for var in plotvars:
    fig,ax=plt.subplots()
    datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
    plt.savefig(figdir + var + '.png', dpi=100)
    plt.close()

