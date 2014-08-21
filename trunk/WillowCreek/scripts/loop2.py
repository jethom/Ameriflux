import pyinotify
from archivedata import archivedata

def onChange(ev):
     archivedata(ev.pathname)
     print ev.pathname
wm = pyinotify.WatchManager()
wm.add_watch('/home/flux/Documents/incoming/', pyinotify.IN_CLOSE_WRITE, onChange)
notifier = pyinotify.Notifier(wm)
notifier.loop()
