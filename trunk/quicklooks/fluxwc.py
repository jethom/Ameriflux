#!/usr/bin/env python
#
# script to make plots of the flux data files from Willow Creek
#
# do not need this for my laptop
#----------------------------------------------------------------
#import matplotlib
#matplotlib.use('Agg')
#----------------------------------------------------------------
#
import matplotlib
matplotlib.use('Agg')
import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta
from glob import glob
from campbellread import campbellread
from campbellreadEL import wcflux
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
#datestr = '20140220'
#currenttime = datetime.strptime(datestr,'%Y%m%d')
#----------------------------------------------------------------
yesterday = currenttime + timedelta(days=-1)
#----------------------------------------------------------------
#-----------------------------------------------------------
# Directories to look for files and write figures
#-----------------------------------------------------------
# test directories
#-----------------------------------------------------------
#datadir = os.path.expanduser("~") + "/Documents/amerifluxdata/willowcreek/flux/"
#-----------------------------------------------------------
datadir = "/data/incoming/WillowCreek/current/flux/"
figdir = os.path.expanduser("~") + "/public_html/images/willowcreek/flux"

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
if os.path.exists(figdir + '/pressureirga.png'):
    os.remove(figdir + '/pressureirga.png')
if os.path.exists(figdir + '/diagnostics.png'):
    os.remove(figdir + '/diagnostics.png')
#slow plots
if os.path.exists(figdir + '/temps.png'):
    os.remove(figdir + '/temps.png')
if os.path.exists(figdir + '/sw.png'):
    os.remove(figdir + '/sw.png')
if os.path.exists(figdir + '/lw.png'):
    os.remove(figdir + '/lw.png')
if os.path.exists(figdir + '/rh.png'):
    os.remove(figdir + '/rh.png')
if os.path.exists(figdir + '/pressure.png'):
    os.remove(figdir + '/pressure.png')
if os.path.exists(figdir + '/battvolt.png'):
    os.remove(figdir + '/battvolt.png')
if os.path.exists(figdir + '/swinstd.png'):
    os.remove(figdir + '/swinstd.png')
if os.path.exists(figdir + '/leaf.png'):
    os.remove(figdir + '/leaf.png')

# find the files that we need
# ts data
# initialize the lists for storing the data
fastfiles = []
slowfiles = []
fast = []
slow = []
fasttimelist = []
slowtimelist = []
#create directories to look in and make a list of files to read
yesterdaydir = datadir + yesterday.strftime('%Y%m%d')
todaydir = datadir + currenttime.strftime('%Y%m%d')
fastfiles.extend(glob(yesterdaydir + '*/*1.dat'))
fastfiles.extend(glob(todaydir + '*/*1.dat'))
slowfiles.extend(glob(yesterdaydir + '*/*2.dat'))
slowfiles.extend(glob(todaydir + '*/*2.dat'))
# loop through the files and read in the data
for filein in fastfiles:
   filedata = wcflux(filein)   
   fast.extend(filedata)
for filein in slowfiles:
   filedata = wcflux(filein)   
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
# clear tslist 
fastlist[:] = []
slowlist[:] = []

# do some gross error checking
# make qc limits dict
qclim = {}
# fast data qc limits
qclim['co2'] = [-5000, 5000]
qclim['Uy'] = [-65, 65]
qclim['Ux'] = [-65, 65]
qclim['Uz'] = [-9, 9]
qclim['LI_P'] = [87, 110]
qclim['LI_T'] = [-40, 70]
qclim['Ts'] = [-40, 70]
qclim['h2o'] = [-5000, 5000]
qclim['RECORD'] = [0,1]
qclim['diag_csat'] = [0, 65534]
# slow data qc limits
qclim['RTD_T_AVG'] = [-40, 70]
qclim['Atm_P'] = [950,1040]
qclim['RH'] = [0, 100]
qclim['Solar_In_AVG'] = [0, 1500]
qclim['Solar_Out_AVG'] = [0, 1000]
qclim['IR_In_AVG'] = [-150, 100]
qclim['IR_Out_AVG'] = [-150, 100]
qclim['KZ_T_AVG'] = [-40, 70]
qclim['Battery'] = [0, 20]
qclim['Leaf_Wet'] = [0, 99999]
qclim['Solar_In_STD'] = [0, 10]

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
# plot 3-d winds
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('Ux')],'.',
                xdate=True,ydate=False,label='Ux')
axarr[0].set_ylabel('Ux (m/s)')
axarr[0].set_title('CSAT3 Wind ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('Uy')],'.',
                xdate=True,ydate=False,label='Uy')
axarr[1].set_ylabel('Uy (m/s)')
axarr[1].grid(True)
axarr[2].plot_date(fasttimelist,fastarray[fastkeys.index('Uz')],'.',
                xdate=True,ydate=False,label='Uz')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('Uz (m/s)')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/wind.png', dpi=100)

# plot sonic temp 
fig, ax = plt.subplots()
ax.plot_date(fasttimelist,fastarray[fastkeys.index('Ts')],'.',
             xdate=True,ydate=False,label='Sonic temp')
ax.plot_date(fasttimelist,fastarray[fastkeys.index('LI_T')],'.',
             xdate=True,ydate=False,label='LI6262 temp')
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
ax.plot_date(fasttimelist,fastarray[fastkeys.index('co2')],'.',
             xdate=True,ydate=False,label='CO2')
ax.set_xlabel('Time')
ax.set_ylabel('mV')
plt.title('CO2 Voltage ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/co2.png', dpi=100)
# h2o plot
fig, ax = plt.subplots()
ax.plot_date(fasttimelist,fastarray[fastkeys.index('h2o')],'.',
             xdate=True,ydate=False,label='H2O')
ax.set_xlabel('Time')
ax.set_ylabel('mV')
plt.title('H2O Voltage' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/h2o.png', dpi=100)
# plot LI 6262 pressure
fig, ax = plt.subplots()
ax.plot_date(fasttimelist,fastarray[fastkeys.index('LI_P')],'.',
             xdate=True,ydate=False,label='LI6262 pres')
ax.set_xlabel('Time')
ax.set_ylabel('Pressure (kPa)')
plt.title('IRGA Pressures ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/pressureirga.png', dpi=100)
# plot CSAT Diagnostic
fig, ax = plt.subplots()
ax.plot_date(fasttimelist,fastarray[fastkeys.index('diag_csat')],'.',
             xdate=True,ydate=False,label='csat3 diag')
ax.set_xlabel('Time')
ax.set_ylabel('Diag')
plt.title('CSAT3 Diagnostic ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/diagnostics.png', dpi=100)
#-----------------------------------------------------------------------------
# plot slow data
#-----------------------------------------------------------------------------
# plot temp 
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RTD_T_AVG')],'.',
             xdate=True,ydate=False,label='Air temp')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('KZ_T_AVG')],'.',
             xdate=True,ydate=False,label='CNR1 temp')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (deg C)')
plt.title('Temperature ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/temps.png', dpi=100)
# plot SW radiation 
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('Solar_In_AVG')],'.',
             xdate=True,ydate=False,label='Downwelling')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('Solar_Out_AVG')],'.',
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
# plot LW radiation 
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('IR_In_AVG')],'.',
             xdate=True,ydate=False,label='Downwelling')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('IR_Out_AVG')],'.',
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
# plot RH radiation 
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH')],'.',
             xdate=True,ydate=False,label='RH')
ax.set_xlabel('Time')
ax.set_ylabel('%')
plt.title('Relative Humidity ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/rh.png', dpi=100)
# plot atmopsheric pressure
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('Atm_P')],'.',
             xdate=True,ydate=False,label='Air pressure (MSLP)')
ax.set_xlabel('Time')
ax.set_ylabel('hPA')
plt.title('Mean Sea Level Pressure (estimate) ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/pressure.png', dpi=100)
# plot  battery voltage
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('Battery')],'.',
             xdate=True,ydate=False,label='Battery Voltage')
ax.set_xlabel('Time')
ax.set_ylabel('Volts')
plt.title('Battery Voltage at Flux Box ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/battvolt.png', dpi=100)
# plot  solar in STD
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('Solar_In_STD')],'.',
             xdate=True,ydate=False,label='Solar In STD')
ax.set_xlabel('Time')
plt.title('STD of Short Wave downwelling ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/swinstd.png', dpi=100)
# plot leaf wetness
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('Leaf_Wet')],'.',
             xdate=True,ydate=False,label='Leaf Wetness')
ax.set_xlabel('Time')
plt.title('Leaf Wetness Indicator ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/leaf.png', dpi=100)
