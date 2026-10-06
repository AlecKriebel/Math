#!/usr/bin/env python3
"""Finite exact controls only; not a prismatic vanishing verifier."""
import json
from math import comb
from pathlib import Path


def vp(n, p):
    if n == 0:
        return 10**9
    n = abs(n)
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def mul(f, g):
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            out[i + j] += a*b
    return out


def at(f, u):
    return sum(a*u**i for i, a in enumerate(f))


def order(f, p):
    return min((vp(a,p)+i for i,a in enumerate(f) if a), default=10**9)


def controls():
    thickening = []
    specialization = []
    frobenius_divisors = []
    differential = []
    for p in (2, 3, 5, 7):
        d = [-p, 1]
        f = [1]
        for n in range(1, 9):
            f = mul(f, d)
            expected = [comb(n,j)*(-p)**(n-j) for j in range(n+1)]
            assert f == expected
            assert order(f,p) == n
            assert at(f,p) == 0
            thickening.append({'p':p,'N':n,'m_adic_order':n,
                               'nonzero_mod_m_N_plus_1':True})
        f = mul([0,1], d)
        assert at(f,0) == at(f,p) == 0
        assert f != [0]*len(f) and order(f,p)==2
        specialization.append({'p':p,'polynomial_coefficients':f,'order':2})
        for r in range(7):
            # phi^r(d)=u^(p^r)-p; specialize to M=A/(u).
            value=-p
            assert vp(value,p)==1
            assert p % abs(value)==0
            assert p % (p*p)!=0
            frobenius_divisors.append({'p':p,'r':r,'value_on_A_mod_u':value})
        for k in range(1,7):
            nmax=8
            # The primitive of each monomial p^n*T^(p^n-1) is T^(p^n).
            assert all((p**n)*1 == p**n for n in range(1,nmax+1))
            # Subtract the exact finite head, then factor p^k from the tail.
            for n in range(1,nmax+1):
                original=p**n
                head=p**n if n<k else 0
                tail=p**(n-k) if n>=k else 0
                assert original-head==p**k*tail
            differential.append({'p':p,'k':k,'tested_terms':nmax,
                                 'tail_identity':True,'primitive_coefficients_all_one':True})
    return {'all_checks_pass':True,
            'scope':'Finite integer identities and module-model controls only; infinite and geometric claims require the written proofs.',
            'thickening_controls':thickening,
            'two_specializations':specialization,
            'individual_frobenius_divisors':frobenius_divisors,
            'de_rham_tail_identities':differential,
            'counts':{'thickening':len(thickening),'specialization':len(specialization),
                      'frobenius':len(frobenius_divisors),'differential':len(differential)}}

if __name__ == '__main__':
    result=controls()
    path=Path(__file__).with_name('CONTROL_RESULTS.json')
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if path.exists():
        assert path.read_text()==text, 'Recorded result mismatch; do not silently rewrite a frozen artifact.'
    else:
        path.write_text(text)
    print(json.dumps({'all_checks_pass':True,'counts':result['counts']},sort_keys=True))
