#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One read-only close: exact source, frozen INITIAL, and finite raw primary references."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

R = Path(__file__).resolve().parent
S = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23411227/sources')
def need(test, message):
    if not test:
        raise RuntimeError(message)
def sha(body):
    return hashlib.sha256(body).hexdigest()
def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonregular guarded file')
    body = path.read_bytes()
    return {'bytes': len(body), 'sha256': sha(body), 'mode': stat.S_IMODE(info.st_mode)}
need(len(sys.argv) == 1, 'No arguments accepted')
seal_path = R / 'INITIAL_SEAL.json'
seal_pin = pin(seal_path)
need(seal_pin == {'bytes': 7353, 'sha256': '9824af712729e883f8871d54fe50d9fb616ccd8c06e57874047bd818b69962e9', 'mode': 0o644}, 'Initial seal changed')
seal = json.loads(seal_path.read_bytes())
for item in seal['payloads']:
    need(pin(R / item['path']) == {'bytes': item['bytes'], 'sha256': item['sha256'], 'mode': int(item['mode'], 8)}, 'Initial payload changed')
for item in seal['directories']:
    info = (R / item['path']).lstat()
    need(stat.S_ISDIR(info.st_mode) and stat.S_IMODE(info.st_mode) == int(item['mode'], 8), 'Initial directory mode changed')
baseline = json.loads((R / 'SOURCE_CUSTODY.json').read_bytes())
need(stat.S_IMODE(S.lstat().st_mode) == baseline['source_root_mode'], 'Source root mode changed')
files, directories = [], []
for here, names, filenames in os.walk(S, followlinks=False):
    names.sort()
    filenames.sort()
    parent = Path(here)
    for name in names:
        path = parent / name
        info = path.lstat()
        need(stat.S_ISDIR(info.st_mode), 'Source symlink/special directory')
        directories.append({'path': str(path.relative_to(S)), 'mode': stat.S_IMODE(info.st_mode)})
    for name in filenames:
        path = parent / name
        files.append({'path': str(path.relative_to(S)), **pin(path)})
files.sort(key=lambda x: x['path'])
directories.sort(key=lambda x: x['path'])
need(files == baseline['files'] and directories == baseline['directories'], 'Whole source bytes/modes/topology changed')
sources = json.loads((R / 'PRIMARY_SOURCES.json').read_bytes())['raw_bodies']
need(len(sources) == 10, 'Unexpected primary reference extent')
for item in sources:
    need(pin(Path(item['path'])) == {'bytes': item['bytes'], 'sha256': item['sha256'], 'mode': int(item['mode'], 8)}, 'Raw primary reference changed')
print(json.dumps({'source_files': len(files), 'source_child_directories': len(directories), 'source_whole_unchanged': True, 'INITIAL_files_unchanged': len(seal['payloads']) + 1, 'INITIAL_old_directory_modes_unchanged': True, 'raw_primary_bodies_unchanged': len(sources), 'complete_source_files': files, 'complete_source_directories': directories, 'exact_initial_seal': seal_pin, 'scientific_execution_by_this_helper': False}, indent=2))
