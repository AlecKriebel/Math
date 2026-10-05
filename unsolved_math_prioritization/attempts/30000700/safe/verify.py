#!/usr/bin/env python3
"""Exact rational polynomial controls; the universal proofs are in PROOF.md.

No external libraries, source corpora, network access, or floating point.
Polynomial coefficient lists are in ascending order.
"""
from fractions import Fraction as Q
from math import factorial
import json

def trim(p):
    p=list(map(Q,p))
    while len(p)>1 and p[-1]==0:p.pop()
    return p

def deriv(p):
    return trim([i*p[i] for i in range(1,len(p))] or [0])

def theta(p):
    return trim([i*p[i] for i in range(len(p))])

def val(p,x):
    y=Q(0)
    for c in reversed(p):y=y*x+c
    return y

def remainder(p,q):
    p=trim(p);q=trim(q)
    assert q!=[0]
    while p!=[0] and len(p)>=len(q):
        j=len(p)-len(q); c=p[-1]/q[-1]
        for i,v in enumerate(q):p[i+j]-=c*v
        p=trim(p)
    return p

def sub_const(p,c):
    p=list(p);p[0]-=c;return trim(p)

def main():
    basic=[Q(0),Q(0),Q(1,2)]
    assert deriv(basic)==[Q(0),Q(1)]
    assert deriv(deriv(basic))==[Q(1)]
    assert val(basic,Q(0))==val(deriv(basic),Q(0))==0
    assert val(deriv(basic),Q(1))==1
    assert val(deriv(deriv(basic)),Q(1))==1

    positive=negative=total=0
    for n in range(2,13):
        for b in [Q(1),Q(-2),Q(3,7)]:
            for A in sorted({b/Q(factorial(n)),Q(1,2),Q(1),Q(2)}):
                f=[Q(0)]*n+[A]
                fp=deriv(f)
                for k in range(2,15):
                    fk=list(f)
                    for _ in range(k):fk=deriv(fk)
                    # f'-b is squarefree because b != 0 and f=A*z^n.
                    actual=remainder(sub_const(fk,b),sub_const(fp,b))==[0]
                    expected=(k==n and A*factorial(n)==b)
                    assert actual==expected,(n,b,A,k,actual,expected)
                    total+=1
                    if actual:positive+=1
                    else:negative+=1

    trans=[]
    base=[Q(1),Q(-2),Q(1)]
    fp_over_lambda=theta(base)
    b_over_lambda=Q(-1,2)
    assert sub_const(fp_over_lambda,b_over_lambda)==[Q(1,2),Q(-2),Q(2)]
    assert val(sub_const(fp_over_lambda,b_over_lambda),Q(1,2))==0
    assert val(deriv(sub_const(fp_over_lambda,b_over_lambda)),Q(1,2))==0
    for k in range(3,25):
        p=list(base)
        for _ in range(k):p=theta(p)
        assert p==[Q(0),Q(-2),Q(2**k)]
        lam_power=Q(-1,2**(k-1)-2)
        normalized=[lam_power*c for c in p]
        residual=sub_const(normalized,b_over_lambda)
        assert val(normalized,Q(1,2))==b_over_lambda
        assert remainder(residual,[Q(-1,2),Q(1)])==[0]
        # The value condition at b is IM implication, not a CM divisibility demand.
        assert remainder(residual,sub_const(fp_over_lambda,b_over_lambda))!=[0]
        # Negative control: dropping the necessary lambda relation fails.
        assert val(p,Q(1,2))!=b_over_lambda
        trans.append({'k':k,'lambda_power':str(lam_power),'normalized_value_at_half':str(val(normalized,Q(1,2)))})

    report={
        'status':'PASS',
        'arithmetic':'Python standard-library Fraction; no floating point',
        'basic_quadratic_control':'PASS',
        'polynomial_classification_controls':{'tested':total,'positive':positive,'negative':negative,'degree_range':[2,12],'k_range':[2,14]},
        'transcendental_identity_controls':trans,
        'negative_controls':['wrong coefficient or derivative order rejected','lambda=1 rejected for transcendental family','CM demand at b deliberately distinguished from required value implication'],
        'limits':'Finite controls check algebra and implementation. Universal classification and transcendental construction are proved in PROOF.md, not inferred from tests.'
    }
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':main()
