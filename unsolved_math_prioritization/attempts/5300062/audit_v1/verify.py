#!/usr/bin/env python3
"""Audit-packet integrity and independent finite-control replay only."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

if sys.flags.optimize:raise SystemExit('Optimized Python is not supported.')

def demand(ok,why):
    if not ok:raise SystemExit(why)

def run():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);a=p.parse_args()
    root=Path(__file__).resolve().parent;raw=(root/'MANIFEST.json').read_bytes()
    digest=hashlib.sha256(raw).hexdigest();demand(digest==a.expected_manifest,'External manifest anchor mismatch')
    rows=json.loads(raw)['files'];names=[r['path'] for r in rows]
    demand(len(names)==len(set(names)),'Duplicate path')
    files=set(names)|{'MANIFEST.json'};dirs=set()
    for name in files:
        q=PurePosixPath(name)
        demand(not q.is_absolute() and '..' not in q.parts and q.as_posix()==name,'Unsafe path')
        dirs.update(str(v) for v in q.parents if str(v)!='.')
    observed=set()
    for item in root.rglob('*'):
        rel=item.relative_to(root).as_posix()
        demand(not item.is_symlink(),'Symlink rejected')
        if item.is_dir():demand(rel in dirs,'Extra directory')
        elif item.is_file():observed.add(rel)
        else:raise SystemExit('Unsupported object')
    demand(observed==files,'Strict inventory mismatch')
    for r in rows:
        b=(root/r['path']).read_bytes();demand(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'File content mismatch: '+r['path'])
    replay=subprocess.run([sys.executable,'-B',str(root/'code/independent_controls.py')],capture_output=True,check=True,timeout=120)
    demand(replay.stdout==(root/'results/independent_controls.json').read_bytes(),'Independent retained controls changed')
    print(json.dumps({'audit_integrity':'PASS','external_anchor':True,'independent_controls':'EXACT_RESULT_BYTES','manifest_sha256':digest,'mathematical_verdict':json.loads((root/'RESULTS.json').read_text())['verdict']},sort_keys=True))

if __name__=='__main__':run()
