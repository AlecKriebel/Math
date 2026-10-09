#!/usr/bin/env python3
"""Exact isolated finite-interface replay. Geometry is proved in both audits."""
import hashlib,json,math,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ORIGINAL=['bad_group','bad_relation','missing_section','bad_branch','bad_characteristic']
INDEPENDENT=['rank_two_group','dependent_kummer_classes','diagonal_quotient','opposite_F_generators','duality_sign_error','missing_canonical_section','extra_canonical_section','wrong_divisor_coefficients','omitted_singular_stratum','printed_quadric_relation','smooth_quadric_claim','construction_degree_confusion']
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
 need(type(contract) is dict and set(contract)=={'schema','problem_id','expected_records','role'} and type(contract['schema']) is int and contract['schema']==1 and type(contract['problem_id']) is int and contract['problem_id']==30000977,'contract schema')
 expected=contract['expected_records'];identities=[(s,m) for s,ms in [('verify_counterexample.py',ORIGINAL),('independent_exact_checks.py',INDEPENDENT)] for m in [None]+ms]
 need(type(expected) is list and len(expected)==19,'nonempty exact suite cardinality')
 need([(r['program'],r['mutation']) for r in expected]==identities,'all intended case identities and order')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];rows=[]
 for row in expected:
  need(type(row) is dict and set(row)=={'program','mutation','expected_exit','stdout','stderr'},'case schema')
  script,mutation=row['program'],row['mutation'];code=2 if mutation else 0
  need(type(row['expected_exit']) is int and row['expected_exit']==code,'case exit schema')
  need(type(row['stdout']) is str and type(row['stderr']) is str and row['stdout'] and row['stderr']=='','raw expected outputs')
  refout=row['stdout'].encode();referr=row['stderr'].encode()
  p=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(HERE/'current'/script),*(['--mutate',mutation] if mutation else [])],cwd=HERE,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=60)
  need(type(p.returncode) is int and p.returncode==code,'intended exit '+script+' '+str(mutation))
  need(p.stdout==refout and p.stderr==referr,'complete raw output or intended rejection reason differs '+script+' '+str(mutation))
  structured=mutation is None or script=='independent_exact_checks.py'
  if structured:need(same(parse(p.stdout),parse(refout)),'recursive exact types')
  parsed=parse(p.stdout) if structured else None
  if mutation:
   if structured:
    need(set(parsed)=={'status','mutation','reason','uid','euid'} and parsed['status']=='REJECTED' and parsed['mutation']==mutation and type(parsed['uid']) is int and type(parsed['euid']) is int and parsed['uid']==parsed['euid']==1000,'intended structured rejection')
    reason=parsed['reason']
   else:
    need(p.stdout.startswith(b'GUARD_FAILURE: ') and p.stdout.endswith(b'\n'),'intended guard rejection');reason=p.stdout.decode()[15:-1]
  else:
   reason='positive finite interfaces accepted'
   want={'A2_points':9,'K_squared':24,'canonical_degree':12,'cover_degree':27,'p_g':4}
   need(all(type(parsed[k]) is int and parsed[k]==v for k,v in want.items()),'positive exact invariant counts')
   if script=='verify_counterexample.py':
    need(parsed['status']=='PASS_FINITE_CHECKS_ONLY' and parsed['character_rows']==27 and parsed['branch_strata_checked']==25 and parsed['curve_genus']==10,'original counts')
   else:
    need(parsed['status']=='PASS_FINITE_INTERFACES_ONLY' and parsed['uid']==parsed['euid']==1000,'independent identity')
    need([parsed[k] for k in ['character_pairs_checked','character_group_evaluations','local_invariant_monomials_checked','quadric_rank','genus_E','genus_F']]==[729,19683,625,3,10,10],'independent counts')
    need([len(parsed[k]) for k in ['character_table','crossings','branch_strata','divisors','complete_basis_duality_labels']]==[27,16,25,4,4],'complete identities')
    need(parsed['complete_basis_duality_labels']==[[0,1,0],[1,0,1],[0,2,0],[2,2,2]],'canonical basis')
  rows.append(dict(script='current/'+script,mutation=mutation,exit_code=p.returncode,expected_exit=code,rejected=mutation is not None,reason=reason,stdout=p.stdout.decode(),stderr=p.stderr.decode(),complete_output_comparison=True,recursive_exact_type_comparison=structured,normalization='NONE'))
 need(len(rows)==19 and sum(r['rejected'] is False for r in rows)==2 and sum(r['rejected'] is True for r in rows)==17,'exact totals')
 print(json.dumps(dict(status='passed',problem_id=30000977,uid=os.getuid(),euid=os.geteuid(),python_optimize=sys.flags.optimize,positive_checker_runs=2,expected_mutant_rejections=17,cases=rows,geometry='NOT_FORMALLY_VERIFIED: see both complete geometric audits; finite algebra only.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as e:
  print('REJECT: finite-interface replay failed: '+str(e),file=sys.stderr);sys.exit(1)
