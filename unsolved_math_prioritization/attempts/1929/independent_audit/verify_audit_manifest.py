#!/usr/bin/env python3
"""Exact allowlist and content verification for this independent audit sidecar."""
from pathlib import Path
import hashlib,json,stat

def require(ok,message):
    if not ok:raise ValueError(message)

def distinct(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key'); d[k]=v
    return d

def verify(root):
    root=Path(root)
    require(root.is_dir() and not root.is_symlink(),'regular audit directory required')
    p=root/'AUDIT_MANIFEST.json'
    require(stat.S_ISREG(p.lstat().st_mode),'regular manifest required')
    m=json.loads(p.read_text(),object_pairs_hook=distinct)
    require(m['schema']==1 and m['problem_id']==1929 and m['verdict']=='PASS','audit identity')
    entries=m['files']; names=[e['path'] for e in entries]
    require(len(names)==len(set(names)),'duplicate member')
    require(all(isinstance(s,str) and s not in ('','.','..','AUDIT_MANIFEST.json') and '/' not in s and '\\' not in s for s in names),'unsafe member name')
    require({p.name for p in root.iterdir()}==set(names)|{'AUDIT_MANIFEST.json'},'exact allowlist mismatch')
    for p in root.iterdir():require(stat.S_ISREG(p.lstat().st_mode),'nonregular member')
    for e in entries:
        b=(root/e['path']).read_bytes()
        require(type(e['bytes']) is int and len(b)==e['bytes'],'size mismatch')
        require(hashlib.sha256(b).hexdigest()==e['sha256'],'hash mismatch')
    return {'passed':True,'files':len(entries),'verdict':'PASS','problem_id':1929}

if __name__=='__main__':
    print(json.dumps(verify(Path(__file__).parent),sort_keys=True))
