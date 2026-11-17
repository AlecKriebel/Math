#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only authentication of the exact supplied196-file source namespace."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

S = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23411227/sources')
def need(test, message):
    if not test:
        raise RuntimeError(message)
def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonregular source object')
    body = path.read_bytes()
    return {'path': str(path.relative_to(S)), 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'mode': stat.S_IMODE(info.st_mode)}
need(len(sys.argv) == 1, 'No arguments accepted')
final_pin = pin(S / 'SOURCE_FINAL.json')
manifest_pin = pin(S / 'SOURCE_MANIFEST.json')
need(final_pin['bytes'] == 910 and final_pin['sha256'] == '46a1f71e118fff3101c7f0af2158658847ad338172d7bd6d119ba041c8613886', 'SOURCE_FINAL identity mismatch')
need(manifest_pin['bytes'] == 60052 and manifest_pin['sha256'] == '3bd41786837658193a0258d1f1a70dc719f0e321647ed885294e9947f64a1e7b', 'SOURCE_MANIFEST identity mismatch')
manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
need(int(manifest['root_mode'], 8) == stat.S_IMODE(S.lstat().st_mode), 'Source root mode mismatch')
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
    files.extend(pin(parent / name) for name in filenames)
actual = {x['path']: x for x in files}
need(len(actual) == len(files) == 196 and len(directories) == 21, 'Source extent mismatch')
need(set(actual) == set(manifest['actual_file_paths_including_controls']), 'Source complete file set mismatch')
expected_dirs = {x['path']: int(x['mode'], 8) for x in manifest['directories']}
need({x['path']: x['mode'] for x in directories} == expected_dirs, 'Source complete directory topology/modes mismatch')
for entry in manifest['files']:
    item = actual[entry['path']]
    need(item['bytes'] == entry['bytes'] and item['sha256'] == entry.get('SHA256', entry.get('sha256')), 'Source payload byte identity mismatch')
    need(item['mode'] == int(entry['mode'], 8), 'Source payload mode mismatch')
need(set(actual) - {x['path'] for x in manifest['files']} == {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}, 'Unexpected source hash exclusions')
need(final_pin['mode'] == manifest_pin['mode'] == 0o644, 'Source control mode mismatch')
print(json.dumps({'source_root': str(S), 'all196_whole_buffers_authenticated': True, 'child_directories': 21, 'source_root_mode': stat.S_IMODE(S.lstat().st_mode), 'files': sorted(files, key=lambda x: x['path']), 'directories': sorted(directories, key=lambda x: x['path']), 'scientific_program_execution': False, 'archived_opinion_body_used_as_evidence': False}, indent=2))
