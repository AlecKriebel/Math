#!/usr/bin/env python3
"""Exact search evidence for wreath-product monodromy of F composed with F.

This script derives the degree-nine fiber polynomial of G = F o F at a
rational target. If PARI/GP is installed, it also asks polgalois for the
arithmetic Galois group. The publication proof is geometric and does not rely
on polgalois; this is an independent arithmetic check.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import sympy as sp


t, r = sp.symbols("t r")


@dataclass(frozen=True)
class FiberCertificate:
    target: tuple[int, int, int]
    outer_cubic: sp.Poly
    degree_nine: sp.Poly


def fiber_polynomial(target: tuple[int, int, int]) -> FiberCertificate:
    """Return the primitive integral degree-nine fiber polynomial."""
    a, b, c = map(sp.Rational, target)
    outer = sp.Poly(2 * a * t**3 - b * t**2 + 2 * t - c, t)

    y = sp.cancel(-(b * t**2 + 3 * c - 6 * t) / (2 * t**2))
    x = sp.cancel(t / (1 - t * y))
    z = sp.cancel((2 * x - 3 * x**2 * y - c) / x**3)

    inner = sp.cancel(2 * x * r**3 - y * r**2 + 2 * r - z)
    inner_num = sp.fraction(inner)[0]

    resultant = sp.Poly(sp.resultant(outer.as_expr(), inner_num, t), r,
                        domain=sp.QQ)
    integral = resultant.clear_denoms()[1].primitive()[1]
    assert integral.degree() == 9
    return FiberCertificate(target, outer, integral)


def pari_galois(poly: sp.Poly) -> str | None:
    gp = shutil.which("gp") or "/opt/homebrew/bin/gp"
    if not Path(gp).exists():
        return None
    expr = str(poly.as_expr()).replace("**", "^")
    result = subprocess.run(
        [gp, "-fq"],
        input=f"p={expr}; print(polgalois(p))\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=300,
    )
    return result.stdout.strip()


def main() -> None:
    targets = [(1, 2, 3), (2, 3, 5), (1, 1, 2), (2, -1, 3), (3, 2, 1)]
    for target in targets:
        cert = fiber_polynomial(target)
        factors = sp.factor_list(cert.degree_nine.as_expr())[1]
        assert len(factors) == 1 and sp.degree(factors[0][0], r) == 9
        print(f"target={target}")
        print(f"outer={cert.outer_cubic.as_expr()}")
        print(f"fiber={cert.degree_nine.as_expr()}")
        answer = pari_galois(cert.degree_nine)
        if answer is not None:
            print(f"PARI polgalois: {answer}")
        print()


if __name__ == "__main__":
    main()
