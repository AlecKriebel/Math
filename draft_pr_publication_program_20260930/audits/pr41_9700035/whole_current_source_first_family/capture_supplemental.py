#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
r=Path(__file__).resolve().parent;s=r/'supplemental_readonly_controls.py';c=r/'supplemental_actual_capture';c.mkdir(exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def row(p):
 b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(c/'PRELAUNCH_SOURCE.py').write_bytes(s.read_bytes());argv=[sys.executable,'-B',str(s)];start=now()
with (c/'stdout.bin').open('wb') as out,(c/'stderr.bin').open('wb') as err:
 p=subprocess.Popen(argv,cwd=r,stdin=subprocess.DEVNULL,stdout=out,stderr=err);pid=p.pid;code=p.wait(timeout=180)
obj={'argv':argv,'cwd':str(r),'source':row(c/'PRELAUNCH_SOURCE.py'),'pid':pid,'started_utc':start,'finished_utc':now(),'actual_execution':True,'completed':True,'stdin_supplied':False,'returncode':code,'stdout':row(c/'stdout.bin'),'stderr':row(c/'stderr.bin')};(c/'CAPTURE.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps(obj,indent=2))
