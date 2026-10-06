#!/usr/bin/env python3
"""Capture only this family's independently authored source/finite controls."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def record(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
receipts=[]
for name in ('source_provenance_control','independent_finite_controls'):
 stdout=R/'streams'/f'{name}.stdout';stderr=R/'streams'/f'{name}.stderr';begin=now();args=[sys.executable,str(R/f'{name}.py')]
 with stdout.open('wb') as out,stderr.open('wb') as err:
  p=subprocess.Popen(args,cwd=R,stdout=out,stderr=err);pid=p.pid;code=p.wait(timeout=90)
 receipts.append({'name':name,'argv':args,'cwd':str(R),'pid':pid,'started_utc':begin,'completed_utc':now(),'returncode':code,'stdout':record(stdout),'stderr':record(stderr),'authored_input':record(R/f'{name}.py')})
 if code:raise RuntimeError(f'{name} exited {code}')
(R/'independent_run_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps({'receipts':receipts},indent=2))
