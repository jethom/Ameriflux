#!/usr/bin/env python

import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta

LOG = logging.getLogger(__name__)

def campbellread(filepth):

    records=[]

    LOG.info("opening %s" % filepth)
    lines=open(filepth,'rt').readlines()
    line=lines[1]
    line=line[:-2]
    line=line.replace('"','')
    var_name=line.split(',') 
    LOG.info("starting data")
    for line in lines[4:]:
        type(line)
        line=line[:-2]
        # print line
        LOG.info("break data into a list")
        line=line.replace('"','')
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

 
# how do I deal with NAN in the data string
        data={}
        for k,v in zip(data_only_var_name,data_only):
            data[k]=float(v)

        records.append((stamp, data))

    return records

        
