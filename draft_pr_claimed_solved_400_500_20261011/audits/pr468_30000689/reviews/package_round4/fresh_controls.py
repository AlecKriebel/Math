#!/usr/bin/env python3
"""Fresh faults target computed results; malformed syntax/import failures do not count."""
from pathlib import Path
import ast,datetime,hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
CLEAN=HERE/'private_sources/fresh_archive/verification'
FIXTURES=HERE/'private_sources/fault_fixtures'
FIXTURES.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def require(test,message):
 if not test:raise RuntimeError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def replacement(text,old,new):
 require(text.count(old)==1,'Ambiguous fault insertion: '+old)
 return text.replace(old,new)
# (name, program, original construction, mutated construction, intended diagnostic)
mutations=[
 ('author_add_back_missing_face','check_exact.py','tt = tuple(sorted(t))','tt = tuple(sorted(t))\n    s.add(tt)','original line 32: tt not in s'),
 ('author_damage_hvector','check_exact.py','require((h == h[::-1])','h[0] += 1\n    require((h == h[::-1])','original line 43: h == h[::-1]'),
 ('author_corrupt_quotient_rank','check_exact.py','rank=rank_mod(rows,p)','rank=rank_mod(rows,p)+1','original line 139:'),
 ('author_damage_computed_flores_boundary','check_exact.py','require((not any(boundary.values()))','boundary[next(iter(boundary))] ^= 1\n    require((not any(boundary.values()))','original line 107: not any(boundary.values())'),
 ('author_damage_computed_crossings','check_exact.py','require((crossings==2*d+3','crossings += 1\n    require((crossings==2*d+3','original line 108:'),
 ('audit_corrupt_homology_rank','check_independent.py','r2=rank2([sum(1<<ei[f] for f in boundary(t)) for t in ts])','r2=rank2([sum(1<<ei[f] for f in boundary(t)) for t in ts])+1','original line 143: betti01(complement)==[0,0]'),
 ('audit_drop_filling_triangle','check_independent.py','return {pool[j] for j in solve(cols,target)}','result={pool[j] for j in solve(cols,target)}\n if degree==2 and result:result.remove(min(result,key=lambda f:tuple(sorted(f))))\n return result','original line 106: not bd'),
 ('audit_drop_witness_cell','check_independent.py','bd=set()','omega.remove(min(omega))\n bd=set()','original line 106: not bd'),
 ('audit_damage_missing_partner_chain','check_independent.py','require((paired==set(boundary(a)))','paired.clear()\n require((paired==set(boundary(a)))','original line 108: paired==set(boundary(a))'),
 ('audit_damage_computed_pairing','check_independent.py','require((crossings%2==1)','crossings+=1\n require((crossings%2==1)','original line 113: crossings%2==1'),
 ('bitmask_corrupt_quotient_rank','check_bitmask_controls.py','relation_rank = rank(rows,prime)','relation_rank = rank(rows,prime)+1','Source quotient dimensions'),
 ('bitmask_damage_computed_affine_circuit','check_bitmask_controls.py','for power in range(ambient_dimension+1):','coefficients=(-coefficients[0],)+coefficients[1:]\n    for power in range(ambient_dimension+1):','Circuit affine dependence fails'),
 ('bitmask_drop_flores_cell','check_bitmask_controls.py','require(not deleted_boundary(cells),','cells.remove(min(cells))\n        require(not deleted_boundary(cells),','Flores chain not closed'),
 ('bitmask_drop_computed_filling_triangle','check_bitmask_controls.py','actual=set()','if result:result.remove(min(result))\n    actual=set()','Returned filling has wrong boundary'),
 ('bitmask_drop_transferred_cell','check_bitmask_controls.py','require(not deleted_boundary(omega),','omega.remove(min(omega))\n    require(not deleted_boundary(omega),','Transferred deleted chain has boundary'),
 ('bitmask_damage_computed_witness_pairing','check_bitmask_controls.py','pairing=sum(intersects(s,t,4) for s,t in omega)%2','pairing=(sum(intersects(s,t,4) for s,t in omega)+1)%2','Transferred rational-circuit pairing vanished'),
]
records=[]
for name,program,old,new,expected in mutations:
 source=replacement((CLEAN/'checks'/program).read_text(),old,new);ast.parse(source)
 fixture=FIXTURES/(name+'.py');fixture.write_text(source)
 for optimized in (False,True):
  command=[sys.executable]+(['-O'] if optimized else [])+[str(fixture)]
  result=subprocess.run(command,env=env,capture_output=True,timeout=300)
  diagnostic=result.stderr.decode(errors='replace');syntax_import=any(s in diagnostic for s in ('SyntaxError:','IndentationError:','ImportError:','ModuleNotFoundError:'))
  valid=result.returncode!=0 and 'RuntimeError:' in diagnostic and expected in diagnostic and not syntax_import
  records.append({'fault':name,'program':program,'mode':'optimized' if optimized else 'normal','fixture_sha256':sha(fixture.read_bytes()),'changes_computed_construction':True,'ast_parse_pass':True,'intended_runtime_rejection':valid,'returncode':result.returncode,'stdout_bytes':len(result.stdout),'intended_diagnostic':expected,'actual_diagnostic':diagnostic,'arbitrary_syntax_or_import_failure':syntax_import,'accepted':result.returncode==0})
checks=[('script_checksum','Control file checksum mismatch'),('expected_checksum','Control file checksum mismatch'),('missing_file','Missing regular control file'),('directory_as_file','Missing regular control file'),('direct_symlink','Missing regular control file'),('escaped_path','Control path escapes package'),('wrong_expected_bytes_bound_by_manifest','output differs from recorded bytes'),('correct_output_with_stderr','produced unexpected diagnostic output'),('bound_actual_computation_fault','failed:')]
driver=[]
for name,expected in checks:
 root=FIXTURES/name;shutil.copytree(CLEAN,root,dirs_exist_ok=True);manifest=json.loads((root/'CONTROL_MANIFEST.json').read_text());case=manifest['cases'][0];script=root/case['script'];expectedfile=root/case['expected']
 if name=='script_checksum':script.write_bytes(script.read_bytes()+b'\n# actual checksum corruption\n')
 elif name=='expected_checksum':expectedfile.write_bytes(expectedfile.read_bytes()+b'\n')
 elif name=='missing_file':script.unlink()
 elif name=='directory_as_file':script.unlink();script.mkdir()
 elif name=='direct_symlink':
  target=root/'regular_script.py';target.write_bytes(script.read_bytes());script.unlink();script.symlink_to(target)
 elif name=='escaped_path':
  target=FIXTURES/'outside_regular_script.py';target.write_bytes(script.read_bytes());case['script']='../outside_regular_script.py'
 elif name=='wrong_expected_bytes_bound_by_manifest':
  expectedfile.write_bytes(expectedfile.read_bytes()+b'\n');case['expected_sha256']=sha(expectedfile.read_bytes())
 elif name=='correct_output_with_stderr':
  script.write_bytes(script.read_bytes()+b'\nimport sys\nprint("fresh diagnostic corruption",file=sys.stderr)\n');case['script_sha256']=sha(script.read_bytes())
 elif name=='bound_actual_computation_fault':
  source=replacement(script.read_text(),'rank=rank_mod(rows,p)','rank=rank_mod(rows,p)+1');ast.parse(source);script.write_text(source);case['script_sha256']=sha(script.read_bytes())
 (root/'CONTROL_MANIFEST.json').write_text(json.dumps(manifest))
 for optimized in (False,True):
  command=[sys.executable]+(['-O'] if optimized else [])+['reproduce.py','--mode','optimized' if optimized else 'normal']
  result=subprocess.run(command,cwd=root,env=env,capture_output=True,timeout=300);diagnostic=result.stderr.decode(errors='replace')
  valid=result.returncode!=0 and 'RuntimeError:' in diagnostic and expected in diagnostic and not any(s in diagnostic for s in ('SyntaxError:','IndentationError:','ImportError:','ModuleNotFoundError:'))
  if name=='bound_actual_computation_fault':valid=valid and 'original line 139:' in diagnostic
  driver.append({'control':name,'mode':'optimized' if optimized else 'normal','expected_rejection':True,'intended_runtime_rejection':valid,'returncode':result.returncode,'intended_diagnostic':expected,'actual_diagnostic':diagnostic,'stdout_bytes':len(result.stdout),'accepted':result.returncode==0})
# This is deliberately an acceptance probe: no ancestor-symlink ban is advertised.
root=FIXTURES/'internal_ancestor_symlink';shutil.copytree(CLEAN,root,dirs_exist_ok=True);(root/'checks').rename(root/'actual_checks');(root/'checks').symlink_to(root/'actual_checks',target_is_directory=True)
for optimized in (False,True):
 command=[sys.executable]+(['-O'] if optimized else [])+['reproduce.py','--mode','optimized' if optimized else 'normal']
 result=subprocess.run(command,cwd=root,env=env,capture_output=True,timeout=300);valid=result.returncode==0 and not result.stderr and len(json.loads(result.stdout)['results'])==3
 driver.append({'control':'internal_ancestor_symlink_with_same_regular_file_bytes','mode':'optimized' if optimized else 'normal','expected_rejection':False,'permitted_acceptance_verified':valid,'returncode':result.returncode,'actual_diagnostic':result.stderr.decode(),'accepted':result.returncode==0,'interpretation':'No security or ancestor-symlink ban is advertised; all resolved files remain inside package and match hashes.'})
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'construction_fault_variants':len(mutations),'construction_fault_runs':len(records),'valid_intended_construction_rejections':sum(r['intended_runtime_rejection'] for r in records),'construction_accepted':sum(r['accepted'] for r in records),'driver_rejection_variants':len(checks),'driver_rejection_runs':2*len(checks),'valid_intended_driver_rejections':sum(r.get('intended_runtime_rejection',False) for r in driver),'permitted_acceptance_runs':2,'permitted_acceptances_verified':sum(r.get('permitted_acceptance_verified',False) for r in driver),'records':records,'driver_controls':driver,'invalid_fixtures_private_only':True,'scope':'Actual finite computed-construction faults and documented driver checks, not universal proof certification or a security audit.'}
(HERE/'FRESH_ADVERSARIAL_CONTROLS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
require(report['valid_intended_construction_rejections']==len(records),'One or more construction fault probes did not reject at intended RuntimeError; inspect honest report')
require(report['valid_intended_driver_rejections']==2*len(checks),'One or more driver probes failed intended rejection')
require(report['permitted_acceptances_verified']==2,'Permitted internal-ancestor-symlink probe failed')
print(json.dumps({k:v for k,v in report.items() if k not in ('records','driver_controls')},indent=2))
