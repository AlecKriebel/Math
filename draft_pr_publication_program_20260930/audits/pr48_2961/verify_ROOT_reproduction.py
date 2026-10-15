"""Readonly complete postchild verification of ROOT's closed PR48 reproduction."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat,sys
A=Path(__file__).absolute().parent;R=A.parents[2];D=A/'root_original_actual_reproduction_v2';B=A.parent/'pr45_9900007'
assert __debug__ and not sys.flags.optimize
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
 return p.read_bytes()
def unique(items):
 o={}
 for k,v in items:
  assert k not in o;o[k]=v
 return o
def load(p):return json.loads(read(p),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
m=load(D/'MANIFEST.json');assert sha(read(D/'MANIFEST.json'))=='f4d8a828e659c5f233053fb3309c38c8d3fe1c90520d6abef2d73b30df7776e9' and m['files_count']==len(m['files'])==254 and len(m['directories'])==53 and m['self_excluded']==['MANIFEST.json'] and m['future_acceptance_approved'] is False
for r in m['files']:
 p=D/r['path'];b=read(p);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444 and r['full_mode']=='0444'
assert stat.S_IMODE((D/'MANIFEST.json').stat().st_mode)==0o444
assert {p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}=={r['path'] for r in m['files']}|{'MANIFEST.json'}
assert {p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_dir()}==set(m['directories'])
s=load(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json');assert sha(read(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json'))=='437312da163e7fa4e64363fab7de5c624fab79672509f725ba1a3c3402dae13f' and s['actual_closure_pid']==19105 and s['future_acceptance_approved'] is False
for r in s['failed_V1_complete_bindings']:
 b=read(R/r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
C=B/'root_pr48_reproduction_closure_actual_capture';c=load(C/'CAPTURE.json');assert c['pid']==19105 and c['exit_code']==0 and c['actual_execution'] is True and c['completed'] is True and c['operator_unchanged'] is True
for k in ['stdout','stderr']:
 b=read(C/c[k]['path']);assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
assert not read(C/'stderr.bin');out=load(C/'stdout.bin');assert out['manifest']['sha256']==sha(read(D/'MANIFEST.json')) and out['summary']['sha256']==sha(read(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json'))
assert dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(m['created_utc'])<dt.datetime.fromisoformat(c['finished_utc'])<dt.datetime.now(dt.timezone.utc)
print(json.dumps(dict(status='PASS_COMPLETE_ROOT_CLOSED_REPRODUCTION_POSTCHILD',actual_readback_pid=os.getpid(),payload_files=254,directories=53,manifest_sha256=sha(read(D/'MANIFEST.json')),entire_failed_V1_bindings_checked=len(s['failed_V1_complete_bindings']),actual_closing_child_pid=19105,future_acceptance_approved=False),indent=2))
