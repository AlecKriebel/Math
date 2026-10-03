"""Retain full subprocess outputs while running the immutable package verifier."""
import base64,datetime,gzip,json,runpy,subprocess,sys
sys.dont_write_bytecode=True
original=subprocess.run
with gzip.open(sys.argv[2],'wb') as log:
 def retained(*args,**kwargs):
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();result=original(*args,**kwargs)
  row={'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'args':list(map(str,result.args)),'cwd':str(kwargs.get('cwd')),'returncode':result.returncode,'stdout_b64':base64.b64encode(result.stdout or b'').decode(),'stderr_b64':base64.b64encode(result.stderr or b'').decode()}
  log.write((json.dumps(row,separators=(',',':'))+'\n').encode());log.flush();return result
 subprocess.run=retained
 runpy.run_path(sys.argv[1],run_name='__main__')
