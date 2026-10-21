from pathlib import Path
import datetime,hashlib,json,os,platform,subprocess,sys,time
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def capture(label,argv,cwd,inputs,expected=0):
 root=Path(__file__).resolve().parent/'outer_processes'/label
 root.mkdir(parents=True)
 record={'label':label,'argv':argv,'cwd':str(cwd),'recorder_pid':os.getpid(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs],'environment':{'python':platform.python_version(),'PYTHON_variables_removed':sorted(k for k in os.environ if k.startswith('PYTHON'))}}
 env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
 start=time.monotonic()
 with (root/'stdout.bin').open('wb') as o,(root/'stderr.bin').open('wb') as e:
  child=subprocess.Popen(argv,cwd=cwd,env=env,stdout=o,stderr=e);record['pid']=child.pid;code=child.wait()
 record.update(exit_code=code,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start)
 for name in ['stdout.bin','stderr.bin']:
  p=root/name;record[name]={'sha256':sha(p),'bytes':p.stat().st_size}
 (root/'process.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
 if code!=expected:raise RuntimeError(label+' unexpected exit '+str(code))
 return record
if __name__=='__main__':
 P=Path(__file__).resolve().parent.parent;N=P/'private_notes';F=P/'publicfiles'
 positive=capture('clean_archive',[sys.executable,'-E','-B',str(N/'clean_extracted/verification/run_all.py'),'--output-dir',str(N/'clean_archive_run')],N/'clean_extracted',[F/'pr95_support.zip',N/'clean_extracted/PAYLOAD_MANIFEST.json'])
 negative=capture('tamper_guard',[sys.executable,'-E','-B','-O',str(N/'tampered_extracted/verification/run_all.py'),'--output-dir',str(N/'tamper_output')],N/'tampered_extracted',[F/'pr95_support.zip',N/'tampered_extracted/verification/verify.py'],1)
 if (N/'tamper_output').exists():raise RuntimeError('tamper rejected after creating outputs')
 if b'payload hash mismatch: verification/verify.py' not in (N/'outer_processes/tamper_guard/stderr.bin').read_bytes():raise RuntimeError('wrong tamper rejection')
 check=capture('zenodo_local_check',[sys.executable,'-E','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(P/'zenodo-deposit.json')],Path('/Users/alec/Documents/Math'),[P/'zenodo-deposit.json',F/'SHA256SUMS.txt'])
 print(json.dumps({'clean_archive_exit':positive['exit_code'],'tamper_expected_exit':negative['exit_code'],'zenodo_check_exit':check['exit_code']}))
