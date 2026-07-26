#!/usr/bin/env python3
"""Independent finite probe for the simplicial-neighborhood reduction.

The only external executable used is nauty's ``geng``, solely as a source of
one graph6 representative of each unlabeled graph.  Graph6 decoding, graph
parameters, the one-guard eternal safety game, and every reduction check are
implemented here with Python integer masks.  No campaign evaluator is imported.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import platform
import subprocess
import sys


EXPECTED_UNLABELED_COUNTS = {
    1: 1,
    2: 2,
    3: 4,
    4: 11,
    5: 34,
    6: 156,
    7: 1044,
    8: 12346,
}


def require(condition: bool, label: str, **context: object) -> None:
    if not condition:
        payload = {"failed_check": label, **context}
        raise AssertionError(json.dumps(payload, sort_keys=True))


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_graph6(encoded: str) -> tuple[int, ...]:
    """Decode the small graph6 format (orders at most 62)."""

    raw = encoded.encode("ascii")
    require(bool(raw), "graph6_nonempty", graph6=encoded)
    require(raw[0] != 126, "small_graph6_header", graph6=encoded)
    order = raw[0] - 63
    require(0 <= order <= 62, "graph6_order", graph6=encoded, order=order)

    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        require(0 <= value < 64, "graph6_payload_byte", graph6=encoded)
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))

    needed = order * (order - 1) // 2
    require(len(bits) >= needed, "graph6_payload_length", graph6=encoded)
    require(
        not any(bits[needed:]),
        "graph6_nonzero_padding",
        graph6=encoded,
    )

    adjacency = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1

    for vertex, neighborhood in enumerate(adjacency):
        require(
            not neighborhood & (1 << vertex),
            "loop_free",
            graph6=encoded,
            vertex=vertex,
        )
        for neighbor in range(order):
            require(
                bool(neighborhood & (1 << neighbor))
                == bool(adjacency[neighbor] & (1 << vertex)),
                "symmetric_adjacency",
                graph6=encoded,
                vertex=vertex,
                neighbor=neighbor,
            )
    return tuple(adjacency)


def unlabeled_graphs(
    geng: Path, maximum_order: int
) -> Iterable[tuple[int, str, tuple[int, ...]]]:
    for order in range(1, maximum_order + 1):
        completed = subprocess.run(
            [str(geng), "-q", str(order)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
        if order in EXPECTED_UNLABELED_COUNTS:
            require(
                len(lines) == EXPECTED_UNLABELED_COUNTS[order],
                "unlabeled_graph_count",
                order=order,
                expected=EXPECTED_UNLABELED_COUNTS[order],
                observed=len(lines),
            )
        require(
            len(lines) == len(set(lines)),
            "distinct_graph6_records",
            order=order,
        )
        for encoded in lines:
            adjacency = decode_graph6(encoded)
            require(
                len(adjacency) == order,
                "decoded_order",
                graph6=encoded,
                expected=order,
                observed=len(adjacency),
            )
            yield order, encoded, adjacency


def is_clique(adjacency: tuple[int, ...], state: int) -> bool:
    cursor = state
    while cursor:
        bit = cursor & -cursor
        vertex = bit.bit_length() - 1
        if (state ^ bit) & ~adjacency[vertex]:
            return False
        cursor ^= bit
    return True


def is_independent(adjacency: tuple[int, ...], state: int) -> bool:
    cursor = state
    while cursor:
        bit = cursor & -cursor
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & (state ^ bit):
            return False
        cursor ^= bit
    return True


def is_dominating(adjacency: tuple[int, ...], state: int) -> bool:
    dominated = state
    cursor = state
    while cursor:
        bit = cursor & -cursor
        vertex = bit.bit_length() - 1
        dominated |= adjacency[vertex]
        cursor ^= bit
    return dominated == (1 << len(adjacency)) - 1


def states_of_size(order: int, size: int) -> Iterable[int]:
    for vertices in combinations(range(order), size):
        state = 0
        for vertex in vertices:
            state |= 1 << vertex
        yield state


def domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(len(adjacency) + 1):
        if any(is_dominating(adjacency, state) for state in states_of_size(len(adjacency), size)):
            return size
    raise AssertionError("full vertex set failed to dominate")


def independent_states(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        state
        for state in range(1 << len(adjacency))
        if is_independent(adjacency, state)
    )


def independence_number(adjacency: tuple[int, ...]) -> int:
    return max(state.bit_count() for state in independent_states(adjacency))


def maximal_independent_sizes(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            state.bit_count()
            for state in independent_states(adjacency)
            if is_dominating(adjacency, state)
        )
    )


def clique_partition_number(adjacency: tuple[int, ...]) -> int:
    order = len(adjacency)
    full = (1 << order) - 1
    clique = tuple(is_clique(adjacency, state) for state in range(1 << order))
    memo = {0: 0}

    def solve(remaining: int) -> int:
        if remaining in memo:
            return memo[remaining]
        anchor = remaining & -remaining
        best = order + 1
        part = remaining
        while part:
            if part & anchor and clique[part]:
                best = min(best, 1 + solve(remaining ^ part))
            part = (part - 1) & remaining
        memo[remaining] = best
        return best

    return solve(full)


def eternal_kernel(adjacency: tuple[int, ...], guard_count: int) -> frozenset[int]:
    """Greatest closed family of dominating ``guard_count``-states."""

    order = len(adjacency)
    full = (1 << order) - 1
    alive = {
        state
        for state in states_of_size(order, guard_count)
        if is_dominating(adjacency, state)
    }
    while True:
        retained: set[int] = set()
        for state in alive:
            valid = True
            attacks = full ^ state
            while attacks:
                attack_bit = attacks & -attacks
                attacked = attack_bit.bit_length() - 1
                responders = adjacency[attacked] & state
                witnessed = False
                while responders:
                    guard_bit = responders & -responders
                    successor = (state ^ guard_bit) | attack_bit
                    if successor in alive:
                        witnessed = True
                        break
                    responders ^= guard_bit
                if not witnessed:
                    valid = False
                    break
                attacks ^= attack_bit
            if valid:
                retained.add(state)
        if retained == alive:
            return frozenset(alive)
        alive = retained


def eternal_domination(
    adjacency: tuple[int, ...], lower_bound: int
) -> tuple[int, frozenset[int]]:
    for guard_count in range(lower_bound, len(adjacency) + 1):
        family = eternal_kernel(adjacency, guard_count)
        if family:
            return guard_count, family
    raise AssertionError("full occupied state was not eternally closed")


def induced_adjacency(
    adjacency: tuple[int, ...], kept: tuple[int, ...]
) -> tuple[int, ...]:
    new_index = {old: new for new, old in enumerate(kept)}
    induced: list[int] = []
    for old_vertex in kept:
        neighborhood = 0
        for old_neighbor in kept:
            if adjacency[old_vertex] & (1 << old_neighbor):
                neighborhood |= 1 << new_index[old_neighbor]
        induced.append(neighborhood)
    return tuple(induced)


def project_state(state: int, kept: tuple[int, ...]) -> int:
    projected = 0
    for new_vertex, old_vertex in enumerate(kept):
        if state & (1 << old_vertex):
            projected |= 1 << new_vertex
    return projected


def lift_state(state: int, kept: tuple[int, ...]) -> int:
    lifted = 0
    for new_vertex, old_vertex in enumerate(kept):
        if state & (1 << new_vertex):
            lifted |= 1 << old_vertex
    return lifted


def connected(adjacency: tuple[int, ...]) -> bool:
    if not adjacency:
        return False
    full = (1 << len(adjacency)) - 1
    reached = 1
    frontier = 1
    while frontier:
        neighbors = 0
        cursor = frontier
        while cursor:
            bit = cursor & -cursor
            vertex = bit.bit_length() - 1
            neighbors |= adjacency[vertex]
            cursor ^= bit
        frontier = neighbors & ~reached
        reached |= frontier
    return reached == full


def fresh_order_row() -> dict[str, int]:
    return {
        "graphs": 0,
        "gamma_equals_gamma_eternal_graphs": 0,
        "eligible_graphs": 0,
        "eligible_simplicial_vertices": 0,
        "q_empty_simplicial_vertices": 0,
        "projected_states": 0,
        "projected_attack_obligations": 0,
        "states_in_v_slices": 0,
        "independent_target_states": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-order", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require(1 <= args.maximum_order <= 8, "supported_maximum_order")

    review_directory = Path(__file__).resolve().parent
    repository = review_directory.parents[1]
    geng = repository / "tools" / "nauty2_9_3" / "geng"
    target = repository / "math" / "lemmas" / "simplicial_neighborhood_reduction.md"
    output = args.output or review_directory / "probe_result.json"
    require(geng.is_file(), "geng_exists", path=str(geng))
    require(target.is_file(), "target_exists", path=str(target))
    require(
        output.resolve().parent == review_directory,
        "output_confined_to_review_directory",
        output=str(output.resolve()),
        review_directory=str(review_directory),
    )

    by_order = {
        str(order): fresh_order_row()
        for order in range(1, args.maximum_order + 1)
    }
    totals = fresh_order_row()
    totals["connected_no_simplicial_graphs"] = 0
    totals["counterexamples_gamma_equals_gamma_eternal_less_than_theta"] = 0
    totals["counterexample_eligible_simplicial_vertices"] = 0

    for order, encoded, adjacency in unlabeled_graphs(geng, args.maximum_order):
        row = by_order[str(order)]
        row["graphs"] += 1
        totals["graphs"] += 1

        has_simplicial = any(
            is_clique(adjacency, adjacency[vertex] | (1 << vertex))
            for vertex in range(order)
        )
        if connected(adjacency) and not has_simplicial:
            totals["connected_no_simplicial_graphs"] += 1
            require(
                min(mask.bit_count() for mask in adjacency) >= 2,
                "no_simplicial_implies_minimum_degree_two",
                graph6=encoded,
            )
            for vertex, neighborhood in enumerate(adjacency):
                if neighborhood.bit_count() != 2:
                    continue
                pair = tuple(
                    neighbor
                    for neighbor in range(order)
                    if neighborhood & (1 << neighbor)
                )
                require(
                    not adjacency[pair[0]] & (1 << pair[1]),
                    "degree_two_neighbors_nonadjacent",
                    graph6=encoded,
                    vertex=vertex,
                    neighbors=pair,
                )

        gamma = domination_number(adjacency)
        gamma_eternal, family = eternal_domination(adjacency, gamma)
        if gamma != gamma_eternal:
            continue

        row["gamma_equals_gamma_eternal_graphs"] += 1
        totals["gamma_equals_gamma_eternal_graphs"] += 1
        alpha = independence_number(adjacency)
        theta = clique_partition_number(adjacency)
        maximal_sizes = maximal_independent_sizes(adjacency)
        require(alpha == gamma, "equality_collapse_alpha", graph6=encoded)
        require(
            set(maximal_sizes) == {gamma},
            "equality_collapse_well_covered",
            graph6=encoded,
            maximal_independent_sizes=maximal_sizes,
            gamma=gamma,
        )

        independent_targets = tuple(
            state
            for state in independent_states(adjacency)
            if state.bit_count() == gamma
        )
        row["independent_target_states"] += len(independent_targets)
        totals["independent_target_states"] += len(independent_targets)
        for target_state in independent_targets:
            require(
                target_state in family,
                "independent_target_in_greatest_family",
                graph6=encoded,
                target_state=target_state,
            )
            for state in family:
                if state == target_state:
                    continue
                missing = target_state & ~state
                require(
                    bool(missing),
                    "proper_target_progress_has_missing_attack",
                    graph6=encoded,
                    state=state,
                    target_state=target_state,
                )
                attack_bit = missing & -missing
                attacked = attack_bit.bit_length() - 1
                responders = adjacency[attacked] & state
                require(
                    not responders & target_state,
                    "independence_forces_external_responder",
                    graph6=encoded,
                    state=state,
                    target_state=target_state,
                    attacked=attacked,
                )
                require(
                    any(
                        ((state ^ guard_bit) | attack_bit) in family
                        for guard_bit in (
                            1 << guard
                            for guard in range(order)
                            if responders & (1 << guard)
                        )
                    ),
                    "target_progress_has_family_response",
                    graph6=encoded,
                    state=state,
                    target_state=target_state,
                    attacked=attacked,
                )

        if theta > gamma:
            totals[
                "counterexamples_gamma_equals_gamma_eternal_less_than_theta"
            ] += 1

        eligible_in_graph = 0
        for vertex in range(order):
            vertex_bit = 1 << vertex
            closed = adjacency[vertex] | vertex_bit
            if not is_clique(adjacency, closed):
                continue

            outside = ((1 << order) - 1) ^ closed
            if not outside:
                row["q_empty_simplicial_vertices"] += 1
                totals["q_empty_simplicial_vertices"] += 1
                require(
                    is_clique(adjacency, (1 << order) - 1),
                    "q_empty_graph_complete",
                    graph6=encoded,
                    vertex=vertex,
                )
                require(
                    gamma == gamma_eternal == theta == 1,
                    "q_empty_complete_parameters",
                    graph6=encoded,
                    vertex=vertex,
                    gamma=gamma,
                    gamma_eternal=gamma_eternal,
                    theta=theta,
                )
                continue

            eligible_in_graph += 1
            row["eligible_simplicial_vertices"] += 1
            totals["eligible_simplicial_vertices"] += 1
            if theta > gamma:
                totals["counterexample_eligible_simplicial_vertices"] += 1

            kept = tuple(
                old_vertex
                for old_vertex in range(order)
                if outside & (1 << old_vertex)
            )
            q_adjacency = induced_adjacency(adjacency, kept)
            q_gamma = domination_number(q_adjacency)
            q_alpha = independence_number(q_adjacency)
            q_gamma_eternal, q_family = eternal_domination(q_adjacency, q_gamma)
            q_theta = clique_partition_number(q_adjacency)
            q_maximal_sizes = maximal_independent_sizes(q_adjacency)

            require(
                q_gamma == gamma - 1,
                "q_domination_number",
                graph6=encoded,
                vertex=vertex,
                gamma=gamma,
                q_gamma=q_gamma,
            )
            require(
                q_alpha == gamma - 1,
                "q_independence_number",
                graph6=encoded,
                vertex=vertex,
                gamma=gamma,
                q_alpha=q_alpha,
            )
            require(
                q_gamma_eternal == gamma - 1,
                "q_eternal_domination_number",
                graph6=encoded,
                vertex=vertex,
                gamma=gamma,
                q_gamma_eternal=q_gamma_eternal,
            )
            require(
                set(q_maximal_sizes) == {gamma - 1},
                "q_well_covered",
                graph6=encoded,
                vertex=vertex,
                gamma=gamma,
                maximal_independent_sizes=q_maximal_sizes,
            )
            require(
                theta == q_theta + 1,
                "clique_partition_identity",
                graph6=encoded,
                vertex=vertex,
                theta=theta,
                q_theta=q_theta,
            )

            sliced_states = tuple(
                state for state in family if state & vertex_bit
            )
            row["states_in_v_slices"] += len(sliced_states)
            totals["states_in_v_slices"] += len(sliced_states)
            require(
                bool(sliced_states),
                "nonempty_v_slice",
                graph6=encoded,
                vertex=vertex,
            )

            projected: set[int] = set()
            for state in sliced_states:
                require(
                    not state & adjacency[vertex],
                    "no_state_contains_v_and_neighbor",
                    graph6=encoded,
                    vertex=vertex,
                    state=state,
                )
                q_state = project_state(state ^ vertex_bit, kept)
                require(
                    q_state.bit_count() == gamma - 1,
                    "projected_state_size",
                    graph6=encoded,
                    vertex=vertex,
                    state=state,
                    q_state=q_state,
                )
                require(
                    is_dominating(q_adjacency, q_state),
                    "projected_state_dominates_q",
                    graph6=encoded,
                    vertex=vertex,
                    state=state,
                    q_state=q_state,
                )
                projected.add(q_state)

            require(
                len(projected) == len(sliced_states),
                "projection_is_injective_on_v_slice",
                graph6=encoded,
                vertex=vertex,
            )
            row["projected_states"] += len(projected)
            totals["projected_states"] += len(projected)

            full_q = (1 << len(q_adjacency)) - 1
            for q_state in projected:
                lifted = lift_state(q_state, kept) | vertex_bit
                require(
                    lifted in family,
                    "projected_state_lifts_to_original_family",
                    graph6=encoded,
                    vertex=vertex,
                    q_state=q_state,
                )
                attacks = full_q ^ q_state
                while attacks:
                    attack_bit = attacks & -attacks
                    attacked = attack_bit.bit_length() - 1
                    responders = q_adjacency[attacked] & q_state
                    witnesses = [
                        guard
                        for guard in range(len(q_adjacency))
                        if responders & (1 << guard)
                        and ((q_state ^ (1 << guard)) | attack_bit) in projected
                    ]
                    require(
                        bool(witnesses),
                        "projected_forall_attack_exists_response_closure",
                        graph6=encoded,
                        vertex=vertex,
                        q_state=q_state,
                        attacked=attacked,
                    )
                    for guard in witnesses:
                        old_guard = kept[guard]
                        old_attacked = kept[attacked]
                        old_successor = (
                            lifted ^ (1 << old_guard)
                        ) | (1 << old_attacked)
                        require(
                            old_successor in family,
                            "projected_witness_is_lifted_family_move",
                            graph6=encoded,
                            vertex=vertex,
                            q_state=q_state,
                            attacked=attacked,
                            guard=guard,
                        )
                    row["projected_attack_obligations"] += 1
                    totals["projected_attack_obligations"] += 1
                    attacks ^= attack_bit

            require(
                projected.issubset(q_family),
                "projected_family_within_q_greatest_kernel",
                graph6=encoded,
                vertex=vertex,
            )

        if eligible_in_graph:
            row["eligible_graphs"] += 1
            totals["eligible_graphs"] += 1

    expected_total = sum(
        EXPECTED_UNLABELED_COUNTS[order]
        for order in range(1, args.maximum_order + 1)
    )
    require(
        totals["graphs"] == expected_total,
        "total_unlabeled_graph_count",
        expected=expected_total,
        observed=totals["graphs"],
    )

    result = {
        "schema": "simplicial-neighborhood-hostile-probe-v1",
        "verdict": "PASS",
        "model": {
            "attacks": "unoccupied vertices only",
            "response": "exactly one guard moves along one edge to the attack",
            "family_quantifiers": "for every family state and every unoccupied attack, at least one successor remains in the family",
        },
        "scope": {
            "maximum_order": args.maximum_order,
            "unlabeled_graphs": "all graph6 representatives supplied by nauty geng",
            "eligible_vertex": "simplicial v in a graph with gamma=gamma_eternal and nonempty G-N[v]",
            "projected_family": "the v-slice of the independently computed greatest eternal k-family",
        },
        "implementation": {
            "language": "Python standard library only",
            "graph_representation": "integer adjacency masks",
            "eternal_solver": "independent greatest-fixed-point elimination",
            "campaign_evaluator_imports": False,
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "hashes": {
            "target_sha256": file_sha256(target),
            "probe_sha256": file_sha256(Path(__file__).resolve()),
            "geng_sha256": file_sha256(geng),
        },
        "counts_by_order": by_order,
        "totals": totals,
        "limitations": [
            "The finite probe is a falsification check, not a proof beyond order 8.",
            "It directly projects the greatest eternal family; the theorem's assertion for every eternal subfamily is established analytically by independent-target forcing, not by enumerating all subfamilies.",
            "No gamma=gamma_eternal<theta graph exists in this order range, so finite counterexample-preservation checks are vacuous.",
        ],
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
