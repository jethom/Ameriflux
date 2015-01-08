#!/usr/bin/env python
#
# script to make plots of the ts data files from Lost Creek
#
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
#import pandas as pd
runmode = 'OPER'
if runmode == 'TEST':
# file directory
# TEST -------------------------------------------------------------------------------
    #datadir = os.path.expanduser("~") + "/Documents/amerifluxdata/"
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

# directory where figures are stored
figdir = os.path.expanduser("~") + "/public_html/images/lostcreek"

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
if os.path.exists(figdir + '/SS7500.png'):
    os.remove(figdir + '/SS7500.png')

# find the files that we need
# ts data
# initialize the lists for storing the data
tsfiles = []
ts = []
tstimelist = []
#create directories to look in and make a list of files to read
yesterdaydir = datadir + yesterday.strftime('%Y%m%d')
todaydir = datadir + currenttime.strftime('%Y%m%d')
tsfiles.extend(glob(yesterdaydir + '/*ts*'))
tsfiles.extend(glob(todaydir + '/*ts*'))
# loop through the files and read in the data
for filein in tsfiles:
   filedata = toa5head(filein)   
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
qclim['RECORD'] = [0,1]
# put in some dummy limits for diagnostic values
qclim['diag_irga'] = [0, 255]
qclim['diag_csat'] = [0, 65534]
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
#fig, ax = plt.subplots()
#ax.plot_date(tstimelist,tsarray[tskeys.index('Ux')],'r.',
             #xdate=True,ydate=False,label='Ux')
#ax.plot_date(tstimelist,tsarray[tskeys.index('Uy')],'b.',
             #xdate=True,ydate=False,label='Uy')
#ax.plot_date(tstimelist,tsarray[tskeys.index('Uz')],'g.',
             #xdate=True,ydate=False,label='Uz')
#ax.set_xlabel('Time')
#ax.set_ylabel('Wind speed (m/s)')
#plt.title('Lost Creek wind speeds ' + figdate)
#ax.legend(loc='best',fontsize='x-small')
#ax.xaxis.set_major_locator(hrs3)
#ax.xaxis.set_major_formatter(hrsfmt)
#ax.autoscale_view()
#ax.grid(True)
#plt.savefig(figdir + '/wind.png', dpi=100)
# plot 3-d winds
f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot_date(tstimelist,tsarray[tskeys.index('Ux')],'.',
                xdate=True,ydate=False,label='Ux')
axarr[0].set_ylabel('Ux (m/s)')
axarr[0].set_title('CSAT3 Wind ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(tstimelist,tsarray[tskeys.index('Uy')],'.',
                xdate=True,ydate=False,label='Uy')
axarr[1].set_ylabel('Uy (m/s)')
axarr[1].grid(True)
axarr[2].plot_date(tstimelist,tsarray[tskeys.index('Uz')],'.',
                xdate=True,ydate=False,label='Uz')
axarr[2].set_xlabel('Time')
axarr[2].set_ylabel('Uz (m/s)')
axarr[2].grid(True)
axarr[2].xaxis.set_major_locator(hrs3)
axarr[2].xaxis.set_major_formatter(hrsfmt)
axarr[2].autoscale_view()
plt.savefig(figdir + '/wind.png', dpi=100)
# plot sonic temp and LI7700 temps
fig, ax = plt.subplots()
ax.plot_date(tstimelist,tsarray[tskeys.index('Ts')],'.',
             xdate=True,ydate=False,label='Sonic temp')
ax.plot_date(tstimelist,tsarray[tskeys.index('Temperature')],'.',
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
ax.plot_date(tstimelist,tsarray[tskeys.index('co2')],'.',
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
ax.plot_date(tstimelist,tsarray[tskeys.index('h2o')],'.',
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
ax.plot_date(tstimelist,tsarray[tskeys.index('CH4_density')],'.',
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
ax.plot_date(tstimelist,tsarray[tskeys.index('press_li7500')],'.',
             xdate=True,ydate=False,label='LI7500 pres')
ax.plot_date(tstimelist,tsarray[tskeys.index('press_li7700')],'g.',
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

# make more meaningful values for the diagnositcs
# plot the diagnostics for the csat3, li7500, li7700
diag_irga = tsarray[tskeys.index('diag_irga')]
# for now: change the diagnostic value back to its default value (this may change in the future)
for i in range(len(diag_irga)):
    diag_irga[i]=(int(diag_irga[i]) ^ 240)
# LI7500 diaganostics
ss_7500 = [0] * len(diag_irga)   # signal strength
chopper = [0] * len(diag_irga)
detect = [0] * len(diag_irga)
PLL = [0] * len(diag_irga)
sync = [0] * len(diag_irga)
for i in range(len(diag_irga)):
   ss_7500[i]=((int(diag_irga[i]) & 15) * 6.67)
   chopper[i]=(int(diag_irga[i]) & 128) >> 7
   detect[i]=(int(diag_irga[i]) & 64) >> 6
   PLL[i]=(int(diag_irga[i]) & 32) >> 5
   sync[i]=(int(diag_irga[i]) & 16) >> 4
ss_7500=np.array(ss_7500,dtype='float')
# li7500 signal strength plot
fig, ax = plt.subplots()
ax.plot_date(tstimelist,ss_7500,'.',
             xdate=True,ydate=False,label='SS_7500')
ax.set_xlabel('Time')
ax.set_ylabel('Signal Strength')
plt.title('LI7500 Signal Strength (0-100) ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/SS7500.png', dpi=100)
# CSAT 3 diagnostics
csat_diag=tsarray[tskeys.index('diag_csat')]
#61502 : anemometer does not respond
#61440 : lost trigger
#61503 : no data available
#61551 : SDM Comms error
#61442 : Wrong CSAT3 embedded code
ux_range = [0] *len(csat_diag)
uy_range = [0] *len(csat_diag)
uz_range = [0] *len(csat_diag)
counter = [0] *len(csat_diag)
b15 = [0] *len(csat_diag) 
b14 = [0] *len(csat_diag)
b13 = [0] *len(csat_diag)
b12 = [0] *len(csat_diag)
for i in range(len(csat_diag)):
    counter[i] = int(csat_diag[i]) & 63
    uz_range[i]=(int(csat_diag[i])&192) >> 6
    uy_range[i]=(int(csat_diag[i])&768) >> 8
    ux_range[i]=(int(csat_diag[i])&3072) >> 10
    b12[i]=(int(csat_diag[i])&4096) >> 12
    b13[i]=(int(csat_diag[i])&8192) >> 13
    b14[i]=(int(csat_diag[i])&16384) >> 14
    b15[i]=(int(csat_diag[i])&32768) >> 15
# LI7700 diagnostics
diag_7700 = tsarray[tskeys.index('Diag_li7700')]
#32768 : not ready 2**15
#16384 : nosignal 2**14
#8192 : refunlocked 2**13
#4096 : badtemp 2**12
#2048 : lasertempunregulated 2**11
#1024 : blocktempunregulated 2**10
#512 : motorspinning 2**9
#256 : pumpon 2**8
#128 : topHeateron 2**7
#64 : bottomheateron 2**6
#32 : calibrating 2**5
#16 : motorfailure 2**4
#8 : badauxtc1 2**3
#4 : badauxtc2 2**2
#2 : badauxtc3 2**1
#1 : boxconnected (li-7550 attached) 2**0

