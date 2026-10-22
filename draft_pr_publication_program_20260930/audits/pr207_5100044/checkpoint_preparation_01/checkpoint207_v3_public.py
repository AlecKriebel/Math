"""PR207 findings45 audit checkpoint. Import has no service or filesystem mutation.
Root alone runs candidate creation, external expected-SHA CAS, and later local sync.
No ref update route exists here. dry is offline; plan/verify are GET-only.
"""
import argparse, base64, datetime, fcntl, hashlib, importlib.util, json, os, re, stat, subprocess, sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
PROGRAM=BASE.parents[2]
REPO=PROGRAM.parent
P='draft_pr_publication_program_20260930/'
CASE=P+'audits/pr207_5100044/'
PREFIX=CASE+'checkpoint_preparation_01/'
VIEWS=(CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md',P+'CURRENT_PROGRESS.json',P+'CURRENT_PROGRESS.md',P+'RESEARCH_LOG.md')
ANCHOR='1c4540b748e73711d720672791ccba9d5452a5eb'
CORE_PIN={'bytes':22049,'sha256':'8a61aee886e7a19bba6c7369944d778614b4099cbe1a060cf7e8acf2f52ec4d5'}
ASSESSMENT_PIN={'bytes':6452,'sha256':'752164d3a66b7d5843afaa46af699c4f681858dc046aa68c08d48dd4065dc05e'}
PRIORITY_PIN={'bytes': 5138, 'sha256': 'b80f892435459a81327a8d85291f3d24f6b36241e4b972c2b579eaf601dbfa38'}
PROOF_PIN={'bytes':2205,'sha256':'da1c7ee5b0eb0d1004956abd36f3ec13cc5f8d3d8ef23a5667cc453918d62e5a'}
ARCHIVE_PIN={'bytes':2270,'sha256':'cd395a1c9d92ae2ab05e93f918e8fc84356e1e7508b5c8129ff5124bfcb39245'}
LOCK_BYTES=b'PR publication program: stable Root cooperating global-five writer lock v1\nNever unlink or replace this inode; every existing-view writer must flock it.\n'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
def need(ok,message):
 if type(ok) is not bool or not ok:raise RuntimeError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def sealed(path,wanted=None):
 need(path.resolve()==path and stat.S_ISREG(path.lstat().st_mode) and stat.S_IMODE(path.stat().st_mode)==0o444,'Canonical readonly source required')
 raw=path.read_bytes()
 if wanted is not None:need(pin(raw)==wanted,'Pinned source changed')
 return raw
def core():
 path=BASE/'archive206_verified_reference.py';sealed(path,CORE_PIN)
 spec=importlib.util.spec_from_file_location('verified_native_trees_reference',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module

def inputs(wanted):
 c=core();raw=sealed(BASE/'CHECKPOINT_INPUTS_V3_PUBLIC.json',wanted);m=c.decode(raw)
 need(m.get('schema')=='pr207-findings45-checkpoint-inputs-v1' and m.get('assessment_pin')==ASSESSMENT_PIN and m.get('priority_assessment_pin')==PRIORITY_PIN,'Exact PR207 checkpoint manifest')
 rows=m['files'];need(type(rows) is list and 0<len(rows)<=199,'Bounded curated allowlist')
 overlay={}
 for row in rows:
  target=c.rel(row['path']);local=BASE/c.rel(row['payload']);need(local.is_relative_to(BASE),'Owned payload required')
  allowed=target.startswith(CASE) or target in VIEWS or target in (P+'audits/pr206_5100062/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json',P+'audits/pr206_5100062/ROOT_LATE_OPERATIONS_ARCHIVE_ACCEPTANCE_01.json')
  need(allowed and target not in overlay,'Exact audit/five-only target allowlist')
  body=sealed(local,{k:row[k] for k in ('bytes','sha256')});need(c.native('blob',body)==row['git_blob'] and b'\0' not in body and body.decode('utf-8').encode('utf-8')==body,'Inline selected body identity')
  overlay[target]=body
 need(m['total_files']==len(rows) and m['total_bytes']==sum(len(x) for x in overlay.values()),'Selected totals')
 need(overlay.get(PREFIX+'checkpoint207_v3_public.py')==sealed(Path(__file__)) and overlay.get(PREFIX+'archive206_verified_reference.py')==sealed(BASE/'archive206_verified_reference.py',CORE_PIN),'Exact helper and verified core are archived')
 assessment=c.decode(overlay[CASE+'ROOT_SCOPED_MATHEMATICAL_ASSESSMENT_01.json']);need(pin(overlay[CASE+'ROOT_SCOPED_MATHEMATICAL_ASSESSMENT_01.json'])==ASSESSMENT_PIN and assessment['accepted_scoped_mathematics'] is True and assessment['publication_ready'] is False and assessment['priority_audit_complete'] is False,'Pinned scoped mathematics only')
 priority_raw=overlay[CASE+'ROOT_PRIORITY_AND_EDITORIAL_ASSESSMENT_01.json'];priority=c.decode(priority_raw);need(pin(priority_raw)==PRIORITY_PIN and priority['bounded_priority_audit_complete'] is True and priority['case_workflow_estimate_percent']==45 and priority['publication_ready'] is False and priority['theorem_novelty_cleared'] is False and priority['proof_method_novelty_cleared'] is False,'Separate actual bounded priority/editorial gate')
 proof=c.decode(overlay[P+'audits/pr206_5100062/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json']);archive=c.decode(overlay[P+'audits/pr206_5100062/ROOT_LATE_OPERATIONS_ARCHIVE_ACCEPTANCE_01.json'])
 need(pin(overlay[P+'audits/pr206_5100062/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json'])==PROOF_PIN and proof['completed'] is True and proof['fully_completed_count']==49 and proof['published_count']==33,'Actual49/33 predecessor proof')
 need(pin(overlay[P+'audits/pr206_5100062/ROOT_LATE_OPERATIONS_ARCHIVE_ACCEPTANCE_01.json'])==ARCHIVE_PIN and archive['accepted'] is True and archive['full_scope_verified'] is True and archive['actual_MAIN_observed']==archive['candidate']==ANCHOR,'Actual accepted archive anchor')
 pre=m['preimages'];need(type(pre) is list and len(pre)==5 and {x['path'] for x in pre}==set(VIEWS),'Exact five local preimages')
 for row in pre:
  need(type(row['exists']) is bool,'Explicit preimage existence')
  if row['exists']:
   snap=overlay[row['snapshot_path']];need(pin(snap)=={k:row[k] for k in ('bytes','sha256')} and c.native('blob',snap)==row['git_blob'],'Exact historical preimage archive')
 status=c.decode(overlay[VIEWS[0]]);progress=c.decode(overlay[VIEWS[2]])
 for obj in (status,progress):
  for k,v in {'active_PR':207,'case_workflow_estimate_percent':45,'fully_completed_count':49,'published_count':33,'last_completed_PR':206,'next_numeric_intake_cursor':207,'advance_to_next_PR_authorized_now':False,'goal_complete':False,'publication_ready':False,'priority_audit_complete':True,'bounded_priority_audit_complete':True,'accepted_scoped_mathematics':True}.items():need(type(obj.get(k)) is type(v) and obj[k]==v,'Current facts mismatch: '+k)
  need(obj['positive_theorem']==assessment['positive_theorem'] and obj['alternative_reading_resolution']==assessment['alternative_reading_resolution'] and obj['preserved_QUEUE_status']=='claimed_solved' and obj['preserved_QUEUE_effort_cell']=='1/5','Explicit scoped theorem/boundary and submitted status')
 historical=c.decode(overlay[next(x['snapshot_path'] for x in pre if x['path']==VIEWS[2])])
 need(progress['dated_eligible_total']==99 and len(progress['published_PRs'])==len(set(progress['published_PRs']))==33 and progress['published_PRs']==historical['published_PRs'] and len(progress['fully_completed_eligible_PRs'])==49 and progress['fully_completed_eligible_PRs']==historical['fully_completed_eligible_PRs'],'Preserved33 published/49 completed lists and dated denominator')
 overlay[PREFIX+'CHECKPOINT_INPUTS_V3_PUBLIC.json']=raw
 return c,m,overlay

def local_state(path):
 if not path.exists():need(not path.is_symlink(),'Absent view is symlink');return None
 need(path.resolve()==path and stat.S_ISREG(path.lstat().st_mode),'Canonical regular current view');return pin(path.read_bytes())
def local_preimages(m,overlay,allow_post=False):
 for row in m['preimages']:
  old={k:row[k] for k in ('bytes','sha256')} if row['exists'] else None;now=local_state(REPO/row['path'])
  need(now==old or (allow_post and now==pin(overlay[row['path']])),'Exact local preimage mismatch: '+row['path'])

class API:
 def __init__(self,c,journal,mutate=False):self.c=c;self.journal=journal;self.mutate=mutate;self.number=0
 def __call__(self,method,path,body=None):
  get=path=='git/ref/heads/main' or re.fullmatch(r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',path) is not None or re.fullmatch(r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',path) is not None
  need((method=='GET' and get and body is None) or (method=='POST' and self.mutate and path in ('git/trees','git/commits') and type(body) is dict),'No ref or other mutation route')
  self.number+=1;name=str(self.number).zfill(5)+'.API.json';argv=[GH,'api','--method',method,'repos/AlecKriebel/Math/'+path]
  if body is not None:argv+=['--input','-']
  try:r=subprocess.run(argv,input=self.c.enc(body) if body is not None else None,capture_output=True,timeout=120)
  except BaseException as error:self.c.put(self.journal,name,{'method':method,'path':path,'outcome_unknown':True,'exception_type':type(error).__name__});raise RuntimeError('API outcome unknown; no automatic mutation retry') from None
  record={'method':method,'path':path,'request_pin':pin(self.c.enc(body)) if body is not None else None,'exit':r.returncode,'stdout_pin':pin(r.stdout),'stderr_pin':pin(r.stderr)}
  try:value=self.c.decode(r.stdout)
  except BaseException:self.c.put(self.journal,name,record);raise RuntimeError('API decode failure; inspect same attempt read-only') from None
  if type(value) is dict and self.c.hexid(value.get('sha')):record['returned_sha']=value['sha']
  self.c.put(self.journal,name,record);need(r.returncode==0 and type(value) is dict,'Native API failed; raw outputs suppressed');return value

def expected(c,trees,root,overlay,m):
 pre={x['path']:x for x in m['preimages']};trie={};changed=set();added_dirs=set()
 for path,raw in overlay.items():
  node=trie
  for part in c.rel(path).split('/')[:-1]:need(part not in node or type(node[part]) is dict,'Overlay ancestor collision');node=node.setdefault(part,{})
  leaf=path.rsplit('/',1)[-1];need(leaf not in node,'Overlay leaf collision');node[leaf]=raw
 def rebuild(oid,node,prefix,depth):
  need(depth<=c.MAX_DEPTH,'Overlay depth bound');entries=dict(trees.get(oid,depth)) if oid else {}
  for name,value in node.items():
   path=prefix+name;old=entries.get(name)
   if type(value) is bytes:
    wanted=('100644','blob',c.native('blob',value))
    if old!=wanted:
     allowed=old is None
     if path in pre and old is not None:
      row=pre[path];allowed=row['exists'] and old==('100644','blob',row['git_blob'])
     need(allowed,'Existing native tuple differs outside exact five preimages: '+path)
     # Program views must have the accepted local preimage, rather than disappear silently.
     if path in VIEWS[2:]:need(old is not None and pre[path]['exists'],'Existing program view required')
     changed.add(path)
    entries[name]=wanted
   else:
    need(old is None or old[:2]==('040000','tree'),'Native overlay ancestor is a leaf')
    if old is None:added_dirs.add(path)
    entries[name]=('040000','tree',rebuild(old[2] if old else None,value,path+'/',depth+1))
  return c.tree_hash([(name,*value) for name,value in entries.items()])
 return rebuild(root,trie,'',0),changed,added_dirs

def state(c,m,overlay,api,parent=None,require_lease=True):
 observed=api('GET','git/ref/heads/main')['object']['sha'];parent=parent or observed;need(c.hexid(parent),'Exact native parent')
 commit=api('GET','git/commits/'+parent);need(commit.get('sha')==parent and c.hexid(commit['tree']['sha']),'Parent commit/tree identity')
 if parent!=ANCHOR:
  comp=api('GET','compare/'+ANCHOR+'...'+parent);need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==ANCHOR,'Parent must descend accepted206 archive')
 trees=c.NativeTrees(api);wanted,changed,dirs=expected(c,trees,commit['tree']['sha'],overlay,m)
 if require_lease:need(observed==parent and api('GET','git/ref/heads/main')['object']['sha']==parent,'Fresh MAIN parent lease lost')
 return {'parent':parent,'parent_tree':commit['tree']['sha'],'wanted':wanted,'changed':changed,'dirs':dirs,'trees':trees}
def verify_candidate(c,m,overlay,api,s,candidate,require_lease=True):
 need(c.hexid(candidate),'Candidate SHA required');commit=api('GET','git/commits/'+candidate)
 need(commit.get('sha')==candidate and [x['sha'] for x in commit['parents']]==[s['parent']] and commit['tree']['sha']==s['wanted'],'Exact single-parent candidate/tree')
 # A new independent tree reader authenticates actual candidate data, not the construction cache.
 trees=c.NativeTrees(api);leaves,dirs,deleted=trees.changes(s['parent_tree'],s['wanted']);need(leaves==s['changed'] and dirs==s['dirs'] and not deleted,'Exact computed change allowlist/foreign tuple scope')
 selected={}
 for path,raw in overlay.items():
  oid=c.native('blob',raw);need(trees.lookup(s['wanted'],path)==('100644','blob',oid),'Selected candidate tuple');c.blob_matches(api,oid,raw);selected[path]={**pin(raw),'git_blob':oid}
 if require_lease:need(api('GET','git/ref/heads/main')['object']['sha']==s['parent'],'MAIN lease lost during candidate verification')
 return {'schema':'pr207-findings45-native-candidate-verification-v1','parent':s['parent'],'candidate':candidate,'tree':s['wanted'],'selected_files':selected,'changed_leaves':sorted(leaves),'new_directories':sorted(dirs),'all_selected_bodies_verified':True,'full_scope_verified':True,'foreign_tuples_and_QUEUE_preserved':True,'MAIN_moved_by_helper':False}
def candidate(c,m,overlay,api,journal,wanted):
 local_preimages(m,overlay);s=state(c,m,overlay,api);need(bool(s['changed']),'No empty candidate checkpoint')
 c.put(journal,'TREE_INFLIGHT.json',{'parent':s['parent'],'tree':s['wanted'],'manifest_pin':wanted,'semantics':'One tree attempt; uncertainty must be inspected read-only, never retried automatically.'})
 inputs(wanted);need(api('GET','git/ref/heads/main')['object']['sha']==s['parent'],'Lease lost before tree POST')
 result=api('POST','git/trees',{'base_tree':s['parent_tree'],'tree':[{'path':path,'mode':'100644','type':'blob','content':raw.decode('utf-8')} for path,raw in sorted(overlay.items())]});need(result.get('sha')==s['wanted'],'Tree result differs from exact computed root')
 c.put(journal,'TREE_RESULT.json',{'parent':s['parent'],'tree':s['wanted']})
 need(api('GET','git/ref/heads/main')['object']['sha']==s['parent'],'Lease lost before commit POST');c.put(journal,'COMMIT_INFLIGHT.json',{'parent':s['parent'],'tree':s['wanted'],'manifest_pin':wanted,'semantics':'One single-parent commit attempt; no ref action.'})
 result=api('POST','git/commits',{'message':'Checkpoint PR207 scoped mathematics and period boundary; bounded priority complete','tree':s['wanted'],'parents':[s['parent']]});oid=result.get('sha');need(c.hexid(oid),'Commit result SHA');c.put(journal,'COMMIT_RESULT.json',{'parent':s['parent'],'candidate':oid,'tree':s['wanted']})
 result=verify_candidate(c,m,overlay,api,s,oid);c.put(journal,'CANDIDATE_VERIFIED.json',result);return result

class WriterLock:
 def __init__(self):self.fd=None;self.pid=os.getpid()
 def check(self):
  need(self.fd is not None and os.getpid()==self.pid,'Current-process lock ownership');path=PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock';a=os.fstat(self.fd);b=path.lstat()
  need(path.resolve()==path and stat.S_ISREG(a.st_mode) and stat.S_ISREG(b.st_mode) and (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino)==self.identity and stat.S_IMODE(a.st_mode)==stat.S_IMODE(b.st_mode)==0o444 and os.pread(self.fd,len(LOCK_BYTES)+1,0)==LOCK_BYTES,'Stable lock inode/payload mismatch')
 def __enter__(self):
  path=PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock';need(path.resolve()==path,'Canonical program lock');self.fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK);a=os.fstat(self.fd);self.identity=(a.st_dev,a.st_ino)
  try:self.check();fcntl.flock(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB);self.check();return self
  except BaseException:os.close(self.fd);self.fd=None;raise
 def __exit__(self,kind,value,tb):
  try:self.check()
  finally:
   try:fcntl.flock(self.fd,fcntl.LOCK_UN)
   finally:os.close(self.fd);self.fd=None

def sync(c,m,overlay,api,journal,wanted,accept_path,accept_pin):
 raw=sealed(accept_path,accept_pin);a=c.decode(raw);need(a.get('schema')=='pr207-root-findings-checkpoint-acceptance-v1' and a.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and type(a.get('PR')) is int and a['PR']==207 and a.get('accepted') is True and a.get('full_scope_verified') is True,'Actual Root acceptance required')
 need(a.get('checkpoint_manifest_pin')==wanted and a.get('helper_pin')==pin(sealed(Path(__file__))) and a.get('assessment_pin')==ASSESSMENT_PIN and a.get('priority_assessment_pin')==PRIORITY_PIN,'Actual acceptance source/manifest/assessment/priority binding')
 for k,v in {'fully_completed_count':49,'published_count':33,'last_completed_PR':206,'next_numeric_intake_cursor':207,'case_workflow_estimate_percent':45,'advance_to_next_PR_authorized_now':False,'goal_complete':False}.items():need(type(a.get(k)) is type(v) and a[k]==v,'Actual acceptance facts')
 ref=a['Root_ref_update'];need(ref['expected_sha']==a['parent'] and ref['sha']==a['candidate'] and ref['force'] is False and ref['success_confirmed_by_actual_native_readback'] is True,'Actual Root expected-parent CAS readback')
 need(a['actual_MAIN_observed']==a['candidate'] and api('GET','git/ref/heads/main')['object']['sha']==a['candidate'],'Actual MAIN is accepted candidate')
 s=state(c,m,overlay,api,parent=a['parent'],require_lease=False);verified=verify_candidate(c,m,overlay,api,s,a['candidate'],require_lease=False);need(verified['tree']==a['tree'],'Accepted actual tree mismatch')
 pointer=BASE.parent/'ROOT_ACTUAL_FINDINGS_CHECKPOINT_01.json';need(not pointer.exists() and not pointer.is_symlink(),'Actual pointer already exists')
 with WriterLock() as lock:
  local_preimages(m,overlay,allow_post=True);c.put(journal,'LOCAL_FIVE_SYNC_INTENT.json',{'acceptance_pin':accept_pin,'candidate':a['candidate'],'semantics':'Cooperating-writer lock; per-file atomic installs, no five-file transaction or arbitrary same-UID CAS claim.'})
  for index,row in enumerate(m['preimages']):
   path=REPO/row['path'];body=overlay[row['path']];wanted_body=pin(body);lock.check()
   if local_state(path)!=wanted_body:
    old={k:row[k] for k in ('bytes','sha256')} if row['exists'] else None;need(local_state(path)==old,'Local preimage changed before install')
    temp=path.parent/('.pr207-'+journal.name+'-'+str(index)+'.tmp');need(path.parent.resolve()==path.parent,'Canonical view parent');fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    try:
     with os.fdopen(fd,'wb',closefd=False) as f:need(f.write(body)==len(body),'Short postimage write');f.flush();os.fchmod(fd,0o444);os.fsync(fd)
    finally:os.close(fd)
    lock.check();need(local_state(path)==old,'Local preimage changed before replace')
    if old is None:os.link(temp,path,follow_symlinks=False);temp.unlink()
    else:os.replace(temp,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
   need(local_state(path)==wanted_body,'Local installed postimage mismatch');c.put(journal,'LOCAL_VIEW_'+str(index)+'.json',{'path':row['path'],'postimage':wanted_body})
  lock.check();need(api('GET','git/ref/heads/main')['object']['sha']==a['candidate'],'MAIN changed before local actual receipt')
  need(all(local_state(REPO/path)==pin(overlay[path]) for path in VIEWS),'All five exact postimages required')
  receipt={'schema':'pr207-findings45-local-five-sync-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':a['candidate'],'tree':a['tree'],'acceptance_path':str(accept_path),'acceptance_pin':accept_pin,'manifest_pin':wanted,'all_five_local_files_match_actual_checkpoint':True,'files':[{ 'path':path,'postimage':pin(overlay[path])} for path in VIEWS]}
  c.put(journal,'LOCAL_GLOBAL_FIVE_SYNC.json',receipt);sync_pin=pin(c.enc(receipt));lock.check();c.put(BASE.parent,pointer.name,{'schema':'pr207-actual-findings-checkpoint-pointer-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'candidate':a['candidate'],'tree':a['tree'],'case_workflow_estimate_percent':45,'fully_completed_count':49,'published_count':33,'last_completed_PR':206,'next_numeric_intake_cursor':207,'advance_to_next_PR_authorized_now':False,'goal_complete':False,'acceptance_path':str(accept_path),'acceptance_pin':accept_pin,'sync_path':str(journal/'LOCAL_GLOBAL_FIVE_SYNC.json'),'sync_pin':sync_pin})
 return receipt

def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Ordinary Python -E -S -B -P required')
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=('dry','plan','candidate','verify','sync'));ap.add_argument('--manifest-bytes',type=int,required=True);ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--journal');ap.add_argument('--parent');ap.add_argument('--candidate');ap.add_argument('--acceptance',type=Path);ap.add_argument('--acceptance-bytes',type=int);ap.add_argument('--acceptance-sha256');args=ap.parse_args();wanted={'bytes':args.manifest_bytes,'sha256':args.manifest_sha256};c,m,overlay=inputs(wanted)
 if args.action=='dry':local_preimages(m,overlay);print(json.dumps({'status':'DRY_PREPARED_ONLY','selected_files':len(overlay),'selected_bytes':sum(map(len,overlay.values())),'five_views':list(VIEWS),'MAIN_moved':False},sort_keys=True));return
 need(args.journal is not None and Path(args.journal).name==args.journal,'Fresh owned journal basename required');journal=BASE/args.journal;need(not journal.exists() and not journal.is_symlink(),'No journal replay');journal.mkdir(mode=0o700)
 for directory in (journal,journal.parent):
  fd=os.open(directory,os.O_RDONLY)
  try:os.fsync(fd)
  finally:os.close(fd)
 api=API(c,journal,mutate=args.action=='candidate')
 if args.action=='plan':local_preimages(m,overlay);s=state(c,m,overlay,api);result={'status':'GET_ONLY_PLAN','parent':s['parent'],'parent_tree':s['parent_tree'],'expected_tree':s['wanted'],'changed_leaves':sorted(s['changed']),'new_directories':sorted(s['dirs']),'MAIN_moved':False};c.put(journal,'PLAN.json',result)
 elif args.action=='candidate':result=candidate(c,m,overlay,api,journal,wanted)
 elif args.action=='verify':s=state(c,m,overlay,api);need(s['parent']==args.parent,'Exact fresh candidate parent');result=verify_candidate(c,m,overlay,api,s,args.candidate);c.put(journal,'VERIFIED.json',result)
 else:need(args.acceptance is not None and args.acceptance_bytes is not None and args.acceptance_sha256 is not None,'Externally pinned actual acceptance required');result=sync(c,m,overlay,api,journal,wanted,args.acceptance.absolute(),{'bytes':args.acceptance_bytes,'sha256':args.acceptance_sha256})
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
