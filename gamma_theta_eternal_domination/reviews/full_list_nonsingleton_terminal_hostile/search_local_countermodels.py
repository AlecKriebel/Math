#!/usr/bin/env python3
"""Exhaustive local-role attempts to falsify Lemma 2.1.

The first sweep tests every seven-vertex graph completion of the direct-root
role constraints.  The second tests every completion of the nonroot diamond
constraints.  The local sweeps deliberately weaken greatest-family membership
to mere domination, so a counterexample here would also refute the proof.
An exact sub-sweep additionally reconstructs greatest families and the stated
equality/full-target hypotheses whenever the local premises occur.
"""

from __future__ import annotations

import itertools
import json


N = 7
ALL = (1 << N) - 1
TRIPLES = tuple(sum(1 << v for v in choice) for choice in itertools.combinations(range(N), 3))


def verts(mask: int) -> tuple[int, ...]:
    result: list[int] = []
    while mask:
        bit = mask & -mask
        result.append(bit.bit_length() - 1)
        mask ^= bit
    return tuple(result)


def dominates(state: int, adjacency: tuple[int, ...]) -> bool:
    covered = state
    for v in verts(state):
        covered |= adjacency[v]
    return covered == ALL


def missed(state: int, adjacency: tuple[int, ...]) -> tuple[int, ...]:
    covered = state
    for v in verts(state):
        covered |= adjacency[v]
    return verts(ALL ^ covered)


def graph_from_completion(
    forced_present: set[tuple[int, int]],
    forced_absent: set[tuple[int, int]],
    assignment: int,
) -> tuple[int, ...]:
    normalized_present = {tuple(sorted(edge)) for edge in forced_present}
    normalized_absent = {tuple(sorted(edge)) for edge in forced_absent}
    assert not (normalized_present & normalized_absent)
    all_edges = list(itertools.combinations(range(N), 2))
    free_edges = [
        edge
        for edge in all_edges
        if edge not in normalized_present and edge not in normalized_absent
    ]
    adjacency = [0] * N
    chosen = set(normalized_present)
    for index, edge in enumerate(free_edges):
        if assignment & (1 << index):
            chosen.add(edge)
    for a, b in chosen:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
    return tuple(adjacency)


def free_edge_count(
    forced_present: set[tuple[int, int]],
    forced_absent: set[tuple[int, int]],
) -> int:
    fixed = {
        tuple(sorted(edge))
        for edge in forced_present | forced_absent
    }
    return N * (N - 1) // 2 - len(fixed)


def universe_outside_ban(
    adjacency: tuple[int, ...],
    root: int,
    color: int,
    target: int,
) -> tuple[set[int], set[int]]:
    nonneighbors = ALL ^ (1 << target) ^ adjacency[target]
    anchors = root ^ (1 << color)
    ban = {anchors | (1 << z) for z in verts(nonneighbors)}
    universe = {state for state in TRIPLES if dominates(state, adjacency)} - ban
    return universe, ban


def no_unbanned_response(
    state: int,
    attacked: int,
    universe: set[int],
    adjacency: tuple[int, ...],
) -> bool:
    for mover in verts(state):
        if adjacency[mover] & (1 << attacked):
            successor = (state ^ (1 << mover)) | (1 << attacked)
            if successor in universe:
                return False
    return True


def peel(
    universe: set[int],
    adjacency: tuple[int, ...],
) -> tuple[frozenset[int], dict[int, int]]:
    active = set(universe)
    rank: dict[int, int] = {}
    round_number = 0
    while True:
        doomed: list[int] = []
        for state in active:
            for attacked in verts(ALL ^ state):
                if no_unbanned_response(state, attacked, active, adjacency):
                    doomed.append(state)
                    break
        if not doomed:
            return frozenset(active), rank
        for state in doomed:
            rank[state] = round_number
        active.difference_update(doomed)
        round_number += 1


def maximum_independent_size(adjacency: tuple[int, ...]) -> int:
    for size in range(N, 0, -1):
        for choice in itertools.combinations(range(N), size):
            state = sum(1 << v for v in choice)
            if all((adjacency[v] & state) == 0 for v in choice):
                return size
    raise AssertionError


def domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, N + 1):
        for choice in itertools.combinations(range(N), size):
            state = sum(1 << v for v in choice)
            if dominates(state, adjacency):
                return size
    raise AssertionError


def greatest_family(adjacency: tuple[int, ...]) -> frozenset[int]:
    universe = {state for state in TRIPLES if dominates(state, adjacency)}
    return peel(universe, adjacency)[0]


def full_at_root(
    root: int,
    target: int,
    greatest: frozenset[int],
    adjacency: tuple[int, ...],
) -> bool:
    for color in verts(root):
        successor = (root ^ (1 << color)) | (1 << target)
        if not (adjacency[color] & (1 << target) and successor in greatest):
            return False
    return True


def direct_root_sweep() -> dict[str, int]:
    # u=0, v=1, t=2, x=3, r=4; vertices 5 and 6 are arbitrary residuals.
    u, v, t, x, r = 0, 1, 2, 3, 4
    root = (1 << u) | (1 << v) | (1 << t)
    present = {(x, u), (x, v), (x, t), (u, r)}
    absent = {(u, v), (u, t), (v, t), (x, r)}
    freedom = free_edge_count(present, absent)
    counts = {
        "graph_completions": 1 << freedom,
        "local_rank_zero_rows": 0,
        "local_rows_with_secondary_dominating_response": 0,
        "exact_equality_full_rows": 0,
        "exact_palette_violations": 0,
    }
    for assignment in range(1 << freedom):
        adjacency = graph_from_completion(present, absent, assignment)
        universe, ban = universe_outside_ban(adjacency, root, u, x)
        terminal_state = (root ^ (1 << u)) | (1 << r)
        if (
            root not in universe
            or terminal_state not in ban
            or not dominates(terminal_state, adjacency)
            or not no_unbanned_response(root, r, universe, adjacency)
        ):
            continue
        counts["local_rank_zero_rows"] += 1
        local_secondaries = []
        for secondary in (v, t):
            response = (root ^ (1 << secondary)) | (1 << r)
            if adjacency[secondary] & (1 << r) and dominates(response, adjacency):
                local_secondaries.append(secondary)
        if local_secondaries:
            counts["local_rows_with_secondary_dominating_response"] += 1

        if domination_number(adjacency) != 3 or maximum_independent_size(adjacency) != 3:
            continue
        greatest = greatest_family(adjacency)
        if not greatest or not full_at_root(root, x, greatest, adjacency):
            continue
        if terminal_state not in greatest:
            continue
        restricted, _ = peel(universe, adjacency)
        # Rank zero is equivalent here to deletion in the first synchronous round.
        if root in restricted:
            continue
        _, ranks = peel(universe, adjacency)
        if ranks.get(root) != 0:
            continue
        counts["exact_equality_full_rows"] += 1
        actual_secondary = [
            secondary
            for secondary in (v, t)
            if adjacency[secondary] & (1 << r)
            and ((root ^ (1 << secondary)) | (1 << r)) in greatest
        ]
        if actual_secondary:
            counts["exact_palette_violations"] += 1
    return counts


def nonroot_sweep() -> dict[str, int]:
    # u=0, v=1, t=2, x=3, q=4, r=5, w=6.
    u, v, t, x, q, r, w = 0, 1, 2, 3, 4, 5, 6
    root = (1 << u) | (1 << v) | (1 << t)
    predecessor = (1 << v) | (1 << t) | (1 << q)
    terminal_state = (1 << v) | (1 << t) | (1 << r)
    present = {
        (x, u),
        (x, v),
        (x, t),
        (x, q),
        (u, q),
        (u, r),
        (q, r),
    }
    absent = {(u, v), (u, t), (v, t), (x, r)}
    freedom = free_edge_count(present, absent)
    counts = {
        "graph_completions": 1 << freedom,
        "local_rank_zero_rows": 0,
        "local_secondary_incidences": 0,
        "nondomination_violations": 0,
        "witness_location_or_adjacency_violations": 0,
        "two_secondary_rows": 0,
        "two_secondary_witness_set_intersections": 0,
        "exact_equality_full_secondary_incidences": 0,
        "exact_lemma_violations": 0,
    }
    for assignment in range(1 << freedom):
        adjacency = graph_from_completion(present, absent, assignment)
        universe, ban = universe_outside_ban(adjacency, root, u, x)
        if (
            predecessor not in universe
            or terminal_state not in ban
            or not dominates(terminal_state, adjacency)
            or not no_unbanned_response(predecessor, r, universe, adjacency)
        ):
            continue
        counts["local_rank_zero_rows"] += 1
        local_witness_sets: dict[int, set[int]] = {}
        local_secondaries: list[int] = []
        for secondary in (v, t):
            root_response = (root ^ (1 << secondary)) | (1 << r)
            if not (
                adjacency[secondary] & (1 << r)
                and dominates(root_response, adjacency)
            ):
                continue
            counts["local_secondary_incidences"] += 1
            local_secondaries.append(secondary)
            alternate = (predecessor ^ (1 << secondary)) | (1 << r)
            alternate_missed = set(missed(alternate, adjacency))
            local_witness_sets[secondary] = alternate_missed
            if not alternate_missed:
                counts["nondomination_violations"] += 1
            forbidden_roles = {u, v, t, x, q, r}
            if any(
                z in forbidden_roles
                or not (adjacency[secondary] & (1 << z))
                for z in alternate_missed
            ):
                counts["witness_location_or_adjacency_violations"] += 1

        if len(local_secondaries) == 2:
            counts["two_secondary_rows"] += 1
            if local_witness_sets[v] & local_witness_sets[t]:
                counts["two_secondary_witness_set_intersections"] += 1

        if not local_secondaries:
            continue
        if domination_number(adjacency) != 3 or maximum_independent_size(adjacency) != 3:
            continue
        greatest = greatest_family(adjacency)
        if not greatest or not full_at_root(root, x, greatest, adjacency):
            continue
        if predecessor not in greatest or terminal_state not in greatest:
            continue
        kernel, ranks = peel(universe, adjacency)
        if predecessor in kernel or ranks.get(predecessor) != 0:
            continue
        for secondary in local_secondaries:
            root_response = (root ^ (1 << secondary)) | (1 << r)
            if root_response not in greatest:
                continue
            counts["exact_equality_full_secondary_incidences"] += 1
            alternate = (predecessor ^ (1 << secondary)) | (1 << r)
            alternate_missed = set(missed(alternate, adjacency))
            if (
                not alternate_missed
                or any(z in {u, v, t, x, q, r} for z in alternate_missed)
                or any(
                    not adjacency[secondary] & (1 << z)
                    for z in alternate_missed
                )
            ):
                counts["exact_lemma_violations"] += 1
    return counts


def nonroot_eight_vertex_local_sweep() -> dict[str, int]:
    """Repeat the weakened local test with two possible outside witnesses."""

    n = 8
    all_vertices = (1 << n) - 1
    u, v, t, x, q, r = 0, 1, 2, 3, 4, 5
    root = (1 << u) | (1 << v) | (1 << t)
    predecessor = (1 << v) | (1 << t) | (1 << q)
    terminal_state = (1 << v) | (1 << t) | (1 << r)
    present = {
        tuple(sorted(edge))
        for edge in {
            (x, u),
            (x, v),
            (x, t),
            (x, q),
            (u, q),
            (u, r),
            (q, r),
        }
    }
    absent = {
        tuple(sorted(edge))
        for edge in {(u, v), (u, t), (v, t), (x, r)}
    }
    all_edges = list(itertools.combinations(range(n), 2))
    free_edges = [edge for edge in all_edges if edge not in present and edge not in absent]
    counts = {
        "graph_completions": 1 << len(free_edges),
        "local_rank_zero_rows": 0,
        "local_secondary_incidences": 0,
        "nondomination_violations": 0,
        "witness_location_or_adjacency_violations": 0,
        "two_secondary_rows": 0,
        "two_secondary_witness_set_intersections": 0,
    }

    def dominates8(state: int, adjacency: tuple[int, ...]) -> bool:
        covered = state
        for vertex in verts(state):
            covered |= adjacency[vertex]
        return covered == all_vertices

    def missed8(state: int, adjacency: tuple[int, ...]) -> set[int]:
        covered = state
        for vertex in verts(state):
            covered |= adjacency[vertex]
        return set(verts(all_vertices ^ covered))

    for assignment in range(1 << len(free_edges)):
        adjacency_list = [0] * n
        selected = set(present)
        for index, edge in enumerate(free_edges):
            if assignment & (1 << index):
                selected.add(edge)
        for a, b in selected:
            adjacency_list[a] |= 1 << b
            adjacency_list[b] |= 1 << a
        adjacency = tuple(adjacency_list)

        if not dominates8(predecessor, adjacency) or not dominates8(terminal_state, adjacency):
            continue
        nonneighbors = all_vertices ^ (1 << x) ^ adjacency[x]
        anchors = root ^ (1 << u)
        ban = {anchors | (1 << z) for z in verts(nonneighbors)}
        if terminal_state not in ban or predecessor in ban:
            continue
        witness_attack = True
        for mover in verts(predecessor):
            if adjacency[mover] & (1 << r):
                successor = (predecessor ^ (1 << mover)) | (1 << r)
                if successor not in ban and dominates8(successor, adjacency):
                    witness_attack = False
                    break
        if not witness_attack:
            continue

        counts["local_rank_zero_rows"] += 1
        witness_sets: dict[int, set[int]] = {}
        secondaries: list[int] = []
        for secondary in (v, t):
            root_response = (root ^ (1 << secondary)) | (1 << r)
            if not (
                adjacency[secondary] & (1 << r)
                and dominates8(root_response, adjacency)
            ):
                continue
            counts["local_secondary_incidences"] += 1
            secondaries.append(secondary)
            alternate = (predecessor ^ (1 << secondary)) | (1 << r)
            alternate_missed = missed8(alternate, adjacency)
            witness_sets[secondary] = alternate_missed
            if not alternate_missed:
                counts["nondomination_violations"] += 1
            if any(
                z in {u, v, t, x, q, r}
                or not adjacency[secondary] & (1 << z)
                for z in alternate_missed
            ):
                counts["witness_location_or_adjacency_violations"] += 1
        if len(secondaries) == 2:
            counts["two_secondary_rows"] += 1
            if witness_sets[v] & witness_sets[t]:
                counts["two_secondary_witness_set_intersections"] += 1
    return counts


def main() -> None:
    direct = direct_root_sweep()
    nonroot = nonroot_sweep()
    nonroot_eight = nonroot_eight_vertex_local_sweep()
    assert direct["local_rows_with_secondary_dominating_response"] == 0
    assert direct["exact_palette_violations"] == 0
    assert nonroot["nondomination_violations"] == 0
    assert nonroot["witness_location_or_adjacency_violations"] == 0
    assert nonroot["two_secondary_witness_set_intersections"] == 0
    assert nonroot["exact_lemma_violations"] == 0
    assert nonroot_eight["nondomination_violations"] == 0
    assert nonroot_eight["witness_location_or_adjacency_violations"] == 0
    assert nonroot_eight["two_secondary_witness_set_intersections"] == 0
    print(
        json.dumps(
            {
                "schema": "rank-zero-secondary-response-local-falsification-v1",
                "direct_root": direct,
                "nonroot_corridor": nonroot,
                "nonroot_corridor_eight_vertices": nonroot_eight,
                "scope": (
                    "all seven-vertex graph completions of the named direct-root "
                    "and nonroot role constraints, plus all eight-vertex nonroot "
                    "completions with two residual witnesses; local sweeps weaken "
                    "family membership to domination"
                ),
                "verdict": "NO_COUNTERMODEL",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
