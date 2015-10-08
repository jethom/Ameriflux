#
#
# make daily plots of the WLEF flux calculations
#
#
#-----------------------------------------------------
import matplotlib
import sys
import collections
from datetime import datetime, timedelta
import urllib2

# file names/url links
#http://flux.aos.wisc.edu/data/cheas/wlef/flux/prelim/2015/diagch4_2015.txt
vardiagch4=['Cflx_122','Cstor_122','CH4flx_122','CH4stor_122']
#http://flux.aos.wisc.edu/data/cheas/wlef/flux/prelim/2015/diag_2015.txt
vardiag=['Cstor_30','Cstor_122','Cstor_396','Qstor_30','Qstor_122','Qstor_396','Tstor_30','Tstor_122','Tstor_396','Hflx_30','Hflx_122','Hflx_396','Mflx_30','Mflx_122','Mflx_396','Qflx_30','Qflx_122','Qflx_396','Qflx_122i','Qflx_396i','Cflx_30','Cflx_122','Cflx_396','Cflx_122i','Cflx_396i']
#http://flux.aos.wisc.edu/data/wlef/ch4/profile/lefch4_2015.txt
varlefch4=['CO2_122_p','CH4_122_p','CH4_30','CH4_122','CH4_396','CO2_30','CO2_122','CO2_396','CO2_30_N','CO2_122_N','CO2_396_N']


runmode = 'OPER'
if runmode == 'TEST':
# file directory
# TEST -------------------------------------------------------------------------------
    figdir='/Users/jthom/public_html/images/wlef/'
# TEST -------------------------------------------------------------------------------
else:
# OPERATIONAL ------------------------------------------------------------------------
    matplotlib.use('Agg')
    figdir='/home/jthom/public_html/images/wlef/flux/'
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
import numpy as np
import pandas as pd
from dataread import *
import xray
from record2xray import record2xray

today=datetime.now()-timedelta(1)

tminusx=today-timedelta(10)

TsliceE=today.strftime('%Y-%m-%d')
TsliceB=tminusx.strftime('%Y-%m-%d')

#http://flux.aos.wisc.edu/data/cheas/wlef/flux/prelim/2015/diag_2015.txt
filename=today.strftime('http://flux.aos.wisc.edu/data/cheas/wlef/flux/prelim/%Y/diag_%Y.txt')
flptr=urllib2.urlopen(filename)

data=wlef_flux_read(flptr)

flptr.close()

datax=record2xray(data)
for var in vardiag:
 #   print var
    fig,ax=plt.subplots()
    try:
        datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    except:
        plt.plot_date(datax.time.sel(time=slice(TsliceB,TsliceE)),datax.sel(varname=var, time=slice(TsliceB,TsliceE)),'-.')
    ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
    plt.savefig(figdir + var + '.png', dpi=100)
    plt.close()

#http://flux.aos.wisc.edu/data/cheas/wlef/flux/prelim/2015/diagch4_2015.txt
filename=today.strftime('http://flux.aos.wisc.edu/data/cheas/wlef/flux/prelim/%Y/diagch4_%Y.txt')

flptr=urllib2.urlopen(filename)
data=wlef_flux_read(flptr)
# print len(data)
flptr.close()
datax=record2xray(data)
for var in vardiagch4:
  #   print var
    fig,ax=plt.subplots()
    try:
        datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    except:
        plt.plot_date(datax.time.sel(time=slice(TsliceB,TsliceE)),datax.sel(varname=var, time=slice(TsliceB,TsliceE)),'-.')
   # datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
    plt.savefig(figdir + var + '_2.png', dpi=100)
    plt.close()

#http://flux.aos.wisc.edu/data/wlef/ch4/profile/lefch4_2015.txt
filename=today.strftime('http://flux.aos.wisc.edu/data/wlef/ch4/profile/lefch4_%Y.txt')


flptr=urllib2.urlopen(filename)
data=noaa_wlef_read(flptr)
# print len(data)
flptr.close()
datax=record2xray(data)
for var in varlefch4:
#    print var
    fig,ax=plt.subplots()
    try:
        datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    except:
        plt.plot_date(datax.time.sel(time=slice(TsliceB,TsliceE)),datax.sel(varname=var, time=slice(TsliceB,TsliceE)),'-.')
   # datax.sel(varname=var, time=slice(TsliceB, TsliceE)).plot(marker='.')
    ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
    plt.savefig(figdir + var + '.png', dpi=100)
    plt.close()

