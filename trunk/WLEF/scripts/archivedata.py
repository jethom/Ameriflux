import os,shutil
from time import mktime
from datetime import datetime, timedelta

def archivedata(filepth):
    dirpath = os.path.expanduser("~") + '/Documents/data/'
    now = datetime.now()
    if now.minute < 30:
        datepath = datetime.strftime(datetime.now(),'%Y_%m/%d/%H00/')
    elif now.minute >= 30:
        datepath = datetime.strftime(datetime.now(),'%Y_%m/%d/%H30/')

    if not os.path.exists(dirpath + datepath):
        os.makedirs(dirpath + datepath)

    shutil.move(filepth, dirpath + datepath)
