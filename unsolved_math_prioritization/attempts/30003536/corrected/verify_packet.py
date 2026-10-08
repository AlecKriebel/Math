#!/usr/bin/env python3
"""Strict pinned-manifest and deterministic-check replay; writes no packet files."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

class VerificationError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def strict_json(data):
    def pairs(items):
        result = {}
        for k,v in items:
            require(k not in result, 'duplicate JSON key')
            result[k] = v
        return result
    def nonfinite(value):
        raise VerificationError('nonfinite JSON value')
    return json.loads(data, object_pairs_hook=pairs, parse_constant=nonfinite)

def verify(root, pin):
    require(re.fullmatch('[0-9a-f]{64}',pin) is not None,'invalid manifest pin')
    manifest_path=root/'MANIFEST.json'
    require(not manifest_path.is_symlink(),'manifest symlink forbidden')
    raw=manifest_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==pin,'manifest pin mismatch')
    manifest=strict_json(raw)
    require(type(manifest) is dict and set(manifest)=={'format','files'},'manifest shape')
    require(manifest['format']=='riesz-author-packet-v1','manifest format')
    rows=manifest['files']
    require(type(rows) is list and rows,'manifest file list')
    names=set()
    for row in rows:
        require(type(row) is dict and set(row)=={'path','bytes','sha256'},'manifest row shape')
        name=row['path']
        require(type(name) is str and name and '\\' not in name,'invalid path')
        rel=PurePosixPath(name)
        require(not rel.is_absolute() and len(rel.parts)==1 and rel.parts[0] not in ('.','..'), 'unsafe path')
        require(name != 'MANIFEST.json' and name not in names,'duplicate or self path')
        names.add(name)
        require(type(row['bytes']) is int and row['bytes']>=0,'invalid byte count')
        require(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'invalid file digest')
        path=root/name
        require(path.is_file() and not path.is_symlink(),'missing, nonfile, or symlink payload')
        data=path.read_bytes()
        require(len(data)==row['bytes'],'byte count mismatch: '+name)
        require(hashlib.sha256(data).hexdigest()==row['sha256'],'digest mismatch: '+name)
    entries={p.name for p in root.iterdir()}
    require(entries==names|{'MANIFEST.json'},'complete inventory mismatch')
    require({'REPORT.md','CLAIMS.json','check_math.py','CHECKS.expected.json'}.issubset(names),'required payload missing')
    flags=['-I','-B']+(['-O'] if sys.flags.optimize==1 else ['-OO'] if sys.flags.optimize>=2 else [])
    completed=subprocess.run([sys.executable,*flags,str(root/'check_math.py')],capture_output=True,check=False)
    require(completed.returncode==0,'mathematical control subprocess failed')
    require(completed.stdout==(root/'CHECKS.expected.json').read_bytes(),'control output is not byte-identical')
    require(not completed.stderr,'unexpected checker stderr')
    return {'result':'PASS','files_verified':len(names),'manifest_sha256':pin,
            'control_output':'byte-identical','packet_writes':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expected-manifest-sha256',required=True)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    a=p.parse_args()
    try:
        result=verify(a.root.resolve(),a.expected_manifest_sha256)
    except (VerificationError,ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({'result':'FAIL','error':str(exc)},sort_keys=True))
        return 2
    print(json.dumps(result,sort_keys=True,indent=2))
    return 0

if __name__=='__main__':
    sys.exit(main())
