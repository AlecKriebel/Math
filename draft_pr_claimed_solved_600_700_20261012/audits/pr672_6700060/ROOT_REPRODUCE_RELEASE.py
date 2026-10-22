"""Repeat frozen PR672 release controls only from temporary copies."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,tempfile
A=Path(__file__).absolute().parent;N=A/'native/unsolved_math_prioritization/attempts/6700060';P=A.parents[1]/'tooling/math-venv/bin/python'
def hashes():return {p.relative_to(N).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in N.rglob('*') if p.is_file()}
before=hashes();out=[];(A/'tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='repeat-native-',dir=A/'tmp') as temporary:
 dest=Path(temporary)/'release';shutil.copytree(N,dest)
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  r=subprocess.run([str(P),'-I','-B',*flags,str(dest/'verify_release.py'),'--self-test'],cwd=dest,capture_output=True,text=True,env=os.environ|{'TMPDIR':temporary})
  if r.returncode:raise RuntimeError(r.stderr)
  out.append({'mode':mode,'result':json.loads(r.stdout)})
if before!=hashes():raise ValueError('Frozen source changed')
print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_files':len(before),'native_unchanged':True,'runs':out,'scope':'finite diagnostics, not analytic theorem certification'},indent=2))
