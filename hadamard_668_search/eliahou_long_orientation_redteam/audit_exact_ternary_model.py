#!/usr/bin/env python3
"""Audit the exact ternary lower/upper/none formulation.

For each open long case, a ternary variable t_j records no s-flip (0), a
lower-endpoint flip (+1), or an upper-endpoint flip (-1), and u_j=t_j^2.
The physical rows are affine in (u,t).  This verifier checks the resulting
quadratic correlation polynomials and the precise scope of the two 42-fold
norms.

The plus and anti folds alone do not reconstruct the aperiodic norm.  Adding
the 41 high-lag ("causal") equations C_43,...,C_83 does.  The transformed
system has the same union of quadratic monomials as the direct aperiodic
system, but exposes support-only, orientation-only, and mixed stages.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import random
import sys
from typing import TypeAlias

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
CHAR3 = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(HERE), str(CHAR3), str(SEARCH)]

import audit_orientation_redteam as orientation  # noqa: E402
import search_char3_local as local  # noqa: E402
import verify_eliahou_adjacent42_repair as adjacent  # noqa: E402


# A formal variable is (physical support index, 0 for u or 1 for t).
Formal: TypeAlias = tuple[int, int]
# Monomials are (), (formal,), or (formal, formal).  Products on one ternary
# coordinate are reduced by u^2=u, t^2=u, and ut=t.
Monomial: TypeAlias = tuple[Formal, ...]
Polynomial: TypeAlias = dict[Monomial, int]


def add_polynomials(*terms: tuple[int, Polynomial]) -> Polynomial:
    result: Polynomial = {}
    for multiplier, polynomial in terms:
        for monomial, coefficient in polynomial.items():
            result[monomial] = (
                result.get(monomial, 0) + multiplier * coefficient
            )
            if result[monomial] == 0:
                del result[monomial]
    return result


def multiply_formals(left: Formal, right: Formal) -> Monomial:
    if left[0] == right[0]:
        # u*u=u, t*t=u, and u*t=t on {-1,0,1}.
        output_type = 0 if left[1] == right[1] else 1
        return ((left[0], output_type),)
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def multiply_affine(left: Polynomial, right: Polynomial) -> Polynomial:
    if any(len(key) > 1 for key in left) or any(
        len(key) > 1 for key in right
    ):
        raise ValueError("multiply_affine accepts affine polynomials only")
    result: Polynomial = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            if not left_monomial:
                product = right_monomial
            elif not right_monomial:
                product = left_monomial
            else:
                product = multiply_formals(
                    left_monomial[0], right_monomial[0]
                )
            result[product] = (
                result.get(product, 0) + left_value * right_value
            )
            if result[product] == 0:
                del result[product]
    return result


def symbolic_rows(case, keys: tuple[tuple[str, int], ...]):
    constants = orientation.q_adjusted_rows(case)
    rows: list[list[Polynomial]] = [
        [{(): int(constants[row, coordinate])} for coordinate in range(84)]
        for row in range(4)
    ]
    # The padded final entry of each short row is exactly zero.
    rows[2][83] = {}
    rows[3][83] = {}
    for variable, (block, cell) in enumerate(keys):
        pair = (0, 1) if block == "L" else (2, 3)
        for row in pair:
            lower = int(constants[row, cell])
            upper = int(constants[row, cell + 42])
            if lower != -upper:
                raise AssertionError("eligible endpoints ceased to be opposite")
            rows[row][cell] = {
                (): lower,
                ((variable, 0),): -lower,
                ((variable, 1),): -lower,
            }
            rows[row][cell + 42] = {
                (): upper,
                ((variable, 0),): -upper,
                ((variable, 1),): upper,
            }
    return rows


def correlation_polynomial(rows, lag: int) -> Polynomial:
    result: Polynomial = {}
    for row in rows:
        length = 83 if not row[83] else 84
        for left in range(length - lag):
            result = add_polynomials(
                (1, result),
                (1, multiply_affine(row[left], row[left + lag])),
            )
    return result


def evaluate_polynomial(polynomial: Polynomial, ternary: list[int]) -> int:
    result = 0
    for monomial, coefficient in polynomial.items():
        value = 1
        for variable, kind in monomial:
            value *= ternary[variable] ** (2 if kind == 0 else 1)
        result += coefficient * value
    return result


def physical_rows(case, keys, ternary: list[int]):
    rows = orientation.q_adjusted_rows(case).tolist()
    for state, (block, cell) in zip(ternary, keys):
        if state == 0:
            continue
        coordinate = cell if state == 1 else cell + 42
        for row in ((0, 1) if block == "L" else (2, 3)):
            rows[row][coordinate] *= -1
    return rows


def direct_correlation(rows, lag: int) -> int:
    return sum(
        sum(
            row[index] * row[index + lag]
            for index in range(len(row) - lag)
        )
        for row in (rows[0], rows[1], rows[2][:83], rows[3][:83])
        if lag < len(row)
    )


def quadratic_support(polynomials: list[Polynomial]) -> set[Monomial]:
    return {
        monomial
        for polynomial in polynomials
        for monomial in polynomial
        if len(monomial) == 2 and polynomial[monomial]
    }


def type_histogram(monomials: set[Monomial]) -> dict[str, int]:
    histogram = Counter(
        ("u" if monomial[0][1] == 0 else "t")
        + ("u" if monomial[1][1] == 0 else "t")
        for monomial in monomials
    )
    return dict(sorted(histogram.items()))


def half_polynomial(polynomial: Polynomial) -> Polynomial:
    if any(coefficient % 2 for coefficient in polynomial.values()):
        raise AssertionError("polynomial is not coefficientwise even")
    return {
        monomial: coefficient // 2
        for monomial, coefficient in polynomial.items()
        if coefficient
    }


def derive_case(case_number: int) -> dict[str, object]:
    case, keys, _, _, _, _ = local.arrays(case_number)
    rows = symbolic_rows(case, keys)
    correlations = {
        lag: correlation_polynomial(rows, lag)
        for lag in range(84)
    }

    # C_42 is exactly -156+4*sum(u_j) in every long case.  Thus the shell
    # constraint sum u_j=39 forces the missing central correlation to zero.
    expected_c42: Polynomial = {(): -156}
    for variable in range(len(keys)):
        expected_c42[((variable, 0),)] = 4
    if correlations[42] != expected_c42:
        raise AssertionError("the universal lag-42 shell identity changed")

    anti = [
        add_polynomials(
            (1, correlations[k]),
            (-1, correlations[42 - k]),
            (-1, correlations[42 + k]),
            (1, correlations[84 - k]),
        )
        for k in range(1, 21)
    ]
    plus = [
        add_polynomials(
            (1, correlations[k]),
            (1, correlations[42 - k]),
            (1, correlations[42 + k]),
            (1, correlations[84 - k]),
        )
        for k in range(1, 21)
    ]
    plus.append(
        add_polynomials(
            (2, correlations[21]), (2, correlations[63])
        )
    )
    causal = [correlations[lag] for lag in range(43, 84)]

    # Reconstruct every C_k except the shell-forced C_42 from the folds and
    # causal half.  This is an exact polynomial identity over Z.
    reconstructed: dict[int, Polynomial] = {
        lag: correlations[lag] for lag in range(43, 84)
    }
    for k in range(1, 21):
        reconstructed[k] = add_polynomials(
            (1, half_polynomial(add_polynomials((1, plus[k - 1]), (1, anti[k - 1])))),
            (-1, correlations[84 - k]),
        )
        reconstructed[42 - k] = add_polynomials(
            (1, half_polynomial(add_polynomials((1, plus[k - 1]), (-1, anti[k - 1])))),
            (-1, correlations[42 + k]),
        )
    reconstructed[21] = add_polynomials(
        (1, half_polynomial(plus[20])),
        (-1, correlations[63]),
    )
    if set(reconstructed) != set(range(1, 84)) - {42}:
        raise AssertionError("causal reconstruction missed a lag")
    for lag, polynomial in reconstructed.items():
        if polynomial != correlations[lag]:
            raise AssertionError(
                f"causal reconstruction failed at lag {lag}"
            )

    # Direct physical replay on bounded ternary fixtures checks the symbolic
    # row convention and the u=t^2 reduction.
    generator = random.Random(7_668_330_000 + case_number)
    for _ in range(16):
        ternary = [generator.randrange(-1, 2) for _ in keys]
        concrete = physical_rows(case, keys, ternary)
        for lag in range(84):
            if evaluate_polynomial(correlations[lag], ternary) != (
                direct_correlation(concrete, lag)
            ):
                raise AssertionError("symbolic physical replay failed")

    direct_polynomials = [
        correlations[lag] for lag in range(1, 84) if lag != 42
    ]
    direct_products = quadratic_support(direct_polynomials)
    anti_products = quadratic_support(anti)
    plus_products = quadratic_support(plus)
    causal_products = quadratic_support(causal)
    transformed_products = anti_products | plus_products | causal_products
    if transformed_products != direct_products:
        raise AssertionError(
            "invertible fold/causal transform changed product support"
        )
    if anti_products & plus_products:
        raise AssertionError("support/orientation fold products overlap")
    if type_histogram(anti_products).keys() - {"uu"}:
        raise AssertionError("anti fold gained orientation products")
    if type_histogram(plus_products).keys() - {"tt"}:
        raise AssertionError("plus fold gained support products")
    expected_anti_products = 1445 if case_number in (2, 14) else 1446
    if (
        len(direct_products) != 5928
        or type_histogram(direct_products)
        != {"tt": 1482, "tu": 1482, "ut": 1482, "uu": 1482}
        or len(anti_products) != expected_anti_products
        or type_histogram(anti_products) != {"uu": expected_anti_products}
        or len(plus_products) != 1482
        or type_histogram(plus_products) != {"tt": 1482}
        or len(causal_products) != 5928
        or transformed_products != direct_products
    ):
        raise AssertionError("the frozen ternary product certificate changed")

    return {
        "case": case_number,
        "q_index": case.index,
        "ternary_variables": len(keys),
        "state_encoding": (
            "t_j in {-1,0,1}; u_j=t_j^2; +1 lower, -1 upper, 0 none"
        ),
        "shell_constraint": "sum_j u_j=39",
        "lag42_identity": "C_42=-156+4 sum_j u_j=0",
        "anti_fold_equations": len(anti),
        "plus_fold_equations": len(plus),
        "causal_high_lag_equations": len(causal),
        "reconstructed_noncentral_lags": len(reconstructed),
        "direct_quadratic_products": len(direct_products),
        "direct_product_type_histogram": type_histogram(direct_products),
        "anti_quadratic_products": len(anti_products),
        "plus_quadratic_products": len(plus_products),
        "causal_quadratic_products": len(causal_products),
        "anti_causal_shared_products": len(anti_products & causal_products),
        "plus_causal_shared_products": len(plus_products & causal_products),
        "causal_product_type_histogram": type_histogram(causal_products),
        "transformed_quadratic_products": len(transformed_products),
        "fewer_products_than_direct": len(transformed_products) < len(
            direct_products
        ),
        "structural_advantage": (
            "no global product-count reduction; the invertible transform "
            "separates 20 support-only and 21 orientation-only equations "
            "before the 41 mixed causal equations and reuses products"
        ),
        "conditional_linearity": (
            "fixing u leaves tt quadratics; prescribing endpoint signs "
            "leaves uu quadratics; fixing the complete lower half makes "
            "the 41 causal high-lag equations linear in the upper half"
        ),
    }


def kernel_counterexample() -> dict[str, object]:
    """Record the exact kernel missed by both 42-fold norm maps."""

    coefficients = {1: 2, 83: -2}
    plus = {
        k: coefficients.get(k, 0)
        + coefficients.get(42 - k, 0)
        + coefficients.get(42 + k, 0)
        + coefficients.get(84 - k, 0)
        for k in range(1, 21)
    }
    plus[21] = 2 * (
        coefficients.get(21, 0) + coefficients.get(63, 0)
    )
    anti = {
        k: coefficients.get(k, 0)
        - coefficients.get(42 - k, 0)
        - coefficients.get(42 + k, 0)
        + coefficients.get(84 - k, 0)
        for k in range(1, 21)
    }
    if any(plus.values()) or any(anti.values()):
        raise AssertionError("the fold-kernel counterexample stopped vanishing")
    # On |z|=1 the perturbation has absolute value at most eight, so adding
    # it to the target 334 remains strictly positive.
    return {
        "nonzero_lag_coefficients": {"1": 2, "83": -2},
        "plus_fold_nonzero_coefficients": {},
        "anti_fold_nonzero_coefficients": {},
        "aperiodic_nonzero": True,
        "integral_and_binary_correlation_parity_compatible": True,
        "target_plus_kernel_spectral_lower_bound": 326,
        "conclusion": (
            "the two folds prove periodic length-84 complementarity, not "
            "aperiodic base-sequence complementarity"
        ),
    }


def main() -> None:
    cases = [derive_case(case_number) for case_number in range(1, 21)]
    signatures = {
        (
            item["direct_quadratic_products"],
            json.dumps(item["direct_product_type_histogram"], sort_keys=True),
            item["anti_quadratic_products"],
            item["plus_quadratic_products"],
            item["causal_quadratic_products"],
            item["anti_causal_shared_products"],
            item["plus_causal_shared_products"],
        )
        for item in cases
    }
    print(
        json.dumps(
            {
                "status": (
                    "exact ternary-model algebra verified; no solution or "
                    "long-case exclusion claimed"
                ),
                "fold_kernel": kernel_counterexample(),
                "distinct_product_count_signatures": len(signatures),
                "cases": cases,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
