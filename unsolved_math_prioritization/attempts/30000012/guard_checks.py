#!/usr/bin/env python3
"""Fresh semantic and CLI controls; expected failures never replace positives."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
EXPECTED_ERRORS = {'algebraic_dimensions_add': 'CHECK_FAILED[field_scope]: elliptic K3 disproves unqualified additivity\n', 'blowup_preserves_positive_degrees': 'CHECK_FAILED[normal_data]: lifted fibre normal is trivial\n', 'conic_scaling_retained': 'CHECK_FAILED[dimensions]: nonzero quadrics modulo scalar\n', 'finite_incidence_dropped': 'CHECK_FAILED[source_interface]: BM finite-incidence hypothesis retained\n', 'full_tangent_replaces_normal': 'CHECK_FAILED[normal_data]: quotient by TY discards plane slope\n', 'incidence_condition_dropped': 'CHECK_FAILED[dimensions]: main incident conic parameter dimension\n', 'initial_data_fibre_off_by_one': 'CHECK_FAILED[normal_data]: initial normal-data generic fibre dimension\n', 'local_rank_promoted_to_global_finite': 'CHECK_FAILED[proof_scope]: local rank is not a global finite map assertion\n', 'local_separation_dropped': 'CHECK_FAILED[source_interface]: BM separation hypothesis retained\n', 'nondivisible_trace_survives': 'CHECK_FAILED[trace]: independent multiplication-matrix trace\n', 'peternell_kahler_removed': 'CHECK_FAILED[source_interface]: Peternell curve case scope\n', 'plane_parameter_shift': 'CHECK_FAILED[dimensions]: planes containing a fixed P1 in P4\n', 'polynomial_growth_removed': 'CHECK_FAILED[proof_scope]: unproved boundary bound remains a hypothesis\n', 'pure_y_coefficient_sign': 'CHECK_FAILED[logarithm]: Euler derivative/inverse-series oracle\n', 'residual_case_erased': 'CHECK_FAILED[source_interface]: residual case not silently solved\n', 'shape_coefficient_sign': 'CHECK_FAILED[logarithm]: Euler derivative/inverse-series oracle\n', 'shape_pole_promoted': 'CHECK_FAILED[logarithm]: Euler derivative/inverse-series oracle\n', 'target_dimensions_swapped': 'CHECK_FAILED[source_interface]: OWR dimensions\n', 'target_kahler_added': 'CHECK_FAILED[source_interface]: OWR has no Kahler hypothesis\n', 'trace_degree_factor_removed': 'CHECK_FAILED[trace]: independent multiplication-matrix trace\n', 'trace_exponent_shifted': 'CHECK_FAILED[trace]: independent multiplication-matrix trace\n', 'trace_laurent_series_truncated': 'CHECK_FAILED[trace_series]: nonzero negative Laurent coefficients persist\n'}
SCOPE_GUARDS = {'local_rank_promoted_to_global_finite', 'finite_incidence_dropped', 'polynomial_growth_removed', 'peternell_kahler_removed', 'target_kahler_added', 'target_dimensions_swapped', 'local_separation_dropped', 'residual_case_erased'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def main():
 root=Path(__file__).resolve().parent
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 files=sorted(str(p.relative_to(root)) for p in (root/'current').iterdir())
 need(len(files)==19,'exact 19 accepted input identities')
 def snapshot():return {n:dict(bytes=len(b),sha256=sha(b)) for n in files for b in [(root/n).read_bytes()]}
 before=snapshot();physical=[]
 for p,label,create in [(root/'current','current',True),(root/'current/check_exact.py','current/check_exact.py',False)]:
  need(not p.stat().st_mode&0o222 and not os.access(p,os.W_OK),'read-only mode')
  try:fd=os.open(p/'DENIED' if create else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if create else os.O_APPEND),0o600)
  except PermissionError as exc:need(exc.errno==13,'EACCES required');physical.append(dict(path=label,operation='create' if create else 'append_open',errno=13,denied=True))
  else:os.close(fd);raise ValueError('physical denial missing')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C');runs=[];cli=[]
 def run(script,*args):return subprocess.run([sys.executable,'-I','-S','-B',*mode,script,*args],cwd=root,env=env,capture_output=True,timeout=100)
 for name,count in [('exact',600),('negative',12),('all',612)]:
  for fail in [False,True]:
   r=run('current/check_exact.py','--mode',name,*(['--inject-failure'] if fail else []))
   expected=dict(status='FAIL' if fail else 'PASS',mode=name,checks=count)
   if fail:expected['error']='Deliberately injected failure'
   expected.update(arithmetic='exact',numerical_claims=False)
   if not fail:expected['scope']='Finite algebraic checks only; not a geometric proof certificate'
   raw=(json.dumps(expected)+'\n').encode()
   need(type(r.returncode) is int and r.returncode==(1 if fail else 0) and r.stdout==raw and r.stderr==b'' and same(json.loads(r.stdout),expected),'wrong original CLI identity/count/output')
   cli.append(dict(control=name+('_injected_failure' if fail else '_positive'),category='injected_failure_control' if fail else 'positive_suite',expected_exit=1 if fail else 0,exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),full_raw_output_equal=True,recursive_exact_json_equal=True))
 invalid=run('current/check_exact.py','--mode','not-a-mode')
 invalid_error=b"usage: check_exact.py [-h] [--mode {exact,negative,all}] [--inject-failure]\ncheck_exact.py: error: argument --mode: invalid choice: 'not-a-mode' (choose from exact, negative, all)\n"
 need(invalid.returncode==2 and invalid.stdout==b'' and invalid.stderr==invalid_error,'exact invalid CLI rejection')
 invalid_record=dict(exit_code=invalid.returncode,stdout=invalid.stdout.decode(),stderr=invalid.stderr.decode(),category='CLI_schema_control')
 for mutant,error in EXPECTED_ERRORS.items():
  r=run('current/audit_exact.py','--require-readonly','--mutant',mutant)
  need(r.returncode==1 and r.stdout==b'' and r.stderr==error.encode(),'wrong semantic rejection '+mutant)
  runs.append(dict(control=mutant,category='documentary_scope_guard' if mutant in SCOPE_GUARDS else 'finite_mathematics',exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),intended_rejection_verified=True))
 need(len(runs)==22 and len({r['control'] for r in runs})==22,'exact semantic identities')
 need(sum(r['category']=='finite_mathematics' for r in runs)==14,'exact mutant categories')
 after=snapshot();need(after==before,'protected mathematics changed')
 print(json.dumps(dict(schema=1,problem_id=30000012,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,semantic_mutants=22,finite_mathematics_mutants=14,documentary_scope_mutants=8,physical_denials=physical,runs=runs,original_cli=cli,invalid_cli=invalid_record,positive_cli_suites=3,injected_failure_controls=3,before=before,after=after,whole_mathematics_unchanged=True,limitations='Finite mathematics, documentary scope guards and injected failures are separate; analytic theorems and infinite claims require written proof review.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as exc:print('REJECT: semantic controls failed: '+str(exc),file=sys.stderr);sys.exit(1)
