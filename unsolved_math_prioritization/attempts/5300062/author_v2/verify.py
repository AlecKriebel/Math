#!/usr/bin/env python3
"""Integrity and retained-control replay. This does not prove the mathematics."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

if sys.flags.optimize:
    raise SystemExit('Run with unoptimized Python; optimization is not supported.')


def fail(message):
    raise SystemExit(message)


def run():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected-manifest')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    raw=(root/'MANIFEST.json').read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if args.expected_manifest is not None and args.expected_manifest != digest:
        fail('Externally supplied manifest digest mismatch')
    manifest=json.loads(raw)
    entries=manifest['files']
    names=[x['path'] for x in entries]
    if len(names)!=len(set(names)):
        fail('Duplicate manifest entry')
    allowed=set(names)|{'MANIFEST.json'}
    for name in allowed:
        pp=Path(name)
        if pp.is_absolute() or '..' in pp.parts or str(pp)!=name:
            fail('Unsafe manifest path')
    expected_dirs={str(Path(name).parent) for name in allowed if str(Path(name).parent)!='.'}
    for name in tuple(expected_dirs):
        expected_dirs.update(str(p) for p in Path(name).parents if str(p)!='.')
    seen=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix()
        if p.is_symlink():
            fail('Symlink rejected')
        if p.is_dir():
            if rel not in expected_dirs:
                fail('Unexpected directory: '+rel)
        elif p.is_file():
            seen.add(rel)
        else:
            fail('Unsupported filesystem object')
    if seen!=allowed:
        fail('Strict inventory mismatch')
    for item in entries:
        b=(root/item['path']).read_bytes()
        if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256']:
            fail('Content mismatch: '+item['path'])
    proc=subprocess.run([sys.executable,'-B',str(root/'code/check_controls.py')],capture_output=True,check=True)
    if proc.stdout!=(root/'results/controls.json').read_bytes():
        fail('Retained controls did not reproduce exactly')
    print(json.dumps({'integrity':'PASS','controls_replay':'EXACT_BYTES','manifest_sha256':digest,'external_anchor_supplied':args.expected_manifest is not None,'mathematical_scope':'Unrefereed authored partial, not formal verification'},sort_keys=True))

if __name__=='__main__':
    run()
