#!/usr/bin/env python3
"""Exact finite audit of a multinomial pin-word Schur conjecture.

For a pin-count vector ``counts`` of total order ``t``, let ``V_counts``
be the active reward averaged uniformly over all words having precisely
those pin multiplicities.  Equivariance makes the scalar control

    h(counts) = nu_0 V_counts

symmetric in the coordinates of ``counts``.  The conjectural discrete
Schur inequality is

    h(counts + e_i) >= h(counts + e_j)  whenever counts_i >= counts_j.

Thus adding a pin to a label that is already at least as frequent cannot
decrease the order-averaged inverse-rank reward.  This is stronger than
the one-versus-rest Bernstein-quotient inequality used by the standard
fixed-count-two sector.

The script reconstructs the labelled active operators directly and uses
only exact rational arithmetic.  Its finite audit is evidence, not an
all-order proof.
"""

from __future__ import annotations

from fractions import Fraction as Q
from typing import Iterator

from verify_standard_pin_bernstein import (
    Operator,
    active_operator,
    apply,
    dot,
    replacement_pin,
)


def compositions(total: int, length: int) -> Iterator[tuple[int, ...]]:
    """Yield all weak compositions in a deterministic order."""

    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def add_unit(counts: tuple[int, ...], coordinate: int) -> tuple[int, ...]:
    answer = list(counts)
    answer[coordinate] += 1
    return tuple(answer)


def exact_order_screen(n: int, final_time: int) -> int:
    """Audit every add-one comparison through ``final_time``."""

    operators: list[Operator] = []
    states = None
    for pin in range(n):
        pin_states, operator = active_operator(replacement_pin(n, pin))
        if states is None:
            states = pin_states
        else:
            assert pin_states == states
        operators.append(operator)
    assert states is not None

    N = n - 1
    nu = [
        Q(Bset.bit_count(), n * N * 2 ** (N - 1))
        for Bset, _target in states
    ]
    H = [Q(1, Bset.bit_count()) for Bset, _target in states]

    controls: dict[tuple[int, ...], list[Q]] = {(0,) * n: H}
    comparisons = 0
    for time in range(1, final_time + 1):
        previous = controls
        controls = {}
        for counts in compositions(time, n):
            value = [Q(0) for _state in states]
            for pin, multiplicity in enumerate(counts):
                if not multiplicity:
                    continue
                predecessor = list(counts)
                predecessor[pin] -= 1
                image = apply(operators[pin], previous[tuple(predecessor)])
                scale = Q(multiplicity, time)
                for state, entry in enumerate(image):
                    value[state] += scale * entry
            controls[counts] = value

        rewards = {
            counts: dot(nu, value) for counts, value in controls.items()
        }
        for base in compositions(time - 1, n):
            for more_frequent in range(n):
                for less_frequent in range(n):
                    if base[more_frequent] < base[less_frequent]:
                        continue
                    concentrated = add_unit(base, more_frequent)
                    dispersed = add_unit(base, less_frequent)
                    assert rewards[concentrated] >= rewards[dispersed]
                    comparisons += 1
    return comparisons


def main() -> None:
    scopes = ((3, 35), (4, 14), (5, 9))
    total = 0
    for n, final_time in scopes:
        checked = exact_order_screen(n, final_time)
        total += checked
        print(
            "PASS (EXACT FINITE): "
            f"n={n}, t<={final_time}, comparisons={checked}"
        )
    assert total == 95495
    print(f"PASS (EXACT FINITE): {total} multinomial add-one comparisons")
    print("OPEN: prove discrete Schur-convexity for arbitrary n and t")


if __name__ == "__main__":
    main()
