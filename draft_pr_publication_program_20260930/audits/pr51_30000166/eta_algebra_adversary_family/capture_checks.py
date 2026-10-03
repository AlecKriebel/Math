#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import os,subprocess,json,hashlib,stat
f=Path(__file__).resolve().parent
p=f/'independent_exact_checks.py'
c=f/'exact_checks_capture';c.mkdir(exist_ok=False)
b=p.read_bytes();(c/'SOURCE_PRELAUNCH.py').write_bytes(b)
def binding(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':oct(stat.S_IMODE(p.stat().st_mode))}
start=datetime.now(timezone.utc).isoformat()
argv=['/usr/bin/python3','-B',str(p)]
(c/'PRELAUNCH.json').write_text(json.dumps({'started_utc':start,'argv':argv,'cwd':str(f),'operator_pid':os.getpid(),'source':binding(p)},indent=2)+'\n')
with (c/'stdout.bin').open('wb') as out,(c/'stderr.bin').open('wb') as err:
 proc=subprocess.Popen(argv,cwd=f,stdout=out,stderr=err)
 code=proc.wait()
end=datetime.now(timezone.utc).isoformat()
result={'status':'PASS' if code==0 else 'FAIL','started_utc':start,'ended_utc':end,'operator_pid':os.getpid(),'child_pid':proc.pid,'exit_code':code,'argv':argv,'cwd':str(f),'source_unchanged':p.read_bytes()==b,'source':binding(p),'stdout':binding(c/'stdout.bin'),'stderr':binding(c/'stderr.bin')}
(c/'CAPTURE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));print((c/'stdout.bin').read_text());print((c/'stderr.bin').read_text())
raise SystemExit(code)
