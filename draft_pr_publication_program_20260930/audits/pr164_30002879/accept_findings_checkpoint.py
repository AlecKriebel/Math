"""Read back the PR164 scoped commits and prepare one bounded factual completion commit."""
from pathlib import Path
import base64,datetime,hashlib,json,sys,concurrent.futures,importlib.util
A=Path(__file__).resolve().parent;C=A.parents[2];P=C/'draft_pr_publication_program_20260930'
s=importlib.util.spec_from_file_location('prepare',A/'prepare_findings_checkpoint.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
api,require,save,lookup,changed_leaves,body_at,pin,stamp=m.api,m.require,m.save,m.lookup,m.changed_leaves,m.body_at,m.pin,m.stamp
def accept(prepname,receiptname):
 prep=json.loads((A/prepname).read_text());actual=api('git/ref/heads/main')['object']['sha']
 require(actual==prep['commit'],'Actual MAIN differs; reconcile, never overwrite')
 commit=api('git/commits/'+actual);require(commit['tree']['sha']==prep['tree'] and [r['sha'] for r in commit['parents']]==[prep['expected_main']],'Actual commit/tree/parent differs')
 require(changed_leaves(prep['parent_tree'],prep['tree'])==set(prep['actual_changed_paths']),'Actual full-tree scope differs')
 byblob={}
 for n,r in prep['selected_files'].items():
  require(lookup(prep['tree'],n)==('100644','blob',r['git_blob']),'Selected tree path differs '+n)
  byblob.setdefault(r['git_blob'],r)
 def check_blob(item):
  sha,r=item;v=api('git/blobs/'+sha);require(v['encoding']=='base64','Unexpected blob encoding')
  b=base64.b64decode(v['content']);require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'Exact remote bytes differ')
  require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==sha,'Remote Git blob mismatch')
  return {'git_blob':sha,'bytes':len(b),'sha256':r['sha256']}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:identities=list(pool.map(check_blob,byblob.items()))
 pr=api('pulls/164');require(pr['state']=='closed' and not pr['merged'] and pr['head']['sha']==m.ORIGINAL,'Actual PR disposition changed')
 rec={'UTC':stamp(),'status':'ACTUAL_MAIN_SCOPED_COMMIT_TREE_PARENT_AND_SELECTED_BYTES_ACCEPTED','PR':164,'actual_MAIN':actual,'actual_tree':prep['tree'],'actual_sole_parent':prep['expected_main'],'selected_files':prep['selected_files'],'unique_remote_blob_readbacks':identities,'actual_changed_paths':prep['actual_changed_paths'],'foreign_base_tree_paths_preserved':True,'no_local_Git_mutations':True,'actual_PR_closed_unmerged':True,'original_head_unchanged':True,'new_paper':False,'new_DOI':False,'new_tracker_row':False,'goal_complete':False}
 save(A/receiptname,rec);print(json.dumps({'status':rec['status'],'actual_MAIN':actual,'selected_files':len(prep['selected_files']),'unique_remote_blobs':len(identities),'receipt':receiptname}))
 return rec
def prepare_final():
 first=json.loads((A/'FINDINGS_CHECKPOINT_ACCEPTANCE.json').read_text());expected=first['actual_MAIN']
 require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced after findings')
 grant=json.loads((A/'MAIN_WRITER_RETURN.json').read_text());require(grant['explicit_return_received'],'Writer grant absent')
 out=A/'final_checkpoint';require(not out.exists(),'Final preparation exists; inspect first');out.mkdir();now=stamp()
 j=json.loads(body_at('draft_pr_publication_program_20260930/CURRENT_PROGRESS.json',expected))
 require(j['fully_completed_count']==32 and 164 in j['fully_completed_eligible_PRs'] and j['published_count']==18,'Actual census differs')
 j.update({'UTC':now,'updated_UTC':now,'current_status':'CLOSED_ALREADY_SOLVED_FINDINGS_ACTUALLY_ACCEPTED','current_PR_workflow_percent':100,'current_workflow_estimate_percent':100,'current_remaining_required_steps':'None for this case after actual acceptance of this factual completion checkpoint.','current_findings_commit':expected,'current_findings_acceptance_receipt':'audits/pr164_30002879/FINDINGS_CHECKPOINT_ACCEPTANCE.json','completion_metadata_checkpoint_pending_at_snapshot':False,'program_snapshot_semantics':'PR164 actual closed disposition and science/findings accepted; this commit records completion facts.','program_snapshot_authority_condition':'This completion metadata applies upon actual expected-old nonforce acceptance and readback of its own commit; FINAL_CHECKPOINT_ACCEPTANCE.json records the actual object identities.','active_checkpoint_commit':expected,'active_checkpoint_acceptance_receipt':'audits/pr164_30002879/FINAL_CHECKPOINT_ACCEPTANCE.json','active_checkpoint_actual_readback_required':True,'advance_to_next_PR_authorized_now':True,'remaining_current_step':'None for PR164 after factual checkpoint acceptance; return bounded window before next intake.','next_step':'Continue original-head status-only intake at PR165 after actual final acceptance and writer return.','workflow_estimate_definition':'32/dated99=32.32% completed,18 published; PR164 already_solved closed unmerged, no paper/DOI/tracker.','goal_work_continuing':True,'persistent_goal_complete':False})
 save(out/'CURRENT_PROGRESS.json',j)
 note='\n\n'+now+' — PR164 completion: actual science and closure accepted; MAIN findings commit '+expected+' read back with exact selected bytes and full actual tree scope. Case100%, programme32/dated99=32.32%,18 published; exact prior LSZ full theorem, valid reconstruction retained, no paper/DOI/tracker. This bounded factual checkpoint records completion; actual final receipt and explicit writer return precede PR165 status-only intake. Goal incomplete.\n'
 for n in ('CURRENT_PROGRESS.md','RESEARCH_LOG.md'):(out/n).write_bytes(body_at('draft_pr_publication_program_20260930/'+n,expected)+note.encode())
 status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());status.update({'UTC':now,'status':'CLOSED_ALREADY_SOLVED_FINDINGS_ACCEPTED_FINAL_FACTUAL_CHECKPOINT_READY','case_percent':100,'findings_MAIN_acceptance_pending':False,'findings_MAIN_commit':expected,'fully_completed_count':32,'published_count':18,'final_factual_checkpoint_acceptance_required':True,'bounded_remote_MAIN_writer_authority':True,'persistent_goal_complete':False});save(A/'CURRENT_CASE_STATUS.json',status)
 done=json.loads((A/'WORKFLOW_COMPLETION.json').read_text());done.update({'UTC':now,'status':'ACTUAL_SCIENCE_CLOSURE_AND_FINDINGS_COMPLETE_FACTUAL_CHECKPOINT','case_workflow_percent':100,'findings_MAIN_commit':expected,'findings_MAIN_accepted':True,'fully_completed_count':32,'published_count':18,'final_factual_checkpoint_acceptance_required':True});save(A/'WORKFLOW_COMPLETION.json',done)
 with (A/'RESEARCH_LOG.md').open('a') as h:h.write(note)
 overlay={'draft_pr_publication_program_20260930/'+n:out/n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
 for n in ('CURRENT_CASE_STATUS.json','WORKFLOW_COMPLETION.json','RESEARCH_LOG.md','FINDINGS_CHECKPOINT_ACCEPTANCE.json'):overlay[(A/n).relative_to(C).as_posix()]=A/n
 pins={n:pin(p) for n,p in sorted(overlay.items())};parent=api('git/commits/'+expected)
 tree=api('git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':[{'path':n,'mode':'100644','type':'blob','content':p.read_text()} for n,p in sorted(overlay.items())]})
 changed={n for n,r in pins.items() if lookup(parent['tree']['sha'],n)!=('100644','blob',r['git_blob'])}
 require(changed_leaves(parent['tree']['sha'],tree['sha'])==changed,'Final factual scope differs')
 for n,r in pins.items():require(lookup(tree['sha'],n)==('100644','blob',r['git_blob']),'Final selected blob differs')
 commit=api('git/commits','POST',{'message':'Record actual PR164 already-solved disposition and findings acceptance\n\n32 of dated99 eligible cases complete;18 preprints. No new publication forPR164. Seven factual audit/programme files only; foreign scientific paths preserved.','tree':tree['sha'],'parents':[expected]})
 actual=api('git/commits/'+commit['sha']);require(actual['tree']['sha']==tree['sha'] and [p['sha'] for p in actual['parents']]==[expected],'Final commit differs')
 require(api('git/ref/heads/main')['object']['sha']==expected,'MAIN advanced; no stale update')
 rec={'UTC':stamp(),'status':'FACTUAL_COMPLETION_PREPARED_MAIN_NOT_UPDATED','expected_main':expected,'parent_tree':parent['tree']['sha'],'tree':tree['sha'],'commit':commit['sha'],'selected_files':pins,'actual_changed_paths':sorted(changed),'foreign_base_tree_paths_preserved':True,'no_local_Git_mutations':True};save(A/'FINAL_CHECKPOINT_PREPARATION.json',rec)
 print(json.dumps({k:rec[k] for k in ('status','expected_main','tree','commit')}))
if __name__=='__main__':
 require(len(sys.argv)==2,'Pass findings-accept, final-prepare or final-accept')
 if sys.argv[1]=='findings-accept':accept('FINDINGS_CHECKPOINT_PREPARATION.json','FINDINGS_CHECKPOINT_ACCEPTANCE.json')
 elif sys.argv[1]=='final-prepare':prepare_final()
 elif sys.argv[1]=='final-accept':accept('FINAL_CHECKPOINT_PREPARATION.json','FINAL_CHECKPOINT_ACCEPTANCE.json')
 else:raise RuntimeError('Unknown action')

