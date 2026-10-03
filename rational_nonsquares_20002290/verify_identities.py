#!/usr/bin/env python3
"""Exact identities and bounded falsification checks, not proofs of Question 6.
Requires Python 3 and SymPy. Writes deterministic verification.json beside itself.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt, prod
from pathlib import Path
import json
import sympy as sp


def is_square(v):
    v = Q(v)
    return v >= 0 and isqrt(v.numerator) ** 2 == v.numerator and isqrt(v.denominator) ** 2 == v.denominator


def local_roots_through(x, p, exponent=6):
    roots = [a for a in range(p) if (a*a-x) % p == 0]
    modulus = p
    for _ in range(1, exponent):
        roots = [a + j*modulus for a in roots for j in range(p)
                 if ((a+j*modulus)**2-x) % (modulus*p) == 0]
        modulus *= p
        assert roots
    return roots, modulus


def main():
    results = {}
    primes = [2,3,5,7,11]
    sets = [s for k in range(6) for s in combinations(primes,k)]
    local_tests = 0
    for s in sets:
        m = 4*prod(s)
        x = m*m+1
        assert m*m < x < (m+1)*(m+1)
        assert not is_square(x)
        for p in s:
            roots, modulus = local_roots_through(x,p)
            assert all((r*r-x) % modulus == 0 for r in roots)
            local_tests += 1
    results['finite_place_examples'] = {'sets':len(sets), 'prime_power_lifts':local_tests,
        'exponent':6, 'passed':True}

    H = 1000
    templates = [(Q(2),Q(3)),(Q(-1),Q(-1)),(Q(1,3),Q(5,7)),(Q(-2),Q(100))]
    rows=[]
    for a,b in templates:
        D = sp.ilcm(a.denominator,b.denominator)
        A,B = int(D*D*a),int(D*D*b)
        count = sum(is_square(a*n+b) for n in range(1,H+1))
        upper = 2*isqrt(abs(A)*H+abs(B))+1
        assert count <= upper
        rows.append({'a':str(a),'b':str(b),'count':count,'upper':upper})
    results['one_square_count_samples']={'H':H,'templates':rows,'passed':True}

    residues=[(u,v) for u in range(3) for v in range(3) if (u*u+v*v)%3==0]
    assert residues==[(0,0)]
    sample_z={Q(n,d) for n in range(-20,21) for d in range(1,11)}
    assert all(not is_square(3+2*z*z) for z in sample_z)
    results['quadratic_image_example']={'image':'3+2*z^2','mod_3_anisotropy':True,
        'rational_samples':len(sample_z),'passed':True}

    roots=[Q(t,9) for t in [11,50,71,88,103]]
    x,y=Q(383,27),Q(121,81)
    vals=[y+2*i*x+i*i for i in range(5)]
    assert vals==[r*r for r in roots]
    assert [vals[i+2]-2*vals[i+1]+vals[i] for i in range(3)]==[Q(2)]*3
    assert y-x*x==Q(-145600,729)
    results['buchi_five_false_positive']={'x':str(x),'y':str(y),'defect':str(y-x*x),'passed':True}

    U,c,delta,a,b = sp.symbols('U c delta a b')
    g=(U**3+c)**2+delta
    assert sp.expand(sp.diff(g,U)-6*U**2*(U**3+c))==0
    discriminant=sp.factor(sp.discriminant(g,U))
    assert sp.expand(discriminant+46656*delta**3*(c*c+delta)**2)==0
    results['genus_two_squarefreeness_identity']={'discriminant':str(discriminant),'passed':True}

    x,y=Q(-1,2),Q(0)
    assert y-x*x != 0
    assert [i*i+2*x*i+y for i in range(3)]==[Q(0),Q(0),Q(2)]
    results['three_shift_exception']={'f':'T*(T-1)','values_0_1_2':['0','0','2'],'passed':True}

    assert sp.expand((a+b)**2-a*a-b*b-2*a*b)==0
    results['polarization_identity']={'passed':True}

    coeffs=[Q(9,25),Q(16,25)]
    inputs=[1/q for q in coeffs]
    assert sum(coeffs)==1 and all(is_square(q) for q in coeffs+inputs)
    assert sum(c*x for c,x in zip(coeffs,inputs))==2
    assert not is_square(2)
    results['nonprojection_square_failure_example']={'coefficients':list(map(str,coeffs)),
        'square_inputs':list(map(str,inputs)), 'image':'2', 'passed':True}

    output={'scope':'Exact identities and bounded sanity checks only; no proof of the full question.',
        'groups':len(results),'all_passed':True,'results':results}
    dest=Path(__file__).with_name('verification.json')
    dest.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':
    main()
