"""Root whole-stream preclosure reproduction and immutable postclosure verification."""
from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
A=Path(__file__).resolve().parent;N=A/'preprint_review_01';PY='/opt/homebrew/bin/python3.11'
phase=sys.argv[1];assert phase in {'pre','post'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def inv():
 out={}
 for p in sorted(N.rglob('*')):
  assert not p.is_symlink() and (p.is_file() or p.is_dir())
  e={'type':'file' if p.is_file() else 'directory','mode':stat.S_IMODE(p.stat().st_mode)}
  if p.is_file():b=p.read_bytes();e.update(bytes=len(b),sha256=sha(b))
  out[p.relative_to(N).as_posix()]=e
 return out
result_name='ROOT_PREPRINT01_PRECLOSURE_REPLAY.json' if phase=='pre' else 'ROOT_PREPRINT_REVIEW01_VERIFICATION.json'
assert not (A/result_name).exists()
D=A/'root_replay_private'/('preprint_review01_'+phase+'_001');D.mkdir(parents=True,exist_ok=False)
before=inv();(D/'whole_namespace_before.json').write_text(json.dumps(before,indent=2)+'\n')
pins=[{'path':name,**pin} for name,pin in load(A/'ROOT_PREPRINT_PACKAGE_VERIFICATION.json')['files'].items()]
for e in pins:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
for label,root_path in [('default','preprint_draft002/integrity.stdout'),('full','preprint_draft001/full.stdout')]:
 assert (N/'execution_private'/(label+'.stdout')).read_bytes()==(A/'root_replay_private'/root_path).read_bytes()
 assert (N/'execution_private'/(label+'.stderr')).read_bytes()==b''
runs=[]
def run(label,args,expected):
 prep={'utc':utc(),'argv':args,'orchestrator_sha256':sha(Path(__file__).read_bytes()),
  'program_sha256':sha(Path(args[2]).read_bytes()),'expected_whole_stdout_bytes':len(expected),'expected_whole_stdout_sha256':sha(expected)}
 (D/(label+'.preexecution.json')).write_text(json.dumps(prep,indent=2)+'\n')
 z=subprocess.run(args,cwd=A,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 for k,b in [('stdout',z.stdout),('stderr',z.stderr)]:(D/(label+'.'+k)).write_bytes(b)
 r={**prep,'finished_utc':utc(),'exit_code':z.returncode,'stdout_path':str(D/(label+'.stdout')),
  'stderr_path':str(D/(label+'.stderr')),'stdout_bytes':len(z.stdout),'stdout_sha256':sha(z.stdout),'stderr_bytes':len(z.stderr),'whole_expected_output_compared':z.stdout==expected}
 (D/(label+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');runs.append(r)
 assert z.returncode==0 and not z.stderr and z.stdout==expected,(label,z.stderr)
if phase=='pre':
 assert not (N/'CLOSURE.json').exists()
 run('literal',[PY,'-B',str(N/'controls/independent_literal_controls.py')],(N/'execution_private/independent_literal.stdout').read_bytes())
for mode,extra in [('public',[]),('full',['--full','--include-external'])]:
 expected=(N/'verification_private'/(mode+'.stdout')).read_bytes()
 if phase=='post':
  obj=json.loads(expected);obj['state']='closed'
  obj['files_bound']=len(load(N/'PRIVATE_MANIFEST.json')['files']) if mode=='full' else len(load(N/'public/PUBLIC_MANIFEST.json')['files'])
  expected=(json.dumps(obj,indent=2)+'\n').encode()
 run(mode,[PY,'-B',str(N/'public/verify_review.py'),*extra],expected)
assert inv()==before
for e in pins:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
r={'utc':utc(),'status':'PASS_WHOLE_FIRST_FRESH_PREPRINT_REVIEW_'+phase.upper(),'mandatory_findings':0,
 'whole_verifier_output_compared':True,'closed_namespace_unchanged':phase=='post','all_mandatory_submission_findings_resolved':True,
 'sealed_submission_files':pins,'native_runs':runs,'captures':runs,'whole_namespace':before,'package_full_and_default_outputs_equal_root':True,
 'scope':'Universal proof/report/code concretely read by root. Native literal controls independently reproduced before closure; read-only evidence verification compares every whole stream. No global priority or external human-review certificate.'}
if phase=='post':
 old=load(A/'ROOT_PREPRINT01_PRECLOSURE_REPLAY.json')['whole_namespace'];assert set(before)-set(old)=={'public/PUBLIC_MANIFEST.json','PRIVATE_MANIFEST.json','CLOSURE.json'}
 for path,e in old.items():
  if path=='research_log.md':continue
  assert before[path]==e,path
 assert (N/'research_log.md').read_bytes().startswith((A/'root_replay_private/preprint_review01_pre_001/research_log.before.md').read_bytes())
 assert before['research_log.md']['mode']==old['research_log.md']['mode']
 r.update(review_seal_path='CLOSURE.json',review_seal_sha256=sha((N/'CLOSURE.json').read_bytes()),closure_authorization_sha256=sha((A/'ROOT_PREPRINT01_CLOSURE_AUTHORIZATION.json').read_bytes()))
 r['package_native_streams']={label:{'stdout_path':str(N/'execution_private'/(label+'.stdout')),'stderr_path':str(N/'execution_private'/(label+'.stderr')),
  'bytes':(N/'execution_private'/(label+'.stdout')).stat().st_size,'sha256':sha((N/'execution_private'/(label+'.stdout')).read_bytes()),'exit_code':load(N/'execution_private'/(label+'.after.json'))['exit_code']} for label in ['default','full']}
else:(D/'research_log.before.md').write_bytes((N/'research_log.md').read_bytes())
(A/result_name).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in {'whole_namespace','captures'}},indent=2))
