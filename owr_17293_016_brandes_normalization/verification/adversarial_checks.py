#!/usr/bin/env python3
"""Reproduce the additional independent exact spot checks from the code audit.

Python standard library only. These comparisons exercise implementation details;
they are not a proof of the universal basis-existence theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import random
import runpy
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def leibniz(matrix):
    """Independent determinant definition by signed permutation sum."""
    total = F(0)
    for permutation in itertools.permutations(range(len(matrix))):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(len(matrix))
                         for j in range(i + 1, len(matrix)))
        term = F((-1) ** inversions)
        for i, j in enumerate(permutation):
            term *= matrix[i][j]
        total += term
    return total


def main():
    sys.dont_write_bytecode = True
    verifier_path = Path(__file__).with_name('verify.py')
    verifier = runpy.run_path(str(verifier_path))
    rng = random.Random(17293016)
    determinant_checks = 0
    for n in range(1, 6):
        for case in range(100):
            matrix = [[F(rng.randint(-4, 4), rng.randint(1, 4))
                       for _ in range(n)] for _ in range(n)]
            if n > 1 and case % 7 == 0:
                matrix[-1] = matrix[0][:]
            require(verifier['determinant'](matrix) == leibniz(matrix),
                    f'determinant mismatch: dimension={n}, case={case}')
            determinant_checks += 1

    polarization_checks = 0
    for m, d in ((1, 2), (2, 2), (2, 4), (3, 4)):
        classes = list(verifier['compositions'](d, m))
        for case in range(5):
            polynomial = {alpha: F(rng.randint(-4, 4)) for alpha in classes}
            vectors = [[F(rng.randint(-3, 3)) for _ in range(m)]
                       for _ in range(d)]
            # Count tuple multiplicities directly; do not reuse multinomial().
            counts = {alpha: 0 for alpha in classes}
            for index in itertools.product(range(m), repeat=d):
                alpha = tuple(index.count(i) for i in range(m))
                counts[alpha] += 1
            direct = F(0)
            for index in itertools.product(range(m), repeat=d):
                alpha = tuple(index.count(i) for i in range(m))
                term = polynomial[alpha] / counts[alpha]
                for r, i in enumerate(index):
                    term *= vectors[r][i]
                direct += term
            require(verifier['polarization'](polynomial, vectors) == direct,
                    f'polarization mismatch: dimension={m}, degree={d}, case={case}')
            polarization_checks += 1

    print(json.dumps({
        'status': 'PASS',
        'scope': 'independent exact finite spot checks, not a theorem proof',
        'random_seed': 17293016,
        'independent_determinant_comparisons': determinant_checks,
        'independent_polarization_comparisons': polarization_checks,
        'verifier_sha256': hashlib.sha256(verifier_path.read_bytes()).hexdigest()
    }, indent=2))


if __name__ == '__main__':
    main()
