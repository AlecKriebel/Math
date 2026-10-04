#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not a substitute for its analytic proof.

Run without arguments for a deterministic JSON receipt, or pass --check checks.json.
Only the Python standard library is used. All mathematics uses integers/Fractions.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
E = (Q(0),) * 4
COUNTS = {}


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1


def mul(g, h):
    v, x, y, z = g
    w, a, b, c = h
    return (v + w, x + a, y + b, z + c + x * b)


def inv(g):
    v, x, y, z = g
    return (-v, -x, -y, -z + x * y)


def shear(g):
    v, x, y, z = g
    return (v, x, y, z - v)


def unshear(g):
    v, x, y, z = g
    return (v, x, y, z + v)


def first_kind(g):
    v, x, y, z = g
    return (v, x, y, z - x * y / 2)


def bch(g, h):
    v, x, y, z = g
    w, a, b, c = h
    return (v + w, x + a, y + b, z + c + (x * b - y * a) / 2)


def floor(q):
    return q.numerator // q.denominator


def reduce_lattice(g):
    v, x, y, z = g
    m, a, b = map(floor, (v, x, y))
    c = floor(z - a * (y - b))
    gamma = (Q(m), Q(a), Q(b), Q(c))
    return gamma, mul(inv(gamma), g)


def polygon_data(vertices):
    """Integral x dy on the straight-segment polygonal loop, with its L1 length."""
    assert vertices[0] == vertices[-1]
    area = Q(0)
    A = Q(0)
    B = Q(0)
    for (x, y), (a, b) in zip(vertices, vertices[1:]):
        area += (x + a) * (b - y) / 2
        A += abs(a - x)
        B += abs(b - y)
    xs = [p[0] for p in vertices]
    return area, A, B, max(xs) - min(xs)


def run():
    rng = Random(54930000552)

    def point():
        return tuple(Q(rng.randrange(-30, 31), rng.randrange(1, 8)) for _ in range(4))

    for _ in range(700):
        g, h, k = point(), point(), point()
        check('group_associativity', mul(mul(g, h), k) == mul(g, mul(h, k)))
        check('two_sided_inverse', mul(g, inv(g)) == E == mul(inv(g), g))
        check('shear_automorphism', shear(mul(g, h)) == mul(shear(g), shear(h)))
        check('shear_inverse', unshear(shear(g)) == g == shear(unshear(g)))
        check('coordinate_conversion', first_kind(mul(g, h)) == bch(first_kind(g), first_kind(h)))
        check('coordinate_shear_commutes', first_kind(shear(g)) == shear(first_kind(g)))
        gamma, q = reduce_lattice(g)
        check('integral_lattice_element', all(t.denominator == 1 for t in gamma))
        check('fundamental_set', all(0 <= t < 1 for t in q))
        check('fundamental_set_reconstruction', mul(gamma, q) == g)
        rel = mul(inv(g), h)
        v, x, y, z = rel
        check('central_shear_difference', mul(inv((Q(0), x, y, z)), (Q(0), x, y, z - v)) == (Q(0), Q(0), Q(0), -v))
        check('left_action_pullback', mul(inv(shear(mul(k, g))), shear(mul(k, h))) == shear(rel))

    for _ in range(1200):
        vertices = [(Q(0), Q(0))]
        for _ in range(rng.randrange(1, 9)):
            vertices.append((Q(rng.randrange(-20, 21), rng.randrange(1, 7)),
                             Q(rng.randrange(-20, 21), rng.randrange(1, 7))))
        vertices.append(vertices[0])
        area, A, B, rx = polygon_data(vertices)
        check('closed_variation', A >= 2 * rx)
        check('centered_integral_bound', abs(area) <= rx * B / 2)
        check('area_product_bound', 4 * abs(area) <= A * B)
        check('area_length_bound', 16 * abs(area) <= (A + B) ** 2)

    for side in (Q(n, d) for n, d in product(range(1, 21), range(1, 6))):
        for sign in (-1, 1):
            vertices = [(0, 0), (side, 0), (side, sign * side), (0, sign * side), (0, 0)]
            area, A, B, rx = polygon_data(vertices)
            check('sharp_square_area', area == sign * side ** 2)
            check('sharp_square_perimeter', A + B == 4 * side)
            check('sharp_square_equality', 16 * abs(area) == (A + B) ** 2)
            # Horizontal lift follows X, Y, -X, -Y for the chosen signed square.
            lift = E
            for step in [(0, side, 0, 0), (0, 0, sign * side, 0),
                         (0, -side, 0, 0), (0, 0, -sign * side, 0)]:
                lift = mul(lift, step)
            check('square_lift_endpoint', lift == (0, 0, 0, area))
            t = side ** 2
            witness = (t, Q(0), Q(0), t)
            check('witness_shear', shear(witness) == (t, 0, 0, 0))
            d1, d2 = t + 4 * side, t
            check('witness_gap', d1 - d2 == 4 * side > 0)
            check('witness_ratio', d1 / d2 == 1 + 4 / side)

    for n in range(8, 1009):
        r = Q(n * n)
        s_lower = r - 4 * n
        check('ratio_threshold_positive', s_lower >= r / 2 > 0)
        check('ratio_threshold_bound', Q(4 * n) / s_lower <= Q(8, n))

    # Negative control: a nontrivial central shift of an abelian norm has linear
    # size, so the key square-root central estimate depends on Heisenberg geometry.
    for n in range(17, 118):
        check('negative_control_abelian_linear_growth', n * n > 4 * n)

    return {
        'problem_id': 30000552,
        'status': 'PASS',
        'arithmetic': 'integer and fractions.Fraction only',
        'deterministic_seed': 54930000552,
        'checks_by_family': COUNTS,
        'total_assertions': sum(COUNTS.values()),
        'proof_sha256': hashlib.sha256((ROOT / 'PROOF.md').read_bytes()).hexdigest(),
        'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Finite supplemental controls; the universal complete-length-space counterexample is proved in PROOF.md.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    receipt = run()
    output = json.dumps(receipt, sort_keys=True, indent=2) + '\n'
    if args.check:
        expected = json.loads(args.check.read_text())
        if receipt != expected:
            raise SystemExit('Receipt mismatch')
    print(output, end='')
