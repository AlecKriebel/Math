#!/usr/bin/env python3
"""Exact checks for the Pfender/local-hybrid two-point barrier.

Only Python's standard library is used.  The certificate is a
pseudo-distance distribution, not a spherical code.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "local_hybrid_pseudodistribution.json"


def zonal_values(t: Q, degree: int) -> list[Q]:
    """Normalized dimension-five Gegenbauer values P_0(t),...,P_degree(t)."""

    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if degree == 0:
        return [Q(1)]
    values = [Q(1), t]
    for k in range(2, degree + 1):
        values.append(
            (
                (2 * k + 1) * t * values[k - 1]
                - (k - 1) * values[k - 2]
            )
            / (k + 2)
        )
    return values


def integer_wedge_minimum(total_degree: int, vertices: int) -> int:
    """Minimum of sum binom(d_i,2) for integer d_i>=0 with fixed sum."""

    quotient, remainder = divmod(total_degree, vertices)
    return (
        (vertices - remainder) * quotient * (quotient - 1) // 2
        + remainder * quotient * (quotient + 1) // 2
    )


def common_center_bound(q: Q) -> int:
    """Certified common-center bound for q=a^2 in (3/8,3/4]."""

    assert Q(3, 8) < q <= Q(3, 4)
    ratio = Q(3) / (8 * q - 3)
    return min(5, ratio.numerator // ratio.denominator)


def load_certificate() -> tuple[int, tuple[Q, ...], tuple[int, ...], int, Q]:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert data["dimension"] == 5
    size = int(data["size"])
    nodes = tuple(
        Q(atom["t_numerator"], atom["t_denominator"]) for atom in data["atoms"]
    )
    counts = tuple(int(atom["ordered_count"]) for atom in data["atoms"])
    finite_degree = int(data["finite_gegenbauer_check_degree"])
    a_data = data["rank_deficit_test_a"]
    rank_a = Q(a_data["numerator"], a_data["denominator"])
    return size, nodes, counts, finite_degree, rank_a


def threshold_values(
    q: Q, nodes: tuple[Q, ...], counts: tuple[int, ...]
) -> tuple[int, int]:
    """Return ordered D_a and Q_b counts using q=a^2 and b=2q-1."""

    deep = sum(
        count
        for t, count in zip(nodes, counts, strict=True)
        if t < 0 and t * t >= q
    )
    high = sum(
        count
        for t, count in zip(nodes, counts, strict=True)
        if t >= 2 * q - 1
    )
    return deep, high


def threshold_test_points(nodes: tuple[Q, ...]) -> tuple[Q, ...]:
    """One exact point in every event cell, plus every included boundary."""

    lower = Q(3, 8)
    upper = Q(3, 4)
    events = {lower, upper}

    # D_a and Q_{2a^2-1} change only at these support events.
    for t in nodes:
        high_event = (Q(1) + t) / 2
        if lower < high_event <= upper:
            events.add(high_event)
        if t < 0 and lower < t * t <= upper:
            events.add(t * t)

    # floor(3/(8q-3)), capped by 5, changes only at these points.
    for denominator_value in range(1, 6):
        event = (Q(3) + Q(3, denominator_value)) / 8
        if lower < event <= upper:
            events.add(event)

    ordered = sorted(events)
    checks: set[Q] = set()
    for index, event in enumerate(ordered):
        if event > lower:
            checks.add(event)
        if index + 1 < len(ordered):
            checks.add((event + ordered[index + 1]) / 2)
    return tuple(sorted(checks))


def verify() -> dict[str, object]:
    size, nodes, counts, finite_degree, rank_a = load_certificate()
    assert size == 41
    assert len(nodes) == len(counts) == 5
    assert all(count > 0 and count % 2 == 0 for count in counts)
    assert sum(counts) == size * (size - 1)
    assert all(Q(-1) <= t < Q(1, 2) for t in nodes)

    weights = tuple(Q(count, size) for count in counts)
    assert Q(1) + sum(weights, Q(0)) == size

    # All-degree ordinary Delsarte feasibility.
    values = tuple(zonal_values(t, finite_degree) for t in nodes)
    moments = [
        Q(1)
        + sum(
            (weights[i] * values[i][degree] for i in range(len(nodes))),
            Q(0),
        )
        for degree in range(1, finite_degree + 1)
    ]
    minimum_moment, minimum_degree = min(
        (moment, degree) for degree, moment in enumerate(moments, 1)
    )
    assert (minimum_moment, minimum_degree) == (Q(29759, 656000), 2)
    assert minimum_moment > Q(1, 23)

    # Tail constants for the integral estimate in two_point_lp_barrier.md.
    q_values = tuple(Q(1) - t * t for t in nodes)
    q_inverse_three_halves_upper = (
        Q(4),
        Q(3),
        Q(7, 5),
        Q(51, 50),
        Q(31, 20),
    )
    assert all(
        q > 0 and q**3 > Q(1) / upper**2
        for q, upper in zip(
            q_values, q_inverse_three_halves_upper, strict=True
        )
    )
    weighted_q_upper = sum(
        (
            weight * upper
            for weight, upper in zip(
                weights, q_inverse_three_halves_upper, strict=True
            )
        ),
        Q(0),
    )
    assert weighted_q_upper == Q(129117, 2050)
    assert Q(44, 7) < Q(251, 100) ** 2
    analytic_constant_upper = Q(22, 7) ** 2 * Q(251, 100) / 4
    assert analytic_constant_upper < Q(31, 5)
    tail_numerator_upper = Q(31, 5) * weighted_q_upper
    assert tail_numerator_upper == Q(4002627, 10250)
    assert tail_numerator_upper < 391
    assert 391**2 < 54**3

    # Pfender's z=1/2 row generator, summed over rows.  Only -77/100
    # lies strictly below -1/sqrt(2).
    assert nodes[0] ** 2 > Q(1, 2)
    assert all(t * t <= Q(1, 2) for t in nodes[1:] if t < 0)
    pfender_cost = weights[0] * (2 * nodes[0] ** 2 - 1)
    assert pfender_cost == Q(15793, 20500)
    assert Q(1) - pfender_cost == Q(4707, 20500) > 0

    # Pfender's g_{pi/3}: no off-diagonal atom is below -sqrt(3)/2.
    assert all(not (t < 0 and t * t > Q(3, 4)) for t in nodes)

    # Exact event-cell verification of every common-center/integer-envelope
    # cut L(q) Q_b >= 2 F_41(D_a), q=a^2 in (3/8,3/4].
    wedge_checks = []
    for q in threshold_test_points(nodes):
        deep, high = threshold_values(q, nodes, counts)
        common_bound = common_center_bound(q)
        twice_wedge_minimum = 2 * integer_wedge_minimum(deep, size)
        slack = common_bound * high - twice_wedge_minimum
        assert slack >= 0
        wedge_checks.append((q, common_bound, deep, high, slack))

    # Dimension-five cap bound D_a <= 5N for every a>1/sqrt(2).
    # D_a changes only at the stored squared radii.
    for q in threshold_test_points(nodes):
        if q > Q(1, 2):
            deep, _ = threshold_values(q, nodes, counts)
            assert deep <= 5 * size

    # Rank-deficit inequality at the worst support event a=77/100.
    # It is the worst point throughout 3/4<a<=77/100 because the slack
    # derivative is -1700+60a<0.
    assert Q(3, 4) < rank_a
    assert rank_a * rank_a < Q(3, 5)
    beta = Q(3) - 5 * rank_a * rank_a
    b = 2 * rank_a * rank_a - 1
    deep_count = sum(
        count
        for t, count in zip(nodes, counts, strict=True)
        if t <= -rank_a
    )
    deep_excess = sum(
        Q(count) * (-t - rank_a)
        for t, count in zip(nodes, counts, strict=True)
        if t <= -rank_a
    )
    high_deficit = sum(
        Q(count) * (Q(1, 2) - t)
        for t, count in zip(nodes, counts, strict=True)
        if t >= b
    )
    rank_left = beta * (deep_count - 4 * size)
    rank_right = 10 * deep_excess + high_deficit
    assert beta == Q(71, 2000)
    assert b == Q(929, 5000)
    assert deep_count == 170
    assert deep_excess == 0
    assert high_deficit == Q(11, 20)
    assert rank_left == Q(213, 1000)
    assert rank_right - rank_left == Q(337, 1000) > 0
    assert -1700 + 60 * rank_a < 0

    return {
        "mass": Q(1) + sum(weights, Q(0)),
        "minimum_moment": minimum_moment,
        "minimum_moment_degree": minimum_degree,
        "pfender_margin": Q(1) - pfender_cost,
        "wedge_event_checks": len(wedge_checks),
        "minimum_wedge_slack": min(item[4] for item in wedge_checks),
        "rank_deficit_margin": rank_right - rank_left,
        "tail_numerator_upper": tail_numerator_upper,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
