"""Exact open-unit-cube sign certificates for sparse integer polynomials."""

from __future__ import annotations

from fractions import Fraction
import hashlib
from itertools import product
import math

from jc_tensor import Poly, primitive


def to_sympy(poly: Poly):
    import sympy as sp

    variables = len(next(iter(poly))) if poly else 0
    symbols = sp.symbols(f"z0:{variables}")
    expression = sp.Integer(0)
    for exponents, coefficient in poly.items():
        term = sp.Integer(coefficient)
        for symbol, exponent in zip(symbols, exponents):
            if exponent:
                term *= symbol ** exponent
        expression += term
    return symbols, sp.expand(expression)


def bernstein_sign(expression, symbols, max_elevation: int = 3):
    """Sufficient exact strict-sign proof on the open cube."""
    import sympy as sp

    polynomial = sp.Poly(expression, *symbols, domain=sp.QQ)
    degrees_all = polynomial.degree_list()
    used = tuple(i for i, degree in enumerate(degrees_all) if degree)
    if not used:
        value = Fraction(polynomial.LC())
        return {
            "certified": value != 0,
            "sign": 1 if value > 0 else -1 if value < 0 else 0,
            "constant": str(value),
            "used_variables": [],
        }
    power_coefficients = {
        tuple(exponents[i] for i in used): Fraction(coefficient)
        for exponents, coefficient in polynomial.terms()
    }
    native = tuple(degrees_all[i] for i in used)
    for elevation in range(max_elevation + 1):
        degrees = tuple(degree + elevation for degree in native)
        coefficients = []
        for bernstein_index in product(*(range(degree + 1) for degree in degrees)):
            value = Fraction(0)
            for powers, coefficient in power_coefficients.items():
                if all(power <= index for power, index in zip(powers, bernstein_index)):
                    ratio = Fraction(1)
                    for index, power, degree in zip(bernstein_index, powers, degrees):
                        ratio *= Fraction(math.comb(index, power), math.comb(degree, power))
                    value += coefficient * ratio
            coefficients.append(value)
        positive = all(value >= 0 for value in coefficients) and any(value > 0 for value in coefficients)
        negative = all(value <= 0 for value in coefficients) and any(value < 0 for value in coefficients)
        if positive or negative:
            # Every Bernstein basis function is strictly positive in the open
            # cube; one strict coefficient therefore makes the sum strict.
            return {
                "certified": True,
                "sign": 1 if positive else -1,
                "used_variables": used,
                "degrees": degrees,
                "elevation": elevation,
                "coefficient_count": len(coefficients),
                "minimum": str(min(coefficients)),
                "maximum": str(max(coefficients)),
            }
    return {
        "certified": False,
        "used_variables": used,
        "native_degrees": native,
        "max_elevation": max_elevation,
    }


def certify(poly: Poly, *, max_elevation: int = 3):
    import sympy as sp

    if not poly:
        return {"certified": False, "reason": "zero polynomial"}
    coefficients = tuple(poly.values())
    if all(value >= 0 for value in coefficients) and any(value > 0 for value in coefficients):
        return {
            "certified": True,
            "strict_sign": 1,
            "domain": "all variables lie in (0,1)",
            "method": "same-sign sparse power coefficients",
            "polynomial_sha256": hashlib.sha256(repr(primitive(poly)).encode()).hexdigest(),
            "term_count": len(poly),
            "factors": [],
        }
    if all(value <= 0 for value in coefficients) and any(value < 0 for value in coefficients):
        return {
            "certified": True,
            "strict_sign": -1,
            "domain": "all variables lie in (0,1)",
            "method": "same-sign sparse power coefficients",
            "polynomial_sha256": hashlib.sha256(repr(primitive(poly)).encode()).hexdigest(),
            "term_count": len(poly),
            "factors": [],
        }
    symbols, expression = to_sympy(poly)
    constant, factors = sp.factor_list(expression, *symbols)
    sign = 1 if constant > 0 else -1
    rows = []
    for factor, multiplicity in factors:
        proof = bernstein_sign(factor, symbols, max_elevation=max_elevation)
        expanded = sp.expand(factor)
        row = {
            "expanded_sha256": hashlib.sha256(str(expanded).encode()).hexdigest(),
            "degree": int(sp.Poly(expanded, *symbols).total_degree()),
            "terms": len(sp.Poly(expanded, *symbols).terms()),
            "multiplicity": int(multiplicity),
            "proof": proof,
        }
        rows.append(row)
        if not proof["certified"]:
            return {
                "certified": False,
                "polynomial_sha256": hashlib.sha256(repr(primitive(poly)).encode()).hexdigest(),
                "factors": rows,
            }
        if multiplicity % 2:
            sign *= int(proof["sign"])
    return {
        "certified": True,
        "strict_sign": sign,
        "domain": "all effective JC edge multipliers and inheritance probabilities lie in (0,1)",
        "polynomial_sha256": hashlib.sha256(repr(primitive(poly)).encode()).hexdigest(),
        "term_count": len(poly),
        "factors": rows,
    }
