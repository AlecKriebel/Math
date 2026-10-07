#!/usr/bin/env python3
"""Exact, offline arithmetic checks. These do not prove the missing intersection vanishings."""
from fractions import Fraction as Q
from math import factorial as fac, comb
from itertools import product
import json

def bernoulli(n):
    # Standard B_1=-1/2 convention; only positive even indices are used below.
    bs=[Q(1)]
    for m in range(1,n+1):
        bs.append(-sum(Q(comb(m+1,k))*bs[k] for k in range(m))/Q(m+1))
    return bs[n]

def double_odd(k):
    v=1
    for n in range(1,2*k,2):v*=n
    return v

def hodge(g):
    G=g*(g+1)//2
    v=Q((-1)**G*fac(G),2**g)
    for k in range(1,g+1):v*=(-bernoulli(2*k)/Q(2*k))/double_odd(k)
    return v

def rank_one(g):return Q(1,2)*(-2)**(g-1)*fac(g-1)*hodge(g-1)

def C(g,a,b):
    h=g-2
    assert a>0 and b>0 and a+b<=2*g-1
    return (-1)**(a+b+g)*fac(h)*sum((Q((-4)**i*fac(a-1)*fac(b-1)*fac(2*h-2*i),fac(i)*fac(a-1-i)*fac(b-1-i)*fac(h-i)) for i in range(min(a-1,b-1,h)+1)),Q(0))

def corank_two(g):
    N=2*g-1; H=hodge(g-2)
    I=Q(fac(2*g-2),2**g*fac(g-1))*rank_one(g-1)
    printed_I=I+(-1)**g*fac(2*g-3)*H*sum((-bernoulli(2*m)*Q(2)**(2*m+2-2*g)/fac(2*g-2*m-1)/fac(2*m) for m in range(1,g)),Q(0))
    double=sum((Q((-1)**(k+n+1))*bernoulli(k)*C(g,k-n,2*g-k-1)/fac(k)/Q(2)**(2*g-2-k)/fac(2*g-2-k) for k in range(2,2*g-1,2) for n in range(1,k)),Q(0))
    I_raw=2**(2*g-3)*fac(2*g-2)*(rank_one(g-1)/Q(8**(g-1)*fac(g-1))-Q(1,2)*H*double)
    I+=2**(2*g-4)*fac(2*g-2)*(-1)**g*fac(2*g-3)*H*sum((-bernoulli(2*m)*Q(2)**(2*m+2-2*g)/fac(2*g-2*m-1)/fac(2*m) for m in range(1,g)),Q(0))
    assert I==I_raw,(g,I,I_raw)
    assert printed_I!=I
    II=H/Q(4)*sum((comb(N,a)*C(g,a,N-a) for a in range(1,N)),Q(0))
    III=H/Q(12)*sum((Q(fac(N),fac(a)*fac(b)*fac(N-a-b))*C(g,a,b) for a in range(1,N-1) for b in range(1,N-a)),Q(0))
    closed_II=-H/Q(64*(2*g-1))*(2**(4*g)*fac(g-1)*fac(g-2)+32*(-1)**g*fac(2*g-3))
    assert II==closed_II,(g,II,closed_II)
    return I,II,III,I+II+III

def poly_mul(A,B):
    out={}
    for a,ca in A.items():
        for b,cb in B.items():
            k=tuple(x+y for x,y in zip(a,b));out[k]=out.get(k,0)+ca*cb
    return {k:v for k,v in out.items() if v}

def poly_power(A,n):
    out={(0,)*len(next(iter(A))):1}
    for _ in range(n):out=poly_mul(out,A)
    return out

def checks():
    assert [hodge(i) for i in range(1,6)]==[Q(1,24),Q(1,2880),Q(1,181440),Q(1,1814400),Q(13,16329600)]
    assert rank_one(4)==Q(-1,7560) and rank_one(5)==Q(1,9450)
    expected={
      2:[Q(1,12),Q(-3,2),Q(1,2),Q(-11,12)],
      3:[Q(-1,80),Q(-25,24),Q(5,24),Q(-203,240)],
      4:[Q(1,672),Q(-49,80),Q(7,80),Q(-1759,3360)],
      5:[Q(-1,1296),Q(-3637,2520),Q(1063,7560),Q(-59123,45360)],
      6:[Q(1,220),Q(-23837,315),Q(1639,315),Q(-976649,13860)],
      7:[Q(-11,18),Q(-4194073,189),Q(17594928013,16329600),Q(-49254708341,2332800)]}
    rows={g:list(corank_two(g)) for g in range(2,11)}
    for g in range(2,6):assert rows[g]==expected[g],(g,rows[g],expected[g])
    discrepancies={g:{'finite_sums':[str(x) for x in rows[g]],'v1_table':[str(x) for x in expected[g]]} for g in [6,7]}
    assert rows[6][1]*2==expected[6][1] and rows[6][2]*2==expected[6][2]
    assert rows[7][0:2]==expected[7][0:2] and rows[7][2]!=expected[7][2]
    # Independent Todd-series convolution, before using the simplified b_(n,m).
    todd_count=0
    for n in range(1,10):
        for m in range(1,10):
            raw=sum((Q((-1)**(n+m-i-j))*Q((-1)**i)*bernoulli(i)/fac(i)*Q((-1)**j)*bernoulli(j)/fac(j)/Q(n+m-i-j+1)/fac(n-i)/fac(m-j) for i in range(n+1) for j in range(m+1)),Q(0))
            predicted=Q((-1)**(n+1))*bernoulli(n+m)/fac(n+m) if (n+m)%2==0 else Q(0)
            assert raw==predicted,(n,m,raw,predicted)
            todd_count+=1
    # Expand theta polynomials directly and integrate via the determinant formula.
    # This is independent of the factorial C_g finite sum used for term I.
    direct_checks=0
    for g in range(2,9):
        h=g-2
        for k in range(2,2*g-1):
            for n in range(1,k):
                A=2*g-2-k;B=k-n-1
                raw=Q(0)
                for i in range(min(A,B,h)+1):
                    coefficient=Q(comb(A,i)*comb(B,i))*Q(1,2)**(A-i)*(-2)**i*(-1)**(B-i)
                    fiber=Q((-1)**(h-i)*fac(h)*fac(2*h-2*i)*fac(i),fac(h-i))
                    raw+=coefficient*fiber
                predicted=Q((-1)**k,2**(2*g-2-k))*C(g,k-n,2*g-k-1)
                assert raw==predicted,(g,k,n,raw,predicted)
                direct_checks+=1
    # The source's genus-four coarse numbers are twice the stack numbers.
    assert 2*hodge(4)==Q(1,907200)
    assert 2*rank_one(4)==Q(-1,3780)
    assert 2*rows[4][-1]==Q(-1759,1680)
    # Multiplication-by-m on each factor forces weights 2h, not just total degree rh.
    # r=2: det([[s,u],[u,t]])^h.
    det2={(1,1,0):1,(0,0,2):-1}
    count2=0
    for h in range(9):
        p=poly_power(det2,h)
        for k in range(h+1):
            exps=(h-k,h-k,2*k)
            integral=p[exps]*fac(h-k)**2*fac(2*k)
            assert integral==(-1)**k*fac(h)*fac(2*k)*fac(h-k)//fac(k)
            assert 2*exps[0]+exps[2]==2*h==2*exps[1]+exps[2]
            count2+=1
    # r=3 variables s1,s2,s3,u12,u13,u23.
    det3={(1,1,1,0,0,0):1,(0,0,0,1,1,1):2,(1,0,0,0,0,2):-1,(0,1,0,0,2,0):-1,(0,0,1,2,0,0):-1}
    terms3={}
    for h in range(1,5):
        p=poly_power(det3,h);terms3[h]=len(p)
        for (a,b,c,d,e,f),co in p.items():
            assert 2*a+d+e==2*h and 2*b+d+f==2*h and 2*c+e+f==2*h
            assert a+b+c+d+e+f==3*h
    # Exact residual set after EGH N<3g-3, equivalent to n>T_{g-3}.
    residual={}
    for g in range(3,21):
        G=g*(g+1)//2; tris={k*(k+1)//2 for k in range(g+1)}
        unknown=[n for n in range(G+1) if n not in tris and G-n>=3*g-3]
        assert unknown==[n for n in range((g-3)*(g-2)//2+1) if n not in tris]
        assert len(unknown)==(g-3)*(g-4)//2
        residual[g]=unknown
    assert residual[5]==[2] and residual[6]==[2,4,5]
    # Four-sample coefficient extraction for R(t)=c12+c13*t+c14*t^2+c15*t^3.
    stencil={-2:Q(1,12),-1:Q(-8,12),1:Q(8,12),2:Q(-1,12)}
    for d in range(4):assert sum(w*Q(t)**d for t,w in stencil.items())==int(d==1)
    assert comb(15,13)==105
    # Formal genus-five data do not force a13=0: arbitrary assignments survive known constraints.
    baseline={0:hodge(5),5:rank_one(5),9:rows[5][-1]}
    def evaluate(t,c12,c13,c14,c15):
        values={**baseline,12:Q(c12),13:Q(c13),14:Q(c14),15:Q(c15)}
        return sum((comb(15,N)*v*Q(t)**N for N,v in values.items()),Q(0))
    for vals in product([-1,0,1],repeat=4):
        c12,c13,c14,c15=vals
        def R(t):
            K=sum((comb(15,N)*v*Q(t)**N for N,v in baseline.items()),Q(0))
            return (evaluate(t,*vals)-K)/Q(t)**12
        extracted=sum(w*R(t) for t,w in stencil.items())/105
        assert extracted==c13
    # Cancellation after theta normalization: unnormalized theta'=theta+ell/2.
    for h in range(1,9):
        for k in range(h,21):
            value=sum((Q(comb(k,m)*comb(m,h)*fac(h))*(-2)**m*Q(1,2)**(m-h) for m in range(h,k+1)),Q(0))
            assert value==((-2)**h*fac(h) if k==h else 0)
    # A weight-zero base twist creates positive-codimension pushforward terms.
    # h=1: p_*((theta+c*p^*ell)^2)=2*c*ell, not zero when c*ell is nonzero.
    assert comb(2,1)==2
    return {
      'status':'PASS','arithmetic':'fractions.Fraction; no floating point; standard library only',
      'hodge_degrees_g1_to_g10':{g:str(hodge(g)) for g in range(1,11)},
      'rank_one_g2_to_g10':{g:str(rank_one(g)) for g in range(2,11)},
      'corank_two_terms_g2_to_g10':{g:[str(x) for x in v] for g,v in rows.items()},
      'corank_two_source_table_rows_matched':[2,3,4,5],
      'preprint_v1_reproducibility_discrepancies':discrepancies,
      'preprint_v1_I_formula':'Printed simplified Proposition 9.4 differs from preceding finite-sum calculation; correction term needs multiplicative 2^(2g-4)*(2g-2)!. This is a v1 comparison, not an erratum claim about the unavailable journal PDF.',
      'todd_convolution_checks':todd_count,'direct_theta_expansion_checks':direct_checks,
      'determinant2_monomials_checked':count2,'determinant3_nonzero_monomial_counts':terms3,
      'residual_required_zero_hodge_exponents_g3_to_g20':residual,
      'genus5_stencil_cases_checked':81,
      'scope':'Reproduces low-genus known numbers, flags preprint arithmetic inconsistencies, and checks finite algebra identities. No value for actual genus-five L^2 D^13 was computed.'}

if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
