#!/usr/bin/env python3
"""Validate entire lstat inventory before reading manifest or any payload content."""
import os, stat, json, hashlib
from pathlib import Path

def require(ok,msg):
    if not ok: raise ValueError(msg)
def validate(root):
    root=Path(root)
    require(stat.S_ISDIR(root.lstat().st_mode),'root must be a real directory')
    inventory={}
    for base,dirs,files in os.walk(root,followlinks=False):
        for name in dirs+files:
            p=Path(base)/name; s=p.lstat(); rel=p.relative_to(root).as_posix()
            require(stat.S_ISREG(s.st_mode),'nonregular entry: '+rel)
            require(s.st_nlink==1,'hardlinked entry: '+rel)
            inventory[rel]=s.st_size
    require('MANIFEST.json' in inventory,'missing manifest')
    m=json.loads((root/'MANIFEST.json').read_text())
    require(set(m)=={'schema_version','problem_id','disposition','files'},'manifest fields')
    require(type(m['schema_version']) is int and m['schema_version']==1,'schema integer')
    require(type(m['problem_id']) is int and m['problem_id']==30002271,'problem integer')
    require(m['disposition']=='already_solved1','disposition')
    require(type(m['files']) is list,'files array')
    names=[]
    for row in m['files']:
        require(type(row) is dict and set(row)=={'name','bytes','sha256'},'file schema')
        name=row['name']; require(type(name) is str and name not in ('','MANIFEST.json') and '/' not in name and '\\' not in name and name not in ('.','..'),'safe filename')
        require(type(row['bytes']) is int and row['bytes']>=0,'strict byte integer')
        h=row['sha256']; require(type(h) is str and len(h)==64 and all(c in '0123456789abcdef' for c in h),'sha256 schema')
        names.append(name)
    require(len(names)==len(set(names)),'duplicate file')
    require(set(inventory)==set(names)|{'MANIFEST.json'},'inventory mismatch')
    for row in m['files']:
        p=root/row['name']
        require(inventory[row['name']]==row['bytes'],'size mismatch')
        require(hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],'hash mismatch')
    return {'passed':True,'payload_files':len(names),'inventory_entries':len(inventory),'manifest_inventoried_before_read':True}
if __name__=='__main__': print(json.dumps(validate(Path(__file__).parent),indent=2))
