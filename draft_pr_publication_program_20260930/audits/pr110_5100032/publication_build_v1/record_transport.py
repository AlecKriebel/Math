#!/usr/bin/env python3
"""Record a genuine completed CLI operation; environment values never retained."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parents[1]
def now():return datetime.now(timezone.utc).isoformat()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    label=sys.argv[1]; argv=sys.argv[2:]
    if not label.replace('_','').isalnum() or not argv: raise ValueError('Invalid operation label/argv')
    D=A/'actual_operations'/label;D.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ);envsha=hashlib.sha256(json.dumps(env,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    start=now();p=subprocess.Popen(argv,cwd=Path.cwd(),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate();end=now()
    (D/'stdout.bin').write_bytes(out);(D/'stderr.bin').write_bytes(err)
    r={'schema':'pr110-actual-cli-execution/v1','actual_recorder_PID':os.getpid(),'child_PID':p.pid,
       'argv':argv,'cwd':str(Path.cwd()),'environment_sha256':envsha,'UTC_start':start,'UTC_end':end,
       'exit_code':p.returncode,'reaped':True,'termination':{'wait_method':'Popen.communicate','returncode':p.returncode,'signal':-p.returncode if p.returncode<0 else None},
       'stdout':{'path':'stdout.bin',**hp(out)},'stderr':{'path':'stderr.bin',**hp(err)}}
    (D/'execution.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'label':label,'child_PID':p.pid,'exit_code':p.returncode,'stdout_bytes':len(out),'stderr_bytes':len(err)}))
    if p.returncode:print(err.decode('utf-8','replace')[:1000],file=sys.stderr)
    return p.returncode
if __name__=='__main__':sys.exit(main())
