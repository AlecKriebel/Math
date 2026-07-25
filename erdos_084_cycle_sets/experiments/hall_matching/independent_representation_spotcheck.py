#!/usr/bin/env python3
"""Independent m=6 spot-check of the representation-aware Hall graph.

This deliberately uses direct Python sets for fibers and typed endpoint
tuples, then an elementary one-vertex-at-a-time augmenting-path matcher.  It
does not read any output or data structure from representation_hall.cpp.
"""

from __future__ import annotations

from array import array
from dataclasses import dataclass
import sys
from typing import Iterable


M = 6
ROW_COUNT = 2 * M
SELECTION_COUNT = 1 << ROW_COUNT
SIGNATURE_COUNT = 1 << (2 * M + 1)
PROFILE_COUNT = 1 << (2 * M - 1)
BOTTOM = 1
ALL_SIGNATURE_BITS = SIGNATURE_COUNT - 1
WITHOUT_BOTTOM = ALL_SIGNATURE_BITS ^ BOTTOM
ROWS = tuple(range(-M, 0)) + tuple(range(1, M + 1))


def bit(value: int) -> int:
    return 1 << (value + M)


def set_bit_indices(mask: int) -> Iterable[int]:
    while mask:
        lowest = mask & -mask
        yield lowest.bit_length() - 1
        mask ^= lowest


def full_parameter(optional: int) -> int:
    return (optional << 1) | 1


def generator_mask(parameter: int, row: int) -> int:
    values = {row, -row}
    for index in set_bit_indices(parameter):
        value = row - index - 1
        if -M <= value <= M:
            values.add(value)
    result = 0
    for value in values:
        result |= bit(value)
    return result


def u_mask(parameter: int) -> int:
    result = 0
    for index in set_bit_indices(parameter):
        result |= bit(M - index)
    return result


@dataclass(frozen=True)
class Left:
    identifier: int
    parameter: int
    signature: int
    representations: tuple[int, ...]


@dataclass(frozen=True)
class Profile:
    u: int
    left: tuple[Left, ...]
    type0: frozenset[int]
    type1: frozenset[int]


def build_signature_table() -> array:
    table = array("H", [0]) * (PROFILE_COUNT * SELECTION_COUNT)
    for optional in range(PROFILE_COUNT):
        generators = tuple(
            generator_mask(full_parameter(optional), row) for row in ROWS
        )
        offset = optional * SELECTION_COUNT
        for selection in range(1, SELECTION_COUNT):
            lowest = selection & -selection
            row_index = lowest.bit_length() - 1
            table[offset + selection] = (
                table[offset + selection - lowest] | generators[row_index]
            )
    return table


def build_profiles(table: array) -> tuple[list[Profile], list[Left]]:
    profiles: list[Profile] = []
    all_left: list[Left] = []
    for optional in range(PROFILE_COUNT):
        offset = optional * SELECTION_COUNT
        values = table[offset : offset + SELECTION_COUNT]
        family = set(values)
        safe = {signature for signature in family if not signature & BOTTOM}
        unsafe = {
            signature & WITHOUT_BOTTOM
            for signature in family
            if signature & BOTTOM
        }

        shadow = u_mask(full_parameter(optional))
        outside = ALL_SIGNATURE_BITS ^ shadow
        safe_traces = {signature & outside for signature in safe}
        unsafe_traces = {signature & outside for signature in unsafe}
        fiber_tops: dict[int, int] = {}
        for signature in safe:
            trace = signature & outside
            fiber_tops[trace] = fiber_tops.get(trace, 0) | signature
        if set(fiber_tops) != safe_traces:
            raise AssertionError("fiber trace mismatch")
        if not set(fiber_tops.values()) <= safe:
            raise AssertionError("fiber join is not a safe family member")

        left_signatures = sorted(
            signature
            for signature in safe
            if signature != fiber_tops[signature & outside]
        )
        representation_lists = {
            signature: [] for signature in left_signatures
        }
        for selection, signature in enumerate(values):
            if signature in representation_lists:
                representation_lists[signature].append(selection)
        profile_left: list[Left] = []
        for signature in left_signatures:
            left = Left(
                identifier=len(all_left),
                parameter=optional,
                signature=signature,
                representations=tuple(representation_lists[signature]),
            )
            profile_left.append(left)
            all_left.append(left)

        not_in_k = {
            trace
            for trace in safe_traces | unsafe_traces
            if trace | shadow not in unsafe
        }
        type0 = frozenset(unsafe_traces & not_in_k)
        type1 = frozenset((safe_traces | unsafe_traces) & not_in_k)
        profiles.append(
            Profile(
                u=shadow,
                left=tuple(profile_left),
                type0=type0,
                type1=type1,
            )
        )
    return profiles, all_left


def reachable_selections(
    representations: tuple[int, ...], stage_b: bool
) -> set[int]:
    reached: set[int] = set()
    for representation in representations:
        reached.add(representation)
        reached.update(representation ^ (1 << first) for first in range(ROW_COUNT))
        for first in range(ROW_COUNT):
            first_present = bool(representation & (1 << first))
            for second in range(first + 1, ROW_COUNT):
                second_present = bool(representation & (1 << second))
                if stage_b or first_present != second_present:
                    reached.add(
                        representation ^ (1 << first) ^ (1 << second)
                    )
    return reached


def endpoint_code(parameter: int, endpoint_type: int, trace: int) -> int:
    return (parameter << (2 * M + 2)) | (endpoint_type << (2 * M + 1)) | trace


def children(parameter: int) -> tuple[int, ...]:
    return (parameter,) + tuple(
        parameter ^ (1 << coordinate)
        for coordinate in set_bit_indices(parameter)
    )


def build_right_ids(profiles: list[Profile]) -> dict[int, int]:
    codes: list[int] = []
    for parameter, profile in enumerate(profiles):
        codes.extend(
            endpoint_code(parameter, 0, trace)
            for trace in profile.type0
        )
        codes.extend(
            endpoint_code(parameter, 1, trace)
            for trace in profile.type1
        )
    if len(codes) != len(set(codes)):
        raise AssertionError("typed endpoint codes are not unique")
    return {code: identifier for identifier, code in enumerate(sorted(codes))}


def adjacency_for_left(
    left: Left,
    profiles: list[Profile],
    table: array,
    right_ids: dict[int, int],
    stage_b: bool,
) -> list[int]:
    endpoints: set[int] = set()
    targets = reachable_selections(left.representations, stage_b)
    for child in children(left.parameter):
        profile = profiles[child]
        outside = ALL_SIGNATURE_BITS ^ profile.u
        offset = child * SELECTION_COUNT
        for target in targets:
            signature = table[offset + target]
            trace = (signature & WITHOUT_BOTTOM) & outside
            if signature & BOTTOM:
                if trace in profile.type0:
                    endpoints.add(endpoint_code(child, 0, trace))
                if trace in profile.type1:
                    endpoints.add(endpoint_code(child, 1, trace))
            elif trace in profile.type1:
                endpoints.add(endpoint_code(child, 1, trace))
    return sorted(right_ids[endpoint] for endpoint in endpoints)


def build_graph(
    profiles: list[Profile],
    all_left: list[Left],
    table: array,
    right_ids: dict[int, int],
    stage_b: bool,
) -> list[list[int]]:
    adjacency: list[list[int]] = []
    for left in all_left:
        adjacency.append(
            adjacency_for_left(left, profiles, table, right_ids, stage_b)
        )
    return adjacency


def elementary_matching(
    adjacency: list[list[int]], right_count: int
) -> tuple[list[int], list[int]]:
    """Maximum matching by repeated elementary DFS augmentations (Kuhn)."""

    sys.setrecursionlimit(100_000)
    pair_left = [-1] * len(adjacency)
    pair_right = [-1] * right_count
    seen_right = [0] * right_count
    stamp = 0

    def augment(left: int) -> bool:
        nonlocal stamp
        for right in adjacency[left]:
            if seen_right[right] == stamp:
                continue
            seen_right[right] = stamp
            previous = pair_right[right]
            if previous == -1 or augment(previous):
                pair_left[left] = right
                pair_right[right] = left
                return True
        return False

    # Low-degree vertices first makes this elementary implementation quick,
    # and has no effect on maximality because every failed search examines
    # the complete alternating component for that insertion.
    for left in sorted(range(len(adjacency)), key=lambda item: len(adjacency[item])):
        stamp += 1
        augment(left)

    return pair_left, pair_right


def verify_matching(
    adjacency: list[list[int]], pair_left: list[int], pair_right: list[int]
) -> int:
    matched = 0
    for left, right in enumerate(pair_left):
        if right == -1:
            continue
        matched += 1
        if pair_right[right] != left or right not in adjacency[left]:
            raise AssertionError("invalid matching edge or inverse")
    if sum(right != -1 for right in pair_right) != matched:
        raise AssertionError("matching cardinalities disagree")
    return matched


def check_stage(
    label: str,
    profiles: list[Profile],
    all_left: list[Left],
    table: array,
    right_ids: dict[int, int],
    stage_b: bool,
) -> tuple[list[list[int]], list[int]]:
    adjacency = build_graph(
        profiles, all_left, table, right_ids, stage_b=stage_b
    )
    edge_count = sum(map(len, adjacency))
    isolated = [
        left.identifier
        for left, neighbors in zip(all_left, adjacency)
        if not neighbors
    ]
    pair_left, pair_right = elementary_matching(adjacency, len(right_ids))
    matching = verify_matching(adjacency, pair_left, pair_right)
    print(
        f"{label} edges={edge_count} isolated={len(isolated)} "
        f"matching={matching} shortfall={len(all_left) - matching} "
        f"isolated_ids={isolated}"
    )
    return adjacency, isolated


def main() -> None:
    table = build_signature_table()
    profiles, all_left = build_profiles(table)
    right_ids = build_right_ids(profiles)
    print(
        f"m={M} left={len(all_left)} right={len(right_ids)} "
        f"representation_mass={sum(len(left.representations) for left in all_left)}"
    )
    if len(all_left) != 11_155 or len(right_ids) != 54_924:
        raise AssertionError("independent profile totals disagree")

    stage_a, isolated_a = check_stage(
        "stage_A", profiles, all_left, table, right_ids, stage_b=False
    )
    stage_b, isolated_b = check_stage(
        "stage_B", profiles, all_left, table, right_ids, stage_b=True
    )

    if sum(map(len, stage_a)) != 722_305:
        raise AssertionError("stage-A edge count disagrees")
    if len(isolated_a) != 20:
        raise AssertionError("stage-A isolated count disagrees")
    if sum(map(len, stage_b)) != 851_589:
        raise AssertionError("stage-B edge count disagrees")
    if isolated_b:
        raise AssertionError("stage B contains an isolated left vertex")
    if any(not stage_b[left] for left in isolated_a):
        raise AssertionError("stage B failed to rescue a stage-A isolate")
    print("independent representation spot-check passed")


if __name__ == "__main__":
    main()
