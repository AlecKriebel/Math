#!/usr/bin/env python3
"""Exact regression for a four-leaf graft of the edgewise-CT K2P collision.

The old leaf 1 is replaced by a tree vertex h1 with new leaves 1 and 4.
Both new pendant edges carry K=(1,1/2,1/2,1/2).  The verifier reconstructs
the literal grafted network and comparison quartet, checks every Fourier
coordinate, and independently checks every ordinary-state probability by
displayed-tree pruning, quartet-tree pruning, Fourier inversion, and Markov
kernel extension.  Only the Python standard library is used.

This finite regression certifies the stated n=4 graft.  Iteration to arbitrary
n is a theorem-level consequence of the shared-kernel graft identity, not a
claim made by this script.
"""
from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from typing import Dict, Iterable, Mapping, Sequence, Tuple

# Importing the sibling verifier supplies the exact number field and binds this
# regression to the canonical continuous-time K2P certificate.  Avoid leaving
# bytecode caches when the focused checker is replayed directly.
sys.dont_write_bytecode = True
import verify_k2p_extended as v


def alg_sum(values: Iterable[v.Alg]) -> v.Alg:
    return sum(values, v.Alg.zero())


GRAFT = v.network_vectors["K"]
LEAF_POS4 = {"1": 0, "2": 1, "3": 2, "4": 3}

NODES4 = dict(v.NODES)
NODES4.update({"h1": "tree", "4": "leaf"})

ARCS4 = dict(v.ARCS)
del ARCS4["rho_1"]
ARCS4.update(
    {
        "rho_h1": ("rho", "h1", "K"),
        "h1_1": ("h1", "1", "K"),
        "h1_4": ("h1", "4", "K"),
    }
)

TREE_NODES4 = {"t": "tree", "h1": "tree", "1": "leaf", "2": "leaf", "3": "leaf", "4": "leaf"}
TREE_ARCS4 = {
    "t_h1": ("t", "h1", "alpha"),
    "t_2": ("t", "2", "beta"),
    "t_3": ("t", "3", "gamma"),
    "h1_1": ("h1", "1", "K"),
    "h1_4": ("h1", "4", "K"),
}


def undirected_reachable(
    start: str,
    nodes: Iterable[str],
    edges: Iterable[frozenset[str]],
) -> set[str]:
    node_set = set(nodes)
    adjacency = {node: set() for node in node_set}
    for edge in edges:
        v.require(len(edge) == 2 and edge <= node_set, "valid undirected edge")
        left, right = tuple(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbor in adjacency[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen


def undirected_connected(nodes: Iterable[str], edges: Iterable[frozenset[str]]) -> bool:
    node_set = set(nodes)
    return not node_set or undirected_reachable(next(iter(node_set)), node_set, edges) == node_set


def retained_edges4(choice2: int, choice3: int) -> Tuple[str, ...]:
    v.require(choice2 in (0, 1) and choice3 in (0, 1), "binary reticulation choices")
    retained = list(ARCS4)
    for reticulation, choice in (("r2", choice2), ("r3", choice3)):
        incoming = [row["edge_id"] for row in v.RETICS[reticulation]]
        v.require(len(incoming) == 2, f"two incoming arcs at {reticulation}")
        retained.remove(incoming[1 - choice])
    v.require(len(retained) == len(NODES4) - 1 == 10,
              "each four-leaf switching has ten retained arcs")
    return tuple(retained)


def directed_structure(
    nodes: Mapping[str, str],
    arcs: Mapping[str, Tuple[str, str, str]],
    retained: Sequence[str],
) -> Tuple[Dict[str, list[Tuple[str, str]]], Tuple[str, ...]]:
    children: Dict[str, list[Tuple[str, str]]] = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}
    for edge_id in retained:
        v.require(edge_id in arcs, f"known retained edge {edge_id}")
        parent, child, _ = arcs[edge_id]
        v.require(parent in nodes and child in nodes, f"known endpoints on {edge_id}")
        children[parent].append((child, edge_id))
        indegree[child] += 1
    queue = [node for node in nodes if indegree[node] == 0]
    order: list[str] = []
    while queue:
        parent = queue.pop()
        order.append(parent)
        for child, _ in children[parent]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    v.require(len(order) == len(nodes), "retained graph is acyclic")
    return children, tuple(order)


def labelled_descendants(
    start: str,
    children: Mapping[str, Sequence[Tuple[str, str]]],
) -> frozenset[str]:
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for child, _ in children.get(node, ()):  # type: ignore[arg-type]
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return frozenset(leaf for leaf in LEAF_POS4 if leaf in seen)


def descendant_character(leaves: Iterable[str], labels: Sequence[int]) -> int:
    character = 0
    for leaf in leaves:
        character ^= labels[LEAF_POS4[leaf]]
    return character


def switch_weight(choice2: int, choice3: int) -> Fraction:
    weights2 = (v.MIXING["r2"], 1 - v.MIXING["r2"])
    weights3 = (v.MIXING["r3"], 1 - v.MIXING["r3"])
    return weights2[choice2] * weights3[choice3]


def network_fourier4_from_graph(labels: Tuple[int, int, int, int]) -> v.Alg:
    if labels[0] ^ labels[1] ^ labels[2] ^ labels[3]:
        return v.Alg.zero()
    total = v.Alg.zero()
    for choice2, choice3 in itertools.product((0, 1), repeat=2):
        retained = retained_edges4(choice2, choice3)
        children, _ = directed_structure(NODES4, ARCS4, retained)
        term = v.Alg.one()
        for edge_id in retained:
            _, child, vector_name = ARCS4[edge_id]
            leaves = labelled_descendants(child, children)
            character = descendant_character(leaves, labels)
            term = term * v.network_vectors[vector_name][character]
        total += term.scale(switch_weight(choice2, choice3))
    return total


def tree_fourier4_from_graph(labels: Tuple[int, int, int, int]) -> v.Alg:
    if labels[0] ^ labels[1] ^ labels[2] ^ labels[3]:
        return v.Alg.zero()
    children, _ = directed_structure(TREE_NODES4, TREE_ARCS4, tuple(TREE_ARCS4))
    vectors = {**v.tree_vectors, "K": GRAFT}
    term = v.Alg.one()
    for edge_id, (_, child, vector_name) in TREE_ARCS4.items():
        leaves = labelled_descendants(child, children)
        term = term * vectors[vector_name][descendant_character(leaves, labels)]
    return term


def graft_formula(q3, labels: Tuple[int, int, int, int]) -> v.Alg:
    a, b, c, d = labels
    return q3((a ^ d, b, c)) * GRAFT[a] * GRAFT[d]


def inverse_fourier4(
    coordinates: Mapping[Tuple[int, int, int, int], v.Alg],
    pattern: Tuple[int, int, int, int],
) -> v.Alg:
    total = v.Alg.zero()
    for labels in itertools.product(range(4), repeat=4):
        coefficient = 1
        for character, state in zip(labels, pattern):
            coefficient *= v.CHAR[character][state]
        total += coordinates[labels].scale(v.F(coefficient, 256))
    return total


def direct_display_probability4(
    pattern: Tuple[int, int, int, int],
    choice2: int,
    choice3: int,
) -> v.Alg:
    retained = retained_edges4(choice2, choice3)
    children, order = directed_structure(NODES4, ARCS4, retained)
    observed = {leaf: pattern[position] for leaf, position in LEAF_POS4.items()}
    likelihood: Dict[str, list[v.Alg]] = {}
    for node in reversed(order):
        if node in observed:
            likelihood[node] = [
                v.Alg.one() if state == observed[node] else v.Alg.zero()
                for state in range(4)
            ]
            continue
        values = [v.Alg.one() for _ in range(4)]
        for child, edge_id in children[node]:
            probabilities = v.transition_probs(v.network_vectors[ARCS4[edge_id][2]])
            contribution = []
            for parent_state in range(4):
                subtotal = v.Alg.zero()
                for child_state in range(4):
                    subtotal += probabilities[parent_state ^ child_state] * likelihood[child][child_state]
                contribution.append(subtotal)
            values = [left * right for left, right in zip(values, contribution)]
        likelihood[node] = values
    return alg_sum(likelihood["rho"]).scale(v.F(1, 4))


def direct_network_probability4(pattern: Tuple[int, int, int, int]) -> v.Alg:
    return alg_sum(
        direct_display_probability4(pattern, choice2, choice3).scale(
            switch_weight(choice2, choice3)
        )
        for choice2, choice3 in itertools.product((0, 1), repeat=2)
    )


def direct_tree_probability4(pattern: Tuple[int, int, int, int]) -> v.Alg:
    state1, state2, state3, state4 = pattern
    alpha = v.transition_probs(v.tree_vectors["alpha"])
    beta = v.transition_probs(v.tree_vectors["beta"])
    gamma = v.transition_probs(v.tree_vectors["gamma"])
    graft1 = v.transition_probs(GRAFT)
    graft4 = v.transition_probs(GRAFT)
    total = v.Alg.zero()
    for root_state in range(4):
        for cherry_state in range(4):
            total += (
                alpha[root_state ^ cherry_state]
                * beta[root_state ^ state2]
                * gamma[root_state ^ state3]
                * graft1[cherry_state ^ state1]
                * graft4[cherry_state ^ state4]
            )
    return total.scale(v.F(1, 4))


def direct_markov_extension(
    old_probabilities: Mapping[Tuple[int, int, int], v.Alg],
    pattern: Tuple[int, int, int, int],
) -> v.Alg:
    state1, state2, state3, state4 = pattern
    graft = v.transition_probs(GRAFT)
    return alg_sum(
        old_probabilities[(hidden, state2, state3)]
        * graft[hidden ^ state1]
        * graft[hidden ^ state4]
        for hidden in range(4)
    )


def verify_topology4() -> None:
    expected_nodes = {
        "rho": "root", "u": "tree", "p": "tree", "q": "tree",
        "r2": "reticulation", "r3": "reticulation", "h1": "tree",
        "1": "leaf", "2": "leaf", "3": "leaf", "4": "leaf",
    }
    expected_arcs = {
        "rho_h1": ("rho", "h1", "K"), "rho_u": ("rho", "u", "K"),
        "u_p": ("u", "p", "U"), "u_q": ("u", "q", "V"),
        "p_r2": ("p", "r2", "A"), "q_r2": ("q", "r2", "B"),
        "p_r3": ("p", "r3", "A"), "q_r3": ("q", "r3", "B"),
        "r2_2": ("r2", "2", "K"), "r3_3": ("r3", "3", "K"),
        "h1_1": ("h1", "1", "K"), "h1_4": ("h1", "4", "K"),
    }
    v.require(NODES4 == expected_nodes, "exact four-leaf vertex/type map")
    v.require(ARCS4 == expected_arcs, "exact four-leaf arc/vector map")

    indegree = {node: 0 for node in NODES4}
    outdegree = {node: 0 for node in NODES4}
    for parent, child, _ in ARCS4.values():
        indegree[child] += 1
        outdegree[parent] += 1
    v.require((indegree["rho"], outdegree["rho"]) == (0, 2), "four-leaf root degree")
    for node in ("u", "p", "q", "h1"):
        v.require((indegree[node], outdegree[node]) == (1, 2), f"four-leaf tree vertex {node}")
    for node in ("r2", "r3"):
        v.require((indegree[node], outdegree[node]) == (2, 1), f"four-leaf reticulation {node}")
    for node in ("1", "2", "3", "4"):
        v.require((indegree[node], outdegree[node]) == (1, 0), f"four-leaf leaf {node}")
    _, full_order = directed_structure(NODES4, ARCS4, tuple(ARCS4))
    v.require(full_order[0] == "rho", "unique four-leaf root")

    for choices in itertools.product((0, 1), repeat=2):
        retained = retained_edges4(*choices)
        children, order = directed_structure(NODES4, ARCS4, retained)
        v.require(order[0] == "rho", f"displayed root for choices {choices}")
        reachable = {"rho"}
        stack = ["rho"]
        while stack:
            node = stack.pop()
            for child, _ in children[node]:
                if child not in reachable:
                    reachable.add(child)
                    stack.append(child)
        v.require(reachable == set(NODES4), f"displayed-tree reachability for choices {choices}")

    # Suppress rho, composing rho->h1 and rho->u into the bridge h1--u.
    semi_nodes = set(NODES4) - {"rho"}
    semi_edges = {
        frozenset((parent, child))
        for edge_id, (parent, child, _) in ARCS4.items()
        if edge_id not in {"rho_h1", "rho_u"}
    }
    semi_edges.add(frozenset(("h1", "u")))
    v.require(len(semi_nodes) == 10 and len(semi_edges) == 11,
              "root-suppressed four-leaf graph size")
    v.require(undirected_connected(semi_nodes, semi_edges), "root-suppressed graph connectivity")

    core_nodes = {"u", "p", "q", "r2", "r3"}
    core_edges = {
        frozenset(("u", "p")), frozenset(("u", "q")),
        frozenset(("p", "r2")), frozenset(("q", "r2")),
        frozenset(("p", "r3")), frozenset(("q", "r3")),
    }
    v.require(core_edges <= semi_edges and len(core_edges) - len(core_nodes) + 1 == 2,
              "theta core has cycle rank two")
    v.require(undirected_connected(core_nodes, core_edges), "theta core connectivity")
    for omitted in core_nodes:
        remaining_nodes = core_nodes - {omitted}
        remaining_edges = {edge for edge in core_edges if omitted not in edge}
        v.require(undirected_connected(remaining_nodes, remaining_edges),
                  f"theta core remains connected after deleting {omitted}")
    outside_edges = semi_edges - core_edges
    v.require(len(outside_edges) == 5, "five cut edges outside the theta blob")
    for edge in outside_edges:
        v.require(not undirected_connected(semi_nodes, semi_edges - {edge}),
                  f"edge {sorted(edge)} outside theta core is a bridge")
    v.require({node for node in core_nodes if NODES4[node] == "reticulation"} == {"r2", "r3"},
              "exactly two reticulations in the theta blob")

    noncore_edges = semi_edges - core_edges
    leaf_sides = []
    for attachment in ("u", "r2", "r3"):
        component = undirected_reachable(attachment, semi_nodes, noncore_edges)
        leaf_sides.append({node for node in component if NODES4[node] == "leaf"})
    v.require(leaf_sides == [{"1", "4"}, {"2"}, {"3"}],
              "three incident leaf components, with the new cherry outside the blob")

    tree_edges = {frozenset((parent, child)) for parent, child, _ in TREE_ARCS4.values()}
    v.require(undirected_connected(TREE_NODES4, tree_edges), "comparison quartet connectivity")
    degree = {node: 0 for node in TREE_NODES4}
    for edge in tree_edges:
        for node in edge:
            degree[node] += 1
    v.require(degree["t"] == degree["h1"] == 3, "binary quartet internal degrees")
    v.require(all(degree[leaf] == 1 for leaf in ("1", "2", "3", "4")),
              "binary quartet leaf degrees")
    split_edge = frozenset(("t", "h1"))
    split_graph = tree_edges - {split_edge}
    side_14 = undirected_reachable("1", TREE_NODES4, split_graph)
    v.require({leaf for leaf in side_14 if TREE_NODES4[leaf] == "leaf"} == {"1", "4"},
              "comparison quartet split 14|23")

    print("[four-leaf topology] PASS  exact rooted binary graft has 11 vertices, 12 arcs, and four displayed trees")
    print("[four-leaf topology] PASS  root suppression retains one maximal strict level-2 theta blob; the cherry is on a cut-edge side")
    print("[four-leaf topology] PASS  comparison tree is the binary quartet with split 14|23")


def verify_edges4() -> None:
    half = v.Alg.rat(v.F(1, 2))
    expected_graft = (v.Alg.one(), half, half, half)
    v.require(GRAFT == expected_graft, "exact graft eigenvector K=(1,1/2,1/2,1/2)")
    v.check_edge("new graft edge h1->1", GRAFT)
    v.check_edge("new graft edge h1->4", GRAFT)
    expected_transition = tuple(
        v.Alg.rat(value) for value in (v.F(5, 8), v.F(1, 8), v.F(1, 8), v.F(1, 8))
    )
    v.require(v.transition_probs(GRAFT) == expected_transition,
              "new graft transition row (5/8,1/8,1/8,1/8)")
    graft_margin = GRAFT[2] - GRAFT[1] * GRAFT[1]
    v.require(graft_margin == v.Alg.rat(v.F(1, 4)), "new graft CT margin 1/4")

    effective_stem = tuple(left * right for left, right in zip(GRAFT, v.network_vectors["K"]))
    quarter = v.Alg.rat(v.F(1, 4))
    v.require(effective_stem == (v.Alg.one(), quarter, quarter, quarter),
              "root-suppressed K odot K stem")
    v.check_edge("root-suppressed h1--u stem", effective_stem)
    expected_stem_transition = tuple(
        v.Alg.rat(value) for value in (v.F(7, 16), v.F(3, 16), v.F(3, 16), v.F(3, 16))
    )
    v.require(v.transition_probs(effective_stem) == expected_stem_transition,
              "effective-stem transition row (7/16,3/16,3/16,3/16)")
    stem_margin = effective_stem[2] - effective_stem[1] * effective_stem[1]
    v.require(stem_margin == v.Alg.rat(v.F(3, 16)), "effective-stem CT margin 3/16")

    base_minimum_margin = v.Alg.rat(v.F(11, 900))
    (graft_margin - base_minimum_margin).require_positive("new graft margin exceeds 11/900")
    (stem_margin - base_minimum_margin).require_positive("effective stem margin exceeds 11/900")
    print("[four-leaf edges] PASS  each new K edge has row (5/8,1/8,1/8,1/8) and CT margin 1/4")
    print("[four-leaf edges] PASS  suppressed K odot K stem has row (7/16,3/16,3/16,3/16) and CT margin 3/16")
    print("[four-leaf edges] PASS  the full graft retains the certified global CT-margin minimum 11/900")


def verify_distribution4(
    old_probabilities: Mapping[Tuple[int, int, int], v.Alg],
) -> None:
    labels4 = list(itertools.product(range(4), repeat=4))
    q_network: Dict[Tuple[int, int, int, int], v.Alg] = {}
    q_tree: Dict[Tuple[int, int, int, int], v.Alg] = {}
    consistent = 0
    inconsistent = 0
    for labels in labels4:
        graph_network = network_fourier4_from_graph(labels)
        graph_tree = tree_fourier4_from_graph(labels)
        lifted_network = graft_formula(v.network_q, labels)
        lifted_tree = graft_formula(v.tree_q, labels)
        v.require(graph_network == lifted_network,
                  f"literal-network/graft-formula Fourier equality at {labels}")
        v.require(graph_tree == lifted_tree,
                  f"literal-tree/graft-formula Fourier equality at {labels}")
        v.require(graph_network == graph_tree, f"four-leaf network/tree Fourier equality at {labels}")
        q_network[labels] = graph_network
        q_tree[labels] = graph_tree
        if labels[0] ^ labels[1] ^ labels[2] ^ labels[3]:
            inconsistent += 1
            v.require(graph_network.is_zero(), f"inconsistent four-leaf Fourier coordinate {labels}")
        else:
            consistent += 1
            graph_network.require_positive(f"consistent four-leaf Fourier coordinate {labels}")
    v.require((consistent, inconsistent) == (64, 192),
              "64 consistent and 192 vanishing four-leaf Fourier coordinates")
    v.require(q_network[(0, 0, 0, 0)] == v.Alg.one(), "q_AAAA normalization")
    v.require(q_network == q_tree, "complete four-leaf Fourier dictionaries")
    print("[four-leaf Fourier] PASS  literal graphs and graft formula agree on all 256 coordinates (64 consistent, 192 zero)")

    probabilities: Dict[Tuple[int, int, int, int], v.Alg] = {}
    for pattern in itertools.product(range(4), repeat=4):
        fourier = inverse_fourier4(q_network, pattern)
        network = direct_network_probability4(pattern)
        tree = direct_tree_probability4(pattern)
        extension = direct_markov_extension(old_probabilities, pattern)
        v.require(fourier == network == tree == extension,
                  f"four-way ordinary-state equality at pattern {pattern}")
        fourier.require_positive(f"four-leaf pattern probability {pattern}")
        probabilities[pattern] = fourier
    v.require(alg_sum(probabilities.values()) == v.Alg.one(),
              "four-leaf pattern probabilities sum to one")

    claimed_minimum = v.Alg(
        (
            v.F(5681, 1966080),
            v.F(79, 15728640),
            -v.F(3, 65536),
            v.F(0), v.F(0), v.F(0),
        )
    )
    minimizers = v.require_global_minimum(
        ((str(pattern), value) for pattern, value in probabilities.items()),
        claimed_minimum,
        "four-leaf pattern probability",
    )
    v.require(len(minimizers) == 16, "sixteen four-leaf minimum-probability patterns")
    print("[four-leaf pruning] PASS  all 256 patterns agree by displayed-tree pruning, quartet pruning, Fourier inversion, and Markov extension")
    print("[four-leaf patterns] PASS  all probabilities are positive, sum to 1, and the certified exact minimum has 16 minimizers")
    print("[four-leaf scope] PASS  this is an exact n=4 regression of the shared cherry-graft identity")
    print("[four-leaf scope] INFO  iteration to arbitrary n requires the separate theorem-level graft lemma")


def main() -> None:
    v.require_python()
    v.verify_field()
    v.verify_topology()
    v.verify_parameters()
    v.verify_construction()
    _, old_probabilities = v.verify_factorization_and_distribution()
    verify_topology4()
    verify_edges4()
    verify_distribution4(old_probabilities)
    print()
    print("ALL FOUR-LEAF GRAFT CHECKS PASSED")


if __name__ == "__main__":
    main()
