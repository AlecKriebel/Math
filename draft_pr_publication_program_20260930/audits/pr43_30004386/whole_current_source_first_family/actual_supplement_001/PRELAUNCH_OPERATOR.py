"""Capture only this family's ancillary read program, keeping complete evidence."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
P=Path(__file__).resolve().parent;D=P/'actual_supplement_001';D.mkdir(exist_ok=False)
src=(P/'supplemental_closed_inputs.py').read_bytes();op=Path(__file__).read_bytes()
(D/'PRELAUNCH_SOURCE.py').write_bytes(src);(D/'PRELAUNCH_OPERATOR.py').write_bytes(op)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (D/'stdout.bin').open('wb') as out,(D/'stderr.bin').open('wb') as err:
    child=subprocess.Popen([sys.executable,str(D/'PRELAUNCH_SOURCE.py')],cwd=P,stdout=out,stderr=err);code=child.wait()
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
r={'actual_parent_pid':os.getpid(),'actual_child_pid':child.pid,'actual_start_utc':start,'actual_end_utc':end,'exit_code':code,'argv':[sys.executable,str(D/'PRELAUNCH_SOURCE.py')],'cwd':str(P),'prelaunch_source_sha256':hashlib.sha256(src).hexdigest(),'prelaunch_operator_sha256':hashlib.sha256(op).hexdigest(),'complete_after_child_exit':True,'foreign_source_executed':False}
for ch in ['stdout','stderr']:
    b=(D/(ch+'.bin')).read_bytes();r[ch]={'path':str(D/(ch+'.bin')),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(D/'CAPTURE.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));print((D/'stdout.bin').read_text());print((D/'stderr.bin').read_text());raise SystemExit(code)
