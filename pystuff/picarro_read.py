#!/usr/bin/env python

import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta

LOG = logging.getLogger(__name__)

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

        
