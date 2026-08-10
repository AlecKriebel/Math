#!/usr/bin/env python3
"""Independent exact checks for directed-containment and open-cube signs."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path
import re


def compact_sha(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def necessary_containment_mask(source: bytes, target: bytes) -> bool:
    """Return the invariant-deck necessary condition for source <= target.

    A set bit means that the corresponding invariant pullback is not the zero
    polynomial.  Source containment in target implies I(target) subset I(source),
    hence nonzero(source) subset nonzero(target).
    """
    if len(source) != len(target):
        return False
    return all((s & (~t & 0xFF)) == 0 for s, t in zip(source, target))


def strict_separator_valid(source_zero: bool, target_sign: int) -> bool:
    """A source identity plus a fixed nonzero target sign gives disjointness."""
    return source_zero and target_sign in (-1, 1)


def _symbol_number(name: str) -> tuple[str, int, str]:
    match = re.fullmatch(r"([^0-9]*)([0-9]+)", name)
    return (match.group(1), int(match.group(2)), name) if match else (name, -1, name)


def bernstein_strict_sign(poly, symbols, max_elevation: int = 3) -> int:
    """Certify a strict sign on (0,1)^n from exact Bernstein coefficients.

    Returns +1 or -1.  Raises when this sufficient certificate does not decide
    the sign.  Zero Bernstein coefficients are harmless on the open cube:
    every basis function is strictly positive there.
    """
    import sympy as sp

    p = sp.Poly(sp.expand(poly), *symbols, domain=sp.QQ)
    if p.is_zero:
        raise ValueError("zero polynomial has no strict sign")
    base_degree = tuple(p.degree(x) for x in symbols)
    terms = [(tuple(m), Fraction(int(c.p), int(c.q))) for m, c in p.terms()]
    for elevation in range(max_elevation + 1):
        degree = tuple(d + elevation for d in base_degree)
        coefficients = []
        for index in product(*(range(d + 1) for d in degree)):
            value = Fraction(0)
            for exponent, coefficient in terms:
                if all(a <= k for a, k in zip(exponent, index)):
                    multiplier = Fraction(1)
                    for a, k, d in zip(exponent, index, degree):
                        multiplier *= Fraction(comb(k, a), comb(d, a))
                    value += coefficient * multiplier
            coefficients.append(value)
        if all(c >= 0 for c in coefficients) and any(c > 0 for c in coefficients):
            return 1
        if all(c <= 0 for c in coefficients) and any(c < 0 for c in coefficients):
            return -1
    raise ValueError("Bernstein certificate did not decide the factor sign")


def verify_sign_record(record: dict) -> dict:
    """Rebuild one factored sign certificate without trusting stored signs."""
    import sympy as sp

    certificate = record["certificate"]
    expression = sp.sympify(certificate["expression"])
    symbols = tuple(sorted(expression.free_symbols, key=lambda x: _symbol_number(str(x))))
    coefficient = sp.Rational(certificate["coefficient"])
    rebuilt = coefficient
    total_sign = 1 if coefficient > 0 else -1 if coefficient < 0 else 0
    checked = []
    for item in certificate["factors"]:
        factor = sp.sympify(item["factor"])
        exponent = int(item["exponent"])
        rebuilt *= factor**exponent
        sign = bernstein_strict_sign(factor, symbols)
        if sign != int(item["sign"]):
            raise AssertionError((item["factor"], sign, item["sign"]))
        total_sign *= sign**exponent
        checked.append((item["factor"], exponent, sign))
    if sp.expand(expression - rebuilt) != 0:
        raise AssertionError("stored factors do not multiply to the expression")
    if total_sign != int(certificate["total_sign"]):
        raise AssertionError((total_sign, certificate["total_sign"]))
    if not strict_separator_valid(True, total_sign):
        raise AssertionError("certificate does not prove a strict separator")
    return {
        "certificate_sha256": compact_sha(certificate),
        "factor_count": len(checked),
        "recomputed_total_sign": total_sign,
    }


def audit_library(path: Path) -> dict:
    data = json.loads(path.read_text())
    records = [verify_sign_record(record) for record in data["records"]]
    return {
        "path": str(path),
        "records": len(records),
        "all_recomputed": True,
        "certificate_hashes": [record["certificate_sha256"] for record in records],
    }


def self_test() -> dict:
    assert necessary_containment_mask(bytes([0b0011]), bytes([0b0111]))
    assert not necessary_containment_mask(bytes([0b0111]), bytes([0b0011]))
    assert strict_separator_valid(True, 1)
    assert strict_separator_valid(True, -1)
    assert not strict_separator_valid(False, 1)
    assert not strict_separator_valid(True, 0)
    return {
        "bit_meaning": "1 iff the invariant pullback is a nonzero polynomial",
        "necessary_relation": "ones(source) subseteq ones(target)",
        "strict_separator": "source pullback zero; target pullback fixed nonzero sign",
        "mutation_reversal_rejected": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("libraries", nargs="*", type=Path)
    args = parser.parse_args()
    result = {"logic": self_test(), "libraries": [audit_library(p) for p in args.libraries]}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

