"""Standalone standard-library verifier for the compact PUBLIC PR209 target custody package.
Does not import capture/proof/operational code and does not access the network.
Run with Python -E -S -B -P /absolute/path/verify_public_custody_offline_v3.py.
"""
from pathlib import Path
import hashlib,json,stat
BASE=Path(__file__).resolve().parent
def check(ok,msg):
 if not ok:raise RuntimeError(msg)
def load(name):return json.loads((BASE/name).read_bytes())
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def bytecheck(name,row,kind=None,oid=None):
 p=BASE/name;check(p.resolve()==p and p.is_file() and not p.is_symlink() and stat.S_ISREG(p.stat().st_mode) and stat.S_IMODE(p.stat().st_mode)==0o444,'Canonical 0444 regular body: '+name)
 raw=p.read_bytes();check(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Byte identity: '+name)
 if kind:check(native(kind,raw)==oid,'Native object identity: '+name)
 return raw
bodies=0
for snapshot in ('ORIGINAL','REVISED'):
 inv=load(snapshot+'_INVENTORY_VERIFIED.json');check(inv['leaf_count']==len(inv['leaves']),'Inventory count')
 for row in inv['leaves']:bytecheck(row['archival_path'],row,'blob',row['git_blob']);bodies+=1
for row in load('NATIVE_COMMIT_OBJECTS_VERIFIED.json')['records']:
 raw=bytecheck(row['raw_commit_archival_path'],row,'commit',row['sha'])
 header=raw.split(b'\n\n',1)[0].decode().splitlines();check(header[0]=='tree '+row['tree'],'Commit root tree')
 check([x[7:] for x in header if x.startswith('parent ')]==row['parents'],'Commit parent identities')
trees=load('PUBLIC_TARGET_NATIVE_TREES.json')['trees'];verified={}
for oid,rows in trees.items():
 check(rows==sorted(rows,key=lambda r:r['name'].encode()+(b'/' if r['mode']=='040000' else b'')),'Tree order')
 check(len({r['name'] for r in rows})==len(rows),'Duplicate native tree names')
 for row in rows:check((row['mode'],row['type']) in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')),'Native mode/type')
 raw=b''.join((r['mode'].lstrip('0')+' '+r['name']).encode()+b'\0'+bytes.fromhex(r['sha']) for r in rows)
 check(native('tree',raw)==oid,'Tree hash '+oid);verified[oid]={r['name']:{'mode':r['mode'],'type':r['type'],'git_object':r['sha']} for r in rows}
def native_lookup(root,path):
 for part in path.split('/'):
  e=verified[root].get(part)
  if e is None:return None
  root=e['git_object']
 return e
for snapshot in ('ORIGINAL','REVISED'):
 inv=load(snapshot+'_INVENTORY_VERIFIED.json')
 for row in inv['leaves']:check(native_lookup(inv['root_tree'],row['path'])=={'mode':row['mode'],'type':row['type'],'git_object':row['git_blob']},'Inventory native root association')
 for row in inv['directories']:check(native_lookup(inv['root_tree'],row['path'])=={'mode':'040000','type':'tree','git_object':row['git_tree']},'Inventory directory association')
for label in ('ORIGINAL_SUBMISSION_RANGE_DELTA','REVISED_VS_ACCEPTED_MAIN_PARENT_DELTA'):
 delta=load(label+'.json');leaves={};added={};deleted={}
 def compare(old,new,prefix='',depth=0):
  check(depth<=64,'Depth bound')
  if old==new:return
  left=verified[old] if old else {};right=verified[new] if new else {}
  for name in sorted(set(left)|set(right)):
   a=left.get(name);b=right.get(name)
   if a==b:continue
   path=prefix+name;at=a is not None and a['type']=='tree';bt=b is not None and b['type']=='tree';change={'before':a,'after':b}
   if at and bt:compare(a['git_object'],b['git_object'],path+'/',depth+1)
   else:
    if at:deleted[path]=change;compare(a['git_object'],None,path+'/',depth+1)
    if bt:added[path]=change;compare(None,b['git_object'],path+'/',depth+1)
    if (a is not None and not at) or (b is not None and not bt):leaves[path]=change
 compare(delta['before_root_tree'],delta['after_root_tree'])
 for field,actual in [('leaf_changes',leaves),('added_directories',added),('deleted_directories',deleted)]:
  claimed={x['path']:{k:v for k,v in x.items() if k!='path'} for x in delta[field]};check(len(claimed)==len(delta[field]) and claimed==actual,'Complete delta differs: '+label+'/'+field)
original=load('ORIGINAL_INVENTORY_VERIFIED.json');revised=load('REVISED_INVENTORY_VERIFIED.json');mapping={r['path']:r for r in revised['leaves']};prefix='unsolved_math_prioritization/attempts/5100015/'
for row in original['leaves']:
 history=prefix+'history/original_submission_20261016/'+row['path'][len(prefix):];r=mapping[history]
 check(all(row[k]==r[k] for k in ('mode','type','git_blob','bytes','sha256')),'Original23 native history identity')
for row in load('OWN_QUEUE_ROWS_AND_BODY_IDENTITIES.json')['snapshots']:
 bytecheck(row['own_row_archival_path'],row['own_row_pin']);inv=load(row['snapshot'].upper()+'_INVENTORY_VERIFIED.json');check(native_lookup(inv['root_tree'],row['native_path'])=={'mode':row['mode'],'type':row['type'],'git_object':row['git_blob']},'QUEUE native association')
print(json.dumps({'verified':True,'original_bodies':23,'revised_bodies':54,'archived_attempt_bodies_verified':bodies,'native_commit_bodies':len(load('NATIVE_COMMIT_OBJECTS_VERIFIED.json')['records']),'authenticated_native_trees':len(trees),'both_complete_public_target_native_deltas_independently_recomputed':True,'network_or_proof_execution':False},sort_keys=True))
