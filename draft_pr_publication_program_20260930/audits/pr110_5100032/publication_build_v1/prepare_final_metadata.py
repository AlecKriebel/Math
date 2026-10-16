#!/usr/bin/env python3
"""Prepare completion records only from genuine merged PR110 receipts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,sys
A=Path(__file__).resolve().parents[1];P=A.parents[1];C=A.parents[2]
def need(v,s):
    if not v:raise RuntimeError(s)
def can(v):return (json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ap(f):return {'path':str(f.relative_to(A)),**hp(f.read_bytes())}
def cp(f):return {'path':str(f.relative_to(C)),**hp(f.read_bytes())}
def read(f):return json.loads(f.read_bytes())
mergefile=Path(sys.argv[1]);need(mergefile.is_relative_to(A),'Actual local merge record')
merge=read(mergefile);need(merge['native_acceptance_and_merge_complete'] is True and merge['GitHub_MERGED_confirmed'] is True and merge['remote_push_complete'] is True and merge['tree_equality_verified'] is True and merge['accepted_tree']==merge['merge_tree'] and merge['exact_parents']==[merge['accepted_commit'],'3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35'],'Actual main exact-tree original-head merge')
timestamp=datetime.now(timezone.utc).isoformat()
native=A/'ROOT_NATIVE_MERGE_COMPLETION_20261006.json';need(not native.exists(),'Unique native completion')
native.write_bytes(can({'schema':'pr110-root-native-merge-completion/v1','UTC':timestamp,'actual_root_PID':os.getpid(),'PR':110,'problem_id':5100032,'original_status':'claimed_solved','original_budget':'2/5','DOI':'10.5281/zenodo.23191247','tracker_range':"'Math Puzzles'!A32:D32",'native_acceptance_and_merge_complete':True,'actual_merge_receipt_pin':ap(mergefile),'merge_commit':merge['merge_commit'],'accepted_commit':merge['accepted_commit'],'accepted_tree':merge['accepted_tree'],'merge_tree':merge['merge_tree'],'mergedAt':merge['mergedAt'],'full_mathematical_resolution':True,'bounded_priority_cleared':True,'absolute_first_priority_claimed':False,'all_required_mathematical_and_priority_findings':[],'actual_publication_and_tracker_complete':True,'whole_package_R1_R2_clean':True,'native_candidate_original17_prior_2_of_5_and_unrelated_records_preserved':True,'original_native_assess_calls':1,'new_central_proof_search_turns':0,'source_cache_mutated':False,'primary_checkout_mutated':False,'GitHub_release_created':False,'writer_release_pending':True,'final_metadata_checkpoint_pending':True,'completed_PRs':18,'dated_eligible_total':99,'workflow_estimate_percent':18/99*100,'persistent_goal_complete':False}))
d=read(P/'CURRENT_PROGRESS.json');need(d['current_PR']==110 and 110 not in d['fully_completed_eligible_PRs'] and d['fully_completed_count']==17,'Exact previous program state')
d['fully_completed_eligible_PRs'].append(110);d['published_PRs'].append(110)
d.update({'UTC':timestamp,'updated_UTC':timestamp,'fully_completed_count':18,'fully_completed_fraction_percent':18/99*100,'workflow_estimate_percent':18/99*100,'workflow_estimate_definition':'Eleven published completed workflows, three credited prior-result dispositions, one verified partial disposition and three novelty-based closures divided by the dated99-PR census.','current_PR_workflow_percent':100,'current_workflow_estimate_percent':100,'current_native_integration_complete':True,'current_native_candidate_adversarial_review_complete':True,'current_native_acceptance_and_merge_complete':True,'current_native_merge_commit':merge['merge_commit'],'current_native_acceptance_commit':merge['accepted_commit'],'current_native_merge_completion_record':'audits/pr110_5100032/'+native.name,'current_remaining_required_steps':'Final completion metadata readback and explicit writer release; then next numeric claimed_solved intake.','current_remaining_step':'Final completion metadata readback and explicit writer release.','remaining_current_step':'Final completion metadata readback and explicit writer release.','last_completed_PR':110,'last_completed_DOI':'10.5281/zenodo.23191247','last_completed_PR_workflow_percent':100,'last_completed_merge_commit':merge['merge_commit'],'last_completed_record':'audits/pr110_5100032/'+native.name,'last_completed_actual_final_gate':'audits/pr110_5100032/'+native.name,'last_completed_final_completion_readback':'audits/pr110_5100032/FINAL_COMPLETION_OWNER_RELEASE_20261006.json','last_completed_full_source_solved':True,'last_completed_outcome':'published_and_merged_substantive_new_literal_source_resolution','last_completed_priority_clearance':True,'last_completed_publication_authorization':True,'last_completed_closing_comment_url':None,'last_completed_tracker_range':"'Math Puzzles'!A32:D32",'last_completed_source_resolution_scope':'Every regular closed nonretracing elliptic billiard with strictly inner elliptic confocal caustic: focal antipedal ordinary norm sums agree, including all admitted periods, winding/star trajectories, repeats and reversal; bounded proof priority relative to inspected corpus.','last_completed_metadata_checkpoint_commit':None,'last_completed_audit_checkpoint_push_pending':True,'completion_metadata_checkpoint_pending_at_snapshot':True,'next_numeric_intake_cursor':111,'next_step':'Complete final metadata readback, explicitly release other writer with exact main, then live numeric status-only intake111.','advance_to_next_PR_authorized_now':False,'next_intake_requires_actual_completion_receipt_and_explicit_writer_release':True,'next_intake_requires_actual_isolated_metadata_checkpoint':True,'next_intake_requires_actual_isolated_final_readback':True,'primary_checkout_synchronization_pending':True,'persistent_goal_status':'active','persistent_goal_complete':False})
(P/'CURRENT_PROGRESS.json').write_bytes(can(d))
entry=f'\n{timestamp}: PR110 actually merged as {merge["merge_commit"]}, parents [{merge["accepted_commit"]},3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35], exact accepted tree {merge["accepted_tree"]}; GitHub MERGED/mergedAt authenticated. DOI10.5281/zenodo.23191247 and actual tracker A32:D32 complete. Math, bounded priority, clean R1/R2 and current PR workflow100%; program18/99=18.18%, goalactive/incomplete. Original17/nonemptyprior/2of5 and unrelated records preserved; no extra proof turn. Final metadata checkpoint/readback and writer release pending before intake111.\n'
for log in (A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md'):
    with log.open('a') as f:f.write(entry)
selected={P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',native}
selected|={A/'publication_build_v1'/n for n in ('record_native_action_v5.py','commission_native_action_v5.py','reconcile_acceptance_commit.py','scoped_final_checkpoint.py','prepare_final_metadata.py','authenticate_repair_and_commission_publish.py')}
for n in ('acceptance_commit','ready','merge','status'):
    g=A/'actual_action_commissions_20261006'/(n+'_ROOT_GATE.json')
    e=A/'actual_action_inputs_20261006'/(n+'_EXTRA.json')
    for f in (g,e):
        if f.is_file():selected.add(f)
selected|={f for f in (A/'actual_action_inputs_20261006').glob('RECONCILE_*_ROOT_GATE.json')}
selected|={f for f in (A/'actual_acceptance_reconciliation_20261006').glob('*/RECEIPT.json')}
selected|={f for f in (A/'actual_acceptance_reconciliation_20261006').glob('*/STOPPED_ACTION_FRESH_ABSENCE.json')}
selected|={f for f in (A/'actual_acceptance_reconciliation_20261006').glob('*/PROCESS_JOURNAL.json')}
selected|={f for f in (A/'actual_acceptance_reconciliation_20261006').glob('*/PROCESS_LAUNCHES.json')}
selected|={f for f in (A/'actual_acceptance_reconciliation_20261006').glob('*/START.json')}
selected|={A/'ROOT_ACTUAL_NATIVE_CANDIDATE_REVIEW_AUTHENTICATION_V2_20261006.json'}
for name in ('pr110_acceptance_commit_20261006','pr110_ready_20261006','pr110_merge_20261006','pr110_status_20261006'):
    folder=A/'actual_acceptance_actions_20261006'/name
    selected|={f for f in folder.glob('*.json') if f.name in ('START.json','FAILURE.json','PROCESS_JOURNAL.json','PROCESS_LAUNCHES.json','RECEIPT.json','LOCAL_RECEIPT.json','REMOTE_RECEIPT.json','GITHUB_STATUS_READBACK.json','PRE_MERGE_READBACK.json')}
for name in ('root_actual_pr110_acceptance_commit_20261006','root_actual_pr110_ready_20261006','root_actual_pr110_merge_20261006','root_actual_pr110_status_20261006'):
    folder=A/'actual_operations'/name;selected|={folder/n for n in ('execution.json','LAUNCH.json') if (folder/n).is_file()}
# Repair-review manifest members are supplied explicitly by the root at launch.
repair_manifest=Path(sys.argv[2]);need(repair_manifest.is_relative_to(A),'Actual completed independent repair manifest')
selected|={repair_manifest}|{repair_manifest.parent/x['path'] for x in read(repair_manifest)['files']}
need(all(f.is_file() and not f.is_symlink() for f in selected) and len(selected)<=128,'Bounded regular final evidence')
gatefile=A/'actual_action_inputs_20261006/FINAL_METADATA_ROOT_GATE.json';need(not gatefile.exists(),'Unique actual final metadata decision')
gatefile.write_bytes(can({'schema':'pr110-final-scoped-checkpoint/v1','role':'root','UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'actual_review':True,'clearance':True,'required_findings':[],'program_pin':hp((A/'publication_build_v1/scoped_final_checkpoint.py').read_bytes()),'actual_merge_receipt_pin':ap(mergefile),'expected_main':merge['merge_commit'],'commit_message':'Record PR110 publication, exact-tree merge, and completed audit','pins':[cp(f) for f in sorted(selected)]}))
print(json.dumps({'actual_root_PID':os.getpid(),'gate_pin':ap(gatefile),'selected_count':len(selected),'PR_workflow_percent':100,'program_completed_percent':18/99*100,'checkpoint_executed':False,'writer_released':False}))
