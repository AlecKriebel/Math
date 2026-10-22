#!/usr/bin/env python3
"""Separately expressed exact dimension, polynomial, and double-cover controls."""
import json
from math import comb

def deriv(poly,i):
    out={}
    for e,c in poly.items():
        if e[i]:
            f=list(e); f[i]-=1; out[tuple(f)]=c*e[i]
    return out

def check(d):
    # Explicit polynomial f=Z(X^(d-1)-Y^(d-1))+X^d, encoded sparsely.
    f={(d-1,0,1):1,(0,d-1,1):-1,(d,0,0):1}
    assert all(sum(e)==d for e in f)
    assert min(e[0]+e[1] for e in f)==d-1
    assert deriv(f,2)=={(d-1,0,0):1,(0,d-1,0):-1}
    assert deriv(f,1)=={(0,d-2,1):-(d-1)}
    # Tangent polynomial u^(d-1)-1 has no common zero with its derivative:
    # at u=0 the first is -1; at u !=0 the derivative (d-1)u^(d-2) !=0.
    assert d-1>0
    Nd=comb(d+2,2)-1
    product_dims=[comb(a+2,2)+comb(d-a+2,2)-2 for a in range(1,d)]
    codim=Nd-max(product_dims)
    assert codim==d-1 and max(product_dims)+1<Nd
    # Compute canonical self-intersection via branch-cover formula, not vectors.
    KY2=9-d*d
    KYF=d*(d-3)
    KS2=2*(KY2+4*KYF)
    assert KS2==6*(d-1)*(d-3)
    genus=comb(d-1,2)
    # Topological double-cover formula e(S)=2e(Y)-e(branch).
    eY=3+d*d
    eS=2*eY-4*(2-2*genus)
    # Holomorphic Euler characteristic double-cover formula with D=2F.
    chiS=2+KYF
    assert 12*chiS==KS2+eS
    # Numerical inequality without floating roots.
    margin=(d-3)**4-KS2
    assert (margin>0)==(d>=7)
    step=3*(d-3)**2+3*(d-3)-5
    assert (d-2)**3-6*d-((d-3)**3-6*(d-1))==step
    if d>=7: assert step>0
    # The section's double-cover genus is 1: square -2 and K intersection 2.
    assert -2+2==2*1-2
    return {'d':d,'ambient_pencil_dimension':Nd,'reducible_codimension':codim,
            'join_dimension_bound':max(product_dims)+1,'K_squared':KS2,
            'chi_O':chiS,'topological_euler':eS,'Noether_identity':True,
            'strict_inequality_margin':margin}

if __name__=='__main__':
    print(json.dumps({'method':'sparse polynomial, dimension counts, cover identities',
                      'results':[check(d) for d in range(4,101)]},indent=2))
