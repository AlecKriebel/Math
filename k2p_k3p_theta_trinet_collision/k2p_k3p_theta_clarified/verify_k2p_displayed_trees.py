#!/usr/bin/env python3
"""Exact graph-derived audit of the simple K2P displayed-tree collision.

The four Fourier monomials are reconstructed from the rooted arc list after
deleting one incoming edge at each reticulation.  They are not used as the
definition of the network distribution.  A second calculation performs
ordinary-state Markov pruning on the four retained-edge graphs and compares
all 64 patterns with the comparison tree and with Fourier inversion.

Only the Python standard library is required.  Every equality is exact in
Q(sqrt(71)); floating-point arithmetic is used nowhere.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from typing import Dict, Iterable, Mapping, Sequence, Tuple


ROOT = Path(__file__).resolve().parent
CERT = json.loads((ROOT / "certificate_k2p_simple.json").read_text())
SYMBOLS = ("A", "C", "G", "T")
CHARACTERS = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)
LEAF_POSITION = {"1": 0, "2": 1, "3": 2}


def F(value: str | int | Fraction, denominator: int | None = None) -> Fraction:
    if denominator is not None:
        return Fraction(int(value), denominator)
    return value if isinstance(value, Fraction) else Fraction(str(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


@dataclass(frozen=True)
class Quad:
    """The exact number a+b*sqrt(71)."""

    a: Fraction
    b: Fraction = Fraction(0)

    @staticmethod
    def zero() -> "Quad":
        return Quad(F(0))

    @staticmethod
    def one() -> "Quad":
        return Quad(F(1))

    def __add__(self, other: "Quad") -> "Quad":
        return Quad(self.a + other.a, self.b + other.b)

    def __radd__(self, other: int) -> "Quad":
        return self if other == 0 else NotImplemented

    def __neg__(self) -> "Quad":
        return Quad(-self.a, -self.b)

    def __sub__(self, other: "Quad") -> "Quad":
        return self + (-other)

    def __mul__(self, other: "Quad") -> "Quad":
        return Quad(
            self.a * other.a + F(71) * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def scale(self, scalar: str | int | Fraction) -> "Quad":
        scalar = F(scalar)
        return Quad(scalar * self.a, scalar * self.b)

    def raw(self) -> list[str]:
        return [str(self.a), str(self.b)]


ZERO = Quad.zero()
ONE = Quad.one()


def parse_quad(raw: Sequence[str]) -> Quad:
    require(len(raw) == 2, "Q(sqrt(71)) coefficient vector must have length two")
    return Quad(F(raw[0]), F(raw[1]))


def parse_vector(raw: Sequence[Sequence[str]]) -> Tuple[Quad, Quad, Quad, Quad]:
    require(len(raw) == 4, "Fourier vector must have four entries")
    return tuple(parse_quad(entry) for entry in raw)  # type: ignore[return-value]


NETWORK_VECTORS = {
    name: parse_vector(raw)
    for name, raw in CERT["network_vectors"].items()
    if name in {"K", "U", "V", "S", "T"}
}
TREE_VECTORS = {
    name: parse_vector(CERT["comparison_tree"][name])
    for name in ("alpha", "beta", "gamma")
}
P = parse_vector(CERT["core_factors"]["P"])
R = parse_vector(CERT["core_factors"]["R"])


# The graph comes from the certificate.  This table fixes only which vector is
# placed on each graph edge; no displayed-tree monomial appears here.
EDGE_VECTOR = {
    ("rho", "1"): "K",
    ("rho", "u"): "K",
    ("u", "p"): "U",
    ("u", "q"): "V",
    ("p", "r2"): "S",
    ("p", "r3"): "S",
    ("q", "r2"): "T",
    ("q", "r3"): "T",
    ("r2", "2"): "K",
    ("r3", "3"): "K",
}
ARC_ROWS = CERT["rooted_network"]["arcs"]
CERT_ARCS = {(row["parent"], row["child"]) for row in ARC_ROWS}
require(
    len(ARC_ROWS) == len(CERT_ARCS) == len(EDGE_VECTOR) == 10,
    "certificate must contain ten distinct theta arcs",
)
require(CERT_ARCS == set(EDGE_VECTOR), "certificate arc list does not match the theta graph")
ARCS = {
    f"{row['parent']}->{row['child']}": (
        row["parent"], row["child"], EDGE_VECTOR[row["parent"], row["child"]]
    )
    for row in CERT["rooted_network"]["arcs"]
}
require(len(ARCS) == 10, "certificate arc list contains a duplicate")
VERTEX_ROWS = CERT["rooted_network"]["vertices"]
NODE_TYPES = {row["id"]: row["type"] for row in VERTEX_ROWS}
EXPECTED_NODE_TYPES = {
    "rho": "root", "u": "tree", "p": "tree", "q": "tree",
    "r2": "reticulation", "r3": "reticulation",
    "1": "leaf", "2": "leaf", "3": "leaf",
}
require(
    len(VERTEX_ROWS) == len(NODE_TYPES) == len(EXPECTED_NODE_TYPES)
    and NODE_TYPES == EXPECTED_NODE_TYPES,
    "certificate vertex list or vertex types do not match the rooted theta graph",
)
NODES = set(NODE_TYPES)

MIXING = {name: F(value) for name, value in CERT["mixing_parameters"].items()}
require(MIXING == {"r2": F(1, 2), "r3": F(1, 2)},
        "the simple displayed-tree audit requires inheritance weights 1/2,1/2")


def retained_edges(parent_r2: str, parent_r3: str) -> Tuple[str, ...]:
    """Delete the unselected incoming arc at each reticulation."""
    require(parent_r2 in {"p", "q"} and parent_r3 in {"p", "q"}, "invalid switch")
    other_parent = {"p": "q", "q": "p"}
    deleted = {
        f"{other_parent[parent_r2]}->r2",
        f"{other_parent[parent_r3]}->r3",
    }
    kept = tuple(edge_id for edge_id in ARCS if edge_id not in deleted)
    require(len(kept) == 8, "a displayed tree must retain eight rooted edges")
    return kept


def child_map(edge_ids: Iterable[str]) -> Dict[str, list[Tuple[str, str]]]:
    children: Dict[str, list[Tuple[str, str]]] = {node: [] for node in NODES}
    for edge_id in edge_ids:
        parent, child, _ = ARCS[edge_id]
        children[parent].append((child, edge_id))
    return children


def labelled_descendants(start: str, children: Mapping[str, Sequence[Tuple[str, str]]]) -> frozenset[str]:
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for child, _ in children.get(node, ()):
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return frozenset(leaf for leaf in LEAF_POSITION if leaf in seen)


def descendant_sets(edge_ids: Iterable[str]) -> Dict[str, frozenset[str]]:
    edge_ids = tuple(edge_ids)
    children = child_map(edge_ids)
    return {
        edge_id: labelled_descendants(ARCS[edge_id][1], children)
        for edge_id in edge_ids
    }


def set_text(leaves: Iterable[str]) -> str:
    return "{" + ",".join(sorted(leaves)) + "}"


def symbolic_label(leaves: frozenset[str]) -> str:
    labels = {
        frozenset(): "A",
        frozenset({"1"}): "x",
        frozenset({"2"}): "y",
        frozenset({"3"}): "z",
        frozenset({"2", "3"}): "(y+z)",
        frozenset({"1", "2", "3"}): "A",
    }
    require(leaves in labels, f"unexpected descendant set {set_text(leaves)}")
    return labels[leaves]


def core_monomial(edge_ids: Iterable[str]) -> str:
    """Derive the nonidentity U,V,S,T factors from one retained graph."""
    edge_ids = tuple(edge_ids)
    below = descendant_sets(edge_ids)
    factors: list[Tuple[Tuple[int, str], str]] = []
    for edge_id in edge_ids:
        _, child, vector = ARCS[edge_id]
        if vector == "K":
            continue
        label = symbolic_label(below[edge_id])
        if label == "A":
            continue
        factor = f"{vector}_{label}"
        # Reticulation factors at leaves 2 and 3 are printed first, followed by
        # the U and V path factors.  The order changes no mathematics.
        rank = 0 if child == "r2" else (1 if child == "r3" else (2 if vector == "U" else 3))
        factors.append(((rank, edge_id), factor))
    return "*".join(factor for _, factor in sorted(factors))


EXPECTED_MONOMIALS = {
    ("p", "p"): "S_y*S_z*U_(y+z)",
    ("p", "q"): "S_y*T_z*U_y*V_z",
    ("q", "p"): "T_y*S_z*U_z*V_y",
    ("q", "q"): "T_y*T_z*V_(y+z)",
}


def verify_displayed_tree_monomials() -> None:
    common_k_signature = None
    for parent_r2, parent_r3 in product(("p", "q"), repeat=2):
        kept = retained_edges(parent_r2, parent_r3)
        below = descendant_sets(kept)
        monomial = core_monomial(kept)
        require(monomial == EXPECTED_MONOMIALS[parent_r2, parent_r3],
                f"wrong graph-derived monomial for switch {(parent_r2, parent_r3)}")

        k_edges = [edge_id for edge_id in kept if ARCS[edge_id][2] == "K"]
        signature = tuple(symbolic_label(below[edge_id]) for edge_id in k_edges)
        require(sorted(signature) == ["(y+z)", "x", "y", "z"], "wrong common K factor")
        common_k_signature = signature if common_k_signature is None else common_k_signature
        require(sorted(signature) == sorted(common_k_signature), "K factor depends on switching")

        print(f"[switch {parent_r2},{parent_r3}]")
        print("  retained edges = " + ", ".join(kept))
        print(f"  u->p descendants = {set_text(below['u->p'])}")
        print(f"  u->q descendants = {set_text(below['u->q'])}")
        print(f"  core monomial = {monomial}")

    print("[common K factor] PASS  K_x*K_(y+z)*K_y*K_z = K_x^2*K_y*K_z")
    print("[displayed trees] PASS  four monomials reconstructed from retained edges")


def group_sum(leaves: Iterable[str], leaf_labels: Sequence[int]) -> int:
    value = 0
    for leaf in leaves:
        value ^= leaf_labels[LEAF_POSITION[leaf]]
    return value


def edge_product(edge_ids: Iterable[str], leaf_labels: Sequence[int], core_only: bool = False) -> Quad:
    edge_ids = tuple(edge_ids)
    below = descendant_sets(edge_ids)
    value = ONE
    for edge_id in edge_ids:
        vector = ARCS[edge_id][2]
        if core_only and vector == "K":
            continue
        label = group_sum(below[edge_id], leaf_labels)
        value = value * NETWORK_VECTORS[vector][label]
    return value


def network_fourier(leaf_labels: Tuple[int, int, int]) -> Quad:
    if leaf_labels[0] ^ leaf_labels[1] ^ leaf_labels[2]:
        return ZERO
    total = ZERO
    for parent_r2, parent_r3 in product(("p", "q"), repeat=2):
        total += edge_product(retained_edges(parent_r2, parent_r3), leaf_labels)
    return total.scale(F(1, 4))


def tree_fourier(leaf_labels: Tuple[int, int, int]) -> Quad:
    if leaf_labels[0] ^ leaf_labels[1] ^ leaf_labels[2]:
        return ZERO
    x, y, z = leaf_labels
    return TREE_VECTORS["alpha"][x] * TREE_VECTORS["beta"][y] * TREE_VECTORS["gamma"][z]


def verify_core_and_fourier() -> Dict[Tuple[int, int, int], Quad]:
    for y, z in product(range(4), repeat=2):
        x = y ^ z
        labels = (x, y, z)
        graph_mixture = ZERO
        graph_terms: list[Quad] = []
        for parent_r2, parent_r3 in product(("p", "q"), repeat=2):
            term = edge_product(
                retained_edges(parent_r2, parent_r3), labels, core_only=True
            )
            graph_terms.append(term)
            graph_mixture += term
        stored_terms = [
            parse_quad(entry)
            for entry in CERT["displayed_core_terms"][SYMBOLS[y] + SYMBOLS[z]]
        ]
        require(graph_terms == stored_terms, f"displayed contribution mismatch at {(y, z)}")
        graph_mixture = graph_mixture.scale(F(1, 4))
        expected_matrix = parse_quad(CERT["core_matrix"][SYMBOLS[y] + SYMBOLS[z]])
        require(graph_mixture == expected_matrix, f"core matrix mismatch at {(y, z)}")
        require(graph_mixture == P[x] * R[y] * R[z], f"factorization mismatch at {(y, z)}")

    require(parse_quad(CERT["core_matrix"]["AC"]) == Quad(F(151, 1440)), "M_AC fingerprint")
    require(parse_quad(CERT["core_matrix"]["CC"]) == Quad(F(71, 1600)), "M_CC fingerprint")
    print("[core matrix] PASS  graph mixture gives all 16 factors; M_AC=151/1440 and M_CC=71/1600")

    q_network: Dict[Tuple[int, int, int], Quad] = {}
    for labels in product(range(4), repeat=3):
        labels = tuple(labels)  # type: ignore[assignment]
        q_network[labels] = network_fourier(labels)
        q_tree = tree_fourier(labels)
        label = "".join(SYMBOLS[value] for value in labels)
        require(q_network[labels] == q_tree, f"Fourier mismatch at {labels}")
        require(q_network[labels] == parse_quad(CERT["fourier_network"][label]),
                f"stored network Fourier mismatch at {labels}")
        require(q_tree == parse_quad(CERT["fourier_tree"][label]),
                f"stored tree Fourier mismatch at {labels}")
    print("[Fourier] PASS  all 64 graph-derived network/tree coordinates agree exactly")
    return q_network


def transition_kernel(vector: Sequence[Quad]) -> Tuple[Quad, Quad, Quad, Quad]:
    one, c, g, t = vector
    return (
        (one + c + g + t).scale(F(1, 4)),
        (one + c - g - t).scale(F(1, 4)),
        (one - c + g - t).scale(F(1, 4)),
        (one - c - g + t).scale(F(1, 4)),
    )


def transition_matrix(vector: Sequence[Quad]) -> Tuple[Tuple[Quad, Quad, Quad, Quad], ...]:
    kernel = transition_kernel(vector)
    return tuple(
        tuple(kernel[parent_state ^ child_state] for child_state in range(4))
        for parent_state in range(4)
    )


def verify_transition_data() -> None:
    for name, vector in NETWORK_VECTORS.items():
        require(vector[0] == ONE, f"network vector {name} has wrong identity eigenvalue")
        calculated = transition_kernel(vector)
        stored = tuple(
            parse_quad(entry)
            for entry in CERT["network_transition_probabilities"][name]
        )
        require(calculated == stored, f"stored transition row mismatch for {name}")
        require(sum(calculated, ZERO) == ONE, f"transition row {name} does not sum to one")
        matrix = transition_matrix(vector)
        require(all(sum(row, ZERO) == ONE for row in matrix),
                f"transition matrix {name} has a nonstochastic row")
    for name, vector in TREE_VECTORS.items():
        require(vector[0] == ONE, f"tree vector {name} has wrong identity eigenvalue")
        calculated = transition_kernel(vector)
        stored = tuple(
            parse_quad(entry)
            for entry in CERT["comparison_tree"]["transition_probabilities"][name]
        )
        require(calculated == stored, f"stored tree transition row mismatch for {name}")
        require(sum(calculated, ZERO) == ONE, f"tree transition row {name} does not sum to one")
        matrix = transition_matrix(vector)
        require(all(sum(row, ZERO) == ONE for row in matrix),
                f"tree transition matrix {name} has a nonstochastic row")
    print("[transition matrices] PASS  all exact 4x4 K2P matrices reconstructed from the stored Fourier vectors")


def topological_order(edge_ids: Iterable[str]) -> Tuple[str, ...]:
    edge_ids = tuple(edge_ids)
    children = child_map(edge_ids)
    indegree = {node: 0 for node in NODES}
    for edge_id in edge_ids:
        indegree[ARCS[edge_id][1]] += 1
    require(indegree["rho"] == 0 and all(indegree[node] == 1 for node in NODES - {"rho"}),
            "retained graph must have one root and indegree one elsewhere")
    queue = [node for node in NODES if indegree[node] == 0]
    order: list[str] = []
    while queue:
        node = queue.pop()
        order.append(node)
        for child, _ in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    require(len(order) == len(NODES), "retained graph is not acyclic")
    require(set(order) == NODES, "not every displayed-tree vertex is reachable from rho")
    return tuple(order)


def displayed_pattern_probability(
    pattern: Tuple[int, int, int], parent_r2: str, parent_r3: str
) -> Quad:
    kept = retained_edges(parent_r2, parent_r3)
    children = child_map(kept)
    observed = {leaf: pattern[position] for leaf, position in LEAF_POSITION.items()}
    likelihood: Dict[str, list[Quad]] = {}

    for node in reversed(topological_order(kept)):
        if node in observed:
            likelihood[node] = [ONE if state == observed[node] else ZERO for state in range(4)]
            continue
        values = [ONE for _ in range(4)]
        for child, edge_id in children[node]:
            vector = NETWORK_VECTORS[ARCS[edge_id][2]]
            matrix = transition_matrix(vector)
            contribution: list[Quad] = []
            for parent_state in range(4):
                subtotal = ZERO
                for child_state in range(4):
                    subtotal += matrix[parent_state][child_state] * likelihood[child][child_state]
                contribution.append(subtotal)
            values = [left * right for left, right in zip(values, contribution)]
        # A dangling unlabelled branch has no children and therefore likelihood 1.
        likelihood[node] = values
    return sum(likelihood["rho"], ZERO).scale(F(1, 4))


def tree_pattern_probability(pattern: Tuple[int, int, int]) -> Quad:
    matrices = [transition_matrix(TREE_VECTORS[name]) for name in ("alpha", "beta", "gamma")]
    total = ZERO
    for root_state in range(4):
        term = ONE
        for leaf_state, matrix in zip(pattern, matrices):
            term = term * matrix[root_state][leaf_state]
        total += term
    return total.scale(F(1, 4))


def fourier_inversion(
    q: Mapping[Tuple[int, int, int], Quad]
) -> Dict[Tuple[int, int, int], Quad]:
    probabilities: Dict[Tuple[int, int, int], Quad] = {}
    for pattern in product(range(4), repeat=3):
        value = ZERO
        for labels in product(range(4), repeat=3):
            coefficient = (
                CHARACTERS[labels[0]][pattern[0]]
                * CHARACTERS[labels[1]][pattern[1]]
                * CHARACTERS[labels[2]][pattern[2]]
            )
            value += q[labels].scale(F(coefficient, 64))
        probabilities[pattern] = value
    return probabilities


def verify_direct_pruning(q_network: Mapping[Tuple[int, int, int], Quad]) -> None:
    inverted = fourier_inversion(q_network)
    direct_probabilities: Dict[Tuple[int, int, int], Quad] = {}
    for pattern in product(range(4), repeat=3):
        network = ZERO
        for parent_r2, parent_r3 in product(("p", "q"), repeat=2):
            network += displayed_pattern_probability(pattern, parent_r2, parent_r3).scale(F(1, 4))
        tree = tree_pattern_probability(pattern)
        label = "".join(SYMBOLS[value] for value in pattern)
        require(network == tree, f"ordinary-state network/tree mismatch at {pattern}")
        require(network == inverted[pattern], f"ordinary-state/Fourier mismatch at {pattern}")
        require(network == parse_quad(CERT["patterns_network"][label]),
                f"stored network pattern mismatch at {pattern}")
        require(tree == parse_quad(CERT["patterns_tree"][label]),
                f"stored tree pattern mismatch at {pattern}")
        direct_probabilities[pattern] = network

    require(sum(direct_probabilities.values(), ZERO) == ONE, "pattern probabilities do not sum to one")
    certificate_minimum = parse_quad(CERT["minimum_pattern"]["value"])
    require(certificate_minimum in direct_probabilities.values(), "certificate minimum not reproduced")
    print("[direct pruning] PASS  all 64 network/tree probabilities agree exactly")


def main() -> None:
    verify_displayed_tree_monomials()
    verify_transition_data()
    q_network = verify_core_and_fourier()
    verify_direct_pruning(q_network)
    print("\nALL DISPLAYED-TREE CHECKS PASSED")


if __name__ == "__main__":
    main()
