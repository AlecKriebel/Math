#!/usr/bin/env python3
"""First-party real subprocess capture; metadata is written before child launch."""
import hashlib,json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
BASE=Path(__file__).resolve().parent
def now(): return datetime.now(timezone.utc).isoformat()
def bind(p):
 p=Path(p).resolve(); b=p.read_bytes()
 return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode':p.stat().st_mode&0o7777}
def capture(name,argv,cwd,inputs=()):
 dest=BASE/name; dest.mkdir(exist_ok=False)
 own=Path(__file__).read_bytes();(dest/'prelaunch_operator.py').write_bytes(own)
 source_copies=[]
 for i,p in enumerate(inputs):
  p=Path(p)
  if p.suffix=='.py':
   q=dest/('prelaunch_source_'+str(i)+'.py');q.write_bytes(p.read_bytes());source_copies.append({'original':bind(p),'copy':bind(q)})
 pre={'schema':'pr47-cover-real-prelaunch/v1','name':name,'prepared_utc':now(),'operator_pid':os.getpid(),'argv':list(argv),'cwd':str(Path(cwd).resolve()),'operator':bind(dest/'prelaunch_operator.py'),'inputs':[bind(p) for p in inputs],'prelaunch_source_copies':source_copies,'environment':{k:os.environ.get(k) for k in ('PATH','PYTHONPATH','PYTHONDONTWRITEBYTECODE')}}
 (dest/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
 start=now(); child=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 stdout,stderr=child.communicate();end=now()
 (dest/'stdout.bin').write_bytes(stdout);(dest/'stderr.bin').write_bytes(stderr)
 receipt={'schema':'pr47-cover-completed-capture/v1','prelaunch':bind(dest/'PRELAUNCH.json'),'actual_child_pid':child.pid,'operator_pid':os.getpid(),'started_utc':start,'finished_utc':end,'returncode':child.returncode,'completed':True,'argv':list(argv),'cwd':str(Path(cwd).resolve()),'stdout':bind(dest/'stdout.bin'),'stderr':bind(dest/'stderr.bin'),'inputs_unchanged':[bind(p)==a for p,a in zip(inputs,pre['inputs'])]}
 (dest/'CAPTURE.json').write_text(json.dumps(receipt,indent=2)+'\n')
 return receipt
if __name__=='__main__':
 print(json.dumps(capture(sys.argv[1],sys.argv[3:],sys.argv[2],tuple(Path(x) for x in sys.argv[3:] if Path(x).is_file())),indent=2))
