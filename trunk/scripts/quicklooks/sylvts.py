#
#
# make daily plots of the lost creek flux calculations
#
#
#-----------------------------------------------------
import matplotlib
import sys
from campbellread import *
import collections
from datetime import datetime, timedelta
from glob import glob

# variables to plot. If variables are similar plot on same figure
plotvars=[["UxCSAT"],["UyCSAT"],["UzCSAT"],["TsCSAT"],["LI7500_CO2"],["LI7500_H2O"],["press_LI7500"]]

# plot title and the name to used to save the figure
plotname=["UxCSAT","UyCSAT","UzCSAT","TsCSAT","diag_CSAT","LI7500_CO2","LI7500_H2O","press_LI7500","diag_LI7500"]

runmode = 'OPER'
if runmode == 'TEST':
# file directory
# TEST -------------------------------------------------------------------------------
    datadir='/Users/jthom/Documents/data/sylvania/2015/'
    figdir='/Users/jthom/public_html/images/sylvania/ts/'
    today=datetime(2015,1,7)
# TEST -------------------------------------------------------------------------------
else:
# OPERATIONAL ------------------------------------------------------------------------
    matplotlib.use('Agg')
    datadir='/air/incoming/sylvania/2015/'
    figdir='/home/jthom/public_html/images/sylvania/ts/'
    today=datetime.now()
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
import numpy as np
import pandas as pd
import xray
from dataread import *
from record2xray import record2xray

# get files for the last two days of data

data=[]
for i in range(2,-1,-1):
    datesearch=today-timedelta(days=i)
    filesearch=datesearch.strftime('*ts_data*%Y_%m_%d*.dat')
    files=glob(datadir + filesearch)
    for fn in files:
        filedata=toa5head(fn) 
        data.extend(filedata) 
    
datax=record2xray(data)
agc=((datax.sel(varname='diag_LI7500').astype('uint8'))&15) * 6.25
# plot the AGC from the LI7500. 
fig,ax=plt.subplots()
agc.transpose().plot(marker='.')
plt.title('LI 7500 AGC')
plt.savefig(figdir + 'agc.png', dpi=100)
plt.close()

for i,xvar in enumerate(plotvars):
    fig,ax=plt.subplots()
    for var in xvar:
        #print var
        try:
            datax.sel(varname=var).plot(marker='.',label=var)
        except:
            print 'error: ',var

    ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
    plt.title(plotname[i])
#    ax.legend(loc='best',fontsize='x-small')
    try:
        plt.savefig(figdir + plotname[i] + '.png', dpi=100)
    except:
        print 'cannot save figure:',plotname[i]
    plt.close(fig)

