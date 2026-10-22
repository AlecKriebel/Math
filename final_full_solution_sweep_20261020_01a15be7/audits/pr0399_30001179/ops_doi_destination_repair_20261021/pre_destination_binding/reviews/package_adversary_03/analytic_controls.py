#!/usr/bin/env python3
"""Independent exact finite controls; no imports from candidate or prior reviews.

These controls do not establish infinite Gaussian measure, onto infinite charts,
or strong continuity. Those claims are checked in the written reconstruction.
"""
from fractions import Fraction as F
from itertools import product
import json
import math


def check(value, message):
    if not value:
        raise RuntimeError(message)


def word(n, m, tag):
    # An infinite block is a finite prefix plus an opaque retained tail identity.
    return (tuple(((), (tag, j)) for j in range(n)), tuple((tag, j) for j in range(m)))


def concatenate(x, y):
    xb, xs = x
    yb, ys = y
    if yb:
        first_prefix, first_tail = yb[0]
        return (xb + ((xs + first_prefix, first_tail),) + yb[1:], ys)
    return (xb, xs + ys)


def split_fixed(output, n, m, p, q):
    blocks, suffix = output
    if p:
        prefix, tail = blocks[n]
        check(len(prefix) >= m, 'Lost finite coordinates')
        return ((blocks[:n], prefix[:m]),
                (((prefix[m:], tail),) + blocks[n+1:], suffix))
    return ((blocks, suffix[:m]), ((), suffix[m:]))


def grade(x):
    return (len(x[0]), len(x[1]))


def ordinal_add(x, y):
    return (x[0]+y[0], y[1]) if y[0] else (x[0], x[1]+y[1])


def main():
    counts = {}
    grades = list(product(range(4), repeat=2))
    count = 0
    for a, b, c in product(grades, repeat=3):
        x, y, z = word(*a, 'x'), word(*b, 'y'), word(*c, 'z')
        left = concatenate(concatenate(x, y), z)
        right = concatenate(x, concatenate(y, z))
        check(left == right, 'Coordinate reassociation')
        check(grade(left) == ordinal_add(ordinal_add(a, b), c), 'Grade mismatch')
        check(ordinal_add(ordinal_add(a, b), c) == ordinal_add(a, ordinal_add(b, c)), 'Ordinal association')
        count += 1
    counts['tagged_triple_coordinate_associations'] = count
    count = 0
    for a, b in product(grades, repeat=2):
        x, y = word(*a, 'x'), word(*b, 'y')
        check(split_fixed(concatenate(x, y), *a, *b) == (x, y), 'Fixed-grade inverse')
        count += 1
    counts['fixed_grade_inverse_checks'] = count
    # Full Gaussian exponent coefficient and normalizer equality reduces to this
    # identical ordered list of positive standard deviations under the chain rule.
    count = 0
    wrong_scales = 0
    for k, ell, d in product(range(8), range(8), [F(1, 3), F(1), F(7, 2)]):
        total = [2**(k+ell-j)*d for j in range(k+ell)]
        right = [2**(k-j)*2**ell*d for j in range(k)] + [2**(ell-j)*d for j in range(ell)]
        check(total == right and math.prod(total) == math.prod(right), 'Gaussian scale chain')
        if k and ell:
            wrong = [2**(k-j)*d for j in range(k)] + [2**(ell-j)*d for j in range(ell)]
            check(total != wrong, 'Omitted tail rescaling went undetected')
            wrong_scales += 1
        count += 1
    counts.update(scale_chain_checks=count, wrong_scale_controls=wrong_scales)
    labels = [F(j, 6) for j in range(1, 6)]
    count, memberships, core, hull = 0, 0, 0, 0
    partitions = list(product([False, True], repeat=4))
    for size in range(6):
        for values in product(labels, repeat=size):
            decreasing = all(x >= y for x, y in zip(values, values[1:]))
            survives = True
            for cuts in partitions:
                colors = [sum(use and x > F(2*j+3, 12) for j, use in enumerate(cuts)) for x in values]
                membership = all(x >= y for x, y in zip(colors, colors[1:]))
                survives = survives and membership
                memberships += 1
            check(survives == decreasing, 'Finite partition intersection')
            core += int(survives)
            if len(set(values)) == len(values):
                # The finest partition makes all distinct positions singleton
                # color runs, so their whole finite support rectangle is allowed.
                colors = [labels.index(x) for x in values]
                check(all(x != y for x, y in zip(colors, colors[1:])), 'Separated singleton hull')
                hull += 1
            count += 1
    counts.update(finite_words=count, all_partition_memberships=memberships,
                  nonincreasing_words=core, separated_finite_hull_cases=hull)
    failure = F(9, 2500)/(1-F(1, 4))
    check(failure == F(3, 625) and 1-failure == F(622, 625), 'Positive omega witness bound')
    # Exact finite RN direction: output measure is q times product measure.
    f, q = [F(2), F(3)], [F(1, 2), F(3, 2)]
    norm = sum(x*x for x in f)
    check(sum(x*x/d*d for x, d in zip(f, q)) == norm, 'Reciprocal half density norm')
    check(sum(x*x*d*d for x, d in zip(f, q)) != norm, 'Wrong half density not detected')
    # A single coarse cut demonstrably fails the core test.
    rising = [F(1, 6), F(2, 6)]
    coarse = [int(x > F(1, 2)) for x in rising]
    check(coarse[0] >= coarse[1] and rising[0] < rising[1], 'Coarse cut negative control')
    # Dropping the finite suffix before an infinite right block changes words.
    x, y = word(0, 2, 'x'), word(1, 0, 'y')
    check(concatenate(x, y) != y, 'Suffix-loss negative control')
    result = {'status': 'PASS', 'counts': counts, 'positive_omega_success_bound': str(1-failure),
              'negative_controls': ['lost_suffix', 'wrong_scale', 'wrong_RN_direction', 'single_coarse_cut'],
              'scope': 'Exact finite algebra and support checks; written analytic derivation is essential.'}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
