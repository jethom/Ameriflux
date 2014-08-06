#!/usr/bin/env python

import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta

LOG = logging.getLogger(__name__)

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
        # print line
        LOG.info("break data into a list")

 
        data={}
        for k,v in zip(data_only_var_name,data_list):
            data[k]=float(v)

        records.append((stamp, data))

    return records
