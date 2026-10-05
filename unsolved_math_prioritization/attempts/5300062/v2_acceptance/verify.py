#!/usr/bin/env python3
"""Strict acceptance-packet verification, with optional frozen-input replay."""
import argparse
import hashlib
import json
from pathlib import Path,PurePosixPath
import subprocess
import sys

if sys.flags.optimize:raise SystemExit('Optimized Python is not supported.')

def need(ok,message):
    if not ok:raise SystemExit(message)

def run():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True)
    for name in ['original','v2','audit']:p.add_argument('--'+name,type=Path)
    args=p.parse_args();root=Path(__file__).resolve().parent;raw=(root/'MANIFEST.json').read_bytes()
    h=hashlib.sha256(raw).hexdigest();need(h==args.expected_manifest,'External manifest mismatch')
    entries=json.loads(raw)['files'];names=[e['path'] for e in entries];need(len(names)==len(set(names)),'Duplicate manifest paths')
    files=set(names)|{'MANIFEST.json'};dirs=set()
    for name in files:
        q=PurePosixPath(name);need(not q.is_absolute() and '..' not in q.parts and str(q)==name,'Unsafe path')
        dirs.update(str(v) for v in q.parents if str(v)!='.')
    seen=set()
    for item in root.rglob('*'):
        rel=item.relative_to(root).as_posix();need(not item.is_symlink(),'Symlink rejected')
        if item.is_dir():need(rel in dirs,'Extra directory')
        elif item.is_file():seen.add(rel)
        else:raise SystemExit('Unsupported filesystem object')
    need(seen==files,'Strict inventory mismatch')
    for e in entries:
        b=(root/e['path']).read_bytes();need((len(b),hashlib.sha256(b).hexdigest())==(e['bytes'],e['sha256']),'Content mismatch: '+e['path'])
    paths=[args.original,args.v2,args.audit];need(all(paths) or not any(paths),'Supply all three frozen-input paths together')
    replay='NOT_REQUESTED'
    if all(paths):
        cmd=[sys.executable,'-B',str(root/'code/check_delta.py')]
        for name,path in zip(['original','v2','audit'],paths):cmd+=['--'+name,str(path.resolve())]
        completed=subprocess.run(cmd,capture_output=True,check=True,timeout=120)
        need(completed.stdout==(root/'results/delta_checks.json').read_bytes(),'Bounded-delta results changed');replay='EXACT_RESULT_BYTES'
    result=json.loads((root/'ACCEPTANCE.json').read_text())
    print(json.dumps({'integrity':'PASS','external_anchor':True,'manifest_sha256':h,'bounded_delta_replay':replay,'verdict':result['verdict'],'general_problem_status':result['general_problem_status']},sort_keys=True))

if __name__=='__main__':run()
