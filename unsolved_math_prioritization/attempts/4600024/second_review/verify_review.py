#!/usr/bin/env python3
"""Fail-closed inventory, then isolated source-only replay."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED = {'README.md', 'REVIEW.md', 'METADATA.json', 'checks.py', 'RESULTS.json',
            'tamper_checks.py', 'TAMPER_RESULTS.json', 'verify_review.py', 'MANIFEST.json'}

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def main():
    need(sys.argv[1:] in ([], ['--inventory-only']), 'unknown arguments')
    actual = set()
    for p in ROOT.iterdir():
        need(stat.S_ISREG(p.lstat().st_mode), 'nonregular node: '+p.name)
        actual.add(p.name)
    need(actual == EXPECTED, 'incorrect file inventory')
    manifest = json.loads((ROOT/'MANIFEST.json').read_bytes())
    need(isinstance(manifest, dict) and set(manifest) == {'schema', 'files'}, 'manifest schema')
    need(type(manifest['schema']) is int and manifest['schema'] == 1, 'schema version')
    files = manifest['files']
    need(isinstance(files, dict) and set(files) == EXPECTED-{'MANIFEST.json'}, 'manifest inventory')
    for name, info in files.items():
        need(isinstance(info, dict) and set(info) == {'bytes', 'sha256'}, 'file metadata')
        need(type(info['bytes']) is int and info['bytes'] >= 0, 'size type')
        need(isinstance(info['sha256'], str) and len(info['sha256']) == 64, 'digest type')
        data = (ROOT/name).read_bytes()
        need(len(data) == info['bytes'] and hashlib.sha256(data).hexdigest() == info['sha256'],
             'digest mismatch: '+name)
    if sys.argv[1:] == ['--inventory-only']:
        print('PASS inventory')
        return
    for optimized in (False, True):
        flags = ['-I', '-B'] + (['-O'] if optimized else [])
        for script, expected in [('checks.py', 'RESULTS.json'), ('tamper_checks.py', 'TAMPER_RESULTS.json')]:
            result = subprocess.run([sys.executable, *flags, str(ROOT/script)],
                                    cwd='/tmp', capture_output=True, check=True)
            need(result.stdout == (ROOT/expected).read_bytes(), 'replay mismatch: '+script)
    result = json.loads((ROOT/'RESULTS.json').read_bytes())
    tamper = json.loads((ROOT/'TAMPER_RESULTS.json').read_bytes())
    print(json.dumps({'status': 'PASS', 'regular_files': len(EXPECTED),
                      'finite_checks': result['checks'], 'inventory_controls': tamper['controls'],
                      'modes': ['ordinary', 'optimized'],
                      'mathematical_disposition': 'See REVIEW.md; not formal verification'}, sort_keys=True))

if __name__ == '__main__':
    main()
