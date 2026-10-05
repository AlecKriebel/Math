"""Commit/push only completed PR55 audits and late PR50 receipts on main."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

F=Path(__file__).resolve().parent; A=F.parent; P=A.parents[1]; R=P.parent
O=A/'partial_integration_operations_20261004'; C=A.parent/'pr45_9900007'
private=F/'private/completion-commit'; private.mkdir()
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
def paths(body): return {x.decode() for x in body.split(b'\0') if x}
def pin(name):
    p=R/name
    if not p.exists(): return {'absent':True}
    assert p.is_file() and not p.is_symlink()
    b=p.read_bytes(); return {'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
merge=json.loads((O/'NATIVE_MERGE_RESULT.json').read_bytes())
mirror=json.loads((O/'NATIVE_ACCEPTANCE_RESULT.json').read_bytes())
done=json.loads((F/'FULLY_COMPLETED_SCOPED_RESULT.json').read_bytes())
assert done['all_required_scoped_partial_outcome_steps_verified'] is True and done['persistent_goal_complete'] is False
assert done['full_source_solved'] is False and done['new_publication_DOI'] is None and done['tracker_row'] is False
assert run('branch','--show-current').strip()==b'main' and not run('diff','--cached','--name-only','-z')
base=run('rev-parse','HEAD').decode().strip()
assert base==mirror['acceptance_commit']==run('ls-remote','--heads','origin','main').decode().split()[0]
window_path=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
def window_check():
    w=json.loads(window_path.read_bytes())
    assert w['shared_git_writes_paused'] is True and 'PR55' in w['paused_for']
    assert w['local_main_at_pause']==w['remote_main_at_pause']==merge['base']
    assert w['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True
    assert w['all_staged_path_count']==0 and not w['owned_staged_paths']
    return w
w=window_check()
assert run('show','-s','--format=%P',base).decode().strip()==merge['merge_commit']
assert run('show','-s','--format=%P',merge['merge_commit']).decode().strip().split()==[merge['base'],done['reviewed_head']]
roots=[A,P/'CURRENT_PROGRESS.json']
late50=A.parent/'pr50_10600042/qualified_publication_20261004/COMPLETION_CHECKPOINT_RECEIPT.json'
if late50.exists(): roots.append(late50)
for capture in sorted(C.glob('root_pr55*')):
    evidence=capture/'CAPTURE.json'
    if evidence.is_file():
        record=json.loads(evidence.read_bytes())
        assert record['schema']=='root-explicit-command-capture/v1' and record['completed'] is True
        roots.append(capture)
late_capture=C/'root_pr50_qualified_completion_push_20261004_actual_capture'
if (late_capture/'CAPTURE.json').exists(): roots.append(late_capture)
relative=[p.relative_to(R).as_posix() for p in roots]
selected=paths(run('diff','--name-only','-z','--',*relative))|paths(run('ls-files','--others','--exclude-standard','-z','--',*relative))
selected={n for n in selected if 'private' not in Path(n).parts and '__pycache__' not in Path(n).parts
          and not n.endswith(('.png','.log','.pyc'))}
assert selected and all(any(n==root or n.startswith(root+'/') for root in relative) for n in selected)
assert not any('SHARED_GIT_WINDOW_STATUS' in n or 'draft_pr_descending' in n for n in selected)
foreign={n:pin(n) for n in paths(run('diff','--name-only','-z'))-selected}
owned={n:pin(n) for n in sorted(selected)}
assert all(not x.get('absent') for x in owned.values())
plan={'schema':'pr55-attributed-completion-scoped-commit-plan/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
      'parent':base,'owned':owned,'foreign':foreign,'acknowledged_window':w,
      'PR55_scoped_disposition_complete':True,'full_source_solved':False,'publication_count':4,'partial_acceptance_count':1,
      'dated_program_percent':5/99*100,'persistent_goal_complete':False}
plan_path=F/'COMPLETION_CHECKPOINT_PLAN.json'
with plan_path.open('x') as out: json.dump(plan,out,indent=2);out.write('\n')
name=plan_path.relative_to(R).as_posix(); selected.add(name); owned[name]=pin(name)
def preserve():
    window_check()
    assert paths(run('diff','--name-only','-z'))-selected==set(foreign)
    for n,b in foreign.items(): assert pin(n)==b
    for n,b in owned.items(): assert pin(n)==b
preserve(); run('add','--',*sorted(selected))
assert paths(run('diff','--cached','--name-only','-z'))==selected
for n,b in owned.items(): assert sha(run('show',':'+n))==b['sha256']
preserve(); run('commit','-m','Complete PR55 scoped prior-result audit and attributed partial acceptance')
commit=run('rev-parse','HEAD').decode().strip()
assert run('show','-s','--format=%P',commit).decode().strip()==base
assert paths(run('diff-tree','--no-commit-id','--name-only','-r','-z',commit))==selected
assert run('ls-remote','--heads','origin','main').decode().split()[0]==base
preserve(); run('push','origin','main')
assert run('ls-remote','--heads','origin','main').decode().split()[0]==commit
assert not run('diff','--cached','--name-only','-z'); preserve()
receipt={'schema':'pr55-attributed-completion-scoped-push/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
         'commit':commit,'parent':base,'remote_main':commit,'committed_owned_paths':len(selected),
         'foreign_preserved_paths':len(foreign),'index_empty':True,'PR55_scoped_disposition_complete':True,
         'full_source_solved':False,'new_paper':False,'new_publication_DOI':None,'tracker_row':False,
         'new_central_proof_attempts':0,'PR55_workflow_percent':100,'dated_program_percent':5/99*100,
         'persistent_goal_complete':False,'postpush_receipt_not_embedded_in_its_own_containing_commit':True}
with (F/'COMPLETION_CHECKPOINT_RECEIPT.json').open('x') as out: json.dump(receipt,out,indent=2);out.write('\n')
print(json.dumps(receipt,indent=2))
