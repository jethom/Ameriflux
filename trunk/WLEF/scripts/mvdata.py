import os,shutil
from time import mktime
from datetime import datetime, timedelta
from glob import glob
filepattern = 'testAvg'
# directory where data is located
datapath = os.path.expanduser("~") + '/Documents/loggernet/data/'

# determine what files need to be moved
filelist = glob(datapath + filepattern + '*.dat')

# directory to write data (dirpath + datepath)
dirpath = os.path.expanduser("~") + '/Documents/data/CR3000/'

for filename in filelist:
    filedate = datetime.strptime(filename,datapath + filepattern+'_%Y_%m_%d_%H%M.dat')
    datepath = datetime.strftime(filedate,'%Y%m%d%H00')

    if not os.path.exists(dirpath + datepath):
        os.makedirs(dirpath + datepath)
    
    shutil.move(filename, dirpath + datepath)
