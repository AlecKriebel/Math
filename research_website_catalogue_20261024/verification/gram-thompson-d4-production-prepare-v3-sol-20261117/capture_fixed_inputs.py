#!/usr/bin/env python3
"""One passive before/after custody capture; never import or run a release helper."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/gram-thompson-d4-production-prepare-v3-sol-20261117'
FIXED = [
    P / 'verification/gram-thompson-d4-production-prepare-corrected-sol-20261117',
    P / 'verification/gram-thompson-d4-production-corrected-static-audit-sol-20261117',
    P / 'verification/gram-thompson-d4-overlay-sol-20261117',
    P / 'verification/root-gram-thompson-d4-overlay-adoption-20261117.json',
    P / 'verification/root-checkpoint-436ec-adoption-20261117.json',
]

def identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)

def snapshot():
    rows = []
    def visit(path):
        before = path.lstat()
        if any(part.is_symlink() for part in (path, *path.parents)):
            raise RuntimeError('symbolic fixed input: ' + str(path))
        row = {'path': str(path), 'mode': format(stat.S_IMODE(before.st_mode), '04o'),
               'device': before.st_dev, 'inode': before.st_ino,
               'mtime_ns': before.st_mtime_ns, 'ctime_ns': before.st_ctime_ns}
        if stat.S_ISDIR(before.st_mode):
            children = sorted(path.iterdir())
            row.update(kind='directory', empty=not children)
            rows.append(row)
            for child in children:
                visit(child)
        elif stat.S_ISREG(before.st_mode):
            descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
            try:
                if identity(before) != identity(os.fstat(descriptor)):
                    raise RuntimeError('fixed input identity changed at open')
                digest = hashlib.sha256()
                length = 0
                while True:
                    block = os.read(descriptor, 1048576)
                    if not block:
                        break
                    digest.update(block)
                    length += len(block)
                if identity(before) != identity(os.fstat(descriptor)) or length != before.st_size:
                    raise RuntimeError('fixed input changed during held read')
            finally:
                os.close(descriptor)
            row.update(kind='file', bytes=length, SHA256=digest.hexdigest(), empty=length == 0)
            rows.append(row)
        else:
            raise RuntimeError('special fixed input: ' + str(path))
        if identity(before) != identity(path.lstat()):
            raise RuntimeError('fixed input changed during snapshot')
    for root in FIXED:
        visit(root)
    return rows

def write_new(name, payload):
    raw = (json.dumps(payload, indent=2, sort_keys=True) + '\n').encode()
    path = OWN / name
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        os.fchmod(descriptor, 0o644)
        offset = 0
        while offset < len(raw):
            count = os.write(descriptor, raw[offset:])
            if count <= 0:
                raise RuntimeError('incomplete custody write')
            offset += count
        os.fsync(descriptor)
    finally:
        os.close(descriptor)

if Path(__file__).absolute() != OWN / 'capture_fixed_inputs.py':
    raise RuntimeError('exact administrative capture path required')
before_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
before = snapshot()
write_new('FIXED_INPUTS_BEFORE.json', {'UTC': before_utc, 'roots': [str(p) for p in FIXED], 'entries': before})
print('BEFORE_CAPTURE_COMPLETE; waiting for one local continuation after source review', flush=True)
if input() != 'CAPTURE_AFTER':
    raise RuntimeError('exact local continuation required; no retry')
after = snapshot()
after_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
write_new('FIXED_INPUTS_AFTER.json', {'UTC': after_utc, 'roots': [str(p) for p in FIXED], 'entries': after,
                                     'entries_identical_to_before': after == before})
if after != before:
    raise RuntimeError('fixed inputs changed; stop with both literal snapshots retained')
print('AFTER_CAPTURE_COMPLETE; all fixed rows identical; no helper executed', flush=True)
