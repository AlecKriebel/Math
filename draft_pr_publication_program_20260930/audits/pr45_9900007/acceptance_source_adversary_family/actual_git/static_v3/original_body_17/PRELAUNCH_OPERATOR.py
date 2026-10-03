"""Execute only this new adversary's own controls or self closure, retaining full evidence."""
from pathlib import Path
import argparse,datetime as dt,hashlib,json,os,subprocess,sys
H=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def enc(x):return (json.dumps(x,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def main():
    a=argparse.ArgumentParser();a.add_argument('label');a.add_argument('script',choices=['independent_static_controls.py','close_self.py']);a.add_argument('--outside',action='store_true');a.add_argument('--expected-exit',type=int,default=0);a.add_argument('--mutant',default='none');v=a.parse_args()
    if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise ValueError('Unoptimized own process required')
    if not v.label or '/' in v.label or v.label in ('.','..'):raise ValueError('Literal new label required')
    if v.outside!=(v.script=='close_self.py'):raise ValueError('Only self closure uses outside completed capture')
    source=H/v.script;source_raw=source.read_bytes();operator_raw=Path(__file__).read_bytes()
    d=(H.parent if v.outside else H/'actual_runs')/v.label
    if not v.outside:d.parent.mkdir(exist_ok=True)
    d.mkdir(mode=0o700)
    argv=[sys.executable,'-B',str(source)]
    if v.script=='independent_static_controls.py':argv+=['--mutant',v.mutant,'--run-tag',v.label]
    pre={'schema':'pr45-acceptance-source-adversary-prelaunch/v1','operator_pid':os.getpid(),'argv':argv,'cwd':str(H),'prepared_utc':utc(),'source_sha256':sha(source_raw),'operator_sha256':sha(operator_raw),'stdin_supplied':False,'production_imported_compiled_executed':False,'completed_capture_absent_before_launch':not (d/'CAPTURE.json').exists()}
    put(d/'PRELAUNCH_SOURCE.py',source_raw);put(d/'PRELAUNCH_OPERATOR.py',operator_raw);put(d/'PRELAUNCH.json',enc(pre))
    start=utc();p=subprocess.Popen(argv,cwd=H,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));out,err=p.communicate();end=utc()
    rec={'schema':'pr45-acceptance-source-adversary-actual-capture/v1',**pre,'started_utc':start,'finished_utc':end,'child_pid':p.pid,'actual_execution':True,'completed':True,'exit_code':p.returncode,'expected_exit_code':v.expected_exit,'source_unchanged':source.read_bytes()==source_raw,'operator_unchanged':Path(__file__).read_bytes()==operator_raw,'future_acceptance_approved':False}
    for channel,b in [('stdout',out),('stderr',err)]:put(d/(channel+'.bin'),b);rec[channel]={'path':channel+'.bin','bytes':len(b),'sha256':sha(b)}
    good=p.returncode==v.expected_exit and rec['source_unchanged'] and rec['operator_unchanged'];rec['status']='PASS_OWN_EXPECTED_OUTCOME' if good else 'FAIL'
    put(d/'CAPTURE.json',enc(rec))
    print(json.dumps({'capture':str(d),'status':rec['status'],'operator_pid':os.getpid(),'child_pid':p.pid,'exit_code':p.returncode,'stdout':out.decode(errors='replace'),'stderr':err.decode(errors='replace')}))
    return 0 if good else 1
if __name__=='__main__':sys.exit(main())
