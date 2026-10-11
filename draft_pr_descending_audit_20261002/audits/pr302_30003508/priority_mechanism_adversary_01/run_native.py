#!/usr/bin/env python3
"""Retain complete actual native process custody for this read-only family."""
import datetime, hashlib, json, os, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    p = pathlib.Path(p)
    if not p.is_file(): return None
    b=p.read_bytes()
    return {'path':str(p), 'resolved_path':str(p.resolve()), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest(), 'mode':oct(p.stat().st_mode & 0o777)}
label=sys.argv[1]; argv=sys.argv[2:]
dest=ROOT/'process_evidence'/label
dest.mkdir(exist_ok=False)
source=pathlib.Path(__file__)
(dest/'executed_recorder.py').write_bytes(source.read_bytes())
exe=shutil.which(argv[0]) or argv[0]
record={'label':label,'recorder_pid':os.getpid(),'argv':argv,'cwd':str(ROOT),'started_utc':now(),'recorder_source':pin(source),'executed_recorder':pin(dest/'executed_recorder.py'),'executable':pin(exe),'argument_file_pins':[pin(a) for a in argv[1:] if pathlib.Path(a).is_absolute() and pathlib.Path(a).is_file()]}
try:
    child=subprocess.Popen(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    record['actual_pid']=child.pid
    out,err=child.communicate(); record['exit_code']=child.returncode
except Exception as e:
    record['launch_failure']=repr(e); out=b'';err=str(e).encode(); record['exit_code']=None
record['ended_utc']=now()
for name,b in [('stdout.bin',out),('stderr.bin',err)]:
    p=dest/name;p.write_bytes(b);record[name]=pin(p)
(dest/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'label':label,'actual_pid':record.get('actual_pid'),'exit_code':record['exit_code'],'stdout_bytes':len(out),'stderr_bytes':len(err),'receipt':str(dest/'execution.json')}))
sys.exit(record['exit_code'] if record['exit_code'] is not None else 125)
