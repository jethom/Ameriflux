from subprocess import call
from datetime import timedelta, datetime

# run rsync for yesterday to make sure all of the data was copied
ymyest = datetime.strftime(datetime.now()-timedelta(days=1),'%Y_%m/')
dateyest = datetime.strftime(datetime.now()-timedelta(days=1),'%Y_%m/%d')
cmd = 'rsync -qrlt /home/flux/Documents/data/' + dateyest + ' co2.aos.wisc.edu::WLEFFlux/Data/' + ymyest 
sts = call(cmd, shell=True)
print 'yesterdays rsync {}'.format(sts)
# rsync todays data
ymtoday = datetime.strftime(datetime.now(),'%Y_%m/')
datetoday = datetime.strftime(datetime.now(),'%Y_%m/%d')
cmd = 'rsync -qrlt /home/flux/Documents/data/' + datetoday + ' co2.aos.wisc.edu::WLEFFlux/Data/' + ymtoday
sts = call(cmd, shell=True)
print 'todays rsync {}'.format(sts)
