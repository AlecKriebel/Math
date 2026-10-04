"""Capture only this family's own independent controls, with real prelaunch."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,traceback
D=Path(__file__).absolute().parent
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
src=D/'independent_whole_controls.py';run=D/('actual_controls_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'));run.mkdir()
a=src.read_bytes();o=Path(__file__).read_bytes();(run/'PRELAUNCH_SOURCE.py').write_bytes(a);(run/'PRELAUNCH_OPERATOR.py').write_bytes(o)
argv=['/usr/bin/python3','-B',str(src)]
rec={'schema':'pr44-own-actual-source-first-capture/v1','operator_pid':os.getpid(),'argv':argv,'cwd':str(D),'started_utc':stamp(),'source_sha256':sha(a),'operator_sha256':sha(o),'stdin_supplied':False,'actual_execution':False,'completed':False,'pid':None,'exit_code':None}
dump(run/'PRELAUNCH.json',rec)
try:
    with (run/'stdout.bin').open('xb') as out,(run/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(argv,cwd=D,stdin=subprocess.DEVNULL,stdout=out,stderr=err);rec['pid']=child.pid;rec['actual_execution']=True;rec['exit_code']=child.wait(timeout=60);rec['completed']=True
except BaseException:rec['failure']=traceback.format_exc()
finally:
    rec['finished_utc']=stamp();rec['source_unchanged']=src.read_bytes()==a;rec['operator_unchanged']=Path(__file__).read_bytes()==o
    for k in ['stdout','stderr']:
        p=run/(k+'.bin');b=p.read_bytes() if p.exists() else b'';rec[k]={'path':p.name,'bytes':len(b),'sha256':sha(b)}
    rec['status']='PASS_OWN_CONTROLS' if rec['exit_code']==0 and rec['completed'] and rec['source_unchanged'] and rec['operator_unchanged'] else 'FAILED_OWN_RUN_PRESERVED'
    dump(run/'CAPTURE.json',rec)
print(json.dumps({'capture':str(run),'pid':rec['pid'],'status':rec['status'],'exit_code':rec['exit_code']}))
sys.exit(0 if rec['status']=='PASS_OWN_CONTROLS' else 1)
