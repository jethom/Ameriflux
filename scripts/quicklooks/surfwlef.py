#!/usr/bin/env python
#
# script to make plots of the profiler data from Willow Creek
#
# do not need this for my laptop
#----------------------------------------------------------------
import matplotlib
matplotlib.use('Agg')
#----------------------------------------------------------------
import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta
from glob import glob
from campbellread import toa5head
from campbellread import wlefsurf
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib.dates import HourLocator, DateFormatter

logger = 'surface'
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
figdir = os.path.expanduser("~") + "/public_html/images/wlef/"  + logger + '/'


# clean up the existing figures in the directory
# slow plots
if os.path.exists(figdir + '/temp.png'):
    os.remove(figdir + '/temp.png')
if os.path.exists(figdir + '/pyran.png'):
    os.remove(figdir + '/pyran.png')
if os.path.exists(figdir + '/pressure.png'):
    os.remove(figdir + '/pressure.png')
if os.path.exists(figdir + '/precip.png'):
    os.remove(figdir + '/precip.png')
if os.path.exists(figdir + '/par.png'):
    os.remove(figdir + '/par.png')
if os.path.exists(figdir + '/rh.png'):
    os.remove(figdir + '/rh.png')

# find the files that we need
# ts data
# initialize the lists for storing the data
slowfiles = []
slow = []
slowtimelist = []
#create directories to look in and make a list of files to read
yesterdaydir = datadir + yesterday.strftime('%Y_%m/%d/*/')
#print yesterdaydir
todaydir = datadir + currenttime.strftime('%Y_%m/%d/*/') 
#print todaydir
slowfiles.extend(glob(yesterdaydir + 'surface*.dat'))
slowfiles.extend(glob(todaydir + 'surface*.dat'))
#print slowfiles
# loop through the files and read in the data
for filein in slowfiles:
   filedata = wlefsurf(filein)   
   slow.extend(filedata)
#print slow
# get the keys for the data stored in the dictionaries
slowkeys = slow[0][1].keys()
# make a list of list to put the data in before tranferring it to a numpy array
slowlist = [[] for i in range(len(slowkeys))]

#  make a list of all of the datetime objects
for i in range(len(slow)):
    slowtimelist.append(slow[i][0])
# put the data from each dictionary into a list of lists
for j in slowkeys:
    for i in range(len(slow)):
        slowlist[slowkeys.index(j)].append(slow[i][1].get(j))         
# put the data into a numpy array
slowarray = np.array(slowlist, dtype='d')
# clear tslist 
slowlist[:] = []

# do some gross error checking
# make qc limits dict
qclim = {}
# slow data qc limits
qclim['air_t_AVG'] = [-40, 70]
qclim['pyran_AVG'] = [0, 2000]
qclim['par_AVG'] = [0, 2200]
qclim['atm_p_AVG'] = [80, 120]
qclim['precip_TOT'] = [0, 50]
qclim['rh_AVG'] = [0, 105]

# clean up the data with the qc limits
for j in slowkeys:
    qcarr = np.ma.masked_outside(slowarray[slowkeys.index(j)],qclim[j][0],qclim[j][1])
    qcarr.fill_value = np.nan
    slowarray[slowkeys.index(j)] = qcarr.filled()

# date string for title
figdate = yesterday.strftime('%Y%m%d') + ' - ' + currenttime.strftime('%m%d')

# setup up the plots axes
hrs3 = HourLocator(range(24), interval=3)
hrsfmt = DateFormatter("%H")

# plot met data
# volatage for data logger
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('air_t_AVG')],'.',
             xdate=True,ydate=False,label='Air Temperature')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('Air Temperature ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/temp.png', dpi=100)
# rh
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('rh_AVG')],'.',
             xdate=True,ydate=False,label='RH')
ax.set_xlabel('Time')
ax.set_ylabel('%')
plt.title('Relative Humidity ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/rh.png', dpi=100)
# par
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('par_AVG')],'.',
             xdate=True,ydate=False,label='PAR')
ax.set_xlabel('Time')
ax.set_ylabel('micro mol m^-2 s^-1')
plt.title('PAR ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/par.png', dpi=100)
# Pyranometer
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('pyran_AVG')],'.',
             xdate=True,ydate=False,label='Pyranometer')
ax.set_xlabel('Time')
ax.set_ylabel('W m^-2')
plt.title('Pyranometer ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/pyran.png', dpi=100)
# Pressure
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('atm_p_AVG')],'.',
             xdate=True,ydate=False,label='Pressure')
ax.set_xlabel('Time')
ax.set_ylabel('hPa')
plt.title('Station Pressure ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/pressure.png', dpi=100)
# precip
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('precip_TOT')],'.',
             xdate=True,ydate=False,label='Precip')
ax.set_xlabel('Time')
ax.set_ylabel('mm')
plt.title('Precipitation ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/precip.png', dpi=100)
