from glob import glob
from datetime import datetime, timedelta
from campbellread import toa5head

namematch= { 'LW_up_Avg':'LWout_1_1_1', \
 'PAR_Den_Avg': 'PPFD_1_1_1', \
 'panel_temp_Avg': 'enctemp_1_1_1', \
 'Water_Temp_C_Avg': 'Ts_1_1_1', \
 'SW_up_Avg': 'SWout_1_1_1', \
 'rain_mm_Tot': 'P_rain_1_1_1' , \
 'RECORD': 'RECORD_1_1_1', \
 'airTC_Avg': 'Ta_1_1_1', \
 'atmpres_Avg': 'Pa_1_1_1', \
 'RH_Avg': 'RH_1_1_1', \
 'Level_Avg': 'waterlevel_1_1_1', \
 'LW_down_Avg': 'LWin_1_1_1', \
 'cnr4_T_C_Avg': 'cnr4temp_1_1_1', \
 'SW_down_Avg': 'SWin_1_1_1'} 

unitsmatch = {'LW_up_Avg': 'W+1m-2', \
'batt_volt_Avg': 'volts', \
'PAR_Den_Avg': 'umol+1m-2s-1', \
'panel_temp_Avg' : 'C', \
'Water_Temp_C_Avg' : 'C', \
'SW_up_Avg' : 'W+1m-2', \
'rain_mm_Tot' : 'mm', \
'RECORD' : 'dimensionless', \
'airTC_Avg' : 'C', \
'atmpres_Avg' : 'hPa', \
'RH_Avg' : '%', \
'Level_Avg' : 'psi', \
'LW_down_Avg' : 'W+1m-2', \
'cnr4_T_C_Avg' : 'C', \
'SW_down_Avg' : 'W+1m-2'}

keystoprint = ['airTC_Avg','RH_Avg','LW_up_Avg', 'LW_down_Avg', 'SW_up_Avg', 'SW_down_Avg', 'PAR_Den_Avg', 'Water_Temp_C_Avg']

timetitle='TIMESTAMP_1'
timeunits='yyyy-mm-dd HHMM'

#filesin=glob('/air/incoming/LostCreek/2014/2014*/*metvalues*')
filesin=glob('/air/incoming/LostCreek/201510*/*metvalues*')
unitslist=[]
titlelist=[]
for j in keystoprint:
    unitslist.append(unitsmatch[j])
    titlelist.append(namematch[j])

headtitles=timetitle + ',' + ','.join(titlelist) + '\n'
headunits=timeunits + ',' + ','.join(unitslist) + '\n'

for fn in filesin:
    timelist=[]
    datalist=[]
    #timestr=[]
    #datastr=[]
    printstr=[]
    data=toa5head(fn)
    for i in range(len(data)):
        timelist.append(data[i][0]) 
        datalist.append(data[i][1]) 
    for i in range(len(data)):
        datafrmt=[]
        for j in keystoprint:
            datafrmt.append('%.2f' % datalist[i][j])
 #       datastr.append(','.join(datafrmt) + '\n')     
 #       timstr.append(timelist[i].strftime('%Y-%m-%d %H%M'))
        printstr.append(timelist[i].strftime('%Y-%m-%d %H%M') + ', ' + ','.join(datafrmt) + '\n')
     
    fout=fn.replace('metvalues','biomet')
    fo=open(fout,'wt')
    fo.write(headtitles)
    fo.write(headunits)
    fo.writelines(printstr)
    fo.close()
