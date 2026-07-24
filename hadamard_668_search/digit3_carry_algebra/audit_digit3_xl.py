#!/usr/bin/env python3
"""Degree-3 XL audit after eliminating the delayed linear row.

The audit restricts profile h2-422220-0 to the 35-dimensional affine
hyperplane cut out by E1(origin)'s delayed digit-3 equation.  It derives:

* the eighteen second-digit quadrics;
* the eighteen remaining digit-3 carry cubics, using
  floor(S/3) == binom(S,3) (mod 3);
* all affine multiples (1,z_j) of the quadrics.

It then computes exact F_3 ranks in the reduced function ring
F_3[z_1,...,z_35]/(z_i^3-z_i), looking for a degree-3 refutation or new
linear/quadratic consequences.  Bit-packed ternary elimination keeps the
memory footprint small.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
HIGHER_DIGITS = SECOND_DIGIT / "higher_digits"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(HIGHER_DIGITS))
sys.path.insert(0, str(SEARCH_ROOT))

import audit_digit3_carry as carry  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402


Polynomial = dict[tuple[int, ...], int]
GENERIC_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def add_term(
    polynomial: Polynomial,
    monomial: tuple[int, ...],
    coefficient: int,
) -> None:
    coefficient %= 3
    if not coefficient:
        return
    following = (polynomial.get(monomial, 0) + coefficient) % 3
    if following:
        polynomial[monomial] = following
    else:
        polynomial.pop(monomial, None)


def effective_rows(profiles, origin, basis):
    rows = []
    for terms, constant_at_zero in second.second_digit_term_data(profiles):
        grouped = defaultdict(int)
        for term in terms:
            constant = (
                term.constant
                + sum(
                    coefficient * origin[variable]
                    for variable, coefficient in term.coefficients
                )
            ) % 3
            slopes = tuple(
                sum(
                    coefficient * basis[column][variable]
                    for variable, coefficient in term.coefficients
                )
                % 3
                for column in range(len(basis))
            )
            grouped[(constant, slopes)] += term.sign
        rows.append(
            (
                constant_at_zero,
                tuple(
                    (form, multiplicity)
                    for form, multiplicity in sorted(grouped.items())
                    if multiplicity
                ),
            )
        )
    return tuple(rows)


def delayed_hyperplane(candidate_index: int):
    candidate = second.CANDIDATES[candidate_index]
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    equations = second.first_digit_equations(profiles)
    origin, basis = second.affine_parameterization(equations, 54)
    rows36 = effective_rows(profiles, origin, basis)
    constant_at_zero, grouped = rows36[7]
    delayed_constant = constant_at_zero // 3
    delayed_linear = [0] * 36
    for (constant, slopes), multiplicity in grouped:
        if multiplicity % 3:
            raise AssertionError("the delayed row lost its common factor")
        epsilon = multiplicity // 3
        delayed_constant -= epsilon * constant
        for index, slope in enumerate(slopes):
            delayed_linear[index] -= epsilon * slope
    delayed_constant %= 3
    delayed_linear = tuple(value % 3 for value in delayed_linear)
    pivot = next(
        index for index, value in enumerate(delayed_linear) if value
    )
    inverse = pow(delayed_linear[pivot], -1, 3)
    pivot_constant = -delayed_constant * inverse % 3
    free = tuple(index for index in range(36) if index != pivot)
    pivot_slopes = tuple(
        -delayed_linear[index] * inverse % 3 for index in free
    )

    new_origin = tuple(
        (
            origin[row]
            + pivot_constant * basis[pivot][row]
        )
        % 3
        for row in range(54)
    )
    new_basis = tuple(
        tuple(
            (
                basis[source][row]
                + slope * basis[pivot][row]
            )
            % 3
            for row in range(54)
        )
        for source, slope in zip(free, pivot_slopes)
    )
    if len(new_basis) != 35:
        raise AssertionError("the delayed hyperplane dimension changed")
    rows35 = effective_rows(profiles, new_origin, new_basis)
    for fixture in range(12):
        point = tuple(
            (fixture * (index + 1) + index * index + 1) % 3
            for index in range(35)
        )
        placement = second.lift_affine_point(
            new_origin, new_basis, point
        )
        if second.symbolic_first_digits(equations, placement) != (0,) * 20:
            raise AssertionError("the 35-space left the first digit")
        a, _ = carry.row_statistics(rows35[7], point)
        if a % 9:
            raise AssertionError("the 35-space left delayed digit 3")
    return (
        profiles,
        new_origin,
        new_basis,
        rows35,
        {
            "eliminated_coordinate": pivot,
            "delayed_constant": delayed_constant,
            "delayed_linear_sha256": compact_hash(delayed_linear),
            "new_origin_sha256": compact_hash(new_origin),
            "new_basis_sha256": compact_hash(new_basis),
        },
    )


def affine_carry_polynomial(
    constant: int,
    slopes: Sequence[int],
) -> Polynomial:
    """Return binom(d+sum s_i*z_i,3) mod 3.

    Vandermonde's identity is truncated at auxiliary degree three.  For a
    variable contribution x=s*z, the required coefficients are:

      s=1: C(x,1)=z, C(x,2)=2z^2+z, C(x,3)=0;
      s=2: C(x,1)=2z, C(x,2)=2z^2+2z,
             C(x,3)=2z^2+z.
    """

    support = tuple(
        (index, int(slope) % 3)
        for index, slope in enumerate(slopes)
        if int(slope) % 3
    )
    first: list[Polynomial] = []
    second_value: list[Polynomial] = []
    third: list[Polynomial] = []
    for index, slope in support:
        first.append({(index,): slope})
        if slope == 1:
            second_value.append({(index,): 1, (index, index): 2})
            third.append({})
        else:
            second_value.append({(index,): 2, (index, index): 2})
            third.append({(index,): 1, (index, index): 2})

    coefficient_one: Polynomial = {}
    coefficient_two: Polynomial = {}
    coefficient_three: Polynomial = {}
    for polynomial in first:
        for monomial, coefficient in polynomial.items():
            add_term(coefficient_one, monomial, coefficient)
    for polynomial in second_value:
        for monomial, coefficient in polynomial.items():
            add_term(coefficient_two, monomial, coefficient)
    for left in range(len(first)):
        for right in range(left + 1, len(first)):
            for monomial_left, coefficient_left in first[left].items():
                for monomial_right, coefficient_right in first[right].items():
                    add_term(
                        coefficient_two,
                        tuple(sorted(monomial_left + monomial_right)),
                        coefficient_left * coefficient_right,
                    )
    for polynomial in third:
        for monomial, coefficient in polynomial.items():
            add_term(coefficient_three, monomial, coefficient)
    for left in range(len(second_value)):
        for right in range(len(first)):
            if left == right:
                continue
            for monomial_left, coefficient_left in second_value[left].items():
                for monomial_right, coefficient_right in first[right].items():
                    add_term(
                        coefficient_three,
                        tuple(sorted(monomial_left + monomial_right)),
                        coefficient_left * coefficient_right,
                    )
    for first_index in range(len(first)):
        for second_index in range(first_index + 1, len(first)):
            for third_index in range(second_index + 1, len(first)):
                monomial = tuple(
                    sorted(
                        next(iter(first[first_index]))
                        + next(iter(first[second_index]))
                        + next(iter(first[third_index]))
                    )
                )
                coefficient = (
                    next(iter(first[first_index].values()))
                    * next(iter(first[second_index].values()))
                    * next(iter(first[third_index].values()))
                )
                add_term(coefficient_three, monomial, coefficient)

    result: Polynomial = {}
    multiplier_one = int(constant == 2)  # binom(d,2)
    multiplier_two = int(constant) % 3   # binom(d,1)
    for source, multiplier in (
        (coefficient_one, multiplier_one),
        (coefficient_two, multiplier_two),
        (coefficient_three, 1),
    ):
        for monomial, coefficient in source.items():
            add_term(result, monomial, multiplier * coefficient)
    return result


def digit3_polynomial(row) -> Polynomial:
    constant_at_zero, grouped = row
    base_constant = constant_at_zero
    base_linear = [0] * 35
    for (constant, slopes), multiplicity in grouped:
        base_constant -= multiplicity * constant
        for index, slope in enumerate(slopes):
            base_linear[index] -= multiplicity * slope
    if base_constant % 3 or any(value % 3 for value in base_linear):
        raise AssertionError("the first digit is not coefficientwise zero")
    result: Polynomial = {}
    add_term(result, (), base_constant // 3)
    for index, value in enumerate(base_linear):
        add_term(result, (index,), value // 3)
    for (constant, slopes), multiplicity in grouped:
        local = affine_carry_polynomial(constant, slopes)
        for monomial, coefficient in local.items():
            add_term(result, monomial, multiplicity * coefficient)
    return result


def quadratic_polynomial(
    constant: int,
    linear: Sequence[int],
    polar: Sequence[Sequence[int]],
) -> Polynomial:
    result: Polynomial = {}
    add_term(result, (), constant)
    for index, coefficient in enumerate(linear):
        add_term(result, (index,), coefficient)
        add_term(result, (index, index), 2 * polar[index][index])
        for right in range(index + 1, len(linear)):
            add_term(
                result,
                (index, right),
                polar[index][right],
            )
    return result


def evaluate(polynomial: Polynomial, point: Sequence[int]) -> int:
    return sum(
        coefficient
        * (
            1
            if not monomial
            else __import__("functools").reduce(
                lambda left, index: left * int(point[index]),
                monomial,
                1,
            )
        )
        for monomial, coefficient in polynomial.items()
    ) % 3


def multiply_by_variable(
    polynomial: Polynomial,
    variable: int,
) -> Polynomial:
    result: Polynomial = {}
    for monomial, coefficient in polynomial.items():
        count = monomial.count(variable)
        if count == 2:
            reduced = tuple(
                index for index in monomial if index != variable
            ) + (variable,)
            reduced = tuple(sorted(reduced))
        else:
            reduced = tuple(sorted(monomial + (variable,)))
        add_term(result, reduced, coefficient)
    return result


def monomial_catalog(variables: int):
    result = [()]
    result.extend((index,) for index in range(variables))
    result.extend(
        (left, right)
        for left in range(variables)
        for right in range(left, variables)
    )
    result.extend(
        (repeated, repeated, other)
        if repeated < other
        else (other, repeated, repeated)
        for repeated in range(variables)
        for other in range(variables)
        if repeated != other
    )
    result.extend(
        (first, second_value, third)
        for first in range(variables)
        for second_value in range(first + 1, variables)
        for third in range(second_value + 1, variables)
    )
    if len(result) != len(set(result)):
        raise AssertionError("the reduced monomial catalog has duplicates")
    return tuple(result)


def polynomial_bits(polynomial: Polynomial, indices):
    ones = 0
    twos = 0
    for monomial, coefficient in polynomial.items():
        bit = 1 << indices[monomial]
        if coefficient % 3 == 1:
            ones |= bit
        elif coefficient % 3 == 2:
            twos |= bit
    return ones, twos


def add_bits(left, right, mask: int):
    left_one, left_two = left
    right_one, right_two = right
    left_zero = mask ^ (left_one | left_two)
    right_zero = mask ^ (right_one | right_two)
    return (
        (left_zero & right_one)
        | (left_one & right_zero)
        | (left_two & right_two),
        (left_zero & right_two)
        | (left_two & right_zero)
        | (left_one & right_one),
    )


def rank_bits(rows, mask: int) -> int:
    basis = {}
    for source_one, source_two in rows:
        row = source_one & mask, source_two & mask
        while row[0] | row[1]:
            pivot = (row[0] | row[1]).bit_length() - 1
            if pivot not in basis:
                if row[1] & (1 << pivot):
                    row = row[1], row[0]
                basis[pivot] = row
                break
            pivot_row = basis[pivot]
            if row[0] & (1 << pivot):
                # row - pivot = row + 2*pivot
                row = add_bits(
                    row, (pivot_row[1], pivot_row[0]), mask
                )
            else:
                # row - 2*pivot = row + pivot
                row = add_bits(row, pivot_row, mask)
    return len(basis)


def audit() -> dict[str, object]:
    profiles, origin, basis, rows, hyperplane = delayed_hyperplane(1)
    term_data = second.second_digit_term_data(profiles)
    constants, linears, polars = second.derive_quadratics(
        term_data, origin, basis
    )
    quadrics = tuple(
        quadratic_polynomial(
            constants[index], linears[index], polars[index]
        )
        for index in GENERIC_ROWS
    )
    cubics = tuple(digit3_polynomial(rows[index]) for index in GENERIC_ROWS)

    validation_points = tuple(
        tuple(
            (
                fixture * fixture
                + fixture * (index + 1)
                + index * index
                + 2
            )
            % 3
            for index in range(35)
        )
        for fixture in range(12)
    )
    for point in validation_points:
        placement = second.lift_affine_point(origin, basis, point)
        direct_second = second.direct_second_digits(profiles, placement)
        statistics = tuple(
            carry.row_statistics(row, point) for row in rows
        )
        for polynomial, row_index in zip(quadrics, GENERIC_ROWS):
            if evaluate(polynomial, point) != direct_second[row_index]:
                raise AssertionError("a restricted quadric failed replay")
        for polynomial, row_index in zip(cubics, GENERIC_ROWS):
            if evaluate(polynomial, point) != (
                statistics[row_index][0] // 3
            ) % 3:
                raise AssertionError("a carry cubic failed exact replay")

    xl_polynomials = []
    for quadric in quadrics:
        xl_polynomials.append(quadric)
        xl_polynomials.extend(
            multiply_by_variable(quadric, variable)
            for variable in range(35)
        )
    xl_polynomials.extend(cubics)
    monomials = monomial_catalog(35)
    indices = {monomial: index for index, monomial in enumerate(monomials)}
    if any(
        monomial not in indices
        for polynomial in xl_polynomials
        for monomial in polynomial
    ):
        raise AssertionError("an XL polynomial escaped degree three")
    bit_rows = tuple(
        polynomial_bits(polynomial, indices)
        for polynomial in xl_polynomials
    )
    all_mask = (1 << len(monomials)) - 1
    degree_masks = {
        degree: sum(
            1 << index
            for index, monomial in enumerate(monomials)
            if len(monomial) == degree
        )
        for degree in range(4)
    }
    full_rank = rank_bits(bit_rows, all_mask)
    cubic_projection_rank = rank_bits(bit_rows, degree_masks[3])
    degree_at_least_two_rank = rank_bits(
        bit_rows, degree_masks[2] | degree_masks[3]
    )
    nonconstant_rank = rank_bits(
        bit_rows,
        degree_masks[1] | degree_masks[2] | degree_masks[3],
    )
    quadric_bits = tuple(
        polynomial_bits(polynomial, indices) for polynomial in quadrics
    )
    quadric_rank = rank_bits(
        quadric_bits,
        degree_masks[0] | degree_masks[1] | degree_masks[2],
    )
    quadratic_or_lower = full_rank - cubic_projection_rank
    linear_or_lower = full_rank - degree_at_least_two_rank
    constant_only = full_rank - nonconstant_rank
    result = {
        "schema": "lp333-order3-digit3-xl-v1",
        "label": second.CANDIDATES[1][0],
        "hyperplane": hyperplane,
        "variables": 35,
        "second_digit_quadrics": len(quadrics),
        "remaining_digit3_cubics": len(cubics),
        "xl_rows": len(xl_polynomials),
        "monomials": {
            "degree_0": sum(len(value) == 0 for value in monomials),
            "degree_1": sum(len(value) == 1 for value in monomials),
            "degree_2": sum(len(value) == 2 for value in monomials),
            "degree_3": sum(len(value) == 3 for value in monomials),
            "total": len(monomials),
        },
        "ranks": {
            "original_quadric_span": quadric_rank,
            "full_xl": full_rank,
            "cubic_projection": cubic_projection_rank,
            "quadratic_or_lower_intersection": quadratic_or_lower,
            "linear_or_lower_intersection": linear_or_lower,
            "constant_only_intersection": constant_only,
            "new_quadratic_or_lower_beyond_original_span": (
                quadratic_or_lower - quadric_rank
            ),
        },
        "conclusions": {
            "degree_3_refutation": constant_only > 0,
            "new_linear_consequence": linear_or_lower > 0,
            "new_quadratic_consequence": (
                quadratic_or_lower > quadric_rank
            ),
        },
        "validation_points": len(validation_points),
        "quadrics_sha256": compact_hash(
            tuple(tuple(sorted(polynomial.items())) for polynomial in quadrics)
        ),
        "cubics_sha256": compact_hash(
            tuple(tuple(sorted(polynomial.items())) for polynomial in cubics)
        ),
    }
    return result


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={compact_hash(result)}")


if __name__ == "__main__":
    main()
