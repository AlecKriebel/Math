from pathlib import Path
import datetime as dt,subprocess,hashlib,json,sys
O=Path(__file__).resolve().parent;p=O/'independent_static_controls.py';source=p.read_bytes();started=dt.datetime.now(dt.timezone.utc).isoformat()
proc=subprocess.Popen([sys.executable,str(p)],cwd='/Users/alec/Documents/Math',stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate();finished=dt.datetime.now(dt.timezone.utc).isoformat()
(O/'controls.stdout').write_bytes(out);(O/'controls.stderr').write_bytes(err)
x={'schema':'own-static-control-execution/v1','actual_own_control_execution':True,'reviewed_helper_execution':False,'pid':proc.pid,'argv':[sys.executable,str(p)],'cwd':'/Users/alec/Documents/Math','started_utc':started,'finished_utc':finished,'exit_code':proc.returncode,'source':{'path':p.name,'bytes':len(source),'sha256':hashlib.sha256(source).hexdigest()},'stdout':{'path':'controls.stdout','bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'path':'controls.stderr','bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
(O/'CONTROL_EXECUTION.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print(out.decode());print(err.decode());print('OWN_CONTROL_EXIT',proc.returncode)
