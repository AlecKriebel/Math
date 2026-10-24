#!/usr/bin/env python3
"""Independent exact audit; no imports from the author's checker.

The main computations use 4x4 affine matrices over Fraction and generic
Gauss-Jordan inversion, rather than the author's two-coordinate formulas.
Finite computations supplement the review's all-degree proof.
"""
from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent
AUTHOR = ROOT.parent


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def product(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def inverse(a):
    n = len(a)
    augmented = [list(row) + unit for row, unit in zip(a, identity(n))]
    for column in range(n):
        pivot = next(row for row in range(column, n)
                     if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        leading = augmented[column][column]
        augmented[column] = [x / leading for x in augmented[column]]
        for row in range(n):
            if row != column:
                leading = augmented[row][column]
                augmented[row] = [x - leading * y for x, y in
                                  zip(augmented[row], augmented[column])]
    return [row[n:] for row in augmented]


def power(a, exponent):
    if exponent < 0:
        return power(inverse(a), -exponent)
    result = identity(len(a))
    while exponent:
        if exponent % 2:
            result = product(result, a)
        a = product(a, a)
        exponent //= 2
    return result


def translation(x, y, z):
    return [[Q(1), Q(0), Q(0), Q(x)],
            [Q(0), Q(1), Q(0), Q(y)],
            [-Q(y, 2), Q(x, 2), Q(1), Q(z)],
            [Q(0), Q(0), Q(0), Q(1)]]


T = [[Q(10), Q(3), Q(0), Q(0)],
     [Q(3), Q(1), Q(0), Q(0)],
     [Q(0), Q(0), Q(1), Q(0)],
     [Q(0), Q(0), Q(0), Q(1)]]
A = translation(1, 0, 0)
B_GENERATOR = translation(0, 1, 0)


def commutator(a, b):
    return product(product(product(inverse(a), inverse(b)), a), b)


def delta2(a, b, c, d):
    return commutator(commutator(a, b), commutator(c, d))


def central_coordinate(matrix):
    coefficient = matrix[2][3]
    assert matrix == translation(0, 0, coefficient)
    return coefficient


def reduce_q(x, modulus):
    return (x.numerator * pow(x.denominator, -1, modulus)) % modulus


def reduced(matrix, modulus):
    return [[reduce_q(x, modulus) for x in row] for row in matrix]


def mod_product(a, b, modulus):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) % modulus
             for j in range(len(b[0]))] for i in range(len(a))]


def mod_power(a, exponent, modulus):
    result = [[int(x) for x in row] for row in identity(len(a))]
    while exponent:
        if exponent % 2:
            result = mod_product(result, a, modulus)
        a = mod_product(a, a, modulus)
        exponent //= 2
    return result


def run():
    rng = random.Random(21122)
    heisenberg_checks = 0
    for _ in range(80):
        x, y, z, r, s, w = [rng.randrange(-20, 21) for _ in range(6)]
        assert product(translation(x, y, z), translation(r, s, w)) == \
            translation(x + r, y + s, Q(z + w) + Q(x * s - y * r, 2))
        assert commutator(translation(x, y, z), translation(r, s, w)) == \
            translation(0, 0, x * s - y * r)
        assert product(product(T, translation(x, y, z)), inverse(T)) == \
            translation(10 * x + 3 * y, 3 * x + y, z)
        heisenberg_checks += 3

    raw = [central_coordinate(delta2(A, power(T, n), B_GENERATOR, T))
           for n in range(66)]
    assert raw[:4] == [0, -9, -18, -108]
    assert all(x.denominator == 1 for x in raw)
    recurrence_checks = 0
    for n in range(64):
        assert raw[n + 2] + 9 == 11 * (raw[n + 1] + 9) - (raw[n] + 9)
        recurrence_checks += 1
    differences = raw[:]
    nonzero_witnesses = []
    for degree in range(1, 65):
        differences = [b - a for a, b in zip(differences, differences[1:])]
        assert differences[0] or differences[1]
        nonzero_witnesses.append([degree, str(differences[0]), str(differences[1])])

    # Check negative n independently: no one-sided action convention is hidden.
    inverse_slice_checks = 0
    for n in range(-9, 0):
        value = central_coordinate(delta2(A, power(T, n), B_GENERATOR, T))
        if n == -1:
            assert value == 90
        assert value.denominator == 1
        inverse_slice_checks += 1

    # Direct witnesses for the exact 9*Z_3 image, at all finite residues sampled.
    scaled_slice_checks = 0
    for u in range(-80, 81):
        value = central_coordinate(delta2(translation(u, 0, 0), T, B_GENERATOR, T))
        assert value == -9 * u
        scaled_slice_checks += 1

    quotient_levels = []
    for level in range(1, 10):
        modulus = 3 ** (level + 1)
        ti = reduced(T, modulus)
        assert mod_power(ti, 3 ** level, modulus) == reduced(identity(4), modulus)
        quotient_levels.append(level)

    compatible_action_checks = 0
    for level in range(1, 7):
        modulus = 3 ** level
        ti = reduced(T, modulus)
        for _ in range(40):
            u, lift = rng.randrange(modulus), rng.randrange(1, 7)
            assert mod_power(ti, u, modulus) == mod_power(ti, u + lift * modulus, modulus)
            compatible_action_checks += 1

    # Generic affine representatives from G. Every delta2 is central and in9R.
    general_word_checks = 0
    for _ in range(100):
        inputs = []
        for unused in range(4):
            x, y, z, u = [rng.randrange(-4, 5) for _ in range(4)]
            inputs.append(product(translation(x, y, z), power(T, u)))
        value = central_coordinate(delta2(*inputs))
        assert value.denominator == 1 and value.numerator % 9 == 0
        general_word_checks += 1

    author_hashes = {name: sha256((AUTHOR / name).read_bytes()).hexdigest()
                     for name in ['CENTRAL_NONPOLYNOMIAL.md',
                                  'check_central_countermodel.py',
                                  'central_countermodel_results.json']}
    return {
        'utc': datetime.now(timezone.utc).isoformat(),
        'result': 'PASS_INDEPENDENT_AFFINE_MATRIX_AUDIT',
        'review_completion_percent': 100,
        'author_hashes_at_check': author_hashes,
        'method': 'Generic 4x4 Fraction matrices and Gauss-Jordan inversion; no author imports',
        'heisenberg_and_action_checks': heisenberg_checks,
        'recurrence_checks': recurrence_checks,
        'finite_difference_degrees': [1, 64],
        'finite_difference_witnesses': nonzero_witnesses,
        'negative_exponent_slice_checks': inverse_slice_checks,
        'scaled_slice_checks': scaled_slice_checks,
        'finite_action_period_levels': quotient_levels,
        'compatible_action_checks': compatible_action_checks,
        'general_central_word_checks': general_word_checks,
        'first_slice_values': [str(x) for x in raw[:8]],
        'scope': 'Route obstruction only. Finite checks do not establish the all-degree claim; see independent review proof.',
    }


if __name__ == '__main__':
    receipt = run()
    (ROOT / 'independent_affine_results.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: value for key, value in receipt.items()
                      if key != 'finite_difference_witnesses'}, indent=2))
