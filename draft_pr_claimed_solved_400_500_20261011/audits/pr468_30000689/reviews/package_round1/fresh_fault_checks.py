from pathlib import Path
import subprocess,sys,json,hashlib,datetime,tempfile,shutil
P=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_400_500_20261011/audits/pr468_30000689');Q=P/'package';R=P/'reviews/package_round1'
cases=[
('author_retains_missing','check_exact.py','    require((tt not in s)', '    s.add(tt)\n    require((tt not in s)','original line 32'),
('author_zero_coefficients','check_exact.py','row[idx[mv]]=pow(v+1,power,p)','row[idx[mv]]=0','original line 139'),
('author_wrong_rank','check_exact.py','    return len(basis)','    return len(basis)+1','original line 139'),
('author_zero_crossings','check_exact.py','    require((crossings==2*d+3','    crossings=0\n    require((crossings==2*d+3','original line 108'),
('author_nonflag_cliques','check_exact.py','if all(x<=y or y<=x for x,y in [(a,b),(a,c),(b,c)]):','if True:','original line 120'),
('audit_empty_filling','check_independent.py',' return {pool[j] for j in solve(cols,target)}',' return set()','original line 106'),
('audit_wrong_betti','check_independent.py',' return [len(vs)-r1-1,len(es)-r1-r2]',' return [len(vs)-r1,len(es)-r1-r2]','original line 143'),
('audit_zero_crossings','check_independent.py',' require((crossings%2==1)',' crossings=0\n require((crossings%2==1)','original line 113'),
('audit_wrong_partner','check_independent.py',' require((paired==set(boundary(a)))',' paired=set()\n require((paired==set(boundary(a)))','original line 108'),
('bitmask_retains_missing','check_bitmask_controls.py','        require(t not in faces','        faces.add(t)\n        require(t not in faces','Missing face condition'),
('bitmask_wrong_rank','check_bitmask_controls.py','    return pivot_row','    return pivot_row+1','Source quotient dimensions'),
('bitmask_bad_rational_circuit','check_bitmask_controls.py','    for power in range(ambient_dimension+1):','    coefficients=(coefficients[0]+1,)+coefficients[1:]\n    for power in range(ambient_dimension+1):','Circuit affine dependence fails'),
('bitmask_empty_filling','check_bitmask_controls.py','    actual=set()','    result=set()\n    actual=set()','Returned filling has wrong boundary'),
('bitmask_empty_product','check_bitmask_controls.py','    require(not deleted_boundary(omega)','    omega=set()\n    require(not deleted_boundary(omega)','Wrong triangles paired with missing face'),
('bitmask_wrong_betti','check_bitmask_controls.py','    return [len(vs)-r1-1,len(es)-r1-r2]','    return [len(vs)-r1,len(es)-r1-r2]','Complement mod-2 homology fails')]
results=[]
for label,filename,old,new,marker in cases:
 source=(Q/'verification/checks'/filename).read_text()
 if source.count(old)!=1:raise RuntimeError('Ambiguous mutation anchor '+label)
 mutated=source.replace(old,new)
 for optimized in [False,True]:
  command=[sys.executable]+(['-O'] if optimized else [])+['-c','import sys; exec(compile(sys.stdin.read(), "fresh_actual_fault", "exec"))']
  run=subprocess.run(command,input=mutated.encode(),capture_output=True,timeout=300)
  err=run.stderr.decode(errors='replace');passed=run.returncode!=0 and 'RuntimeError' in err and marker in err
  rec={'label':label,'mode':'optimized' if optimized else 'normal','current_source_sha256':hashlib.sha256(source.encode()).hexdigest(),'fault_source_sha256':hashlib.sha256(mutated.encode()).hexdigest(),'exit_code':run.returncode,'intended_error':marker,'rejected_by_intended_condition':passed,'stderr':err,'stdout_sha256':hashlib.sha256(run.stdout).hexdigest()};results.append(rec)
  if not passed:print(json.dumps(rec));raise RuntimeError('Failed fault check '+label)
print('All',len(results),'fresh mathematical faults rejected in both modes')
driver=[]
for fault in ['edited_program','edited_expected','escaping_path']:
 with tempfile.TemporaryDirectory(dir=R,prefix='driver_fault_') as tmp:
  t=Path(tmp)/'verification';shutil.copytree(Q/'verification',t)
  if fault=='edited_program':
   f=t/'checks/check_exact.py';f.write_bytes(f.read_bytes()+b'\n# actual checksum fault\n')
  elif fault=='edited_expected':
   f=t/'expected/author_results.json';f.write_bytes(f.read_bytes()+b'\n')
  else:
   f=t/'CONTROL_MANIFEST.json';m=json.loads(f.read_text());m['cases'][0]['script']='../../escaping.py';f.write_text(json.dumps(m))
  marker='Control path escapes package' if fault=='escaping_path' else 'Control file checksum mismatch'
  for optimized in [False,True]:
   run=subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(t/'reproduce.py'),'--mode','normal'],capture_output=True,timeout=300)
   err=run.stderr.decode();passed=run.returncode!=0 and 'RuntimeError' in err and marker in err
   driver.append({'fault':fault,'mode':'optimized' if optimized else 'normal','exit_code':run.returncode,'rejected':passed,'stderr':err})
   if not passed:raise RuntimeError('Driver fault survived')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Actual finite mathematical and integrity faults only, not universal proof certification. Mutated source was supplied in-memory; temporary driver copies removed. Package unchanged.','mathematical_faults':results,'driver_faults':driver}
(R/'FRESH_NEGATIVE_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('All',len(driver),'fresh driver faults rejected in both modes')
