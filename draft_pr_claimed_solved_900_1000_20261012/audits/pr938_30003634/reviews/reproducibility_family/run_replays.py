import os,sys,json,subprocess,shutil,time,datetime,hashlib,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('guard',HERE/'guarded_replay.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=HERE.parents[1]/'original/unsolved_math_prioritization/attempts/30003634'
SCRATCH=HERE/'tmp';SCRATCH.mkdir(exist_ok=True);TMP=SCRATCH/'temp';TMP.mkdir(exist_ok=True)
PACKET=SCRATCH/'packet';OUT=HERE/'REPLAY_RESULTS.json';RAW=HERE/'raw';RAW.mkdir(exist_ok=True)
PYTHON='/Users/alec/Documents/Math/.venv/bin/python'
if not PACKET.exists():
 g.authenticate(SOURCE)
 shutil.copytree(SOURCE,PACKET)
 for p in PACKET.rglob('*'):p.chmod(0o555 if p.is_dir()else 0o444)
 PACKET.chmod(0o555)
g.authenticate(PACKET,True)
results=[]
def run(label,script,args=(),mode='normal',timeout=1500,expected=None,allow_fail=False):
 g.authenticate(PACKET,True)
 env={k:v for k,v in os.environ.items()if not k.startswith('PYTHON')};env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(TMP))
 flags={'normal':[],'O':['-O'],'OO':['-OO'],'env2':[]}[mode];startup=[]if mode=='env2'else['-I']
 if mode=='env2':env['PYTHONOPTIMIZE']='2'
 probe=subprocess.run([PYTHON,*startup,'-B',*flags,'-c','import sys,json;print(json.dumps({"optimization":sys.flags.optimize,"isolated":sys.flags.isolated,"python":sys.version.split()[0]}))'],env=env,capture_output=True,text=True,check=True)
 cmd=[PYTHON,*startup,'-B',*flags,str(PACKET/script),*map(str,args)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 try:cp=subprocess.run(cmd,cwd=SCRATCH,env=env,capture_output=True,timeout=timeout); rc=cp.returncode;stdout=cp.stdout;stderr=cp.stderr
 except subprocess.TimeoutExpired as e:rc='TIMEOUT';stdout=e.stdout or b'';stderr=e.stderr or b''
 (RAW/(label+'.stdout')).write_bytes(stdout);(RAW/(label+'.stderr')).write_bytes(stderr)
 match=None
 if expected and rc==0:
  try:
   got=json.loads(stdout);want=json.loads((PACKET/expected).read_bytes())
   if script=='audit1/recovery_controls.py':got.pop('python_version',None);want.pop('python_version',None)
   match=got==want
  except ValueError:match=False
 result=dict(label=label,utc=start,elapsed_seconds=round(time.monotonic()-t,3),script=script,args=list(map(str,args)),mode=mode,actual_parent_startup=json.loads(probe.stdout),returncode=rc,stdout_sha256=hashlib.sha256(stdout).hexdigest(),stderr_tail=stderr.decode(errors='replace')[-2000:],saved_json_equal=match,expected_failure=allow_fail)
 results.append(result);OUT.write_text(json.dumps({'results':results},indent=2)+'\n');print(label,rc,match,result['elapsed_seconds'],flush=True)
 g.authenticate(PACKET,True)
 return result
for mode in ['normal','O','OO','env2']:run('author_verify_'+mode,'original/verify.py',mode=mode,expected='original/VERIFY_OUTPUT.json')
run('author_adversarial','original/test_replay.py',expected='original/TEST_REPORT.json')
run('original_independent_hardcoded_path','audit2/independent_check.py',allow_fail=True)
for mode in ['normal','O','OO','env2']:
 run('audit1_recovery_'+mode,'audit1/recovery_controls.py',['--packet',PACKET/'original'],mode,expected='audit1/RECOVERY_CONTROLS.json')
 run('audit2_recovery_'+mode,'audit2/recovery_controls.py',['--author-packet',PACKET/'original'],mode,expected='audit2/RECOVERY_CONTROLS.json')
run('audit2_portable','audit2/test_second_audit_replay.py',['--author-packet',PACKET/'original'],expected='audit2/PORTABLE_REPLAY.json')
# All files authenticated before the trusted copies are made; originals remain frozen.
for name in ['BOOTSTRAP.py','TEST_MUTATIONS.py']:shutil.copyfile(PACKET/name,SCRATCH/name)
def external(label,script,args):
 g.authenticate(PACKET,True);need=g.need;raw=(SCRATCH/script).read_bytes();need(hashlib.sha256(raw).hexdigest()==g.PINS[script][1],'external script identity')
 env={k:v for k,v in os.environ.items()if not k.startswith('PYTHON')};env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(TMP))
 t=time.monotonic();cp=subprocess.run([PYTHON,'-I','-B',str(SCRATCH/script),*map(str,args)],cwd=SCRATCH,env=env,capture_output=True,timeout=1800)
 (RAW/(label+'.stdout')).write_bytes(cp.stdout);(RAW/(label+'.stderr')).write_bytes(cp.stderr)
 result=dict(label=label,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=round(time.monotonic()-t,3),returncode=cp.returncode,stdout_sha256=hashlib.sha256(cp.stdout).hexdigest(),stderr_tail=cp.stderr.decode(errors='replace')[-3000:])
 if script=='TEST_MUTATIONS.py'and cp.returncode==0:result['saved_json_equal']=json.loads(cp.stdout)==json.loads((PACKET/'MUTATION_RESULTS.json').read_bytes())
 results.append(result);OUT.write_text(json.dumps({'results':results},indent=2)+'\n');print(label,cp.returncode,result['elapsed_seconds'],flush=True);g.authenticate(PACKET,True)
external('outer_bootstrap_full','BOOTSTRAP.py',['--packet',PACKET,'--expected-manifest',g.HEX,'--filesystem-profile','readonly'])
# Mutation driver normalizes copies, baseline input must be normal modes.
BASELINE=SCRATCH/'baseline'
if not BASELINE.exists():
 shutil.copytree(SOURCE,BASELINE)
 for p in BASELINE.rglob('*'):p.chmod(0o755 if p.is_dir()else 0o644)
 BASELINE.chmod(0o755)
g.authenticate(BASELINE)
external('outer_original_mutation_harness','TEST_MUTATIONS.py',['--packet',BASELINE,'--bootstrap',SCRATCH/'BOOTSTRAP.py','--expected-manifest',g.HEX])
