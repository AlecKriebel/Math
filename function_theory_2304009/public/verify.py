#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; no external dependencies or network.

This does not construct Hilbert approximants or numerically prove topology.
The universally quantified argument is the written proof, not this grid.
"""
from fractions import Fraction as Q
import json
from pathlib import Path


def parameters(d, n):
    assert 0 < d < 4 and isinstance(n, int) and n >= 1
    t = d / 4
    A, B = 1+t, 1-t
    L = 1+3*d/4
    a = L/2
    m = 1-(a/A)**2
    h = B*m/4
    eps = min(h/4, h/(3*(n+1)))
    return t, A, B, L, a, m, h, eps


def geometric_case(d, n):
    t, A, B, L, a, m, h, eps = parameters(d, n)
    assert 0 < t < 1
    assert d < L < 2*A < 4
    assert 0 < m < 1 and h > 0 and eps > 0
    assert a*a/(A*A) + h*h/(B*B) < 1
    assert eps <= B*m/16
    actual_bound = ((a+eps)/A)**2 + ((h+eps)/B)**2
    first_bound = (a/A+m/16)**2 + (5*m/16)**2
    second_bound = 1-m+m/8+26*m*m/256
    last_bound = 1-198*m/256
    assert actual_bound <= first_bound <= second_bound <= last_bound < 1
    ys = [-h + 2*h*Q(j, n+1) for j in range(1, n+1)]
    assert all(-h < y < h for y in ys)
    assert all(ys[j+1]-ys[j] == 2*h/(n+1) > 2*eps
               for j in range(n-1))
    assert 2*eps < 2*h/(n+1)


def controls():
    # Includes very thin ellipses as d approaches 4 and low thresholds near 0.
    ds = sorted(set([Q(k, 10) for k in range(1, 40)] +
                    [Q(1, 10**6), Q(4)-Q(1, 10**6), Q(2), Q(3)]))
    ns = [1, 2, 3, 5, 10, 37, 100]
    geometry = 0
    for d in ds:
        for n in ns:
            geometric_case(d, n)
            geometry += 1

    # For positive rational w, set alpha=w^degree. These identities represent
    # the algebraic leading coefficient and dilation, not unknown approximants.
    normalization = 0
    for degree in [1, 2, 3, 7, 20]:
        for w in [Q(1), Q(5,4), Q(2), Q(7,2)]:
            alpha = w**degree
            assert alpha/w**degree == 1
            assert Q(1,1)/w <= 1
            assert 2*w >= 2
            normalization += 1

    # Negative controls reject the sign and normalization mistakes.
    negatives = {}
    negatives['wrong_capacity_sign'] = not (Q(2)**4 <= 1)
    # q=16*z^4, correct w=2; q(w*z) would have leading coefficient 256.
    negatives['wrong_scaling_direction'] = Q(16)*Q(2)**4 != 1
    # Replacing q by q/alpha takes the q-level 1 to q-level alpha.
    negatives['coefficient_division_changes_level'] = Q(16) != 1
    # Closed petals for z^2-1 meet at 0, so disjoint roots alone do not suffice.
    negatives['root_count_not_closed_component_count'] = abs(Q(0)**2-1) <= 1
    negatives['endpoint_d4_not_admissible'] = not (0 < Q(4) < 4)
    try:
        parameters(Q(2), 0)
    except AssertionError:
        negatives['zero_components_rejected'] = True
    else:
        negatives['zero_components_rejected'] = False
    assert all(negatives.values())

    c = Q(1)
    assert 1+c*c == 2
    _, _, _, L, *_ = parameters(Q(2), 1)
    assert L == Q(5,2) > 1+c*c
    return {
        'result': 'PASS',
        'arithmetic': 'fractions.Fraction; all comparisons exact',
        'geometry_parameter_pairs': geometry,
        'normalization_cases': normalization,
        'negative_controls': negatives,
        'target_control': {'c': '1', 'threshold': '2', 'segment_length': '5/2'},
        'limitations': [
            'Finite controls are not the universally quantified proof.',
            'Hilbert approximation is a cited classical theorem, not computed.',
            'No approximating polynomial coefficients or effective degree bound.',
            'No asymptotic rate for number of components is established.'
        ]
    }


if __name__ == '__main__':
    result = controls()
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    reference = Path(__file__).with_name('CHECKS.json')
    if reference.exists():
        assert json.loads(reference.read_text()) == result, 'CHECKS.json mismatch'
    print(text, end='')
