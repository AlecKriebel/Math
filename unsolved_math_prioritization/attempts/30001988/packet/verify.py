#!/usr/bin/env python3
"""Exact finite controls for the authored partial result; not a theorem prover."""
import itertools
import json
from pathlib import Path

def add(p, q):
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, 0) + c
        if not out[m]:
            del out[m]
    return out

def mul(p, q):
    out = {}
    for m, c in p.items():
        for n, d in q.items():
            k = tuple(x+y for x,y in zip(m,n))
            out[k] = out.get(k, 0) + c*d
    return {m:c for m,c in out.items() if c}

def neg(p):
    return {m:-c for m,c in p.items()}

def deriv(p):
    out = {}
    # delta z_0=z_1 and delta z_1=z_2. Inputs use only z_0,z_1.
    for m,c in p.items():
        assert m[2] == 0
        for i in (0,1):
            if m[i]:
                n=list(m); n[i]-=1; n[i+1]+=1; n=tuple(n)
                out[n]=out.get(n,0)+c*m[i]
    return {m:c for m,c in out.items() if c}

def main():
    one={(0,0,0):1}; z0={(1,0,0):1}; z1={(0,1,0):1}; z2={(0,0,1):1}
    assert deriv(one)=={}
    assert deriv(z0)==z1
    assert deriv(z1)==z2
    assert add(mul(deriv(one),z0), neg(mul(one,deriv(z0))))==neg(z1)
    mons=[(0,0,0),(1,0,0),(0,1,0)]
    polys=[{m:c for m,c in zip(mons,cs) if c} for cs in itertools.product((-1,0,1), repeat=3)]
    checks=0
    for n in polys:
        for d in polys:
            if not d: continue
            numerator=add(mul(deriv(n),d),neg(mul(n,deriv(d))))
            for a in (-1,1):
                target=mul({(1,0,0):a},mul(d,d))
                assert numerator!=target
                checks+=1
    assert checks==1404
    root=Path(__file__).resolve().parent
    status=json.loads((root/'STATUS.json').read_text())
    assert status['status']=='unsolved'
    assert status['substantive_approaches']==5
    assert not status['full_target_claimed']
    assert not status['novelty_claimed']
    turns=[json.loads(x) for x in (root/'turns.jsonl').read_text().splitlines()]
    assert [x['turn'] for x in turns]==[1,2,3,4,5]
    assert len({x['mechanism'] for x in turns})==5
    assert all(x['remaining_gap'] for x in turns)
    result={
        'passed':True,
        'rational_derivative_nonprimitive_cases':checks,
        'tested_base':'Q with zero derivation',
        'tested_rational_functions':'N/D; N,D linear in z_0,z_1 with coefficients -1,0,1; D nonzero',
        'tested_rhs':['z_0','-z_0'],
        'identity_controls':4,
        'scope_guards':'unsolved; 5 distinct approaches; no full-target or novelty claim',
        'limitation':'Finite exact controls only. The general partial lemma is proved in PROOF.md. No full-target decision algorithm is tested.'
    }
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
