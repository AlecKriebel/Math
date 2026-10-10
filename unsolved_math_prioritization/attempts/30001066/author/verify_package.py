#!/usr/bin/env python3
"""Check this frozen packet's exact file inventory and SHA-256 hashes."""
import hashlib
import json
from pathlib import Path
import re
import sys

EXPECTED={'README.md','proof.md','approach_audit.md','certificate.json','verify.py','test_verifier.py',
          'source_audit.json','results.json','verify_package.py'}

def need(ok,message):
    if not ok:raise ValueError(message)

def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate manifest key');out[k]=v
    return out

def main():
    root=Path(__file__).resolve().parent
    manifest=root/'MANIFEST.json'
    need(manifest.is_file() and not manifest.is_symlink(),'manifest missing or symlink')
    obj=json.loads(manifest.read_text(),object_pairs_hook=unique)
    need(type(obj) is dict and set(obj)=={'schema','version','files'},'bad manifest schema')
    need(obj['schema']=='isolated-transversal-manifest-v1' and obj['version']=='1-reconstructed','bad manifest identity')
    entries=obj['files'];need(type(entries) is list and len(entries)==len(EXPECTED),'wrong manifest count')
    seen=set()
    for row in entries:
        need(type(row) is dict and set(row)=={'path','bytes','sha256'},'bad manifest entry')
        name=row['path'];need(type(name) is str and name in EXPECTED and name not in seen,'unknown or duplicate manifest path')
        seen.add(name);p=root/name;need(p.is_file() and not p.is_symlink(),'missing or symlink payload')
        need(type(row['bytes']) is int and row['bytes']>=0,'bad byte count')
        need(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'bad digest')
        data=p.read_bytes();need(len(data)==row['bytes'],'size mismatch: '+name)
        need(hashlib.sha256(data).hexdigest()==row['sha256'],'hash mismatch: '+name)
    need(seen==EXPECTED,'incomplete manifest')
    actual=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if '__pycache__' in rel.parts:
            need(not p.is_symlink(),'symlink in bytecode cache');continue
        need(not p.is_symlink(),'unexpected symlink')
        if p.is_file():actual.add(rel.as_posix())
        elif p.is_dir():raise ValueError('unexpected directory: '+rel.as_posix())
    need(actual==EXPECTED|{'MANIFEST.json'},'unexpected or missing payload files')
    print(json.dumps({'status':'PASS','manifest_files':len(entries),'version':obj['version']},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,TypeError,KeyError,OSError) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
