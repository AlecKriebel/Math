"""Preserve this family's actual new acceptance-control process evidence."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
OWN=Path(__file__).resolve().parent
CAP=OWN/'actual_acceptance_controls_001'
CAP.mkdir(exist_ok=False)
source=(OWN/'independent_acceptance_controls.py').read_bytes(); operator=Path(__file__).read_bytes()
(CAP/'PRELAUNCH_SOURCE.py').write_bytes(source); (CAP/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (CAP/'stdout.bin').open('wb') as out,(CAP/'stderr.bin').open('wb') as err:
    p=subprocess.Popen([sys.executable,str(CAP/'PRELAUNCH_SOURCE.py')],cwd=OWN,stdout=out,stderr=err)
    code=p.wait()
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
r={'actual_parent_pid':os.getpid(),'actual_child_pid':p.pid,'actual_start_utc':start,'actual_end_utc':end,
   'exit_code':code,'argv':[sys.executable,str(CAP/'PRELAUNCH_SOURCE.py')],'cwd':str(OWN),
   'prelaunch_source_sha256':hashlib.sha256(source).hexdigest(),'prelaunch_operator_sha256':hashlib.sha256(operator).hexdigest(),
   'capture_complete_after_child_exit':True,'foreign_source_executed':False}
for ch in ['stdout','stderr']:
    b=(CAP/(ch+'.bin')).read_bytes();r[ch]={'path':str(CAP/(ch+'.bin')),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(CAP/'CAPTURE.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2));print((CAP/'stdout.bin').read_text());print((CAP/'stderr.bin').read_text())
raise SystemExit(code)
