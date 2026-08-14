#!/usr/bin/env python3
"""Minimal exact verifier for equation-only YES and Real-Nullstellensatz NO certificates.

This verifier deliberately does not search for certificates.  It checks a
claimed finite object by rational polynomial arithmetic or by reduction in one
specified real algebraic number field.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import sympy as sp


@dataclass(frozen=True)
class CoefficientField:
    alpha: sp.Symbol | None
    minimal_polynomial: sp.Poly | None
    interval: tuple[sp.Rational, sp.Rational] | None

    @property
    def is_rational(self) -> bool:
        return self.alpha is None


def _parse_expr(text: str, local_symbols: Mapping[str, sp.Symbol]) -> sp.Expr:
    if not isinstance(text, str):
        raise ValueError("polynomial data must be strings")
    expression = sp.sympify(text, locals=dict(local_symbols), evaluate=True)
    allowed = set(local_symbols.values())
    if not expression.free_symbols.issubset(allowed):
        raise ValueError("expression contains undeclared symbols")
    if expression.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
        raise ValueError("non-finite expression")
    return sp.cancel(expression)


def parse_field(raw: Mapping[str, Any]) -> CoefficientField:
    kind = raw.get("type")
    if kind == "rational":
        return CoefficientField(None, None, None)
    if kind != "real_algebraic":
        raise ValueError("unsupported coefficient field")
    name = raw.get("symbol")
    if not isinstance(name, str) or not name.isidentifier():
        raise ValueError("invalid primitive-element symbol")
    alpha = sp.Symbol(name)
    polynomial_expr = _parse_expr(raw.get("minimal_polynomial"), {name: alpha})
    polynomial = sp.Poly(polynomial_expr, alpha, domain=sp.QQ)
    if polynomial.degree() < 1 or polynomial.LC() == 0:
        raise ValueError("minimal polynomial must be nonconstant")
    polynomial = sp.Poly(polynomial.monic(), alpha, domain=sp.QQ)
    if not polynomial.is_sqf:
        raise ValueError("minimal polynomial must be square-free")
    if not polynomial.is_irreducible:
        raise ValueError("minimal polynomial must be irreducible over Q")
    interval_raw = raw.get("isolating_interval")
    if not isinstance(interval_raw, list) or len(interval_raw) != 2:
        raise ValueError("isolating interval must contain two rational endpoints")
    lo, hi = map(sp.Rational, interval_raw)
    if not lo < hi:
        raise ValueError("isolating interval endpoints are not ordered")
    if polynomial.eval(lo) == 0 or polynomial.eval(hi) == 0:
        raise ValueError("isolating interval endpoints may not be roots")
    if polynomial.count_roots(lo, hi) != 1:
        raise ValueError("interval does not isolate exactly one real root")
    return CoefficientField(alpha, polynomial, (lo, hi))


def _ensure_field_element(expression: sp.Expr, field: CoefficientField) -> None:
    """Reject radicals or transcendental constants not represented by alpha."""
    expression = sp.cancel(expression)
    numerator, denominator = sp.fraction(expression)
    if field.is_rational:
        if not (numerator.is_Rational and denominator.is_Rational):
            raise ValueError("coordinate is not rational in the declared field")
        return
    assert field.alpha is not None
    try:
        sp.Poly(numerator, field.alpha, domain=sp.QQ)
        sp.Poly(denominator, field.alpha, domain=sp.QQ)
    except Exception as exc:
        raise ValueError("coordinate is not a rational function of the primitive element") from exc


def _reduce_coefficient(expression: sp.Expr, field: CoefficientField) -> sp.Expr:
    expression = sp.cancel(expression)
    if field.is_rational:
        if expression.free_symbols:
            raise ValueError("nonrational coefficient in rational field")
        return sp.Rational(expression)
    assert field.alpha is not None and field.minimal_polynomial is not None
    numerator, denominator = sp.fraction(expression)
    num_poly = sp.Poly(numerator, field.alpha, domain=sp.QQ)
    den_poly = sp.Poly(denominator, field.alpha, domain=sp.QQ)
    mod = field.minimal_polynomial
    denominator_gcd = sp.gcd(den_poly, mod)
    if denominator_gcd.degree() > 0:
        raise ValueError("coefficient denominator vanishes in the number field")
    inverse = sp.invert(den_poly, mod)
    residue = (num_poly * inverse).rem(mod)
    return sp.expand(residue.as_expr())


def _is_zero_over_field(expression: sp.Expr, variables: Sequence[sp.Symbol], field: CoefficientField) -> bool:
    expression = sp.together(sp.expand(expression))
    numerator, denominator = sp.fraction(expression)
    # Denominators are allowed only in the coefficient field, never in system variables.
    if any(variable in denominator.free_symbols for variable in variables):
        raise ValueError("certificate expression is not polynomial in the system variables")
    polynomial = sp.Poly(numerator, *variables, domain="EX") if variables else None
    coefficients = polynomial.coeffs() if polynomial is not None else [numerator]
    if any(_reduce_coefficient(coefficient / denominator, field) != 0 for coefficient in coefficients):
        return False
    return True


def _declare_variables(raw: Any, field: CoefficientField) -> tuple[tuple[sp.Symbol, ...], dict[str, sp.Symbol]]:
    if not isinstance(raw, list) or any(not isinstance(name, str) or not name.isidentifier() for name in raw):
        raise ValueError("variables must be identifier strings")
    if len(set(raw)) != len(raw):
        raise ValueError("variables must be distinct")
    if field.alpha is not None and field.alpha.name in raw:
        raise ValueError("system variable collides with primitive element")
    variables = tuple(sp.Symbol(name) for name in raw)
    symbols = {var.name: var for var in variables}
    if field.alpha is not None:
        symbols[field.alpha.name] = field.alpha
    return variables, symbols


def verify_sample_yes(data: Mapping[str, Any]) -> None:
    field = parse_field(data.get("coefficient_field", {}))
    variables, symbols = _declare_variables(data.get("variables"), field)
    equations_raw = data.get("equations")
    values_raw = data.get("values")
    if not isinstance(equations_raw, list) or not isinstance(values_raw, list) or len(values_raw) != len(variables):
        raise ValueError("malformed equations or values")
    equations = [_parse_expr(text, symbols) for text in equations_raw]
    values = [_parse_expr(text, symbols) for text in values_raw]
    if any(value.free_symbols - ({field.alpha} if field.alpha is not None else set()) for value in values):
        raise ValueError("sample coordinates may depend only on the primitive element")
    for value in values:
        _ensure_field_element(value, field)
    substitution = dict(zip(variables, values))
    for index, equation in enumerate(equations):
        if not _is_zero_over_field(equation.subs(substitution), (), field):
            raise ValueError(f"equation {index} does not vanish at the sample point")


def verify_nullstellensatz_no(data: Mapping[str, Any]) -> None:
    field = parse_field(data.get("coefficient_field", {}))
    variables, symbols = _declare_variables(data.get("variables"), field)
    equations_raw = data.get("equations")
    squares_raw = data.get("sum_of_squares")
    multipliers_raw = data.get("multipliers")
    if not isinstance(equations_raw, list) or not isinstance(squares_raw, list) or not isinstance(multipliers_raw, list):
        raise ValueError("malformed identity lists")
    if len(multipliers_raw) != len(equations_raw):
        raise ValueError("one ideal multiplier is required for each equation")
    equations = [_parse_expr(text, symbols) for text in equations_raw]
    squares = [_parse_expr(text, symbols) for text in squares_raw]
    multipliers = [_parse_expr(text, symbols) for text in multipliers_raw]
    identity = sp.Integer(1) + sum((s * s for s in squares), sp.Integer(0))
    identity += sum((q * f for q, f in zip(multipliers, equations)), sp.Integer(0))
    if not _is_zero_over_field(identity, variables, field):
        raise ValueError("claimed Real-Nullstellensatz identity is false")


def verify_certificate(data: Mapping[str, Any]) -> str:
    kind = data.get("certificate_type")
    if kind == "real_algebraic_sample_yes":
        verify_sample_yes(data)
        return "YES_CERTIFICATE_OK"
    if kind == "real_nullstellensatz_no":
        verify_nullstellensatz_no(data)
        return "NO_CERTIFICATE_OK"
    raise ValueError("unsupported certificate type")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text())
    print(verify_certificate(data))


if __name__ == "__main__":
    main()
