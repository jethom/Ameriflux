#!/usr/bin/env python
#
# script to make plots of the ts data files from Lost Creek
#
import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta
from glob import glob
from campbellread import campbellread
import os
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
from matplotlib.dates import HourLocator, DateFormatter

# file directory
datadir = os.path.expanduser("~") + "/Documents/amerifluxdata/"
figdir = os.path.expanduser("~") + "/Documents/amerifluxdata/fig"

# clean up the existing figures in the directory
if os.path.exists(figdir + '/ch4.png'):
    os.remove(figdir + '/ch4.png')
if os.path.exists(figdir + '/co2.png'):
    os.remove(figdir + '/co2.png')
if os.path.exists(figdir + '/h2o.png'):
    os.remove(figdir + '/h2o.png')
if os.path.exists(figdir + '/tempts.png'):
    os.remove(figdir + '/tempts.png')
if os.path.exists(figdir + '/wind.png'):
    os.remove(figdir + '/wind.png')
if os.path.exists(figdir + '/pressureirga.png'):
    os.remove(figdir + '/pressureirga.png')
if os.path.exists(figdir + '/diagnostics.png'):
    os.remove(figdir + '/diagnostics.png')

# plot current day number of days of data
#currenttime = datetime.now()
datestr = '20140218'
currenttime = datetime.strptime(datestr,'%Y%m%d')
# to get the diagnostics file
yesterday = currenttime + timedelta(days=-1)

# find the files that we need
# ts data
# initialize the lists for storing the data
tsfiles = []
ts = []
tstimelist = []
#create directories to look in and make a list of files to read
yesterdaydir = datadir + yesterday.strftime('%Y%m%d')
todaydir = datadir + currenttime.strftime('%Y%m%d')
if not(os.path.exists(todaydir)):
     tsfiles.extend(glob(yesterdaydir + '/*ts*'))
else:
     tsfiles.extend(glob(yesterdaydir + '/*ts*'))
     tsfiles.extend(glob(todaydir + '/*ts*'))
# loop through the files and read in the data
for filein in tsfiles:
   filedata = campbellread(filein)   
   ts.extend(filedata)
# get the keys for the data stored in the dictionaries
tskeys = ts[0][1].keys()
# make a list of list to put the data in before tranferring it to a numpy array
tslist = [[] for i in range(len(tskeys))]
#  make a list of all of the datetime objects
for i in range(len(ts)):
    tstimelist.append(ts[i][0])
# put the data from each dictionary into a list of lists
for j in tskeys:
    for i in range(len(ts)):
        tslist[tskeys.index(j)].append(ts[i][1].get(j))         
# put the data into a numpy array
tsarray = np.array(tslist, dtype='d')
# clear tslist 
tslist[:] = []

#adjust the pressure offset
tsarray[tskeys.index('press_li7700')] = tsarray[tskeys.index('press_li7700')] + 50
tsarray[tskeys.index('press_li7500')] = tsarray[tskeys.index('press_li7500')] + 50

# do some gross error checking
# make qc limits dict
qclim = {}
qclim['co2'] = [-10, 3000]
qclim['Uy'] = [-65, 65]
qclim['Ux'] = [-65, 65]
qclim['Uz'] = [-9, 9]
qclim['Temperature'] = [-40, 70]
qclim['press_li7700'] = [87, 110]
qclim['Ts'] = [-40, 70]
qclim['h2o'] = [0, 40]
qclim['press_li7500'] = [85, 110]
qclim['CH4_density'] = [0, 5]
qclim['RECORD'] = [0, 1]
# put in some dummy limits for diagnostic values
qclim['diag_irga'] = [0, 255]
qclim['diag_csat'] = [0, 65535]
qclim['Diag_li7700'] = [0, 65534]

for j in tskeys:
    qcarr = np.ma.masked_outside(tsarray[tskeys.index(j)],qclim[j][0],qclim[j][1])
    qcarr.fill_value = np.nan
    tsarray[tskeys.index(j)] = qcarr.filled()

# date string for title
figdate = yesterday.strftime('%Y%m%d') + ' - ' + currenttime.strftime('%m%d')

# setup up the plots axes
hrs3 = HourLocator(range(24), interval=3)
hrsfmt = DateFormatter("%H")

#plot wind speeds
fig, ax = plt.subplots()
ax.plot_date(tstimelist,tsarray[tskeys.index('Ux')],'r-',
             xdate=True,ydate=False,label='Ux')
ax.plot_date(tstimelist,tsarray[tskeys.index('Uy')],'b-',
             xdate=True,ydate=False,label='Uy')
ax.plot_date(tstimelist,tsarray[tskeys.index('Uz')],'g-',
             xdate=True,ydate=False,label='Uz')
ax.set_xlabel('Time')
ax.set_ylabel('Wind speed (m/s)')
plt.title('Lost Creek wind speeds ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/wind.png', dpi=100)
# plot sonic temp and LI7700 temps
fig, ax = plt.subplots()
ax.plot_date(tstimelist,tsarray[tskeys.index('Ts')],'-',
             xdate=True,ydate=False,label='Sonic temp')
ax.plot_date(tstimelist,tsarray[tskeys.index('Temperature')],'-',
             xdate=True,ydate=False,label='LI7700 temp')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (deg C)')
plt.title('Temperature ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/tempts.png', dpi=100)
# co2 plot
fig, ax = plt.subplots()
ax.plot_date(tstimelist,tsarray[tskeys.index('co2')],'-',
             xdate=True,ydate=False,label='CO2')
ax.set_xlabel('Time')
ax.set_ylabel('mg/m^3')
plt.title('CO2 ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/co2.png', dpi=100)
# h2o plot
fig, ax = plt.subplots()
ax.plot_date(tstimelist,tsarray[tskeys.index('h2o')],'-',
             xdate=True,ydate=False,label='H2O')
ax.set_xlabel('Time')
ax.set_ylabel('g/m^3')
plt.title('H2O ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/h2o.png', dpi=100)
# ch4 plot
fig, ax = plt.subplots()
ax.plot_date(tstimelist,tsarray[tskeys.index('CH4_density')],'-',
             xdate=True,ydate=False,label='CH4')
ax.set_xlabel('Time')
ax.set_ylabel('mmol/m^3')
plt.title('CH4 ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/ch4.png', dpi=100)
# plot LI7500 and LI7700 pressures
fig, ax = plt.subplots()
#print np.nanmax(tsarray[tskeys.index('press_li7500')])
#print np.nanmin(tsarray[tskeys.index('press_li7500')])
#print np.nanmax(tsarray[tskeys.index('press_li7700')])
#print np.nanmin(tsarray[tskeys.index('press_li7700')])
ax.plot_date(tstimelist,tsarray[tskeys.index('press_li7500')],'-',
             xdate=True,ydate=False,label='LI7500 pres')
ax.plot_date(tstimelist,tsarray[tskeys.index('press_li7700')],'-',
             xdate=True,ydate=False,label='LI7700 pres')
ax.set_xlabel('Time')
ax.set_ylabel('Pressure (kPa)')
plt.title('IRGA Pressures ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/pressureirga.png', dpi=100)
# plot the diagnostics for the csat3, li7500, li7700
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(tstimelist,tsarray[tskeys.index('diag_csat')],'.',
                xdate=True,ydate=False,label='CSAT3 Diag')
axarr[0].set_ylabel('CSAT3')
axarr[0].set_title('Diagnostics for CSAT3, LI7500, and LI7700' + figdate)
axarr[1].plot_date(tstimelist,tsarray[tskeys.index('diag_irga')],'.',
                xdate=True,ydate=False,label='LI7500 Diag')
axarr[1].set_ylabel('LI7500')
axarr[2].plot_date(tstimelist,tsarray[tskeys.index('Diag_li7700')],'.',
                xdate=True,ydate=False,label='LI7700 Diag')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('LI7700')
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/diagnostics.png', dpi=100)
