from pathlib import Path
import json,hashlib,base64,stat
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244");D=A/'native_merge_source_custody_03'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def native(t,b):return hashlib.sha1(t.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def read(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and stat.S_IMODE(s.st_mode)==0o444
 b=p.read_bytes();t=p.lstat();assert (t.st_dev,t.st_ino,t.st_mode,t.st_size,t.st_mtime_ns,t.st_ctime_ns)==(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 return b
ledger=json.loads(read(D/'_private/API_LEDGER.json'));bodies={};trees={};commits={}
for row in ledger:
 assert row['method']=='GET' and row['hostname']=='github.com' and row['exit']==0
 raw=read(D/'_private'/row['raw_path']);assert pin(raw)==row['stdout_pin'];j=json.loads(raw);route=row['route'];oid=route.rsplit('/',1)[1]
 assert j['sha']==oid
 if '/trees/' in route:
  assert j['truncated'] is False
  rows=j['tree'];assert len(rows)==len({r['path'] for r in rows})
  ordered=sorted(rows,key=lambda r:r['path'].encode()+(b'/' if r['type']=='tree' else b''))
  assert rows==ordered
  bb=b''.join(r['mode'].lstrip('0').encode()+b' '+r['path'].encode()+b'\0'+bytes.fromhex(r['sha']) for r in rows)
  assert native('tree',bb)==oid;trees[oid]={r['path']:{k:r[k] for k in ('mode','type','sha')} for r in rows}
 elif '/blobs/' in route:
  assert j['encoding']=='base64'
  bb=base64.b64decode(''.join(j['content'].split()),validate=True);assert len(bb)==j['size'] and native('blob',bb)==oid
  assert read(D/'_private/blobs'/oid)==bb;bodies[oid]=bb
 elif '/commits/' in route:
  bb=read(D/'_private/native_commits'/(oid+'.commit'));assert native('commit',bb)==oid
  hd,body=bb.split(b'\n\n',1);headers=hd.split(b'\n')
  assert headers[0]==('tree '+j['tree']['sha']).encode()
  assert [x.decode().split(' ',1)[1] for x in headers if x.startswith(b'parent ')]==[p['sha'] for p in j['parents']]
  if j.get('verification',{}).get('payload'):
   unsigned=j['verification']['payload'].encode();uh,ub=unsigned.split(b'\n\n',1)
   expected=uh+b'\ngpgsig '+b'\n '.join(j['verification']['signature'].encode().split(b'\n'))+b'\n\n'+ub
   assert bb==expected
  commits[oid]=pin(bb)
 else:raise AssertionError(route)
def lookup(root,path):
 parts=path.split('/')
 for n,name in enumerate(parts):
  row=trees[root][name]
  if n<len(parts)-1:assert row['type']=='tree';root=row['sha']
 return row
receipt=json.loads(read(D/'ROOT_MERGE_MAIN_ASSOCIATION_01.json'));R=receipt['actual_MAIN_observed'];root=receipt['actual_MAIN_tree']
records=json.loads(read(D/'MAIN_OWN_BODY_RECORDS.json'));assert len(records)==42
for row in records:
 path=row['path'];entry=lookup(root,path);assert entry=={k:row[k] for k in ('mode','type','sha')}
 bb=read(D/'_private/reading/Main'/path);assert bb==bodies[row['sha']] and pin(bb)=={k:row[k] for k in ('bytes','sha256')}
manifest=json.loads(bodies[lookup(root,'unsolved_math_prioritization/attempts/30005244/CURRENT_SOURCE_MANIFEST.json')['sha']])
for row in manifest['current_files']:
 bb=bodies[lookup(root,'unsolved_math_prioritization/attempts/30005244/'+row['path'])['sha']]
 assert pin(bb)=={k:row[k] for k in ('bytes','sha256')}
for label in ['MAIN_BEFORE','MAIN_AFTER']:
 raw=read(D/'_private'/(label+'.RAW_STDOUT.json'));j=json.loads(raw);assert j['object']['sha']==R and j['ref']=='refs/heads/main'
delta=json.loads(read(D/'PREPARED_TO_MAIN_OWN_DELTA.json'))
assert len(delta['changed'])==8 and delta['removed']==[]
assert delta['analytical_candidate_after_exact_title_unchanged'] is True and delta['history_subtree_unchanged'] is True
print(json.dumps({'Root_replayed_actual_GETs':len(ledger),'trees':len(trees),'raw_native_commits':commits,'Main_own_bodies':len(records),'Main_current_manifest_rows_verified':len(manifest['current_files']),'actual_Root_full_diff_read':True,'all_replayed':True,'receipt':pin(read(D/'ROOT_MERGE_MAIN_ASSOCIATION_01.json'))}))
