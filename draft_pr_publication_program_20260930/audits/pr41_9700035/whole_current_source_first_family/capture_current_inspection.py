#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
r=Path(__file__).resolve().parent;source=r/'inspect_whole_current.py';cap=r/'whole_current_actual_capture';cap.mkdir(exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def row(p):
 b=p.read_bytes();return {'path':p.relative_to(r).as_posix(),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(cap/'PRELAUNCH_SOURCE.py').write_bytes(source.read_bytes());args=[sys.executable,'-B',str(source)];start=now()
with (cap/'stdout.bin').open('wb') as out,(cap/'stderr.bin').open('wb') as err:
 p=subprocess.Popen(args,cwd=r,stdin=subprocess.DEVNULL,stdout=out,stderr=err);pid=p.pid;code=p.wait(timeout=180)
receipt={'argv':args,'cwd':str(r),'source':row(cap/'PRELAUNCH_SOURCE.py'),'pid':pid,'started_utc':start,'finished_utc':now(),'actual_execution':True,'completed':True,'stdin_supplied':False,'returncode':code,'stdout':row(cap/'stdout.bin'),'stderr':row(cap/'stderr.bin')}
(cap/'CAPTURE.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
