#!/usr/bin/env python3
"""Hostile exact screen of sparse multinomial pin-word Schur comparisons.

Only ``d`` pin labels are allowed to occur, while the remaining ``n-d``
labels are permuted.  The active chain then lumps to O(2^d d n) states,
which permits much larger population orders than the full labelled chain.

This is a discovery screen, not a proof.  It constructs the quotient from
canonical representatives and the pin update rule, audits it against the
full labelled chain at small orders, and stops with the exact first failed
add-one comparison if one is encountered.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from math import comb
from typing import Iterator

from verify_standard_pin_bernstein import (
    Operator,
    active_operator,
    apply,
    dot,
    replacement_pin,
)


Orbit = tuple[int, int, int]  # distinguished B-mask, ordinary B-count, target


def compositions(total: int, length: int) -> Iterator[tuple[int, ...]]:
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def orbit_of(Bset: frozenset[int], target: int, d: int) -> Orbit:
    mask = sum(1 << label for label in Bset if label < d)
    ordinary_count = sum(label >= d for label in Bset)
    target_type = target if target < d else d
    return mask, ordinary_count, target_type


def orbit_states(n: int, d: int) -> list[Orbit]:
    ordinary = n - d
    states = []
    for mask in range(1 << d):
        marked_count = mask.bit_count()
        for target_type in range(d):
            if (mask >> target_type) & 1:
                continue
            for ordinary_count in range(ordinary + 1):
                if marked_count + ordinary_count:
                    states.append((mask, ordinary_count, target_type))
        if ordinary:
            for ordinary_count in range(ordinary):
                if marked_count + ordinary_count:
                    states.append((mask, ordinary_count, d))
    return states


def representative(state: Orbit, n: int, d: int) -> tuple[frozenset[int], int]:
    mask, ordinary_count, target_type = state
    Bset = {label for label in range(d) if (mask >> label) & 1}
    if target_type == d:
        target = d
        Bset.update(range(d + 1, d + 1 + ordinary_count))
    else:
        target = target_type
        Bset.update(range(d, d + ordinary_count))
    assert target not in Bset and Bset
    assert max(Bset | {target}) < n
    return frozenset(Bset), target


def pin_targets(n: int, pin: int, source: int) -> list[tuple[int, Q]]:
    if source == pin:
        return [(target, Q(1, n - 1)) for target in range(n) if target != pin]
    return [(pin, Q(1))]


def sparse_quotient(n: int, d: int, pin: int) -> tuple[list[Orbit], Operator]:
    assert 2 <= d <= n and 0 <= pin < d
    states = orbit_states(n, d)
    index = {state: position for position, state in enumerate(states)}
    operator: Operator = []
    for state in states:
        Bset, target = representative(state, n, d)
        rank = len(Bset)
        row: dict[int, Q] = {}

        def add(new_B: frozenset[int], new_target: int, mass: Q) -> None:
            orbit = orbit_of(new_B, new_target, d)
            position = index[orbit]
            row[position] = row.get(position, Q(0)) + mass

        for replacement, mass in pin_targets(n, pin, target):
            add(Bset | {replacement}, target, mass / 2)
        for source in Bset:
            removed = Bset - {source}
            for replacement, mass in pin_targets(n, pin, source):
                add(removed | {replacement}, source, mass / (2 * rank))
        assert sum(row.values(), Q(0)) == 1
        operator.append(row)
    return states, operator


def initial_and_reward(n: int, d: int, states: list[Orbit]) -> tuple[list[Q], list[Q]]:
    ordinary = n - d
    nu = []
    reward = []
    for mask, ordinary_count, target_type in states:
        rank = mask.bit_count() + ordinary_count
        if target_type == d:
            orbit_size = ordinary * comb(ordinary - 1, ordinary_count)
        else:
            orbit_size = comb(ordinary, ordinary_count)
        nu.append(Q(orbit_size * rank, n * (n - 1) * 2 ** (n - 2)))
        reward.append(Q(1, rank))
    assert sum(nu, Q(0)) == 1
    return nu, reward


def labelled_lump_audit() -> None:
    for n in range(3, 7):
        for d in range(2, min(4, n) + 1):
            states = orbit_states(n, d)
            orbit_index = {state: position for position, state in enumerate(states)}
            for pin in range(d):
                _, quotient = sparse_quotient(n, d, pin)
                labelled_states, labelled = active_operator(replacement_pin(n, pin))
                for source, (Bmask, target) in enumerate(labelled_states):
                    Bset = frozenset(
                        label for label in range(n) if (Bmask >> label) & 1
                    )
                    source_orbit = orbit_index[orbit_of(Bset, target, d)]
                    aggregated: dict[int, Q] = {}
                    for labelled_target, mass in labelled[source].items():
                        next_mask, next_vertex = labelled_states[labelled_target]
                        next_B = frozenset(
                            label
                            for label in range(n)
                            if (next_mask >> label) & 1
                        )
                        target_orbit = orbit_index[orbit_of(next_B, next_vertex, d)]
                        aggregated[target_orbit] = (
                            aggregated.get(target_orbit, Q(0)) + mass
                        )
                    assert aggregated == quotient[source_orbit]


def exact_screen(n: int, d: int, final_time: int) -> int:
    states = None
    operators = []
    for pin in range(d):
        pin_states, operator = sparse_quotient(n, d, pin)
        if states is None:
            states = pin_states
        else:
            assert pin_states == states
        operators.append(operator)
    assert states is not None
    nu, reward = initial_and_reward(n, d, states)

    controls: dict[tuple[int, ...], list[Q]] = {(0,) * d: reward}
    checked = 0
    for time in range(1, final_time + 1):
        previous = controls
        controls = {}
        for counts in compositions(time, d):
            value = [Q(0) for _ in states]
            for pin, multiplicity in enumerate(counts):
                if not multiplicity:
                    continue
                predecessor = list(counts)
                predecessor[pin] -= 1
                image = apply(operators[pin], previous[tuple(predecessor)])
                scale = Q(multiplicity, time)
                for position, entry in enumerate(image):
                    value[position] += scale * entry
            controls[counts] = value

        scalar = {counts: dot(nu, value) for counts, value in controls.items()}
        for base in compositions(time - 1, d):
            for high in range(d):
                for low in range(d):
                    if base[high] < base[low]:
                        continue
                    concentrated = list(base)
                    dispersed = list(base)
                    concentrated[high] += 1
                    dispersed[low] += 1
                    left = scalar[tuple(concentrated)]
                    right = scalar[tuple(dispersed)]
                    if left < right:
                        raise AssertionError(
                            "exact sparse Schur failure: "
                            f"n={n}, d={d}, time={time}, base={base}, "
                            f"high={high}, low={low}, difference={left-right}"
                        )
                    checked += 1
    return checked


def two_delta_packet_search(n: int, max_gap: int) -> tuple[int, int, int, Q] | None:
    """Find a negative nu M^a Delta M^b Delta M^c H packet, if any."""

    states, left = sparse_quotient(n, 2, 0)
    _, right = sparse_quotient(n, 2, 1)
    nu, reward = initial_and_reward(n, 2, states)
    M: Operator = []
    Delta: Operator = []
    for left_row, right_row in zip(left, right):
        targets = set(left_row) | set(right_row)
        M.append({
            target: (left_row.get(target, Q(0)) + right_row.get(target, Q(0))) / 2
            for target in targets
            if left_row.get(target, Q(0)) + right_row.get(target, Q(0))
        })
        Delta.append({
            target: (left_row.get(target, Q(0)) - right_row.get(target, Q(0))) / 2
            for target in targets
            if left_row.get(target, Q(0)) != right_row.get(target, Q(0))
        })

    right_vectors = [reward]
    for _ in range(max_gap):
        right_vectors.append(apply(M, right_vectors[-1]))
    for middle in range(max_gap + 1):
        core = apply(Delta, right_vectors[0])
        for _ in range(middle):
            core = apply(M, core)
        core = apply(Delta, core)
        left_vector = core
        for left_gap in range(max_gap + 1):
            for right_gap in range(max_gap + 1):
                # Recompute only the right M power to keep the packet order
                # explicit; this screen is tiny compared with the DP above.
                vector = apply(Delta, right_vectors[right_gap])
                for _ in range(middle):
                    vector = apply(M, vector)
                vector = apply(Delta, vector)
                for _ in range(left_gap):
                    vector = apply(M, vector)
                value = dot(nu, vector)
                if value < 0:
                    return left_gap, middle, right_gap, value
            if left_gap < max_gap:
                left_vector = apply(M, left_vector)
    return None


def main() -> None:
    labelled_lump_audit()
    scopes = (
        (8, 2, 160),
        (15, 2, 100),
        (8, 3, 28),
        (12, 3, 20),
        (8, 4, 13),
    )
    total = 0
    for n, d, final_time in scopes:
        checked = exact_screen(n, d, final_time)
        total += checked
        print(
            f"PASS (EXACT FINITE): n={n}, active labels={d}, "
            f"t<={final_time}, comparisons={checked}"
        )
    packet = two_delta_packet_search(5, 8)
    print(f"first negative two-Delta packet in searched box: {packet}")
    print(f"PASS (EXACT FINITE): total sparse comparisons={total}")


if __name__ == "__main__":
    main()
