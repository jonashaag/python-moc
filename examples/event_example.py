#!/usr/bin/env python
import moc

@moc.event.register('song-changed')
def song_changed_cb(dct):
    print "Song changed to %s by %s" % (dct['songtitle'], dct['artist'])

@moc.event.register('state-changed')
def state_changed_cb(dct):
    print "State changed to", dct['state']

@moc.event.register('moc-started')
def moc_started_cb(dct):
    print "Moc was started"

@moc.event.register('moc-closed')
def moc_quitted_cb(dct):
    print "Moc was quitted"

if __name__ == '__main__':
    moc.event.mainloop()
