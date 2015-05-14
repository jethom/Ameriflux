#!/usr/bin/env python

import sys
import re
import logging
import struct
from datetime import datetime, timedelta
import binascii
# date used for base time on Campbell scientific data loggers.
csibasedate = '1990-01-01:000000'
csiepochstart=631152000  # seconds difference between unix epoch 1970-01-01,00:00:00 and CSI epoch 1990-01-01, 00:00:00

LOG = logging.getLogger(__name__)

def toa5head(filepth):
# included logic to handle TOACI1 files as well. These are not very common.

    records=[]

    LOG.info("opening %s" % filepth)
    lines=open(filepth,'rt').readlines()
    lineno=0
    line=lines[lineno]
    line=line[:-2]
    line=line.replace('"','')
    filetype=line.split(',')[0]
    
    lineno+=1
    line=lines[lineno]
    line=line[:-2]
    line=line.replace('"','')
    var_name=line.split(',') 
    lineno+=1
    if filetype=='TOA5':
        line=lines[lineno]
        line=line.replace('\n','')
        line=line.replace('"','')
        units=line.split(',')
        lineno+=3
    LOG.info("starting data")
    for line in lines[lineno:]:
        type(line)
        # print line
        LOG.info("break data into a list")
        line=line.replace('"','')
        line=line.replace('\n','')
        # make a timestamp for the observation
        data_list=line.split(',')
        # extract the data
        # get the time
        needmicrosec = data_list[0].find('.')
        if needmicrosec>0:
            microsecs = int(data_list[0][(needmicrosec+1):]) * 100000
            data_list[0] = data_list[0][:needmicrosec]
            data_list[0] = data_list[0] + ':' + str(microsecs)
            # found a period in the date string
        else:
            data_list[0] = data_list[0] + ':000000'
        stamp=datetime.strptime(data_list[0], '%Y-%m-%d %H:%M:%S:%f')
        # check to see if RECORD is a variable name if it exists then remove it
        #try:
            #recordidx = var_name.index('RECORD')
            #var_name.pop(recordidx)
            #data_list.pop(recordidx)
        #except ValueError:
            #pass
        # data list
        data_only=data_list[1:]
        data_only_var_name=var_name[1:]
        if filetype=='TOA5':
            data_only_units_name=units[1:]

 
# how do I deal with NAN in the data string
        data={}
        metadata={}
        for k,v in zip(data_only_var_name,data_only):
            data[k]=float(v)
        if filetype=='TOA5':
            for k,v in zip(data_only_var_name,data_only_units_name):
                metadata[k]=v
            records.append((stamp, data,metadata))
        else:
            records.append((stamp, data))

    return records


def parse_csi_value(sval):
    """Parse a HEX string from data into a value using the CSI FP2 data format
    Each 16 bit hex values are defined as bit 1= polarity,
    bits 2-3 = decimal location
    bits 4-16 = data value
    """
    if sval:
       polarity=-1 if int(sval,16) & (1 << 15) else 1
       places = int(sval,16) >> 13 & 3
       value = float(int(sval,16) & 0x1FFF)

       return polarity*value/10**places
    else:
       return float('nan')


def readtob1file(fileptr):
    records=[]
    fileptr.seek(0)
    CSItypes = {'ULONG': 'I', 'IEEE4': 'f', 'FP2': '', 'UINT2': 'H', 'UINT4': 'I'}
    CSItypelen = {'ULONG': 4, 'IEEE4': 4, 'FP2': 2 ,'UINT2': 2, 'UINT4' : 4}
    # read in the first five lines of file description
    infolines = []
    for i in range(5):
        infolines.append(fileptr.readline())
    infolines[1] = infolines[1].replace('"','')
    infolines[1] = infolines[1].replace('\r\n','')
    varnames = infolines[1].split(',')
    infolines[4] = infolines[4].replace('"','') 
    infolines[4] = infolines[4].replace('\r\n','') 
    types=infolines[4].split(',')
# read in the binary data
    data = fileptr.read()
# initialize the location in the string
    i=0
# move through the string reading each data type
    while i<len(data):
       dataline = []
       for dt in types:
           if dt.rfind('FP2')==0:
               dataline.append(parse_csi_value(binascii.hexlify(data[i:i+CSItypelen.get(dt)])))
           else:
               dataline.append(struct.unpack(CSItypes.get(dt),data[i:i+CSItypelen.get(dt)])[0])
           i=i+CSItypelen.get(dt)
# make the time stamp
       stamp = datetime.utcfromtimestamp(dataline[0] + csiepochstart)
       stamp = stamp.replace(microsecond=int(dataline[1]/1e3))
       datadict={}
       for k,v in zip(varnames[2:],dataline[2:]):
           datadict[k]=v
       records.append((stamp,datadict))
    return records

def wcflux(filepth):

    records=[]

    LOG.info("opening %s" % filepth)
    lines=open(filepth,'rt').readlines()
    LOG.info("starting data")
    for line in lines:
        
        line=line.replace('\r\n','')
        file_id = line.split(',')[0]
        if file_id=='114':
            time_list = line.split(',')[1:5]
            #print time_list
            hour = int(time_list[2])/100
            minute = int(time_list[2])%100
            seconds = float(time_list[3])
            microsecs = '{:06d}'.format((int((seconds - int(seconds))*1000000)))
            data_only_var_name = ['Ux', 'Uy', 'Uz', 'Ts', 'diag_csat', 
                                  'co2', 'h2o', 'LI_P', 'LI_T']    
            data_list = line.split(',')[5:]
            # if line is short fill it in with "nan"
            data_list=filter(None,data_list)
            while len(data_list) < len(data_only_var_name):
                data_list.append('nan')
        elif file_id=='2': 
            time_list = line.split(',')[1:4]
            hour = int(time_list[2])/100
            minute = int(time_list[2])%100
            seconds = 0.0
            microsecs='000000'
            data_only_var_name = ['RTD_T_AVG', 'Atm_P', 'RH', 
                                  'Solar_In_AVG', 'Solar_Out_AVG', 
                                  'IR_In_AVG', 'IR_Out_AVG', 
                                  'KZ_T_AVG', 'Battery', 
                                  'Leaf_Wet', 'Solar_In_STD']    
            data_list = line.split(',')[4:]
            # if line is short fill it in with "nan"
            data_list=filter(None,data_list)
            while len(data_list) < len(data_only_var_name):
                data_list.append('nan')
        my_date = time_list[0] + ':' + time_list[1] + ':' '{:02d}'.format(hour) + ':' \
                  '{:02d}'.format(minute) + ':' + '{:02d}'.format(int(seconds)) + ':'  \
                  + microsecs
        stamp = datetime.strptime(my_date, '%Y:%j:%H:%M:%S:%f')
        # print line
        LOG.info("break data into a list")

 
        data={}
        for k,v in zip(data_only_var_name,data_list):
            data[k]=float(v)

        records.append((stamp, data))

    return records

def wcprofile(filepth):
    records=[]

    LOG.info("opening %s" % filepth)
    lines=open(filepth,'rt').readlines()
    LOG.info("starting data")
    for line in lines:
        
        line=line.replace('\r\n','')
        file_id = line.split(',')[0]
        if file_id!='2':
            data_only_var_name = ['ID', 'AVG_T', 'AVG_P', 'AVG_CO2']
        elif file_id=='2': 
            data_only_var_name = ['Battery',
                                  'AirT_200','AirT_100','AirT_75','AirT_50','AirT_25',
                                  'SoilT_0','SoilT_5','SoilT_10','SoilT_20','SoilT_50','SoilT_100',
                                  'TreeT_N','TreeT_S',
                                  'Heatflux',
                                  'SoilW_5','SoilW_10','SoilW_20','SoilW_50','SoilW_100',
                                  'PAR_60ft_AVG', 'PAR_40ft_AVG', 'PAR_25ft_AVG', 'PAR_2m_AVG',
                                  'WSpd_80ft_S_WVT', 'WDir_80ft_D1_WVT',
                                  'WSpd_40ft_S_WVT', 'WDir_40ft_D1_WVT',
                                  'WSpd_2m_S_WVT', 'WDir_2m_D1_WVT',
                                  'AirT_80ft_AVG',
                                  'AirT_60ft_AVG',
                                  'AirT_40ft_AVG',
                                  'AirT_25ft_AVG',
                                  'AirT_2m_AVG',
                                  'RH_80ft_AVG',
                                  'RH_60ft_AVG',
                                  'RH_40ft_AVG',
                                  'RH_25ft_AVG',
                                  'RH_2m_AVG',
                                  'NRad_Cs_AVG','NRad_Cd_AVG',
                                  'xPAR_Glb_AVG','xPAR_Dif_AVG', 'Err_flag']
        time_list = line.split(',')[1:4]
        hour = int(time_list[2])/100
        minute = int(time_list[2])%100
        seconds = 0.0
        microsecs='000000'
        my_date = time_list[0] + ':' + time_list[1] + ':' '{:02d}'.format(hour) + ':' \
                  '{:02d}'.format(minute) + ':' + '{:02d}'.format(int(seconds)) + ':'  \
                  + microsecs
        stamp = datetime.strptime(my_date, '%Y:%j:%H:%M:%S:%f')
        data_list = line.split(',')[4:]
        # if line is short fill it in with "nan"
        data_list=filter(None,data_list)
        while len(data_list) < len(data_only_var_name):
            data_list.append('nan')

        # print line
        LOG.info("break data into a list")

 
        data={}
        for k,v in zip(data_only_var_name,data_list):
            data[k]=float(v)

        records.append((stamp, data))

    return records

def wlefsurf(filepth):
    records=[]

    LOG.info("opening %s" % filepth)
    lines=open(filepth,'rt').readlines()
    LOG.info("starting data")
    for line in lines:
        
        line=line.replace('\r\n','')
        file_id = line.split(',')[0]
        data_only_var_name = ['par_AVG','pyran_AVG', 'air_t_AVG', 'rh_AVG', 'precip_TOT', 'atm_p_AVG']
        time_list = line.split(',')[1:4]
        hour = int(time_list[2])/100
        minute = int(time_list[2])%100
        seconds = 0.0
        microsecs='000000'
        my_date = time_list[0] + ':' + time_list[1] + ':' '{:02d}'.format(hour) + ':' \
                  '{:02d}'.format(minute) + ':' + '{:02d}'.format(int(seconds)) + ':'  \
                  + microsecs
        stamp = datetime.strptime(my_date, '%Y:%j:%H:%M:%S:%f')
        data_list = line.split(',')[4:]
        # if line is short fill it in with "nan"
        data_list=filter(None,data_list)
        while len(data_list) < len(data_only_var_name):
            data_list.append('nan')
        # print line
        LOG.info("break data into a list")

 
        data={}
        for k,v in zip(data_only_var_name,data_list):
            data[k]=float(v)

        records.append((stamp, data))

    return records
