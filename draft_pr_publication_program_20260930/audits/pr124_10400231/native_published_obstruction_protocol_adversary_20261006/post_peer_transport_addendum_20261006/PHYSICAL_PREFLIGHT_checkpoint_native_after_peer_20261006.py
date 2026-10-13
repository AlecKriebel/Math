"""Scoped native/main checkpoint; execute only after the exact fresh concrete writer grant."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;P=A.parent.parent;C=P.parent;R=Path('/Users/alec/Documents/Math')
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
D=A/'actual_native_published_obstruction_checkpoint_20261006';events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def req(v,s):
 if not v:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run(args,cwd=C):
 start=now();ch=subprocess.Popen([GIT,*args],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 events.append({'PID':ch.pid,'UTC_start':start,'UTC_end':now(),'argv':[GIT,*args],'cwd':str(cwd),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'small_stdout':out.decode('utf8','replace') if len(out)<1200 else None,'stderr':err.decode('utf8','replace')})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
 req(ch.returncode==0,'Actual checkpoint action failed; inspect before retry')
 return out
def pin(p):
 req(p.is_relative_to(C) and p.is_file() and not p.is_symlink(),'Regular owned file')
 req(not {'private_sources','private_renders','private_backend','__pycache__'}.intersection(p.parts),'Private body excluded')
 req(p.suffix.lower() not in {'.pdf','.png','.html','.sqlite3','.zip'},'Private/binary source excluded')
 b=p.read_bytes();return {'path':str(p.relative_to(C)),'bytes':len(b),'sha256':sha(b)}
req(not D.exists(),'Existing actual checkpoint; inspect')
window=load(A/'PUBLISHED_OBSTRUCTION_WRITER_HANDOFF_20261006.json')
req(window['explicit_release_received'] and window['purpose']=='PR124 scoped published-obstruction native correction and completion','Exact fresh specific handoff')
gb=Path(window['grant_path']).read_bytes();req(sha(gb)==window['grant_sha256'],'Actual grant body changed');grant=json.loads(gb)
BASE=window['remote_main']
def live_window():req(grant['granted'] and datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(grant['expires_UTC']),'Writer window expired')
live_window()
req(grant['owner_thread_id']=='01a0f08c-564b-7a51-bc3c-09cc9990d0fd' and grant['remote_main_expected_before']==BASE,'Grant owner/base')
planpath=A/'PUBLISHED_OBSTRUCTION_CHECKPOINT_PLAN_AFTER_PEER_20261006.json';plan=load(planpath)
req(sha(planpath.read_bytes())==grant['concrete_plan']['sha256'],'Reviewed concrete plan changed')
req(plan['observed_main']==BASE,'Private native plan stale')
req(set(grant['allowed_existing_tracked_updates'])==set(plan['allowed_existing_tracked_updates']),'Granted tracked scope differs from concrete plan')
prepared=load(A/'native_published_obstruction_preparation_20261006/CORRECTED_PREPARED_RECEIPT_V2.json')
protocol=load(A/'ROOT_NATIVE_PUBLISHED_OBSTRUCTION_PROTOCOL_READY_20261006.json')
ready=load(A/'ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_READY_20261006.json');closed=load(A/'actual_closure_20261006/RECEIPT.json')
transport=load(A/'POST_PEER_MAIN_TRANSPORT_AUTHENTICATION_20261006.json')
req(protocol['fresh_protocol_PASS'] and prepared['base_commit']==transport['prepared_base'] and BASE==transport['actual_new_main'] and transport['all12_native_source_inputs_and4_program_preimages_unchanged'] and ready['fresh_disposition_review_PASS'],'Fresh source/protocol/unchanged transport gate')
req(plan['transport_authentication_sha256']==sha((A/'POST_PEER_MAIN_TRANSPORT_AUTHENTICATION_20261006.json').read_bytes()),'Exact actual transport evidence')
req(closed['same_head_closed_without_merge'] and closed['original_head']==ready['original_head'],'Actual original-head unmerged closure')
transport_protocol=load(A/'ROOT_POST_PEER_TRANSPORT_PROTOCOL_READY_20261006.json')
req(transport_protocol['PASS'] and transport_protocol['transport_authentication_sha256']==plan['transport_authentication_sha256'],'Fresh exact additive transport review')
for x in transport_protocol['sealed_members']:
 b=(A/x['path']).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Transport protocol seal changed')
D.mkdir()
req(run(['branch','--show-current']).strip()==b'main','Remain main')
req(run(['rev-parse','HEAD']).decode().strip()==transport['current_local_main_before_fresh_writer_window'],'Pre-fast-forward local main drift')
req(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==BASE,'Remote main drift')
req(not run(['diff','--cached','--name-only']) and not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Foreign staged/materialized change')
run(['merge-base','--is-ancestor',transport['current_local_main_before_fresh_writer_window'],BASE])
for x in transport['verified_preimages']:
 b=run(['show',BASE+':'+x['path']]);req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Transport preimage drift')
primaryhead=run(['rev-parse','HEAD'],R).decode().strip();primaryindex=run(['diff','--cached','--raw','-z'],R)
req(primaryhead==grant['ROOT_primary_local_HEAD_observed_tool'] and not primaryindex,'Primary grant invariant')
primarynames=run(['diff','--name-only','--diff-filter=ACMRTUXB','-z','--','draft_pr_descending_audit_20261002'],R).decode().split('\0')
primarypins={s:{'bytes':(R/s).stat().st_size,'sha256':sha((R/s).read_bytes())} for s in primarynames if s}
for x in grant['held_ROOT_descending_bodies']:
 b=Path(x['path']).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Held grant body changed')
req(transport['peer_changed_physical_paths_absent_or_equal_new_main'],'Changed physical path transport check')
for x in transport['peer_changed_physical_preflight']:
 dest=C/x['path'];req(not dest.is_symlink(),'Changed physical path symlink')
 if dest.exists():
  b=dest.read_bytes();req(dest.is_file() and len(b)==x['new_bytes'] and sha(b)==x['new_sha256'],'Changed physical path preflight drift')
live_window();run(['reset','--mixed',BASE])
req(run(['rev-parse','HEAD']).decode().strip()==BASE and not run(['diff','--cached','--name-only']) and not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Guarded main fast-forward/index preservation')
selected={}
for x in plan['owned_new_public_members']:
 req(pin(C/x['path'])==x,'Prepared public body changed '+x['path']);selected[x['path']]=x
req(len(selected)==plan['owned_new_public_member_count'],'Owned plan cardinality')
for x in plan['existing_program_preimages']:
 b=(C/x['path']).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Program preimage changed')
req(protocol['protocol_report_sha256']==sha((A/protocol['protocol_report']).read_bytes()),'Protocol report changed')
for x in protocol['sealed_protocol_members']:
 p=A/x['path'];b=p.read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Protocol seal changed')
for x in prepared['proposed_native_pins']:
 p=Path(x['prepared_local_path']);b=p.read_bytes()
 req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Prepared native postimage changed')
 before=[z for z in prepared['source_inputs'] if z['path']==x['path']]
 dest=C/x['path']
 req(not dest.is_symlink(),'Native destination symlink')
 if before:
  raw=run(['show',BASE+':'+x['path']]);req(len(raw)==before[0]['bytes'] and sha(raw)==before[0]['sha256'],'Native preimage stale')
  req(not dest.exists() or dest.read_bytes()==raw,'Unknown materialized native edit')
 else:
  req(not dest.exists() and not run(['ls-tree','-r','--name-only',BASE,'--',x['path']]),'New native attempt path collision')
req(all(x['path'] in plan['allowed_existing_tracked_updates'] or x['path'] in plan['new_native_attempt_paths'] for x in prepared['proposed_native_pins']),'Native export path outside plan')
live_window()
for x in prepared['proposed_native_pins']:
 dest=C/x['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(Path(x['prepared_local_path']).read_bytes())
 actual=pin(dest);req(actual=={k:x[k] for k in ['path','bytes','sha256']},'Native copied body mismatch');selected[x['path']]=actual
progress=P/'CURRENT_PROGRESS.json';data=load(progress)
req(data['current_PR']==124 and data['fully_completed_count']==20 and data['current_original_head']==ready['original_head'] and len(data['published_PRs'])==11,'Ascending progress scope')
stamp=now()
data.update({'UTC':stamp,'updated_UTC':stamp,'current_disposition':'already_solved_published_obstruction_direct_corollary_explicit_application_priority_unresolved','current_native_assessment_performed':True,'current_native_status':'already_solved','current_native_status_mutated':True,'current_native_correction_checkpoint_pending':True,'current_counterexample_valid':True,'current_mathematical_clearance':True,'current_mathematical_audit_percent':100,'current_priority_audit_percent':100,'current_priority_audit_scope':'Bounded published-content disposition; earliest/express application history unestablished','current_priority_clearance':False,'current_novelty_established':False,'current_old_published_full_family_and_general_obstruction_verified':True,'current_scoped_prior_content_disposition_supported':True,'current_blanket_already_solved_no_new_contribution_supported':False,'current_explicit_prior_conjecture_refutation_located':False,'current_application_priority_unresolved':True,'current_human_source_access_question_pending':False,'current_requested_source_no_longer_needed_for_disposition':True,'current_book_chapters_read':False,'current_book_required_core_primary_statements_read':True,'current_book_primary_pages_read':[20,22,23,26,27,28,45,46,114,118],'current_whole_book_read':False,'current_priority_gate':'audits/pr124_10400231/ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_READY_20261006.json','current_priority_review':'audits/pr124_10400231/ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_20261006.md','current_priority_root_authentication':'audits/pr124_10400231/ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json','current_actual_closed_at':closed['after']['closedAt'],'current_actual_closing_comment_url':closed['closing_comment_url'],'current_closed_without_merging':True,'current_original_budget':'2/5','current_new_central_proof_search_turns':0,'current_core_disposition_complete':False,'current_PR_workflow_percent':95,'current_workflow_estimate_percent':95,'current_this_goal_turn_classification':'progress','current_publication_preparation_percent':0,'current_publication_ready':False,'current_DOI':None,'current_Zenodo_published':False,'current_tracker_updated':False,'current_math_priority_checkpoint_actual_receipt_pending_at_snapshot':False,'current_math_priority_checkpoint_commit':'5de48499b84f168099d0273a340f4976f841f691','current_math_priority_checkpoint_actual_receipt':'audits/pr124_10400231/actual_math_priority_root_checkpoint_20261006/RECEIPT.json','current_remaining_required_steps':'Actual native correction commit/push/full-body readbacks, completion metadata/final readback and explicit writer release.','remaining_current_step':'PR124 scoped published-obstruction closure and native checkpoint finalization.','next_step':'Complete PR124 actual native/main readbacks and writer release, then status-only intake from125.','advance_to_next_PR_authorized_now':False,'main_writer_owner_at_snapshot':'This chat exclusive scoped PR124 native/completion checkpoint; release pending.','persistent_goal_status':'active','persistent_goal_complete':False})
if 124 not in data['closed_without_publication_PRs']:data['closed_without_publication_PRs'].append(124)
dump(progress,data)
line='\n'+stamp+': PR124 actual original-head closed unmerged '+closed['closing_comment_url']+'. Core primary book evidence and three fresh source/disposition reviews establish published II.3.3/3.4+II.5.2 already imply the full all-prime family/general bound. Mathematics valid100%; published-content disposition100%; express earlier named refutation/first application remains unestablished. already_solved explicitly scoped to old mathematical content. Original2/5 imported; newproof0; no paper/DOI/tracker. Private native correction independently protocol-verified; all other assessment/state/campaign rows preserved, catalog rank-only changes,48preexisting discrepancies preserved. Workflow95% pending actual native push/readback and metadata/release; program20/99=20.20%,11published; goalactive. Earlier source-access hold superseded by positive actual preview evidence, kept historical.\n'
for path in [P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with path.open('a') as h:h.write(line)
for path in [progress,P/'CURRENT_PROGRESS.md',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',planpath,A/'PUBLISHED_OBSTRUCTION_WRITER_HANDOFF_20261006.json',A/'PUBLISHED_OBSTRUCTION_WRITER_REQUEST_API_RESPONSE_20261006.json']:
 selected[str(path.relative_to(C))]=pin(path)
selection=A/'PUBLISHED_OBSTRUCTION_CHECKPOINT_SELECTION_20261006.json'
dump(selection,{'schema':'pr124-scoped-published-obstruction-checkpoint-selection/v1','UTC':now(),'actual_operator_PID':os.getpid(),'base':BASE,'members':[selected[s] for s in sorted(selected)],'source_images_PDFs_SQLite_private_excluded':True,'original_budget':'2/5','new_central_proof_turns':0,'self_hash_omitted':True})
selected[str(selection.relative_to(C))]=pin(selection)
run(['add','--',*sorted(selected)])
staged=set(run(['diff','--cached','--name-only','-z']).decode().split('\0'))-{''}
req(staged and staged<=set(selected),'Staged scope')
req(not run(['diff','--cached','--diff-filter=D','--name-only']),'No staged deletions')
for s in sorted(staged):
 b=run(['show',':'+s]);req(len(b)==selected[s]['bytes'] and sha(b)==selected[s]['sha256'],'Full index body mismatch')
live_window();run(['commit','-m','Close PR124 with attributed published obstruction and preserved valid proof'])
commit=run(['rev-parse','HEAD']).decode().strip();req(run(['rev-parse','HEAD^']).decode().strip()==BASE,'Sole parent mismatch')
changed=set(run(['diff-tree','--no-commit-id','--name-only','-r','-z',commit]).decode().split('\0'))-{''};req(changed==staged,'Committed path scope')
for s in sorted(staged):
 b=run(['show',commit+':'+s]);req(len(b)==selected[s]['bytes'] and sha(b)==selected[s]['sha256'],'Committed body mismatch')
live_window();run(['push','origin','HEAD:refs/heads/main'])
req(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==commit,'Remote push ref mismatch')
run(['fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main'])
req(run(['rev-parse','origin/main']).decode().strip()==commit,'Fetched main mismatch')
for s in sorted(staged):
 b=run(['show','origin/main:'+s]);req(len(b)==selected[s]['bytes'] and sha(b)==selected[s]['sha256'],'Fetched full body mismatch')
req(not run(['diff','--cached','--name-only']) and not run(['diff','--name-only','--diff-filter=ACMRTUXB']),'Post-checkpoint shared edit')
req(run(['diff','--cached','--raw','-z'],R)==primaryindex and run(['rev-parse','HEAD'],R).decode().strip()==primaryhead,'Primary HEAD/index changed')
for s,x in primarypins.items():
 b=(R/s).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Held materialized descending body changed')
for x in grant['held_ROOT_descending_bodies']:
 b=Path(x['path']).read_bytes();req(len(b)==x['bytes'] and sha(b)==x['sha256'],'Granted held body changed')
receipt={'schema':'pr124-actual-native-published-obstruction-checkpoint/v2','UTC':now(),'actual_operator_PID':os.getpid(),'base_commit':BASE,'prepared_original_base':transport['prepared_base'],'actual_unchanged_source_transport_verified':True,'commit':commit,'selected_count':len(selected),'changed_count':len(staged),'changed_members':[selected[s] for s in sorted(staged)],'actual_nonforce_push_passed':True,'all_changed_full_bodies_verified_in_index_commit_fetched_main':True,'native_correction_committed':True,'native_status':'already_solved','native_classification_scoped_to_old_mathematical_content':True,'same_head_closed_without_merge':True,'closing_comment_url':closed['closing_comment_url'],'original_budget':'2/5','new_central_proof_search_turns':0,'program_completed':20,'published':11,'completion_metadata_pending':True,'writer_release_pending':True,'primary_HEAD_unchanged':primaryhead,'primary_index_and_held_descending_bodies_unchanged':True,'late_receipt_not_in_its_own_commit':True,'persistent_goal_status':'active'}
dump(D/'RECEIPT.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='changed_members'},sort_keys=True))

