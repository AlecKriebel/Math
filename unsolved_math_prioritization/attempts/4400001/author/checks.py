#!/usr/bin/env python3
"""Exact finite controls; not a proof of the noncompact extension theorem."""
import itertools
import json

A = ((1, 1), (1, 1))
B = ((0, 1, 1), (1, 0, 1), (1, 1, 0))

def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))

def power(a, n):
    r = tuple(tuple(int(i == j) for j in range(len(a))) for i in range(len(a)))
    for _ in range(n):
        r = mul(r, a)
    return r

def trace(a):
    return sum(a[i][i] for i in range(len(a)))

def finite_counts(a, n):
    legal = closed = exact = examined = 0
    for w in itertools.product(range(len(a)), repeat=n):
        examined += 1
        if all(a[w[i]][w[i + 1]] for i in range(n - 1)):
            legal += 1
            if a[w[-1]][w[0]]:
                closed += 1
                if all(any(w[i] != w[(i + d) % n] for i in range(n))
                       for d in range(1, n) if n % d == 0):
                    exact += 1
    return legal, closed, exact, examined

def run():
    count = 0
    def check(condition, label):
        nonlocal count
        count += 1
        if not condition:
            raise AssertionError(label)
    check(power(B, 2) == ((2, 1, 1), (1, 2, 1), (1, 1, 2)), 'B squared')
    check(all(v == 2 for m in (A, B) for row in m for v in [sum(row)]), 'row sums')
    data = []
    examined = 0
    for n in range(1, 41):
        an, bn = power(A, n), power(B, n)
        check(trace(an) == 2**n, 'binary trace')
        check(trace(bn) == 2**n + 2 * (-1)**n, 'coloring trace')
        if n >= 2:
            check(all(v > 0 for row in bn for v in row), 'mixing powers')
    exact_counts = {'X': {}, 'Y': {}}
    for name, matrix in [('X', A), ('Y', B)]:
        for n in range(1, 41):
            e = trace(power(matrix, n)) - sum(exact_counts[name][d]
                    for d in range(1, n) if n % d == 0)
            exact_counts[name][n] = e
            check(e >= 0 and e % n == 0, 'least period orbit count')
        for n in range(1, 11):
            legal, closed, exact, work = finite_counts(matrix, n)
            examined += work
            wanted_legal = 2**n if name == 'X' else 3 * 2**(n - 1)
            check(legal == wanted_legal, 'brute legal words')
            check(closed == trace(power(matrix, n)), 'brute closed walks')
            check(exact == exact_counts[name][n], 'brute least period')
            data.append({'system': name, 'n': n, 'legal': legal,
                         'fixed_by_n': closed, 'least_period_n': exact})
    for name, matrix in [('X', A), ('Y', B)]:
        for p in itertools.permutations(range(len(matrix))):
            check(all(matrix[i][j] == matrix[p[i]][p[j]]
                      for i in range(len(matrix)) for j in range(len(matrix))),
                  'positive coordinate relabeling control')
    # Reject specific false deductions, not the actual extension theorem.
    negatives = {
        'equal_row_sums_do_not_imply_equal_fixed_point_counts': trace(A) != trace(B),
        'linear_legal_words_are_not_closed_walks': finite_counts(B, 3)[0] != trace(power(B, 3)),
        'period_dividing_two_is_not_least_period_two': trace(power(A, 2)) != exact_counts['X'][2],
        'proper_coloring_forbids_constant_points': trace(B) == 0,
        'removing_only_fixed_points_retains_period_two': exact_counts['X'][2] > 0,
        'loop_mutation_changes_the_target': trace(((1, 1, 1), (1, 0, 1), (1, 1, 0))) != trace(B)
    }
    for label, success in negatives.items():
        check(success, label)
    return {'status': 'pass', 'assertions': count,
            'brute_force_words_examined': examined,
            'matrix_power_range': [1, 40], 'brute_force_length_range': [1, 10],
            'negative_controls': negatives, 'tables': data,
            'scope': 'Finite algebraic and combinatorial checks only; no computational certification of Salo theorem.'}

if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
