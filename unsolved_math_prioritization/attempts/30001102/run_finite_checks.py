#!/usr/bin/env python3
"""Fresh isolated finite diagnostics; no implemented polynomial optimizer or proof assistant."""
import json,math,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
REASONS={'positive_only':'layer reconstruction','reverse_negative':'layer reconstruction','omit_base':'mutated ring','omit_chains':'mutated ring','reverse_implication_shift':'mutated ring','floor_instead_of_ceiling':'floor-rounded assignment infeasible','omit_bipartition_sign_change':'cover min fails','remove_subunit_layer':'subunit removal infeasible','replace_hull_with_relaxation':'LP point outside mixed hull','replace_hull_with_mixed_set':'hull point need not be mixed integral','explicit_exception_control':'explicit guard remains live'}
COUNTS=[dict(instances=24,slice_lps=5380,submodular_pairs=65014,proximity_steps=1723,layer_vectors=1000,ring_checks=1692,negative_checks=9),dict(layer_vectors=2601,signed_difference_checks=106080,instances=17,slices=531,submodular_pairs=14530,removal_checks=395,ring_instances=189,ring_subsets=1029,boundary_checks=4,unbounded_ray_checks=4,ring_extension_pairs=256,nonroot_readonly_probes=3)]
FUNCTION_MUTANTS=['positive_only','reverse_negative','omit_base','omit_chains','reverse_implication_shift']
COUNTEREXAMPLES=['floor_instead_of_ceiling','omit_bipartition_sign_change','remove_subunit_layer','replace_hull_with_relaxation','replace_hull_with_mixed_set','explicit_exception_control']
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
 need(type(contract) is dict and set(contract)=={'schema','problem_id','modes','role'} and type(contract['schema']) is int and contract['schema']==1 and type(contract['problem_id']) is int and contract['problem_id']==30001102,'contract schema')
 need(type(contract['modes']) is dict and set(contract['modes'])=={'0','1','2'},'all optimization modes')
 expected=contract['modes'][str(sys.flags.optimize)];identities=[('current/exact_checks.py',None),('current/independent_checks.py',None)]+[('check_math_case.py',m) for m in sorted(REASONS)]
 need(type(expected) is list and len(expected)==13,'exact nonempty suite size')
 need([(r['program'],r['mutation']) for r in expected]==identities,'exact identities and order')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];rows=[]
 for index,row in enumerate(expected):
  need(type(row) is dict and set(row)=={'program','mutation','expected_exit','stdout','stderr'},'case schema')
  script,mutation=row['program'],row['mutation'];code=1 if mutation else 0
  need(type(row['expected_exit']) is int and row['expected_exit']==code,'case exit schema')
  need(type(row['stdout']) is str and row['stdout'] and type(row['stderr']) is str and row['stderr']=='','raw reference fields')
  args=[script]+([mutation] if mutation else [])
  p=subprocess.run([sys.executable,'-I','-S','-B',*mode,*args],cwd=HERE,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=300)
  need(type(p.returncode) is int and p.returncode==code,'exact intended exit')
  need(p.stdout==row['stdout'].encode() and p.stderr==row['stderr'].encode(),'entire raw output differs '+script+' '+str(mutation))
  parsed=parse(p.stdout);need(same(parsed,parse(row['stdout'])),'recursive exact output types')
  if mutation:
   reason=REASONS[mutation];need(same(parsed,dict(ok=False,python_optimize=sys.flags.optimize,mutation=mutation,failure=reason)),'intended rejection identity and reason')
   category='function_mutant' if mutation in FUNCTION_MUTANTS else 'exception_guard' if mutation=='explicit_exception_control' else 'mathematical_counterexample'
  else:
   reason='positive finite diagnostics accepted';category='positive_checker'
   wanted=dict(status='PASS_FINITE_DIAGNOSTICS' if index==0 else 'PASS_INDEPENDENT_FINITE_DIAGNOSTICS',python_optimize=sys.flags.optimize,counts=COUNTS[index],limitations='Exact finite tests only. No production SFM or ellipsoid implementation; universal and bit-complexity claims rely on the written proof.' if index==0 else 'Finite exact diagnostics only. Universal validity and bit complexity are audited in the written report, not certified by these tests.')
   if index==1:wanted.update(uid=1000,killed_function_mutants=FUNCTION_MUTANTS,rejected_counterexample_controls=COUNTEREXAMPLES)
   need(same(parsed,wanted),'exact positive identities and counts')
  rows.append(dict(script=script,mutation=mutation,category=category,exit_code=p.returncode,expected_exit=code,rejected=mutation is not None,reason=reason,stdout=p.stdout.decode(),stderr=p.stderr.decode(),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='NONE'))
 need(len(rows)==13 and sum(r['rejected'] is False for r in rows)==2 and sum(r['rejected'] is True for r in rows)==11,'exact totals')
 print(json.dumps(dict(status='passed',problem_id=30001102,uid=os.getuid(),euid=os.geteuid(),python_optimize=sys.flags.optimize,positive_checker_runs=2,expected_mutant_rejections=11,rejection_categories={'function_mutants':5,'mathematical_counterexamples':5,'exception_guard':1},cases=rows,mathematics='Finite diagnostics only; imported polynomial LP/SFM/GLS algorithms and universal bit complexity are established by the full proof and audit, not implemented here. The original nine negative/guard diagnostics and independent nested eleven controls are included within positives; separate cases replay those same eleven controls and are not new mathematical coverage.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as error:
  print('REJECT: finite-interface replay failed: '+str(error),file=sys.stderr);sys.exit(1)
