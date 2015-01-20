#!/usr/bin/env python

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
    datadir = "/air/incoming/LostCreek/"
    currenttime = datetime.now()
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
yesterday = currenttime + timedelta(days=-1)

# file directory
#datadir = os.path.expanduser("~") + "/Documents/amerifluxdata/"
datadir = "/air/incoming/LostCreek/"
figdir = os.path.expanduser("~") + "/public_html/images/lostcreek"

# clean up the existing figures in the directory
if os.path.exists(figdir + '/battvolt.png'):
    os.remove(figdir + '/battvolt.png')
if os.path.exists(figdir + '/temps.png'):
    os.remove(figdir + '/temps.png')
if os.path.exists(figdir + '/rh.png'):
    os.remove(figdir + '/rh.png')
if os.path.exists(figdir + '/pressure.png'):
    os.remove(figdir + '/pressure.png')
if os.path.exists(figdir + '/lw.png'):
    os.remove(figdir + '/lw.png')
if os.path.exists(figdir + '/sw.png'):
    os.remove(figdir + '/sw.png')
if os.path.exists(figdir + '/par.png'):
    os.remove(figdir + '/par.png')
if os.path.exists(figdir + '/rain.png'):
    os.remove(figdir + '/rain.png')
if os.path.exists(figdir + '/water.png'):
    os.remove(figdir + '/water.png')

# find the files that we need
# met data
# initialize the lists for storing the data
metfiles = []
met = []
mettimelist = []
#create directories to look in
yesterdaydir = datadir + yesterday.strftime('%Y%m%d')
todaydir = datadir + currenttime.strftime('%Y%m%d')
metfiles.extend(glob(yesterdaydir + '/*met*'))
metfiles.extend(glob(todaydir + '/*met*'))
for filein in metfiles:
   filedata = toa5head(filein)   
   met.extend(filedata)
metkeys = met[0][1].keys()
metlist = [[] for i in range(len(metkeys))]

# put met data into a list of lists
for i in range(len(met)):
    mettimelist.append(met[i][0])
for j in metkeys:
    for i in range(len(met)):
        metlist[metkeys.index(j)].append(met[i][1].get(j))         

# put the data into a numpy array
metarray = np.array(metlist, dtype='d')
#adjust the pressure offset
metarray[metkeys.index('atmpres_Avg')] = metarray[metkeys.index('atmpres_Avg')] + 500
#
#  need to do some gross error checks on the data
# make a limits dict
qclim = {}
qclim['LW_up_Avg'] = [-150, 100]
qclim['batt_volt_Avg'] = [0, 20]
qclim['PAR_Den_Avg'] = [0, 2300]
qclim['panel_temp_Avg'] = [-40, 70]
qclim['Water_Temp_C_Avg'] = [-2, 30]
qclim['SW_up_Avg'] = [0, 1000]
qclim['rain_mm_Tot'] = [0, 10]
qclim['airTC_Avg'] = [-40, 70]
qclim['atmpres_Avg'] = [800, 1100]
qclim['RH_Avg'] = [0, 100]
qclim['Level_Avg'] = [0, 8]
qclim['LW_down_Avg'] = [-150,100]
qclim['cnr4_T_C_Avg'] = [-40, 70]
qclim['SW_down_Avg'] = [0, 1500]
qclim['RECORD'] = [0,1]
for j in metkeys:
#    print j,metkeys.index(j), qclim[j][0],qclim[j][1]
    qcarr = np.ma.masked_outside(metarray[metkeys.index(j)],qclim[j][0],qclim[j][1])
    qcarr.fill_value = np.nan
    metarray[metkeys.index(j)] = qcarr.filled() 


# date string for plot title
figdate = yesterday.strftime('%Y%m%d') + ' - ' + currenttime.strftime('%m%d')
# setup up the plots axes
hrs3 = HourLocator(range(24), interval=3)
hrsfmt = DateFormatter("%H")
# plot shortwave radiation
#plt.figure(1)
fig, ax = plt.subplots()
ax.plot_date(mettimelist,metarray[metkeys.index('SW_down_Avg')],'.',
             xdate=True,ydate=False,label='Downwelling')
ax.plot_date(mettimelist,metarray[metkeys.index('SW_up_Avg')],'g.',
             xdate=True,ydate=False,label='Upwelling')
ax.set_xlabel('Time')
ax.set_ylabel('W m^-2')
plt.title('Short Wave Radiation ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/sw.png', dpi=100)
# plot longwave radiation
#plt.figure(2)
fig, ax = plt.subplots()
ax.plot_date(mettimelist,metarray[metkeys.index('LW_down_Avg')],'.',
             xdate=True,ydate=False,label='Downwelling')
ax.plot_date(mettimelist,metarray[metkeys.index('LW_up_Avg')],'g.',
             xdate=True,ydate=False,label='Upwelling')
ax.set_xlabel('Time')
ax.set_ylabel('W m^-2')
plt.title('Long Wave Radiation ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/lw.png', dpi=100)
# plot PAR
#plt.figure(3)
fig, ax = plt.subplots()
ax.plot_date(mettimelist,metarray[metkeys.index('PAR_Den_Avg')],'.',
             xdate=True,ydate=False,label='PAR Density')
ax.set_xlabel('Time')
ax.set_ylabel('micro-mol s^-1 m^-2')
plt.title('PAR Density ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/par.png', dpi=100)
# plot RH
#plt.figure(4)
fig, ax = plt.subplots()
ax.plot_date(mettimelist,metarray[metkeys.index('RH_Avg')],'.',
             xdate=True,ydate=False,label='Relavtive Humidity')
ax.set_xlabel('Time')
ax.set_ylabel('%')
plt.title('Relative Humidity ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/rh.png', dpi=100)
# plot temperatures measured at station
#plt.figure(5)
fig, ax = plt.subplots()
ax.plot_date(mettimelist,metarray[metkeys.index('airTC_Avg')],'r.',
             xdate=True,ydate=False,label='Air Temperature')
ax.plot_date(mettimelist,metarray[metkeys.index('panel_temp_Avg')],'b.',
             xdate=True,ydate=False,label='Enclosure Temperature')
ax.plot_date(mettimelist,metarray[metkeys.index('cnr4_T_C_Avg')],'g.',
             xdate=True,ydate=False,label='CNR4 Temp')
ax.set_xlabel('Time')
ax.set_ylabel('deg C')
plt.title('Lost Creek Temperatures ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/temps.png', dpi=100)
# plot battery voltage
#plt.figure(6)
fig, ax = plt.subplots()
ax.plot_date(mettimelist,metarray[metkeys.index('batt_volt_Avg')],'.',
             xdate=True,ydate=False,label='Battery Voltage')
ax.set_xlabel('Time')
ax.set_ylabel('volts')
plt.title('Battery Voltage ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/battvolt.png', dpi=100)
#plot rain total
fig, ax = plt.subplots()
ax.plot_date(mettimelist,metarray[metkeys.index('rain_mm_Tot')],'.',
             xdate=True,ydate=False,label='rain total')
ax.set_xlabel('Time')
ax.set_ylabel('mm')
plt.title('Rain total ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/rain.png', dpi=100)
#plot water level and temp
# if water level's first field is nan then set to 0
if np.isnan(metarray[10][0]):
    metarray[10][0]=0
fig, ax1 = plt.subplots()
ax1.plot_date(mettimelist,metarray[metkeys.index('Level_Avg')],'b.',
              xdate=True,ydate=False,label='water level')
ax1.set_ylabel('water level (psi)', color = 'b')
for t1 in ax1.get_yticklabels():
    t1.set_color('b')
plt.title('Water Level and Temperature ' + figdate)
ax1.xaxis.set_major_locator(hrs3)
ax1.xaxis.set_major_formatter(hrsfmt)
ax1.autoscale_view()
ax2 = ax1.twinx()
ax2.plot_date(mettimelist,metarray[metkeys.index('Water_Temp_C_Avg')],'r.',
              xdate=True,ydate=False,label='Water Temp')
ax2.set_ylabel('water temp (deg C)', color='r')
for t1 in ax2.get_yticklabels():
    t1.set_color('r')
ax2.autoscale_view()
plt.savefig(figdir + '/water.png', dpi=100)
#plot pressure 
fig, ax = plt.subplots()
ax.plot_date(mettimelist,metarray[metkeys.index('atmpres_Avg')],'.',
             xdate=True,ydate=False,label='Pressure')
ax.set_xlabel('Time')
ax.set_ylabel('Pressure (mb)')
plt.title('Station Pressure ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/pressure.png', dpi=100)

