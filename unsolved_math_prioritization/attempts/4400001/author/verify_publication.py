#!/usr/bin/env python3
"""Offline packet integrity and exact-control replay; no source files needed."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def matches(data, record):
    return len(data) == record['bytes'] and digest(data) == record['sha256']

def main():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    expected = {item['path'] for item in manifest['files']}
    actual = {p.name for p in ROOT.iterdir() if p.is_file()} - {'MANIFEST.json'}
    if expected != actual:
        raise AssertionError('Unexpected or missing packet files')
    for item in manifest['files']:
        if Path(item['path']).name != item['path']:
            raise AssertionError('Nonlocal manifest path')
        data = (ROOT / item['path']).read_bytes()
        if not matches(data, item):
            raise AssertionError('Integrity mismatch: ' + item['path'])
        if data:
            mutated = bytes([data[0] ^ 1]) + data[1:]
            if matches(mutated, item) or matches(data[:-1], item):
                raise AssertionError('Integrity negative control failed')
    replay = subprocess.check_output([sys.executable, str(ROOT / 'checks.py')])
    if replay != (ROOT / 'checks.json').read_bytes():
        raise AssertionError('Exact replay output differs')
    report = json.loads(replay)
    print(json.dumps({'status': 'pass', 'files_verified': len(expected),
                      'replay_byte_identical': True,
                      'one_bit_and_truncation_controls': 'rejected for every nonempty file',
                      'assertions': report['assertions'],
                      'brute_force_words_examined': report['brute_force_words_examined']},
                     indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
