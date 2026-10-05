#!/usr/bin/env python3
"""Deterministic exact-rational controls, not proof of an elliptic gauge theorem."""
from fractions import Fraction as F
import json

def run():
    counts={}
    tested=[]
    n=0
    for q in range(1,9):
        for p in range(1,9):
            for j in range(1,40):
                h=F(1)+F(j,40)
                if h<=F(2*q,q+1):
                    continue
                alpha=(q+1)*h-2*q
                beta=(p+1)*h-p
                assert 0<alpha<h<beta
                assert beta-alpha==p*(h-1)+q*(2-h)
                assert 2-h*(1+F(1,q))==-alpha/q
                a=h*F(p+1,p)
                assert p*(a-1)==beta
                assert (a>2)==(h>F(2*p,p+1))
                n+=5
                tested.append([q,p,str(h),str(alpha),str(beta)])
    counts['exponent_and_moment_identities']=n
    # Exact chain-rule and interval controls for phi(x)=x/(1+x).
    n=0
    for x0 in [F(1,7),F(1,2),F(2,3),F(1),F(7,3)]:
        x=x0;d=F(1)
        for k in range(129):
            assert x==x0/(1+k*x0)
            assert d==(1+k*x0)**-2
            n+=2
            d*=1/(1+x)**2
            x=x/(1+x)
    for k in range(129):
        lo=F(1,2)/(1+F(k,2));hi=F(1)/(1+k)
        assert lo==F(1,k+2) and hi==F(1,k+1)
        assert hi-lo==F(1,(k+1)*(k+2))
        assert lo==F(1,k+2)
        n+=3
    counts['parabolic_iterates_and_intervals']=n
    n=0
    for N in range(1,129):
        assert sum(8*k for k in range(N,2*N))==12*N*N-4*N
        n+=1
    counts['square_lattice_annulus_counts']=n
    # The cocycle is an exact algebraic identity for arbitrary derivative and weights.
    # Inputs need not arise from an elliptic map; no such existence is claimed.
    n=0
    for rz in [F(1),F(1,2),F(1,5),F(2,7)]:
        for rf in [F(1),F(1,3),F(3,5)]:
            for derivative in [F(1,4),F(1),F(7,2)]:
                for h_int in [1,2,3,4]:
                    spherical=derivative*rf/rz
                    assert rf**(-h_int)*spherical**h_int == derivative**h_int*rz**(-h_int)
                    n+=1
    counts['metric_cocycle_identities']=n
    # Integral-test controls for the exact model h=3/2, p=1, hence a=3.
    n=0
    for N in [1,2,4,8,16,32]:
        M=256
        partial=sum((F(1,k**3) for k in range(N,M+1)),F(0))
        # Tail after M lies between integral_{M+1}^inf and integral_M^inf.
        lower=partial+F(1,2*(M+1)**2)
        upper=partial+F(1,2*M*M)
        assert lower<=upper
        assert upper>=F(1,2*N*N)
        assert lower<=F(1,N**3)+F(1,2*N*N)
        n+=3
    counts['exact_tail_integral_brackets']=n
    # Boundary exclusions and a concrete compatible algebraic triple.
    h=F(3,2);p=1;q=2
    assert (q+1)*h-2*q==F(1,2)
    assert (p+1)*h-p==2
    assert q*(2-h)==1
    kappa=((q+1)*h-2*q)/(q*(2-h))
    assert kappa==F(1,2)
    assert kappa*2==1  # a_n=n^2 has harmonic exceedance probabilities in iid model.
    for p in range(1,9):
        boundary=F(2*p,p+1)
        assert boundary*F(p+1,p)==2
    counts['boundary_and_extreme_value_exponents']=13
    return {'all_passed':True,'total_exact_assertions':sum(counts.values()),'families':counts,
            'arithmetic':'Python fractions.Fraction; no floating point and no external packages',
            'scope':'Finite algebraic and model controls only. Not a realized elliptic parameter, not a gauge existence or nonexistence test.',
            'independent_audit':False}
if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
