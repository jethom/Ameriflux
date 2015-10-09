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

plotvarsflux=['Cflux_30', 'Cstor_30', 'NEE_30', 'LE_30', 'H_30', 'u*']
plotvarsmet=['CO2_2','CO2_5','CO2_10','CO2_25','CO2_45','CO2_70','CO2_97']

runmode = 'OPER'
if runmode == 'TEST':
# file directory
# TEST -------------------------------------------------------------------------------
    figdir='/Users/jthom/public_html/images/willowcreek/'
# TEST -------------------------------------------------------------------------------
else:
# OPERATIONAL ------------------------------------------------------------------------
    matplotlib.use('Agg')
    figdir='/home/jthom/public_html/images/willowcreek/'
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
import numpy as np
import pandas as pd
import xray
from dataread import *
from record2xray import record2xray

today=datetime.now()
tminus5=today-timedelta(5)

TsliceE=today.strftime('%Y-%m-%d')
TsliceB=tminus5.strftime('%Y-%m-%d')

filename=today.strftime('http://flux.aos.wisc.edu/data/wcreek-raw/flux/wcreek%Y_flux.txt')
flptr=urllib2.urlopen(filename)

data=wc_flux_read(flptr)

flptr.close()

datax=record2xray(data)
for var in plotvarsflux:
    fig,ax=plt.subplots()
    datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
    plt.savefig(figdir + var + '.png', dpi=100)
    plt.close()

# read the met file
filename=today.strftime('http://flux.aos.wisc.edu/data/wcreek-raw/flux/wcreek%Y_met.txt')
flptr=urllib2.urlopen(filename)
data=wc_met_read(flptr)
flptr.close()
datax=record2xray(data)
fig,ax=plt.subplots()
for var in plotvarsmet:
    datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.',label=var)
plt.legend(loc='best')
plt.title('CO2 Profile')
ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
plt.savefig(figdir + 'CO2profile.png', dpi=100)
plt.close()

for var in plotvarsmet:
    fig,ax=plt.subplots()
    datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
    plt.savefig(figdir + var + '.png', dpi=100)
    plt.close()

