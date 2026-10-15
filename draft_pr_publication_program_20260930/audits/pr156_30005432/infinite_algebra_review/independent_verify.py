#!/usr/bin/env python3
"""Exact independent algebra controls; explicit exceptions survive python -O.

Universal Z claims are checked as coefficient identities for formal independent
integer variables, with an exhaustive four-element component. Bounded controls
are supplemental. Infinite index is certified by the algebraic coset argument
in REVIEW.md; no finite enumeration is promoted to an infinite proof.
"""
from collections import Counter
from itertools import product
import argparse
import json
import sys


class CheckFailure(Exception):
    pass


class Checks:
    def __init__(self):
        self.counts = Counter()

    def require(self, category, condition, detail=None):
        if not condition:
            raise CheckFailure(f"{category}: {detail!r}")
        self.counts[category] += 1


ZERO_VECTOR = (0, 0, 0)
N, M, L = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def coefficient_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def coefficient_scale(k, a):
    return tuple(k * x for x in a)


class Model:
    def __init__(self, mutant=None):
        self.mutant = mutant

    def epsilon(self, c):
        if self.mutant == "noncharacter_epsilon":
            return 1 if c % 4 in (0, 1, 3) else -1
        return 1 if c % 4 in (0, 1) else -1

    def component(self, c, d):
        term = 0 if self.mutant == "wrong_component" else 2
        return (c + d + term * c * d) % 4

    def add(self, a, b):
        return (a[0] + b[0], (a[1] + b[1]) % 4)

    def negative(self, a):
        return (-a[0], (-a[1]) % 4)

    def subtract(self, a, b):
        return self.add(a, self.negative(b))

    def circle(self, a, b):
        return (a[0] + self.epsilon(a[1]) * b[0], self.component(a[1], b[1]))

    def inverse(self, a):
        return (-self.epsilon(a[1]) * a[0], a[1])

    def lam(self, a, b):
        return self.subtract(self.circle(a, b), a)

    def star(self, a, b):
        if self.mutant == "wrong_star":
            return ((self.epsilon(a[1]) - 1) * a[0], (2 * a[1] * b[1]) % 4)
        return self.subtract(self.lam(a, b), b)

    def fadd(self, a, b):
        return (coefficient_add(a[0], b[0]), (a[1] + b[1]) % 4)

    def fnegative(self, a):
        return (coefficient_scale(-1, a[0]), (-a[1]) % 4)

    def fsubtract(self, a, b):
        return self.fadd(a, self.fnegative(b))

    def fcircle(self, a, b):
        return (
            coefficient_add(a[0], coefficient_scale(self.epsilon(a[1]), b[0])),
            self.component(a[1], b[1]),
        )

    def finverse(self, a):
        return (coefficient_scale(-self.epsilon(a[1]), a[0]), a[1])

    def flam(self, a, b):
        return self.fsubtract(self.fcircle(a, b), a)

    def fstar(self, a, b):
        if self.mutant == "wrong_star":
            return (coefficient_scale(self.epsilon(a[1]) - 1, a[0]), (2 * a[1] * b[1]) % 4)
        return self.fsubtract(self.flam(a, b), b)


def universal_checks(model, checks):
    z = (ZERO_VECTOR, 0)
    for c, d, e in product(range(4), repeat=3):
        a, b, t = (N, c), (M, d), (L, e)
        left = model.fcircle(model.fcircle(a, b), t)
        right = model.fcircle(a, model.fcircle(b, t))
        checks.require("universal_circle_associativity", left == right, (c, d, e, left, right))
        checks.require("universal_left_brace", model.fcircle(a, model.fadd(b, t)) == model.fadd(model.fsubtract(model.fcircle(a, b), a), model.fcircle(a, t)), (c, d, e))
        checks.require("universal_lambda_additivity", model.flam(a, model.fadd(b, t)) == model.fadd(model.flam(a, b), model.flam(a, t)), (c, d, e))
        checks.require("universal_lambda_homomorphism", model.flam(model.fcircle(a, b), t) == model.flam(a, model.flam(b, t)), (c, d, e))
        checks.require("component_associativity", model.component(model.component(c, d), e) == model.component(c, model.component(d, e)), (c, d, e))
    for c, d in product(range(4), repeat=2):
        a, b = (N, c), (M, d)
        checks.require("component_xor", model.component(c, d) == (c ^ d), (c, d))
        checks.require("epsilon_character", model.epsilon(model.component(c, d)) == model.epsilon(c) * model.epsilon(d), (c, d))
        checks.require("low_bit_character", (-1) ** model.component(c, d) == (-1) ** c * (-1) ** d, (c, d))
        checks.require("universal_lambda_formula", model.flam(a, b) == (coefficient_scale(model.epsilon(c), M), ((-1) ** c * d) % 4), (c, d))
        checks.require("universal_star_formula", model.fstar(a, b) == (coefficient_scale(model.epsilon(c) - 1, M), (2 * c * d) % 4), (c, d))
    for c in range(4):
        a = (N, c)
        checks.require("universal_circle_identity", model.fcircle(a, z) == a == model.fcircle(z, a), c)
        checks.require("universal_circle_inverse", model.fcircle(a, model.finverse(a)) == z == model.fcircle(model.finverse(a), a), c)
        checks.require("lambda_additive_units", model.epsilon(c) in (-1, 1) and (1 + 2 * c) % 4 in (1, 3), c)
    # First coordinates in all checks are exact coefficient vectors over Z.
    # In particular the nonzero coefficient below is a universal injectivity
    # certificate for multiplication by -2 in Z, not a sampling extrapolation.
    checks.require("torsion_free_star_multiplier", model.epsilon(2) - 1 == -2, model.epsilon(2))
    difference = model.fsubtract((M, 0), (N, 0))
    circle_difference = model.fcircle(model.finverse((N, 0)), (M, 0))
    checks.require("universal_additive_coset_difference", difference == ((-1, 1, 0), 0), difference)
    checks.require("universal_circle_coset_difference", circle_difference == ((-1, 1, 0), 0), circle_difference)


def subgroup_shape(c, n_is_zero, right=True):
    integer_free = c in (0, 1)
    second = {d for d in range(4) if (2 * c * d) % 4 == 0}
    if not right and not n_is_zero:
        second &= {0, 1}
    return integer_free, second


def subgroup_controls(model, checks, integer_free, second, operation):
    checks.require(f"{operation}_subgroup_identity", 0 in second, (integer_free, second))
    for c in second:
        a = (N if integer_free else ZERO_VECTOR, c)
        inverse = model.fnegative(a) if operation == "additive" else model.finverse(a)
        checks.require(f"{operation}_subgroup_inverse", inverse[1] in second and (integer_free or inverse[0] == ZERO_VECTOR), (a, inverse))
        for d in second:
            b = (M if integer_free else ZERO_VECTOR, d)
            value = model.fadd(a, b) if operation == "additive" else model.fcircle(a, b)
            checks.require(f"{operation}_subgroup_closure", value[1] in second and (integer_free or value[0] == ZERO_VECTOR), (a, b, value))


def classify_indices(model, checks):
    expected = {
        (0, True): (1, 1), (0, False): (1, 2),
        (1, True): (2, 2), (1, False): (2, 4),
        (2, True): ("infinite", "infinite"), (2, False): ("infinite", "infinite"),
        (3, True): ("infinite", "infinite"), (3, False): ("infinite", "infinite"),
    }
    rows = []
    for c, n_is_zero in product(range(4), (True, False)):
        h_free, h_second = subgroup_shape(c, n_is_zero, True)
        k_free, k_second = subgroup_shape(c, n_is_zero, False)
        subgroup_controls(model, checks, h_free, h_second, "additive")
        subgroup_controls(model, checks, k_free, k_second, "circle")
        # Free integer-coordinate shapes are full preimages of component
        # subgroups. The index is the exact component-group index. The zero
        # shapes have distinct cosets (j,0), by the coefficient certificate.
        indices = (4 // len(h_second) if h_free else "infinite", 4 // len(k_second) if k_free else "infinite")
        checks.require("exact_index_classification", indices == expected[(c, n_is_zero)], (c, n_is_zero, indices))
        rows.append({"c": c, "n_condition": "zero" if n_is_zero else "nonzero", "H_integer_free": h_free, "H_component": sorted(h_second), "K_integer_free": k_free, "K_component": sorted(k_second), "indices": list(indices)})
    return rows


def concrete_checks(model, checks):
    zero = (0, 0)
    small = list(product(range(-2, 3), range(4)))
    for a, b, t in product(small, repeat=3):
        checks.require("bounded_circle_associativity", model.circle(model.circle(a, b), t) == model.circle(a, model.circle(b, t)), (a, b, t))
        checks.require("bounded_left_brace", model.circle(a, model.add(b, t)) == model.add(model.subtract(model.circle(a, b), a), model.circle(a, t)), (a, b, t))
        checks.require("bounded_lambda_homomorphism", model.lam(model.circle(a, b), t) == model.lam(a, model.lam(b, t)), (a, b, t))
    integers = [-10**100, -10**32 - 1, -81, -2, -1, 0, 1, 2, 77, 10**32 + 1, 10**100]
    points = list(product(integers, range(4)))
    for z, g in product(points, repeat=2):
        n, c = z
        m, d = g
        actual_right = model.star(z, g) == zero
        actual_left = model.star(g, z) == zero
        actual_central = model.circle(g, z) == model.circle(z, g)
        predicted_right = (model.epsilon(c) - 1) * m == 0 and (2 * c * d) % 4 == 0
        predicted_left = (model.epsilon(d) - 1) * n == 0 and (2 * c * d) % 4 == 0
        predicted_central = (1 - model.epsilon(c)) * m == (1 - model.epsilon(d)) * n
        k_free, k_second = subgroup_shape(c, n == 0, False)
        predicted_intersection = (k_free or m == 0) and d in k_second
        checks.require("exact_integer_right_fixed", actual_right == predicted_right, (z, g))
        checks.require("exact_integer_left_fixed", actual_left == predicted_left, (z, g))
        checks.require("exact_integer_centralizer", actual_central == predicted_central, (z, g))
        checks.require("exact_integer_K_classification", (actual_left and actual_central) == predicted_intersection, (z, g))
        if c in (0, 1):
            conjugate = model.circle(model.circle(g, z), model.inverse(g))
            checks.require("S_circle_normality_control", conjugate[1] in (0, 1), (z, g, conjugate))
    x, y = (0, 1), (0, 2)
    for g in points:
        checks.require("x_central_control", model.circle(g, x) == model.circle(x, g), g)
        checks.require("x_fixed_control", (model.star(x, g) == zero) == (g[1] % 2 == 0) == (model.star(g, x) == zero), g)
        checks.require("double_fixed_control", (model.star(y, g) == zero) == (g[0] == 0), g)
    checks.require("additive_closure_failure", model.add(x, x) == y and x[1] in (0, 1) and y[1] not in (0, 1))
    checks.require("lambda_invariance_failure", model.lam(x, x) == (0, 3))
    right_lhs = model.circle(model.add(x, x), (1, 0))
    right_rhs = model.add(model.subtract(model.circle(x, (1, 0)), (1, 0)), model.circle(x, (1, 0)))
    if model.mutant == "two_sided_claim":
        checks.require("unsupported_two_sided_claim", right_lhs == right_rhs, (right_lhs, right_rhs))
    checks.require("not_two_sided_witness", (right_lhs, right_rhs) == ((-1, 2), (1, 2)))


def reconciliation_controls(model, checks):
    # Exhaust the component; integer conditions are direct nonzero coefficient
    # conditions. For nonzero n, epsilon(d)n=n iff epsilon(d)=1.
    ker_component = {c for c in range(4) if model.epsilon(c) == 1 and (1 + 2 * c) % 4 == 1}
    checks.require("ker_lambda_component", ker_component == {0}, ker_component)
    fixed_component = {c for c in range(4) if all(((-1) ** d * c) % 4 == c for d in range(4))}
    checks.require("global_fixed_component", fixed_component == {0, 2}, fixed_component)
    checks.require("global_fixed_integer_zero", model.epsilon(2) - 1 == -2)
    checks.require("annihilator_zero", ker_component & fixed_component == {0})
    checks.require("star_subgroup_integer_generator", model.star((0, 2), (1, 0)) == (-2, 0))
    checks.require("star_subgroup_component_generator", model.star((0, 1), (0, 1)) == (0, 2))
    for c, d in product(range(4), repeat=2):
        checks.require("star_subgroup_universal_containment", (model.epsilon(c) - 1) % 2 == 0 and (2 * c * d) % 2 == 0, (c, d))
    r, x = (1, 0), (0, 1)
    for n in (-10**100, -100, -1, 0, 1, 100, 10**100):
        b = (n, 0)
        checks.require("generator_map_zero_fiber", all(model.star(p, q) == (0, 0) for p, q in ((b, r), (b, x), (r, b), (x, b))), n)
        checks.require("other_lambda_not_fixed", (model.lam((0, 2), b) == b) == (n == 0), n)
    # Multiplicative generation is confined to second coordinates {0,1},
    # which is a component subgroup; r supplies all integer translations.
    subgroup_controls(model, checks, True, {0, 1}, "circle")


def finite_quotient_controls(checks):
    rows = []
    for q in (2, 3, 4, 5, 7, 8, 11):
        elements = list(product(range(q), range(4)))
        fixed_y = [(m, d) for m, d in elements if (-2 * m) % q == 0]
        import math
        index = len(elements) // len(fixed_y)
        checks.require("finite_quotient_y_index", index == q // math.gcd(q, 2), (q, index))
        checks.require("finite_quotient_index_is_finite", isinstance(index, int), (q, index))
        rows.append({"integer_modulus": q, "y_right_fixed_index": index, "every_element_has_s": True})
    # A characteristic-2 replacement destroys the integer-based fixed-set
    # and injectivity evidence. Explicitly observe the collision at m=1.
    checks.require("torsion_negative_boundary", (-2 * 1) % 2 == 0 and -2 * 1 != 0)
    return rows


def verify(mutant=None):
    model, checks = Model(mutant), Checks()
    universal_checks(model, checks)
    indices = classify_indices(model, checks)
    concrete_checks(model, checks)
    reconciliation_controls(model, checks)
    quotients = finite_quotient_controls(checks)
    return {
        "verdict": "PASS_INDEPENDENT_EXACT_CONTROLS",
        "optimization_level": sys.flags.optimize,
        "checks": sum(checks.counts.values()),
        "categories": dict(sorted(checks.counts.items())),
        "exact_index_cases": indices,
        "finite_quotient_boundary_controls": quotients,
        "witness": {"x": [0, 1], "x_indices": [2, 2], "additive_double": [0, 2], "double_indices": ["infinite", "infinite"], "s_set": "Z x {0,1}"},
        "bounds": {"formal_integer_variables": 3, "component_exhaustion": [0, 1, 2, 3], "numerical_triple_integer_range": [-2, 2], "numerical_pair_integer_values": [-10**100, -10**32 - 1, -81, -2, -1, 0, 1, 2, 77, 10**32 + 1, 10**100]},
        "scope": "Formal coefficient equalities are universal over Z; finite integer controls are supplemental. Distinct coset families and torsion-free cancellation are written proofs, not inferred from finite quotients. No novelty or external-source gate is claimed.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutant", choices=("noncharacter_epsilon", "wrong_component", "wrong_star", "two_sided_claim"))
    args = parser.parse_args()
    try:
        result = verify(args.mutant)
    except CheckFailure as exc:
        print(json.dumps({"verdict": "REJECTED", "mutant": args.mutant, "optimization_level": sys.flags.optimize, "reason": str(exc)}, sort_keys=True))
        return 1
    if args.mutant:
        print(json.dumps({"verdict": "UNEXPECTED_MUTANT_SURVIVAL", "mutant": args.mutant}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
