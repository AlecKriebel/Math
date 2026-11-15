#!/usr/bin/env python3
"""Fresh exact arithmetic check; no dependencies and no imported old script.

This verifies the adjoint-trace identity for cyclic word 1121222 and the
candidate's integer witness. It does not verify geometry or integration.
Failures use exceptions rather than assert, including under python -O.
"""
import itertools
import json
from collections import Counter
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def cyclic(word):
    word = tuple(word)
    return min(word[i:] + word[:i] for i in range(len(word))) if word else ()


def grouped_expansion(word):
    answer = Counter()
    for mask in itertools.product((0, 1), repeat=len(word)):
        left = tuple(c for c, bit in zip(word, mask) if bit == 0)
        right = tuple(c for c, bit in zip(word, mask) if bit == 1)[::-1]
        # The two traces multiply, so their pair is unordered.
        key = tuple(sorted((cyclic(left), cyclic(right))))
        answer[key] += (-1) ** sum(mask)
    return {key: value for key, value in answer.items() if value}


def multiply(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def trace_word(word, matrices):
    P = identity(len(matrices[1]))
    for c in word:
        P = multiply(P, matrices[c])
    return trace(P)


def adjoint(A):
    n = len(A)
    result = [[0] * (n * n) for _ in range(n * n)]
    # Column a*n+b represents E_ab, and ad_A(E_ab)=A E_ab-E_ab A.
    for a in range(n):
        for b in range(n):
            for i in range(n):
                result[i * n + b][a * n + b] += A[i][a]
            for j in range(n):
                result[a * n + j][a * n + b] -= A[b][j]
    return result


def expand_numerically(word, matrices):
    return sum((-1) ** sum(mask)
               * trace_word(tuple(c for c, b in zip(word, mask) if not b), matrices)
               * trace_word(tuple(c for c, b in zip(word, mask) if b)[::-1], matrices)
               for mask in itertools.product((0, 1), repeat=len(word)))


def main():
    w = (1, 1, 2, 1, 2, 2, 2)
    expected = {
        tuple(sorted(((), cyclic((1, 1, 2, 1, 2, 2, 2))))): 1,
        tuple(sorted(((), cyclic((1, 1, 2, 2, 2, 1, 2))))): -1,
        tuple(sorted(((2,), cyclic((1, 1, 2, 2, 1, 2))))): 3,
        tuple(sorted(((2,), cyclic((1, 1, 2, 1, 2, 2))))): -3,
    }
    grouped = grouped_expansion(w)
    require(grouped == expected, '128-term grouping differs from printed formula')
    X = [[0, 1, 1, 1], [1, 0, 0, 0], [0, -1, 0, 0], [-1, -1, -1, 1]]
    Y = [[0, 0, -1, 1], [-1, -1, 1, 1], [-1, 0, 0, 0], [0, 0, -1, -1]]
    matrices = {1: X, 2: Y}
    traces = {''.join(map(str, u)): trace_word(u, matrices)
              for u in [(2,), w, (1, 1, 2, 2, 2, 1, 2),
                        (1, 1, 2, 2, 1, 2), (1, 1, 2, 1, 2, 2)]}
    require(traces == {'2': -2, '1121222': 38, '1122212': 20,
                       '112212': -12, '112122': -23}, 'trace witness mismatch')
    scalar = sum(coef * trace_word(a, matrices) * trace_word(b, matrices)
                 for (a, b), coef in grouped.items())
    direct_128 = expand_numerically(w, matrices)
    ad_matrices = {1: adjoint(X), 2: adjoint(Y)}
    direct_adjoint = trace_word(w, ad_matrices)
    reversed_adjoint = trace_word(w[::-1], ad_matrices)
    require(scalar == direct_128 == direct_adjoint == 6, 'independent channels disagree')
    require(reversed_adjoint == -6, 'odd-wheel reversal fails')
    for i in range(len(w)):
        require(trace_word(w[i:] + w[:i], ad_matrices) == 6, 'cyclic invariance fails')
    corrupt = dict(grouped)
    corrupt[tuple(sorted(((2,), cyclic((1, 1, 2, 2, 1, 2)))))] = 2
    require(corrupt != grouped_expansion(w), 'coefficient mutation escaped control')
    bad_value = sum(coef * trace_word(a, matrices) * trace_word(b, matrices)
                    for (a, b), coef in corrupt.items())
    require(bad_value != direct_adjoint, 'corrupted formula accidentally matches witness')
    report = {
        'word': ''.join(map(str, w)), 'term_count': 2 ** len(w),
        'grouped_nonzero_terms': [
            {'traces': [''.join(map(str, a)), ''.join(map(str, b))], 'coefficient': c}
            for (a, b), c in sorted(grouped.items())],
        'trace_values': traces, 'grouped_value': scalar,
        'ungrouped_128_value': direct_128, 'direct_16_by_16_adjoint_value': direct_adjoint,
        'reversed_direct_adjoint_value': reversed_adjoint,
        'antisymmetric_difference': direct_adjoint - reversed_adjoint,
        'coefficient_3_to_2_control_value': bad_value, 'all_checks_pass': True,
        'limit': 'Exact Lie weight certificate only; no link evaluation, deframing proof, or integration computation.'
    }
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
