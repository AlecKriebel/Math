import argparse,subprocess,datetime,os,json,sys
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument('--receipt',required=True);a.add_argument('--cwd',required=True);a.add_argument('command',nargs=argparse.REMAINDER);v=a.parse_args();cmd=v.command[1:] if v.command[:1]==['--'] else v.command
r={'runner_pid':os.getpid(),'runner_argv':[sys.executable,*sys.argv],'cwd':v.cwd,'argv':cmd,'UTC_start':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 p=subprocess.Popen(cmd,cwd=v.cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);r['pid']=p.pid
except BaseException as exc:
 import traceback
 r.update(pid=None,UTC_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit=1,stdout='',stderr=traceback.format_exc());Path(v.receipt).write_text(json.dumps(r,indent=2));sys.stderr.write(r['stderr']);sys.exit(1)
s,e=p.communicate();r.update(UTC_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit=p.returncode,stdout=s.decode('utf-8','replace'),stderr=e.decode('utf-8','replace'))
Path(v.receipt).write_text(json.dumps(r,indent=2));sys.stdout.buffer.write(s);sys.stderr.buffer.write(e);sys.exit(p.returncode)
