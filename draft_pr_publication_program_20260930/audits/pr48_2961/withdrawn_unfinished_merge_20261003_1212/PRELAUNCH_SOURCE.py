"""Withdraw only ROOT's untouched original PR48 merge; preserve foreign staging."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess
R=Path('/Users/alec/Documents/Math'); A=R/'draft_pr_publication_program_20260930/audits/pr48_2961'
O='e2e5c8c3e5ad218f867fa753c465bb96b3687bda'
Q='unsolved_math_prioritization/QUEUE.md'; prefix='unsolved_math_prioritization/attempts/2961/'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def digest(b):return hashlib.sha256(b).hexdigest()
def row(n):
 p=R/n;s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 b=p.read_bytes();return dict(path=n,bytes=len(b),sha256=digest(b),mode=stat.S_IMODE(s.st_mode))
def index():return {x.split(b'\t',1)[1].decode():x for x in git('ls-files','--stage','-z').split(b'\0') if x}
assert git('branch','--show-current')==b'main\n'
head=git('rev-parse','HEAD').decode().strip()
assert (R/'.git/MERGE_HEAD').read_text()==O+'\n'
assert not (A/'root_overlay_actual_capture').exists() and not (A/'integration_check.json').exists()
assert git('diff','--name-only','--diff-filter=U').decode()==Q+'\n'
q=(R/Q).read_bytes();assert len(q)==386771 and digest(q)=='3ec5a2028f4bfdfecaf6f3dff6afb0e70a292607170e1442d218d9788d47ef52'
fresh=json.loads((A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json').read_bytes())
assert subprocess.run(['git','merge-base','--is-ancestor',fresh['current_head'],head],cwd=R).returncode==0
assert git('diff','--name-only',fresh['current_head'],head,'--',Q,prefix)==b''
oldq=git('show',head+':'+Q); qref=next(x for x in fresh['files'] if x['path']==Q)
assert len(oldq)==qref['bytes'] and digest(oldq)==qref['sha256']
original=git('ls-tree','-r','-z',O,'--',prefix)
orig={}
for x in original.split(b'\0'):
 if not x:continue
 fields,n=x.split(b'\t',1);mode,kind,oid=fields.decode().split();assert mode=='100644' and kind=='blob'
 orig[n.decode()]=oid
assert len(orig)==17 and git('ls-tree','-r','-z',head,'--',prefix)==b''
idx=index(); ours={Q,*orig}; foreign={n:x.hex() for n,x in idx.items() if n not in ours}
for n,oid in orig.items():
 assert idx[n].decode()=='100644 '+oid+' 0\t'+n
 assert git('show',':'+n)==git('show',O+':'+n)==(R/n).read_bytes()
native=[row(z['path']) for z in fresh['files'] if z['path']!=Q]
assert all(z['bytes']==next(v for v in fresh['files'] if v['path']==z['path'])['bytes'] and z['sha256']==next(v for v in fresh['files'] if v['path']==z['path'])['sha256'] and z['mode']==next(v for v in fresh['files'] if v['path']==z['path'])['worktree_mode'] for z in native)
# Snapshot every foreign staged/unstaged tracked worktree body and full mode.
dirty={x.decode() for x in git('diff','--name-only','-z').split(b'\0') if x}
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}
protected=sorted((dirty|staged)-ours); before=[row(n) for n in protected]
D=A/'withdrawn_unfinished_merge_20261003_1212';D.mkdir(exist_ok=False)
def put(n,b):
 with (D/n).open('xb') as f:f.write(b)
put('PRELAUNCH_SOURCE.py',Path(__file__).read_bytes());put('AUTOMATIC_QUEUE_PREIMAGE.md',q)
control={n:(R/'.git'/n).read_bytes().hex() for n in ['MERGE_HEAD','MERGE_MSG','ORIG_HEAD'] if (R/'.git'/n).exists()}
facts=dict(schema='pr48-withdraw-unfinished-owned-merge/v1',prepared_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),pid=os.getpid(),head=head,original_head=O,owned_paths=sorted(ours),foreign_index_entries_sha256=digest(json.dumps(foreign,sort_keys=True).encode()),foreign_index_entry_count=len(foreign),foreign_staged_entries={n:foreign[n] for n in protected if n in foreign and n in staged},foreign_worktree_preimages=before,native12_preimages=native,merge_control_preimages_hex=control,root_overlay_never_launched=True)
put('BEFORE.json',(json.dumps(facts,indent=2)+'\n').encode())
assert git('rev-parse','HEAD').decode().strip()==head and (R/'.git/MERGE_HEAD').read_text()==O+'\n'
subprocess.run(['git','restore','--source='+head,'--staged','--worktree','--',*sorted(ours)],cwd=R,check=True)
assert git('rev-parse','HEAD').decode().strip()==head
assert {n:x.hex() for n,x in index().items() if n not in ours}==foreign and [row(n) for n in protected]==before
assert (R/Q).read_bytes()==oldq and all(not (R/n).exists() for n in orig)
assert [row(z['path']) for z in fresh['files'] if z['path']!=Q]==native
assert (R/'.git/MERGE_HEAD').read_text()==O+'\n'
subprocess.run(['git','merge','--quit'],cwd=R,check=True)
assert not (R/'.git/MERGE_HEAD').exists() and git('rev-parse','HEAD').decode().strip()==head
assert {n:x.hex() for n,x in index().items() if n not in ours}==foreign and [row(n) for n in protected]==before
facts.update(status='PASS_WITHDRAWN_OWNED_UNFINISHED_MERGE_FOREIGN_STAGING_PRESERVED',finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),foreign_index_entries_preserved=True,foreign_worktree_bodies_and_full_modes_preserved=True,native12_preserved=True,QUEUE_restored_to_exact_unchanged_current_HEAD=True,ROOT_math_and_SOURCE_review_unchanged=True,acceptance_completed=False)
put('RESULT.json',(json.dumps(facts,indent=2)+'\n').encode())
print(json.dumps({k:facts[k] for k in ['status','head','original_head','foreign_index_entries_preserved','foreign_worktree_bodies_and_full_modes_preserved','native12_preserved','QUEUE_restored_to_exact_unchanged_current_HEAD','acceptance_completed']}))
