"""Push only PR57 public audit evidence and its fresh status-only successor intake."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]; P=R/'draft_pr_publication_program_20260930'; O=A/'ordered_publication_operations_20261004'; C=A.parent/'pr45_9900007'
D=F/'private/completion_commit'; D.mkdir(parents=True); (D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes()); commands=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def run(*parts):
    argv=['git','--no-optional-locks',*parts]; start=dt.datetime.now(dt.timezone.utc).isoformat(); child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE); out,err=child.communicate()
    n=len(commands)+1; (D/(str(n)+'.stdout')).write_bytes(out); (D/(str(n)+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)}); (D/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n'); assert child.returncode==0; return out
def names(body): return {s.decode() for s in body.split(b'\0') if s}
def pin(name):
    p=R/name
    if not p.exists(): return {'absent':True}
    assert p.is_file() and not p.is_symlink(); body=p.read_bytes(); return {'bytes':len(body),'sha256':sha(body),'mode':stat.S_IMODE(p.stat().st_mode)}
merge=load(O/'NATIVE_MERGE_RESULT.json'); native=load(O/'NATIVE_ACCEPTANCE_RESULT.json'); done=load(F/'FULLY_COMPLETED_PUBLISHED_RESULT.json'); intake=load(P/'ordered_intake_20261004/after_PR57/INTAKE_AFTER_PR57.json')
assert done['all_mathematical_package_priority_publication_tracker_and_native_steps_verified'] and not done['persistent_goal_complete'] and intake['next_eligible_PR']==65
assert run('branch','--show-current').strip()==b'main' and not run('diff','--cached','--name-only','-z')
base=run('rev-parse','HEAD').decode().strip(); assert base==native['acceptance_commit']==run('ls-remote','--heads','origin','main').decode().split()[0]
window_path=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'; window_body=window_path.read_bytes()
def check_window():
    w=load(window_path); assert window_path.read_bytes()==window_body and w['shared_git_writes_paused'] is True and w['paused_for'].startswith('PR57 ordered publication native integration')
    assert w['local_main_at_pause']==w['remote_main_at_pause']==merge['base'] and w['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True and w['all_staged_path_count']==0 and not w['owned_staged_paths']; return w
w=check_window(); assert run('show','-s','--format=%P',base).decode().strip()==merge['merge_commit']
roots=[A,P/'CURRENT_PROGRESS.json',P/'ordered_intake_20261004/after_PR57',P/'ordered_intake_20261004/STATUS_CHECKPOINT_RECEIPT.json']
for folder in sorted(C.glob('root_pr57*')):
    if (folder/'CAPTURE.json').is_file():
        rec=load(folder/'CAPTURE.json'); assert rec['schema']=='root-explicit-command-capture/v1' and rec['completed'] is True; roots.append(folder)
for folder in [C/'root_ordered_intake_status_push_20261004_actual_capture',C/'root_ordered_intake_after_PR57_20261004_actual_capture']:
    assert load(folder/'CAPTURE.json')['completed'] is True; roots.append(folder)
relative=[p.relative_to(R).as_posix() for p in roots]
selected=names(run('diff','--name-only','-z','--',*relative))|names(run('ls-files','--others','--exclude-standard','-z','--',*relative))
selected={n for n in selected if not any(part in Path(n).parts for part in ['private','private_primary_reading_cache','generated_gws_reference','tracker','fresh_tracker_readback','__pycache__']) and not n.endswith(('.png','.log','.pyc'))}
assert selected and all(any(n==root or n.startswith(root+'/') for root in relative) for n in selected)
assert not any('SHARED_GIT_WINDOW_STATUS' in n or 'draft_pr_descending' in n for n in selected)
foreign={n:pin(n) for n in names(run('diff','--name-only','-z'))-selected}; owned={n:pin(n) for n in sorted(selected)}; assert all(not x.get('absent') for x in owned.values())
plan={'schema':'pr57-publication-completion-scoped-checkpoint-plan/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'parent':base,'owned':owned,'foreign':foreign,'acknowledged_window':w,'published_DOI':done['DOI'],'verified_tracker_range':done['tracker_range'],'next_eligible_PR':65,'excluded_58_64_processed':False,'PR57_workflow_percent':100,'dated_completed_program_fraction_percent':6/99*100,'persistent_goal_complete':False,'private_primary_service_or_generated_cache_files_kept_local':True}
planpath=F/'COMPLETION_CHECKPOINT_PLAN.json'
with planpath.open('x') as f: json.dump(plan,f,indent=2); f.write('\n')
n=planpath.relative_to(R).as_posix(); selected.add(n); owned[n]=pin(n)
def preserve():
    check_window(); assert names(run('diff','--name-only','-z'))-selected==set(foreign)
    for n,p in foreign.items(): assert pin(n)==p
    for n,p in owned.items(): assert pin(n)==p
preserve(); run('add','--',*sorted(selected)); assert names(run('diff','--cached','--name-only','-z'))==selected
for n,p in owned.items(): assert sha(run('show',':'+n))==p['sha256']
preserve(); run('commit','-m','Complete PR57 reviewed publication DOI tracker and exact acceptance audit')
commit=run('rev-parse','HEAD').decode().strip(); assert run('show','-s','--format=%P',commit).decode().strip()==base and names(run('diff-tree','--no-commit-id','--name-only','-r','-z',commit))==selected
assert run('ls-remote','--heads','origin','main').decode().split()[0]==base
preserve(); run('push','origin','main'); assert run('ls-remote','--heads','origin','main').decode().split()[0]==commit and not run('diff','--cached','--name-only','-z'); preserve()
receipt={'schema':'pr57-published-completion-scoped-push/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'commit':commit,'parent':base,'remote_main':commit,'committed_owned_paths':len(selected),'foreign_preserved_paths':len(foreign),'index_empty':True,'PR57_complete':True,'DOI':done['DOI'],'tracker_range':done['tracker_range'],'next_eligible_PR':65,'PR57_workflow_percent':100,'dated_completed_program_fraction_percent':6/99*100,'new_central_proof_attempts':0,'persistent_goal_complete':False,'postpush_receipt_not_embedded_in_its_own_containing_commit':True}
with (F/'COMPLETION_CHECKPOINT_RECEIPT.json').open('x') as f: json.dump(receipt,f,indent=2); f.write('\n')
print(json.dumps(receipt,indent=2))
