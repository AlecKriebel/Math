#!/usr/bin/env python3
"""Strict flat administrative review custody; no assertions, subprocesses, or source writes."""
import hashlib,json,stat,sys
from pathlib import Path
def need(ok,message):
    if not ok:raise ValueError(message)
def unique_object(pairs):
    result={}
    for key,value in pairs:
        need(key not in result,'duplicate JSON key')
        result[key]=value
    return result
def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
    f=root/'MANIFEST.json';st=f.lstat()
    need(stat.S_ISREG(st.st_mode) and st.st_nlink==1 and st.st_size<1_000_000,'manifest regular/single-link/bounded')
    data=json.loads(f.read_text(),object_pairs_hook=unique_object)
    need(data['schema']=='pr786-administrative-merge-scope/v1','schema')
    need(data['explicit_exceptions']==['MANIFEST.json'],'exact explicit exception')
    rows=data['files'];need(isinstance(rows,dict) and bool(rows),'nonempty flat inventory')
    need(set(p.name for p in root.iterdir())==set(rows)|{'MANIFEST.json'},'closed inventory')
    seen=set()
    for name,row in rows.items():
        need(isinstance(name,str) and name not in ('.','..','MANIFEST.json') and not name.startswith('.') and '/' not in name and '\\' not in name,'safe flat name')
        need(set(row)=={'bytes','sha256'} and type(row['bytes']) is int and 0<=row['bytes']<8_000_000,'record schema')
        need(isinstance(row['sha256'],str) and len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256']),'SHA256 schema')
        f=root/name;st=f.lstat()
        need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'single-link regular file '+name)
        need((st.st_dev,st.st_ino) not in seen,'distinct inode');seen.add((st.st_dev,st.st_ino))
        need(st.st_size==row['bytes'],'byte count '+name)
        b=f.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'hash '+name)
    print(json.dumps({'result':'PASS','files_checked':len(rows),'explicit_exceptions':['MANIFEST.json'],'optimization_safe':True},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(json.dumps({'result':'FAIL','reason':str(exc)},sort_keys=True));raise SystemExit(1)
