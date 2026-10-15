"""Commit only status intake/cursor correction and genuine late55 receipts."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

F=Path(__file__).resolve().parent; P=F.parent; R=P.parent
C=P/'audits/pr45_9900007'; A55=P/'audits/pr55_30006309/root_goal_resumption_20261004'
private=F/'private/status-checkpoint'; private.mkdir(parents=True)
(private/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def run(*parts):
    argv=['git','--no-optional-locks',*parts]; start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(); n=len(commands)+1
    (private/(str(n)+'.stdout')).write_bytes(out); (private/(str(n)+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
                     'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
    (private/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    assert child.returncode==0
    return out
def paths(b): return {x.decode() for x in b.split(b'\0') if x}
def pin(n):
    p=R/n
    assert p.is_file() and not p.is_symlink()
    b=p.read_bytes(); return {'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
intake=json.loads((F/'INTAKE_56_57.json').read_bytes())
assert intake['next_eligible_PR']==57 and intake['PR56_science_processed'] is False
receipt55=json.loads((A55/'COMPLETION_CHECKPOINT_RECEIPT.json').read_bytes())
assert receipt55['commit']=='c5d5f778f07c0c17d3dd65a7729ed95d253ed309'
assert run('branch','--show-current').strip()==b'main' and not run('diff','--cached','--name-only','-z')
base=run('rev-parse','HEAD').decode().strip()
assert base==receipt55['commit']==run('ls-remote','--heads','origin','main').decode().split()[0]
window=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
def window_check():
    w=json.loads(window.read_bytes())
    assert w['shared_git_writes_paused'] is True and 'follow-up literal-status intake' in w['paused_for']
    assert w['local_main_at_pause']==w['remote_main_at_pause']==base
    assert w['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True and w['all_staged_path_count']==0
    return w
w=window_check()
progress=json.loads((P/'CURRENT_PROGRESS.json').read_bytes())
assert progress['current_PR']==57 and progress['fully_completed_eligible_PRs']==[9,16,18,50,55]
progress['last_completed_scientific_disposition_record']=progress['last_completed_record']
progress['last_completed_record']='audits/pr55_30006309/root_goal_resumption_20261004/COMPLETION_CHECKPOINT_RECEIPT.json'
progress['last_completed_final_audit_checkpoint_commit']=receipt55['commit']
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
roots=[F,P/'CURRENT_PROGRESS.json',A55/'COMPLETION_CHECKPOINT_RECEIPT.json',
       C/'root_pr55_completion_scoped_push_20261004_actual_capture',C/'root_ordered_intake_56_57_20261004_actual_capture']
relative=[p.relative_to(R).as_posix() for p in roots]
selected=paths(run('diff','--name-only','-z','--',*relative))|paths(run('ls-files','--others','--exclude-standard','-z','--',*relative))
selected={n for n in selected if 'private' not in Path(n).parts}
assert selected and all(any(n==s or n.startswith(s+'/') for s in relative) for n in selected)
foreign={n:pin(n) for n in paths(run('diff','--name-only','-z'))-selected}
owned={n:pin(n) for n in selected}
plan={'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'parent':base,'owned':owned,'foreign':foreign,'actual_window':w,
      'status_only':True,'next_eligible_PR':57,'PR56_science_processed':False,'new_central_proof_attempts':0,
      'dated_completed_program_fraction_percent':5/99*100,'goal_complete':False}
plan_path=F/'STATUS_CHECKPOINT_PLAN.json'
with plan_path.open('x') as out: json.dump(plan,out,indent=2);out.write('\n')
n=plan_path.relative_to(R).as_posix(); selected.add(n); owned[n]=pin(n)
def preserve():
    window_check()
    assert paths(run('diff','--name-only','-z'))-selected==set(foreign)
    for n,b in foreign.items(): assert pin(n)==b
    for n,b in owned.items(): assert pin(n)==b
preserve(); run('add','--',*sorted(selected))
assert paths(run('diff','--cached','--name-only','-z'))==selected
for n,b in owned.items(): assert sha(run('show',':'+n))==b['sha256']
preserve(); run('commit','-m','Skip nonclaimed PR56 and bind ordered claimed-solved intake to PR57')
commit=run('rev-parse','HEAD').decode().strip()
assert run('show','-s','--format=%P',commit).decode().strip()==base
assert paths(run('diff-tree','--no-commit-id','--name-only','-r','-z',commit))==selected
preserve(); run('push','origin','main')
assert run('ls-remote','--heads','origin','main').decode().split()[0]==commit
assert not run('diff','--cached','--name-only','-z'); preserve()
receipt={'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'commit':commit,'parent':base,'remote_main':commit,
         'owned_paths':len(selected),'foreign_preserved_paths':len(foreign),'index_empty':True,'next_eligible_PR':57,
         'PR56_science_processed':False,'goal_complete':False,'new_central_proof_attempts':0,
         'postpush_receipt_not_embedded_in_its_own_containing_commit':True}
with (F/'STATUS_CHECKPOINT_RECEIPT.json').open('x') as out: json.dump(receipt,out,indent=2);out.write('\n')
print(json.dumps(receipt,indent=2))
