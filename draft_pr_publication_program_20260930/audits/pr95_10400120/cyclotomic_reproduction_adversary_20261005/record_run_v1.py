#!/usr/bin/env python3
import sys,json,subprocess,hashlib,os
from pathlib import Path
from datetime import datetime,timezone
base=Path(__file__).resolve().parent
label,cwd,*argv=sys.argv[1:]
out=base/'runs'/label;out.mkdir(parents=True,exist_ok=True)
def utc():return datetime.now(timezone.utc).isoformat()
def hashes():
 return {str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(base.rglob('*.py')) if 'runs' not in p.relative_to(base).parts}
start=utc(); before=hashes()
with (out/'stdout.txt').open('wb') as so,(out/'stderr.txt').open('wb') as se:
 child=subprocess.Popen(argv,cwd=cwd,stdout=so,stderr=se)
 pid=child.pid
 receipt={'label':label,'actual_argv':argv,'actual_child_PID':pid,'actual_launcher_PID':os.getpid(),'actual_cwd':str(Path(cwd).resolve()),'utc_start':start,'source_sha256_before':before,'environment_note':'No PYTHONPATH injection; child inherits native environment; Python invoked with -E -B.'}
 (out/'running_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 status=child.wait()
receipt.update(utc_end=utc(),exit_code=status,source_sha256_after=hashes())
for kind in ['stdout','stderr']:
 data=(out/(kind+'.txt')).read_bytes();receipt[kind+'_bytes']=len(data);receipt[kind+'_sha256']=hashlib.sha256(data).hexdigest()
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');(out/'running_receipt.json').unlink()
print(json.dumps({'label':label,'actual_child_PID':pid,'exit_code':status,'stdout_bytes':receipt['stdout_bytes'],'stderr_bytes':receipt['stderr_bytes']}))
