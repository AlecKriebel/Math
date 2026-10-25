"""Isolated unmodified current verifier replay; archived opinions remain opaque."""
from pathlib import Path
from datetime import datetime,timezone
import shutil,subprocess,sys,json,hashlib,time,os

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[1]/'sources/published-source'
COPY=ROOT/'cache/replay-publication'
COPY.parent.mkdir(exist_ok=True)
shutil.copytree(SOURCE,COPY)
inputs={str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.rglob('*') if p.is_file()}
(ROOT/'replay-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
out={'started_utc':datetime.now(timezone.utc).isoformat(),'runtime':sys.executable,'copied_files':len(inputs),'runs':[]}
env=os.environ.copy();env.update({'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
for label,args,expected in [
 ('default',['verification/verify_all.py'],0),
 ('optional-matrix',['verification/optional_matrix_diagnostics.py'],0),
 ('optional-reject-optimized',['-O','verification/optional_matrix_diagnostics.py'],1)
]:
    start=time.monotonic();p=subprocess.run([sys.executable,'-B',*args],cwd=COPY,env=env,capture_output=True,text=True)
    (ROOT/('replay-'+label+'.stdout.txt')).write_text(p.stdout)
    (ROOT/('replay-'+label+'.stderr.txt')).write_text(p.stderr)
    assert p.returncode==expected,(label,p.returncode,p.stderr)
    out['runs'].append({'label':label,'arguments':args,'seconds':time.monotonic()-start,'exit_code':p.returncode,'expected_exit_code':expected})
    (ROOT/'replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(label,p.returncode,flush=True)
assert all(hashlib.sha256((SOURCE/n).read_bytes()).hexdigest()==h for n,h in inputs.items())
out['completed_utc']=datetime.now(timezone.utc).isoformat();out['status']='PASS';out['sources_unchanged']=True
(ROOT/'replay.json').write_text(json.dumps(out,indent=2)+'\n')
