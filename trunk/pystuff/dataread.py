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


def wc_flux_read(filepth):
    var_name=['YY', 'MM','DD','HH','DOY','fDOY','Cstor_30','Cflux_30','NEE_30','LE_30','H_30','u*','Flag']
    records=[]
    lines=filepth.readlines()
    for line in lines:
        line=line.replace('\n','')
        data_list=line.split()
        # extract the data
        try: 
            stamp=datetime.strptime('{} {} {} {} {}'.format(data_list[0],data_list[1],data_list[2],int(float(data_list[3])),int((float(data_list[3])*60)%60)),'%Y %m %d %H %M')
        except ValueError:
            break
        # data list
        data_only=data_list[6:]
        data_only_var_name=var_name[6:]

 
# how do I deal with NAN in the data string
        data={}
        for k,v in zip(data_only_var_name,data_only):
            if float(v)==-999:
                data[k]=float('nan')
            else:
                data[k]=float(v)

        records.append((stamp, data))

    return records

def wc_met_read(filepth):
# 69 columns in met file
    var_name=[None]*69
    var_name[0:13]=['YY', 'MM','DD','HH','DOY','fDOY','CO2_2','CO2_5','CO2_10','CO2_25','CO2_45','CO2_70','CO2_97']
    for i in range(13,69):
        var_name[i]='col{:02d}'.format(i)
    records=[]
    lines=filepth.readlines()
    len(lines)
    for line in lines:
        line=line.replace('\n','')
        data_list=line.split()
        # extract the data
        try: 
            stamp=datetime.strptime('{} {} {} {} {}'.format(data_list[0],data_list[1],data_list[2],int(float(data_list[3])),int((float(data_list[3])*60)%60)),'%Y %m %d %H %M')
        except ValueError:
            break
        # data list
        data_only=data_list[6:]
        data_only_var_name=var_name[6:]

 
# how do I deal with NAN in the data string
        data={}
        for k,v in zip(data_only_var_name,data_only):
            if float(v)==-999:
                data[k]=float('nan')
            else:
                data[k]=float(v)

        records.append((stamp, data))

    return records

def sylv_flux_read(filepth):
    records=[]
    lines=filepth.readlines()
    line=lines[18].replace('\n','')
    var_name=line.split(',')
    for line in lines[20:]:
        line=line.replace('\n','')
        data_list=line.split(',')
        # extract the data
      #  print data_list[0], data_list[3], data_list[4]
        if data_list[4]=='2400':
            data_list[4]='0000'
        try: 
            stamp=datetime.strptime('{} {} {} {}'.format(data_list[0],int(float(data_list[2])),data_list[4][0:2], data_list[4][2:4]),'%Y %j %H  %M')
        except ValueError:
            print 'bad date', data_list[0],data_list[3], data_list[4]
            break
        # data list
        data_only=data_list[5:]
        data_only_var_name=var_name[5:]

 
# how do I deal with NAN in the data string
        data={}
        for k,v in zip(data_only_var_name,data_only):
           # print v
            if v=='':
                data[k]=float('nan')
            elif float(v)==-9999:
                data[k]=float('nan')
            else:
                data[k]=float(v)

        records.append((stamp, data))

    return records


def flux_read(filepth):
    records=[]
    lines=filepth.readlines()
    var_name=lines[0].split()
    for line in lines[1:]:
        line=line.replace('\n','')
        data_list=line.split()
        # extract the data
        try: 
            stamp=datetime.strptime('{} {} {} {}'.format(data_list[0],data_list[1],int(float(data_list[2])),int((float(data_list[2])*60)%60)),'%Y %j %H %M')
        except ValueError:
            break
        # data list
        print stamp
        data_only=data_list[3:]
        data_only_var_name=var_name[3:]

 
# how do I deal with NAN in the data string
        data={}
        for k,v in zip(data_only_var_name,data_only):
            if float(v)==-999:
                data[k]=float('nan')
            else:
                data[k]=float(v)

        records.append((stamp, data))

    return records


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

def picarro_read(filepth):

    records=[]

    LOG.info("opening %s" % filepth)
    lines=open(filepth,'rt').readlines()
    line=lines[0]
    line=line.replace('\r\n','')
    var_name=line.split() 
    LOG.info("starting data")
    for line in lines[1:]:
        line=line.replace('\r\n','')
        # print line
        LOG.info("break data into a list")
        # make a timestamp for the observation
        data_list=line.split()
        # extract the data
        stamp=datetime.strptime(data_list[0]+' '+data_list[1], 
                                '%Y-%m-%d %H:%M:%S.%f')
        # data list
        data_only=data_list[6:]
        data_only_var_name=var_name[6:]

 
# how do I deal with NAN in the data string
        data={}
        for k,v in zip(data_only_var_name,data_only):
            data[k]=float(v)

        records.append((stamp, data))

    return records
        
def minico2_read(filepth):

    var_name=[]
    units=[]
    records=[]
    pat = re.compile(r'([^(]+)\s*\(([^)]+)\)\s*(?:,\s*|$)')

    LOG.info("opening %s" % filepth)
    lines=open(filepth,'rt').readlines()
    line=lines[2]
    line=line.replace('\r\n','')
    lst = [(t[0].strip(), t[1].strip()) for t in pat.findall(line)]
   
    for i in range(len(lst)):
        var_name.append(lst[i][0])
        units.append(lst[i][1])
    var_name_data=var_name[1:]
    LOG.info("starting data")
    for line in lines[3:]:
        line=line.replace('\r\n','')
        # print line
        LOG.info("break data into a list")
        # make a timestamp for the observation
        data_list=line.split(',')
        # extract the time
        stamp=datetime.utcfromtimestamp(int(data_list[0]))
        # data only list
        data_only=data_list[1:]

 
# how do I deal with NAN in the data string
        data={}
        for k,v in zip(var_name_data,data_only):
            data[k]=float(v)

        records.append((stamp, data))

    return records

        
