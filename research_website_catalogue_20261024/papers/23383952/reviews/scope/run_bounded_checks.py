"""Safe inspected arithmetic runs only, with outputs in this evidence namespace.
The geometric supplied program writes beside itself and is deliberately not run.
"""
from pathlib import Path
import subprocess,datetime,json,hashlib
E=Path(__file__).resolve().parent;S=E.parents[1]/'sources';script=S/'published-source/trace_audit_01/check_trace_bounds.py';out=E/'execution';out.mkdir(exist_ok=True);tmp=E/'tmp';tmp.mkdir(exist_ok=True)
py='/Users/alec/Documents/Math/research_website_catalogue_20261024/tmp/shared-math-runtime/bin/python'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
tasks=[('supplied-trace',[py,'-I','-B',str(script)],0),('supplied-trace-optimized',[py,'-I','-B','-O',str(script)],0),('independent-rational',[py,'-I','-B',str(E/'independent_rational.py')],0)]
# Import executes definitions only; source was fully inspected and has no
# top-level writes. Definitions are called with deliberately invalid controls.
prefix='import importlib.util; from fractions import Fraction; s=importlib.util.spec_from_file_location("trace_checked",'+repr(str(script))+'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); '
for label,call in [('short-cylinder','m.calculate(length=1)'),('false-round-threshold','m.calculate(round_limit=Fraction(1,2))'),('invalid-root-domain','m.sqrt_bracket(Fraction(9))'),('invalid-tail-time','m.remaining_upper(Fraction(1))'),('invalid-Taylor-ratio','m.positive_exponential_bracket(Fraction(20),14)')]:tasks.append(('negative-'+label,[py,'-I','-B','-O','-c',prefix+call],1))
receipts=[]
for label,cmd,expected in tasks:
 start=now();r=subprocess.run(cmd,cwd=tmp,capture_output=True,timeout=45)
 p=out/(label+'.stdout.txt');q=out/(label+'.stderr.txt');assert not p.exists() and not q.exists();p.write_bytes(r.stdout);q.write_bytes(r.stderr)
 rec={'label':label,'command':cmd,'cwd':str(tmp),'started_utc':start,'completed_utc':now(),'returncode':r.returncode,'expected_returncode':expected,'stdout':{'path':str(p),'bytes':len(r.stdout),'sha256':sha(r.stdout)},'stderr':{'path':str(q),'bytes':len(r.stderr),'sha256':sha(r.stderr)}};receipts.append(rec)
 if r.returncode!=expected:raise RuntimeError(rec)
 if label=='supplied-trace':
  data=json.loads(r.stdout);limits=[629002,631338,636143,639464,641172,641202,639541];from fractions import Fraction as F
  vals=[F(data['small_time_bound_exact'])]+[F(x['bound_exact']) for x in data['middle_intervals']]
  assert all(v<F(c,10**6) for v,c in zip(vals,limits));rec['all_seven_displayed_rows_checked_from_actual_stdout']=True
f=E/'EXECUTION_RECEIPTS.json';assert not f.exists();f.write_text(json.dumps({'utc':now(),'runs':receipts,'supplied_source_sha256':sha(script.read_bytes()),'source_code_inspected_before_execution':True,'finite_arithmetic_not_universal_time_grid':True,'geometry_program_not_run_because_it_writes_next_to_source':True},indent=2)+'\n');print(json.dumps({'positive_runs':3,'negative_runs':5,'all_expected_statuses_observed':True},indent=2))
