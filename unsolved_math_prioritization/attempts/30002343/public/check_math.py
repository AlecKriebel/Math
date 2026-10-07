#!/usr/bin/env python3
"""Finite regression checks, not a proof of geometric theorems. Python 3 stdlib only."""
from fractions import Fraction
from math import ceil
import hashlib
import json
from pathlib import Path
import sys


def weighted_monomials(m, weights=(1,1,2,5)):
    out=[]
    def rec(i,left,exps):
        if i==len(weights):
            if left==0: out.append(tuple(exps))
            return
        for k in range(left//weights[i]+1): rec(i+1,left-k*weights[i],exps+[k])
    rec(0,m,[])
    return out


def numerical_failures(I, max_degree=200, coefficient=5):
    out=[]
    for d in range(1,max_degree+1):
        gmax=(Fraction(3*I+1,I)*d+2)//2
        for g in range(int(gmax)+1):
            if coefficient*d<2*g+1: out.append((d,g))
    return out


def run():
    counts=[len(weighted_monomials(m)) for m in range(1,6)]
    assert counts==[2,4,6,9,13],counts
    assert all(e[3]==0 for m in range(1,5) for e in weighted_monomials(m))
    assert (0,0,0,1) in weighted_monomials(5)
    # Explicit two-sheet sample x=1,y=z=0,w=+/-1.
    def ev(exps,w):
        x,y,z,t=exps
        return (0 if y or z else w**t)
    assert all(ev(e,1)==ev(e,-1) for e in weighted_monomials(4))
    assert any(ev(e,1)!=ev(e,-1) for e in weighted_monomials(5))
    assert numerical_failures(1)==[(1,3),(2,5)]
    for I in range(2,101): assert numerical_failures(I)==[],I
    cyclic=[]
    for n in range(2,31):
        for d in range(1,101):
            a=(n-1)*d-3
            if a>0:
                m=ceil(Fraction(d,a)); assert 1<=m<=4
                assert m*a>=d and (m-1)*a<d
                cyclic.append((n,d,a,m))
    assert max(t[3] for t in cyclic)==4
    assert (2,4,1,4) in cyclic
    # Tangent direction (1,-1,0) annihilates z and x+y but not x,y.
    tangent=(1,-1,0)
    assert tangent[2]==0 and tangent[0]+tangent[1]==0
    assert any(tangent[:2])
    controls={}
    # Negative controls catch tempting changes in bounds and weights.
    controls['false_extension_to_index_one']=bool(numerical_failures(1))
    controls['replace_five_by_four']=bool(numerical_failures(2,coefficient=4))
    controls['move_deck_generator_to_degree_four']=any(e[3] for e in weighted_monomials(4,(1,1,2,4)))
    controls['replace_cyclic_maximum_by_three']=any(t[3]>3 for t in cyclic)
    assert all(controls.values())
    return {'status':'PASS','weighted_dimensions_1_through_5':counts,
            'index_one_numerical_exceptions':numerical_failures(1),
            'index_at_least_two_checked':{'I':[2,100],'degree':[1,200],'failures':0},
            'cyclic_cases':len(cyclic),'cyclic_maximum_embedding_threshold':4,
            'negative_controls_detected':controls,
            'scope':'Finite arithmetic, monomial, and tangent checks only. Geometry is proved in PROOF.md using the declared dependencies.'}


def verify_manifest():
    root=Path(__file__).resolve().parent
    M=json.loads((root/'FROZEN_MANIFEST.json').read_text())
    listed=set()
    for x in M['files']:
        p=root/x['path']; b=p.read_bytes()
        assert len(b)==x['bytes'],str(p)
        assert hashlib.sha256(b).hexdigest()==x['sha256'],str(p)
        listed.add(x['path'])
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
            and p.name!='FROZEN_MANIFEST.json' and '__pycache__' not in p.parts}
    assert actual==listed,{'extra':sorted(actual-listed),'missing':sorted(listed-actual)}
    return {'status':'PASS','verified_files':len(listed)}

if __name__=='__main__':
    result=verify_manifest() if '--verify-manifest' in sys.argv else run()
    print(json.dumps(result,indent=2,sort_keys=True))
