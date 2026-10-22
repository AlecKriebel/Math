#!/usr/bin/env python3
"""Strict regular-file inventory and hashes precede independent code execution."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

NAMES={'README.md','mathematical_audit.md','independent_check.py','independent_results.json',
       'replay_author.py','author_replay_results.json','public_source_verification.json',
       'audit_gate.py','acceptance_results.json','test_gate.py'}

def need(ok,msg):
    if not ok:
        raise ValueError(msg)

def main():
    root=Path(__file__).absolute().parent
    need(stat.S_ISDIR(root.lstat().st_mode),'root is not a regular directory')
    entries={p.name:p for p in root.iterdir()}
    need(set(entries)==NAMES|{'manifest.json'},'unexpected or missing inventory entry')
    for name,p in entries.items():
        need(stat.S_ISREG(p.lstat().st_mode),'nonregular entry: '+name)
    m=json.loads(entries['manifest.json'].read_text())
    need(set(m)=={'schema','files'} and m['schema']=='young-tops-independent-audit-v1','manifest schema mismatch')
    need(set(m['files'])==NAMES,'manifest inventory mismatch')
    for name,meta in m['files'].items():
        need(set(meta)=={'bytes','sha256'},'metadata keys changed: '+name)
        raw=entries[name].read_bytes()
        need(type(meta['bytes']) is int and len(raw)==meta['bytes'],'byte-count mismatch: '+name)
        need(hashlib.sha256(raw).hexdigest()==meta['sha256'],'hash mismatch: '+name)
    flags=['-B']+(['-O'] if sys.flags.optimize else [])
    out=subprocess.run([sys.executable,*flags,str(root/'independent_check.py')],cwd=root,capture_output=True,text=True,timeout=30)
    need(out.returncode==0,'independent checker failed: '+out.stderr)
    need(json.loads(out.stdout)==json.loads(entries['independent_results.json'].read_text()),'independent results differ')
    print(json.dumps({'status':'PASS','inventory_files':len(entries),'source_sha256':m['files']['independent_check.py']['sha256']},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,TypeError,KeyError,subprocess.TimeoutExpired) as error:
        print('REJECT: '+str(error),file=sys.stderr)
        sys.exit(1)
