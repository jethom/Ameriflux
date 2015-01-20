#!/usr/bin/env python
#
# script to make plots of the profiler data from Willow Creek
#
#----------------------------------------------------------------
import matplotlib
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

runmode = 'OPER'
if runmode == 'TEST':
# file directory
# TEST -------------------------------------------------------------------------------
    datadir = os.path.expanduser("~") + "/Documents/data/LostCreek/"
    datestr = '20140713'
    currenttime = datetime.strptime(datestr,'%Y%m%d')
# TEST -------------------------------------------------------------------------------
else:
# OPERATIONAL ------------------------------------------------------------------------
    matplotlib.use('Agg')
    datadir = "/air/incoming/WillowCreek/"
    currenttime = datetime.now()
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
yesterday = currenttime + timedelta(days=-1)

#-----------------------------------------------------------
figdir = os.path.expanduser("~") + "/public_html/images/willowcreek/profiler"


# clean up the existing figures in the directory
if os.path.exists(figdir + '/irgatp.png'):
    os.remove(figdir + '/irgatp.png')
if os.path.exists(figdir + '/co2.png'):
    os.remove(figdir + '/co2.png')

ft = 'licordata'
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
IDlist=[]

#  make a list of all of the datetime objects
for i in range(len(data)):
    datatimelist.append(data[i][0])
# put the data from each dictionary into a list of lists
for j in datakeys:
    for i in range(len(data)):
        datalist[datakeys.index(j)].append(data[i][1].get(j))         
for i in range(len(data)):
    IDlist.append(data[i][1].get('ID'))
# put the data into a numpy array
dataarray = np.array(datalist, dtype='d')
IDarray = np.array(IDlist, dtype = 'd')
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
qclim['l'] = [1,100]
qclim['valveset'] = [1,10000]
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
qclim['WSpd_80ft_S_WVT'] = [0, 50]
qclim['WDir_80ft_D1_WVT'] = [0, 360]
qclim['WSpd_40ft_S_WVT'] = [0, 50]
qclim['WDir_40ft_D1_WVT'] = [0, 360]
qclim['WSpd_2m_S_WVT'] = [0, 50]
qclim['WDir_2m_D1_WVT'] = [0, 360]
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
#
# Licor Data plots
#
#
values = range(1,11)
fig,ax = plt.subplots()
rbcm = plt.get_cmap('rainbow')
cNorm = colors.Normalize(vmin=1, vmax=values[-1])
scalarMap = cm.ScalarMappable(norm=cNorm, cmap = rbcm)
for i in values:
    timeplot = []
    dataplot = []
    colorVal = scalarMap.to_rgba(values[i-1])
    id_indx = np.nonzero(IDarray==i)[0].tolist()
    labtext = ('%2d'%i)
    for j in id_indx:
        timeplot.append(datatimelist[j]) 
        dataplot.append(dataarray[datakeys.index('avg_CO2')][j])
    plt.plot_date(timeplot,dataplot,color=colorVal,marker='.',label=labtext)
ax.legend(loc='best',fontsize='x-small')

ax.set_xlabel('Time')
ax.set_ylabel('mV')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
plt.title('IRGA CO2 voltage output ' + figdate)
plt.savefig(figdir + '/co2.png', dpi=100)
# plot IRGA pressure and temp
f, axarr = plt.subplots(2,sharex=True)
axarr[0].plot_date(datatimelist,dataarray[datakeys.index('avg_T')],'.',
                xdate=True,ydate=False,label='Avg temp')
axarr[0].set_ylabel('Temp (degC)')
axarr[0].set_title('IRGA temp and pressure ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(datatimelist,dataarray[datakeys.index('avg_P')],'.',
                xdate=True,ydate=False,label='Avg pressure')
axarr[1].set_xlabel('Time')
axarr[1].set_ylabel('hPa')
axarr[1].grid(True)
axarr[1].xaxis.set_major_locator(hrs3)
axarr[1].xaxis.set_major_formatter(hrsfmt)
axarr[1].autoscale_view()
plt.savefig(figdir + '/irgatp.png', dpi=100)
#
#-----------------------------------------------------------------------------------
