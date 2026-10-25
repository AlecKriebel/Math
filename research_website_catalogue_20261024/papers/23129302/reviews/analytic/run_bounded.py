#!/usr/bin/env python3
"""Bounded process-group runner for owned independent controls only."""
import datetime,json,os,signal,subprocess,sys
from pathlib import Path
O=Path(__file__).resolve().parent
target=O/sys.argv[1]
if target.name not in {'check_exact.py','check_probability.py'}:raise ValueError('Not an owned control')
process=subprocess.Popen([sys.executable,str(target)],cwd=O,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
timed_out=False
try:out,err=process.communicate(timeout=45)
except subprocess.TimeoutExpired:
 timed_out=True;os.killpg(process.pid,signal.SIGTERM)
 try:out,err=process.communicate(timeout=2)
 except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);out,err=process.communicate(timeout=2)
row={'script':target.name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout_seconds':45,'process_group_cleanup_on_timeout':True,'timed_out':timed_out,'returncode':process.returncode,'stdout':out,'stderr':err}
(O/(target.stem+'-run.json')).write_text(json.dumps(row,indent=2)+'\n')
print(json.dumps(row))
sys.exit(1 if timed_out or process.returncode else 0)
