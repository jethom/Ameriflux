# make Licor style biomet files from Sylvania TOA5 files
from glob import glob
from datetime import datetime, timedelta
from math import isnan
from campbellread import toa5head
import os

namematch= { 'IR01Up_Avg':'LWout_1_1_1', \
'PAR_Den_Avg': 'PPFD_1_1_1', \
'panel_temp_Avg': 'enctemp_1_1_1', \
's_temp_1_Avg': 'Ts_1_1_1', \
'SR01Up_Avg': 'SWout_1_1_1', \
'Rain_accum_Max': 'P_rain_1_1_1' , \
'RECORD': 'RECORD_1_1_1', \
'Air_temp_Avg': 'Ta_1_1_1', \
't_hmp_Avg': 'Ta_1_1_1', \
'Pressure_Avg': 'Pa_1_1_1', \
'RH_Avg': 'RH_1_1_1', \
'rh_hmp_Avg': 'RH_1_1_1', \
'water_content_1_Avg': 'SWC_1_1_1', \
'IR01Dn_Avg': 'LWin_1_1_1', \
'SR01Dn_Avg': 'SWin_1_1_1', \
'Wind_Speed_max_Max' : 'MWS_1_1_1', \
'Wind_Dir_mean_Avg' : 'WD_1_1_1'}

unitsmatch = {'IR01Up_Avg': 'W+1m-2', \
'PAR_Den_Avg': 'umol+1m-2s-1', \
'panel_temp_Avg' : 'C', \
's_temp_1_Avg' : 'C', \
'SR01Up_Avg' : 'W+1m-2', \
'Rain_accum_Max' : 'mm', \
'RECORD' : 'dimensionless', \
'Air_temp_Avg' : 'C', \
't_hmp_Avg' : 'C', \
'Pressure_Avg' : 'hPa', \
'RH_Avg' : '%', \
'rh_hmp_Avg' : '%', \
'water_content_1_Avg': 'm+3m-3', \
'IR01Dn_Avg' : 'W+1m-2', \
'SR01Dn_Avg' : 'W+1m-2', \
'Wind_Speed_max_Max' : 'm+1s-1', \
'Wind_Dir_mean_Avg' : 'degrees'}

keystoprint = ['Air_temp_Avg','RH_Avg','IR01Up_Avg', 'IR01Dn_Avg', 'SR01Up_Avg', 'SR01Dn_Avg', 'PAR_Den_Avg', 's_temp_1_Avg', \
'water_content_1_Avg', 'Wind_Speed_max_Max', 'Wind_Dir_mean_Avg', 'Pressure_Avg']

missing=-999.9

# make header strings for the biomet file
timetitle='TIMESTAMP_1'
timeunits='yyyy-mm-dd HHMM'

dates=datetime.now() - timedelta(days=1)
#filepath='/air/incoming/sylvania/YYYY/'
#filepath=dates.strftime('/Users/jthom/Documents/data/sylvania/%Y/')
filepath=dates.strftime('/air/incoming/sylvania/%Y/')
fndate=dates.strftime('*met_data_%Y_%m_%d_*.dat')

filesin=glob(filepath + fndate)
fout = dates.strftime(filepath + '%jbiomet.txt')

timelist=[]
datalist=[]
for fn in filesin:
    data=toa5head(fn)

    timelist=[]
    datalist=[]
    for i in range(len(data)):
        timelist.append(data[i][0]) 
        datalist.append(data[i][1]) 

# convert the long wave data to include the sensor body temperature adjustment
    for i in range(len(data)):
        datalist[i]['IR01Dn_Avg'] = datalist[i]['IR01Dn_Avg'] + 5.67e-8 * (datalist[i]['TC_Avg'] + 273.15) ** 4  
        datalist[i]['IR01Up_Avg'] = datalist[i]['IR01Up_Avg'] + 5.67e-8 * (datalist[i]['TC_Avg'] + 273.15) ** 4  


    unitslist=[]
    titlelist=[]
    for j in keystoprint:
        unitslist.append(unitsmatch[j])
        titlelist.append(namematch[j])

    headtitles=timetitle + ',' + ','.join(titlelist) + '\n'
    headunits=timeunits + ',' + ','.join(unitslist) + '\n'

    datafrmt=[]
    printstr=[]
    for i in range(len(timelist)):
        for j in keystoprint:
            if isnan(datalist[i][j]):
                datalist[i][j]=missing
            datafrmt.append('%.2f' % datalist[i][j])
        printstr.append(timelist[i].strftime('%Y-%m-%d %H%M') + ',' + ','.join(datafrmt) + '\n')
        datafrmt=[]
 
    if os.path.exists(fout):
        fo=open(fout,'at')
        fo.writelines(printstr)
        fo.close()
    else:
        fo=open(fout,'wt')
        fo.write(headtitles)
        fo.write(headunits)
        fo.writelines(printstr)
        fo.close()
