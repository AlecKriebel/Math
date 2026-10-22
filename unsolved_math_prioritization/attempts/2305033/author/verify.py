#!/usr/bin/env python3
"""Finite exact controls; this does NOT verify the historical covering theorem."""
from fractions import Fraction as Q
import json


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])


def power(z, n):
    out = (Q(1), Q(0))
    for _ in range(n):
        out = mul(out, z)
    return out


def evaluate(coefficients, z):
    out = (Q(0), Q(0))
    for a in reversed(coefficients):
        out = add(mul(out, z), a)
    return out


def main():
    counts = {"affine_rotation_evaluation": 0,
              "positive_degree_translation_invariance": 0,
              "lacunary_finite_bloch_controls": 0,
              "lacunary_coefficient_controls": 0}
    coeff = [(Q(n+1, n+2), Q((-1)**n, n+3)) for n in range(13)]
    rotations = [(Q(1), Q(0)), (Q(0), Q(1)),
                 (Q(-1), Q(0)), (Q(0), Q(-1))]
    scales = [(Q(2, 3), Q(0)), (Q(0), Q(3, 2)), (Q(2), Q(-1))]
    shifts = [(Q(1), Q(2)), (Q(-3, 4), Q(0))]
    points = [(Q(1, 5), Q(1, 7)), (Q(-2, 5), Q(1, 3)), (Q(0), Q(0))]
    for u in rotations:
        for c in scales:
            unshifted = [mul(c, mul(power(u, n), a)) for n, a in enumerate(coeff)]
            for b in shifts:
                transformed = unshifted.copy()
                transformed[0] = add(transformed[0], b)
                assert transformed[1:] == unshifted[1:]
                counts["positive_degree_translation_invariance"] += 1
                for z in points:
                    left = evaluate(transformed, z)
                    right = add(b, mul(c, evaluate(coeff, mul(u, z))))
                    assert left == right
                    counts["affine_rotation_evaluation"] += 1
    for k in range(11):
        exponents = [2**j for j in range(k+1)]
        for r in (Q(1, 4), Q(1, 2), Q(3, 4), Q(9, 10)):
            derivative = sum((m*r**(m-1) for m in exponents), Q(0))
            assert (1-r*r)*derivative <= 8
            counts["lacunary_finite_bloch_controls"] += 1
        sparse = {n: 1 for n in exponents}
        assert sparse[2**k] == 1
        assert sparse.get(3, 0) == 0
        counts["lacunary_coefficient_controls"] += 2
    result = {
        "schema": "function-theory-2305033-exact-controls/v1",
        "arithmetic": "Python standard-library fractions.Fraction; no floats",
        "counts": counts,
        "total_checks": sum(counts.values()),
        "all_passed": True,
        "scope": "Finite algebra and finite lacunary-sum controls only. The infinite statements are justified by the written proofs.",
        "historical_covering_theorem_independently_proved": False,
        "new_solution_claimed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
