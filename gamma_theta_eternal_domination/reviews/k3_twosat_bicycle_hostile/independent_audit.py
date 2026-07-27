#!/usr/bin/env python3
"""Clean-room hostile audit for the k=3 2-SAT-bicycle lane.

This file imports no code from the target evidence generator.  It uses
ordinary Python sets, direct truth tables, exhaustive subset checks, and a
literal greatest-fixed-point deletion implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import subprocess
import time
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
CAMPAIGN = REPOSITORY / "gamma_theta_eternal_domination"
TARGET = CAMPAIGN / "math" / "working" / "k3_twosat_bicycle"
GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"

Edge = tuple[int, int]
State = frozenset[int]


def canonical_edge(left: int, right: int) -> Edge:
    if left == right:
        raise ValueError("loops are not graph edges")
    return (left, right) if left < right else (right, left)


def all_pairs(vertices):
    return itertools.combinations(vertices, 2)


def graph6_decode(record: str) -> tuple[tuple[int, ...], set[Edge]]:
    data = record.encode("ascii")
    if not data or not 63 <= data[0] <= 125:
        raise ValueError("only short graph6 records are supported")
    order = data[0] - 63
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(bits) < required:
        raise ValueError("truncated graph6 record")
    graph_edges: set[Edge] = set()
    position = 0
    for high in range(1, order):
        for low in range(high):
            if bits[position]:
                graph_edges.add((low, high))
            position += 1
    return tuple(range(order)), graph_edges


def graph6_encode(vertices, graph_edges: set[Edge]) -> str:
    order = len(vertices)
    if tuple(vertices) != tuple(range(order)) or order > 62:
        raise ValueError("short graph6 encoder requires vertices 0,...,n-1")
    bits = [
        int((low, high) in graph_edges)
        for high in range(1, order)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for offset in range(6):
            value = (value << 1) | bits[start + offset]
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def graph_complement(vertices, graph_edges: set[Edge]) -> set[Edge]:
    return {
        canonical_edge(left, right)
        for left, right in all_pairs(vertices)
        if canonical_edge(left, right) not in graph_edges
    }


def is_independent(state, graph_edges: set[Edge]) -> bool:
    return all(canonical_edge(u, v) not in graph_edges for u, v in all_pairs(state))


def dominates(state, vertices, graph_edges: set[Edge]) -> bool:
    occupied = set(state)
    for vertex in vertices:
        if vertex in occupied:
            continue
        if not any(canonical_edge(vertex, guard) in graph_edges for guard in state):
            return False
    return True


def successors(state: State, attack: int, graph_edges: set[Edge]) -> set[State]:
    if attack in state:
        raise AssertionError("the one-guard model has no occupied attack")
    return {
        frozenset((set(state) - {guard}) | {attack})
        for guard in state
        if canonical_edge(guard, attack) in graph_edges
    }


def family_is_eternal(
    vertices,
    graph_edges: set[Edge],
    family: set[State],
) -> tuple[bool, int, dict | None]:
    obligations = 0
    for state in sorted(family, key=lambda item: tuple(sorted(item))):
        if not dominates(state, vertices, graph_edges):
            return False, obligations, {
                "reason": "nondominating_state",
                "state": sorted(state),
            }
        for attack in sorted(set(vertices) - set(state)):
            obligations += 1
            legal = successors(state, attack, graph_edges)
            if not (legal & family):
                return False, obligations, {
                    "reason": "missing_one_guard_response",
                    "state": sorted(state),
                    "attack": attack,
                    "legal_successors": [
                        sorted(item)
                        for item in sorted(legal, key=lambda item: tuple(sorted(item)))
                    ],
                }
    return True, obligations, None


def greatest_family(
    vertices,
    graph_edges: set[Edge],
    guard_count: int,
    banned: set[State] | frozenset[State] = frozenset(),
) -> set[State]:
    current = {
        frozenset(choice)
        for choice in itertools.combinations(vertices, guard_count)
        if frozenset(choice) not in banned
        and dominates(choice, vertices, graph_edges)
    }
    while True:
        rejected = set()
        for state in current:
            for attack in set(vertices) - set(state):
                if not (successors(state, attack, graph_edges) & current):
                    rejected.add(state)
                    break
        if not rejected:
            return current
        current -= rejected


def domination_number(vertices, graph_edges: set[Edge]) -> int:
    for size in range(1, len(vertices) + 1):
        for state in itertools.combinations(vertices, size):
            if dominates(state, vertices, graph_edges):
                return size
    raise AssertionError("finite graph must have a dominating set")


def independence_number(vertices, graph_edges: set[Edge]) -> int:
    for size in range(len(vertices), -1, -1):
        if any(
            is_independent(state, graph_edges)
            for state in itertools.combinations(vertices, size)
        ):
            return size
    raise AssertionError("empty set is independent")


def colorable(vertices, edges: set[Edge], color_count: int) -> bool:
    neighborhoods = {
        vertex: {
            other
            for other in vertices
            if other != vertex
            and canonical_edge(vertex, other) in edges
        }
        for vertex in vertices
    }
    order = sorted(vertices, key=lambda vertex: (-len(neighborhoods[vertex]), vertex))
    assigned: dict[int, int] = {}

    def extend(position: int) -> bool:
        if position == len(order):
            return True
        vertex = order[position]
        forbidden = {
            assigned[neighbor]
            for neighbor in neighborhoods[vertex]
            if neighbor in assigned
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if extend(position + 1):
                return True
            del assigned[vertex]
        return False

    return extend(0)


def chromatic_number(vertices, edges: set[Edge]) -> int:
    for number in range(1, len(vertices) + 1):
        if colorable(vertices, edges, number):
            return number
    raise AssertionError("finite graph must be colorable")


def response_lists(
    reference: State,
    vertices,
    graph_edges: set[Edge],
    family: set[State],
) -> dict[int, set[int]]:
    result: dict[int, set[int]] = {}
    for attacked in set(vertices) - set(reference):
        result[attacked] = set()
        for guard in reference:
            successor = frozenset((set(reference) - {guard}) | {attacked})
            if (
                canonical_edge(guard, attacked) in graph_edges
                and successor in family
            ):
                result[attacked].add(guard)
    return result


def list_colorings(
    outside,
    complement_edges: set[Edge],
    lists: dict[int, set[int]],
) -> list[dict[int, int]]:
    order = sorted(outside, key=lambda vertex: (len(lists[vertex]), vertex))
    assigned: dict[int, int] = {}
    found: list[dict[int, int]] = []

    def extend(position: int):
        if position == len(order):
            found.append(dict(assigned))
            return
        vertex = order[position]
        for color in sorted(lists[vertex]):
            if any(
                canonical_edge(vertex, previous) in complement_edges
                and assigned[previous] == color
                for previous in assigned
            ):
                continue
            assigned[vertex] = color
            extend(position + 1)
            del assigned[vertex]

    extend(0)
    return found


def ridge_countermodel_audit() -> dict:
    vertices, graph_edges = graph6_decode("GFznc{")
    expected_graph_edges = {
        canonical_edge(*pair)
        for pair in (
            (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 3), (1, 4), (1, 5), (1, 6),
            (2, 3), (2, 4), (2, 5), (2, 6),
            (3, 6), (3, 7), (4, 5), (4, 7), (5, 7), (6, 7),
        )
    }
    if graph_edges != expected_graph_edges:
        raise AssertionError("graph6 record disagrees with the displayed graph")
    if graph6_encode(vertices, graph_edges) != "GFznc{":
        raise AssertionError("independent graph6 round trip failed")
    complement_edges = graph_complement(vertices, graph_edges)
    expected_complement_edges = {
        canonical_edge(*pair)
        for pair in (
            (0, 1), (0, 2), (1, 2), (1, 7), (2, 7),
            (3, 4), (3, 5), (4, 6), (5, 6),
        )
    }
    if complement_edges != expected_complement_edges:
        raise AssertionError("displayed complement edge set is wrong")

    family_strings = (
        "012 015 016 024 026 036 045 046 056 "
        "123 124 125 127 135 136 145 146 156 157 167 "
        "234 236 245 246 247 256 267 "
        "345 346 356 367 456 457 467 567"
    ).split()
    family = {
        frozenset(int(character) for character in item)
        for item in family_strings
    }
    accepted, obligations, defect = family_is_eternal(vertices, graph_edges, family)
    if not accepted or obligations != 175:
        raise AssertionError(f"family replay failed: {defect}")

    reference = frozenset({0, 1, 2})
    other = frozenset({1, 2, 7})
    expected_lists = {
        3: {0},
        4: {0, 1},
        5: {0, 2},
        6: {1, 2},
        7: {0},
    }
    expected_other_lists = {
        0: {7},
        3: {7},
        4: {1, 7},
        5: {2, 7},
        6: {1, 2},
    }
    lists = response_lists(reference, vertices, graph_edges, family)
    other_lists = response_lists(other, vertices, graph_edges, family)
    if lists != expected_lists or other_lists != expected_other_lists:
        raise AssertionError("ridge-end response list mismatch")

    independent_triples = {
        frozenset(state)
        for state in itertools.combinations(vertices, 3)
        if is_independent(state, graph_edges)
    }
    if independent_triples != {reference, other}:
        raise AssertionError("independent triple census mismatch")

    swap = {0: 7, 7: 0}
    image = lambda vertex: swap.get(vertex, vertex)
    for vertex, source_list in lists.items():
        transported = {image(color) for color in source_list}
        if transported != other_lists[image(vertex)]:
            raise AssertionError("ridge covariance table mismatch")

    direct_coloring_counts = {
        "S": len(
            list_colorings(
                sorted(set(vertices) - set(reference)),
                complement_edges,
                lists,
            )
        ),
        "T": len(
            list_colorings(
                sorted(set(vertices) - set(other)),
                complement_edges,
                other_lists,
            )
        ),
    }
    if direct_coloring_counts != {"S": 0, "T": 0}:
        raise AssertionError("one ridge-end list instance is colorable")
    if any(len(item) == 3 for item in lists.values()) or any(
        len(item) == 3 for item in other_lists.values()
    ):
        raise AssertionError("counterboundary contains a full response list")

    gamma = domination_number(vertices, graph_edges)
    alpha = independence_number(vertices, graph_edges)
    theta = chromatic_number(vertices, complement_edges)
    if (gamma, alpha, theta) != (2, 3, 3):
        raise AssertionError("counterboundary parameter mismatch")
    clique_partition = ({0, 7}, {1, 3, 6}, {2, 4, 5})
    if not all(
        canonical_edge(left, right) in graph_edges
        for part in clique_partition
        for left, right in all_pairs(part)
    ):
        raise AssertionError("displayed clique partition is invalid")

    nondominating = next(
        frozenset(state)
        for state in itertools.combinations(vertices, 3)
        if not dominates(state, vertices, graph_edges)
    )
    mutated_family = set(family) | {nondominating}
    mutation_accepted, _, mutation_defect = family_is_eternal(
        vertices, graph_edges, mutated_family
    )
    if mutation_accepted or mutation_defect["reason"] != "nondominating_state":
        raise AssertionError("checker failed a nondominating-state mutation")

    family_bytes = ("\n".join(family_strings) + "\n").encode()
    return {
        "accepted": True,
        "graph6": "GFznc{",
        "order": len(vertices),
        "size": len(graph_edges),
        "family_states": len(family),
        "unoccupied_attack_obligations": obligations,
        "occupied_vertices_deliberately_not_attacked_per_state": 3,
        "all_vertices_attack_count_if_model_were_wrong": len(family) * len(vertices),
        "parameters": {
            "gamma": gamma,
            "alpha": alpha,
            "gamma_infinity": 3,
            "theta": theta,
        },
        "independent_triples": [
            sorted(state)
            for state in sorted(independent_triples, key=lambda item: tuple(sorted(item)))
        ],
        "list_coloring_counts": direct_coloring_counts,
        "covariance_identities": len(lists),
        "family_manifest_sha256": hashlib.sha256(family_bytes).hexdigest(),
        "negative_mutation": mutation_defect,
    }


def pattern_completion_audit(
    *,
    order: int,
    required_h: set[Edge],
    required_g: set[Edge],
    banned: set[State],
) -> dict:
    vertices = tuple(range(order))
    universe = {canonical_edge(*pair) for pair in all_pairs(vertices)}
    if required_h & required_g:
        raise AssertionError("a pattern edge is both required and forbidden")
    optional = sorted(universe - required_h - required_g)
    reference = frozenset({0, 1, 2})
    surviving = []
    for mask in range(1 << len(optional)):
        graph_edges = set(required_g)
        graph_edges.update(
            pair
            for index, pair in enumerate(optional)
            if mask & (1 << index)
        )
        safe = greatest_family(vertices, graph_edges, 3, banned)
        if reference in safe:
            surviving.append(mask)
    if surviving:
        raise AssertionError(f"pattern survived graph completions {surviving[:5]}")
    return {
        "graph_completions": 1 << len(optional),
        "optional_edges": len(optional),
        "reference_survivors_under_relaxed_positive_membership": 0,
        "accepted": True,
    }


def canonical_pattern_audits() -> dict:
    anchor_h = {
        canonical_edge(0, 1),
        canonical_edge(0, 2),
        canonical_edge(1, 2),
    }
    lollipop_h = anchor_h | {
        canonical_edge(*pair)
        for pair in ((3, 4), (4, 5), (4, 6), (5, 6))
    }
    lollipop_g = {
        canonical_edge(*pair)
        for pair in ((0, 3), (1, 5), (2, 5), (1, 6), (2, 6))
    }
    # Exact absences for p={a}, r=s={b,c}.  No condition on L(q).
    lollipop_banned = {
        frozenset(state)
        for state in ((0, 1, 3), (0, 2, 3), (1, 2, 5), (1, 2, 6))
    }

    bicycle_h = anchor_h | {
        canonical_edge(*pair)
        for pair in (
            (3, 4), (3, 5), (3, 6), (3, 7),
            (4, 7), (5, 6), (6, 7),
        )
    }
    bicycle_g = {
        canonical_edge(anchor, outside)
        for outside in (3, 4, 5)
        for anchor in (0, 1)
    } | {
        canonical_edge(anchor, outside)
        for outside in (6, 7)
        for anchor in (0, 2)
    }
    bicycle_banned = {
        frozenset((0, 1, outside))
        for outside in (3, 4, 5)
    } | {
        frozenset((0, 2, outside))
        for outside in (6, 7)
    }
    return {
        "one_unit_lollipop": pattern_completion_audit(
            order=7,
            required_h=lollipop_h,
            required_g=lollipop_g,
            banned=lollipop_banned,
        ),
        "unit_free_two_variable_bicycle": pattern_completion_audit(
            order=8,
            required_h=bicycle_h,
            required_g=bicycle_g,
            banned=bicycle_banned,
        ),
    }


def literal_complement(literal: int) -> int:
    return literal ^ 1


def formula_satisfiable(variable_count: int, units, binary) -> bool:
    for values in itertools.product((0, 1), repeat=variable_count):
        if not all(values[literal // 2] == literal % 2 for literal in units):
            continue
        if all(
            values[left // 2] == left % 2
            or values[right // 2] == right % 2
            for left, right in binary
        ):
            return True
    return False


def path_clause_sets(source: int, target: int, binary) -> set[frozenset[int]]:
    adjacency: dict[int, list[tuple[int, int]]] = {}
    for clause_id, (left, right) in enumerate(binary):
        adjacency.setdefault(literal_complement(left), []).append((right, clause_id))
        adjacency.setdefault(literal_complement(right), []).append((left, clause_id))
    answer: set[frozenset[int]] = set()

    def walk(current: int, seen: frozenset[int], used: frozenset[int]):
        if current == target:
            answer.add(used)
            return
        for following, clause_id in adjacency.get(current, []):
            if following not in seen:
                walk(following, seen | {following}, used | {clause_id})

    walk(source, frozenset({source}), frozenset())
    return answer


def trichotomy_class(variable_count: int, units, binary) -> str:
    all_ids = frozenset(range(len(binary)))
    if len(units) == 2:
        first, second = units
        for source, target in (
            (first, literal_complement(second)),
            (second, literal_complement(first)),
        ):
            if all_ids in path_clause_sets(source, target, binary):
                return "two_unit_chain"
    elif len(units) == 1:
        source = units[0]
        if all_ids in path_clause_sets(source, literal_complement(source), binary):
            return "one_unit_lollipop"
    elif not units:
        for variable in range(variable_count):
            for value in (0, 1):
                source = 2 * variable + value
                opposite = literal_complement(source)
                for forward in path_clause_sets(source, opposite, binary):
                    for backward in path_clause_sets(opposite, source, binary):
                        if forward | backward == all_ids:
                            return "unit_free_bicycle"
    raise AssertionError((variable_count, units, binary))


def systematic_trichotomy(max_variables: int = 3) -> dict:
    result = {}
    for variable_count in range(1, max_variables + 1):
        unit_universe = list(range(2 * variable_count))
        binary_universe = [
            (2 * left_variable + left_value, 2 * right_variable + right_value)
            for left_variable in range(variable_count)
            for right_variable in range(left_variable + 1, variable_count)
            for left_value in (0, 1)
            for right_value in (0, 1)
        ]
        constraints = [("u", item) for item in unit_universe] + [
            ("b", item) for item in binary_universe
        ]
        counts = {
            "two_unit_chain": 0,
            "one_unit_lollipop": 0,
            "unit_free_bicycle": 0,
        }
        minimal_count = 0
        for mask in range(1, 1 << len(constraints)):
            chosen = [
                constraints[index]
                for index in range(len(constraints))
                if mask & (1 << index)
            ]
            units = [item for kind, item in chosen if kind == "u"]
            binary = [item for kind, item in chosen if kind == "b"]
            if formula_satisfiable(variable_count, units, binary):
                continue
            is_minimal = True
            for removed in range(len(chosen)):
                reduced = chosen[:removed] + chosen[removed + 1 :]
                reduced_units = [item for kind, item in reduced if kind == "u"]
                reduced_binary = [item for kind, item in reduced if kind == "b"]
                if not formula_satisfiable(
                    variable_count, reduced_units, reduced_binary
                ):
                    is_minimal = False
                    break
            if not is_minimal:
                continue
            kind = trichotomy_class(variable_count, units, binary)
            counts[kind] += 1
            minimal_count += 1
        result[str(variable_count)] = {
            "inclusion_minimal_unsatisfiable": minimal_count,
            "trichotomy_counts": counts,
        }
    return result


def random_trichotomy_falsifier(samples: int = 5000) -> dict:
    generator = random.Random(20260726)
    tested = 0
    unsatisfiable_draws = 0
    for _ in range(samples):
        variable_count = generator.randint(4, 8)
        universe = [("u", literal) for literal in range(2 * variable_count)]
        universe.extend(
            ("b", (2 * left + left_value, 2 * right + right_value))
            for left in range(variable_count)
            for right in range(left + 1, variable_count)
            for left_value in (0, 1)
            for right_value in (0, 1)
        )
        chosen = generator.sample(
            universe,
            generator.randint(variable_count + 1, min(len(universe), 4 * variable_count)),
        )

        def split(items):
            return (
                [item for kind, item in items if kind == "u"],
                [item for kind, item in items if kind == "b"],
            )

        units, binary = split(chosen)
        if formula_satisfiable(variable_count, units, binary):
            continue
        unsatisfiable_draws += 1
        generator.shuffle(chosen)
        changed = True
        while changed:
            changed = False
            for index in range(len(chosen)):
                candidate = chosen[:index] + chosen[index + 1 :]
                candidate_units, candidate_binary = split(candidate)
                if not formula_satisfiable(
                    variable_count, candidate_units, candidate_binary
                ):
                    chosen = candidate
                    changed = True
                    break
        units, binary = split(chosen)
        trichotomy_class(variable_count, units, binary)
        tested += 1
    return {
        "seed": 20260726,
        "draws": samples,
        "unsatisfiable_draws": unsatisfiable_draws,
        "minimal_formulas_classified": tested,
        "failures": 0,
    }


def parity_truth_table_audit() -> dict:
    internal_cases = 0
    terminal_cases = 0
    for parity_x, parity_y, index_w, index_w_prime in itertools.product(
        (0, 1), repeat=4
    ):
        event_x = parity_x ^ index_w
        event_y = parity_y ^ index_w_prime
        if event_y != 1 - event_x:
            continue
        internal_cases += 1
        expected = 1 ^ index_w ^ index_w_prime
        if (parity_x ^ parity_y) != expected:
            raise AssertionError("internal connector parity sign failure")
        if ((parity_x ^ parity_y) == 1) != (index_w == index_w_prime):
            raise AssertionError("same-color oddness failure")
    for parity_s, parity_x, index_d, index_w in itertools.product(
        (0, 1), repeat=4
    ):
        forced_value = parity_s ^ index_d
        port_value = parity_x ^ index_w
        if forced_value != port_value:
            continue
        terminal_cases += 1
        if (parity_s ^ parity_x) != (index_d ^ index_w):
            raise AssertionError("terminal connector parity sign failure")
    return {
        "accepted": True,
        "internal_complement-event_cases": internal_cases,
        "terminal_agreement_cases": terminal_cases,
    }


def order8_scan() -> dict:
    records = subprocess.check_output([str(GENG), "-cq", "8"], text=True).splitlines()
    counters = {
        "2": {
            "eligible_graphs": 0,
            "reference_states": 0,
            "restrictions": 0,
            "surviving_exact_two_list_families": 0,
        },
        "3": {
            "eligible_graphs": 0,
            "reference_states": 0,
            "restrictions": 0,
            "surviving_exact_two_list_families": 0,
        },
    }
    uncolorable = []
    for record in records:
        vertices, graph_edges = graph6_decode(record)
        if independence_number(vertices, graph_edges) != 3:
            continue
        gamma = domination_number(vertices, graph_edges)
        if gamma not in (2, 3):
            continue
        unrestricted = greatest_family(vertices, graph_edges, 3)
        if not unrestricted:
            continue
        bucket = counters[str(gamma)]
        bucket["eligible_graphs"] += 1
        for state_tuple in itertools.combinations(vertices, 3):
            reference = frozenset(state_tuple)
            if not is_independent(reference, graph_edges):
                continue
            candidates: dict[int, list[tuple[int, State]]] = {}
            for attacked in set(vertices) - set(reference):
                candidates[attacked] = []
                for guard in reference:
                    successor = frozenset(
                        (set(reference) - {guard}) | {attacked}
                    )
                    if (
                        canonical_edge(guard, attacked) in graph_edges
                        and successor in unrestricted
                    ):
                        candidates[attacked].append((guard, successor))
            if any(len(items) < 2 for items in candidates.values()):
                continue
            bucket["reference_states"] += 1
            per_vertex_bans = []
            for attacked in sorted(candidates):
                choices = []
                for selected in itertools.combinations(candidates[attacked], 2):
                    selected_guards = {item[0] for item in selected}
                    choices.append(
                        frozenset(
                            successor
                            for guard, successor in candidates[attacked]
                            if guard not in selected_guards
                        )
                    )
                per_vertex_bans.append(choices)
            for selected_bans in itertools.product(*per_vertex_bans):
                bucket["restrictions"] += 1
                banned = frozenset().union(*selected_bans)
                restricted = greatest_family(vertices, graph_edges, 3, banned)
                if reference not in restricted:
                    continue
                lists = response_lists(reference, vertices, graph_edges, restricted)
                if any(len(item) != 2 for item in lists.values()):
                    continue
                bucket["surviving_exact_two_list_families"] += 1
                complement_edges = graph_complement(vertices, graph_edges)
                if not list_colorings(
                    sorted(set(vertices) - set(reference)),
                    complement_edges,
                    lists,
                ):
                    uncolorable.append(
                        {"graph6": record, "reference": sorted(reference)}
                    )
    expected = {
        "connected_graphs": 11117,
        "by_gamma": {
            "2": {
                "eligible_graphs": 4779,
                "reference_states": 1373,
                "restrictions": 18985,
                "surviving_exact_two_list_families": 14372,
            },
            "3": {
                "eligible_graphs": 140,
                "reference_states": 0,
                "restrictions": 0,
                "surviving_exact_two_list_families": 0,
            },
        },
        "uncolorable_count": 0,
    }
    actual = {
        "connected_graphs": len(records),
        "by_gamma": counters,
        "uncolorable_count": len(uncolorable),
    }
    if actual != expected:
        raise AssertionError({"expected": expected, "actual": actual})
    return {
        **actual,
        "uncolorable_records": uncolorable,
        "geng_sha256": hashlib.sha256(GENG.read_bytes()).hexdigest(),
        "scope": (
            "Order exactly eight; connected unlabeled graphs; alpha="
            "gamma_infinity=3; gamma in {2,3}; independent references; "
            "exact two-list restrictions only. This is a clean-room replay "
            "of an OBSERVED scan, not a coverage certificate or frontier theorem."
        ),
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "independent_result.json")
    parser.add_argument("--skip-order8", action="store_true")
    args = parser.parse_args()
    started = time.time()
    result = {
        "schema": "k3-twosat-bicycle-hostile-cleanroom-v1",
        "reviewed_target_hashes": {
            name: file_sha256(TARGET / name)
            for name in ("NOTE.md", "evidence.py", "evidence.json", "RESEARCH_LOG.md")
        },
        "trichotomy_systematic": systematic_trichotomy(),
        "trichotomy_random_falsifier": random_trichotomy_falsifier(),
        "parity_translation": parity_truth_table_audit(),
        "canonical_pattern_completions": canonical_pattern_audits(),
        "ridge_countermodel": ridge_countermodel_audit(),
        "order8_exact_two_list_scan": (
            {"status": "SKIPPED"} if args.skip_order8 else order8_scan()
        ),
    }
    result["elapsed_seconds"] = time.time() - started
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "sha256": file_sha256(args.output),
                "elapsed_seconds": result["elapsed_seconds"],
                "ridge": result["ridge_countermodel"]["accepted"],
                "pattern_completions": result["canonical_pattern_completions"],
                "order8_uncolorable": result["order8_exact_two_list_scan"].get(
                    "uncolorable_count"
                ),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
