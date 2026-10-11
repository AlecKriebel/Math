#!/usr/bin/env python3
"""Exact arithmetic and free-group Fox identities; these do not certify cost or l2 injectivity."""
from collections import defaultdict
from fractions import Fraction
import json

def reduce_word(w):
    result=[]
    for x in w:
        if result and result[-1] == -x:
            result.pop()
        else:
            result.append(x)
    return tuple(result)

def inverse(w):
    return tuple(-x for x in reversed(w))

def plus(*terms):
    p=defaultdict(int)
    for a in terms:
        for w,c in a.items():
            p[w]+=c
    return {w:c for w,c in p.items() if c}

def scale(a,c):
    return {w:v*c for w,v in a.items() if v*c}

def product(a,b):
    p=defaultdict(int)
    for w,c in a.items():
        for v,d in b.items():
            p[reduce_word(w+v)]+=c*d
    return {w:c for w,c in p.items() if c}

def monomial(w):
    return {reduce_word(w):1}

def fox(word,x):
    """Enumerate actual lifted oriented edges along the attaching loop."""
    p=defaultdict(int);prefix=()
    for letter in word:
        if letter==x:
            p[prefix]+=1
        prefix=reduce_word(prefix+(letter,))
        if letter==-x:
            p[prefix]-=1
    return {w:c for w,c in p.items() if c}

def verify():
    alpha=Fraction(1,2**61);eta=alpha/100
    q_upper=Fraction(3**97*96**4,2**183)
    assert 0<alpha<Fraction(1,200) and q_upper<Fraction(1,2)
    height=99*eta.denominator+1
    assert height>100 and Fraction(99,height)<eta
    a=1;bs=list(range(2,101));t=101
    us=[()]
    for b in bs:
        us.append(us[-1]+(a,b))
    w=us[-1]+(a,);rw=(t,)+w+(-t,)+inverse(w)
    S=plus(*(monomial(u) for u in us))
    assert fox(w,a)==S
    telescoping=product(S,plus(monomial((a,)),{():-1}))
    for i,b in enumerate(bs):
        P=monomial(us[i]+(a,))
        assert fox(w,b)==P
        telescoping=plus(telescoping,product(P,plus(monomial((b,)),{():-1})))
    assert telescoping==plus(monomial(w),{():-1})
    # Test each raw free-group commutator derivative before quotient evaluation.
    for x in [a,*bs]:
        Dw=fox(w,x)
        expected=plus(product(monomial((t,)),Dw),scale(product(monomial(rw),Dw),-1))
        assert fox(rw,x)==expected
    assert fox(rw,t)==plus({():1},scale(monomial((t,)+w+(-t,)),-1))
    for b in bs:
        ri=(t,b,-t,-b)
        assert fox(ri,b)==plus(monomial((t,)),scale(monomial(ri),-1))
        assert fox(ri,t)==plus({():1},scale(monomial((t,b,-t)),-1))
        assert fox(ri,a)=={}
    return {
        "result":"PASS", "alpha":str(alpha),"eta":str(eta),
        "K_alpha_cubed_strict_upper":str(q_upper),"admissible_height_M":height,
        "Fox_derivative_coordinates_checked":100,
        "commutator_derivatives_checked":398,
        "telescoping_identity":"S(a-1)+sum_i P_i(b_i-1)=w-1 in the free group ring",
        "scope":"Exact integer/rational parameter and free-group chain identities. Tree kernel, topology, measured cost and dimension arguments require the proofs and audits."
    }

if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
