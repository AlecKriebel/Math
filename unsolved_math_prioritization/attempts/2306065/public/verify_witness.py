#!/usr/bin/env python3
"""Exact rational certificate, standard library only; no floating-point tests."""
from fractions import Fraction as F
from math import comb
import json
from pathlib import Path


def add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    return c


def chebyshev(n):
    ts=[[F(1)],[F(0),F(1)]]
    for k in range(2,n+1): ts.append(add([F(0)]+[2*x for x in ts[-1]],[-x for x in ts[-2]]))
    return ts[:n+1]


def bernstein_on_unit(power):
    # First substitute x=2*t-1; then power-to-Bernstein conversion.
    n=len(power)-1
    shifted=[sum(power[k]*comb(k,j)*2**j*(-1)**(k-j) for k in range(j,n+1)) for j in range(n+1)]
    return [sum(shifted[j]*F(comb(k,j),comb(n,j)) for j in range(k+1)) for k in range(n+1)]


def split(bs):
    row=bs[:];left=[row[0]];right=[row[-1]]
    while len(row)>1:
        row=[(a+b)/2 for a,b in zip(row,row[1:])]
        left.append(row[0]);right.append(row[-1])
    return left,list(reversed(right))


def positive_certificate(poly,max_depth=20):
    stack=[(bernstein_on_unit(poly),0)]; leaves=0; depth=0; lower=None
    while stack:
        bs,d=stack.pop(); m=min(bs)
        if m>0:
            leaves+=1;depth=max(depth,d);lower=m if lower is None else min(lower,m)
        elif d>=max_depth:
            raise AssertionError('unresolved Bernstein cell at maximum depth')
        else:
            left,right=split(bs); stack.extend([(left,d+1),(right,d+1)])
    return {'positive':True,'dyadic_leaves':leaves,'max_depth':depth,'certified_lower_bound':str(lower)}


def verify():
    w=json.loads((Path(__file__).parent/'WITNESS.json').read_text())
    c=[F(n,w['coefficient_denominator']) for n in w['coefficient_numerators']]
    L=F(w['L_numerator'],w['L_denominator']); ts=chebyshev(len(c)); p=[F(1)];q=[L]
    for n,v in enumerate(c,1):
        p=add(p,[n*v*x for x in ts[n]]);q=add(q,[-v*x for x in ts[n]])
    # Boundary Re(1+zg')=p(cos(theta))>0 and L-Re g=q(cos(theta))>0.
    a3=c[1]+c[0]**2/2
    assert a3>F(9,10)>F(8,9)
    # e^L: Taylor through k=30 plus a geometric bound on its positive tail.
    term=F(1);s=term
    for k in range(1,31): term*=L/k;s+=term
    first_omitted=term*L/31
    upper=s+first_omitted/(1-L/32)
    assert 0<L<32 and upper<3
    results={'degree':len(c),'all_arithmetic':'exact Python Fraction','a3':str(a3),'a3_greater_than_9_over_10':True,'exp_L_strictly_less_than_3':True,'p':positive_certificate(p),'q':positive_certificate(q),'limits':'Proves only feasibility of this entire starlike function and its coefficient. Does not certify sharpness or the full M-interval.'}
    return results

if __name__=='__main__': print(json.dumps(verify(),indent=2))
