from glob import glob
from subprocess import call
from datetime import datetime, timedelta
from time import mktime
from shutil import move, copyfile

cd /air/incoming/LostCreek/tmp

metfiles = glob('*met*')
tsfiles = glob('*ts*')

for i in range(len(metfiles)):
    try:
        datefield = datetime.strptime(metfiles[i],'LostCreek_metvalues_%Y_%m_%d_%H%M.dat')
    except ValueError:
        datefield = datetime.strptime(metfiles[i],'LostCreek_metvalues_%Y_%m_%d_%H%M_1.dat')
    datestr = datefield.strftime('/air/incoming/LostCreek/%Y%m%d')
    searchDate = datefield.strftime('%Y_%m_%d')
    retCode = call(['mkdir',datestr])
    if retCode == 0:
         for j in glob('*' + searchDate + '*'):
             copyfile(j,datestr + '/' + j)


