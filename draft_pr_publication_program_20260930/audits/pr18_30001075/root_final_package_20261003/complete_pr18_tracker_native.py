"""Finish PR18's current native records using the actual verified tracker row."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:]!=['--exclusive-window-confirmed']:
    raise RuntimeError('Requires confirmed exclusive shared Git writer window')
own=Path(__file__).resolve().parent
a18=own.parent
program=a18.parents[1]
repo=program.parent
native=repo/'unsolved_math_prioritization'
canonical=native/'attempts/30001075'
def sha(body): return hashlib.sha256(body).hexdigest()
def git(*args):
    p=subprocess.run(['git',*args],cwd=repo,capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace'))
    return p.stdout
def must(ok,message):
    if not ok: raise RuntimeError(message)
def binding(p): return {'path':p.relative_to(repo).as_posix(),'sha256':sha(p.read_bytes())}
must(git('branch','--show-current').strip()==b'main' and not git('diff','--cached','--name-only').strip(),'Requires clean real index on main; preserve foreign staging')
base=git('rev-parse','HEAD').decode().strip()
must(git('ls-remote','--heads','origin','main').decode().split()[0]==base,'Local/remote main differ')
tracker_path=a18/'publication/TRACKER_VERIFICATION.json'
tracker=json.loads(tracker_path.read_bytes())
must(tracker['append_performed'] is True and tracker['independent_readback_exact'] is True and tracker['fresh_full_table_exactly_one_matching_problem_DOI_row'] is True,'Actual tracker completion has not passed')
must(tracker['DOI']=='10.5281/zenodo.23127955' and tracker['range']=="'Math Puzzles'!A14:D14",'Tracker identity differs')
acceptance_path=canonical/'acceptance.json'
old_acceptance=acceptance_path.read_bytes()
acceptance=json.loads(old_acceptance)
must(acceptance['tracker_row_written'] is False and acceptance['merge_commit']=='3a844edfe0a203b16f6b90a2ae01cecf5801c7f2','Unexpected previous acceptance')
for value in acceptance.values():
    if isinstance(value,dict) and 'path' in value and 'sha256' in value:
        must(sha((repo/value['path']).read_bytes())==value['sha256'],'Accepted scientific/publication/review evidence drifted')
state_path=native/'state.json'; history_path=native/'history.jsonl'
state_bytes=state_path.read_bytes(); history_before=history_path.read_bytes()
must(state_bytes==git('show',base+':unsolved_math_prioritization/state.json') and history_before==git('show',base+':unsolved_math_prioritization/history.jsonl'),'Foreign native edits present')
state=json.loads(state_bytes); old_event=state['30001075']
must(old_event['event']=='acceptance_mirror_import' and old_event['turns_used']==1 and old_event['turn_limit']==5,'Unexpected native event/budget')
must(old_event['evidence']['canonical_acceptance']['sha256']==sha(old_acceptance),'Previous acceptance hash drifted')
now=dt.datetime.now(dt.timezone.utc).isoformat()
archive=a18/'publication/ACCEPTANCE_BEFORE_TRACKER_COMPLETION.json'
must(not archive.exists(),'Do not overwrite earlier acceptance snapshot')
archive.write_bytes(old_acceptance)
acceptance.update({'current_updated_at':now,'tracker_range':tracker['range'],'tracker_row_written':True,
    'tracker_status':'Google Workspace CLI append and independent four-cell readback verified; fresh full-table uniqueness check passed.',
    'tracker_verified_utc':tracker['UTC'],'tracker_verification':binding(tracker_path),
    'previous_acceptance_version':binding(archive),'previous_acceptance_git_version':'0269cf076c461bdf28b963258d3cb8727c2f66e0',
    'workflow_completion_estimate_percent':100})
acceptance_path.write_text(json.dumps(acceptance,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
event=dict(old_event)
event.update({'at':now,'event':'publication_tracker_verified','prior_event_id':old_event['event_id'],
    'note':'Actual present-day tracker completion after human Google reauthentication; original acceptance and historical lifecycle remain preserved.',
    'tracker_range':tracker['range'],'tracker_row_written':True,'workflow_completion_estimate_percent':100})
event.pop('event_id')
event['evidence']=dict(old_event['evidence'])
event['evidence'].update({'canonical_acceptance':binding(acceptance_path),'tracker_verification':binding(tracker_path),
    'previous_acceptance_version':binding(archive),'tracker_row_written':True})
event['event_id']=sha(json.dumps(event,sort_keys=True).encode())
state['30001075']=event
state_path.write_text(json.dumps(state,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
history_path.write_bytes(history_before+json.dumps(event,ensure_ascii=False,sort_keys=True).encode()+b'\n')
must({k:v for k,v in json.loads(state_path.read_bytes()).items() if k!='30001075'}=={k:v for k,v in json.loads(state_bytes).items() if k!='30001075'},'Foreign state entries changed')
must(history_path.read_bytes().startswith(history_before) and len(history_path.read_bytes().splitlines())==len(history_before.splitlines())+1,'History prefix or update count changed')
current_path=canonical/'CURRENT_RESULT.md'; current=current_path.read_text()
must(current.count('The Google tracker row remains pending credential reconnection.')==1,'Current tracker sentence differs')
current=current.replace('The Google tracker row remains pending credential reconnection.',f'The Google tracker row is verified at `{tracker["range"]}` after an actual Google Workspace CLI append, independent four-cell readback and fresh full-table uniqueness check.')
current=current.replace('The state and history record one current acceptance mirror; no historical lifecycle transitions are reconstructed.','The state and history preserve the original present-day acceptance mirror and append one actual tracker-completion event; no historical lifecycle transitions are reconstructed. Historical acceptance hashes bind their dated version, preserved in the audit archive and Git history. The PR18 workflow is complete.')
current_path.write_text(current)
queue_path=native/'QUEUE.md'; queue_before=queue_path.read_bytes()
must(queue_before==git('show',base+':unsolved_math_prioritization/QUEUE.md'),'Foreign queue edits present')
lines=queue_before.decode().splitlines(keepends=True)
indexes=[i for i,line in enumerate(lines) if '| 30001075 /' in line]
must(len(indexes)==1,'Native queue identity not unique')
i=indexes[0]; cells=lines[i].split('|')
must(cells[8].strip()=='preprint_published' and cells[9].strip()=='1/5' and cells[12].strip()==tracker['DOI'],'Native queue status/budget/DOI differs')
must(cells[11].count('tracker pending')==1,'Expected pending tracker note absent')
cells[11]=cells[11].replace('tracker pending','tracker verified at Math Puzzles row14')
lines[i]='|'.join(cells); queue_path.write_text(''.join(lines))
plan=json.loads((a18/'native_acceptance_plan_20261003/PLAN.json').read_bytes())
for item in plan['original_scientific_files_to_preserve_exactly']:
    must(sha((repo/item['canonical_path']).read_bytes())==item['sha256'],'Original scientific source file changed')
body_path=own/'ACCEPTED_PR_BODY.md'; body=body_path.read_text()
must(body.count('The Google tracker entry is pending credential reconnection and is not represented as written.')==1,'PR body pending sentence differs')
body_path.write_text(body.replace('The Google tracker entry is pending credential reconnection and is not represented as written.',f'The Google Workspace CLI appended the publication tracker entry at `{tracker["range"]}`; an independent readback and fresh full-table check verified the four cells and exactly one matching problem/DOI row.'))
readme_path=program/'README.md'; readme=readme_path.read_text()
old='Current checkpoint: PR9 and PR16 completed publication, tracker and merge. PR18\nhas completed rigorous review, the full named 2024 source check, two fresh\nwhole-package reviews, publication at DOI `10.5281/zenodo.23127955`, exact public\nfile readbacks, merge and native acceptance. Its tracker entry remains pending\nGoogle CLI credential reconnection. PR18 workflow estimate: 98%. Do not advance\nto PR50 until that entry is independently verified. See `CURRENT_PROGRESS.json`.'
must(readme.count(old)==1,'Program current checkpoint paragraph differs')
readme_path.write_text(readme.replace(old,'Current checkpoint: PR9, PR16 and PR18 have completed publication, tracker and\nmerge. PR18 completed rigorous review, the full named 2024 source check, two\nfresh whole-package reviews, publication at DOI `10.5281/zenodo.23127955`, exact\npublic file readbacks, merge and native acceptance. Its Google Workspace CLI\ntracker entry is independently verified at `Math Puzzles!A14:D14`. PR18 workflow\nestimate: 100%. The next eligible PR is PR50. See `CURRENT_PROGRESS.json`.'))
progress_path=program/'CURRENT_PROGRESS.json'; progress=json.loads(progress_path.read_bytes())
progress.update({'UTC':now,'fully_completed_eligible_PRs':[9,16,18],
    'published_and_merged_but_tracker_pending':[],'fully_completed_count':3,
    'fully_completed_fraction_percent':round(300/99,6),'workflow_estimate_percent':round(300/99,6),
    'workflow_estimate_definition':'Three completed eligible workflows divided by the dated99-PR eligibility census; refresh eligibility before claiming whole-program completion.',
    'last_completed_PR':18,'last_completed_PR_workflow_percent':100,
    'last_completed_DOI':tracker['DOI'],'last_completed_merge_commit':acceptance['merge_commit'],
    'last_completed_tracker_range':tracker['range'],'current_PR':50,'current_PR_workflow_percent':0,
    'current_DOI':None,'current_merge_commit':None,'remaining_current_step':'Fresh eligibility and exact-head audit of PR50; only claimed_solved PRs are processed.',
    'advance_to_next_PR_authorized_now':True,'persistent_goal_complete':False})
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
record={'schema':'pr18-full-workflow-completion/v1','UTC':now,'actual_author_pid':os.getpid(),
    'PR':18,'reviewed_head':acceptance['reviewed_head'],'merge_commit':acceptance['merge_commit'],
    'DOI':tracker['DOI'],'tracker_range':tracker['range'],'tracker_verification':binding(tracker_path),
    'all_scientific_publication_review_bindings_unchanged':True,'original_budget':'1/5','new_central_attempts':0,
    'history_update':'One actual publication_tracker_verified event; entire prior prefix preserved',
    'foreign_native_state_entries_unchanged':True,'PR18_workflow_percent':100,
    'current_native_acceptance':binding(acceptance_path),'next_eligible_PR':50,
    'whole_program_complete':False,'PR_metadata_update_and_final_remote_checkpoint_readback_pending':True}
completion=a18/'publication/WORKFLOW_COMPLETION.json'
must(not completion.exists(),'Do not overwrite a previous completion record')
completion.write_text(json.dumps(record,indent=2)+'\n')
entry=f'\n## {now} — PR18 tracker verified; workflow100%\n\nHuman completed the Google CLI reauthentication. One guarded append placed the exact DOI and paper details at {tracker["range"]}; independent four-cell readback and a fresh full-table uniqueness check passed. The previous malformed read request was repaired before any write. Current native acceptance, queue, state/history and PR body are reconciled; historical pending-auth observations remain dated evidence. Original 1/5 and all scientific/publication bytes remain unchanged. PR18 workflow estimate100%; three eligible workflows completed in the dated99-PR census (3.0303%). Next eligible PR50 after final metadata/checkpoint readback. Whole goal remains unfinished.\n'
for log in [program/'RESEARCH_LOG.md',a18/'RESEARCH_LOG.md']:
    with log.open('a') as f: f.write(entry)
selected={acceptance_path,state_path,history_path,current_path,queue_path,body_path,readme_path,progress_path,program/'RESEARCH_LOG.md',a18/'RESEARCH_LOG.md'}
selected.update(p for p in (a18/'publication').iterdir() if p.is_file())
selected.add(a18/'publication/tracker_private/.gitignore')
selected.update(p for p in own.iterdir() if p.is_file() and p.name!='TRACKER_NATIVE_CHECKPOINT_RESULT.json')
for folder in (program/'audits/pr45_9900007').glob('root_pr18_*_actual_capture'):
    selected.update(p for p in folder.iterdir() if p.is_file())
paths=sorted(p.relative_to(repo).as_posix() for p in selected)
path_bytes={p.encode() for p in paths}; pins={p:sha((repo/p).read_bytes()) for p in paths}
def foreign_index():
    return b'\0'.join(e for e in git('ls-files','--stage','-z').split(b'\0') if e and e.split(b'\t',1)[1] not in path_bytes)
foreign=foreign_index()
must(git('rev-parse','HEAD').decode().strip()==base,'Main moved during preparation')
git('add','--',*paths)
must(foreign_index()==foreign,'Foreign index changed')
git('commit','--only','-m','Complete PR18 verified Google tracker and reconcile acceptance records','--',*paths)
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0'))-{b''}
must(changed<=path_bytes and git('rev-parse',commit+'^').decode().strip()==base,'Unexpected checkpoint scope/parent')
must(foreign_index()==foreign and all(sha((repo/p).read_bytes())==pin for p,pin in pins.items()),'Foreign index or selected file drift')
git('push','origin','main')
remote=git('ls-remote','--heads','origin','main').decode().split()[0]
must(remote==commit and foreign_index()==foreign,'Remote/index readback mismatch')
result={'schema':'pr18-tracker-native-checkpoint/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
    'actual_pid':os.getpid(),'base':base,'commit':commit,'remote_main':remote,
    'tracker_range':tracker['range'],'DOI':tracker['DOI'],'foreign_index_unchanged':True,
    'PR18_workflow_percent':100,'PR_metadata_update_and_final_remote_readback_pending':True}
(own/'TRACKER_NATIVE_CHECKPOINT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
