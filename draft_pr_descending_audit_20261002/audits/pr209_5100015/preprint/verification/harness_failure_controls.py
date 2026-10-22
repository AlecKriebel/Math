"""Synthetic failure controls of the actual replay harness; no scientific checker runs.

Execute exact orchestration AST with subprocess replaced solely by controlled child
outcomes. Synthetic successful child JSON is fixture data, never scientific evidence.
All fixture outputs are outside the archive and explicitly labelled synthetic.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,contextlib,hashlib,importlib.util,io,json,subprocess,sys,types
if not __debug__ or sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Use Python -B without optimization')
V=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True);args=parser.parse_args();OUT=Path(args.output).resolve()
assert not OUT.exists() and not OUT.is_relative_to(V.parent) and not V.parent.is_relative_to(OUT)
OUT.mkdir(parents=True)
raw=(V/'run_checks.py').read_bytes();tree=ast.parse(raw)
cases=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='cases' for t in n.targets)))
byprogram={Path(row[1]).name:row for row in cases}
# Retain actual source orchestration/functions; redirect only child process API.
for node in tree.body:
 if isinstance(node,ast.Import):node.names=[a for a in node.names if a.name!='subprocess']
tree.body=[n for n in tree.body if not(isinstance(n,ast.ImportFrom) and n.module=='integrity') and not(isinstance(n,ast.Import) and not n.names)]
code=compile(tree,str(V/'run_checks.py')+'[controlled-child-fixtures]','exec')
spec=importlib.util.spec_from_file_location('integrity_for_failure_controls',V/'integrity.py');integrity=importlib.util.module_from_spec(spec);spec.loader.exec_module(integrity)
rows=[];stdout_marker=b'partial fixture stdout\x00\xff\n';stderr_marker=b'partial fixture stderr\x00\xfe\n'
for mode in ['success_fixture','ordinary_nonzero_exit','timeout_with_binary_partial_output','launch_error','after_input_integrity_failure']:
 target=OUT/mode;calls=[];verification_calls=[]
 def verify():
  verification_calls.append(True)
  if mode=='after_input_integrity_failure' and len(verification_calls)==2:raise AssertionError('controlled after-input integrity failure; no actual input mutation')
  return integrity.verify()
 def child(command,**kw):
  program=Path(command[2]);case=byprogram[program.name];name,script,copytree,outfile,expected,ignored=case;calls.append(name)
  if name=='classical_bridge':
   if mode=='ordinary_nonzero_exit':return subprocess.CompletedProcess(command,17,stdout_marker,stderr_marker)
   if mode=='timeout_with_binary_partial_output':raise subprocess.TimeoutExpired(command,kw['timeout'],output=stdout_marker,stderr=stderr_marker)
   if mode=='launch_error':raise FileNotFoundError('controlled executable lookup failure')
  expected_bytes=(V/expected).read_bytes()
  if outfile:
   output=Path(command[command.index('--output')+1]) if name=='physical' else Path(kw['cwd'])/outfile
   output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(expected_bytes)
   return subprocess.CompletedProcess(command,0,b'SYNTHETIC child fixture; no scientific execution\n',b'')
  return subprocess.CompletedProcess(command,0,expected_bytes,b'')
 ns=dict(__file__=str(V/'run_checks.py'),__name__='__main__',subprocess=types.SimpleNamespace(run=child,TimeoutExpired=subprocess.TimeoutExpired),verify=verify)
 original_argv=sys.argv;sys.argv=[str(V/'run_checks.py'),'--output',str(target),'--jobs','2'];stream=io.StringIO();exitcode=None
 try:
  with contextlib.redirect_stdout(stream):
   try:exec(code,ns)
   except SystemExit as e:exitcode=e.code
 finally:sys.argv=original_argv
 (target/'THIS_IS_SYNTHETIC.json').write_text(json.dumps(dict(scope=__doc__,mode=mode),indent=2)+'\n');(target/'harness_stdout.txt').write_text(stream.getvalue())
 receipt=json.loads((target/'REPRODUCTION.json').read_text());assert len(calls)==len(cases)==8 and len(receipt['results'])==8 and len(verification_calls)==2
 expected_pass=mode=='success_fixture';assert receipt['status']==('PASS' if expected_pass else 'FAIL') and exitcode==(0 if expected_pass else 1)
 failed=[r for r in receipt['results'] if r['status']=='FAIL']
 if mode in ['ordinary_nonzero_exit','timeout_with_binary_partial_output','launch_error']:
  assert len(failed)==1 and failed[0]['name']=='classical_bridge' and len([r for r in receipt['results'] if r['status']=='PASS'])==7
  r=failed[0];folder=target/'classical_bridge';assert receipt['input_integrity_error'] is None
  if mode!='launch_error':assert (folder/'stdout.txt').read_bytes()==stdout_marker and (folder/'stderr.txt').read_bytes()==stderr_marker
  else:assert (folder/'stdout.txt').read_bytes()==(folder/'stderr.txt').read_bytes()==b'' and r['execution_error']['kind']=='launch_error'
  if mode.startswith('timeout'):assert r['execution_error']['kind']=='timeout' and r['returncode'] is None
 if mode=='after_input_integrity_failure':assert not failed and receipt['input_integrity_error'] is not None
 rows.append(dict(mode=mode,actual_harness_exit=exitcode,aggregate_status=receipt['status'],all_eight_synthetic_outcomes_retained=True,before_after_checks_called=2,failed_suite_count=len(failed),role='Synthetic orchestration evidence only; no scientific program executed'))
# Full-archive output isolation must reject before creating a sibling in the archive.
for guard,name in [('archive_output','synthetic-output-must-not-exist')]:
 target=V.parent/name;assert not target.exists();original_argv=sys.argv;sys.argv=[str(V/'run_checks.py'),'--output',str(target)]
 try:
  try:exec(code,dict(__file__=str(V/'run_checks.py'),__name__='__main__',subprocess=types.SimpleNamespace(run=lambda *a,**k: (_ for _ in ()).throw(AssertionError('Child must not run')),TimeoutExpired=subprocess.TimeoutExpired),verify=integrity.verify));raise RuntimeError('Unsafe output accepted')
  except AssertionError as exc:assert 'outside the entire source archive' in str(exc)
 finally:sys.argv=original_argv
 assert not target.exists();rows.append(dict(mode=guard,rejected_before_directory_or_child=True))
for name in ['run_checks.py','integrity.py']:
 command=[sys.executable,'-B','-O',str(V/name)]
 if name=='run_checks.py':command+=['--output',str(OUT/'optimized-output-must-not-exist')]
 run=subprocess.run(command,capture_output=True);assert run.returncode!=0 and b'Optimized Python' in run.stderr and not (OUT/'optimized-output-must-not-exist').exists()
 (OUT/(name+'.optimized-stderr.txt')).write_bytes(run.stderr);rows.append(dict(mode='optimized_'+name,rejected=True))
integrity.verify()
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',tested_actual_harness_sha256=hashlib.sha256(raw).hexdigest(),tested_integrity_sha256=hashlib.sha256((V/'integrity.py').read_bytes()).hexdigest(),controls=rows,role='All child outcomes in orchestration tests are synthetic, explicitly labelled, and not scientific reproduction. Actual eight-suite reproduction is a separate real execution.',no_scientific_program_or_network_executed=True)
(OUT/'HARNESS_FAILURE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
