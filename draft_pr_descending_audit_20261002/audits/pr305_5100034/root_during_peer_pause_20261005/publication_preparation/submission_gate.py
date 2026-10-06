"""Require exact closed scientific/operational clearances and an actual write lease.

No gate writes a clearance or invents process completion. No execution is
permitted during the shared pause. Inputs and whole namespaces are checked
before every action, and the same OS lock is held throughout an action.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json,stat,os,subprocess,fcntl,sys
if sys.flags.optimize:
 raise RuntimeError("Optimized Python is forbidden: publication hardguards must remain active.")
D=Path(__file__).resolve().parent.parent;A=D.parent;P=A.parent.parent;R=P.parent
C=D/'preprint_review02_candidate_frozen';O=D/'submission_v02';OUT=D/'publication_actual'
THREAD='01a0ff30-7e80-7053-abb4-4a9c45f2fd62'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink(),str(p)
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'mode':format(stat.S_IMODE(s.st_mode),'04o')}
def git(*args):
 r=subprocess.run(['/usr/bin/git',*args],cwd=R,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),stdin=subprocess.DEVNULL,timeout=30);assert r.returncode==0,('Git gate failed',args);return r.stdout

def current_clearance():
 clear=load(D/'ROOT_FULL_PREPRINT_PUBLICATION_CLEARANCE.json')
 assert clear['status']=='PASS_PR305_FULL_PREPRINT_REVISION02_READY' and clear['pr']==305
 assert clear['original_head']=='cc083024dbd00de06ad444cd4070f51f60d209eb' and clear['original_status']=='claimed_solved'
 assert clear['mandatory_unresolved_findings']==0 and clear['new_whole_review_round']==2
 assert clear['candidate_manifest_sha256']=='b82312f47046c9a530fea5050c4ab3771195fa31cf42d5e3537691d532df47bc'
 assert pin(C/'MANIFEST.json')['sha256']==clear['candidate_manifest_sha256']
 m=load(C/'MANIFEST.json');rows=m['files'];assert len(rows)==23
 assert {str(p.relative_to(C)) for p in C.rglob('*') if p.is_file()}=={x['path'] for x in rows}|{'MANIFEST.json'}
 for e in rows:assert pin(C/e['path'])=={'bytes':e['bytes'],'sha256':e['sha256'],'mode':'0444'}
 assert set(clear['submission_files'])=={'focal-pedal-ratios-note.pdf','focal-pedal-ratios-verification.zip','zenodo-deposit.json','SUBMISSION_MANIFEST.json'}
 assert {p.name for p in O.iterdir()}==set(clear['submission_files'])
 for n,e in clear['submission_files'].items():assert pin(O/n)==e
 assert clear['submission_files']['focal-pedal-ratios-note.pdf']['sha256']=='426e2f9809b6f02bf03ee564cad40ae41cc0cee68dfafb907257bd17c6f04686'
 assert clear['submission_files']['focal-pedal-ratios-verification.zip']['sha256']=='08194099e1c287c8c71fd6693c8070d4db73d2fe43db7447de5924aaa919de8f'
 assert clear['submission_files']['zenodo-deposit.json']['sha256']=='85b16b561dacb6a393f0ec40a4c88e54e8482aa5c41cd3e21a74f63b3cf6fcc1'
 for absolute,e in clear['closed_evidence_bindings'].items():assert pin(absolute)==e
 return clear

def operational_clearance():
 v=load(D/'ROOT_PUBLICATION_OPERATIONAL_CLEARANCE.json')
 assert v['status']=='PASS_PR305_EXACT_ZENODO_AND_TRACKER_OPERATORS' and v['unresolved_mandatory_findings']==0
 names={'submission_gate.py','run_zenodo_step.py','public_identity.py','verify_public_record.py','append_tracker.py'}
 assert set(v['reviewed_programs'])==names
 for n,e in v['reviewed_programs'].items():assert pin(D/'publication_preparation'/n)==e
 evidence=v['closed_review_evidence'];assert len(evidence)>=2
 for name in ['REVIEW_REPORT.md','OUTPUT_INVENTORY.json']:
  assert str(D/'publication_operations_review_02'/name) in evidence
 for absolute,e in evidence.items():assert pin(absolute)==e
 return v

def safe_endpoints():
 # Reject any URL rewrite privately, then inspect both directions. No config
 # names/values or potential credentials enter retained/public streams.
 r=subprocess.run(['/usr/bin/git','config','--get-regexp',r'^url\..*\.(insteadof|pushinsteadof)$'],cwd=R,capture_output=True)
 assert r.returncode==1 and not r.stdout and not r.stderr,'URL rewrite requires explicit reconciliation.'
 fetch=git('remote','get-url','--all','origin').decode().splitlines();push=git('remote','get-url','--push','--all','origin').decode().splitlines()
 approved={'https://github.com/AlecKriebel/Math.git','git@github.com:AlecKriebel/Math.git','ssh://git@github.com/AlecKriebel/Math.git'}
 assert len(fetch)==len(push)==1 and fetch[0] in approved and push[0] in approved
 return fetch[0],push[0]

def window():
 s=load(P/'SHARED_GIT_WINDOW_STATUS.json');assert s['shared_git_writes_paused'] is False
 lease=s['descending_shared_write_lease'];assert lease['owner_thread']==THREAD and lease['pr']==305 and lease['publication_authorized'] is True
 actual=load(D/'ROOT_FINAL_WRITE_LEASE.json');assert actual['status']=='ACTIVE_PR305_FINAL_WRITE_LEASE' and actual['owner_thread']==THREAD and actual['pr']==305 and actual['token']==lease['token']
 times={}
 for key in ['issued_utc','not_before_utc','expires_utc']:
  assert type(actual[key]) is str and actual[key]==lease[key]
  value=datetime.fromisoformat(actual[key].replace('Z','+00:00'));assert value.utcoffset()==timedelta(0)
  times[key]=value
 now=datetime.now(timezone.utc)
 assert times['issued_utc']<=times['not_before_utc']<=now
 assert timedelta(0)<times['expires_utc']-times['issued_utc']<=timedelta(seconds=600)
 assert now+timedelta(seconds=60)<=times['expires_utc'],'Lease must cover the complete55-second subprocess deadline.'
 released=load(D/'ROOT_PR80_PUBLICATION_WINDOW_RELEASE_VERIFICATION.json');assert released['status']=='PASS_PR80_ALL_THREE_PHASES_AND_RELEASE' and released['all_held_bodies_modes_unchanged'] and released['foreign_logical_index_unchanged']
 assert git('branch','--show-current')==b'main\n';fetch,push=safe_endpoints();assert (fetch,push)==(actual['fetch_endpoint'],actual['push_endpoint'])
 head=git('rev-parse','HEAD').decode().strip();assert head==actual['main']
 assert git('ls-remote',fetch,'refs/heads/main').decode().split()[0]==head
 git('merge-base','--is-ancestor',released['released_main'],head)
 assert not git('diff','--cached','--raw','-z'),'Shared index must be empty before this operation.'
 assert datetime.now(timezone.utc)+timedelta(seconds=60)<=times['expires_utc'],'Fresh Git readbacks consumed the remaining lease; refresh before any action.'
 return actual

def acquire():
 # Existing cooperative lock; no new lock or held-file body is created.
 fd=os.open(P/'audits/pr311_30005303/root_integration_private/SHARED_WRITE_LEASE.lock',os.O_RDWR|os.O_NOFOLLOW)
 lock=os.fdopen(fd,'r+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 current_clearance();operational_clearance();window();return lock

def execute(label,argv,private=None):
 out=Path(private) if private else OUT;out.mkdir(parents=True,exist_ok=True)
 pre=out/(label+'_preexecution.json');assert not pre.exists(),'Prior/uncertain attempt exists; read back and reconcile before any retry.'
 spec={'argv':[str(x) for x in argv],'cwd':str(R),'started_utc':utc(),'automatic_retry':False,'programs':{str(p):pin(p) for p in [D/'publication_preparation/submission_gate.py']+ [Path(x) for x in argv if Path(x).suffix=='.py' and Path(x).is_file()]}}
 pre.write_text(json.dumps(spec,indent=2)+'\n');timed=False
 try:r=subprocess.run(spec['argv'],cwd=R,capture_output=True,stdin=subprocess.DEVNULL,timeout=55)
 except subprocess.TimeoutExpired as e:timed=True;r=subprocess.CompletedProcess(spec['argv'],124,e.stdout or b'',e.stderr or b'')
 for kind,b in [('stdout',r.stdout),('stderr',r.stderr)]: (out/(label+'.'+kind)).write_bytes(b);spec[kind+'_bytes']=len(b);spec[kind+'_sha256']=sha(b)
 spec.update(ended_utc=utc(),exit_code=r.returncode,timed_out=timed);(out/(label+'_execution.json')).write_text(json.dumps(spec,indent=2)+'\n')
 assert r.returncode==0,(label,'No retry made; reconcile uncertain external state read-only.')
 return json.loads(r.stdout)
