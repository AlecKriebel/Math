#!/usr/bin/env python3
"""Accept actual scoped PR154 findings; never change refs or a Git index."""
import datetime,hashlib,json,importlib.util
from pathlib import Path
A=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('findings',A/'prepare_findings_checkpoint.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
api,require,lookup,changed_leaves,body_at,save,C=m.api,m.require,m.lookup,m.changed_leaves,m.body_at,m.save,m.C
def main():
 p=json.loads((A/'FINDINGS_CHECKPOINT_PREPARATION.json').read_text())
 require(api('git/ref/heads/main')['object']['sha']==p['commit'],'Actual MAIN differs')
 actual=api('git/commits/'+p['commit'])
 require(actual['tree']['sha']==p['tree'] and [x['sha'] for x in actual['parents']]==[p['expected_main']],'Actual tree/sole parent differs')
 require(changed_leaves(p['parent_tree'],p['tree'])==set(p['actual_changed_paths']),'Full actual changed scope differs')
 for name,pin in p['selected_files'].items():
  require(lookup(p['tree'],name)==('100644','blob',pin['git_blob']),'Actual selected blob differs')
  b=Path(pin['local_path']).read_bytes()
  require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'Prepared local body changed')
 fresh=[]
 for name in ['unsolved_math_prioritization/QUEUE.md']+['draft_pr_publication_program_20260930/'+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')]:
  pin=p['selected_files'][name];b=body_at(name,p['commit'])
  require(hashlib.sha256(b).hexdigest()==pin['sha256'],'Fresh target/programme body differs')
  (C/name).write_bytes(b);fresh.append(name)
 pr=api('pulls/154')
 require(pr['state']=='closed' and not pr['merged'] and pr['head']['sha']==m.ORIGINAL,'Actual closed original PR differs')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 rec={'UTC':now,'status':'SCOPED_FINDINGS_ACTUALLY_ACCEPTED_REMOTE_AND_OWN_LOCAL_BODIES','MAIN':p['commit'],'tree':p['tree'],'parents':[p['expected_main']],'original_head':m.ORIGINAL,'PR_closed':True,'PR_merged':False,'selected_files_verified':len(p['selected_files']),'actual_full_changed_scope_and_blob_ids_verified':True,'all_other_base_tree_paths_preserved':True,'fresh_target_and_programme_readbacks':fresh,'QUEUE_rows_changed':1,'QUEUE_status':'already_solved','original_submission_files_preserved':16,'original_author_branch_modified':False,'new_paper':False,'new_Zenodo_record':False,'new_tracker_row':False,'local_git_index_or_refs_modified':False,'primary_checkout_modified':False,'case_percent':100,'fully_completed_eligible_count':30,'published_count':17,'persistent_goal_complete':False,'next_numeric_intake_cursor':155}
 save(A/'FINDINGS_CHECKPOINT_ACCEPTANCE.json',rec)
 done=json.loads((A/'WORKFLOW_COMPLETION.json').read_text())
 done.update({'UTC':now,'status':'ALL_REQUIRED_CASE_STEPS_ACTUALLY_COMPLETE','case_workflow_percent':100,'findings_MAIN':p['commit'],'findings_tree':p['tree'],'findings_acceptance':'FINDINGS_CHECKPOINT_ACCEPTANCE.json','fully_completed_count':30})
 save(A/'WORKFLOW_COMPLETION.json',done)
 status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
 status.update({'UTC':now,'status':'ALL_REQUIRED_CASE_STEPS_ACTUALLY_COMPLETE_ALREADY_SOLVED_CLOSED','case_percent':100,'findings_MAIN_acceptance_pending':False,'findings_checkpoint_MAIN':p['commit'],'MAIN_window_owner':'ROOT until immediate explicit return'})
 save(A/'CURRENT_CASE_STATUS.json',status)
 with (A/'RESEARCH_LOG.md').open('a') as h:h.write('\n\n'+now+' — Actual scoped findings accepted at '+p['commit']+' tree'+p['tree']+', sole parent'+p['expected_main']+'. Full selected bytehash/blob scope and four fresh own target/programme readbacks passed. PR154 closed unmerged original HEAD unchanged. Case100%, programme30/dated99=30.30%,17published. No new paper/DOI/tracker or local Git index/ref mutation. Writer return follows immediately.\n')
 print(json.dumps(rec,indent=2))
if __name__=='__main__':main()

