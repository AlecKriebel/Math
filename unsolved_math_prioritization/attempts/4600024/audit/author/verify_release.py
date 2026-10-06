#!/usr/bin/env python3
"""Fail-closed inventory, followed by isolated execution of verified text code."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED = {'README.md','PROOF.md','APPROACHES.md','PROVENANCE.json','STATUS.json',
            'verify_math.py','MATH_RESULTS.json','verify_release.py','MANIFEST.json'}

def fail(message):
    raise RuntimeError(message)

def main():
    actual = set()
    for path in ROOT.iterdir():
        mode = path.lstat().st_mode
        if not stat.S_ISREG(mode):
            fail('nonregular node forbidden: '+path.name)
        actual.add(path.name)
    if actual != EXPECTED:
        fail('inventory mismatch: '+repr(sorted(actual ^ EXPECTED)))
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    if set(manifest) != {'schema','files'} or manifest['schema'] != 1:
        fail('invalid manifest schema')
    if set(manifest['files']) != EXPECTED - {'MANIFEST.json'}:
        fail('invalid manifest file inventory')
    for name, info in manifest['files'].items():
        if set(info) != {'bytes','sha256'}:
            fail('invalid file metadata: '+name)
        data = (ROOT/name).read_bytes()
        if len(data)!=info['bytes'] or hashlib.sha256(data).hexdigest()!=info['sha256']:
            fail('hash or size mismatch: '+name)
    proc = subprocess.run([sys.executable,'-I','-B',str(ROOT/'verify_math.py')],
                          cwd=ROOT,capture_output=True,check=True)
    expected = (ROOT/'MATH_RESULTS.json').read_bytes()
    if proc.stdout != expected:
        fail('mathematical replay differs from frozen expected bytes')
    result=json.loads(proc.stdout)
    print(json.dumps({'status':'PASS','verified_regular_files':len(EXPECTED),
                      'mathematical_checks':result['checks'],
                      'scope':'author packet integrity and finite controls only'},sort_keys=True))

if __name__=='__main__':
    main()
