#!/usr/bin/env python3
"""Closed flat packet custody; explicit exceptions, no assertions or code execution."""
import hashlib,json,os,stat,sys
from pathlib import Path
def need(ok,message):
    if not ok: raise ValueError(message)
def object_unique(pairs):
    result={}
    for key,value in pairs:
        need(key not in result,'duplicate JSON key')
        result[key]=value
    return result
def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
    manifest=root/'MANIFEST.json'
    st=manifest.lstat()
    need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'manifest must be single-link regular file')
    need(st.st_size<=1_000_000,'manifest too large')
    data=json.loads(manifest.read_text(),object_pairs_hook=object_unique)
    need(data['schema']=='pr786-math-schur-flat/v1','manifest schema')
    need(data['explicit_exceptions']==['MANIFEST.json'],'explicit exception set')
    rows=data['files'];need(isinstance(rows,dict) and bool(rows),'file inventory')
    need('MANIFEST.json' not in rows,'manifest self-reference')
    for name,row in rows.items():
        need(isinstance(name,str) and name not in ('.','..') and '/' not in name and '\\' not in name and not name.startswith('.'),'unsafe flat path')
        need(set(row)=={'bytes','sha256'},'entry schema')
        need(type(row['bytes']) is int and 0<=row['bytes']<=8_000_000,'entry size')
        need(isinstance(row['sha256'],str) and len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256']),'entry digest')
    actual={p.name for p in root.iterdir()}
    need(actual==set(rows)|{'MANIFEST.json'},'closed inventory mismatch')
    inodes=set()
    for name,row in rows.items():
        f=root/name;st=f.lstat()
        need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'not single-link regular file: '+name)
        need((st.st_dev,st.st_ino) not in inodes,'duplicate inode')
        inodes.add((st.st_dev,st.st_ino))
        need(st.st_size==row['bytes'],'size mismatch: '+name)
        body=f.read_bytes()
        need(len(body)==row['bytes'] and hashlib.sha256(body).hexdigest()==row['sha256'],'digest mismatch: '+name)
    print(json.dumps({'result':'PASS','checked_files':len(rows),'explicit_exceptions':['MANIFEST.json'],'optimization_safe':True},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(json.dumps({'result':'FAIL','reason':str(exc)},sort_keys=True))
        raise SystemExit(1)
