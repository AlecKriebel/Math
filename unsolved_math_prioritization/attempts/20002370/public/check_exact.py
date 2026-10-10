#!/usr/bin/env python3
"""Exact logical/arithmetic controls; no finite-model approximation to R(t)."""
from fractions import Fraction
from itertools import product
from math import factorial
import json


def run():
    checks = 0
    def check(c):
        nonlocal checks
        assert c
        checks += 1

    # Every interpretation of two binary predicates H,G and one unary C
    # on two elements: compare the actual distributive/prenex identities.
    d = range(2)
    branching_cases = 0
    diagonal_failures = 0
    guard_cases = 0
    first = None
    for h_mask, c_mask, g_mask in product(range(16), range(4), range(16)):
        H = lambda x, v: bool(h_mask & (1 << (2*x+v)))
        C = lambda u: bool(c_mask & (1 << u))
        G = lambda x, u: bool(g_mask & (1 << (2*x+u)))
        branched = all(all(not H(x,v) for v in d)
                       or all(C(u) or G(x,u) for u in d) for x in d)
        prenex = all(not H(x,v) or C(u) or G(x,u)
                     for x,v,u in product(d,repeat=3))
        diagonal = all(not H(x,u) or C(u) or G(x,u)
                       for x,u in product(d,repeat=2))
        check(branched == prenex)
        check(not prenex or diagonal)
        branching_cases += 1
        if diagonal and not prenex:
            diagonal_failures += 1
            if first is None:
                first = {'H': [[x,v] for x,v in product(d,repeat=2) if H(x,v)],
                         'C': [u for u in d if C(u)],
                         'G': [[x,u] for x,u in product(d,repeat=2) if G(x,u)]}
        if all(not H(x,v) or C(v) for x,v in product(d,repeat=2)):
            check(diagonal)
            guard_cases += 1

    # Factorial digit arithmetic, all exact. m<=5 gives next index<=720;
    # arithmetic size is tiny (the largest integer has 721 bits).
    witnesses = []
    for m in range(2, 6):
        digits = {factorial(j) for j in range(1,m+2)}
        q = sum((Fraction(1, 2**factorial(j)) for j in range(1,m+1)), Fraction(0))
        upto = factorial(m+1)
        b = 0
        first_n = None
        for n in range(1,upto+1):
            b = 2*b + int(n in digits)
            scaled = abs(2**n*q-b)
            if n < upto:
                check(scaled < 1)
            else:
                check(scaled == 1)
            if first_n is None and scaled >= 1:
                first_n = n
        check(first_n == upto)
        witnesses.append({'m':m,'partial_sum':str(q),'first_failure_index':first_n})

    # Verify the source's offset identity on matched finite truncations.
    offsets=[]
    for p in (2,3,5,7):
        for m in range(2,7):
            original = sum((Fraction(1,p**factorial(j)) for j in range(m+1)),Fraction(0))
            distinct = sum((Fraction(1,p**factorial(j)) for j in range(1,m+1)),Fraction(0))
            check(original-distinct == Fraction(1,p))
            check((1+distinct)-original == 1-Fraction(1,p))
        offsets.append({'p':p,'printed_rhs_minus_lhs':str(1-Fraction(1,p))})

    # Explicit two-element countermodel with H(x,v)=>C(v), yet diagonal
    # replacement true while full formula false. This is a logic control.
    H = lambda x,v: x==0 and v==0
    C = lambda u: u==0
    G = lambda x,u: False
    check(all(not H(x,u) or C(u) or G(x,u) for x,u in product(d,repeat=2)))
    check(not all(not H(x,v) or C(u) or G(x,u) for x,v,u in product(d,repeat=3)))

    return {'assertions': checks,
            'all_two_element_interpretations': branching_cases,
            'diagonal_false_positives': diagonal_failures,
            'H_implies_C_second_coordinate_cases': guard_cases,
            'first_diagonal_countermodel':first,
            'cut_witness_examples':witnesses,
            'finite_source_offset_checks':offsets,
            'scope':'Exact logical transformations and rational arithmetic only; not a field-theory decision procedure.'}

if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
