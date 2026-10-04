#!/usr/bin/env python3
"""Independent finite controls for the accompanying analytic audit.

The author's public files are read, never modified. This script works primarily
in exponential coordinates to check the matrix-coordinate lattice conversion.
Finite controls do not establish the complete length-space or uniform-limit claims.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
COUNTS = {}


def require(family, value):
    assert value, family
    COUNTS[family] = COUNTS.get(family, 0) + 1


def bch(g, h):
    v, x, y, z = g
    w, a, b, c = h
    return v+w, x+a, y+b, z+c+(x*b-y*a)/2


def exponential(g):
    v, x, y, z = g
    return v, x, y, z-x*y/2


def matrix(g):
    v, x, y, z = g
    return v, x, y, z+x*y/2


def shear(g, sign=-1):
    v, x, y, z = g
    return v, x, y, z+sign*v


def inverse(g):
    return tuple(-c for c in g)


def in_lattice(g):
    return all(c.denominator == 1 for c in matrix(g))


def reduce(g):
    v, x, y, z = matrix(g)
    m, a, b = int(v // 1), int(x // 1), int(y // 1)
    c = int((z-a*(y-b)) // 1)
    gamma = exponential(tuple(map(Q, (m, a, b, c))))
    return gamma, bch(inverse(gamma), g)


def run():
    inputs = list(product(map(Q, range(-2, 3)), repeat=4))
    for i, gm in enumerate(inputs):
        g = exponential(gm)
        h = exponential(inputs[(317*i+83) % len(inputs)])
        require('coordinate_round_trip', matrix(g) == gm)
        require('first_kind_lattice_closure', in_lattice(bch(g, h)))
        require('first_kind_lattice_inverse', in_lattice(inverse(g)))
        require('shear_preserves_lattice_both_ways', in_lattice(shear(g)) and in_lattice(shear(g, 1)))
        require('shear_is_bch_automorphism', shear(bch(g, h)) == bch(shear(g), shear(h)))
        require('shear_is_bijective', shear(shear(g), 1) == g)
        r = tuple(c / 3 for c in gm)
        gamma, remainder = reduce(exponential(r))
        require('fractional_fundamental_set', all(0 <= c <= 1 for c in matrix(remainder)) and all(c < 1 for c in matrix(remainder)))
        require('fractional_lattice_reconstruction', bch(gamma, remainder) == exponential(r) and in_lattice(gamma))

    # Check the group commutator: [exp(aX),exp(bY)] = exp(abZ).
    # Its four axis legs have L1 length 2|a|+2|b|. Equal sides
    # achieve exactly L^2=16|z|, consistent with the analytic lower bound.
    for a, b in product((Q(n, 3) for n in range(-9, 10)), repeat=2):
        X = (Q(0), a, Q(0), Q(0))
        Y = (Q(0), Q(0), b, Q(0))
        comm = bch(bch(bch(X, Y), inverse(X)), inverse(Y))
        require('commutator_normalization', comm == (0, 0, 0, a*b))
        perimeter = 2*abs(a)+2*abs(b)
        require('rectangle_area_bound', perimeter**2 >= 16*abs(a*b))
        if abs(a) == abs(b):
            require('square_sharpness', perimeter**2 == 16*abs(a*b))

    # Tangent directions for the second metric: F maps V+Z, X, Y
    # to V, X, Y and preserves the three control coefficients.
    for a, b, c in product(map(Q, range(-3, 4)), repeat=3):
        require('pullback_horizontal_basis', shear((a, b, c, a)) == (a, b, c, 0))

    # A tempting replacement, integer first-kind quadruples, is not a subgroup.
    X, Y = (Q(0), Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(1), Q(0))
    require('negative_control_integer_first_kind', bch(X, Y)[3] == Q(1, 2))

    return {
        'problem_id': 30000552,
        'result': 'PASS',
        'arithmetic': 'fractions.Fraction only',
        'counts': COUNTS,
        'total_assertions': sum(COUNTS.values()),
        'proof_sha256': hashlib.sha256((ROOT/'public'/'PROOF.md').read_bytes()).hexdigest(),
        'author_manifest_sha256': hashlib.sha256((ROOT/'public'/'SHA256SUMS').read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Finite algebra, normalization and lattice controls; the audit separately supplies analytic reasoning.'
    }


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
