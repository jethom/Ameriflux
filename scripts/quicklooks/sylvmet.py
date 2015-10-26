#
#
# make daily plots of the lost creek flux calculations
#
#
#-----------------------------------------------------
import matplotlib
import sys
from campbellread import *
import collections
from datetime import datetime, timedelta
from glob import glob

# variables to plot. If variables are similar plot on same figure
plotvars=[["t_hmp_Avg","Air_temp_Avg","TC_Avg"],
["rh_hmp_Avg","RH_Avg"],
["batt_volt_Avg"],
["panel_temp_Avg"],
["SR01Up_Avg","SR01Dn_Avg"],
["IR01Up_Avg","IR01Dn_Avg"],
["water_content_1_Avg","water_content_2_Avg","water_content_3_Avg","water_content_4_Avg"],
["elec_cond_1_Avg","elec_cond_2_Avg","elec_cond_3_Avg","elec_cond_4_Avg"],
["s_temp_1_Avg","s_temp_2_Avg","s_temp_3_Avg","s_temp_4_Avg"],
["PAR_Den_Avg"],
["Wind_Dir_min_Min","Wind_Dir_mean_Avg","Wind_Dir_max_Max"],
["Wind_Speed_min_Min","Wind_Speed_mean_Avg","Wind_Speed_max_Max"],
["Pressure_Avg"],
["Rain_accum_Max"],
["GMP_upper_Avg","GMP_lower_Avg"]]

# plot title and the name to used to save the figure
plotname=["AirTemp", "RelativeHumidity","BatteryVoltage","PanelTemp","ShortWave","LongWave",
"WaterContent","ElecCond","SoilTemp","PAR","WindDir","WindSpeed","Pressure","RainAccum","GMPProfile"]

runmode = 'TEST'
if runmode == 'TEST':
# file directory
# TEST -------------------------------------------------------------------------------
    datadir='/Users/jthom/Documents/data/sylvania/2015/'
    figdir='/Users/jthom/public_html/images/sylvania/'
    today=datetime(2015,1,7)
# TEST -------------------------------------------------------------------------------
else:
# OPERATIONAL ------------------------------------------------------------------------
    matplotlib.use('Agg')
    datadir='/air/incoming/sylvania/2015/'
    figdir='/home/jthom/public_html/images/sylvania/'
    today=datetime.now()
# OPERATIONAL ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
import numpy as np
import pandas as pd
import xray
from dataread import *
from record2xray import record2xray

# get files for the last two days of data

data=[]
for i in range(2,-1,-1):
    datesearch=today-timedelta(days=i)
    filesearch=datesearch.strftime('*met_data*%Y_%m_%d*.dat')
    files=glob(datadir + filesearch)
    for fn in files:
        filedata=toa5head(fn) 
        data.extend(filedata) 
    
datax=record2xray(data)

for i,xvar in enumerate(plotvars):
    fig,ax=plt.subplots()
    for var in xvar:
        datax.sel(varname=var).plot(marker='.',label=var)

    ax.xaxis.set_major_formatter(DateFormatter("%m/%d-%H"))
    plt.title(plotname[i])
    ax.legend(loc='best',fontsize='x-small')
    plt.savefig(figdir + plotname[i] + '.png', dpi=100)
    plt.close(fig)

