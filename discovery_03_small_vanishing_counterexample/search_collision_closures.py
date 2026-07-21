#!/usr/bin/env python3
"""Search rational fibers whose cubic-homogeneous collision closure is small.

For the announced map, if (P,Q,R) is the target and T=y+1/x, every finite
preimage satisfies

    R*T^3 - 2*T^2 + Q*T - 2*P = 0.

Choosing three distinct rational roots therefore produces a rational fiber.
We lift each fiber through the certified 13-variable stable reduction and the
27-variable BCW homogenization, then compute the invariant tensor closure of
each collision pair over a large prime.  Any improved candidate must later be
recomputed and certified over Q.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery_02_explicit_vanishing_counterexample"))

from construction import degree_reduction, cubic_homogeneous_map  # noqa: E402


MODULUS = 1_000_003


def mod_rational(value, modulus=MODULUS):
    value = sp.Rational(value)
    return int(value.p % modulus) * pow(int(value.q), -1, modulus) % modulus


def target_and_preimages(roots):
    r1, r2, r3 = map(sp.Rational, roots)
    root_sum = r1 + r2 + r3
    if root_sum == 0:
        return None
    target_r = sp.Rational(2, 1) / root_sum
    target_q = target_r * (r1 * r2 + r1 * r3 + r2 * r3)
    target_p = target_r * r1 * r2 * r3 / 2
    points = []
    for parameter in (r1, r2, r3):
        denominator = target_q - 4 * parameter + 3 * target_r * parameter**2
        if denominator == 0:
            return None
        x = 2 / denominator
        y = parameter - denominator / 2
        v = x * y
        gamma = target_r / x
        tau = 2 - 3 * v - gamma
        z = tau / x**2
        points.append((sp.factor(x), sp.factor(y), sp.factor(z)))
    return (target_p, target_q, target_r), points


def lift_stable(point):
    x, y, z = map(sp.Rational, point)
    g1a = -x**2
    g1b = -(x * z + 3 * y)
    g2a = -3 * x**2 * y
    g2b = -(2 * z + x * y * z + 3 * y**2)
    g3a = -x * y
    g3b = -(g2a * z + 3 * x * g2b)
    g4a = -x * y**2
    g4b = -(7 * y + 3 * x * z + 3 * x * y**2 + x**2 * y * z)
    g5a = -(g4a * x * y)
    g6b = -(g4a * g1b - y * g4b)
    return (
        x, y, z, g1a, g1b, g2a, g2b, g3a, g3b,
        g4a, g4b, g5a, g6b,
    )


def cubic_point(stable_point, reduction):
    substitutions = dict(zip(reduction.variables, stable_point))
    cubic_values = tuple(
        sp.factor(component.subs(substitutions))
        for component in reduction.cubic_part
    )
    return tuple(stable_point) + cubic_values + (sp.Integer(1),)


def ordered_tensor_terms(variables, mapping):
    """Sparse ordered tensor T with h(x)=T(x,x,x), reduced modulo p."""
    result = []
    for component in mapping:
        terms = []
        for monomial, coefficient in sp.Poly(component, *variables).terms():
            if coefficient == 0:
                continue
            indices = []
            for variable_index, exponent in enumerate(monomial):
                indices.extend([variable_index] * exponent)
            if len(indices) != 3:
                raise ValueError("mapping is not cubic homogeneous")
            ordered = sorted(set(permutations(indices)))
            tensor_coefficient = sp.Rational(coefficient, len(ordered))
            modular_coefficient = mod_rational(tensor_coefficient)
            terms.extend((triple, modular_coefficient) for triple in ordered)
        result.append(terms)
    return result


def tensor_value(tensor, first, second, third):
    result = []
    for component_terms in tensor:
        value = 0
        for (i, j, k), coefficient in component_terms:
            value += coefficient * first[i] * second[j] * third[k]
        result.append(value % MODULUS)
    return result


class ModularBasis:
    def __init__(self, dimension):
        self.dimension = dimension
        self.rows = []
        self.pivots = []

    def add(self, vector):
        row = [value % MODULUS for value in vector]
        for pivot, basis_row in zip(self.pivots, self.rows):
            if row[pivot]:
                factor = row[pivot]
                row = [
                    (entry - factor * base) % MODULUS
                    for entry, base in zip(row, basis_row)
                ]
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is None:
            return False
        inverse = pow(row[pivot], -1, MODULUS)
        row = [(value * inverse) % MODULUS for value in row]
        for row_index, (old_pivot, basis_row) in enumerate(zip(self.pivots, self.rows)):
            if basis_row[pivot]:
                factor = basis_row[pivot]
                self.rows[row_index] = [
                    (entry - factor * new_entry) % MODULUS
                    for entry, new_entry in zip(basis_row, row)
                ]
        insert_at = sum(old_pivot < pivot for old_pivot in self.pivots)
        self.pivots.insert(insert_at, pivot)
        self.rows.insert(insert_at, row)
        return True


def closure_dimension(tensor, first, second):
    basis = ModularBasis(len(first))
    basis.add(first)
    basis.add(second)
    processed_dimension = 0
    while processed_dimension < len(basis.rows):
        current = list(basis.rows)
        # Recomputing all triples is cheap in dimension <=27 and avoids subtle
        # incremental bookkeeping errors.
        for i, j, k in combinations_with_replacement(range(len(current)), 3):
            basis.add(tensor_value(tensor, current[i], current[j], current[k]))
        if len(basis.rows) == processed_dimension:
            break
        processed_dimension = len(current)
        if len(basis.rows) == len(current):
            break
    return len(basis.rows)


def verify_announced_target(target, points):
    x, y, z = sp.symbols("x y z")
    u = 1 + x * y
    raw = (
        sp.expand(u**3 * z + y**2 * u * (4 + 3 * x * y)),
        sp.expand(y + 3 * x * u**2 * z + 3 * x * y**2 * (4 + 3 * x * y)),
        sp.expand(2 * x - 3 * x**2 * y - x**3 * z),
    )
    for point in points:
        value = tuple(component.subs(dict(zip((x, y, z), point))) for component in raw)
        if tuple(map(sp.factor, value)) != tuple(map(sp.factor, target)):
            return False
    return True


def main():
    reduction = degree_reduction()
    cubic_variables, cubic_mapping = cubic_homogeneous_map(reduction)
    tensor = ordered_tensor_terms(cubic_variables, cubic_mapping)
    best = (len(cubic_variables) + 1, None)

    root_pool = [sp.Rational(value) for value in range(-6, 7) if value]
    for roots in combinations(root_pool, 3):
        data = target_and_preimages(roots)
        if data is None:
            continue
        target, source_points = data
        if not verify_announced_target(target, source_points):
            raise AssertionError((roots, target, source_points))
        stable_points = [lift_stable(point) for point in source_points]
        cubic_points = [cubic_point(point, reduction) for point in stable_points]
        modular_points = [
            [mod_rational(coordinate) for coordinate in point]
            for point in cubic_points
        ]
        for pair in combinations(range(3), 2):
            dimension = closure_dimension(
                tensor, modular_points[pair[0]], modular_points[pair[1]]
            )
            if dimension < best[0]:
                best = (dimension, (roots, pair, target, source_points))
                print("new best", best, flush=True)

    print("best closure", best)


if __name__ == "__main__":
    main()
