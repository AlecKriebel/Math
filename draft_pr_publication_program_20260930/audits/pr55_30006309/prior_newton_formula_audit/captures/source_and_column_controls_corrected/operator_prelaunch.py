#!/usr/bin/python3
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
name=sys.argv[1]
assert '/' not in name and name not in ('.','..')
script=ROOT/sys.argv[2]
inputs=[script]+[ROOT/p for p in sys.argv[3:]]
out=ROOT/'captures'/name
out.mkdir(parents=True,exist_ok=False)
def row(p):
 b=p.read_bytes();return {'path':str(p),'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(p.stat().st_mode&0o7777,'04o')}
operator_bytes=Path(__file__).read_bytes();(out/'operator_prelaunch.py').write_bytes(operator_bytes)
source_rows=[]
for i,p in enumerate(inputs):
 p=p.resolve();r=row(p);r['prelaunch_copy']=str(out/('source_prelaunch_'+str(i)+p.suffix));Path(r['prelaunch_copy']).write_bytes(p.read_bytes());source_rows.append(r)
argv=['/usr/bin/python3','-B',str(script)]
started=datetime.now(timezone.utc).isoformat()
child=subprocess.Popen(argv,cwd=str(ROOT),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr=child.communicate();ended=datetime.now(timezone.utc).isoformat()
(out/'stdout.bin').write_bytes(stdout);(out/'stderr.bin').write_bytes(stderr)
cap={'schema':'actual-independent-subprocess-v1','operator_pid':os.getpid(),'child_pid':child.pid,'argv':argv,'cwd':str(ROOT),'started_at_utc':started,'ended_at_utc':ended,'exit_code':child.returncode,'operator_sha256':hashlib.sha256(operator_bytes).hexdigest(),'source_prelaunch':source_rows,'source_after_unchanged':all(row(Path(r['path']))=={k:r[k] for k in ('path','size','sha256','mode')} for r in source_rows),'stdout':row(out/'stdout.bin'),'stderr':row(out/'stderr.bin'),'acceptance_authority':False}
(out/'CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n')
print(json.dumps(cap,indent=2))
print(stdout.decode(errors='replace'));print(stderr.decode(errors='replace'),file=sys.stderr)
sys.exit(child.returncode)
