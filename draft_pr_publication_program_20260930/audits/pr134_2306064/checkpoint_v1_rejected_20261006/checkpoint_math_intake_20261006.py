from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent;R=Path('/Users/alec/Documents/Math')
G='/opt/homebrew/Cellar/git/2.38.2/bin/git';GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
PEER='01a0ff30-7e80-7053-abb4-4a9c45f2fd62';OWNER='01a0f08c-564b-7a51-bc3c-09cc9990d0fd'
def ck(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(f,mode=False):
 ck(f.is_file() and not f.is_symlink(),'regular body '+str(f));b=f.read_bytes();v={'bytes':len(b),'sha256':sha(b)}
 if mode:v['mode']=f.stat().st_mode&0o7777
 return v
def read(f):return json.loads(f.read_bytes())
def now():return datetime.datetime.now(datetime.timezone.utc)
mode=sys.argv[1] if len(sys.argv)>1 else None
ck(mode=='checkpoint' and len(sys.argv)==3,'checkpoint and fresh peer grant only')
planfile=A/'MATH_INTAKE_CHECKPOINT_PLAN_20261006.json';plan=read(planfile)
ck(plan['operator_sha256']==sha(Path(__file__).read_bytes()),'reviewed operator')
grantfile=Path(sys.argv[2]);grant=read(grantfile)
ck(grant['source_thread_id']==PEER and grant['owner_thread_id']==OWNER and grant['scope']=='PR134_math_intake_main_archive_only','grant owner/scope')
ck(grant['concrete_plan_sha256']==sha(planfile.read_bytes()) and grant['operator_sha256']==plan['operator_sha256'] and grant['base_main']==plan['base_main'],'grant exact plan/operator/base')
ck(set(grant['allowed_existing_tracked_updates'])==set(plan['allowed_existing_tracked_updates']),'tracked grant scope')
ck(set(grant['allowed_new_public_paths'])==set(plan['new_public_paths']) and set(grant['allowed_future_protocol_paths'])==set(plan['future_protocol_paths']),'new/future grant scope')
D=A/'actual_math_intake_checkpoint_20261006';ck(not D.exists(),'already attempted; inspect actual journal, never blind retry');D.mkdir()
events=[]
def dump(f,v):f.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def run(exe,args,cwd=C):
 t=now().isoformat();ch=subprocess.Popen([exe,*args],cwd=cwd,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 events.append({'child_PID':ch.pid,'UTC_started':t,'UTC_finished':now().isoformat(),'argv':[exe,*args],'cwd':str(cwd),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf8','replace')[:1500]})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
 ck(ch.returncode==0,'operation failed; inspect actual outcome; no blind retry')
 return out
def git(*args,cwd=C):return run(G,list(args),cwd)
def primary():
 ck(git('rev-parse','HEAD',cwd=R).decode().strip()==plan['primary_HEAD'],'primary head')
 for x in plan['protected_primary_pins']:ck(pin(Path(x['path']),True)=={k:x[k] for k in ['bytes','sha256','mode']},'primary physical '+x['path'])
def guard():
 ck(now()>=datetime.datetime.fromisoformat(grant['granted_at_utc'].replace('Z','+00:00')) and now()<datetime.datetime.fromisoformat(grant['expires_at_utc'].replace('Z','+00:00')),'grant interval')
 primary()
def target():
 out=run(GH,['api','--hostname','github.com','repos/AlecKriebel/Math/pulls/134']);pr=json.loads(out)
 ck(pr['html_url']=='https://github.com/AlecKriebel/Math/pull/134' and pr['head']['sha']==plan['original_PR134_head'] and pr['state']=='open' and pr['draft'] and not pr['merged'],'same-head current draft')
 return pr['head']['sha']
guard()
ck(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==plan['base_main'],'local main baseline')
ck(git('ls-remote','origin','refs/heads/main').decode().split()[0]==plan['base_main'],'remote baseline')
ck(not git('diff','--cached','--name-only') and not git('diff','--name-only','--diff-filter=ACMRTUXB'),'foreign staged or materialized modifications')
ck(pin(C/'.git/index',True)==plan['own_full_index_preimage'],'own physical baseline')
target()
for x in plan['new_public_members']:
 ck(pin(C/x['path'])=={k:x[k] for k in ['bytes','sha256']},'frozen new body')
 ck(not git('ls-tree','-r','--name-only',plan['base_main'],'--',x['path']),'new body collision')
for x in plan['program_updates']:
 ck(pin(C/x['path'])==x['preimage'],'full program preimage')
 ck(pin(Path(x['prepared_path']))==x['postimage'],'prepared program postimage')
 ck(pin(Path(x['prepared_path']))==pin(Path(x['prepared_path'])),'postimage stable')
for x in plan['protected_originals']:
 ck(pin(A/'original_head_authentication_20261006/original_attempt'/x['path'])=={k:x[k] for k in ['bytes','sha256']},'original archival bytes')
gate=read(A/'MATHEMATICS_SOURCE_GATE_20261006.json');ck(gate['verdict']=='PASS_EXACT_MATHEMATICS_AND_SOURCE_AFTER_EXERCISED_METHOD_CONTROL_REPAIR' and gate['priority_gate'].startswith('now may begin') and not gate['service_mutations'],'science gate only')
proto=A/'math_intake_checkpoint_protocol_adversary_20261006'
result=read(proto/'RESULT.json');mf=read(proto/'FINAL_MANIFEST.json')
ck(result['verdict']=='PASS' and result['operator_sha256']==plan['operator_sha256'] and result['plan_sha256']==sha(planfile.read_bytes()) and not result['mandatory_corrections'],'fresh exact protocol clearance')
for x in mf['files']:ck(pin(proto/x['path'])=={k:x[k] for k in ['bytes','sha256']},'full protocol seal')
selected={x['path']:{k:x[k] for k in ['bytes','sha256']} for x in plan['new_public_members']}
for s in plan['future_protocol_paths']:
 f=C/s;ck(f.is_file() and not f.is_symlink(),'future authority body');selected[s]=pin(f)
ck(pin(A/'MAIN_ARCHIVE_GRANT_REQUEST_20261006.json')['sha256']==grant['root_request_sha256'],'exact root request')
guard()
for x in plan['program_updates']:
 dest=C/x['path'];dest.write_bytes(Path(x['prepared_path']).read_bytes());ck(pin(dest)==x['postimage'],'installed program exact body');selected[x['path']]=x['postimage']
git('add','--',*sorted(selected))
staged=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
ck(staged==set(selected),'exact staged scope')
ck(not git('diff','--cached','--diff-filter=D','--name-only'),'no deletions')
for s in sorted(staged):ck({'bytes':len(b:=git('show',':'+s)),'sha256':sha(b)}==selected[s],'full staged body')
guard();ck(git('ls-remote','origin','refs/heads/main').decode().split()[0]==plan['base_main'],'remote before commit')
git('commit','-m','Audit PR134 mathematics and preserve completed PR126 readbacks')
commit=git('rev-parse','HEAD').decode().strip();ck(git('rev-list','--parents','-n','1',commit).decode().split()==[commit,plan['base_main']],'exact single parent')
changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).decode().split('\0'))-{''};ck(changed==staged,'exact commit scope')
for s in sorted(staged):ck({'bytes':len(b:=git('show',commit+':'+s)),'sha256':sha(b)}==selected[s],'full committed body')
guard();git('push','origin','HEAD:refs/heads/main')
ck(git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit,'actual remote readback')
git('fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main')
ck(git('rev-parse','origin/main').decode().strip()==commit,'fetched main')
for s in sorted(staged):
 ck({'bytes':len(b:=git('show','origin/main:'+s)),'sha256':sha(b)}==selected[s] and pin(C/s)==selected[s],'full fetched/materialized body')
ck(not git('diff','--cached','--name-only') and not git('diff','--name-only','--diff-filter=ACMRTUXB'),'post-checkpoint index/nondeletion clean')
guard();target()
v={'schema':'pr134-actual-math-intake-main-checkpoint/v1','UTC':now().isoformat(),'actual_operator_PID':os.getpid(),'sole_parent':plan['base_main'],'commit':commit,'actual_nonforce_push_and_remote_fetched_readback':True,'full_selected_member_count':len(selected),'full_selected_members':[{'path':s,**selected[s]} for s in sorted(selected)],'all_fullbody_staged_committed_fetched_materialized_verified':True,'same_original_open_draft_PR134_verified':True,'all_nine_primary_physical_pins_and_primary_HEAD_unchanged':True,'own_final_full_index_pin':pin(C/'.git/index',True),'index_empty_and_non_deletion_tracked_changes_empty':True,'original1of5_unchanged':True,'new_central_proof_search_turns':0,'program_completed':22,'published':11,'math_source':100,'priority_in_progress_no_clearance':True,'paper_Zenodo_tracker_merge_close_comment_native_author_actions':False,'no_outstanding_child':True,'actual_writer_release_still_required':True,'plan_sha256':sha(planfile.read_bytes()),'grant':pin(grantfile)}
dump(D/'RECEIPT.json',v)
print(json.dumps({k:v[k] for k in ['UTC','actual_operator_PID','commit','sole_parent','full_selected_member_count','actual_nonforce_push_and_remote_fetched_readback','actual_writer_release_still_required']}))

