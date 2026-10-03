"""Independently reconcile PR18 native acceptance and checkpoint the pending tracker handoff."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:] != ['--exclusive-window-confirmed']:
    raise RuntimeError('Confirmed shared Git writer window required')
own=Path(__file__).resolve().parent
a18=own.parent
program=a18.parents[1]
repo=program.parent
def sha(body): return hashlib.sha256(body).hexdigest()
def cmd(argv):
    proc=subprocess.run(argv,cwd=repo,capture_output=True)
    if proc.returncode: raise RuntimeError(proc.stderr.decode(errors='replace'))
    return proc.stdout
def git(*args): return cmd(['git',*args])
def must(condition,message):
    if not condition: raise RuntimeError(message)
base=git('rev-parse','HEAD').decode().strip()
acceptance_checkpoint=json.loads((own/'ACCEPTANCE_CHECKPOINT_RESULT.json').read_bytes())
must(base==acceptance_checkpoint['acceptance_commit'],'Main changed since acceptance checkpoint')
must(git('branch','--show-current').strip()==b'main' and not git('diff','--cached','--name-only').strip(),'Clean real index on main required')
must(git('ls-remote','--heads','origin','main').decode().split()[0]==base,'Remote main differs')
pr_bytes=cmd(['gh','pr','view','18','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,title,url,mergedAt,mergeCommit'])
pr=json.loads(pr_bytes)
merge=json.loads((own/'NATIVE_MERGE_RESULT.json').read_bytes())
must(pr['state']=='MERGED' and pr['mergeCommit']['oid']==merge['merge_commit'] and pr['headRefOid']==merge['submitted_head'],'Actual GitHub merged readback differs')
(own/'FINAL_GITHUB_READBACK.json').write_bytes(pr_bytes)
canonical=repo/'unsolved_math_prioritization/attempts/30001075'
acceptance=json.loads((canonical/'acceptance.json').read_bytes())
for value in acceptance.values():
    if isinstance(value,dict) and 'path' in value and 'sha256' in value:
        must(sha((repo/value['path']).read_bytes())==value['sha256'],'Acceptance evidence binding changed')
plan=json.loads((a18/'native_acceptance_plan_20261003/PLAN.json').read_bytes())
for item in plan['original_scientific_files_to_preserve_exactly']:
    name=item['canonical_path']
    must(sha((repo/name).read_bytes())==item['sha256'] and sha(git('show',base+':'+name))==item['sha256'],'Original canonical file differs from frozen head')
native=repo/'unsolved_math_prioritization'
old_state=json.loads(git('show',merge['base']+':unsolved_math_prioritization/state.json'))
state=json.loads((native/'state.json').read_bytes())
must({k:v for k,v in state.items() if k!='30001075'}==old_state,'Foreign native state entry changed')
event=state['30001075']
must(event['turns_used']==1 and event['turn_limit']==5 and event['status']=='preprint_published' and event['doi']==acceptance['doi'],'Current state or original budget differs')
event_copy=dict(event); event_id=event_copy.pop('event_id')
must(sha(json.dumps(event_copy,sort_keys=True).encode())==event_id,'Acceptance event ID differs')
for value in event['evidence'].values():
    if isinstance(value,dict) and 'path' in value and 'sha256' in value:
        must(sha((repo/value['path']).read_bytes())==value['sha256'],'Native event evidence changed')
history=(native/'history.jsonl').read_bytes()
old_history=git('show',merge['base']+':unsolved_math_prioritization/history.jsonl')
must(history.startswith(old_history),'Historical event prefix changed')
suffix=history[len(old_history):].splitlines()
must(len(suffix)==1 and json.loads(suffix[0])==event,'History must append exactly the current mirror')
old_q=git('show',merge['base']+':unsolved_math_prioritization/QUEUE.md').decode().splitlines(keepends=True)
new_q=(native/'QUEUE.md').read_text().splitlines(keepends=True)
must(len(old_q)==len(new_q),'Queue row count changed')
changed=[i for i,(old,new) in enumerate(zip(old_q,new_q)) if old!=new]
must(len(changed)==1 and '| 30001075 /' in new_q[changed[0]],'Unrelated queue row changed')
old_cells=old_q[changed[0]].split('|'); new_cells=new_q[changed[0]].split('|')
must([i for i,(old,new) in enumerate(zip(old_cells,new_cells)) if old!=new]==[8,9,11,12],'Non-authorized target cells changed')
must(new_cells[8].strip()=='preprint_published' and new_cells[9].strip()=='1/5' and new_cells[12].strip()==acceptance['doi'],'Queue differs from published acceptance')
must(acceptance['tracker_row_written'] is False and acceptance['tracker_range'] is None,'Do not invent a tracker write')
notes_path=a18/'publication/TRACKER_NOTES.txt'
notes=notes_path.read_text().rstrip('\n')
row=['https://www.unsolvedmath.com/problems/OWR-2090-028','',acceptance['doi'],notes]
tracker={'schema':'pr18-intended-tracker-row/v1','status':'PREPARED_NOT_SENT_AUTH_RECONNECTION_REQUIRED',
    'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','sheet_id':1254632077,
    'historical_tab':'Math Puzzles','historical_headers':['Original Problem','Solution Chat URL','DOI','Notes'],
    'intended_values':row,'verified_problem_alias':'https://www.unsolvedmath.com/problems/30001075',
    'notes_sha256':sha(notes.encode()),'notes_file':notes_path.relative_to(repo).as_posix(),
    'before_any_append':'Resolve target sheet ID and exact headers live; read full values/formulas; reconcile problem/DOI duplicates; use existing one-shot append utility with persistent PR18 receipt directory; independently read back. Unknown write outcome requires live reconciliation, never blind retry.',
    'write_attempted':False}
(a18/'publication/INTENDED_TRACKER_ROW.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n')
now=dt.datetime.now(dt.timezone.utc).isoformat()
verification={'schema':'pr18-final-native-readback/v1','UTC':now,'actual_pid':os.getpid(),
    'current_remote_main':base,'merge_commit':merge['merge_commit'],'GitHub_state':'MERGED',
    'all_15_original_blob_hashes_checked':True,'accepted_publication_and_review_bindings_checked':True,
    'QUEUE_only_target_four_cells_changed':True,'all_other_native_state_entries_unchanged':True,
    'complete_history_prefix_unchanged':True,'exactly_one_current_mirror_event':True,
    'original_budget':'1/5','new_central_attempts':0,'DOI':acceptance['doi'],
    'tracker_row_written':False,'workflow_percent':98,'remaining_required_step':'Google CLI reauthentication, live guarded append and independent tracker readback'}
(own/'FINAL_NATIVE_VERIFICATION.json').write_text(json.dumps(verification,indent=2)+'\n')
progress={'schema':'claimed-solved-program-current-progress/v1','UTC':now,
    'authoritative_scope':'Persistent goal objective; only literal submitted/current claimed_solved PR heads; skip8 and all other statuses entirely.',
    'eligibility_census':'claimed_solved_scope_20261003/SCOPE_LEDGER.json','dated_eligible_total':99,
    'fully_completed_eligible_PRs':[9,16],'published_and_merged_but_tracker_pending':[18],
    'fully_completed_count':2,'fully_completed_fraction_percent':round(200/99,6),
    'workflow_estimate_percent':round(298/99,6),'workflow_estimate_definition':'Two completed eligible workflows plus PR18 at98%, divided by the dated99-PR eligibility census; subjective workflow estimate, not mathematical certainty.',
    'current_PR':18,'current_PR_workflow_percent':98,'current_DOI':acceptance['doi'],
    'current_merge_commit':merge['merge_commit'],'remaining_current_step':'Google tracker row; prior readonly GET failed401 expired/revoked credentials; human reconnect question pending.',
    'next_eligible_PR_after_current_completion':50,'advance_to_next_PR_authorized_now':False,
    'persistent_goal_complete':False}
(program/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
entry=f'\n## {now} — PR18 final native readback\n\nIndependent GitHub/main/evidence readback passed. Exactly the target four queue cells changed; all other state entries and the complete history prefix are preserved, with one present-day mirror and original 1/5. Current workflow estimate: 98%; two fully completed eligible PRs plus PR18 pending only the tracker, approximately3.01% weighted workflow across the dated99-PR eligible census. Scope remains claimed_solved only. No advancement beyond PR18 before the live tracker append/readback.\n'
for log in [program/'RESEARCH_LOG.md',a18/'RESEARCH_LOG.md']:
    with log.open('a') as f: f.write(entry)
selected={program/'README.md',program/'CURRENT_PROGRESS.json',program/'RESEARCH_LOG.md',a18/'RESEARCH_LOG.md'}
selected.update(p for p in (a18/'publication').iterdir() if p.is_file())
selected.update(p for p in own.iterdir() if p.is_file() and p.name!='FINAL_REPOSITORY_CHECKPOINT_RESULT.json')
for folder in (program/'audits/pr45_9900007').glob('root_pr18_*_actual_capture'):
    selected.update(p for p in folder.iterdir() if p.is_file())
paths=sorted(p.relative_to(repo).as_posix() for p in selected)
path_bytes={p.encode() for p in paths}
pins={p:sha((repo/p).read_bytes()) for p in paths}
def foreign_index():
    return b'\0'.join(e for e in git('ls-files','--stage','-z').split(b'\0') if e and e.split(b'\t',1)[1] not in path_bytes)
foreign=foreign_index()
must(git('rev-parse','HEAD').decode().strip()==base,'Main moved during final readback')
git('add','--',*paths)
must(foreign_index()==foreign,'Foreign index changed')
git('commit','--only','-m','Record PR18 final acceptance readback and pending tracker handoff','--',*paths)
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0'))-{b''}
must(changed<=path_bytes and git('rev-parse',commit+'^').decode().strip()==base,'Unexpected final checkpoint scope or parent')
must(foreign_index()==foreign and all(sha((repo/p).read_bytes())==pin for p,pin in pins.items()),'Foreign index or selected source drift')
git('push','origin','main')
remote_main=git('ls-remote','--heads','origin','main').decode().split()[0]
must(remote_main==commit and foreign_index()==foreign,'Final remote/index readback mismatch')
result={'schema':'pr18-final-repository-checkpoint/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
    'actual_pid':os.getpid(),'base':base,'commit':commit,'remote_main':remote_main,
    'foreign_index_unchanged':True,'DOI':acceptance['doi'],'GitHub_PR18':'MERGED',
    'tracker_row_written':False,'workflow_percent':98,'persistent_goal_complete':False}
(own/'FINAL_REPOSITORY_CHECKPOINT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
