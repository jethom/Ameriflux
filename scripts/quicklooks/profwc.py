#!/usr/bin/env python
#
# script to make plots of the profiler data from Willow Creek
#
# do not need this for my laptop
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
    datadir = "/air/incoming/WillowCreek/profiler/"
    currenttime = datetime.now()
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
yesterday = currenttime + timedelta(days=-1)

figdir = os.path.expanduser("~") + "/public_html/images/willowcreek/profiler"


# clean up the existing figures in the directory
if os.path.exists(figdir + '/irgatp.png'):
    os.remove(figdir + '/irgatp.png')
if os.path.exists(figdir + '/co2.png'):
    os.remove(figdir + '/co2.png')
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

filetypes = ['licordata','metdata','oldsensors','profileDiag']
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
files.extend(glob(yesterdaydir + '*/Profiler_' + ft + '*.dat'))
files.extend(glob(todaydir + '*/Profiler_' + ft + '.dat'))
# metdata table
#metdatafiles.extend(glob(yesterdaydir + '*/Profiler_metdata*.dat'))
#metdatafiles.extend(glob(todaydir + '*/Profiler_metdata*.dat'))
# oldsensors table
#oldsensorsfiles.extend(glob(yesterdaydir + '*/Profiler_oldsensors*.dat'))
#oldsensorsfiles.extend(glob(todaydir + '*/Profiler_oldsensors*.dat'))
# profileDiag table
#profileDiagfiles.extend(glob(yesterdaydir + '*/Profiler_profileDiag*.dat'))
#profileDiagfiles.extend(glob(todaydir + '*/Profiler_profileDiag*.dat'))


# loop through the files and read in the data
for filein in fastfiles:
   #print filein
   filedata = toa5head(filein)   
   data.extend(filedata)
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
#
#-----------------------------------------------------------------------------------
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
ax.plot_date(slowtimelist,slowarray[slowkeys.index('PAR_60ft_Avg')],'r.',
             xdate=True,ydate=False,label='PAR_60ft_Avg')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('PAR_40ft_Avg')],'b.',
             xdate=True,ydate=False,label='PAR_40ft_Avg')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('PAR_25ft_Avg')],'g.',
             xdate=True,ydate=False,label='PAR_25ft_Avg')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('PAR_2m_Avg')],'k.',
             xdate=True,ydate=False,label='PAR_2m_Avg')
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
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_80ft_Avg')],'b.',
             xdate=True,ydate=False,label='AirT 80ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_60ft_Avg')],'r.',
             xdate=True,ydate=False,label='AirT 60ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_40ft_Avg')],'g.',
             xdate=True,ydate=False,label='AirT 40ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_25ft_Avg')],'m.',
             xdate=True,ydate=False,label='AirT 25ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('AirT_2m_Avg')],'k.',
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
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_80ft_Avg')],'b.',
             xdate=True,ydate=False,label='RH 80ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_60ft_Avg')],'r.',
             xdate=True,ydate=False,label='RH 60ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_40ft_Avg')],'g.',
             xdate=True,ydate=False,label='RH 40ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_25ft_Avg')],'m.',
             xdate=True,ydate=False,label='RH 25ft')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('RH_2m_Avg')],'k.',
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
ax.plot_date(slowtimelist,slowarray[slowkeys.index('NRad_Cs_Avg')],'.',
             xdate=True,ydate=False,label='NRad_Cs')
ax.plot_date(slowtimelist,slowarray[slowkeys.index('NRad_Cd_Avg')],'g.',
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
