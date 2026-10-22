from pathlib import Path
import sys,json,hashlib,subprocess,time,datetime,shutil,os,math
P=Path(__file__).resolve().parent
R=P/'_private_package'
EXE='/opt/homebrew/bin/python3.11'
O=P/'replay';O.mkdir(mode=0o700)
original=R/'pr_update/30005244/history/original_submission_20261015'
programs=[(original/x['script'],x.get('expected')) for x in json.loads((R/'verification/ORIGINAL_CHECKS.json').read_text())]
programs += [(R/'verification'/x,None) for x in ['ball_exact_controls.py','kernel_controls.py','spectral_illustration.py']]
rows=[]
def compare(a,b,path='root'):
 if type(b) is dict:
  assert type(a) is dict and a.keys()==b.keys(),path
  for k in b:compare(a[k],b[k],path+'.'+k)
 elif type(b) is list:
  assert type(a) is list and len(a)==len(b),path
  for j,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'.'+str(j))
 elif type(b) is float:assert type(a) in (int,float) and math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12),path
 else:assert type(a)==type(b) and a==b,(path,a,b)
for j,(source,expected) in enumerate(programs):
 w=O/('program_%02d'%j);w.mkdir(mode=0o700);(w/'private').mkdir(mode=0o700)
 script=w/source.name;raw=source.read_bytes();script.write_bytes(raw)
 cmd=[EXE,'-E','-B','-P',str(script)]
 if source.name=='kernel_controls.py':cmd += ['--output',str(w/'kernel_result.json')]
 start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=subprocess.run(cmd,cwd=w,capture_output=True,timeout=180)
 elapsed=time.monotonic()-start
 (w/'stdout.bin').write_bytes(result.stdout);(w/'stderr.bin').write_bytes(result.stderr)
 row={'index':j,'source_relative':str(source.relative_to(R)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'command':cmd,'cwd':str(w),'utc_start':utc,'elapsed_seconds':elapsed,'exit_status':result.returncode,'stdout_bytes':len(result.stdout),'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'stderr_bytes':len(result.stderr),'stderr_sha256':hashlib.sha256(result.stderr).hexdigest(),'classification':'inherited unchanged replay'}
 assert script.read_bytes()==raw
 if result.returncode==0:
  data=json.loads(result.stdout)
  row['reported_exact_assertions']=data.get('exact_assertions',data.get('count'))
  if expected:
   compare(data,json.loads((R/'verification'/expected).read_text()));row['comparison_with_archived_expected_all_fields_1e12']=True
  row['result']=data
 rows.append(row)
 (O/'REPLAY_RESULTS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'programs':rows},indent=2)+'\n')
 print(json.dumps({k:v for k,v in row.items() if k not in ['command','cwd','result']}),flush=True)
 assert result.returncode==0,(j,result.stderr)
print(json.dumps({'all_seven_unchanged_programs_exit_zero':True,'original_reported_checks':sum(x.get('reported_exact_assertions') or 0 for x in rows[:4]),'all_stderr_empty':all(x['stderr_bytes']==0 for x in rows)}))
