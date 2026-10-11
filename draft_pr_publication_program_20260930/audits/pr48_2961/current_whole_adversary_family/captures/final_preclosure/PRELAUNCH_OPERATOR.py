"""Capture only this reviewer's own explicitly named private child."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, subprocess, sys, traceback
F = Path(__file__).absolute().parent
def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
def digest(b): return hashlib.sha256(b).hexdigest()
def encode(x): return (json.dumps(x, indent=2, allow_nan=False) + '\n').encode()
assert __debug__ and not sys.flags.optimize
name, source_name = sys.argv[1:3]
assert name.replace('_','').isalnum() and '/' not in source_name
source = F/source_name
assert source.is_file() and not source.is_symlink()
body=source.read_bytes(); operator=Path(__file__).read_bytes()
out=F/'captures'/name; out.mkdir(parents=True, exist_ok=False)
(out/'PRELAUNCH_SOURCE.py').write_bytes(body)
(out/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
argv=['/usr/bin/python3','-B',str(source),*sys.argv[3:]]
record={'schema':'pr48-whole-independent-private-actual-capture/v1',
 'operator_pid':os.getpid(),'argv':argv,'cwd':str(F),'started_utc':stamp(),
 'source_sha256':digest(body),'operator_sha256':digest(operator),
 'actual_execution':False,'completed':False,'pid':None,'exit_code':None,
 'stdin_supplied':False,'production_builder_or_operator_run':False}
(out/'PRELAUNCH.json').write_bytes(encode(record))
try:
 with (out/'stdout.bin').open('xb') as so, (out/'stderr.bin').open('xb') as se:
  child=subprocess.Popen(argv,cwd=F,stdin=subprocess.DEVNULL,stdout=so,stderr=se,
    env=dict(os.environ,PYTHONOPTIMIZE='0',GIT_OPTIONAL_LOCKS='0'))
  record.update(actual_execution=True,pid=child.pid)
  try: record['exit_code']=child.wait(timeout=300); record['completed']=True
  except BaseException: child.kill(); record['exit_code']=child.wait(); raise
except BaseException: record['failure']=traceback.format_exc()
finally:
 record['finished_utc']=stamp()
 for channel in ['stdout','stderr']:
  p=out/(channel+'.bin')
  if p.exists():
   b=p.read_bytes(); record[channel]={'path':p.name,'bytes':len(b),'sha256':digest(b)}
 record['source_unchanged_after_child']=source.read_bytes()==body
 record['operator_unchanged_after_child']=Path(__file__).read_bytes()==operator
 record['future_acceptance_approved']=False
 (out/'CAPTURE.json').write_bytes(encode(record))
print(json.dumps(record,indent=2))
sys.exit(0 if record['completed'] is True and record['exit_code']==0 else 1)
