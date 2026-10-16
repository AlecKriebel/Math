#!/usr/bin/env python3
"""Independent adversarial controls for an externally pinned read-only packet."""
import pathlib,json,copy,subprocess,sys,os,hashlib,tempfile,shutil

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def must(v,m):
 if not v:raise RuntimeError(m)
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve();pins=json.loads(pathlib.Path(sys.argv[3]).read_text());data=json.loads((root/'COUNTEREXAMPLE.json').read_text())
must(os.getuid()!=0 and os.geteuid()!=0,'genuine nonroot required')
for name,pin in pins.items():must(sha(root/name)==pin,'external pin '+name)
raws=[]
def mutate(label,key,value):
 d=copy.deepcopy(data);d[key]=value;raws.append((label,json.dumps(d).encode()))
for label,key,val in [
 ('degree_true','degree',True),('degree_float','degree',10.0),('grid_false','grid_N',False),('grid_float','grid_N',8192.0),('scale_true','sqrt_scale',True),('scale_float','sqrt_scale',1e9),
 ('degree_overflow','degree',float('inf')),('grid_overflow','grid_N',float('inf')),('scale_overflow','sqrt_scale',float('inf')),('rational_float','q1',0.7875),('rational_bool','q1',True),('rational_null','q1',None),('rational_bad_sign','q1','+63/80'),('rational_negative_zero','q1','-0'),('rational_unreduced','q1','126/160'),('rational_leading_zero','q1','063/80'),('rational_zero_denom','q1','63/0'),('rational_huge','q1','9'*81),('rational_whitespace','q1',' 63/80'),('coefficient_wrong_type','coefficients',{}),('coefficient_float','coefficients',[[0.1,0.2]]*9),('coefficient_bool','coefficients',[[True,'0']]*9),('coefficient_zero','coefficients',[['0','0']]*9),('cover_too_coarse','grid_N',64),('cover_missing_N','grid_N',0),('coefficient_count_short','coefficients',data['coefficients'][:-1]),('coefficient_count_extra','coefficients',data['coefficients']+[data['coefficients'][0]]),('extra_key','ignored',1)]:mutate(label,key,val)
d=copy.deepcopy(data);d['coefficients'][0]=['0','0'];raws.append(('leading_coefficient_deleted',json.dumps(d).encode()))
raws += [('large_integer_5000_digits',b'{"degree":'+b'9'*5000+b'}'),('exponent_overflow',json.dumps(data).replace('"degree": 10','"degree": 1e1000000').encode()),('top_null',b'null'),('top_list',b'[]'),('duplicate_key',b'{"degree":10,"degree":10}'),('invalid_utf8',b'\xff'),('missing_fields',b'{}'),('oversize',b' '*10001),('trailing_json',json.dumps(data).encode()+b' {}')]
results=[]
with tempfile.TemporaryDirectory(prefix='sigma-independent-hostile-') as name:
 work=pathlib.Path(name);(work/'fractions.py').write_text('raise RuntimeError("HOSTILE fractions imported")\n');(work/'sitecustomize.py').write_text('raise RuntimeError("HOSTILE sitecustomize imported")\n')
 env=dict(os.environ,PYTHONPATH=name,PYTHONHOME='/nonexistent/hostile-home',PYTHONOPTIMIZE='99',PYTHONDONTWRITEBYTECODE='0')
 for opt,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
  for checker in ['verify_counterexample.py','verify_alternative.py']:
   for label,payload in raws:
    file=work/'input.json';file.write_bytes(payload)
    proc=subprocess.run([sys.executable,'-I','-B',*flags,str(root/checker),str(file)],cwd=work,env=env,text=True,capture_output=True,timeout=180)
    try:obj=json.loads(proc.stdout)
    except Exception:obj={}
    must(proc.returncode==2 and obj.get('status')=='REJECT',f'{opt} {checker} {label}: {proc.returncode} {proc.stdout} {proc.stderr}')
    results.append({'mode':opt,'checker':checker,'case':label,'status':'REJECT','reason':obj.get('reason')})
 # Pin and inventory controls exercise the supplied driver, without executing a corrupted checker.
 def run_driver(packet,pin):
  return subprocess.run([sys.executable,'-I','-B',str(root/'replay_controls.py'),str(packet),'--manifest-sha256',pin],cwd=work,env=env,text=True,capture_output=True,timeout=10)
 pin_cases=[]
 proc=run_driver(root,'0'*64);must(proc.returncode==2 and 'external manifest pin mismatch' in proc.stdout,'wrong external manifest pin');pin_cases.append('wrong_external_pin')
 for case in ('missing_file','extra_file','checker_truncated_circle','checker_omit_disk_child','witness_perturbed','manifest_modified'):
  packet=work/case;shutil.copytree(root,packet);packet.chmod(0o755)
  for f in packet.iterdir():f.chmod(0o644)
  if case=='missing_file':(packet/'COUNTEREXAMPLE.json').unlink()
  if case=='extra_file':(packet/'unexpected.txt').write_text('extra')
  if case=='checker_truncated_circle':
   f=packet/'verify_counterexample.py';f.write_text(f.read_text().replace('range(-N,N+1)','range(0,1)'))
  if case=='checker_omit_disk_child':
   f=packet/'verify_alternative.py';f.write_text(f.read_text().replace('(rm,r1,t0,t1,sgn,depth+1)','(r0,rm,t0,t1,sgn,depth+1)'))
  if case=='witness_perturbed':(packet/'COUNTEREXAMPLE.json').write_bytes((packet/'COUNTEREXAMPLE.json').read_bytes()+b' ')
  if case=='manifest_modified':(packet/'MANIFEST.json').write_bytes((packet/'MANIFEST.json').read_bytes()+b' ')
  for f in packet.iterdir():f.chmod(0o444)
  packet.chmod(0o555)
  proc=run_driver(packet,pins['MANIFEST.json']);must(proc.returncode==2 and json.loads(proc.stdout)['status']=='REJECT',case);pin_cases.append(case)
  packet.chmod(0o755)
 for name,pin in pins.items():must(sha(root/name)==pin,'post-run mutation '+name)
report={'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'input_cases_per_mode_per_checker':len(raws),'rejected_input_executions':len(results),'modes':['normal','O','OO'],'hostile_environment':'PYTHONHOME, PYTHONPATH, PYTHONOPTIMIZE, bytecode settings and hostile fractions/sitecustomize modules ignored under -I -B','pin_and_inventory_controls':pin_cases,'post_run_hashes_unchanged':True,'results':results}
out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
