#!/usr/bin/env python3
"""Trusted isolated bootstrap for the separately pinned corrected derivative.
Verify this entry point against the independently trusted audit receipt before use.
Requires a trusted interpreter/runtime and a quiescent filesystem, not a sandbox.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    sys.stderr.write('ISOLATED STARTUP REQUIRED: python -I -S -B ISOLATED_VERIFY.py PACKAGE MANIFEST\n')
    sys.exit(2)
import hashlib
import json
from pathlib import Path
import stat
import subprocess

MANIFEST_SHA256='fa1046d7262b9682a98007bc12ad2b33de095e692dc3ee8e94b0f77e39f1bb30'
FILES={'APPROACHES.md','EXPECTED.json','PROVENANCE.json','README.md','RESULT.md','SOURCES.json','certificate.py','controls.py','verify.py'}

def require(condition,message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result

def validate(package,manifest):
    require(stat.S_ISDIR(package.lstat().st_mode),'package root must be a real directory')
    require(stat.S_ISREG(manifest.lstat().st_mode),'manifest must be a regular nonsymlink file')
    raw=manifest.read_bytes()
    require(sha(raw)==MANIFEST_SHA256,'untrusted external manifest')
    entries=list(package.iterdir())
    require({p.name for p in entries}==FILES,'unexpected or missing package node')
    require(all(stat.S_ISREG(p.lstat().st_mode) for p in entries),'nonregular package node')
    seal=json.loads(raw,object_pairs_hook=unique)
    require(type(seal) is dict and set(seal)=={'schema','problem_id','files'},'manifest schema')
    require(type(seal['schema']) is int and seal['schema']==1,'manifest version')
    require(type(seal['problem_id']) is int and seal['problem_id']==30001707,'problem id')
    require(set(seal['files'])==FILES,'manifest inventory')
    for name in sorted(FILES):
        data=(package/name).read_bytes();entry=seal['files'][name]
        require(len(data)==entry['bytes'] and sha(data)==entry['sha256'],'member identity: '+name)
    return sha(raw)

def main():
    require(stat.S_ISREG(Path(__file__).absolute().lstat().st_mode),'bootstrap entry point must be a regular nonsymlink file')
    require(len(sys.argv)==3,'usage: ISOLATED_VERIFY.py PACKAGE MANIFEST')
    package=Path(sys.argv[1]).absolute();manifest=Path(sys.argv[2]).absolute()
    before=validate(package,manifest)
    args=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+[str(package/'verify.py'),str(manifest)]
    result=subprocess.run(args,cwd='/tmp',capture_output=True,text=True,timeout=60,check=False)
    require(result.returncode==0 and not result.stderr,'pinned verifier failed')
    output=json.loads(result.stdout,object_pairs_hook=unique)
    require(output.get('verified') is True,'verification output')
    require(validate(package,manifest)==before,'post-execution identity')
    return {'accepted':True,'isolated_startup':True,'full_inventory_pinned_before_package_execution':True,'package_files':len(FILES),'manifest_sha256':before,'verifier_result':output,'scope':'corrected integrity and exact finite checks only; no general-conjecture resolution'}

if __name__=='__main__':
    try:
        print(json.dumps(main(),sort_keys=True,indent=2))
    except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired) as error:
        print('BOOTSTRAP REJECTED: '+str(error),file=sys.stderr)
        sys.exit(1)
