#!/usr/bin/env python3
"""Exact isolated finite interfaces; full mathematical arguments are in the prose."""
import json,math,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
CORRECTED=['missing_parameter_shift','wrong_involution_scalar']
INDEPENDENT=['quotient_action','derivation_weight','parameter_shift','conjugator_translation','projective_scalar','fixed_ring']
REASONS=['induced Q-action','coboundary of y','projective conjugacy','projective conjugacy','projective conjugacy','j fixed-ring linear coefficient']
CHECKS=['all 16 group-composition identities','quotient invariance, induced action, derivative','exact rational invariant and coboundary identities for z^0 through z^8','conjugacy and involution in F4[e]/e^3','all 64 elements: j-fixed iff linear coefficient is zero']
def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def unique(pairs):
 result={}
 for k,v in pairs:need(k not in result,'duplicate JSON key');result[k]=v
 return result
def nonfinite(token):raise ValueError('nonfinite JSON')
def number(token):
 x=float(token);need(math.isfinite(x),'nonfinite float');return x
def parse(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=nonfinite,parse_float=number)
def main():
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required')
 need(len(sys.argv)==1,'no optional or skip arguments')
 contract=parse((HERE/'FINITE_CONTRACT.json').read_bytes())
 need(type(contract) is dict and set(contract)=={'schema','problem_id','modes','role'} and type(contract['schema']) is int and contract['schema']==1 and type(contract['problem_id']) is int and contract['problem_id']==30001113,'contract schema')
 need(type(contract['modes']) is dict and set(contract['modes'])=={'0','1','2'},'all exact optimization modes')
 expected=contract['modes'][str(sys.flags.optimize)];identities=[(s,m) for s,ms in [('check_conjugacy.py',CORRECTED),('verify_exact.py',INDEPENDENT)] for m in [None]+ms]
 need(type(expected) is list and len(expected)==10,'nonempty exact suite cardinality')
 need([(r['program'],r['mutation']) for r in expected]==identities,'all intended case identities and order')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];rows=[]
 for row in expected:
  need(type(row) is dict and set(row)=={'program','mutation','expected_exit','stdout','stderr'},'case schema')
  script,mutation=row['program'],row['mutation'];code=1 if mutation else 0
  need(type(row['expected_exit']) is int and row['expected_exit']==code,'case exit schema')
  need(type(row['stdout']) is str and type(row['stderr']) is str and row['stdout'] and row['stderr']=='','raw expected outputs')
  refout=row['stdout'].encode();referr=row['stderr'].encode()
  args=['check_corrected_case.py',mutation or 'none'] if script=='check_conjugacy.py' else ['current/verify_exact.py','--mutant',mutation or 'none']
  p=subprocess.run([sys.executable,'-I','-S','-B',*mode,*args],cwd=HERE,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=60)
  need(type(p.returncode) is int and p.returncode==code,'intended exit '+script+' '+str(mutation))
  need(p.stdout==refout and p.stderr==referr,'complete raw output or intended rejection reason differs '+script+' '+str(mutation))
  parsed=parse(p.stdout);need(same(parsed,parse(refout)),'recursive exact types')
  if mutation:
   wanted=REASONS[INDEPENDENT.index(mutation)] if script=='verify_exact.py' else ('Projective conjugacy identity failed' if mutation=='missing_parameter_shift' else 'Involution identity failed')
   obj=dict(ok=False,mutant=mutation,failure=wanted)
   if script=='verify_exact.py':obj['optimization_level']=sys.flags.optimize
   need(same(parsed,obj),'intended exact rejection identity and reason');reason=wanted
  else:
   reason='positive finite interfaces accepted'
   if script=='check_conjugacy.py':
    need(same(parsed,{'ring':'F_2[e]/(e^3)','encoding':'bit i is the coefficient of e^i','conjugacy_identity':'M_(e+e^2) C = (1+e) C M_e','conjugacy_verified':True,'involution_verified':True,'both_conjugacy_sides':[[3,4],[3,3]]}),'corrected exact identities')
   else:need(same(parsed,dict(ok=True,optimization_level=sys.flags.optimize,mutant='none',checks=CHECKS,limitation='Finite identities support but do not prove the formal power-series or functor arguments.')),'independent exact identities')
  rows.append(dict(script='current/'+script,mutation=mutation,exit_code=p.returncode,expected_exit=code,rejected=mutation is not None,reason=reason,stdout=p.stdout.decode(),stderr=p.stderr.decode(),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='NONE'))
 need(len(rows)==10 and sum(r['rejected'] is False for r in rows)==2 and sum(r['rejected'] is True for r in rows)==8,'exact totals')
 print(json.dumps(dict(status='passed',problem_id=30001113,uid=os.getuid(),euid=os.geteuid(),python_optimize=sys.flags.optimize,positive_checker_runs=2,expected_mutant_rejections=8,cases=rows,mathematics='NOT_FORMALLY_VERIFIED: finite identities only; full formal-series, cohomology and naturality arguments are in both written proofs.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as e:
  print('REJECT: finite-interface replay failed: '+str(e),file=sys.stderr);sys.exit(1)
