#!/usr/bin/env python3
"""Strict inventory first; only then run the hash-checked numerical support."""
import hashlib
import json
import stat
import subprocess
import sys
from pathlib import Path

EXPECTED = {'README.md','proof.md','verify.py','case.json','expected_results.json','sources.json','audit.py'}

def require(condition,message):
    if not condition:
        raise ValueError(message)

def validate(root):
    require(stat.S_ISDIR(root.lstat().st_mode),'root must be a real directory')
    entries={p.name:p for p in root.iterdir()}
    require(set(entries)==EXPECTED|{'manifest.json'},'unexpected or missing inventory entry')
    for name,p in entries.items():
        require(stat.S_ISREG(p.lstat().st_mode),f'nonregular entry: {name}')
    manifest=json.loads(entries['manifest.json'].read_text())
    require(set(manifest)=={'schema','files'},'manifest keys changed')
    require(manifest['schema']=='young-tops-safe-v1','manifest schema changed')
    require(set(manifest['files'])==EXPECTED,'manifest inventory changed')
    for name,description in manifest['files'].items():
        require(set(description)=={'sha256','bytes'},f'invalid metadata: {name}')
        raw=entries[name].read_bytes()
        require(len(raw)==description['bytes'],f'byte-count mismatch: {name}')
        require(hashlib.sha256(raw).hexdigest()==description['sha256'],f'hash mismatch: {name}')
    return manifest

def main():
    root=Path(__file__).absolute().parent
    manifest=validate(root)
    # verify.py has been hash checked above before subprocess execution.
    flags=['-B']+(['-O'] if sys.flags.optimize else [])
    run=subprocess.run([sys.executable,*flags,str(root/'verify.py')],cwd=root,capture_output=True,text=True)
    require(run.returncode==0,'supporting checker failed: '+run.stderr)
    result=json.loads(run.stdout)
    require(result==json.loads((root/'expected_results.json').read_text()),'result differs from expected')
    print(json.dumps({'status':'PASS','inventory_files':len(manifest['files'])+1,
       'verified_source_sha256':manifest['files']['verify.py']['sha256'],
       'supporting_results':result},sort_keys=True,indent=2))

if __name__=='__main__':
    try:
        main()
    except (OSError,ValueError,TypeError,KeyError) as e:
        print('REJECT: '+str(e),file=sys.stderr)
        sys.exit(1)
