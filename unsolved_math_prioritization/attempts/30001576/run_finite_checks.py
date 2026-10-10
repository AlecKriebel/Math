#!/usr/bin/env python3
"""Complete raw and recursively typed finite-checker replay; no normalization."""
import json, math, os, subprocess, sys
from pathlib import Path

def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def unique(pairs):
 out={}
 for k,v in pairs:need(k not in out,'duplicate JSON key');out[k]=v
 return out
def bad(token):raise ValueError('nonfinite JSON')
def number(token):
 v=float(token);need(math.isfinite(v),'overflow JSON');return v
def parse(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=bad,parse_float=number)
REASONS={'remove_factorials':'g=3: full cubic jet 1','wrong_heat_scale':'g=3: full cubic jet 1','wrong_cross_multiplicity':'g=5: full cubic jet 4','wrong_elimination_sign':'g=4: reduced jet 4','wrong_residual_coefficient':'g=4: reduced jet 4','wrong_fourier_lead':'Elliptic Fourier coefficient'}

def main():
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required');need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 root=Path(__file__).resolve().parent;contract=parse((root/'FINITE_CONTRACT.json').read_bytes());rows=[]
 expected=[('original',None),('independent',None)]+[('independent',m) for m in sorted(REASONS)]
 need(type(contract) is dict and set(contract)=={'schema','problem_id','cases','role'} and type(contract['schema']) is int and contract['schema']==1 and type(contract['problem_id']) is int and contract['problem_id']==30001576,'contract schema')
 need(type(contract['cases']) is list and [(c['program'],c['mutation']) for c in contract['cases']]==expected,'exact ordered case identities')
 flags=['-I','-S','-B']+([] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize]);env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C')
 for c in contract['cases']:
  program,mutation=c['program'],c['mutation'];reason=None if mutation is None else REASONS[mutation];code=0 if mutation is None else 1;category='positive_checker' if mutation is None else 'mathematical_mutation'
  need(set(c)=={'program','mutation','category','expected_exit','reason','stdout','stderr'} and type(c['stdout']) is str and type(c['stderr']) is str and same(c['expected_exit'],code) and same(c['reason'],reason) and c['category']==category,'exact case schema and reason')
  args=[sys.executable,*flags,str(root/'run_checker.py'),program]+([] if mutation is None else [mutation]);p=subprocess.run(args,cwd=root,env=env,capture_output=True,timeout=180)
  need(type(p.returncode) is int and p.returncode==code and p.stdout==c['stdout'].encode() and p.stderr==c['stderr'].encode(),'complete checker exit/stdout/stderr equality: '+str((program,mutation)))
  if mutation is None:
   parsed=parse(p.stdout);need(same(parsed,parse(c['stdout'])),'recursive typed positive output')
   if program=='original':
    need(parsed['status']=='PASS' and [x['g'] for x in parsed['formal_jet_cases']]==list(range(3,9)) and [x['retained_heat_monomials'] for x in parsed['formal_jet_cases']]==[15,40,71,108,151,200],'original exact mathematical counts')
   else:
    need(parsed['status']=='PASS' and type(parsed['uid']) is int and parsed['uid']==1000 and type(parsed['euid']) is int and parsed['euid']==1000 and parsed['full_cubic_includes_repeated_edge_factorials'] is True and parsed['jet_cases']==[dict(g=g,full_cubic_equations=g,reduced_equations=g-3,status='PASS') for g in range(3,9)] and parsed['cubic_ranks']==[dict(g=g,diagonal=3,nondegenerate_product=g) for g in range(3,9)],'independent full-cubic exact cases')
  else:need(p.stdout==b'' and p.stderr==('REJECT: intended mathematical mutation: '+reason+'\n').encode(),'intended mathematical rejection reason')
  rows.append(dict(script='run_checker.py',program=program,mutation=mutation,category=category,exit_code=p.returncode,expected_exit=code,rejected=mutation is not None,reason=reason,stdout=p.stdout.decode(),stderr=p.stderr.decode(),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='NONE'))
 need(len(rows)==8 and sum(r['rejected'] is False for r in rows)==2 and sum(r['rejected'] is True for r in rows)==6,'exact totals')
 print(json.dumps(dict(status='passed',problem_id=30001576,uid=os.getuid(),euid=os.geteuid(),python_optimize=sys.flags.optimize,positive_checker_runs=2,expected_mutant_rejections=6,rejection_categories={'mathematical_mutations':6},cases=rows,installed_adapter={'sympy':'1.14.0','mpmath':'1.3.0','site_processing':False,'cwd_imports':False},mathematics='Finite exact sanity checks only. The original factorial coverage gap is documented; the independent full-third-jet checker rejects its removal. All-genus local proofs and conditional boundary interfaces are written arguments. Global target unresolved.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as error:
  print('REJECT: finite-interface replay failed: '+str(error),file=sys.stderr);sys.exit(1)
