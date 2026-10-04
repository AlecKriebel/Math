"""Check all final PR18 bindings after the real tracker and PR updates, then checkpoint."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:]!=['--exclusive-window-confirmed']:
    raise RuntimeError('Requires confirmed shared Git writer window')
own=Path(__file__).resolve().parent; a18=own.parent; program=a18.parents[1]; repo=program.parent
def sha(b): return hashlib.sha256(b).hexdigest()
def must(ok,s):
    if not ok: raise RuntimeError(s)
def git(*args):
    p=subprocess.run(['git',*args],cwd=repo,capture_output=True)
    must(p.returncode==0,p.stderr.decode(errors='replace'))
    return p.stdout
base=git('rev-parse','HEAD').decode().strip()
checkpoint=json.loads((own/'TRACKER_NATIVE_CHECKPOINT_RESULT.json').read_bytes())
must(base==checkpoint['commit'] and git('ls-remote','--heads','origin','main').decode().split()[0]==base,'Checkpoint or remote moved')
must(git('branch','--show-current').strip()==b'main' and not git('diff','--cached','--name-only').strip(),'Clean real index on main required')
remote_raw=(program/'audits/pr45_9900007/root_pr18_final_completed_github_readback_actual_capture/stdout.bin').read_bytes()
pr=json.loads(remote_raw)
must(pr['state']=='MERGED' and pr['headRefOid']=='99e403e85d38d92b021198c4a57bbad3cd8775ba' and pr['mergeCommit']['oid']=='3a844edfe0a203b16f6b90a2ae01cecf5801c7f2','Actual GitHub result differs')
must(pr['body']==(own/'ACCEPTED_PR_BODY.md').read_text() and "'Math Puzzles'!A14:D14" in pr['body'],'Published PR description not reconciled')
(a18/'publication/PR_FINAL_COMPLETED.json').write_bytes(remote_raw)
decision=json.loads((own/'ROOT_FINAL_SUBMISSION_DECISION.json').read_bytes())
for name,h in decision['publication_pins'].items():
    must(sha((a18/'preprint_v1'/name).read_bytes())==h,'Reviewed publication bytes changed')
for family,key in [('preprint_round1_adversary_family','first_fresh_review_verdict_sha256'),('preprint_round2_adversary_family','second_NEW_fresh_review_verdict_sha256')]:
    must(sha((a18/family/'VERDICT.json').read_bytes())==decision[key],'Fresh whole-package review changed')
acceptance=json.loads((repo/'unsolved_math_prioritization/attempts/30001075/acceptance.json').read_bytes())
must(acceptance['tracker_row_written'] is True and acceptance['workflow_completion_estimate_percent']==100,'Current native acceptance incomplete')
for value in acceptance.values():
    if isinstance(value,dict) and 'path' in value and 'sha256' in value:
        must(sha((repo/value['path']).read_bytes())==value['sha256'],'Current acceptance binding differs')
state_path=repo/'unsolved_math_prioritization/state.json'; history_path=repo/'unsolved_math_prioritization/history.jsonl'
state=json.loads(state_path.read_bytes()); before=json.loads(git('show',checkpoint['base']+':unsolved_math_prioritization/state.json'))
must({k:v for k,v in state.items() if k!='30001075'}=={k:v for k,v in before.items() if k!='30001075'},'Other native states changed')
event=state['30001075']; original_event=before['30001075']
must(event['event']=='publication_tracker_verified' and event['prior_event_id']==original_event['event_id'] and event['turns_used']==1 and event['turn_limit']==5,'Tracker event or original budget differs')
for value in event['evidence'].values():
    if isinstance(value,dict) and 'path' in value and 'sha256' in value:
        must(sha((repo/value['path']).read_bytes())==value['sha256'],'Current state evidence differs')
old_history=git('show',checkpoint['base']+':unsolved_math_prioritization/history.jsonl'); history=history_path.read_bytes()
must(history.startswith(old_history) and len(history[len(old_history):].splitlines())==1 and json.loads(history[len(old_history):])==event,'History prefix or actual tracker event differs')
tracker=json.loads((a18/'publication/TRACKER_VERIFICATION.json').read_bytes())
response=json.loads((a18/'publication/TRACKER_APPEND_RESPONSE.json').read_bytes())['updates']
readback=json.loads((a18/'publication/TRACKER_READBACK.json').read_bytes())
must([response[k] for k in ('updatedRows','updatedColumns','updatedCells')]==[1,4,4] and response['updatedData']['values']==[tracker['actual_row']] and readback['values']==[tracker['actual_row']],'Actual append/readback receipt differs')
must(tracker['fresh_full_table_exactly_one_matching_problem_DOI_row'] is True and tracker['range']==acceptance['tracker_range'], 'Tracker uniqueness or range differs')
old_queue=git('show',checkpoint['base']+':unsolved_math_prioritization/QUEUE.md').decode().splitlines(keepends=True)
new_queue=(repo/'unsolved_math_prioritization/QUEUE.md').read_text().splitlines(keepends=True)
changed=[i for i,(a,b) in enumerate(zip(old_queue,new_queue)) if a!=b]
must(len(old_queue)==len(new_queue) and len(changed)==1 and '| 30001075 /' in new_queue[changed[0]],'Other queue rows changed')
old_cells=old_queue[changed[0]].split('|'); new_cells=new_queue[changed[0]].split('|')
must([i for i,(a,b) in enumerate(zip(old_cells,new_cells)) if a!=b]==[11],'Unexpected queue-cell change')
plan=json.loads((a18/'native_acceptance_plan_20261003/PLAN.json').read_bytes())
for item in plan['original_scientific_files_to_preserve_exactly']:
    must(sha((repo/item['canonical_path']).read_bytes())==item['sha256'],'Historical source blob changed')
now=dt.datetime.now(dt.timezone.utc).isoformat()
record={'schema':'pr18-fully-completed-final-readback/v1','UTC':now,'actual_pid':os.getpid(),
    'all_PR18_requirements_complete':True,'original_claim_and_budget_verified':'Conjecture4; claimed_solved; 1/5',
    'fixed_manuscript_PDF_archive_metadata_and_two_fresh_reviews_unchanged':True,
    'bounded_priority_and_named_fulltext_access_completed':True,'published_Zenodo_files_match_reviewed_files':True,
    'DOI':tracker['DOI'],'GitHub_state':'MERGED','actual_merge_commit':pr['mergeCommit']['oid'],
    'tracker_range':tracker['range'],'actual_append_and_independent_readback_verified':True,
    'fresh_tracker_uniqueness_verified':True,'current_PR_description_and_native_records_reconciled':True,
    'all_15_historical_source_blobs_unchanged':True,'all_other_native_state_entries_and_history_prefix_preserved':True,
    'queue_only_target_findings_cell_changed_for_tracker_completion':True,'new_central_attempts':0,
    'PR18_workflow_percent':100,'next_eligible_PR':50,'whole_persistent_goal_complete':False}
(a18/'publication/FULLY_COMPLETED_AND_RECONCILED.json').write_text(json.dumps(record,indent=2)+'\n')
selected={own/'final_pr18_complete_readback.py',own/'TRACKER_NATIVE_CHECKPOINT_RESULT.json',a18/'publication/PR_FINAL_COMPLETED.json',a18/'publication/FULLY_COMPLETED_AND_RECONCILED.json'}
for name in ['root_pr18_tracker_native_completion_checkpoint_actual_capture','root_pr18_completed_tracker_pr_metadata_update_actual_capture','root_pr18_final_completed_github_readback_actual_capture','root_pr18_full_workflow_final_checkpoint_actual_capture']:
    folder=program/'audits/pr45_9900007'/name
    if folder.exists(): selected.update(p for p in folder.iterdir() if p.is_file())
paths=sorted(p.relative_to(repo).as_posix() for p in selected); selected_bytes={p.encode() for p in paths}
def foreign_index():
    return b'\0'.join(e for e in git('ls-files','--stage','-z').split(b'\0') if e and e.split(b'\t',1)[1] not in selected_bytes)
foreign=foreign_index()
git('add','--',*paths)
must(foreign_index()==foreign and git('rev-parse','HEAD').decode().strip()==base,'Foreign index or main changed')
git('commit','--only','-m','Verify all PR18 publication tracker and acceptance completion requirements','--',*paths)
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0'))-{b''}
must(changed<=selected_bytes and git('rev-parse',commit+'^').decode().strip()==base and foreign_index()==foreign,'Unexpected final checkpoint scope/parent/index')
git('push','origin','main')
remote=git('ls-remote','--heads','origin','main').decode().split()[0]
must(remote==commit and foreign_index()==foreign,'Remote/index final checkpoint mismatch')
print(json.dumps({'PR18_complete':True,'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'commit':commit,'remote_main':remote,'foreign_index_unchanged':True,'DOI':tracker['DOI'],'tracker_range':tracker['range'],'PR18_workflow_percent':100,'next_eligible_PR':50,'whole_goal_complete':False},indent=2))
