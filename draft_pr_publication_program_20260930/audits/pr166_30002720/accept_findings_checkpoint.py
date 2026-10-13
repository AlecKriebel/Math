"""Read actual PR166 remote artifacts; prepare only a seven-file factual completion commit."""
from pathlib import Path
import base64,datetime,hashlib,json,sys,concurrent.futures,importlib.util
A=Path(__file__).resolve().parent;C=A.parents[2]
s=importlib.util.spec_from_file_location('prepare166',A/'prepare_findings_checkpoint.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
api,require,save,lookup,changed_leaves,body_at,pin,stamp=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at,m.pin,m.stamp
def accept(prepname,receiptname):
 prep=json.loads((A/prepname).read_text());actual=api('git/ref/heads/main')['object']['sha']
 require(actual==prep['commit'],'Actual MAIN differs; inspect, never overwrite')
 commit=api('git/commits/'+actual);require(commit['tree']['sha']==prep['tree'] and [r['sha'] for r in commit['parents']]==[prep['expected_main']],'Actual commit tree or sole parent differs')
 require(changed_leaves(prep['parent_tree'],prep['tree'])==set(prep['actual_changed_paths']),'Full actual tree diff differs')
 byblob={}
 for n,r in prep['selected_files'].items():
  require(lookup(prep['tree'],n)==('100644','blob',r['git_blob']),'Selected tree path differs '+n);byblob.setdefault(r['git_blob'],r)
 def check_blob(item):
  sha,r=item;v=api('git/blobs/'+sha);require(v['encoding']=='base64','Unexpected blob encoding');b=base64.b64decode(v['content'])
  require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'Exact remote bytes differ')
  require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==sha,'Remote Git blob identity differs')
  return dict(git_blob=sha,bytes=len(b),sha256=r['sha256'])
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:identities=list(pool.map(check_blob,byblob.items()))
 pr=api('pulls/166');plan=json.loads((A/'PR_DISPOSITION_PLAN.json').read_text());closure=json.loads((A/'PR_CLOSURE_ACCEPTANCE.json').read_text())
 require(pr['state']=='closed' and not pr['merged'] and pr['head']['sha']==m.ORIGINAL and pr['title']==plan['intended_title'] and pr['body']==(A/'PR_CLOSURE_BODY.md').read_text(),'Actual PR metadata/disposition differs')
 comment=api('issues/comments/'+str(closure['comment_id']));require(comment['body']==(A/'PR_CLOSURE_COMMENT.md').read_text(),'Actual closure comment differs')
 rec=dict(UTC=stamp(),status='ACTUAL_MAIN_SCOPED_COMMIT_TREE_PARENT_AND_SELECTED_BYTES_ACCEPTED',PR=166,actual_MAIN=actual,actual_tree=prep['tree'],actual_sole_parent=prep['expected_main'],selected_files=prep['selected_files'],unique_remote_blob_readbacks=identities,actual_changed_paths=prep['actual_changed_paths'],foreign_base_tree_paths_preserved=True,no_local_Git_mutations=True,actual_PR_closed_unmerged=True,original_head_unchanged=True,exact_comment_title_body_accepted=True,new_paper=False,new_DOI=False,new_tracker_row=False,goal_complete=False)
 save(A/receiptname,rec);print(json.dumps(dict(status=rec['status'],actual_MAIN=actual,selected_files=len(prep['selected_files']),unique_remote_blobs=len(identities),receipt=receiptname)));return rec
def prepare_final():
 first=json.loads((A/'FINDINGS_CHECKPOINT_ACCEPTANCE.json').read_text());expected=first['actual_MAIN'];require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced after accepted findings')
 grant=json.loads((A/'MAIN_WRITER_RETURN.json').read_text());require(grant['explicit_return_received'] and grant['PR']==166,'Fresh bounded grant absent')
 out=A/'final_checkpoint';require(not out.exists(),'Final objects may exist; inspect before retry');out.mkdir();now=stamp()
 j=json.loads(body_at('draft_pr_publication_program_20260930/CURRENT_PROGRESS.json',expected));require(j['fully_completed_count']==33 and 166 in j['fully_completed_eligible_PRs'] and j['published_count']==18,'Actual census differs')
 j.update(dict(UTC=now,updated_UTC=now,current_status='CLOSED_ORIGINAL_TARGET_PRIOR_KNOWN_VALID_REFINEMENT_FINDINGS_ACTUALLY_ACCEPTED',current_PR_workflow_percent=100,current_workflow_estimate_percent=100,current_remaining_required_steps='None for this case after actual factual checkpoint acceptance.',current_findings_commit=expected,current_findings_acceptance_receipt='audits/pr166_30002720/FINDINGS_CHECKPOINT_ACCEPTANCE.json',completion_metadata_checkpoint_pending_at_snapshot=False,program_snapshot_semantics='PR166 actual closure and full science/findings accepted; factual completion records that state.',program_snapshot_authority_condition='Actual expected-old nonforce acceptance and readback of this factual commit; FINAL_CHECKPOINT_ACCEPTANCE.json records actual objects.',active_checkpoint_commit=expected,active_checkpoint_acceptance_receipt='audits/pr166_30002720/FINAL_CHECKPOINT_ACCEPTANCE.json',active_checkpoint_actual_readback_required=True,advance_to_next_PR_authorized_now=True,remaining_current_step='None forPR166 after factual checkpoint acceptance; return bounded window before next intake.',next_step='Status-only original-head intake fromPR167 after actual final acceptance and writer return.',workflow_estimate_definition='33/dated99=33.33% completed,18published. PR166 prior-known original target; exact refinement and new category deduction retained; no paper/DOI/tracker.',goal_work_continuing=True,persistent_goal_complete=False))
 save(out/'CURRENT_PROGRESS.json',j)
 note='\n\n'+now+' — PR166 completed: actual closure and science/findings accepted; MAIN '+expected+' independently read back with full semantic tree scope and exact selected bytes. Case100%, programme33/dated99=33.33%,18publications. Valid explicit refinement and fresh category theorem retained, priority unestablished for them; original unrestricted target prior known. No paper/DOI/tracker. Factual checkpoint actual acceptance and writer return precedePR167 intake. Goal unfinished.\n'
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:(out/n).write_bytes(body_at('draft_pr_publication_program_20260930/'+n,expected)+note.encode())
 status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());status.update(UTC=now,status='CLOSED_ORIGINAL_TARGET_PRIOR_KNOWN_FINDINGS_ACCEPTED_FINAL_FACTUAL_CHECKPOINT_READY',case_percent=100,MAIN_findings_pending=False,findings_MAIN_commit=expected,fully_completed_count=33,published_count=18,final_factual_checkpoint_acceptance_required=True,bounded_remote_MAIN_writer_authority=True,persistent_goal_complete=False);save(A/'CURRENT_CASE_STATUS.json',status)
 done=json.loads((A/'WORKFLOW_COMPLETION.json').read_text());done.update(UTC=now,status='ACTUAL_SCIENCE_CLOSURE_AND_FINDINGS_COMPLETE_FACTUAL_CHECKPOINT',case_workflow_percent=100,findings_MAIN_commit=expected,findings_MAIN_accepted=True,fully_completed_count=33,published_count=18,final_factual_checkpoint_acceptance_required=True);save(A/'WORKFLOW_COMPLETION.json',done)
 with (A/'RESEARCH_LOG.md').open('a') as h:h.write(note)
 overlay={'draft_pr_publication_program_20260930/'+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
 for n in ['CURRENT_CASE_STATUS.json','WORKFLOW_COMPLETION.json','RESEARCH_LOG.md','FINDINGS_CHECKPOINT_ACCEPTANCE.json']:overlay[(A/n).relative_to(C).as_posix()]=A/n
 require(len(overlay)==7,'Factual scope exceeds concrete window')
 m.create_objects(expected,overlay,'Record actual PR166 original-target disposition and accepted verified findings\n\n33 of dated99 eligible cases complete;18publications. Seven factual ROOT audit/programme files only. No new paper/DOI/tracker or native author-branch merge. Preserve foreign paths.','FINAL_CHECKPOINT_PREPARATION.json')
if __name__=='__main__':
 require(len(sys.argv)==2,'Pass findings-accept, final-prepare or final-accept')
 action=sys.argv[1]
 if action=='findings-accept':accept('FINDINGS_CHECKPOINT_PREPARATION.json','FINDINGS_CHECKPOINT_ACCEPTANCE.json')
 elif action=='final-prepare':prepare_final()
 elif action=='final-accept':accept('FINAL_CHECKPOINT_PREPARATION.json','FINAL_CHECKPOINT_ACCEPTANCE.json')
 else:raise RuntimeError('Unknown action')

