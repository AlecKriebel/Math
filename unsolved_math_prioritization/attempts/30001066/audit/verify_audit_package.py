#!/usr/bin/env python3
"""Verify exact clean inventory and hashes of this independent audit directory."""
import hashlib
import json
from pathlib import Path
import re

FILES = {'README.md','INDEPENDENT_AUDIT.md','RESULTS.json','RESULTS_OPTIMIZED_RELOCATED.json',
         'strict_inventory.py','independent_test.py','verify_package_strict.patch','PATCH_REPLAY.json',
         'verify_corpora.py','CORPUS_REPLAY.json','SOURCES.json','ACCEPTANCE.json','verify_audit_package.py'}


def require(ok,message):
    if not ok:raise ValueError(message)


def unique(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key');out[key]=value
    return out


def main():
    root=Path(__file__).resolve().parent
    payload={}
    for p in root.iterdir():
        require(p.is_file() and not p.is_symlink(),'nested or nonregular package entry')
        payload[p.name]=p.read_bytes()
    require(set(payload)==FILES|{'AUDIT_MANIFEST.json'},'unexpected or missing package member')
    m=json.loads(payload['AUDIT_MANIFEST.json'],object_pairs_hook=unique)
    require(type(m) is dict and set(m)=={'schema','files'},'invalid manifest schema')
    require(m['schema']=='isolated-transversal-independent-audit-manifest-v1','invalid manifest identity')
    require(type(m['files']) is list and len(m['files'])==len(FILES),'wrong manifest count')
    seen=set()
    for row in m['files']:
        require(type(row) is dict and set(row)=={'path','bytes','sha256'},'bad row schema')
        name=row['path']
        require(type(name) is str and name in FILES and name not in seen,'unknown or duplicate member')
        seen.add(name)
        require(type(row['bytes']) is int and row['bytes']>=0,'invalid size')
        require(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'invalid digest')
        require(len(payload[name])==row['bytes'],'size mismatch: '+name)
        require(hashlib.sha256(payload[name]).hexdigest()==row['sha256'],'digest mismatch: '+name)
    require(seen==FILES,'missing manifest row')
    print(json.dumps({'status':'PASS','manifest_files':len(FILES),'total_files':len(payload)},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError) as exc:raise SystemExit('FAIL: '+str(exc))
