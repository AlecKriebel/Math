#!/usr/bin/env python3
"""Independent exhaustive finite-deck / tableau check of historical-rank formulas.
No campaign implementation is imported. Stdlib and integer arithmetic only.
"""
from collections import Counter, defaultdict
from itertools import permutations
from bisect import bisect_right
from fractions import Fraction
from math import factorial
from pathlib import Path
import json, hashlib
from datetime import datetime, timezone


def tops(permutation):
    row = []
    for v in permutation:
        j = bisect_right(row, v)
        if j == len(row):
            row.append(v)
        else:
            row[j] = v
    return tuple(row)


def addable(shape):
    for i in range(len(shape) + 1):
        if i == len(shape):
            yield shape + (1,), i
        elif i == 0 or shape[i] < shape[i - 1]:
            a = list(shape)
            a[i] += 1
            yield tuple(a), i


def hook_count(shape):
    n = sum(shape)
    prod = 1
    for i, length in enumerate(shape):
        for j in range(length):
            prod *= length - j + sum(r > j for r in shape[i+1:])
    assert factorial(n) % prod == 0
    return factorial(n) // prod


def tableau_histories(N):
    # (shape, first-row labels) -> number of standard tableaux
    states = {((), ()): 1}
    output = {0: states}
    for v in range(1, N+1):
        nxt = defaultdict(int)
        for (shape, first), count in states.items():
            for added, row in addable(shape):
                nxt[(added, first + (v,) if row == 0 else first)] += count
        states = dict(nxt)
        output[v] = states
    return output


def main():
    max_n = 8
    hist = {}
    tableaux = tableau_histories(max_n)
    receipts = []
    for n in range(1, max_n+1):
        direct = Counter(tops(p) for p in permutations(range(1,n+1)))
        by_tableau = Counter()
        shape_totals = Counter()
        for (shape, first), C in tableaux[n].items():
            shape_totals[shape] += C
            by_tableau[first] += C * hook_count(shape)
        assert direct == by_tableau
        assert sum(direct.values()) == factorial(n)
        for shape, count in shape_totals.items():
            assert count == hook_count(shape)
        hist[n] = direct
        receipts.append(dict(n=n, permutation_count=factorial(n),
                             row_patterns=len(direct), shapes=len(shape_totals),
                             exact_RSK_weighted_row_match=True,
                             exact_hook_dimension_match=True))
    compatibility_checks = 0
    for n, h in hist.items():
        for b, count in h.items():
            if b[-1] != n:
                continue
            k = len(b)
            mass = Fraction(count, factorial(n))
            for m in range(n, max_n+1):
                later = sum(v for row,v in hist[m].items() if row[:k] == b)
                assert mass == Fraction(later, factorial(m))
                compatibility_checks += 1
    b2 = []
    for n in range(2,max_n+1):
        computed = Fraction(hist[n][(1,n)], factorial(n))
        expected = Fraction(1,n*factorial(n-2))
        assert computed == expected
        b2.append(dict(b=n, numerator=computed.numerator,denominator=computed.denominator))
    tails=[]
    for n,h in hist.items():
        for k in range(2,6):
            numerator=sum(v for row,v in h.items() if len(row)<k)
            actual=Fraction(numerator,factorial(n))
            bound=Fraction((k-1)**(2*n),factorial(n))
            assert actual <= bound
            tails.append(dict(N=n,k=k,exact=str(actual),color_bound=str(bound)))
    examples=[]
    for n in range(3,7):
        for b,count in sorted(hist[n].items()):
            if len(b)==3 and b[-1]==n:
                examples.append(dict(b=list(b),permutation_count=count,mass=str(Fraction(count,factorial(n)))))
    result=dict(utc=datetime.now(timezone.utc).isoformat(),max_n=max_n,
                independent_of_campaign_code=True,checks=receipts,
                exact_compatibility_checks=compatibility_checks,
                second_rank_known_formula=b2,
                tail_checks=tails,three_rank_examples=examples,
                all_checks_passed=True)
    path=Path(__file__).with_name('COHERENT_RANK_CHECK.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['utc','max_n','exact_compatibility_checks','all_checks_passed']}))

if __name__ == '__main__':
    main()
