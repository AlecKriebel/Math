#!/usr/bin/env python3
"""Exact continuum audit of pair-conditioned robust-depth inequalities.

The source object is the exact centered quarter-grid pair/triple
pseudodistribution.  For each base inner product q and every nonzero
direction lambda*y + mu*z, robust depth would give a lower bound on the
number of third points in each strict 1/300 half-plane.

After positive scaling, directions with lambda != 0 are represented by
(lambda, mu) = +/- (1, r).  Membership changes only when

    (u + r v)^2 = (1/300)^2 (1 + r^2 + 2 q r).

Every critical r is rational or quadratic over Q.  This verifier represents
those roots exactly, orders them using rational isolating intervals, checks
every open cell at a rational sample, and evaluates every strict algebraic
boundary exactly.  It uses only the Python standard library.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import cmp_to_key
import hashlib
from math import isqrt
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
SOURCE_SHA256 = "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"

DELTA_SQUARED = Q(1, 300**2)

EXPECTED_CRITICAL_COUNTS = {
    Q(-3, 4): 30,
    Q(-1, 2): 40,
    Q(-1, 4): 44,
    Q(0): 48,
    Q(1, 4): 46,
    Q(1, 2): 42,
}

EXPECTED_BASE_MINIMA = {
    Q(-1): Q(28662449004360233, 962000000000000),
    Q(-3, 4): Q(
        94901776282718104409, 1919190000000000000
    ),
    Q(-1, 2): Q(7870553503445319, 19000000000000),
    Q(-1, 4): Q(2452528744092591, 25000000000000),
    Q(0): Q(18980140755958197, 37000000000000),
    Q(1, 4): Q(
        9426027066077596589, 342712500000000000
    ),
    Q(1, 2): Q(6984244011424181, 14000000000000),
}

EXPECTED_GLOBAL_MINIMUM = Q(
    9426027066077596589, 342712500000000000
)
EXPECTED_MINIMUM_LHS = Q(
    11197706977392614317, 252525000000000000
)
EXPECTED_MINIMUM_RHS = Q(
    26930684548457773259, 1599325000000000000
)


def sign(value: Q) -> int:
    return (value > 0) - (value < 0)


def rational_square_root(value: Q) -> Q | None:
    """Return sqrt(value) when it is rational, and None otherwise."""

    assert value >= 0
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if (
        numerator * numerator == value.numerator
        and denominator * denominator == value.denominator
    ):
        return Q(numerator, denominator)
    return None


@dataclass(frozen=True)
class ExactRoot:
    """A rational root or one selected root of an irreducible monic quadratic."""

    rational: Q | None
    linear: Q | None
    constant: Q | None
    branch: int

    @classmethod
    def from_rational(cls, value: Q) -> "ExactRoot":
        return cls(value, None, None, 0)

    @classmethod
    def from_quadratic(
        cls, linear: Q, constant: Q, branch: int
    ) -> "ExactRoot":
        assert branch in (-1, 1)
        discriminant = linear * linear - 4 * constant
        assert discriminant > 0
        assert rational_square_root(discriminant) is None
        return cls(None, linear, constant, branch)

    def bounds(self, bits: int) -> tuple[Q, Q]:
        """Return exact dyadic bounds containing this root."""

        if self.rational is not None:
            return self.rational, self.rational
        assert self.linear is not None and self.constant is not None
        discriminant = self.linear * self.linear - 4 * self.constant
        scale = 1 << bits
        floor_scaled = isqrt(
            (discriminant.numerator * scale * scale)
            // discriminant.denominator
        )
        square_root_lower = Q(floor_scaled, scale)
        square_root_upper = Q(floor_scaled + 1, scale)
        center = -self.linear / 2
        if self.branch == 1:
            return (
                center + square_root_lower / 2,
                center + square_root_upper / 2,
            )
        return (
            center - square_root_upper / 2,
            center - square_root_lower / 2,
        )

    def compare(self, other: "ExactRoot") -> int:
        if self == other:
            return 0
        for bits in range(16, 4097, 16):
            lower_self, upper_self = self.bounds(bits)
            lower_other, upper_other = other.bounds(bits)
            if upper_self < lower_other:
                return -1
            if upper_other < lower_self:
                return 1
        raise AssertionError("failed to separate distinct quadratic roots")

    def compare_rational(self, value: Q) -> int:
        if self.rational is not None:
            return sign(self.rational - value)
        for bits in range(16, 4097, 16):
            lower, upper = self.bounds(bits)
            if upper < value:
                return -1
            if lower > value:
                return 1
            if lower == upper == value:
                return 0
        raise AssertionError("failed to separate a quadratic root from Q")

    def sign_polynomial(self, constant: Q, linear: Q, quadratic: Q) -> int:
        """Sign of constant + linear*r + quadratic*r^2 at this root."""

        if self.rational is not None:
            value = (
                constant
                + linear * self.rational
                + quadratic * self.rational * self.rational
            )
            return sign(value)

        assert self.linear is not None and self.constant is not None
        # r^2 = -self.linear*r - self.constant.
        affine_constant = constant - quadratic * self.constant
        affine_linear = linear - quadratic * self.linear
        if affine_linear == 0:
            return sign(affine_constant)
        threshold = -affine_constant / affine_linear
        return sign(affine_linear) * self.compare_rational(threshold)

    def display(self) -> str:
        if self.rational is not None:
            return str(self.rational)
        assert self.linear is not None and self.constant is not None
        branch = "+" if self.branch == 1 else "-"
        return (
            f"(-({self.linear}) {branch} "
            f"sqrt(({self.linear})^2-4*({self.constant})))/2"
        )


def real_roots(
    quadratic: Q, linear: Q, constant: Q
) -> tuple[ExactRoot, ...]:
    """All distinct real roots of a rational polynomial of degree at most 2."""

    if quadratic == 0:
        if linear == 0:
            return ()
        return (ExactRoot.from_rational(-constant / linear),)

    discriminant = linear * linear - 4 * quadratic * constant
    if discriminant < 0:
        return ()
    square_root = rational_square_root(discriminant)
    if square_root is not None:
        first = ExactRoot.from_rational(
            (-linear - square_root) / (2 * quadratic)
        )
        second = ExactRoot.from_rational(
            (-linear + square_root) / (2 * quadratic)
        )
        return (first,) if first == second else (first, second)

    # Divide by the leading coefficient to obtain the canonical monic
    # irreducible quadratic.  Any rational polynomial sharing either
    # irrational root has this same monic polynomial, so this representation
    # also groups coincident critical slopes exactly.
    monic_linear = linear / quadratic
    monic_constant = constant / quadratic
    return (
        ExactRoot.from_quadratic(monic_linear, monic_constant, -1),
        ExactRoot.from_quadratic(monic_linear, monic_constant, 1),
    )


def critical_roots(
    base: Q, event_pairs: Iterable[tuple[Q, Q]]
) -> tuple[ExactRoot, ...]:
    answer: set[ExactRoot] = set()
    for first, second in event_pairs:
        # (first + r*second)^2
        #   - DELTA_SQUARED*(1+r^2+2*base*r).
        quadratic = second * second - DELTA_SQUARED
        linear = 2 * (first * second - DELTA_SQUARED * base)
        constant = first * first - DELTA_SQUARED
        answer.update(real_roots(quadratic, linear, constant))
    return tuple(sorted(answer, key=cmp_to_key(lambda x, y: x.compare(y))))


def separating_bounds(
    left: ExactRoot, right: ExactRoot
) -> tuple[Q, Q]:
    assert left.compare(right) < 0
    for bits in range(16, 4097, 16):
        _, upper_left = left.bounds(bits)
        lower_right, _ = right.bounds(bits)
        if upper_left < lower_right:
            return upper_left, lower_right
    raise AssertionError("failed to isolate adjacent critical roots")


def open_cell_samples(roots: tuple[ExactRoot, ...]) -> tuple[Q, ...]:
    assert roots
    lower_first, _ = roots[0].bounds(32)
    _, upper_last = roots[-1].bounds(32)
    samples = [lower_first - 1]
    for left, right in zip(roots, roots[1:]):
        upper_left, lower_right = separating_bounds(left, right)
        samples.append((upper_left + lower_right) / 2)
    samples.append(upper_last + 1)
    return tuple(samples)


def rational_qualifies(
    first: Q,
    second: Q,
    base: Q,
    slope: Q,
    orientation: int,
) -> bool:
    determinant = 1 + slope * slope + 2 * base * slope
    assert determinant > 0
    projection = orientation * (first + slope * second)
    return (
        projection > 0
        and projection * projection
        > DELTA_SQUARED * determinant
    )


def root_qualifies(
    first: Q,
    second: Q,
    base: Q,
    root: ExactRoot,
    orientation: int,
) -> bool:
    determinant_sign = root.sign_polynomial(1, 2 * base, 1)
    assert determinant_sign > 0
    projection_sign = orientation * root.sign_polynomial(
        first, second, 0
    )
    boundary_sign = root.sign_polynomial(
        first * first - DELTA_SQUARED,
        2 * (first * second - DELTA_SQUARED * base),
        second * second - DELTA_SQUARED,
    )
    # Equality is deliberately excluded.  The enlarged-cap theorem includes
    # the closed slab boundary, so its tail conclusion is strict.
    return projection_sign > 0 and boundary_sign > 0


def direction_qualifies(
    first: Q,
    second: Q,
    base: Q,
    direction: tuple[Q, Q],
) -> bool:
    lam, mu = direction
    determinant = lam * lam + mu * mu + 2 * base * lam * mu
    assert determinant > 0
    projection = lam * first + mu * second
    return (
        projection > 0
        and projection * projection
        > DELTA_SQUARED * determinant
    )


def event_weights(
    base_index: int,
    grid: list[Q],
    triples: list[tuple[int, int, int]],
    nu: list[Q],
) -> dict[tuple[Q, Q], Q]:
    """Weights for all oriented base-edge/third-vertex incidences."""

    answer: defaultdict[tuple[Q, Q], Q] = defaultdict(Q)
    for triple, mass in zip(triples, nu):
        for position in range(3):
            if triple[position] != base_index:
                continue
            others = [
                triple[other]
                for other in range(3)
                if other != position
            ]
            first, second = grid[others[0]], grid[others[1]]
            answer[first, second] += mass
            answer[second, first] += mass
    return dict(answer)


def rational_slope_row(
    base: Q,
    alpha: Q,
    weights: dict[tuple[Q, Q], Q],
    slope: Q,
    orientation: int,
) -> tuple[Q, Q, Q, int]:
    endpoint_count = sum(
        rational_qualifies(first, second, base, slope, orientation)
        for first, second in ((Q(1), base), (base, Q(1)))
    )
    required = 7 - endpoint_count
    left = sum(
        weight
        for (first, second), weight in weights.items()
        if rational_qualifies(
            first, second, base, slope, orientation
        )
    )
    right = 6 * required * alpha
    return left - right, left, right, required


def algebraic_boundary_row(
    base: Q,
    alpha: Q,
    weights: dict[tuple[Q, Q], Q],
    root: ExactRoot,
    orientation: int,
) -> tuple[Q, Q, Q, int]:
    endpoint_count = sum(
        root_qualifies(first, second, base, root, orientation)
        for first, second in ((Q(1), base), (base, Q(1)))
    )
    required = 7 - endpoint_count
    left = sum(
        weight
        for (first, second), weight in weights.items()
        if root_qualifies(first, second, base, root, orientation)
    )
    right = 6 * required * alpha
    return left - right, left, right, required


def explicit_direction_row(
    base: Q,
    alpha: Q,
    weights: dict[tuple[Q, Q], Q],
    direction: tuple[Q, Q],
) -> tuple[Q, Q, Q, int]:
    endpoint_count = sum(
        direction_qualifies(first, second, base, direction)
        for first, second in ((Q(1), base), (base, Q(1)))
    )
    required = 7 - endpoint_count
    left = sum(
        weight
        for (first, second), weight in weights.items()
        if direction_qualifies(first, second, base, direction)
    )
    right = 6 * required * alpha
    return left - right, left, right, required


def audit_nonantipodal_base(
    base: Q,
    alpha: Q,
    weights: dict[tuple[Q, Q], Q],
) -> dict[str, object]:
    event_pairs = set(weights)
    event_pairs.update(((Q(1), base), (base, Q(1))))
    roots = critical_roots(base, event_pairs)
    assert len(roots) == EXPECTED_CRITICAL_COUNTS[base]
    samples = open_cell_samples(roots)
    assert len(samples) == len(roots) + 1

    candidates: list[tuple[Q, str, Q, Q, int]] = []
    for slope in samples:
        for orientation in (1, -1):
            slack, left, right, required = rational_slope_row(
                base, alpha, weights, slope, orientation
            )
            assert slack > 0
            candidates.append(
                (
                    slack,
                    f"open:{orientation}",
                    left,
                    right,
                    required,
                )
            )

    for root in roots:
        for orientation in (1, -1):
            slack, left, right, required = algebraic_boundary_row(
                base, alpha, weights, root, orientation
            )
            assert slack > 0
            candidates.append(
                (
                    slack,
                    f"boundary:{orientation}:{root.display()}",
                    left,
                    right,
                    required,
                )
            )

    # lambda=0 is the projective point at infinity.  Check both orientations
    # explicitly instead of relying on limiting behavior in the two tails.
    for direction in ((Q(0), Q(1)), (Q(0), Q(-1))):
        slack, left, right, required = explicit_direction_row(
            base, alpha, weights, direction
        )
        assert slack > 0
        candidates.append(
            (
                slack,
                f"infinity:{direction[1]}",
                left,
                right,
                required,
            )
        )

    minimum = min(candidates, key=lambda item: item[0])
    assert minimum[0] == EXPECTED_BASE_MINIMA[base]
    return {
        "critical_slopes": len(roots),
        "open_cells": len(samples),
        "strict_boundaries_checked": 2 * len(roots),
        "projective_infinity_rows_checked": 2,
        "minimum_slack": str(minimum[0]),
        "minimum_row_kind": minimum[1],
        "minimum_required_third_points": minimum[4],
    }


def audit_antipodal_base(
    base_index: int,
    base: Q,
    alpha: Q,
    weights: dict[tuple[Q, Q], Q],
) -> dict[str, object]:
    assert base == -1
    # If z=-y, every feasible third-point correlation pair is (u,-u).
    # Therefore every nonzero lambda*y+mu*z is a positive or negative
    # multiple of y; the continuum reduces to the two one-axis rows.
    assert all(first == -second for first, second in weights)
    candidates = []
    for direction in ((Q(1), Q(0)), (Q(-1), Q(0))):
        row = explicit_direction_row(base, alpha, weights, direction)
        assert row[0] > 0
        candidates.append(row)
    minimum = min(candidates, key=lambda item: item[0])
    assert minimum[0] == EXPECTED_BASE_MINIMA[base]
    return {
        "base_index": base_index,
        "coverage": (
            "z=-y; every nonzero lambda*y+mu*z reduces to one of two axes"
        ),
        "axis_rows_checked": 2,
        "minimum_slack": str(minimum[0]),
        "minimum_required_third_points": minimum[3],
    }


def verify(source_path: Path = SOURCE) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256
    source = json.loads(source_bytes)
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert source["cardinality"] == 41 and source["dimension"] == 5

    grid = [Q(value) for value in source["grid"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    nu = [Q(value) for value in source["nu"]]
    assert grid == [
        Q(-1),
        Q(-3, 4),
        Q(-1, 2),
        Q(-1, 4),
        Q(0),
        Q(1, 4),
        Q(1, 2),
    ]
    assert len(alpha) == 7 and len(triples) == len(nu) == 51
    assert all(value > 0 for value in alpha + nu)
    assert sum(alpha) == 40 and sum(nu) == 40 * 39
    for index in range(7):
        marginal = sum(
            mass * Q(triple.count(index), 3)
            for triple, mass in zip(triples, nu)
        )
        assert marginal == 39 * alpha[index]

    base_results: dict[str, dict[str, object]] = {}
    for base_index, base in enumerate(grid):
        weights = event_weights(base_index, grid, triples, nu)
        if base == -1:
            result = audit_antipodal_base(
                base_index, base, alpha[base_index], weights
            )
        else:
            result = audit_nonantipodal_base(
                base, alpha[base_index], weights
            )
        base_results[str(base)] = result

    computed_global = min(
        Q(result["minimum_slack"]) for result in base_results.values()
    )
    assert computed_global == EXPECTED_GLOBAL_MINIMUM > 0

    # Rebuild the named attaining row directly.  On the quarter grid the
    # robust gap threshold is smaller than every nonzero node difference,
    # but the verifier still uses the exact squared test.
    base_index = grid.index(Q(1, 4))
    weights = event_weights(base_index, grid, triples, nu)
    attaining = explicit_direction_row(
        Q(1, 4),
        alpha[base_index],
        weights,
        (Q(1), Q(-1)),
    )
    assert attaining[0] == EXPECTED_GLOBAL_MINIMUM
    assert attaining[1] == EXPECTED_MINIMUM_LHS
    assert attaining[2] == EXPECTED_MINIMUM_RHS
    assert attaining[3] == 6

    return {
        "status": "PASS",
        "source_sha256": SOURCE_SHA256,
        "base_results": base_results,
        "global_minimum_slack": str(computed_global),
        "global_minimum_base_inner_product": "1/4",
        "attaining_direction": "(lambda,mu)=(1,-1)",
        "attaining_left": str(attaining[1]),
        "attaining_right": str(attaining[2]),
        "scope": (
            "all pair/triple-measure rows obtained by summing the "
            "pair-conditioned strict +/-1/300 depth theorem over an exact "
            "base-inner-product stratum; not an edgewise realization"
        ),
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
