#!/usr/bin/env python3
"""Pinned, read-only inventory and finite-mathematics replay. No asserts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

class PacketError(Exception):
    pass

def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise PacketError('duplicate JSON key: '+key)
        out[key] = value
    return out

def reject_constant(value):
    raise PacketError('nonfinite JSON number: '+value)

def strict_json(text):
    return json.loads(text, object_pairs_hook=strict_object, parse_constant=reject_constant)

def need(ok,why):
    if not ok:raise PacketError(why)

def sha(b):return hashlib.sha256(b).hexdigest()

def validate(root,pin):
    root=root.resolve()
    need(type(pin) is str and re.fullmatch('[0-9a-f]{64}',pin) is not None,'invalid manifest pin')
    manifest=root/'MANIFEST.json'
    need(manifest.is_file() and not manifest.is_symlink(),'missing manifest or symlink')
    data=manifest.read_bytes();need(sha(data)==pin,'external manifest pin mismatch')
    m=strict_json(data)
    need(type(m) is dict and set(m)=={'schema','files'},'manifest schema')
    need(type(m['schema']) is int and m['schema']==1 and type(m['files']) is list,'manifest types')
    names=[]
    for row in m['files']:
        need(type(row) is dict and set(row)=={'path','bytes','sha256'},'entry schema')
        name=row['path'];need(type(name) is str and re.fullmatch('[A-Za-z0-9_.-]+',name) is not None and name!='MANIFEST.json','unsafe member name')
        need(name not in names,'duplicate member');names.append(name)
        need(type(row['bytes']) is int and row['bytes']>=0,'invalid byte count')
        need(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'invalid digest')
        p=root/name;need(p.is_file() and not p.is_symlink(),'missing member or symlink')
        b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'member bytes mismatch: '+name)
    actual=set()
    for p in root.iterdir():
        need(p.is_file() and not p.is_symlink(),'non-regular or unexpected directory')
        actual.add(p.name)
    need(actual==set(names)|{'MANIFEST.json'},'inventory mismatch')
    flags=[] if not sys.flags.optimize else ['-'+'O'*sys.flags.optimize]
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    run=subprocess.run([sys.executable,*flags,'-B',str(root/'exact_checks.py')],capture_output=True,env=env)
    need(run.returncode==0,'exact controls failed: '+run.stderr.decode(errors='replace')+run.stdout.decode(errors='replace'))
    need(run.stdout==(root/'CHECK_RESULTS.json').read_bytes(),'exact replay differs')
    return {'verdict':'PASS_PINNED_PACKET','files_checked':len(names),'exact_output_sha256':sha(run.stdout),'manifest_sha256':pin,'optimization_level':sys.flags.optimize}

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--manifest-sha256',required=True)
    a=p.parse_args()
    try:result=validate(a.root,a.manifest_sha256)
    except (PacketError,OSError,ValueError,TypeError,KeyError) as e:
        print(json.dumps({'verdict':'FAIL','reason':str(e)},sort_keys=True));return 1
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
