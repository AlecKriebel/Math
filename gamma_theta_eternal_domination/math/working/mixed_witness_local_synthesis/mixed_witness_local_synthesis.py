#!/usr/bin/env python3
"""Bounded exact local synthesis for the mixed-P4 witness configuration.

The search is deliberately small and labeled.  Vertices are

    0=a, 1=b, 2=c, 3=x0, 4=x1, 5=x2, 6=x3, 7=w [, 8=y].

It enumerates every unspecified graph edge at orders 8 and 9, enforces
gamma(G)=alpha(G)=3, and tests existence of an arbitrary (not necessarily
greatest) one-guard eternal family having the exact response lists

    L(x0)={a}, L(x1)={a,c}, L(x2)={b,c}, L(x3)={b}.

Existence of a proper family is decided exactly by a safety fixed point:
remove the six forbidden direct-swap states from the dominating triples,
then repeatedly delete any state with an attack having no legal successor.
The remaining fixed point is the union/greatest member of all eternal
families avoiding the forbidden states.  Hence the required states survive
iff some exact-list family exists.

The program also:

* records the weaker static and unrestricted-eternal frontiers;
* searches all proper subfamilies for a counterexample to base-orderability
  of the disjoint independent states S={a,b,c} and T={w,x1,x2}; and
* audits a gamma=2 near-countermodel supplied only after the independent
  search formulation was fixed.

No SAT solver, graph generator, or external dependency is used.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


FORMAT = "mixed-witness-local-synthesis-v1"
CHECKPOINT_FORMAT = "mixed-witness-local-synthesis-checkpoint-v1"
NEAR_STRESS_GRAPH6 = "HDzruf]"

S_VERTICES = (0, 1, 2)
X_VERTICES = (3, 4, 5, 6)
W_VERTEX = 7
T_VERTICES = (7, 4, 5)

# Positive list memberships supply both these graph edges and family states.
POSITIVE_LISTS = {
    3: (0,),
    4: (0, 2),
    5: (1, 2),
    6: (1,),
}

# These six direct swaps must be absent from an exact-list family.
NEGATIVE_LISTS = {
    3: (1, 2),
    4: (1,),
    5: (0,),
    6: (0, 2),
}

# The reference state is independent; x0..x3 induce a P4 in the complement;
# and w is missed by {x1,x2}.
FIXED_NONEDGES = frozenset(
    {
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (4, 5),
        (5, 6),
        (4, 7),
        (5, 7),
    }
)

FIXED_EDGES = frozenset(
    {
        (0, 3),
        (0, 4),
        (2, 4),
        (1, 5),
        (2, 5),
        (1, 6),
        (3, 5),
        (3, 6),
        (4, 6),
    }
)


def bitset(vertices: Iterable[int]) -> int:
    value = 0
    for vertex in vertices:
        value |= 1 << vertex
    return value


S_STATE = bitset(S_VERTICES)
T_STATE = bitset(T_VERTICES)


def swap_state(attacked: int, guard: int) -> int:
    return (S_STATE ^ (1 << guard)) | (1 << attacked)


POSITIVE_STATES = tuple(
    swap_state(attacked, guard)
    for attacked, guards in POSITIVE_LISTS.items()
    for guard in guards
)
NEGATIVE_STATES = tuple(
    swap_state(attacked, guard)
    for attacked, guards in NEGATIVE_LISTS.items()
    for guard in guards
)


@dataclass(frozen=True)
class SearchSpec:
    order: int
    labels: tuple[str, ...]
    full: int
    all_pairs: tuple[tuple[int, int], ...]
    unknown_edges: tuple[tuple[int, int], ...]
    triples: tuple[tuple[tuple[int, int, int], int], ...]
    quads: tuple[tuple[int, int, int, int], ...]
    base_closed: tuple[int, ...]
    base_paths: tuple[tuple[int, ...], ...]


def make_spec(order: int) -> SearchSpec:
    if order not in (8, 9):
        raise ValueError("only orders 8 and 9 are supported")
    labels = ("a", "b", "c", "x0", "x1", "x2", "x3", "w")
    if order == 9:
        labels += ("y",)
    all_pairs = tuple(itertools.combinations(range(order), 2))
    unknown_edges = tuple(
        edge
        for edge in all_pairs
        if edge not in FIXED_EDGES and edge not in FIXED_NONEDGES
    )
    triples = tuple(
        (vertices, bitset(vertices))
        for vertices in itertools.combinations(range(order), 3)
    )
    quads = tuple(itertools.combinations(range(order), 4))
    base_closed = [1 << vertex for vertex in range(order)]
    for left, right in FIXED_EDGES:
        base_closed[left] |= 1 << right
        base_closed[right] |= 1 << left

    paths: list[tuple[int, ...]] = []
    for image in itertools.permutations(T_VERTICES):
        interior: list[int] = []
        for subset in range(1, 7):
            state = 0
            for index, source in enumerate(S_VERTICES):
                target = image[index] if subset & (1 << index) else source
                state |= 1 << target
            interior.append(state)
        paths.append(tuple(interior))

    return SearchSpec(
        order=order,
        labels=labels,
        full=(1 << order) - 1,
        all_pairs=all_pairs,
        unknown_edges=unknown_edges,
        triples=triples,
        quads=quads,
        base_closed=tuple(base_closed),
        base_paths=tuple(paths),
    )


def source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def source_campaign_path() -> str:
    resolved = Path(__file__).resolve()
    campaign = resolved.parents[3]
    return str(resolved.relative_to(campaign))


def timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


class RunLog:
    def __init__(self, path: Path | None, append: bool) -> None:
        self.path = path
        self.handle = None
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            self.handle = path.open(
                "a" if append else "w",
                encoding="utf-8",
            )

    def write(self, message: str) -> None:
        line = f"[{timestamp()}] {message}"
        print(line, flush=True)
        if self.handle is not None:
            self.handle.write(line + "\n")
            self.handle.flush()
            os.fsync(self.handle.fileno())

    def close(self) -> None:
        if self.handle is not None:
            self.handle.close()


def graph_for_mask(spec: SearchSpec, mask: int) -> tuple[int, ...]:
    closed = list(spec.base_closed)
    for index, (left, right) in enumerate(spec.unknown_edges):
        if mask & (1 << index):
            closed[left] |= 1 << right
            closed[right] |= 1 << left
    return tuple(closed)


def edge_present(closed: Sequence[int], left: int, right: int) -> bool:
    return bool(closed[left] & (1 << right))


def dominates(closed: Sequence[int], state: int, full: int) -> bool:
    covered = 0
    remaining = state
    while remaining:
        vertex_bit = remaining & -remaining
        remaining -= vertex_bit
        covered |= closed[vertex_bit.bit_length() - 1]
    return covered == full


def independent_four_exists(
    spec: SearchSpec,
    closed: Sequence[int],
) -> bool:
    for quad in spec.quads:
        if not any(
            edge_present(closed, left, right)
            for left, right in itertools.combinations(quad, 2)
        ):
            return True
    return False


def dominating_pair(
    spec: SearchSpec,
    closed: Sequence[int],
) -> tuple[int, int] | None:
    for left, right in spec.all_pairs:
        if closed[left] | closed[right] == spec.full:
            return (left, right)
    return None


def connected(spec: SearchSpec, closed: Sequence[int]) -> bool:
    reached = 1
    while True:
        expanded = reached
        for vertex in range(spec.order):
            if reached & (1 << vertex):
                expanded |= closed[vertex]
        if expanded == reached:
            return reached == spec.full
        reached = expanded


def eligible_dominating_states(
    spec: SearchSpec,
    closed: Sequence[int],
    banned: frozenset[int],
) -> set[int]:
    return {
        state
        for vertices, state in spec.triples
        if state not in banned
        and (
            closed[vertices[0]]
            | closed[vertices[1]]
            | closed[vertices[2]]
        )
        == spec.full
    }


def greatest_safe_family(
    spec: SearchSpec,
    closed: Sequence[int],
    banned: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], tuple[int, ...], int]:
    """Return the greatest closed family, deletion-wave sizes, initial size."""
    family = eligible_dominating_states(spec, closed, banned)
    initial_size = len(family)
    waves: list[int] = []
    while family:
        remove: list[int] = []
        for state in family:
            for attacked in range(spec.order):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                legal = False
                guards = state
                while guards:
                    guard_bit = guards & -guards
                    guards -= guard_bit
                    guard = guard_bit.bit_length() - 1
                    successor = (state ^ guard_bit) | attacked_bit
                    if (
                        edge_present(closed, guard, attacked)
                        and successor in family
                    ):
                        legal = True
                        break
                if not legal:
                    remove.append(state)
                    break
        if not remove:
            break
        waves.append(len(remove))
        family.difference_update(remove)
    return frozenset(family), tuple(waves), initial_size


def verify_family_literal(
    spec: SearchSpec,
    closed: Sequence[int],
    family: frozenset[int],
    banned: frozenset[int] = frozenset(),
) -> int:
    """A separately structured direct checker; return obligation count."""
    if not family:
        raise AssertionError("literal verifier requires a nonempty family")
    obligations = 0
    for state in sorted(family):
        if state.bit_count() != 3:
            raise AssertionError("family contains a non-triple")
        if state in banned:
            raise AssertionError("family contains a banned state")
        if not dominates(closed, state, spec.full):
            raise AssertionError("family contains a nondominating state")
        occupied = tuple(
            vertex
            for vertex in range(spec.order)
            if state & (1 << vertex)
        )
        for attacked in range(spec.order):
            if state & (1 << attacked):
                continue
            obligations += 1
            successors = []
            for guard in occupied:
                if not edge_present(closed, guard, attacked):
                    continue
                successor = (state ^ (1 << guard)) | (1 << attacked)
                if successor in family:
                    successors.append(successor)
            if not successors:
                raise AssertionError(
                    f"no response from {state} to attack {attacked}"
                )
    return obligations


def family_lists(
    spec: SearchSpec,
    closed: Sequence[int],
    family: frozenset[int],
    vertices: Iterable[int] | None = None,
) -> dict[str, list[str]]:
    if vertices is None:
        vertices = range(3, spec.order)
    output: dict[str, list[str]] = {}
    for attacked in vertices:
        output[spec.labels[attacked]] = [
            spec.labels[guard]
            for guard in S_VERTICES
            if edge_present(closed, guard, attacked)
            and swap_state(attacked, guard) in family
        ]
    return output


def state_labels(spec: SearchSpec, state: int) -> list[str]:
    return [
        spec.labels[vertex]
        for vertex in range(spec.order)
        if state & (1 << vertex)
    ]


def canonical_family(
    spec: SearchSpec,
    family: frozenset[int],
) -> list[list[str]]:
    return [
        state_labels(spec, state)
        for state in sorted(family)
    ]


def family_sha256(family: frozenset[int]) -> str:
    payload = ",".join(str(state) for state in sorted(family)).encode()
    return hashlib.sha256(payload).hexdigest()


def positive_name(spec: SearchSpec, attacked: int, guard: int) -> str:
    return f"{spec.labels[guard]}->{spec.labels[attacked]}"


def positive_pattern(
    spec: SearchSpec,
    family: frozenset[int],
) -> tuple[str, ...]:
    return tuple(
        positive_name(spec, attacked, guard)
        for attacked, guards in POSITIVE_LISTS.items()
        for guard in guards
        if swap_state(attacked, guard) in family
    )


def negative_pattern(
    spec: SearchSpec,
    family: frozenset[int],
) -> tuple[str, ...]:
    return tuple(
        positive_name(spec, attacked, guard)
        for attacked, guards in NEGATIVE_LISTS.items()
        for guard in guards
        if swap_state(attacked, guard) in family
    )


def pattern_key(pattern: Sequence[str]) -> str:
    return "|".join(pattern) if pattern else "<none>"


def mask_digest(masks: Sequence[int]) -> str:
    payload = ",".join(str(mask) for mask in masks).encode()
    return hashlib.sha256(payload).hexdigest()


def graph6(spec: SearchSpec, closed: Sequence[int]) -> str:
    bits: list[int] = []
    for right in range(1, spec.order):
        for left in range(right):
            bits.append(int(edge_present(closed, left, right)))
    while len(bits) % 6:
        bits.append(0)
    body = []
    for start in range(0, len(bits), 6):
        value = sum(bits[start + index] << (5 - index) for index in range(6))
        body.append(chr(value + 63))
    return chr(spec.order + 63) + "".join(body)


def decode_graph6(value: str) -> tuple[SearchSpec, tuple[int, ...]]:
    order = ord(value[0]) - 63
    spec = make_spec(order)
    bits: list[int] = []
    for character in value[1:]:
        encoded = ord(character) - 63
        bits.extend((encoded >> shift) & 1 for shift in range(5, -1, -1))
    closed = [1 << vertex for vertex in range(order)]
    index = 0
    for right in range(1, order):
        for left in range(right):
            if bits[index]:
                closed[left] |= 1 << right
                closed[right] |= 1 << left
            index += 1
    return spec, tuple(closed)


def edge_list(
    spec: SearchSpec,
    closed: Sequence[int],
) -> list[list[str]]:
    return [
        [spec.labels[left], spec.labels[right]]
        for left, right in spec.all_pairs
        if edge_present(closed, left, right)
    ]


def unknown_present(spec: SearchSpec, mask: int) -> list[list[str]]:
    return [
        [spec.labels[left], spec.labels[right]]
        for index, (left, right) in enumerate(spec.unknown_edges)
        if mask & (1 << index)
    ]


def forced_unknown_edges(
    spec: SearchSpec,
    masks: Sequence[int],
) -> dict[str, list[list[str]]]:
    if not masks:
        return {"edges": [], "nonedges": []}
    forced_edges = []
    forced_nonedges = []
    for index, (left, right) in enumerate(spec.unknown_edges):
        bit = 1 << index
        label_pair = [spec.labels[left], spec.labels[right]]
        if all(mask & bit for mask in masks):
            forced_edges.append(label_pair)
        if all(not (mask & bit) for mask in masks):
            forced_nonedges.append(label_pair)
    return {"edges": forced_edges, "nonedges": forced_nonedges}


def base_orderings(
    spec: SearchSpec,
    family: frozenset[int],
) -> list[int]:
    return [
        index
        for index, path in enumerate(spec.base_paths)
        if all(state in family for state in path)
    ]


def find_nonbase_proper_family(
    spec: SearchSpec,
    closed: Sequence[int],
    greatest: frozenset[int],
) -> tuple[
    tuple[frozenset[int], frozenset[int]] | None,
    int,
    int,
]:
    """CEGAR over omitted cube states; complete for proper subfamilies.

    If a target family has no base ordering, it omits at least one interior
    state of each currently live base cube.  Branching over such an omitted
    state and recomputing the greatest safe family is therefore exhaustive.
    """
    cache: dict[frozenset[int], frozenset[int]] = {
        frozenset(): greatest,
    }
    maximum_banned = 0

    def fixed_point(banned: frozenset[int]) -> frozenset[int]:
        nonlocal maximum_banned
        maximum_banned = max(maximum_banned, len(banned))
        if banned not in cache:
            cache[banned] = greatest_safe_family(
                spec,
                closed,
                banned,
            )[0]
        return cache[banned]

    def descend(
        banned: frozenset[int],
    ) -> tuple[frozenset[int], frozenset[int]] | None:
        family = fixed_point(banned)
        if S_STATE not in family or T_STATE not in family:
            return None
        live_paths = [
            path
            for path in spec.base_paths
            if all(state in family for state in path)
        ]
        if not live_paths:
            return family, banned
        frequencies = Counter(
            state
            for path in live_paths
            for state in path
        )
        branch_path = live_paths[0]
        for state in sorted(
            branch_path,
            key=lambda item: (-frequencies[item], item),
        ):
            answer = descend(banned | {state})
            if answer is not None:
                return answer
        return None

    answer = descend(frozenset())
    return answer, len(cache), maximum_banned


def new_accumulator(spec: SearchSpec, stop_mask: int) -> dict[str, object]:
    return {
        "format": CHECKPOINT_FORMAT,
        "source_sha256": source_sha256(),
        "order": spec.order,
        "next_mask": 0,
        "stop_mask": stop_mask,
        "counts": {
            "masks_examined": 0,
            "reference_and_six_positive_states_dominate": 0,
            "alpha_equals_3": 0,
            "reference_and_six_positive_states_dominate_and_alpha_equals_3": 0,
            "reference_state_dominates": 0,
            "gamma_alpha_equals_3": 0,
            "all_required_states_dominate": 0,
            "unrestricted_eternal_equality": 0,
            "unrestricted_contains_all_positive_swaps": 0,
            "exact_safe_family_nonempty": 0,
            "exact_realizations": 0,
            "literal_families_checked": 0,
            "literal_attack_obligations_checked": 0,
            "base_cegar_fixed_points": 0,
            "base_counterexamples": 0,
        },
        "gamma_alpha_masks": [],
        "required_dominating_masks": [],
        "unrestricted_eternal_masks": [],
        "unrestricted_positive_pattern_histogram": {},
        "unrestricted_negative_pattern_histogram": {},
        "unrestricted_family_size_histogram": {},
        "unrestricted_base_count_histogram": {},
        "single_negative_unavoidable_histogram": {},
        "joint_but_not_singleton_unavoidable_masks": [],
        "exact_extinction_wave_count_histogram": {},
        "exact_initial_state_count_histogram": {},
        "max_positive_count": -1,
        "closest_masks": [],
        "exact_masks": [],
        "base_counterexample_records": [],
        "maximum_base_cegar_fixed_points_for_one_graph": 0,
        "maximum_base_cegar_banned_depth": 0,
    }


def increment(mapping: dict[str, int], key: object, amount: int = 1) -> None:
    string_key = str(key)
    mapping[string_key] = mapping.get(string_key, 0) + amount


def record_mask(
    spec: SearchSpec,
    mask: int,
    accumulator: dict[str, object],
) -> None:
    counts = accumulator["counts"]
    assert isinstance(counts, dict)
    counts["masks_examined"] += 1
    closed = graph_for_mask(spec, mask)
    direct_required = (S_STATE,) + POSITIVE_STATES
    direct_required_dominate = all(
        dominates(closed, state, spec.full)
        for state in direct_required
    )
    if direct_required_dominate:
        counts["reference_and_six_positive_states_dominate"] += 1

    if independent_four_exists(spec, closed):
        return
    counts["alpha_equals_3"] += 1
    if direct_required_dominate:
        counts[
            "reference_and_six_positive_states_dominate_and_alpha_equals_3"
        ] += 1

    if not dominates(closed, S_STATE, spec.full):
        return
    counts["reference_state_dominates"] += 1

    if dominating_pair(spec, closed) is not None:
        return
    counts["gamma_alpha_equals_3"] += 1
    assert connected(spec, closed)
    gamma_alpha_masks = accumulator["gamma_alpha_masks"]
    assert isinstance(gamma_alpha_masks, list)
    gamma_alpha_masks.append(mask)

    required = (S_STATE,) + POSITIVE_STATES + (T_STATE,)
    if all(dominates(closed, state, spec.full) for state in required):
        counts["all_required_states_dominate"] += 1
        required_masks = accumulator["required_dominating_masks"]
        assert isinstance(required_masks, list)
        required_masks.append(mask)

    greatest, _, _ = greatest_safe_family(spec, closed)
    if greatest:
        counts["unrestricted_eternal_equality"] += 1
        if S_STATE not in greatest or T_STATE not in greatest:
            raise AssertionError("independent-state forcing failed")
        obligations = verify_family_literal(spec, closed, greatest)
        counts["literal_families_checked"] += 1
        counts["literal_attack_obligations_checked"] += obligations
        unrestricted_masks = accumulator["unrestricted_eternal_masks"]
        assert isinstance(unrestricted_masks, list)
        unrestricted_masks.append(mask)

        pattern = positive_pattern(spec, greatest)
        if len(pattern) == len(POSITIVE_STATES):
            counts["unrestricted_contains_all_positive_swaps"] += 1
        positive_histogram = accumulator[
            "unrestricted_positive_pattern_histogram"
        ]
        negative_histogram = accumulator[
            "unrestricted_negative_pattern_histogram"
        ]
        size_histogram = accumulator["unrestricted_family_size_histogram"]
        base_histogram = accumulator["unrestricted_base_count_histogram"]
        assert isinstance(positive_histogram, dict)
        assert isinstance(negative_histogram, dict)
        assert isinstance(size_histogram, dict)
        assert isinstance(base_histogram, dict)
        increment(positive_histogram, pattern_key(pattern))
        increment(negative_histogram, pattern_key(negative_pattern(spec, greatest)))
        increment(size_histogram, len(greatest))
        increment(base_histogram, len(base_orderings(spec, greatest)))

        maximum = accumulator["max_positive_count"]
        assert isinstance(maximum, int)
        closest_masks = accumulator["closest_masks"]
        assert isinstance(closest_masks, list)
        if len(pattern) > maximum:
            accumulator["max_positive_count"] = len(pattern)
            closest_masks[:] = [mask]
        elif len(pattern) == maximum:
            closest_masks.append(mask)

        individually_unavoidable: list[str] = []
        individually_avoidable = True
        for attacked, guards in NEGATIVE_LISTS.items():
            for guard in guards:
                negative_state = swap_state(attacked, guard)
                safe_single, _, _ = greatest_safe_family(
                    spec,
                    closed,
                    frozenset({negative_state}),
                )
                if safe_single:
                    verify_family_literal(
                        spec,
                        closed,
                        safe_single,
                        frozenset({negative_state}),
                    )
                    counts["literal_families_checked"] += 1
                    counts["literal_attack_obligations_checked"] += (
                        len(safe_single) * (spec.order - 3)
                    )
                else:
                    individually_avoidable = False
                    individually_unavoidable.append(
                        positive_name(spec, attacked, guard)
                    )
        unavoidable_histogram = accumulator[
            "single_negative_unavoidable_histogram"
        ]
        assert isinstance(unavoidable_histogram, dict)
        increment(
            unavoidable_histogram,
            pattern_key(individually_unavoidable),
        )

        answer, fixed_point_calls, maximum_banned = (
            find_nonbase_proper_family(spec, closed, greatest)
        )
        counts["base_cegar_fixed_points"] += fixed_point_calls
        accumulator["maximum_base_cegar_fixed_points_for_one_graph"] = max(
            accumulator["maximum_base_cegar_fixed_points_for_one_graph"],
            fixed_point_calls,
        )
        accumulator["maximum_base_cegar_banned_depth"] = max(
            accumulator["maximum_base_cegar_banned_depth"],
            maximum_banned,
        )
        if answer is not None:
            family, banned = answer
            verify_family_literal(spec, closed, family, banned)
            counts["base_counterexamples"] += 1
            records = accumulator["base_counterexample_records"]
            assert isinstance(records, list)
            records.append(
                {
                    "mask": mask,
                    "graph6": graph6(spec, closed),
                    "family_size": len(family),
                    "family": canonical_family(spec, family),
                    "banned_cube_states": [
                        state_labels(spec, state)
                        for state in sorted(banned)
                    ],
                }
            )
    else:
        individually_avoidable = False

    exact, waves, initial_size = greatest_safe_family(
        spec,
        closed,
        frozenset(NEGATIVE_STATES),
    )
    wave_histogram = accumulator["exact_extinction_wave_count_histogram"]
    initial_histogram = accumulator["exact_initial_state_count_histogram"]
    assert isinstance(wave_histogram, dict)
    assert isinstance(initial_histogram, dict)
    increment(wave_histogram, len(waves))
    increment(initial_histogram, initial_size)
    if exact:
        counts["exact_safe_family_nonempty"] += 1
        obligations = verify_family_literal(
            spec,
            closed,
            exact,
            frozenset(NEGATIVE_STATES),
        )
        counts["literal_families_checked"] += 1
        counts["literal_attack_obligations_checked"] += obligations
    elif greatest and individually_avoidable:
        masks = accumulator["joint_but_not_singleton_unavoidable_masks"]
        assert isinstance(masks, list)
        masks.append(mask)

    if exact and all(state in exact for state in required):
        counts["exact_realizations"] += 1
        exact_masks = accumulator["exact_masks"]
        assert isinstance(exact_masks, list)
        exact_masks.append(mask)


def checkpoint(
    path: Path,
    accumulator: dict[str, object],
    next_mask: int,
) -> None:
    accumulator["next_mask"] = next_mask
    atomic_json(path, accumulator)


def detail_for_mask(
    spec: SearchSpec,
    mask: int,
) -> dict[str, object]:
    closed = graph_for_mask(spec, mask)
    family, _, _ = greatest_safe_family(spec, closed)
    pattern = positive_pattern(spec, family)
    all_positive_names = tuple(
        positive_name(spec, attacked, guard)
        for attacked, guards in POSITIVE_LISTS.items()
        for guard in guards
    )
    return {
        "mask": mask,
        "graph6": graph6(spec, closed),
        "unknown_edges_present": unknown_present(spec, mask),
        "greatest_family_size": len(family),
        "family_lists_at_S": family_lists(spec, closed, family),
        "positive_swaps_present": list(pattern),
        "positive_swaps_missing": [
            item for item in all_positive_names if item not in pattern
        ],
        "negative_swaps_present": list(negative_pattern(spec, family)),
        "base_ordering_indices": base_orderings(spec, family),
        "family_sha256": family_sha256(family),
    }


def disjunctive_detail(
    spec: SearchSpec,
    mask: int,
) -> dict[str, object]:
    closed = graph_for_mask(spec, mask)
    families: dict[str, dict[str, object]] = {}
    avoided_by_hash: dict[str, list[str]] = {}
    for attacked, guards in NEGATIVE_LISTS.items():
        for guard in guards:
            label = positive_name(spec, attacked, guard)
            banned = frozenset({swap_state(attacked, guard)})
            family, _, _ = greatest_safe_family(spec, closed, banned)
            digest = family_sha256(family)
            avoided_by_hash.setdefault(digest, []).append(label)
            if digest not in families:
                obligations = verify_family_literal(
                    spec,
                    closed,
                    family,
                    banned,
                )
                families[digest] = {
                    "size": len(family),
                    "states": canonical_family(spec, family),
                    "lists_at_S": family_lists(spec, closed, family),
                    "literal_attack_obligations": obligations,
                }
    for digest, labels in avoided_by_hash.items():
        families[digest]["obtained_when_avoiding"] = labels
    greatest, _, _ = greatest_safe_family(spec, closed)
    return {
        "interpretation": (
            "Every eternal family contains at least one of the six negative "
            "swap states, but for each individual negative state there is "
            "an eternal family avoiding it. Thus the obstruction is "
            "disjunctive and no single extra response is family-independent."
        ),
        "mask": mask,
        "graph6": graph6(spec, closed),
        "edges": edge_list(spec, closed),
        "parameters": {
            "gamma": 3,
            "alpha": 3,
            "gamma_infinity": 3,
        },
        "greatest_family_size": len(greatest),
        "greatest_lists_at_S": family_lists(spec, closed, greatest),
        "greatest_negative_swaps_present": list(
            negative_pattern(spec, greatest)
        ),
        "safe_families_by_sha256": families,
    }


def near_stress_detail() -> dict[str, object]:
    spec, closed = decode_graph6(NEAR_STRESS_GRAPH6)
    family, waves, initial_size = greatest_safe_family(
        spec,
        closed,
        frozenset(NEGATIVE_STATES),
    )
    obligations = verify_family_literal(
        spec,
        closed,
        family,
        frozenset(NEGATIVE_STATES),
    )
    alpha = 3 if not independent_four_exists(spec, closed) else "at least 4"
    pair = dominating_pair(spec, closed)
    required = (S_STATE,) + POSITIVE_STATES + (T_STATE,)
    return {
        "scope": (
            "Post-setup stress test only; not used in search formulation "
            "or coverage."
        ),
        "graph6": NEAR_STRESS_GRAPH6,
        "edges": edge_list(spec, closed),
        "parameters": {
            "gamma": 2 if pair is not None else "at least 3",
            "alpha": alpha,
            "gamma_infinity": 3,
        },
        "dominating_pair": (
            [spec.labels[pair[0]], spec.labels[pair[1]]]
            if pair is not None
            else None
        ),
        "all_required_states_dominate": all(
            dominates(closed, state, spec.full)
            for state in required
        ),
        "safe_greatest_family_size": len(family),
        "safe_greatest_family_initial_size": initial_size,
        "safe_greatest_family_deletion_waves": list(waves),
        "literal_attack_obligations": obligations,
        "family_lists_at_S": family_lists(spec, closed, family),
        "family_states": canonical_family(spec, family),
        "interpretation": (
            "Literal mixed-P4 closure plus the w/y list pattern is possible "
            "when gamma=2; equality is an essential hypothesis."
        ),
    }


def finalize(
    spec: SearchSpec,
    accumulator: dict[str, object],
    checkpoint_path: Path,
) -> dict[str, object]:
    counts = accumulator["counts"]
    gamma_alpha_masks = accumulator["gamma_alpha_masks"]
    required_masks = accumulator["required_dominating_masks"]
    unrestricted_masks = accumulator["unrestricted_eternal_masks"]
    closest_masks = accumulator["closest_masks"]
    exact_masks = accumulator["exact_masks"]
    disjunctive_masks = accumulator[
        "joint_but_not_singleton_unavoidable_masks"
    ]
    assert isinstance(counts, dict)
    assert isinstance(gamma_alpha_masks, list)
    assert isinstance(required_masks, list)
    assert isinstance(unrestricted_masks, list)
    assert isinstance(closest_masks, list)
    assert isinstance(exact_masks, list)
    assert isinstance(disjunctive_masks, list)
    complete_coverage = (
        accumulator["stop_mask"] == (1 << len(spec.unknown_edges))
        and counts["masks_examined"] == (1 << len(spec.unknown_edges))
    )
    required_unrestricted_masks: list[int] = []
    required_positive_histogram: Counter[str] = Counter()
    required_extinction_histogram: Counter[str] = Counter()
    required_maximum_positive = -1
    required_closest_masks: list[int] = []
    for mask in required_masks:
        closed = graph_for_mask(spec, mask)
        greatest, _, _ = greatest_safe_family(spec, closed)
        if greatest:
            required_unrestricted_masks.append(mask)
            pattern = positive_pattern(spec, greatest)
            required_positive_histogram[pattern_key(pattern)] += 1
            if len(pattern) > required_maximum_positive:
                required_maximum_positive = len(pattern)
                required_closest_masks = [mask]
            elif len(pattern) == required_maximum_positive:
                required_closest_masks.append(mask)
        _, waves, initial_size = greatest_safe_family(
            spec,
            closed,
            frozenset(NEGATIVE_STATES),
        )
        profile = (
            f"initial={initial_size};waves="
            + ",".join(str(size) for size in waves)
        )
        required_extinction_histogram[profile] += 1

    result: dict[str, object] = {
        "format": FORMAT,
        "claim_status": (
            "OBSERVED_EXHAUSTIVE_LABELED_SEARCH"
            if complete_coverage
            else "PARTIAL_LABELED_SEARCH"
        ),
        "scope_warning": (
            "This is exact finite evidence for the stated labeled orders "
            "and literal model. It is not a universal theorem, an order-10+ "
            "exclusion, or a literature-priority claim."
        ),
        "completed_at": timestamp(),
        "source": {
            "path": source_campaign_path(),
            "sha256": source_sha256(),
        },
        "order": spec.order,
        "labels": {
            str(index): label
            for index, label in enumerate(spec.labels)
        },
        "model": {
            "attacks": "unoccupied vertices only",
            "move": "exactly one adjacent guard moves along one graph edge",
            "family_states": "dominating 3-subsets of the full graph",
            "closure": (
                "for every family state and every unoccupied attack, at "
                "least one legal successor is in the same family"
            ),
            "family_scope": (
                "arbitrary proper families covered by greatest safe fixed "
                "point after banning the six negative direct swaps"
            ),
            "reference_state": ["a", "b", "c"],
            "second_independent_state": ["w", "x1", "x2"],
            "positive_lists": {
                "x0": ["a"],
                "x1": ["a", "c"],
                "x2": ["b", "c"],
                "x3": ["b"],
            },
        },
        "coverage": {
            "fixed_edges": [
                [spec.labels[left], spec.labels[right]]
                for left, right in sorted(FIXED_EDGES)
            ],
            "fixed_nonedges": [
                [spec.labels[left], spec.labels[right]]
                for left, right in sorted(FIXED_NONEDGES)
            ],
            "unknown_edge_bit_order": [
                [spec.labels[left], spec.labels[right]]
                for left, right in spec.unknown_edges
            ],
            "unknown_edge_count": len(spec.unknown_edges),
            "mask_interval_start_inclusive": 0,
            "mask_interval_stop_exclusive": accumulator["stop_mask"],
            "complete_mask_space_covered": complete_coverage,
            "expected_full_mask_count": 1 << len(spec.unknown_edges),
            "checkpoint_path": str(checkpoint_path.resolve()),
            "counts": counts,
        },
        "gamma_alpha_frontier": {
            "masks": gamma_alpha_masks,
            "mask_list_sha256": mask_digest(gamma_alpha_masks),
            "forced_unknown_adjacencies": forced_unknown_edges(
                spec,
                gamma_alpha_masks,
            ),
            "all_connected": True,
        },
        "required_state_domination_frontier": {
            "definition": (
                "S, T, and all six positive direct-swap states dominate "
                "the full graph; necessary before family closure"
            ),
            "masks": required_masks,
            "mask_list_sha256": mask_digest(required_masks),
            "forced_unknown_adjacencies": forced_unknown_edges(
                spec,
                required_masks,
            ),
            "unrestricted_eternal_masks": required_unrestricted_masks,
            "unrestricted_eternal_count": len(required_unrestricted_masks),
            "unrestricted_positive_pattern_histogram": dict(
                required_positive_histogram
            ),
            "maximum_positive_swaps_surviving_closure_out_of_6": (
                required_maximum_positive
            ),
            "closest_masks_after_closure": required_closest_masks,
            "exact_safe_extinction_profile_histogram": dict(
                required_extinction_histogram
            ),
        },
        "unrestricted_eternal_frontier": {
            "masks": unrestricted_masks,
            "mask_list_sha256": mask_digest(unrestricted_masks),
            "forced_unknown_adjacencies": forced_unknown_edges(
                spec,
                unrestricted_masks,
            ),
            "family_size_histogram": accumulator[
                "unrestricted_family_size_histogram"
            ],
            "positive_pattern_histogram": accumulator[
                "unrestricted_positive_pattern_histogram"
            ],
            "negative_pattern_histogram": accumulator[
                "unrestricted_negative_pattern_histogram"
            ],
            "greatest_family_base_ordering_count_histogram": accumulator[
                "unrestricted_base_count_histogram"
            ],
            "max_positive_swaps_present_out_of_6": accumulator[
                "max_positive_count"
            ],
            "closest_masks": closest_masks,
            "closest_forced_unknown_adjacencies": forced_unknown_edges(
                spec,
                closest_masks,
            ),
            "closest_details": [
                detail_for_mask(spec, mask)
                for mask in closest_masks
            ],
        },
        "exact_safe_fixed_point": {
            "banned_direct_swaps": [
                positive_name(spec, attacked, guard)
                for attacked, guards in NEGATIVE_LISTS.items()
                for guard in guards
            ],
            "initial_state_count_histogram": accumulator[
                "exact_initial_state_count_histogram"
            ],
            "deletion_wave_count_histogram": accumulator[
                "exact_extinction_wave_count_histogram"
            ],
            "surviving_masks": exact_masks,
            "conclusion": (
                f"No order-{spec.order} equality realization exists in "
                "this labeled full-graph model."
                if complete_coverage and not exact_masks
                else (
                    f"{len(exact_masks)} order-{spec.order} labeled "
                    "realizations survive."
                    if complete_coverage
                    else (
                        "The requested mask interval is partial; no "
                        "full-order conclusion is made."
                    )
                )
            ),
        },
        "proper_family_base_ordering_falsifier": {
            "target": (
                "an eternal subfamily containing disjoint independent S,T "
                "but no subset-compatible bijection S->T"
            ),
            "method": (
                "complete CEGAR: branch on one omitted interior state of "
                "each live base cube and recompute the greatest safe family"
            ),
            "graphs_tested": counts["unrestricted_eternal_equality"],
            "fixed_points_computed": counts["base_cegar_fixed_points"],
            "maximum_fixed_points_for_one_graph": accumulator[
                "maximum_base_cegar_fixed_points_for_one_graph"
            ],
            "maximum_banned_depth": accumulator[
                "maximum_base_cegar_banned_depth"
            ],
            "counterexamples": accumulator["base_counterexample_records"],
            "scope_warning": (
                "Zero counterexamples is finite evidence in this local "
                "labeled pool, not a proof of universal base-orderability."
            ),
        },
        "disjunctive_negative_response_probe": {
            "single_state_unavoidable_histogram": accumulator[
                "single_negative_unavoidable_histogram"
            ],
            "joint_but_no_singleton_unavoidable_masks": disjunctive_masks,
            "exemplar": (
                disjunctive_detail(spec, disjunctive_masks[0])
                if disjunctive_masks
                else None
            ),
        },
        "post_setup_near_countermodel": near_stress_detail(),
    }
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, choices=(8, 9), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--checkpoint-every", type=int, default=4096)
    parser.add_argument(
        "--stop-mask",
        type=int,
        help="exclusive end mask; defaults to the complete mask space",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spec = make_spec(args.order)
    full_stop = 1 << len(spec.unknown_edges)
    stop_mask = full_stop if args.stop_mask is None else args.stop_mask
    if not (0 <= stop_mask <= full_stop):
        raise ValueError("stop-mask is outside the mask space")
    if args.checkpoint_every <= 0:
        raise ValueError("checkpoint-every must be positive")

    if args.resume:
        accumulator = json.loads(args.checkpoint.read_text(encoding="utf-8"))
        if accumulator.get("format") != CHECKPOINT_FORMAT:
            raise ValueError("checkpoint format mismatch")
        if accumulator.get("source_sha256") != source_sha256():
            raise ValueError("checkpoint source hash mismatch")
        if accumulator.get("order") != spec.order:
            raise ValueError("checkpoint order mismatch")
        if accumulator.get("stop_mask") != stop_mask:
            raise ValueError("checkpoint stop-mask mismatch")
        start_mask = accumulator["next_mask"]
    else:
        accumulator = new_accumulator(spec, stop_mask)
        start_mask = 0

    log = RunLog(args.log, append=args.resume)
    try:
        log.write(
            f"order={spec.order} unknown_edges={len(spec.unknown_edges)} "
            f"range=[{start_mask},{stop_mask}) resume={args.resume}"
        )
        for mask in range(start_mask, stop_mask):
            record_mask(spec, mask, accumulator)
            next_mask = mask + 1
            if (
                next_mask % args.checkpoint_every == 0
                or next_mask == stop_mask
            ):
                checkpoint(args.checkpoint, accumulator, next_mask)
                counts = accumulator["counts"]
                log.write(
                    f"checkpoint next_mask={next_mask} "
                    f"gamma_alpha={counts['gamma_alpha_equals_3']} "
                    f"required_dominating="
                    f"{counts['all_required_states_dominate']} "
                    f"unrestricted_eternal="
                    f"{counts['unrestricted_eternal_equality']} "
                    f"exact={counts['exact_realizations']}"
                )

        result = finalize(spec, accumulator, args.checkpoint)
        atomic_json(args.output, result)
        log.write(
            f"complete output={args.output} "
            f"sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}"
        )
    finally:
        log.close()


if __name__ == "__main__":
    main()
