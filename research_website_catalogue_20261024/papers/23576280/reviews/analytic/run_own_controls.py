from pathlib import Path
import subprocess,os,signal,time,json
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');O=Path(__file__).resolve().parent;start=time.time();p=subprocess.Popen([str(P/'tmp/shared-math-runtime/bin/python'),'-I','-B',str(O/'independent_controls.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
try:
 out,err=p.communicate(timeout=25);result={'returncode':p.returncode,'stdout':out,'stderr':err,'elapsed_seconds':time.time()-start}
except subprocess.TimeoutExpired:
 os.killpg(p.pid,signal.SIGKILL);out,err=p.communicate();result={'timeout':True,'stdout':out,'stderr':err}
finally:
 try:os.killpg(p.pid,signal.SIGKILL)
 except ProcessLookupError:pass
result.update({'watchdog_seconds':25,'start_new_session':True,'descendant_cleanup':'SIGKILL process group attempted in finally'});(O/'CONTROL_PROCESS_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
