#!/usr/bin/python3
"""Dependency-free exact audit of the vertical fixed-linear cubic-pencil claim.

The candidate package uses SymPy and PARI.  This audit instead uses a small
dictionary polynomial implementation, Fraction Gaussian elimination, and
integer divisor enumeration.  Set AUDIT_MUTATION to exercise a fail-closed
guard from the accompanying shell wrapper.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import os
import sys
from typing import Iterable


MUTATION = os.environ.get("AUDIT_MUTATION", "strict")
NVAR = 4  # x,y,z,tau
ZERO_EXP = (0,) * NVAR


def fail(message: str) -> None:
    print(f"FAIL [{MUTATION}]: {message}")
    raise SystemExit(1)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


Poly = dict[tuple[int, ...], Fraction]


def clean(poly: Poly) -> Poly:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def constant(value: int | Fraction) -> Poly:
    value = Fraction(value)
    return {} if not value else {ZERO_EXP: value}


def variable(index: int) -> Poly:
    exponent = [0] * NVAR
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def add(*polynomials: Poly) -> Poly:
    result: Poly = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return clean(result)


def neg(poly: Poly) -> Poly:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def sub(left: Poly, right: Poly) -> Poly:
    return add(left, neg(right))


def scale(poly: Poly, scalar: int | Fraction) -> Poly:
    scalar = Fraction(scalar)
    return clean({monomial: scalar * coefficient for monomial, coefficient in poly.items()})


def mul(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] = result.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
    return clean(result)


def power(poly: Poly, exponent: int) -> Poly:
    check(exponent >= 0, "negative polynomial exponent")
    result = constant(1)
    base = poly
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = mul(result, base)
        base = mul(base, base)
        remaining //= 2
    return result


def derivative(poly: Poly, index: int) -> Poly:
    result: Poly = {}
    for monomial, coefficient in poly.items():
        if monomial[index]:
            derived = list(monomial)
            factor = derived[index]
            derived[index] -= 1
            result[tuple(derived)] = coefficient * factor
    return clean(result)


def substitute(poly: Poly, images: tuple[Poly, Poly, Poly, Poly]) -> Poly:
    result: Poly = {}
    for monomial, coefficient in poly.items():
        term = constant(coefficient)
        for index, exponent in enumerate(monomial):
            term = mul(term, power(images[index], exponent))
        result = add(result, term)
    return result


def det3(matrix: list[list[Poly]]) -> Poly:
    positive = add(
        mul(mul(matrix[0][0], matrix[1][1]), matrix[2][2]),
        mul(mul(matrix[0][1], matrix[1][2]), matrix[2][0]),
        mul(mul(matrix[0][2], matrix[1][0]), matrix[2][1]),
    )
    negative = add(
        mul(mul(matrix[0][2], matrix[1][1]), matrix[2][0]),
        mul(mul(matrix[0][1], matrix[1][0]), matrix[2][2]),
        mul(mul(matrix[0][0], matrix[1][2]), matrix[2][1]),
    )
    return sub(positive, negative)


def jacobian3(first: Poly, second: Poly, third: Poly) -> Poly:
    return det3(
        [
            [derivative(form, index) for index in range(3)]
            for form in (first, second, third)
        ]
    )


def jacobian_matrix(forms: tuple[Poly, Poly, Poly]) -> list[list[Poly]]:
    return [[derivative(form, index) for index in range(3)] for form in forms]


def matrix_add(*matrices: list[list[Poly]]) -> list[list[Poly]]:
    return [
        [add(*(matrix[row][column] for matrix in matrices)) for column in range(3)]
        for row in range(3)
    ]


def tau_shift(poly: Poly, exponent: int) -> Poly:
    shifted: Poly = {}
    for monomial, coefficient in poly.items():
        new_monomial = list(monomial)
        new_monomial[3] += exponent
        shifted[tuple(new_monomial)] = coefficient
    return shifted


def matrix_tau_shift(matrix: list[list[Poly]], exponent: int) -> list[list[Poly]]:
    return [[tau_shift(entry, exponent) for entry in row] for row in matrix]


def homogeneous_monomials(degree: int) -> list[tuple[int, ...]]:
    return [
        (x_degree, y_degree, degree - x_degree - y_degree, 0)
        for x_degree in range(degree + 1)
        for y_degree in range(degree + 1 - x_degree)
    ]


def rank_fraction(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def operator_rank(P: Poly, Q: Poly, degree: int) -> int:
    inputs = homogeneous_monomials(degree)
    outputs = homogeneous_monomials(3 + 3 + degree - 1)
    columns: list[list[Fraction]] = []
    for input_monomial in inputs:
        image = jacobian3(P, Q, {input_monomial: Fraction(1)})
        columns.append([image.get(output_monomial, Fraction(0)) for output_monomial in outputs])
    matrix = [[columns[column][row] for column in range(len(columns))] for row in range(len(outputs))]
    return rank_fraction(matrix)


def constant_matrix_rank(matrix: list[list[Poly]]) -> int:
    rational_matrix: list[list[Fraction]] = []
    for row in matrix:
        rational_row: list[Fraction] = []
        for entry in row:
            check(set(entry).issubset({ZERO_EXP}), "expected a constant Hessian entry")
            rational_row.append(entry.get(ZERO_EXP, Fraction(0)))
        rational_matrix.append(rational_row)
    return rank_fraction(rational_matrix)


X, Y, Z, TAU = (variable(index) for index in range(NVAR))
ONE = constant(1)
ZERO: Poly = {}


def monomial(x_degree: int, y_degree: int, z_degree: int) -> Poly:
    return power(X, x_degree) if y_degree == z_degree == 0 else mul(
        power(X, x_degree), mul(power(Y, y_degree), power(Z, z_degree))
    )


# ---------------------------------------------------------------------------
# 1. Exact valuation enumeration.
# ---------------------------------------------------------------------------


def h_solutions(multiplicity: int, degree: int) -> list[tuple[int, int]]:
    solutions: list[tuple[int, int]] = []
    fixed_multiplicity = multiplicity
    if MUTATION == "valuation_h_shift":
        fixed_contribution = degree * fixed_multiplicity
    else:
        fixed_contribution = degree * (fixed_multiplicity + 1)
    for valuation in range(degree + 1):
        numerator = 4 * valuation - fixed_contribution
        if numerator % fixed_multiplicity == 0:
            solutions.append((numerator // fixed_multiplicity, valuation))
    return solutions


expected_h = {
    1: [(-6, 0), (-2, 1), (2, 2), (6, 3)],
    2: [],
    3: [(-4, 0), (0, 3)],
}
for multiplicity, expected in expected_h.items():
    check(h_solutions(multiplicity, 3) == expected, f"degree-three h-valuation for m={multiplicity}")

quadratic_factorizations = (
    ((1, 2),),          # irreducible quadratic
    ((1, 1), (1, 1)),  # two reduced lines
    ((2, 1),),          # a double line
)
for order_at_infinity, _ in expected_h[1]:
    compatible = False
    for factorization in quadratic_factorizations:
        local_ok = True
        for multiplicity, _component_degree in factorization:
            numerator = multiplicity * (3 + order_at_infinity)
            if numerator % 4:
                local_ok = False
                break
            if numerator // 4 < 0:
                local_ok = False
                break
        compatible |= local_ok
    check(not compatible, f"m=1 must be excluded for s={order_at_infinity}")

# Repeat the same divisor arithmetic for the degree-two kernel quoted in
# the candidate.  The only m=1 solution is s=0 with a double-line
# quadratic cofactor; m=2 has incompatible parity at its residual line,
# and m=3 exhausts the degree on h.
expected_h_degree_two = {
    1: [(-4, 0), (0, 1), (4, 2)],
    2: [(-3, 0), (-1, 1), (1, 2)],
    3: [(0, 2)],
}
for multiplicity, expected in expected_h_degree_two.items():
    check(h_solutions(multiplicity, 2) == expected,
          f"degree-two h-valuation for m={multiplicity}")

degree_two_m1_solutions: list[tuple[int, tuple[tuple[int, int], ...]]] = []
for order_at_infinity, h_valuation in expected_h_degree_two[1]:
    for factorization in quadratic_factorizations:
        component_valuations: list[tuple[int, int]] = []
        for multiplicity, component_degree in factorization:
            numerator = multiplicity * (2 + order_at_infinity)
            if numerator % 4 or numerator // 4 < 0:
                break
            component_valuations.append((numerator // 4, component_degree))
        else:
            forced_degree = h_valuation + sum(
                valuation * component_degree
                for valuation, component_degree in component_valuations
            )
            if forced_degree <= 2:
                degree_two_m1_solutions.append((order_at_infinity, factorization))
check(degree_two_m1_solutions == [(0, ((2, 1),))],
      "degree-two m=1 kernel occurs exactly for r=L^2")

for order_at_infinity, _ in expected_h_degree_two[2]:
    check((2 + order_at_infinity) % 4 != 0,
          "degree-two m=2 residual line is incompatible with the h equation")


cubic_fibre_types = (
    ((1, 3),),                  # irreducible cubic
    ((1, 2), (1, 1)),          # conic plus line
    ((1, 1), (1, 1), (1, 1)),  # three reduced lines
    ((2, 1), (1, 1)),          # double line plus line
    ((3, 1),),                  # triple line
)


def zero_order_supported(order: int) -> bool:
    modulus = 2 if MUTATION == "fibre_modulus" else 4
    return any(
        all((order * multiplicity) % modulus == 0 for multiplicity, _ in fibre_type)
        for fibre_type in cubic_fibre_types
    )


check(all(not zero_order_supported(order) for order in (1, 2, 3)),
      "no finite zero of order below four can support a cubic fibre")
check(all(zero_order_supported(4) for _ in (0,)), "order four supports every cubic fibre type")
check(all(
    not any(
        all(
            (order * multiplicity) % 4 == 0
            and order * multiplicity // 4 >= 0
            for multiplicity, _ in fibre_type
        )
        for fibre_type in cubic_fibre_types
    )
    for order in (-1, -2, -3, -4)
), "finite poles cannot occur when s=-4")


def compositions(total: int) -> Iterable[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    for first in range(1, total + 1):
        for rest in compositions(total - first):
            yield (first,) + rest


supported_zero_patterns = [
    pattern for pattern in compositions(4)
    if all(zero_order_supported(order) for order in pattern)
]
check(supported_zero_patterns == [(4,)], "s=-4 has exactly one finite zero of order four")


# ---------------------------------------------------------------------------
# 2. Companion orbits under q -> a q + b p and target scaling.
# ---------------------------------------------------------------------------


def normalize_companion(alpha: Fraction, beta: Fraction) -> tuple[str, Fraction, Fraction]:
    check(alpha != 0 or beta != 0, "zero companion is handled by the quadratic exit")
    if beta == 0:
        target_scale = 1 / alpha
        return ("p", target_scale * alpha, Fraction(0))
    a = Fraction(1)
    b = alpha / beta
    if MUTATION == "orbit_shear_sign":
        b = -b
    new_p = alpha - beta * b / a
    new_q = beta / a
    target_scale = 1 / new_q
    return ("q", target_scale * new_p, target_scale * new_q)


for alpha, beta in (
    (Fraction(1), Fraction(0)),
    (Fraction(-3, 2), Fraction(0)),
    (Fraction(0), Fraction(1)),
    (Fraction(2), Fraction(3)),
    (Fraction(-5, 7), Fraction(11, 13)),
):
    label, normalized_p, normalized_q = normalize_companion(alpha, beta)
    if beta == 0:
        check((label, normalized_p, normalized_q) == ("p", 1, 0), "vertical companion normalization")
    else:
        check((label, normalized_p, normalized_q) == ("q", 0, 1), "nonvertical companion normalization")

for beta in (Fraction(0), Fraction(2, 3)):
    transformed_beta = Fraction(5, 7) * beta / Fraction(-3, 4)
    check((transformed_beta == 0) == (beta == 0), "h-divisibility separates the two companion orbits")

if MUTATION == "companion_collapse":
    check(False, "the p and q companion orbits cannot merge")


# ---------------------------------------------------------------------------
# 3. Marked-member orbits and stabilizer legality.
# ---------------------------------------------------------------------------


quadratic_representatives = (
    (mul(X, Y), (2, 2)),
    (add(mul(X, Y), power(Z, 2)), (2, 3)),
    (power(X, 2), (1, 1)),
    (add(power(X, 2), power(Z, 2)), (1, 2)),
    (add(power(X, 2), mul(Y, Z)), (1, 3)),
)

observed_rank_pairs: list[tuple[int, int]] = []
for quadratic, expected_ranks in quadratic_representatives:
    hessian = [[derivative(derivative(quadratic, row), column) for column in range(3)] for row in range(3)]
    restricted = [[hessian[row][column] for column in range(2)] for row in range(2)]
    actual = (constant_matrix_rank(restricted), constant_matrix_rank(hessian))
    observed_rank_pairs.append(actual)
    check(actual == expected_ranks, "parabolic quadratic-orbit rank pair")

expected_rank_pairs = [(2, 2), (2, 3), (1, 1), (1, 2), (1, 3)]
if MUTATION == "orbit_merge_ranks":
    expected_rank_pairs[-1] = (1, 2)
check(observed_rank_pairs == expected_rank_pairs, "five marked simple-vertical source orbits stay disjoint")

identity_images = (X, Y, Z, TAU)
triple_images = (
    add(scale(X, 2), scale(Y, 3), scale(Z, 5)),
    add(scale(X, -1), scale(Y, 4), scale(Z, 7)),
    scale(Z, -2),
    TAU,
)
if MUTATION == "stabilizer_z_shear":
    triple_images = (triple_images[0], triple_images[1], add(scale(Z, -2), X), TAU)
check(substitute(power(Z, 3), triple_images) == scale(power(Z, 3), -8),
      "full triple-vertical parabolic preserves z^3")

square_images = (
    scale(X, 3),
    add(scale(Y, 2), scale(X, 5), scale(Z, 7)),
    scale(Z, -2),
    TAU,
)
if MUTATION == "illegal_square_shear":
    square_images = (add(scale(X, 3), Z), square_images[1], square_images[2], TAU)
check(substitute(mul(Z, power(X, 2)), square_images) == scale(mul(Z, power(X, 2)), -18),
      "simple-square stabilizer forbids an x-by-z shear")


# ---------------------------------------------------------------------------
# 4. E8 kernels and exact top-three survivors.
# ---------------------------------------------------------------------------


q_fermat = add(power(X, 3), power(Y, 3))
q_mixed = add(power(X, 3), power(Y, 3), mul(mul(X, Y), Z))
marked_members = (
    mul(Z, mul(X, Y)),
    mul(Z, add(mul(X, Y), power(Z, 2))),
    mul(Z, power(X, 2)),
    mul(Z, add(power(X, 2), power(Z, 2))),
    mul(Z, add(power(X, 2), mul(Y, Z))),
    mul(power(Z, 2), X),
    power(Z, 3),
)
expected_cubic_nullities = (0, 0, 0, 0, 0, 0, 2)
expected_quadratic_nullities = (0, 0, 1, 0, 0, 0, 1)
for marked_member, expected_nullity in zip(marked_members, expected_cubic_nullities):
    P = mul(Z, marked_member)
    Q = mul(Z, q_fermat)
    quadratic_nullity = 6 - operator_rank(P, Q, 2)
    quadratic_expected = expected_quadratic_nullities[marked_members.index(marked_member)]
    if MUTATION == "quadratic_kernel" and marked_member == mul(Z, power(X, 2)):
        quadratic_expected = 0
    check(quadratic_nullity == quadratic_expected,
          "exact quadratic E7 kernel on a marked-member representative")
    nullity = 10 - operator_rank(P, Q, 3)
    if MUTATION == "kernel_dimension" and marked_member == power(Z, 3):
        expected_nullity = 3
    check(nullity == expected_nullity, "exact cubic E8 kernel on a marked-member representative")

for q_sample in (q_fermat, q_mixed):
    P = power(Z, 4)
    Q = mul(Z, q_sample)
    check(jacobian3(P, Q, power(Z, 3)) == {}, "z^3 lies in the triple-vertical E8 kernel")
    check(jacobian3(P, Q, q_sample) == {}, "q lies in the triple-vertical E8 kernel")
    check(10 - operator_rank(P, Q, 3) == 2, "primitive q sample has no third E8 companion")

q_nonminimal = add(power(X, 3), mul(power(X, 2), Z), mul(X, power(Z, 2)))
boundary_nullity = 10 - operator_rank(power(Z, 4), mul(Z, q_nonminimal), 3)
boundary_expected = 4
if MUTATION == "drop_minimality":
    boundary_expected = 2
check(boundary_nullity == boundary_expected,
      "dropping minimality creates extra E8 survivors, so the boundary is retained")

identity = [[ONE if row == column else ZERO for column in range(3)] for row in range(3)]
for normal in (power(Z, 3), q_fermat):
    chosen_normal = normal
    if MUTATION == "e8_outside" and normal == q_fermat:
        chosen_normal = add(normal, mul(power(X, 2), Z))
    H4 = (power(Z, 4), mul(Z, q_fermat), ZERO)
    H3 = (ZERO, ZERO, chosen_normal)
    weighted = matrix_add(
        identity,
        matrix_tau_shift(jacobian_matrix(H3), 2),
        matrix_tau_shift(jacobian_matrix(H4), 3),
    )
    determinant = det3(weighted)
    for tau_degree in (8, 7, 6):
        coefficient_terms = {
            monomial: coefficient
            for monomial, coefficient in determinant.items()
            if monomial[3] == tau_degree
        }
        check(not coefficient_terms, f"companion top coefficient E{tau_degree}")
    check(any(monomial[3] <= 5 for monomial in determinant if monomial != ZERO_EXP),
          "a lower determinant obstruction remains")

print("PASS valuation congruences and m=1,2 exclusion")
print("PASS m=3 divisor classification and two companion orbits")
print("PASS marked-member orbit/stabilizer guards")
print("PASS exact E7/E8 kernels and top-three survivors")
print("ALL VERTICAL-LOCUS HOSTILE EXACT CHECKS PASSED")
