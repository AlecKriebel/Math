#!/usr/bin/env python3
"""Exact finite checks for the accompanying partial mathematical note.

Only Python's standard library is used. These checks verify finite instances and
algebraic specializations; they do not prove the conjecture or literature status.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb, factorial
from pathlib import Path
import json


def solve3(rows, rhs):
    a = [[F(x) for x in row] + [F(y)] for row,y in zip(rows,rhs)]
    for j in range(3):
        k = next((k for k in range(j,3) if a[k][j]), None)
        if k is None: return None
        a[j],a[k]=a[k],a[j]
        d=a[j][j]; a[j]=[x/d for x in a[j]]
        for k in range(3):
            if k!=j:
                d=a[k][j]; a[k]=[x-d*y for x,y in zip(a[k],a[j])]
    return tuple(a[j][3] for j in range(3))


def cube_certificate(n):
    d=sum((-1)**j*comb(n,j)*(n-2*j)**(n-1) for j in range(n//2+1))
    gamma=2*comb(n-1,(n-1)//2)
    # Independent elementary binomial identity behind the cosine polynomial.
    assert sum(comb(n,j)*abs(n-2*j) for j in range(n+1)) == n*gamma
    w=F(2**n*factorial(n-1),d)-F(gamma*n,2**(n-1))
    return d,gamma,w


def verify_arrangement_3d():
    # Hyperplanes on which one of the absolute-value expressions changes sign.
    diag=[(1,a,b) for a,b in product((-1,1),repeat=2)]
    axes=[tuple(int(i==j) for i in range(3)) for j in range(3)]
    planes=[(q,0) for q in diag+axes]
    planes += [(q,b) for q in axes for b in (-1,1)]
    vertices=set()
    for triple in combinations(planes,3):
        x=solve3([p[0] for p in triple],[p[1] for p in triple])
        if x is not None and all(abs(t)<=1 for t in x): vertices.add(x)
    # Every piece is a bounded polytope, whose vertices occur in this arrangement.
    values=[2*sum(abs(sum(qi*xi for qi,xi in zip(q,x))) for q in diag)
            -4*sum(abs(xi) for xi in x) for x in vertices]
    assert values and min(values)==0 and all(y>=0 for y in values)
    return len(vertices),str(min(values)),str(max(values))


def verify_flat_jets():
    # Taylor coefficients of 1/H at t=1, then of t^2/H, through order two.
    count=0
    for b in [F(1,2),F(1),F(3,2),F(2)]:
        for h in [F(1,3),F(1),F(7,4),F(5)]:
            hp=b**3; hpp=-3*b**3
            inv0=1/h
            inv1=-hp/h**2
            inv2=hp**2/h**3-hpp/(2*h**2)
            g=inv1+2*inv0
            gp=2*(inv2+2*inv1+inv0)
            assert gp-g==2*b**6/h**3
            pole_Lg=3*(g-gp)
            assert pole_Lg == -6*b**6/h**3 < 0
            # Generating density is this number times 3/(32*pi^2).
            count+=1
    return count


def verify_cylinder_integrals():
    # At t=1/sqrt(2): t/sqrt(1-t^2)=1.
    # For the upper h primitive -1/(4t^4)+1/(2t^2), t^-2=2 or 1.
    h_lower=F(1)
    h_upper=(-F(1,4)+F(1,2))-(-F(4,4)+F(2,2))
    # Lower k integral uses z=t/sqrt(1-t^2), yielding int_0^1 z^2 dz.
    k_lower=F(1,3)
    k_upper=-F(1,2)+F(2,2)
    h=h_lower+h_upper; k=k_lower+k_upper
    assert h==F(5,4) and k==F(5,6)
    gap=h-2*k*k
    assert gap==F(-5,36)
    return {'h':str(h),'k':str(k),'hr_minus_2k2':str(gap)}


def main():
    dims={n:cube_certificate(n) for n in range(3,65)}
    assert dims[3][2]==F(-1,3) and dims[4][2]==0
    assert all(dims[n][2]<0 for n in range(5,65))
    vertices,minimum,maximum=verify_arrangement_3d()
    out={
      'status':'passed',
      'arithmetic':'exact rational and integer; no floating-point tests',
      'cube_witness_3d':str(dims[3][2]),
      'cube_witness_4d':str(dims[4][2]),
      'strict_cube_dimensions':[3]+list(range(5,65)),
      'cube_sample_values':{str(n):str(dims[n][2]) for n in range(3,13)},
      'piecewise_linear_3d_check':{'vertices':vertices,'minimum':minimum,'maximum':maximum},
      'flat_top_exact_jet_instances':verify_flat_jets(),
      'cylinder_6d_moments':verify_cylinder_integrals(),
      'limits':'Finite checks do not establish unrestricted density, all-dimensional cube signs, or novelty.'
    }
    path=Path(__file__).with_name('exact_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
