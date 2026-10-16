import json,os,subprocess,shutil,time,hashlib
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent
A=BASE.parents[1]
ORIG=A/'original/unsolved_math_prioritization/attempts/6000001'
RUNTIME=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python')
TMP=BASE/'private/tmp'; TMP.mkdir(parents=True,exist_ok=True)
PIN='29cb50b07af6a65b633516b5d86eed1dae93d57cf2abfb264b18eb9555a29903'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(label,args,env=None,timeout=300):
 start=datetime.now(timezone.utc).isoformat(); t=time.monotonic()
 e=dict(os.environ);e['TMPDIR']=str(TMP);e['PYTHONDONTWRITEBYTECODE']='1'
 if env:e.update(env)
 p=subprocess.run([str(RUNTIME),*args],cwd=TMP,env=e,capture_output=True,text=True,timeout=timeout)
 (BASE/'evidence'/f'{label}.stdout').write_text(p.stdout)
 (BASE/'evidence'/f'{label}.stderr').write_text(p.stderr)
 r=dict(label=label,start_utc=start,elapsed_seconds=time.monotonic()-t,command=[str(RUNTIME),*args],environment_overrides={'TMPDIR':str(TMP),'PYTHONDONTWRITEBYTECODE':'1',**(env or {})},returncode=p.returncode,stdout_bytes=len(p.stdout.encode()),stdout_sha256=sha(p.stdout.encode()),stderr_bytes=len(p.stderr.encode()),stderr_sha256=sha(p.stderr.encode()))
 (BASE/'evidence'/f'{label}.receipt.json').write_text(json.dumps(r,indent=2)+'\n')
 print(label,p.returncode,p.stderr[-350:].strip(),flush=True)
 return p
run('runtime',['-I','-B','-c','import sys,sympy,numpy,json; print(json.dumps(dict(python=sys.version,sympy=sympy.__version__,numpy=numpy.__version__,optimize=sys.flags.optimize)))'])
records=[]
for label,opts,env in [('normal',[],{}),('O',['-O'],{}),('OO',['-OO'],{}),('inherited_env2',[],{'PYTHONOPTIMIZE':'2','PYTHONPATH':'/does/not/exist'})]:
 packet=TMP/('original_'+label)
 shutil.copytree(ORIG,packet)
 args=['-I','-S','-B',*opts,str(packet/'verify_publication.py'),PIN,str(packet)]
 run('original_wrapper_'+label,args,env)
 run('original_integrity_'+label,args+['--integrity-only'],env)
# Execute authenticated individual checks on an owned copy, untouched originals retained.
packet=TMP/'individual'
shutil.copytree(ORIG,packet)
checks=[('author_math','public/verify_math.py',[]),('auditA_controls','independent_global_audit/public/independent_controls.py',[]),('auditB_checks','independent_audit_b/public/independent_checks.py',[])]
for label,name,extra in checks:
 run(label,['-I','-B',str(packet/name),*extra])
for label,name,extra in checks:
 for mode,opts,env in [('O',['-O'],{}),('OO',['-OO'],{}),('env2',[],{'PYTHONOPTIMIZE':'2'})]:
  # -I deliberately omitted ONLY for inherited_env2 assertion behavior; absolute runtime and -B retained.
  isolated=[] if mode=='env2' else ['-I']
  run(label+'_'+mode,[*isolated,'-B',*opts,str(packet/name)],env)
# Original mutation suite uses its own copies and preserves source.
run('original_mutations',['-I','-S','-B',str(ORIG/'mutation_tests.py'),PIN,str(ORIG)],timeout=600)
