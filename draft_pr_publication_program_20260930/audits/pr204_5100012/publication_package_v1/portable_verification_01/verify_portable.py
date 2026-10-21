#!/usr/bin/env python3
"""Portable, fail-closed finite scientific controls. Standard library driver only."""
import sys
sys.dont_write_bytecode = True
import argparse, base64, concurrent.futures, datetime, gzip, hashlib, importlib.util
import json, math, os, pathlib, re, shutil, subprocess, tempfile, threading

HERE = pathlib.Path(__file__).resolve().parent
PIN_MANIFEST_SHA256 = '4ed6d852c19e811b87dc68e932888645f355487f16233f69bb3c747d9ab0d3fe'
COMPLEX_PARENT = 'math_independent_complex_01/AUTHORED_MANIFEST.json'
COMPLEX_PARENT_SHA256 = '4ca9a0a74d59acd78865252388696b7e8b71a8ed71d1c0669b0a078413ae6071'
PHYSICAL = 'math_algebra_physical_01/'
REPAIR = PHYSICAL + 'repaired_original_controls_01/'
PROGRAMS = {
 'physical': (PHYSICAL+'physical_shooting.py', PHYSICAL+'physical_shooting_ordinary.stdout'),
 'exact': (PHYSICAL+'exact_low_period.py', PHYSICAL+'exact_low_period_ordinary.stdout'),
 'source': ('math_source_analytic_01/independent_controls_01.py','math_source_analytic_01/independent_controls_output_01.json'),
 'direct': ('math_direct_geometry_01/verify_direct_geometry_01.py','math_direct_geometry_01/verification_normal_01.json'),
 'complex_v2': ('math_independent_complex_01/v2_validation/verify_complex_v2.py','math_independent_complex_01/v2_validation/valid_normal.json'),
 'repaired_author': (REPAIR+'valid/verify.py','original_submitted_head/verification.json'),
 'repaired_reviewer': (REPAIR+'valid/independent_review/independent_check.py','original_submitted_head/independent_review/independent_output.json'),
}
NORMALIZATION = {'source':['optimization_flag'], 'direct':['optimized_mode'],
 'complex_v2':['utc','optimized','runtime.method']}

def require(ok, message):
 if not ok: raise RuntimeError(message)
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(data): return hashlib.sha256(data).hexdigest()
def compact(value): return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def reject_constant(value): raise RuntimeError('Nonfinite JSON constant: '+value)
def parsed(raw): return json.loads(raw.decode('utf-8'),parse_constant=reject_constant)
def contained(path, root): return path == root or root in path.parents
def finite_tree(value):
 if isinstance(value,float): require(math.isfinite(value),'Nonfinite numeric output')
 elif isinstance(value,str):
  require(not re.search(r'(?<![A-Za-z0-9_])[-+]?(?:nan|inf(?:inity)?)(?![A-Za-z0-9_])',value,re.I),'Nonfinite string output: '+value)
 elif isinstance(value,dict):
  for v in value.values(): finite_tree(v)
 elif isinstance(value,list):
  for v in value: finite_tree(v)
def normalize(program, value):
 value=json.loads(json.dumps(value,allow_nan=False))
 for field in NORMALIZATION.get(program,[]):
  if field=='runtime.method': value['runtime'].pop('method',None)
  else: value.pop(field,None)
 return value
def snapshot(materials, pins):
 result={}
 for rel, expected in pins.items():
  path=materials/rel
  require(path.resolve()==path,'Material path contains a symlink: '+rel)
  require(path.is_file() and not path.is_symlink(),'Missing/nonregular/symlink material: '+rel)
  stat=path.stat(); actual=digest(path.read_bytes())
  require(stat.st_size==expected['bytes'] and actual==expected['sha256'],'Material byte pin failed: '+rel)
  result[rel]={'sha256':actual,'bytes':stat.st_size,'mtime_ns':stat.st_mtime_ns,'ctime_ns':stat.st_ctime_ns}
 return result
def cache_inventory(roots):
 rows=[]
 for root in sorted(set(roots)):
  root=pathlib.Path(root)
  for directory, dirs, files in os.walk(root):
   for name in dirs:
    if name=='__pycache__':
     q=pathlib.Path(directory)/name;s=q.stat();rows.append([str(q),'directory',s.st_mtime_ns,s.st_ctime_ns])
   for name in files:
    if name.endswith(('.pyc','.pyo')):
     q=pathlib.Path(directory)/name;s=q.stat();rows.append([str(q),s.st_size,s.st_mtime_ns,s.st_ctime_ns,digest(q.read_bytes())])
 return {'entries':len(rows),'sha256':digest(compact(sorted(rows))),'records':sorted(rows)}

def validate_valid(program,data,opt,raw,baseline_raw):
 finite_tree(data)
 if program in ('physical','exact','source','repaired_author','repaired_reviewer'):
  require(data.get('status')=='PASS','Missing PASS: '+program)
 if program=='physical':
  require([data.get(k) for k in ('physical_rotation_cases','target_rotation_cases','phase_direction_orbits')]==[63,54,378],'Physical counts changed')
 elif program=='exact': require(data.get('checks_total')==209,'Exact count changed')
 elif program=='source':
  require(data.get('active_checks')==187 and data.get('explicit_false_rejection') is True,'Source controls changed')
  require(data.get('optimization_flag')==int(opt),'Wrong source mode')
 elif program=='direct':
  require(data.get('optimized_mode') is opt and len(data.get('families',[]))==11,'Direct mode/count changed')
  require(len(data['exact']['low_periods'])==4 and data['exact']['false_identity_rejected'] is True,'Direct exact controls changed')
  require(data['exact']['exact_reflection_and_distinct_vertex_checks'] is True,'Direct reflection controls missing')
 elif program=='complex_v2':
  require(data['mutation']=='none' and data['optimized'] is opt,'Complex mode changed')
  require(data['counts']==dict(symbolic_identities=5,configurations=27,phases=81,wrong_parity_configurations_enforced=6,repeated_list_phases=2),'Complex counts changed')
  require(data['runtime']['sympy']=='1.14.0' and data['runtime']['mpmath']=='1.3.0' and data['runtime']['bytecode_disabled'] is True,'Complex runtime changed')
  require(data['parent_manifest']==dict(expected_sha256=COMPLEX_PARENT_SHA256,available=True,verified_if_available=True),'Complex parent layout/pin not checked')
 elif program=='repaired_author':
  require(data['exact_assertions']==37393 and data['numerical_diagnostics']==4092,'Author counts changed')
 elif program=='repaired_reviewer':
  require(data['exact_lattice_assertions']==13712 and data['high_precision_diagnostics']==348,'Reviewer counts changed')
 if program.startswith('repaired_'): require(raw==baseline_raw,'Repaired output differs bytewise from original archived JSON')
 baseline=parsed(baseline_raw);finite_tree(baseline)
 require(normalize(program,data)==normalize(program,baseline),'Valid output differs from pinned baseline: '+program)
 return normalize(program,data)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--materials',type=pathlib.Path,help='Root containing the pinned A204 relative material paths')
 parser.add_argument('--work-dir',type=pathlib.Path,help='Writable directory for disposable layouts; default system temporary directory')
 parser.add_argument('--output',default='-',help='New receipt JSON file, or - for stdout with embedded compressed evidence')
 parser.add_argument('--jobs',type=int,default=2,choices=range(1,5))
 parser.add_argument('--timeout',type=int,default=900,help='Seconds per child process')
 args=parser.parse_args();start=utc();driver_hash=digest(pathlib.Path(__file__).read_bytes())
 pin_bytes=(HERE/'INPUT_PINS.json').read_bytes()
 require(digest(pin_bytes)==PIN_MANIFEST_SHA256,'Portable INPUT_PINS.json changed')
 pins_doc=parsed(pin_bytes);pins=pins_doc['files'];require(len(pins)==142,'Expected142 input pins')
 candidates=[args.materials] if args.materials else [HERE.parent/'materials',HERE.parent.parent/'materials',HERE.parent]
 materials=None;selection=None
 for candidate in candidates:
  if candidate is not None and (candidate/'original_submitted_head').is_dir():
   materials=candidate.resolve();selection='explicit --materials' if args.materials else 'documented relative default';break
 require(materials is not None,'Cannot find materials; pass --materials PATH explicitly')
 immutable_roots=[(materials/name).resolve() for name in sorted({r.split('/')[0] for r in pins})]
 def writable(path):
  path=path.expanduser().resolve()
  require(not any(contained(path,r) for r in immutable_roots),'Write target intersects immutable material family: '+str(path))
  return path
 output=None if args.output=='-' else writable(pathlib.Path(args.output))
 archive_path=output.with_name(output.name+'.raw.json.gz') if output else None
 if output:
  require(not output.exists() and not archive_path.exists(),'Refuse to overwrite prior receipt/evidence')
  output.parent.mkdir(parents=True,exist_ok=True)
 work=writable(args.work_dir) if args.work_dir else None
 if work: work.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
 runtime=env.get('PR204_RUNTIME_PACKAGES')
 if runtime:
  runtime=str(pathlib.Path(runtime).expanduser().resolve())
  require(all((pathlib.Path(runtime)/n).is_dir() for n in ('sympy','mpmath')),'Invalid PR204_RUNTIME_PACKAGES')
  env['PR204_RUNTIME_PACKAGES']=runtime
  env['PYTHONPATH']=runtime+(os.pathsep+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
 relevant_env={k:env.get(k) for k in ('PR204_RUNTIME_PACKAGES','PYTHONPATH','PYTHONDONTWRITEBYTECODE','PYTHONHASHSEED')}
 before=snapshot(materials,pins);raw_records=[];results=[];normalized={};errors=[];lock=threading.Lock()
 parent_manifest=parsed((materials/COMPLEX_PARENT).read_bytes())
 require(digest((materials/COMPLEX_PARENT).read_bytes())==COMPLEX_PARENT_SHA256,'Complex parent manifest pin failed')
 complex_fixture=['math_independent_complex_01/'+x['path'] for x in parent_manifest['files']]+[COMPLEX_PARENT]
 cases=[]
 for program in PROGRAMS:
  mutations=['none']
  if program in ('physical','exact','repaired_author','repaired_reviewer'): mutations+=['false_identity']
  if program=='complex_v2': mutations+=['false_identity','false_numeric_identity','nan_residual']
  for mutation in mutations:
   for opt in (False,True): cases.append((program,mutation,opt))
 require(len(cases)==28,'Wrong case inventory')
 with tempfile.TemporaryDirectory(prefix='pr204-portable-',dir=work) as temporary:
  temp=pathlib.Path(temporary)
  # Locate package roots without importing either external package, then inventory caches.
  locate="import importlib.util,json,pathlib,sys; print(json.dumps({'roots':{n:str(pathlib.Path(importlib.util.find_spec(n).origin).resolve().parent) for n in ('sympy','mpmath')},'bytecode_disabled':sys.dont_write_bytecode}))"
  located=subprocess.run([sys.executable,'-B','-c',locate],env=env,cwd=temp,capture_output=True,timeout=args.timeout)
  require(located.returncode==0,'Dependency location failed: '+located.stderr.decode(errors='replace'))
  locations=parsed(located.stdout);require(locations['bytecode_disabled'] is True,'Probe bytecode enabled')
  cache_before=cache_inventory(locations['roots'].values())
  probe="import sympy,mpmath,json,sys; print(json.dumps({'sympy':sympy.__version__,'mpmath':mpmath.__version__,'files':{'sympy':sympy.__file__,'mpmath':mpmath.__file__},'bytecode_disabled':sys.dont_write_bytecode,'python':sys.version}))"
  probed=subprocess.run([sys.executable,'-B','-c',probe],env=env,cwd=temp,capture_output=True,timeout=args.timeout)
  require(probed.returncode==0,'Dependency import failed: '+probed.stderr.decode(errors='replace'))
  dependency=parsed(probed.stdout)
  require(dependency['sympy']=='1.14.0' and dependency['mpmath']=='1.3.0' and dependency['bytecode_disabled'] is True,'Require SymPy1.14.0/mpmath1.3.0 with bytecode disabled')
  for name in ('sympy','mpmath'):
   require(pathlib.Path(dependency['files'][name]).resolve().parent==pathlib.Path(locations['roots'][name]),'Dependency location changed')
   if runtime: require(contained(pathlib.Path(dependency['files'][name]).resolve(),pathlib.Path(runtime)),'Dependency escaped explicit runtime')
  def run_case(index,case):
   program,mutation,opt=case;name=program+'__'+mutation+'__'+('optimized' if opt else 'ordinary');began=utc()
   root=temp/name;root.mkdir()
   try:
    script,baseline=PROGRAMS[program]
    if program.startswith('repaired_') and mutation!='none': script=script.replace('/valid/','/false_identity/')
    rels=list(complex_fixture) if program=='complex_v2' else []
    rels.append(script)
    for rel in rels:
     require(rel in pins,'Unpinned copied source: '+rel)
     dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(materials/rel,dest)
     require(digest(dest.read_bytes())==pins[rel]['sha256'],'Temporary copy changed')
    proof_copy=None
    if program=='repaired_author':
     historical='original_submitted_head/PROOF.md';dest=(root/script).parent/'PROOF.md';shutil.copyfile(materials/historical,dest)
     require(digest(dest.read_bytes())==pins[historical]['sha256'],'Historical proof copy changed')
     proof_copy={'role':'unchanged historical original proof for legacy hash binding; NOT a current manuscript','input':historical,'sha256':pins[historical]['sha256']}
    argv=[sys.executable,'-B']+(['-O'] if opt else [])+[str(root/script)]
    if mutation!='none' and program in ('physical','exact'): argv+=['--false-identity']
    if program=='complex_v2': argv+=['--mutation',mutation]
    try:
     proc=subprocess.run(argv,env=env,cwd=root,capture_output=True,timeout=args.timeout);stdout,stderr=proc.stdout,proc.stderr;exitcode=proc.returncode;failure=None;norm=None
    except subprocess.TimeoutExpired as error:
     stdout=error.stdout or b'';stderr=error.stderr or b'';exitcode=None;failure='TIMEOUT';norm=None
    try:
     if failure: raise RuntimeError(failure)
     if mutation=='none':
      require(exitcode==0 and stderr==b'','Valid process failed: '+name)
      norm=validate_valid(program,parsed(stdout),opt,stdout,(materials/baseline).read_bytes())
     elif program=='complex_v2':
      require(exitcode==2 and stdout==b'','Complex mutation exited incorrectly')
      rejection=parsed(stderr)
      kind,label={'false_identity':('symbolic_identity','contact_minus'),'false_numeric_identity':('upper_bound','first_area_identity'),'nan_residual':('nonfinite','first_area_identity')}[mutation]
      require(rejection.get('rejected') is True and rejection.get('mutation')==mutation and rejection.get('optimized') is opt and rejection.get('kind')==kind and rejection.get('name')==label,'Complex mutation failed at wrong identity')
     else:
      require(exitcode==1 and stdout==b'','False identity exited incorrectly')
      last=stderr.decode('utf-8').strip().splitlines()[-1]
      expected={'physical':('RuntimeError:','FALSE_physical_product_plus_one'),'exact':('RuntimeError:','FALSE_three_phase_product_plus_one'),'repaired_author':('AssertionError:','universal_chord_contact_plus'),'repaired_reviewer':('AssertionError:','area product 3/1')}[program]
      require(last.startswith(expected[0]) and expected[1] in last,'False control failed for wrong reason: '+last)
     require(not any(q.name=='__pycache__' or q.suffix in ('.pyc','.pyo') for q in root.rglob('*')),'Bytecode created in temporary layout')
    except Exception as error: failure=str(error)
    item={'case':name,'program':program,'mutation':mutation,'optimized':opt,'UTC_start':began,'UTC_end':utc(),'source':script,'source_sha256':pins[script]['sha256'],'exit_code':exitcode,'expected_outcome_verified':failure is None,'stdout_sha256':digest(stdout),'stdout_bytes':len(stdout),'stderr_sha256':digest(stderr),'stderr_bytes':len(stderr),'failure':failure}
    if proof_copy: item['historical_proof_copy']=proof_copy
    with lock:
     stream={'case':name,'argv':argv,'cwd':str(root)}
     for label,raw in [('stdout',stdout),('stderr',stderr)]:
      try: stream[label+'_utf8']=raw.decode('utf-8')
      except UnicodeDecodeError: stream[label+'_b64']=base64.b64encode(raw).decode()
     results.append(item);raw_records.append(stream)
     if norm is not None: normalized[(program,opt)]=norm
     if failure: errors.append(name+': '+failure)
     print(str(len(results))+'/28 '+name+(' PASS' if failure is None else ' FAIL: '+failure),file=sys.stderr,flush=True)
   finally:
    shutil.rmtree(root,ignore_errors=True)
  with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
   futures=[pool.submit(run_case,i,case) for i,case in enumerate(cases)]
   for future in futures:
    try: future.result()
    except Exception as error: errors.append('Case setup failed: '+repr(error))
  cache_after=cache_inventory(locations['roots'].values())
  if cache_before!=cache_after: errors.append('Dependency bytecode/cache inventory changed')
  for program in PROGRAMS:
   if (program,False) not in normalized or (program,True) not in normalized: errors.append('Missing valid mode pair: '+program)
   elif normalized[(program,False)]!=normalized[(program,True)]: errors.append('Mode comparison failed: '+program)
 after=snapshot(materials,pins)
 if before!=after: errors.append('Material hash/size/mtime/ctime changed')
 if len(results)!=28: errors.append('Only '+str(len(results))+' of28 cases recorded')
 results.sort(key=lambda x:x['case']);raw_records.sort(key=lambda x:x['case'])
 evidence={'input_before':before,'input_after':{'identical_to':'input_before'} if before==after else after,'dependency_cache_before':cache_before,'dependency_cache_after':{'identical_to':'dependency_cache_before'} if cache_before==cache_after else cache_after,'dependency_location_probe':{'stdout_b64':base64.b64encode(located.stdout).decode(),'stderr_b64':base64.b64encode(located.stderr).decode()},'dependency_version_probe':{'stdout_b64':base64.b64encode(probed.stdout).decode(),'stderr_b64':base64.b64encode(probed.stderr).decode()},'raw_cases':raw_records}
 compressed=gzip.compress(compact(evidence),mtime=0)
 if digest(pathlib.Path(__file__).read_bytes())!=driver_hash: errors.append('Driver changed during execution')
 report={'schema':'pr204-portable-run-v1','status':'PASS' if not errors else 'FAIL','UTC_start':start,'UTC_end':utc(),'driver_sha256':driver_hash,'input_manifest_sha256':PIN_MANIFEST_SHA256,'materials':str(materials),'materials_selection':selection,'input_files_checked':len(pins),'input_before_after_equal_including_ctime':before==after,'input_snapshot_sha256_before':digest(compact(before)),'input_snapshot_sha256_after':digest(compact(after)),'runtime':dependency,'environment_overrides':relevant_env,'python_executable':sys.executable,'work_dir':str(work) if work else 'system TemporaryDirectory','jobs':args.jobs,'case_timeout_seconds':args.timeout,'full_valid_runs':sum(x['mutation']=='none' and x['expected_outcome_verified'] for x in results),'intended_false_rejections':sum(x['mutation']!='none' and x['expected_outcome_verified'] for x in results),'required_cases':28,'recorded_cases':len(results),'normalization_only':NORMALIZATION,'all_valid_mode_pairs_match':all(normalized.get((p,False))==normalized.get((p,True)) and (p,False) in normalized for p in PROGRAMS),'dependency_cache_inventory_before':{k:v for k,v in cache_before.items() if k!='records'},'dependency_cache_inventory_after':{k:v for k,v in cache_after.items() if k!='records'},'raw_archive_sha256':digest(compressed),'raw_archive_bytes':len(compressed),'cases':results,'errors':errors,'historical_bare_assert_scripts_executed':False,'limits':'Finite exact controls and noninterval diagnostics. No universal proof or novelty certification.'}
 if output:
  archive_path.write_bytes(compressed);report['raw_archive_file']=archive_path.name;output.write_bytes(compact(report)+b'\n')
 else:
  report['raw_archive_gzip_base64']=base64.b64encode(compressed).decode();sys.stdout.buffer.write(compact(report)+b'\n')
 return 0 if not errors else 1

if __name__=='__main__':
 try: raise SystemExit(main())
 except Exception as error:
  print(json.dumps({'status':'FAIL','error':str(error),'type':type(error).__name__},sort_keys=True),file=sys.stderr)
  raise SystemExit(1)
