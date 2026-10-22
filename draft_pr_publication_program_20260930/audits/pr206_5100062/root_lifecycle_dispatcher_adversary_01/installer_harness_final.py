"""Owned synthetic installer namespace; never operates actual program paths."""
import sys
from pathlib import Path
import fcntl
import hashlib
import json
import os
import stat
import types

HERE = Path(__file__).absolute().parent
SCENARIO = sys.argv[1]
TARGET = HERE.parent / 'root_program_lock_installation_01/install_program_lock206_v4.py'
SOURCE = TARGET.read_bytes()
assert len(SOURCE) == 5869
assert hashlib.sha256(SOURCE).hexdigest() == '0efd81e6b8e55335cdacefca4c44167a030806cf8013dbff040bc15dd359fe98'
assert stat.S_IMODE(TARGET.stat().st_mode) == 0o444
ROOT = HERE / 'final_installer_fixtures' / SCENARIO / 'ROOT'
P = ROOT / 'draft_pr_publication_program_20260930'
A = P / 'audits/pr206_5100062'
D = A / 'root_program_lock_installation_01'
D.mkdir(parents=True)
COPY = D / TARGET.name
COPY.write_bytes(SOURCE)
COPY.chmod(0o444)
M = types.ModuleType('synthetic_installer')
M.__file__ = str(COPY)
exec(compile(SOURCE, str(COPY), 'exec'), M.__dict__)
def pin(raw): return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def put(path, raw, mode=0o444): path.write_bytes(raw); path.chmod(mode)
protocol = {'schema':'pr206-program-view-writer-protocol-v1',
            'lock_path':'draft_pr_publication_program_20260930/ROOT_GLOBAL_FIVE_WRITER.lock',
            'lock_payload':M.EXPECTED,'every_existing_view_writer_must_hold_same_stable_inode':True,
            'never_unlink_or_replace_lock_inode':True,'Root_alone_operates_existing_views':True,
            'uncooperative_same_UID_content_CAS_guaranteed':False}
adopt = {'schema':'pr206-root-lifecycle-source-adoption-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
         'PR':206,'accepted_preparation_only':True,'program_lock_installer_pin':pin(SOURCE),
         'program_view_writer_protocol':protocol}
if SCENARIO == 'bad_protocol': protocol['never_unlink_or_replace_lock_inode'] = False
if SCENARIO == 'bad_self_pin': adopt['program_lock_installer_pin']['sha256'] = '0' * 64
raw = (json.dumps(adopt, sort_keys=True) + '\n').encode()
put(A / 'ROOT_LIFECYCLE_SOURCE_ADOPTION_01.json', raw)
if SCENARIO == 'fifo_adoption':
    (A / 'ROOT_LIFECYCLE_SOURCE_ADOPTION_01.json').unlink()
    os.mkfifo(A / 'ROOT_LIFECYCLE_SOURCE_ADOPTION_01.json', 0o444)
if SCENARIO not in ('create', 'bad_protocol', 'bad_self_pin', 'fifo_adoption', 'error_uncaught'):
    if SCENARIO == 'fifo_lock': os.mkfifo(M.LOCK, 0o444)
    elif SCENARIO == 'symlink_lock':
        put(P / 'referent', M.PAYLOAD)
        M.LOCK.symlink_to(P / 'referent')
    else: put(M.LOCK, b'bad' if SCENARIO == 'bad_payload' else M.PAYLOAD, 0o644 if SCENARIO == 'bad_mode' else 0o444)
before = M.LOCK.lstat() if os.path.lexists(M.LOCK) else None
busy_fd = None
if SCENARIO == 'busy_lock':
    busy_fd = os.open(M.LOCK, os.O_RDONLY)
    fcntl.flock(busy_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
if SCENARIO == 'existing_receipt': put(D / 'ROOT_PROGRAM_LOCK_INSTALLATION_RECEIPT.json', b'preserve me\n')
events = []
saved = {}
for name in ('chmod', 'fchmod', 'unlink', 'link'):
    saved[name] = getattr(M.os, name)
    def wrapper(*args, _name=name, **kwargs):
        events.append(_name)
        return saved[_name](*args, **kwargs)
    setattr(M.os, name, wrapper)
if SCENARIO == 'error_uncaught':
    def fail(*args, **kwargs): raise OSError('SYNTHETIC_INSTALLER_CREDENTIAL_SENTINEL_206')
    M.fcntl.flock = fail
if SCENARIO == 'fifo_swap_before_lock_open':
    original_read = M.read
    swapped = False
    def replace_after_read(path, wanted):
        global swapped
        body = original_read(path, wanted)
        if path == M.LOCK and not swapped:
            swapped = True
            M.LOCK.rename(P / 'preserved_original_lock')
            os.mkfifo(M.LOCK, 0o444)
        return body
    M.read = replace_after_read
sys.argv = [str(COPY), '--adoption-bytes', str(len(raw)), '--adoption-sha256', pin(raw)['sha256']]
if SCENARIO == 'error_uncaught':
    M.entry()
else:
    error = None
    try: M.main()
    except BaseException as exc: error = {'type':type(exc).__name__, 'message':str(exc)}
    after = M.LOCK.lstat() if os.path.lexists(M.LOCK) else None
    if busy_fd is not None:
        fcntl.flock(busy_fd, fcntl.LOCK_UN)
        os.close(busy_fd)
    released = None
    if after is not None and stat.S_ISREG(after.st_mode):
        fd = os.open(M.LOCK, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            released = True
            fcntl.flock(fd, fcntl.LOCK_UN)
        except BlockingIOError: released = False
        finally: os.close(fd)
    receipt = D / 'ROOT_PROGRAM_LOCK_INSTALLATION_RECEIPT.json'
    print(json.dumps({'scenario':SCENARIO,'exception':error,'mutations':events,
                      'before_inode':None if before is None else [before.st_dev,before.st_ino],
                      'after_inode':None if after is None else [after.st_dev,after.st_ino],
                      'mode':None if after is None else oct(stat.S_IMODE(after.st_mode)),
                      'attempt_preserved':(D/'INSTALL_ATTEMPT.json').exists(),
                      'receipt_exists':receipt.exists(),'lock_released_after_return':released,
                      'staged_files':sorted(x.name for x in D.glob('stable_program_lock_staged_*'))}, sort_keys=True))
