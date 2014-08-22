#!/usr/bin/env python
#
# script to make quicklook plots of the trailer data files from WLEF
#
# do not need this for my laptop
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

# plot current day number of days of data
currenttime = datetime.now()
#----------------------------------------------------------------
# will use this for testing
#----------------------------------------------------------------
#datestr = '20140305'
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
figdir = os.path.expanduser("~") + "/public_html/images/wlef/newtrailer"

# clean up the existing figures in the directory
# fast plots
if os.path.exists(figdir + '/co2.png'):
    os.remove(figdir + '/co2.png')
if os.path.exists(figdir + '/h2o.png'):
    os.remove(figdir + '/h2o.png')
if os.path.exists(figdir + '/temp1.png'):
    os.remove(figdir + '/temp1.png')
if os.path.exists(figdir + '/temp2.png'):
    os.remove(figdir + '/temp2.png')
if os.path.exists(figdir + '/pressure.png'):
    os.remove(figdir + '/pressure.png')
#slow plots
if os.path.exists(figdir + '/flow.png'):
    os.remove(figdir + '/flow.png')
if os.path.exists(figdir + '/psi.png'):
    os.remove(figdir + '/psi.png')

# initialize lists to store the files to read
fastfiles = []
slowfiles = []
# find the files that we need
#create directories to look in and make a list of files to read
yesterdaydir = datadir + yesterday.strftime('%Y_%m/%d/*/') 
todaydir = datadir + currenttime.strftime('%Y_%m/%d/*/') 
fastfiles.extend(glob(yesterdaydir + 'newtrailer_fastData_*.dat'))
fastfiles.extend(glob(todaydir + 'newtrailer_fastData_*.dat'))
slowfiles.extend(glob(yesterdaydir + 'newtrailer_diagnostics*.dat'))
slowfiles.extend(glob(todaydir + 'newtrailer_diagnostics*.dat'))
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
# clear some lists
fastfiles[:] = []
slowfiles[:] = []
fastlist[:] = []
slowlist[:] = []

# do some gross error checking
# make qc limits dict
qclim = {}
# fast data qc limits
qclim['top_co2'] = [-5000, 5000]
qclim['mid_co2'] = [-5000, 5000]
qclim['bot_co2'] = [-5000, 5000]
qclim['top_h20'] = [-5000, 5000]
qclim['mid_h20'] = [-5000, 5000]
qclim['bot_h20'] = [-5000, 5000]
qclim['top_p'] = [0, 120]
qclim['mid_p'] = [0, 120]
qclim['bot_p'] = [0, 120]
qclim['top_t'] = [-10, 40]
qclim['mid_t'] = [-10, 40]
qclim['bot_t'] = [-10, 40]
qclim['top_t2'] = [-10, 40]
qclim['mid_t2'] = [-10, 40]
qclim['bot_t2'] = [-10, 40]
qclim['RECORD'] = [0,1]
# slow data qc limits
qclim['top_flow'] = [0, 50]
qclim['mid_flow'] = [0, 50]
qclim['bot_flow'] = [0, 50]
qclim['licorN2'] = [0,3000]
qclim['towerN2'] = [0,3000]

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
# plot co2 voltages
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('top_co2')],'.',
                xdate=True,ydate=False,label='top co2')
axarr[0].set_ylabel('Top voltage')
axarr[0].set_title('Trailer CO2 Licor Voltages ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('mid_co2')],'.',
                xdate=True,ydate=False,label='mid co2')
axarr[1].set_ylabel('Mid voltage')
axarr[1].grid(True)
axarr[2].plot_date(fasttimelist,fastarray[fastkeys.index('bot_co2')],'.',
                xdate=True,ydate=False,label='bot co2')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('Bot voltage')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/co2.png', dpi=100)

# plot h2o voltages
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('top_h20')],'.',
                xdate=True,ydate=False,label='top h2o')
axarr[0].set_ylabel('Top voltage')
axarr[0].set_title('Trailer H2O Licor Voltages ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('mid_h20')],'.',
                xdate=True,ydate=False,label='mid h2o')
axarr[1].set_ylabel('Mid voltage')
axarr[1].grid(True)
axarr[2].plot_date(fasttimelist,fastarray[fastkeys.index('bot_h20')],'.',
                xdate=True,ydate=False,label='bot h2o')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('Bot voltage')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/h2o.png', dpi=100)

# plot pressure hPa
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('top_p')],'.',
                xdate=True,ydate=False,label='top p')
axarr[0].set_ylabel('Top (hPa)')
axarr[0].set_title('Trailer Licor Pressures ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('mid_p')],'.',
                xdate=True,ydate=False,label='mid p')
axarr[1].set_ylabel('Mid (hPa)')
axarr[1].grid(True)
axarr[2].plot_date(fasttimelist,fastarray[fastkeys.index('bot_p')],'.',
                xdate=True,ydate=False,label='bot p')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('Bot (hPa)')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/pressure.png', dpi=100)

# plot temperature 1
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('top_t')],'.',
                xdate=True,ydate=False,label='top t')
axarr[0].set_ylabel('Top (degC)')
axarr[0].set_title('Trailer Licor Temperatures ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('mid_t')],'.',
                xdate=True,ydate=False,label='mid t')
axarr[1].set_ylabel('Mid (degC)')
axarr[1].grid(True)
axarr[2].plot_date(fasttimelist,fastarray[fastkeys.index('bot_t')],'.',
                xdate=True,ydate=False,label='bot t')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('Bot (degC)')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/temp1.png', dpi=100)

# plot temperature 2
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('top_t2')],'.',
                xdate=True,ydate=False,label='top t2')
axarr[0].set_ylabel('Top (degC)')
axarr[0].set_title('Trailer Licor Temperatures 2 ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('mid_t2')],'.',
                xdate=True,ydate=False,label='mid t2')
axarr[1].set_ylabel('Mid (degC)')
axarr[1].grid(True)
axarr[2].plot_date(fasttimelist,fastarray[fastkeys.index('bot_t2')],'.',
                xdate=True,ydate=False,label='bot t2')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('Bot (degC)')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/temp2.png', dpi=100)

#-----------------------------------------------------------------------------
# plot the slow data (diagnostic data)
#-----------------------------------------------------------------------------
# plot flow lpm
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(slowtimelist,slowarray[slowkeys.index('top_flow')],'.',
                xdate=True,ydate=False,label='top flow')
axarr[0].set_ylabel('Top (lpm)')
axarr[0].set_title('Trailer Flow rates ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(slowtimelist,slowarray[slowkeys.index('mid_flow')],'.',
                xdate=True,ydate=False,label='mid flow')
axarr[1].set_ylabel('Mid (lpm)')
axarr[1].grid(True)
axarr[2].plot_date(slowtimelist,slowarray[slowkeys.index('bot_flow')],'.',
                xdate=True,ydate=False,label='bot flow')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('Bot (lpm)')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/flow.png', dpi=100)

# plot N2 tanks levels for licor and tower
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('licorN2')],'.',
             xdate=True,ydate=False,label='Licor N2')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('towerN2')],'g.',
             xdate=True,ydate=False,label='Tower N2')
ax.set_xlabel('Time')
ax.set_ylabel('Tank levels (psi)')
plt.title('N2 Tank Pressures ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/psi.png', dpi=100)
