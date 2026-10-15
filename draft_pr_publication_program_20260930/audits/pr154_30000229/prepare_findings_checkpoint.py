#!/usr/bin/env python3
"""Publish only the completed PR154 research audit, after an explicit writer return."""
import datetime,hashlib,json,sys,importlib.util
from pathlib import Path
A=Path(__file__).resolve().parent
C=A.parents[2]
P=C/'draft_pr_publication_program_20260930'
spec=importlib.util.spec_from_file_location('scope',P/'audits/pr152_5000006/prepare_scoped_merge.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
api,require,lookup,changed_leaves,body_at,save=m.api,m.require,m.lookup,m.changed_leaves,m.body_at,m.save
ORIGINAL='58bee8514677549ee5a7cd699028a5f3a616c5bc'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 require(len(sys.argv)==2,'Pass actual returned MAIN SHA')
 expected=sys.argv[1]
 window=json.loads((A/'MAIN_WRITER_RETURN.json').read_text())
 require(window['explicit_return_received'] and window['returned_MAIN']==expected,'Actual explicit writer return required')
 require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced; inspect actual state')
 pr=api('pulls/154')
 require(pr['state']=='closed' and not pr['merged'] and pr['head']['sha']==ORIGINAL,'Actual closed original PR required')
 gate=json.loads((A/'ROOT_MATHEMATICAL_GATE.json').read_text())
 priority=json.loads((A/'ROOT_PRIORITY_GATE.json').read_text())
 closure=json.loads((A/'PR_CLOSURE_ACCEPTANCE.json').read_text())
 require(gate['status']=='ROOT_ACCEPTED_MATHEMATICAL_ENDPOINT_COUNTEREXAMPLE','Mathematical gate differs')
 require(priority['status']=='ROOT_PRIORITY_GATE_FAIL_ALREADY_SOLVED','Priority gate differs')
 require(closure['status']=='ACTUAL_PR_CLOSED_UNMERGED_AND_EXACT_COMMENT_METADATA_ACCEPTED','Closure not accepted')
 now=stamp()
 out=A/'findings_checkpoint';require(not out.exists(),'Preparation exists: inspect actual outcome before retry')
 out.mkdir()
 parent=api('git/commits/'+expected)
 qpath='unsolved_math_prioritization/QUEUE.md'
 old=body_at(qpath,expected).decode()
 lines=old.splitlines(keepends=True)
 target=[i for i,s in enumerate(lines) if '| 30000229 /' in s]
 require(len(target)==1,'Target QUEUE row not unique')
 i=target[0];cells=lines[i].rstrip('\n').split('|')
 require(len(cells)==14,'QUEUE schema changed')
 base_queue_observation=json.loads((A/'PREFLIGHT_BASE_QUEUE_STATUS_OBSERVATION.json').read_text())
 require(base_queue_observation['MAIN']==expected and base_queue_observation['target_rows']==[lines[i].rstrip('\n')],'Observed live target row changed; inspect')
 cells[8]=' already_solved ';cells[9]=' 2/5 '
 cells[11]=(' Original claimed_solved submission mathematically valid at s=1/2, but endpoint already resolved by Kreuzer-Veeser arXiv:1903.05915 (14 March 2019), Lemma21 with Lemma4(ii); Numer.Math.148(2021), DOI10.1007/s00211-021-01194-8. Their formula3.19b is the identical corrected edge bubble up to normalization. Logarithmic bound is an elementary sharpening of the old CDN/KV ingredients; no substantive novelty established. Three independent math and three priority families accepted. PR154 closed unmerged; no paper/DOI/tracker. Audit: draft_pr_publication_program_20260930/audits/pr154_30000229; detailed closure https://github.com/AlecKriebel/Math/pull/154#issuecomment-6118299650. ')
 cells[12]=' — '
 lines[i]='|'.join(cells)+'\n';new=''.join(lines)
 require(len(old.splitlines())==len(new.splitlines()) and sum(x!=y for x,y in zip(old.splitlines(),new.splitlines()))==1,'Other QUEUE lines changed')
 queue=out/'QUEUE.accepted.md';queue.write_text(new)
 names=['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']
 before={n:body_at('draft_pr_publication_program_20260930/'+n,expected) for n in names}
 j=json.loads(before[names[0]])
 require(j['fully_completed_count']==29 and len(j['fully_completed_eligible_PRs'])==29 and 154 not in j['fully_completed_eligible_PRs'],'Programme completed census changed')
 require(j['published_count']==17 and len(j['published_PRs'])==17,'Publication census changed')
 j.setdefault('historical_completed_case_records',[]).append({'PR':152,'fields':{k:v for k,v in j.items() if k.startswith('last_completed_')},'actual_completion_receipt':'audits/pr152_5000006/FINAL_CHECKPOINT_ACCEPTANCE.json'})
 j.setdefault('historical_preparation_snapshots',[]).append({'UTC':now,'PR':154,'fields':{k:v for k,v in j.items() if k.startswith('current_')},'note':'Prior dated mathematical/priority preparation retained; superseded by actual closed disposition.'})
 for k in list(j):
  if k.startswith(('current_','last_completed_')):del j[k]
 j['fully_completed_eligible_PRs'].append(154)
 j.update({'UTC':now,'updated_UTC':now,'fully_completed_count':30,'fully_completed_fraction_percent':round(3000/99,2),'workflow_estimate_percent':round(3000/99,2),'published_count':17,
 'last_completed_PR':154,'last_completed_PR_workflow_percent':100,'last_completed_original_head':ORIGINAL,'last_completed_original_budget':'2/5','last_completed_original_QUEUE_status':'claimed_solved','last_completed_mathematical_result_valid':True,'last_completed_priority_clearance':False,'last_completed_outcome':'already_solved_closed_unmerged_no_new_paper','last_completed_DOI':None,'last_completed_merge_commit':None,'last_completed_tracker_range':None,'last_completed_source_resolution_scope':'Endpoint counterexample and edge bubble already in Kreuzer-Veeser2019/2021; exact logarithmic bound elementary from old CDN/KV ingredients. Full math valid; no substantive novelty established.','last_completed_record':'audits/pr154_30000229/WORKFLOW_COMPLETION.json',
 'current_PR':154,'current_problem_id':30000229,'current_original_head':ORIGINAL,'current_original_QUEUE_status':'claimed_solved','current_original_budget':'2/5','current_PR_workflow_percent':100,'current_workflow_estimate_percent':100,'current_status':'ACTUALLY_CLOSED_ALREADY_SOLVED_FINDINGS_ACCEPTANCE_PENDING_AT_SNAPSHOT','current_mathematical_review_percent':100,'current_mathematical_result_valid':True,'current_mathematics_cleared':True,'current_priority_clearance':False,'current_priority_decision_percent':100,'current_priority_status':'Three independent primary-source priority families accepted: exact prior endpoint and bubble, no substantive novelty.','current_Zenodo_published':False,'current_original_PR_merged':False,'current_tracker_updated':False,'current_closed':True,'current_publication_ready':False,'current_publication_disposition_pending':False,'current_publication_package_reviews_complete':False,'current_publication_package_reviews_required':False,'current_remaining_required_steps':'This prepared findings snapshot requires actual expected-old nonforce MAIN acceptance and readback; mathematical/priority/disposition steps complete.','current_record':'audits/pr154_30000229/CURRENT_CASE_STATUS.json','current_mathematical_gate':'audits/pr154_30000229/ROOT_MATHEMATICAL_GATE.json','current_priority_gate':'audits/pr154_30000229/ROOT_PRIORITY_GATE.json',
 'next_numeric_intake_cursor':155,'next_eligible_PR_after_current_completion':None,'next_eligible_order_requires_fresh_status_check':True,'next_step':'After findings acceptance and writer return, continue original-head status-only intake from PR155; skip all original statuses other than claimed_solved entirely.','remaining_current_step':'Actual scope/readback acceptance of prepared PR154 findings checkpoint.','advance_to_next_PR_authorized_now':False,
 'persistent_goal_status':'active','persistent_goal_complete':False,'workflow_estimate_definition':'30/dated99=30.30% completed and17published after actual acceptance of this scoped findings snapshot; PR154 receives no new paper, DOI or tracker row.',
 'program_snapshot_semantics':'All external/scientific PR154 steps actually complete; these updated programme counts apply upon actual acceptance, never merely from preparation.','program_snapshot_authority_condition':'audits/pr154_30000229/FINDINGS_CHECKPOINT_ACCEPTANCE.json must report actual commit/tree/sole parent and exact selected bodies.',
 'completion_metadata_checkpoint_pending_at_snapshot':True,'active_checkpoint_commit':None,'active_checkpoint_acceptance_receipt':'audits/pr154_30000229/FINDINGS_CHECKPOINT_ACCEPTANCE.json','active_checkpoint_actual_readback_required':True,'active_checkpoint_source_plan_review_required':False,'active_checkpoint_publication_performed_by_this_preparation':False,'active_checkpoint_local_installation_performed_by_this_preparation':False})
 j.update({'next_eligible_after_PR154':156,'next_numeric_intake_cursor':157,'next_eligible_PR_after_current_completion':156,'next_step':'After PR154 findings acceptance, continue mathematical audit of PR156, original claimed_solved2/5; original PR155 already_solved0/5 status-only skip is complete and untouched.', 'PR155_status_only_skip':{'original_literal_status':'already_solved','original_budget':'0/5','processed':False,'basis':'Actual original-head status-only intake, untouched per scope'}, 'read_only_next_case':{'PR':156,'problem_id':30005432,'original_literal_status':'claimed_solved','original_budget':'2/5','original_head':'aec31742f3f26c5b1e533404da57539d17dc94a1','original_files_Git_authenticated':22,'mathematical_gate_accepted':False,'case_percent':10,'status':'Three independent mathematical families started; no result clearance or priority audit yet'}})
 save(out/names[0],j)
 note='\n\n'+now+' — PR154: original claimed_solved2/5 mathematically accepted (three distinct independent adversaries), priority decision accepted (three primary-source families): endpoint and bubble already Kreuzer-Veeser2019/2021. Logarithmic strengthening follows elementary retention of the old CDN/KV estimates. Actual PR closed unmerged2026-10-12T05:25:54Z, comment6118299650. No new paper/DOI/tracker/native author-branch merge. Dedicated audit preserves original16files and corrected diagnostics. This scoped MAIN findings preparation updates only target QUEUE30000229 and own audit/programme metadata; counts30/dated99=30.30%,17published conditional on actual acceptance. PR152 already actually complete, DOI10.5281/zenodo.23308905, merged4ac2eb7811bf2f288ac330e93b740751edb510d2; chronology qualified. Persistent goal active/incomplete; next numeric155 eligibility requires original-status-only check.\n'
 for n in names[1:]:(out/n).write_bytes(before[n]+note.encode())
 status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
 status.update({'UTC':now,'status':'ACTUALLY_CLOSED_ALREADY_SOLVED_FINDINGS_PREPARED_NOT_ACCEPTED','case_percent':85,'priority_preliminary_source':'Superseded by ROOT_PRIORITY_GATE.json: exact Kreuzer-Veeser2019/2021 prior result; priority comparison complete.','MAIN_window_owner':'ROOT explicit bounded window','findings_MAIN_acceptance_pending':True})
 save(A/'CURRENT_CASE_STATUS.json',status)
 done={'schema':'audited-pr-workflow-completion/v1','UTC':now,'PR':154,'problem_id':30000229,'original_head':ORIGINAL,'original_QUEUE_status':'claimed_solved','original_budget':'2/5','status':'SCIENCE_AND_ACTUAL_CLOSURE_COMPLETE_FINDINGS_ACCEPTANCE_PENDING','mathematics_valid':True,'mathematical_review_percent':100,'priority_decision_percent':100,'novelty_established':False,'disposition':'already_solved closed without merge or new paper','GitHub_PR_state':'CLOSED','GitHub_PR_merged':False,'closed_at':pr['closed_at'],'closure_comment_url':'https://github.com/AlecKriebel/Math/pull/154#issuecomment-6118299650','new_paper':False,'new_Zenodo_record':False,'new_tracker_row':False,'mathematical_gate':'ROOT_MATHEMATICAL_GATE.json','priority_gate':'ROOT_PRIORITY_GATE.json','closure_acceptance':'PR_CLOSURE_ACCEPTANCE.json','case_workflow_percent':85,'fully_completed_count_before_findings_acceptance':29,'fully_completed_count_after_findings_acceptance':30,'published_count':17,'dated_eligible_total':99,'persistent_goal_complete':False,'next_numeric_intake_cursor':155,'publication_performed_by_this_preparation':False}
 save(A/'WORKFLOW_COMPLETION.json',done)
 with (A/'RESEARCH_LOG.md').open('a') as h:h.write(note)
 plan=json.loads((A/'FINDINGS_SCOPE_PLAN.json').read_text())
 overlay={qpath:queue}
 for n in names:overlay['draft_pr_publication_program_20260930/'+n]=out/n
 for rel in plan['public_audit_relative_paths']:
  f=A/rel;require(f.is_file(),'Missing public own audit '+rel);overlay[f.relative_to(C).as_posix()]=f
 for rel in plan['PR152_factual_receipt_relative_paths']:
  f=P/'audits/pr152_5000006'/rel;require(f.is_file(),'Missing actual PR152 receipt '+rel);overlay[f.relative_to(C).as_posix()]=f
 for rel in plan['ordered_intake_public_relative_paths']:
  f=P/rel;require(f.is_file(),'Missing status-only ordered intake '+rel);overlay[f.relative_to(C).as_posix()]=f
 pins={};entries=[]
 for name,f in sorted(overlay.items()):
  b=f.read_bytes();sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  entries.append({'path':name,'mode':'100644','type':'blob','content':b.decode('utf8')})
  pins[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':sha,'local_path':str(f)}
 tree=api('git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':entries})
 changed={n for n,p in pins.items() if lookup(parent['tree']['sha'],n)!=('100644','blob',p['git_blob'])}
 require(changed_leaves(parent['tree']['sha'],tree['sha'])==changed,'Unexpected full-tree changed path')
 for n,p in pins.items():require(lookup(tree['sha'],n)==('100644','blob',p['git_blob']),'Selected blob differs')
 commit=api('git/commits','POST',{'message':'Record PR154 as already solved after full independent audit\n\nEndpoint result and edge bubble already Kreuzer-Veeser2019/2021; quantitative strengthening elementary from old CDN/KV ingredients. Original claimed_solved2/5 PR actually closed unmerged. No new preprint, DOI or tracker entry. Only target QUEUE row and authored audit/programme factual metadata; all other base paths preserved. Programme30/dated99 completed,17published upon actual findings acceptance.','tree':tree['sha'],'parents':[expected]})
 actual=api('git/commits/'+commit['sha'])
 require(actual['tree']['sha']==tree['sha'] and [x['sha'] for x in actual['parents']]==[expected],'Commit tree/sole parent differs')
 require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced; never apply stale lease')
 rec={'UTC':stamp(),'status':'SCOPED_FINDINGS_PREPARED_MAIN_NOT_UPDATED','expected_main':expected,'parent_tree':parent['tree']['sha'],'tree':tree['sha'],'commit':commit['sha'],'selected_files':pins,'actual_changed_paths':sorted(changed),'QUEUE_rows_changed':1,'original_author_branch_modified':False,'original_PR_merged':False,'publication_performed':False,'all_other_base_tree_paths_preserved':True}
 save(A/'FINDINGS_CHECKPOINT_PREPARATION.json',rec)
 print(json.dumps({k:rec[k] for k in ('status','expected_main','tree','commit','QUEUE_rows_changed')}));print('Selected own paths',len(pins))
if __name__=='__main__':main()
