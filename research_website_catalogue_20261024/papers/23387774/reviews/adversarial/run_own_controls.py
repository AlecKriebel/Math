import subprocess,os,signal,time,json,datetime
from pathlib import Path
p=Path(__file__).resolve().parent; start=time.monotonic(); process=None
try:
 process=subprocess.Popen(['/Users/alec/Documents/Math/research_website_catalogue_20261024/tmp/shared-math-runtime/bin/python','-I','-B',str(p/'independent_controls.py')],cwd=p/'cache',stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 out,err=process.communicate(timeout=25)
 (p/'own_controls.stdout.json').write_text(out); (p/'own_controls.stderr.txt').write_text(err)
 receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start,'returncode':process.returncode,'timeout_seconds':25,'process_group_cleanup':'SIGKILL finally, including descendants'}
except subprocess.TimeoutExpired:
 receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start,'timed_out':True}
finally:
 if process:
  try: os.killpg(process.pid,signal.SIGKILL)
  except ProcessLookupError: pass
 (p/'own_controls_run.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
