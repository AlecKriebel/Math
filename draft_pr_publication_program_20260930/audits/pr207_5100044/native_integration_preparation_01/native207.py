"""PR207 two-phase native objects and independent GET verification; no ref writer.
Import is inert. Operational CLI requires ordinary Python -E -S -B -P.
Only candidate allows POST, and only git/blobs, git/trees and git/commits.
Root supplies frozen actual inputs; this preparer supplies no actual authority.
"""
import argparse, base64, datetime, fcntl, hashlib, importlib.util, json, math, os, re, stat, subprocess, sys
from pathlib import Path, PurePosixPath

BASE=Path(__file__).absolute().parent
A=BASE.parent
P=A.parents[1]
C=P.parent
PROGRAM='draft_pr_publication_program_20260930/'
CASE=PROGRAM+'audits/pr207_5100044/'
ATTEMPT='unsolved_math_prioritization/attempts/5100044/'
QUEUE='unsolved_math_prioritization/QUEUE.md'
VIEWS=(CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md',PROGRAM+'CURRENT_PROGRESS.json',PROGRAM+'CURRENT_PROGRESS.md',PROGRAM+'RESEARCH_LOG.md')
ANCHOR='063dd13ada2e9fc004f2fcb919f1ccefbbb895a9'
HEAD='a7f8486548122c7d545430821afeedbccf48b3e7'
HEAD_TREE='d5711f92b999c72068a38726ae552e894b350c1a'
CORE_PIN={'bytes':22049,'sha256':'8a61aee886e7a19bba6c7369944d778614b4099cbe1a060cf7e8acf2f52ec4d5'}
INVENTORY_PIN={'bytes':6874,'sha256':'6923e78c3306a40bba66cdbe1a7b901b811a7d3ef51a07824ca3d81ed62d8e40'}
DELTA_PIN={'bytes':6012,'sha256':'f21c2f8fdac614365afe6860bfd5d956a18ebcbe607085f983653eb5a3df854d'}
QUEUED_ROW_PIN={'bytes':123,'sha256':'3f0adcd50022e57df962becd3fb600e0d1e59dc6ebeb2ddb5627ea7ea299a4d1'}
LOCK_BYTES=b'PR publication program: stable Root cooperating global-five writer lock v1\nNever unlink or replace this inode; every existing-view writer must flock it.\n'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
MAX_FILES=1500
MAX_BODY=8000000

def need(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def compact(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
def decode(raw):
 def pairs(items):
  result={}
  for k,v in items:need(k not in result,'Duplicate JSON key');result[k]=v
  return result
 def finite(value):
  number=float(value);need(math.isfinite(number),'Nonfinite JSON');return number
 return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda _:need(False,'Nonfinite JSON'))
def hexid(v,n=40):return type(v) is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',v) is not None
def rel(v):
 need(type(v) is str and v and not PurePosixPath(v).is_absolute() and '\\' not in v and all(ord(x)>=32 and ord(x)!=127 for x in v) and all(x not in ('','.','..') for x in v.split('/')) and len(v.encode())<=4096,'Unsafe relative path')
 return v
def bytepin(v):
 need(type(v) is dict and set(v)=={'bytes','sha256'} and type(v['bytes']) is int and 0<=v['bytes']<=MAX_BODY and hexid(v['sha256'],64),'Exact bounded byte pin required');return v
def tuple_pin(v):
 if v is None:return None
 need(type(v) is dict and set(v)=={'mode','type','sha'} and (v['mode'],v['type'])==('100644','blob') and hexid(v['sha']),'Exact regular-blob preimage required')
 return v['mode'],v['type'],v['sha']
def sealed(path,wanted=None):
 need(path.is_absolute() and path.resolve()==path,'Canonical source path required')
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  before=os.fstat(fd);need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444 and before.st_size<=MAX_BODY,'Readonly bounded regular source required')
  with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read(MAX_BODY+1)
  after=os.fstat(fd);entry=path.lstat()
  need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns) and (after.st_dev,after.st_ino)==(entry.st_dev,entry.st_ino) and stat.S_ISREG(entry.st_mode) and stat.S_IMODE(entry.st_mode)==0o444 and len(raw)==after.st_size,'Source changed during read')
 finally:os.close(fd)
 if wanted is not None:need(pin(raw)==bytepin(wanted),'Pinned source changed')
 return raw
def owned(name,wanted=None):return sealed(BASE/rel(name),wanted)
def core():
 path=BASE/'archive206_verified_reference.py';sealed(path,CORE_PIN)
 spec=importlib.util.spec_from_file_location('pr207_owned_audited_native_trees',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def durable_dir(path):
 fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
def put(directory,name,value):
 need(directory.resolve()==directory and directory.is_dir() and Path(name).name==name,'Canonical journal basename/directory')
 fd=os.open(directory/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
 try:
  with os.fdopen(fd,'wb',closefd=False) as f:
   raw=enc(value);need(f.write(raw)==len(raw),'Short journal write');f.flush();os.fchmod(fd,0o444);os.fsync(fd)
 finally:os.close(fd)
 durable_dir(directory)
def journal_new(name):
 need(type(name) is str and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,79}',name) is not None,'Owned journal basename required')
 path=BASE/name;need(BASE.resolve()==BASE and not path.exists() and not path.is_symlink(),'Fresh exclusive attempt required')
 path.mkdir(mode=0o700);durable_dir(path);durable_dir(BASE);return path

def phase_facts(phase):
 need(phase in ('merge95','completion100'),'Exactly two supported phases')
 done=phase=='completion100'
 return {'active_PR':207,'case_workflow_estimate_percent':100 if done else 95,'fully_completed_count':50 if done else 49,'published_count':34,'last_completed_PR':207 if done else 206,'next_numeric_intake_cursor':208 if done else 207,'advance_to_next_PR_authorized_now':done,'goal_complete':False,'completed':done,'publication_ready':True}
def matches(obj,wanted,msg):
 need(type(obj) is dict,msg)
 for k,v in wanted.items():need(type(obj.get(k)) is type(v) and obj[k]==v,msg+': '+k)
def marker(facts):return ('<!-- PR207_NATIVE_PHASE_FACTS '+compact(facts)+' -->').encode()
def queue_change(old,new,phase):
 def split(raw):
  lines=raw.splitlines(keepends=True)
  rows=[i for i,line in enumerate(lines) if re.match(rb'^\|[^|]*\|\s*5100044\s*/',line)]
  need(len(rows)==1,'Exactly one own QUEUE row required');return lines,rows[0]
 before,i=split(old);after,j=split(new)
 need(i==j and len(before)==len(after) and before[:i]==after[:j] and before[i+1:]==after[j+1:],'Foreign QUEUE bytes/line order changed')
 a=before[i].split(b'|');b=after[j].split(b'|')
 need(len(a)==len(b)==14 and b[8].strip()==b'claimed_solved' and b[9].strip()==b'1/5','Submitted historical status/effort must remain literal')
 if phase=='merge95':need(pin(before[i])==QUEUED_ROW_PIN,'Only exact captured queued/0/5 own preimage accepted for merge95')
 else:need(phase=='completion100' and old==new and a[8].strip()==b'claimed_solved' and a[9].strip()==b'1/5','completion100 QUEUE must remain byteexact accepted claimed_solved/1/5 postimage')
 need(all(a[k]==b[k] for k in range(14) if k not in (8,9,11,12)),'Only own status/effort/findings/DOI cells may change')
 need(before[i].endswith(b'\n')==after[j].endswith(b'\n'),'Own QUEUE newline changed')

def inputs(manifest,wanted):
 c=core();need(manifest.is_relative_to(BASE),'Owned manifest required');raw=sealed(manifest,wanted);m=decode(raw)
 need(type(m) is dict and m.get('schema')=='pr207-native-integration-inputs-v1' and m.get('PR')==207 and type(m.get('PR')) is int,'PR207 frozen manifest schema')
 need(m.get('anchor')==ANCHOR and m.get('original_head')==HEAD and m.get('original_head_tree')==HEAD_TREE and hexid(m.get('expected_parent')),'Exact Root expected SHA/original identity')
 need(m.get('helper_pin')==pin(sealed(Path(__file__).absolute())) and m.get('core_pin')==CORE_PIN,'Explicit helper/core binding')
 facts=phase_facts(m.get('phase'));need(type(m.get('facts')) is dict and set(m['facts'])==set(facts),'Exact phase fact fields');matches(m['facts'],facts,'Exact phase counters and gates')
 rows=m['files'];need(type(rows) is list and 0<len(rows)<=MAX_FILES,'Bounded explicit file overlay')
 overlay={};pre={};sourcepins={}
 for row in rows:
  need(type(row) is dict and set(row)=={'path','source','bytes','sha256','git_blob','preimage'},'Exact overlay row fields')
  path=rel(row['path']);need(path.startswith(CASE) or path.startswith(ATTEMPT) or path in VIEWS[2:] or path==QUEUE,'Foreign overlay refused')
  need(path not in overlay,'Duplicate overlay path')
  body=owned(row['source'],{k:row[k] for k in ('bytes','sha256')});need(c.native('blob',body)==row['git_blob'],'Selected blob SHA1 differs')
  overlay[path]=body;pre[path]=tuple_pin(row['preimage']);sourcepins[path]={'source':row['source'],**pin(body),'mode':'100644','type':'blob','git_blob':row['git_blob']}
 need(type(m.get('total_files')) is int and m['total_files']==len(rows) and type(m.get('total_bytes')) is int and m['total_bytes']==sum(map(len,overlay.values()))<=40000000,'Exact bounded count/byte totals')
 # The custody metadata fixes the native QUEUE location; no root-level QUEUE alias exists.
 delta=decode(owned('CUSTODY_DELTA.json',DELTA_PIN));q=[x for x in delta['changes'] if not x['path'].startswith(ATTEMPT)]
 need(len(q)==1 and q[0]['path']==QUEUE,'Custody QUEUE path differs')
 inventory=decode(owned('CUSTODY_INVENTORY.json',INVENTORY_PIN));need(len(inventory)==20 and sum(x['bytes'] for x in inventory.values())==61131,'Original twenty-file custody')
 need({x for x in overlay if x.startswith(ATTEMPT)}=={ATTEMPT+x for x in inventory}|{ATTEMPT+'requirements.txt',ATTEMPT+'current_execution_receipt.json'},'Native attempt must be exactly original twenty names plus two additions')
 for name,identity in inventory.items():
  body=overlay.get(CASE+'submitted_snapshot/'+name);need(type(body) is bytes and pin(body)=={k:identity[k] for k in ('bytes','sha256')} and c.native('blob',body)==identity['git_blob'],'Every original archive body must be preserved byteexact')
 need(all(x in overlay for x in VIEWS),'Exact five selected views required')
 for path in (VIEWS[0],VIEWS[2]):
  obj=decode(overlay[path]);matches(obj,facts,'Structured current view facts differ')
  for alias,key in (('current_case_percent','case_workflow_estimate_percent'),('workflow_percent','case_workflow_estimate_percent'),('case_percent','case_workflow_estimate_percent'),('current_publication_ready','publication_ready')):
   if alias in obj:matches(obj,{alias:facts[key]},'Current view fact alias differs')
 progress=decode(overlay[VIEWS[2]])
 for key,count in (('published_PRs',facts['published_count']),('fully_completed_eligible_PRs',facts['fully_completed_count'])):
  values=progress.get(key);need(type(values) is list and all(type(x) is int and 1<=x<=207 for x in values) and len(values)==len(set(values))==count,'Exact current program membership/count: '+key)
  need((207 in values)==(key=='published_PRs' or m['phase']=='completion100'),'Phase current program PR207 membership: '+key)
 need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total']==99,'Preserved dated eligible denominator')
 if 'fully_completed_fraction_percent' in progress:need(type(progress['fully_completed_fraction_percent']) in (int,float) and math.isfinite(progress['fully_completed_fraction_percent']) and abs(progress['fully_completed_fraction_percent']-100*facts['fully_completed_count']/99)<1e-12,'Current completed fraction alias differs')
 for path in (VIEWS[1],VIEWS[3],VIEWS[4]):
  need(overlay[path].count(b'<!-- PR207_NATIVE_PHASE_FACTS ')==1 and marker(facts) in overlay[path].splitlines(),'Markdown current facts marker differs')
 views=m['local_views'];need(type(views) is list and len(views)==5 and {x['path'] for x in views}==set(VIEWS),'Exactly five local preimages')
 for row in views:
  need(set(row)=={'path','preimage'} and (row['preimage'] is None or bytepin(row['preimage'])) is not False,'Explicit local byte preimage')
 # Root authors this actual envelope after publication/tracker/review, never this preparer.
 gatepath=rel(m['gate_receipt']);need(gatepath.startswith(CASE) and gatepath in overlay,'Actual gates must be in selected case scope')
 gates=decode(overlay[gatepath]);matches(gates,{'schema':'pr207-root-native-phase-gates-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':m['phase'],'accepted':True,'original_head':HEAD,'facts':facts,'scientific_accepted':True,'whole_package_accepted':True,'actual_publication_verified':True,'actual_tracker_verified':True,'ready_for_merge':True},'Actual scientific/publication/tracker/gate envelope required')
 need(type(gates['facts']) is dict and set(gates['facts'])==set(facts),'Actual gate fact fields');matches(gates['facts'],facts,'Actual gate fact types')
 roles={'scientific','whole_package_review','publication','tracker'}|({'ready_PR_merge'} if m['phase']=='completion100' else set())
 receipts=gates['receipts'];need(type(receipts) is dict and set(receipts)==roles,'Exact phase evidence roles required')
 for role,e in receipts.items():
  need(type(e) is dict and set(e)=={'path','bytes','sha256'} and e['path'] in overlay and e['path']!=gatepath and pin(overlay[e['path']])=={k:e[k] for k in ('bytes','sha256')},'Explicit actual evidence pin: '+role)
 need(type(m.get('commit_message')) is str and 1<=len(m['commit_message'].encode())<=1000 and '\0' not in m['commit_message'],'Bounded explicit commit message')
 return c,m,overlay,pre,sourcepins

class API:
 """Fresh attempt only. Each object mutation has a durable intent before dispatch."""
 def __init__(self,journal,mutate=False):self.journal=journal;self.mutate=mutate;self.number=0;self.failed=False
 def __call__(self,method,path,body=None):
  need(not self.failed,'Attempt stopped; inspect read-only with a new journal')
  get=path in ('git/ref/heads/main','pulls/207') or re.fullmatch(r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',path) is not None or re.fullmatch(r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',path) is not None
  need((method=='GET' and get and body is None) or (method=='POST' and self.mutate and path in ('git/blobs','git/trees','git/commits') and type(body) is dict),'No ref/service/other mutation route')
  self.number+=1;name=str(self.number).zfill(5)
  request={'method':method,'path':path,'request_pin':pin(enc(body)) if body is not None else None}
  if method=='POST':put(self.journal,name+'.OBJECT_INTENT.json',{**request,'semantics':'One dispatch only. Any uncertainty stops this attempt; no mutation retry.'})
  argv=[GH,'api','--method',method,'repos/AlecKriebel/Math/'+path]
  if body is not None:argv+=['--input','-']
  try:
   result=subprocess.run(argv,input=enc(body) if body is not None else None,capture_output=True,timeout=120)
   receipt={**request,'exit':result.returncode,'stdout_pin':pin(result.stdout),'stderr_pin':pin(result.stderr)}
   put(self.journal,name+'.API_RECEIPT.json',receipt)
   need(result.returncode==0,'Native API failed; outputs suppressed, no retry')
   value=decode(result.stdout);need(type(value) is dict,'Native API object required')
   if method=='POST':
    need(hexid(value.get('sha')),'Native object result SHA required');put(self.journal,name+'.OBJECT_RESULT.json',{**request,'returned_sha':value['sha']})
   return value
  except BaseException as error:
   self.failed=True
   put(self.journal,name+'.STOPPED.json',{**request,'outcome_unknown':True,'exception_type':type(error).__name__})
   raise RuntimeError('Attempt stopped; inspect same object read-only, never retry automatically') from None

def expected(c,trees,root,overlay,pre):
 trie={};changed=set();dirs=set()
 for path,body in overlay.items():
  parts=rel(path).split('/');need(len(parts)-1<=c.MAX_DEPTH,'Overlay depth bound');node=trie
  for name in parts[:-1]:need(name not in node or type(node[name]) is dict,'Overlay ancestor/file collision');node=node.setdefault(name,{})
  need(parts[-1] not in node,'Overlay leaf/ancestor collision');node[parts[-1]]=body
 def rebuild(oid,node,prefix,depth):
  need(depth<=c.MAX_DEPTH,'Overlay recursion bound');entries=dict(trees.get(oid,depth)) if oid is not None else {}
  for name,body in node.items():
   path=prefix+name;old=entries.get(name)
   if type(body) is bytes:
    # Frozen preimages describe fresh MAIN, even if the selected body is unchanged.
    need(old==pre[path],'Fresh native preimage tuple differs: '+path)
    wanted=('100644','blob',c.native('blob',body))
    if old!=wanted:changed.add(path)
    entries[name]=wanted
   else:
    need(old is None or old[:2]==('040000','tree'),'Overlay native ancestor is a leaf')
    if old is None:dirs.add(path)
    entries[name]=('040000','tree',rebuild(old[2] if old else None,body,path+'/',depth+1))
  return c.tree_hash([(name,*entry) for name,entry in entries.items()])
 return rebuild(root,trie,'',0),changed,dirs

def read_blob(c,api,oid):
 j=api('GET','git/blobs/'+oid);need(j.get('sha')==oid and j.get('encoding')=='base64' and type(j.get('size')) is int and 0<=j['size']<=MAX_BODY and type(j.get('content')) is str,'Bounded native blob')
 body=base64.b64decode(''.join(j['content'].split()),validate=True);need(len(body)==j['size'] and c.native('blob',body)==oid,'Native preimage body differs');return body
def original_pr(api,phase,after_cas=False):
 original=api('GET','git/commits/'+HEAD);need(original.get('sha')==HEAD and original['tree']['sha']==HEAD_TREE,'Exact original HEAD/tree')
 pr=api('GET','pulls/207');need(type(pr.get('number')) is int and pr['number']==207 and pr['head']['sha']==HEAD and pr['base']['ref']=='main' and pr.get('draft') is False,'Actual ready original PR identity')
 if phase=='completion100':need(pr.get('merged') is True and pr.get('state')=='closed' and hexid(pr.get('merge_commit_sha')),'Actual original ready PR merge required')
 elif after_cas:need((pr.get('merged') is False and pr.get('state')=='open') or (pr.get('merged') is True and pr.get('state')=='closed' and hexid(pr.get('merge_commit_sha'))),'After-CAS original PR transition differs')
 else:need(pr.get('merged') is False and pr.get('state')=='open','merge95 requires actual still-open ready PR')
 return pr
def state(c,m,overlay,pre,api,parent=None,after_cas=False):
 parent=parent or m['expected_parent'];need(parent==m['expected_parent'] and hexid(parent),'Externally pinned Root expected SHA differs')
 observed=api('GET','git/ref/heads/main')['object']['sha'];need(hexid(observed),'Native MAIN identity')
 if not after_cas:need(observed==parent,'Fresh MAIN parent lease differs')
 commit=api('GET','git/commits/'+parent);need(commit.get('sha')==parent and hexid(commit['tree']['sha']),'Parent/tree native identity')
 if parent!=ANCHOR:
  compare=api('GET','compare/'+ANCHOR+'...'+parent);need(compare.get('status')=='ahead' and compare['merge_base_commit']['sha']==ANCHOR,'Parent must descend from fixed accepted anchor')
 pr=original_pr(api,m['phase'],after_cas)
 if m['phase']=='completion100':
  compare=api('GET','compare/'+HEAD+'...'+parent);need(compare.get('status')=='ahead' and compare['merge_base_commit']['sha']==HEAD,'Actual merged original HEAD must be ancestor of completion parent')
 trees=c.NativeTrees(api);wanted,changed,dirs=expected(c,trees,commit['tree']['sha'],overlay,pre)
 if QUEUE in overlay:
  need(pre[QUEUE] is not None,'QUEUE cannot be added/deleted');queue_change(read_blob(c,api,pre[QUEUE][2]),overlay[QUEUE],m['phase'])
 if not after_cas:need(api('GET','git/ref/heads/main')['object']['sha']==parent,'Fresh MAIN lease lost')
 parents=[parent,HEAD] if m['phase']=='merge95' else [parent]
 return {'parent':parent,'parent_tree':commit['tree']['sha'],'wanted':wanted,'changed':changed,'dirs':dirs,'parents':parents,'pr':pr}
def verify(c,m,overlay,pre,pins,api,parent,candidate,after_cas=False):
 need(hexid(candidate),'Candidate commit SHA required');s=state(c,m,overlay,pre,api,parent,after_cas)
 commit=api('GET','git/commits/'+candidate);need(commit.get('sha')==candidate and [x['sha'] for x in commit['parents']]==s['parents'] and commit['tree']['sha']==s['wanted'] and commit.get('message')==m['commit_message'],'Exact commit parents/tree/message differ')
 # New independent reader: construction cache cannot supply the verification tree.
 trees=c.NativeTrees(api);leaves,dirs,deleted=trees.changes(s['parent_tree'],s['wanted'])
 need(leaves==s['changed'] and dirs==s['dirs'] and not deleted,'Full changed-leaf/directory scope differs')
 selected={}
 for path,body in sorted(overlay.items()):
  oid=c.native('blob',body);need(trees.lookup(s['wanted'],path)==('100644','blob',oid),'Selected native tuple differs');c.blob_matches(api,oid,body)
  selected[path]={k:pins[path][k] for k in ('bytes','sha256','mode','type','git_blob')}
 observed=api('GET','git/ref/heads/main')['object']['sha']
 if not after_cas:need(observed==parent,'MAIN lease lost before verification success')
 return {'schema':'pr207-native-integration-verification-v1','phase':m['phase'],'facts':m['facts'],'parent':parent,'parents':s['parents'],'parent_tree':s['parent_tree'],'candidate':candidate,'tree':s['wanted'],'original_head':HEAD,'original_head_tree':HEAD_TREE,'selected_files':selected,'selected_file_count':len(selected),'selected_bytes':sum(map(len,overlay.values())),'changed_leaves':sorted(leaves),'new_directories':sorted(dirs),'deleted_directories':[],'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,'fresh_parent_lease_required':not after_cas,'actual_MAIN_observed':observed,'ref_actions_performed':False}
def plan(c,m,overlay,pre,pins,api):
 s=state(c,m,overlay,pre,api)
 return {'schema':'pr207-native-integration-plan-v1','status':'GET_ONLY_PLAN','phase':m['phase'],'facts':m['facts'],'parent':s['parent'],'parents':s['parents'],'parent_tree':s['parent_tree'],'tree':s['wanted'],'selected_files':pins,'changed_leaves':sorted(s['changed']),'new_directories':sorted(s['dirs']),'ref_actions_performed':False}
def candidate(c,m,overlay,pre,pins,api,journal):
 s=state(c,m,overlay,pre,api);need(bool(s['changed']),'Empty candidate refused')
 entries=[];binary={}
 for path,body in sorted(overlay.items()):
  try:
   text=body.decode('utf-8');need('\0' not in text,'Binary NUL');inline=True
  except (UnicodeError,RuntimeError):inline=False
  entry={'path':path,'mode':'100644','type':'blob'}
  if inline:entry['content']=text
  else:
   oid=c.native('blob',body)
   if oid not in binary:
    need(api('GET','git/ref/heads/main')['object']['sha']==s['parent'],'Lease lost before binary blob POST')
    result=api('POST','git/blobs',{'content':base64.b64encode(body).decode('ascii'),'encoding':'base64'});need(result.get('sha')==oid,'Binary blob POST differs');binary[oid]=True
   entry['sha']=oid
  entries.append(entry)
 need(api('GET','git/ref/heads/main')['object']['sha']==s['parent'],'Lease lost before tree POST')
 result=api('POST','git/trees',{'base_tree':s['parent_tree'],'tree':entries});need(result.get('sha')==s['wanted'],'Native tree POST differs')
 need(api('GET','git/ref/heads/main')['object']['sha']==s['parent'],'Lease lost before commit POST')
 result=api('POST','git/commits',{'message':m['commit_message'],'tree':s['wanted'],'parents':s['parents']});oid=result.get('sha');need(hexid(oid),'Native commit POST identity')
 put(journal,'CANDIDATE_IDENTITY.json',{'parent':s['parent'],'parents':s['parents'],'candidate':oid,'tree':s['wanted']})
 result=verify(c,m,overlay,pre,pins,api,s['parent'],oid);put(journal,'CANDIDATE_VERIFIED.json',result);return result

def local_pin(path):
 need(path.resolve()==path,'Canonical local view path')
 if not path.exists():need(not path.is_symlink(),'Absent view is symlink');return None
 need(stat.S_ISREG(path.lstat().st_mode),'Ordinary local view required');return pin(path.read_bytes())
def local_preimages(m,overlay,resume=False):
 for row in m['local_views']:
  now=local_pin(C/row['path']);need(now==row['preimage'] or (resume and now==pin(overlay[row['path']])),'Local view differs from explicit old/accepted postimage: '+row['path'])
class WriterLock:
 def __enter__(self):
  self.path=P/'ROOT_GLOBAL_FIVE_WRITER.lock';need(self.path.resolve()==self.path,'Canonical existing stable lock')
  self.fd=os.open(self.path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK);s=os.fstat(self.fd);self.identity=(s.st_dev,s.st_ino);self.pid=os.getpid()
  try:self.check();fcntl.flock(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB);self.check();return self
  except BaseException:os.close(self.fd);raise
 def check(self):
  a=os.fstat(self.fd);b=self.path.lstat();need(os.getpid()==self.pid and self.path.resolve()==self.path and stat.S_ISREG(a.st_mode) and stat.S_ISREG(b.st_mode) and (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino)==self.identity and stat.S_IMODE(a.st_mode)==stat.S_IMODE(b.st_mode)==0o444 and os.pread(self.fd,len(LOCK_BYTES)+1,0)==LOCK_BYTES,'Stable lock inode/payload changed')
 def __exit__(self,*unused):
  try:self.check()
  finally:
   try:fcntl.flock(self.fd,fcntl.LOCK_UN)
   finally:os.close(self.fd)
def acceptance(m,wanted,path,accept_pin):
 need(path.is_relative_to(BASE),'Owned actual acceptance required');a=decode(sealed(path,accept_pin))
 matches(a,{'schema':'pr207-root-native-integration-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':m['phase'],'accepted':True,'full_scope_verified':True,'all_selected_native_bodies_verified':True,'manifest_pin':wanted,'helper_pin':pin(sealed(Path(__file__).absolute())),'facts':m['facts'],'parent':m['expected_parent'],'original_head':HEAD,'original_head_tree':HEAD_TREE},'Externally byte-pinned actual Root acceptance required')
 need(type(a['facts']) is dict and set(a['facts'])==set(m['facts']),'Actual acceptance fact fields');matches(a['facts'],m['facts'],'Actual acceptance fact types')
 need(hexid(a.get('candidate')) and hexid(a.get('tree')) and a.get('actual_MAIN_observed')==a['candidate'],'Actual candidate/tree/readback required')
 matches(a.get('Root_ref_update'),{'expected_sha':a['parent'],'sha':a['candidate'],'force':False,'success_confirmed_by_actual_native_readback':True},'Actual external Root expectedSHA force=false CAS receipt required')
 return a
def sync(c,m,overlay,pre,pins,api,journal,wanted,accept_path,accept_pin):
 a=acceptance(m,wanted,accept_path,accept_pin)
 need(api('GET','git/ref/heads/main')['object']['sha']==a['candidate'],'Actual MAIN is not accepted candidate')
 # PR207 may now report merged, so after-CAS merge95 checks accept that transition.
 result=verify(c,m,overlay,pre,pins,api,a['parent'],a['candidate'],after_cas=True)
 need(result['tree']==a['tree'] and result['actual_MAIN_observed']==a['candidate'],'Actual full native readback differs')
 pointer=BASE/('ROOT_ACTUAL_'+m['phase'].upper()+'_POINTER.json');need(not pointer.exists() and not pointer.is_symlink(),'Actual phase pointer already exists')
 with WriterLock() as lock:
  local_preimages(m,overlay,resume=True);put(journal,'LOCAL_FIVE_SYNC_INTENT.json',{'acceptance_pin':accept_pin,'candidate':a['candidate'],'semantics':'Cooperating stable-inode lock; each file atomic, no five-file transaction.'})
  for i,row in enumerate(m['local_views']):
   path=C/row['path'];body=overlay[row['path']];new=pin(body);lock.check();now=local_pin(path)
   if now!=new:
    need(now==row['preimage'] and path.parent.resolve()==path.parent,'Local preimage changed before install')
    temp=path.parent/('.pr207-native-'+journal.name+'-'+str(i)+'.tmp');fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    try:
     with os.fdopen(fd,'wb',closefd=False) as f:need(f.write(body)==len(body),'Short local view write');f.flush();os.fchmod(fd,0o444);os.fsync(fd)
    finally:os.close(fd)
    lock.check();need(local_pin(path)==row['preimage'],'Local preimage changed before replace')
    if row['preimage'] is None:os.link(temp,path,follow_symlinks=False);temp.unlink()
    else:os.replace(temp,path)
    durable_dir(path.parent)
   need(local_pin(path)==new,'Installed postimage differs');put(journal,'VIEW_'+str(i)+'.json',{'path':row['path'],'postimage':new})
  lock.check();need(api('GET','git/ref/heads/main')['object']['sha']==a['candidate'],'MAIN moved before actual pointer')
  need(all(local_pin(C/path)==pin(overlay[path]) for path in VIEWS),'Exact all-five postimages required')
  receipt={'schema':'pr207-native-integration-five-sync-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':m['phase'],'facts':m['facts'],'candidate':a['candidate'],'tree':a['tree'],'acceptance_pin':accept_pin,'manifest_pin':wanted,'all_five_local_files_match_actual_checkpoint':True,'files':[{'path':path,'postimage':pin(overlay[path])} for path in VIEWS]}
  put(journal,'LOCAL_GLOBAL_FIVE_SYNC.json',receipt);lock.check();put(BASE,pointer.name,{'schema':'pr207-native-integration-actual-pointer-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':m['phase'],'facts':m['facts'],'candidate':a['candidate'],'tree':a['tree'],'acceptance_pin':accept_pin,'manifest_pin':wanted,'sync_path':str(journal/'LOCAL_GLOBAL_FIVE_SYNC.json'),'sync_pin':pin(enc(receipt)),'recorded_only_after_actual_ref_readback_and_exact_all_five_files':True})
 return receipt

def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Ordinary Python -E -S -B -P required')
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=('dry','plan','candidate','verify','sync'));ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--manifest-bytes',type=int,required=True);ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--journal');ap.add_argument('--parent');ap.add_argument('--candidate');ap.add_argument('--after-cas',action='store_true');ap.add_argument('--acceptance',type=Path);ap.add_argument('--acceptance-bytes',type=int);ap.add_argument('--acceptance-sha256');args=ap.parse_args()
 wanted=bytepin({'bytes':args.manifest_bytes,'sha256':args.manifest_sha256});c,m,overlay,pre,pins=inputs(args.manifest.absolute(),wanted)
 need(not args.after_cas or (args.action=='verify' and args.parent is not None),'Lease-free after-CAS only explicit readonly verify with parent')
 if args.action=='dry':
  local_preimages(m,overlay);print(compact({'status':'OFFLINE_DRY_ONLY','phase':m['phase'],'facts':m['facts'],'selected_files':pins,'total_files':len(overlay),'total_bytes':sum(map(len,overlay.values())),'actual_acceptance_inferred':False,'ref_actions_performed':False}));return
 journal=journal_new(args.journal);api=API(journal,mutate=args.action=='candidate');put(journal,'FROZEN_INPUT.json',{'manifest_path':str(args.manifest.absolute()),'manifest_pin':wanted,'helper_pin':pin(sealed(Path(__file__).absolute())),'action':args.action,'after_cas':args.after_cas})
 if args.action=='plan':local_preimages(m,overlay);result=plan(c,m,overlay,pre,pins,api);put(journal,'PLAN.json',result)
 elif args.action=='candidate':local_preimages(m,overlay);result=candidate(c,m,overlay,pre,pins,api,journal)
 elif args.action=='verify':need(args.parent is not None and args.candidate is not None,'Explicit parent/candidate required');result=verify(c,m,overlay,pre,pins,api,args.parent,args.candidate,args.after_cas);put(journal,'VERIFIED.json',result)
 else:
  need(args.acceptance is not None and args.acceptance_bytes is not None and args.acceptance_sha256 is not None,'Externally byte-pinned actual Root acceptance required');result=sync(c,m,overlay,pre,pins,api,journal,wanted,args.acceptance.absolute(),bytepin({'bytes':args.acceptance_bytes,'sha256':args.acceptance_sha256}))
 print(compact(result))
if __name__=='__main__':main()
