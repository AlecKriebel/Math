#!/usr/bin/env python3
from pathlib import Path
import datetime,json,os,signal,subprocess,sys
O=Path(__file__).resolve().parent
process=subprocess.Popen([sys.executable,str(O/'check_exact.py')],cwd=O,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
timed_out=False
try:out,err=process.communicate(timeout=45)
except subprocess.TimeoutExpired:
 timed_out=True;os.killpg(process.pid,signal.SIGTERM)
 try:out,err=process.communicate(timeout=2)
 except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);out,err=process.communicate(timeout=2)
row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout_seconds':45,'process_group_cleanup_on_timeout':True,'timed_out':timed_out,'returncode':process.returncode,'stdout':out,'stderr':err}
(O/'exact-run.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row));sys.exit(1 if timed_out or process.returncode else 0)
