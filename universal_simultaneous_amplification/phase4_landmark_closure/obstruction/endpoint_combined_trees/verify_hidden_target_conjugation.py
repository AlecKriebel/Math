#!/usr/bin/env python3
"""Exact audit of the hidden-target degree conjugation at r=3/2.

The labelled source/target ratio is exact, but after the source label is
hidden a repeated draw of an already represented lineage leaves a collision
factor that no endpoint diagonal and target-only clock can absorb.  The
weighted path P3 with degrees (1,17,18) refutes the proposed marked-space
conjugation both at one selective draw and after the full geometric mixture.
"""

from __future__ import annotations

from flint import fmpq


P_NEUTRAL = fmpq(2, 3)
Q_SELECTIVE = fmpq(1, 3)


def subsets(mask: int):
    current = mask
    while True:
        yield current
        if current == 0:
            return
        current = (current - 1) & mask


def geometric_union_law(row):
    """Union of N iid draws, P(N=m)=p*q^(m-1), m>=1."""
    support = sum(1 << index for index, value in enumerate(row) if value)

    def pgf(mass):
        return P_NEUTRAL * mass / (1 - Q_SELECTIVE * mass)

    law = {}
    for target_set in subsets(support):
        if not target_set:
            continue
        probability = fmpq(0)
        for included in subsets(target_set):
            mass = sum(
                row[index]
                for index in range(len(row))
                if included & (1 << index)
            )
            sign = -1 if (target_set.bit_count() - included.bit_count()) % 2 else 1
            probability += sign * pgf(mass)
        assert probability > 0
        law[target_set] = probability
    assert sum(law.values()) == 1
    return law


def exact_n_draw_union_law(row, draws: int):
    support = sum(1 << index for index, value in enumerate(row) if value)
    law = {}
    for target_set in subsets(support):
        if not target_set:
            continue
        probability = fmpq(0)
        for included in subsets(target_set):
            mass = sum(
                row[index]
                for index in range(len(row))
                if included & (1 << index)
            )
            sign = -1 if (target_set.bit_count() - included.bit_count()) % 2 else 1
            probability += sign * mass**draws
        if probability:
            law[target_set] = probability
    assert all(value > 0 for value in law.values())
    assert sum(law.values()) == 1
    return law


def normalized_endpoint_clocks(law_l, law_c, h_initial, h_endpoint):
    """Ratios left after dividing by the proposed endpoint conjugation."""
    return {
        endpoint: (law_l[endpoint] / law_c[endpoint])
        / (h_initial / h_endpoint[endpoint])
        for endpoint in law_c
    }


def main() -> None:
    # Weighted path: leaf 0 --(1)-- center 2 --(17)-- leaf 1.
    degrees = (fmpq(1), fmpq(17), fmpq(18))
    center = 2

    # The locked dB/C source law is the target row.  Reversing the labelled
    # arrow gives raw masses w_uv/d_u=(1,1), hence conditional law (1/2,1/2).
    c_source = (fmpq(1, 18), fmpq(17, 18), fmpq(0))
    l_source = (fmpq(1, 2), fmpq(1, 2), fmpq(0))
    target_incoming_clock = fmpq(2)  # sum_u w_uv/d_u
    selective_target_clock = degrees[center] / target_incoming_clock
    assert selective_target_clock == 9

    # A single neutral draw is exactly endpoint-conjugate with row clock 1/2.
    one_c = exact_n_draw_union_law(c_source, 1)
    one_l = exact_n_draw_union_law(l_source, 1)
    h_initial = degrees[center]
    h_endpoint = {
        1 << 0: degrees[0],
        1 << 1: degrees[1],
        (1 << 0) | (1 << 1): degrees[0] * degrees[1],
    }
    neutral_clocks = normalized_endpoint_clocks(
        one_l, one_c, h_initial, h_endpoint
    )
    assert neutral_clocks == {1 << 0: fmpq(1, 2), 1 << 1: fmpq(1, 2)}

    # One selective draw followed by the neutral draw.  The target-only
    # prediction is (1/2)*9=9/2.  It works for two distinct sources and for
    # repeating the degree-one leaf, but repeating the degree-17 leaf leaves
    # the exact collision factor 1/17.
    two_c = exact_n_draw_union_law(c_source, 2)
    two_l = exact_n_draw_union_law(l_source, 2)
    two_clocks = normalized_endpoint_clocks(
        two_l, two_c, h_initial, h_endpoint
    )
    assert two_clocks[1 << 0] == fmpq(9, 2)
    assert two_clocks[(1 << 0) | (1 << 1)] == fmpq(9, 2)
    assert two_clocks[1 << 1] == fmpq(9, 34)
    assert two_clocks[1 << 1] == two_clocks[1 << 0] / 17

    # The magic 2/3--1/3 geometric mixture does not cancel the defect.
    burst_c = geometric_union_law(c_source)
    burst_l = geometric_union_law(l_source)
    assert burst_c == {
        1 << 0: fmpq(2, 53),
        1 << 1: fmpq(34, 37),
        (1 << 0) | (1 << 1): fmpq(85, 1961),
    }
    assert burst_l == {
        1 << 0: fmpq(2, 5),
        1 << 1: fmpq(2, 5),
        (1 << 0) | (1 << 1): fmpq(1, 5),
    }
    burst_clocks = normalized_endpoint_clocks(
        burst_l, burst_c, h_initial, h_endpoint
    )
    assert burst_clocks == {
        1 << 0: fmpq(53, 90),
        1 << 1: fmpq(37, 90),
        (1 << 0) | (1 << 1): fmpq(1961, 450),
    }
    assert len(set(burst_clocks.values())) == 3

    print("one-neutral endpoint clocks:", neutral_clocks)
    print("one-selective endpoint clocks:", two_clocks)
    print("geometric endpoint clocks:", burst_clocks)
    print(
        "PASS: target-only diagonal conjugation is exactly refuted by the",
        "first collision term",
    )


if __name__ == "__main__":
    main()
