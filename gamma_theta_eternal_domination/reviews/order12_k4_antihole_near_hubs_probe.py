#!/usr/bin/env python3
"""Clean-room probe for the proposed anti-C7 near-hub lemma.

The one-guard evaluator is implemented directly from the greatest-fixed-point
definition and imports no campaign graph or eternal-domination code.  The
finite calculations are regression evidence for the handwritten proof; they
do not replace induced-subgraph monotonicity or the accepted ambient inputs.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[1]
NOTE = CAMPAIGN / "math/lemmas/order12_k4_antihole_near_hubs.md"
FROZEN_NOTE_SHA256 = (
    "39182554433e413741f15d7c70e89d07389c8d1ebd658ab74c39bc596fc825c5"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def cycle(n: int) -> tuple[int, ...]:
    adjacency = [0] * n
    for vertex in range(n):
        neighbor = (vertex + 1) % n
        adjacency[vertex] |= 1 << neighbor
        adjacency[neighbor] |= 1 << vertex
    return tuple(adjacency)


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    full = (1 << len(adjacency)) - 1
    return tuple(
        (full ^ (1 << vertex)) & ~neighbors
        for vertex, neighbors in enumerate(adjacency)
    )


def add_vertex_with_cycle_neighborhood(
    neighborhood: int,
) -> tuple[int, ...]:
    adjacency = list(cycle(7)) + [0]
    for vertex in range(7):
        if neighborhood >> vertex & 1:
            adjacency[vertex] |= 1 << 7
            adjacency[7] |= 1 << vertex
    return tuple(adjacency)


def two_spoke_graph(
    first_neighbor: int,
    second_neighbor: int,
    outside_edge: bool,
) -> tuple[int, ...]:
    adjacency = list(cycle(7)) + [0, 0]
    for outside, rim in ((7, first_neighbor), (8, second_neighbor)):
        adjacency[outside] |= 1 << rim
        adjacency[rim] |= 1 << outside
    if outside_edge:
        adjacency[7] |= 1 << 8
        adjacency[8] |= 1 << 7
    return tuple(adjacency)


def configuration(vertices: set[int] | tuple[int, ...]) -> int:
    return sum(1 << vertex for vertex in vertices)


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(mask.bit_length())
        if mask >> vertex & 1
    )


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    selected = vertices(state)
    return all(
        not (adjacency[first] >> second & 1)
        for first, second in combinations(selected, 2)
    )


def covered_mask(adjacency: tuple[int, ...], state: int) -> int:
    covered = state
    remaining = state
    while remaining:
        least = remaining & -remaining
        vertex = least.bit_length() - 1
        covered |= adjacency[vertex]
        remaining ^= least
    return covered


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    return covered_mask(adjacency, state) == (1 << len(adjacency)) - 1


def undominated(adjacency: tuple[int, ...], state: int) -> tuple[int, ...]:
    covered = covered_mask(adjacency, state)
    return tuple(
        vertex
        for vertex in range(len(adjacency))
        if not (covered >> vertex & 1)
    )


def legal_successors(
    adjacency: tuple[int, ...],
    state: int,
    attacked: int,
) -> tuple[int, ...]:
    require(not (state >> attacked & 1), "attack must be unoccupied")
    successors: list[int] = []
    guards = state & adjacency[attacked]
    while guards:
        guard = guards & -guards
        successors.append((state ^ guard) | (1 << attacked))
        guards ^= guard
    return tuple(successors)


def eternal_live_states(
    adjacency: tuple[int, ...],
    guard_count: int,
) -> set[int]:
    live = {
        configuration(set(selected))
        for selected in combinations(range(len(adjacency)), guard_count)
        if dominates(adjacency, configuration(set(selected)))
    }
    changed = True
    while changed:
        changed = False
        remove: set[int] = set()
        for state in live:
            for attacked in range(len(adjacency)):
                if state >> attacked & 1:
                    continue
                if not any(
                    successor in live
                    for successor in legal_successors(
                        adjacency,
                        state,
                        attacked,
                    )
                ):
                    remove.add(state)
                    break
        if remove:
            live.difference_update(remove)
            changed = True
    return live


def gamma_infinity(adjacency: tuple[int, ...]) -> int:
    for guard_count in range(1, len(adjacency) + 1):
        if eternal_live_states(adjacency, guard_count):
            return guard_count
    raise AssertionError("all-occupied state must be eternal")


def verify_single_extensions() -> dict[str, object]:
    values: dict[int, int] = {}
    for neighborhood in range(1 << 7):
        values[neighborhood] = gamma_infinity(
            add_vertex_with_cycle_neighborhood(neighborhood)
        )
    require(values[0] == 5, "isolated C7 extension must need five guards")
    require(
        all(values[mask] == 4 for mask in range(1, 1 << 7)),
        "a nonempty C7 attachment unexpectedly needs more than four guards",
    )
    return {
        "extensions_checked": len(values),
        "isolated_value": values[0],
        "nonempty_value_four_count": sum(
            value == 4 for mask, value in values.items() if mask
        ),
    }


def verify_all_two_spokes() -> dict[str, object]:
    counts: dict[int, int] = {}
    for first in range(7):
        for second in range(7):
            for outside_edge in (False, True):
                value = gamma_infinity(
                    two_spoke_graph(first, second, outside_edge)
                )
                counts[value] = counts.get(value, 0) + 1
                expected = 4 if outside_edge and first == second else 5
                require(
                    value == expected,
                    "two-spoke alignment characterization failed",
                )
    require(counts == {4: 7, 5: 91}, "two-spoke value counts differ")
    return {
        "labeled_ordered_extensions_checked": sum(counts.values()),
        "gamma_infinity_counts": {
            str(value): count for value, count in sorted(counts.items())
        },
        "value_four_iff_edge_and_common_neighbor": True,
    }


def verify_independent_five_sets() -> dict[str, object]:
    rim = cycle(7)
    witnesses = 0
    for first in range(7):
        for second in range(7):
            found = False
            for triple in combinations(range(7), 3):
                state = configuration(set(triple))
                if (
                    first not in triple
                    and second not in triple
                    and independent(rim, state)
                ):
                    found = True
                    break
            require(found, "two deleted rim vertices hit every stable triple")
            witnesses += 1
    return {
        "ordered_neighbor_pairs_checked": witnesses,
        "stable_triple_avoiding_each_pair": True,
    }


def verify_attack_table() -> dict[str, object]:
    cases = {
        1: {
            "forced": {1, 3, 6, 7},
            "first_attack": 2,
            "first_good": {2, 3, 6, 7},
            "first_bad": {
                configuration({1, 2, 6, 7}): (4,),
            },
            "second_attack": 0,
            "second_bad": {
                configuration({0, 2, 3, 7}): (5,),
                configuration({0, 2, 3, 6}): (8,),
            },
        },
        2: {
            "forced": {1, 3, 6, 7},
            "first_attack": 0,
            "first_good": {0, 3, 6, 7},
            "first_bad": {
                configuration({0, 1, 3, 7}): (5,),
                configuration({0, 1, 3, 6}): (8,),
            },
            "second_attack": 2,
            "second_bad": {
                configuration({0, 2, 6, 7}): (4,),
            },
        },
        3: {
            "forced": {1, 4, 6, 7},
            "first_attack": 0,
            "first_good": {0, 1, 4, 7},
            "first_bad": {
                configuration({0, 4, 6, 7}): (2,),
                configuration({0, 1, 4, 6}): (8,),
            },
            "second_attack": 3,
            "second_bad": {
                configuration({0, 1, 3, 7}): (5,),
            },
        },
    }
    for distance, case in cases.items():
        adjacency = two_spoke_graph(0, distance, True)
        forced = configuration(case["forced"])
        first_good = configuration(case["first_good"])
        require(independent(adjacency, forced), "forced state is not independent")
        require(dominates(adjacency, forced), "forced state does not dominate")

        first_successors = legal_successors(
            adjacency,
            forced,
            case["first_attack"],
        )
        dominating_first = tuple(
            state for state in first_successors if dominates(adjacency, state)
        )
        require(
            dominating_first == (first_good,),
            "first attack does not have the stated unique dominating response",
        )
        actual_first_bad = {
            state: undominated(adjacency, state)
            for state in first_successors
            if state != first_good
        }
        require(
            actual_first_bad == case["first_bad"],
            "first non-dominating responses differ from table",
        )

        second_successors = legal_successors(
            adjacency,
            first_good,
            case["second_attack"],
        )
        require(
            not any(dominates(adjacency, state) for state in second_successors),
            "second attack has a dominating response",
        )
        actual_second_bad = {
            state: undominated(adjacency, state)
            for state in second_successors
        }
        require(
            actual_second_bad == case["second_bad"],
            "second non-dominating responses differ from table",
        )
    return {
        "dihedral_distance_cases_checked": len(cases),
        "all_forced_states_independent_and_dominating": True,
        "all_first_responses_exact": True,
        "all_second_responses_nondominating": True,
    }


def verify_p3_cap() -> dict[str, object]:
    antihole = complement(cycle(7))
    full = (1 << 7) - 1
    base_triples = (
        (0, 1, 4),
        (0, 2, 5),
        (0, 3, 6),
    )
    no_hub_survivors = 0
    pattern_count = 0
    for gap in range(7):
        triples = tuple(
            tuple((vertex + gap) % 7 for vertex in triple)
            for triple in base_triples
        )
        require(
            set().union(*(set(triple) for triple in triples)) == set(range(7)),
            "rotated P3 triples do not cover the rim",
        )
        for triple in triples:
            triple_mask = configuration(set(triple))
            internal_witnesses = tuple(
                witness
                for witness in range(7)
                if not (triple_mask >> witness & 1)
                and all(
                    antihole[witness] >> vertex & 1
                    for vertex in triple
                )
            )
            require(
                not internal_witnesses,
                "P3 cap triple has an internal antihole witness",
            )
            require(
                not all(
                    ((full ^ (1 << gap)) >> vertex) & 1
                    for vertex in triple
                ),
                "common-gap near-hub witnesses a cap triple",
            )

        for remaining_neighborhood in range(1 << 7):
            pattern_count += 1
            witnesses_all = all(
                all(
                    remaining_neighborhood >> vertex & 1
                    for vertex in triple
                )
                for triple in triples
            )
            if witnesses_all and remaining_neighborhood != full:
                no_hub_survivors += 1
            require(
                not witnesses_all or remaining_neighborhood == full,
                "a non-hub remaining vertex witnesses all cap triples",
            )

    require(no_hub_survivors == 0, "P3 cap has a no-hub survivor")
    return {
        "rotated_gap_cases": 7,
        "remaining_neighborhood_patterns_checked": pattern_count,
        "no_hub_patterns_witnessing_all_three_triples": no_hub_survivors,
        "five_near_hubs_fail_each_triple_immediately": True,
    }


def main() -> None:
    note_hash = sha256(NOTE.read_bytes()).hexdigest()
    require(note_hash == FROZEN_NOTE_SHA256, "proposed note hash differs")
    require(gamma_infinity(cycle(7)) == 4, "C7 sanity value differs")

    report = {
        "schema": "order12-k4-antihole-near-hubs-probe-v1",
        "frozen_note_sha256": note_hash,
        "one_guard_definition": {
            "attacks_only_unoccupied": True,
            "exactly_one_guard_moves_along_one_edge": True,
            "live_family_operator": "greatest_fixed_point",
            "campaign_evaluator_imported": False,
        },
        "cycle_sanity": {"gamma_infinity_C7": 4},
        "single_extensions": verify_single_extensions(),
        "two_spoke_extensions": verify_all_two_spokes(),
        "independent_five_sets": verify_independent_five_sets(),
        "attack_table": verify_attack_table(),
        "p3_cap": verify_p3_cap(),
        "verdict_signal": "PASS_PROPOSED_LEMMA_REGRESSION",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
