"""Independent offline-only containment helper. No live-service capability."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BLOCKED_EVENTS = []

def _own(path):
    if isinstance(path, int):
        return True
    return Path(os.fsdecode(path)).resolve().is_relative_to(ROOT)

def audit(event, args):
    if event.startswith(('socket.', 'http.client.', 'urllib.')) or event in ('subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.spawn'):
        BLOCKED_EVENTS.append([event, repr(args)[:250]])
        raise RuntimeError('OFFLINE_ADVERSARY_BLOCKED:' + event)
    if event == 'open':
        path, mode, flags = args
        write = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)))
        if write and not _own(path):
            BLOCKED_EVENTS.append([event, repr(args)[:250]])
            raise RuntimeError('ADVERSARY_WRITE_OUTSIDE_OWN_FOLDER')
    if event in ('os.mkdir', 'os.remove', 'os.rmdir', 'os.chmod', 'os.truncate', 'os.utime') and not _own(args[0]):
        raise RuntimeError('ADVERSARY_MUTATION_OUTSIDE_OWN_FOLDER:' + event)
    if event in ('os.rename', 'os.replace') and (not _own(args[0]) or not _own(args[1])):
        raise RuntimeError('ADVERSARY_MUTATION_OUTSIDE_OWN_FOLDER:' + event)

def install():
    sys.dont_write_bytecode = True
    sys.addaudithook(audit)
