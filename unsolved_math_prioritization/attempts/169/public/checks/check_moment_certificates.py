#!/usr/bin/env python3
"""Exact checks of abstract moment obstructions and Charlier minorants.

No distribution in this file is asserted to be a translate convolution.
Floating-point LP was used only to propose finite supports in moment_*.json;
every accepted weight and identity below is checked with rational arithmetic.
"""
from fractions import Fraction
import json
import math
from pathlib import Path
HERE=Path(__file__).resolve().parent
def check(b,s):
    if not b:raise ValueError(s)
def falling(n,r):return math.prod(range(n-r+1,n+1)) if n>=r else 0
def rat(q):return [q.numerator,q.denominator]
def coeff(j,M):return [Fraction(math.comb(j,l)*(-1)**l,M**l) for l in range(j+1)]
def polyadd(a,b):
    out=[Fraction()] * max(len(a),len(b))
    for i,x in enumerate(a):out[i]+=x
    for i,x in enumerate(b):out[i]+=x
    return out
def polymul(a,b):
    out=[Fraction()]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out
def ordinary_charlier(j,M):
    out=[Fraction()]*(j+1);fall=[Fraction(1)]
    for l,c in enumerate(coeff(j,M)):
        for i,x in enumerate(fall):out[i]+=c*x
        fall=polymul(fall,[Fraction(-l),Fraction(1)])
    return out
def poisson_ordinary_moments(M,n):
    row=[1];out=[]
    for degree in range(n+1):
        if degree:
            row=[0]+[row[j-1]+j*(row[j] if j<len(row) else 0) for j in range(1,degree+1)]
        out.append(sum(s*M**j for j,s in enumerate(row)))
    return out
def finite_rational_laws():
    result=[]
    for d in (4,10,20,30):
        r=json.loads((HERE.parent/'fixtures'/f'moment_{d}.json').read_text())
        xs=r['support'];weights=[Fraction(*w) for w in r['weights']];M=r['lambda']
        check(r['degree']==d and len(xs)==len(weights),'finite law metadata')
        check(all(x>=1 for x in xs) and len(set(xs))==len(xs),'positive support')
        check(all(w>0 for w in weights) and sum(weights)==1,'positive normalized weights')
        for j in range(d+1):
            check(sum(w*falling(x,j) for x,w in zip(xs,weights))==M**j,'finite exact factorial moment')
        result.append({'degree':d,'lambda':M,'support_size':len(xs),'support_min':min(xs),
                       'support_max':max(xs),'zero_mass':0,'exact_moments_verified':d+1,
                       'certificate_file':f'moment_{d}.json'})
    return result
def zero_free_laws():
    result=[]
    for M in (1,2,3,5,10,100):
        scaled=[]
        for j in range(M+1):
            w=Fraction(M**j,math.factorial(j))-(-1)**j*math.comb(M,j)
            check(w>=0,'negative zero-free mass')
            if j==0:check(w==0,'zero atom retained')
            elif j<=M:check(w>0,'unexpected vanishing positive atom')
            scaled.append(rat(w))
        for r in range(M):
            value=sum((-1)**j*math.comb(M,j)*falling(j,r) for j in range(M+1))
            check(value==0,'finite-difference cancellation')
        defect=sum((-1)**j*math.comb(M,j)*falling(j,M) for j in range(M+1))
        check(defect==(-1)**M*math.factorial(M),'first unmatched moment')
        result.append({'lambda':M,'matched_degree':M-1,'zero_mass':0,
                       'scaled_weights_qj_div_exp_minus_M_through_M':scaled,
                       'tail':'For j>M, q_j=e^-M M^j/j! unchanged.',
                       'normalization':'Poisson normalization plus the exact r=0 cancellation.',
                       'first_unmatched_factorial_moment_order':M,
                       'first_unmatched_factorial_moment_defect_scaled_by_exp_minus_M':-defect})
    return result
def verify_recurrence(j,M):
    c=coeff(j,M);left=[Fraction()]*(j+2)
    for l,x in enumerate(c):left[l]+=l*x;left[l+1]+=x
    right=[Fraction()]*(j+2)
    for l,x in enumerate(coeff(j+1,M)):right[l]-=M*x
    for l,x in enumerate(c):right[l]+=(M+j)*x
    if j:
        for l,x in enumerate(coeff(j-1,M)):right[l]-=j*x
    check(left==right,'normalized Charlier recurrence')
def charlier_minorants():
    result=[]
    for M in (1,2,3,4,5,6,10,100):
        a=[Fraction(M**j,math.factorial(j)) for j in range(M+1)]
        b=[a[j]*Fraction(M-j,M) for j in range(M)]+[a[M-1]/(2*M-1)]
        q0=sum(b);norm=sum(b[j]*b[j]/a[j] for j in range(M+1))
        xnorm=sum((M+j)*b[j]*b[j]/a[j] for j in range(M+1))
        xnorm-=2*sum(M*b[j]*b[j+1]/a[j+1] for j in range(M))
        value=norm-xnorm
        check(q0==Fraction(2*M,2*M-1)*a[M-1],'Charlier Q(0)')
        check(value==a[M-1]/(2*M-1),'Charlier tridiagonal expectation')
        normalized=value/(q0*q0)
        check(normalized==Fraction(2*M-1,4*M*M)/a[M-1] and normalized>0,'minorant margin')
        for j in range(M+1):verify_recurrence(j,M)
        if M<=6:
            Q=[Fraction()]
            for j,bj in enumerate(b):Q=polyadd(Q,[bj*x for x in ordinary_charlier(j,M)])
            P=polymul([Fraction(1),Fraction(-1)],polymul(Q,Q))
            moments=poisson_ordinary_moments(M,len(P)-1)
            direct=sum(c*m for c,m in zip(P,moments))
            check(direct==value,'independent monomial expectation')
            for n in range(0,3*M+5):
                pn=sum(c*n**j for j,c in enumerate(P))/(q0*q0)
                check(pn<=(1 if n==0 else 0),'minorant integer inequality')
                if n==0:check(pn==1,'minorant normalization')
        result.append({'M':M,'degree':2*M+1,'Q_coefficients_in_normalized_Charlier_basis':list(map(rat,b)),
                       'Q_at_zero':rat(q0),'unnormalized_expectation':rat(value),
                       'normalized_positive_margin':rat(normalized),
                       'polynomial':'P(x)=(1-x)(Q(x)/Q(0))^2',
                       'minorant_reason':'P(0)=1 and (1-x)<=0 for every integer x>=1.'})
    return result
def main():
    result={'scope':'Abstract integer-valued moment laws and polynomial certificates only; no convolution realizability or uniform random-A moment theorem asserted.',
            'finite_rational_positive_support_laws':finite_rational_laws(),
            'zero_free_finite_difference_laws':zero_free_laws(),
            'nonnegative_square_minorants':charlier_minorants()}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
