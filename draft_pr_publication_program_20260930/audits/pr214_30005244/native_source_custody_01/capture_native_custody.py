"""Bounded GET-only PR214 native artifact custody. No Git/service mutation or math.
Only this new custody folder is written. No dynamic provider routes or retries.
"""
from pathlib import Path
import base64,copy,datetime,hashlib,json,os,re,stat,sys,types
HERE=Path(__file__).absolute().parent
PROGRAM=HERE.parents[2]
HELPER=PROGRAM/'ordered_intakes_after_PR212_20261017/preparation_01/status_only_intake_after_pr212.py'
HELPER_PIN={'bytes':24760,'sha256':'0292388c3722d04cb2c11108d409c14759b61a370b0478fbbef41c92e19349eb'}
INTAKE=PROGRAM/'ordered_intakes_after_PR212_20261017/PR214_PRESERVED_STATUS_INTAKE.json'
INTAKE_PIN={'bytes':33461,'sha256':'abd2aa6d2535d48e8e628110eb83e8a690975e9168c68e8aff5c91a9178080ec'}
ORIGINAL='36d5ef15098163e74bf14c2e696f560ce592affd'
CURRENT='95ba37055ebf1e7b4f9d76aa43816c9978c7bce8'
MERGE='4abf30daa991860a275b3d25745159852757ad35'
ORIGINAL_ROOT='6788a74181eb1730ec961f78c3ddee6c763b728c'
CURRENT_ROOT='eb7cdb30bff245e3f36ea282fbcaa099e1038c57'
ATTEMPT='unsolved_math_prioritization/attempts/30005244'
MAX_CALLS=350
MAX_BODY=8_000_000
MAX_WIRE=120_000_000
PRIVATE=HERE/'_private'
TREES={}
def need(x,msg):
 if type(x) is not bool or not x:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def native(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def encode(x):return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def write(path,raw):
 need(path.is_relative_to(HERE) and not path.is_symlink(),'Only own ordinary output')
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():need(path.read_bytes()==raw,'Existing own evidence differs');return
 with path.open('xb') as f:f.write(raw);f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
def load_helper():
 raw=HELPER.read_bytes();need(pin(raw)==HELPER_PIN,'Pinned explicit-host bounded GET helper')
 h=types.ModuleType('owned_readonly_intake_transport');h.__file__=str(HELPER)
 exec(compile(raw,str(HELPER),'exec'),h.__dict__);return h
h=load_helper()
def intake():
 raw=INTAKE.read_bytes();need(pin(raw)==INTAKE_PIN,'Exact accepted intake pin')
 value=h.decode(raw);need(value['PR']==214 and value['eligible'] is True and value['preserved_submission_head']==ORIGINAL and value['current_status_custody']['actual_head']==CURRENT,'Intake native identities');return value
def ledger():
 p=PRIVATE/'API_LEDGER.json'
 return json.loads(p.read_bytes()) if p.exists() else []
def record_ledger(rows):
 path=PRIVATE/'API_LEDGER.json';raw=encode(rows)
 if path.exists():path.chmod(0o644)
 path.write_bytes(raw);path.chmod(0o444)
def fetch(route,fresh=False):
 need(route=='pulls/214' or re.fullmatch(r'git/(commits|trees|blobs)/[0-9a-f]{40}',route) is not None,'Exact metadata/immutable native GET only')
 rows=ledger();cache=next((r for r in rows if r['route']==route and r['exit']==0),None)
 if cache and not fresh:
  raw=(PRIVATE/cache['raw_path']).read_bytes();need(pin(raw)==cache['stdout_pin'],'Cached actual immutable response identity');return h.decode(raw)
 need(len(rows)<MAX_CALLS and sum(r['stdout_pin']['bytes'] for r in rows)<MAX_WIRE,'Finite total GET budget')
 result=h.bounded_get(h.api_argv(214,route))
 need(sum(r['stdout_pin']['bytes'] for r in rows)+len(result.stdout)<=MAX_WIRE,'Aggregate native wire bound')
 name=str(len(rows)+1).zfill(4)+'.json';write(PRIVATE/'api'/name,result.stdout)
 record={'route':route,'method':'GET','hostname':'github.com','exit':result.returncode,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout_pin':pin(result.stdout),'stderr_pin':pin(result.stderr),'raw_path':'api/'+name}
 rows.append(record);record_ledger(rows)
 need(result.returncode==0,'GET failure: stop, no automatic retry')
 value=h.decode(result.stdout);need(type(value) is dict,'Native GET dictionary')
 return value
def raw_commit(j):
 oid=j['sha'];tree=j['tree']['sha'];parents=[x['sha'] for x in j['parents']]
 need(h.hexid(oid) and h.hexid(tree) and 1<=len(parents)<=2 and all(h.hexid(p) for p in parents),'Native commit identities')
 verification=j.get('verification',{});payload=verification.get('payload');signature=verification.get('signature')
 if type(payload) is str and type(signature) is str:
  header,body=payload.encode().split(b'\n\n',1)
  signed=header+b'\ngpgsig '+b'\n '.join(signature.encode().splitlines())+b'\n\n'+body
  if native('commit',signed)==oid:return signed
 def who(meta,offset):
  d=datetime.datetime.fromisoformat(meta['date'].replace('Z','+00:00'));seconds=int(d.timestamp())
  sign='+' if offset>=0 else '-';a=abs(offset);zone=sign+str(a//60).zfill(2)+str(a%60).zfill(2)
  return (meta['name']+' <'+meta['email']+'> '+str(seconds)+' '+zone).encode()
 need(verification.get('reason')=='unsigned' and payload is None and signature is None,'Unsupported signed/native commit encoding')
 prefix=('tree '+tree+'\n'+''.join('parent '+p+'\n' for p in parents)).encode()
 offsets=[0,-420,420]+[n for n in range(-840,841,15) if n not in (0,-420,420)]
 for a,c in [(n,n) for n in offsets]+[(a,c) for a in offsets for c in offsets if a!=c]:
  header=prefix+b'author '+who(j['author'],a)+b'\ncommitter '+who(j['committer'],c)+b'\n\n'
  for message in (j['message'],j['message']+'\n'):
   raw=header+message.encode()
   if native('commit',raw)==oid:return raw
 raise RuntimeError('Cannot reconstruct exact native commit object')
def tree(oid):
 if oid in TREES:return TREES[oid]
 j=fetch('git/trees/'+oid);need(j.get('sha')==oid and j.get('truncated') is False and type(j.get('tree')) is list and len(j['tree'])<=30000,'Complete bounded native immediate tree')
 rows=j['tree'];names=set()
 for r in rows:
  name=r['path'];need(type(name) is str and name not in ('','.','..') and '/' not in name and '\0' not in name and name not in names,'Native basename');names.add(name)
  need((r['mode'],r['type']) in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')) and h.hexid(r['sha']),'Native modes and OIDs')
 ordered=sorted(rows,key=lambda x:x['path'].encode()+(b'/' if x['type']=='tree' else b''))
 raw=b''.join(r['mode'].lstrip('0').encode()+b' '+r['path'].encode()+b'\0'+bytes.fromhex(r['sha']) for r in ordered)
 need(rows==ordered and native('tree',raw)==oid,'Authenticated immediate native tree SHA/order')
 TREES[oid]={r['path']:{k:r[k] for k in ('mode','type','sha')} for r in rows};return TREES[oid]
def lookup(oid,path):
 parts=path.split('/');need(len(parts)<=32 and all(p not in ('','.','..') for p in parts),'Bounded targeted path')
 for i,p in enumerate(parts):
  row=tree(oid).get(p)
  if row is None:return None
  if i<len(parts)-1:
   need(row['type']=='tree','Target ancestor tree');oid=row['sha']
 return row
def descendants(oid,prefix,depth=0):
 need(depth<=16,'Owned attempt recursion bound')
 out={}
 for name,row in tree(oid).items():
  path=prefix+'/'+name
  if row['type']=='tree':out.update(descendants(row['sha'],path,depth+1))
  else:out[path]=row
 need(len(out)<=500,'Finite owned attempt leaf bound');return out
def body(oid):
 path=PRIVATE/'blobs'/oid
 if path.exists():raw=path.read_bytes()
 else:
  j=fetch('git/blobs/'+oid);need(j.get('sha')==oid and j.get('encoding')=='base64' and type(j.get('size')) is int and 0<=j['size']<=MAX_BODY and type(j.get('content')) is str,'Bounded complete native blob response')
  raw=base64.b64decode(''.join(j['content'].split()),validate=True);need(len(raw)==j['size'],'Full decoded native blob size');write(path,raw)
 need(len(raw)<=MAX_BODY and native('blob',raw)==oid,'Full native blob SHA1');return raw
def current_pr():
 j=fetch('pulls/214',fresh=True)
 need(j.get('number')==214 and j['head']['sha']==CURRENT and j.get('state')=='closed' and j.get('merged') is True and j.get('draft') is False and j.get('merge_commit_sha')==MERGE and j.get('merged_at')=='2026-10-15T09:28:52Z','Fresh already-merged exact current PR identity')
 return {k:j.get(k) for k in ('number','state','draft','merged','merge_commit_sha','merged_at','updated_at','created_at','title','head','base')}
def inventory():
 accepted=intake();pr=current_pr();commits={}
 for name,oid,expected in (('original',ORIGINAL,ORIGINAL_ROOT),('current',CURRENT,CURRENT_ROOT)):
  j=fetch('git/commits/'+oid);need(j['sha']==oid and j['tree']['sha']==expected,'Pinned original/current root')
  if name=='original':need([p['sha'] for p in j['parents']]==['37e5d6ee0f3e03de5636edf2b00dd6df77f9a494'],'Original sole parent')
  else:need([p['sha'] for p in j['parents']]==[ORIGINAL,'5fde5b9aa46bb620d7a0d3b036ceb914076c6303'],'Exact revised ordered parents')
  raw=raw_commit(j);write(PRIVATE/'native_commits'/(oid+'.commit'),raw);commits[name]={'sha':oid,'tree':expected,'parents':[p['sha'] for p in j['parents']],'raw_commit_pin':pin(raw)}
 snapshots={}
 for name,root in (('original',ORIGINAL_ROOT),('current',CURRENT_ROOT)):
  attempt=lookup(root,ATTEMPT);need(attempt is not None and attempt['type']=='tree','Owned attempt subtree exists')
  leaves=descendants(attempt['sha'],ATTEMPT);need(bool(leaves),'Nonempty owned attempt')
  if name=='original':need(len(leaves)==31,'Exact original31 custody scope')
  instructions={}
  for prefix in ('','unsolved_math_prioritization','unsolved_math_prioritization/attempts',ATTEMPT):
   for filename in ('AGENTS.md','CLAUDE.md'):
    p=(prefix+'/' if prefix else '')+filename;r=lookup(root,p)
    if r is not None:
     need(r['type']=='blob' and r['mode'] in ('100644','100755'),'Ordinary applicable instruction entry');raw=body(r['sha']);instructions[p]={**r,**pin(raw)};write(PRIVATE/'reading'/name/p,raw)
  queue=lookup(root,'unsolved_math_prioritization/QUEUE.md');need(queue is not None and queue['mode']=='100644' and queue['type']=='blob','Regular native QUEUE')
  raw=body(queue['sha']);matches=[]
  for line in raw.splitlines(keepends=True):
   cells=line.decode().split('|')
   if len(cells)==14 and cells[2].strip().split(' / ')[0]=='30005244':matches.append((line,cells))
  need(len(matches)==1,'Exactly one own native QUEUE row')
  line,cells=matches[0]
  if name=='original':
   need(pin(raw)=={k:accepted['preserved_QUEUE_blob'][k] for k in ('bytes','sha256')} and queue['sha']==accepted['preserved_QUEUE_blob']['git_blob'],'Original exact accepted whole QUEUE')
   need(cells[8].strip()=='claimed_solved' and cells[9].strip()=='2/5' and hashlib.sha256(line.removesuffix(b'\n')).hexdigest()==accepted['dated_registry_row']['status_projection']['targets'][0]['selected_row_sha256'],'Original exact claimed2/5 row')
  write(PRIVATE/'reading'/name/'unsolved_math_prioritization/QUEUE.md',raw)
  snapshots[name]={'commit':commits[name],'attempt':attempt,'leaves':leaves,'instructions':instructions,'queue':{**queue,**pin(raw),'row_pin':pin(line),'row':line.decode(),'status':cells[8].strip(),'effort':cells[9].strip()},'root_names':sorted(tree(root)),'prioritization_names':sorted(tree(lookup(root,'unsolved_math_prioritization')['sha']))}
 result={'schema':'pr214-native-custody-inventory-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'intake_pin':INTAKE_PIN,'original':snapshots['original'],'current':snapshots['current'],'PR':pr}
 write(HERE/'INVENTORY.json',encode(result));write(HERE/'AUTHENTICATED_TREES.json',encode(TREES))
 print(json.dumps({'original_files':len(snapshots['original']['leaves']),'current_files':len(snapshots['current']['leaves']),'original_instructions':list(snapshots['original']['instructions']),'current_instructions':list(snapshots['current']['instructions']),'prioritization_names':snapshots['current']['prioritization_names'],'root_names':snapshots['current']['root_names'],'current_own_paths':list(snapshots['current']['leaves'])},sort_keys=True))
if __name__=='__main__':
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Use -E -S -B -P')
 need(sys.argv[1:]==['inventory'],'Inventory stage only')
 inventory()

