from glob import glob
from datetime import datetime, timedelta
from campbellread import toa5head

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

missing = -999.9
keystoprint1 = ['t_hmp_Avg','rh_hmp_Avg','IR01Up_Avg', 'IR01Dn_Avg', 'SR01Up_Avg', 'SR01Dn_Avg', 'PAR_Den_Avg', 's_temp_1_Avg', \
'water_content_1_Avg' ]
date1=datetime(2014,06,19)
keystoprint2 = ['Air_temp_Avg','RH_Avg','IR01Up_Avg', 'IR01Dn_Avg', 'SR01Up_Avg', 'SR01Dn_Avg', 'PAR_Den_Avg', 's_temp_1_Avg', \
'water_content_1_Avg', 'Wind_Speed_max_Max', 'Wind_Dir_mean_Avg', 'Pressure_Avg']
date2=datetime(2014,6,20)

# make header strings for the biomet file
timetitle='TIMESTAMP_1'
timeunits='yyyy-mm-dd HHMM'

filepath='/Users/jthom/Documents/data/sylvania/2015/'
# find dates to process
dates=datetime.now() - timedelta(days=1)
datestr = dates.strftime('%Y%m%d')


filesin=glob(filepath + '/met_data*.dat')
timelist=[]
datalist=[]
for fn in filesin:
    datefilenameIn=datetime.strptime(fn,filepath + 'met_data_%Y_%m_%d_%H%M.dat')
    data=toa5head(fn)
    for i in range(len(data)):
        timelist.append(data[i][0]) 
        datalist.append(data[i][1]) 

    if datefilenameIn < date1:
        keystoprint=keystoprint1
    elif datefilenameIn >= date2:
        keystoprint=keystoprint2

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
            datafrmt.append('%.2f' % datalist[i][j])
        printstr.append(timelist[i].strftime('%Y-%m-%d %H%M') + ',' + ','.join(datafrmt) + '\n')
        datafrmt=[]
 
    fout = datefilenameIn.strftime(filepath + '%jbiomet.txt')
    fo=open(fout,'wt')
    fo.write(headtitles)
    fo.write(headunits)
    fo.writelines(printstr)
    fo.close()
