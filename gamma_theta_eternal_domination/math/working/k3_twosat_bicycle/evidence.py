#!/usr/bin/env python3
"""Exact bounded evidence for the k=3 2-SAT bicycle analysis.

The script is deliberately independent of the campaign evaluators.  It uses
ordinary Python sets and exhaustive subsets.  Its largest optional scan is
the 11,117 connected unlabeled graphs of order eight, followed by 18,985
two-list family restrictions; this takes seconds, not hours, on the campaign
machine.

The mathematical theorems in NOTE.md have written proofs.  The computations
here are falsifiers, literal certificate replays, and bounded observations.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import time
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUTPUT = Path(__file__).with_name("evidence.json")
GENG = ROOT / "gamma_theta_eternal_domination" / "tools" / "nauty2_9_3" / "geng"


State = frozenset[int]
Edge = tuple[int, int]
Literal = tuple[int, int]  # (variable, satisfying Boolean value)


def pairs(vertices):
    return itertools.combinations(vertices, 2)


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def complement_edges(vertices, graph_edges: set[Edge]) -> set[Edge]:
    return {edge(u, v) for u, v in pairs(vertices) if edge(u, v) not in graph_edges}


def graph_edges_from_complement(vertices, h_edges: set[Edge]) -> set[Edge]:
    return {edge(u, v) for u, v in pairs(vertices) if edge(u, v) not in h_edges}


def dominates(state, vertices, graph_edges: set[Edge]) -> bool:
    covered = set(state)
    for u in state:
        covered.update(v for v in vertices if v != u and edge(u, v) in graph_edges)
    return covered == set(vertices)


def independent(state, graph_edges: set[Edge]) -> bool:
    return all(edge(u, v) not in graph_edges for u, v in pairs(state))


def domination_number(vertices, graph_edges: set[Edge]) -> int:
    for size in range(1, len(vertices) + 1):
        if any(dominates(set_, vertices, graph_edges) for set_ in itertools.combinations(vertices, size)):
            return size
    raise AssertionError("finite graph has no dominating set")


def independence_number(vertices, graph_edges: set[Edge]) -> int:
    for size in range(len(vertices), 0, -1):
        if any(independent(set_, graph_edges) for set_ in itertools.combinations(vertices, size)):
            return size
    return 0


def chromatic_number(vertices, h_edges: set[Edge]) -> int:
    neighbors = {
        u: {v for v in vertices if v != u and edge(u, v) in h_edges}
        for u in vertices
    }
    order = sorted(vertices, key=lambda u: (-len(neighbors[u]), u))
    for color_count in range(1, len(vertices) + 1):
        assignment: dict[int, int] = {}

        def visit(position: int) -> bool:
            if position == len(order):
                return True
            u = order[position]
            forbidden = {assignment[v] for v in neighbors[u] if v in assignment}
            for color in range(color_count):
                if color not in forbidden:
                    assignment[u] = color
                    if visit(position + 1):
                        return True
                    del assignment[u]
            return False

        if visit(0):
            return color_count
    raise AssertionError("unreachable")


def graph6_encode(vertices, graph_edges: set[Edge]) -> str:
    n = len(vertices)
    assert tuple(vertices) == tuple(range(n))
    assert n <= 62
    bits = []
    for high in range(1, n):
        for low in range(high):
            bits.append(int((low, high) in graph_edges))
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = sum(bits[start + offset] << (5 - offset) for offset in range(6))
        payload.append(chr(63 + value))
    return chr(63 + n) + "".join(payload)


def graph6_decode(record: str) -> tuple[tuple[int, ...], set[Edge]]:
    raw = record.encode("ascii")
    if not raw or not 63 <= raw[0] <= 125:
        raise ValueError("only short graph6 records are supported")
    n = raw[0] - 63
    bits = []
    for byte in raw[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    graph_edges = set()
    position = 0
    for high in range(1, n):
        for low in range(high):
            if bits[position]:
                graph_edges.add((low, high))
            position += 1
    return tuple(range(n)), graph_edges


def family_successors(
    state: State,
    attack: int,
    graph_edges: set[Edge],
) -> list[State]:
    return sorted(
        (
            frozenset((set(state) - {guard}) | {attack})
            for guard in state
            if edge(guard, attack) in graph_edges
        ),
        key=lambda item: tuple(sorted(item)),
    )


def greatest_safe_family(
    vertices,
    graph_edges: set[Edge],
    guard_count: int,
    banned: set[State] | frozenset[State] = frozenset(),
    *,
    retain_trace: bool = False,
):
    states = {
        frozenset(state)
        for state in itertools.combinations(vertices, guard_count)
        if frozenset(state) not in banned
        and dominates(state, vertices, graph_edges)
    }
    deletion_rounds = []
    rank: dict[State, int] = {}
    round_number = 1
    while True:
        removed: dict[State, dict] = {}
        for state in sorted(states, key=lambda item: tuple(sorted(item))):
            for attack in sorted(set(vertices) - set(state)):
                successors = family_successors(state, attack, graph_edges)
                if not any(successor in states for successor in successors):
                    removed[state] = {
                        "attack": attack,
                        "successors": successors,
                    }
                    break
        if not removed:
            break
        for state in removed:
            rank[state] = round_number
        states -= set(removed)
        if retain_trace:
            deletion_rounds.append(removed)
        round_number += 1
    if retain_trace:
        return states, deletion_rounds, rank
    return states


def verify_family(vertices, graph_edges: set[Edge], family: set[State]) -> dict:
    obligations = 0
    for state in sorted(family, key=lambda item: tuple(sorted(item))):
        assert dominates(state, vertices, graph_edges)
        for attack in sorted(set(vertices) - set(state)):
            obligations += 1
            assert any(
                successor in family
                for successor in family_successors(state, attack, graph_edges)
            )
    return {
        "states": len(family),
        "unoccupied_attack_obligations": obligations,
        "accepted": True,
    }


def response_lists(
    reference: State,
    vertices,
    graph_edges: set[Edge],
    family: set[State],
) -> dict[int, set[int]]:
    lists = {}
    for x in set(vertices) - set(reference):
        lists[x] = {
            u
            for u in reference
            if edge(u, x) in graph_edges
            and frozenset((set(reference) - {u}) | {x}) in family
        }
    return lists


def direct_list_colorings(
    outside_vertices,
    h_edges: set[Edge],
    lists: dict[int, set[int]],
) -> list[dict[int, int]]:
    order = sorted(outside_vertices, key=lambda x: (len(lists[x]), x))
    colorings = []
    assignment: dict[int, int] = {}

    def visit(position: int):
        if position == len(order):
            colorings.append(dict(assignment))
            return
        x = order[position]
        forbidden = {
            assignment[y]
            for y in assignment
            if edge(x, y) in h_edges
        }
        for color in sorted(lists[x]):
            if color not in forbidden:
                assignment[x] = color
                visit(position + 1)
                del assignment[x]

    visit(0)
    return colorings


def bipartition(vertices, h_edges: set[Edge]):
    adjacency = {u: set() for u in vertices}
    for u, v in h_edges:
        if u in adjacency and v in adjacency:
            adjacency[u].add(v)
            adjacency[v].add(u)
    parity: dict[int, int] = {}
    components = []
    for root in sorted(vertices):
        if root in parity:
            continue
        parity[root] = 0
        component = []
        queue = deque([root])
        while queue:
            u = queue.popleft()
            component.append(u)
            for v in sorted(adjacency[u]):
                if v not in parity:
                    parity[v] = parity[u] ^ 1
                    queue.append(v)
                else:
                    assert parity[v] != parity[u]
        components.append(sorted(component))
    return parity, components


def projection_formula(
    reference: State,
    vertices,
    h_edges: set[Edge],
    lists: dict[int, set[int]],
) -> dict:
    """Construct the exact simplified no-full-list projection formula."""

    colors = sorted(reference)
    outside = sorted(set(vertices) - set(reference))
    assert all(0 < len(lists[x]) < 3 for x in outside)
    component_data = {}
    variables = []
    projections = {}
    for frozen in colors:
        remaining = sorted(set(reference) - {frozen})
        projected = set(remaining) | {x for x in outside if frozen not in lists[x]}
        parity, components = bipartition(projected, h_edges)
        anchor_component = next(
            index for index, component in enumerate(components) if remaining[0] in component
        )
        assert remaining[1] in components[anchor_component]
        if parity[remaining[0]]:
            for x in components[anchor_component]:
                parity[x] ^= 1
        for index, component in enumerate(components):
            variable = None
            if index != anchor_component:
                variable = len(variables)
                variables.append(
                    {
                        "id": variable,
                        "frozen": frozen,
                        "component": component,
                    }
                )
            for x in component:
                component_data[(frozen, x)] = {
                    "variable": variable,
                    "parity": parity[x],
                    "remaining": remaining,
                }
        projections[str(frozen)] = {
            "vertices": sorted(projected),
            "components": components,
            "anchor_component": anchor_component,
            "parity": {str(x): parity[x] for x in sorted(projected)},
        }

    constraints = []
    fixed_contradictions = []
    for x in outside:
        if len(lists[x]) != 1:
            continue
        demanded = next(iter(lists[x]))
        for frozen in sorted(set(reference) - {demanded}):
            data = component_data[(frozen, x)]
            required = data["parity"] ^ data["remaining"].index(demanded)
            if data["variable"] is None:
                if required:
                    fixed_contradictions.append(
                        {
                            "kind": "fixed_unit_conflict",
                            "marker": x,
                            "frozen": frozen,
                            "demanded": demanded,
                        }
                    )
            else:
                constraints.append(
                    {
                        "kind": "unit",
                        "var": data["variable"],
                        "value": required,
                        "origin": {
                            "marker": x,
                            "frozen": frozen,
                            "demanded": demanded,
                        },
                    }
                )

    for x, y in itertools.combinations(outside, 2):
        if edge(x, y) not in h_edges:
            continue
        if len(lists[x]) != 2 or len(lists[y]) != 2:
            continue
        omitted_x = next(iter(set(reference) - lists[x]))
        omitted_y = next(iter(set(reference) - lists[y]))
        if omitted_x == omitted_y:
            continue
        shared = next(iter(lists[x] & lists[y]))
        endpoint_data = []
        for vertex, omitted in ((x, omitted_x), (y, omitted_y)):
            data = component_data[(omitted, vertex)]
            event_value = data["parity"] ^ data["remaining"].index(shared)
            endpoint_data.append((data["variable"], event_value))
        (var_x, event_x), (var_y, event_y) = endpoint_data
        fixed_x = var_x is None
        fixed_y = var_y is None
        event_x_true = fixed_x and event_x == 0
        event_y_true = fixed_y and event_y == 0
        if fixed_x and fixed_y:
            if event_x_true and event_y_true:
                fixed_contradictions.append(
                    {
                        "kind": "fixed_clause_conflict",
                        "edge": [x, y],
                        "shared": shared,
                    }
                )
        elif fixed_x:
            if event_x_true:
                constraints.append(
                    {
                        "kind": "unit",
                        "var": var_y,
                        "value": 1 - event_y,
                        "origin": {"edge": [x, y], "shared": shared},
                    }
                )
        elif fixed_y:
            if event_y_true:
                constraints.append(
                    {
                        "kind": "unit",
                        "var": var_x,
                        "value": 1 - event_x,
                        "origin": {"edge": [x, y], "shared": shared},
                    }
                )
        else:
            constraints.append(
                {
                    "kind": "binary",
                    "literals": [
                        [var_x, 1 - event_x],
                        [var_y, 1 - event_y],
                    ],
                    "origin": {"edge": [x, y], "shared": shared},
                }
            )

    # Logical duplicates are irrelevant to inclusion-minimal cores.
    deduplicated = {}
    for constraint in constraints:
        if constraint["kind"] == "unit":
            key = ("unit", constraint["var"], constraint["value"])
        else:
            key = (
                "binary",
                *sorted(tuple(literal) for literal in constraint["literals"]),
            )
        deduplicated.setdefault(key, constraint)
    constraints = list(deduplicated.values())
    return {
        "variables": variables,
        "projections": projections,
        "constraints": constraints,
        "fixed_contradictions": fixed_contradictions,
    }


def constraint_satisfied(constraint: dict, assignment: tuple[int, ...]) -> bool:
    if constraint["kind"] == "unit":
        return assignment[constraint["var"]] == constraint["value"]
    return any(assignment[var] == value for var, value in constraint["literals"])


def formula_satisfiable(variable_count: int, constraints: list[dict]) -> bool:
    return any(
        all(constraint_satisfied(constraint, assignment) for constraint in constraints)
        for assignment in itertools.product((0, 1), repeat=variable_count)
    )


def inclusion_minimal_cores(variable_count: int, constraints: list[dict]) -> list[list[dict]]:
    cores = []
    for size in range(1, len(constraints) + 1):
        for indices in itertools.combinations(range(len(constraints)), size):
            candidate = [constraints[index] for index in indices]
            if formula_satisfiable(variable_count, candidate):
                continue
            if all(
                formula_satisfiable(
                    variable_count,
                    candidate[:position] + candidate[position + 1 :],
                )
                for position in range(size)
            ):
                cores.append(candidate)
        if cores:
            break
    return cores


def logical_constraint(constraint: dict):
    if constraint["kind"] == "unit":
        return ["unit", constraint["var"], constraint["value"]]
    return ["binary", *sorted(constraint["literals"])]


def clique_hall_ok(
    outside,
    h_edges: set[Edge],
    lists: dict[int, set[int]],
) -> bool:
    for size in range(1, len(outside) + 1):
        for clique in itertools.combinations(outside, size):
            if all(edge(u, v) in h_edges for u, v in pairs(clique)):
                if len(set().union(*(lists[x] for x in clique))) < size:
                    return False
    return True


def vertex_edge_minimal_list_obstruction(
    outside,
    h_edges: set[Edge],
    lists: dict[int, set[int]],
) -> dict:
    assert not direct_list_colorings(outside, h_edges, lists)
    vertex_minimal = True
    for removed in outside:
        remaining = [x for x in outside if x != removed]
        if not direct_list_colorings(remaining, h_edges, lists):
            vertex_minimal = False
    relevant_edges = {uv for uv in h_edges if uv[0] in outside and uv[1] in outside}
    edge_minimal = all(
        direct_list_colorings(outside, h_edges - {removed}, lists)
        for removed in relevant_edges
    )
    return {"vertex_minimal": vertex_minimal, "edge_minimal": edge_minimal}


def make_direct_swap_bans(reference: State, lists: dict[int, set[int]]) -> set[State]:
    return {
        frozenset((set(reference) - {u}) | {x})
        for x, response in lists.items()
        for u in reference
        if u not in response
    }


def policy_audit(
    vertices,
    graph_edges: set[Edge],
    banned: set[State],
    policy: dict[State, tuple[int, int]],
) -> dict:
    """Check a decreasing-rank adversarial attack policy."""

    rows = []
    for state, (rank, attack) in sorted(
        policy.items(), key=lambda item: (-item[1][0], tuple(sorted(item[0])))
    ):
        assert attack not in state
        successors = family_successors(state, attack, graph_edges)
        successor_rows = []
        for successor in successors:
            if successor in banned:
                status = "forbidden_direct_swap"
            elif not dominates(successor, vertices, graph_edges):
                status = "fails_named_domination"
            elif successor in policy and policy[successor][0] < rank:
                status = "lower_policy_rank"
            else:
                raise AssertionError(
                    f"unclassified successor {sorted(successor)} "
                    f"from {sorted(state)} at {attack}"
                )
            successor_rows.append(
                {
                    "state": sorted(successor),
                    "status": status,
                    "rank": policy[successor][0] if successor in policy else 0,
                }
            )
        assert successors
        rows.append(
            {
                "state": sorted(state),
                "rank": rank,
                "attack": attack,
                "successors": successor_rows,
            }
        )
    return {"accepted": True, "states": len(policy), "rows": rows}


def pattern_report(name: str, outside_lists, outside_h_edges, policy_spec) -> dict:
    reference = frozenset({0, 1, 2})
    outside = sorted(outside_lists)
    vertices = tuple(range(max(outside) + 1))
    h_edges = {(0, 1), (0, 2), (1, 2)} | set(outside_h_edges)
    graph_edges = graph_edges_from_complement(vertices, h_edges)
    formula = projection_formula(reference, vertices, h_edges, outside_lists)
    cores = inclusion_minimal_cores(len(formula["variables"]), formula["constraints"])
    assert cores
    banned = make_direct_swap_bans(reference, outside_lists)
    family, rounds, ranks = greatest_safe_family(
        vertices,
        graph_edges,
        3,
        banned,
        retain_trace=True,
    )
    assert not family
    policy = {
        frozenset(state): (rank, attack)
        for state, rank, attack in policy_spec
    }
    policy_result = policy_audit(vertices, graph_edges, banned, policy)
    assert frozenset({0, 1, 2}) in policy
    assert ranks[frozenset({0, 1, 2})] == policy[frozenset({0, 1, 2})][0]
    return {
        "name": name,
        "reference": sorted(reference),
        "outside_lists": {
            str(x): sorted(outside_lists[x]) for x in sorted(outside_lists)
        },
        "required_complement_edges": [list(item) for item in sorted(outside_h_edges)],
        "maximal_named_host": {
            "order": len(vertices),
            "graph6": graph6_encode(vertices, graph_edges),
            "graph_edges": [list(item) for item in sorted(graph_edges)],
            "complement_edges": [list(item) for item in sorted(h_edges)],
        },
        "projection_variable_count": len(formula["variables"]),
        "formula_constraints": [
            logical_constraint(item) for item in formula["constraints"]
        ],
        "minimum_core_size": len(cores[0]),
        "minimum_cores": [
            [logical_constraint(item) for item in core] for core in cores
        ],
        "minimum_core_unit_counts": [
            sum(item["kind"] == "unit" for item in core) for core in cores
        ],
        "direct_list_coloring_count": len(
            direct_list_colorings(outside, h_edges, outside_lists)
        ),
        "clique_hall": clique_hall_ok(outside, h_edges, outside_lists),
        "minimality": vertex_edge_minimal_list_obstruction(
            outside, h_edges, outside_lists
        ),
        "greatest_safe_named_family_size": len(family),
        "deletion_round_sizes": [len(round_) for round_ in rounds],
        "reference_deletion_rank": ranks[reference],
        "attack_policy": policy_result,
    }


def enumerate_simple_clause_paths(
    source: Literal,
    target: Literal,
    binary_constraints: list[tuple[Literal, Literal, int]],
) -> list[frozenset[int]]:
    adjacency: dict[Literal, list[tuple[Literal, int]]] = {}
    for left, right, clause_id in binary_constraints:
        adjacency.setdefault((left[0], 1 - left[1]), []).append((right, clause_id))
        adjacency.setdefault((right[0], 1 - right[1]), []).append((left, clause_id))
    results = set()

    def visit(current: Literal, seen: set[Literal], used: frozenset[int]):
        if current == target:
            results.add(used)
            return
        for next_literal, clause_id in adjacency.get(current, []):
            if next_literal not in seen:
                visit(
                    next_literal,
                    seen | {next_literal},
                    used | {clause_id},
                )

    visit(source, {source}, frozenset())
    return sorted(results, key=lambda item: (len(item), sorted(item)))


def classify_minimal_formula(
    variable_count: int,
    constraints: list[tuple],
) -> str:
    units = [(item[1], item[2]) for item in constraints if item[0] == "unit"]
    binary = [
        (item[1], item[2], index)
        for index, item in enumerate(constraints)
        if item[0] == "binary"
    ]
    binary_ids = frozenset(item[2] for item in binary)
    paths = {}

    def path_sets(source: Literal, target: Literal):
        key = (source, target)
        if key not in paths:
            paths[key] = enumerate_simple_clause_paths(source, target, binary)
        return paths[key]

    if len(units) == 2:
        p, q = units
        if any(
            used == binary_ids
            for source, target in ((p, (q[0], 1 - q[1])), (q, (p[0], 1 - p[1])))
            for used in path_sets(source, target)
        ):
            return "two_unit_chain"
    elif len(units) == 1:
        p = units[0]
        if any(
            used == binary_ids
            for used in path_sets(p, (p[0], 1 - p[1]))
        ):
            return "one_unit_lollipop"
    elif len(units) == 0:
        for variable in range(variable_count):
            for value in (0, 1):
                literal = (variable, value)
                opposite = (variable, 1 - value)
                for forward in path_sets(literal, opposite):
                    for backward in path_sets(opposite, literal):
                        if forward | backward == binary_ids:
                            return "unit_free_bicycle"
    raise AssertionError(f"minimal formula escaped trichotomy: {constraints}")


def generic_formula_trichotomy(max_variables: int = 3) -> dict:
    report = {}
    for variable_count in range(1, max_variables + 1):
        universe = [
            ("unit", variable, value)
            for variable in range(variable_count)
            for value in (0, 1)
        ]
        universe += [
            ("binary", (left, left_value), (right, right_value))
            for left in range(variable_count)
            for right in range(left + 1, variable_count)
            for left_value in (0, 1)
            for right_value in (0, 1)
        ]

        satisfying_masks = []
        assignment_count = 1 << variable_count
        for constraint in universe:
            mask = 0
            for assignment_mask in range(assignment_count):
                assignment = tuple(
                    (assignment_mask >> variable) & 1
                    for variable in range(variable_count)
                )
                if constraint[0] == "unit":
                    accepted = assignment[constraint[1]] == constraint[2]
                else:
                    accepted = (
                        assignment[constraint[1][0]] == constraint[1][1]
                        or assignment[constraint[2][0]] == constraint[2][1]
                    )
                if accepted:
                    mask |= 1 << assignment_mask
            satisfying_masks.append(mask)

        minimal_counts = {
            "two_unit_chain": 0,
            "one_unit_lollipop": 0,
            "unit_free_bicycle": 0,
        }
        total_minimal = 0
        for subset_mask in range(1, 1 << len(universe)):
            active = [
                index
                for index in range(len(universe))
                if subset_mask & (1 << index)
            ]
            common = (1 << assignment_count) - 1
            for index in active:
                common &= satisfying_masks[index]
            if common:
                continue
            minimal = True
            for removed in active:
                reduced = (1 << assignment_count) - 1
                for index in active:
                    if index != removed:
                        reduced &= satisfying_masks[index]
                if not reduced:
                    minimal = False
                    break
            if not minimal:
                continue
            formula = [universe[index] for index in active]
            kind = classify_minimal_formula(variable_count, formula)
            minimal_counts[kind] += 1
            total_minimal += 1
        report[str(variable_count)] = {
            "constraint_universe_size": len(universe),
            "formulas_examined": (1 << len(universe)) - 1,
            "inclusion_minimal_unsatisfiable": total_minimal,
            "trichotomy_counts": minimal_counts,
        }
    return report


def ridge_countermodel() -> dict:
    vertices = tuple(range(8))
    h_edges = {
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 7),
        (2, 7),
        (3, 4),
        (3, 5),
        (4, 6),
        (5, 6),
    }
    graph_edges = graph_edges_from_complement(vertices, h_edges)
    graph6 = graph6_encode(vertices, graph_edges)
    assert graph6 == "GFznc{"
    reference = frozenset({0, 1, 2})
    expected_lists = {
        3: {0},
        4: {0, 1},
        5: {0, 2},
        6: {1, 2},
        7: {0},
    }
    banned = make_direct_swap_bans(reference, expected_lists)
    family = greatest_safe_family(vertices, graph_edges, 3, banned)
    expected_family_strings = [
        "012",
        "015",
        "016",
        "024",
        "026",
        "036",
        "045",
        "046",
        "056",
        "123",
        "124",
        "125",
        "127",
        "135",
        "136",
        "145",
        "146",
        "156",
        "157",
        "167",
        "234",
        "236",
        "245",
        "246",
        "247",
        "256",
        "267",
        "345",
        "346",
        "356",
        "367",
        "456",
        "457",
        "467",
        "567",
    ]
    expected_family = {
        frozenset(int(character) for character in record)
        for record in expected_family_strings
    }
    assert family == expected_family
    family_verification = verify_family(vertices, graph_edges, family)
    actual_lists = response_lists(reference, vertices, graph_edges, family)
    assert actual_lists == expected_lists

    other_reference = frozenset({1, 2, 7})
    independent_states = sorted(
        tuple(state)
        for state in itertools.combinations(vertices, 3)
        if independent(state, graph_edges)
    )
    assert independent_states == [(0, 1, 2), (1, 2, 7)]
    other_lists = response_lists(other_reference, vertices, graph_edges, family)
    expected_other_lists = {
        0: {7},
        3: {7},
        4: {1, 7},
        5: {2, 7},
        6: {1, 2},
    }
    assert other_lists == expected_other_lists

    rho = {0: 7, 7: 0}

    def image(vertex: int) -> int:
        return rho.get(vertex, vertex)

    covariance_rows = []
    for x in sorted(set(vertices) - set(reference)):
        y = image(x)
        transported = {image(color) for color in actual_lists[x]}
        assert transported == other_lists[y]
        covariance_rows.append(
            {
                "source_vertex": x,
                "target_vertex": y,
                "transported_list": sorted(transported),
            }
        )

    formula_reports = {}
    for name, ref, lists in (
        ("S", reference, actual_lists),
        ("T", other_reference, other_lists),
    ):
        formula = projection_formula(ref, vertices, h_edges, lists)
        cores = inclusion_minimal_cores(
            len(formula["variables"]), formula["constraints"]
        )
        colorings = direct_list_colorings(
            sorted(set(vertices) - set(ref)), h_edges, lists
        )
        assert not colorings
        assert not formula_satisfiable(
            len(formula["variables"]), formula["constraints"]
        )
        formula_reports[name] = {
            "reference": sorted(ref),
            "lists": {str(x): sorted(lists[x]) for x in sorted(lists)},
            "full_list_vertices": [
                x for x in lists if len(lists[x]) == len(ref)
            ],
            "projection_variable_count": len(formula["variables"]),
            "constraint_count": len(formula["constraints"]),
            "minimum_core_size": len(cores[0]),
            "minimum_core_unit_counts": [
                sum(item["kind"] == "unit" for item in core) for core in cores
            ],
            "direct_list_coloring_count": len(colorings),
        }

    clique_partition = [{0, 7}, {1, 3, 6}, {2, 4, 5}]
    assert all(
        edge(u, v) in graph_edges
        for part in clique_partition
        for u, v in pairs(part)
    )
    parameters = {
        "gamma": domination_number(vertices, graph_edges),
        "alpha": independence_number(vertices, graph_edges),
        "gamma_infinity": 3,
        "theta": chromatic_number(vertices, h_edges),
    }
    assert parameters == {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    assert dominates({0, 3}, vertices, graph_edges)
    family_bytes = ("\n".join(expected_family_strings) + "\n").encode()
    return {
        "graph6": graph6,
        "order": len(vertices),
        "size": len(graph_edges),
        "graph_edges": [list(item) for item in sorted(graph_edges)],
        "complement_edges": [list(item) for item in sorted(h_edges)],
        "parameters": parameters,
        "dominating_pair": [0, 3],
        "independent_states": [list(item) for item in independent_states],
        "ridge_pair": [[0, 1, 2], [1, 2, 7]],
        "ridge_transposition": [0, 7],
        "family": expected_family_strings,
        "family_manifest_sha256": hashlib.sha256(family_bytes).hexdigest(),
        "family_verification": family_verification,
        "covariance_rows": covariance_rows,
        "formula_reports": formula_reports,
        "clique_partition": [sorted(part) for part in clique_partition],
        "scope": (
            "Exact nonvacuous covariance countermodel to automatic gluing; "
            "not a gamma-theta counterexample because gamma=2."
        ),
    }


def bounded_order8_zero_unit_scan() -> dict:
    """Search order-eight equality and gamma=2 near-hosts for a zero-unit core."""

    assert GENG.exists()
    records = subprocess.check_output(
        [str(GENG), "-cq", "8"],
        text=True,
    ).splitlines()
    connected_graphs = len(records)
    by_gamma = {
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
        gamma_value = domination_number(vertices, graph_edges)
        if gamma_value not in (2, 3):
            continue
        greatest = greatest_safe_family(vertices, graph_edges, 3)
        if not greatest:
            continue
        bucket = by_gamma[str(gamma_value)]
        bucket["eligible_graphs"] += 1
        for state in itertools.combinations(vertices, 3):
            reference = frozenset(state)
            if not independent(reference, graph_edges):
                continue
            candidates = {}
            for x in set(vertices) - set(reference):
                candidates[x] = [
                    (
                        u,
                        frozenset((set(reference) - {u}) | {x}),
                    )
                    for u in reference
                    if edge(u, x) in graph_edges
                    and frozenset((set(reference) - {u}) | {x}) in greatest
                ]
            if any(len(items) < 2 for items in candidates.values()):
                continue
            bucket["reference_states"] += 1
            choices = []
            for x in sorted(candidates):
                vertex_choices = []
                for pair in itertools.combinations(candidates[x], 2):
                    kept_colors = {item[0] for item in pair}
                    bans = {
                        successor
                        for color, successor in candidates[x]
                        if color not in kept_colors
                    }
                    vertex_choices.append(frozenset(bans))
                choices.append(vertex_choices)
            for selected in itertools.product(*choices):
                bucket["restrictions"] += 1
                banned = frozenset().union(*selected)
                family = greatest_safe_family(vertices, graph_edges, 3, banned)
                if reference not in family:
                    continue
                lists = response_lists(reference, vertices, graph_edges, family)
                if any(len(response) != 2 for response in lists.values()):
                    continue
                bucket["surviving_exact_two_list_families"] += 1
                h_edges = complement_edges(vertices, graph_edges)
                if not direct_list_colorings(
                    sorted(set(vertices) - set(reference)),
                    h_edges,
                    lists,
                ):
                    uncolorable.append(
                        {
                            "graph6": record,
                            "reference": sorted(reference),
                        }
                    )
    return {
        "status": "OBSERVED_BOUNDED_FALSIFICATION",
        "scope": (
            "All connected unlabeled order-eight graphs with alpha="
            "gamma_infinity=3 and gamma in {2,3}; all selected exact "
            "two-list restrictions at independent references."
        ),
        "connected_graphs": connected_graphs,
        "by_gamma": by_gamma,
        "eligible_graphs": sum(item["eligible_graphs"] for item in by_gamma.values()),
        "reference_states_with_two_candidates_per_outside_vertex": sum(
            item["reference_states"] for item in by_gamma.values()
        ),
        "two_list_restrictions": sum(item["restrictions"] for item in by_gamma.values()),
        "surviving_exact_two_list_families": sum(
            item["surviving_exact_two_list_families"] for item in by_gamma.values()
        ),
        "uncolorable_count": len(uncolorable),
        "uncolorable_records": uncolorable,
        "geng_sha256": hashlib.sha256(GENG.read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--skip-order8-scan", action="store_true")
    args = parser.parse_args()
    started = time.time()

    lollipop_lists = {
        3: {0},
        4: {0, 1},
        5: {1, 2},
        6: {1, 2},
    }
    lollipop_h = {
        (3, 4),
        (4, 5),
        (4, 6),
        (5, 6),
    }
    lollipop_policy = [
        ((0, 1, 2), 4, 3),
        ((1, 2, 3), 3, 5),
        ((1, 3, 5), 2, 6),
        ((1, 5, 6), 1, 2),
        ((2, 3, 5), 2, 6),
        ((2, 5, 6), 1, 1),
    ]

    bicycle_lists = {
        3: {0, 1},
        4: {0, 1},
        5: {0, 1},
        6: {0, 2},
        7: {0, 2},
    }
    bicycle_h = {
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (4, 7),
        (5, 6),
        (6, 7),
    }
    bicycle_policy = [
        ((0, 1, 2), 4, 4),
        ((0, 2, 4), 2, 6),
        ((0, 4, 6), 1, 3),
        ((2, 4, 6), 1, 3),
        ((1, 2, 4), 3, 7),
        ((1, 4, 7), 2, 5),
        ((1, 4, 5), 1, 0),
        ((1, 5, 7), 1, 3),
        ((2, 4, 7), 2, 6),
        ((2, 6, 7), 1, 0),
    ]

    result = {
        "schema": "k3-twosat-bicycle-evidence-v1",
        "source_binding": {
            "evidence_py_sha256": hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
            "note_sha256": hashlib.sha256(
                Path(__file__).with_name("NOTE.md").read_bytes()
            ).hexdigest(),
        },
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one occupied adjacent guard moves",
            "family": "every retained state dominates",
        },
        "generic_formula_trichotomy": generic_formula_trichotomy(),
        "excluded_canonical_patterns": {
            "one_unit_lollipop": pattern_report(
                "one-unit lollipop",
                lollipop_lists,
                lollipop_h,
                lollipop_policy,
            ),
            "unit_free_bicycle": pattern_report(
                "unit-free two-variable bicycle",
                bicycle_lists,
                bicycle_h,
                bicycle_policy,
            ),
        },
        "ridge_countermodel": ridge_countermodel(),
        "bounded_order8_zero_unit_scan": (
            {"status": "SKIPPED"}
            if args.skip_order8_scan
            else bounded_order8_zero_unit_scan()
        ),
        "claim_boundary": {
            "proved_by_note": [
                "minimal-unsat terminal trichotomy",
                "projection port-parity translation",
                "canonical one-unit lollipop exclusion",
                "canonical unit-free bicycle exclusion",
            ],
            "exact_countermodel": (
                "GFznc{ has an unsatisfiable no-full-list formula at both "
                "ends of a nontrivial independent ridge, but gamma=2."
            ),
            "not_claimed": [
                "all one-unit lollipops are excluded",
                "all unit-free bicycles are excluded",
                "every minimal bicycle contains a mixed P4",
                "the k=3 slice is resolved",
                "the universal gamma-theta conjecture is resolved",
            ],
        },
    }
    result["elapsed_seconds"] = time.time() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(
        {
            "output": str(args.output),
            "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
            "elapsed_seconds": result["elapsed_seconds"],
            "ridge_graph6": result["ridge_countermodel"]["graph6"],
            "lollipop_policy": result["excluded_canonical_patterns"][
                "one_unit_lollipop"
            ]["attack_policy"]["accepted"],
            "bicycle_policy": result["excluded_canonical_patterns"][
                "unit_free_bicycle"
            ]["attack_policy"]["accepted"],
            "order8_uncolorable": result["bounded_order8_zero_unit_scan"].get(
                "uncolorable_count"
            ),
        },
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
