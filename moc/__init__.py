import os
import input_helper as ih
import bg_helper as bh
from glob import glob
from time import sleep


AUDIO_EXTENSIONS = (
    '.mp3'
)


def _start_jack():
    """Start jackd if on a Mac and it's not running"""
    bh.SimpleBackgroundTask('[[ $(uname) == "Darwin" ]] && [[ -z "$(ps aux | grep jackd | grep -v grep)" ]] && jackd -d coreaudio &>/dev/null')


def rm_pid_and_kill_jack():
    bh.SimpleBackgroundTask("rm ~/.moc/pid 2>/dev/null")
    bh.SimpleBackgroundTask("for pid in $(ps aux | grep jackd | awk '{print $2}'); do kill $pid &>/dev/null; done")
    sleep(.5)
    bh.SimpleBackgroundTask("for pid in $(ps aux | grep jackd | awk '{print $2}'); do kill -9 $pid &>/dev/null; done")


def start_server(n=1, max_calls=3):
    output = bh.run_output('mocp --server', timeout=2)
    if 'Server is already running' in output:
        pass
    elif 'No valid sound driver' in output:
        _start_jack()
        sleep(.5)
        print(bh.run_output('mocp --server', timeout=2))
    elif 'It seems that the server is already running' in output:
        rm_pid_and_kill_jack()
        if n < max_calls:
            start_server(n + 1)
        else:
            print(output)
            print('\nstart_server func was called {} times'.format(n))
    elif output:
        print(output)


def get_info_dict():
    output = bh.run_output('mocp --info', timeout=2)
    return dict([
        (k.lower(), v.strip())
        for k, v in [
            line.split(':', 1)
            for line in output.split('\n')
            if line
        ]
    ])


def info_string(template='{currenttime} ({currentsec}) of {totaltime} into {file}'):
    make_string = ih.get_string_maker(template)
    current_info = get_info_dict()
    if 'fatal_error' in current_info:
        return ''
    elif 'timeout' in current_info:
        return ''
    elif current_info.get('state') == 'STOP':
        return ''
    return make_string(current_info)


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
    found = ' '.join(find_audio(*paths))
    if not found:
        print('No files found matching {}'.format(repr(paths)))
        return
    start_server()
    output = bh.run_output('mocp --playit {}'.format(found), timeout=10)
    if output:
        print(output)


def find_select_and_play(*paths):
    """Find all audio files at the given paths, select interactively, and play

    - paths: filename and dirname globs that either are audio files, or contain
      audio files
    """
    results = find_audio(*paths)
    if results:
        selected = ih.make_selections(
            results,
            wrap=False
        )
        if selected:
            start_server()
            output = bh.run_output(
                'mocp --playit {}'.format(' '.join(selected)),
                timeout=10
            )
            if output:
                print(output)
    else:
        print('No files found matching {}'.format(repr(paths)))


def toggle_pause():
    output = bh.run_output('mocp --toggle-pause', timeout=2)
    if 'server is not running' in output:
        start_server()
    elif output:
        print(output)


def seek(n):
    """Move forward or backwaard by n seconds"""
    output = bh.run_output('mocp --seek {}'.format(n), timeout=2)
    if 'server is not running' in output:
        start_server()
    elif output:
        print(output)


def go(timestamp):
    """Jump to timestamp in the current file and play (wrapper to 'seek')

    - timestamp: a string in one the following formats: '3h4m5s', '2h15s', '47m',
      '300s', '3:04:05', '2:00:15', '47:00', '300'
    """
    seconds = ih.timestamp_to_seconds(timestamp)
    if seconds is None:
        return
    if get_info_dict().get('state') == 'PAUSE':
        toggle_pause()

    output = bh.run_output('mocp --jump {}s'.format(seconds), timeout=2)
    if 'server is not running' in output:
        start_server()
    elif 'Segmentation fault' in output:
        seek(seconds - int(get_info_dict()['currentsec']))
    elif output:
        print(output)


def volume_up(n=5):
    output = bh.run_output('mocp --volume +{}'.format(n), timeout=2)
    if 'server is not running' in output:
        start_server()
    elif output:
        print(output)


def volume_down(n=5):
    output = bh.run_output('mocp --volume -{}'.format(n), timeout=2)
    if 'server is not running' in output:
        start_server()
    elif output:
        print(output)


def volume(n):
    output = bh.run_output('mocp --volume {}'.format(n), timeout=2)
    if 'server is not running' in output:
        start_server()
    elif output:
        print(output)


def next():
    output = bh.run_output('mocp --next', timeout=2)
    if 'server is not running' in output:
        start_server()
    elif output:
        print(output)


def previous():
    output = bh.run_output('mocp --previous', timeout=2)
    if 'server is not running' in output:
        start_server()
    elif output:
        print(output)


def stop():
    output = bh.run_output('mocp --stop', timeout=2)
    if 'server is not running' in output:
        pass
    elif output:
        print(output)


def stop_server():
    output = bh.run_output('mocp --exit', timeout=2)
    if 'server is not running' in output:
        pass
    elif output:
        print(output)
    else:
        rm_pid_and_kill_jack()
