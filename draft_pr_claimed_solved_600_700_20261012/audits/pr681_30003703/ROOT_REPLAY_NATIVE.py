"""Reproduce exact captured PR681 packet from disposable copies only."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,tempfile
A=Path(__file__).absolute().parent;N=A/'native/unsolved_math_prioritization/attempts/30003703';P=A.parents[1]/'tooling/math-venv/bin/python';TMP=A/'tmp';TMP.mkdir(exist_ok=True)
def hashes():return {p.relative_to(N).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in N.rglob('*') if p.is_file()}
before=hashes();snapshot=json.loads((A/'SCOPE_AND_SNAPSHOT.json').read_text())
for name,pin in snapshot['original_blobs'].items():
 raw=(A/'native'/name).read_bytes()
 if len(raw)!=pin['size'] or hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError(name)
reports=[]
with tempfile.TemporaryDirectory(prefix='root-native-',dir=TMP) as temporary:
 dest=Path(temporary)/'packet';shutil.copytree(N,dest)
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  result=subprocess.run([str(P),'-I','-B',*flags,str(dest/'verify_publication.py')],cwd=dest,capture_output=True,text=True,env=os.environ|{'TMPDIR':temporary})
  (A/f'ROOT_NATIVE_REPLAY.{mode}.stdout').write_text(result.stdout);(A/f'ROOT_NATIVE_REPLAY.{mode}.stderr').write_text(result.stderr)
  if result.returncode:raise RuntimeError(result.stderr)
  reports.append({'mode':mode,'exit_code':result.returncode,'result':json.loads(result.stdout)})
if before!=hashes():raise ValueError('Native changed')
x={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','original_files':len(before),'native_unchanged':True,'temporary_copies_only':True,'runs':reports,'scope':'Exact integrity/algebra reproduction, not formal proof or priority certification'}
(A/'ROOT_NATIVE_REPLAY.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({'status':'PASS','original_files':len(before),'modes':[x['mode'] for x in reports]}))
