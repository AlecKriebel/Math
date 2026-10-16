"""Root-reviewed archive object preparation and separate read-only verification.
No ref update operation exists. Import performs no API call or file write.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path, PurePosixPath
import argparse, base64, datetime, hashlib, json, os, re, stat, subprocess
CASE='draft_pr_publication_program_20260930/audits/pr206_5100062/'
HEAD='488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7'
PROPOSAL='late_operations_archival_preparation_01/PROPOSED_NATIVE_ARCHIVE_INPUT_MANIFEST.json'
PROPOSAL_PIN={'bytes':153431,'sha256':'0304689e3ca555add5e66ead1259f8105be1032fc536c7dd806dd87f9864bdc7'}
AUTH='ROOT_LATE_OPERATIONS_ARCHIVE_AUTHORIZATION_01.json'
PROOF='ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json'
GEN='publication_lifecycle_preparation_02/completion100_01/'
VIEWS=(CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md')+tuple('draft_pr_publication_program_20260930/'+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md'))
MAX_ENTRIES=30000
MAX_DEPTH=64
INPUT_COUNT=154
INPUT_BYTES=1648944
def need(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pin(raw):return {'bytes':len(raw),'sha256':sha(raw)}
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def decode(raw):
 def pairs(items):
  result={}
  for k,v in items:need(k not in result,'Duplicate JSON key');result[k]=v
  return result
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:need(False,'Nonfinite JSON'))
def hexid(v,n=40):return type(v) is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',v) is not None
def rel(v):
 need(type(v) is str and v and not PurePosixPath(v).is_absolute() and '\\' not in v and '\0' not in v and all(x not in ('','.','..') for x in v.split('/')),'Unsafe relative path');return v
def bytepin(v):
 need(type(v) is dict and set(v)=={'bytes','sha256'} and type(v['bytes']) is int and 0<=v['bytes']<=4000000 and hexid(v['sha256'],64),'Exact bounded byte pin required');return v
def source(base,name,wanted):
 p=base/rel(name);need(p.resolve()==p and p.is_file() and not p.is_symlink() and stat.S_ISREG(p.stat().st_mode) and stat.S_IMODE(p.stat().st_mode)==0o444,'Canonical sealed regular input')
 raw=p.read_bytes();need(pin(raw)==bytepin(wanted),'Pinned input changed');return raw
def pinned(base,name,wanted):return decode(source(base,name,wanted))
def put(directory,name,value):
 need(directory.resolve()==directory and directory.is_dir() and not directory.is_symlink() and Path(name).name==name,'Canonical journal directory/basename')
 fd=os.open(directory/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
 try:
  with os.fdopen(fd,'wb',closefd=False) as f:
   raw=enc(value);need(f.write(raw)==len(raw),'Short journal write');f.flush();os.fchmod(fd,0o444);os.fsync(fd)
 finally:os.close(fd)
 fd=os.open(directory,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
def repository_root(base):return base.parents[2]
def conditions(base,authorization_pin):
 a=pinned(base,AUTH,authorization_pin)
 need(a.get('schema')=='pr206-root-late-operations-archive-authorization-v1' and a.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and type(a.get('PR')) is int and a.get('PR')==206 and a.get('accepted') is True,'Explicit Root archive authorization absent')
 need(a.get('create_archive_objects_only') is True and a.get('ref_update_authorized') is False and a.get('no_other_service_or_workflow_actions') is True,'Archive-only authority boundary')
 helper=Path(__file__);need(helper.resolve()==helper and helper.is_file() and not helper.is_symlink() and stat.S_IMODE(helper.stat().st_mode)==0o444 and a.get('helper_pin')==pin(helper.read_bytes()) and a.get('proposal_pin')==PROPOSAL_PIN,'Exact helper/proposal authority required')
 p=pinned(base,PROOF,a['completion_verification_pin'])
 need(p.get('schema')=='pr206-root-actual-completion-verification-v1' and p.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and type(p.get('PR')) is int and p.get('PR')==206 and p.get('original_HEAD')==HEAD,'Actual100 Root proof identity')
 for k in ('completed','all_five_local_views_match_actual_checkpoint','both_current_native_checker_pins_accepted'):need(p.get(k) is True,'Actual100 proof flag: '+k)
 need(p.get('next_status_only_intake_performed') is False and p.get('goal_complete') is False,'No next-intake/goal inference')
 for k in ('checkpoint_commit','tree','original_merge_commit','factual98_commit'):need(hexid(p.get(k)),'Actual100 proof native identity')
 counts={'fully_completed_count':49,'published_count':33,'last_completed_PR':206,'next_numeric_intake_cursor':207,'advance_to_next_PR_authorized_now':True,'goal_complete':False,'completed':True}
 for k,v in counts.items():need(type(p.get(k)) is type(v) and p[k]==v,'Actual100 proof count: '+k)
 need(type(p.get('workflow_percent')) is int and p['workflow_percent']==100,'Actual100 proof phase')
 links=[('completion_pointer_pin','actual_pointer_pin','ROOT_ACTUAL_COMPLETION_CHECKPOINT.json'),('completion_map_pin','actual_map_pin',GEN+'ACCEPTANCE_CURRENT_SELECTED_MAP.json'),('completion_sync_pin','actual_sync_pin',GEN+'LOCAL_GLOBAL_FIVE_SYNC.json')]
 objects={}
 for ak,pk,path in links:
  need(a[ak]==p[pk],'Actual100 authority/proof cross-pin');objects[ak]=pinned(base,path,a[ak])
 ap=p['actual_acceptance'];need(type(ap) is dict and set(ap)=={'path','bytes','sha256'} and ap['path']==GEN+'ACCEPTANCE.json' and {k:ap[k] for k in ('bytes','sha256')}==a['completion_acceptance_pin'],'Actual100 acceptance path/pin')
 ac=pinned(base,ap['path'],a['completion_acceptance_pin']);ptr=objects['completion_pointer_pin'];sy=objects['completion_sync_pin'];m=objects['completion_map_pin']
 need(ac.get('schema')=='pr206-lifecycle-actual-acceptance-v1' and ac.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and type(ac.get('PR')) is int and ac.get('PR')==206 and ac.get('phase')=='completion' and ac.get('accepted') is True and type(ac.get('case_percent')) is int and ac['case_percent']==100,'Full actual100 acceptance absent')
 for k in ('every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','original_native_custody_retained','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged'):need(ac.get(k) is True,'Incomplete actual100 scope: '+k)
 need(ac.get('original_head')==ac.get('actual_original_PR_head')==HEAD and ac.get('actual_original_PR_is_draft') is False and ac.get('actual_original_PR_state')=='closed','Actual100 original PR facts')
 for k,v in counts.items():need(type(ac.get(k)) is type(v) and ac[k]==v and type(ac['facts'].get(k)) is type(v) and ac['facts'][k]==v,'Actual100 counters/aliases')
 need(ptr.get('schema')=='pr206-lifecycle-actual-pointer-v1' and type(ptr.get('PR')) is int and ptr.get('PR')==206 and ptr.get('phase')=='completion' and ptr.get('directory')==GEN[:-1] and ptr.get('Root_recorded_only_after_actual_full_scope_acceptance') is True,'Actual100 full pointer absent')
 need(sy.get('schema')=='pr206-lifecycle-five-sync-v1' and type(sy.get('PR')) is int and sy.get('PR')==206 and sy.get('phase')=='completion' and sy.get('all_five_local_files_match_actual_checkpoint') is True and sy.get('facts')==ac['facts'],'Actual100 full sync absent')
 need(ptr['acceptance_pin']==sy['acceptance_pin']==a['completion_acceptance_pin'] and ptr['checkpoint_commit']==sy['actual_checkpoint']==ac['checkpoint_commit']==p['checkpoint_commit'] and ptr['main_observed']==ac['main_observed'] and ac['actual_tree']==p['tree'],'Actual100 receipt/sync/pointer chain')
 need(ac['actual_current_map_file']==a['completion_map_pin'],'Actual100 selected-map pin')
 selected=m['selected_files'];need(type(selected) is dict and 0<len(selected)<=MAX_ENTRIES,'Bounded actual100 selected map')
 for path,v in selected.items():
  rel(path);need(type(v) is dict and set(v)=={'bytes','sha256','git_blob'} and type(v['bytes']) is int and v['bytes']>=0 and hexid(v['sha256'],64) and hexid(v['git_blob']),'Actual100 selected identity')
 digest=sha(json.dumps(selected,sort_keys=True,separators=(',',':')).encode())
 need(type(p['selected_files']) is int and type(ac['selected_files']) is int and len(selected)==p['selected_files']==ac['selected_files'] and digest==m['selected_map_sha256']==ac['actual_current_selected_map_sha256']==p['selected_map_sha256'],'Actual100 full map count/digest')
 rows=sy['files'];need(type(rows) is list and len(rows)==5 and {x['path'] for x in rows}==set(VIEWS),'Exact five synced postimages')
 for row in rows:
  need(set(row)=={'path','postimage'} and row['postimage']=={k:selected[row['path']][k] for k in ('bytes','sha256')},'Five-sync historical map identity')
  raw=source(repository_root(base),row['path'],row['postimage']);need(native('blob',raw)==selected[row['path']]['git_blob'],'Current five readonly local postimages differ')
 proposal=pinned(base,PROPOSAL,PROPOSAL_PIN);need(proposal['total_files']==INPUT_COUNT and proposal['total_bytes']==INPUT_BYTES and len(proposal['files'])==INPUT_COUNT and proposal['status']=='PROPOSED_NOT_ARCHIVED','Exact154 proposal')
 overlay={}
 for e in proposal['files']:
  path=rel(e['path']);name=rel(e['case_relative_path']);need(path==CASE+name and path not in overlay and e['source_path']==str(base/name),'Exact allowlist source/target')
  raw=source(base,name,{k:e[k] for k in ('bytes','sha256')});need(raw.decode('utf-8').encode('utf-8')==raw and b'\0' not in raw and native('blob',raw)==e['git_blob'] and e['source_mode']=='0o444','Inline UTF8 source identity')
  overlay[path]=raw
 need(sum(len(raw) for raw in overlay.values())==INPUT_BYTES,'Exact allowlist byte total')
 return a,p,selected,overlay
class GitHub:
 def __init__(self,journal):self.journal=journal;self.number=0
 def __call__(self,method,path,body=None):
  need(method=='GET' or (method=='POST' and path in ('git/trees','git/commits')),'Ref/other mutation route refused')
  self.number+=1;name=str(self.number).zfill(5)+'.API.json'
  argv=['gh','api','--method',method,'repos/AlecKriebel/Math/'+path]
  if body is not None:argv+=['--input','-']
  try:
   r=subprocess.run(argv,input=enc(body) if body is not None else None,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
  except Exception as error:
   put(self.journal,name,{'method':method,'path':path,'exception_type':type(error).__name__,'outcome_unknown':True});raise RuntimeError('API outcome unknown; inspect same attempt read-only') from None
  record={'method':method,'path':path,'request_pin':pin(enc(body)) if body is not None else None,'exit':r.returncode,'stdout_pin':pin(r.stdout),'stderr_pin':pin(r.stderr)}
  try:value=decode(r.stdout);record['returned_sha']=value.get('sha') if type(value) is dict and hexid(value.get('sha')) else None
  except Exception:
   put(self.journal,name,record);raise RuntimeError('API decode failed; captured only hashes, never retry mutation') from None
  put(self.journal,name,record);need(r.returncode==0 and type(value) is dict,'Native API failed; raw stderr never echoed');return value
def tree_hash(rows):
 rows=sorted(rows,key=lambda x:x[0].encode()+ (b'/' if x[1]=='040000' else b''))
 raw=b''.join((mode.lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(oid) for name,mode,kind,oid in rows)
 return native('tree',raw)
class NativeTrees:
 """Authenticate only needed immediate trees; equal foreign SHAs stay opaque."""
 def __init__(self,api):self.api=api;self.cache={};self.inspected=0
 def get(self,oid,depth):
  need(hexid(oid) and depth<=MAX_DEPTH,'Native tree identity/depth bound')
  if oid in self.cache:return self.cache[oid]
  j=self.api('GET','git/trees/'+oid);need(j.get('sha')==oid and j.get('truncated') is False and type(j.get('tree')) is list,'Complete immediate native tree required')
  need(len(j['tree'])<=MAX_ENTRIES-self.inspected,'Actually inspected native entry bound')
  rows=[];names=set()
  for e in j['tree']:
   name=e['path'];need(type(name) is str and name and '/' not in name and '\0' not in name and name not in ('.','..') and name not in names and hexid(e['sha']),'Native tree entry')
   name.encode('utf-8');names.add(name);mode=e['mode'];kind=e['type']
   need((mode,kind) in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')),'Native mode/type');rows.append((name,mode,kind,e['sha']))
  need(rows==sorted(rows,key=lambda x:x[0].encode()+(b'/' if x[1]=='040000' else b'')) and tree_hash(rows)==oid,'Immediate native tree order/SHA1 mismatch')
  self.inspected+=len(rows);self.cache[oid]={name:(mode,kind,sha1) for name,mode,kind,sha1 in rows};return self.cache[oid]
 def lookup(self,root,path):
  parts=rel(path).split('/');need(len(parts)-1<=MAX_DEPTH,'Lookup depth bound');oid=root
  for depth,name in enumerate(parts):
   entry=self.get(oid,depth).get(name)
   if entry is None:return None
   if depth==len(parts)-1:return entry
   if entry[0:2]!=('040000','tree'):return None
   oid=entry[2]
 def expected(self,root,overlay):
  trie={};missing=set();newdirs=set()
  for path,raw in overlay.items():
   parts=rel(path).split('/');need(len(parts)-1<=MAX_DEPTH,'Archive path depth bound');node=trie
   for name in parts[:-1]:
    need(name not in node or type(node[name]) is dict,'Overlay ancestor/file collision');node=node.setdefault(name,{})
   need(parts[-1] not in node,'Overlay path/ancestor collision');node[parts[-1]]=raw
  def rebuild(oid,node,prefix,depth):
   need(depth<=MAX_DEPTH,'Expected tree depth bound');entries=dict(self.get(oid,depth)) if oid is not None else {}
   for name,value in node.items():
    old=entries.get(name);path=prefix+name
    if type(value) is bytes:
     wanted=('100644','blob',native('blob',value));need(old is None or old==wanted,'Preexisting allowlist path mismatches')
     if old is None:missing.add(path)
     entries[name]=wanted
    else:
     need(old is None or old[0:2]==('040000','tree'),'Allowlist ancestor is a native leaf')
     if old is None:newdirs.add(path)
     entries[name]=('040000','tree',rebuild(old[2] if old else None,value,path+'/',depth+1))
   return tree_hash([(name,*entry) for name,entry in entries.items()])
  return rebuild(root,trie,'',0),missing,newdirs
 def changes(self,before,after):
  leaves=set();added=set();deleted=set()
  def compare(old,new,prefix,depth):
   need(depth<=MAX_DEPTH,'Changed subtree depth bound')
   if old==new:return
   left=self.get(old,depth) if old else {};right=self.get(new,depth) if new else {}
   for name in sorted(set(left)|set(right),key=lambda x:x.encode()):
    a=left.get(name);b=right.get(name)
    if a==b:continue
    path=prefix+name;at=a is not None and a[0:2]==('040000','tree');bt=b is not None and b[0:2]==('040000','tree')
    if at and bt:compare(a[2],b[2],path+'/',depth+1)
    else:
     if at:deleted.add(path);compare(a[2],None,path+'/',depth+1)
     if bt:added.add(path);compare(None,b[2],path+'/',depth+1)
     if (a is not None and not at) or (b is not None and not bt):leaves.add(path)
  compare(before,after,'',0);return leaves,added,deleted
def exact_scope(state):
 leaves,added,deleted=state['trees'].changes(state['parent_tree'],state['wanted'])
 need(leaves==state['missing'] and added==state['newdirs'] and not deleted,'Full changed-leaf/directory scope differs; no deletion/foreign change')
 return len(leaves)
def blob_matches(api,oid,raw):
 j=api('GET','git/blobs/'+oid);need(j.get('sha')==oid and j.get('encoding')=='base64' and type(j.get('size')) is int,'Native blob response')
 body=base64.b64decode(''.join(j['content'].split()),validate=True)
 need(j['size']==len(body)==len(raw) and native('blob',body)==oid and pin(body)==pin(raw),'Native blob body identity mismatch')
def parent_state(api,proof,selected,overlay):
 main=api('GET','git/ref/heads/main')['object']['sha'];need(hexid(main),'Fresh MAIN SHA')
 c=api('GET','git/commits/'+main);need(c.get('sha')==main and hexid(c['tree']['sha']),'Native parent commit identity')
 checkpoint=c if main==proof['checkpoint_commit'] else api('GET','git/commits/'+proof['checkpoint_commit'])
 need(checkpoint.get('sha')==proof['checkpoint_commit'] and checkpoint['tree']['sha']==proof['tree'],'Actual100 checkpoint/tree association differs')
 if main!=proof['checkpoint_commit']:
  compare=api('GET','compare/'+proof['checkpoint_commit']+'...'+main)
  need(compare.get('status')=='ahead' and compare['merge_base_commit']['sha']==proof['checkpoint_commit'],'Fresh MAIN must descend from actual100')
 root=c['tree']['sha'];trees=NativeTrees(api)
 for path,v in selected.items():need(trees.lookup(root,path)==('100644','blob',v['git_blob']),'Fresh parent changes selected mode/type/blob identity')
 wanted,missing,newdirs=trees.expected(root,overlay)
 for path,raw in overlay.items():
  old=trees.lookup(root,path)
  if old is not None:blob_matches(api,old[2],raw)
 need(api('GET','git/ref/heads/main')['object']['sha']==main,'Fresh MAIN lease lost')
 return dict(parent=main,parent_tree=root,trees=trees,wanted=wanted,missing=missing,newdirs=newdirs)
def inspect_candidate(api,state,candidate,overlay):
 need(hexid(candidate),'Candidate commit SHA');parent=state['parent'];wanted=state['wanted'];trees=state['trees']
 c=api('GET','git/commits/'+candidate);need(c.get('sha')==candidate and [x['sha'] for x in c['parents']]==[parent] and c['tree']['sha']==wanted,'Single-parent candidate/tree differs')
 changed=exact_scope(state)
 for path,raw in overlay.items():
  oid=native('blob',raw);need(trees.lookup(wanted,path)==('100644','blob',oid),'Candidate allowlist identity');blob_matches(api,oid,raw)
 need(api('GET','git/ref/heads/main')['object']['sha']==parent,'MAIN lease lost before verification success')
 return dict(parent=parent,candidate=candidate,tree=wanted,changed_leaves=changed,allowlisted_files=len(overlay),inspected_native_entries=trees.inspected,all_inspected_native_trees_and_allowlist_blobs_authenticated=True,unchanged_foreign_subtrees_preserved_by_native_SHA=True,full_scope_verified=True,MAIN_moved=False)
def verify(base,authorization_pin,api,parent,candidate):
 a,p,selected,overlay=conditions(base,authorization_pin);state=parent_state(api,p,selected,overlay)
 need(state['parent']==parent,'Candidate fresh parent lease differs');return inspect_candidate(api,state,candidate,overlay)
def prepare(base,authorization_pin,api,journal):
 a,p,selected,overlay=conditions(base,authorization_pin)
 need(journal==base/rel(a['journal_directory']) and journal.resolve()==journal and journal.is_dir() and not list(journal.glob('*INFLIGHT.json')),'Exact fresh authorized attempt journal required')
 for directory in (journal,journal.parent):
  fd=os.open(directory,os.O_RDONLY)
  try:os.fsync(fd)
  finally:os.close(fd)
 state=parent_state(api,p,selected,overlay);parent=state['parent'];wanted=state['wanted'];missing=state['missing']
 if not missing:return dict(status='NO_ADDITIONS_REQUIRED',parent=parent,allowlisted_files=INPUT_COUNT,MAIN_moved=False)
 put(journal,'TREE_INFLIGHT.json',dict(parent=parent,base_tree=state['parent_tree'],expected_tree=wanted,authorization_pin=authorization_pin,proposal_pin=PROPOSAL_PIN,changed_leaf_count=len(missing),semantics='Exclusive fsynced intent; no second tree attempt after uncertainty.'))
 conditions(base,authorization_pin);need(api('GET','git/ref/heads/main')['object']['sha']==parent,'MAIN lease lost before tree POST')
 j=api('POST','git/trees',dict(base_tree=state['parent_tree'],tree=[dict(path=path,mode='100644',type='blob',content=raw.decode('utf-8')) for path,raw in sorted(overlay.items())]));need(j.get('sha')==wanted,'Tree POST returned unexpected native tree')
 exact_scope(state);put(journal,'TREE_RESULT.json',dict(parent=parent,tree=wanted,changed_leaves=len(missing)))
 conditions(base,authorization_pin);need(api('GET','git/ref/heads/main')['object']['sha']==parent,'MAIN lease lost before commit intent')
 put(journal,'COMMIT_INFLIGHT.json',dict(parent=parent,tree=wanted,authorization_pin=authorization_pin,semantics='One single-parent commit object only; no ref update and no automatic retry.'))
 j=api('POST','git/commits',dict(message='Archive PR206 late operations repair evidence',tree=wanted,parents=[parent]));candidate=j.get('sha');need(hexid(candidate),'Commit response native identity')
 put(journal,'COMMIT_RESPONSE.json',dict(candidate=candidate,parent=parent,tree=wanted))
 result=verify(base,authorization_pin,api,parent,candidate);put(journal,'PREPARED_VERIFIED.json',result);return result
class SafeParser(argparse.ArgumentParser):
 def error(self,message):raise RuntimeError('Invalid archive helper arguments')
def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Live helper requires Python -E -S -B -P without -O')
 ap=SafeParser(description=__doc__);ap.add_argument('action',choices=('prepare','verify'));ap.add_argument('--authorization-bytes',type=int,required=True);ap.add_argument('--authorization-sha256',required=True);ap.add_argument('--journal',type=Path,required=True);ap.add_argument('--parent');ap.add_argument('--candidate');args=ap.parse_args()
 base=Path(__file__).resolve().parent.parent;journal=args.journal.absolute();need(journal.resolve()==journal and journal.is_relative_to(base) and not journal.exists(),'Fresh journal under case required')
 wanted={'bytes':args.authorization_bytes,'sha256':args.authorization_sha256};conditions(base,wanted)
 journal.mkdir(mode=0o700)
 for directory in (journal,journal.parent):
  fd=os.open(directory,os.O_RDONLY)
  try:os.fsync(fd)
  finally:os.close(fd)
 api=GitHub(journal)
 result=prepare(base,wanted,api,journal) if args.action=='prepare' else verify(base,wanted,api,args.parent,args.candidate)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 try:main()
 except BaseException as error:
  sys.stderr.write('PR206 archive helper refused: '+type(error).__name__+'\n');raise SystemExit(1) from None
