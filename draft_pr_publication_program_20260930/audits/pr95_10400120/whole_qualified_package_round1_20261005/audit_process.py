from pathlib import Path
import subprocess, json, hashlib, datetime, os, sys
A=Path(__file__).resolve().parent

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def run(label, argv, cwd=None, inputs=(), expected=None):
 d=A/'processes'/label; d.mkdir(parents=True,exist_ok=False)
 env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}; env['PYTHONDONTWRITEBYTECODE']='1'
 rows=[]
 for v in (inputs or [x for x in argv if Path(x).is_file()]):
  f=Path(v).resolve(); b=f.read_bytes(); rows.append({'path':str(f),'bytes':len(b),'sha256':sha(b)})
 t=now(); p=subprocess.Popen(argv,cwd=cwd or A,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=p.communicate(); (d/'stdout.bin').write_bytes(out); (d/'stderr.bin').write_bytes(err)
 rec={'schema':'actual-process/v1','operator_pid':os.getpid(),'child_pid':p.pid,'argv':argv,'cwd':str(cwd or A),'start_utc':t,'end_utc':now(),'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'inputs':rows,'python_environment_removed':sorted(k for k in os.environ if k.startswith('PYTHON'))}
 (d/'process.json').write_text(json.dumps(rec,indent=2)+'\n')
 print(json.dumps({'label':label,'pid':p.pid,'exit':p.returncode,'stdout_bytes':len(out),'stderr_bytes':len(err)}),flush=True)
 if expected is not None and p.returncode!=expected: raise RuntimeError((label,p.returncode,expected,err[-1000:]))
 return out,err,p.returncode
if __name__=='__main__': run(sys.argv[1],sys.argv[2:])
