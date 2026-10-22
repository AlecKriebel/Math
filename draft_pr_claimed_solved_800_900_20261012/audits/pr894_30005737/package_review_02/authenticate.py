from pathlib import Path
import json,hashlib,stat,datetime,sys
A=Path(__file__).resolve().parent.parent; R=Path(__file__).resolve().parent;C=A/'package_assembly_01/candidate'
def sha(b):return hashlib.sha256(b).hexdigest()
frozen=json.loads((A/'FROZEN_CANDIDATE_CORE.json').read_bytes()); rows=[]
for p in sorted(C.rglob('*')):
 if p.is_file() or p.is_symlink():
  st=p.lstat();assert stat.S_ISREG(st.st_mode),(p,'nonregular');assert stat.S_IMODE(st.st_mode)==0o644,(p,oct(st.st_mode))
  b=p.read_bytes();rows.append({'path':p.relative_to(C).as_posix(),'git_mode':'100644','bytes':len(b),'sha256':sha(b)})
digest=sha(json.dumps(rows,sort_keys=True,separators=(',',':')).encode());assert rows==frozen['files'];assert len(rows)==253;assert digest=='c06bf8dfd12c840d0f4af7af32ef6253de1c9f8d3b47f7a0618dedd7fd17ed2b'
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(rows),'core_sha256':digest,'full_rows_equal_frozen':True,'regular_0644':True,'files':rows}
out=R/('AUTH_FINAL.json' if '--final' in sys.argv else 'AUTH_INITIAL.json');out.write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='files'})
if '--final' not in sys.argv:
 exp={'private_native/canonical_pair.json':(3524,'b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298'),'private_native/statement.txt':(183,'a8224e60e73ef6f78e8af57e836e4cc5246a0b1cd12d1af10393d8fd0104149e'),'SOURCE_MANIFEST.json':(4654,'1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c')}
 for n,(size,h) in exp.items():
  b=(A/n).read_bytes();assert (len(b),sha(b))==(size,h);print(n,size,h)
 print((A/'private_native/statement.txt').read_text())
