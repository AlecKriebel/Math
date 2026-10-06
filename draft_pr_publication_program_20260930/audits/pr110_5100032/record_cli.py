#!/usr/bin/env python3
"""Record actual, nonsecret CLI executions for this PR effort."""
from pathlib import Path
import sys,subprocess,json,hashlib,datetime,os
A=Path(__file__).resolve().parent
label=sys.argv[1];args=sys.argv[2:]
if not label.replace('_','').replace('-','').isalnum() or not args: raise ValueError('label/argv')
D=A/'actual_operations'/label
D.mkdir(parents=True,exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
start=now()
(D/'started.json').write_text(json.dumps({'UTC_start':start,'recorder_PID':os.getpid(),'argv':args,'cwd':os.getcwd()},indent=2)+'\n')
try:
 p=subprocess.Popen(args,cwd=os.getcwd(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
except OSError as exc:
 (D/'spawn_failure.json').write_text(json.dumps({'UTC':now(),'recorder_PID':os.getpid(),'child_PID':None,'error':str(exc)},indent=2)+'\n')
 raise
out,err=p.communicate()
(D/'stdout.bin').write_bytes(out);(D/'stderr.bin').write_bytes(err)
r={'UTC_start':start,'UTC_end':now(),'recorder_PID':os.getpid(),'child_PID':p.pid,'argv':args,'cwd':os.getcwd(),'exit_code':p.returncode,
   'stdout':{'path':'stdout.bin','bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},
   'stderr':{'path':'stderr.bin','bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
(D/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'label':label,'child_PID':p.pid,'exit_code':p.returncode,'stdout_bytes':len(out),'stderr_bytes':len(err),'directory':str(D)}))
if p.returncode:print(err.decode('utf-8','replace')[:1000],file=sys.stderr)
sys.exit(p.returncode)
