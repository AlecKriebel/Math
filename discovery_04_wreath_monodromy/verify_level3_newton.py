#!/usr/bin/env python3
"""Independent PARI check of the degree-27 Newton edge for F^3.

SymPy constructs the exact tower equations; PARI performs both nested
resultants.  Common factors depending only on s shift every coefficient
valuation equally and therefore do not affect the Newton edge.
"""

from __future__ import annotations

import ast
import re
import shutil
import subprocess
from pathlib import Path

import sympy as sp


s, t, r, q = sp.symbols("s t r q")


def reconstruct(A: sp.Expr, B: sp.Expr, C: sp.Expr, T: sp.Symbol) -> tuple[sp.Expr, ...]:
    Y = sp.cancel(-(B * T**2 + 3 * C - 6 * T) / (2 * T**2))
    X = sp.cancel(T / (1 - T * Y))
    Z = sp.cancel((2 * X - 3 * X**2 * Y - C) / X**3)
    return X, Y, Z


def to_gp(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def lower_hull(values: list[int]) -> list[tuple[int, int]]:
    hull: list[tuple[int, int]] = []
    for point in enumerate(values):
        while len(hull) >= 2:
            left, middle = hull[-2], hull[-1]
            cross = (middle[0] - left[0]) * (point[1] - middle[1]) - (
                middle[1] - left[1]
            ) * (point[0] - middle[0])
            if cross <= 0:
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


def main() -> None:
    gp = shutil.which("gp") or "/opt/homebrew/bin/gp"
    if not Path(gp).exists():
        raise SystemExit("PARI/GP is required for this optional level-three check")

    X1 = reconstruct(1, 2, s, t)
    C0 = 2 * t**3 - 2 * t**2 + 2 * t - s
    C1 = sp.together(2 * X1[0] * r**3 - X1[1] * r**2 + 2 * r - X1[2])
    C1 = C1.as_numer_denom()[0]
    X2 = reconstruct(*X1, r)
    C2 = sp.together(2 * X2[0] * q**3 - X2[1] * q**2 + 2 * q - X2[2])
    C2 = C2.as_numer_denom()[0]

    program = "\n".join(
        [
            "default(parisizemax,2000000000);",
            "default(breakloop,0);",
            "t='t; r='r; q='q; s='s;",
            f"C0={to_gp(C0)};",
            f"C1={to_gp(C1)};",
            f"C2={to_gp(C2)};",
            "R1=polresultant(C1,C2,r);",
            "R2=polresultant(C0,R1,t);",
            'print("QDEG=",poldegree(R2,q));',
            'print("DEGREES=",vector(28,i,poldegree(polcoef(R2,i-1,q),s)));',
            "quit;",
        ]
    )
    result = subprocess.run(
        [gp, "-fq"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=300,
    )
    marked_lines = [
        line
        for stream in (result.stdout, result.stderr)
        for line in stream.splitlines()
        if "***" in line and "Warning:" not in line
    ]
    assert not marked_lines, "\n".join(marked_lines)
    assert "QDEG=27" in result.stdout
    match = re.search(r"DEGREES=(\[[^\n]+\])", result.stdout)
    assert match is not None
    degrees = ast.literal_eval(match.group(1))
    expected = [
        244, 240, 241, 240, 238, 237, 236, 234, 233, 232, 230, 229,
        228, 226, 226, 225, 223, 222, 221, 219, 218, 217, 215, 214,
        213, 211, 210, 210,
    ]
    assert degrees == expected
    valuations = [max(degrees) - degree for degree in degrees]
    assert lower_hull(valuations) == [(0, 0), (27, 34)]
    print("PASS level 3: degree 27; one Newton edge (0,0)-(27,34)")


if __name__ == "__main__":
    main()
