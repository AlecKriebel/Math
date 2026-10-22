#!/usr/bin/env python3
"""Exact finite checks supporting SOURCE_ONLY_RECONSTRUCTION.md.

No assert statements are used: optimized Python must retain all checks.
This checks finite obstructions and witnesses, not a bounded prime/clique search.
"""

import itertools
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def multiply(x, y):
    a, b = x
    c, d = y
    return (a * c + 10 * b * d, a * d + b * c)


def norm(x):
    a, b = x
    return a * a - 10 * b * b


def phi(x):
    return x[0] % 2


def divides_by_two(x):
    return all(coefficient % 2 == 0 for coefficient in x)


def main():
    squares5 = sorted({a * a % 5 for a in range(5)})
    require(squares5 == [0, 1, 4], "Incorrect square residues modulo 5")
    forbidden_targets = sorted({target % 5 for target in [-3, -2, 2, 3]})
    require(not (set(squares5) & set(forbidden_targets)),
            "Norm +/-2 or +/-3 obstruction failed")
    # This is the complete two-coordinate ring modulo 2, not a sample.
    residues2 = list(itertools.product(range(2), repeat=2))
    for x, y in itertools.product(residues2, repeat=2):
        added = tuple(a + b for a, b in zip(x, y))
        require(phi(added) == (phi(x) + phi(y)) % 2,
                "Quotient map failed additivity")
        require(phi(multiply(x, y)) == phi(x) * phi(y) % 2,
                "Quotient map failed multiplicativity")
    require({phi(x) for x in residues2} == {0, 1},
            "Quotient map is not surjective")
    sqrt10 = (0, 1)
    sqrt10_squared = multiply(sqrt10, sqrt10)
    require(sqrt10_squared == (10, 0), "Square-root multiplication failed")
    require(divides_by_two(sqrt10_squared), "2 must divide sqrt(10)^2")
    require(not divides_by_two(sqrt10), "2 must not divide sqrt(10)")
    require(norm((2, 0)) == 4, "Norm of 2 must be 4")
    require(norm((1, 0)) == 1, "Lower-bound clique witness must be a unit")
    # Justification for this denominator search is s^2 | 40, hence s <= 6.
    denominator_possibilities = [s for s in range(1, 7) if 40 % (s * s) == 0]
    require(denominator_possibilities == [1, 2],
            "Quadratic integral-element denominator reduction failed")
    # t^2 - 10u^2 == 0 modulo 4 forces t and u even.
    trace_coefficient_pairs = [
        [t, u] for t, u in itertools.product(range(4), repeat=2)
        if (t * t - 10 * u * u) % 4 == 0
    ]
    require(all(t % 2 == 0 and u % 2 == 0 for t, u in trace_coefficient_pairs),
            "Integral-element parity reduction failed")
    result = {
        "all_checks_passed": True,
        "square_residues_mod_5": squares5,
        "forbidden_norm_targets_mod_5": forbidden_targets,
        "complete_mod_2_ring_elements": len(residues2),
        "mod_2_addition_pairs_checked": len(residues2) ** 2,
        "mod_2_multiplication_pairs_checked": len(residues2) ** 2,
        "quotient_field_size": 2,
        "sqrt10_square_coordinates": list(sqrt10_squared),
        "two_divides_sqrt10_square": True,
        "two_divides_sqrt10": False,
        "norm_two": norm((2, 0)),
        "integral_denominator_possibilities": denominator_possibilities,
        "integral_trace_coefficient_pairs_mod_4": trace_coefficient_pairs,
        "scope": "exact finite obstructions and witnesses; full proofs are in the report",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
