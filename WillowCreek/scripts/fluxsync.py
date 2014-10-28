from subprocess import call
from datetime import timedelta, datetime

# run rsync for todays data
datetoday = datetime.strftime(datetime.now(),'%Y%m%d')
cmd = 'rsync -qrlt /home/flux/Documents/data/' + datetoday + ' co2.aos.wisc.edu::WillowCreek/'
sts = call(cmd, shell=True)
print cmd
print 'todays rsync {}'.format(sts)
# run rsync for previous 8 days of data to make sure all of the data was copied
for i in range(1,9):
    dateyest = datetime.strftime(datetime.now()-timedelta(days=i),'%Y%m%d')
    cmd = 'rsync -qrlt /home/flux/Documents/data/' + dateyest + ' co2.aos.wisc.edu::WillowCreek/'
    sts = call(cmd, shell=True)
    print cmd
    print 'pastdays rsync {}'.format(sts)
# rsync the Willow Creek CTN data
cmd = 'rsync -qrlt /home/flux/Documents/data/WILLOWCREEKCTN co2.aos.wisc.edu::WillowCreek/'
sts = call(cmd, shell=True)
print cmd
print 'CTN rsync {}'.format(sts)
