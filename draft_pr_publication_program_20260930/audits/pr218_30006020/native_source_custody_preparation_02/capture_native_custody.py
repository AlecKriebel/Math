"""INACTIVE PR218 bounded GET-only native custody. No submitted code or math is run.
Execution requires explicit Root review; source preparation creates no live authority.
"""
from pathlib import Path
import argparse,base64,copy,datetime,hashlib,json,os,re,stat,sys,types
HERE=Path(__file__).absolute().parent
PROGRAM=HERE.parents[2]
HELPER=PROGRAM/'ordered_intakes_after_PR214_20261017/preparation_01/status_only_intake_after_pr214.py'
HELPER_PIN={'bytes':24956,'sha256':'a5dd2b47e66dff21fff04a1a0efac9edace7c911c2fba951471bac1013e7b7c0'}
INTAKE=PROGRAM/'ordered_intakes_after_PR214_20261017/PR218_PRESERVED_STATUS_INTAKE.json'
INTAKE_PIN={'bytes':24998,'sha256':'2a56688bb676f9eac75ecfdf2998ea0f4c225290ef53813c5c36fe41ac74283e'}
STATUS=HERE.parent/'root_current_status_custody_01/ROOT_CURRENT_STATUS_OBSERVATION_01.json'
STATUS_PIN={'bytes':3620,'sha256':'762817d63ec5f3dd04c1ed8e66ebed01a8426c561f7f813552f412d33db45a83'}
ORIGINAL='dc457c741c779fbf90fbfdcdc73f750b3716f561'
CURRENT='698f85a0f608e5a90924567d761663dfb100f3c2'
MERGE='8172b404db36b931005ac48a94ec91fdff866023'
ORIGINAL_ROOT='4e8470aa1962e3137be0aaf062b6e913c6674f35'
CURRENT_ROOT='95efad392b6c8ac117557252faaf34d43d41a1a9'
ORIGINAL_PARENT='7004f06fada174b500d9c308d622b4c08728d8b9'
CURRENT_PARENTS=[ORIGINAL,'2f6aa7a8a4c2456c335be24d64ba9c071d599944']
ATTEMPT='unsolved_math_prioritization/attempts/30006020'
OLD_AUDIT='draft_pr_descending_audit_20261002/audits/pr218_30006020'
QUEUE='unsolved_math_prioritization/QUEUE.md'
CRITICAL=[OLD_AUDIT+'/preprint/cylinder_areas.tex',OLD_AUDIT+'/preprint/output/pdf/cylinder_areas.pdf',OLD_AUDIT+'/preprint/output/cylinder_areas_verification.zip']
MAX_CALLS=800
MAX_WIRE=120_000_000
MAX_BODY=8_000_000
MAX_ROLE_FILES=400
MAX_ROLE_BYTES=8_000_000
MAX_DECODED=32_000_000
MAX_TREES=2000
MAX_TREE_ENTRIES=200000
MAX_DIFF_LEAVES=10000
def need(x,msg):
 if type(x) is not bool or not x:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def hexid(x):return type(x) is str and re.fullmatch('[0-9a-f]{40}',x) is not None
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def encode(x):return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def regular(path,cap=4_000_000):
 need(path.is_absolute() and path.resolve()==path,'Canonical regular source/input')
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY);parents=[]
 try:
  for part in path.parts[1:-1]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);parents.append(fd);fd=nxt
  leaf=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
  try:
   before=os.fstat(leaf);ident=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode)
   need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444 and 0<=before.st_size<=cap,'Bounded0444 ordinary input')
   data=os.read(leaf,cap+1)
   need(ident(before)==ident(os.fstat(leaf))==ident(os.stat(path.name,dir_fd=fd,follow_symlinks=False)) and len(data)==before.st_size and path.resolve()==path,'Source/input identity changed')
   return data
  finally:os.close(leaf)
 finally:
  os.close(fd)
  for ancestor in reversed(parents):os.close(ancestor)
def load_helper():
 raw=regular(HELPER);need(pin(raw)==HELPER_PIN,'Exact accepted GET-only helper source')
 h=types.ModuleType('pr218_pinned_GET_transport');h.__file__=str(HELPER)
 exec(compile(raw,str(HELPER),'exec'),h.__dict__);return h
def decode_tree(j,oid):
 need(type(j) is dict and j.get('sha')==oid and j.get('truncated') is False and type(j.get('tree')) is list and len(j['tree'])<=30000,'Complete bounded native immediate tree')
 rows=j['tree'];names=set()
 for r in rows:
  name=r['path'];need(type(name) is str and name not in ('','.','..') and '/' not in name and '\0' not in name and name not in names,'Unique native basename');names.add(name)
  need((r['mode'],r['type']) in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')) and hexid(r['sha']),'Native modes/OIDs')
 ordered=sorted(rows,key=lambda r:r['path'].encode()+(b'/' if r['type']=='tree' else b''))
 raw=b''.join(r['mode'].lstrip('0').encode()+b' '+r['path'].encode()+b'\0'+bytes.fromhex(r['sha']) for r in ordered)
 need(rows==ordered and native('tree',raw)==oid,'Exact native tree SHA1/order')
 return {r['path']:{k:r[k] for k in ('mode','type','sha')} for r in rows}
def decode_blob(j,oid):
 need(type(j) is dict and j.get('sha')==oid and j.get('encoding')=='base64' and type(j.get('size')) is int and 0<=j['size']<=MAX_BODY and type(j.get('content')) is str,'Bounded complete native blob')
 raw=base64.b64decode(''.join(j['content'].split()),validate=True)
 need(len(raw)==j['size'] and native('blob',raw)==oid,'Full native blob SHA1/size');return raw
def raw_commit(j):
 oid=j['sha'];root=j['tree']['sha'];parents=[p['sha'] for p in j['parents']]
 need(hexid(oid) and hexid(root) and 1<=len(parents)<=2 and all(hexid(p) for p in parents),'Native commit identities')
 verification=j.get('verification',{});payload=verification.get('payload');signature=verification.get('signature')
 def checked(raw):
  header=raw.split(b'\n\n',1)[0].splitlines()
  need(header[0]==('tree '+root).encode() and [v[7:].decode() for v in header if v.startswith(b'parent ')]==parents,'Raw commit tree/ordered parents vs metadata')
  need(native('commit',raw)==oid,'Exact complete raw commit SHA1');return raw
 if type(payload) is str and type(signature) is str:
  head,body=payload.encode().split(b'\n\n',1)
  # split, not splitlines: a terminal signature LF contributes an empty folded line.
  raw=head+b'\ngpgsig '+b'\n '.join(signature.encode().split(b'\n'))+b'\n\n'+body
  return checked(raw)
 need(verification.get('reason')=='unsigned' and payload is None and signature is None,'Unsupported native signed encoding')
 def who(meta,offset):
  stamp=int(datetime.datetime.fromisoformat(meta['date'].replace('Z','+00:00')).timestamp())
  a=abs(offset);zone=('+' if offset>=0 else '-')+str(a//60).zfill(2)+str(a%60).zfill(2)
  return (meta['name']+' <'+meta['email']+'> '+str(stamp)+' '+zone).encode()
 prefix=('tree '+root+'\n'+''.join('parent '+p+'\n' for p in parents)).encode()
 offsets=[0,-420,420]+[n for n in range(-840,841,15) if n not in (0,-420,420)]
 for a,c in [(n,n) for n in offsets]+[(a,c) for a in offsets for c in offsets if a!=c]:
  header=prefix+b'author '+who(j['author'],a)+b'\ncommitter '+who(j['committer'],c)+b'\n\n'
  for message in (j['message'],j['message']+'\n'):
   raw=header+message.encode()
   if native('commit',raw)==oid:return checked(raw)
 raise RuntimeError('Unsupported native commit encoding; no guessed authentication')
def own_queue_row(raw):
 matches=[]
 for line in raw.splitlines(keepends=True):
  cells=line.decode().split('|')
  candidate='|' in line.decode() and any(re.search(r'(?<![0-9])30006020(?![0-9])',c) for c in cells[:4])
  if candidate:
   need(line.startswith(b'|') and len(cells)==14 and re.fullmatch(r'30006020(?: / [^|\x60\[\]]+)?',cells[2].strip()) is not None,'Noncanonical or malformed own QUEUE row')
   matches.append((line,cells))
 need(len(matches)==1,'Exactly one canonical own native QUEUE row')
 line,cells=matches[0];return {'row':line.decode(),'row_pin':pin(line),'status':cells[8].strip(),'effort':cells[9].strip()}
def allowed(route):
 return route in ('pulls/218','git/ref/heads/main') or re.fullmatch(r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',route) is not None or re.fullmatch(r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',route) is not None
class Capture:
 def __init__(self,name):
  need(re.fullmatch(r'_private_capture_[A-Za-z0-9_-]{1,48}',name) is not None,'Explicit new private output child')
  self.source_pin=pin(regular(Path(__file__).absolute()))
  self.h=load_helper()
  intake_raw=regular(INTAKE);status_raw=regular(STATUS)
  need(pin(intake_raw)==INTAKE_PIN and pin(status_raw)==STATUS_PIN,'Exact intake and Root current status pins')
  self.intake=self.h.decode(intake_raw);self.status=self.h.decode(status_raw)
  need(self.intake['PR']==218 and self.intake['eligible'] is True and self.intake['preserved_submission_head']==ORIGINAL and self.intake['preserved_QUEUE_status']=='claimed_solved' and self.intake['preserved_QUEUE_effort_cell']=='1/5','Preserved eligibility only')
  need(self.status['PR']==218 and self.status['current_head']==CURRENT and self.status['current_status']=='claimed_solved' and self.status['current_effort']=='1/5','Current status only')
  need(HERE.resolve()==HERE and not (HERE/name).exists() and not (HERE/name).is_symlink(),'Fresh canonical owned output only')
  self.out=HERE/name;self.out.mkdir(mode=0o700)
  self.fd=os.open(self.out,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  self.rows=[];self.cache={};self.trees={};self.commits={};self.blobs={};self.decoded=0;self.failed=False;self.paths=[]
 def write(self,relative,raw):
  parts=relative.split('/');need(all(x not in ('','.','..') for x in parts),'Owned relative output')
  fd=os.dup(self.fd)
  try:
   for part in parts[:-1]:
    try:os.mkdir(part,mode=0o700,dir_fd=fd)
    except FileExistsError:pass
    nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
   leaf=os.open(parts[-1],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=fd)
   try:
    with os.fdopen(leaf,'wb',closefd=False) as f:need(f.write(raw)==len(raw),'Complete evidence write');f.flush();os.fchmod(leaf,0o444);os.fsync(leaf)
   finally:os.close(leaf)
   os.fsync(fd)
  finally:os.close(fd)
  self.paths.append({'path':relative,**pin(raw)});return {'path':relative,**pin(raw)}
 def fetch(self,route,fresh=False):
  need(not self.failed and allowed(route),'GET-only finite route, failstop')
  immutable=re.fullmatch(r'git/(commits|trees|blobs)/[0-9a-f]{40}',route) is not None
  if immutable and not fresh and route in self.cache:return copy.deepcopy(self.cache[route])
  need(len(self.rows)<MAX_CALLS and sum(r['stdout_pin']['bytes'] for r in self.rows)<MAX_WIRE,'Finite GET budget')
  argv=[self.h.GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/'+route]
  n=str(len(self.rows)+1).zfill(4)
  try:result=self.h.bounded_get(argv)
  except BaseException as exc:
   self.failed=True;self.write('raw/'+n+'.TRANSPORT_STOPPED.json',encode({'method':'GET','hostname':'github.com','route':route,'exception':type(exc).__name__,'automatic_retry':False}));raise
  stdout=self.write('raw/'+n+'.STDOUT.json',result.stdout);stderr=self.write('raw/'+n+'.STDERR.txt',result.stderr)
  row={'method':'GET','hostname':'github.com','repository':'AlecKriebel/Math','route':route,'exit':result.returncode,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout_pin':pin(result.stdout),'stderr_pin':pin(result.stderr),'raw_stdout':stdout,'raw_stderr':stderr,'automatic_retry':False}
  self.write('raw/'+n+'.RECEIPT.json',encode(row));self.rows.append(row)
  try:
   need(sum(r['stdout_pin']['bytes'] for r in self.rows)<=MAX_WIRE,'Aggregate native wire cap')
   need(result.returncode==0 and not result.stderr,'Native GET exit0/empty stderr; no retry')
   value=self.h.decode(result.stdout);need(type(value) is dict,'Native metadata object')
   if immutable:need(value.get('sha')==route.rsplit('/',1)[1],'Native route identity');self.cache[route]=copy.deepcopy(value)
   return value
  except BaseException:self.failed=True;raise
 def tree(self,oid):
  if oid not in self.trees:
   need(len(self.trees)<MAX_TREES,'Native metadata tree count cap')
   entries=decode_tree(self.fetch('git/trees/'+oid),oid)
   need(sum(len(x) for x in self.trees.values())+len(entries)<=MAX_TREE_ENTRIES,'Native metadata aggregate entry cap')
   self.trees[oid]=entries
  return self.trees[oid]
 def lookup(self,oid,path):
  parts=path.split('/');need(len(parts)<=32 and all(x not in ('','.','..') for x in parts),'Finite targeted native path')
  for i,part in enumerate(parts):
   row=self.tree(oid).get(part)
   if row is None:return None
   if i<len(parts)-1:need(row['type']=='tree','Target ancestor tree');oid=row['sha']
  return row
 def descendants(self,oid,prefix,depth=0):
  need(depth<=20,'Owned subtree depth cap');out={}
  for name,row in self.tree(oid).items():
   path=prefix+'/'+name
   if row['type']=='tree':out.update(self.descendants(row['sha'],path,depth+1))
   else:out[path]=row
   need(len(out)<=10000,'Metadata owned leaf cap')
  return out
 def blob(self,oid):
  if oid not in self.blobs:
   raw=decode_blob(self.fetch('git/blobs/'+oid),oid)
   need(self.decoded+len(raw)<=MAX_DECODED,'Aggregate decoded native body cap')
   self.blobs[oid]={'pin':pin(raw),'private_body':self.write('bodies/'+oid,raw)};self.decoded+=len(raw)
   return raw
  raw=regular(self.out/self.blobs[oid]['private_body']['path'],MAX_BODY)
  need(pin(raw)==self.blobs[oid]['pin'] and native('blob',raw)==oid,'Existing private native body changed');return raw
 def commit(self,oid,root=None,parents=None):
  if oid not in self.commits:
   j=self.fetch('git/commits/'+oid);raw=raw_commit(j)
   self.commits[oid]={'sha':oid,'tree':j['tree']['sha'],'parents':[p['sha'] for p in j['parents']],'raw_commit':self.write('commits/'+oid+'.commit',raw)}
  record=self.commits[oid]
  need(root is None or record['tree']==root,'Expected exact commit root')
  need(parents is None or record['parents']==parents,'Expected exact ordered parents')
  return record
 def pr(self):
  j=self.fetch('pulls/218',fresh=True)
  need(type(j.get('number')) is int and j['number']==218 and j['head']['sha']==CURRENT and j['head']['ref']==self.intake['dated_registry_row']['headRefName'] and j.get('state')=='closed' and j.get('merged') is True and j.get('draft') is False and j.get('merge_commit_sha')==MERGE and j.get('merged_at')=='2026-10-15T07:35:42Z' and j.get('commits')==3,'Fresh exact already-merged218 PR identity')
  need(j.get('title')=='30006020: audited intermediate-area cylinder theorem and published preprint','Exact opaque current title')
  return {k:j.get(k) for k in ('number','state','draft','merged','merge_commit_sha','merged_at','updated_at','title','head','base','commits')}
 def main(self):
  j=self.fetch('git/ref/heads/main',fresh=True);need(j.get('ref')=='refs/heads/main' and j['object']['type']=='commit' and hexid(j['object']['sha']),'Fresh Main ref');return j['object']['sha']
 def diff(self,left,right,prefix='',depth=0):
  need(depth<=32,'Native diff depth cap')
  if left==right:return []
  a={} if left is None else self.tree(left);b={} if right is None else self.tree(right);out=[]
  for name in sorted(set(a)|set(b)):
   old=a.get(name);new=b.get(name);path=(prefix+'/' if prefix else '')+name
   if old==new:continue
   if (old is None or old['type']=='tree') and (new is None or new['type']=='tree'):
    out.extend(self.diff(old['sha'] if old else None,new['sha'] if new else None,path,depth+1))
   elif (old and old['type']=='tree') or (new and new['type']=='tree'):
    for side,node in (('old',old),('new',new)):
     if node and node['type']=='tree':
      out.extend({'path':p,'old':r if side=='old' else None,'new':r if side=='new' else None} for p,r in self.descendants(node['sha'],path).items())
     elif node:out.append({'path':path,'old':node if side=='old' else None,'new':node if side=='new' else None})
   else:out.append({'path':path,'old':old,'new':new})
   need(len(out)<=MAX_DIFF_LEAVES,'Full original/current changed native leaf bound')
  return out
 def owned_diff(self,left,right):
  out=[]
  for label in ('attempt','old_publication_audit'):
   a=left['owned'][label];b=right['owned'][label]
   need(a['path']==b['path'],'Exact owned diff prefix')
   out.extend(self.diff(a['node']['sha'] if a['node'] else None,b['node']['sha'] if b['node'] else None,a['path']))
  return out
 def snapshot(self,role,commit):
  root=commit['tree'];trees={}
  for label,path in (('attempt',ATTEMPT),('old_publication_audit',OLD_AUDIT)):
   node=self.lookup(root,path)
   need(node is None or node['type']=='tree','Owned scope must be subtree')
   leaves=self.descendants(node['sha'],path) if node else {}
   if label=='attempt' and role!='original_parent':need(node is not None and bool(leaves),'Attempt required for original/current/merge/Main; parent absence is factual')
   trees[label]={'path':path,'node':node,'leaves':leaves}
  q=self.lookup(root,QUEUE);need(q is not None and (q['mode'],q['type'])==('100644','blob'),'Whole ordinary native QUEUE')
  critical={p:self.lookup(root,p) for p in CRITICAL}
  return {'commit':commit,'owned':trees,'queue_tuple':q,'publication_critical_path_tuples':critical}
 def bodies_for(self,role,snapshot):
  records=[];leaves={}
  for scope,record in snapshot['owned'].items():leaves.update(record['leaves'])
  need(len(leaves)<=MAX_ROLE_FILES,'Role exceeds400 owned files; metadata retained for Root scope decision')
  total=0
  for path,node in sorted(leaves.items()):
   need(node['type']=='blob' and node['mode'] in ('100644','100755','120000'),'Gitlink body requires separate Root scope decision')
   raw=self.blob(node['sha']);total+=len(raw);need(total<=MAX_ROLE_BYTES,'Role exceeds8MB decoded; metadata retained for Root scope decision')
   records.append({'path':path,**node,**pin(raw),'private_body':self.blobs[node['sha']]['private_body']})
  q=snapshot['queue_tuple'];raw=self.blob(q['sha']);row=own_queue_row(raw)
  if role=='original':
   need(pin(raw)=={k:self.intake['preserved_QUEUE_blob'][k] for k in ('bytes','sha256')} and q['sha']==self.intake['preserved_QUEUE_blob']['git_blob'] and row['row_pin']==self.intake['preserved_QUEUE_row_pin'] and row['status']=='claimed_solved' and row['effort']=='1/5','Exact preserved original eligible row/whole QUEUE')
  if role=='current':
   need(q['sha']==self.status['current_QUEUE_tuple']['sha'] and pin(raw)=={k:self.status['current_QUEUE_body'][k] for k in ('bytes','sha256')} and row['row_pin']==self.status['current_own_row_pin'] and row['status']=='claimed_solved' and row['effort']=='1/5','Exact current claimed row/whole QUEUE')
  return {'full_owned_bodies':records,'owned_file_count':len(records),'owned_decoded_bytes':total,'queue':{**q,**pin(raw),**row,'private_body':self.blobs[q['sha']]['private_body']}}
 def run(self):
  start=self.main();before=self.pr()
  commits={'original_parent':self.commit(ORIGINAL_PARENT),'original':self.commit(ORIGINAL,ORIGINAL_ROOT,[ORIGINAL_PARENT]),'current':self.commit(CURRENT,CURRENT_ROOT,CURRENT_PARENTS),'merge':self.commit(MERGE),'Main':self.commit(start)}
  need(commits['merge']['parents'][-1]==CURRENT and len(commits['merge']['parents'])==2,'Actual merge ordered current-HEAD association; no root equality inferred')
  comparison=self.fetch('compare/'+MERGE+'...'+start)
  need(comparison.get('status') in ('ahead','identical') and comparison['merge_base_commit']['sha']==MERGE,'Actual merged commit must be ancestor of observed Main')
  snapshots={role:self.snapshot(role,commit) for role,commit in commits.items()}
  changes=self.owned_diff(snapshots['original'],snapshots['current'])
  left=self.tree(ORIGINAL_ROOT);right=self.tree(CURRENT_ROOT)
  root_changes=[{'path':p,'old':left.get(p),'new':right.get(p)} for p in sorted(set(left)|set(right)) if left.get(p)!=right.get(p)]
  self.write('SCOPE_METADATA.json',encode({'schema':'pr218-native-custody-scope-v1','snapshots':snapshots,'original_to_current_owned_changed_native_leaves':changes,'immediate_root_changed_tuples_without_foreign_descent':root_changes,'no_foreign_bodies_copied':True}))
  bodies={role:self.bodies_for(role,value) for role,value in snapshots.items()}
  original=snapshots['original']['owned']['attempt']['leaves'];current=snapshots['current']['owned']['attempt']['leaves']
  history={}
  for path,node in original.items():
   suffix=path.removeprefix(ATTEMPT+'/')
   found=[p for p,n in current.items() if p.startswith(ATTEMPT+'/history/') and p.endswith('/'+suffix) and n==node]
   history[path]={'matching_current_history_paths':found,'exact_mode_type_native_body':bool(found)}
  # Factual evidence, not a guessed preservation assertion when history is absent.
  after=self.pr();need(before==after,'PR identity changed during custody')
  end=self.main();need(end==start,'Main advanced during custody: stale capture, no silent rebind/retry')
  need(pin(regular(Path(__file__).absolute()))==self.source_pin,'Capture source drift')
  result={'schema':'pr218-native-full-custody-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'evidence_scope':'ACTUAL_GET_CUSTODY_ONLY','source_pin':self.source_pin,
   'helper_pin':HELPER_PIN,'intake_pin':INTAKE_PIN,'Root_current_status_pin':STATUS_PIN,
   'start_Main':start,'end_Main':end,'coherent_Main_ref':True,'PR_before':before,'PR_after':after,
   'snapshots':snapshots,'body_records':bodies,'original_history_associations':history,
   'all_original_bodies_present_in_current_history':all(v['exact_mode_type_native_body'] for v in history.values()),
   'original_to_current_owned_changed_native_leaves':changes,'immediate_root_changed_tuples_without_foreign_descent':root_changes,'aggregate_unique_decoded_bytes':self.decoded,
   'API_calls':len(self.rows),'API_stdout_bytes':sum(r['stdout_pin']['bytes'] for r in self.rows),
   'original_eligible_status':'claimed_solved','current_status':'claimed_solved',
   'mathematical_priority_publication_or_checkpoint_acceptance':False,
   'opening_transaction_HEAD_author_turns_firstness_or_current_root_equality_inferred':False,
   'no_submitted_scientific_script_execution':True}
  self.write('AUTHENTICATED_TREES.json',encode(self.trees));self.write('API_LEDGER.json',encode(self.rows))
  self.write('CUSTODY_SUMMARY.json',encode(result))
  self.write('PRIVATE_EVIDENCE_MANIFEST.json',encode({'schema':'pr218-native-private-evidence-manifest-v1','files':self.paths.copy(),'private_original_current_Main_native_bodies_not_for_blanket_public_export':True}))
  return {'output':str(self.out),'summary_pin':pin(encode(result)),'API_calls':len(self.rows),'roles':{r:v['owned_file_count'] for r,v in bodies.items()},'math_acceptance':False}
 def close(self):os.close(self.fd)
def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Use python3.11 -E -S -B -P without optimization')
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('output_child',help='Fresh _private_capture_NAME child inside this source folder');args=p.parse_args()
 capture=Capture(args.output_child)
 try:print(json.dumps(capture.run(),sort_keys=True))
 except BaseException as exc:
  capture.write('CAPTURE_STOPPED.json',encode({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exception':type(exc).__name__,'reason':str(exc),'successful_complete_summary_authority':False,'no_automatic_retry':True}));raise
 finally:capture.close()
if __name__=='__main__':main()

