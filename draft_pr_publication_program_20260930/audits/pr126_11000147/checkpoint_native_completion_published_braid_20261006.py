"""Exact scoped native/main and completion checkpoints; requires a fresh full-plan peer grant."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent;R=Path('/Users/alec/Documents/Math')
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git';GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
ROOT_THREAD='01a0f08c-564b-7a51-bc3c-09cc9990d0fd';PEER_THREAD='01a0ff30-7e80-7053-abb4-4a9c45f2fd62'
K='11000147';HEAD='a1df84a64fa96d53f3a8c6fec9db8bc48bd1533c';events=[]
PRIVATE={'private_sources','private_renders','private_backend','private_primary_source_20261006','__pycache__'}
def now():return datetime.datetime.now(datetime.timezone.utc)
def require(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):
 require(p.is_file() and not p.is_symlink(),'Required regular authority '+str(p))
 return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def pin(p,absolute=False):
 require(p.is_file() and not p.is_symlink(),'Regular body '+str(p))
 b=p.read_bytes();return {'path':str(p) if absolute else str(p.relative_to(C)),'bytes':len(b),'sha256':sha(b),'mode':p.stat().st_mode&0o7777} if absolute else {'path':str(p.relative_to(C)),'bytes':len(b),'sha256':sha(b)}
def public(p):
 ignore_policy=p.name=='.gitignore' and p.read_bytes()==b'*\n!.gitignore\n'
 require(p.is_relative_to(C) and (not PRIVATE.intersection(p.parts) or ignore_policy) and p.suffix.lower() not in {'.pdf','.png','.jpg','.html','.sqlite','.sqlite3','.zip'},'Private source excluded')
 return pin(p)
def run(exe,args,cwd=C):
 t=now().isoformat();ch=subprocess.Popen([exe,*args],cwd=cwd,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 events.append({'actual_child_PID':ch.pid,'UTC_start':t,'UTC_end':now().isoformat(),'argv':[exe,*args],'cwd':str(cwd),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf8','replace')[:1800]})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'mode':mode,'events':events})
 require(ch.returncode==0,'Actual operation failed; inspect journal and actual outcome, do not blindly retry')
 return out
def git(*a,cwd=C):return run(GIT,list(a),cwd)
def api(*a):return run(GH,['api','--hostname','github.com',*a])
def primary():
 require(git('rev-parse','HEAD',cwd=R).decode().strip()==plan['primary_HEAD'],'Primary HEAD changed')
 result=[pin(Path(x['path']),True) for x in plan['protected_primary_pins']]
 require(result==plan['protected_primary_pins'],'Full primary index or one of eight held bodies changed')
 return result
def live_closed():
 x=json.loads(api('repos/AlecKriebel/Math/pulls/126'))
 require(x['html_url']=='https://github.com/AlecKriebel/Math/pull/126' and x['base']['ref']=='main' and x['state']=='closed' and x['head']['sha']==HEAD and not x['merged'] and x['merged_at'] is None and x['closed_at'],'Original-head closed-unmerged PR readback')
 comment=json.loads(api('repos/AlecKriebel/Math/issues/comments/'+str(closed['closing_comment_id'])))
 require(comment['body']==(A/'PROPOSED_CLOSING_COMMENT_20261006.md').read_text() and sha(comment['body'].encode())==closed['closing_comment_sha256'],'Full exact closing comment readback')
 return {'closed_at':x['closed_at'],'comment_url':comment['html_url'],'head_sha':x['head']['sha']}
def live_grant():
 require(now()>=datetime.datetime.fromisoformat(grant['granted_at_utc'].replace('Z','+00:00')) and now()<datetime.datetime.fromisoformat(grant['expires_at_utc'].replace('Z','+00:00')),'Fresh writer grant not effective or expired')
 primary()
def verify_members(members,root=C):
 for x in members:
  b=public(root/x['path']);require(b=={k:x[k] for k in ['path','bytes','sha256']},'Complete public member changed '+x['path'])
def remote_base(base):
 require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==base,'Main branch/local baseline')
 require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==base,'Remote main baseline')
 require(not git('diff','--cached','--name-only') and not git('diff','--name-only','--diff-filter=ACMRTUXB'),'Foreign staged/materialized non-deletion change')
def checkpoint(selected,base,message):
 live_grant()
 git('add','--',*sorted(selected))
 staged=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
 require(staged and staged<=set(selected) and not git('diff','--cached','--diff-filter=D','--name-only'),'Exact staged scope without deletions')
 for s in sorted(staged):
  b=git('show',':'+s);require(len(b)==selected[s]['bytes'] and sha(b)==selected[s]['sha256'],'Full staged body mismatch')
 require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==base,'Remote advanced before commit')
 live_grant();git('commit','-m',message)
 commit=git('rev-parse','HEAD').decode().strip();require(git('rev-parse','HEAD^').decode().strip()==base,'Exact single parent')
 changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).decode().split('\0'))-{''};require(changed==staged,'Exact changed paths')
 for s in sorted(staged):
  b=git('show',commit+':'+s);require(len(b)==selected[s]['bytes'] and sha(b)==selected[s]['sha256'],'Full committed body mismatch')
 live_grant();git('push','origin','HEAD:refs/heads/main')
 require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit,'Actual nonforce remote ref readback')
 git('fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main')
 require(git('rev-parse','origin/main').decode().strip()==commit,'Fetched remote main')
 for s in sorted(staged):
  b=git('show','origin/main:'+s);require(len(b)==selected[s]['bytes'] and sha(b)==selected[s]['sha256'],'Full fetched committed body mismatch')
 require(not git('diff','--cached','--name-only') and not git('diff','--name-only','--diff-filter=ACMRTUXB'),'Post-checkpoint index/non-deletion tracked changes')
 primary()
 return commit,[selected[s] for s in sorted(staged)]
require(len(sys.argv)==3 and sys.argv[1] in {'native','metadata','readback'},'Mode and base/grant path required')
mode=sys.argv[1];D=A/('actual_'+('native_published_braid_checkpoint' if mode=='native' else 'completion_metadata' if mode=='metadata' else 'final_completion_readback')+'_20261006')
require(not D.exists(),'Existing actual mode: inspect and recover receipts, do not repeat mutations')
plan_path=A/'PUBLISHED_BRAID_CHECKPOINT_PLAN_20261006.json';plan=load(plan_path)
require(plan['operator_sha256']==sha(Path(__file__).read_bytes()),'Exact reviewed operator')
closed=load(A/'actual_closure_20261006/RECEIPT.json');require(closed['same_head_closed_without_merge'] and closed['original_head']==HEAD,'Actual closed original authority')
prep=load(A/'native_published_braid_preparation_20261006/PREPARED_RECEIPT.json')
require(prep['base_commit']==plan['observed_main'] and sha((A/'native_published_braid_preparation_20261006/PREPARED_RECEIPT.json').read_bytes())==plan['prepared_receipt_sha256'],'Prepared native full binding')
if mode!='readback':
 grant_path=Path(sys.argv[2]);grant=load(grant_path)
 require(grant['source_thread_id']==PEER_THREAD and grant['owner_thread_id']==ROOT_THREAD and grant['scope']=='PR126_scoped_native_completion_main','Exact peer owner/mode authority')
 require(grant['concrete_plan_sha256']==sha(plan_path.read_bytes()) and grant['operator_sha256']==sha(Path(__file__).read_bytes()) and grant['base_main']==plan['observed_main'],'Full concrete grant binding')
 require(set(grant['allowed_existing_tracked_updates'])==set(plan['allowed_existing_tracked_updates']),'Exact granted tracked scope')
D.mkdir()
if mode!='readback':live_grant()
else:primary()
closed_live=live_closed()
if mode=='native':
 base=plan['observed_main'];remote_base(base)
 require(pin(C/'.git/index',True)==plan['isolated_full_index_preimage'],'Complete own physical index baseline')
 protocol_path=A/'ROOT_NATIVE_PUBLISHED_BRAID_PROTOCOL_READY_20261006.json';protocol=load(protocol_path)
 require(protocol['fresh_protocol_PASS'] and protocol['operator_sha256']==plan['operator_sha256'] and protocol['concrete_plan_sha256']==sha(plan_path.read_bytes()),'Fresh exact scoped native protocol clearance')
 for x in protocol['sealed_protocol_members']:
  p=A/x['path'];b=p.read_bytes();require(p.is_file() and not p.is_symlink() and len(b)==x['bytes'] and sha(b)==x['sha256'],'Complete native protocol seal')
 selected={x['path']:x for x in plan['owned_new_public_members']};verify_members(list(selected.values()))
 for x in plan['existing_program_preimages']:
  require(public(C/x['path'])==x,'Program preimage')
 for x in prep['proposed_native_pins']:
  p=Path(x['prepared_local_path']);require(pin(p)=={'path':str(p.relative_to(C)),'bytes':x['bytes'],'sha256':x['sha256']},'Prepared native postimage')
  dest=C/x['path'];require(not dest.is_symlink(),'Native destination redirected')
  old=[z for z in prep['source_inputs'] if z['path']==x['path']]
  if old:
   b=git('show',base+':'+x['path']);require(len(b)==old[0]['bytes'] and sha(b)==old[0]['sha256'] and (not dest.exists() or dest.read_bytes()==b),'Full native preimage')
  else:require(not dest.exists() and not git('ls-tree','-r','--name-only',base,'--',x['path']),'New native attempt collision')
  require(x['path'] in plan['allowed_existing_tracked_updates'] or x['path'] in plan['new_native_attempt_paths'],'Native scope')
 auth_path=A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json';auth=load(auth_path)
 require(sha(auth_path.read_bytes())==plan['original_authentication_sha256'],'Original authority changed')
 for x in auth['original_files']:
  original=auth_path.parent/'original_attempt'/x['path'];require(original.is_file() and not original.is_symlink(),'Regular original body');b=original.read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Original16 unchanged')
 live_grant()
 for x in prep['proposed_native_pins']:
  dest=C/x['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(Path(x['prepared_local_path']).read_bytes());selected[x['path']]=public(dest)
 progress=P/'CURRENT_PROGRESS.json';data=load(progress)
 require(data['current_PR']==124 and data['fully_completed_count']==21 and len(data['published_PRs'])==11,'Ascending program preimage')
 # Replace obsolete current-case fields instead of carrying source claims from PR124.
 data={k:v for k,v in data.items() if not k.startswith('current_')}
 stamp=now().isoformat();data.update({'UTC':stamp,'updated_UTC':stamp,'current_PR':126,'current_problem_id':11000147,'current_code':'AMR-109-0147','current_original_head':HEAD,'current_original_literal_status':'claimed_solved','current_original_budget':'1/5','current_new_central_proof_search_turns':0,'current_disposition':'already_solved_published_braid_content_named_answer_priority_unresolved','current_mathematical_clearance':True,'current_mathematical_audit_percent':100,'current_source_authentication_percent':100,'current_priority_audit_percent':100,'current_priority_audit_scope':'Bounded published mathematical-content disposition; express named-answer, first-application and exact-matrix priority unestablished','current_priority_clearance':False,'current_novelty_established':False,'current_old_published_whole_narrow_result_verified':True,'current_express_historical_named_answer_established':False,'current_actual_closed_at':closed_live['closed_at'],'current_actual_closing_comment_url':closed_live['comment_url'],'current_closed_without_merging':True,'current_native_status':'already_solved','current_native_status_mutated':True,'current_native_correction_checkpoint_pending':True,'current_core_disposition_complete':False,'current_PR_workflow_percent':95,'current_workflow_estimate_percent':95,'current_publication_ready':False,'current_DOI':None,'current_Zenodo_published':False,'current_tracker_updated':False,'current_mathematical_gate':'audits/pr126_11000147/MATHEMATICAL_SOURCE_GATE_20261006.json','current_priority_gate':'audits/pr126_11000147/ROOT_PUBLISHED_BRAID_DISPOSITION_READY_20261006.json','current_priority_review':'audits/pr126_11000147/ROOT_PUBLISHED_BRAID_DISPOSITION_20261006.md','current_original_independent_assert_guard_repaired_in_separate_diagnostic_copy':True,'current_remaining_required_steps':'Actual native/main commit, full fetched body readbacks, completion metadata and explicit release.','latest_ordered_intake_record':'ordered_intake_20261006/after_PR124/INTAKE_AFTER_PR124.json','skipped_since_last_completion':[{'PR':125,'literal_status':'already_solved','effort':'1/5','reviewed':False}],'remaining_current_step':'PR126 native/completion checkpoints and readbacks/release.','next_numeric_intake_cursor':127,'advance_to_next_PR_authorized_now':False,'next_step':'Finish PR126 operational readbacks/release, then fresh ascending status-only intake127.','main_writer_owner_at_snapshot':'This chat scoped PR126 native/completion window; release pending.','persistent_goal_status':'active','persistent_goal_complete':False,'last_completed_metadata_checkpoint_commit':'4c4e6450fd9aa479a54bb6d098f923b02cafa5f5','last_completed_final_completion_readback':'audits/pr124_10400231/actual_final_completion_readback_20261006/RECEIPT.json','last_completed_actual_writer_release':'audits/pr124_10400231/FINAL_COMPLETION_OWNER_RELEASE_20261006.json','last_completed_audit_checkpoint_push_pending':True})
 if 126 not in data['closed_without_publication_PRs']:data['closed_without_publication_PRs'].append(126)
 dump(progress,data)
 line='\n'+stamp+': PR126 mathematics/source100%, bounded published-content disposition100%: original closed-torus triple valid, whole narrow theorem already follows from BKL1998 band relations and Wajnryb source pair. Express earlier named answer, first application and exact-matrix priority remain unestablished. Same-head closed unmerged '+closed_live['comment_url']+'. Original1/5 preserved/imported, audit0; original16 immutable; optimized independent-assert weakness repaired only in separately bound diagnostic copies. Native/main workflow95% pending actual push/readbacks, completion metadata/release. Program21/99=21.21%,11published; goalactive. PR125 skipped by literal already_solved status only.\n'
 for f in [P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
  with f.open('a') as h:h.write(line)
 for p in [progress,P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:selected[str(p.relative_to(C))]=public(p)
 for rel in plan['future_native_checkpoint_members']:
  p=C/rel;require(p.exists(),'Required actual future protocol/grant body '+rel);selected[rel]=public(p)
 selection=A/'PUBLISHED_BRAID_CHECKPOINT_SELECTION_20261006.json';dump(selection,{'schema':'pr126-exact-native-checkpoint-selection/v1','UTC':now().isoformat(),'actual_operator_PID':os.getpid(),'base':base,'members':[selected[s] for s in sorted(selected)],'self_hash_omitted':True});selected[str(selection.relative_to(C))]=public(selection)
 commit,members=checkpoint(selected,base,'Close PR126 as qualified published braid consequence and preserve verified proof')
 record={'schema':'pr126-actual-native-published-braid-checkpoint/v1','UTC':now().isoformat(),'actual_operator_PID':os.getpid(),'base_commit':base,'commit':commit,'changed_members':members,'changed_count':len(members),'all_index_commit_fetched_full_bodies_verified':True,'actual_nonforce_push_passed':True,'native_correction_committed':True,'native_status':'already_solved','original_budget':'1/5','new_central_proof_search_turns':0,'same_head_closed_without_merge':True,'closing_comment_url':closed_live['comment_url'],'primary_full_index_and_eight_held_bodies_unchanged':True,'completion_metadata_pending':True,'writer_release_pending':True,'program_completed':21,'published':11,'persistent_goal_status':'active','late_receipt_not_in_own_commit':True}
 dump(D/'RECEIPT.json',record)
elif mode=='metadata':
 native=load(A/'actual_native_published_braid_checkpoint_20261006/RECEIPT.json');base=native['commit'];remote_base(base)
 require(native['native_correction_committed'],'Actual native checkpoint required')
 for x in native['changed_members']:
  b=git('show','origin/main:'+x['path']);require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Reverified entire native checkpoint')
 require(load(C/'unsolved_math_prioritization/state.json')[K]['status']=='already_solved' and load(C/'unsolved_math_prioritization/state.json')[K]['turns_used']==1,'Actual native target status/effort')
 live_grant();stamp=now().isoformat()
 core={'schema':'pr126-core-closure-completion/v1','UTC':stamp,'actual_operator_PID':os.getpid(),'PR':126,'original_head':HEAD,'same_head_closed_without_merge':True,'closing_comment_url':closed_live['comment_url'],'actual_full_comment_verified':True,'native_checkpoint_commit':base,'native_checkpoint_changed_count':len(native['changed_members']),'all_native_checkpoint_full_bodies_reverified':True,'status':'already_solved','scope':'Whole narrow torus triple follows from BKL1998 band relations and Wajnryb source pair; express named-answer/first-application/exact-matrix priority unestablished.','mathematical_clearance':True,'old_published_whole_narrow_result_verified':True,'substantive_novel_resolution_established':False,'original_budget':'1/5','new_central_proof_search_turns':0,'paper_Zenodo_DOI_tracker_merge_actions':False,'workflow_percent':100,'program_completed':22,'program_percent':22/99*100,'published':11,'persistent_goal_status':'active','completion_metadata_checkpoint_pending':True,'writer_release_pending':True}
 dump(A/'ROOT_CLOSURE_COMPLETION_20261006.json',core)
 path=P/'CURRENT_PROGRESS.json';d=load(path);require(d['current_PR']==126 and d['fully_completed_count']==21 and 126 not in d['fully_completed_eligible_PRs'],'Exact completion cursor');d['fully_completed_eligible_PRs'].append(126)
 d={k:v for k,v in d.items() if not k.startswith('last_completed_')}
 d.update({'UTC':stamp,'updated_UTC':stamp,'fully_completed_count':22,'fully_completed_fraction_percent':22/99*100,'workflow_estimate_percent':22/99*100,'workflow_estimate_definition':'Eleven published workflows, four legacy partial dispositions and seven priority/source-based closures divided by dated99-PR census; actual final operational release is separately receipted.','current_core_disposition_complete':True,'current_PR_workflow_percent':100,'current_workflow_estimate_percent':100,'current_native_correction_checkpoint_pending':False,'current_native_disposition_checkpoint_commit':base,'current_completion_metadata_checkpoint_pending':True,'current_remaining_required_steps':'Actual completion metadata push/full readbacks and explicit writer release.','last_completed_PR':126,'last_completed_DOI':None,'last_completed_PR_workflow_percent':100,'last_completed_outcome':'already_solved_scoped_published_braid_consequence','last_completed_record':'audits/pr126_11000147/ROOT_CLOSURE_COMPLETION_20261006.json','last_completed_actual_final_gate':'audits/pr126_11000147/ROOT_CLOSURE_COMPLETION_20261006.json','last_completed_PR_workflow_percent':100,'last_completed_final_completion_readback':'audits/pr126_11000147/actual_final_completion_readback_20261006/RECEIPT.json','last_completed_closing_comment_url':closed_live['comment_url'],'last_completed_native_correction_commit':base,'last_completed_metadata_checkpoint_commit':None,'last_completed_merge_commit':None,'last_completed_tracker_range':None,'last_completed_mathematical_result_valid':True,'last_completed_source_resolution_scope':core['scope'],'last_completed_priority_clearance':False,'last_completed_publication_authorization':False,'last_completed_audit_checkpoint_push_pending':True,'last_completed_late_release_audit_checkpoint_pending':True,'last_completed_actual_writer_release':None,'completion_metadata_checkpoint_pending_at_snapshot':True,'advance_to_next_PR_authorized_now':False,'next_step':'Verify PR126 completion metadata and explicitly release writer; then fresh status-only ascending intake127.','remaining_current_step':'PR126 completion metadata/readback/release.','persistent_goal_status':'active','persistent_goal_complete':False});dump(path,d)
 line='\n'+stamp+': PR126 core disposition complete: original-head closed unmerged and full comment reverified; native correction '+base+' all'+str(len(native['changed_members']))+' bodies reverified. Valid old mathematical-content consequence; historical explicit answer/first application/exact matrix priority unresolved. Original1/5, audit0; no paper/DOI/tracker/merge. Workflow100%, program22/99=22.22%,11published; actual metadata push, final readback and release pending at snapshot; goalactive.\n'
 for f in [P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
  with f.open('a') as h:h.write(line)
 paths=[path,P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'ROOT_CLOSURE_COMPLETION_20261006.json',A/'actual_native_published_braid_checkpoint_20261006/RECEIPT.json',A/'actual_native_published_braid_checkpoint_20261006/PROCESS_JOURNAL.json']
 selected={str(p.relative_to(C)):public(p) for p in paths}
 selection=A/'COMPLETION_METADATA_SELECTION_20261006.json';dump(selection,{'schema':'pr126-completion-metadata-selection/v1','UTC':now().isoformat(),'actual_operator_PID':os.getpid(),'base':base,'members':list(selected.values()),'self_hash_omitted':True});selected[str(selection.relative_to(C))]=public(selection)
 require(set(selected)<=set(plan['allowed_completion_metadata_paths']),'Completion metadata exact granted paths')
 commit,members=checkpoint(selected,base,'Record completed PR126 qualified published braid disposition')
 record={'schema':'pr126-actual-completion-metadata-checkpoint/v1','UTC':now().isoformat(),'actual_operator_PID':os.getpid(),'base':base,'commit':commit,'changed_members':members,'changed_count':len(members),'actual_nonforce_push_passed':True,'actual_full_changed_bodies_verified':True,'program_completed':22,'published':11,'persistent_goal_status':'active','final_readback_and_writer_release_pending':True};dump(D/'RECEIPT.json',record)
else:
 meta=load(A/'actual_completion_metadata_20261006/RECEIPT.json');native=load(A/'actual_native_published_braid_checkpoint_20261006/RECEIPT.json');base=sys.argv[2];require(base==meta['commit'],'Actual metadata base');remote_base(base)
 require(git('rev-parse','origin/main').decode().strip()==base,'Final fetched ref')
 pins={x['path']:x for x in native['changed_members']};pins.update({x['path']:x for x in meta['changed_members']})
 for path,x in pins.items():
  b=git('show','origin/main:'+path);require(len(b)==x['bytes'] and sha(b)==x['sha256'] and (C/path).read_bytes()==b,'Actual full latest remote/materialized body '+path)
 for x in prep['proposed_native_pins']:
  b=(C/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Final native postimage')
 st=load(C/'unsolved_math_prioritization/state.json')[K];require(st['status']=='already_solved' and st['turns_used']==1,'Final native state/effort')
 d=load(P/'CURRENT_PROGRESS.json');require(d['current_PR']==126 and d['fully_completed_count']==22 and 126 in d['fully_completed_eligible_PRs'] and len(d['published_PRs'])==11 and d['persistent_goal_status']=='active','Final program cursor')
 primary();record={'schema':'pr126-actual-final-completion-readback/v1','UTC':now().isoformat(),'actual_operator_PID':os.getpid(),'PR':126,'remote_main':base,'native_checkpoint_commit':native['commit'],'metadata_checkpoint_commit':base,'same_head_closed_without_merge':True,'actual_full_comment_body_verified':True,'all_latest_native_and_metadata_changed_bodies_verified':True,'latest_combined_body_count':len(pins),'native_target_status':'already_solved','original_budget':'1/5','new_central_proof_search_turns':0,'primary_full_index_and_eight_held_bodies_unchanged':True,'index_empty_and_materialized_non_deletion_tracked_changes_empty':True,'writer_release_pending':True,'goal_active':True,'program_completed':22,'program_percent':22/99*100,'published':11,'next_numeric_cursor':127,'paper_Zenodo_tracker_merge_actions':False,'closing_comment_url':closed_live['comment_url']};dump(D/'RECEIPT.json',record)
print(json.dumps({k:v for k,v in record.items() if k!='changed_members'},sort_keys=True))
