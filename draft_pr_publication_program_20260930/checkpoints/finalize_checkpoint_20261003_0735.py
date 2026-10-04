"""Stage genuinely completed outer capture after child exit and recheck exact index scope."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess
P=Path(__file__).absolute().parents[1];R=P.parent;C=P/'checkpoints/CHECKPOINT_20261003_0735.json';B=P/'audits/pr45_9900007/root_checkpoint_0735_stage_actual_capture'
assert __debug__
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def row(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))
o=json.loads(C.read_bytes());owned={r['path'] for r in o['owned_files']}|{C.relative_to(R).as_posix()}
before={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n};assert before<=owned
for r in o['owned_files']:
 p=R/r['path'];b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
for n in before:assert git('show',':'+n)==(R/n).read_bytes()
cap=json.loads((B/'CAPTURE.json').read_bytes());assert cap['completed'] is True and cap['actual_execution'] is True and cap['pid']==json.loads((B/'stdout.bin').read_bytes())['actual_pid'] and cap['exit_code']==0 and cap['operator_unchanged'] is True
assert {p.name for p in B.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
for k in ['stdout','stderr']:
 b=(B/cap[k]['path']).read_bytes();assert len(b)==cap[k]['bytes'] and sha(b)==cap[k]['sha256']
assert not (B/'stderr.bin').read_bytes()
head=git('rev-parse','HEAD').decode().strip()
assert subprocess.run(['git','merge-base','--is-ancestor',o['main_before'],head],cwd=R).returncode==0
foreign_current=[row(R/r['path']) for r in o['foreign_dirty_before']]
q=P/'checkpoints/CHECKPOINT_20261003_0735_POST_STAGE.json'
record=dict(schema='ROOT_completed_checkpoint_actual_postchild_stage/v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_pid=os.getpid(),original_dated_checkpoint=row(C),dated_checkpoint_future_authority=False,actual_completed_stage_capture=cap,complete_capture_members=[row(p) for p in sorted(B.iterdir())],latest_main_for_scoped_checkpoint=head,concurrent_ancestor_progress_preserved=True,foreign_or_active_members_staged=False,foreign_current_readonly_bindings=foreign_current,dated_foreign_changes_not_rejected=True,completed35of180_percent=35/180*100,current_pr=46,future_merge_authority=False)
with q.open('x') as f:json.dump(record,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
extras=list(B.iterdir())+[q,Path(__file__).absolute()]
new={p.relative_to(R).as_posix() for p in extras};owned|=new
subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=b''.join(n.encode()+b'\0' for n in sorted(new)),check=True)
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n};assert staged==before|new
for n in new:assert git('show',':'+n)==(R/n).read_bytes()
for r in o['foreign_dirty_before']:
 assert r['path'] not in staged
assert git('branch','--show-current')==b'main\n'
print(json.dumps(dict(status='PASS_COMPLETE_OWNED_INDEX_AND_POSTCHILD_CAPTURE',staged_files=len(staged),main_before=head,actual_pid=os.getpid(),foreign_dirty_preserved=len(o['foreign_dirty_before']),future_acceptance_approved=False)))
