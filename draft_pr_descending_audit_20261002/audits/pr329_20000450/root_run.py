"""Retain actual command streams and contemporaneous timestamps, never a verdict."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,hashlib,json,sys
A=Path(__file__).resolve().parent
assert len(sys.argv)>=4 and sys.argv[2]=='--'
name=sys.argv[1];assert name.replace('_','').isalnum()
D=A/'root_runs_private'/name;D.mkdir(parents=True,exist_ok=False)
args=sys.argv[3:]
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
j={'argv':args,'cwd':str(A),'started_utc':utc(),'driver_sha256':sha(Path(__file__).read_bytes())}
for x in args:
    p=Path(x)
    if p.is_file() and p.suffix=='.py':j.setdefault('programs',[]).append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
(D/'execution_spec.json').write_text(json.dumps(j,indent=2)+'\n')
with (D/'stdout.bin').open('wb') as out,(D/'stderr.bin').open('wb') as err:
    r=subprocess.run(args,cwd=A,stdout=out,stderr=err)
j.update(ended_utc=utc(),exit_code=r.returncode)
for k in ['stdout','stderr']:
    b=(D/(k+'.bin')).read_bytes();j[k+'_bytes']=len(b);j[k+'_sha256']=sha(b)
(D/'execution.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2))
for k in ['stdout','stderr']:
    b=(D/(k+'.bin')).read_bytes()
    if len(b)<=16000:print(b.decode(errors='replace'))
    else:print('Retained complete '+k+'; '+str(len(b))+'bytes require direct file read.')
sys.exit(r.returncode)
