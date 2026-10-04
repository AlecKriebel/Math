#!/usr/bin/env python3
"""Exact finite algebra controls only; no test here decides CW-structure existence."""
import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def determinant(a):
    a = [[Fraction(x) for x in row] for row in a]
    sign = 1
    result = Fraction(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        p = a[k][k]
        result *= p
        for i in range(k+1, len(a)):
            q = a[i][k] / p
            for j in range(k+1, len(a)):
                a[i][j] -= q * a[k][j]
            a[i][k] = 0
    result *= sign
    assert result.denominator == 1
    return result.numerator


def leibniz(a):
    result = 0
    for p in itertools.permutations(range(len(a))):
        term = (-1) ** sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))
        for i, j in enumerate(p):
            term *= a[i][j]
        result += term
    return result


def block_sum(a, b):
    return [row + [0]*len(b) for row in a] + [[0]*len(a) + row for row in b]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    edges = [(i, i+1) for i in range(6)] + [(2, 7)]
    e8 = [[2 if i == j else 0 for j in range(8)] for i in range(8)]
    for i, j in edges:
        e8[i][j] = e8[j][i] = -1
    e16 = block_sum(e8, e8)
    leading = [determinant([row[:k] for row in e8[:k]]) for k in range(1,9)]
    assert leading == [2,3,4,5,6,7,8,1]
    assert determinant(e8) == leibniz(e8) == 1
    assert determinant(e16) == 1
    assert all(determinant([row[:k] for row in e16[:k]]) > 0 for k in range(1,17))
    assert all(e8[i][j] == e8[j][i] for i in range(8) for j in range(8))
    assert all(e16[i][i] % 2 == 0 for i in range(16))
    # Exact parity formula: x^T Q x = sum Q_ii x_i^2 + 2 sum_{i<j} Q_ij x_i x_j.
    # With even diagonal this is even for every integer vector, not merely samples.
    for x in itertools.product((-1,0,1), repeat=8):
        value = sum(x[i]*e8[i][j]*x[j] for i in range(8) for j in range(8))
        assert value % 2 == 0
        assert value > 0 or not any(x)
    # Negative control: deleting the last E8 branch produces A7 plus A1, determinant 16.
    broken = [row[:] for row in e8]
    broken[2][7] = broken[7][2] = 0
    assert determinant(broken) == 16
    # Positive and boundary controls for elimination/sign and evenness.
    hyperbolic = [[0,1],[1,0]]
    assert determinant(hyperbolic) == -1
    assert determinant([[1]]) == 1 and 1 % 2 == 1
    assert determinant([[0]]) == 0
    assert determinant(block_sum(e16,hyperbolic)) == -1
    result = {
        'status':'pass',
        'E8_matrix':e8,
        'E8_leading_principal_minors':leading,
        'E8_determinant_two_independent_algorithms':1,
        'E8_plus_E8_determinant':1,
        'E8_signature_from_Sylvester_criterion':8,
        'E8_plus_E8_signature_from_Sylvester_criterion':16,
        'E8_KS_value_conditional_on_classification_formula':1,
        'E8_plus_E8_KS_value_conditional_on_classification_formula':0,
        'sampled_vectors':3**8,
        'negative_control_deleted_branch_determinant':16,
        'limits':[
            'Integer/Fraction arithmetic only; maximum matrix dimension 18.',
            'Leibniz comparison enumerates 8! permutations; positivity/parity sample covers only {-1,0,1}^8.',
            'Universal positivity follows separately from exact leading minors and Sylvester criterion; parity from the displayed algebraic formula.',
            'No CW attaching map, homeomorphism, manifold recognition, triangulation, or end computation is performed.',
            'Does not verify Freedman, Donaldson, smoothing theory, or any general CW-existence conclusion.'
        ]
    }
    data=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(data)
    else:
        print(data,end='')

if __name__ == '__main__':
    main()
