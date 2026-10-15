"""Own actual control launch, preserving source before execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
root=Path(__file__).resolve().parent
src=root/sys.argv[1];run=root/sys.argv[2];run.mkdir(exist_ok=False)
def utc():return datetime.now(timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(run/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
(run/'PRELAUNCH_SOURCE.py').write_bytes(src.read_bytes())
source=pin(run/'PRELAUNCH_SOURCE.py');started=utc()
argv=[sys.executable,'-B',str(src)]
p=subprocess.Popen(argv,cwd=root,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate();finished=utc()
(run/'stdout.bin').write_bytes(out);(run/'stderr.bin').write_bytes(err)
record={'schema':'OWN_GENUINE_CONTROL_CAPTURE_v1','actual_execution':True,'pid':p.pid,'operator_pid':os.getpid(),'started_utc':started,'finished_utc':finished,'argv':argv,'cwd':str(root),'stdin_supplied':False,'exit_code':p.returncode,'source':source,'source_unchanged':src.read_bytes()==(run/'PRELAUNCH_SOURCE.py').read_bytes(),'stdout':pin(run/'stdout.bin'),'stderr':pin(run/'stderr.bin'),'completed':True}
(run/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
sys.exit(p.returncode)
