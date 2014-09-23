from subprocess import call
from datetime import timedelta, datetime

# run rsync for yesterday to make sure all of the data was copied
dateyest = datetime.strftime(datetime.now()-timedelta(days=1),'%Y%m%d')
cmd = 'rsync -qrlt /home/flux/Documents/data/' + dateyest + ' co2.aos.wisc.edu::WillowCreek/'
sts = call(cmd, shell=True)
print 'yesterdays rsync {}'.format(sts)
datetoday = datetime.strftime(datetime.now(),'%Y%m%d')
cmd = 'rsync -qrlt /home/flux/Documents/data/' + datetoday + ' co2.aos.wisc.edu::WillowCreek/'
sts = call(cmd, shell=True)
print 'todays rsync {}'.format(sts)
# rsync the Willow Creek CTN data
cmd = 'rsync -qrlt /home/flux/Documents/data/WILLOWCREEKCTN co2.aos.wisc.edu::WillowCreek/'
sts = call(cmd, shell=True)
print 'CTN rsync {}'.format(sts)
