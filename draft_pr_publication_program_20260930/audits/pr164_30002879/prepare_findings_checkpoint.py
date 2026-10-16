"""Publish the PR164 audit only; never merge its author branch or touch local Git."""
from pathlib import Path
import datetime,hashlib,json,importlib.util,sys
A=Path(__file__).resolve().parent
C=A.parents[2];P=C/'draft_pr_publication_program_20260930'
s=importlib.util.spec_from_file_location('base_scope',P/'audits/pr156_30005432/prepare_scoped_merge.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
api,require,save,lookup,changed_leaves,body_at=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at
ORIGINAL='7c8acab3ff84c6c8caadec8998296936a156e0bd'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'local_path':str(p)}
def prepare(expected):
 grant=json.loads((A/'MAIN_WRITER_RETURN.json').read_text())
 require(grant['explicit_return_received'] and grant['returned_MAIN']==expected,'Fresh explicit writer grant required')
 require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced')
 pr=api('pulls/164');require(pr['state']=='closed' and not pr['merged'] and pr['head']['sha']==ORIGINAL,'Actual original closed PR required')
 require(json.loads((A/'ROOT_PRIORITY_GATE.json').read_text())['status']=='ROOT_PRIORITY_GATE_FAIL_ALREADY_SOLVED','Priority gate absent')
 require(json.loads((A/'ROOT_MATHEMATICAL_GATE.json').read_text())['status']=='ACCEPTED_UNIVERSAL_ORDINARY_CUP_AND_GRADED_LIE_RESULT','Math gate absent')
 require(json.loads((A/'PR_CLOSURE_ACCEPTANCE.json').read_text())['status']=='ACTUAL_PR_CLOSED_UNMERGED_AND_EXACT_COMMENT_METADATA_ACCEPTED','Closure receipt absent')
 out=A/'findings_checkpoint';require(not out.exists(),'Preparation exists; inspect before retry')
 out.mkdir();now=stamp();parent=api('git/commits/'+expected)
 qpath='unsolved_math_prioritization/QUEUE.md';old=body_at(qpath,expected).decode();ls=old.splitlines(keepends=True)
 idx=[i for i,l in enumerate(ls) if '| 30002879 /' in l];require(len(idx)==1,'QUEUE target not unique')
 i=idx[0];oldrow=ls[i];cells=oldrow.rstrip('\n').split('|');require(len(cells)==14,'QUEUE schema changed')
 save(A/'PREFLIGHT_BASE_QUEUE_STATUS_OBSERVATION.json',{'UTC':now,'MAIN':expected,'target_row':oldrow.rstrip('\n'),'original_literal_status':'claimed_solved','original_effort':'2/5'})
 cells[8]=' already_solved ';cells[9]=' 2/5 '
 cells[11]=' Full ordinary Gerstenhaber result mathematically valid, but explicit prior Long-Shi-Zhou arXiv:2609.19560v1 (17 September2026), Theorems7.1/8.3, predates original30 September GitHub disclosure; exact all-field/all-degree algebra and generator dictionary verified. Strong nilpotent-ideal quotientK also prior8.6; coefficient-sequence route uses Hermann6.17/8.11 and is alternative reconstruction, no substantive new resolution established. Three mathematical and three priority families accepted. PR164 closed unmerged; no paper/DOI/tracker. Audit: draft_pr_publication_program_20260930/audits/pr164_30002879; https://github.com/AlecKriebel/Math/pull/164#issuecomment-6122094867. '
 cells[12]=' — ';ls[i]='|'.join(cells)+'\n';new=''.join(ls)
 require(len(old.splitlines())==len(new.splitlines()) and sum(x!=y for x,y in zip(old.splitlines(),new.splitlines()))==1,'Other QUEUE rows changed')
 (out/'QUEUE.accepted.md').write_text(new)
 names=['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md'];before={n:body_at('draft_pr_publication_program_20260930/'+n,expected) for n in names}
 j=json.loads(before[names[0]]);require(j['fully_completed_count']==31 and len(j['fully_completed_eligible_PRs'])==31 and 164 not in j['fully_completed_eligible_PRs'],'Completion census changed')
 require(j['published_count']==18 and len(j['published_PRs'])==18,'Publication census changed')
 j.setdefault('historical_completed_case_records',[]).append({'PR':156,'fields':{k:v for k,v in j.items() if k.startswith('last_completed_')},'actual_receipt':'audits/pr156_30005432/FINAL_CHECKPOINT_ACCEPTANCE.json'})
 j.setdefault('historical_preparation_snapshots',[]).append({'UTC':now,'PR':164,'fields':{k:v for k,v in j.items() if k.startswith('current_')},'note':'PR156 already actually complete; prior snapshot condition fulfilled by actual final receipt.'})
 for k in list(j):
  if k.startswith(('current_','last_completed_')):del j[k]
 j['fully_completed_eligible_PRs'].append(164)
 if 164 not in j['closed_without_publication_PRs']:j['closed_without_publication_PRs'].append(164)
 j.pop('persistent_goal_status',None)
 j.update({'UTC':now,'updated_UTC':now,'fully_completed_count':32,'fully_completed_fraction_percent':round(3200/99,2),'workflow_estimate_percent':round(3200/99,2),'published_count':18,'last_completed_PR':164,'last_completed_PR_workflow_percent':100,'last_completed_original_head':ORIGINAL,'last_completed_original_QUEUE_status':'claimed_solved','last_completed_original_budget':'2/5','last_completed_mathematical_result_valid':True,'last_completed_priority_clearance':False,'last_completed_outcome':'already_solved_closed_unmerged_no_new_paper','last_completed_DOI':None,'last_completed_merge_commit':None,'last_completed_tracker_range':None,'last_completed_record':'audits/pr164_30002879/WORKFLOW_COMPLETION.json',
 'current_PR':164,'current_problem_id':30002879,'current_original_head':ORIGINAL,'current_original_QUEUE_status':'claimed_solved','current_original_budget':'2/5','current_status':'ACTUALLY_CLOSED_ALREADY_SOLVED_FINDINGS_ACCEPTANCE_PENDING_AT_SNAPSHOT','current_PR_workflow_percent':100,'current_workflow_estimate_percent':100,'current_mathematical_review_percent':100,'current_mathematics_cleared':True,'current_mathematical_result_valid':True,'current_priority_decision_percent':100,'current_priority_clearance':False,'current_priority_status':'Exact explicit earlier full result LSZ7.1/8.3; no substantive new target theorem. All three scientific priority families accepted.','current_Zenodo_published':False,'current_tracker_updated':False,'current_original_PR_merged':False,'current_closed':True,'current_publication_ready':False,'current_publication_disposition_pending':False,'current_publication_package_reviews_required':False,'current_remaining_required_steps':'Actual normal expected-old MAIN findings acceptance and final factual checkpoint readback.','current_record':'audits/pr164_30002879/CURRENT_CASE_STATUS.json','current_mathematical_gate':'audits/pr164_30002879/ROOT_MATHEMATICAL_GATE.json','current_priority_gate':'audits/pr164_30002879/ROOT_PRIORITY_GATE.json',
 'next_numeric_intake_cursor':165,'next_eligible_PR_after_current_completion':None,'next_eligible_order_requires_fresh_status_check':True,'next_step':'After actual PR164 completion and writer return, continue original-head status-only intake from PR165; skip every originally non-claimed status entirely.','remaining_current_step':'Actual PR164 findings and final factual checkpoint acceptance.','advance_to_next_PR_authorized_now':False,'goal_work_continuing':True,'persistent_goal_complete':False,'actual_goal_runtime_status_last_read':'blocked; objective file read; continuing directly authorized work','workflow_estimate_definition':'32/dated99=32.32% after actual accepted PR164 disposition/findings;18 published. PR164 receives no paper/DOI/tracker.',
 'program_snapshot_authority_condition':'audits/pr164_30002879/FINDINGS_CHECKPOINT_ACCEPTANCE.json must report actual MAIN commit/tree/sole parent and selected object readbacks.','program_snapshot_semantics':'Counts apply upon actual accepted findings snapshot, never merely from preparation.','completion_metadata_checkpoint_pending_at_snapshot':True,'active_checkpoint_commit':None,'active_checkpoint_acceptance_receipt':'audits/pr164_30002879/FINDINGS_CHECKPOINT_ACCEPTANCE.json','active_checkpoint_actual_readback_required':True,'active_checkpoint_source_plan_review_required':False,'active_checkpoint_local_installation_performed_by_this_preparation':False,'active_checkpoint_publication_performed_by_this_preparation':False})
 j['skipped_since_last_completion']=[157,158,159,160,161,162,163]
 j['latest_ordered_intake_record']='status_intakes_after_pr156/INTAKE_SUMMARY.json'
 save(out/names[0],j)
 note='\n\n'+now+' — PR164: mathematics100%, priority decision100%; exact prior LSZ arXiv2609.19560v1 (17 September2026), Theorems7.1/8.3/8.6, precedes original30 September proof/PR. Shorter coefficient route retained as verified reconstruction using prior Hermann machinery. Actual PR closed unmerged10:07:14UTC; comment6122094867. No paper/DOI/tracker. This one-row QUEUE and own audit/programme findings snapshot brings completed count32/dated99=32.32%,18 published upon actual MAIN acceptance. Original nonclaimed PR157–163 status-only skipped untouched. Actual final acceptance and writer return required before PR165 intake. Goal work continues and is incomplete.\n'
 for n in names[1:]:(out/n).write_bytes(before[n]+note.encode())
 status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());status.update({'UTC':now,'status':'ACTUALLY_CLOSED_ALREADY_SOLVED_FINDINGS_PREPARED_NOT_ACCEPTED','case_percent':85,'MAIN_shared_index_ref_checkout_writer_authority':False,'bounded_remote_MAIN_writer_authority':True,'findings_MAIN_acceptance_pending':True});save(A/'CURRENT_CASE_STATUS.json',status)
 done={'UTC':now,'PR':164,'problem_id':30002879,'original_head':ORIGINAL,'original_QUEUE_status':'claimed_solved','original_budget':'2/5','status':'SCIENCE_AND_ACTUAL_CLOSURE_COMPLETE_FINDINGS_ACCEPTANCE_PENDING','case_workflow_percent':85,'mathematics_valid':True,'mathematical_review_percent':100,'priority_decision_percent':100,'novelty_established':False,'disposition':'already_solved closed unmerged','closed_at':pr['closed_at'],'closure_comment_url':'https://github.com/AlecKriebel/Math/pull/164#issuecomment-6122094867','new_paper':False,'new_Zenodo_record':False,'new_tracker_row':False,'fully_completed_count_before_acceptance':31,'fully_completed_count_after_acceptance':32,'published_count':18,'dated_eligible_total':99,'goal_complete':False,'next_numeric_intake_cursor':165};save(A/'WORKFLOW_COMPLETION.json',done)
 with (A/'RESEARCH_LOG.md').open('a') as h:h.write(note)
 plan=json.loads((A/'FINDINGS_SCOPE_PLAN.json').read_text())
 overlay={qpath:out/'QUEUE.accepted.md',**{'draft_pr_publication_program_20260930/'+n:out/n for n in names}}
 for rel in plan['public_audit_relative_paths']:
  p=A/rel;require(p.is_file(),'Missing own selected '+rel);overlay[p.relative_to(C).as_posix()]=p
 for rel in plan['ordered_intake_public_relative_paths']:
  p=P/rel;require(p.is_file(),'Missing intake '+rel);overlay[p.relative_to(C).as_posix()]=p
 pins={n:pin(p) for n,p in sorted(overlay.items())};entries=[{'path':n,'mode':'100644','type':'blob','content':p.read_text()} for n,p in sorted(overlay.items())]
 tree=api('git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':entries})
 changed={n for n,v in pins.items() if lookup(parent['tree']['sha'],n)!=('100644','blob',v['git_blob'])}
 require(changed_leaves(parent['tree']['sha'],tree['sha'])==changed,'Unexpected actual tree diff')
 for n,v in pins.items():require(lookup(tree['sha'],n)==('100644','blob',v['git_blob']),'Selected tree identity differs')
 commit=api('git/commits','POST',{'message':'Record PR164 as already solved after independent mathematical and priority audits\n\nExact prior full Gerstenhaber result LSZ September17 predates original September30 disclosure. Preserve verified alternative derivation; actual PR closed unmerged. No new paper/DOI/tracker. Change only target QUEUE row and own audit/programme/intake evidence; all foreign base-tree paths preserved.','tree':tree['sha'],'parents':[expected]})
 actual=api('git/commits/'+commit['sha']);require(actual['tree']['sha']==tree['sha'] and [p['sha'] for p in actual['parents']]==[expected],'Commit tree/parent mismatch')
 require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced; do not apply stale commit')
 rec={'UTC':stamp(),'status':'SCOPED_FINDINGS_PREPARED_MAIN_NOT_UPDATED','expected_main':expected,'parent_tree':parent['tree']['sha'],'tree':tree['sha'],'commit':commit['sha'],'selected_files':pins,'actual_changed_paths':sorted(changed),'QUEUE_rows_changed':1,'foreign_base_tree_paths_preserved':True,'no_local_Git_mutations':True,'original_author_branch_modified':False,'original_PR_merged':False,'new_publication':False}
 save(A/'FINDINGS_CHECKPOINT_PREPARATION.json',rec)
 print(json.dumps({k:rec[k] for k in ('status','expected_main','tree','commit')}));print('Selected',len(pins))
if __name__=='__main__':
 require(len(sys.argv)==2,'Actual fresh returned MAIN SHA required')
 prepare(sys.argv[1])
