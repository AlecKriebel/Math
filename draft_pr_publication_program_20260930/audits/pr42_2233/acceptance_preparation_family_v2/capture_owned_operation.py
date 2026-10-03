"""Own adjacent source author/control capture; no proposed source execution."""
from pathlib import Path
import subprocess,sys,datetime,json,hashlib,os
H=Path(__file__).resolve().parent
name=sys.argv[1];source=H/sys.argv[2]
if source.parent!=H or name not in {'AUTHORING_ACTUAL_CAPTURE','DATED_NATIVE_REVISION_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE'}:raise ValueError('Own sources only')
C=H/name;C.mkdir(exist_ok=False)
raw=source.read_bytes();(C/'PRELAUNCH_SOURCE.py').write_bytes(raw)
sha=lambda b:hashlib.sha256(b).hexdigest()
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
argv=[sys.executable,'-B',str(source)];started=stamp()
with (C/'stdout.bin').open('xb') as out,(C/'stderr.bin').open('xb') as err:
    child=subprocess.Popen(argv,cwd=H,stdin=subprocess.DEVNULL,stdout=out,stderr=err);code=child.wait()
finished=stamp();pins=[]
for n in ['stdout.bin','stderr.bin']:
    b=(C/n).read_bytes();pins.append({'path':n,'bytes':len(b),'sha256':sha(b)})
record={'schema':'pr42-own-source-operation-capture/v1','actual_execution':True,'completed':True,'pid':child.pid,'argv':argv,'cwd':str(H),'started_utc':started,'finished_utc':finished,'exit_code':code,'status':'PASS' if code==0 else 'FAIL','stdin_supplied':False,'source_sha256':sha(raw),'source_unchanged':source.read_bytes()==raw,'stdout':pins[0],'stderr':pins[1],'proposed_acceptance_helpers_executed':False,'science_helpers_executed':False,'native_Git_remote_people_mutations':False}
(C/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record));sys.exit(code)
