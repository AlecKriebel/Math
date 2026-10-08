#!/usr/bin/env python3
"""Verify an externally pinned local packet and replay exact finite checks."""
import argparse, hashlib, json, pathlib, subprocess, sys

def require(ok,msg):
    if not ok: raise ValueError(msg)

def sha(data):return hashlib.sha256(data).hexdigest()

def verify(root,pin):
    root=pathlib.Path(root)
    raw=(root/'MANIFEST.json').read_bytes()
    require(sha(raw)==pin,'manifest digest mismatch')
    m=json.loads(raw)
    require(m.get('schema')==1,'unknown schema')
    records=m['files']
    wanted={r['path'] for r in records}
    require(len(wanted)==len(records),'duplicate paths')
    require(all('/' not in name and name not in ('.','..','MANIFEST.json') for name in wanted),'unsafe path')
    actual=set()
    for p in root.iterdir():
        require(not p.is_symlink(),'symlink rejected')
        require(p.is_file(),'nonregular entry rejected')
        actual.add(p.name)
    require(actual==wanted|{'MANIFEST.json'},'exact inventory mismatch')
    for r in records:
        b=(root/r['path']).read_bytes()
        require(len(b)==r['bytes'] and sha(b)==r['sha256'],'file mismatch: '+r['path'])
    expected=(root/'CHECK_RESULTS.json').read_bytes()
    for flags in ([],['-O']):
        run=subprocess.run([sys.executable,'-I',*flags,str((root/'checks.py').resolve()),'--self-test'],capture_output=True,check=True)
        require(run.stdout==expected,'mathematical replay mismatch')
    return {'status':'PASS','manifest_sha256':pin,'files':len(records),'normal_replay':'PASS','optimized_replay':'PASS','scope':'inventory and exact finite checks only; not a proof or source-authentication certificate'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest_sha256');p.add_argument('--root',default=str(pathlib.Path(__file__).resolve().parent));a=p.parse_args()
    print(json.dumps(verify(a.root,a.manifest_sha256),indent=2,sort_keys=True))
