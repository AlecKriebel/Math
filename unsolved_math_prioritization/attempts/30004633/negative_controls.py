#!/usr/bin/env python3
"""Local package corruption controls; creates and removes temporary copies."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
FLAGS = (['-I'] if sys.flags.isolated else []) + (['-O'] if sys.flags.optimize else [])

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def alter_manifest(directory, filename):
    path = directory / 'PUBLICATION_MANIFEST.json'
    manifest = json.loads(path.read_text())
    for row in manifest['files']:
        if row['file'] == filename:
            data = (directory / filename).read_bytes()
            row.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    path.write_text(json.dumps(manifest))

def mutate(directory, case):
    if case == 'missing-file':
        (directory / 'README.md').unlink()
    elif case == 'extra-file':
        (directory / 'unexpected.txt').write_text('negative control')
    elif case == 'altered-proof':
        path = directory / 'APPROACH_02_COMPACT_DOMAIN.md'
        path.write_bytes(path.read_bytes() + b'\nmutation\n')
    elif case == 'malformed-manifest':
        (directory / 'PUBLICATION_MANIFEST.json').write_text('{}')
    elif case == 'corrupted-archive':
        name = 'POROUS_MEDIUM_30004633_AUTHOR_CONTINUATION_A2_A5.zip'
        path = directory / name
        data = bytearray(path.read_bytes()); data[len(data)//2] ^= 1; path.write_bytes(data)
        alter_manifest(directory, name)
    elif case == 'tampered-proof-pin':
        name = 'APPROACH_03_REGULAR_FREE_BOUNDARIES.md'
        path = directory / name
        path.write_bytes(path.read_bytes() + b'\nmutation\n')
        alter_manifest(directory, name)
    elif case == 'tampered-audit-pin':
        name = 'AUDIT_MANIFEST.json'
        path = directory / name
        audit = json.loads(path.read_text()); audit['inputs'][0]['sha256'] = '0'*64
        path.write_text(json.dumps(audit)); alter_manifest(directory, name)
    else:
        raise RuntimeError('unknown corruption case')

def main():
    cases = ['missing-file', 'extra-file', 'altered-proof', 'malformed-manifest', 'corrupted-archive', 'tampered-proof-pin', 'tampered-audit-pin']
    with tempfile.TemporaryDirectory(prefix='porous-medium-controls-') as temporary:
        for case in cases:
            directory = Path(temporary) / case
            shutil.copytree(ROOT, directory, ignore=shutil.ignore_patterns('__pycache__'))
            mutate(directory, case)
            run = subprocess.run([sys.executable, *FLAGS, str(directory / 'verify_publication.py'), '--integrity-only'], cwd=temporary, capture_output=True, text=True, timeout=120)
            require(run.returncode != 0 and 'PASS' not in run.stdout, 'corruption not rejected: ' + case)
    print(json.dumps({'status': 'PASS', 'publication_corruptions_detected': cases, 'count': len(cases)}, sort_keys=True))

if __name__ == '__main__':
    main()
