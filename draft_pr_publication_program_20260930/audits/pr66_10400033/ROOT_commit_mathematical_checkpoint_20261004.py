"""Scoped math-audit checkpoint, only after the other writer's fresh pause."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess, sys

assert __debug__ and sys.flags.ignore_environment and sys.flags.dont_write_bytecode
A = Path(__file__).resolve().parent
P = A.parents[1]
R = P.parent
F = A/'mathematical_checkpoint_20261004'
D = F/'private_actual_git_commands'
assert not D.exists(), 'one-shot operator already used'
D.mkdir()
(D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands = []

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_bytes())
def require(c, message):
    if not c: raise RuntimeError(message)
def names(b): return {p.decode() for p in b.split(b'\0') if p}
def pin(name):
    p = R/name
    if not p.exists(): return {'absent':True}
    require(p.is_file() and not p.is_symlink(), 'path type: '+name)
    b = p.read_bytes()
    return {'bytes':len(b), 'sha256':sha(b), 'mode':stat.S_IMODE(p.stat().st_mode)}
def run(*args):
    argv = ['git','--no-optional-locks',*args]
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    proc = subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = proc.communicate()
    label = str(len(commands)+1)
    (D/(label+'.stdout')).write_bytes(out);(D/(label+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':proc.pid,'cwd':str(R),'start_utc':start,
                     'end_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':proc.returncode,
                     'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
    (D/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    require(proc.returncode==0,'Git command failure: '+err.decode(errors='replace'))
    return out

selection = read(F/'SELECTION.json')
window_path = R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
window_bytes = window_path.read_bytes()
def window():
    w = read(window_path)
    require(window_path.read_bytes()==window_bytes and w.get('shared_git_writes_paused') is True
            and w.get('paused_for')=='PR66 mathematical checkpoint 20261004'
            and w.get('dirty_tracked_bodies_modes_frozen_after_acknowledgement') is True
            and w.get('all_staged_path_count')==0 and not w.get('owned_staged_paths')
            and w.get('local_main_at_pause')==w.get('remote_main_at_pause')
            and dt.datetime.fromisoformat(w['utc'])>=dt.datetime.fromisoformat(selection['utc']),
            'Fresh exclusive writer acknowledgement missing or changed')
    return w
w = window()
require(run('branch','--show-current').strip()==b'main' and not run('diff','--cached','--name-only','-z'),'branch/index drift')
base = run('rev-parse','HEAD').decode().strip()
require(base==w['local_main_at_pause']==run('ls-remote','--heads','origin','main').decode().split()[0],'main/remote/ack drift')
gate = read(A/'ROOT_FULL_MATHEMATICAL_GATE_20261004.json')
require(gate['verdict']=='PASS_FULL_CLASSICAL_TARGET' and not gate['priority_clearance'] and not gate['merge_clearance'],'math-only gate drift')
require(read(A/'ROOT_completed_math_family_readback_20261004/READBACK.json')['status']=='PASS','family evidence custody drift')
progress = read(P/'CURRENT_PROGRESS.json')
require(progress['current_PR']==66 and progress['current_mathematical_audit_percent']==100
        and not progress['current_priority_clearance'] and not progress['current_publication_authorization']
        and not progress['persistent_goal_complete'],'progress drift')
for row in selection['files']:
    got = pin(row['path'])
    require(got.get('bytes')==row['bytes'] and got.get('sha256')==row['sha256'],'selection body drift: '+row['path'])
requested = [r['path'] for r in selection['files']] + [str((F/'SELECTION.json').relative_to(R)), str(Path(__file__).relative_to(R))]
selected = names(run('diff','--name-only','-z','--',*requested)) | names(run('ls-files','--others','--exclude-standard','-z','--',*requested))
require(selected and selected<=set(requested),'checkpoint scope mismatch')
require(all(not name.endswith(('.pdf','.png','.txt','.stdout','.stderr','.bin','.tex','.zip','.pyc'))
            and 'private_actual_git_commands' not in Path(name).parts for name in selected),'private scope violation')
owned = {name:pin(name) for name in sorted(selected)}
foreign = {name:pin(name) for name in names(run('diff','--name-only','-z'))-selected}
native = {name:pin(name) for name in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl']}
plan = {'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_controller_pid':os.getpid(),'base':base,
        'acknowledgement_sha256':sha(window_bytes),'owned':owned,'foreign':foreign,'native_to_preserve':native,
        'math_audit_percent':100,'priority_clearance':False,'publication':False,'merge':False,
        'full_local_manifests_do_not_assert_all_files_included_in_Git':True}
plan_path = F/'PLAN.json';plan_path.write_text(json.dumps(plan,indent=2)+'\n')
plan_name = str(plan_path.relative_to(R));selected.add(plan_name);owned[plan_name]=pin(plan_name)
def preserve():
    window()
    require(names(run('diff','--name-only','-z'))-selected==set(foreign),'foreign tracked path-set drift')
    for name,row in {**foreign,**owned,**native}.items():require(pin(name)==row,'body/mode drift: '+name)
preserve()
run('add','--',*sorted(selected))
require(names(run('diff','--cached','--name-only','-z'))==selected,'staged scope mismatch')
for name,row in owned.items():require(sha(run('show',':'+name))==row['sha256'],'index body drift: '+name)
preserve()
run('commit','-m','Record independently verified PR66 mathematics; priority remains under audit')
commit = run('rev-parse','HEAD').decode().strip()
require(run('show','-s','--format=%P',commit).decode().strip()==base and names(run('diff-tree','--no-commit-id','--name-only','-r','-z',commit))==selected,'commit parent/scope drift')
require(run('ls-remote','--heads','origin','main').decode().split()[0]==base,'remote advanced before push')
preserve()
run('push','origin','main')
require(run('ls-remote','--heads','origin','main').decode().split()[0]==commit and not run('diff','--cached','--name-only','-z'),'remote/index readback failure')
preserve()
receipt = {'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_controller_pid':os.getpid(),
           'status':'PASS','commit':commit,'base':base,'remote_main':commit,'owned_path_count':len(selected),
           'foreign_tracked_paths_preserved':len(foreign),'index_empty':True,'native_QUEUE_state_history_unchanged':True,
           'PR66_math_percent':100,'PR66_workflow_percent':30,'priority_clearance':False,'publication':False,'merge':False,
           'program_completed':'7/99 dated intake census','goal_complete':False,'receipt_created_after_push':True}
(F/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
