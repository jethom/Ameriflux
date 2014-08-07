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
from campbellread import campbellread
from campbellreadEL import wcprofile
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
#datadir = os.path.expanduser("~") + "/Documents/amerifluxdata/willowcreek/profiler/"
#figdir = os.path.expanduser("~") + "/Documents/amerifluxdata/willowcreek/images/profiler"
#-----------------------------------------------------------
datadir = "/air/incoming/WillowCreek/profiler/"
figdir = os.path.expanduser("~") + "/public_html/images/willowcreek/profiler"


# clean up the existing figures in the directory
# fast plots
if os.path.exists(figdir + '/irgatp.png'):
    os.remove(figdir + '/irgatp.png')
if os.path.exists(figdir + '/co2.png'):
    os.remove(figdir + '/co2.png')
# slow plots
if os.path.exists(figdir + '/battvolt.png'):
    os.remove(figdir + '/battvolt.png')
if os.path.exists(figdir + '/airtlow.png'):
    os.remove(figdir + '/airtlow.png')
if os.path.exists(figdir + '/soilt.png'):
    os.remove(figdir + '/soilt.png')
if os.path.exists(figdir + '/soilw.png'):
    os.remove(figdir + '/soilw.png')
if os.path.exists(figdir + '/treet.png'):
    os.remove(figdir + '/treet.png')
if os.path.exists(figdir + '/heatflux.png'):
    os.remove(figdir + '/heatflux.png')
if os.path.exists(figdir + '/par.png'):
    os.remove(figdir + '/par.png')
if os.path.exists(figdir + '/airt.png'):
    os.remove(figdir + '/airt.png')
if os.path.exists(figdir + '/rh.png'):
    os.remove(figdir + '/rh.png')
if os.path.exists(figdir + '/wind80.png'):
    os.remove(figdir + '/wind80.png')
if os.path.exists(figdir + '/wind40.png'):
    os.remove(figdir + '/wind40.png')
if os.path.exists(figdir + '/wind2.png'):
    os.remove(figdir + '/wind2.png')
if os.path.exists(figdir + '/netrad.png'):
    os.remove(figdir + '/netrad.png')

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
   #print filein
   filedata = wcprofile(filein)   
   fast.extend(filedata)
for filein in slowfiles:
   #print filein
   filedata = wcprofile(filein)   
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
qclim['ID'] = [1, 11]
qclim['AVG_T'] = [-40, 70]
qclim['AVG_P'] = [0, 110]
qclim['AVG_CO2'] = [-2500, 2500]
# slow data qc limits
qclim['Battery'] = [0, 20]
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
qclim['PAR_60ft_AVG'] = [0, 2200]
qclim['PAR_40ft_AVG'] = [0, 2200]
qclim['PAR_25ft_AVG'] = [0, 2200]
qclim['PAR_2m_AVG'] = [0, 2200]
qclim['WSpd_80ft_S_WVT'] = [0, 50]
qclim['WDir_80ft_D1_WVT'] = [0, 360]
qclim['WSpd_40ft_S_WVT'] = [0, 50]
qclim['WDir_40ft_D1_WVT'] = [0, 360]
qclim['WSpd_2m_S_WVT'] = [0, 50]
qclim['WDir_2m_D1_WVT'] = [0, 360]
qclim['AirT_80ft_AVG'] = [-40, 70]
qclim['AirT_60ft_AVG'] = [-40, 70]
qclim['AirT_40ft_AVG'] = [-40, 70]
qclim['AirT_25ft_AVG'] = [-40, 70]
qclim['AirT_2m_AVG'] = [-40, 70]
qclim['RH_80ft_AVG'] = [0, 105]
qclim['RH_60ft_AVG'] = [0, 105]
qclim['RH_40ft_AVG'] = [0, 105]
qclim['RH_25ft_AVG'] = [0, 105]
qclim['RH_2m_AVG'] = [0, 105]
qclim['NRad_Cs_AVG'] = [-2000, 2000]
qclim['NRad_Cd_AVG'] = [-2000, 2000]
qclim['xPAR_Glb_AVG'] = [0, 2000]
qclim['xPAR_Dif_AVG'] = [0, 2000]
qclim['Err_flag'] = [0, 20]

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

#plot co2 and ID
#f, axarr = plt.subplots(2,sharex=True)
#axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('ID')],'.',
                #xdate=True,ydate=False,label='ID')
#axarr[0].set_ylabel('ID')
#axarr[0].set_title('CO2 mv and ID ' + figdate)
#axarr[0].grid(True)
#axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('AVG_CO2')],'.',
                #xdate=True,ydate=False,label='Avg CO2')
#axarr[1].set_xlabel('Time')
#axarr[1].set_ylabel('mV')
#axarr[1].grid(True)
#axarr[1].xaxis.set_major_locator(hrs3)
#axarr[1].xaxis.set_major_formatter(hrsfmt)
#axarr[1].autoscale_view()
# set up the colors for the plots
values = range(1,11)
fig,ax = plt.subplots()
rbcm = plt.get_cmap('rainbow')
cNorm = colors.Normalize(vmin=1, vmax=values[-1])
scalarMap = cm.ScalarMappable(norm=cNorm, cmap = rbcm)
for i in values:
    timelist = []
    datalist = []
    colorVal = scalarMap.to_rgba(values[i-1])
    id_indx = np.nonzero(fastarray[3]==i)
    id_indx = id_indx[0]
    id_indx = id_indx.tolist()
    labtext = ('%2d'%i)
    for j in id_indx:
        timelist.append(fasttimelist[j]) 
        datalist.append(fastarray[1][j])
    plt.plot_date(timelist,datalist,color=colorVal,marker='.',label=labtext)
ax.legend(loc='best',fontsize='x-small')

ax.set_xlabel('Time')
ax.set_ylabel('mV')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
plt.title('IRGA CO2 voltage output ' + figdate)
plt.savefig(figdir + '/co2.png', dpi=100)
# plot IRGA pressure and temp
f, axarr = plt.subplots(2,sharex=True)
axarr[0].plot_date(fasttimelist,fastarray[fastkeys.index('AVG_T')],'.',
                xdate=True,ydate=False,label='Avg temp')
axarr[0].set_ylabel('Temp (degC)')
axarr[0].set_title('IRGA temp and pressure ' + figdate)
axarr[0].grid(True)
axarr[1].plot_date(fasttimelist,fastarray[fastkeys.index('AVG_P')],'.',
                xdate=True,ydate=False,label='Avg pressure')
axarr[1].set_xlabel('Time')
axarr[1].set_ylabel('hPa')
axarr[1].grid(True)
axarr[1].xaxis.set_major_locator(hrs3)
axarr[1].xaxis.set_major_formatter(hrsfmt)
axarr[1].autoscale_view()
plt.savefig(figdir + '/irgatp.png', dpi=100)

# plot met, surface and soil data
# volatage for data logger
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('Battery')],'.',
             xdate=True,ydate=False,label='Battery Voltage')
ax.set_xlabel('Time')
ax.set_ylabel('Volts')
plt.title('Battery Votlage ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/battvolt.png', dpi=100)
# AirT_200 - AirT_25
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_200')],'b.',
             xdate=True,ydate=False,label='AirT 200')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_100')],'r.',
             xdate=True,ydate=False,label='AirT 100')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_75')],'g.',
             xdate=True,ydate=False,label='AirT 75')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_50')],'m.',
             xdate=True,ydate=False,label='AirT 50')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_25')],'k.',
             xdate=True,ydate=False,label='AirT 25')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('AirT_200 - AirT25 ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.legend(loc='best',fontsize='x-small')
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/airtlow.png', dpi=100)
# SoilT_0 - SoilT_100
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilT_0')],'b.',
             xdate=True,ydate=False,label='SoilT 0')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilT_5')],'r.',
             xdate=True,ydate=False,label='SoilT 5')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilT_10')],'g.',
             xdate=True,ydate=False,label='SoilT 10')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilT_20')],'k.',
             xdate=True,ydate=False,label='SoilT 20')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilT_50')],'m.',
             xdate=True,ydate=False,label='SoilT 50')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilT_100')],'c.',
             xdate=True,ydate=False,label='SoilT 100')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('SoilT_0 - SoilT_100 ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.legend(loc='best', fontsize='x-small')
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/soilt.png', dpi=100)
# SoilW_5 - SoilW_100
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilW_5')],'b.',
             xdate=True,ydate=False,label='SoilW 5')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilW_10')],'r.',
             xdate=True,ydate=False,label='SoilW 10')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilW_20')],'g.',
             xdate=True,ydate=False,label='SoilW 20')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilW_50')],'k.',
             xdate=True,ydate=False,label='SoilW 50')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('SoilW_100')],'m.',
             xdate=True,ydate=False,label='SoilW 100')
ax.set_xlabel('Time')
ax.set_ylabel('Volumetric Water Content (m^3/m^3)')
plt.title('SoilW_5 - SoilW_100 ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.legend(loc='best', fontsize='x-small')
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/soilw.png', dpi=100)
# plot Tree temps
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('TreeT_N')],'.',
             xdate=True,ydate=False,label='Tree T North')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('TreeT_S')],'g.',
             xdate=True,ydate=False,label='Tree T South')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('Tree Temps ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/treet.png', dpi=100)
# heatflux
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('Heatflux')],'.',
             xdate=True,ydate=False,label='Soil heatflux')
ax.set_xlabel('Time')
ax.set_ylabel('W m^-2')
plt.title('Heatflux ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/heatflux.png', dpi=100)
# PAR
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('PAR_60ft_AVG')],'r.',
             xdate=True,ydate=False,label='PAR_60ft_AVG')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('PAR_40ft_AVG')],'b.',
             xdate=True,ydate=False,label='PAR_40ft_AVG')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('PAR_25ft_AVG')],'g.',
             xdate=True,ydate=False,label='PAR_25ft_AVG')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('PAR_2m_AVG')],'k.',
             xdate=True,ydate=False,label='PAR_2m_AVG')
ax.set_xlabel('Time')
ax.set_ylabel('micro-mol s^-1 m^-2')
plt.title('PAR ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.legend(loc='best', fontsize='x-small')
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/par.png', dpi=100)
# AirT_80ft - AirT_2m
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_80ft_AVG')],'b.',
             xdate=True,ydate=False,label='AirT 80ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_60ft_AVG')],'r.',
             xdate=True,ydate=False,label='AirT 60ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_40ft_AVG')],'g.',
             xdate=True,ydate=False,label='AirT 40ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_25ft_AVG')],'m.',
             xdate=True,ydate=False,label='AirT 25ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_2m_AVG')],'k.',
             xdate=True,ydate=False,label='AirT 2m')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('AirT_80ft - AirT_2m ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.legend(loc='best',fontsize='x-small')
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/airt.png', dpi=100)
# RH_80ft - RH_2m
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_80ft_AVG')],'b.',
             xdate=True,ydate=False,label='RH 80ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_60ft_AVG')],'r.',
             xdate=True,ydate=False,label='RH 60ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_40ft_AVG')],'g.',
             xdate=True,ydate=False,label='RH 40ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_25ft_AVG')],'m.',
             xdate=True,ydate=False,label='RH 25ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_2m_AVG')],'k.',
             xdate=True,ydate=False,label='RH 2m')
ax.set_xlabel('Time')
ax.set_ylabel('degC')
plt.title('RH_80ft - RH_2m ' + figdate)
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.legend(loc='best',fontsize='x-small')
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/rh.png', dpi=100)
# plot wind speed 80ft
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot_date(slowtimelist,slowarray[slowkeys.index('WSpd_80ft_S_WVT')],'.',
                xdate=True,ydate=False,label='WSpd_80ft')
axarr[0].set_ylabel('m/s')
axarr[0].set_title('Wind speed and direction 80 ft' + figdate)
axarr[1].plot_date(slowtimelist,slowarray[slowkeys.index('WDir_80ft_D1_WVT')],'.',
                xdate=True,ydate=False,label='WDir_80ft')
axarr[1].set_ylabel('degrees')
axarr[1].set_xlabel('Time')
axarr[1].xaxis.set_major_locator(hrs3)
axarr[1].xaxis.set_major_formatter(hrsfmt)
axarr[1].autoscale_view()
plt.savefig(figdir + '/wind80.png', dpi=100)
# plot wind speed 40ft
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot_date(slowtimelist,slowarray[slowkeys.index('WSpd_40ft_S_WVT')],'.',
                xdate=True,ydate=False,label='WSpd_40ft')
axarr[0].set_ylabel('m/s')
axarr[0].set_title('Wind speed and direction 40 ft' + figdate)
axarr[1].plot_date(slowtimelist,slowarray[slowkeys.index('WDir_40ft_D1_WVT')],'.',
                xdate=True,ydate=False,label='WDir_40ft')
axarr[1].set_ylabel('degrees')
axarr[1].set_xlabel('Time')
axarr[1].xaxis.set_major_locator(hrs3)
axarr[1].xaxis.set_major_formatter(hrsfmt)
axarr[1].autoscale_view()
plt.savefig(figdir + '/wind40.png', dpi=100)
# plot wind speed 2m
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot_date(slowtimelist,slowarray[slowkeys.index('WSpd_2m_S_WVT')],'.',
                xdate=True,ydate=False,label='WSpd_2m')
axarr[0].set_ylabel('m/s')
axarr[0].set_title('Wind speed and direction 2 m' + figdate)
axarr[1].plot_date(slowtimelist,slowarray[slowkeys.index('WDir_2m_D1_WVT')],'.',
                xdate=True,ydate=False,label='WDir_2m')
axarr[1].set_ylabel('degrees')
axarr[1].set_xlabel('Time')
axarr[1].xaxis.set_major_locator(hrs3)
axarr[1].xaxis.set_major_formatter(hrsfmt)
axarr[1].autoscale_view()
plt.savefig(figdir + '/wind2.png', dpi=100)
# plot Net radiometer
fig, ax = plt.subplots()
ax.plot_date(slowtimelist,slowarray[slowkeys.index('NRad_Cs_AVG')],'.',
             xdate=True,ydate=False,label='NRad_Cs')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('NRad_Cd_AVG')],'g.',
             xdate=True,ydate=False,label='NRad_Cd')
ax.set_xlabel('Time')
ax.set_ylabel('W m^-2 (?)')
plt.title('Sub-canopy net radiometer ' + figdate)
ax.legend(loc='best',fontsize='x-small')
ax.xaxis.set_major_locator(hrs3)
ax.xaxis.set_major_formatter(hrsfmt)
ax.autoscale_view()
ax.grid(True)
plt.savefig(figdir + '/netrad.png', dpi=100)
