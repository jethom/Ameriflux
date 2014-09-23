import os,shutil
from time import mktime
from datetime import datetime, timedelta

def archivedata(filepth):
    dirpath = os.path.expanduser("~") + '/Documents/data/'
    datepath = datetime.strftime(datetime.now(),'%Y%m%d/%H00')

    if not os.path.exists(dirpath + datepath):
        os.makedirs(dirpath + datepath)

    shutil.move(filepth, dirpath + datepath)
