"""Observe child outcomes while executing the exact authenticated original driver."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.optimize==0):raise RuntimeError('Use -I -S -B')
from pathlib import Path
import subprocess,json,hashlib,os
O=Path(__file__).resolve().parent;PK=O/'private/cold';P=PK/'original/unsolved_math_prioritization/attempts/6000001';b=(P/'mutation_tests.py').read_bytes();m=json.loads((PK/'PACKAGE_MANIFEST.json').read_text());assert hashlib.sha256(b).hexdigest()==m['files']['original/unsolved_math_prioritization/attempts/6000001/mutation_tests.py']['sha256']
os.environ['TMPDIR']=str(O/'private/temp');actual=subprocess.run;records=[]
def observe(*args,**kwargs):
 r=actual(*args,**kwargs)
 argv=args[0]
 if '--child-optimize' in argv:records.append({'argv_tail':argv[-4:],'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 return r
subprocess.run=observe;sys.argv=[str(P/'mutation_tests.py'),'29cb50b07af6a65b633516b5d86eed1dae93d57cf2abfb264b18eb9555a29903',str(P)]
from contextlib import redirect_stdout
import io
out=io.StringIO();error=None
try:
 with redirect_stdout(out):exec(compile(b,str(P/'mutation_tests.py'),'exec',dont_inherit=True,optimize=0),{'__name__':'__main__','__file__':str(P/'mutation_tests.py')})
except SystemExit as e:error=str(e)
finally:subprocess.run=actual
(O/'MUTATION_CHILD_OBSERVATIONS.json').write_text(json.dumps({'actual_unmodified_driver':True,'error':error,'optimized_child_records':records},indent=2)+'\n')
if error:raise RuntimeError(error)
j=json.loads(out.getvalue());assert j['status']=='PASS' and j['negative_controls']==63;(O/'ORIGINAL_MUTATIONS_REPLAY.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps({'status':'PASS','controls':63,'optimized_child_observations':len(records)}))
