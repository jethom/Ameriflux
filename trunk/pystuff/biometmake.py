from glob import glob
from datetime import datetime, timedelta
from campbellread import toa5head

namematch= { 'LW_up_Avg':'LWout', \
 'PAR_Den_Avg': 'PPFD', \
 'panel_temp_Avg': 'enctemp', \
 'Water_Temp_C_Avg': 'Ts', \
 'SW_up_Avg': 'SWout', \
 'rain_mm_Tot': 'P_rain' , \
 'RECORD': 'RECORD', \
 'airTC_Avg': 'Ta', \
 'atmpres_Avg': 'Pa', \
 'RH_Avg': 'RH', \
 'Level_Avg': 'waterlevel', \
 'LW_down_Avg': 'LWin', \
 'cnr4_T_C_Avg': 'cnr4temp', \
 'SW_down_Avg': 'SWin'} 

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

filesin=glob('*metvalues*')
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
