from pathlib import Path
import subprocess,sys,os,json,hashlib
from datetime import datetime,timezone
base=Path(__file__).resolve().parent
operator=base/'reproduce_package.py'
def utc():return datetime.now(timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
pre={'capture_pid':os.getpid(),'start_utc':utc(),'argv':[sys.executable,'-B',str(operator)],'cwd':str(base),'prelaunch_operator':pin(operator.read_bytes()),'launcher':pin(Path(__file__).read_bytes())}
(base/'OPERATOR_PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
p=subprocess.Popen(pre['argv'],cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate(timeout=120)
(base/'operator.stdout.bin').write_bytes(out);(base/'operator.stderr.bin').write_bytes(err)
cap=dict(pre,operator_pid=p.pid,end_utc=utc(),exit_code=p.returncode,stdout=pin(out),stderr=pin(err),actual_execution=True)
(base/'OPERATOR_CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n')
print(json.dumps(cap,indent=2));print(out.decode());print(err.decode());sys.exit(p.returncode)
