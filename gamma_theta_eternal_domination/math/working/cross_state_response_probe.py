#!/usr/bin/env python3
"""Bounded ordinary-set probe for cross-state one-guard response claims.

The implementation is intentionally separate from the campaign evaluators.
It uses Python ``set``/``frozenset`` objects, a local graph6 decoder, direct
subset enumeration, and literal greatest-fixed-point deletion.  The only
external program invoked is the pinned nauty ``geng`` executable, restricted
to connected unlabeled graphs.

Scope
-----
Only graphs satisfying

    gamma(G) = alpha(G) = gamma^infinity(G) = k

are used for the cross-state tests.  The equality with eternal domination is
certified here by a nonempty greatest one-guard k-family together with
gamma=alpha=k.

The probe distinguishes:

* static lists: the swap is along an edge and the successor dominates;
* family lists: the swap is along an edge and the successor is in the
  greatest eternal k-family.

It writes an atomic JSON checkpoint after every completed order.  A strict
wall-clock gate stops before beginning another graph once the budget expires.
No SAT solver and no order-13/order-14 computation is used.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Iterable


CAMPAIGN = Path(__file__).resolve().parents[2]
DEFAULT_GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
DEFAULT_OUTPUT = CAMPAIGN / "results" / "cross_state_response_probe.json"
DEFAULT_LOG = CAMPAIGN / "results" / "cross_state_response_probe.log"

State = frozenset[int]
Graph = tuple[frozenset[int], ...]
ListFunction = Callable[[State, int], frozenset[int]]


PROPERTY_DESCRIPTIONS = {
    "co_state_common_H_neighborhood_is_H_edgeless": (
        "For every greatest-family state D=R union {u}, the common open "
        "H-neighborhood C=N_H(R), with H the complement, is edgeless in H "
        "(equivalently, C is a clique in G)."
    ),
    "co_state_unique_forced_response": (
        "For D=R union {u} and every r in N_H(R)-D, the only guard adjacent "
        "to r is u and the forced successor R union {r} remains in the "
        "greatest eternal family."
    ),
    "tight_Hall_endpoint_membership": (
        "For an independent family state S and independent outside set X, "
        "if U is the union of the family-response lists of X and "
        "|U|=|X|, then (S-U) union X lies in the family."
    ),
    "tight_Hall_all_orders_force_endpoint": (
        "Under the preceding tight-Hall hypotheses, every ordering of X and "
        "every sequence of family-retained legal responses ends at the same "
        "state (S-U) union X."
    ),
    "maximum_independent_exchange_graph_connected": (
        "The graph whose vertices are maximum independent states and whose "
        "edges are one-vertex exchanges is connected."
    ),
    "exchange_transport_has_trivial_holonomy": (
        "Within every component of the maximum-independent exchange graph, "
        "transporting guard labels along one-vertex exchanges is independent "
        "of the chosen path."
    ),
    "control_directed_static_matching": (
        "For every ordered pair S,T of maximum independent states, the "
        "static S-response relation from S-T to T-S has a perfect matching."
    ),
    "control_directed_family_matching": (
        "For every ordered pair S,T of maximum independent states, the "
        "greatest-family S-response relation from S-T to T-S has a perfect "
        "matching. This is a finite control for the proved Hall theorem."
    ),
    "pairwise_static_reciprocity": (
        "For every maximum-independent pair S,T and every u in S-T, x in "
        "T-S, u is a static S-response to x iff x is a static T-response "
        "to u."
    ),
    "pairwise_family_reciprocity": (
        "The preceding reciprocity assertion with greatest-family response "
        "lists."
    ),
    "mutual_static_matching": (
        "For every maximum-independent pair S,T, the edges that are static "
        "responses in both directions contain a perfect matching."
    ),
    "mutual_family_matching": (
        "For every maximum-independent pair S,T, the edges that are "
        "greatest-family responses in both directions contain a perfect "
        "matching."
    ),
    "static_state_base_orderability": (
        "For every maximum-independent pair S,T there is a bijection phi "
        "from S-T to T-S such that every mixed state "
        "(S-A) union phi(A) dominates, for every A subseteq S-T."
    ),
    "family_state_base_orderability": (
        "The preceding assertion with every mixed state required to lie in "
        "the greatest eternal family."
    ),
    "static_response_base_orderability": (
        "Static state base-orderability holds with every paired u,phi(u) "
        "adjacent, so all paired singleton exchanges are legal responses."
    ),
    "family_response_base_orderability": (
        "Greatest-family state base-orderability holds with every paired "
        "u,phi(u) adjacent."
    ),
    "adjacent_static_common_color_stability": (
        "If T=S-a+b is an adjacent maximum-independent exchange, then for "
        "each y outside S union T and common guard v, v belongs to the "
        "static list at S iff it belongs to the static list at T."
    ),
    "adjacent_family_common_color_stability": (
        "The preceding common-color stability assertion for greatest-family "
        "lists."
    ),
    "adjacent_static_exchanged_color_reciprocity": (
        "Under T=S-a+b, a belongs to the static S-list of y iff b belongs "
        "to the static T-list of y."
    ),
    "adjacent_family_exchanged_color_reciprocity": (
        "The preceding exchanged-color assertion for greatest-family lists."
    ),
    "adjacent_static_transport_equality": (
        "Under T=S-a+b, transporting colors by a->b and fixing S intersect "
        "T sends the complete static S-list of y exactly to its T-list."
    ),
    "adjacent_family_transport_equality": (
        "The preceding transported-list equality for greatest-family lists."
    ),
    "adjacent_static_list_size_equality": (
        "Static response-list cardinality is unchanged under an adjacent "
        "maximum-independent reference-state exchange."
    ),
    "adjacent_family_list_size_equality": (
        "Greatest-family response-list cardinality is unchanged under an "
        "adjacent maximum-independent reference-state exchange."
    ),
}


ANALYTIC_DEDUCTIONS = [
    {
        "name": "co_state_ridge_link",
        "status": "PROVED",
        "statement": (
            "Let H be the complement of G, let F be an eternal k-family, "
            "and write any D in F as R union {u}. If C=N_H(R) is the common "
            "open H-neighborhood of R, then H[C] is edgeless. For every "
            "r in C-D, the attack at r has the unique possible response "
            "u->r, and R union {r} lies in F."
        ),
        "proof": (
            "Every r in C-D is nonadjacent in G to all guards in R. Since "
            "D dominates r, ur is an edge; hence u is the unique possible "
            "responding guard, and closure puts R union {r} in F. If "
            "distinct r,s in C were nonadjacent in G, first use the forced "
            "move u->r (when needed) and then attack s. No guard in R union "
            "{r} would be adjacent to s, contradicting eternal closure. "
            "Pairs involving u are already adjacent by domination, so all "
            "of C is a G-clique."
        ),
    },
    {
        "name": "tight_Hall_forced_state",
        "status": "PROVED",
        "statement": (
            "Let S be an independent k-state in an eternal family F, let X "
            "be an independent subset of V-S, and put "
            "U=union_{x in X} L_F,S(x). If |U|=|X|, then attacking the "
            "vertices of X in any order, with any family-retained legal "
            "responses, ends at the fixed state (S-U) union X in F."
        ),
        "proof": (
            "Because X is independent, a guard moved to an earlier attacked "
            "vertex cannot answer a later attack. Thus the final state is "
            "(S-W) union X for a set W of |X| distinct original guards. "
            "The family-response restoration argument gives W subseteq U. "
            "Tightness |W|=|X|=|U| forces W=U, independently of the attack "
            "order and all response choices. The endpoint belongs to F "
            "because every chosen successor did."
        ),
    },
    {
        "name": "adjacent_exchanged_color_reciprocity",
        "status": "PROVED",
        "statement": (
            "Let F be an eternal k-family and let S=C union {a} and "
            "T=C union {b} be independent states in F, differing by one "
            "position. For y outside S union T, a is in L_F,S(y) iff b is "
            "in L_F,T(y). The same equivalence holds for static dominating "
            "response lists."
        ),
        "proof": (
            "Maximality of the equal-size independent states forces ab to be "
            "an edge. Both list memberships use the same successor C union "
            "{y}. If that successor dominates, then y must dominate both "
            "omitted vertices a and b because C is nonadjacent to both. Thus "
            "both required move edges exist, and family membership is "
            "literally the same condition on both sides."
        ),
    },
    {
        "name": "adjacent_family_response_list_transport",
        "status": "PROVED",
        "statement": (
            "Under the preceding hypotheses, let tau:S->T fix C and send "
            "a to b. For every y outside S union T, "
            "tau(L_F,S(y))=L_F,T(y)."
        ),
        "proof": (
            "Exchanged-color membership is the preceding deduction. For "
            "v in C, suppose D=(C-{v}) union {a,y} lies in F and vy is an "
            "edge. Attack the unoccupied vertex b. No guard in C-{v} can "
            "respond because T is independent. Moving y to b would leave "
            "(C-{v}) union {a,b}, which does not dominate v because v is "
            "nonadjacent to C-{v}, a, and b. Hence closure forces a to move "
            "to b, placing (C-{v}) union {b,y} in F. This proves preservation "
            "of the common color v; the reverse implication is symmetric."
        ),
        "corollary": (
            "Along any path in the maximum-independent one-exchange graph, "
            "greatest-family response lists are transported exactly by the "
            "composed token-label map. This does not coordinate distinct "
            "components and does not make the transport path-independent."
        ),
    },
]

ANALYTICALLY_PROVED_PROPERTIES = {
    "co_state_common_H_neighborhood_is_H_edgeless",
    "co_state_unique_forced_response",
    "tight_Hall_endpoint_membership",
    "tight_Hall_all_orders_force_endpoint",
    "adjacent_static_exchanged_color_reciprocity",
    "adjacent_family_exchanged_color_reciprocity",
    "adjacent_family_common_color_stability",
    "adjacent_family_transport_equality",
    "adjacent_family_list_size_equality",
}


def decode_graph6(record: str) -> Graph:
    """Decode canonical short graph6 without using a graph library."""

    raw = record.strip().encode("ascii")
    if not raw or not 63 <= raw[0] <= 125:
        raise ValueError(f"unsupported graph6 header: {record!r}")
    order = raw[0] - 63
    if order > 62:
        raise ValueError("this bounded probe accepts short graph6 only")
    bit_count = order * (order - 1) // 2
    payload_length = (bit_count + 5) // 6
    if len(raw) != payload_length + 1:
        raise ValueError(f"noncanonical graph6 payload: {record!r}")

    payload_bits: list[int] = []
    for byte in raw[1:]:
        if not 63 <= byte <= 126:
            raise ValueError(f"invalid graph6 byte in {record!r}")
        six = byte - 63
        payload_bits.extend((six >> shift) & 1 for shift in range(5, -1, -1))
    if any(payload_bits[bit_count:]):
        raise ValueError(f"nonzero graph6 padding in {record!r}")

    neighbors = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if payload_bits[cursor]:
                neighbors[low].add(high)
                neighbors[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in neighbors)


def connected_graph6_records(geng: Path, order: int) -> tuple[str, ...]:
    completed = subprocess.run(
        (str(geng), "-cq", str(order)),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stderr:
        raise RuntimeError(
            f"pinned geng unexpectedly wrote stderr at order {order}: "
            f"{completed.stderr!r}"
        )
    return tuple(line for line in completed.stdout.splitlines() if line)


def choices(vertices: Iterable[int], size: int) -> tuple[State, ...]:
    return tuple(frozenset(group) for group in itertools.combinations(vertices, size))


def independent(graph: Graph, state: State) -> bool:
    return all(not (graph[vertex] & state) for vertex in state)


def dominates(graph: Graph, state: State) -> bool:
    covered = set(state)
    for vertex in state:
        covered.update(graph[vertex])
    return len(covered) == len(graph)


def independence_number(graph: Graph) -> int:
    vertices = range(len(graph))
    for size in range(len(graph), -1, -1):
        if any(independent(graph, state) for state in choices(vertices, size)):
            return size
    raise AssertionError("the empty set is independent")


def domination_number(graph: Graph) -> int:
    vertices = range(len(graph))
    for size in range(len(graph) + 1):
        if any(dominates(graph, state) for state in choices(vertices, size)):
            return size
    raise AssertionError("the full vertex set dominates")


def maximum_independent_states(graph: Graph, size: int) -> tuple[State, ...]:
    return tuple(
        state
        for state in choices(range(len(graph)), size)
        if independent(graph, state)
    )


def greatest_one_guard_family(graph: Graph, size: int) -> frozenset[State]:
    """Literal greatest-fixed-point deletion from dominating size-k states."""

    vertices = frozenset(range(len(graph)))
    family = frozenset(
        state
        for state in choices(range(len(graph)), size)
        if dominates(graph, state)
    )
    while True:
        retained: set[State] = set()
        for state in family:
            closed = True
            for attack in vertices - state:
                has_response = False
                for guard in state & graph[attack]:
                    successor = state - {guard} | {attack}
                    if successor in family:
                        has_response = True
                        break
                if not has_response:
                    closed = False
                    break
            if closed:
                retained.add(state)
        next_family = frozenset(retained)
        if next_family == family:
            return family
        family = next_family


def static_response_list(graph: Graph, reference: State, target: int) -> frozenset[int]:
    if target in reference:
        raise ValueError("response-list target must be unoccupied")
    return frozenset(
        guard
        for guard in reference & graph[target]
        if dominates(graph, reference - {guard} | {target})
    )


def family_response_list(
    graph: Graph, family: frozenset[State], reference: State, target: int
) -> frozenset[int]:
    if target in reference:
        raise ValueError("response-list target must be unoccupied")
    return frozenset(
        guard
        for guard in reference & graph[target]
        if reference - {guard} | {target} in family
    )


def has_perfect_matching(
    left: State,
    right: State,
    edge: Callable[[int, int], bool],
) -> bool:
    """Small deterministic augmenting-path matcher."""

    if len(left) != len(right):
        return False
    matched_right: dict[int, int] = {}

    def augment(u: int, seen: set[int]) -> bool:
        for x in sorted(right):
            if x in seen or not edge(u, x):
                continue
            seen.add(x)
            if x not in matched_right or augment(matched_right[x], seen):
                matched_right[x] = u
                return True
        return False

    return all(augment(u, set()) for u in sorted(left))


def powerset(state: State) -> tuple[State, ...]:
    ordered = sorted(state)
    return tuple(
        frozenset(part)
        for size in range(len(ordered) + 1)
        for part in itertools.combinations(ordered, size)
    )


def base_ordering(
    graph: Graph,
    family: frozenset[State],
    first: State,
    second: State,
    require_family: bool,
    require_response_edges: bool,
) -> tuple[tuple[int, int], ...] | None:
    left = tuple(sorted(first - second))
    right = tuple(sorted(second - first))
    if len(left) != len(right):
        raise AssertionError("equal-size states have balanced symmetric difference")

    for permuted_right in itertools.permutations(right):
        pairing = dict(zip(left, permuted_right, strict=True))
        if require_response_edges and any(
            pairing[u] not in graph[u] for u in left
        ):
            continue
        valid = True
        for removed in powerset(frozenset(left)):
            mixed = first - removed | {pairing[u] for u in removed}
            if require_family:
                if mixed not in family:
                    valid = False
                    break
            elif not dominates(graph, mixed):
                valid = False
                break
        if valid:
            return tuple((u, pairing[u]) for u in left)
    return None


def ordered(state: State) -> list[int]:
    return sorted(state)


def state_pair_witness(
    record: str,
    first: State,
    second: State,
    **extra: object,
) -> dict[str, object]:
    witness: dict[str, object] = {
        "graph6": record,
        "S": ordered(first),
        "T": ordered(second),
        "S_minus_T": ordered(first - second),
        "T_minus_S": ordered(second - first),
    }
    witness.update(extra)
    return witness


def response_matrix(
    left: State,
    right: State,
    list_function: ListFunction,
    reference: State,
) -> dict[str, list[int]]:
    return {
        str(target): ordered(list_function(reference, target) & left)
        for target in sorted(right)
    }


def state_key(state: State) -> tuple[int, ...]:
    return tuple(sorted(state))


def exchange_transport(
    labels: dict[int, int], first: State, second: State
) -> dict[int, int]:
    removed_set = first - second
    inserted_set = second - first
    if len(removed_set) != 1 or len(inserted_set) != 1:
        raise ValueError("exchange transport requires a one-vertex exchange")
    removed = next(iter(removed_set))
    inserted = next(iter(inserted_set))
    transported = {vertex: labels[vertex] for vertex in first & second}
    transported[inserted] = labels[removed]
    return transported


def check_exchange_structure(
    record: str,
    graph: Graph,
    references: tuple[State, ...],
    properties: dict[str, dict[str, object]],
) -> tuple[int, bool, bool]:
    """Check connectivity and path-independence of token-label transport."""

    ordered_references = tuple(sorted(references, key=state_key))
    neighbors: dict[State, list[State]] = {
        state: [] for state in ordered_references
    }
    for first, second in itertools.combinations(ordered_references, 2):
        if len(first - second) == len(second - first) == 1:
            neighbors[first].append(second)
            neighbors[second].append(first)
    for state in ordered_references:
        neighbors[state].sort(key=state_key)

    components: list[list[State]] = []
    unseen = set(ordered_references)
    while unseen:
        root = min(unseen, key=state_key)
        component: list[State] = []
        queue = [root]
        unseen.remove(root)
        for state in queue:
            component.append(state)
            for adjacent in neighbors[state]:
                if adjacent in unseen:
                    unseen.remove(adjacent)
                    queue.append(adjacent)
        components.append(component)

    connectivity_witness = {
        "graph6": record,
        "n": len(graph),
        "k": len(ordered_references[0]),
        "maximum_independent_states": [ordered(state) for state in ordered_references],
        "exchange_components": [
            [ordered(state) for state in component] for component in components
        ],
    }
    connected = len(components) == 1
    register(
        properties,
        "maximum_independent_exchange_graph_connected",
        connected,
        connectivity_witness,
    )

    holonomy_witness: dict[str, object] | None = None
    for component in components:
        root = component[0]
        labelings: dict[State, dict[int, int]] = {
            root: {vertex: vertex for vertex in root}
        }
        paths: dict[State, list[State]] = {root: [root]}
        queue = [root]
        cursor = 0
        while cursor < len(queue) and holonomy_witness is None:
            state = queue[cursor]
            cursor += 1
            for adjacent in neighbors[state]:
                if adjacent not in component:
                    continue
                proposed = exchange_transport(labelings[state], state, adjacent)
                proposed_path = paths[state] + [adjacent]
                if adjacent not in labelings:
                    labelings[adjacent] = proposed
                    paths[adjacent] = proposed_path
                    queue.append(adjacent)
                    continue
                if labelings[adjacent] != proposed:
                    established = labelings[adjacent]
                    permutation = {
                        str(established[vertex]): proposed[vertex]
                        for vertex in sorted(adjacent)
                    }
                    holonomy_witness = {
                        "graph6": record,
                        "n": len(graph),
                        "k": len(root),
                        "root_state": ordered(root),
                        "meeting_state": ordered(adjacent),
                        "established_path": [
                            ordered(path_state) for path_state in paths[adjacent]
                        ],
                        "alternative_path": [
                            ordered(path_state) for path_state in proposed_path
                        ],
                        "established_vertex_to_root_label": {
                            str(vertex): established[vertex]
                            for vertex in sorted(adjacent)
                        },
                        "alternative_vertex_to_root_label": {
                            str(vertex): proposed[vertex]
                            for vertex in sorted(adjacent)
                        },
                        "induced_root_label_permutation": permutation,
                    }
                    break
        if holonomy_witness is not None:
            break

    trivial_holonomy = holonomy_witness is None
    register(
        properties,
        "exchange_transport_has_trivial_holonomy",
        trivial_holonomy,
        holonomy_witness or connectivity_witness,
    )
    return len(components), connected, trivial_holonomy


def common_open_complement_neighborhood(graph: Graph, ridge: State) -> State:
    """Return N_H(ridge)=intersection_{v in ridge} N_H(v), H=bar(G)."""

    vertices = range(len(graph))
    return frozenset(
        candidate
        for candidate in vertices
        if all(
            candidate != ridge_vertex
            and candidate not in graph[ridge_vertex]
            for ridge_vertex in ridge
        )
    )


def check_co_state_links(
    graph: Graph,
    record: str,
    family: frozenset[State],
    properties: dict[str, dict[str, object]],
) -> tuple[int, int]:
    ridge_obligations = 0
    forced_attack_obligations = 0
    for state in sorted(family, key=state_key):
        for distinguished in sorted(state):
            ridge_obligations += 1
            ridge = state - {distinguished}
            common = common_open_complement_neighborhood(graph, ridge)
            nonedge_pair: tuple[int, int] | None = None
            for first, second in itertools.combinations(sorted(common), 2):
                if second not in graph[first]:
                    nonedge_pair = (first, second)
                    break
            base = {
                "graph6": record,
                "n": len(graph),
                "k": len(state),
                "D": ordered(state),
                "R": ordered(ridge),
                "u": distinguished,
                "common_H_neighborhood_C": ordered(common),
            }
            register(
                properties,
                "co_state_common_H_neighborhood_is_H_edgeless",
                nonedge_pair is None,
                {
                    **base,
                    "H_edge_inside_C": (
                        list(nonedge_pair) if nonedge_pair is not None else None
                    ),
                },
            )

            for attack in sorted(common - state):
                forced_attack_obligations += 1
                responders = state & graph[attack]
                successor = ridge | {attack}
                holds = (
                    responders == frozenset({distinguished})
                    and successor in family
                )
                register(
                    properties,
                    "co_state_unique_forced_response",
                    holds,
                    {
                        **base,
                        "attack": attack,
                        "adjacent_guards": ordered(responders),
                        "expected_successor": ordered(successor),
                        "successor_in_family": successor in family,
                    },
                )
    return ridge_obligations, forced_attack_obligations


def family_retained_successors(
    graph: Graph,
    family: frozenset[State],
    state: State,
    attack: int,
) -> frozenset[State]:
    if attack in state:
        raise AssertionError("tight-Hall audit attempted an occupied attack")
    return frozenset(
        state - {guard} | {attack}
        for guard in state & graph[attack]
        if state - {guard} | {attack} in family
    )


def check_tight_hall_states(
    graph: Graph,
    record: str,
    family: frozenset[State],
    references: tuple[State, ...],
    properties: dict[str, dict[str, object]],
) -> tuple[int, int, int]:
    tight_sets = 0
    attack_orderings = 0
    retained_transition_edges = 0
    vertices = frozenset(range(len(graph)))

    for reference in references:
        outside = vertices - reference
        for size in range(1, len(reference) + 1):
            for attacked in choices(sorted(outside), size):
                if not independent(graph, attacked):
                    continue
                lists = {
                    target: family_response_list(
                        graph, family, reference, target
                    )
                    for target in attacked
                }
                union = frozenset().union(*lists.values())
                if len(union) != len(attacked):
                    continue
                tight_sets += 1
                expected = reference - union | attacked
                base = {
                    "graph6": record,
                    "n": len(graph),
                    "k": len(reference),
                    "S": ordered(reference),
                    "X": ordered(attacked),
                    "response_lists": {
                        str(target): ordered(lists[target])
                        for target in sorted(attacked)
                    },
                    "U": ordered(union),
                    "expected_endpoint": ordered(expected),
                }
                register(
                    properties,
                    "tight_Hall_endpoint_membership",
                    expected in family,
                    {
                        **base,
                        "expected_endpoint_in_family": expected in family,
                    },
                )

                for attack_order in itertools.permutations(sorted(attacked)):
                    attack_orderings += 1
                    current_states = frozenset({reference})
                    layer_sizes = [1]
                    for attack in attack_order:
                        next_states: set[State] = set()
                        for state in current_states:
                            successors = family_retained_successors(
                                graph, family, state, attack
                            )
                            retained_transition_edges += len(successors)
                            next_states.update(successors)
                        current_states = frozenset(next_states)
                        layer_sizes.append(len(current_states))
                    holds = current_states == frozenset({expected})
                    register(
                        properties,
                        "tight_Hall_all_orders_force_endpoint",
                        holds,
                        {
                            **base,
                            "attack_order": list(attack_order),
                            "reachable_family_endpoint_states": [
                                ordered(state)
                                for state in sorted(current_states, key=state_key)
                            ],
                            "reachable_layer_sizes": layer_sizes,
                        },
                    )
    return tight_sets, attack_orderings, retained_transition_edges


def fresh_property_table() -> dict[str, dict[str, object]]:
    return {
        name: {
            "description": description,
            "tests": 0,
            "violations": 0,
            "first_counterexample": None,
        }
        for name, description in PROPERTY_DESCRIPTIONS.items()
    }


def register(
    table: dict[str, dict[str, object]],
    name: str,
    holds: bool,
    witness: dict[str, object],
) -> None:
    entry = table[name]
    entry["tests"] = int(entry["tests"]) + 1
    if not holds:
        entry["violations"] = int(entry["violations"]) + 1
        if entry["first_counterexample"] is None:
            entry["first_counterexample"] = witness


def check_state_pair(
    graph: Graph,
    record: str,
    family: frozenset[State],
    first: State,
    second: State,
    properties: dict[str, dict[str, object]],
) -> tuple[int, int]:
    left = first - second
    right = second - first

    static_lists = lambda reference, target: static_response_list(  # noqa: E731
        graph, reference, target
    )
    family_lists = lambda reference, target: family_response_list(  # noqa: E731
        graph, family, reference, target
    )

    for label, lists in (("static", static_lists), ("family", family_lists)):
        matrix_forward = response_matrix(left, right, lists, first)
        matrix_reverse = response_matrix(right, left, lists, second)
        base_witness = state_pair_witness(
            record,
            first,
            second,
            n=len(graph),
            k=len(first),
            forward_response_lists=matrix_forward,
            reverse_response_lists=matrix_reverse,
        )

        directed_forward = has_perfect_matching(
            left, right, lambda u, x: u in lists(first, x)
        )
        directed_reverse = has_perfect_matching(
            right, left, lambda x, u: x in lists(second, u)
        )
        register(
            properties,
            f"control_directed_{label}_matching",
            directed_forward and directed_reverse,
            {
                **base_witness,
                "forward_has_perfect_matching": directed_forward,
                "reverse_has_perfect_matching": directed_reverse,
            },
        )

        mismatch: dict[str, object] | None = None
        for u in sorted(left):
            for x in sorted(right):
                forward = u in lists(first, x)
                reverse = x in lists(second, u)
                if forward != reverse:
                    mismatch = {
                        **base_witness,
                        "u": u,
                        "x": x,
                        "u_in_S_list_of_x": forward,
                        "x_in_T_list_of_u": reverse,
                    }
                    break
            if mismatch is not None:
                break
        register(
            properties,
            f"pairwise_{label}_reciprocity",
            mismatch is None,
            mismatch or base_witness,
        )

        mutual_matching = has_perfect_matching(
            left,
            right,
            lambda u, x: (
                u in lists(first, x) and x in lists(second, u)
            ),
        )
        register(
            properties,
            f"mutual_{label}_matching",
            mutual_matching,
            base_witness,
        )

        state_ordering = base_ordering(
            graph,
            family,
            first,
            second,
            require_family=(label == "family"),
            require_response_edges=False,
        )
        register(
            properties,
            f"{label}_state_base_orderability",
            state_ordering is not None,
            base_witness,
        )

        response_ordering = base_ordering(
            graph,
            family,
            first,
            second,
            require_family=(label == "family"),
            require_response_edges=True,
        )
        register(
            properties,
            f"{label}_response_base_orderability",
            response_ordering is not None,
            base_witness,
        )

    adjacent_pairs = 0
    adjacent_triples = 0
    if len(left) == len(right) == 1:
        removed = next(iter(left))
        inserted = next(iter(right))
        if inserted not in graph[removed]:
            raise AssertionError(
                "two maximum independent sets differing once must exchange "
                "adjacent vertices, or their union is larger independent"
            )
        adjacent_pairs = 1
        common = first & second
        outside = sorted(set(range(len(graph))) - first - second)
        for target in outside:
            adjacent_triples += 1
            for label, lists in (("static", static_lists), ("family", family_lists)):
                first_list = lists(first, target)
                second_list = lists(second, target)
                transported = (
                    first_list - {removed}
                    | ({inserted} if removed in first_list else set())
                )
                detail = state_pair_witness(
                    record,
                    first,
                    second,
                    n=len(graph),
                    k=len(first),
                    y=target,
                    exchanged_pair=[removed, inserted],
                    S_list=ordered(first_list),
                    T_list=ordered(second_list),
                    transported_S_list=ordered(frozenset(transported)),
                )
                common_stable = (first_list & common) == (second_list & common)
                exchanged_reciprocal = (
                    (removed in first_list) == (inserted in second_list)
                )
                register(
                    properties,
                    f"adjacent_{label}_common_color_stability",
                    common_stable,
                    detail,
                )
                register(
                    properties,
                    f"adjacent_{label}_exchanged_color_reciprocity",
                    exchanged_reciprocal,
                    detail,
                )
                register(
                    properties,
                    f"adjacent_{label}_transport_equality",
                    frozenset(transported) == second_list,
                    detail,
                )
                register(
                    properties,
                    f"adjacent_{label}_list_size_equality",
                    len(first_list) == len(second_list),
                    detail,
                )
    return adjacent_pairs, adjacent_triples


def self_test() -> None:
    # C4, labeled cyclically.
    c4: Graph = (
        frozenset({1, 3}),
        frozenset({0, 2}),
        frozenset({1, 3}),
        frozenset({0, 2}),
    )
    assert independence_number(c4) == 2
    assert domination_number(c4) == 2
    c4_family = greatest_one_guard_family(c4, 2)
    assert c4_family
    c4_references = maximum_independent_states(c4, 2)
    assert c4_references == (
        frozenset({0, 2}),
        frozenset({1, 3}),
    )
    c4_properties = fresh_property_table()
    c4_components, c4_connected, c4_trivial_holonomy = check_exchange_structure(
        "manual-C4", c4, c4_references, c4_properties
    )
    assert c4_components == 2
    assert not c4_connected
    assert c4_trivial_holonomy
    c4_reference = frozenset({0, 2})
    c4_target = 1
    assert family_response_list(
        c4, c4_family, c4_reference, c4_target
    ) == frozenset({0, 2})
    c4_branching = family_retained_successors(
        c4, c4_family, c4_reference, c4_target
    )
    assert c4_branching == frozenset(
        {frozenset({0, 1}), frozenset({1, 2})}
    )
    # Here |union L|=2>|X|=1 and the endpoint is not forced, checking that
    # tightness is an essential hypothesis rather than decorative wording.

    # P3 catches the replacement of full eternal closure by domination:
    # one guard is not eternal even though its center dominates.
    p3: Graph = (
        frozenset({1}),
        frozenset({0, 2}),
        frozenset({1}),
    )
    assert domination_number(p3) == 1
    assert independence_number(p3) == 2
    assert not greatest_one_guard_family(p3, 1)
    assert greatest_one_guard_family(p3, 2)
    p3_center = frozenset({1})
    assert dominates(p3, p3_center)
    p3_common = common_open_complement_neighborhood(p3, frozenset())
    assert p3_common == frozenset({0, 1, 2})
    assert 2 not in p3[0]
    # Thus the co-state clique conclusion fails for the merely dominating
    # state {1}; eternal-family membership is essential.

    # C5's maximum-independent exchange cycle swaps the two transported
    # labels. It is deliberately not an equality graph
    # (gamma^infinity(C5)=3>alpha(C5)=2), and verifies that the holonomy test
    # detects the obstruction rather than reporting zero by construction.
    c5: Graph = tuple(
        frozenset({(vertex - 1) % 5, (vertex + 1) % 5})
        for vertex in range(5)
    )
    c5_references = maximum_independent_states(c5, 2)
    c5_properties = fresh_property_table()
    c5_components, c5_connected, c5_trivial_holonomy = check_exchange_structure(
        "manual-C5", c5, c5_references, c5_properties
    )
    assert c5_components == 1
    assert c5_connected
    assert not c5_trivial_holonomy

    # Direct matcher check.
    assert has_perfect_matching(
        frozenset({0, 1}),
        frozenset({2, 3}),
        lambda u, x: (u, x) in {(0, 2), (1, 3)},
    )
    assert not has_perfect_matching(
        frozenset({0, 1}),
        frozenset({2, 3}),
        lambda u, x: x == 2,
    )


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def max_rss_bytes() -> int:
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Darwin reports bytes; Linux reports KiB.
    return int(raw if sys.platform == "darwin" else raw * 1024)


def finalize_properties(properties: dict[str, dict[str, object]]) -> None:
    for name, entry in properties.items():
        entry["finite_outcome"] = (
            "ZERO_VIOLATIONS_IN_SCOPE"
            if int(entry["violations"]) == 0
            else "REFUTED_IN_SCOPE"
        )
        entry["mathematical_status"] = (
            "PROVED"
            if name in ANALYTICALLY_PROVED_PROPERTIES
            else "FINITE_TEST_ONLY"
        )


def result_payload(
    *,
    args: argparse.Namespace,
    properties: dict[str, dict[str, object]],
    orders: list[dict[str, object]],
    totals: dict[str, int],
    status: str,
    stop_reason: str,
    start_time: float,
) -> dict[str, object]:
    return {
        "schema": "cross-state-response-probe-v1",
        "status": status,
        "stop_reason": stop_reason,
        "scope": {
            "graph_universe": "connected unlabeled graphs from pinned nauty geng -cq",
            "minimum_order": args.min_order,
            "requested_maximum_order": args.max_order,
            "last_completed_order": (
                next(
                    (
                        int(order_record["order"])
                        for order_record in reversed(orders)
                        if order_record["complete"]
                    ),
                    None,
                )
            ),
            "wall_clock_gate_seconds": args.max_seconds,
            "equality_filter": (
                "gamma(G)=alpha(G)=k and greatest literal one-guard "
                "k-family nonempty"
            ),
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one graph edge",
            "solver_use": "none",
            "orders_13_or_14": False,
        },
        "implementation": {
            "script": str(Path(__file__).relative_to(CAMPAIGN)),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "geng": str(args.geng.relative_to(CAMPAIGN)),
            "geng_sha256": hashlib.sha256(args.geng.read_bytes()).hexdigest(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "representation": "ordinary Python set/frozenset",
            "independent_of_campaign_evaluator_core": True,
        },
        "totals": totals,
        "orders": orders,
        "properties": properties,
        "analytic_deductions": ANALYTIC_DEDUCTIONS,
        "resource_usage": {
            "elapsed_seconds": round(time.monotonic() - start_time, 6),
            "maximum_resident_set_bytes": max_rss_bytes(),
        },
        "interpretation_guardrails": [
            "Every zero-violation outcome is finite evidence only, not a theorem.",
            "A refuted candidate is not used as a reduction.",
            "The directed family matching is an implementation control for the "
            "already-proved Hall consequence, not a new result.",
            "Only greatest-family lists were computed; no claim about a "
            "smaller chosen eternal family follows unless logically inherited.",
        ],
    }


def run(args: argparse.Namespace) -> dict[str, object]:
    self_test()
    if not args.geng.is_file():
        raise FileNotFoundError(args.geng)
    start = time.monotonic()
    deadline = start + args.max_seconds
    properties = fresh_property_table()
    orders: list[dict[str, object]] = []
    totals = {
        "connected_graphs": 0,
        "gamma_equals_alpha_graphs": 0,
        "equality_graphs": 0,
        "maximum_independent_states": 0,
        "maximum_independent_state_pairs": 0,
        "adjacent_maximum_independent_state_pairs": 0,
        "adjacent_pair_outside_vertex_triples": 0,
        "maximum_independent_exchange_components": 0,
        "graphs_with_disconnected_maximum_independent_exchange_graph": 0,
        "graphs_with_nontrivial_exchange_transport_holonomy": 0,
        "greatest_family_states": 0,
        "co_state_ridge_obligations": 0,
        "co_state_forced_attack_obligations": 0,
        "tight_Hall_sets": 0,
        "tight_Hall_attack_orderings": 0,
        "tight_Hall_retained_transition_edges": 0,
    }
    status = "COMPLETE"
    stop_reason = "completed requested finite scope"

    for order in range(args.min_order, args.max_order + 1):
        properties_before_order = copy.deepcopy(properties)
        records = connected_graph6_records(args.geng, order)
        stream = hashlib.sha256()
        order_counts = {
            "order": order,
            "complete": False,
            "connected_graphs": 0,
            "gamma_equals_alpha_graphs": 0,
            "equality_graphs": 0,
            "maximum_independent_states": 0,
            "maximum_independent_state_pairs": 0,
            "adjacent_maximum_independent_state_pairs": 0,
            "adjacent_pair_outside_vertex_triples": 0,
            "maximum_independent_exchange_components": 0,
            "graphs_with_disconnected_maximum_independent_exchange_graph": 0,
            "graphs_with_nontrivial_exchange_transport_holonomy": 0,
            "greatest_family_states": 0,
            "co_state_ridge_obligations": 0,
            "co_state_forced_attack_obligations": 0,
            "tight_Hall_sets": 0,
            "tight_Hall_attack_orderings": 0,
            "tight_Hall_retained_transition_edges": 0,
            "graph6_stream_sha256": None,
        }
        timed_out = False

        for record in records:
            if time.monotonic() >= deadline:
                timed_out = True
                break
            stream.update(record.encode("ascii") + b"\n")
            graph = decode_graph6(record)
            if len(graph) != order:
                raise AssertionError("graph6 order mismatch")
            order_counts["connected_graphs"] += 1

            alpha = independence_number(graph)
            gamma = domination_number(graph)
            if gamma != alpha:
                continue
            order_counts["gamma_equals_alpha_graphs"] += 1
            family = greatest_one_guard_family(graph, alpha)
            if not family:
                continue
            order_counts["equality_graphs"] += 1

            references = maximum_independent_states(graph, alpha)
            if not set(references).issubset(family):
                raise AssertionError(
                    "maximum independent state missing from nonempty "
                    "greatest family; model or chain implementation is wrong"
                )
            order_counts["maximum_independent_states"] += len(references)
            order_counts["greatest_family_states"] += len(family)
            ridge_count, forced_attack_count = check_co_state_links(
                graph, record, family, properties
            )
            order_counts["co_state_ridge_obligations"] += ridge_count
            order_counts[
                "co_state_forced_attack_obligations"
            ] += forced_attack_count
            (
                tight_set_count,
                tight_order_count,
                tight_transition_count,
            ) = check_tight_hall_states(
                graph, record, family, references, properties
            )
            order_counts["tight_Hall_sets"] += tight_set_count
            order_counts[
                "tight_Hall_attack_orderings"
            ] += tight_order_count
            order_counts[
                "tight_Hall_retained_transition_edges"
            ] += tight_transition_count
            component_count, exchange_connected, trivial_holonomy = (
                check_exchange_structure(record, graph, references, properties)
            )
            order_counts[
                "maximum_independent_exchange_components"
            ] += component_count
            if not exchange_connected:
                order_counts[
                    "graphs_with_disconnected_maximum_independent_exchange_graph"
                ] += 1
            if not trivial_holonomy:
                order_counts[
                    "graphs_with_nontrivial_exchange_transport_holonomy"
                ] += 1

            for first, second in itertools.combinations(references, 2):
                order_counts["maximum_independent_state_pairs"] += 1
                adjacent_pairs, adjacent_triples = check_state_pair(
                    graph,
                    record,
                    family,
                    first,
                    second,
                    properties,
                )
                order_counts[
                    "adjacent_maximum_independent_state_pairs"
                ] += adjacent_pairs
                order_counts[
                    "adjacent_pair_outside_vertex_triples"
                ] += adjacent_triples

        if timed_out:
            # A partial order has no coverage hash and is not part of the
            # certified scope. Restore property counters to the preceding
            # atomic checkpoint rather than silently mixing partial evidence
            # into completed-order claims.
            properties = properties_before_order
            status = "STOPPED_AT_WALL_CLOCK_GATE"
            stop_reason = (
                f"strict {args.max_seconds:g}-second wall-clock gate reached "
                f"during order {order}; partial order is not counted in totals"
            )
            order_counts["partial_connected_graphs_seen"] = order_counts[
                "connected_graphs"
            ]
            order_counts["connected_graphs"] = 0
            order_counts["gamma_equals_alpha_graphs"] = 0
            order_counts["equality_graphs"] = 0
            order_counts["maximum_independent_states"] = 0
            order_counts["maximum_independent_state_pairs"] = 0
            order_counts["adjacent_maximum_independent_state_pairs"] = 0
            order_counts["adjacent_pair_outside_vertex_triples"] = 0
            order_counts["maximum_independent_exchange_components"] = 0
            order_counts[
                "graphs_with_disconnected_maximum_independent_exchange_graph"
            ] = 0
            order_counts[
                "graphs_with_nontrivial_exchange_transport_holonomy"
            ] = 0
            order_counts["greatest_family_states"] = 0
            order_counts["co_state_ridge_obligations"] = 0
            order_counts["co_state_forced_attack_obligations"] = 0
            order_counts["tight_Hall_sets"] = 0
            order_counts["tight_Hall_attack_orderings"] = 0
            order_counts["tight_Hall_retained_transition_edges"] = 0
            orders.append(order_counts)
            break

        order_counts["complete"] = True
        order_counts["graph6_stream_sha256"] = stream.hexdigest()
        orders.append(order_counts)
        for key in totals:
            totals[key] += int(order_counts[key])

        checkpoint = result_payload(
            args=args,
            properties=properties,
            orders=orders,
            totals=totals,
            status="CHECKPOINT",
            stop_reason=f"completed and checkpointed through order {order}",
            start_time=start,
        )
        atomic_write(args.output, json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")

    finalize_properties(properties)
    payload = result_payload(
        args=args,
        properties=properties,
        orders=orders,
        totals=totals,
        status=status,
        stop_reason=stop_reason,
        start_time=start,
    )
    atomic_write(args.output, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def write_log(args: argparse.Namespace, payload: dict[str, object]) -> None:
    output_sha = hashlib.sha256(args.output.read_bytes()).hexdigest()
    properties = payload["properties"]
    refuted = [
        name
        for name, entry in properties.items()
        if int(entry["violations"]) > 0
    ]
    survived = [
        name
        for name, entry in properties.items()
        if int(entry["violations"]) == 0
    ]
    proved = [
        name
        for name, entry in properties.items()
        if entry["mathematical_status"] == "PROVED"
    ]
    lines = [
        "Cross-state response probe",
        "==========================",
        "",
        f"status: {payload['status']}",
        f"stop_reason: {payload['stop_reason']}",
        (
            "command: "
            f"{Path(__file__).relative_to(CAMPAIGN)} "
            f"--min-order {args.min_order} --max-order {args.max_order} "
            f"--max-seconds {args.max_seconds:g}"
        ),
        f"result_sha256: {output_sha}",
        f"script_sha256: {payload['implementation']['script_sha256']}",
        f"geng_sha256: {payload['implementation']['geng_sha256']}",
        "",
        "Completed-order totals:",
        json.dumps(payload["totals"], sort_keys=True),
        "",
        "Refuted candidates:",
        *(f"- {name}" for name in sorted(refuted)),
        "",
        "Analytically proved (proofs embedded in JSON):",
        *(f"- {name}" for name in sorted(proved)),
        "",
        "Zero-violation finite observations:",
        *(
            f"- {name}"
            for name in sorted(set(survived) - set(proved))
        ),
        "",
        "Guardrail: zero violations in this finite scope is not a theorem.",
        "Checkpoint policy: the JSON file was atomically replaced after every "
        "completed order.",
        "Stop policy: no graph was begun after the wall-clock gate.",
        "",
    ]
    atomic_write(args.log, "\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-order", type=int, default=1)
    parser.add_argument("--max-order", type=int, default=8)
    parser.add_argument("--max-seconds", type=float, default=60.0)
    parser.add_argument("--geng", type=Path, default=DEFAULT_GENG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    args = parser.parse_args()
    args.geng = args.geng.resolve()
    args.output = args.output.resolve()
    args.log = args.log.resolve()
    if args.min_order < 1 or args.max_order < args.min_order:
        parser.error("require 1 <= min-order <= max-order")
    if args.max_order > 8:
        parser.error("this bounded probe intentionally refuses orders above 8")
    if args.max_seconds <= 0:
        parser.error("max-seconds must be positive")
    return args


def main() -> int:
    args = parse_args()
    payload = run(args)
    write_log(args, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
