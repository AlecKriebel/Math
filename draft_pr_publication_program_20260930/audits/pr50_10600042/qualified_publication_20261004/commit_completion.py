"""Scoped PR50 completion checkpoint; preserve every foreign body and index entry."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

Q=Path(__file__).resolve().parent; A=Q.parent; P=A.parents[1]; R=P.parent
O=A/'qualified_publication_operations_20261004'; C=A.parent/'pr45_9900007'
private=O/'private/completion-commit'; private.mkdir()
(private/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands=[]
def run(*parts):
    argv=['git','--no-optional-locks',*parts]; start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(); n=len(commands)+1
    (private/(str(n)+'.stdout')).write_bytes(out); (private/(str(n)+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_utc':start,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,
       'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    (private/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    assert child.returncode==0
    return out
def paths(body): return {x.decode() for x in body.split(b'\0') if x}
def pin(name):
    p=R/name
    if not p.exists(): return {'absent':True}
    assert p.is_file() and not p.is_symlink()
    b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
merge=json.loads((O/'NATIVE_MERGE_RESULT.json').read_bytes()); mirror=json.loads((O/'NATIVE_ACCEPTANCE_RESULT.json').read_bytes())
done=json.loads((Q/'FULLY_COMPLETED_AND_RECONCILED.json').read_bytes())
assert done['all_required_PR50_steps_complete_under_explicit_human_exception'] is True and done['persistent_goal_complete'] is False
assert run('branch','--show-current').strip()==b'main' and not run('diff','--cached','--name-only','-z')
base=run('rev-parse','HEAD').decode().strip()
assert base==mirror['acceptance_commit']==run('ls-remote','--heads','origin','main').decode().split()[0]
window_path=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
def window_check():
    w=json.loads(window_path.read_bytes())
    assert w['shared_git_writes_paused'] is True and 'PR50' in w['paused_for']
    assert w['local_main_at_pause']==w['remote_main_at_pause']==merge['base']
    return w
w=window_check()
assert run('show','-s','--format=%P',mirror['acceptance_commit']).decode().strip()==merge['merge_commit']
assert run('show','-s','--format=%P',merge['merge_commit']).decode().strip().split()==[merge['base'],done['reviewed_head']]
roots=[Q,A/'qualified_round1_adversary_20261004',A/'qualified_round2_adversary_20261004',O,P/'CURRENT_PROGRESS.json']
for capture in sorted(C.glob('root_pr50_qualified_*_20261004_actual_capture')):
    evidence=capture/'CAPTURE.json'
    if evidence.exists():
        record=json.loads(evidence.read_bytes())
        if record['status']=='PASS' and record['completed'] is True: roots.append(capture)
relative=[p.relative_to(R).as_posix() for p in roots]
selected=paths(run('diff','--name-only','-z','--',*relative))|paths(run('ls-files','--others','--exclude-standard','-z','--',*relative))
selected={n for n in selected if 'private' not in Path(n).parts and 'generated_cli' not in Path(n).parts and not n.endswith(('.png','.log','.pyc')) and not n.endswith('git_commands.jsonl')}
assert selected and all(any(n==root or n.startswith(root+'/') for root in relative) for n in selected)
foreign={n:pin(n) for n in paths(run('diff','--name-only','-z'))-selected}
owned={n:pin(n) for n in sorted(selected)}; assert all(not x.get('absent') for x in owned.values())
plan={'schema':'pr50-qualified-completion-scoped-commit-plan/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'parent':base,'owned':owned,'foreign':foreign,
  'acknowledged_window':w,'PR50_complete':True,'priority_clearance':False,'program_percent':4.040404}
plan_path=Q/'COMPLETION_CHECKPOINT_PLAN.json'
with plan_path.open('x') as f:json.dump(plan,f,indent=2);f.write('\n')
name=plan_path.relative_to(R).as_posix();selected.add(name);owned[name]=pin(name)
def preserve():
    window_check()
    for n,b in foreign.items(): assert pin(n)==b
    for n,b in owned.items(): assert pin(n)==b
preserve();run('add','--',*sorted(selected))
assert paths(run('diff','--cached','--name-only','-z'))==selected
for n,b in owned.items(): assert hashlib.sha256(run('show',':'+n)).hexdigest()==b['sha256']
preserve();run('commit','-m','Complete PR50 qualified publication, clean reviews and verified registration')
commit=run('rev-parse','HEAD').decode().strip()
assert run('show','-s','--format=%P',commit).decode().strip()==base
assert paths(run('diff-tree','--no-commit-id','--name-only','-r','-z',commit))==selected
assert run('ls-remote','--heads','origin','main').decode().split()[0]==base
preserve();run('push','origin','main')
assert run('ls-remote','--heads','origin','main').decode().split()[0]==commit
assert not run('diff','--cached','--name-only','-z');preserve()
receipt={'schema':'pr50-qualified-completion-scoped-push/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
 'commit':commit,'parent':base,'remote_main':commit,'committed_owned_paths':len(selected),'foreign_preserved_paths':len(foreign),
 'index_empty':True,'publication_and_registration_and_merge_complete':True,'DOI':done['DOI'],'tracker_range':done['tracker_range'],
 'historical_priority_certified':False,'new_central_proof_attempts':0,'PR50_percent':100,'dated_program_percent':4.040404,'persistent_goal_complete':False,
 'postpush_receipt_not_embedded_in_its_own_containing_commit':True}
with (Q/'COMPLETION_CHECKPOINT_RECEIPT.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt,indent=2))
