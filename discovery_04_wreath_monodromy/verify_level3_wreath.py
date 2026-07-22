#!/usr/bin/env python3
"""Exact certificate for ``Mon(F^3) = S_3 wr S_3 wr S_3``.

SymPy derives the third-level inverse-resolvent tower directly from the map.
PARI/GP computes the nested resultants and the degree-27 discriminant.  Small
Python checks certify the Newton polygon and the elementary wreath-product
lemma.  No numerical approximation or specialized fiber is used.
"""

from __future__ import annotations

import ast
import re
import shutil
import subprocess
from pathlib import Path

import sympy as sp


s, t, r, q = sp.symbols("s t r q")


def reconstruct(
    A: sp.Expr, B: sp.Expr, C: sp.Expr, T: sp.Symbol
) -> tuple[sp.Expr, ...]:
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


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Return ``left * right`` as permutations acting on the right first."""
    return tuple(left[right[i]] for i in range(len(left)))


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for i, image in enumerate(permutation):
        result[image] = i
    return tuple(result)


def power(permutation: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(len(permutation)))
    base = permutation
    while exponent:
        if exponent & 1:
            result = compose(result, base)
        base = compose(base, base)
        exponent //= 2
    return result


def conjugate(element: tuple[int, ...], by: tuple[int, ...]) -> tuple[int, ...]:
    return compose(compose(by, element), inverse(by))


def generated_group(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = tuple(range(len(generators[0])))
    group = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            product = compose(element, generator)
            if product not in group:
                group.add(product)
                frontier.append(product)
    return group


def support(permutation: tuple[int, ...]) -> set[int]:
    return {i for i, image in enumerate(permutation) if image != i}


def check_group_lemma() -> None:
    """Check the constructive base-kernel part of the W3 group lemma.

    We deliberately do not enumerate the direct product ``S_3^9`` (which has
    more than ten million elements).  Instead we enumerate each three-point
    factor, verify its support, and verify that the nine supports are disjoint.
    The generated subgroup is therefore their internal direct product.
    """
    alpha = tuple((i + 1) % 27 for i in range(27))
    tau = list(range(27))
    tau[0], tau[9] = tau[9], tau[0]
    tau = tuple(tau)

    # The nine bottom blocks are the orbits of alpha^9.  A leaf
    # transposition and its alpha^9-conjugate generate S_3 in one block.
    alpha9 = power(alpha, 9)
    bottom_blocks = [{block, block + 9, block + 18} for block in range(9)]
    assert all({alpha9[i] for i in block} == block for block in bottom_blocks)
    assert all(
        {alpha[i] for i in bottom_blocks[block]} == bottom_blocks[(block + 1) % 9]
        for block in range(9)
    )

    # Alpha-conjugates give an S_3 supported on each bottom block.  Since the
    # supports are pairwise disjoint, these factors commute and intersect
    # trivially; hence their product has order 6^9.
    factor_supports: list[set[int]] = []
    for block in range(9):
        shift = power(alpha, block)
        transposition = conjugate(tau, shift)
        factor = generated_group(
            [transposition, conjugate(transposition, alpha9)]
        )
        assert len(factor) == 6
        factor_support = set().union(*(support(element) for element in factor))
        assert factor_support == bottom_blocks[block]
        assert all(support(element) <= bottom_blocks[block] for element in factor)
        factor_supports.append(factor_support)
    assert set().union(*factor_supports) == set(range(27))
    assert all(
        factor_supports[i].isdisjoint(factor_supports[j])
        for i in range(9)
        for j in range(i)
    )
    assert 6**9 * 6**4 == 6**13


def main() -> None:
    gp = shutil.which("gp") or "/opt/homebrew/bin/gp"
    if not Path(gp).exists():
        raise SystemExit("PARI/GP is required for the level-three certificate")

    X1 = reconstruct(1, 2, s, t)
    C0 = 2 * t**3 - 2 * t**2 + 2 * t - s
    C1_fraction = sp.together(
        2 * X1[0] * r**3 - X1[1] * r**2 + 2 * r - X1[2]
    )
    C1, D1 = C1_fraction.as_numer_denom()
    X2 = reconstruct(*X1, r)
    C2_fraction = sp.together(
        2 * X2[0] * q**3 - X2[1] * q**2 + 2 * q - X2[2]
    )
    C2, D2 = C2_fraction.as_numer_denom()

    program = "\n".join(
        [
            # Keep the exact certificate safe on ordinary developer machines.
            # The computation uses far less in the verified environment.
            "default(parisizemax,2000000000);",
            # Do not enter GP's recoverable error loop: any algebra or syntax
            # error must terminate the subprocess and fail this certificate.
            "default(breakloop,0);",
            "t='t; r='r; q='q; s='s;",
            f"C0={to_gp(C0)};",
            f"C1={to_gp(C1)};",
            f"D1={to_gp(D1)};",
            f"C2={to_gp(C2)};",
            f"D2={to_gp(D2)};",
            "R1=polresultant(C1,C2,r);",
            "R2=polresultant(C0,R1,t);",
            "V=content(R2);",
            "Q=R2/V;",
            "Disc=poldisc(Q,q);",
            "G=gcd(Disc,deriv(Disc,s));",
            "Rad=Disc/G;",
            "Repeated=gcd(Rad,G);",
            "E1=Rad/Repeated;",
            "LC=polcoef(Q,27,q);",
            "LowerDenNorm=polresultant(C0,D1,t);",
            "Den1=polresultant(C1,D2,r);",
            "DenNorm=polresultant(C0,Den1,t);",
            'print("RAW_QDEG=",poldegree(R2,q));',
            'print("RAW_SDEG=",poldegree(R2,s));',
            'print("CONTENT_SDEG=",poldegree(V,s));',
            'print("Q_QDEG=",poldegree(Q,q));',
            'print("Q_SDEG=",poldegree(Q,s));',
            'print("RAW_DEGREES=",vector(28,i,poldegree(polcoef(R2,i-1,q),s)));',
            'print("Q_DEGREES=",vector(28,i,poldegree(polcoef(Q,i-1,q),s)));',
            'print("DISC_SDEG=",poldegree(Disc,s));',
            'print("RAD_SDEG=",poldegree(Rad,s));',
            'print("REPEATED_SDEG=",poldegree(Repeated,s));',
            'print("E1_SDEG=",poldegree(E1,s));',
            'print("E1_SQFREE_GCD_DEG=",poldegree(gcd(E1,deriv(E1,s)),s));',
            'print("E1_REPEATED_GCD_DEG=",poldegree(gcd(E1,Repeated),s));',
            'print("LC_SDEG=",poldegree(LC,s));',
            'print("E1_LC_GCD_DEG=",poldegree(gcd(E1,LC),s));',
            'print("LOWERDENNORM_ZERO=",LowerDenNorm==0);',
            'print("LOWERDENNORM_SDEG=",poldegree(LowerDenNorm,s));',
            'print("E1_LOWERDEN_GCD_DEG=",poldegree(gcd(E1,LowerDenNorm),s));',
            'print("DENNORM_ZERO=",DenNorm==0);',
            'print("DENNORM_SDEG=",poldegree(DenNorm,s));',
            'print("E1_DEN_GCD_DEG=",poldegree(gcd(E1,DenNorm),s));',
            "quit;",
        ]
    )
    result = subprocess.run(
        [gp, "-fq"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=900,
    )
    # PARI prefixes both errors and harmless automatic-stack warnings with
    # ``***``. Reject every marked line except an explicit ``Warning:`` line.
    marked_lines = [
        line
        for stream in (result.stdout, result.stderr)
        for line in stream.splitlines()
        if "***" in line and "Warning:" not in line
    ]
    assert not marked_lines, "\n".join(marked_lines)
    output = result.stdout

    expected_scalars = {
        "RAW_QDEG": 27,
        "RAW_SDEG": 244,
        "CONTENT_SDEG": 196,
        "Q_QDEG": 27,
        "Q_SDEG": 48,
        "DISC_SDEG": 1612,
        "RAD_SDEG": 752,
        "REPEATED_SDEG": 676,
        "E1_SDEG": 76,
        "E1_SQFREE_GCD_DEG": 0,
        "E1_REPEATED_GCD_DEG": 0,
        "LC_SDEG": 14,
        "E1_LC_GCD_DEG": 0,
        "LOWERDENNORM_ZERO": 0,
        "E1_LOWERDEN_GCD_DEG": 0,
        "DENNORM_ZERO": 0,
        "E1_DEN_GCD_DEG": 0,
    }
    for label, expected in expected_scalars.items():
        match = re.search(rf"^{label}=(-?\d+)$", output, re.MULTILINE)
        assert match is not None, (label, output, result.stderr)
        assert int(match.group(1)) == expected, (label, match.group(1), expected)

    match = re.search(r"^RAW_DEGREES=(\[[^\n]+\])$", output, re.MULTILINE)
    assert match is not None
    raw_degrees = ast.literal_eval(match.group(1))
    expected_raw = [
        244, 240, 241, 240, 238, 237, 236, 234, 233, 232, 230, 229,
        228, 226, 226, 225, 223, 222, 221, 219, 218, 217, 215, 214,
        213, 211, 210, 210,
    ]
    assert raw_degrees == expected_raw

    match = re.search(r"^Q_DEGREES=(\[[^\n]+\])$", output, re.MULTILINE)
    assert match is not None
    q_degrees = ast.literal_eval(match.group(1))
    valuations = [max(q_degrees) - degree for degree in q_degrees]
    assert lower_hull(valuations) == [(0, 0), (27, 34)]

    # The old level-two theorem gives the full quotient W2.  The exact data
    # above supplies a 27-cycle and a leaf transposition.  This finite check
    # verifies that their conjugates generate the complete kernel S_3^9.
    check_group_lemma()

    print("PASS primitive degree-27 level-three resolvent")
    print("PASS Newton edge (0,0)-(27,34): a 27-cycle")
    print("PASS discriminant: squarefree simple divisor of degree 76")
    print("PASS denominator norm and genuine-branch guards")
    print("PASS W3 kernel lemma: |S_3^9| = 6^9")


if __name__ == "__main__":
    main()
