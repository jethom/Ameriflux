#!/usr/bin/env python
#
# script to make plots of the profiler data from Willow Creek
#
# do not need this for my laptop
#----------------------------------------------------------------
#import matplotlib
#matplotlib.use('Agg')
#----------------------------------------------------------------
import matplotlib
matplotlib.use('Agg')
import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta
from glob import glob
from campbellread import toa5head
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
#import pandas as pd
from matplotlib.dates import HourLocator, DateFormatter

# plot current day number of days of data
currenttime = datetime.now()
#----------------------------------------------------------------
# will use this for testing
#----------------------------------------------------------------
#datestr = '20140828'
#currenttime = datetime.strptime(datestr,'%Y%m%d')
#----------------------------------------------------------------
yesterday = currenttime + timedelta(days=-1)
#----------------------------------------------------------------

#-----------------------------------------------------------
# Directories to look for files and write figures
#-----------------------------------------------------------
# test directories
#-----------------------------------------------------------
#datadir = os.path.expanduser("~") + "/Documents/dev/dailyView/data/"
#figdir = os.path.expanduser("~") + "/Documents/amerifluxdata/willowcreek/images/profiler"
#-----------------------------------------------------------
datadir = "/air/incoming/WillowCreek/"
figdir = os.path.expanduser("~") + "/public_html/images/willowcreek/profiler"


# clean up the existing figures in the directory
if os.path.exists(figdir + '/oldairt.png'):
    os.remove(figdir + '/oldairt.png')
if os.path.exists(figdir + '/oldrh.png'):
    os.remove(figdir + '/oldrh.png')

ft = 'oldsensors' # 'oldsensors','profileDiag']
# find the files that we need
# ts data
# initialize the lists for storing the data
files = []
data = []
datatimelist = []

#create directories to look in and make a list of files to read
yesterdaydir = datadir + yesterday.strftime('%Y%m%d')
todaydir = datadir + currenttime.strftime('%Y%m%d')

# create list of files that will be read
#licor table
files.extend(glob(yesterdaydir + '/*/Profiler_' + ft + '*.dat'))
files.extend(glob(todaydir + '/*/Profiler_' + ft + '*.dat'))

# loop through the files and read in the data
for filein in files:
   #print filein
   datain = toa5head(filein)   
   data.extend(datain)
# get the keys for the data stored in the dictionaries
datakeys = data[0][1].keys()
# make a list of list to put the data in before tranferring it to a numpy array
datalist = [[] for i in range(len(datakeys))]

#  make a list of all of the datetime objects
for i in range(len(data)):
    datatimelist.append(data[i][0])
# put the data from each dictionary into a list of lists
for j in datakeys:
    for i in range(len(data)):
        datalist[datakeys.index(j)].append(data[i][1].get(j))         
# put the data into a numpy array
dataarray = np.array(datalist, dtype='d')
# clear tslist 
datalist[:] = []

# do some gross error checking
# make qc limits dict
qclim = {}
# licordata qc limits
qclim['ID'] = [1, 11]
qclim['avg_T'] = [-40, 70]
qclim['avg_P'] = [0, 110]
qclim['avg_CO2'] = [-2500, 2500]
qclim['RECORD'] = [0, "inf"]
qclim['level'] = [1, 92]
# Diag data qc limits
qclim['batt_volt'] = [0, 20]
qclim['battery_direct'] = [0, 20]
qclim['PTemp'] = [-40, 70]
qclim['flux'] = [0, 3000]
qclim['hightank'] = [0, 3000]
qclim['lowtank'] = [0, 3000]
qclim['nafion'] = [0, 3000]
qclim['reftank'] = [0, 3000]
# metdata qc limits
qclim['AirT_200'] = [-40, 70]
qclim['AirT_100'] = [-40, 70]
qclim['AirT_75'] = [-40, 70]
qclim['AirT_50'] = [-40, 70]
qclim['AirT_25'] = [-40, 70]
qclim['SoilT_0'] = [-40, 70]
qclim['SoilT_5'] = [-40, 70]
qclim['SoilT_10'] = [-40, 70]
qclim['SoilT_20'] = [-40, 70]
qclim['SoilT_50'] = [-40, 70]
qclim['SoilT_100'] = [-40, 70]
qclim['TreeT_N'] = [-20, 50]
qclim['TreeT_S'] = [-20, 50]
qclim['Heatflux'] = [-1000, 1000]
qclim['SoilW_5'] = [0, 100]
qclim['SoilW_10'] = [0, 100]
qclim['SoilW_20'] = [0, 100]
qclim['SoilW_50'] = [0, 100]
qclim['SoilW_100'] = [0, 100]
qclim['PAR_60ft_Avg'] = [0, 2200]
qclim['PAR_40ft_Avg'] = [0, 2200]
qclim['PAR_25ft_Avg'] = [0, 2200]
qclim['PAR_2m_Avg'] = [0, 2200]
qclim['WSpd_80ft_WVc(1)'] = [0, 50]
qclim['WDir_80ft_WVc(2)'] = [0, 360]
qclim['WSpd_60ft_WVc(1)'] = [0, 50]
qclim['WDir_60ft_WVc(2)'] = [0, 360]
qclim['WSpd_40ft_WVc(1)'] = [0, 50]
qclim['WDir_40ft_WVc(2)'] = [0, 360]
qclim['WSpd_25ft_WVc(1)'] = [0, 50]
qclim['WDir_25ft_WVc(2)'] = [0, 360]
qclim['WSpd_2m_WVc(1)'] = [0, 50]
qclim['WDir_2m_WVc(2)'] = [0, 360]
qclim['AirT_80ft_Avg'] = [-40, 70]
qclim['AirT_60ft_Avg'] = [-40, 70]
qclim['AirT_40ft_Avg'] = [-40, 70]
qclim['AirT_25ft_Avg'] = [-40, 70]
qclim['AirT_2m_Avg'] = [-40, 70]
qclim['RH_80ft_Avg'] = [0, 105]
qclim['RH_60ft_Avg'] = [0, 105]
qclim['RH_40ft_Avg'] = [0, 105]
qclim['RH_25ft_Avg'] = [0, 105]
qclim['RH_2m_Avg'] = [0, 105]
qclim['NRad_Cs_Avg'] = [-2000, 2000]
qclim['NRad_Cd_Avg'] = [-2000, 2000]
# oldsensor qc limits
qclim['oldAirT2_Avg'] = [-40, 70]
qclim['oldAirT25_Avg'] = [-40, 70]
qclim['oldAirT40_Avg'] = [-40, 70]
qclim['oldAirT60_Avg'] = [-40, 70]
qclim['oldAirT80_Avg'] = [-40, 70]
qclim['oldRH2_Avg'] = [0, 105]
qclim['oldRH25_Avg'] = [0, 105]
qclim['oldRH40_Avg'] = [0, 105]
qclim['oldRH60_Avg'] = [0, 105]
qclim['oldRH80_Avg'] = [0, 105]

# clean up the data with the qc limits
for j in datakeys:
    qcarr = np.ma.masked_outside(dataarray[datakeys.index(j)],qclim[j][0],qclim[j][1])
    qcarr.fill_value = np.nan
    dataarray[datakeys.index(j)] = qcarr.filled()

# date string for title
figdate = yesterday.strftime('%Y%m%d') + ' - ' + currenttime.strftime('%m%d')

# setup up the plots axes
hrs3 = HourLocator(range(24), interval=3)
hrsfmt = DateFormatter("%H")

#-----------------------------------------------------------------------------------
# AirT_80ft - AirT_2m
fig, ax = plt.subplots()
ax.plot_date(datatimelist,dataarray[datakeys.index('oldAirT80_Avg')],'b.',
             xdate=True,ydate=False,label='AirT 80ft')
ax.plot_date(datatimelist,dataarray[datakeys.index('oldAirT60_Avg')],'r.',
             xdate=True,ydate=False,label='AirT 60ft')
ax.plot_date(datatimelist,dataarray[datakeys.index('oldAirT40_Avg')],'g.',
             xdate=True,ydate=False,label='AirT 40ft')
ax.plot_date(datatimelist,dataarray[datakeys.index('oldAirT25_Avg')],'m.',
             xdate=True,ydate=False,label='AirT 25ft')
ax.plot_date(datatimelist,dataarray[datakeys.index('oldAirT2_Avg')],'k.',
             xdate=True,ydate=False,label='AirT 2m')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('Old AirT_80ft - AirT_2m ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.legend(loc='best',fontsize='x-small')
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/oldairt.png', dpi=100)
# RH_80ft - RH_2m
fig, ax = plt.subplots()
ax.plot_date(datatimelist,dataarray[datakeys.index('oldRH80_Avg')],'b.',
             xdate=True,ydate=False,label='RH 80ft')
ax.plot_date(datatimelist,dataarray[datakeys.index('oldRH60_Avg')],'r.',
             xdate=True,ydate=False,label='RH 60ft')
ax.plot_date(datatimelist,dataarray[datakeys.index('oldRH40_Avg')],'g.',
             xdate=True,ydate=False,label='RH 40ft')
ax.plot_date(datatimelist,dataarray[datakeys.index('oldRH25_Avg')],'m.',
             xdate=True,ydate=False,label='RH 25ft')
ax.plot_date(datatimelist,dataarray[datakeys.index('oldRH2_Avg')],'k.',
             xdate=True,ydate=False,label='RH 2m')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('Old RH_80ft - RH_2m ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.legend(loc='best',fontsize='x-small')
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/oldrh.png', dpi=100)
