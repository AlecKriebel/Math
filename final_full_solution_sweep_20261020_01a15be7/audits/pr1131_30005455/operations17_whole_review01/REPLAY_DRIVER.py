from pathlib import Path
import subprocess,sys,json,datetime,hashlib,os
D=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def allocated():
 seen=set();a=0
 for p in [D,*D.rglob('*')]:
  s=p.lstat();key=s.st_dev,s.st_ino
  if key not in seen:a+=s.st_blocks*512;seen.add(key)
 return a
jobs=[('parameters',[sys.executable,'-I','-S','-B',str(D/'source_parameters17.py')]),('optimized_O',[sys.executable,'-I','-S','-B','-O',str(D/'preload_probe17.py')]),('optimized_OO',[sys.executable,'-I','-S','-B','-OO',str(D/'preload_probe17.py')]),('data',[sys.executable,'-I','-S','-B',str(D/'data17.py')]),('data1337',[sys.executable,'-I','-S','-B',str(D/'assess1337_data17.py')])]
for name in ['focus17.py','retention17.py','native_only17.py','retention_edges17.py','fact_edges17.py','fact_get_corrected17.py','unicode17.py','encoding_component17.py','baseline16_unicode17.py']:
 jobs.append((name,[sys.executable,'-I','-S','-B',str(D/'run_case17.py'),name]))
rows=[]
for name,argv in jobs:
 need(allocated()<8*1024*1024,'Own cap beforecase')
 need(os.statvfs(D).f_bavail*os.statvfs(D).f_frsize>=150*1024*1024+1024*1024,'Own free reserve beforecase')
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 child=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1800)
 out={'at':start,'completed':datetime.datetime.now(datetime.timezone.utc).isoformat(),'name':name,'argv':argv,'returncode':child.returncode,'stdout':child.stdout.decode('utf8','backslashreplace'),'stderr':child.stderr.decode('utf8','backslashreplace'),'allocated':allocated(),'real_effects':0}
 p=D/'private'/('REPLAY_'+name+'.json')
 with p.open('x')as f:f.write(json.dumps(out,ensure_ascii=True,indent=2)+'\n')
 rows.append({k:v for k,v in out.items()if k not in {'stdout','stderr'}})
 print(name,child.returncode,allocated(),flush=True)
 need(child.returncode==0,'Replay aborted; full actual output retained '+name)
(D/'private/REPLAY_DRIVER_RESULTS.json').write_text(json.dumps({'jobs':rows,'real_effects':0,'readiness':False},indent=2)+'\n')
