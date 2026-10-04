#!/usr/bin/env python3
"""Exact finite controls. These do not prove the infinite construction."""
import json
from fractions import Fraction as F

ZERO=(F(0),F(0))
ONE=(F(1),F(0))
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def sub(x,y): return add(x,neg(y))
def mul(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def conj(x): return (x[0],-x[1])
def norm2(x): return x[0]*x[0]+x[1]*x[1]
def div(x,y):
    n=norm2(y)
    assert n != 0
    z=mul(x,conj(y))
    return (z[0]/n,z[1]/n)
def phi(a,u): return div(sub(u,a),sub(ONE,mul(conj(a),u)))
def psi(a,v): return div(add(v,a),add(ONE,mul(conj(a),v)))

def run():
    grid=[(F(x,5),F(y,5)) for x in range(-4,5) for y in range(-4,5)
          if F(x*x+y*y,25)<1]
    inverse=defect=difference=0
    for a in grid:
        assert phi(a,a)==ZERO
        assert phi(a,ZERO)==neg(a)
        for u in grid:
            v=phi(a,u)
            assert norm2(v)<1
            assert psi(a,v)==u
            assert phi(a,psi(a,u))==u
            inverse+=1
            den=sub(ONE,mul(conj(a),u))
            assert 1-norm2(v)==(1-norm2(a))*(1-norm2(u))/norm2(den)
            defect+=1
            # Difference identity used to check local transport near any alpha.
            lhs=sub(phi(a,u),phi(a,ZERO))
            rhs=div(mul((1-norm2(a),F(0)),u),den)
            assert lhs==rhs
            difference+=1
    # A realistic wrong convention must fail: omit conjugation in both maps.
    a=(F(1,3),F(1,4));u=(F(2,5),F(1,5))
    bad=div(sub(u,a),sub(ONE,mul(a,u)))
    assert psi(a,bad)!=u
    assert 1-norm2(bad)!=(1-norm2(a))*(1-norm2(u))/norm2(sub(ONE,mul(conj(a),u)))
    # An omitted value at -alpha does not defeat all neighborhoods of zero.
    a=(F(2,5),F(0)); delta=F(1,5)
    assert norm2(phi(a,ZERO))>delta*delta
    # Quantifier negative control: shrinking radii allow every finite threshold
    # without a common radius. This is only a scalar logical model.
    for n in range(1,101):
        assert F(1,n)>0
        for m in range(n+1,n+11):
            assert F(1,m)<F(1,n)
    return {
      'result':'pass',
      'arithmetic':'exact fractions, including nonreal parameters',
      'disk_grid_points':len(grid),
      'inverse_pair_checks':inverse,
      'disk_defect_identity_checks':defect,
      'difference_identity_checks':difference,
      'negative_controls':[
        'missing complex conjugation rejected',
        'one fixed nonzero omitted value is insufficient',
        'finite-threshold radius does not supply a common radius'
      ],
      'limitations':[
        'No numerical or formal construction of the infinite Riemann surface.',
        'No proof of Stephenson construction theorem, canonical factorization, or Rouche theorem by this code.',
        'Finite samples check implementation identities; general identities are proved algebraically in PROOF.md.',
        'The almost-everywhere shift lemma and quantifier conclusion are analytic proofs, not consequences of these samples.'
      ]
    }

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
