"""Build immutable concrete scoped main plan from private native postimages and owned public archive."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent;R=Path('/Users/alec/Documents/Math')
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git';env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
def require(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def git(*args):return subprocess.check_output([GIT,*args],cwd=C,env=env)
def pin(p,absolute=False):
 require(p.is_file() and not p.is_symlink(),'Regular body')
 b=p.read_bytes();d={'path':str(p) if absolute else str(p.relative_to(C)),'bytes':len(b),'sha256':sha(b)}
 if absolute:d['mode']=p.stat().st_mode&0o7777
 return d
def public(p):
 ignore_policy=p.name=='.gitignore' and p.read_bytes()==b'*\n!.gitignore\n'
 require((not {'private_sources','private_renders','private_backend','private_primary_source_20261006','__pycache__'}.intersection(p.parts) or ignore_policy) and p.suffix.lower() not in {'.pdf','.png','.jpg','.html','.sqlite','.sqlite3','.zip'},'Private source binary excluded')
 return pin(p)
q=A/'PUBLISHED_BRAID_CHECKPOINT_PLAN_20261006.json';require(not q.exists(),'Freeze a concrete plan once')
prep=load(A/'native_published_braid_preparation_20261006/PREPARED_RECEIPT.json');base=prep['base_commit']
require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==base and git('ls-remote','origin','refs/heads/main').decode().split()[0]==base,'Local/remote immutable baseline')
require(not git('diff','--cached','--name-only') and not git('diff','--name-only','--diff-filter=ACMRTUXB'),'Shared index/tracked baseline')
original=load(A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json');closed=load(A/'actual_closure_20261006/RECEIPT.json');require(closed['same_head_closed_without_merge'] and closed['original_head']==original['original_head'],'Actual closed original')
paths=[P/'CURRENT_PROGRESS.json',P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md'];old=[]
for p in paths:
 b=git('show',base+':'+str(p.relative_to(C)));require(b==p.read_bytes(),'Exact tracked program preimage');old.append(public(p))
owned=[str(A.relative_to(C)),str((A.parent/'pr124_10400231').relative_to(C)),str((P/'ordered_intake_20261006/after_PR124').relative_to(C))]
names=git('ls-files','--others','--exclude-standard','-z','--',*owned).decode().split('\0');members=[public(C/n) for n in names if n]
pre=[x['path'] for x in prep['proposed_native_pins'] if any(y['path']==x['path'] for y in prep['source_inputs'])];new=[x['path'] for x in prep['proposed_native_pins'] if x['path'] not in pre];require(len(pre)==9 and len(new)==6,'Exact nine existing plus six new native bodies')
primary=load(A.parent/'pr124_10400231/ACTUAL_PRIMARY_GRANT_INVARIANTS_FINAL_20261006.json')['verified'];require([pin(Path(x['path']),True) for x in primary]==primary,'Full primary index/eight held preimages')
primaryhead=subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=R,env=env).decode().strip();require(primaryhead=='6144d964777214c6963a915288c18fcf97b42026','Primary HEAD')
future=[A/'ROOT_NATIVE_PUBLISHED_BRAID_PROTOCOL_READY_20261006.json',A/'native_protocol_adversary_20261006/AUDIT.md',A/'native_protocol_adversary_20261006/RESULT.json',A/'native_protocol_adversary_20261006/FINAL_MANIFEST.json',A/'MAIN_WRITER_REQUEST_API_RESPONSE_20261006.json',A/'MAIN_WRITER_HANDOFF_20261006.json',q]
metadata=[*paths,A/'RESEARCH_LOG.md',A/'ROOT_CLOSURE_COMPLETION_20261006.json',A/'actual_native_published_braid_checkpoint_20261006/RECEIPT.json',A/'actual_native_published_braid_checkpoint_20261006/PROCESS_JOURNAL.json',A/'COMPLETION_METADATA_SELECTION_20261006.json']
record={'schema':'pr126-concrete-native-and-completion-main-plan/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_readonly_plan_PID':os.getpid(),'PR':126,'observed_main':base,'original_head':original['original_head'],'primary_HEAD':primaryhead,'protected_primary_pins':primary,'isolated_full_index_preimage':pin(C/'.git/index',True),'operator':str(A/'checkpoint_native_completion_published_braid_20261006.py'),'operator_sha256':sha((A/'checkpoint_native_completion_published_braid_20261006.py').read_bytes()),'prepared_receipt_sha256':sha((A/'native_published_braid_preparation_20261006/PREPARED_RECEIPT.json').read_bytes()),'original_authentication_sha256':sha((A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json').read_bytes()),'owned_new_public_members':sorted(members,key=lambda x:x['path']),'owned_new_public_member_count':len(members),'allowed_existing_tracked_updates':[str(p.relative_to(C)) for p in paths]+pre,'existing_program_preimages':old,'new_native_attempt_paths':new,'native_postimages':prep['proposed_native_pins'],'future_native_checkpoint_members':[str(p.relative_to(C)) for p in future],'allowed_completion_metadata_paths':[str(p.relative_to(C)) for p in metadata],'max_main_commits':2,'max_nonforce_main_pushes':2,'max_native_exports':15,'new_PR_service_comment_close_merge_actions':False,'author_branch_writes':False,'branch_deletion':False,'paper_Zenodo_DOI_tracker_actions':False,'status':'already_solved','scope':'Old published band-generator content plus source Anosov pair imply the entire original narrow theorem; express named answer/first-application/exact-matrix priority remain unestablished.','original_budget':'1/5','new_central_proof_search_turns':0,'program_count_before':21,'program_count_after_native_verified':22,'published_unchanged':11,'private_source_bytes_excluded':True,'fresh_protocol_review_pending':True,'fresh_peer_writer_grant_required':True,'actual_main_index_native_writes':False,'persistent_goal_status':'active'}
q.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');print(json.dumps({'path':str(q),'sha256':sha(q.read_bytes()),'public_members':len(members),'existing_tracked_paths':len(record['allowed_existing_tracked_updates']),'new_native_paths':6,'not_executed':True}))
