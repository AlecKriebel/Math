from pathlib import Path
from datetime import datetime, timezone
import subprocess,json,sys,os
base=Path(__file__).resolve().parent
label=sys.argv[1]; args=sys.argv[2:]
start=datetime.now(timezone.utc).isoformat()
stdin_data = sys.stdin.read() if '-' in args else None
child=subprocess.Popen(args,stdin=subprocess.PIPE if stdin_data is not None else None,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,cwd=base)
stdout,stderr=child.communicate(stdin_data)
r=subprocess.CompletedProcess(args,child.returncode,stdout,stderr)
d=base/'private'/'commands';d.mkdir(parents=True,exist_ok=True)
(d/(label+'.stdout')).write_text(r.stdout); (d/(label+'.stderr')).write_text(r.stderr)
m={'operator_pid':os.getpid(),'child_pid':child.pid,'label':label,'argv':args,'cwd':str(base),'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,'stdout_file':str((d/(label+'.stdout')).relative_to(base)),'stderr_file':str((d/(label+'.stderr')).relative_to(base))}
if stdin_data is not None:
 (d/(label+'.stdin')).write_text(stdin_data)
 m['stdin_file']=str((d/(label+'.stdin')).relative_to(base))
(d/(label+'.json')).write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps(m));print(r.stdout);print(r.stderr,file=sys.stderr)
sys.exit(r.returncode)
