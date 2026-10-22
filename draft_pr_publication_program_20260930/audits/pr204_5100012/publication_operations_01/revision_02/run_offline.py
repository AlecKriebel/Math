"""Capture immutable helper-code pins and both offline-only fake-transport modes."""
import sys
sys.dont_write_bytecode=True
import argparse,ast,datetime,hashlib,json,os,pathlib,subprocess
HERE=pathlib.Path(__file__).resolve().parent
CODES=('operations_common.py','publish_exact.py','update_tracker.py','offline_tests.py','run_offline.py')
def require(ok,message):
 if not ok:raise RuntimeError(message)
def pin(path):
 raw=path.read_bytes();st=path.stat()
 return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),mtime_ns=st.st_mtime_ns,ctime_ns=st.st_ctime_ns,mode=oct(st.st_mode&0o777))
def save(path,raw):
 with path.open('xb') as f:
  f.write(raw);f.flush();os.fsync(f.fileno())
 fd=os.open(path.parent,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--prefix',default='REVISION_02_BOUND_01');a=ap.parse_args()
 require(a.prefix and pathlib.Path(a.prefix).name==a.prefix,'Owned output prefix must be a basename')
 for mode in ('NORMAL','OPTIMIZED'):
  for suffix in ('.json','.stdout','.stderr'):
   require(not (HERE/(a.prefix+'_'+mode+suffix)).exists(),'Output already exists; retain it and choose new prefix')
 target=HERE/(a.prefix+'_BINDINGS.json');require(not target.exists(),'Binding exists')
 before={n:pin(HERE/n) for n in CODES}
 for n in CODES:
  require(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse((HERE/n).read_text()))),'Assert correctness guard prohibited')
 executions=[];results=[]
 for optimized in (False,True):
  name=a.prefix+('_OPTIMIZED' if optimized else '_NORMAL')
  output=HERE/(name+'.json')
  command=[sys.executable,'-E','-S','-B']+(['-O'] if optimized else [])+[str(HERE/'offline_tests.py'),'--output',str(output)]
  start=datetime.datetime.now(datetime.timezone.utc).isoformat()
  proc=subprocess.run(command,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=60)
  save(HERE/(name+'.stdout'),proc.stdout);save(HERE/(name+'.stderr'),proc.stderr)
  after={n:pin(HERE/n) for n in CODES}
  e=dict(UTC_start=start,UTC_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=command,PYTHONDONTWRITEBYTECODE='1',exit=proc.returncode,stdout=pin(HERE/(name+'.stdout')),stderr=pin(HERE/(name+'.stderr')),code_before=before,code_after=after)
  if output.exists():e['result']=pin(output)
  executions.append(e)
  if proc.returncode:
   save(target,enc(dict(status='FAIL',offline_only=True,executions=executions)))
   raise RuntimeError('Offline child failed; exact raw streams retained')
  require(after==before,'Code identity/stat changed during offline run')
  result=json.loads(output.read_text());require(result['status']=='PASS' and result['offline_only'] is True and result['optimization_flag']==int(optimized) and result['real_process_or_network_calls']==0,'Offline result failure')
  require(json.loads(proc.stdout)==result and not proc.stderr,'Raw/result mismatch or stderr')
  result.pop('optimization_flag');results.append(result)
 require(results[0]==results[1],'Modes differ beyond documented optimization_flag')
 receipt=dict(status='PASS',offline_only=True,UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,executions=executions,mode_comparison='Exact JSON equality after removing only optimization_flag',active_checks_each=results[0]['active_checks'],all_code_hash_size_mode_mtime_ctime_unchanged=True,no_real_KIT_GWS_network_or_credentials=True,limits='Preparation only; no scientific or publication clearance.')
 save(target,enc(receipt))
 print(json.dumps(dict(status='PASS',active_checks_each=receipt['active_checks_each'],binding_file=target.name,real_service_calls=0),sort_keys=True))
if __name__=='__main__':main()
