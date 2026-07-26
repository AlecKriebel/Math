#!/usr/bin/env python3
"""Small exact probes for the transition/private-neighborhood proof lane.

This is deliberately independent of the campaign's eternal-domination
implementations.  It uses ordinary Python sets, a direct graph6 decoder, and
the definition of the one-guard greatest fixed point.  It invokes only the
pinned ``geng`` graph generator; it does not invoke a SAT solver.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GENG = ROOT / "tools" / "nauty2_9_3" / "geng"
DEFAULT_OUTPUT = ROOT / "results" / "universal_transition_private_probe.json"


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    data = record.strip().encode("ascii")
    if not data or data[0] < 63 or data[0] > 125:
        raise ValueError("only nonempty short graph6 records are accepted")
    n = data[0] - 63
    if n > 62:
        raise ValueError("probe supports graph6 orders at most 62")
    bits: list[int] = []
    for byte in data[1:]:
        if byte < 63 or byte > 126:
            raise ValueError("invalid graph6 payload byte")
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    expected_payload_bytes = (needed + 5) // 6
    if len(data) != 1 + expected_payload_bytes:
        raise ValueError("noncanonical graph6 payload length")
    if any(bits[needed:]):
        raise ValueError("nonzero graph6 padding")
    adjacency = [set() for _ in range(n)]
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                adjacency[left].add(right)
                adjacency[right].add(left)
            cursor += 1
    return tuple(frozenset(row) for row in adjacency)


def graph6_lines(geng: Path, n: int) -> tuple[str, ...]:
    completed = subprocess.run(
        (str(geng), "-q", str(n)),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.stderr:
        raise RuntimeError(f"geng wrote stderr at order {n}: {completed.stderr!r}")
    return tuple(line for line in completed.stdout.splitlines() if line)


def subsets(vertices: range, size: int) -> tuple[frozenset[int], ...]:
    return tuple(frozenset(choice) for choice in itertools.combinations(vertices, size))


def independent(adjacency: tuple[frozenset[int], ...], chosen: frozenset[int]) -> bool:
    return all(not (adjacency[vertex] & chosen) for vertex in chosen)


def dominates(adjacency: tuple[frozenset[int], ...], chosen: frozenset[int]) -> bool:
    dominated = set(chosen)
    for vertex in chosen:
        dominated.update(adjacency[vertex])
    return len(dominated) == len(adjacency)


def alpha(adjacency: tuple[frozenset[int], ...]) -> int:
    vertices = range(len(adjacency))
    for size in range(len(adjacency), 0, -1):
        if any(independent(adjacency, chosen) for chosen in subsets(vertices, size)):
            return size
    return 0


def gamma(adjacency: tuple[frozenset[int], ...]) -> int:
    vertices = range(len(adjacency))
    for size in range(1, len(adjacency) + 1):
        if any(dominates(adjacency, chosen) for chosen in subsets(vertices, size)):
            return size
    raise AssertionError("the full vertex set must dominate")


def dominating_configurations(
    adjacency: tuple[frozenset[int], ...], k: int
) -> frozenset[frozenset[int]]:
    return frozenset(
        chosen
        for chosen in subsets(range(len(adjacency)), k)
        if dominates(adjacency, chosen)
    )


def successors(
    adjacency: tuple[frozenset[int], ...],
    configuration: frozenset[int],
    attack: int,
) -> frozenset[frozenset[int]]:
    if attack in configuration:
        raise ValueError("attacks must be unoccupied")
    return frozenset(
        configuration - {guard} | {attack}
        for guard in configuration
        if guard in adjacency[attack]
    )


def greatest_kernel(
    adjacency: tuple[frozenset[int], ...], k: int
) -> frozenset[frozenset[int]]:
    current = dominating_configurations(adjacency, k)
    vertices = frozenset(range(len(adjacency)))
    while True:
        retained = frozenset(
            configuration
            for configuration in current
            if all(
                successors(adjacency, configuration, attack) & current
                for attack in vertices - configuration
            )
        )
        if retained == current:
            return current
        current = retained


def kernel_rounds(
    adjacency: tuple[frozenset[int], ...], k: int, rounds: int
) -> tuple[frozenset[frozenset[int]], ...]:
    configurations = dominating_configurations(adjacency, k)
    history = [configurations]
    vertices = frozenset(range(len(adjacency)))
    for _ in range(rounds):
        current = history[-1]
        history.append(
            frozenset(
                configuration
                for configuration in configurations
                if all(
                    successors(adjacency, configuration, attack) & current
                    for attack in vertices - configuration
                )
            )
        )
    return tuple(history)


def eternal_number(adjacency: tuple[frozenset[int], ...]) -> int:
    for k in range(alpha(adjacency), len(adjacency) + 1):
        if greatest_kernel(adjacency, k):
            return k
    raise AssertionError("the fully occupied state is eternal")


def maximum_independent_sets(
    adjacency: tuple[frozenset[int], ...], k: int
) -> tuple[frozenset[int], ...]:
    return tuple(
        chosen
        for chosen in subsets(range(len(adjacency)), k)
        if independent(adjacency, chosen)
    )


def private_region(
    adjacency: tuple[frozenset[int], ...],
    configuration: frozenset[int],
    guard: int,
) -> frozenset[int]:
    return frozenset(
        vertex
        for vertex in range(len(adjacency))
        if (adjacency[vertex] | {vertex}) & configuration == {guard}
    )


def viable_lists(
    adjacency: tuple[frozenset[int], ...], reference: frozenset[int]
) -> dict[int, frozenset[int]]:
    result: dict[int, frozenset[int]] = {}
    for attacked in set(range(len(adjacency))) - reference:
        closed = adjacency[attacked] | {attacked}
        result[attacked] = frozenset(
            guard
            for guard in reference
            if guard in adjacency[attacked]
            and private_region(adjacency, reference, guard) <= closed
        )
    return result


def first_hall_violation(
    adjacency: tuple[frozenset[int], ...], reference: frozenset[int]
) -> dict[str, object] | None:
    outside = tuple(sorted(set(range(len(adjacency))) - reference))
    lists = viable_lists(adjacency, reference)
    for size in range(1, len(outside) + 1):
        for choice in itertools.combinations(outside, size):
            chosen = frozenset(choice)
            if not independent(adjacency, chosen):
                continue
            available = frozenset().union(*(lists[vertex] for vertex in chosen))
            if len(available) < size:
                return {
                    "reference": sorted(reference),
                    "independent_outside_set": sorted(chosen),
                    "lists": {
                        str(vertex): sorted(lists[vertex]) for vertex in sorted(chosen)
                    },
                    "union": sorted(available),
                }
    return None


def pointwise_private_condition(
    adjacency: tuple[frozenset[int], ...], k: int
) -> bool:
    return all(
        all(choices for choices in viable_lists(adjacency, reference).values())
        for reference in maximum_independent_sets(adjacency, k)
    )


def all_reference_hall_condition(
    adjacency: tuple[frozenset[int], ...], k: int
) -> bool:
    return all(
        first_hall_violation(adjacency, reference) is None
        for reference in maximum_independent_sets(adjacency, k)
    )


def theta(adjacency: tuple[frozenset[int], ...]) -> int:
    """Exact clique-partition number by a fresh canonical backtracker."""

    n = len(adjacency)
    conflict_degree = [
        n - 1 - len(adjacency[vertex])
        for vertex in range(n)
    ]
    order = tuple(
        sorted(range(n), key=lambda vertex: (-conflict_degree[vertex], vertex))
    )

    def feasible(number_of_parts: int) -> bool:
        parts: list[list[int]] = []

        def search(position: int) -> bool:
            if position == n:
                return True
            vertex = order[position]
            for part in parts:
                if all(other in adjacency[vertex] for other in part):
                    part.append(vertex)
                    if search(position + 1):
                        return True
                    part.pop()
            if len(parts) < number_of_parts:
                parts.append([vertex])
                if search(position + 1):
                    return True
                parts.pop()
            return False

        return search(0)

    lower = alpha(adjacency)
    for number_of_parts in range(lower, n + 1):
        if feasible(number_of_parts):
            return number_of_parts
    raise AssertionError("singleton parts always form a clique partition")


def is_eternal_subfamily(
    adjacency: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
) -> bool:
    if not family:
        return False
    vertices = frozenset(range(len(adjacency)))
    return all(
        all(
            successors(adjacency, configuration, attack) & family
            for attack in vertices - configuration
        )
        for configuration in family
    )


def inclusion_minimal_families(
    adjacency: tuple[frozenset[int], ...], k: int
) -> tuple[frozenset[frozenset[int]], ...]:
    configurations = tuple(sorted(dominating_configurations(adjacency, k), key=sorted))
    if len(configurations) > 20:
        raise ValueError("family enumeration deliberately capped at 20 states")
    minimal: list[frozenset[frozenset[int]]] = []
    for size in range(1, len(configurations) + 1):
        for indices in itertools.combinations(range(len(configurations)), size):
            family = frozenset(configurations[index] for index in indices)
            if any(previous <= family for previous in minimal):
                continue
            if is_eternal_subfamily(adjacency, family):
                minimal.append(family)
    return tuple(minimal)


def transfer_labeling(
    old_configuration: frozenset[int],
    old_labels: tuple[tuple[int, int], ...],
    new_configuration: frozenset[int],
) -> tuple[tuple[int, int], ...]:
    removed = tuple(old_configuration - new_configuration)
    added = tuple(new_configuration - old_configuration)
    if len(removed) != 1 or len(added) != 1:
        raise ValueError("transition must replace exactly one guard")
    labels = dict(old_labels)
    label = labels.pop(removed[0])
    labels[added[0]] = label
    return tuple(sorted(labels.items()))


def labeling_obstruction(
    adjacency: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
    reference: frozenset[int],
) -> dict[str, object] | None:
    initial = tuple((vertex, label) for label, vertex in enumerate(sorted(reference)))
    pending = [(reference, initial)]
    seen = {(reference, initial)}
    vertex_labels: dict[int, set[int]] = {vertex: set() for vertex in range(len(adjacency))}
    configuration_labels: dict[frozenset[int], set[tuple[tuple[int, int], ...]]] = {}
    while pending:
        configuration, labels = pending.pop()
        configuration_labels.setdefault(configuration, set()).add(labels)
        for vertex, label in labels:
            vertex_labels[vertex].add(label)
        for neighbor in family:
            removed = tuple(configuration - neighbor)
            added = tuple(neighbor - configuration)
            if (
                len(removed) != 1
                or len(added) != 1
                or added[0] not in adjacency[removed[0]]
            ):
                continue
            next_labels = transfer_labeling(configuration, labels, neighbor)
            state = (neighbor, next_labels)
            if state not in seen:
                seen.add(state)
                pending.append(state)
    ambiguous_vertices = {
        str(vertex): sorted(labels)
        for vertex, labels in vertex_labels.items()
        if len(labels) > 1
    }
    holonomy_states = {
        ",".join(map(str, sorted(configuration))): len(labelings)
        for configuration, labelings in configuration_labels.items()
        if len(labelings) > 1
    }
    if ambiguous_vertices or holonomy_states:
        return {
            "reference": sorted(reference),
            "family": [sorted(configuration) for configuration in sorted(family, key=sorted)],
            "ambiguous_vertices": ambiguous_vertices,
            "holonomy_states": holonomy_states,
        }
    return None


def response_table(
    adjacency: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
) -> dict[str, list[dict[str, object]]]:
    vertices = frozenset(range(len(adjacency)))
    table: dict[str, list[dict[str, object]]] = {}
    for configuration in sorted(family, key=sorted):
        rows: list[dict[str, object]] = []
        for attack in sorted(vertices - configuration):
            legal = sorted(
                successors(adjacency, configuration, attack) & family,
                key=sorted,
            )
            if not legal:
                raise AssertionError("the requested family is not eternal")
            successor = legal[0]
            guard = next(iter(configuration - successor))
            rows.append(
                {
                    "attack": attack,
                    "move": [guard, attack],
                    "successor": sorted(successor),
                }
            )
        table[",".join(map(str, sorted(configuration)))] = rows
    return table


def unique_response_hamiltonian_cycle(
    adjacency: tuple[frozenset[int], ...],
    family: frozenset[frozenset[int]],
) -> list[dict[str, object]] | None:
    vertices = frozenset(range(len(adjacency)))
    arcs: dict[frozenset[int], list[tuple[frozenset[int], int]]] = {
        configuration: [] for configuration in family
    }
    for configuration in family:
        for attack in sorted(vertices - configuration):
            legal = successors(adjacency, configuration, attack) & family
            if len(legal) == 1:
                arcs[configuration].append((next(iter(legal)), attack))
    start = min(family, key=lambda configuration: tuple(sorted(configuration)))
    path = [start]

    def search() -> tuple[int, ...] | None:
        current = path[-1]
        if len(path) == len(family):
            for successor, attack in arcs[current]:
                if successor == start:
                    return (attack,)
            return None
        for successor, attack in arcs[current]:
            if successor in path:
                continue
            path.append(successor)
            suffix = search()
            if suffix is not None:
                return (attack,) + suffix
            path.pop()
        return None

    attacks = search()
    if attacks is None:
        return None
    targets = path[1:] + [start]
    return [
        {
            "state": sorted(state),
            "attack": attack,
            "unique_successor": sorted(target),
        }
        for state, attack, target in zip(path, attacks, targets)
    ]


def graph_record(
    graph6: str, adjacency: tuple[frozenset[int], ...], k: int
) -> dict[str, object]:
    return {
        "graph6": graph6,
        "n": len(adjacency),
        "m": sum(map(len, adjacency)) // 2,
        "k": k,
        "edges": [
            [left, right]
            for left in range(len(adjacency))
            for right in sorted(adjacency[left])
            if left < right
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geng", type=Path, default=DEFAULT_GENG)
    parser.add_argument("--max-order", type=int, default=7)
    parser.add_argument("--minimal-family-max-order", type=int, default=5)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    geng = arguments.geng.resolve()
    if not geng.is_file():
        raise SystemExit(f"missing pinned geng: {geng}")

    started = time.monotonic()
    counts: dict[str, dict[str, int]] = {}
    first_hall: dict[str, object] | None = None
    first_labeling: dict[str, object] | None = None
    first_nonclique_response_cell: dict[str, object] | None = None
    minimum_family_counts = {
        "families": 0,
        "global_labeling_obstructions": 0,
    }

    for n in range(1, arguments.max_order + 1):
        rows = graph6_lines(geng, n)
        equal_graphs = 0
        references = 0
        hall_violations = 0
        minimal_families = 0
        labeling_obstructions = 0
        for graph6 in rows:
            adjacency = decode_graph6(graph6)
            k = alpha(adjacency)
            if gamma(adjacency) != k:
                continue
            kernel = greatest_kernel(adjacency, k)
            if not kernel:
                continue
            equal_graphs += 1
            independent_sets = maximum_independent_sets(adjacency, k)
            for reference in independent_sets:
                references += 1
                lists = viable_lists(adjacency, reference)
                if first_nonclique_response_cell is None:
                    for guard in sorted(reference):
                        candidates = sorted(
                            vertex for vertex, choices in lists.items() if guard in choices
                        )
                        for left, right in itertools.combinations(candidates, 2):
                            if right not in adjacency[left]:
                                first_nonclique_response_cell = {
                                    **graph_record(graph6, adjacency, k),
                                    "reference": sorted(reference),
                                    "guard": guard,
                                    "nonadjacent_viable_attacks": [left, right],
                                    "private_region": sorted(
                                        private_region(adjacency, reference, guard)
                                    ),
                                }
                                break
                        if first_nonclique_response_cell is not None:
                            break
                violation = first_hall_violation(adjacency, reference)
                if violation is not None:
                    hall_violations += 1
                    if first_hall is None:
                        first_hall = {
                            **graph_record(graph6, adjacency, k),
                            **violation,
                        }
            if n <= arguments.minimal_family_max_order:
                families = inclusion_minimal_families(adjacency, k)
                minimal_families += len(families)
                reference = independent_sets[0]
                minimum_size = min(map(len, families))
                for family in families:
                    obstruction = labeling_obstruction(adjacency, family, reference)
                    if obstruction is not None:
                        labeling_obstructions += 1
                        if first_labeling is None:
                            first_labeling = {
                                **graph_record(graph6, adjacency, k),
                                **obstruction,
                            }
                    if len(family) == minimum_size:
                        minimum_family_counts["families"] += 1
                        if obstruction is not None:
                            minimum_family_counts[
                                "global_labeling_obstructions"
                            ] += 1
        counts[str(n)] = {
            "unlabeled_graphs": len(rows),
            "gamma_alpha_eternal_equal_graphs": equal_graphs,
            "maximum_independent_references": references,
            "independent_set_hall_violations": hall_violations,
            "minimal_eternal_families_enumerated": minimal_families,
            "minimal_family_labeling_obstructions": labeling_obstructions,
        }

    c7 = decode_graph6("FCp`_")
    c7_k = alpha(c7)
    c7_reference = frozenset({0, 1, 2})
    c7_hall = first_hall_violation(c7, c7_reference)
    if c7_hall is None:
        raise AssertionError("expected the fixed C7 Hall witness")

    c15 = tuple(
        frozenset({(vertex - 1) % 15, (vertex + 1) % 15})
        for vertex in range(15)
    )
    c15_k = alpha(c15)
    c15_reference = frozenset({0, 2, 4, 6, 8, 10, 12})
    c15_hall = first_hall_violation(c15, c15_reference)
    if c15_hall is None:
        raise AssertionError("expected the fixed C15 Hall witness")
    c15_rounds = kernel_rounds(c15, c15_k, 3)

    holonomy_graph6 = "E]~o"
    holonomy_graph = decode_graph6(holonomy_graph6)
    holonomy_k = alpha(holonomy_graph)
    holonomy_families = inclusion_minimal_families(holonomy_graph, holonomy_k)
    holonomy_reference = maximum_independent_sets(holonomy_graph, holonomy_k)[0]
    holonomy_witnesses = [
        labeling_obstruction(holonomy_graph, family, holonomy_reference)
        for family in holonomy_families
    ]
    holonomy_witness = next(
        witness for witness in holonomy_witnesses if witness is not None
    )

    hall_insufficiency_graph6 = "J@l|bfNuVK_"
    hall_insufficiency_graph = decode_graph6(hall_insufficiency_graph6)
    hall_insufficiency_k = alpha(hall_insufficiency_graph)
    hall_insufficiency_kernel = greatest_kernel(
        hall_insufficiency_graph, hall_insufficiency_k
    )

    odd_cycle_parity_graph6 = "FUzro"
    odd_cycle_parity_graph = decode_graph6(odd_cycle_parity_graph6)
    odd_cycle_parity_k = alpha(odd_cycle_parity_graph)

    payload = {
        "schema": "universal-transition-private-probe-v1",
        "classification": "OBSERVED",
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one adjacent guard moves to the attack",
            "successor_requirement": "every retained state dominates",
        },
        "method": {
            "graph_generator": str(geng),
            "graph_generator_sha256": hashlib.sha256(geng.read_bytes()).hexdigest(),
            "orders": [1, arguments.max_order],
            "minimal_family_orders": [1, arguments.minimal_family_max_order],
            "solver": None,
            "eternal_core": "independent ordinary-set greatest-fixed-point implementation in this file",
        },
        "counts": counts,
        "minimum_cardinality_family_observation": {
            "orders": [1, arguments.minimal_family_max_order],
            **minimum_family_counts,
        },
        "first_nonclique_one_step_response_cell": first_nonclique_response_cell,
        "first_independent_set_viable_list_hall_violation": first_hall,
        "first_minimal_family_global_labeling_obstruction": first_labeling,
        "strictness_and_limit_witnesses": {
            "hall_strictly_stronger_than_pointwise_private_condition": {
                **graph_record("FCp`_", c7, c7_k),
                "pointwise_condition_on_every_maximum_independent_set": (
                    pointwise_private_condition(c7, c7_k)
                ),
                "hall_witness": c7_hall,
                "size_k_eternal_kernel_nonempty": bool(greatest_kernel(c7, c7_k)),
            },
            "hall_not_implied_by_two_ply_survival": {
                "graph": "C15",
                "n": 15,
                "m": 15,
                "k": c15_k,
                "kernel_sizes_K0_through_K3": [
                    len(level) for level in c15_rounds
                ],
                "every_maximum_independent_set_in_K2": all(
                    reference in c15_rounds[2]
                    for reference in maximum_independent_sets(c15, c15_k)
                ),
                "hall_witness": c15_hall,
            },
            "inclusion_minimal_family_need_not_have_global_guard_labels": {
                **graph_record(holonomy_graph6, holonomy_graph, holonomy_k),
                "gamma": gamma(holonomy_graph),
                "theta": theta(holonomy_graph),
                "number_of_inclusion_minimal_eternal_families": len(
                    holonomy_families
                ),
                "witness": holonomy_witness,
                "eternal_response_table": response_table(
                    holonomy_graph,
                    next(
                        family
                        for family, witness in zip(
                            holonomy_families, holonomy_witnesses
                        )
                        if witness is not None
                    ),
                ),
                "unique_response_cycle_proving_inclusion_minimality": (
                    unique_response_hamiltonian_cycle(
                        holonomy_graph,
                        next(
                            family
                            for family, witness in zip(
                                holonomy_families, holonomy_witnesses
                            )
                            if witness is not None
                        ),
                    )
                ),
            },
            "hall_condition_does_not_force_clique_partition": {
                **graph_record(
                    hall_insufficiency_graph6,
                    hall_insufficiency_graph,
                    hall_insufficiency_k,
                ),
                "gamma": gamma(hall_insufficiency_graph),
                "alpha": hall_insufficiency_k,
                "gamma_infinity": eternal_number(hall_insufficiency_graph),
                "theta": theta(hall_insufficiency_graph),
                "all_reference_hall_condition": all_reference_hall_condition(
                    hall_insufficiency_graph, hall_insufficiency_k
                ),
                "size_k_eternal_kernel_nonempty": bool(
                    hall_insufficiency_kernel
                ),
            },
            "smallest_odd_cycle_parity_limit_found": {
                **graph_record(
                    odd_cycle_parity_graph6,
                    odd_cycle_parity_graph,
                    odd_cycle_parity_k,
                ),
                "description": "the complement of C7",
                "gamma": gamma(odd_cycle_parity_graph),
                "alpha": odd_cycle_parity_k,
                "gamma_infinity": eternal_number(odd_cycle_parity_graph),
                "theta": theta(odd_cycle_parity_graph),
                "all_reference_hall_condition": all_reference_hall_condition(
                    odd_cycle_parity_graph, odd_cycle_parity_k
                ),
                "reference": [0, 1],
                "viable_lists": {
                    str(vertex): sorted(choices)
                    for vertex, choices in viable_lists(
                        odd_cycle_parity_graph, frozenset({0, 1})
                    ).items()
                },
                "size_k_eternal_kernel_nonempty": bool(
                    greatest_kernel(odd_cycle_parity_graph, odd_cycle_parity_k)
                ),
            },
        },
        "elapsed_seconds": time.monotonic() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(encoded, encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
