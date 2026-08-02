#!/usr/bin/env python3
"""Exact radial-union audit for the 120- and 600-point golden H4 orbits.

The 600-point orbit consists of the scaled centroids constructed in
``h4_dual_subset_search.py``.  This checker proves two family-wide negative
results for the mixed-orbit counterexample route.

* The union of the two full antipodal orbits is always five-colorable (in
  fact its diameter graph is a disjoint union of matchings).
* Choose either orientation of every one of the 60 root lines and every one
  of the 300 dual lines, independently.  At every positive radial ratio the
  resulting 360-point diameter graph is five-colorable.

The second statement covers all 2^360 oriented projective representatives.
Three explicit negative signed cycles force the same extreme product in
every switching.  Consequently the radial upper envelope has only two
transition radii.  All arithmetic and all coloring checks are exact.
"""

from __future__ import annotations

import argparse
import collections
import functools
import hashlib
import math
from dataclasses import dataclass
from typing import Iterable, Sequence

from h4_dual_subset_search import (
    Point,
    Quadratic,
    dual_centroid_orbit,
    qcompare,
    qdot,
    qsign,
    qsub,
)


def qneg(value: Quadratic) -> Quadratic:
    return -value[0], -value[1]


def qadd(left: Quadratic, right: Quadratic) -> Quadratic:
    return left[0] + right[0], left[1] + right[1]


def qscale(multiplier: int, value: Quadratic) -> Quadratic:
    return multiplier * value[0], multiplier * value[1]


def qabs(value: Quadratic) -> Quadratic:
    return value if qsign(value) >= 0 else qneg(value)


def negate(point: Point) -> Point:
    return tuple(qneg(coordinate) for coordinate in point)  # type: ignore[return-value]


def canonical_lines(points: Iterable[Point]) -> list[Point]:
    return sorted({max(point, negate(point)) for point in points})


def exact_sorted(values: Iterable[Quadratic]) -> list[Quadratic]:
    return sorted(set(values), key=functools.cmp_to_key(qcompare))


ROOT_NORM: Quadratic = (16, 0)
DUAL_NORM: Quadratic = (112, 48)
ROOT_EXTREME: Quadratic = (4, 4)
DUAL_EXTREME: Quadratic = (104, 48)
CROSS_EXTREME: Quadratic = (28, 12)


# (product, number of 120-by-600 ordered cross pairs, root degree, dual degree)
EXPECTED_CROSS_SPECTRUM = (
    ((-28, -12), 2400, 20, 4),
    ((-20, -12), 2400, 20, 4),
    ((-24, -8), 3600, 30, 6),
    ((-16, -8), 7200, 60, 12),
    ((-12, -4), 7200, 60, 12),
    ((-4, -4), 7200, 60, 12),
    ((-8, 0), 2400, 20, 4),
    ((0, 0), 7200, 60, 12),
    ((8, 0), 2400, 20, 4),
    ((4, 4), 7200, 60, 12),
    ((12, 4), 7200, 60, 12),
    ((16, 8), 7200, 60, 12),
    ((24, 8), 3600, 30, 6),
    ((20, 12), 2400, 20, 4),
    ((28, 12), 2400, 20, 4),
)


# These line colors are the earlier five-color certificate for the
# |dot|=4+4sqrt(5) root-line relation, permuted into canonical_lines order.
ROOT_LINE_COLORS = (
    0, 2, 1, 2, 3, 2, 0, 0, 3, 1, 4, 1, 3, 4, 4, 2, 4, 2, 2, 0,
    0, 1, 4, 0, 1, 1, 4, 1, 4, 2, 1, 2, 1, 2, 4, 0, 0, 0, 4, 2,
    3, 2, 4, 2, 3, 3, 1, 1, 3, 3, 4, 0, 3, 3, 1, 0, 0, 3, 4, 3,
)


# Three-colors the complete 600-vertex oriented relation dot=-104-48sqrt(5).
# Vertex order is the K4 order returned by dual_centroid_orbit().
DUAL_EXTREME_COLORS = (
    "000000000000000000000000000000000000010000000000000000001000"
    "000000000000000000000000100000001100101000001010000000000000"
    "000000000101001000000000000000010000000000000001000000101001"
    "010000000000000000010100000100001110000001011100010110000000"
    "000000001000000011000001001000000001021010122022221111111101"
    "112211111112012121112212221111122110212220221221112222122022"
    "022201121212012111110122211111222222222112121111111211111111"
    "111111111110201211210222121212222210112202222111112222122221"
    "222121111122211222211211111111221212121221112202112111111111"
    "111211111121111111111111111111111111111111111111112211111111"
)


# Switching-cycle vertices use canonical root-line indices 0..59, canonical
# dual-line indices 0..299, and (for CROSS_CYCLE) the concatenated order with
# dual indices shifted by 60.
ROOT_CYCLE = (0, 2, 12, 13, 3, 0)
DUAL_CYCLE = (0, 3, 7, 56, 97, 57, 131, 49, 137, 129, 55, 133, 53, 99, 59, 0)
CROSS_CYCLE = (0, 70, 5, 62, 11, 82, 10, 63, 4, 71, 0)


def verify_cross_spectrum(roots: Sequence[Point], duals: Sequence[Point]) -> None:
    counter = collections.Counter(qdot(root, dual) for root in roots for dual in duals)
    ordered = exact_sorted(counter)
    actual = []
    for product in ordered:
        root_degrees = {
            sum(qdot(root, dual) == product for dual in duals) for root in roots
        }
        dual_degrees = {
            sum(qdot(root, dual) == product for root in roots) for dual in duals
        }
        assert len(root_degrees) == len(dual_degrees) == 1
        actual.append(
            (product, counter[product], root_degrees.pop(), dual_degrees.pop())
        )
    assert tuple(actual) == EXPECTED_CROSS_SPECTRUM
    assert sum(counter.values()) == 120 * 600
    assert DUAL_NORM == qscale(4, CROSS_EXTREME)


def verify_centroid_incidence(
    roots: Sequence[Point], cliques: Sequence[tuple[int, int, int, int]],
    duals: Sequence[Point]
) -> None:
    """The positive cross extreme is exactly root--K4 incidence."""
    assert len(cliques) == len(duals) == 600
    for clique, dual in zip(cliques, duals):
        incident = {i for i, root in enumerate(roots) if qdot(root, dual) == CROSS_EXTREME}
        assert incident == set(clique)


def cycle_sign(
    points: Sequence[Point], cycle: Sequence[int], magnitude: Quadratic
) -> tuple[int, str]:
    product = 1
    word = []
    for left, right in zip(cycle, cycle[1:]):
        value = qdot(points[left], points[right])
        assert qabs(value) == magnitude
        sign = qsign(value)
        assert sign in (-1, 1)
        product *= sign
        word.append("+" if sign > 0 else "-")
    return product, "".join(word)


def verify_projective_extremes(
    root_lines: Sequence[Point], dual_lines: Sequence[Point]
) -> tuple[str, str, str]:
    assert len(root_lines) == 60 and len(dual_lines) == 300

    root_absolute = [
        qabs(qdot(root_lines[i], root_lines[j]))
        for i in range(60) for j in range(i)
    ]
    dual_absolute = [
        qabs(qdot(dual_lines[i], dual_lines[j]))
        for i in range(300) for j in range(i)
    ]
    cross_absolute = [qabs(qdot(root, dual)) for root in root_lines for dual in dual_lines]
    assert max(root_absolute, key=functools.cmp_to_key(qcompare)) == ROOT_EXTREME
    assert max(dual_absolute, key=functools.cmp_to_key(qcompare)) == DUAL_EXTREME
    assert max(cross_absolute, key=functools.cmp_to_key(qcompare)) == CROSS_EXTREME

    root_product, root_word = cycle_sign(root_lines, ROOT_CYCLE, ROOT_EXTREME)
    dual_product, dual_word = cycle_sign(dual_lines, DUAL_CYCLE, DUAL_EXTREME)
    both = list(root_lines) + list(dual_lines)
    cross_product, cross_word = cycle_sign(both, CROSS_CYCLE, CROSS_EXTREME)
    assert (root_product, dual_product, cross_product) == (-1, -1, -1)
    assert (root_word, dual_word, cross_word) == (
        "--+-+", "-+-+++++++++++-", "---++++--+"
    )

    # Association degrees in the three maximum-absolute signed graphs.
    def degrees(points: Sequence[Point], target: Quadratic) -> set[int]:
        return {
            sum(i != j and qabs(qdot(point, points[j])) == target
                for j in range(len(points)))
            for i, point in enumerate(points)
        }

    assert degrees(root_lines, ROOT_EXTREME) == {12}
    assert degrees(dual_lines, DUAL_EXTREME) == {4}
    root_cross_degrees = {
        sum(qabs(qdot(root, dual)) == CROSS_EXTREME for dual in dual_lines)
        for root in root_lines
    }
    dual_cross_degrees = {
        sum(qabs(qdot(root, dual)) == CROSS_EXTREME for root in root_lines)
        for dual in dual_lines
    }
    assert root_cross_degrees == {20}
    assert dual_cross_degrees == {4}
    return root_word, dual_word, cross_word


def verify_coloring(points: Sequence[Point], target: Quadratic, colors: Sequence[int]) -> None:
    assert len(points) == len(colors)
    for i in range(len(points)):
        for j in range(i):
            if qdot(points[i], points[j]) == target:
                assert colors[i] != colors[j]


def verify_coloring_certificates(
    roots: Sequence[Point], duals: Sequence[Point],
    root_lines: Sequence[Point], dual_lines: Sequence[Point]
) -> tuple[str, str, str]:
    assert len(ROOT_LINE_COLORS) == 60
    assert collections.Counter(ROOT_LINE_COLORS) == {0: 12, 1: 12, 2: 12, 3: 12, 4: 12}
    for i in range(60):
        for j in range(i):
            if qabs(qdot(root_lines[i], root_lines[j])) == ROOT_EXTREME:
                assert ROOT_LINE_COLORS[i] != ROOT_LINE_COLORS[j]

    assert len(DUAL_EXTREME_COLORS) == 600
    dual_colors = tuple(int(character) for character in DUAL_EXTREME_COLORS)
    assert collections.Counter(dual_colors) == {0: 258, 1: 231, 2: 111}
    assert hashlib.sha256(DUAL_EXTREME_COLORS.encode()).hexdigest() == (
        "4db72692637cb646a136b858fcc0f060b7a9b8417edca85a9343ad466cf5cba4"
    )
    verify_coloring(duals, qneg(DUAL_EXTREME), dual_colors)

    # Explicit canonical representative coloring at the A--cross transition.
    ax_colors = list(ROOT_LINE_COLORS)
    for dual in dual_lines:
        used = {
            ROOT_LINE_COLORS[i]
            for i, root in enumerate(root_lines)
            if qdot(root, dual) == qneg(CROSS_EXTREME)
        }
        assert len(used) <= 4
        ax_colors.append(next(color for color in range(5) if color not in used))
    ax_points = list(root_lines) + list(dual_lines)
    for i in range(len(ax_points)):
        for j in range(i):
            relation = (
                i < 60 and j < 60
                and qdot(ax_points[i], ax_points[j]) == qneg(ROOT_EXTREME)
            ) or (
                i >= 60 and j < 60
                and qdot(ax_points[i], ax_points[j]) == qneg(CROSS_EXTREME)
            )
            if relation:
                assert ax_colors[i] != ax_colors[j]
    ax_encoded = "".join(map(str, ax_colors))
    assert hashlib.sha256(ax_encoded.encode()).hexdigest() == (
        "d5c6af46a62c1ca46b4179ced4e68227d0cea8cae6feec99807937becf2a96a1"
    )

    # At the B--cross transition, restrict the full three-coloring to the
    # chosen dual orientations and give every root a fourth color.
    dual_color_by_point = {point: dual_colors[i] for i, point in enumerate(duals)}
    xb_colors = [3] * 60 + [dual_color_by_point[point] for point in dual_lines]
    xb_points = list(root_lines) + list(dual_lines)
    for i in range(len(xb_points)):
        for j in range(i):
            relation = (
                i >= 60 and j >= 60
                and qdot(xb_points[i], xb_points[j]) == qneg(DUAL_EXTREME)
            ) or (
                i >= 60 and j < 60
                and qdot(xb_points[i], xb_points[j]) == qneg(CROSS_EXTREME)
            )
            if relation:
                assert xb_colors[i] != xb_colors[j]
    xb_encoded = "".join(map(str, xb_colors))
    assert hashlib.sha256(xb_encoded.encode()).hexdigest() == (
        "d00d9ba2d5044df1100e9194e64c3ea4b00a349a45589963f6d4e2e5e7ad108b"
    )

    return (
        hashlib.sha256("".join(map(str, ROOT_LINE_COLORS)).encode()).hexdigest(),
        hashlib.sha256(ax_encoded.encode()).hexdigest(),
        hashlib.sha256(xb_encoded.encode()).hexdigest(),
    )


@dataclass(frozen=True)
class RadiusEquation:
    """q2*r^2+q1*r+q0=0 in the positive embedding of Q(sqrt(5))."""

    name: str
    q2: Quadratic
    q1: Quadratic
    q0: Quadratic
    lower_milli: int
    upper_milli: int
    norm_polynomial_low_to_high: tuple[int, ...]


RADIUS_EQUATIONS = {
    # Projective A versus cross, and projective B versus cross.
    "AX_P": RadiusEquation("AX_P", (14, 6), (7, 3), (-3, -1), 253, 254,
                           (1, -3, -5, 4, 4)),
    "XB_P": RadiusEquation("XB_P", (40, 18), (-7, -3), (-2, 0), 264, 265,
                           (-1, -7, 39, 5, 5)),
    # Full antipodal A versus cross, and full antipodal B versus cross.
    "AX_F": RadiusEquation("AX_F", (14, 6), (7, 3), (-6, 0), 280, 281,
                           (9, -21, -41, 4, 4)),
    "XB_F": RadiusEquation("XB_F", (42, 18), (-7, -3), (-2, 0), 260, 261,
                           (1, 7, -41, -12, 36)),
    # Direct A--B crossings for FF, FP, PF, PP occupancy modes.
    "AB_FF": RadiusEquation("AB_FF", (7, 3), (0, 0), (-1, 0), 270, 271,
                            (1, 0, -14, 0, 4)),
    "AB_FP": RadiusEquation("AB_FP", (27, 12), (0, 0), (-4, 0), 272, 273,
                            (16, 0, -216, 0, 9)),
    "AB_PF": RadiusEquation("AB_PF", (56, 24), (0, 0), (-5, -1), 256, 257,
                            (5, 0, -80, 0, 64)),
    "AB_PP": RadiusEquation("AB_PP", (54, 24), (0, 0), (-5, -1), 259, 260,
                            (5, 0, -75, 0, 9)),
}


def convolve(left: Sequence[int], right: Sequence[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return result


def norm_polynomial(equation: RadiusEquation) -> tuple[int, ...]:
    # If f=A+sqrt(5)B, its rational norm is A^2-5B^2.
    rational = [equation.q0[0], equation.q1[0], equation.q2[0]]
    radical = [equation.q0[1], equation.q1[1], equation.q2[1]]
    first = convolve(rational, rational)
    second = convolve(radical, radical)
    result = [x - 5 * y for x, y in zip(first, second)]
    divisor = 0
    for coefficient in result:
        divisor = math.gcd(divisor, abs(coefficient))
    result = [coefficient // divisor for coefficient in result]
    if result[-1] < 0:
        result = [-coefficient for coefficient in result]
    return tuple(result)


def evaluate_at_milli(equation: RadiusEquation, numerator: int) -> Quadratic:
    # Return 1000^2 f(numerator/1000), preserving its exact sign.
    return qadd(
        qadd(qscale(numerator * numerator, equation.q2),
             qscale(1000 * numerator, equation.q1)),
        qscale(1000 * 1000, equation.q0),
    )


def verify_radius_equations() -> None:
    for equation in RADIUS_EQUATIONS.values():
        assert qsign(equation.q2) > 0 and qsign(equation.q0) < 0
        # Opposite signs of q2 and q0 imply exactly one positive root.
        assert qsign(evaluate_at_milli(equation, equation.lower_milli)) < 0
        assert qsign(evaluate_at_milli(equation, equation.upper_milli)) > 0
        assert norm_polynomial(equation) == equation.norm_polynomial_low_to_high

    # If XB < AB < AX, the cross curve is hidden.  If AX < AB < XB, it is
    # the unique upper envelope between the two displayed transition roots.
    assert RADIUS_EQUATIONS["XB_F"].upper_milli < RADIUS_EQUATIONS["AB_FF"].lower_milli
    assert RADIUS_EQUATIONS["AB_FF"].upper_milli < RADIUS_EQUATIONS["AX_F"].lower_milli
    assert RADIUS_EQUATIONS["XB_P"].upper_milli < RADIUS_EQUATIONS["AB_FP"].lower_milli
    assert RADIUS_EQUATIONS["AB_FP"].upper_milli < RADIUS_EQUATIONS["AX_F"].lower_milli
    assert RADIUS_EQUATIONS["AX_P"].upper_milli < RADIUS_EQUATIONS["AB_PF"].lower_milli
    assert RADIUS_EQUATIONS["AB_PF"].upper_milli < RADIUS_EQUATIONS["XB_F"].lower_milli
    assert RADIUS_EQUATIONS["AX_P"].upper_milli < RADIUS_EQUATIONS["AB_PP"].lower_milli
    assert RADIUS_EQUATIONS["AB_PP"].upper_milli < RADIUS_EQUATIONS["XB_P"].lower_milli


def tie_equations(u: Quadratic, t: Quadratic, c: Quadratic) -> tuple[
    tuple[Quadratic, Quadratic, Quadratic],
    tuple[Quadratic, Quadratic, Quadratic],
    tuple[Quadratic, Quadratic, Quadratic],
]:
    """Return exact AB, AX, BX equations for arbitrary relation levels.

    Coefficients are returned in descending powers of r.  This is a compact
    exhaustive parametrization of every radial tie using the finite product
    tables:

      A_u = 32-2u,
      B_t = 2r^2(N-t),
      X_c = 16+N r^2-2cr.
    """
    ab = (qsub(DUAL_NORM, t), (0, 0), (u[0] - 16, u[1]))
    ax = (DUAL_NORM, qscale(-2, c), (2 * u[0] - 16, 2 * u[1]))
    bx = (qsub(DUAL_NORM, qscale(2, t)), qscale(2, c), (-16, 0))
    return ab, ax, bx


def verify_general_tie_formulas() -> None:
    c = qneg(CROSS_EXTREME)

    def stored(name: str) -> tuple[Quadratic, Quadratic, Quadratic]:
        equation = RADIUS_EQUATIONS[name]
        return equation.q2, equation.q1, equation.q0

    def scaled(
        factor: int, equation: tuple[Quadratic, Quadratic, Quadratic]
    ) -> tuple[Quadratic, Quadratic, Quadratic]:
        return tuple(qscale(factor, value) for value in equation)  # type: ignore[return-value]

    # F/P denotes a full antipodal orbit or one representative per line.
    # Re-derive every recorded equation directly from the universal formulas.
    modes = {
        "FF": (qneg(ROOT_NORM), qneg(DUAL_NORM),
               ("AB_FF", 32), ("AX_F", 8), ("XB_F", 8)),
        "FP": (qneg(ROOT_NORM), qneg(DUAL_EXTREME),
               ("AB_FP", 8), ("AX_F", 8), ("XB_P", 8)),
        "PF": (qneg(ROOT_EXTREME), qneg(DUAL_NORM),
               ("AB_PF", 4), ("AX_P", 8), ("XB_F", 8)),
        "PP": (qneg(ROOT_EXTREME), qneg(DUAL_EXTREME),
               ("AB_PP", 4), ("AX_P", 8), ("XB_P", 8)),
    }
    for _, (u, t, ab_data, ax_data, bx_data) in modes.items():
        actual = tie_equations(u, t, c)
        for obtained, (name, factor) in zip(actual, (ab_data, ax_data, bx_data)):
            assert obtained == scaled(factor, stored(name))


def format_q(value: Quadratic) -> str:
    a, b = value
    if b == 0:
        return str(a)
    sign = "+" if b > 0 else "-"
    return f"{a}{sign}{abs(b)}s"


def verify() -> None:
    roots, cliques, duals = dual_centroid_orbit()
    assert len(roots) == 120 and len(duals) == 600
    assert {qdot(point, point) for point in roots} == {ROOT_NORM}
    assert {qdot(point, point) for point in duals} == {DUAL_NORM}
    root_lines = canonical_lines(roots)
    dual_lines = canonical_lines(duals)

    verify_cross_spectrum(roots, duals)
    verify_centroid_incidence(roots, cliques, duals)
    cycle_words = verify_projective_extremes(root_lines, dual_lines)
    color_digests = verify_coloring_certificates(
        roots, duals, root_lines, dual_lines
    )
    verify_radius_equations()
    verify_general_tie_formulas()

    print("exact mixed H4 radial audit passed")
    print("oriented_orbits=120+600 projective_lines=60+300")
    print("cross_levels=15 cross_pairs=72000 cross_extreme_incidence_edges=2400")
    print(
        "unbalanced_switching_cycles="
        f"root:{len(ROOT_CYCLE)-1}:{cycle_words[0]} "
        f"dual:{len(DUAL_CYCLE)-1}:{cycle_words[1]} "
        f"cross:{len(CROSS_CYCLE)-1}:{cycle_words[2]}"
    )
    print(
        "all_2^360_projective_switchings_minima="
        f"{format_q(qneg(ROOT_EXTREME))},{format_q(qneg(DUAL_EXTREME))},"
        f"{format_q(qneg(CROSS_EXTREME))}"
    )
    print("radial_envelopes=FF:A/B FP:A/B PF:A/X/B PP:A/X/B")
    for key in (
        "AX_P", "AB_PF", "AB_PP", "XB_F", "XB_P", "AB_FF", "AB_FP", "AX_F"
    ):
        equation = RADIUS_EQUATIONS[key]
        polynomial = ",".join(map(str, equation.norm_polynomial_low_to_high))
        print(
            f"radius={key} interval=({equation.lower_milli}/1000,"
            f"{equation.upper_milli}/1000) norm_poly_low=[{polynomial}]"
        )
    print(
        "color_certificate_sha256="
        f"root:{color_digests[0]} AX:{color_digests[1]} XB:{color_digests[2]}"
    )
    print("all_full_and_all_projective_oriented_radial_unions_five_colorable=true")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="run the exact audit")
    parser.parse_args()
    verify()


if __name__ == "__main__":
    main()
