#!/usr/bin/env python
import time
import mocevent
from lastfm.client import Client as LastFmClient

CLIENT = LastFmClient('python-moc-example')

@mocevent.register('song-changed')
def submit_to_lastfm(song_info):
    try:
        print "Scrobbling %(songtitle)s by %(artist)s..." % song_info
        CLIENT.submit({
            'artist' : song_info['artist'],
            'title'  : song_info['songtitle'],
            'album'  : song_info['album'],
            'length' : int(song_info['totalsec']),
            'time'   : time.gmtime()
        })
    except KeyError:
        # shouldn't happen, does anyway.
        pass

if __name__ == '__main__':
    mocevent.mainloop()
