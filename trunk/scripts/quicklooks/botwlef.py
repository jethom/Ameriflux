#!/usr/bin/env python
#
# script to make quicklook plots of the bot data files from WLEF
#
# do not need this for my lapbot
#----------------------------------------------------------------
import matplotlib
matplotlib.use('Agg')
#----------------------------------------------------------------
#
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
#import pandas as pd
from matplotlib.dates import HourLocator, DateFormatter

logger = 'bot'
# plot current day number of days of data
currenttime = datetime.now()
#----------------------------------------------------------------
# will use this for testing
#----------------------------------------------------------------
#datestr = '20140306'
#currenttime = datetime.strptime(datestr,'%Y%m%d')
#----------------------------------------------------------------
yesterday = currenttime + timedelta(days=-1)
#----------------------------------------------------------------
#-----------------------------------------------------------
# Directories to look for files and write figures
#-----------------------------------------------------------
# test directories
#-----------------------------------------------------------
#datadir = os.path.expanduser("~") + "/Documents/amerifluxdata/wlef/"
#-----------------------------------------------------------
datadir = "/air/incoming/WLEFFlux/Data/"
figdir = os.path.expanduser("~") + "/public_html/images/wlef/" + logger

# clean up the existing figures in the directory
# fast plots
if os.path.exists(figdir + '/co2.png'):
    os.remove(figdir + '/co2.png')
if os.path.exists(figdir + '/h2o.png'):
    os.remove(figdir + '/h2o.png')
if os.path.exists(figdir + '/tempts.png'):
    os.remove(figdir + '/tempts.png')
if os.path.exists(figdir + '/wind.png'):
    os.remove(figdir + '/wind.png')
if os.path.exists(figdir + '/pressure.png'):
    os.remove(figdir + '/pressure.png')
#slow plots
if os.path.exists(figdir + '/flow.png'):
    os.remove(figdir + '/flow.png')
if os.path.exists(figdir + '/rh.png'):
    os.remove(figdir + '/rh.png')
if os.path.exists(figdir + '/tempbot.png'):
    os.remove(figdir + '/tempbot.png')
if os.path.exists(figdir + '/solar.png'):
    os.remove(figdir + '/solar.png')

# initialize lists to store the files to read
fastfiles = []
slowfiles = []
# find the files that we need
#create directories to look in and make a list of files to read
yesterdaydir = datadir + yesterday.strftime('%Y_%m/%d/*/') 
todaydir = datadir + currenttime.strftime('%Y_%m/%d/*/') 
fastfiles.extend(glob(yesterdaydir + logger + '_fast_*.dat'))
fastfiles.extend(glob(todaydir + logger + '_fast_*.dat'))
slowfiles.extend(glob(yesterdaydir + logger + '_slow*.dat'))
slowfiles.extend(glob(todaydir + logger + '_slow*.dat'))

# initialize the lists for storing the data
fast = []
slow = []
fasttimelist = []
slowtimelist = []
# loop through the files and read in the data
for filein in fastfiles:
   filedata = toa5head(filein)   
   fast.extend(filedata)
for filein in slowfiles:
   filedata = toa5head(filein)   
   slow.extend(filedata)
# get the keys for the data stored in the dictionaries
fastkeys = fast[0][1].keys()
slowkeys = slow[0][1].keys()
# make a list of list to put the data in before tranferring it to a numpy array
fastlist = [[] for i in range(len(fastkeys))]
slowlist = [[] for i in range(len(slowkeys))]
#  make a list of all of the datetime objects
for i in range(len(fast)):
    fasttimelist.append(fast[i][0])
for i in range(len(slow)):
    slowtimelist.append(slow[i][0])
# put the data from each dictionary into a list of lists
for j in fastkeys:
    for i in range(len(fast)):
        fastlist[fastkeys.index(j)].append(fast[i][1].get(j))         
for j in slowkeys:
    for i in range(len(slow)):
        slowlist[slowkeys.index(j)].append(slow[i][1].get(j))         
# put the data into a numpy array
fastarray = np.array(fastlist, dtype='d')
slowarray = np.array(slowlist, dtype='d')
# divide the sonic values by 100 to get the decimal place in the correct location
fastarray[fastkeys.index('t')] = fastarray[fastkeys.index('t')]/100
fastarray[fastkeys.index('u')] = fastarray[fastkeys.index('u')]/100
fastarray[fastkeys.index('v')] = fastarray[fastkeys.index('v')]/100
fastarray[fastkeys.index('w')] = fastarray[fastkeys.index('w')]/100
# clear some lists
fastfiles[:] = []
slowfiles[:] = []
fastlist[:] = []
slowlist[:] = []

# do some gross error checking
# make qc limits dict
qclim = {}
# fast data qc limits
qclim['co2'] = [-5000, 5000]
qclim['h2o'] = [-5000, 5000]
qclim['sample_p'] = [0, 120]
qclim['sample_t'] = [-10, 40]
qclim['u'] = [-30, 30]
qclim['v'] = [-30, 30]
qclim['w'] = [-30, 30]
qclim['t'] = [-30, 60]
qclim['li_t'] = [-30, 40]
qclim['RECORD'] = [0,1]
# slow data qc limits
qclim['solar_in_Avg'] = [0, 2000]
qclim['rh_hmp_Avg'] = [0, 110]
qclim['t_hmp_Avg'] = [-40, 50]
qclim['reflected_Avg'] = [0,3000]
qclim['sflow_Avg'] = [0,30]
qclim['rflow_Avg'] = [0,30]

# clean up the data with the qc limits
for j in fastkeys:
    qcarr = np.ma.masked_outside(fastarray[fastkeys.index(j)],qclim[j][0],qclim[j][1])
    qcarr.fill_value = np.nan
    fastarray[fastkeys.index(j)] = qcarr.filled()
for j in slowkeys:
    qcarr = np.ma.masked_outside(slowarray[slowkeys.index(j)],qclim[j][0],qclim[j][1])
    qcarr.fill_value = np.nan
    slowarray[slowkeys.index(j)] = qcarr.filled()

# date string for title
figdate = yesterday.strftime('%Y%m%d') + ' - ' + currenttime.strftime('%m%d')

# setup up the plots axes
hrs3 = HourLocator(range(24), interval=3)
hrsfmt = DateFormatter("%H")

# plot the fast data 
# plot bot wind
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('u')],'.',
                xdate=True,ydate=False,label='u')
axarr[0].set_ylabel('u (m/s)')
axarr[0].set_title('Bot wind speed ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('v')],'.',
                xdate=True,ydate=False,label='v')
axarr[1].set_ylabel('v (m/s)')
axarr[1].grid(True)
axarr[2].plot_date(fasttimelist,fastarray[fastkeys.index('w')],'.',
                xdate=True,ydate=False,label='w')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('w (m/s)')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/wind.png', dpi=100)

# plot temps
fig, ax = plt.subplots()
ax.plot_date(fasttimelist,fastarray[fastkeys.index('t')],'.',
             xdate=True,ydate=False,label='Sonic temp')
#ax.plot_date(fasttimelist,fastarray[fastkeys.index('li_t')],'r.',
             #xdate=True,ydate=False,label='Licor temp')
#ax.plot_date(fasttimelist,fastarray[fastkeys.index('sample_t')],'g.',
             #xdate=True,ydate=False,label='Sample temp')
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
#fig, ax = plt.subplots()
#ax.plot_date(fasttimelist,fastarray[fastkeys.index('co2')],'.',
             #xdate=True,ydate=False,label='CO2')
#ax.set_xlabel('Time')
#ax.set_ylabel('mV')
#plt.title('CO2 Voltage ' + figdate)
#ax.xaxis.set_major_locator(hrs3)
#ax.xaxis.set_major_formatter(hrsfmt)
#ax.autoscale_view()
#ax.grid(True)
#plt.savefig(figdir + '/co2.png', dpi=100)
# h2o plot
#fig, ax = plt.subplots()
#ax.plot_date(fasttimelist,fastarray[fastkeys.index('h2o')],'.',
             #xdate=True,ydate=False,label='H2O')
#ax.set_xlabel('Time')
#ax.set_ylabel('mV')
#plt.title('H2O Voltage' + figdate)
#ax.xaxis.set_major_locator(hrs3)
#ax.xaxis.set_major_formatter(hrsfmt)
#ax.autoscale_view()
#ax.grid(True)
#plt.savefig(figdir + '/h2o.png', dpi=100)
# plot sample pressure
#fig, ax = plt.subplots()
#ax.plot_date(fasttimelist,fastarray[fastkeys.index('sample_p')],'.',
             #xdate=True,ydate=False,label='sample pressure')
#ax.set_xlabel('Time')
#ax.set_ylabel('Pressure (kPa)')
#plt.title('Sample Pressure ' + figdate)
#ax.xaxis.set_major_locator(hrs3)
#ax.xaxis.set_major_formatter(hrsfmt)
#ax.autoscale_view()
#ax.grid(True)
#plt.savefig(figdir + '/pressure.png', dpi=100)

#-----------------------------------------------------------------------------
# plot the slow data (diagnostic data)
#-----------------------------------------------------------------------------
# plot flow lpm
#f, axarr = plt.subplots(2, sharex=True)
#axarr[0].plot_date(slowtimelist,slowarray[slowkeys.index('rflow_Avg')],'.',
                #xdate=True,ydate=False,label='rflow avg')
#axarr[0].set_ylabel('RFlow (lpm)')
#axarr[0].set_title('Bot Flow rates ' + figdate)
#axarr[0].grid(True)
#axarr[1].plot_date(slowtimelist,slowarray[slowkeys.index('sflow_Avg')],'.',
                #xdate=True,ydate=False,label='sflow avg')
#axarr[1].set_ylabel('SFlow (lpm)')
#axarr[1].grid(True)
#axarr[1].set_xlabel('Time')
#axarr[1].grid(True)
#axarr[1].xaxis.set_major_locator(hrs3)
#axarr[1].xaxis.set_major_formatter(hrsfmt)
#axarr[1].autoscale_view()
#plt.savefig(figdir + '/flow.png', dpi=100)
# RH
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('rh_hmp_Avg')],'.',
             xdate=True,ydate=False,label='RH')
ax.set_xlabel('Time')
ax.set_ylabel('%')
plt.title('Bot Relative Humidity ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/rh.png', dpi=100)
# hmp temp
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('t_hmp_Avg')],'.',
             xdate=True,ydate=False,label='Temp')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('Bot Temperature ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/tempbot.png', dpi=100)
# plot solar in and reflected
#fig, ax = plt.subplots()
#ax.plot_date(slowtimelist,slowarray[slowkeys.index('solar_in_Avg')],'.',
             #xdate=True,ydate=False,label='solar in')
#ax.plot_date(slowtimelist,slowarray[slowkeys.index('reflected_Avg')],'g.',
             #xdate=True,ydate=False,label='reflected')
#ax.set_xlabel('Time')
#ax.set_ylabel('W m^-2')
#plt.title('Solar and reflected ' + figdate)
#ax.legend(loc='best',fontsize='x-small')
#ax.xaxis.set_major_locator(hrs3)
#ax.xaxis.set_major_formatter(hrsfmt)
#ax.autoscale_view()
#ax.grid(True)
#plt.savefig(figdir + '/solar.png', dpi=100)
