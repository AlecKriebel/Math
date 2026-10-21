"""Root-only exact custody and independent replay. No original/family file writes."""
from pathlib import Path
import ast,datetime,hashlib,json,subprocess,sys,time
A=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
PY=sys.executable;RUNTIME=A.parent/'pr200_5100007/math_algebra_family_01/runtime_packages'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(c,m):
 if not c:raise RuntimeError(m)
def save(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def enc(x):return (json.dumps(x,indent=2)+'\n').encode()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
safe={}
for family,manifest in [('math_source_family_01','MANIFEST.json'),('math_geometry_family_01','MANIFEST.json'),('math_algebra_family_01','AUTHORED_OUTPUT_MANIFEST.json')]:
 f=A/family/manifest;j=json.loads(f.read_bytes());fs=j['files'];items=fs.items() if isinstance(fs,dict) else [(x['path'],x) for x in fs]
 for rel,x in items:
  p=A/family/rel;need(not Path(rel).is_absolute() and '..' not in Path(rel).parts and p.is_file() and not p.is_symlink(),'unsafe family path')
  b=p.read_bytes();need(pin(b)=={k:x[k] for k in ['bytes','sha256']},'family custody '+str(p));safe[family+'/'+rel]=pin(b);p.chmod(0o444)
 safe[family+'/'+manifest]=pin(f.read_bytes());f.chmod(0o444)
save(D/'ROOT_INPUT_CUSTODY.json',enc({'UTC':utc(),'safe_files':safe,'all_frozen_family_manifest_pins_authenticated':True}))
# Verify original author/reviewer reproducibility ledgers against actual archive bytes.
original=A/'original_submitted_head'
for mode in ['normal','optimized']:
 for name,archive in [('exact','turn1_exact.txt'),('generic','turn1_generic_six.txt'),('reviewer','independent_review/independent_receipt.json')]:
  f=A/'math_algebra_family_01/fresh_reproduction'/('replay_original_'+name+'_'+mode+'.stdout')
  need(f.read_bytes()==(original/archive).read_bytes(),'legacy replay mismatch '+name+mode)
# Root replays new controls from inspected immutable source paths.
jobs=[
 ('source_normal',A/'math_source_family_01/independent_area_checks.py',False,A/'math_source_family_01/normal_output.txt'),
 ('source_optimized',A/'math_source_family_01/independent_area_checks.py',True,A/'math_source_family_01/optimized_output.txt'),
 ('geometry_exact',A/'math_geometry_family_01/exact_geometry_controls.py',False,A/'math_geometry_family_01/exact_geometry_controls.json'),
 ('geometry_direct',A/'math_geometry_family_01/direct_geometry_checks.py',False,A/'math_geometry_family_01/direct_geometry_checks.json'),
 ('algebra_general_axis',A/'math_algebra_family_01/extended_exact_controls.py',False,None),
 ('algebra_physical_fresh',A/'math_algebra_family_01/physical_phase_checks.py',False,None),
 ('legacy_enforcement_normal',A/'math_algebra_family_01/probe_assertion_enforcement.py',False,A/'math_algebra_family_01/enforcement_probe_normal.json'),
 ('legacy_enforcement_optimized',A/'math_algebra_family_01/probe_assertion_enforcement.py',True,A/'math_algebra_family_01/enforcement_probe_optimized.json')]
src=(A/'math_source_family_01/independent_area_checks.py').read_text();old="40*(u*u+v*v+9)/9";need(src.count(old)==1,'mutation selector')
bad=D/'DELIBERATELY_FALSE_source_product.py';save(bad,src.replace(old,"41*(u*u+v*v+9)/9").encode())
for opt in [False,True]:jobs.append(('deliberately_false_'+('optimized' if opt else 'normal'),bad,opt,None))
bootstrap="import runpy,sys;sys.path.insert(0,"+repr(str(RUNTIME))+");runpy.run_path(sys.argv[1],run_name='__main__')"
results=[]
def mathematical(x):
 if isinstance(x,dict):return {k:mathematical(v) for k,v in x.items() if k not in ['optimization','elapsed_seconds']}
 if isinstance(x,list):return [mathematical(v) for v in x]
 return x
for label,path,opt,expected in jobs:
 cmd=[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+['-c',bootstrap,str(path)]
 begin=utc();tick=time.monotonic();r=subprocess.run(cmd,capture_output=True,timeout=300,cwd=D);end=utc()
 save(D/(label+'.stdout'),r.stdout);save(D/(label+'.stderr'),r.stderr)
 deliberate=label.startswith('deliberately_false_')
 if deliberate:need(r.returncode!=0 and b'six-period direct product' in r.stderr,'false mathematical identity failed to reject')
 else:
  need(r.returncode==0,'Root replay failed '+label)
  if expected:need(r.stdout==expected.read_bytes(),'Root output identity '+label)
  if label=='algebra_general_axis':
   prior=json.loads((A/'math_algebra_family_01/extended_exact_normal.json').read_bytes());need(mathematical(json.loads(r.stdout))==mathematical(prior),'general symbolic result changed')
  if label=='algebra_physical_fresh':
   prior=json.loads((A/'math_algebra_family_01/physical_normal.json').read_bytes());need(mathematical(json.loads(r.stdout))==mathematical(prior),'fresh physical results changed')
 results.append({'label':label,'UTC_start':begin,'UTC_end':end,'elapsed_seconds':time.monotonic()-tick,'exit_code':r.returncode,'expected_mathematical_rejection':deliberate,'result_verified':True,'source_pin':pin(path.read_bytes()),'stdout_pin':pin(r.stdout),'stderr_pin':pin(r.stderr)})
 print(json.dumps({'completed':label,'verified':True}),flush=True)
# Execute all three exact archived original programs normally, redirecting only __file__ output.
for label,rel,expected in [('original_exact','turn1_exact.py','turn1_exact.txt'),('original_generic','turn1_generic_six.py','turn1_generic_six.txt'),('original_reviewer','independent_review/independent_check.py','independent_review/independent_receipt.json')]:
 path=original/rel;dest=D/label;dest.mkdir()
 boot="import sys;from pathlib import Path;sys.path.insert(0,"+repr(str(RUNTIME))+");p=Path("+repr(str(path))+");exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__','__file__':"+repr(str(dest/path.name))+",'__builtins__':__builtins__})"
 begin=utc();tick=time.monotonic();r=subprocess.run([PY,'-E','-S','-B','-P','-c',boot],capture_output=True,timeout=300,cwd=D);end=utc()
 save(D/(label+'.stdout'),r.stdout);save(D/(label+'.stderr'),r.stderr);need(r.returncode==0 and r.stdout==(original/expected).read_bytes(),'original Root normal replay '+label)
 if label=='original_reviewer':need((dest/'independent_receipt.json').read_bytes()==(original/expected).read_bytes(),'original reviewer receipt differs')
 results.append({'label':label,'UTC_start':begin,'UTC_end':end,'elapsed_seconds':time.monotonic()-tick,'exit_code':r.returncode,'result_verified':True,'archived_original_bytes_match':True,'stdout_pin':pin(r.stdout),'stderr_pin':pin(r.stderr)})
 print(json.dumps({'completed':label,'verified':True}),flush=True)
save(D/'ROOT_REPRODUCTION_RECEIPT_01.json',enc({'UTC':utc(),'PR':201,'all_jobs_verified':True,'jobs':results,'total_jobs':len(results),'originals_preserved':True,'normal_original_reviewer_enforced_exact_checks':1757,'normal_original_reviewer_enforced_numerical_checks':26568,'optimized_original_assertion_enforcement':0,'new_explicit_false_mathematical_identity_rejected_both_modes':True,'scope':'Exact finite controls and independent physical diagnostic reproduction; no numerical or symbolic finite test establishes the all-period analytic theorem or priority.'}))
print(json.dumps({'Root_reproduction_complete':True,'jobs':len(results)}))

