from subprocess import call
from datetime import timedelta, datetime

# run rsync for yesterday to make sure all of the data was copied
dateyest = datetime.strftime(datetime.now()-timedelta(days=1),'%Y%m%d')
cmd = 'rsync -qrlt /home/flux/Documents/data/CR3000/' + dateyest + '* flux.aos.wisc.edu::WillowCreek/CR3000/'
sts = call(cmd, shell=True)
print 'yesterdays rsync {}'.format(sts)
datetoday = datetime.strftime(datetime.now(),'%Y%m%d')
cmd = 'rsync -qrlt /home/flux/Documents/data/CR3000/' + datetoday + '* flux.aos.wisc.edu::WillowCreek/CR3000/'
sts = call(cmd, shell=True)
print 'todays rsync {}'.format(sts)
