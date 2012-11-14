#!/usr/bin/env python
import time
import moc
from lastfm.client import Client as LastFmClient

CLIENT = LastFmClient('python-moc-example')

@moc.event.register('song-changed')
def submit_to_lastfm(song_info):
    try:
        print "Scrobbling %(songtitle)s by %(artist)s..." % song_info
        CLIENT.submit({
            'artist' : song_info['artist'].decode('utf-8'),
            'title'  : song_info['songtitle'].decode('utf-8'),
            'album'  : song_info['album'],
            'length' : int(song_info['totalsec']),
            'time'   : time.gmtime()
        })
    except KeyError:
        # shouldn't happen, does anyway.
        pass

if __name__ == '__main__':
    moc.event.mainloop()
