"""Reproduce every finite certificate and exact algebra control using Python's standard library.
This is not a proof assistant and does not certify the infinite-n sharp constant.
"""
import json
from pathlib import Path
from fractions import Fraction as F
from exact_core import Q,coeffs_from_sums,sums_from_coeffs,coeffs_from_roots,fixed_root_recurrence

def main():
    if not __debug__: raise SystemExit("Assertions must be enabled; run without -O.")
    p=Path(__file__).parent
    d=json.loads((p/'CERTIFICATE.json').read_text())
    n=d['n']; r=F(d['radius']);s=[Q.parse(x) for x in d['sums']]
    assert n==32 and len(s)==n and r==F(29,40)
    assert all(z.norm2()<r*r for z in s)
    a=coeffs_from_sums(s)
    assert a[0]==Q(1) and sum(a,Q())==Q()
    assert sums_from_coeffs(a)==s
    b=fixed_root_recurrence(s)
    assert b[-1]==Q()
    assert a==[b[0]]+[b[j]-b[j-1] for j in range(1,n+1)]
    # A second route reconstructs the monic degree n polynomial as (X-1)Q(X).
    recovered=[Q(1)]
    recovered.extend(b[j]-b[j-1] for j in range(1,n))
    recovered.append(-b[n-1])
    assert recovered==a
    # The proposed literal strict upper bound is rejected after a substantial perturbation.
    perturbed=s[:];perturbed[-1]+=Q(F(1,10**6))
    assert sum(coeffs_from_sums(perturbed),Q())!=Q()
    assert (s[0]+Q(1)).norm2()>r*r
    # Rational root tuples, including zero roots, repeated roots, and roots outside the unit disk.
    fixtures=[]
    for n0 in range(1,10):
        for seed in range(4):
            roots=[Q(1)]+[Q(F(((j+seed)%5)-2,2),F(((2*j+seed)%7)-3,3)) for j in range(n0-1)]
            fixtures.append(roots)
    fixtures += [[Q(1),Q(),Q(),Q()], [Q(1)]*5, [Q(1),Q(2),Q(-3),Q(0,2)]]
    recurrence_checks=0
    for roots in fixtures:
        ss=[sum((z**k for z in roots),Q()) for k in range(1,len(roots)+1)]
        aa=coeffs_from_roots(roots)
        assert coeffs_from_sums(ss)==aa
        assert sums_from_coeffs(aa)==ss
        bb=fixed_root_recurrence(ss)
        assert bb[:-1]==coeffs_from_roots(roots[1:]) and bb[-1]==Q()
        C=Q(1)
        for t in range(1,len(roots)+1):
            assert sum((ss[k-1]*bb[t-k] for k in range(1,t+1)),Q())==C-t*bb[t]
            C+=bb[t];recurrence_checks+=1
    # Algebraic n=2 identity as a polynomial in x=Re(w), t=|w|^2.
    # Coefficients indexed by (x power, t power).
    lhs={(0,2):F(1),(0,0):F(4),(2,0):F(8),(1,1):F(-4),(1,0):F(-8)}
    rhs={(0,2):F(1),(0,0):F(4),(2,0):F(8),(1,1):F(-4),(1,0):F(-8)}
    # Explicitly expand (t-2)^2/2 + 8(x-(t+2)/4)^2 instead of relying on sampling.
    def mul(A,B):
        c={}
        for (i,j),v in A.items():
            for (k,l),w in B.items():c[i+k,j+l]=c.get((i+k,j+l),F())+v*w
        return c
    def add(A,B):
        c=A.copy()
        for k,v in B.items():c[k]=c.get(k,F())+v
        return {k:v for k,v in c.items() if v}
    sq1=mul({(0,1):F(1),(0,0):F(-2)},{(0,1):F(1),(0,0):F(-2)})
    lin={(1,0):F(1),(0,1):F(-1,4),(0,0):F(-1,2)}
    rhs=add({k:v/2 for k,v in sq1.items()},{k:8*v for k,v in mul(lin,lin).items()})
    assert lhs==rhs
    # Work modulo t^2-6t+4, with t=3-sqrt(5), to check the extremal equality.
    def qmul(x,y):return (x[0]*y[0]-4*x[1]*y[1],x[0]*y[1]+x[1]*y[0]+6*x[1]*y[1])
    t=(F(0),F(1));tminus2=(F(-2),F(1))
    assert tuple(v/2 for v in qmul(tminus2,tminus2))==t
    assert F(3,4)**2-6*F(3,4)+4>0 and F(4,5)**2-6*F(4,5)+4<0
    # Majorant coefficient and partial-sum product identities at exact rational M.
    majorant_checks=0
    for M in [F(0),F(1,4),F(1,2),F(3,4),F(1),F(5,4)]:
        coeff=F(1);partial=F(1);prod=F(1)
        for j in range(1,33):
            coeff*= (M+j-1)/j;partial+=coeff;prod*=1+M/j
            assert partial==prod
            if 0<=M<1:assert coeff<1
            majorant_checks+=1
    # Constant-sum ansatz gives b_n=(1-u)_n/n! and can only terminate at u in {1,...,n}.
    ansatz_checks=0
    for n0 in range(1,10):
        for u in [Q(F(1,3),F(2,5)),Q(F(3,4)),Q(1),Q(2)]:
            coeff=Q(1)
            for j in range(1,n0+1):coeff=coeff*(j-u)/j
            assert fixed_root_recurrence([u]*n0)[-1]==coeff
            ansatz_checks+=1
    # The scalar-cone extension has q^2 <= gamma^2(1-gamma^2) <= 1/4.
    for g2 in [F(j,16) for j in range(17)]:assert F(1,4)-g2*(1-g2)==(g2-F(1,2))**2
    # Normalization cannot be omitted: all-zero tuple has all power sums zero.
    assert sums_from_coeffs([Q(1),Q(),Q(),Q()])==[Q(),Q(),Q()]
    # Extension from n to n+1 by adding zero does not preserve the old observation window.
    z=Q(F(-3,10),F(1,2))
    old=[1+z**k for k in (1,2)]
    assert all(w.norm2()<F(9,10)**2 for w in old) and (1+z**3).norm2()>1
    # Certificate output omits any high-degree root approximations, unnecessary for validity.
    report={'status':'PASS','certificate_n':n,'strict_radius':str(r),'exact_norm_squared_inequalities':len(s),
            'root_at_one_exact':True,'roundtrip_fixture_count':len(fixtures),'recurrence_identity_checks':recurrence_checks,
            'majorant_identity_checks':majorant_checks,'constant_sum_identity_checks':ansatz_checks,
            'n2_polynomial_identity':'PASS','n2_algebraic_endpoint':'PASS','negative_controls':4,
            'sharp_universal_constant_solved':False,'uses_external_source_bytes':False}
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':main()
