import os

MOC_COMMAND = 'mocp --info 2>/dev/null'

STATE_STOPPED = -1
STATE_PAUSED  = 0
STATE_PLAYING = 1

STATES = {
    'PLAY'  : STATE_PLAYING,
    'STOP'  : STATE_STOPPED,
    'PAUSE' : STATE_PAUSED
}

def get_moc_info():
    return os.popen(MOC_COMMAND).read()

def moc_output_to_dict(output):
    if not output:
        return
    return dict((key.lower(), value[1:]) for key, value in [
                line.split(':', 1) for line in output.strip('\n').split('\n')])

def get_info_dict():
    dct = moc_output_to_dict(get_moc_info())
    if dct is None:
        return
    dct['state'] = STATES[dct.pop('state')]
    return dct

def get_state():
    return get_info_dict()['state']

def is_paused():
    return get_state() == STATE_PAUSED

def is_playing():
    return get_state() == STATE_PLAYING

def is_stopped():
    return get_state() == STATE_STOPPED
