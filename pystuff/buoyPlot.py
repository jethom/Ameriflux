from campbellread import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from windrose import WindroseAxes

def buoyLimnoPlot(fileptr):
    wT=[[] for x in range(23)]
    wTLevels=(np.array([0,0.5,1,1.5,2,3,4,5,6,7,8,9,10,
               11,12,13,14,15,16,17,18,19,20]))
    pco2=[]
    o2ppm=[]
    o2temp=[]
    o2sat=[]
    chlor=[]
    phyco=[]
    irT=[]
    airT=[]
    limno_ts=[]

    # read file
    ld = toa5iter(fileptr)
    wTLevels=wTLevels * -1.0
    for i in range(len(ld)):
       limno_ts.append(ld[i][0])
       pco2.append(ld[i][1].get('pco2ppm_Avg'))
       o2ppm.append(ld[i][1].get('doptoppm'))
       o2sat.append(ld[i][1].get('doptosat'))
       o2temp.append(ld[i][1].get('doptotemp'))
       chlor.append(ld[i][1].get('chlor'))
       phyco.append(ld[i][1].get('phyco'))
       irT.append(ld[i][1].get('IRTL'))
       airT.append(ld[i][1].get('airTL'))
       for j in range(23):
           keyName='watertemp({:d})'.format(j+1)
           wT[j].append(ld[i][1].get(keyName))
    
    datadate=limno_ts[1].strftime('(%Y%m%d)')


# plot air temp, ir temp, 0 water temp , -1 water temp
    plt.plot_date(limno_ts,airT,'r.',label='Air Temp')
    plt.plot_date(limno_ts,irT,'g.',label='IR Skin Temp')
    plt.plot_date(limno_ts,wT[0],'b.',label='0m Water Temp')
    plt.plot_date(limno_ts,wT[2],'c.',label='1m Water Temp')
    plt.xlabel('time')
    plt.ylabel('Temp (degC)')
    plt.legend(loc='best')
    plt.title('Near Surface Temperatures ' + datadate)
    plt.savefig('temps.png',dpi=100)

    #plot pco2 and o2ppm
    fig, ax1 = plt.subplots()
    ax1.plot_date(limno_ts,o2ppm,'b.')
    ax1.set_xlabel('time')
    ax1.set_ylabel('O2 (ppm)',color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ax2=ax1.twinx()
    ax2.plot_date(limno_ts,pco2,'r.')
    ax2.set_ylabel('pCO2 (ppm)',color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.title('pCO2 and O2 (ppm) ' + datadate)
    plt.savefig('co2_o2.png',dpi=100)

    #plot o2temp and o2sat
    fig, ax1 = plt.subplots()
    ax1.plot_date(limno_ts,o2temp,'b.')
    ax1.set_xlabel('time')
    ax1.set_ylabel('DOpto temp (degC)',color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ax2=ax1.twinx()
    ax2.plot_date(limno_ts,o2sat,'r.')
    ax2.set_ylabel('O2 Sat (%)',color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.title('DOpto Temp and O2 Sat ' + datadate)
    plt.savefig('dopto_T_sat.png',dpi=100)

    #plot chlor and  phyco
    fig, ax1 = plt.subplots()
    ax1.plot_date(limno_ts,chlor,'g.')
    ax1.set_xlabel('time')
    ax1.set_ylabel('chlor (micrograms/L)',color='g')
    for tl in ax1.get_yticklabels():
        tl.set_color('g')
    ax2=ax1.twinx()
    ax2.plot_date(limno_ts,phyco,'b.')
    ax2.set_ylabel('Phyco (cells/mL)',color='b')
    for tl in ax2.get_yticklabels():
        tl.set_color('b')
    plt.title('Chlorophyll and Phycocyanin ' + datadate)
    plt.savefig('chlor_phyco.png',dpi=100)

# plot the water column contour over time
    plt.figure()
    waterT=np.array(wT) 
    plt.contourf(limno_ts,wTLevels,waterT,50)
#    plt.show()
    plt.colorbar()
    plt.xlabel('time')
    plt.ylabel('depth (m)')
    plt.title('Water Temperature ' + datadate)
    plt.savefig('watertemp.png',dpi=100)

def buoyMetPlot(fileiter):
    windsp=[]
    winddir=[]
    airT=[]
    u=[]
    gust=[]
    irT=[]
    met_ts=[]

# read the file
    md=toa5iter(fileiter)

    for i in range(len(md)):
        met_ts.append(md[i][0])
        windsp.append(md[i][1].get('windsp'))
        winddir.append(md[i][1].get('winddir'))
        airT.append(md[i][1].get('airtemp'))
        u.append(md[i][1].get('relhum'))
        gust.append(md[i][1].get('gust'))
        irT.append(md[i][1].get('TargTempC'))

    datadate=met_ts[1].strftime('(%Y%m%d)')

#plot air and skin temp
    plt.figure()
    plt.plot_date(met_ts,airT,'b.',label='Air Temp')
    plt.plot_date(met_ts,irT,'g.',label='IR Skin Temp')
    plt.xlabel('Time')
    plt.ylabel('Temp (degC)')
    plt.legend(loc='best')
    plt.title('Air Temperature and IR Skin Temperature ' + datadate)
    plt.savefig('air_skin_temp.png', dpi=100)
     

# plot wind speed
    plt.figure()
    plt.plot_date(met_ts,windsp,'.')
    plt.xlabel('Time')
    plt.ylabel('Wind speed (m/s)')
    plt.title('Wind Speed ' + datadate)
    plt.savefig('windspeed.png', dpi=100)
     
# plot wind direction
    plt.figure()
    plt.plot_date(met_ts,winddir,'.')
    plt.xlabel('Time')
    plt.ylabel('Wind direction (degrees)')
    plt.title('Wind Direction ' + datadate)
    plt.savefig('winddir.png', dpi=100)

# plot relative humidity
    plt.figure()
    plt.plot_date(met_ts,u,'.')
    plt.xlabel('Time')
    plt.ylabel('Relative Humidity (%)')
    plt.title('Relative Humidity ' + datadate)
    plt.savefig('rh.png', dpi=100)

# plot windrose
    ax=new_axes()
    ax.bar(winddir,windsp,normed=True, opening=0.8, edgecolor='white')
    set_legend(ax)
    plt.title('Wind Rose ' + datadate)
    plt.savefig('windrose.png')

def set_legend(ax):
    l=ax.legend(loc='best')
    plt.setp(l.get_texts(), fontsize=8)

def new_axes():
    fig = plt.figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

