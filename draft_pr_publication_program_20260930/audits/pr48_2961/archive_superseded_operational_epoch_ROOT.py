"""Preserve the completed, superseded operational epoch before a fresh ROOT run.
No closed scientific/SOURCE family or native/foreign file is modified.
"""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess
R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr48_2961'
D=A/'historical_operational_epoch_20261003_1124'
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def snapshot(p):
    items=[p]+sorted(p.rglob('*')) if p.is_dir() else [p]
    out=[]
    for x in items:
        s=x.lstat();assert not x.is_symlink()
        z={'path':x.relative_to(A).as_posix(),'full_mode':stat.S_IMODE(s.st_mode)}
        if stat.S_ISREG(s.st_mode):
            b=x.read_bytes();z.update(kind='file',bytes=len(b),sha256=sha(b))
        else:assert stat.S_ISDIR(s.st_mode);z['kind']='directory'
        out.append(z)
    return out
assert git('branch','--show-current')==b'main\n'
assert not git('diff','--cached','--name-only')
assert not (A/'root_preflight_actual_capture').exists()
fresh=json.loads((A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json').read_bytes())
head=git('rev-parse','HEAD').decode().strip()
assert subprocess.run(['git','merge-base','--is-ancestor',fresh['current_head'],head],cwd=R).returncode==0
queue='unsolved_math_prioritization/QUEUE.md'
for z in fresh['files']:
    p=R/z['path'];b=p.read_bytes();assert stat.S_IMODE(p.stat().st_mode)==z['worktree_mode']
    if z['path']!=queue:assert len(b)==z['bytes'] and sha(b)==z['sha256']
before=git('show',fresh['current_head']+':'+queue)
after=(R/queue).read_bytes();assert after==git('show',head+':'+queue)
def row(body):
    rows=[x for x in body.splitlines(keepends=True) if x.startswith(b'|') and len(x.split(b'|'))==14 and x.split(b'|')[2].strip()==b'2961 / KP-4.85']
    assert len(rows)==1;return rows[0]
assert row(before)==row(after)
changes={x.decode() for x in git('diff','--name-only','-z',fresh['current_head'],head).split(b'\0') if x}
assert not any(x.startswith(('draft_pr_publication_program_20260930/','unsolved_math_prioritization/attempts/2961/')) for x in changes)
names=['ROOT_SOURCE_ACCEPTANCE_REVIEW.json','ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json','ROOT_FINAL_PLAN.json','ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json','root_acceptance_author_readonly_inputs','root_final_reconciliation_actual_capture','root_final_reconciled']
old={n:snapshot(A/n) for n in names}
assert not D.exists() and git('rev-parse','HEAD').decode().strip()==head
D.mkdir()
for n in names:
    os.rename(A/n,D/n)
    moved=snapshot(D/n)
    normalized=[dict(z,path=z['path'].removeprefix(D.name+'/')) for z in moved]
    assert normalized==old[n]
record={'schema':'ROOT-preserved-superseded-operational-epoch/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'original_current_head':fresh['current_head'],'fresh_observed_head':head,'legitimate_committed_advance_paths':sorted(changes),'selected2961_queue_row_unchanged':True,'other12_native_bodies_full_modes_unchanged':True,'preserved_original_path_bindings':old,'archived_prefix':D.relative_to(R).as_posix(),'qualification':'These seven items preserve complete earlier operational bodies and modes after a legitimate concurrent audit advanced main and foreign tracked work. Their original names describe that dated epoch, not current live namespace authority. Source families, original captures outside these items, author sources, final operator, and native/foreign work remain untouched. The preflight caller39492 failed before any production-phase child or inner capture existed. A new actual author/sealer/preflight is required; no PASS is transferred.'}
with (D/'EPOCH_QUALIFICATION.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
assert git('rev-parse','HEAD').decode().strip()==head and not git('diff','--cached','--name-only')
print(json.dumps({'status':'PASS_PRESERVED_OWN_OPERATIONAL_HISTORY_ONLY','actual_pid':os.getpid(),'archived_items':len(names),'preserved_members':sum(len(v) for v in old.values()),'current_head':head,'native_or_foreign_mutations':False,'production_phase_executed':False}))
