#!/usr/bin/env python3
"""Strict metadata and finite regressions only; not a topology proof checker."""
import argparse
from fractions import Fraction as Q
import itertools
import json
from pathlib import Path
import sys

EXPECTED={'schema':'short-geodesics-scoped-claims-v1','problem_id':10300043,'catalog_id':'AMR-102-0043','rank':1008,'status':'unsolved','turns_used':5,'turns_budget':5,'universal_isotopy_solution':False,'universal_homotopy_solution':False,'geodesic_counterexample':False,'novelty_claim':False,'formal_verification':False,'independent_review':'pending','claim_ids':['leaf_space_gap_reduction','integral_period_bound','meridian_calibration','disk_filling_transverse_core','nongeodesic_trefoil_countercheck']}
def need(ok,msg):
    if not ok: raise ValueError(msg)
def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def no_constant(c):raise ValueError('nonfinite JSON constant')
def load(p):
    p=Path(p);need(p.is_file() and not p.is_symlink(),'nonregular input');b=p.read_bytes();need(len(b)<=2_000_000,'oversized JSON')
    return json.loads(b.decode('utf-8'),object_pairs_hook=pairs,parse_constant=no_constant)
def validate(x):
    need(type(x) is dict and set(x)==set(EXPECTED),'claim key set')
    for k,v in EXPECTED.items():need(type(x[k]) is type(v) and x[k]==v,'claim mismatch: '+k)
def diagnostics():
    counts={'period_controls':0,'hyperbolic_identity_controls':0,'meridian_inequality_controls':0,'trefoil_group_controls':0,'shear_controls':0}
    # Exact rational controls for the integer-period implication. Each triple
    # is a numerical premise/conclusion, not an encoded foliation or loop.
    for a in [Q(i,j) for i in range(1,9) for j in range(1,6)]:
        for length in [Q(i,j) for i in range(1,9) for j in range(1,7)]:
            for n in range(-4,5):
                if abs(n)<=a*length and a*length<1:
                    need(n==0,'integer period');counts['period_controls']+=1
    for t in [Q(i,j) for j in range(1,8) for i in range(j+1,j+12)]:
        c=(t+1/t)/2;s=(t-1/t)/2
        need(c*c-s*s==1 and c>1 and s>0,'hyperbolic rational parametrization');counts['hyperbolic_identity_controls']+=1
        for k in range(-7,8):
            if k==0:continue
            for b in [Q(i,3) for i in range(0,25)]:
                need((abs(k)*(c-1)<=b)==(c<=1+b/abs(k)),'conditional radius algebra');counts['meridian_inequality_controls']+=1
    identity=(0,1,2);a=(1,0,2);b=(0,2,1)
    def comp(p,q):return tuple(p[q[i]] for i in range(3))
    need(comp(comp(a,b),a)==comp(comp(b,a),b),'trefoil relation');counts['trefoil_group_controls']+=1
    need(comp(a,b)!=comp(b,a),'nonabelian quotient');counts['trefoil_group_controls']+=1
    generated={identity};todo=[identity]
    while todo:
        p=todo.pop()
        for q in [a,b]:
            r=comp(p,q)
            if r not in generated:generated.add(r);todo.append(r)
    need(generated==set(itertools.permutations(range(3))),'S3 generation');counts['trefoil_group_controls']+=1
    for derivative in [Q(i,20) for i in range(-19,20)]:
        need(1+derivative/2>0,'positive shear Jacobian');counts['shear_controls']+=1
    return counts

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=Path);args=ap.parse_args();root=Path(__file__).resolve().parent
    validate(load(args.input or root/'CLAIMS.json'))
    l=load(root/'APPROACH_LEDGER.json')
    need(l['schema']=='short-geodesics-ledger-v1' and type(l['problem_id']) is int and l['problem_id']==10300043,'ledger identity')
    need(type(l['total_substantive_turns']) is int and l['total_substantive_turns']==5 and l['turns_limit']==5,'ledger count')
    need([i['turn'] for i in l['approaches']]==list(range(1,6)),'ledger sequence')
    need(len({i['method'] for i in l['approaches']})==5 and all(i['counted'] is True and i['status']=='scoped_partial' for i in l['approaches']),'ledger scope')
    print(json.dumps({'status':'PASS_SCOPED_REGRESSIONS','problem_id':10300043,'general_solution':False,'topological_proof_machine_verified':False,**diagnostics()},sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,TypeError,KeyError,UnicodeError,OSError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(2)
