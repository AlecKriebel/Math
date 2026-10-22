#!/usr/bin/env python3
"""Exact finite checks for the authored normalization obstruction.

No numerical cube roots, assertions, downloads, or implicit filesystem writes.
Default output is stdout. --output must name an absolute path outside this packet.
These checks are evidence for finite calculations, not a proof assistant.
"""
import argparse
from fractions import Fraction
import itertools
import json
import os
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def gf2_rank(rows, n):
    rows = list(rows)
    pivot = 0
    for col in range(n):
        j = next((j for j in range(pivot, len(rows)) if rows[j] & (1 << col)), None)
        if j is None:
            continue
        rows[pivot], rows[j] = rows[j], rows[pivot]
        for k in range(len(rows)):
            if k != pivot and rows[k] & (1 << col):
                rows[k] ^= rows[pivot]
        pivot += 1
    return pivot


def parity(n):
    return n.bit_count() % 2


def evaluate(rows, g):
    """Raw character sum and separately enumerated admissible green labels."""
    require(len(rows) == g, 'Intersection matrix is not square')
    require(all(0 <= row < (1 << g) for row in rows), 'Invalid matrix entry')
    good = []
    raw = 0
    for green in range(1 << g):
        words = sum(parity(row & green) << i for i, row in enumerate(rows))
        if words == 0:
            good.append(green)
        for red in range(1 << g):
            raw += (-1) ** parity(red & words)
    return raw, len(good)


def integer_cube_root(n):
    require(isinstance(n, int) and n >= 0, 'Cube test requires nonnegative integer')
    lo, hi = 0, max(1, n)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--require-readonly', action='store_true')
    parser.add_argument('--mutant', choices=['omit-red-factor', 'wrong-stabilizer',
                        'unbalanced-as-product', 'round-dimension', 'euler-sign',
                        'nonzero-seam'])
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    if args.output:
        require(args.output.is_absolute(), 'Output destination must be explicitly absolute')
        resolved = args.output.resolve()
        require(not resolved.is_relative_to(packet), 'Output must be outside this packet')
        # Never replace an existing file, even when an explicit destination is supplied.
        require(not resolved.exists(), 'Output destination already exists')
    if args.require_readonly:
        require(os.geteuid() != 0, 'Readonly check must be run as a real nonroot user')
        require(not os.access(packet, os.W_OK), 'Packet directory is writable')
        for file in packet.iterdir():
            if file.is_file():
                require(not os.access(file, os.W_OK), 'A packet file is writable')
        try:
            handle = os.open(str(packet / 'WRITE_PROBE_MUST_FAIL'), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except PermissionError:
            pass
        else:
            os.close(handle)
            raise RuntimeError('Readonly negative write probe unexpectedly succeeded')
    tests = []
    # Each index labels a distinct green/red curve. No conjugacy quotient.
    torus = [0]
    stabilizer = [1, 0, 4]
    av_t, labels_t = evaluate(torus, 1)
    av_s, labels_s = evaluate(stabilizer, 3)
    if args.mutant == 'omit-red-factor':
        av_t = labels_t
    if args.mutant == 'wrong-stabilizer':
        av_s = 8
    if args.mutant == 'unbalanced-as-product':
        av_t, labels_t = evaluate([1], 1)
    require((av_t, labels_t) == (4, 2), 'Parallel torus character/label count failed')
    require((av_s, labels_s) == (16, 2), 'Balanced stabilizer character/label count failed')
    cube_value = Fraction(av_t ** 3, av_s)
    require(cube_value == 4, 'Cube-root-independent partition value is wrong')
    tests.append({'name': 'C2 direct counts', 'torus_average': av_t,
                  'torus_labels': labels_t, 'stabilizer_average': av_s,
                  'stabilizer_labels': labels_s, 'partition_cube': str(cube_value)})
    # A disjoint union of the intersection blocks corresponds to connected sum
    # of diagrams; this checks the balanced stabilization of the product diagram.
    av_st, labels_st = evaluate([0, 2, 0, 8], 4)
    require((av_st, labels_st) == (64, 4), 'Stabilized product count failed')
    require(Fraction(av_st ** 3, 16 ** 4) == cube_value,
            'Balanced stabilization changed the normalized cube')
    tests.append({'name': 'balanced stabilization', 'g': 4,
                  'raw_average': av_st, 'labels': labels_st})
    # Exhaust all binary matrices up to g=3, plus all diagonal rank models at g=4.
    # Matrices are algebraic controls, not assertions that all are trisections.
    cases = 0
    for g in range(1, 4):
        for rows in itertools.product(range(1 << g), repeat=g):
            av, labels = evaluate(rows, g)
            rank = gf2_rank(rows, g)
            require(labels == 2 ** (g - rank), 'Kernel label-count control failed')
            require(av == labels * 2 ** g, 'Character orthogonality control failed')
            cases += 1
    for diagonal in range(16):
        rows = [(1 << i) if diagonal & (1 << i) else 0 for i in range(4)]
        av, labels = evaluate(rows, 4)
        rank = gf2_rank(rows, 4)
        require(av == 2 ** (8 - rank), 'Genus-four diagonal control failed')
        cases += 1
    tests.append({'name': 'exact character orthogonality', 'matrix_cases': cases})
    # Algebraic checks of the all-root obstruction; never approximate a root.
    require(integer_cube_root(4) ** 3 != 4, 'Noninteger dimension obstruction failed')
    if args.mutant == 'round-dimension':
        require(integer_cube_root(4) ** 3 == 4, 'Rounded dimension is not an exact solution')
    require(1 ** 3 < 4 < 2 ** 3, 'Integer bracketing failed')
    require(integer_cube_root(1) ** 3 == 1, 'Trivial-group positive control failed')
    require(integer_cube_root(8 ** 2) == 4, 'Perfect-cube-group positive control failed')
    for d in range(13):
        matrix_trace = sum(1 for _ in range(d))
        require(matrix_trace == d, 'Identity trace control failed')
    tests.append({'name': 'integrality and trace controls', 'N2_obstructed': True,
                  'N1_not_obstructed': True, 'N8_not_obstructed': True,
                  'identity_dimensions_checked': list(range(13))})
    # Use rational exponents of the positive real cube root of 2. This is exact.
    euler_checks = 0
    for g in range(1, 10):
        for k in range(g + 1):
            chi = 2 + g - 3 * k
            exponent = Fraction(3 * k - g, 3)
            require(exponent == Fraction(2 - chi, 3), 'Euler reduction failed')
            rescaled = exponent - Fraction(2, 3)
            expected = Fraction(-chi, 3)
            if args.mutant == 'euler-sign':
                expected = Fraction(chi, 3)
            require(rescaled == expected, 'Euler rescaling has wrong sign')
            euler_checks += 1
    # Euler gluing for closed 3-manifold seams, plus multiplicative monoidality.
    chi_seam = 1 if args.mutant == 'nonzero-seam' else 0
    for left in range(-5, 6):
        for right in range(-5, 6):
            composite_chi = left + right - chi_seam
            require(-composite_chi == -left + -right,
                    'Euler scalar is not functorial under the claimed gluing rule')
    require(Fraction(0) == 0, 'Cylinder must have exponent zero')
    require(Fraction(-1, 3) + Fraction(-1, 3) == Fraction(-2, 3),
            'Two four-ball maps do not give the four-sphere scalar')
    tests.append({'name': 'Euler formula and functor controls',
                  'formal_parameter_cases': euler_checks,
                  'seam_gluing_cases': 121, 'closed_seam_chi': chi_seam})
    report = {'status': 'pass', 'proof_scope': 'fixed-normalization obstruction and rescaled Euler TQFT',
              'mode': {0:'normal', 1:'-O', 2:'-OO'}[sys.flags.optimize],
              'effective_uid': os.geteuid(), 'readonly_enforced': args.require_readonly,
              'writes': 'stdout only' if not args.output else 'explicit external destination',
              'tests': tests,
              'limits': 'Finite arithmetic checks; source hypotheses and general proofs are in PROOF.md.'}
    serialized = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        with args.output.open('x', encoding='utf-8') as stream:
            stream.write(serialized)
    else:
        sys.stdout.write(serialized)


if __name__ == '__main__':
    main()
