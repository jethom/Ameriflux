#!/usr/bin/env python

import sys
import re
import logging
import collections
from time import mktime
from datetime import datetime, timedelta

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

        
