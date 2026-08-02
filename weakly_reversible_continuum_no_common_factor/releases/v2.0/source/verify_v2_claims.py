#!/usr/bin/env python3
"""Replay and cross-check every computational claim added in the v2 draft.

This wrapper first checks the two rate tables, their family coordinates,
their displayed fields, affine and homogenized gcds, and the frozen
degree-fifteen mod-19 irreducibility certificate.  It then runs the frozen,
family, and strengthening verifiers.  All local calculations are exact.
"""

from __future__ import annotations

import csv
from functools import reduce
from pathlib import Path
import subprocess
import sys

import sympy as sp


draft_dir = Path(__file__).resolve().parent
project_dir = draft_dir.parent
repository_dir = project_dir.parent

x, y, z, w = sp.symbols("x y z w")
xyz = (x, y, z)

complexes = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 0, 3),
    (0, 1, 1),
    (0, 3, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1),
    (2, 1, 0),
    (3, 0, 0),
)
pairs = ((0, 1), (0, 4), (0, 6), (1, 7), (2, 4),
         (2, 7), (2, 9), (3, 4), (5, 9), (8, 9))
directed = tuple(edge for source, target in pairs
                 for edge in ((source, target), (target, source)))

expected_frozen_rates = (
    845740, 7732494, 702464, 3920, 437290, 4380128, 1405575, 5600,
    706384, 900816, 1518755, 6873328, 3920, 896896, 3863552, 3920,
    3863552, 15680, 4346496, 658560,
)
expected_clean_rates = (
    1160, 10296, 976, 23, 560, 5977, 1800, 25, 1629, 1237,
    1, 9152, 653, 1214, 5368, 1, 5368, 70, 6039, 915,
)


def read_rate_table():
    support = []
    frozen = []
    clean = []
    with (draft_dir / "rates.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for expected_index, row in enumerate(reader):
            assert int(row["index"]) == expected_index
            support.append((int(row["source_index"]), int(row["target_index"])))
            frozen.append(int(row["frozen_v1_rate"]))
            clean.append(int(row["clean_rate"]))
    assert tuple(support) == directed
    assert tuple(frozen) == expected_frozen_rates
    assert tuple(clean) == expected_clean_rates
    return tuple(frozen), tuple(clean)


def monomial(complex_index):
    return sp.prod(variable**power for variable, power
                   in zip(xyz, complexes[complex_index]))


def reconstruct_field(rates):
    result = [sp.Integer(0), sp.Integer(0), sp.Integer(0)]
    for rate, (source, target) in zip(rates, directed):
        for coordinate in range(3):
            result[coordinate] += (
                rate * monomial(source)
                * (complexes[target][coordinate] - complexes[source][coordinate])
            )
    return tuple(sp.expand(polynomial) for polynomial in result)


def family_vector(a, b, c, d):
    return (
        (62*d - 15*c)/48,
        33*(58*d - 45*c)/160,
        16*d/15,
        (c - b)/3,
        (154*d - 221*c)/224,
        (9856*d - 3315*c)/1470,
        45*(154*d - 221*c)/3136,
        5*c/14,
        (15*a + 16*d)/15,
        (62*d - 15*b - 15*c)/45,
        (154*d - 192*a - 221*c)/64,
        11*(58*d - 45*c)/60,
        a,
        2*(31*d - 15*c)/45,
        88*d/15,
        b,
        88*d/15,
        c,
        33*d/5,
        d,
    )


def exact_family_at(parameters):
    return tuple(sp.Rational(value) for value in family_vector(
        *(sp.Rational(parameter) for parameter in parameters)
    ))


def assert_affine_and_projective_gcd_one(field):
    primitive = [
        sp.Poly(polynomial, *xyz, domain=sp.QQ).primitive()[1]
        for polynomial in field
    ]
    assert reduce(sp.gcd, primitive).total_degree() == 0
    assert all(
        sp.gcd(primitive[first], primitive[second]).total_degree() == 0
        for first in range(3) for second in range(first + 1, 3)
    )
    homogenized = [polynomial.homogenize(w) for polynomial in primitive]
    assert reduce(sp.gcd, homogenized).total_degree() == 0


def powmod(base, exponent, modulus):
    result = sp.Poly(1, z, modulus=19)
    while exponent:
        if exponent & 1:
            result = (result * base).rem(modulus)
        base = (base * base).rem(modulus)
        exponent //= 2
    return result


def verify_frozen_mod19_certificate(frozen_field):
    D = (
        y**2 - y*z - y + sp.Rational(7, 16)*z**2
        - sp.Rational(1, 8)*z + sp.Rational(7, 16)
    )
    steady_basis = sp.groebner(frozen_field, x, y, z, order="lex", domain=sp.QQ)
    basis = tuple(polynomial.as_expr() for polynomial in steady_basis.polys)
    common = sp.gcd(sp.Poly(basis[1], *xyz), sp.Poly(basis[2], *xyz)).monic()
    assert sp.expand(common.as_expr() - D) == 0
    eliminant = sp.Poly(basis[2], *xyz).exquo(common).as_expr()
    assert eliminant.free_symbols <= {z} and sp.degree(eliminant, z) == 15
    rational_eliminant = sp.Poly(eliminant, z, domain=sp.QQ)
    _, integer_eliminant = rational_eliminant.clear_denoms(convert=True)
    integer_eliminant = sp.Poly(integer_eliminant, z, domain=sp.ZZ).primitive()[1]
    if integer_eliminant.LC() < 0:
        integer_eliminant = -integer_eliminant

    reduction = sp.Poly(integer_eliminant, z, modulus=19).monic()
    assert [int(coefficient) % 19 for coefficient in reduction.all_coeffs()] == [
        1, 10, 18, 2, 16, 9, 4, 7, 16, 11, 0, 16, 0, 3, 14, 12,
    ]
    coordinate = sp.Poly(z, z, modulus=19)
    for exponent_divisor in (3, 5):
        remainder = (powmod(coordinate, 19**exponent_divisor, reduction)
                     - coordinate).rem(reduction)
        assert sp.gcd(reduction, remainder).degree() == 0
    assert (powmod(coordinate, 19**15, reduction) - coordinate).rem(reduction).is_zero


def run_external_verifier(relative_path):
    subprocess.run(
        [sys.executable, str(project_dir / relative_path)],
        cwd=repository_dir,
        check=True,
    )


def main():
    frozen_rates, clean_rates = read_rate_table()
    assert all(rate > 0 for rate in (*frozen_rates, *clean_rates))
    assert exact_family_at((3920, 3920, 15680, 658560)) == frozen_rates
    assert exact_family_at((653, 1, 70, 915)) == clean_rates
    assert 154*915 - 192*653 - 221*70 == 64
    assert 70 - 1 == 69
    assert max(clean_rates) == 10296 and sum(clean_rates) == 52464
    assert reduce(sp.igcd, clean_rates) == 1

    frozen_field = reconstruct_field(frozen_rates)
    clean_field = reconstruct_field(clean_rates)
    assert_affine_and_projective_gcd_one(frozen_field)
    assert_affine_and_projective_gcd_one(clean_field)
    verify_frozen_mod19_certificate(frozen_field)

    run_external_verifier("verify_construction.py")
    run_external_verifier("family/verify_family.py")
    run_external_verifier("strengthening/clean_rates_stability_verifier.py")

    print("PASS: all exact v2 manuscript claims succeeded")
    print("  appendix rate tables and family coordinates agree")
    print("  both specializations have affine and homogenized gcd 1")
    print("  frozen degree-15 eliminant is irreducible modulo 19")
    print("  family, integer-optimality, radical, and Sturm checks passed")


if __name__ == "__main__":
    main()

