#!/usr/bin/env python3
"""Independent exact checks for the frozen rotation-domino construction.

Uses integer/Fraction arithmetic only. Universal claims are proved in REPORT.md;
this program supplies reproducible arithmetic and negative controls, not a
substitute for the all-real-height or all-period proof.
"""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import sys


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def sign_surd(a, b):
    """Sign of a+b*sqrt(2), with rational coefficients and no rounding."""
    a, b = Fraction(a), Fraction(b)
    if not b:
        return (a > 0) - (a < 0)
    if not a:
        return (b > 0) - (b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    delta = a * a - 2 * b * b
    if a > 0:
        return (delta > 0) - (delta < 0)
    return (delta < 0) - (delta > 0)


def valid_height(p, q):
    r = Fraction(p, q)
    return sign_surd(r, -1) > 0 and sign_surd(r - 1, -1) <= 0


def verify_competitor(n, m, claimed_least_period):
    require(isinstance(n, int) and n >= 1, "n must be a positive integer")
    require(m == isqrt(2 * n * n) + 1, "wrong prescribed ceiling numerator")
    require((m - 1) ** 2 < 2 * n * n < m * m,
            "integer enclosure of n*sqrt(2) failed")
    r = Fraction(m, n)
    require(sign_surd(r, -1) > 0, "competitor is at or below bottom")
    require(sign_surd(r - Fraction(1, n), -1) < 0,
            "competitor violates t_n < 1/n")
    require(valid_height(m, n), "competitor is outside [0,1]")
    q = r.denominator
    require(q == n // gcd(m, n), "denominator reduction mismatch")
    require(claimed_least_period == q, "claimed least period is wrong")
    require((q * r).denominator == 1, "claimed period does not close")
    # Exact analytic bound: t >= (2*sqrt(2)-1)/(7*q^2).
    require(sign_surd(r + Fraction(1, 7 * q * q),
                      -1 - Fraction(2, 7 * q * q)) >= 0,
            "universal least-period bound failed")
    return q


def tile_sequence(theta, rotation, count):
    theta, rotation = Fraction(theta), Fraction(rotation)
    points = [(theta + i * rotation) % 1 for i in range(count + 1)]
    return [(points[i], points[i + 1]) for i in range(count)]


def verify_tile_period(tiles, period):
    require(period >= 1, "period must be positive")
    require(len(tiles) >= 2 * period, "insufficient finite tile control")
    require(all(tiles[i][1] == tiles[i + 1][0]
                for i in range(len(tiles) - 1)), "illegal tile matching")
    require(all(tiles[i] == tiles[i + period]
                for i in range(len(tiles) - period)), "tile sequence is not periodic")


def expect_rejection(name, function):
    try:
        function()
    except CheckFailure as error:
        return {"name": name, "rejected": True, "reason": str(error)}
    raise CheckFailure("negative control incorrectly accepted: " + name)


def run_checks():
    # Exact arithmetic sanity, including near-cancellation and huge coefficients.
    require(sign_surd(0, 0) == 0, "zero sign")
    require(sign_surd(Fraction(3, 2), -1) == 1, "3/2 above sqrt(2)")
    require(sign_surd(Fraction(7, 5), -1) == -1, "7/5 below sqrt(2)")
    require(sign_surd(-Fraction(3, 2), 1) == -1, "negative symmetry")
    ns = list(range(1, 10001)) + [10 ** 30 + 1, 10 ** 60 + 7, 10 ** 120 + 3]
    periods = []
    repeated_denominators = 0
    for n in ns:
        m = isqrt(2 * n * n) + 1
        q = verify_competitor(n, m, n // gcd(m, n))
        periods.append(q)
        repeated_denominators += q < n

    # For all reduced rationals in the indicated finite control range, certify
    # least period by checking every smaller candidate and the analytic bound.
    rational_count = 0
    for q in range(1, 201):
        for p in range(q, 3 * q + 1):
            if gcd(p, q) != 1 or not valid_height(p, q):
                continue
            r = Fraction(p, q)
            require((q * r).denominator == 1, "rational period does not close")
            require(all((k * r).denominator != 1 for k in range(1, q)),
                    "least denominator is not least period")
            require(p * p - 2 * q * q >= 1, "norm integer not positive")
            require(sign_surd(r + Fraction(1, 7 * q * q),
                              -1 - Fraction(2, 7 * q * q)) >= 0,
                    "exact gap control failed")
            rational_count += 1

    # Tile and point periods in a finite rational-phase model are both exact.
    rotations = [Fraction(2), Fraction(3, 2), Fraction(5, 3), Fraction(17, 11)]
    for r in rotations:
        q = r.denominator
        tiles = tile_sequence(Fraction(7, 13), r, 3 * q)
        verify_tile_period(tiles, q)
        if q > 1:
            require(all(tiles[0] != tiles[p] for p in range(1, q)),
                    "tiles have an unexpected smaller period")

    # The source counts N+1 identical costs with denominator N.
    average_cases = 0
    for t in [Fraction(0), Fraction(1, 1000000), Fraction(1, 2), Fraction(1)]:
        c = 1 + t
        for n in [1, 2, 17, 10 ** 6]:
            a = (c + sum([c] * min(n, 17))) / n if n <= 17 else Fraction(n + 1, n) * c
            require(a == Fraction(n + 1, n) * c, "N+1/N average convention failed")
            require(a - c == c / n, "average boundary term failed")
            average_cases += 1

    bad_tiles = tile_sequence(Fraction(7, 13), Fraction(3, 2), 8)
    bad_tiles[3] = (bad_tiles[3][0], Fraction(1, 17))
    negatives = [
        expect_rejection("dropped_plus_one_creates_negative_height",
                         lambda: verify_competitor(4, isqrt(32), 2)),
        expect_rejection("incorrect_least_period_n_instead_of_reduced_denominator",
                         lambda: verify_competitor(4, 6, 4)),
        expect_rejection("zero_denominator_orbit_input",
                         lambda: verify_competitor(0, 1, 1)),
        expect_rejection("wrong_tile_period",
                         lambda: verify_tile_period(tile_sequence(Fraction(7, 13),
                                                                 Fraction(3, 2), 8), 1)),
        expect_rejection("tile_matching_corruption",
                         lambda: verify_tile_period(bad_tiles, 2)),
        expect_rejection("assertion_independent_rejection",
                         lambda: require(False, "explicit rejection remains active under -O")),
    ]
    return {
        "status": "PASS",
        "arithmetic": "exact integers and fractions; no floating point",
        "explicit_competitor_count": len(ns),
        "large_integer_n_digit_counts": [len(str(n)) for n in ns[-3:]],
        "cases_with_q_less_than_n": repeated_denominators,
        "finite_reduced_rational_count": rational_count,
        "finite_reduced_rational_denominator_bound": 200,
        "finite_tile_rotation_count": len(rotations),
        "source_average_control_cases": average_cases,
        "negative_controls": negatives,
        "limitations": [
            "Finite tests do not establish universal real-height or all-period claims.",
            "REPORT.md contains independent analytic and topological proofs of those claims.",
            "The rational-phase tile model does not numerically simulate irrational angles.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_checks()
    result.update({
        "reviewer": "/root/pr462_dynamical_adversary",
        "pr": 462,
        "problem_id": "30005528",
        "frozen_head": "3d5701d67e18745715d384c3db3fbee588b42a98",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "optimization_level": sys.flags.optimize,
        "python_executable": sys.executable,
        "python_version": sys.version,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    })
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "optimization_level": result["optimization_level"],
                      "explicit_competitor_count": result["explicit_competitor_count"],
                      "finite_reduced_rational_count": result["finite_reduced_rational_count"],
                      "negative_controls_rejected": len(result["negative_controls"])}))


if __name__ == "__main__":
    main()
