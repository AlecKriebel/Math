#!/usr/bin/env python3
"""Isolated installed-dependency adapter and actual source-mutation executor.
Only Python's trusted stdlib and version-checked installed SymPy/mpmath are used.
No site startup hooks, current-directory imports, environment package paths, or writes.
"""
import contextlib,hashlib,io,json,math,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
PROGRAMS=['check_hall_certificates.py', 'check_gamma_orders.py', 'independent_checks.py', 'check_scalar_specialization.py']
MUTATIONS=[('matching_orientation', 'prec(S[y[1]],S[x[1]])', 'prec(S[x[1]],S[y[1]])', 'MATCHING_ORIENTATION'), ('shift_direction', 'tuple(t-1 for t in S[a])', 'tuple(t+1 for t in S[a])', 'SHIFT_DIRECTION'), ('gamma_ratio_direction', 'gamma(S[b],S[a],chi,3).subs(z,1/z)/gamma(S[a],S[b],chi,3)', 'gamma(S[a],S[b],chi,3)/gamma(S[b],S[a],chi,3).subs(z,1/z)', 'Bad scalar valuation'), ('overlap_zero_order_capped_at_one', 'return mult(num)-mult(den)', 'return min(1,mult(num)-mult(den))', 'Bad scalar valuation'), ('illegal_linked_swap_order', "orders=['EDCBA','ECDBA','EDBCA']", "orders=['EDCBA','CEDBA','EDBCA']", 'Invalid order'), ('missing_odd_cycle_closing_edge', "edges=[('E','D'),('D','B'),('B','A'),('A','C'),('C','E')]", "edges=[('E','D'),('D','B'),('B','A'),('A','C')]", 'Parity obstruction absent')]
def need(ok,reason):
 if not ok:raise RuntimeError(reason)
def strict_json(raw):
 def unique(pairs):
  result={}
  for key,value in pairs:
   if key in result:raise ValueError('duplicate inner JSON key')
   result[key]=value
  return result
 def nonfinite(token):raise ValueError('nonfinite inner JSON')
 def finite_float(token):
  value=float(token)
  if not math.isfinite(value):raise ValueError('overflow inner JSON')
  return value
 return json.loads(raw,object_pairs_hook=unique,parse_constant=nonfinite,parse_float=finite_float)
def streams(out,err):
 stdout=out.getvalue();stderr=err.getvalue()
 return dict(checker_stdout=stdout,checker_stderr=stderr,checker_stdout_bytes=len(stdout.encode('utf-8')),checker_stderr_bytes=len(stderr.encode('utf-8')),checker_stdout_sha256=hashlib.sha256(stdout.encode('utf-8')).hexdigest(),checker_stderr_sha256=hashlib.sha256(stderr.encode('utf-8')).hexdigest())
def trusted_dependencies():
 site=Path(sys.base_prefix)/'lib'/('python'+str(sys.version_info.major)+'.'+str(sys.version_info.minor))/'site-packages'
 need(site.is_dir() and not site.is_symlink(),'trusted installed dependency path missing')
 sys.path.append(str(site))
 import sympy,mpmath
 need(sympy.__version__=='1.14.0' and mpmath.__version__=='1.3.0','installed dependency version mismatch')
 for module,name in [(sympy,'sympy'),(mpmath,'mpmath')]:
  need(Path(module.__file__).resolve()==(site/name/'__init__.py').resolve(),'installed dependency origin mismatch')
 return {'sympy':'1.14.0','mpmath':'1.3.0','mode':'explicit installed path; -I -S -B; no site hooks'}
def main():
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required')
 need(len(sys.argv) in (2,3),'program and optional mutation required')
 program=sys.argv[1];mutation=sys.argv[2] if len(sys.argv)==3 else None
 need(program in PROGRAMS and (mutation is None or program=='independent_checks.py'),'exact program')
 source=(HERE/'current'/program).read_text();original_sha=hashlib.sha256(source.encode()).hexdigest()
 if mutation is not None:
  candidates=[row for row in MUTATIONS if row[0]==mutation];need(len(candidates)==1,'known mutation')
  _,old,new,_=candidates[0];need(source.count(old)==1,'unique actual mutation')
  source=source.replace(old,new);need(hashlib.sha256(source.encode()).hexdigest()!=original_sha,'actual altered source required')
 dependencies=trusted_dependencies() if program in ('independent_checks.py','check_scalar_specialization.py') else {}
 out=io.StringIO();err=io.StringIO();sys.argv=[program]
 try:
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
   exec(compile(source,'<isolated-authored-finite-check>','exec'),{'__name__':'__main__','__file__':str(HERE/'current'/program)})
 except RuntimeError as error:
  need(out.getvalue()=='' and err.getvalue()=='','unexpected output before finite rejection')
  result=dict(status='FAIL',error_type='RuntimeError',reason=str(error),program=program,mutation=mutation,actual_source_sha256=hashlib.sha256(source.encode()).hexdigest(),uid=os.getuid(),dependencies=dependencies,**streams(out,err))
  print(json.dumps(result,sort_keys=True));return 1
 need(err.getvalue()=='' and out.getvalue(),'checker output missing or stderr present')
 result=strict_json(out.getvalue())
 print(json.dumps(dict(status='PASS',program=program,mutation=mutation,actual_source_sha256=hashlib.sha256(source.encode()).hexdigest(),uid=os.getuid(),dependencies=dependencies,result=result,**streams(out,err)),sort_keys=True));return 0
if __name__=='__main__':
 try:sys.exit(main())
 except (ValueError,OSError,TypeError,KeyError) as error:
  print('REJECT: finite adapter failed: '+str(error),file=sys.stderr);sys.exit(2)
