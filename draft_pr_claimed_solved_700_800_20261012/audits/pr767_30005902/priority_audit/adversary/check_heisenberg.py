"""Supplementary exact checks; the proof for all polynomials is in REPORT.md.

No external packages, files, network, or finite27 audit inputs are used.
"""

from collections import defaultdict
from math import comb
import json


def need(condition, description):
    """Require an exact equality even when Python runs with optimization."""
    if not condition:
        raise RuntimeError(description)


def add(*polys):
    out = defaultdict(int)
    for poly in polys:
        for monomial, coefficient in poly.items():
            out[monomial] += coefficient
    return {m: c for m, c in out.items() if c}


def neg(poly):
    return {m: -c for m, c in poly.items()}


def partial(poly, index):
    out = {}
    for monomial, coefficient in poly.items():
        degree = monomial[index]
        if degree:
            shifted = list(monomial)
            shifted[index] -= 1
            out[tuple(shifted)] = coefficient * degree
    return out


def multiply_variable(poly, index):
    out = {}
    for monomial, coefficient in poly.items():
        shifted = list(monomial)
        shifted[index] += 1
        out[tuple(shifted)] = coefficient
    return out


def coproduct_monomial(monomial):
    """Expand Δ(x^i y^j z^k) exactly in the 6-variable tensor monomials."""
    i, j, k = monomial
    terms = defaultdict(int)
    for x_left in range(i + 1):
        for y_left in range(j + 1):
            for z_left in range(k + 1):
                for z_right in range(k - z_left + 1):
                    cross = k - z_left - z_right
                    left = (x_left + cross, y_left, z_left)
                    right = (i - x_left, j - y_left + cross, z_right)
                    coefficient = (
                        comb(i, x_left)
                        * comb(j, y_left)
                        * comb(k, z_left)
                        * comb(k - z_left, z_right)
                    )
                    terms[(left, right)] += coefficient
    return dict(terms)


def translated(poly, index, side):
    wanted = tuple(int(i == index) for i in range(3))
    out = defaultdict(int)
    for monomial, coefficient in poly.items():
        for (left, right), factor in coproduct_monomial(monomial).items():
            if side == "R" and left == wanted:
                out[right] += coefficient * factor
            if side == "L" and right == wanted:
                out[left] += coefficient * factor
    return {m: c for m, c in out.items() if c}


def explicit(poly, index, side):
    ans = partial(poly, index)
    if side == "R" and index == 0:
        ans = add(ans, multiply_variable(partial(poly, 2), 1))
    if side == "L" and index == 1:
        ans = add(ans, multiply_variable(partial(poly, 2), 0))
    return ans


def commutator(poly, side):
    return add(
        translated(translated(poly, 1, side), 0, side),
        neg(translated(translated(poly, 0, side), 1, side)),
    )


checks = 0
monomials = 0
for total in range(7):
    for i in range(total + 1):
        for j in range(total - i + 1):
            k = total - i - j
            poly = {(i, j, k): 1}
            monomials += 1
            for side in ("L", "R"):
                for index in range(3):
                    need(
                        translated(poly, index, side) == explicit(poly, index, side),
                        f"Translation formula failed for {poly}, {side}, index {index}",
                    )
                    checks += 1
            need(
                commutator(poly, "L") == partial(poly, 2),
                f"Left commutator formula failed for {poly}",
            )
            need(
                commutator(poly, "R") == neg(partial(poly, 2)),
                f"Right commutator formula failed for {poly}",
            )
            checks += 2

need(
    commutator({(0, 0, 1): 1}, "R") == {(0, 0, 0): -1},
    "Right commutator evaluated on z must be -1",
)
checks += 1
print(json.dumps({
    "status": "PASS",
    "coefficient_ring": "integers, hence valid after extension to Q",
    "monomials_tested": monomials,
    "maximum_total_degree": 6,
    "exact_equalities_tested": checks,
    "scope": "Supplementary bounded computation; generator/derivation proof handles all H.",
    "target_bracket_on_z": -1,
    "left_bracket_on_z": 1,
}, indent=2))
