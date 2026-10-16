#!/usr/bin/env python3
"""Authenticate actual completion; prepare a still-pending writer release record."""
from pathlib import Path
import importlib.util,os,sys
A=Path(__file__).resolve().parents[1];C=A.parents[2]
f=A/'native_post_assess_carryforward_v3_20261006/native_acceptance_actions_v4.py'
s=importlib.util.spec_from_file_location('reviewed_phase',f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
need=m.need
need(dict(os.environ)==m.START_ENV and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path,'Exact clean startup')
receipt=m.loads(m.read(A/'actual_final_checkpoint_v2_20261006/RECEIPT.json',2*1024*1024))
merge=m.loads(m.read(A/'actual_acceptance_actions_20261006/pr110_status_20261006/RECEIPT.json',65536))
need(receipt['remote_verified'] is True and receipt['parent']==merge['merge_commit'] and merge['native_acceptance_and_merge_complete'] is True and receipt['completed_PRs']==18 and receipt['persistent_goal_complete'] is False,'Actual complete metadata and merge receipts')
packet=m.loads(m.read(A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json',512*1024));rt=packet['runtime'];m.validate_runtime(rt)
capture=m.Capture(A/'root_final_readback_20261006');m.main_preflight(capture,rt,receipt['commit'])
pr=m.live_pr(capture,rt,state='MERGED');need(pr['mergeCommit']['oid']==merge['merge_commit'] and pr['mergedAt']==merge['mergedAt'],'Actual final GitHub merge OID/time')
need(m.git(capture,rt,'show','-s','--format=%P',receipt['commit']).decode().split()==[merge['merge_commit']],'Metadata single exact parent')
need(m.git(capture,rt,'show','-s','--format=%P',merge['merge_commit']).decode().split()==merge['exact_parents'],'Original head exact merge parents')
need(m.git(capture,rt,'rev-parse',merge['merge_commit']+'^{tree}').decode().strip()==merge['accepted_tree'],'Actual merge still exact accepted tree')
need(not m.git(capture,rt,'diff','--name-only','--diff-filter=ACMRTUXB','-z'),'No materialized tracked drift')
for row in receipt['pins']:
    need(m.pin(m.git(capture,rt,'show',receipt['commit']+':'+row['path']))=={k:row[k] for k in ('bytes','sha256')},'Full committed final metadata body')
    m.read(C/row['path'],spec=row,retain=False)
d=m.loads(m.read(A.parents[1]/'CURRENT_PROGRESS.json',128*1024));need(d['fully_completed_count']==18 and len(d['published_PRs'])==11 and d['last_completed_PR']==110 and d['current_PR_workflow_percent']==100 and d['persistent_goal_complete'] is False,'Exact completed program metadata')
pub=m.loads(m.read(A/'ROOT_ACTUAL_PUBLICATION_TRACKER_AUTHENTICATION_20261006.json'))
need(pub['DOI']==m.DOI and pub['range']==m.RANGE and pub['publication_fullbody_and_all33_logical_members'] is True and pub['actual_GWS_append_and_two_readbacks'] is True,'Actual publication/fullbody/tracker evidence')
final=A/'FINAL_COMPLETION_OWNER_RELEASE_20261006.json';need(not final.exists(),'Unique final release record')
result={'schema':'pr110-final-completion-writer-release/v1','UTC':m.now(),'actual_operator_PID':os.getpid(),'PR':110,'DOI':m.DOI,'tracker_range':m.RANGE,'merge_commit':merge['merge_commit'],'completion_metadata_commit':receipt['commit'],'GitHub_MERGED_confirmed':True,'remote_verified':True,'original_head':m.ORIGINAL,'original_effort':'2/5','new_central_proof_search_turns':0,'program_completed':18,'published':11,'dated_eligible_total':99,'program_estimate_percent':18/99*100,'workflow_percent':100,'unresolved_required_findings':[],'persistent_goal_status':'active','persistent_goal_complete':False,'primary_synchronization_pending':True,'human_question_pending':False,'writer_ownership_released':False,'next_numeric_cursor':111,'next_ordered_status_only_intake_authorized_now':False,'late_actual_release_receipts_join_next_scoped_checkpoint_without_self_commit_claim':True,'actual_final_readback_journal':str(capture.root/'PROCESS_JOURNAL.json'),'writer_release_pending':True}
m.save(final,result);print(m.json.dumps({'actual_operator_PID':os.getpid(),'actual_completed_main':receipt['commit'],'release_record':str(final),'next_cursor':111,'writer_release_pending':True}))
