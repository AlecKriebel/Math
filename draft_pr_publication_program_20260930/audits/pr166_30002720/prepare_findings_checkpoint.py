"""Create only the explicitly selected PR166 findings objects; never mutate local Git."""
from pathlib import Path
import datetime,hashlib,json,importlib.util,sys
A=Path(__file__).resolve().parent;C=A.parents[2];P=C/'draft_pr_publication_program_20260930'
s=importlib.util.spec_from_file_location('safe_primitives',P/'audits/pr156_30005432/prepare_scoped_merge.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
api,require,save,lookup,changed_leaves,body_at=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at
ORIGINAL='efc3f35a72543ad9ae76fd31a860116f1ffd4a32'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return dict(local_path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest())
def create_objects(expected,overlay,message,receipt):
 require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced before object preparation')
 parent=api('git/commits/'+expected)
 pins={n:pin(p) for n,p in sorted(overlay.items())}
 tree=api('git/trees','POST',dict(base_tree=parent['tree']['sha'],tree=[dict(path=n,mode='100644',type='blob',content=p.read_text()) for n,p in sorted(overlay.items())]))
 changed={n for n,v in pins.items() if lookup(parent['tree']['sha'],n)!=('100644','blob',v['git_blob'])}
 require(changed_leaves(parent['tree']['sha'],tree['sha'])==changed,'Unexpected full semantic tree diff')
 for n,v in pins.items():require(lookup(tree['sha'],n)==('100644','blob',v['git_blob']),'Selected tree identity differs '+n)
 commit=api('git/commits','POST',dict(message=message,tree=tree['sha'],parents=[expected]))
 actual=api('git/commits/'+commit['sha']);require(actual['tree']['sha']==tree['sha'] and [x['sha'] for x in actual['parents']]==[expected],'Actual commit tree or sole parent differs')
 require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced; do not apply stale object')
 rec=dict(UTC=stamp(),status='BOUNDED_OBJECTS_PREPARED_MAIN_NOT_UPDATED',expected_main=expected,parent_tree=parent['tree']['sha'],tree=tree['sha'],commit=commit['sha'],selected_files=pins,actual_changed_paths=sorted(changed),foreign_base_tree_paths_preserved=True,no_local_Git_mutations=True,no_author_branch_change=True,no_new_publication=True)
 save(A/receipt,rec);print(json.dumps({k:rec[k] for k in ['status','expected_main','tree','commit']}));print('Selected files',len(pins));return rec
def prepare(expected):
 plan=json.loads((A/'FINDINGS_SCOPE_PLAN.json').read_text());grant=json.loads((A/'MAIN_WRITER_RETURN.json').read_text())
 require(grant['explicit_return_received'] and grant['PR']==166 and grant['returned_MAIN']==expected,'Fresh explicit bounded return required')
 require(grant['scope_plan_sha256']==pin(A/'FINDINGS_SCOPE_PLAN.json')['sha256'],'Writer scope plan differs')
 require(api('git/ref/heads/main')['object']['sha']==expected,'Fresh MAIN differs')
 pr=api('pulls/166');require(pr['state']=='closed' and not pr['merged'] and pr['head']['sha']==ORIGINAL,'Actual original closed-unmerged PR required')
 closure=json.loads((A/'PR_CLOSURE_ACCEPTANCE.json').read_text());require(closure['status']=='ACTUAL_PR166_CLOSED_UNMERGED_EXACT_COMMENT_TITLE_BODY_ACCEPTED','Actual closure acceptance missing')
 science=json.loads((A/'ROOT_FINAL_SCIENTIFIC_DISPOSITION.json').read_text())
 require(science['original_theorem_mathematically_valid'] and science['original_target_prior_negative_answer'] and science['new_Baire_theorem_valid'],'Final scientific verdict absent')
 require(not science['publication_clearance'] and not science['precise_nonboundary_refinement_preempted_by_located_prior_theorem'],'Scientific scope differs')
 out=A/'findings_checkpoint';require(not out.exists(),'Preparation exists; inspect unknown outcome before retry');out.mkdir();now=stamp()
 qpath=plan['QUEUE_path'];old=body_at(qpath,expected).decode();ls=old.splitlines(keepends=True);idx=[i for i,x in enumerate(ls) if '| 30002720 /' in x]
 require(len(idx)==1,'Unique target QUEUE row required');i=idx[0];oldrow=ls[i];cells=oldrow.rstrip('\n').split('|');require(len(cells)==14,'QUEUE schema changed')
 cells[8]=' already_solved ';cells[9]=' 1/5 '
 cells[11]=' Original unrestricted fixed-marginal negative answer already explicit in LNS arXiv:1605.02352v2 Proposition2.9. Explicit nonboundary square-rank all-deterministic-center theorem mathematically verified and not falsely classified as prior known; novelty/current global openness of refinement unestablished. Three math and three priority families, plus fresh verified dense-G_delta audit consequence retained. PR166 closed unmerged as novel-original-resolution submission; no paper/DOI/tracker. Audit: draft_pr_publication_program_20260930/audits/pr166_30002720; '+closure['comment_url']+'. '
 cells[12]=' — ';ls[i]='|'.join(cells)+'\n';new=''.join(ls)
 require(len(old.splitlines())==len(new.splitlines()) and sum(x!=y for x,y in zip(old.splitlines(),new.splitlines()))==1,'Other QUEUE rows changed');(out/'QUEUE.accepted.md').write_text(new)
 names=['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md'];before={n:body_at('draft_pr_publication_program_20260930/'+n,expected) for n in names}
 j=json.loads(before[names[0]]);require(j['fully_completed_count']==32 and len(j['fully_completed_eligible_PRs'])==32 and 166 not in j['fully_completed_eligible_PRs'],'Actual completion census differs')
 require(j['published_count']==18 and len(j['published_PRs'])==18,'Actual publication census differs')
 j.setdefault('historical_completed_case_records',[]).append(dict(PR=164,fields={k:v for k,v in j.items() if k.startswith('last_completed_')},actual_receipt='audits/pr164_30002879/FINAL_CHECKPOINT_ACCEPTANCE.json'))
 j.setdefault('historical_preparation_snapshots',[]).append(dict(UTC=now,PR=166,fields={k:v for k,v in j.items() if k.startswith('current_')},note='Actual preceding PR164 completion facts retained; no foreign scientific paths modified.'))
 for k in list(j):
  if k.startswith(('current_','last_completed_')):del j[k]
 j['fully_completed_eligible_PRs'].append(166)
 if 166 not in j['closed_without_publication_PRs']:j['closed_without_publication_PRs'].append(166)
 j.pop('persistent_goal_status',None)
 j.update(dict(UTC=now,updated_UTC=now,fully_completed_count=33,fully_completed_fraction_percent=round(3300/99,2),workflow_estimate_percent=round(3300/99,2),published_count=18,last_completed_PR=166,last_completed_PR_workflow_percent=100,last_completed_original_head=ORIGINAL,last_completed_original_QUEUE_status='claimed_solved',last_completed_original_budget='1/5',last_completed_mathematical_result_valid=True,last_completed_priority_clearance=False,last_completed_outcome='already_solved_original_target_closed_unmerged_valid_refinement_retained',last_completed_DOI=None,last_completed_merge_commit=None,last_completed_tracker_range=None,last_completed_record='audits/pr166_30002720/WORKFLOW_COMPLETION.json',
 current_PR=166,current_problem_id=30002720,current_original_head=ORIGINAL,current_original_QUEUE_status='claimed_solved',current_original_budget='1/5',current_status='ACTUALLY_CLOSED_ORIGINAL_TARGET_PRIOR_KNOWN_FINDINGS_ACCEPTANCE_PENDING_AT_SNAPSHOT',current_PR_workflow_percent=100,current_workflow_estimate_percent=100,current_mathematical_review_percent=100,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_priority_decision_percent=100,current_priority_clearance=False,current_priority_status='Prior original universal negative at boundaries. Exact verified continuity refinement and new residual deduction retained; their historical novelty unestablished.',current_Zenodo_published=False,current_tracker_updated=False,current_original_PR_merged=False,current_closed=True,current_publication_ready=False,current_publication_disposition_pending=False,current_publication_package_reviews_required=False,current_remaining_required_steps='Actual expected-old MAIN findings acceptance and factual checkpoint readbacks.',current_record='audits/pr166_30002720/CURRENT_CASE_STATUS.json',current_mathematical_gate='audits/pr166_30002720/ROOT_MATH_GATE.json',current_priority_gate='audits/pr166_30002720/ROOT_PRIORITY_GATE.json',current_category_gate='audits/pr166_30002720/ROOT_CATEGORY_GATE.json',
 next_numeric_intake_cursor=167,next_eligible_PR_after_current_completion=None,next_eligible_order_requires_fresh_status_check=True,next_step='After actual PR166 completion and writer return, status-only original-head intake fromPR167; skip every originally nonclaimed status untouched.',remaining_current_step='Actual PR166 findings and factual completion acceptance.',advance_to_next_PR_authorized_now=False,goal_work_continuing=True,persistent_goal_complete=False,actual_goal_runtime_status_last_read='blocked; objective file read; continuing directly authorized work',workflow_estimate_definition='33/dated99=33.33% only upon actual accepted PR166 disposition/findings;18 published.',
 program_snapshot_authority_condition='audits/pr166_30002720/FINDINGS_CHECKPOINT_ACCEPTANCE.json must confirm actual MAIN commit/tree/sole parent and selected bytes.',program_snapshot_semantics='Counts apply upon actual accepted findings snapshot, not preparation.',completion_metadata_checkpoint_pending_at_snapshot=True,active_checkpoint_commit=None,active_checkpoint_acceptance_receipt='audits/pr166_30002720/FINDINGS_CHECKPOINT_ACCEPTANCE.json',active_checkpoint_actual_readback_required=True))
 j['skipped_since_last_completion']=[165];j['latest_ordered_intake_record']='status_intakes_after_pr164/INTAKE_SUMMARY.json'
 save(out/'CURRENT_PROGRESS.json',j)
 note='\n\n'+now+' — PR166: science100%, actual original PR closed unmerged; original unrestricted target prior known at boundaries, exact valid continuity refinement and separately verified residual theorem retained with novelty unestablished. No paper/DOI/tracker. Upon actual MAIN acceptance completed33/dated99=33.33%,18published. Originalalready_solvedPR165 status-only skipped untouched. Factual completion readback and explicit writer return precede PR167 intake. Goal unfinished.\n'
 for n in names[1:]:(out/n).write_bytes(before[n]+note.encode())
 status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());status.update(UTC=now,status='ACTUALLY_CLOSED_ORIGINAL_TARGET_PRIOR_KNOWN_FINDINGS_PREPARED_NOT_ACCEPTED',case_percent=85,native_PR_closure_pending=False,actual_PR_closed_unmerged=True,bounded_remote_MAIN_writer_authority=True,MAIN_writer_authority=False,MAIN_findings_pending=True);save(A/'CURRENT_CASE_STATUS.json',status)
 save(A/'WORKFLOW_COMPLETION.json',dict(UTC=now,PR=166,problem_id=30002720,original_head=ORIGINAL,original_QUEUE_status='claimed_solved',original_budget='1/5',status='SCIENCE_AND_ACTUAL_CLOSURE_COMPLETE_FINDINGS_ACCEPTANCE_PENDING',case_workflow_percent=85,mathematics_valid=True,original_target_already_solved=True,precise_refinement_not_asserted_known=True,new_category_theorem_valid=True,novelty_established=False,disposition='already_solved original target; closed unmerged',closed_at=pr['closed_at'],closure_comment_url=closure['comment_url'],new_paper=False,new_Zenodo_record=False,new_tracker_row=False,fully_completed_count_before_acceptance=32,fully_completed_count_after_acceptance=33,published_count=18,dated_eligible_total=99,goal_complete=False,next_numeric_intake_cursor=167))
 with (A/'RESEARCH_LOG.md').open('a') as h:h.write(note)
 overlay={qpath:out/'QUEUE.accepted.md',**{'draft_pr_publication_program_20260930/'+n:out/n for n in names}}
 for rel in plan['public_audit_relative_paths']:
  p=A/rel;require(p.is_file(),'Missing selected case artifact '+rel);overlay[p.relative_to(C).as_posix()]=p
 for rel in plan['prior_completion_relative_paths']+plan['ordered_intake_public_relative_paths']:
  p=P/rel;require(p.is_file(),'Missing selected prior/intake artifact '+rel);overlay[p.relative_to(C).as_posix()]=p
 require(len(overlay)==162,'Concrete writer file count differs')
 create_objects(expected,overlay,'Record PR166 original target as already solved; preserve verified continuity refinement and new category consequence\n\nPrior boundary theorem answers original universal marginal target. Explicit square-rank theorem and new dense-G_delta audit deduction mathematically verified; historical novelty unestablished. Actual PR166 closed unmerged. One QUEUE row and explicitly owned audit/programme/status evidence only. No new preprint/DOI/tracker; no native author branch or local Git change.','FINDINGS_CHECKPOINT_PREPARATION.json')
if __name__=='__main__':
 require(len(sys.argv)==2,'Pass freshly returned actual MAIN SHA');prepare(sys.argv[1])

