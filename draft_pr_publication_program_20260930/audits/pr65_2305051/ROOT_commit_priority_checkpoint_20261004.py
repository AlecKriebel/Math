"""Normal scoped audit commit/push only under a fresh acknowledged window."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess, sys
if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B and no -O')
A = Path(__file__).resolve().parent
P = A.parents[1]; R = P.parent; C = P / 'audits/pr45_9900007'
F = A / 'ROOT_priority_checkpoint_20261004'; F.mkdir(exist_ok=False)
D = F / 'private_actual_git_commands'; D.mkdir()
(D / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
records = []
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_bytes())
def run(*argv):
    parts = ['git', '--no-optional-locks', *argv]
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(parts, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate(); name = str(len(records)+1)
    (D / (name+'.stdout')).write_bytes(out); (D / (name+'.stderr')).write_bytes(err)
    records.append({'argv':parts,'actual_pid':child.pid,'start_utc':start,'finish_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
    (D / 'COMMANDS.json').write_text(json.dumps(records,indent=2)+'\n')
    if child.returncode: raise RuntimeError(err.decode(errors='replace'))
    return out
def names(b): return {p.decode() for p in b.split(b'\0') if p}
def pin(n):
    p=R/n
    if not p.exists(): return {'absent':True}
    if not p.is_file() or p.is_symlink(): raise RuntimeError('Unexpected path type')
    b=p.read_bytes(); return {'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
wp=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'; wb=wp.read_bytes()
def window():
    w=read(wp)
    if wp.read_bytes()!=wb or w.get('shared_git_writes_paused') is not True or w.get('paused_for')!='PR65 priority audit checkpoint 20261004' or w.get('dirty_tracked_bodies_modes_frozen_after_acknowledgement') is not True or w.get('all_staged_path_count')!=0 or w.get('owned_staged_paths') or w.get('local_main_at_pause')!=w.get('remote_main_at_pause'):
        raise RuntimeError('Fresh exclusive window not acknowledged')
    timestamp=dt.datetime.fromisoformat(w['utc'])
    if timestamp < dt.datetime(2026,10,4,6,27,tzinfo=dt.timezone.utc): raise RuntimeError('Stale acknowledgement')
    return w
w=window()
if run('branch','--show-current').strip()!=b'main' or run('diff','--cached','--name-only','-z'): raise RuntimeError('Branch/index drift')
base=run('rev-parse','HEAD').decode().strip()
if base!=w['local_main_at_pause'] or base!=run('ls-remote','--heads','origin','main').decode().split()[0]: raise RuntimeError('Main drift')
progress=read(P/'CURRENT_PROGRESS.json')
if progress['current_PR']!=65 or progress['current_priority_clearance'] or progress['persistent_goal_complete']: raise RuntimeError('Progress drift')
root_files=['ROOT_PRIORITY_ADJUDICATION_20261004.md','ROOT_PRIORITY_SUPPLEMENTAL_READ_20261004.md','ROOT_NATIVE_COMPILATION_20261004.json','ROOT_PRIORITY_PROGRESS_CHECKPOINT_20261004.json','ROOT_prepare_priority_progress_20261004.py','ROOT_commit_priority_checkpoint_20261004.py','RESEARCH_LOG.md','ROOT_checkpoint_20261004/CHECKPOINT_RECEIPT.json','ROOT_package_preflight_20261004/READBACK.json']
roots=[A/n for n in root_files]+[P/'CURRENT_PROGRESS.json',A/'ROOT_priority_readback_20261004']
for n in ['root_pr65_mathematical_scoped_checkpoint_push_20261004_actual_capture','root_pr65_completed_priority_custody_readback_20261004_actual_capture','root_pr65_third_priority_family_readback_20261004_actual_capture','root_pr65_priority_progress_checkpoint_20261004_actual_capture']:
    p=C/n
    if read(p/'CAPTURE.json')['status']!='PASS': raise RuntimeError('Capture not PASS')
    roots.append(p)
rel=[p.relative_to(R).as_posix() for p in roots]
selected=names(run('diff','--name-only','-z','--',*rel))|names(run('ls-files','--others','--exclude-standard','-z','--',*rel))
if not selected or any(not any(n==r or n.startswith(r+'/') for r in rel) for n in selected): raise RuntimeError('Scope mismatch')
if any(any(x in Path(n).parts for x in ['primary_sources','private_actual_git_commands','publication_package_v1','ROOT_priority_search_20261004','__pycache__']) or n.endswith(('.pdf','.png','.pyc')) for n in selected): raise RuntimeError('Private/package scope violation')
foreign={n:pin(n) for n in names(run('diff','--name-only','-z'))-selected}
owned={n:pin(n) for n in sorted(selected)}
native={n:pin(n) for n in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl']}
plan={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'controller_pid':os.getpid(),'base':base,'acknowledgement_sha256':sha(wb),'owned':owned,'foreign':foreign,'native_to_preserve':native,'priority_clearance':False,'PR65_publication_or_merge':False}
planpath=F/'PLAN.json';planpath.write_text(json.dumps(plan,indent=2)+'\n'); pn=planpath.relative_to(R).as_posix();selected.add(pn);owned[pn]=pin(pn)
def preserve():
    window()
    if names(run('diff','--name-only','-z'))-selected!=set(foreign): raise RuntimeError('Foreign path set drift')
    for n,p in {**foreign,**owned,**native}.items():
        if pin(n)!=p: raise RuntimeError('Body/mode drift: '+n)
preserve();run('add','--',*sorted(selected))
if names(run('diff','--cached','--name-only','-z'))!=selected: raise RuntimeError('Staging scope mismatch')
for n,p in owned.items():
    if sha(run('show',':'+n))!=p['sha256']: raise RuntimeError('Index byte mismatch')
preserve();run('commit','-m','Record PR65 priority audit and retain unpublished package review gate')
commit=run('rev-parse','HEAD').decode().strip()
if run('show','-s','--format=%P',commit).decode().strip()!=base or names(run('diff-tree','--no-commit-id','--name-only','-r','-z',commit))!=selected: raise RuntimeError('Commit scope mismatch')
if run('ls-remote','--heads','origin','main').decode().split()[0]!=base: raise RuntimeError('Remote advanced')
preserve();run('push','origin','main')
if run('ls-remote','--heads','origin','main').decode().split()[0]!=commit or run('diff','--cached','--name-only','-z'): raise RuntimeError('Push/index verification failed')
preserve()
receipt={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_controller_pid':os.getpid(),'commit':commit,'base':base,'remote_main':commit,'owned_path_count':len(selected),'foreign_tracked_paths_preserved':len(foreign),'index_empty':True,'native_QUEUE_state_history_unchanged':True,'PR65_workflow_percent':35,'priority_clearance':False,'PR65_merge_or_publication':False,'publication_package_included':False,'goal_complete':False,'receipt_created_after_push_not_embedded_in_own_commit':True}
(F/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
