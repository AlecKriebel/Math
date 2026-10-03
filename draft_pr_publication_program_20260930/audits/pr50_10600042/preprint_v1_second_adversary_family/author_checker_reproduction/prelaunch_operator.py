from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
base=Path(__file__).absolute().parent
name=sys.argv[1]; source=Path(sys.argv[2]); args=sys.argv[3:]
dest=base/name;dest.mkdir(exist_ok=False)
def now():return datetime.now(timezone.utc).isoformat()
def ref(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(dest/'prelaunch_source.py').write_bytes(source.read_bytes())
(dest/'prelaunch_operator.py').write_bytes(Path(__file__).read_bytes())
argv=[sys.executable,'-B',str(source)]+args
pre={'argv':argv,'cwd':str(base),'operator_pid':os.getpid(),'prepared_utc':now(),'source':ref(source),'operator':ref(Path(__file__))}
(dest/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
start=now()
with (dest/'stdout.bin').open('xb') as out,(dest/'stderr.bin').open('xb') as err:
 child=subprocess.Popen(argv,cwd=base,stdout=out,stderr=err,stdin=subprocess.DEVNULL)
 code=child.wait()
finish=now()
cap={'schema':'pr50-second-adversary-actual-private-capture/v1','actual_execution':True,'completed':True,'argv':argv,'cwd':str(base),'operator_pid':os.getpid(),'child_pid':child.pid,'started_utc':start,'finished_utc':finish,'exit_code':code,'source_unchanged':ref(source)==pre['source'],'operator_unchanged':ref(Path(__file__))==pre['operator'],'stdout':ref(dest/'stdout.bin'),'stderr':ref(dest/'stderr.bin')}
(dest/'CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n')
print(json.dumps(cap,indent=2))
if code:raise SystemExit(code)
