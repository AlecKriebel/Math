#!/usr/bin/env python3
"""Replay unchanged author and audit programs in their final repository layout."""
import json
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parent

def run(path,*args):
    r=subprocess.run([sys.executable,str(path),*map(str,args)],cwd=path.parent,capture_output=True,check=True)
    assert not r.stderr,r.stderr.decode()
    return r.stdout

author_manifest=run(root/'author/verify_manifest.py')
audit_manifest=run(root/'independent_review/verify_audit_manifest.py')
report=json.loads(run(root/'independent_review/run_audit.py','--input',root/'author'))
assert report['author_assertions']==48709
assert report['independent_assertions']==4812
assert report['status']=='PASS'
assert report['zip']=='NOT_REQUESTED'
print(json.dumps({'status':'PASS','author_manifest':author_manifest.decode().strip(),
                  'audit_manifest':audit_manifest.decode().strip(),'audit_replay':report,
                  'original_author_files':12,'original_audit_files':13},indent=2,sort_keys=True))
