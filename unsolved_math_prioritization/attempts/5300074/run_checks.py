#!/usr/bin/env python3
"""Full-count deterministic unittest execution and intended semantic mutations.

Complete JSON output is compared as raw bytes; no output normalization occurs.
Test-result objects deliberately report exception class/message instead of a
wall-clock timer or nondeterministic traceback. This is not an analytic prover.
"""
import contextlib,hashlib,io,json,os,runpy,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,label):
 if not ok:raise ValueError(label)
EXACT=['test_disk_expansion_identity','test_named_rotation_sets','test_non_rotation_orbit_rejected','test_quadratic_coefficients_exactly','test_small_periodic_orbits']
INDEPENDENT=['test_all_small_invariant_subsets','test_integer_oracle_616_cases','test_quadratic_conjugacy_polynomial_identity','test_wringing_beltrami_algebra']
MUTANTS={
 'angle_instead_of_rotation':('self.rotation = Q(shift, m)','self.rotation = a[0]','test_named_rotation_sets','AssertionError','Fraction(1, 3) != Fraction(1, 2)'),
 'reverse_rotation':('self.rotation = Q(shift, m)','self.rotation = Q((-shift) % m, m)','test_named_rotation_sets','AssertionError','Fraction(2, 3) != Fraction(1, 3)'),
 'wrong_gap_denominator':('(a[i + 1] - a[i])','(a[i + 1] - a[i] + 1)','test_named_rotation_sets','AssertionError','Fraction(5, 6) != Fraction(1, 3)'),
 'omit_degree_one_increment':('self.slopes[j] * (u - self.x[j]) + shift','self.slopes[j] * (u - self.x[j])','test_named_rotation_sets','AssertionError','Fraction(1, 7) != Fraction(8, 7)'),
 'truncate_negative_translation':('shift = (t - self.x[0]).numerator // (t - self.x[0]).denominator','shift = int(t - self.x[0])','test_named_rotation_sets','RuntimeError','A degree-one fundamental interval was missed'),
 'remove_affine_interpolation':('self.slopes[j] * (u - self.x[j])','0 * (u - self.x[j])','test_named_rotation_sets','AssertionError','Fraction(2, 3) != Fraction(1, 3)'),
 'iterate_one_too_few':('for _ in range(n):','for _ in range(max(0,n-1)):','test_named_rotation_sets','AssertionError','Fraction(1, 3) != 1'),
 'wrong_centered_parameter_sign':('lam[0] / 2 - square[0] / 4','lam[0] / 2 + square[0] / 4','test_quadratic_coefficients_exactly','AssertionError','Fraction(31, 16)'),
 'wrong_other_multiplier_sign':('other_multiplier = (2 - lam[0], -lam[1])','other_multiplier = (2 - lam[0], lam[1])','test_quadratic_coefficients_exactly','AssertionError','Fraction(-1, 2)'),
 'drop_disk_cross_term':('2*radius*x-x*x-y*y','radius*x-x*x-y*y','test_disk_expansion_identity','AssertionError','Fraction(-28217, 576) != Fraction(-28225, 576)'),
 'restore_invalid_negative_fixture':('FiniteRotationLift(2, [Q(1, 5), Q(2, 5), Q(3, 5), Q(4, 5)])','FiniteRotationLift(2, [Q(1, 15), Q(2, 15), Q(4, 15), Q(8, 15)])','test_non_rotation_orbit_rejected','AssertionError','ValueError not raised'),
}
def readonly(p):
 rows=[]
 for f in [p,*sorted(p.iterdir())]:
  directory=f==p;need((f.stat().st_mode&0o777)==(0o555 if directory else 0o444) and not os.access(f,os.W_OK),'physical read-only fixture')
  try:fd=os.open(f/'FORBIDDEN_CREATE' if directory else f,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if directory else os.O_APPEND),0o600)
  except PermissionError as e:need(e.errno==13,'EACCES required');rows.append(dict(path='.' if directory else f.name,errno=13,denied=True))
  else:os.close(fd);raise ValueError('physical write unexpectedly permitted')
 return rows
def guard(event,args):
 if event=='open':
  _,mode,flags=args
  if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):raise RuntimeError('Forbidden write')
 if event.startswith('socket.') or event in {'os.remove','os.rename','os.rmdir','os.mkdir','os.chmod','os.chown','os.link','os.symlink','subprocess.Popen','os.system'}:raise RuntimeError('Forbidden external side effect: '+event)
class Result(unittest.TestResult):
 def __init__(self):super().__init__();self.rows=[]
 def record(self,t,status,err=None):
  row=dict(test=t._testMethodName,status=status)
  if err:row.update(exception=err[0].__name__,message=str(err[1]))
  self.rows.append(row)
 def addSuccess(self,t):super().addSuccess(t);self.record(t,'PASS')
 def addFailure(self,t,e):super().addFailure(t,e);self.record(t,'FAIL',e)
 def addError(self,t,e):super().addError(t,e);self.record(t,'ERROR',e)
 def addSkip(self,t,reason):super().addSkip(t,reason);self.record(t,'SKIP')
 def addExpectedFailure(self,t,e):super().addExpectedFailure(t,e);self.record(t,'EXPECTED_FAILURE',e)
 def addUnexpectedSuccess(self,t):super().addUnexpectedSuccess(t);self.record(t,'UNEXPECTED_SUCCESS')
def complete(x,expected,baseline):
 need(type(x) is dict and type(x['tests_run']) is int and x['tests_run']==len(expected),'exact full test count')
 need(type(x['records']) is list and [r['test'] for r in x['records']]==expected,'all named tests executed exactly once')
 need(x['skips']==x['expected_failures']==x['unexpected_successes']==0,'no skipped or expected-failure tests')
 need(not x['stopped_early'],'suite did not stop early')
 if baseline:need(x['errors']==x['failures']==0 and all(r['status']=='PASS' for r in x['records']),'baseline requires zero errors and failures')
def child(script):
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 p=Path.cwd();denials=readonly(p);sys.addaudithook(guard)
 expected=INDEPENDENT if script=='independent_exact_checks.py' else EXACT
 ns={'__name__':'guarded_checks','__file__':script};sys.argv=[script]
 if script=='independent_exact_checks.py':sys.argv.append('verify_exact.py')
 raw=Path(script).read_bytes();exec(compile(raw,script,'exec'),ns)
 cls=ns['IndependentChecks' if script=='independent_exact_checks.py' else 'ExactChecks']
 names=unittest.defaultTestLoader.getTestCaseNames(cls)
 need(names==expected,'exact discovered suite names')
 suite=unittest.TestSuite(cls(n) for n in names);need(suite.countTestCases()==len(expected),'nonempty complete discovered suite')
 out=io.StringIO();err=io.StringIO();r=Result()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):suite.run(r)
 x=dict(schema=1,uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,tests_run=r.testsRun,records=r.rows,errors=len(r.errors),failures=len(r.failures),skips=len(r.skipped),expected_failures=len(r.expectedFailures),unexpected_successes=len(r.unexpectedSuccesses),stopped_early=r.shouldStop,captured_stdout=out.getvalue(),captured_stderr=err.getvalue(),physical_denials=denials,runtime_guard=True)
 print(json.dumps(x,sort_keys=True))
 return 0 if r.wasSuccessful() else 1

def main():
 need(len(sys.argv)==1,'no arguments');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 root=Path(__file__).resolve().parent;mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]
 sources={n:(root/n).read_bytes() for n in ('verify_exact.py','independent_exact_checks.py')};src=sources['verify_exact.py'].decode();records=[];suite_controls=[]
 with tempfile.TemporaryDirectory(prefix='external-ray-mathematics-') as td:
  p=Path(td)
  for n,raw in sources.items():(p/n).write_bytes(raw)
  for name,(old,new,*_) in MUTANTS.items():need(src.count(old)==1,'unique mutation anchor '+name);(p/(name+'.py')).write_text(src.replace(old,new))
  controls={
   'empty_suite':src.replace('def test_','def omitted_'),
   'incomplete_suite':src.replace('def test_disk_expansion_identity','def omitted_disk_expansion_identity'),
   'skipped_suite':src.replace('    def test_disk_expansion_identity','    @unittest.skip("synthetic skipped fixture")\n    def test_disk_expansion_identity'),
   'errored_suite':src.replace('    def test_disk_expansion_identity(self):','    def test_disk_expansion_identity(self):\n        raise RuntimeError("synthetic unrelated runtime error")'),
   'expected_failure_suite':src.replace('    def test_disk_expansion_identity(self):','    @unittest.expectedFailure\n    def test_disk_expansion_identity(self):\n        self.fail("synthetic expected failure")'),
   'unexpected_success_suite':src.replace('    def test_disk_expansion_identity','    @unittest.expectedFailure\n    def test_disk_expansion_identity')}
  for n,s in controls.items():(p/(n+'.py')).write_text(s)
  for f in p.iterdir():f.chmod(0o444)
  p.chmod(0o555)
  def snapshot():return {f.name:dict(bytes=f.stat().st_size,sha256=sha(f.read_bytes())) for f in sorted(p.iterdir())}
  before=snapshot();physical=readonly(p)
  try:
   def run(name):
    r=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'run_checks.py'),'--child',name],cwd=p,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=120)
    row=dict(script=name,exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),stdout_bytes=len(r.stdout),stdout_sha256=sha(r.stdout),stderr_bytes=len(r.stderr),stderr_sha256=sha(r.stderr));return r,row
   for n,count,line in [('verify_exact.py',EXACT,'Exact finite rotation orbits checked: 616\n'),('independent_exact_checks.py',INDEPENDENT,'SMALL_INVARIANT_SUBSETS_ACCEPTED 238 REJECTED_NON_ROTATION 423\nINDEPENDENT_ORBIT_COUNT 616 DISTINCT_DEGREE_AND_SET_PAIRS 150\n')]:
    r,row=run(n);need(r.returncode==0 and r.stderr==b'','baseline complete output');x=json.loads(r.stdout);complete(x,count,True);need(x['captured_stdout']==line and x['captured_stderr']=='','exact enumeration output');row.update(accepted=True,full_test_count=len(count),errors=0,skips=0);records.append(row)
   for name,(_,_,test,exception,message) in MUTANTS.items():
    r,row=run(name+'.py');need(r.returncode==1 and r.stderr==b'','semantic mutant execution');x=json.loads(r.stdout);complete(x,EXACT,False)
    expected_errors=1 if name=='truncate_negative_translation' else 0;need(x['errors']==expected_errors,'no unrelated mutant errors')
    target=[q for q in x['records'] if q['test']==test];need(len(target)==1 and target[0]['exception']==exception and message in target[0]['message'],'intended named semantic failure '+name)
    need(all(q['status'] in ('PASS','FAIL') or (name=='truncate_negative_translation' and q['test']==test and q['exception']=='RuntimeError' and q['message']==message) for q in x['records']),'only intended failures')
    need(x['captured_stderr']=='','no hidden diagnostic output');row.update(rejected=True,intended_test=test,intended_exception=exception,intended_message=message,full_test_count=5,skips=0);records.append(row)
   for name in controls:
    r,row=run(name+'.py')
    if name in ('empty_suite','incomplete_suite'):
     need(r.returncode==1 and r.stdout==b'' and r.stderr==b'REJECT: mathematical guard: exact discovered suite names\n','empty/incomplete suite rejected before execution');why='exact discovered suite names'
    else:
     need(r.stderr==b'','suite control unexpected stderr');x=json.loads(r.stdout)
     try:complete(x,EXACT,True)
     except ValueError as exc:why=str(exc)
     else:raise ValueError('bad suite accepted '+name)
    row.update(rejected=True,condition=why);suite_controls.append(row)
   after=snapshot();need(after==before,'mathematical fixtures changed')
  finally:
   p.chmod(0o755)
   for f in p.iterdir():f.chmod(0o644)
 need(all((root/n).read_bytes()==raw for n,raw in sources.items()),'accepted source changed')
 print(json.dumps(dict(schema=1,problem_id=5300074,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,positive_runs=2,positive_test_counts=[5,4],mathematical_negative_controls=11,suite_validity_negative_controls=6,runs=records,suite_controls=suite_controls,physical_denials=physical,before=before,after=after,fixture_unchanged=True,source_unchanged=True,normalization='NONE',historical_replay='NOT_RUN',scope='Exact finite arithmetic and intended mutation checks; analytic proofs and missing indifferent-boundary statements are not machine verified.'),sort_keys=True))
if __name__=='__main__':
 try:
  if len(sys.argv)==3 and sys.argv[1]=='--child':sys.exit(child(sys.argv[2]))
  else:main()
 except (ValueError,TypeError,KeyError,OSError,subprocess.TimeoutExpired) as exc:print('REJECT: mathematical guard: '+str(exc),file=sys.stderr);sys.exit(1)
