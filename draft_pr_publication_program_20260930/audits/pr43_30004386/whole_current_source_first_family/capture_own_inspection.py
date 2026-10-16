"""Capture only this family's newly handwritten reader, with real process clocks."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

OWN = Path(__file__).resolve().parent
CAPTURE = OWN / 'actual_whole_inspection_001'
CAPTURE.mkdir(exist_ok=False)
operator = Path(__file__).resolve().read_bytes()
source = (OWN/'inspect_whole_source.py').read_bytes()
(CAPTURE/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
(CAPTURE/'PRELAUNCH_READER.py').write_bytes(source)
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (CAPTURE/'stdout.bin').open('wb') as out, (CAPTURE/'stderr.bin').open('wb') as err:
    child = subprocess.Popen([sys.executable,str(CAPTURE/'PRELAUNCH_READER.py')],cwd=OWN,stdout=out,stderr=err)
    code = child.wait()
end = datetime.datetime.now(datetime.timezone.utc).isoformat()
record = {'actual_parent_pid':os.getpid(),'actual_child_pid':child.pid,
          'actual_start_utc':start,'actual_end_utc':end,'exit_code':code,
          'command':[sys.executable,str(CAPTURE/'PRELAUNCH_READER.py')],
          'cwd':str(OWN),'prelaunch_reader_sha256':hashlib.sha256(source).hexdigest(),
          'prelaunch_operator_sha256':hashlib.sha256(operator).hexdigest(),
          'stdout':{'path':str(CAPTURE/'stdout.bin'),'bytes':(CAPTURE/'stdout.bin').stat().st_size,'sha256':hashlib.sha256((CAPTURE/'stdout.bin').read_bytes()).hexdigest()},
          'stderr':{'path':str(CAPTURE/'stderr.bin'),'bytes':(CAPTURE/'stderr.bin').stat().st_size,'sha256':hashlib.sha256((CAPTURE/'stderr.bin').read_bytes()).hexdigest()},
          'foreign_source_executed':False,'capture_complete_after_child_exit':True}
(CAPTURE/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
print((CAPTURE/'stdout.bin').read_text(errors='replace'))
print((CAPTURE/'stderr.bin').read_text(errors='replace'))
raise SystemExit(code)
