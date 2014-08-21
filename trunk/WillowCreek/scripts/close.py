#!/usr/bin/env python

import os, sys
from pyinotify import WatchManager, Notifier, ProcessEvent, EventsCodes, IN_CLOSE_WRITE,IN_CLOSE_NOWRITE

def Monitor(path):
    class PClose(ProcessEvent):
        def process_IN_CLOSE(self, event):
            f = event.name and os.path.join(event.path, event.name) or event.path
            print 'close event: ' + f

    wm = WatchManager()
    notifier = Notifier(wm, PClose())
    wm.add_watch(path, IN_CLOSE_WRITE|IN_CLOSE_NOWRITE)

    try:
        while 1:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        return


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        print 'use: %s dir' % sys.argv[0]
    else:
        Monitor(path)
