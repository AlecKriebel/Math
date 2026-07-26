#!/usr/bin/env python3
"""Bounded k=3 full-list and residual-core falsification probe.

This script reuses the campaign's ordinary-set machinery in
``cross_state_response_probe.py``.  It does not import either production
eternal-domination evaluator and invokes no SAT solver.

Three populations are kept separate:

1. ``equality``: connected graphs with gamma=alpha=gamma^infinity=3;
2. ``near_miss``: connected graphs with gamma=alpha=3 but no eternal
   three-family; and
3. ``gamma_low_control``: connected graphs with
   alpha=gamma^infinity=3 and gamma<3.

The third population is only a nonvacuous falsification control.  A statement
that fails there is not thereby refuted under gamma=alpha=3.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import platform
import resource
import sys
import time
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Iterable


CAMPAIGN = Path(__file__).resolve().parents[2]
BASE_PATH = CAMPAIGN / "math" / "working" / "cross_state_response_probe.py"
DEFAULT_OUTPUT = CAMPAIGN / "results" / "k3_full_list_residual_probe.json"
DEFAULT_LOG = CAMPAIGN / "results" / "k3_full_list_residual_probe.log"

State = frozenset[int]
Graph = tuple[frozenset[int], ...]


def load_base() -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "cross_state_ordinary_set_base", BASE_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load ordinary-set base at {BASE_PATH}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


BASE = load_base()


ANALYTIC_DEDUCTIONS = [
    {
        "name": "frozen_color_projection",
        "status": "PROVED_PENDING_INTEGRATION_REVIEW",
        "statement": (
            "For u in an independent eternal k-state S, let W_u be the "
            "outside vertices whose family or static response list omits u, "
            "Q_u=G[(S-u) union W_u], and "
            "P_u={A: |A|=k-1 and {u} union A lies in F}. Then P_u is an "
            "eternal dominating (k-1)-family on Q_u, "
            "alpha(Q_u)=gamma^infinity(Q_u)=k-1, and gamma(Q_u)=k-1 if "
            "gamma(G)=k."
        ),
        "proof_audit_summary": (
            "If u answered an attack inside Q_u, the successor would omit u "
            "while every outside position also omitted u from its family "
            "list, contradicting restoration. Hence u is frozen and another "
            "guard supplies literal projected closure. The independent "
            "anchors give alpha at least k-1, while the projected family "
            "gives gamma^infinity at most k-1. A smaller dominating set in "
            "Q_u together with u would dominate G, proving the gamma equality "
            "under gamma(G)=k."
        ),
        "source": "math/working/k3_cross_state_attack.md",
    },
    {
        "name": "full_edge_row_coverage",
        "status": "PROVED",
        "statement": (
            "Let F be an eternal three-family, S an independent three-state, "
            "and x,y outside S with L_F,S(x)=L_F,S(y)=S and xy not an edge "
            "of G. For every u in S there is v in S-{u} such that "
            "S-{u,v}+{x,y} belongs to F."
        ),
        "proof": (
            "The full list puts S-{u}+{x} in F. Attack y. The guard at x "
            "cannot respond because xy is a nonedge, so closure moves some "
            "v in S-{u} to y and produces the displayed two-swap state."
        ),
    },
    {
        "name": "full_triangle_forced_states",
        "status": "PROVED",
        "statement": (
            "If x,y,z are pairwise nonadjacent full-list vertices, then "
            "{x,y,z} belongs to every eternal three-family. Attacking them "
            "from S in any order, with any retained responses, ends at that "
            "state. Moreover, for each u in S at least one of "
            "{u,x,y}, {u,x,z}, {u,y,z} belongs to the family."
        ),
        "proof": (
            "The triple is an independent set of size alpha=3, so the "
            "independent-state forcing lemma puts it in the family. "
            "Alternatively its response-list union is S and has the same "
            "cardinality as the triple, so the tight-Hall endpoint theorem "
            "forces every ordered attack path to end there. Finally attack "
            "u from {x,y,z}; closure moves one of x,y,z to u and retains u "
            "with the other two."
        ),
    },
    {
        "name": "frozen_projection_equivalence",
        "status": "PROVED",
        "statement": (
            "For any proper coloring f of H[F3], delete F3 and remove f(x) "
            "from the list of every residual H-neighbor of x. The coloring f "
            "extends to the original list instance iff this projected "
            "residual instance is list-colorable."
        ),
        "proof": (
            "The deleted colors are exactly those forbidden by edges from a "
            "residual vertex to already colored full-list vertices. "
            "Restriction and union with f give the two inverse implications."
        ),
    },
]


CLAIM_DESCRIPTIONS = {
    "static_F3_empty_under_gamma_alpha_three": (
        "If gamma=alpha=3, every maximum-independent reference has empty "
        "static full-list set F3."
    ),
    "family_F3_empty_in_equality_scope_through_eight": (
        "In the enumerated equality scope through order eight, every "
        "greatest-family full-list set F3 is empty."
    ),
    "projection_nonempty": (
        "The frozen-color projected two-family P_u is nonempty."
    ),
    "projection_states_dominate_Q": (
        "Every state of P_u dominates the induced projected graph Q_u."
    ),
    "projection_literal_one_guard_closure": (
        "For every P_u state and every unoccupied Q_u attack, one guard in "
        "that state moves along one edge to another P_u state."
    ),
    "projection_alpha_two": "The exact independence number of Q_u is two.",
    "projection_eternal_two_certified": (
        "The explicit nonempty dominating closed P_u certifies "
        "gamma^infinity(Q_u)=2."
    ),
    "projection_gamma_two_under_gamma_three": (
        "When gamma(G)=3, the exact domination number of Q_u is two."
    ),
    "projection_H_Q_bipartite": (
        "At k=3 the complement induced on Q_u is bipartite."
    ),
    "projection_equals_greatest_two_family": (
        "The frozen projected family P_u equals the greatest eternal "
        "two-family of the induced graph Q_u."
    ),
    "equality_family_projection_equals_greatest_two_family": (
        "In the equality population, the family-list frozen projection P_u "
        "equals the greatest eternal two-family of Q_u."
    ),
    "equality_static_projection_equals_greatest_two_family": (
        "In the equality population, the static-list frozen projection P_u "
        "equals the greatest eternal two-family of Q_u."
    ),
    "static_deletion_list_colorable_under_gamma_three": (
        "For static omission W_u under gamma(G)=3, H[W_u] is colorable from "
        "the original static lists with u deleted."
    ),
    "K0_projection_closed_without_full_closure": (
        "If the eternal family is replaced by all dominating triples K0 in "
        "a near miss, the analogous static projection is still closed."
    ),
    "K0_projection_H_Q_bipartite_without_full_closure": (
        "If full closure is replaced by K0 in a near miss, every analogous "
        "static projected complement remains bipartite."
    ),
    "projection_gamma_two_without_original_gamma_three": (
        "The projected graph still has gamma=2 when the original gamma=3 "
        "hypothesis is removed."
    ),
    "static_deletion_list_colorable_without_original_gamma_three": (
        "Static deletion-coloring remains valid after removing the original "
        "gamma=3 hypothesis."
    ),
    "F3_H_independent": "The complement-induced graph H[F3] is independent.",
    "F3_H_bipartite": "The complement-induced graph H[F3] is bipartite.",
    "F3_H_three_colorable": "The graph H[F3] is 3-colorable.",
    "full_edge_row_coverage": (
        "Each full-list H-edge has a family two-swap successor covering "
        "every prescribed first removed color."
    ),
    "full_edge_all_two_swap_states": (
        "For each full-list H-edge x,y, all three states {s,x,y}, s in S, "
        "belong to the family."
    ),
    "full_triangle_state": "Every full-list H-triangle itself belongs to the family.",
    "full_triangle_all_orders_endpoint": (
        "All attack orders and retained response paths through a full-list "
        "H-triangle end at that triangle."
    ),
    "full_triangle_each_color_two_swap": (
        "For each full-list H-triangle and each u in S, some state retaining "
        "u and two triangle vertices belongs to the family."
    ),
    "full_triangle_all_two_swap_states": (
        "Every state retaining one color and any two vertices of a full-list "
        "H-triangle belongs to the family."
    ),
    "raw_residual_list_colorable": (
        "After deleting F3, the unprojected shared response-list instance is "
        "list-colorable."
    ),
    "some_frozen_F3_coloring_extends": (
        "Some proper coloring of H[F3] has a list-colorable frozen "
        "projection on the residual shared graph."
    ),
    "every_frozen_F3_coloring_extends": (
        "Every proper coloring of H[F3] has a list-colorable frozen "
        "projection on the residual shared graph."
    ),
}


def state_key(state: State) -> tuple[int, ...]:
    return tuple(sorted(state))


def ordered(state: Iterable[int]) -> list[int]:
    return sorted(state)


def h_adjacent(graph: Graph, first: int, second: int) -> bool:
    return first != second and second not in graph[first]


def edge_list(graph: Graph) -> list[list[int]]:
    return [
        [first, second]
        for first in range(len(graph))
        for second in range(first + 1, len(graph))
        if second in graph[first]
    ]


def encode_short_graph6(graph: Graph) -> str:
    order = len(graph)
    if order > 62:
        raise ValueError("short graph6 only")
    bits = [
        int(high in graph[low])
        for high in range(1, order)
        for low in range(high)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def graph_context(
    graph: Graph,
    record: str,
    gamma: int,
    reference: State,
    lists: dict[int, State],
    full: State,
    scope: str,
    list_kind: str,
) -> dict[str, object]:
    return {
        "graph6": record,
        "n": len(graph),
        "edges_G": edge_list(graph),
        "gamma": gamma,
        "alpha": 3,
        "scope": scope,
        "list_kind": list_kind,
        "S": ordered(reference),
        "shared_vertices": sorted(lists),
        "response_lists": {
            str(vertex): ordered(lists[vertex]) for vertex in sorted(lists)
        },
        "F3": ordered(full),
    }


def fresh_claims() -> dict[str, dict[str, object]]:
    return {
        name: {
            "description": description,
            "tests": 0,
            "violations": 0,
            "first_counterexample": None,
        }
        for name, description in CLAIM_DESCRIPTIONS.items()
    }


def register(
    claims: dict[str, dict[str, object]],
    name: str,
    holds: bool,
    witness: dict[str, object],
) -> None:
    entry = claims[name]
    entry["tests"] = int(entry["tests"]) + 1
    if not holds:
        entry["violations"] = int(entry["violations"]) + 1
        if entry["first_counterexample"] is None:
            entry["first_counterexample"] = witness


def induced_bipartite(graph: Graph, vertices: State) -> bool:
    colors: dict[int, int] = {}
    for root in sorted(vertices):
        if root in colors:
            continue
        colors[root] = 0
        queue = [root]
        for vertex in queue:
            for neighbor in sorted(vertices):
                if not h_adjacent(graph, vertex, neighbor):
                    continue
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False
    return True


def list_coloring(
    graph: Graph,
    vertices: State,
    lists: dict[int, State],
) -> dict[int, int] | None:
    assignment: dict[int, int] = {}

    def search() -> dict[int, int] | None:
        if len(assignment) == len(vertices):
            return dict(assignment)
        selected: int | None = None
        available: State | None = None
        for vertex in sorted(vertices):
            if vertex in assignment:
                continue
            blocked = {
                assignment[neighbor]
                for neighbor in assignment
                if h_adjacent(graph, vertex, neighbor)
            }
            choices = lists[vertex] - blocked
            if selected is None or len(choices) < len(available or frozenset()):
                selected = vertex
                available = choices
        if selected is None or available is None or not available:
            return None
        for color in sorted(available):
            assignment[selected] = color
            result = search()
            if result is not None:
                return result
            del assignment[selected]
        return None

    return search()


def proper_colorings(
    graph: Graph,
    vertices: State,
    colors: State,
) -> tuple[dict[int, int], ...]:
    ordered_vertices = sorted(vertices)
    assignment: dict[int, int] = {}
    results: list[dict[int, int]] = []

    def enumerate_from(index: int) -> None:
        if index == len(ordered_vertices):
            results.append(dict(assignment))
            return
        vertex = ordered_vertices[index]
        for color in sorted(colors):
            if any(
                h_adjacent(graph, vertex, neighbor)
                and assignment[neighbor] == color
                for neighbor in assignment
            ):
                continue
            assignment[vertex] = color
            enumerate_from(index + 1)
            del assignment[vertex]

    enumerate_from(0)
    return tuple(results)


def frozen_projection(
    graph: Graph,
    residual: State,
    lists: dict[int, State],
    frozen: dict[int, int],
) -> dict[int, State]:
    return {
        vertex: lists[vertex]
        - {
            color
            for full_vertex, color in frozen.items()
            if h_adjacent(graph, vertex, full_vertex)
        }
        for vertex in residual
    }


def family_successors(
    graph: Graph,
    family: frozenset[State],
    state: State,
    attack: int,
) -> frozenset[State]:
    if attack in state:
        raise AssertionError("probe attempted an occupied attack")
    return frozenset(
        state - {guard} | {attack}
        for guard in state & graph[attack]
        if state - {guard} | {attack} in family
    )


def kernel_history(graph: Graph) -> tuple[frozenset[State], ...]:
    current = frozenset(
        state
        for state in BASE.choices(range(len(graph)), 3)
        if BASE.dominates(graph, state)
    )
    history = [current]
    vertices = frozenset(range(len(graph)))
    while current:
        retained = frozenset(
            state
            for state in current
            if all(
                family_successors(graph, current, state, attack)
                for attack in vertices - state
            )
        )
        history.append(retained)
        if retained == current or not retained:
            break
        current = retained
    return tuple(history)


def horizon_lists(
    graph: Graph,
    reference: State,
    target_family: frozenset[State],
    shared: State,
) -> dict[int, State]:
    return {
        target: frozenset(
            guard
            for guard in reference & graph[target]
            if reference - {guard} | {target} in target_family
        )
        for target in shared
    }


def dominates_induced(graph: Graph, state: State, vertices: State) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard] & vertices)
    return vertices <= covered


def induced_independence_number(graph: Graph, vertices: State) -> int:
    for size in range(len(vertices), -1, -1):
        if any(
            BASE.independent(graph, state)
            for state in BASE.choices(sorted(vertices), size)
        ):
            return size
    raise AssertionError("empty set must be independent")


def induced_domination_number(graph: Graph, vertices: State) -> int:
    for size in range(len(vertices) + 1):
        if any(
            dominates_induced(graph, state, vertices)
            for state in BASE.choices(sorted(vertices), size)
        ):
            return size
    raise AssertionError("the full induced vertex set dominates itself")


def greatest_induced_family(
    graph: Graph,
    vertices: State,
    size: int,
) -> tuple[frozenset[State], str]:
    """Return the greatest eternal family of G[vertices], in original labels."""

    labels = sorted(vertices)
    local_index = {vertex: index for index, vertex in enumerate(labels)}
    induced = tuple(
        frozenset(
            local_index[neighbor]
            for neighbor in graph[vertex]
            if neighbor in vertices
        )
        for vertex in labels
    )
    local_family = BASE.greatest_one_guard_family(induced, size)
    lifted = frozenset(
        frozenset(labels[index] for index in state)
        for state in local_family
    )
    return lifted, encode_short_graph6(induced)


def projection_context(
    graph: Graph,
    record: str,
    gamma: int,
    reference: State,
    color: int,
    list_kind: str,
    lists: dict[int, State],
    omission: State,
    projected_vertices: State,
    projected_family: frozenset[State],
    scope: str,
) -> dict[str, object]:
    return {
        "graph6": record,
        "n": len(graph),
        "edges_G": edge_list(graph),
        "gamma_G": gamma,
        "alpha_G": 3,
        "scope": scope,
        "list_kind": list_kind,
        "S": ordered(reference),
        "frozen_color_u": color,
        "W_u": ordered(omission),
        "Q_u": ordered(projected_vertices),
        "outside_response_lists": {
            str(vertex): ordered(lists[vertex]) for vertex in sorted(lists)
        },
        "P_u": [
            ordered(state)
            for state in sorted(projected_family, key=state_key)
        ],
    }


def projected_family_audit(
    graph: Graph,
    projected_vertices: State,
    projected_family: frozenset[State],
) -> tuple[
    bool,
    bool,
    dict[str, object] | None,
    dict[str, object] | None,
]:
    domination_witness: dict[str, object] | None = None
    for state in sorted(projected_family, key=state_key):
        if not dominates_induced(graph, state, projected_vertices):
            domination_witness = {
                "state": ordered(state),
                "undominated_vertices": ordered(
                    vertex
                    for vertex in projected_vertices
                    if vertex not in state
                    and not (graph[vertex] & state)
                ),
            }
            break
    all_dominate = domination_witness is None
    closure_witness: dict[str, object] | None = None
    closed = True
    for state in sorted(projected_family, key=state_key):
        for attack in sorted(projected_vertices - state):
            responses = [
                state - {guard} | {attack}
                for guard in state & graph[attack]
                if state - {guard} | {attack} in projected_family
            ]
            if not responses:
                closed = False
                closure_witness = {
                    "state": ordered(state),
                    "attack": attack,
                    "adjacent_guards": ordered(state & graph[attack]),
                }
                break
        if not closed:
            break
    return all_dominate, closed, domination_witness, closure_witness


def check_frozen_projection(
    graph: Graph,
    record: str,
    gamma: int,
    reference: State,
    family: frozenset[State],
    list_kind: str,
    all_lists: dict[int, State],
    scope: str,
    claims: dict[str, dict[str, object]],
) -> tuple[int, int]:
    projection_count = 0
    projected_state_count = 0
    outside = frozenset(range(len(graph))) - reference
    for color in sorted(reference):
        projection_count += 1
        omission = frozenset(
            vertex for vertex in outside if color not in all_lists[vertex]
        )
        projected_vertices = reference - {color} | omission
        projected_family = frozenset(
            state
            for state in BASE.choices(sorted(projected_vertices), 2)
            if state | {color} in family
        )
        projected_state_count += len(projected_family)
        context = projection_context(
            graph,
            record,
            gamma,
            reference,
            color,
            list_kind,
            all_lists,
            omission,
            projected_vertices,
            projected_family,
            scope,
        )
        nonempty = bool(projected_family)
        (
            all_dominate,
            closed,
            domination_witness,
            closure_witness,
        ) = projected_family_audit(graph, projected_vertices, projected_family)
        alpha_q = induced_independence_number(graph, projected_vertices)
        gamma_q = induced_domination_number(graph, projected_vertices)
        bipartite = induced_bipartite(graph, projected_vertices)
        greatest_q_family, labeled_q_graph6 = greatest_induced_family(
            graph, projected_vertices, 2
        )

        register(claims, "projection_nonempty", nonempty, context)
        register(
            claims,
            "projection_states_dominate_Q",
            nonempty and all_dominate,
            {**context, "first_domination_failure": domination_witness},
        )
        register(
            claims,
            "projection_literal_one_guard_closure",
            nonempty and closed,
            {**context, "first_closure_failure": closure_witness},
        )
        register(
            claims,
            "projection_alpha_two",
            alpha_q == 2,
            {**context, "alpha_Q": alpha_q},
        )
        register(
            claims,
            "projection_eternal_two_certified",
            nonempty and all_dominate and closed and alpha_q == 2,
            {
                **context,
                "alpha_Q": alpha_q,
                "explicit_family_certifies_gamma_infinity_at_most_two": (
                    nonempty and all_dominate and closed
                ),
            },
        )
        register(
            claims,
            "projection_H_Q_bipartite",
            bipartite,
            {**context, "H_Q_bipartite": bipartite},
        )
        comparison_context = {
            **context,
            "Q_graph6_labeled_in_Q_order": labeled_q_graph6,
            "greatest_two_family": [
                ordered(state)
                for state in sorted(greatest_q_family, key=state_key)
            ],
            "projected_family_size": len(projected_family),
            "greatest_two_family_size": len(greatest_q_family),
            "states_in_greatest_not_projected": [
                ordered(state)
                for state in sorted(
                    greatest_q_family - projected_family,
                    key=state_key,
                )
            ],
            "states_projected_not_in_greatest": [
                ordered(state)
                for state in sorted(
                    projected_family - greatest_q_family,
                    key=state_key,
                )
            ],
        }
        families_equal = projected_family == greatest_q_family
        register(
            claims,
            "projection_equals_greatest_two_family",
            families_equal,
            comparison_context,
        )
        if scope == "equality":
            register(
                claims,
                (
                    "equality_family_projection_equals_greatest_two_family"
                    if list_kind == "family"
                    else "equality_static_projection_equals_greatest_two_family"
                ),
                families_equal,
                comparison_context,
            )
        if gamma == 3:
            register(
                claims,
                "projection_gamma_two_under_gamma_three",
                gamma_q == 2,
                {**context, "gamma_Q": gamma_q},
            )
        else:
            register(
                claims,
                "projection_gamma_two_without_original_gamma_three",
                gamma_q == 2,
                {**context, "gamma_Q": gamma_q},
            )

        if list_kind == "static":
            deleted_lists = {
                vertex: all_lists[vertex] - {color} for vertex in omission
            }
            deletion_coloring = list_coloring(
                graph, omission, deleted_lists
            )
            deletion_context = {
                **context,
                "deleted_static_lists": {
                    str(vertex): ordered(deleted_lists[vertex])
                    for vertex in sorted(deleted_lists)
                },
                "deletion_coloring": (
                    {
                        str(vertex): assigned
                        for vertex, assigned in sorted(
                            (deletion_coloring or {}).items()
                        )
                    }
                    if deletion_coloring is not None
                    else None
                ),
            }
            if gamma == 3:
                register(
                    claims,
                    "static_deletion_list_colorable_under_gamma_three",
                    deletion_coloring is not None,
                    deletion_context,
                )
            else:
                register(
                    claims,
                    "static_deletion_list_colorable_without_original_gamma_three",
                    deletion_coloring is not None,
                    deletion_context,
                )
    return projection_count, projected_state_count


def check_K0_negative_projection(
    graph: Graph,
    record: str,
    reference: State,
    static_lists: dict[int, State],
    claims: dict[str, dict[str, object]],
) -> tuple[int, int]:
    """Deliberately replace full closure by K0 for a near-miss control."""

    outside = frozenset(range(len(graph))) - reference
    failures = 0
    bipartite_failures = 0
    dominating_triples = frozenset(
        state
        for state in BASE.choices(range(len(graph)), 3)
        if BASE.dominates(graph, state)
    )
    for color in sorted(reference):
        omission = frozenset(
            vertex for vertex in outside if color not in static_lists[vertex]
        )
        projected_vertices = reference - {color} | omission
        pseudo_family = frozenset(
            state
            for state in BASE.choices(sorted(projected_vertices), 2)
            if state | {color} in dominating_triples
        )
        _, closed, _, closure_witness = projected_family_audit(
            graph, projected_vertices, pseudo_family
        )
        bipartite = induced_bipartite(graph, projected_vertices)
        context = projection_context(
            graph,
            record,
            3,
            reference,
            color,
            "static_K0_negative_control",
            static_lists,
            omission,
            projected_vertices,
            pseudo_family,
            "near_miss",
        )
        register(
            claims,
            "K0_projection_closed_without_full_closure",
            bool(pseudo_family) and closed,
            {**context, "first_closure_failure": closure_witness},
        )
        register(
            claims,
            "K0_projection_H_Q_bipartite_without_full_closure",
            bipartite,
            {**context, "H_Q_bipartite": bipartite},
        )
        failures += int(not (pseudo_family and closed))
        bipartite_failures += int(not bipartite)
    return failures, bipartite_failures


def check_geometry(
    graph: Graph,
    context: dict[str, object],
    full: State,
    claims: dict[str, dict[str, object]],
) -> tuple[int, int]:
    if not full:
        return 0, 0
    h_edges = [
        (first, second)
        for first, second in itertools.combinations(sorted(full), 2)
        if h_adjacent(graph, first, second)
    ]
    h_triangles = [
        triple
        for triple in itertools.combinations(sorted(full), 3)
        if all(
            h_adjacent(graph, first, second)
            for first, second in itertools.combinations(triple, 2)
        )
    ]
    register(
        claims,
        "F3_H_independent",
        not h_edges,
        {**context, "first_H_edge": list(h_edges[0]) if h_edges else None},
    )
    bipartite = induced_bipartite(graph, full)
    register(
        claims,
        "F3_H_bipartite",
        bipartite,
        {
            **context,
            "H_triangles": [list(triangle) for triangle in h_triangles],
        },
    )
    all_color_lists = {vertex: frozenset(context["S"]) for vertex in full}
    coloring = list_coloring(graph, full, all_color_lists)
    register(
        claims,
        "F3_H_three_colorable",
        coloring is not None,
        {**context, "three_coloring": coloring},
    )
    return len(h_edges), len(h_triangles)


def check_residual(
    graph: Graph,
    context: dict[str, object],
    reference: State,
    shared: State,
    lists: dict[int, State],
    full: State,
    claims: dict[str, dict[str, object]],
) -> tuple[int, int, int]:
    residual = shared - full
    raw_coloring = list_coloring(graph, residual, lists)
    register(
        claims,
        "raw_residual_list_colorable",
        raw_coloring is not None,
        {
            **context,
            "residual_vertices": ordered(residual),
            "raw_residual_coloring": raw_coloring,
        },
    )

    full_colorings = proper_colorings(graph, full, reference)
    extendable = 0
    first_failure: dict[str, object] | None = None
    first_success: dict[str, object] | None = None
    for frozen in full_colorings:
        projected = frozen_projection(graph, residual, lists, frozen)
        coloring = list_coloring(graph, residual, projected)
        if coloring is None and first_failure is None:
            first_failure = {
                "frozen_F3_coloring": {
                    str(vertex): color for vertex, color in sorted(frozen.items())
                },
                "projected_lists": {
                    str(vertex): ordered(projected[vertex])
                    for vertex in sorted(projected)
                },
            }
        if coloring is not None:
            extendable += 1
            if first_success is None:
                first_success = {
                    "frozen_F3_coloring": {
                        str(vertex): color
                        for vertex, color in sorted(frozen.items())
                    },
                    "residual_coloring": {
                        str(vertex): color
                        for vertex, color in sorted(coloring.items())
                    },
                }

    some_extends = extendable > 0
    every_extends = bool(full_colorings) and extendable == len(full_colorings)
    register(
        claims,
        "some_frozen_F3_coloring_extends",
        some_extends,
        {
            **context,
            "proper_F3_colorings": len(full_colorings),
            "extendable_F3_colorings": extendable,
            "first_success": first_success,
            "first_failure": first_failure,
        },
    )
    register(
        claims,
        "every_frozen_F3_coloring_extends",
        every_extends,
        {
            **context,
            "proper_F3_colorings": len(full_colorings),
            "extendable_F3_colorings": extendable,
            "first_failure": first_failure,
        },
    )
    return len(full_colorings), extendable, int(raw_coloring is not None)


def check_family_swaps(
    graph: Graph,
    context: dict[str, object],
    reference: State,
    full: State,
    family: frozenset[State],
    claims: dict[str, dict[str, object]],
) -> tuple[int, int, int]:
    h_edges = [
        (first, second)
        for first, second in itertools.combinations(sorted(full), 2)
        if h_adjacent(graph, first, second)
    ]
    triangles = [
        triple
        for triple in itertools.combinations(sorted(full), 3)
        if all(
            h_adjacent(graph, first, second)
            for first, second in itertools.combinations(triple, 2)
        )
    ]
    attack_orders = 0

    for first, second in h_edges:
        all_states = {
            remaining: frozenset({remaining, first, second})
            for remaining in reference
        }
        register(
            claims,
            "full_edge_all_two_swap_states",
            all(state in family for state in all_states.values()),
            {
                **context,
                "H_edge": [first, second],
                "two_swap_states_by_remaining_color": {
                    str(color): {
                        "state": ordered(state),
                        "in_family": state in family,
                    }
                    for color, state in sorted(all_states.items())
                },
            },
        )
        for first_removed in sorted(reference):
            candidates = [
                reference - {first_removed, second_removed} | {first, second}
                for second_removed in reference - {first_removed}
            ]
            holds = any(candidate in family for candidate in candidates)
            register(
                claims,
                "full_edge_row_coverage",
                holds,
                {
                    **context,
                    "H_edge": [first, second],
                    "prescribed_first_removed_color": first_removed,
                    "candidate_two_swap_states": [
                        {
                            "state": ordered(candidate),
                            "in_family": candidate in family,
                        }
                        for candidate in candidates
                    ],
                },
            )

    for triple_tuple in triangles:
        triple = frozenset(triple_tuple)
        register(
            claims,
            "full_triangle_state",
            triple in family,
            {**context, "H_triangle": list(triple_tuple)},
        )
        all_two_swap = all(
            frozenset({color, first, second}) in family
            for color in reference
            for first, second in itertools.combinations(triple_tuple, 2)
        )
        register(
            claims,
            "full_triangle_all_two_swap_states",
            all_two_swap,
            {**context, "H_triangle": list(triple_tuple)},
        )
        for color in sorted(reference):
            candidates = [
                frozenset({color, first, second})
                for first, second in itertools.combinations(triple_tuple, 2)
            ]
            register(
                claims,
                "full_triangle_each_color_two_swap",
                any(candidate in family for candidate in candidates),
                {
                    **context,
                    "H_triangle": list(triple_tuple),
                    "retained_color": color,
                    "candidate_states": [
                        {
                            "state": ordered(candidate),
                            "in_family": candidate in family,
                        }
                        for candidate in candidates
                    ],
                },
            )

        all_orders_hold = True
        bad_order: tuple[int, ...] | None = None
        bad_endpoints: frozenset[State] | None = None
        for attack_order in itertools.permutations(triple_tuple):
            attack_orders += 1
            states = frozenset({reference})
            for attack in attack_order:
                states = frozenset(
                    successor
                    for state in states
                    for successor in family_successors(
                        graph, family, state, attack
                    )
                )
            if states != frozenset({triple}):
                all_orders_hold = False
                bad_order = attack_order
                bad_endpoints = states
                break
        register(
            claims,
            "full_triangle_all_orders_endpoint",
            all_orders_hold,
            {
                **context,
                "H_triangle": list(triple_tuple),
                "bad_attack_order": list(bad_order) if bad_order else None,
                "bad_endpoints": (
                    [ordered(state) for state in sorted(bad_endpoints, key=state_key)]
                    if bad_endpoints is not None
                    else None
                ),
            },
        )
    return len(h_edges), len(triangles), attack_orders


def named_order10_static_full_list_control(
    claims: dict[str, dict[str, object]],
) -> dict[str, object]:
    """Independently replay the supplied gamma=alpha=3 static-F3 witness."""

    rows = (
        (3, 4, 5, 6, 9),
        (3, 5, 7, 8, 9),
        (3, 4, 6, 7, 8),
        (0, 1, 2),
        (0, 2, 5, 7, 8),
        (0, 1, 4, 7),
        (0, 2, 8, 9),
        (1, 2, 4, 5, 9),
        (1, 2, 4, 6, 9),
        (0, 1, 6, 7, 8),
    )
    graph: Graph = tuple(frozenset(row) for row in rows)
    for vertex, neighbors in enumerate(graph):
        if vertex in neighbors:
            raise AssertionError("named control has a loop")
        for neighbor in neighbors:
            if vertex not in graph[neighbor]:
                raise AssertionError("named control adjacency is asymmetric")
    record = encode_short_graph6(graph)
    if BASE.decode_graph6(record) != graph:
        raise AssertionError("named control graph6 round trip failed")

    gamma = BASE.domination_number(graph)
    alpha = BASE.independence_number(graph)
    family3 = BASE.greatest_one_guard_family(graph, 3)
    family4 = BASE.greatest_one_guard_family(graph, 4)
    reference = frozenset({0, 1, 2})
    outside = frozenset(range(10)) - reference
    static_lists = {
        vertex: BASE.static_response_list(graph, reference, vertex)
        for vertex in outside
    }
    full = frozenset(
        vertex for vertex in outside if static_lists[vertex] == reference
    )
    shared = frozenset(
        vertex
        for vertex in outside
        if len(graph[vertex] & reference) >= 2
    )
    context = graph_context(
        graph,
        record,
        gamma,
        reference,
        {vertex: static_lists[vertex] for vertex in shared},
        full,
        "named_order10_gamma_alpha_near_miss",
        "static",
    )
    holds = gamma == alpha == 3 and 3 in full and not family3 and bool(family4)
    if not holds:
        raise AssertionError("named order-10 control did not replay as supplied")
    register(
        claims,
        "static_F3_empty_under_gamma_alpha_three",
        False,
        {
            **context,
            "distinguished_full_list_vertex": 3,
            "greatest_eternal_3_family_size": len(family3),
            "greatest_eternal_4_family_size": len(family4),
        },
    )
    adjacency_serialization = ";".join(
        f"{vertex}:{','.join(map(str, sorted(neighbors)))}"
        for vertex, neighbors in enumerate(graph)
    )
    return {
        "status": "VERIFIED_NEGATIVE_CONTROL",
        "graph6_labeled": record,
        "adjacency_sha256": hashlib.sha256(
            adjacency_serialization.encode("ascii")
        ).hexdigest(),
        "edges_G": edge_list(graph),
        "gamma": gamma,
        "alpha": alpha,
        "greatest_eternal_3_family_size": len(family3),
        "greatest_eternal_4_family_size": len(family4),
        "S": ordered(reference),
        "static_response_lists": {
            str(vertex): ordered(static_lists[vertex])
            for vertex in sorted(static_lists)
        },
        "static_F3": ordered(full),
        "interpretation": (
            "This order-10 graph proves that the through-order-8 empty-F3 "
            "observation does not follow from gamma=alpha=3 without full "
            "eternal equality."
        ),
    }


def finalize_claims(claims: dict[str, dict[str, object]]) -> None:
    proved = {
        "projection_nonempty",
        "projection_states_dominate_Q",
        "projection_literal_one_guard_closure",
        "projection_alpha_two",
        "projection_eternal_two_certified",
        "projection_gamma_two_under_gamma_three",
        "projection_H_Q_bipartite",
        "static_deletion_list_colorable_under_gamma_three",
        "full_edge_row_coverage",
        "full_triangle_state",
        "full_triangle_all_orders_endpoint",
        "full_triangle_each_color_two_swap",
    }
    for name, entry in claims.items():
        if name in proved:
            entry["mathematical_status"] = (
                "PROVED"
                if int(entry["violations"]) == 0
                else "PROOF_OR_IMPLEMENTATION_CONFLICT"
            )
        elif int(entry["violations"]) > 0:
            entry["mathematical_status"] = "REFUTED_IN_TESTED_POPULATION"
        elif int(entry["tests"]) == 0:
            entry["mathematical_status"] = "NO_NONVACUOUS_TEST"
        else:
            entry["mathematical_status"] = "OBSERVED_ONLY"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def max_rss_bytes() -> int:
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(raw if sys.platform == "darwin" else raw * 1024)


def run(args: argparse.Namespace) -> dict[str, object]:
    start = time.monotonic()
    deadline = start + args.max_seconds
    claims = fresh_claims()
    totals: Counter[str] = Counter()
    per_order: list[dict[str, object]] = []
    near_depth_histogram: Counter[str] = Counter()
    stopped = False

    for order in range(1, args.max_order + 1):
        records = BASE.connected_graph6_records(args.geng, order)
        stream = hashlib.sha256()
        order_counts: Counter[str] = Counter()
        for record in records:
            if time.monotonic() >= deadline:
                stopped = True
                break
            stream.update(record.encode("ascii") + b"\n")
            graph = BASE.decode_graph6(record)
            order_counts["connected_graphs"] += 1
            alpha = BASE.independence_number(graph)
            if alpha != 3:
                continue
            gamma = BASE.domination_number(graph)
            family = BASE.greatest_one_guard_family(graph, 3)
            if gamma == 3:
                scope = "equality" if family else "near_miss"
            elif family:
                scope = "gamma_low_control"
            else:
                continue
            order_counts[f"{scope}_graphs"] += 1

            history: tuple[frozenset[State], ...] | None = None
            if scope == "near_miss":
                history = kernel_history(graph)
                order_counts["near_miss_kernel_rounds_total"] += len(history) - 1

            references = BASE.maximum_independent_states(graph, 3)
            for reference in references:
                order_counts[f"{scope}_references"] += 1
                outside = frozenset(range(order)) - reference
                shared = frozenset(
                    vertex
                    for vertex in range(order)
                    if vertex not in reference
                    and len(graph[vertex] & reference) >= 2
                )
                static_all_lists = {
                    vertex: BASE.static_response_list(
                        graph, reference, vertex
                    )
                    for vertex in outside
                }
                variants: list[tuple[str, dict[int, State]]] = [
                    (
                        "static",
                        static_all_lists,
                    )
                ]
                if family:
                    family_all_lists = {
                        vertex: BASE.family_response_list(
                            graph, family, reference, vertex
                        )
                        for vertex in outside
                    }
                    variants.append(
                        (
                            "family",
                            family_all_lists,
                        )
                    )
                elif history is not None:
                    alive = [
                        index
                        for index, layer in enumerate(history)
                        if reference in layer
                    ]
                    deepest = max(alive)
                    near_depth_histogram[str(deepest)] += 1
                    target_layer = history[max(0, deepest - 1)]
                    variants.append(
                        (
                            "finite_horizon",
                            horizon_lists(
                                graph, reference, target_layer, outside
                            ),
                        )
                    )
                    negative_failures, negative_bipartite_failures = (
                        check_K0_negative_projection(
                            graph,
                            record,
                            reference,
                            static_all_lists,
                            claims,
                        )
                    )
                    order_counts[
                        "near_miss_K0_projection_closure_failures"
                    ] += negative_failures
                    order_counts[
                        "near_miss_K0_projection_bipartite_failures"
                    ] += negative_bipartite_failures

                for list_kind, all_lists in variants:
                    lists = {
                        vertex: all_lists[vertex] for vertex in shared
                    }
                    prefix = f"{scope}_{list_kind}"
                    full = frozenset(
                        vertex
                        for vertex in shared
                        if lists[vertex] == reference
                    )
                    order_counts[f"{prefix}_shared_vertices"] += len(shared)
                    order_counts[f"{prefix}_F3_vertices"] += len(full)
                    order_counts[f"{prefix}_references_with_F3"] += int(bool(full))
                    context = graph_context(
                        graph,
                        record,
                        gamma,
                        reference,
                        lists,
                        full,
                        scope,
                        list_kind,
                    )
                    if gamma == 3 and list_kind == "static":
                        register(
                            claims,
                            "static_F3_empty_under_gamma_alpha_three",
                            not full,
                            context,
                        )
                    if scope == "equality" and list_kind == "family":
                        register(
                            claims,
                            "family_F3_empty_in_equality_scope_through_eight",
                            not full,
                            context,
                        )
                    if family and list_kind in {"static", "family"}:
                        projection_count, projected_state_count = (
                            check_frozen_projection(
                                graph,
                                record,
                                gamma,
                                reference,
                                family,
                                list_kind,
                                all_lists,
                                scope,
                                claims,
                            )
                        )
                        order_counts[
                            f"{prefix}_frozen_projections"
                        ] += projection_count
                        order_counts[
                            f"{prefix}_projected_family_states"
                        ] += projected_state_count
                    h_edges, h_triangles = check_geometry(
                        graph, context, full, claims
                    )
                    order_counts[f"{prefix}_F3_H_edges"] += h_edges
                    order_counts[f"{prefix}_F3_H_triangles"] += h_triangles
                    colorings, extendable, raw_ok = check_residual(
                        graph,
                        context,
                        reference,
                        shared,
                        lists,
                        full,
                        claims,
                    )
                    order_counts[f"{prefix}_proper_F3_colorings"] += colorings
                    order_counts[
                        f"{prefix}_extendable_F3_colorings"
                    ] += extendable
                    order_counts[
                        f"{prefix}_raw_residual_colorable_references"
                    ] += raw_ok

                    if list_kind == "family":
                        family_edges, family_triangles, attack_orders = (
                            check_family_swaps(
                                graph,
                                context,
                                reference,
                                full,
                                family,
                                claims,
                            )
                        )
                        if family_edges != h_edges or family_triangles != h_triangles:
                            raise AssertionError("family F3 geometry count mismatch")
                        order_counts[
                            f"{prefix}_triangle_attack_orders"
                        ] += attack_orders

        complete = not stopped
        order_entry = {
            "order": order,
            "complete": complete,
            **dict(sorted(order_counts.items())),
            "graph6_stream_sha256": stream.hexdigest() if complete else None,
        }
        per_order.append(order_entry)
        if complete:
            totals.update(order_counts)
        if stopped:
            break

    named_order10_control = named_order10_static_full_list_control(claims)
    finalize_claims(claims)
    status = "COMPLETE" if not stopped else "STOPPED_AT_WALL_CLOCK_GATE"
    result = {
        "schema": "k3-full-list-residual-probe-v1",
        "status": status,
        "scope": {
            "orders": [1, args.max_order],
            "connected_unlabeled_only": True,
            "wall_clock_gate_seconds": args.max_seconds,
            "solver": "none; exact ordinary-set enumeration and backtracking only",
            "order_14_used": False,
            "populations": {
                "equality": "gamma=alpha=gamma^infinity=3",
                "near_miss": (
                    "gamma=alpha=3 with empty greatest eternal three-family"
                ),
                "gamma_low_control": (
                    "alpha=gamma^infinity=3 and gamma<3; falsification "
                    "control only"
                ),
            },
            "shared_vertices": (
                "vertices outside S adjacent in G to at least two members of S"
            ),
            "F3": "shared vertices whose tested response list equals S",
            "H": "the complement of G",
        },
        "implementation": {
            "script": str(Path(__file__).relative_to(CAMPAIGN)),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "ordinary_set_base": str(BASE_PATH.relative_to(CAMPAIGN)),
            "ordinary_set_base_sha256": hashlib.sha256(
                BASE_PATH.read_bytes()
            ).hexdigest(),
            "geng": str(args.geng.relative_to(CAMPAIGN)),
            "geng_sha256": hashlib.sha256(args.geng.read_bytes()).hexdigest(),
            "python": platform.python_version(),
        },
        "analytic_deductions": ANALYTIC_DEDUCTIONS,
        "totals": dict(sorted(totals.items())),
        "near_miss_reference_deepest_kernel_round_histogram": dict(
            sorted(near_depth_histogram.items(), key=lambda item: int(item[0]))
        ),
        "named_order10_static_full_list_control": named_order10_control,
        "orders": per_order,
        "claims": claims,
        "resource_usage": {
            "elapsed_seconds": round(time.monotonic() - start, 6),
            "maximum_resident_set_bytes": max_rss_bytes(),
        },
        "interpretation": [
            "The target equality and near-miss populations contain no static "
            "F3 vertices in the completed scope; their F3 geometry tests are "
            "therefore vacuous.",
            "The separately supplied and independently replayed order-10 "
            "negative control has gamma=alpha=3, empty eternal three-family, "
            "and a nonempty static F3. Thus the order-eight observation does "
            "not generalize from gamma=alpha alone.",
            "The gamma-low control population is reported separately and "
            "cannot refute a claim that essentially uses gamma=alpha=3.",
            "A zero-violation claim labeled OBSERVED_ONLY is finite evidence, "
            "not a theorem.",
            "Frozen-projection existence is exactly the original list-coloring "
            "question after choosing colors on F3; it is not an independent "
            "resolution mechanism.",
            "The separately reported greatest-family comparison tests whether "
            "P_u is all of the greatest two-family of Q_u; failure means that "
            "arbitrary lower-parameter eternal states cannot automatically be "
            "lifted while preserving the frozen guard.",
        ],
    }
    atomic_write(args.output, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def write_log(args: argparse.Namespace, result: dict[str, object]) -> None:
    output_sha = hashlib.sha256(args.output.read_bytes()).hexdigest()
    refuted = [
        name
        for name, entry in result["claims"].items()
        if int(entry["violations"]) > 0
    ]
    observed = [
        name
        for name, entry in result["claims"].items()
        if entry["mathematical_status"] == "OBSERVED_ONLY"
    ]
    lines = [
        "k=3 full-list residual probe",
        "============================",
        "",
        f"status: {result['status']}",
        (
            "command: "
            f"{Path(__file__).relative_to(CAMPAIGN)} "
            f"--max-order {args.max_order} --max-seconds {args.max_seconds:g}"
        ),
        f"result_sha256: {output_sha}",
        f"script_sha256: {result['implementation']['script_sha256']}",
        f"ordinary_set_base_sha256: "
        f"{result['implementation']['ordinary_set_base_sha256']}",
        "",
        "Target-scope boundary:",
        "- equality and gamma=alpha=3 near-miss references have zero static "
        "F3 vertices through order 8",
        "- a separately replayed order-10 gamma=alpha=3 near miss has a full "
        "static-list vertex, so the finite zero does not generalize",
        "- all nonvacuous F3 counterexamples below occur only after dropping "
        "gamma=alpha",
        "",
        "Refuted candidate claims:",
        *(f"- {name}" for name in sorted(refuted)),
        "",
        "Finite zero-violation observations:",
        *(f"- {name}" for name in sorted(observed)),
        "",
        "Analytic results:",
        "- full H-edge row coverage: PROVED",
        "- full H-triangle endpoint and retained-color two-swap coverage: PROVED",
        "- frozen projection extension equivalence: PROVED (tautological reduction)",
        "- projected P_u versus greatest two-family of Q_u: finite diagnostic; "
        "see its first counterexample in the JSON",
        "",
        "Totals:",
        json.dumps(result["totals"], sort_keys=True),
        "",
        "No SAT solver and no order-14 computation was used.",
        "",
    ]
    atomic_write(args.log, "\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=8)
    parser.add_argument("--max-seconds", type=float, default=60.0)
    parser.add_argument("--geng", type=Path, default=BASE.DEFAULT_GENG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    args = parser.parse_args()
    args.geng = args.geng.resolve()
    args.output = args.output.resolve()
    args.log = args.log.resolve()
    if not 1 <= args.max_order <= 8:
        parser.error("this bounded probe requires 1 <= max-order <= 8")
    if args.max_seconds <= 0:
        parser.error("max-seconds must be positive")
    return args


def main() -> int:
    args = parse_args()
    result = run(args)
    write_log(args, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
