#!/usr/bin/env python3
"""Exact pre-candidate controls. Finite checks are falsifiers, never universal evidence."""
from collections import deque
from fractions import Fraction
import json

def word_dist(elements, mul, inv, seeds):
    closure={mul(mul(h,s),inv(h)) for h in elements for s in seeds+tuple(inv(s) for s in seeds)}
    d={elements[0]:0}; queue=deque(d)
    while queue:
        x=queue.popleft()
        for s in closure:
            y=mul(x,s)
            if y not in d: d[y]=d[x]+1;queue.append(y)
    return d

def dihedral(q):
    E=[(a,b) for b in range(2) for a in range(q)]
    mul=lambda x,y:((x[0]+(-1)**x[1]*y[0])%q,(x[1]+y[1])%2)
    inv=lambda x:((-(-1)**x[1]*x[0])%q,x[1])
    d=word_dist(E,mul,inv,((1,0),(0,1)))
    assert all(d[(n,0)]<=3 for n in range(q))
    return {'q':q,'max_rotation_norm':max(d[(n,0)] for n in range(q))}

def heisenberg(q):
    E=[(a,b,c) for a in range(q) for b in range(q) for c in range(q)]
    mul=lambda x,y:((x[0]+y[0])%q,(x[1]+y[1])%q,(x[2]+y[2]+x[0]*y[1])%q)
    inv=lambda x:(-x[0]%q,-x[1]%q,(-x[2]+x[0]*x[1])%q)
    d=word_dist(E,mul,inv,((1,0,0),(0,1,0)))
    assert all(d[(0,0,n)]<=2 for n in range(q))
    return {'q':q,'max_central_norm':max(d[(0,0,n)] for n in range(q))}

def bs_witness(m,n):
    # Exact infinite affine group over Z[1/m] x Z. t a t^-1 = a^m.
    mul=lambda x,y:(x[0]+Fraction(m)**x[1]*y[0],x[1]+y[1])
    inv=lambda x:(-x[0]*Fraction(m)**(-x[1]),-x[1])
    a=(Fraction(n),0);t=(Fraction(0),1)
    comm=mul(mul(mul(t,a),inv(t)),inv(a))
    assert comm==(Fraction((m-1)*n),0)
    return comm[0].numerator

def cyclic_wrap(q,n):
    # Infinite Z standard norm |n| versus exact quotient C_q norm.
    return {'q':q,'n':n,'infinite_norm':abs(n),'finite_norm':min(n%q,(-n)%q)}

out={'classification':'finite checks do not prove a universal norm estimate',
     'dihedral':[dihedral(q) for q in range(3,20)],
     'heisenberg':[heisenberg(q) for q in (2,3,5,7)],
     'bs_infinite_exact_witnesses':sum(1 for m in range(2,12) for n in range(-100,101) if bs_witness(m,n)==(m-1)*n),
     'cyclic_wrap_adversaries':[cyclic_wrap(q,n) for q in (7,11,101) for n in (q-1,q,q+1,2*q)]}
print(json.dumps(out,indent=2,sort_keys=True))
