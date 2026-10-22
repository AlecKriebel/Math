#!/usr/bin/env python3
"""Exact, dependency-free controls for the scoped Brannan reproduction.
These checks reproduce finite identities; they do not prove a universal
coefficient inequality or certify any literature proof.
"""
from fractions import Fraction as F
from math import comb
import json
from pathlib import Path


def choose(a, k):
    a = F(a)
    v = F(1)
    for r in range(k):
        v *= (a-r)/(r+1)
    return v


def rising(a, k):
    a = F(a)
    v = F(1)
    for r in range(k):
        v *= (a+r)/(r+1)
    return v


def coefficients(a, b, n):
    return [choose(a, k)*rising(b, n-k) for k in range(n+1)]


def evaluation(a, b, n, x):
    return sum(c*F(x)**k for k, c in enumerate(coefficients(a, b, n)))


def witness(a, b, n):
    plus, minus = evaluation(a,b,n,1), evaluation(a,b,n,-1)
    collapsed = (-1)**n*choose(a-b,n)
    assert minus == collapsed
    assert plus > 0 and abs(minus)>plus
    return {"alpha":str(a),"beta":str(b),"index":n,"x":"-1",
            "coefficient_vector":[str(c) for c in coefficients(a,b,n)],
            "A_at_1":str(plus),"A_at_minus_1":str(minus),
            "reverse_gap":str(abs(minus)-plus)}


def run():
    w3=witness(F(3,2),F(1,14),3)
    assert w3['A_at_1']=='33/686' and w3['reverse_gap']=='1/98'
    w5=witness(F(3,2),F(1,32),5)
    assert w5['A_at_1']=='2997183/268435456'
    assert w5['A_at_minus_1']=='3171231/268435456'
    assert w5['reverse_gap']=='5439/8388608'

    # General cubic identity in s=a+b,d=a-b on an exact rational grid.
    cubic_cases=0
    for a in [F(i,7) for i in range(1,29)]:
        for b in [F(i,11) for i in range(1,23)]:
            s,d=a+b,a-b
            plus=evaluation(a,b,3,1)
            assert plus==s*(s*s-3*d+2)/6
            E=(coefficients(a,b,3)[0]+coefficients(a,b,3)[2])
            O=(coefficients(a,b,3)[1]+coefficients(a,b,3)[3])
            wall=3*b*(b+1)+(a-1)*(a-2)
            assert E>0 and O==a*wall/6
            assert (abs(evaluation(a,b,3,-1))<=plus)==(wall>=0)
            cubic_cases+=1

    # Both endpoints and the beta=1 coefficient identification.
    endpoint_cases=0
    for a in [F(i,17) for i in range(1,17)]:
        for n in range(1,32):
            assert coefficients(a,F(1),n)==[choose(a,k) for k in range(n+1)]
            assert evaluation(a,F(1),n,-1)==(-1)**n*choose(a-1,n)
            if n%2:
                assert 0<evaluation(a,F(1),n,-1)<evaluation(a,F(1),n,1)
            endpoint_cases+=1

    # Recurrence derived by logarithmically differentiating the generating germ.
    recurrence_cases=0
    for a,b in [(F(1,3),F(1)),(F(3,2),F(1,32)),(F(5,7),F(2,3))]:
        for x in [F(-1),F(0),F(1),F(3,5)]:
            vals=[evaluation(a,b,n,x) for n in range(18)]
            for n in range(1,17):
                assert (n+1)*vals[n+1]==(a*x+b-n*(x-1))*vals[n]+x*(n-1+b-a)*vals[n-1]
                recurrence_cases+=1

    # Exact identities appearing in the attributed every-index construction.
    derivative_cases=[]
    for j in range(3,41):
        m=j-2; C=m*2**(m+1)+1; c=F(3,2*C)
        total=sum(F(comb(m,k),j-k) for k in range(m+1))
        assert total==F(C,j*(j-1))
        Rp=-F(1,j*(j-1))+c*total
        gap=F(1-c,j*(j-1))-Rp
        assert Rp==F(1,2*j*(j-1))>0
        assert gap==F(C-3,2*C*j*(j-1))>0
        derivative_cases.append(j)

    # Control against accidentally using the cubic witness unchanged for j=5.
    cubic_parameters_at_5=evaluation(F(3,2),F(1,14),5,1)
    assert abs(evaluation(F(3,2),F(1,14),5,-1))<cubic_parameters_at_5
    return {"status":"PASS","arithmetic":"fractions.Fraction exact rational",
            "witnesses":[w3,w5],"cubic_cases":cubic_cases,
            "endpoint_cases":endpoint_cases,"recurrence_cases":recurrence_cases,
            "every_index_identity_cases":derivative_cases,
            "control_cubic_parameters_do_not_violate_index_5":True,
            "universal_beta_1_theorem_independently_certified":False,
            "published_numerical_minima_certified":False}

if __name__=='__main__':
    report=run()
    print(json.dumps(report,indent=2,sort_keys=True))
