#!/usr/bin/env python3
"""Review02: exact symbolic determinants and formal wheel contractions.

Uses only integers. Universal topology, 1T and integration are separate.
"""
import itertools
import json
from collections import Counter

ZERO = (0, 0, 0, 0, 0)


def require(x, message):
    if not x:
        raise RuntimeError(message)


def constant(c):
    return (c, ZERO)


def variable(i, power=1):
    e = list(ZERO)
    e[i] = power
    return (1, tuple(e))


def formal_det(matrix):
    answer = Counter()
    for perm in itertools.permutations(range(len(matrix))):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(len(perm))
                           for j in range(i + 1, len(perm)))
        coefficient, exponent = sign, ZERO
        for i, j in enumerate(perm):
            c, e = matrix[i][j]
            coefficient *= c
            exponent = tuple(a + b for a, b in zip(exponent, e))
        answer[exponent] += coefficient
    return {e: c for e, c in answer.items() if c}


def row(values):
    return [constant(x) if isinstance(x, int) else x for x in values]


def cyclic(w):
    return min(w[i:] + w[:i] for i in range(len(w))) if w else ''


def contraction(word, reverse_right=True):
    result = Counter()
    for selected in range(1 << len(word)):
        l = ''.join(word[i] for i in range(len(word)) if not (selected >> i) & 1)
        r = ''.join(word[i] for i in range(len(word)) if (selected >> i) & 1)
        if reverse_right:
            r = r[::-1]
        result[tuple(sorted((cyclic(l), cyclic(r))))] += (-1) ** selected.bit_count()
    return {k: v for k, v in result.items() if v}


def main():
    r, s, t, u, v = (variable(i) for i in range(5))
    matrix = [row([1, 0, 0, 0, 0, 0]), row([1, 1, 1, 0, 0, 0]),
              row([1, -1, 1, 0, 0, 0]), row([1, r, variable(0, 2), 0, 0, 1]),
              row([1, s, variable(1, 2), 1, 5, u]),
              row([1, t, variable(2, 2), 5, 1, v])]
    require(formal_det(matrix) == {ZERO: -48}, 'full symbolic six-row determinant')
    span = [row([1, 0, 0, 0]), row([1, 1, 1, 0]), row([1, -1, 1, 0]),
            row([1, t, variable(2, 2), 1])]
    require(formal_det(span) == {ZERO: 2}, 'full symbolic spanning determinant')
    require(formal_det([row([2, 0, 0]), row([0, 2, 0]), row([2, 2, -4])]) ==
            {ZERO: -16}, 'slice determinant')
    require(formal_det([row([1, 5]), row([5, 1])]) == {ZERO: -24}, 'component determinant')
    bad = [a[:] for a in matrix]
    bad[3][5] = constant(0)
    require(formal_det(bad) == {}, 'erasing rational plat must destroy rank')
    bad = [a[:] for a in matrix]
    bad[4][4] = bad[5][3] = constant(1)
    require(formal_det(bad) == {}, 'collapsing component values must destroy rank')
    wheel = contraction('1121222')
    expected = {('', cyclic('1121222')): 1, ('', cyclic('1122212')): -1,
                tuple(sorted(('2', cyclic('112212')))): 3,
                tuple(sorted(('2', cyclic('112122')))): -3}
    require(wheel == expected, '128 subset formal contraction grouping')
    reverse = contraction('2221211')
    require(reverse == {k: -v for k, v in wheel.items()}, 'formal odd-wheel reversal')
    require(contraction('1121222', False) != wheel, 'incorrect right factor order must fail')
    print(json.dumps({'passed': True, 'all_unknowns_symbolic': ['r', 's', 't', 'u', 'v'],
                      'six_rows': -48, 'span': 2, 'slice': -16, 'component_pair': -24,
                      'wheel_subset_count': 128, 'nonzero_contraction_groups': 4,
                      'formal_reversal_negates_all_groups': True,
                      'controls': ['erased plat', 'collapsed components', 'incorrect right order'],
                      'scope': 'Exact polynomial and trace-word arithmetic only.'}, indent=2))


if __name__ == '__main__':
    main()
