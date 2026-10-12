"""Record actual same-head closure and select only this effort's release artifacts."""
from pathlib import Path
import datetime, hashlib, json, os
A=Path(__file__).resolve().parent
P=A.parents[1]
C=P.parent
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
closure_path=A/'actual_closure_20261006/RECEIPT.json'
closure=json.loads(closure_path.read_text())
operation=json.loads((A/'actual_operations/close_pr97_novelty/execution.json').read_text())
ready=json.loads((A/'ROOT_NOVELTY_CLOSURE_READY_20261006.json').read_text())
require(operation['exit_code']==0 and operation['child_PID']==closure['operator_PID']
        and closure['same_head_closed_without_merge'] and closure['comment_body_readback_exact'], 'Actual closure not authenticated')
require(closure['PR_after']['state']=='CLOSED' and closure['PR_after']['mergedAt'] is None
        and closure['original_head']==ready['original_head'],'Closure scope changed')
require(sha(C/'unsolved_math_prioritization/QUEUE.md')==closure['global_queue_sha256'], 'Global queue changed')
package=A/'contingent_credited_note_v2'
require(sha(package/'CLOSED_MANIFEST.json')=='b66716a960c07d6064e0108f32dc9c41c1bb61757bbd1fdcb416bba7e42aa8d4'
        and sha(package/'publicfiles/pr97_note.pdf')=='09fa4443ff5a333b487c7e2c0e3c910f7ae53efdebd49d09343019d1322b2667',
        'Prepared frozen paper changed')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'schema':'pr97-completed-human-directed-novelty-closure/v1','UTC':now,'operator_PID':os.getpid(),
 'PR':97,'problem_id':10300055,'original_head':closure['original_head'],'original_literal_status':'claimed_solved',
 'outcome':'closed_without_merge_or_publication_classical_corollary_no_established_novel_contribution',
 'corrected_mathematics_valid':True,'novel_contribution_established':False,
 'ordinary_smooth_target_implied_by_prior_results':True,
 'supplement_historical_novelty':'UNESTABLISHED','full_original_historical_already_solved_authenticated':False,
 'global_queue_status_unchanged':True,'global_queue_sha256':closure['global_queue_sha256'],
 'native_attempts_imported':False,'merge_commit':None,'DOI':None,'tracker_range':None,
 'paper_preserved_unpublished':True,'closing_comment_url':closure['closing_comment_url'],
 'actual_closure_receipt_sha256':sha(closure_path),'actual_closure_operator_PID':closure['operator_PID'],
 'actual_operation_exit_code':operation['exit_code'],'original_author_effort':'2/5','extra_proof_search_turns':0,
 'PR97_disposition_question_resolved':True,'qualified_publication_permission_granted':False,
 'completed_workflow_percent':100,'program_completed':14,'dated_eligible_total':99,
 'program_completion_percent':14/99*100,'scoped_main_checkpoint_pending_at_record':True}
completion_path=A/'ROOT_CLOSURE_COMPLETION_20261006.json'
with completion_path.open('x') as stream:stream.write(json.dumps(result,indent=2)+'\n')
progress_path=P/'CURRENT_PROGRESS.json'
progress=json.loads(progress_path.read_text())
require(progress['current_PR']==97,'Program cursor changed')
completed=progress['fully_completed_eligible_PRs']
require(97 not in completed and len(completed)==13,'Completion already accounted or census changed')
completed.append(97);completed.sort()
for key in list(progress):
    if key.startswith('last_completed_'): del progress[key]
progress.update({'UTC':now,'updated_UTC':now,'current_PR_workflow_percent':100,'current_workflow_estimate_percent':100,
 'current_closed_without_merging':True,'current_closing_comment_url':closure['closing_comment_url'],
 'current_closure_outcome':result['outcome'],'current_actual_completion_record':str(completion_path.relative_to(P)),
 'current_publication_disposition_resolved':True,'current_human_disposition_question_pending':False,
 'current_publication_authorization':False,'current_qualified_publication_authorized':False,
 'current_publication_clearance':False,'current_package_ready_for_publication':False,'current_publication_ready':False,
 'current_user_authorized_qualified_publication':False,'current_qualified_note_ready_for_human_disposition':False,
 'current_DOI':None,'current_merge_commit':None,'current_tracker_range':None,
 'current_native_integration_started':False,'current_native_integration_complete':False,'current_native_acceptance':False,
 'current_user_novelty_based_closure_directive':ready['user_directive'],
 'current_global_historical_status_changed':False,'current_paper_disposition':'preserved_unpublished',
 'fully_completed_count':14,'fully_completed_fraction_percent':14/99*100,'workflow_estimate_percent':14/99*100,
 'closed_without_publication_PRs':sorted(set(progress.get('closed_without_publication_PRs',[])+[97])),
 'last_completed_PR':97,'last_completed_PR_workflow_percent':100,'last_completed_outcome':result['outcome'],
 'last_completed_record':str(completion_path.relative_to(P)),'last_completed_actual_final_gate':str(completion_path.relative_to(P)),
 'last_completed_DOI':None,'last_completed_merge_commit':None,'last_completed_publication_authorization':False,
 'last_completed_priority_clearance':False,'last_completed_full_source_solved':False,
 'last_completed_tracker_range':None,'last_completed_closing_comment_url':closure['closing_comment_url'],
 'last_completed_audit_checkpoint_push_pending':True,
 'completion_metadata_checkpoint_pending_at_snapshot':True,'advance_to_next_PR_authorized_now':True,
 'next_eligible_PR_after_current_completion':None,'next_eligible_order_requires_fresh_status_check':True,
 'next_numeric_intake_cursor':98,'persistent_goal_status_at_last_tool_read':'blocked',
 'current_previous_goal_blocker_resolved':True,
 'remaining_current_step':'Actual same-head closure verified; scoped release checkpoint pending.',
 'next_step':'After the closure release checkpoint, fresh ordered intake after97; only eligible literal claimed_solved heads. The scheduler was last read as blocked, and cannot be resumed by update_goal.',
 'workflow_estimate_definition':'Nine published workflows, three credited prior-result dispositions, one verified partial disposition and one novelty-based closure divided by dated99-PR census.'})
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### '+now+' — actual same-head novelty closure complete\n'
       'Actual closure child89935exit0 independently checked the original OPENdraft head, posted and read back the exact closing note, rechecked the same head, closedPR97 without deleting its branch, then verified CLOSED at fb50facb with no mergedAt. Comment https://github.com/AlecKriebel/Math/pull/97#issuecomment-6008296383. Native QUEUE body/hash and all counters unchanged; original author2/5 and extra search0. Human novelty directive resolves the previous choice gate; no publication authorization, DOI, tracker row or native attempt import. Corrected mathematics/technical supplement and prepared unpublished paper remain preserved. PR97 workflow100%;14/99=14.14% of dated eligible workflows completed. This release record truthfully precedes its own main checkpoint. Next: fresh ordered eligible intake after97 upon continuation; no scope change to other statuses.\n')
selected={progress_path,A/'RESEARCH_LOG.md',completion_path,Path(__file__).resolve(),
 A/'CLOSING_PRIORITY_NOTE_20261006.md',A/'ROOT_NOVELTY_CLOSURE_READY_20261006.json',
 A/'authenticate_novelty_closure_proposal.py',A/'close_pr97_novelty_disposition.py',
 A/'DISPOSITION_HANDOFF_SELECTION_20261006.json',
 A/'actual_checkpoints/disposition_handoff/RECEIPT.json',A/'actual_checkpoints/disposition_handoff/PROCESS_JOURNAL.json'}
for folder in ['actual_closure_20261006','novelty_disposition_adversary_20261006',
               'actual_operations/authenticate_novelty_closure','actual_operations/close_pr97_novelty',
               'actual_operations/prepare_disposition_handoff','actual_operations/checkpoint_disposition_handoff']:
    selected.update(p for p in (A/folder).rglob('*') if p.is_file() and not p.is_symlink())
rows=[]
for p in sorted(selected):
    require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(C.resolve()),'Unsafe scope')
    b=p.read_bytes();rows.append({'path':p.relative_to(C).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
selection={'schema':'pr97-closure-release-checkpoint-selection/v1','UTC':now,'operator_PID':os.getpid(),
 'expected_main':'bfbcc0d69197893fe3156cd7ed0d36acee45e25e','paths':[r['path'] for r in rows],'pins':rows,
 'only_selected_regular_release_artifacts':True,'global_queue_or_attempts_changed':False}
with (A/'CLOSURE_RELEASE_SELECTION_20261006.json').open('x') as stream:
    stream.write(json.dumps(selection,indent=2)+'\n')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'files':len(rows),'bytes':sum(r['bytes'] for r in rows),
                  'PR97_workflow_percent':100,'program_completion_percent':14/99*100,'closure_record':completion_path.name}))
