"""Bind the completed stage capture, check exact owned index, then commit."""
from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess
P=Path(__file__).absolute().parents[1];R=P.parent;C=P/'checkpoints/CHECKPOINT_20261003_0935.json';D=P/'audits/pr45_9900007/root_checkpoint_0935_stage_v3_actual_capture'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def row(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))
o=json.loads(C.read_bytes());owned={z['path']:z for z in o['owned_files']};owned[C.relative_to(R).as_posix()]=row(C)
c=json.loads((D/'CAPTURE.json').read_bytes());assert c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and c['operator_unchanged'] is True
assert json.loads((D/'stdout.bin').read_bytes())['actual_pid']==c['pid']==17374
for k in ('stdout','stderr'):
 b=(D/c[k]['path']).read_bytes();assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
assert not (D/'stderr.bin').read_bytes() and git('branch','--show-current')==b'main\n'
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n};assert staged<=set(owned)
entries={}
for line in git('ls-files','--stage','-z').split(b'\0'):
 if line:
  meta,n=line.split(b'\t');mode,blob,stage=meta.split();assert stage==b'0';entries[n.decode()]=(mode,blob)
for n in staged:
 b=(R/n).read_bytes();z=owned[n];assert len(b)==z['bytes'] and sha(b)==z['sha256']
 assert entries[n]==(b'100644',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode())
head=git('rev-parse','HEAD').decode().strip();assert subprocess.run(['git','merge-base','--is-ancestor',o['main_before'],head],cwd=R).returncode==0
record=P/'checkpoints/CHECKPOINT_20261003_0935_POST_STAGE.json'
with record.open('x') as f:json.dump(dict(schema='ROOT_completed_owned_checkpoint_poststage/v2',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_pid=os.getpid(),dated_checkpoint=row(C),complete_stage_capture=c,complete_stage_capture_members=[row(p) for p in sorted(D.iterdir())],main_before_commit=head,staged_before=len(staged),owned_fullbytes_and_index_blob_ids_checked=True,foreign_or_active_members_staged=False,completed36of180_percent=20.0,current_pr=47,future_acceptance_approved=False),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
extra=list(D.iterdir())+[record,Path(__file__).absolute()];extra_names={p.relative_to(R).as_posix() for p in extra}
subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=b''.join(n.encode()+b'\0' for n in sorted(extra_names)),check=True)
assert {n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n}==staged|extra_names
assert git('rev-parse','HEAD').decode().strip()==head and 'unsolved_math_prioritization/QUEUE.md' not in staged|extra_names
for z in o['foreign_tracked_dirty']:assert z['path'] not in staged|extra_names
subprocess.run(['git','commit','-m','Checkpoint PR46 acceptance and PR47–50 adversarial findings'],cwd=R,check=True,stdout=subprocess.DEVNULL)
assert not git('diff','--cached','--name-only')
commit=git('rev-parse','HEAD').decode().strip()
assert git('show','-s','--format=%P',commit).decode().strip()==head
print(json.dumps(dict(status='PASS_COMMITTED_EXACT_OWNED_CHECKPOINT',actual_pid=os.getpid(),commit=commit,main_before=head,files_committed=len(staged|extra_names),completion_percent=20.0,current_pr=47)))
