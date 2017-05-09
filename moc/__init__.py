#!/usr/bin/env python
from __future__ import with_statement
import os
import subprocess
import input_helper as ih
from glob import glob

STATE_NOT_RUNNING = -1
STATE_STOPPED = 0
STATE_PAUSED  = 1
STATE_PLAYING = 2

STATES = {
    'PLAY'  : STATE_PLAYING,
    'STOP'  : STATE_STOPPED,
    'PAUSE' : STATE_PAUSED
}

AUDIO_EXTENSIONS = (
    '.mp3'
)

class MocError(Exception):
    """ Raised if executing a command failed """

class MocNotRunning(MocError):
    """ Raised if a command failed because the moc server does not run """

# Helper functions
def _quote_file_args(files):
    if isinstance(files, str):
        files = [files]
    quoted = []
    for file in files:
        if os.path.exists(file) or file.startswith(('http://', 'ftp://')):
            # MOC only supports HTTP and FTP, not even HTTPS.
            # (See `is_url` in `files.c`.)
            quoted.append('"%s"' % file)
        else:
            pass
    return ' '.join(quoted)

def _exec_command(command, parameters=''):
    cmd = subprocess.Popen(
            ['mocp --%s %s' %(command, parameters)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, close_fds=True
    )
    stdout, stderr = cmd.communicate()
    if cmd.returncode:
        errmsg = stderr.strip().decode('utf-8')
        if 'server is not running' in errmsg:
            raise MocNotRunning(errmsg)
        else:
            raise MocError(errmsg)
    return stdout

def start_server():
    """ Starts the moc server. """
    _exec_command('server')

def stop_server():
    """ Shuts down the moc server.  """
    _exec_command('exit')

def get_state():
    """
    Returns the current state of moc.

    (``STATE_STOPPED``, ``STATE_PAUSED`` or  ``STATE_PLAYING``)
    """
    try:
        return get_info_dict()['state']
    except MocNotRunning:
        return STATE_NOT_RUNNING

def is_paused():
    return get_state() == STATE_PAUSED

def is_playing():
    return get_state() == STATE_PLAYING

def is_stopped():
    return get_state() == STATE_STOPPED

def play():
    """ Restarts playback after it's been stopped. """
    _exec_command('play')

def stop():
    """ Stops current playback. """
    _exec_command('stop')

def toggle_pause():
    """
    Toggles playback: If playback was paused, resume; if not, pause.
    """
    _exec_command('toggle-pause')

def next():
    """ Plays next track. """
    _exec_command('next')

def previous():
    """
    Plays previous track.
    """
    _exec_command('previous')


def find_audio(*paths):
    """Return a list of audio files from the given paths

    - paths: filename and dirname globs that either are audio files, or contain
      audio files
    """
    visited = set()
    audio_files = list()

    for path in paths:
        abspath = os.path.abspath(os.path.expanduser(path))
        abspaths = glob(abspath)
        if os.path.isdir(abspath) and abspath not in abspaths:
            abspaths.append(abspath)
        for abspath in abspaths:
            if os.path.isdir(abspath) and abspath not in visited:
                for dirpath, dirnames, filenames in os.walk(abspath):
                    visited.add(dirpath)
                    audio_files.extend([
                        repr(os.path.join(dirpath, f))
                        for f in sorted(filenames)
                        if f.lower().endswith(AUDIO_EXTENSIONS)
                    ])
            elif (
                os.path.isfile(abspath)
                and abspath.lower().endswith(AUDIO_EXTENSIONS)
                and abspath not in audio_files
            ):
                audio_files.append(repr(abspath))
    return audio_files


def find_and_play(*paths):
    """Find all audio files at the given paths and play

    - paths: filename and dirname globs that either are audio files, or contain
      audio files
    """
    if get_state() == STATE_NOT_RUNNING:
        start_server()
    if get_state() in (STATE_PLAYING, STATE_PAUSED):
        stop()
    _exec_command('playit', ' '.join(find_audio(*paths)))


def quickplay(files):
    """
    Plays the given `files` without modifying moc's playlist.

    Doesn't care if any of the `files` can not be found.
    """
    _exec_command('playit', _quote_file_args(files))


def _moc_output_to_dict(output):
    """
    Converts the given moc `output` into a dictonary. If the output is empty,
    return ``None`` instead.

    The conversion works as follows:
        For each line:
            split the line on first match of a ":"
            where the first part of the result is the key and the second part
            is the value.
            lowercase the key and add the key/value to the dict.
    """
    if not output:
        return
    elif type(output) == bytes:
        output = output.decode('utf-8')
    lines = output.strip('\n').split('\n')
    if 'Running the server...' in lines[0]:
        del lines[0]
    return dict((key.lower(), value[1:]) for key, value in
                (line.split(':', 1) for line in lines))

def get_info_dict():
    """
    Returns a dictionary with information about the track moc currently plays.
    If moc's not playing any track right now (stopped/shut down), returns ``None``.

    The returned dict looks like this::

        {'album'       : 'Whoracle',
         'artist'      : 'In Flames',
         'avgbitrate'  : '320kbps',
         'bitrate'     : '320kbps',
         'currentsec'  : '10',
         'currenttime' : '00:10',
         'file'        : '.../In Flames/Whoracle/In Flames - The Hive.mp3',
         'rate'        : '44kHz',
         'songtitle'   : 'The Hive',
         'state'       : 2, # STATE_PLAYING
         'timeleft'    : '03:53',
         'title'       : '5 In Flames - The Hive (Whoracle)',
         'totalsec'    : '243',
         'totaltime'   : '04:03'}
    """
    dct = _moc_output_to_dict(_exec_command('info'))
    if dct is None:
        return
    dct['state'] = STATES[dct['state']]
    return dct

def info_string(template='{currenttime} ({currentsec}) of {totaltime} into {file}'):
    """Return a formatted string from current info in `get_info_dict()` call

    Available vars are keys returned by `get_info_dict()`: album artist
    avgbitrate bitrate currentsec currenttime file rate songtitle state
    timeleft title totalsec totaltime
    """
    info_dict = get_info_dict()
    result = ''
    try:
        result = template.format(**info_dict)
    except KeyError as e:
        if not info_dict:
            result = 'No file'
        else:
            result = repr(e)
    return result

def volume_up(level=5):
    """
    """
    _exec_command('volume', '+%d' % level)

def volume_down(level=5):
    """
    """
    _exec_command('volume', '-%d' % level)

def seek(n):
    """
    Moves the current playback seed forward by `n` seconds
    (or backward if `n` is negative).
    """
    _exec_command('seek', n)

def go(timestamp):
    """Jump to timestamp in the current file and play (wrapper to 'seek')

    - timestamp: a string in one the following formats: '3h4m5s', '2h15s', '47m',
      '300s', '3:04:05', '2:00:15', '47:00', '300'
    """
    seconds = ih.timestamp_to_seconds(timestamp)
    if seconds is None:
        return

    if get_state() == STATE_PAUSED:
        toggle_pause()
    seek(seconds - int(get_info_dict()['currentsec']))

def _controls(what):
    makefunc = lambda action: lambda: _exec_command(action, what) and None or None
    return (makefunc(action) for action in ('on', 'off', 'toggle'))

toggle_repeat   = _controls('repeat')
toggle_shuffle  = _controls('shuffle')
toggle_autonext = _controls('autonext')

def playlist_get(mocdir=None):
    """
    Returns the current playlist or ``None`` if none does exist.

    The returned list has the following format::

        [(title, absolute_path_of_file), (title, absolute_path_of_file), ...]

    Contributed by Robin Wittler. Thanks!
    """
    if not mocdir:
        mocdir = os.path.expanduser('~/.moc')

    playlist_path = os.path.join(mocdir, 'playlist.m3u')

    if not os.path.exists(playlist_path):
        return None

    with open(playlist_path, 'r') as playlist_file:
        # read the first two lines of the file:
        header = [playlist_file.next() for i in xrange(2)]
        # the first two lines must be the m3u format id
        # and the serial for this playlist, e.g.
        #     #EXTM3U
        #     #MOCSERIAL: n
        # If not, it is not a moc created playlist
        # and we return None.
        if not header[0].startswith('#EXTM3U') or \
           not header[1].startswith('#MOCSERIAL'):
            return None

        # ok, everything seems to be fine with this file,
        # go on putting the rest of the content into our
        # own fancy datastructures:
        playlist = []
        for line in playlist_file:
            # Every entry for a song counts two lines:
            #     #EXTINF:n,song_title
            #     absolute_file_path
            title = line.split(',', 1)[1]
            path = playlist_file.next()
            playlist.append((title.strip('\r\n'), path.strip('\r\n')))
        return playlist

def playlist_append(files_directories_playlists):
    """
    Appends the files, directories and/or in `files_directories_playlists` to
    moc's playlist.
    """
    _exec_command('append', _quote_file_args(files_directories_playlists))

def playlist_clear():
    """ Clears moc's playlist. """
    _exec_command('clear')
