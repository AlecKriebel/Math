"""Genuine complete prelaunch/child/final records for this family's own controls."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess,sys,traceback
F=Path(__file__).absolute().parent
R=F.parent.parents[2]
def digest(raw):return hashlib.sha256(raw).hexdigest()
def emit(path,obj):
 with path.open('xb') as f:f.write((json.dumps(obj,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
def main():
 parser=argparse.ArgumentParser();parser.add_argument('name');parser.add_argument('--mutant',default='none');a=parser.parse_args()
 assert a.name and '/' not in a.name and a.name not in {'.','..'}
 source=F/'independent_source_controls.py';raw=source.read_bytes();operator=Path(__file__).read_bytes()
 d=F/'actual_runs'/a.name;d.mkdir(parents=True,exist_ok=False)
 for name,body in [('PRELAUNCH_SOURCE.py',raw),('PRELAUNCH_OPERATOR.py',operator)]:
  with (d/name).open('xb') as handle:handle.write(body);handle.flush();os.fsync(handle.fileno())
 argv=['/usr/bin/python3','-B',str(source),'--mutant',a.mutant]
 pre={'schema':'pr45-new-source-adversary-prelaunch/v1','operator_pid':os.getpid(),'argv':argv,'cwd':str(R),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':digest(raw),'operator_sha256':digest(operator),'expected_exit_code':0 if a.mutant=='none' else 1,'only_own_handwritten_control_execution':True,'production_import_compile_or_execution':False}
 emit(d/'PRELAUNCH.json',pre)
 c=dict(pre,schema='pr45-new-source-adversary-actual-capture/v1',actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
 try:
  with (d/'stdout.bin').open('xb') as out,(d/'stderr.bin').open('xb') as err:
   child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
   c.update(actual_execution=True,pid=child.pid)
   emit(d/'LAUNCHED.json',{'pid':child.pid,'operator_pid':os.getpid(),'launched_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prelaunch_sha256':digest((d/'PRELAUNCH.json').read_bytes())})
   c['exit_code']=child.wait(timeout=50);c['completed']=True
 except BaseException:c['operator_error']=traceback.format_exc()
 c['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for name in ['stdout','stderr']:
  path=d/(name+'.bin')
  if path.exists():body=path.read_bytes();c[name]={'path':path.name,'bytes':len(body),'sha256':digest(body)}
 c['source_unchanged']=source.read_bytes()==raw;c['operator_unchanged']=Path(__file__).read_bytes()==operator
 ok=c['actual_execution'] is True and c['completed'] is True and c['exit_code']==c['expected_exit_code'] and c['source_unchanged'] is True and c['operator_unchanged'] is True and 'operator_error' not in c
 c['status']='PASS_OWN_EXPECTED_CONTROL_OUTCOME' if ok else 'FAIL_OWN_CONTROL_CAPTURE_PRESERVED'
 emit(d/'CAPTURE.json',c)
 print(json.dumps(c,indent=2));return 0 if ok else 1
if __name__=='__main__':sys.exit(main())
