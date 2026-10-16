"""Independent read-only full-body transport verification; no actor execution.

Only this addendum folder receives output. Git calls read existing objects/refs
or query remote main; no fetch, merge, reset, add, commit or index write occurs.
"""
from pathlib import Path
import hashlib,json,os,datetime,subprocess
H=Path(__file__).resolve().parent; Q=H.parent; A=Q.parent; C=A.parents[2]
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
OLD='5de48499b84f168099d0273a340f4976f841f691'; NEW='b351c22a4a8fe70a45c670183b8bb1c17aabd1bf'
EXPECTED='0376234e1706e09f8c117a15d8e5fc02692ff824ffc8ec16793c7a8e64daa6c1'
events=[]; inputs={}; checks=[]; gitpins=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,label):
 if not v:raise RuntimeError(label)
 checks.append(label)
def read(p):
 require(p.is_file() and not p.is_symlink(),'Regular input '+str(p))
 b=p.read_bytes();inputs[str(p)]={'path':str(p),'bytes':len(b),'sha256':sha(b)};return b
def load(p):return json.loads(read(p))
def dump(name,x):(H/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def git(*args):
 start=now();p=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));out,err=p.communicate()
 events.append({'actual_PID':p.pid,'UTC_start':start,'UTC_end':now(),'argv':[GIT,*args],'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
 require(p.returncode==0,'Successful independent read-only Git process');return out
def body(commit,path):
 b=git('show',commit+':'+path);gitpins.append({'commit':commit,'path':path,'bytes':len(b),'sha256':sha(b)});return b
start=now()
receiptbody=read(A/'POST_PEER_MAIN_TRANSPORT_AUTHENTICATION_20261006.json');require(sha(receiptbody)==EXPECTED,'Exact supplied actual transport receipt')
t=json.loads(receiptbody);require(t['actual_operator_PID']==88610 and t['UTC']=='2026-10-06T21:21:45.454872+00:00','Actual recorded transport PID/UTC')
require(t['prepared_base']==t['current_local_main_before_fresh_writer_window']==OLD and t['actual_new_main']==NEW,'Exact historical and peer head binding')
prepbody=read(A/'native_published_obstruction_preparation_20261006/CORRECTED_PREPARED_RECEIPT_V2.json');require(sha(prepbody)==t['exact_V2_prepared_receipt_sha256']=='cbcc2d7ada7ccd6d08bec3a8871c42ed3bed7ed5bf5d379ce33663e2cfd747fe','Exact previously sealed V2 preparation')
prep=json.loads(prepbody);plan=load(A/'PUBLISHED_OBSTRUCTION_CHECKPOINT_PLAN_20261006.json')
head=git('rev-parse','HEAD');branch=git('branch','--show-current');index=git('diff','--cached','--raw','-z');dirty=git('diff','--name-only','--diff-filter=ACMRTUXB','-z')
require(head.strip().decode()==OLD and branch==b'main\n' and not index and not dirty,'Actual isolated main/index remains unmutated at historical baseline')
remote=git('ls-remote','origin','refs/heads/main');require(remote.decode().split()[0]==NEW and git('rev-parse','origin/main').strip().decode()==NEW,'Independent actual remote/fetched head matches receipt')
require(git('rev-list','--parents','-n','1',NEW).decode().split()==[NEW,OLD],'Independent exact sole-parent peer commit')
changed=[s for s in git('diff-tree','--no-commit-id','--name-only','-r','-z',OLD,NEW).decode().split('\0') if s]
require(changed==t['peer_changed_paths'] and len(changed)==34 and len(set(changed))==34 and all(s.startswith('draft_pr_descending_audit_20261002/') for s in changed),'Exact 34 distinct descending-only changed paths')
expected=prep['source_inputs']+plan['existing_program_preimages'];require(len(prep['source_inputs'])==12 and len(plan['existing_program_preimages'])==4 and len({x['path'] for x in expected})==16,'Exact 12 native and 4 ascending program source identities')
program=['draft_pr_publication_program_20260930/CURRENT_PROGRESS.json','draft_pr_publication_program_20260930/CURRENT_PROGRESS.md','draft_pr_publication_program_20260930/RESEARCH_LOG.md','draft_pr_publication_program_20260930/audits/pr124_10400231/RESEARCH_LOG.md']
require({x['path'] for x in plan['existing_program_preimages']}==set(program),'Four program preimages target exact expected program paths')
observed=[]
for x in expected:
 oldbody=body(OLD,x['path']);newbody=body(NEW,x['path']);require(newbody==oldbody and len(newbody)==x['bytes'] and sha(newbody)==x['sha256'],'Full unchanged old/new source body '+x['path'])
 observed.append({k:x[k] for k in ['path','bytes','sha256']})
 p=C/x['path']
 if p.exists():require(read(p)==oldbody,'Materialized unchanged source body '+x['path'])
require(observed==t['verified_preimages'],'Receipt full preimage ledger equals independent Git bodies')
require(len(prep['proposed_native_pins'])==15,'Exactly 15 sealed proposed postimages')
for x in prep['proposed_native_pins']:
 b=read(Path(x['prepared_local_path']));require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Unchanged V2 postimage full hash '+x['path'])
require(not (C/'unsolved_math_prioritization/attempts/10400231').exists(),'No native attempt exported before writer window')
physical=t['peer_changed_physical_preflight'];require(len(physical)==34 and [x['path'] for x in physical]==changed,'Physical ledger covers exact full peer changed-path list')
presence=[]; presentold=presentnew=absentold=absentnew=0
for x in physical:
 path=x['path'];p=C/path;newbody=body(NEW,path)
 entry=git('ls-tree','--long',NEW,'--',path).decode().strip();meta,name=entry.split('\t');mode,kind,blob,size=meta.split();require(mode=='100644' and kind=='blob' and name==path and int(size)==len(newbody),'New peer path exact regular Git blob '+path)
 tracked=bool(git('ls-tree','-r','--name-only',OLD,'--',path).strip());require(tracked==x['old_is_tracked'],'Old tracked status exact '+path)
 oldbody=body(OLD,path) if tracked else None
 require(len(newbody)==x['new_bytes'] and sha(newbody)==x['new_sha256'],'Peer full new body pin '+path)
 require((len(oldbody) if oldbody is not None else None)==x['old_bytes'] and (sha(oldbody) if oldbody is not None else None)==x['old_sha256'],'Peer full old body pin '+path)
 require(not p.is_symlink() and p.exists()!=x['observed_absent'],'Actual physical presence/no symlink matches receipt '+path)
 if p.exists():
  b=read(p);require(sha(b)==x['observed_sha256'] and b in [oldbody,newbody],'Actual physical file is exact observed old/new Git bytes '+path)
  if b==oldbody:presentold+=1
  else:presentnew+=1
  presence.append({'path':path,'present':True,'bytes':len(b),'sha256':sha(b),'matches_old':b==oldbody,'matches_new':b==newbody})
 else:
  require(x['observed_sha256'] is None,'Absent file records no synthetic physical hash '+path)
  if tracked:absentold+=1
  else:absentnew+=1
  presence.append({'path':path,'present':False,'old_tracked':tracked})
for e in t['events']:
 require(e['exit_code']==0,'Recorded parent read-only event success')
 require(e['argv'][1] in ['ls-remote','rev-parse','branch','diff','fetch','merge-base','rev-list','show','diff-tree','ls-tree'],'No parent main/index/native operation in transport journal')
 if e['argv'][1]=='show':
  commit,path=e['argv'][2].split(':',1);pin=next(x for x in gitpins if x['commit']==commit and x['path']==path)
  require(e['stdout_bytes']==pin['bytes'] and e['stdout_sha256']==pin['sha256'],'Recorded source stdout matches independently read full body')
require(len([e for e in t['events'] if e['argv'][1]=='fetch'])==1 and t['main_index_worktree_mutations'] is False and t['remote_tracking_fetch_only'] is True,'Transport parent has exactly one remote-cache fetch, no owned-main/index/worktree mutation')
current=load(H/'NORMAL_FF_STATIC_INPUT_HASHES.json')
for x in current['inputs']:
 b=read(Path(x['path']));require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Current exact statically reviewed actor unchanged '+x['path'])
manifest=load(Q/'PUBLIC_MANIFEST.json');priorseal=load(Q/'SEAL.json')
require(sha(read(Q/'PUBLIC_MANIFEST.json'))==priorseal['public_manifest_sha256'],'Prior public manifest seal binding')
for x in manifest['members']:
 b=read(Q/x['path']);require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Prior sealed public member unchanged '+x['path'])
for name,key in [('REPORT.md','REPORT_sha256'),('RESULT.json','RESULT_sha256'),('INPUT_HASHES.json','INPUT_HASHES_sha256')]:require(sha(read(Q/name))==priorseal[key],'Prior core seal unchanged '+name)
require(git('rev-parse','HEAD')==head and git('branch','--show-current')==branch and git('diff','--cached','--raw','-z')==index and git('diff','--name-only','--diff-filter=ACMRTUXB','-z')==dirty,'Independent read-only verification leaves main/index/worktree state unchanged')
dump('ACTUAL_INPUT_HASHES.json',{'schema':'pr124-post-peer-addendum-exact-inputs/v1','UTC':now(),'filesystem_inputs':list(inputs.values()),'full_Git_body_inputs':gitpins,'prior_seal_sha256':sha(read(Q/'SEAL.json')),'peer_release_observed':False,'fresh_writer_grant_observed':False})
dump('ACTUAL_VALIDATION.json',{'schema':'pr124-post-peer-addendum-actual-validation/v1','UTC_start':start,'UTC_end':now(),'actual_reviewer_operator_PID':os.getpid(),'transport_receipt_sha256':EXPECTED,'parent_authenticator_PID':88610,'parent_authenticator_UTC':t['UTC'],'actual_peer_commit':NEW,'exact_sole_parent':OLD,'checks_passed':len(checks),'checks':checks,'read_only_events':events,'full12_native_plus4_program_bodies_unchanged':True,'all15_V2_posts_unchanged':True,'physical_paths':presence,'physical_counts':{'present_exact_old':presentold,'present_exact_new':presentnew,'absent_old_tracked':absentold,'absent_new':absentnew},'prior24_sealed_members_unchanged':True,'own_operator_test_runs':0,'native_CLI_runs':0,'own_fetch_merge_reset_index_write_count':0,'new_central_proof_search_turns':0,'peer_release_observed':False,'fresh_writer_grant_observed':False,'operational_authorization':False})
print(json.dumps({'UTC':now(),'actual_reviewer_PID':os.getpid(),'checks_passed':len(checks),'peer_changed_paths':34,'physical_counts':{'present_exact_old':presentold,'present_exact_new':presentnew,'absent_old_tracked':absentold,'absent_new':absentnew},'own_mutations':'assigned_addendum_files_only'},sort_keys=True))
