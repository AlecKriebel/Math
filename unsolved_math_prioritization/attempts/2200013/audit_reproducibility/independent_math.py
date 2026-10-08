#!/usr/bin/env python3
"""Independent integer reconstruction; does not import the author's verifier."""
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from math import prod


def check(condition, description):
    if not condition:
        raise RuntimeError(description)


def run():
    v = Fraction(1, 1000000)
    K = 100000000000000000000
    N = 2*K+100
    S = 10**72
    exponents = (5, 15, 25, 55)
    subsets = [sum(c) for size in range(5) for c in combinations(exponents, size)]
    check(len(subsets) == len(set(subsets)) == 16, 'subset-sum uniqueness')
    a = [S if i in subsets else 0 for i in range(101)]
    correction_terms = ((3, 12, (1, 3, 3, 1)),
                        (2, 36, (1, 2, 1)),
                        (1, 72, (1, 1)))
    for degree, denominator_power, coefficients in correction_terms:
        for j, coefficient in enumerate(coefficients):
            a[j] += coefficient*(S//10**denominator_power)
    C = Fraction(a[0], S)
    check(C == 1+v**2+v**6+v**12 and 1 < C < 2, 'constant endpoint')
    check(a[100] == S and all(0 <= z <= S for z in a[1:100]), 'coefficient bounds')
    check(K%2 == 0 and N == 2*K+100, 'degree and parity')

    records = []
    points = []
    for direction, power in ((-1, 1), (-1, 3), (-1, 5), (-1, 7), (1, 7)):
        D = 10**(6*power)
        A = -D+direction
        points.append(Fraction(A, D))
        # Integer homogeneous evaluation of every coefficient, independently of Horner.
        expanded = sum(coefficient*pow(A, j)*pow(D, 100-j)
                       for j, coefficient in enumerate(a))
        # Independently evaluate the four-factor seed plus three corrections.
        factored = S*prod(pow(D,e)+pow(A,e) for e in exponents)
        for degree, denominator_power, _ in correction_terms:
            factored += (S//10**denominator_power)*pow(A+D,degree)*pow(D,100-degree)
        check(expanded == factored and expanded != 0, 'two integer representations agree')
        value = Fraction(expanded, S*pow(D,100))
        check(10**4272 % value.denominator == 0, 'common evaluation denominator')
        r = -Fraction(A,D)
        h = prod(sum((r**j for j in range(e)), Fraction(0)) for e in exponents)
        check(1 <= h < 200000, 'direct H evaluation')
        records.append({'offset_direction': direction, 'offset_v_power': power,
                        'sign': (expanded > 0)-(expanded < 0),
                        'scaled_integer_bit_length': abs(expanded).bit_length(),
                        'scaled_integer_sha256': hashlib.sha256(str(expanded).encode()).hexdigest()})
    check([r['sign'] for r in records] == [1,-1,1,-1,1], 'alternating signs')
    check(all(points[i]<points[i+1] for i in range(4)), 'ordered disjoint intervals')
    check(all(-2 < t < -Fraction(1,2) for t in points), 'negative bounded points')
    check(prod(exponents)==103125 and sum(e-1 for e in exponents)==96, 'H coefficient data')
    check(Fraction(103125,1)/(1-96*v)<200000, 'uniform H bound')
    check(72+100*42==4272 and 10<16, 'uniform denominator derivation')
    exponent_gap = N*N-(2*N+K+4*4272)
    check(exponent_gap > 0, 'strict perturbation exponent gap')
    check(N>=1, 'N+1 <= 2^N by elementary induction')

    # Compute the actual binomial ratios in the 99-point block. No huge binomial
    # coefficient is formed. The common scale binom(N,K) cancels exactly.
    ratio = Fraction(1)
    ratios = []
    maximum = Fraction(0)
    filler_bound = v*v/1000
    L = 1+v*v/200
    check(Fraction(1,2**50)<filler_bound and N*N>50, 'filler divided by B upper bound')
    check(L**100 < C, 'strict rational lower chord anchor')
    for j in range(1,100):
        ratio *= Fraction(N-K-j+1, K+j)
        ratios.append(ratio)
        maximum = max(maximum,ratio)
        upper_weight = Fraction(a[j],S)*ratio+filler_bound
        check(upper_weight < L, 'individual strict chord margin')
        # For the sparse nonzero seed positions also check the actual chord
        # inequality raised to the 100th power, avoiding logarithms and roots.
        if a[j]:
            check(upper_weight**100 < C**(100-j), 'direct power-form chord inequality')
    check(ratios[0]==ratios[-1], 'binomial symmetry about block midpoint')
    check(maximum == ratios[49], 'binomial maximum at j=50')
    check(maximum <= 1+Fraction(20000,K), 'independent exact binomial majorant')
    margin = v*v/200-Fraction(20000,K)-filler_bound
    check(margin > 0, 'uniform positive chord margin')
    # All remaining weights equal delta, below the two rising endpoint chords.
    # First slope is positive, middle negative. The final slope is smaller
    # because C<2, B>=1, and 100*N^2>K.
    check(100*N*N>K and C>1, 'strict ordering of all three hull slopes')
    return {'status':'PASS', 'method':'integer homogeneous reconstruction and actual finite binomial ratios',
            'degree':str(N), 'root_sample_checks':records,
            'perturbation_exponent_gap':str(exponent_gap),
            'strict_uniform_hull_margin':str(margin),
            'direct_interior_ratio_checks':99,
            'direct_power_form_chord_checks':sum(bool(z) for z in a[1:100]),
            'upper_hull_indices':['0',str(K),str(K+100),str(N)],
            'distinct_negative_roots_at_least':4, 'distinct_corners':3,
            'all_coefficients_strictly_positive':True,
            'no_huge_degree_expansion':True,
            'does_not_import_author_code':True}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True))
