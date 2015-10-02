#!/usr/bin/env python

import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

LOG = logging.getLogger(__name__)

def lgr_read(filepth):

    records=[]

    LOG.info("opening %s" % filepth)
    lines=open(filepth,'rt').readlines()
    starttime = datetime.strptime(lines[0],'%Y %b %d %H:%M:%S\n')
    line=lines[1]
    line=line.replace('\n','')
    line=line.replace(',',' ')
    var_name=line.split() 
    LOG.info("starting data")
    for line in lines[2:]:
        
        line=line.replace('\n','')
        line=line.replace(',',' ')
        # print line
        LOG.info("break data into a list")
        # make a timestamp for the observation
        data_list=line.split()
        # extract the data
        try: 
            stamp=datetime.strptime(data_list[0] + ' ' + data_list[1],
                                '%m/%d/%y %H:%M:%S.%f')
        except ValueError:
            break
        # data list
        data_only=data_list[2:]
        data_only_var_name=var_name[1:]

 
# how do I deal with NAN in the data string
        data={}
        for k,v in zip(data_only_var_name,data_only):
            data[k]=float(v)

        records.append((stamp, data))

    return records

        
def lgr_cal(co2cal,ch4cal,filename):
    data=lgr_read(filename)

# create savenames for figures
    co2savename='{:5.1f}co2'.format(co2cal)
    co2savename=co2savename.replace('.','_') + '.png'
    ch4savename='{:5.1f}ch4'.format(ch4cal)
    ch4savename=ch4savename.replace('.','_') + '.png'
# initialize the date and co2/ch4 lists
    dt=[]
    co2=[]
    ch4=[]
    
# read in the data from the record
    for i in range(len(data)):
        dt.append(data[i][0])
        co2.append(data[i][1].get('[CO2]_ppm'))
        ch4.append(data[i][1].get('[CH4]_ppm'))

     
    plt.figure()
    co2mean=np.nanmean(co2)
    co2std=np.nanstd(co2)
    figtitle='cal tank = {:5.1f} ppm LGR mean = {:5.1f} ppm; LGR std ={:5.1f} ppm'.format(co2cal,co2mean,co2std)
    plt.title(figtitle)
    plt.plot_date(dt,co2,'b.')
    plt.axhspan(co2mean + co2std, co2mean-co2std,color='y',alpha=0.5,lw=0)
    plt.axhline(y=co2cal, color='r')

    plt.savefig(co2savename,dpi=100)
    plt.close()

    plt.figure()
    ch4mean=np.nanmean(ch4)
    ch4std=np.nanstd(ch4)
    figtitle='cal tank = {:6.4f} ppm LGR mean = {:6.4f} ppm; LGR std ={:6.4f} ppm'.format(ch4cal/1000.,ch4mean,ch4std)
    plt.plot_date(dt,ch4,'b.')
    plt.title(figtitle)
    plt.axhspan(ch4mean + ch4std, ch4mean-ch4std,color='y',alpha=0.5,lw=0)
    plt.axhline(y=ch4cal/1000., color='r')

    plt.savefig(ch4savename,dpi=100)
    plt.close()
