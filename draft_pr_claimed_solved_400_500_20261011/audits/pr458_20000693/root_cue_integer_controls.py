#!/usr/bin/env python3
"""Exact finite CUE controls only; no actual L-function moment assertion."""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    answer = Fraction(1)
    for k in range(len(a)):
        pivot = next((j for j in range(k, len(a)) if a[j][k]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            answer = -answer
        answer *= a[k][k]
        for j in range(k + 1, len(a)):
            factor = a[j][k] / a[k][k]
            for h in range(k, len(a)):
                a[j][h] -= factor * a[k][h]
    return answer


def toeplitz(m, n):
    # Fourier coefficients of |1-exp(i theta)|^(2m), m an integer.
    def coefficient(k):
        return (-1) ** abs(k) * math.comb(2 * m, m + k) if abs(k) <= m else 0
    return determinant([[coefficient(j - k) for k in range(n)] for j in range(n)])


def gamma_product(m, n):
    value = Fraction(1)
    for j in range(1, n + 1):
        value *= Fraction(math.factorial(j - 1) * math.factorial(j + 2 * m - 1),
                          math.factorial(j + m - 1) ** 2)
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wrong-claim', choices=['extra_gamma', 'independent_repetitions'])
    args = parser.parse_args()
    if args.wrong_claim:
        actual = toeplitz(2, 3)
        expected = gamma_product(2, 3)
        if args.wrong_claim == 'extra_gamma':
            expected *= math.factorial(4)
        else:
            expected = gamma_product(1, 3) ** 2
        require(actual == expected, 'FALSE_CUE_CLAIM:' + args.wrong_claim)
        return
    records = []
    for m in range(7):
        for n in range(1, 13):
            exact = toeplitz(m, n)
            require(exact == gamma_product(m, n), 'CUE identity mismatch')
            require(exact > 0, 'CUE positivity mismatch')
            records.append({'m': m, 'N': n, 'exact_numerator': exact.numerator,
                            'exact_denominator': exact.denominator})
    negatives = []
    for claim in ['extra_gamma', 'independent_repetitions']:
        run = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--wrong-claim', claim],
                             capture_output=True, text=True)
        require(run.returncode != 0 and 'FALSE_CUE_CLAIM:' + claim in run.stderr,
                'Wrong claim was accepted or failed for the wrong reason')
        negatives.append({'claim': claim, 'rejected': True, 'intended_diagnostic': True})
    print(json.dumps({'status': 'PASS', 'scope': 'Exact finite integer CUE normalization only; no L-function high-moment test',
                      'exact_cases': len(records), 'explicit_positivity_controls': len(records),
                      'actual_wrong_claim_subprocess_rejections': len(negatives),
                      'asymptotic_proved': False, 'records': records, 'negative_controls': negatives},
                     indent=2))


if __name__ == '__main__':
    main()
