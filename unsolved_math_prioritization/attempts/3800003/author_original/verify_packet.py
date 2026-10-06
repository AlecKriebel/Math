#!/usr/bin/env python3
"""Fail-closed package verifier. Supply the independently held manifest hash."""
import argparse,hashlib,json
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def main():
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--manifest-sha256',required=True);a=p.parse_args();root=Path(a.root)
    b=(root/'MANIFEST.json').read_bytes();need(sha(b)==a.manifest_sha256,'manifest differs from external anchor');m=json.loads(b,object_pairs_hook=unique)
    expected=set(m['files'])|{'MANIFEST.json'};actual=set()
    for path in root.rglob('*'):
        need(not path.is_symlink(),'symlink forbidden')
        if path.is_file():actual.add(path.relative_to(root).as_posix())
    need(actual==expected,'unexpected or missing package file')
    for name,pin in m['files'].items():
        path=Path(name);need(not path.is_absolute() and '..' not in path.parts,'unsafe file path');b=(root/path).read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'member mismatch: '+name)
    s=json.loads((root/'STATUS.json').read_text(),object_pairs_hook=unique)
    need(s['problem_id']==3800003 and not s['full_extremal_problem_solved'] and s['recommended_queue_status']=='stalled','scope escalation')
    print(json.dumps({'result':'PASS','files_verified':len(expected),'external_manifest_anchor_verified':True,'scope':'Integrity only; this checker does not establish mathematical correctness.'},sort_keys=True))
if __name__=='__main__':main()
