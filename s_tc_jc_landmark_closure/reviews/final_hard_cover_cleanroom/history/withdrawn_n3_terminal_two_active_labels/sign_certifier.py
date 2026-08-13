"""Independent exact strict-sign certificates on the open unit cube.

The certifier factors an integer polynomial over QQ and proves the sign of
each nonconstant factor from exact Bernstein coefficients on [0,1]^k.  A
nonzero Bernstein polynomial whose coefficients are all nonnegative is
strictly positive on the open cube because every basis function is strictly
positive there; the analogous statement holds for nonpositive coefficients.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import math

import sympy as sp

from graph_model import digest
from jc_exact import p_hash


def _sympy_expression(polynomial, variables):
    return sum(
        int(coefficient) * sp.prod(variable ** exponent for variable, exponent
                                   in zip(variables, monomial))
        for monomial, coefficient in polynomial.items()
    )


def _factor_sparse(poly, variable_count):
    terms = {}
    for monomial, coefficient in poly.terms():
        full = tuple(int(x) for x in monomial)
        if len(full) != variable_count:
            raise AssertionError((len(full), variable_count))
        value = Fraction(coefficient)
        if value.denominator != 1:
            raise ValueError("factor has nonintegral coefficients")
        if value.numerator:
            terms[full] = value.numerator
    return terms


def _bernstein_coefficients(sparse, used, degrees):
    """Power-to-Bernstein conversion at fixed multidegree, exactly."""
    coefficients = []
    projected = [
        (tuple(monomial[index] for index in used), Fraction(coefficient))
        for monomial, coefficient in sparse.items()
    ]
    for index in itertools.product(*(range(degree + 1) for degree in degrees)):
        value = Fraction(0)
        for monomial, coefficient in projected:
            if all(power <= slot for power, slot in zip(monomial, index)):
                scale = Fraction(1)
                for power, slot, degree in zip(monomial, index, degrees):
                    scale *= Fraction(math.comb(slot, power), math.comb(degree, power))
                value += coefficient * scale
        coefficients.append(value)
    return coefficients


def bernstein_strict_sign(sparse, variable_count, max_elevation=8):
    used = tuple(
        index for index in range(variable_count)
        if any(monomial[index] for monomial in sparse)
    )
    if not used:
        value = next(iter(sparse.values()), 0)
        if not value:
            return None
        return {
            "sign": 1 if value > 0 else -1,
            "used_variables": [],
            "degrees": [],
            "elevation": 0,
            "coefficient_count": 1,
            "minimum": str(value),
            "maximum": str(value),
        }
    base = tuple(max(monomial[index] for monomial in sparse) for index in used)
    for elevation in range(max_elevation + 1):
        degrees = tuple(degree + elevation for degree in base)
        coefficients = _bernstein_coefficients(sparse, used, degrees)
        if all(value >= 0 for value in coefficients) and any(value > 0 for value in coefficients):
            sign = 1
        elif all(value <= 0 for value in coefficients) and any(value < 0 for value in coefficients):
            sign = -1
        else:
            continue
        return {
            "sign": sign,
            "used_variables": list(used),
            "degrees": list(degrees),
            "elevation": elevation,
            "coefficient_count": len(coefficients),
            "minimum": str(min(coefficients)),
            "maximum": str(max(coefficients)),
        }
    return None


def certify_factorized_strict_sign(polynomial, variable_count, max_elevation=8):
    """Prove a nonzero integer polynomial has one strict open-cube sign."""
    if not polynomial:
        return None
    variables = sp.symbols(f"x0:{variable_count}")
    expression = _sympy_expression(polynomial, variables)
    coefficient, factors = sp.factor_list(expression, *variables)
    coefficient = Fraction(coefficient)
    sign = 1 if coefficient > 0 else -1
    factor_records = []
    for factor, multiplicity in factors:
        sparse = _factor_sparse(sp.Poly(factor, *variables, domain=sp.QQ), variable_count)
        proof = bernstein_strict_sign(sparse, variable_count, max_elevation)
        if proof is None:
            return None
        if multiplicity % 2:
            sign *= proof["sign"]
        factor_records.append({
            "multiplicity": int(multiplicity),
            "factor_sha256": p_hash(sparse),
            "term_count": len(sparse),
            "total_degree": max(sum(monomial) for monomial in sparse),
            "proof": proof,
        })
    certificate = {
        "method": "QQ_factorization_and_exact_Bernstein_coefficients",
        "polynomial_sha256": p_hash(polynomial),
        "polynomial_term_count": len(polynomial),
        "variable_count": variable_count,
        "rational_content": str(coefficient),
        "factor_count": len(factor_records),
        "factors": factor_records,
        "strict_sign": sign,
        "domain": "all effective JC edge multipliers and inheritance probabilities in (0,1)",
    }
    certificate["certificate_sha256"] = digest(certificate)
    return certificate
