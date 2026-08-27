#!/usr/bin/env python3
"""Dependency-free exact verifier for the K3P theta-trinet package.

The verifier reads certificate.json, independently reconstructs the rooted
network, its semi-directed root suppression, every displayed tree, all Fourier
and leaf-pattern coordinates, the 15 x 15 Jacobian minor, and the exact fixed-output tangent identity
used in the edgewise strictly continuous-time extension.

Arithmetic is exact in the quartic number field Q(h), represented in the basis
1,h,h^2,h^3 with the relation h^4=1/5.  Strict signs are certified with the rational isolating interval
2/3 < h < 7/10; no floating-point equality is used.
"""
from __future__ import annotations

import argparse
import itertools
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))
from strict_json import load_canonical_certificate


# ---------------------------------------------------------------------------
# Exact quartic-field arithmetic
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Alg:
    """c0+c1*h+c2*h^2+c3*h^3 in the basis representation of Q(h)."""

    c: Tuple[Fraction, Fraction, Fraction, Fraction]

    @staticmethod
    def zero() -> "Alg":
        return Alg((Fraction(0), Fraction(0), Fraction(0), Fraction(0)))

    @staticmethod
    def one() -> "Alg":
        return Alg((Fraction(1), Fraction(0), Fraction(0), Fraction(0)))

    @staticmethod
    def rational(value: int | Fraction) -> "Alg":
        return Alg((Fraction(value), Fraction(0), Fraction(0), Fraction(0)))

    @staticmethod
    def h() -> "Alg":
        return Alg((Fraction(0), Fraction(1), Fraction(0), Fraction(0)))

    def __add__(self, other: "Alg") -> "Alg":
        return Alg(tuple(a + b for a, b in zip(self.c, other.c)))  # type: ignore[arg-type]

    def __neg__(self) -> "Alg":
        return Alg(tuple(-a for a in self.c))  # type: ignore[arg-type]

    def __sub__(self, other: "Alg") -> "Alg":
        return self + (-other)

    def __mul__(self, other: "Alg") -> "Alg":
        raw = [Fraction(0) for _ in range(7)]
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                raw[i + j] += a * b
        # h^4=1/5, hence h^k=h^(k-4)/5 for k=4,5,6.
        for degree in range(6, 3, -1):
            raw[degree - 4] += raw[degree] / 5
            raw[degree] = Fraction(0)
        return Alg(tuple(raw[:4]))  # type: ignore[arg-type]

    def scale(self, value: int | Fraction) -> "Alg":
        value = Fraction(value)
        return Alg(tuple(value * a for a in self.c))  # type: ignore[arg-type]

    def is_zero(self) -> bool:
        return all(a == 0 for a in self.c)

    def inverse(self) -> "Alg":
        if self.is_zero():
            raise ZeroDivisionError("zero has no multiplicative inverse")
        basis = [Alg.one(), Alg.h(), Alg.h() * Alg.h(), Alg.h() * Alg.h() * Alg.h()]
        products = [self * b for b in basis]
        aug = [
            [products[col].c[row] for col in range(4)]
            + [Fraction(1 if row == 0 else 0)]
            for row in range(4)
        ]
        for col in range(4):
            pivot = next((r for r in range(col, 4) if aug[r][col] != 0), None)
            if pivot is None:
                raise ZeroDivisionError("field element is not invertible")
            aug[col], aug[pivot] = aug[pivot], aug[col]
            p = aug[col][col]
            aug[col] = [x / p for x in aug[col]]
            for r in range(4):
                if r == col:
                    continue
                f = aug[r][col]
                if f:
                    aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
        return Alg(tuple(aug[r][4] for r in range(4)))  # type: ignore[arg-type]

    def __truediv__(self, other: "Alg") -> "Alg":
        return self * other.inverse()

    def interval(self, lo: Fraction, hi: Fraction) -> Tuple[Fraction, Fraction]:
        """Natural rational interval enclosure for positive h in [lo,hi]."""
        lower = Fraction(0)
        upper = Fraction(0)
        for degree, coeff in enumerate(self.c):
            lo_pow = lo ** degree
            hi_pow = hi ** degree
            if coeff >= 0:
                lower += coeff * lo_pow
                upper += coeff * hi_pow
            else:
                lower += coeff * hi_pow
                upper += coeff * lo_pow
        return lower, upper

    def __str__(self) -> str:
        return "Alg(" + ", ".join(str(x) for x in self.c) + ")"


def parse_fraction(raw: str | int) -> Fraction:
    return Fraction(str(raw))


def parse_alg(raw: Sequence[str]) -> Alg:
    if len(raw) != 4:
        raise AssertionError(f"field element must have four coefficients: {raw!r}")
    return Alg(tuple(parse_fraction(x) for x in raw))  # type: ignore[arg-type]


def parse_vector(raw: Sequence[Sequence[str]]) -> List[Alg]:
    return [parse_alg(x) for x in raw]


def det_field(matrix: Sequence[Sequence[Alg]]) -> Alg:
    if not matrix or any(len(row) != len(matrix) for row in matrix):
        raise AssertionError("determinant requires a nonempty square matrix")
    a = [list(row) for row in matrix]
    n = len(a)
    sign = 1
    determinant = Alg.one()
    for col in range(n):
        pivot = next((r for r in range(col, n) if not a[r][col].is_zero()), None)
        if pivot is None:
            return Alg.zero()
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign *= -1
        p = a[col][col]
        determinant = determinant * p
        for r in range(col + 1, n):
            if a[r][col].is_zero():
                continue
            factor = a[r][col] / p
            for j in range(col, n):
                a[r][j] = a[r][j] - factor * a[col][j]
    return determinant.scale(sign)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}\n  actual:   {actual!r}\n  expected: {expected!r}")


def require_zero(value: Alg, message: str) -> None:
    if not value.is_zero():
        raise AssertionError(f"{message}: {value}")


def require_positive(value: Alg, lo: Fraction, hi: Fraction, message: str) -> None:
    lower, upper = value.interval(lo, hi)
    if lower <= 0:
        raise AssertionError(f"{message}: enclosure [{lower}, {upper}] is not strictly positive")


def require_between_zero_one(value: Alg, lo: Fraction, hi: Fraction, message: str) -> None:
    require_positive(value, lo, hi, message)
    require_positive(Alg.one() - value, lo, hi, f"1 minus {message}")


def inverse_fourier_edge_probabilities(eigen: Sequence[Alg]) -> List[Alg]:
    require(len(eigen) == 4, "K3P edge vector must have four entries")
    one, c, g, t = eigen
    require_equal(one, Alg.one(), "identity Fourier eigenvalue")
    return [
        (one + c + g + t).scale(Fraction(1, 4)),
        (one + c - g - t).scale(Fraction(1, 4)),
        (one - c + g - t).scale(Fraction(1, 4)),
        (one - c - g + t).scale(Fraction(1, 4)),
    ]


def ct_margins(eigen: Sequence[Alg]) -> Dict[str, Alg]:
    _, c, g, t = eigen
    return {
        "C_minus_G_T": c - g * t,
        "G_minus_C_T": g - c * t,
        "T_minus_C_G": t - c * g,
    }


def ct_margin_derivatives(eigen: Sequence[Alg], direction: Sequence[Alg]) -> Dict[str, Alg]:
    """Directional derivatives of the three K3P rate margins."""
    require(len(eigen) == len(direction) == 4, "K3P margin derivative vectors")
    _, c, g, t = eigen
    _, dc, dg, dt = direction
    return {
        "C_minus_G_T": dc - dg * t - g * dt,
        "G_minus_C_T": dg - dc * t - c * dt,
        "T_minus_C_G": dt - dc * g - c * dg,
    }


# ---------------------------------------------------------------------------
# Graph utilities
# ---------------------------------------------------------------------------


def topological_order(nodes: Sequence[str], directed_edges: Sequence[Tuple[str, str]]) -> List[str]:
    indegree = {v: 0 for v in nodes}
    children: Dict[str, List[str]] = {v: [] for v in nodes}
    for u, v in directed_edges:
        require(u in indegree and v in indegree, f"edge {u}->{v} has an unknown endpoint")
        indegree[v] += 1
        children[u].append(v)
    queue = sorted(v for v in nodes if indegree[v] == 0)
    order: List[str] = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in sorted(children[u]):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
                queue.sort()
    require(len(order) == len(nodes), "rooted graph is not acyclic")
    return order


def reachable(start: str, adjacency: Mapping[str, Iterable[str]]) -> Set[str]:
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in adjacency.get(u, []):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def connected(nodes: Set[str], edges: Iterable[frozenset[str]]) -> bool:
    if not nodes:
        return False
    adjacency: Dict[str, Set[str]] = {v: set() for v in nodes}
    for edge in edges:
        require(len(edge) == 2, f"invalid undirected edge {edge}")
        u, v = tuple(edge)
        if u in nodes and v in nodes:
            adjacency[u].add(v)
            adjacency[v].add(u)
    return reachable(next(iter(nodes)), adjacency) == nodes


def undirected_components(nodes: Set[str], edges: Iterable[frozenset[str]]) -> List[Set[str]]:
    adjacency: Dict[str, Set[str]] = {v: set() for v in nodes}
    for edge in edges:
        u, v = tuple(edge)
        if u in nodes and v in nodes:
            adjacency[u].add(v)
            adjacency[v].add(u)
    components: List[Set[str]] = []
    unseen = set(nodes)
    while unseen:
        start = min(unseen)
        comp = reachable(start, adjacency)
        components.append(comp)
        unseen -= comp
    return components


def bridge_edges(nodes: Set[str], edges: Set[frozenset[str]]) -> Set[frozenset[str]]:
    require(connected(nodes, edges), "semi-directed underlying graph must be connected")
    bridges: Set[frozenset[str]] = set()
    for edge in edges:
        reduced = set(edges)
        reduced.remove(edge)
        if not connected(nodes, reduced):
            bridges.add(edge)
    return bridges


# ---------------------------------------------------------------------------
# Certificate reconstruction
# ---------------------------------------------------------------------------


EXPECTED_VERTEX_ROWS = [
    {"id": "rho", "type": "root"},
    {"id": "u", "type": "tree"},
    {"id": "p", "type": "tree"},
    {"id": "q", "type": "tree"},
    {"id": "r2", "type": "reticulation"},
    {"id": "r3", "type": "reticulation"},
    {"id": "1", "type": "leaf", "label": 1},
    {"id": "2", "type": "leaf", "label": 2},
    {"id": "3", "type": "leaf", "label": 3},
]

EXPECTED_ARC_DESCRIPTORS = [
    {"id": "e_rho_1", "parent": "rho", "child": "1", "vector_name": "K"},
    {"id": "e_rho_u", "parent": "rho", "child": "u", "vector_name": "K"},
    {"id": "e_u_p", "parent": "u", "child": "p", "vector_name": "U"},
    {"id": "e_u_q", "parent": "u", "child": "q", "vector_name": "V"},
    {"id": "e_p_r2", "parent": "p", "child": "r2", "vector_name": "S"},
    {"id": "e_q_r2", "parent": "q", "child": "r2", "vector_name": "T"},
    {"id": "e_p_r3", "parent": "p", "child": "r3", "vector_name": "S"},
    {"id": "e_q_r3", "parent": "q", "child": "r3", "vector_name": "T"},
    {"id": "e_r2_2", "parent": "r2", "child": "2", "vector_name": "K"},
    {"id": "e_r3_3", "parent": "r3", "child": "3", "vector_name": "K"},
]

EXPECTED_RETICULATION_ROWS = [
    {
        "vertex": "r2",
        "incoming": [
            {"edge_id": "e_p_r2", "parent": "p", "weight": "1/2", "choice": "p"},
            {"edge_id": "e_q_r2", "parent": "q", "weight": "1/2", "choice": "q"},
        ],
    },
    {
        "vertex": "r3",
        "incoming": [
            {"edge_id": "e_p_r3", "parent": "p", "weight": "1/2", "choice": "p"},
            {"edge_id": "e_q_r3", "parent": "q", "weight": "1/2", "choice": "q"},
        ],
    },
]


class Verification:
    def __init__(self, certificate: Mapping[str, object]):
        self.cert = certificate
        field = certificate["field"]
        require(isinstance(field, Mapping), "missing field data")
        interval = field["isolating_interval"]
        require(isinstance(interval, list) and len(interval) == 2, "invalid isolating interval")
        self.lo, self.hi = (parse_fraction(x) for x in interval)
        self.symbols = ["A", "C", "G", "T"]
        self.index = {s: i for i, s in enumerate(self.symbols)}

        rooted = certificate["rooted_network"]
        require(isinstance(rooted, Mapping), "missing rooted network")
        vertices = rooted["vertices"]
        arcs = rooted["arcs"]
        retics = rooted["reticulations"]
        require(isinstance(vertices, list) and isinstance(arcs, list) and isinstance(retics, list),
                "invalid rooted network schema")
        for index, row in enumerate(vertices):
            require(isinstance(row, Mapping), f"vertex row {index} must be a mapping")
            require("id" in row, f"vertex row {index} is missing its identifier")
            require(isinstance(row["id"], str),
                    f"vertex identifier at row {index} must be a string")
        vertex_ids = [str(row["id"]) for row in vertices]
        require(len(vertex_ids) == len(set(vertex_ids)), "duplicate vertex identifier")
        require_equal(vertices, EXPECTED_VERTEX_ROWS, "canonical ordered vertex schema")

        arc_keys = {
            "id", "parent", "child", "vector_name", "eigen", "transition_probabilities"
        }
        for index, row in enumerate(arcs):
            require(isinstance(row, Mapping), f"rooted arc row {index} must be a mapping")
            require_equal(set(row), arc_keys, f"closed rooted arc row schema at index {index}")
            for key in ("id", "parent", "child", "vector_name"):
                require(isinstance(row[key], str),
                        f"rooted arc {key} at row {index} must be a string")
        arc_ids = [str(row["id"]) for row in arcs]
        require(len(arc_ids) == len(set(arc_ids)), "duplicate arc identifier")
        arc_descriptors = [
            {key: str(row[key]) for key in ("id", "parent", "child", "vector_name")}
            for row in arcs
        ]
        require_equal(arc_descriptors, EXPECTED_ARC_DESCRIPTORS,
                      "canonical rooted arc ID/endpoint/vector map")

        self.vertex_rows = vertices
        self.arc_rows = arcs
        self.retic_rows = retics
        self.vertex_type = {str(row["id"]): str(row["type"]) for row in vertices}
        self.nodes = list(self.vertex_type)
        self.edge_row_by_id = {str(row["id"]): row for row in arcs}
        self.edge_endpoints = {
            str(row["id"]): (str(row["parent"]), str(row["child"])) for row in arcs
        }
        self.edge_eigen = {
            str(row["id"]): parse_vector(row["eigen"]) for row in arcs
        }
        self.leaf_position = {"1": 0, "2": 1, "3": 2}

        group = certificate["group"]
        require(isinstance(group, Mapping), "missing group data")
        require_equal(group["symbols"], self.symbols, "Klein-group symbol order")
        require_equal(group["indices"], self.index, "Klein-group symbol indices")
        require_equal(group["addition"], "bitwise XOR on indices A=0,C=1,G=2,T=3",
                      "Klein-group addition description")
        self.char_table = group["character_table_rows_A_C_G_T"]
        require_equal(self.char_table,
                      [[1, 1, 1, 1], [1, 1, -1, -1],
                       [1, -1, 1, -1], [1, -1, -1, 1]],
                      "Klein character table")

    # ---- General exact checks ------------------------------------------------

    def verify_field(self) -> None:
        field = self.cert["field"]
        require(isinstance(field, Mapping), "field data")
        require_equal(field["generator"], "h", "field generator")
        require_equal(field["minimal_polynomial"], "5*h^4-1", "minimal polynomial text")
        require_equal(field["relation"], "h^4=1/5", "field relation text")
        require_equal(field["basis"], ["1", "h", "h^2", "h^3"], "field basis labels")
        require_equal(
            field["encoding"],
            "[c0,c1,c2,c3] means c0+c1*h+c2*h^2+c3*h^3",
            "field tuple encoding",
        )
        require_equal(field["number_field"], "Q(h)", "number-field label")
        require(Fraction(0) < self.lo < self.hi < Fraction(1), "invalid positive isolating interval")
        f_lo = 5 * self.lo ** 4 - 1
        f_hi = 5 * self.hi ** 4 - 1
        require(f_lo < 0 < f_hi, "interval does not isolate a root of 5*h^4-1")
        # The polynomial is strictly increasing on the positive axis, so this
        # sign change isolates the unique positive root.
        # If y=1/h then y^4-5=0.  That reciprocal polynomial is Eisenstein at
        # 5, so it is irreducible over Q and the four displayed powers are a
        # genuine field basis rather than merely a quotient-ring convention.
        reciprocal = [-5, 0, 0, 0, 1]
        require(reciprocal[-1] % 5 != 0, "Eisenstein leading coefficient")
        require(all(coefficient % 5 == 0 for coefficient in reciprocal[:-1]),
                "Eisenstein nonleading coefficients")
        require(reciprocal[0] % 25 != 0, "Eisenstein constant coefficient")
        h = Alg.h()
        require_zero((h * h * h * h).scale(5) - Alg.one(), "quartic relation")
        print("[field] PASS  irreducible Q(h), h^4=1/5, basis 1,h,h^2,h^3, with 2/3 < h < 7/10")

    # ---- Topology and root suppression --------------------------------------

    def verify_topology(self) -> None:
        require(len(self.edge_row_by_id) == len(self.arc_rows), "duplicate arc identifier")
        directed = list(self.edge_endpoints.values())
        topological_order(self.nodes, directed)

        indegree = {v: 0 for v in self.nodes}
        outdegree = {v: 0 for v in self.nodes}
        children: Dict[str, List[str]] = {v: [] for v in self.nodes}
        for u, v in directed:
            indegree[v] += 1
            outdegree[u] += 1
            children[u].append(v)
        target_degree = {
            "root": (0, 2),
            "tree": (1, 2),
            "reticulation": (2, 1),
            "leaf": (1, 0),
        }
        for v, typ in self.vertex_type.items():
            require(typ in target_degree, f"unknown vertex type {typ!r}")
            require_equal((indegree[v], outdegree[v]), target_degree[typ], f"binary degree at {v}")
        roots = [v for v in self.nodes if self.vertex_type[v] == "root"]
        require_equal(roots, ["rho"], "unique root")
        require_equal(reachable("rho", children), set(self.nodes), "root reachability")

        for retic in self.retic_rows:
            require(isinstance(retic, Mapping), "reticulation row must be a mapping")
            vertex = str(retic["vertex"])
            incoming = retic["incoming"]
            require(isinstance(incoming, list), f"incoming rows at {vertex}")
            for descriptor in incoming:
                require(isinstance(descriptor, Mapping),
                        f"incoming reticulation descriptor at {vertex}")
                edge_id = str(descriptor["edge_id"])
                require(edge_id in self.edge_endpoints,
                        f"reticulation descriptor references unknown edge {edge_id}")
                actual_parent, actual_child = self.edge_endpoints[edge_id]
                require_equal(str(descriptor["parent"]), actual_parent,
                              f"reticulation descriptor parent for {edge_id}")
                require_equal(actual_child, vertex,
                              f"reticulation descriptor child for {edge_id}")
                require_equal(str(descriptor["choice"]), actual_parent,
                              f"reticulation descriptor choice for {edge_id}")
        require_equal(self.retic_rows, EXPECTED_RETICULATION_ROWS,
                      "canonical ordered reticulation descriptors")
        rooted = self.cert["rooted_network"]
        require(isinstance(rooted, Mapping), "rooted-network certificate")
        require_equal(rooted["display_choice_order"], ["r2", "r3"],
                      "reticulation display-choice order")
        require_equal(rooted["choice_index_meaning"],
                      {"0": "incoming edge from p", "1": "incoming edge from q"},
                      "reticulation choice-index semantics")

        suppression = self.cert["root_suppression"]
        require(isinstance(suppression, Mapping), "missing root suppression data")
        require_equal(suppression["removed_vertex"], "rho", "suppressed root")
        require_equal(set(suppression["removed_arcs"]), {"e_rho_1", "e_rho_u"},
                      "suppressed root arcs")
        root_children = sorted(children["rho"])
        require_equal(root_children, ["1", "u"], "root children")

        semi_rows = suppression["effective_semi_directed_edges"]
        require(isinstance(semi_rows, list), "effective semi-directed edges")
        semi_by_id = {str(row["id"]): row for row in semi_rows}
        require(len(semi_by_id) == len(semi_rows), "duplicate semi-directed edge identifier")
        require_equal(set(semi_by_id),
                      {"e_1_u", "e_u_p", "e_u_q", "e_p_r2", "e_q_r2",
                       "e_p_r3", "e_q_r3", "e_r2_2", "e_r3_3"},
                      "effective semi-directed edge identifiers")
        require("e_1_u" in semi_by_id, "suppressed edge e_1_u is missing")
        require_equal(set(semi_by_id["e_1_u"]["endpoints"]), {"1", "u"},
                      "suppressed edge endpoints")
        require_equal(semi_by_id["e_1_u"]["kind"], "undirected", "suppressed edge kind")
        require_equal(semi_by_id["e_1_u"]["vector_name"], "K_odot_K",
                      "suppressed edge vector name")
        require_equal(semi_by_id["e_1_u"]["source_edges"], ["e_rho_1", "e_rho_u"],
                      "suppressed edge sources")
        expected_composite = [
            a * b for a, b in zip(self.edge_eigen["e_rho_1"], self.edge_eigen["e_rho_u"])
        ]
        stored_composite = parse_vector(semi_by_id["e_1_u"]["eigen"])
        require_equal(stored_composite, expected_composite, "K odot K root-suppressed eigenvector")
        require_equal(stored_composite,
                      [Alg.one(), Alg.rational(Fraction(1, 4)),
                       Alg.rational(Fraction(1, 4)), Alg.rational(Fraction(1, 4))],
                      "explicit K odot K vector")
        expected_probs = inverse_fourier_edge_probabilities(stored_composite)
        require_equal(expected_probs, parse_vector(semi_by_id["e_1_u"]["transition_probabilities"]),
                      "suppressed-edge transition probabilities")
        require_equal(expected_probs,
                      [Alg.rational(Fraction(7, 16)), Alg.rational(Fraction(3, 16)),
                       Alg.rational(Fraction(3, 16)), Alg.rational(Fraction(3, 16))],
                      "explicit suppressed-edge probabilities")

        for edge_id in self.edge_row_by_id:
            if edge_id in {"e_rho_1", "e_rho_u"}:
                continue
            row = semi_by_id[edge_id]
            source = self.edge_row_by_id[edge_id]
            require_equal(row["source_edges"], [edge_id],
                          f"singleton root-suppression source binding for {edge_id}")
            require_equal(set(row["endpoints"]), set(self.edge_endpoints[edge_id]),
                          f"root-suppression endpoints for {edge_id}")
            require_equal(row["vector_name"], source["vector_name"],
                          f"root-suppression vector name for {edge_id}")
            require_equal(parse_vector(row["eigen"]), parse_vector(source["eigen"]),
                          f"root-suppression eigenvector for {edge_id}")
            require_equal(parse_vector(row["transition_probabilities"]),
                          parse_vector(source["transition_probabilities"]),
                          f"root-suppression probabilities for {edge_id}")

        # Verify every non-root arc appears exactly once in the suppressed graph.
        expected_source_sets = {
            frozenset([edge_id]) for edge_id in self.edge_row_by_id
            if edge_id not in {"e_rho_1", "e_rho_u"}
        } | {frozenset(["e_rho_1", "e_rho_u"])}
        actual_source_sets = {frozenset(row["source_edges"]) for row in semi_rows}
        require_equal(actual_source_sets, expected_source_sets, "root-suppression edge accounting")

        semi_nodes = set(self.nodes) - {"rho"}
        semi_edges_by_id = {
            edge_id: frozenset(str(x) for x in row["endpoints"])
            for edge_id, row in semi_by_id.items()
        }
        semi_edges = set(semi_edges_by_id.values())
        require(len(semi_edges) == len(semi_edges_by_id), "duplicate underlying semi-directed edge")
        bridges = bridge_edges(semi_nodes, semi_edges)
        bridge_ids = {edge_id for edge_id, edge in semi_edges_by_id.items() if edge in bridges}
        require_equal(bridge_ids, {"e_1_u", "e_r2_2", "e_r3_3"}, "three pendant cut edges")

        nonbridges = semi_edges - bridges
        nonbridge_components = [c for c in undirected_components(semi_nodes, nonbridges) if len(c) > 1]
        require_equal(nonbridge_components, [{"u", "p", "q", "r2", "r3"}],
                      "maximal nontrivial blob")
        core = nonbridge_components[0]
        core_edge_ids = {
            edge_id for edge_id, edge in semi_edges_by_id.items() if edge.issubset(core)
        }
        require_equal(core_edge_ids,
                      {"e_u_p", "e_u_q", "e_p_r2", "e_q_r2", "e_p_r3", "e_q_r3"},
                      "theta-core edges")

        # Theta graph: p and q have core degree 3, and u,r2,r3 each form a
        # distinct length-two p-q path.
        core_adj: Dict[str, Set[str]] = {v: set() for v in core}
        for edge_id in core_edge_ids:
            u, v = tuple(semi_edges_by_id[edge_id])
            core_adj[u].add(v)
            core_adj[v].add(u)
        require_equal({v: len(nbrs) for v, nbrs in core_adj.items()},
                      {"p": 3, "q": 3, "u": 2, "r2": 2, "r3": 2},
                      "theta-core degrees")
        for middle in ("u", "r2", "r3"):
            require_equal(core_adj[middle], {"p", "q"}, f"theta path through {middle}")
        theta = suppression["theta_core"]
        require(isinstance(theta, Mapping), "theta-core certificate")
        require_equal(set(theta["vertices"]), core, "certified theta-core vertices")
        require_equal(set(theta["edges"]), core_edge_ids, "certified theta-core edges")
        require_equal({tuple(path) for path in theta["three_p_q_paths"]},
                      {("p", "u", "q"), ("p", "r2", "q"), ("p", "r3", "q")},
                      "three certified p-q paths")

        # Each bridge incident to the core leads to exactly one labelled leaf.
        incident_leaf_components: List[Set[str]] = []
        for bridge_id in sorted(bridge_ids):
            edge = semi_edges_by_id[bridge_id]
            require(len(edge & core) == 1, f"bridge {bridge_id} is not incident to the core")
            outside_endpoint = next(v for v in edge if v not in core)
            outside_nodes = semi_nodes - core
            outside_edges = {
                e for e in semi_edges if e.issubset(outside_nodes)
            }
            comp = next(c for c in undirected_components(outside_nodes, outside_edges)
                        if outside_endpoint in c)
            incident_leaf_components.append({v for v in comp if self.vertex_type[v] == "leaf"})
        require_equal({frozenset(c) for c in incident_leaf_components},
                      {frozenset(["1"]), frozenset(["2"]), frozenset(["3"])},
                      "three incident leaf components")

        retics_in_core = {v for v in core if self.vertex_type[v] == "reticulation"}
        require_equal(retics_in_core, {"r2", "r3"}, "reticulations in theta blob")
        require_equal(theta["level"], 2, "certified blob level")
        # There is one nontrivial blob, and it contains exactly two
        # reticulations, so the trinet is strict level two.
        require(len(retics_in_core) == 2, "strict level-two condition")

        # Reticulation arcs retain their directions; all other effective edges
        # are undirected in the semi-directed representation.
        for edge_id, row in semi_by_id.items():
            if edge_id in {"e_p_r2", "e_q_r2", "e_p_r3", "e_q_r3"}:
                require_equal(row["kind"], "reticulation_arc", f"kind of {edge_id}")
                require_equal(tuple(row["direction"]), self.edge_endpoints[edge_id],
                              f"direction of {edge_id}")
            else:
                require_equal(row["kind"], "undirected", f"kind of {edge_id}")

        # Audit the three literal printed clauses of the source paper's
        # 2-sub-blob definition.  This is deliberately separate from the
        # theorem: the theorem needs only the unambiguous maximal theta
        # 3-blob facts above.
        literal = suppression["literal_two_sub_blob_audit"]
        require(isinstance(literal, Mapping), "literal 2-sub-blob audit")
        qualifying: List[Set[str]] = []
        ordered_nodes = sorted(semi_nodes)
        for size in range(1, len(ordered_nodes)):
            for chosen in itertools.combinations(ordered_nodes, size):
                w = set(chosen)
                induced = {edge for edge in semi_edges if edge.issubset(w)}
                if not connected(w, induced):
                    continue
                if induced & bridges:
                    continue
                boundary_vertices = {
                    v for v in w
                    if any(v in edge and not edge.issubset(w) for edge in semi_edges)
                }
                if len(boundary_vertices) == 2:
                    qualifying.append(w)
        expected_literal_sets = {
            frozenset(("p", "u")), frozenset(("q", "u")),
            frozenset(("p", "r2")), frozenset(("q", "r2")),
            frozenset(("p", "r3")), frozenset(("q", "r3")),
        }
        require_equal({frozenset(w) for w in qualifying}, expected_literal_sets,
                      "literal three-clause 2-sub-blob enumeration")
        require_equal({frozenset(x) for x in literal["qualifying_vertex_sets"]},
                      expected_literal_sets, "stored literal 2-sub-blob sets")
        literal_edge_ids: Set[str] = set()
        for w in qualifying:
            induced_ids = {
                edge_id for edge_id, edge in semi_edges_by_id.items()
                if edge.issubset(w)
            }
            require(len(induced_ids) == 1,
                    f"literal qualifying set {sorted(w)} is not a single edge")
            literal_edge_ids |= induced_ids
            crossing = [edge for edge in semi_edges if len(edge & w) == 1]
            require(len(crossing) == 4,
                    f"contracting {sorted(w)} does not have four external incidences")
        require_equal(literal_edge_ids, set(literal["qualifying_edge_ids"]),
                      "literal qualifying edge identifiers")
        require_equal(literal["count"], 6, "literal qualifying-set count")
        require_equal(literal["each_induced_subgraph_is_one_edge"], True,
                      "literal sets are individual edges")
        require_equal(literal["crossing_edge_count_after_contraction"], 4,
                      "four incidences after literal edge contraction")
        require_equal(literal["ordinary_degree_two_suppression_applicable"], False,
                      "ordinary degree-two suppression flag")
        require_equal(literal["theorem_depends_on_suppressing_them"], False,
                      "theorem independence from terminology")

        # Independently audit the alternative criterion that is compatible
        # with the ensuing degree-two suppression instruction: clauses (i)
        # and (ii), but exactly two crossing edge incidences rather than two
        # boundary vertices.  No proper induced subgraph of this theta meets
        # that criterion.
        suppressible = suppression["degree_two_suppressible_audit"]
        require(isinstance(suppressible, Mapping), "degree-two suppressible audit")
        degree_two_sets: List[Set[str]] = []
        for size in range(1, len(ordered_nodes)):
            for chosen in itertools.combinations(ordered_nodes, size):
                w = set(chosen)
                induced = {edge for edge in semi_edges if edge.issubset(w)}
                if not connected(w, induced):
                    continue
                if induced & bridges:
                    continue
                crossing = [edge for edge in semi_edges if len(edge & w) == 1]
                if len(crossing) == 2:
                    degree_two_sets.append(w)
        require_equal(degree_two_sets, [], "degree-two/edge-incidence enumeration")
        require_equal(suppressible["qualifying_vertex_sets"], [],
                      "stored degree-two qualifying sets")
        require_equal(suppressible["count"], 0,
                      "degree-two qualifying-set count")
        require_equal(suppressible["proper_nontrivial_cyclic_two_terminal_substructure_exists"],
                      False, "no proper cyclic two-terminal suppressible substructure")

        print("[topology] PASS  rooted binary DAG and correct semi-directed root suppression")
        print("[topology] PASS  maximal theta 3-blob with three leaf sides and two reticulations")
        print("[topology] PASS  literal three-clause audit finds exactly six single-edge sets; each contracts to four incidences")
        print("[topology] PASS  edge-incidence/degree-two audit finds no proper suppressible substructure")

    # ---- Symmetric construction ansatz --------------------------------------

    def verify_construction_ansatz(self) -> None:
        ansatz = self.cert["construction_ansatz"]
        require(isinstance(ansatz, Mapping), "construction ansatz")
        vectors = self.cert["parameter_vectors"]
        require(isinstance(vectors, Mapping), "parameter vectors for ansatz")
        u = parse_vector(vectors["U"]["eigen"])
        v = parse_vector(vectors["V"]["eigen"])
        s = parse_vector(vectors["S"]["eigen"])
        t = parse_vector(vectors["T"]["eigen"])
        tau = parse_alg(ansatz["tau"])
        sigma = parse_alg(ansatz["sigma"])
        b = parse_alg(ansatz["b"])
        kappa = parse_alg(ansatz["kappa"])
        d = parse_alg(ansatz["d"])
        e = parse_alg(ansatz["e"])
        r = parse_alg(ansatz["r"])
        one = Alg.one()
        h = Alg.h()
        h2 = h * h

        require_equal(u, [one, b * tau, b, tau], "U symmetric-ansatz form")
        require_equal(v, [one, b, b * tau, tau], "V symmetric-ansatz form")
        require_equal(s, [one, kappa * d, d, e], "S symmetric-ansatz form")
        require_equal(t, [one, d, kappa * d, e], "T symmetric-ansatz form")
        require_equal(tau, Alg.rational(Fraction(1, 3)), "ansatz tau")
        require_equal(b, h, "positive ansatz branch b=h")
        require_equal(kappa, h2.scale(3), "ansatz kappa=3h^2")
        require_equal(d, Alg.rational(Fraction(1, 4)), "ansatz d")
        require_equal(e, Alg.rational(Fraction(3, 10)), "ansatz e")
        require_equal(r, h2.scale(Fraction(1, 2)), "ansatz r")
        require_equal(sigma, h2.scale(Fraction(10, 3)), "ansatz sigma")

        sigma_residual = sigma * sigma - (one + tau * tau).scale(2)
        shape_1 = (kappa * (one + tau * tau) + tau.scale(2)
                   - sigma * (kappa * tau + one))
        shape_2 = ((kappa * tau).scale(2)
                   + b * b * (kappa * kappa * tau * tau + one)
                   - (tau.scale(2) / sigma)
                   * (kappa * kappa + one + (kappa * b * b * tau).scale(2)))
        scale_residual = ((e / d) * (e / d)
                          - (kappa * kappa + one + (kappa * b * b * tau).scale(2))
                          / ((one + tau * tau).scale(2)))
        require_zero(sigma_residual, "ansatz sigma relation")
        require_zero(shape_1, "ansatz first shape equation")
        require_zero(shape_2, "ansatz second shape equation")
        require_zero(scale_residual, "ansatz scale equation")
        require_equal(sigma_residual, parse_alg(ansatz["sigma_relation_residual"]),
                      "stored sigma residual")
        require_equal(shape_1, parse_alg(ansatz["shape_equation_1_residual"]),
                      "stored first shape residual")
        require_equal(shape_2, parse_alg(ansatz["shape_equation_2_residual"]),
                      "stored second shape residual")
        require_equal(scale_residual, parse_alg(ansatz["scale_equation_residual"]),
                      "stored scale residual")
        require_zero((b * b) - h2, "b^2=h^2")
        require_zero((b * b) * (b * b) - Alg.rational(Fraction(1, 5)),
                     "b^4=1/5")
        require_equal(e / d, Alg.rational(Fraction(6, 5)), "ansatz e/d")
        for name, value in (("b", b), ("kappa", kappa), ("d", d),
                            ("e", e), ("r", r), ("sigma", sigma)):
            require_positive(value, self.lo, self.hi, f"positive ansatz parameter {name}")

        print("[construction] PASS  C/G-symmetric ansatz reduction verified exactly")
        print("[construction] PASS  tau=1/3 forces kappa=3h^2 and b=h on the positive quartic branch")

    # ---- Edge admissibility --------------------------------------------------

    def check_edge_vector(self, name: str, eigen: Sequence[Alg], stored_probs: Sequence[Alg]) -> None:
        require_equal(eigen[0], Alg.one(), f"identity eigenvalue on {name}")
        for symbol, value in zip(self.symbols[1:], eigen[1:]):
            require_between_zero_one(value, self.lo, self.hi, f"{name}.a_{symbol}")
        calculated = inverse_fourier_edge_probabilities(eigen)
        require_equal(calculated, list(stored_probs), f"inverse Fourier probabilities on {name}")
        total = Alg.zero()
        for i, value in enumerate(calculated):
            require_positive(value, self.lo, self.hi, f"{name} transition probability {self.symbols[i]}")
            total = total + value
        require_equal(total, Alg.one(), f"transition-probability sum on {name}")

    def verify_parameters(self) -> None:
        vector_rows = self.cert["parameter_vectors"]
        require(isinstance(vector_rows, Mapping), "parameter vectors")
        for name, row in vector_rows.items():
            require(isinstance(row, Mapping), f"parameter vector {name}")
            eigen = parse_vector(row["eigen"])
            stored_probs = parse_vector(row["transition_probabilities"])
            self.check_edge_vector(str(name), eigen, stored_probs)
            expected_margins = ct_margins(eigen)
            stored_margins = {k: parse_alg(v) for k, v in row["continuous_time_margins"].items()}
            require_equal(stored_margins, expected_margins, f"continuous-time margins on {name}")

        # Each rooted arc must reproduce its named vector and probabilities.
        for edge_id, row in self.edge_row_by_id.items():
            vector_name = str(row["vector_name"])
            vector = vector_rows[vector_name]
            require_equal(parse_vector(row["eigen"]), parse_vector(vector["eigen"]),
                          f"named vector on rooted edge {edge_id}")
            require_equal(parse_vector(row["transition_probabilities"]),
                          parse_vector(vector["transition_probabilities"]),
                          f"named probabilities on rooted edge {edge_id}")

        # The only certified compatible theta rooting is the u-side split of
        # the effective terminal-1 edge, and both root-adjacent arcs are the
        # literal vector K (not merely two unspecified factors with product
        # K odot K).
        root_k = parse_vector(vector_rows["K"]["eigen"])
        for edge_id in ("e_rho_1", "e_rho_u"):
            row = self.edge_row_by_id[edge_id]
            require_equal(str(row["vector_name"]), "K",
                          f"literal K assignment on rooted edge {edge_id}")
            require_equal(parse_vector(row["eigen"]), root_k,
                          f"literal K eigenvector on rooted edge {edge_id}")

        # Effective semi-directed edges, including K odot K.
        suppression = self.cert["root_suppression"]
        require(isinstance(suppression, Mapping), "root suppression")
        for row in suppression["effective_semi_directed_edges"]:
            eigen = parse_vector(row["eigen"])
            stored_probs = parse_vector(row["transition_probabilities"])
            self.check_edge_vector(f"semi-directed {row['id']}", eigen, stored_probs)
            require_equal(eigen, parse_vector(vector_rows[row["vector_name"]]["eigen"]),
                          f"named effective vector {row['id']}")

        # Tree edges.
        tree = self.cert["comparison_tree"]
        require(isinstance(tree, Mapping), "comparison tree")
        leaf_vectors = tree["leaf_edge_vectors"]
        require(isinstance(leaf_vectors, Mapping), "comparison-tree edge vectors")
        for leaf, row in leaf_vectors.items():
            eigen = parse_vector(row["eigen"])
            stored_probs = parse_vector(row["transition_probabilities"])
            self.check_edge_vector(f"tree leaf {leaf}", eigen, stored_probs)
            expected_margins = ct_margins(eigen)
            stored_margins = {k: parse_alg(v) for k, v in row["continuous_time_margins"].items()}
            require_equal(stored_margins, expected_margins,
                          f"comparison-tree continuous-time margins at leaf {leaf}")
            for margin_name, value in expected_margins.items():
                require_positive(value, self.lo, self.hi,
                                 f"comparison-tree strict margin at leaf {leaf}.{margin_name}")

        # Inheritance probabilities.
        require_equal({str(r["vertex"]) for r in self.retic_rows}, {"r2", "r3"},
                      "reticulation list")
        for retic in self.retic_rows:
            incoming = retic["incoming"]
            require(isinstance(incoming, list) and len(incoming) == 2,
                    f"two incoming edges at {retic['vertex']}")
            weights = [parse_fraction(row["weight"]) for row in incoming]
            require_equal(weights, [Fraction(1, 2), Fraction(1, 2)],
                          f"inheritance weights at {retic['vertex']}")
            require(sum(weights) == 1 and all(0 < w < 1 for w in weights),
                    f"nontrivial inheritance probabilities at {retic['vertex']}")
            expected_edges = {edge_id for edge_id, (_, child) in self.edge_endpoints.items()
                              if child == retic["vertex"]}
            require_equal({str(row["edge_id"]) for row in incoming}, expected_edges,
                          f"incoming reticulation edges at {retic['vertex']}")

        print("[parameters] PASS  every network/effective/tree edge lies in Theta_0^circ")
        print("[parameters] PASS  every transition probability is strictly positive")
        print("[parameters] PASS  both inheritance parameters equal 1/2")
        print("[root splitting] PASS  all three comparison-tree edges admit strict stochastic half-time roots")
        print("[root splitting] PASS  only the compatible u-side theta rooting is certified by K odot K")

    # ---- Displayed trees and Fourier coordinates ----------------------------

    def retained_display(self, choices: Tuple[int, int]) -> Tuple[List[str], Fraction]:
        require(len(choices) == len(self.retic_rows) == 2, "two reticulation choices required")
        retained = list(self.edge_row_by_id)
        weight = Fraction(1)
        for choice, retic in zip(choices, self.retic_rows):
            incoming = retic["incoming"]
            require(isinstance(incoming, list), "reticulation incoming list")
            chosen = incoming[choice]
            deleted = incoming[1 - choice]
            retained.remove(str(deleted["edge_id"]))
            weight *= parse_fraction(chosen["weight"])
        return retained, weight

    def display_children(self, retained: Sequence[str]) -> Dict[str, List[str]]:
        children: Dict[str, List[str]] = {v: [] for v in self.nodes}
        indegree = {v: 0 for v in self.nodes}
        for edge_id in retained:
            u, v = self.edge_endpoints[edge_id]
            children[u].append(v)
            indegree[v] += 1
        require(indegree["rho"] == 0 and all(indegree[v] == 1 for v in self.nodes if v != "rho"),
                "a displayed choice does not produce a rooted tree")
        require_equal(reachable("rho", children), set(self.nodes), "displayed-tree reachability")
        return children

    def edge_character(self, edge_id: str, labels: Tuple[int, int, int],
                       retained: Sequence[str], children: Mapping[str, Sequence[str]] | None = None) -> int:
        if children is None:
            children = self.display_children(retained)
        _, child = self.edge_endpoints[edge_id]
        below = reachable(child, children)
        character = 0
        for leaf, position in self.leaf_position.items():
            if leaf in below:
                character ^= labels[position]
        return character

    def displayed_monomial(self, labels: Tuple[int, int, int], choices: Tuple[int, int]) -> Alg:
        retained, _ = self.retained_display(choices)
        children = self.display_children(retained)
        term = Alg.one()
        for edge_id in retained:
            term = term * self.edge_eigen[edge_id][
                self.edge_character(edge_id, labels, retained, children)
            ]
        return term

    def network_fourier(self, labels: Tuple[int, int, int]) -> Alg:
        if labels[0] ^ labels[1] ^ labels[2]:
            return Alg.zero()
        total = Alg.zero()
        for choices in itertools.product((0, 1), repeat=2):
            _, weight = self.retained_display(choices)
            total = total + self.displayed_monomial(labels, choices).scale(weight)
        return total

    def tree_vectors(self) -> Dict[str, List[Alg]]:
        tree = self.cert["comparison_tree"]
        require(isinstance(tree, Mapping), "comparison tree")
        require_equal(tree["topology"], "semi-directed three-star on leaves 1,2,3",
                      "comparison-tree topology")
        expected_names = {"1": "alpha", "2": "beta", "3": "gamma"}
        require_equal({str(leaf): str(row["name"])
                       for leaf, row in tree["leaf_edge_vectors"].items()},
                      expected_names, "comparison-tree edge names")
        return {
            str(leaf): parse_vector(row["eigen"])
            for leaf, row in tree["leaf_edge_vectors"].items()
        }

    def tree_fourier(self, labels: Tuple[int, int, int]) -> Alg:
        if labels[0] ^ labels[1] ^ labels[2]:
            return Alg.zero()
        vectors = self.tree_vectors()
        x, y, z = labels
        return vectors["1"][x] * vectors["2"][y] * vectors["3"][z]

    def pattern_probability(self, q: Mapping[Tuple[int, int, int], Alg],
                            pattern: Tuple[int, int, int]) -> Alg:
        total = Alg.zero()
        a, b, c = pattern
        for x, y, z in itertools.product(range(4), repeat=3):
            sign = self.char_table[x][a] * self.char_table[y][b] * self.char_table[z][c]
            total = total + q[(x, y, z)].scale(Fraction(sign, 64))
        return total

    def direct_display_probability(self, pattern: Tuple[int, int, int],
                                   choices: Tuple[int, int]) -> Alg:
        """Ordinary-state pruning on one literal retained rooted graph."""
        retained, _ = self.retained_display(choices)
        retained_edges = [self.edge_endpoints[edge_id] for edge_id in retained]
        order = topological_order(self.nodes, retained_edges)
        children: Dict[str, List[Tuple[str, str]]] = {node: [] for node in self.nodes}
        for edge_id in retained:
            parent, child = self.edge_endpoints[edge_id]
            children[parent].append((edge_id, child))
        transitions = {
            edge_id: inverse_fourier_edge_probabilities(self.edge_eigen[edge_id])
            for edge_id in retained
        }
        observed_state = {
            leaf: pattern[position] for leaf, position in self.leaf_position.items()
        }
        likelihood: Dict[str, List[Alg]] = {}
        for node in reversed(order):
            if node in observed_state:
                likelihood[node] = [
                    Alg.one() if state == observed_state[node] else Alg.zero()
                    for state in range(4)
                ]
                continue
            values: List[Alg] = []
            for parent_state in range(4):
                product_value = Alg.one()
                for edge_id, child in children[node]:
                    subtotal = Alg.zero()
                    for child_state in range(4):
                        transition = transitions[edge_id][parent_state ^ child_state]
                        subtotal = subtotal + transition * likelihood[child][child_state]
                    product_value = product_value * subtotal
                values.append(product_value)
            likelihood[node] = values
        return sum(
            (value.scale(Fraction(1, 4)) for value in likelihood["rho"]), Alg.zero()
        )

    def direct_tree_probability(self, pattern: Tuple[int, int, int]) -> Alg:
        """Ordinary-state calculation on the comparison three-star."""
        transitions = {
            leaf: inverse_fourier_edge_probabilities(vector)
            for leaf, vector in self.tree_vectors().items()
        }
        total = Alg.zero()
        for root_state in range(4):
            term = Alg.rational(Fraction(1, 4))
            for leaf, position in self.leaf_position.items():
                term = term * transitions[leaf][root_state ^ pattern[position]]
            total = total + term
        return total

    def verify_direct_state_space(
        self,
        q_network: Mapping[Tuple[int, int, int], Alg],
        q_tree: Mapping[Tuple[int, int, int], Alg],
    ) -> None:
        """Cross-check the K3P collision without Fourier monomial evaluation."""
        for pattern in itertools.product(range(4), repeat=3):
            direct_network = Alg.zero()
            for choices in itertools.product((0, 1), repeat=2):
                _, weight = self.retained_display(choices)
                direct_network = direct_network + self.direct_display_probability(
                    pattern, choices
                ).scale(weight)
            direct_tree = self.direct_tree_probability(pattern)
            fourier_network = self.pattern_probability(q_network, pattern)
            fourier_tree = self.pattern_probability(q_tree, pattern)
            label = "".join(self.symbols[index] for index in pattern)
            require_equal(direct_network, direct_tree,
                          f"direct K3P network/tree probability at {label}")
            require_equal(direct_network, fourier_network,
                          f"direct/Fourier K3P network probability at {label}")
            require_equal(direct_tree, fourier_tree,
                          f"direct/Fourier K3P tree probability at {label}")
        print("[direct probabilities] PASS  exact K3P Markov pruning on all four retained graphs matches the comparison tree and Fourier inversion for all 64 patterns")

    def verify_collision(self) -> Tuple[Dict[Tuple[int, int, int], Alg], Dict[Tuple[int, int, int], Alg]]:
        vector_rows = self.cert["parameter_vectors"]
        require(isinstance(vector_rows, Mapping), "parameter vectors")
        vectors = {name: parse_vector(row["eigen"]) for name, row in vector_rows.items()}
        K, U, V, S, T = (vectors[name] for name in ("K", "U", "V", "S", "T"))

        core = self.cert["core_factorization"]
        require(isinstance(core, Mapping), "core factorization")
        require_equal(core["row_order"], self.symbols, "core row order")
        require_equal(core["column_order"], self.symbols, "core column order")
        require_equal(core["displayed_choice_order"], ["p,p", "p,q", "q,p", "q,q"],
                      "displayed core choice order")
        stored_terms = core["displayed_core_terms"]
        stored_m = [parse_alg(x) for x in core["M_entries_row_major"]]
        stored_factor = [parse_alg(x) for x in core["factorized_entries_row_major"]]
        P = parse_vector(core["P"])
        B = parse_vector(core["B"])
        require(len(stored_terms) == len(stored_m) == len(stored_factor) == 16,
                "core certificate must contain sixteen entries")

        for y, z in itertools.product(range(4), repeat=2):
            x = y ^ z
            terms = [
                S[y] * S[z] * U[x],
                S[y] * T[z] * U[y] * V[z],
                T[y] * S[z] * U[z] * V[y],
                T[y] * T[z] * V[x],
            ]
            position = 4 * y + z
            require_equal(terms, [parse_alg(t) for t in stored_terms[position]],
                          f"four displayed core terms at {(self.symbols[y], self.symbols[z])}")
            average = sum((term.scale(Fraction(1, 4)) for term in terms), Alg.zero())
            factor = P[x] * B[y] * B[z]
            require_equal(average, stored_m[position], f"core M entry at {(y,z)}")
            require_equal(factor, stored_factor[position], f"factorized core entry at {(y,z)}")
            require_equal(average, factor, f"M[y,z]=P[y+z]B[y]B[z] at {(y,z)}")

            # Independently connect each core term to the corresponding full
            # displayed-tree monomial by restoring the four K factors.
            labels = (x, y, z)
            common_k = K[x] * K[x] * K[y] * K[z]
            for choices, term in zip(itertools.product((0, 1), repeat=2), terms):
                require_equal(self.displayed_monomial(labels, choices), common_k * term,
                              f"full displayed contribution for labels {labels}, choices {choices}")

        triples = list(itertools.product(range(4), repeat=3))
        expected_order = ["".join(self.symbols[i] for i in triple) for triple in triples]
        q_cert = self.cert["fourier_coordinates"]
        require(isinstance(q_cert, Mapping), "Fourier coordinate certificate")
        require_equal(q_cert["order"], expected_order, "Fourier coordinate order")
        stored_network = [parse_alg(x) for x in q_cert["network"]]
        stored_tree = [parse_alg(x) for x in q_cert["tree"]]
        require(len(stored_network) == len(stored_tree) == 64, "sixty-four Fourier coordinates")

        q_network: Dict[Tuple[int, int, int], Alg] = {}
        q_tree: Dict[Tuple[int, int, int], Alg] = {}
        consistent_count = 0
        inconsistent_count = 0
        for position, triple in enumerate(triples):
            qn = self.network_fourier(triple)
            qt = self.tree_fourier(triple)
            q_network[triple] = qn
            q_tree[triple] = qt
            require_equal(qn, stored_network[position], f"stored network Fourier coordinate {expected_order[position]}")
            require_equal(qt, stored_tree[position], f"stored tree Fourier coordinate {expected_order[position]}")
            require_equal(qn, qt, f"network/tree Fourier equality at {expected_order[position]}")
            if triple[0] ^ triple[1] ^ triple[2]:
                inconsistent_count += 1
                require_zero(qn, f"inconsistent Fourier coordinate {expected_order[position]}")
            else:
                consistent_count += 1
                require_positive(qn, self.lo, self.hi,
                                 f"consistent Fourier coordinate {expected_order[position]}")
        require_equal((consistent_count, inconsistent_count), (16, 48),
                      "consistent/inconsistent Fourier counts")
        require_equal(q_network[(0, 0, 0)], Alg.one(), "q_AAA normalization")

        # Inverse finite Fourier transform on all sixty-four patterns.
        pattern_cert = self.cert["leaf_pattern_probabilities"]
        require(isinstance(pattern_cert, Mapping), "leaf-pattern certificate")
        require_equal(pattern_cert["order"], expected_order, "leaf-pattern order")
        stored_pattern_network = [parse_alg(x) for x in pattern_cert["network"]]
        stored_pattern_tree = [parse_alg(x) for x in pattern_cert["tree"]]
        require(len(stored_pattern_network) == len(stored_pattern_tree) == 64,
                "sixty-four leaf-pattern probabilities")
        sum_network = Alg.zero()
        sum_tree = Alg.zero()
        for position, pattern in enumerate(triples):
            pn = self.pattern_probability(q_network, pattern)
            pt = self.pattern_probability(q_tree, pattern)
            require_equal(pn, stored_pattern_network[position],
                          f"stored network pattern probability {expected_order[position]}")
            require_equal(pt, stored_pattern_tree[position],
                          f"stored tree pattern probability {expected_order[position]}")
            require_equal(pn, pt, f"network/tree pattern equality at {expected_order[position]}")
            require_positive(pn, self.lo, self.hi,
                             f"leaf-pattern probability {expected_order[position]}")
            sum_network = sum_network + pn
            sum_tree = sum_tree + pt
        require_equal(sum_network, Alg.one(), "network probability sum")
        require_equal(sum_tree, Alg.one(), "tree probability sum")

        print("[collision] PASS  all four displayed-tree terms reconstructed exactly")
        print("[collision] PASS  all 16 core identities M[y,z]=P[y+z]B[y]B[z]")
        print("[collision] PASS  all 64 Fourier coordinates agree (16 consistent, 48 zero)")
        print("[collision] PASS  all 64 positive leaf-pattern probabilities agree and sum to 1")
        return q_network, q_tree

    def verify_k2p_specialization_scope(
        self,
        q_network: Mapping[Tuple[int, int, int], Alg],
        q_tree: Mapping[Tuple[int, int, int], Alg],
    ) -> None:
        """Separate genuine-K3P parameters from the symmetry of their output.

        A globally character-relabelled K2P edge submodel is obtained by requiring one
        of the three pairs of nonidentity Fourier eigenvalues to be equal on
        every edge.  The U edge alone excludes all three possibilities here.
        The common output nevertheless lies in the C=G globally character-relabelled K2P tree
        submodel.  These are deliberately checked as two different facts.
        """
        vector_rows = self.cert["parameter_vectors"]
        require(isinstance(vector_rows, Mapping), "parameter vectors for K2P-scope audit")
        u = parse_vector(vector_rows["U"]["eigen"])
        u_c, u_g, u_t = u[1], u[2], u[3]
        require_positive(u_g - u_c, self.lo, self.hi, "U_G-U_C")
        require_positive(u_t - u_c, self.lo, self.hi, "U_T-U_C")
        require_positive(u_g - u_t, self.lo, self.hi, "U_G-U_T")

        tree = self.tree_vectors()
        alpha, beta, gamma = tree["1"], tree["2"], tree["3"]
        require_equal(alpha[1], alpha[2], "comparison-tree alpha_C=alpha_G")
        require(alpha[1] != alpha[3], "comparison-tree alpha must not be JC")
        for name, edge in (("beta", beta), ("gamma", gamma)):
            require(edge[1] == edge[2] == edge[3],
                    f"comparison-tree {name} must be JC")

        def swapped(labels: Tuple[int, int, int], left: int, right: int) -> Tuple[int, int, int]:
            permutation = list(range(4))
            permutation[left], permutation[right] = permutation[right], permutation[left]
            return tuple(permutation[value] for value in labels)  # type: ignore[return-value]

        expected_differences = {(1, 2): 0, (1, 3): 8, (2, 3): 8}
        for name, coordinates in (("network", q_network), ("tree", q_tree)):
            require_equal(len(coordinates), 64, f"{name} Fourier coordinate count")
            for pair, expected in expected_differences.items():
                difference_count = sum(
                    coordinates[labels] != coordinates[swapped(labels, *pair)]
                    for labels in coordinates
                )
                require_equal(
                    difference_count,
                    expected,
                    f"{name} output differences under {self.symbols[pair[0]]}<->"
                    f"{self.symbols[pair[1]]}",
                )

        print("[K3P/K2P scope] PASS  U_C,U_G,U_T are pairwise distinct, excluding every globally character-relabelled K2P edge-parameter submodel")
        print("[K3P/K2P scope] PASS  the common output/tree lies in exactly the C=G globally character-relabelled K2P specialization")

    # ---- Jacobian ------------------------------------------------------------

    def derivative_edge(self, labels: Tuple[int, int, int], edge_id: str,
                        character: int) -> Alg:
        if labels[0] ^ labels[1] ^ labels[2]:
            return Alg.zero()
        total = Alg.zero()
        for choices in itertools.product((0, 1), repeat=2):
            retained, weight = self.retained_display(choices)
            if edge_id not in retained:
                continue
            children = self.display_children(retained)
            if self.edge_character(edge_id, labels, retained, children) != character:
                continue
            term = Alg.rational(weight)
            for other in retained:
                if other == edge_id:
                    continue
                term = term * self.edge_eigen[other][
                    self.edge_character(other, labels, retained, children)
                ]
            total = total + term
        return total

    def derivative_delta3_p(self, labels: Tuple[int, int, int]) -> Alg:
        """Derivative when p-parent weight at r3 is delta, q-parent is 1-delta."""
        if labels[0] ^ labels[1] ^ labels[2]:
            return Alg.zero()
        total = Alg.zero()
        for c2, c3 in itertools.product((0, 1), repeat=2):
            retained, _ = self.retained_display((c2, c3))
            # r2 contributes 1/2; d/d delta gives +1 for p (choice 0),
            # -1 for q (choice 1).
            derivative_weight = Fraction(1, 2) if c3 == 0 else Fraction(-1, 2)
            children = self.display_children(retained)
            term = Alg.rational(derivative_weight)
            for edge_id in retained:
                term = term * self.edge_eigen[edge_id][
                    self.edge_character(edge_id, labels, retained, children)
                ]
            total = total + term
        return total

    def jacobian_entry(self, labels: Tuple[int, int, int], column: Mapping[str, object]) -> Alg:
        kind = str(column["kind"])
        if kind == "edge_eigen":
            return self.derivative_edge(labels, str(column["edge_id"]),
                                        self.index[str(column["character"])])
        if kind == "inheritance":
            require_equal(column["reticulation"], "r3", "Jacobian inheritance reticulation")
            require_equal(column["parent_choice"], "p", "Jacobian inheritance parent")
            return self.derivative_delta3_p(labels)
        raise AssertionError(f"unknown Jacobian column kind {kind!r}")

    def verify_jacobian(self) -> Tuple[List[Tuple[int, int, int]], List[Mapping[str, object]], List[List[Alg]]]:
        jac = self.cert["jacobian"]
        require(isinstance(jac, Mapping), "Jacobian certificate")
        expected_rows = [
            triple for triple in itertools.product(range(4), repeat=3)
            if (triple[0] ^ triple[1] ^ triple[2]) == 0 and triple != (0, 0, 0)
        ]
        expected_row_labels = ["".join(self.symbols[i] for i in triple) for triple in expected_rows]
        require_equal(jac["row_indices"], [list(t) for t in expected_rows], "Jacobian row indices")
        require_equal(jac["row_order"], expected_row_labels, "Jacobian row labels")
        columns = jac["column_order"]
        require(isinstance(columns, list) and len(columns) == 15, "fifteen Jacobian columns")
        expected_columns = [
            {"name": "e_rho_1.a_C", "kind": "edge_eigen", "edge_id": "e_rho_1", "character": "C"},
            {"name": "e_rho_1.a_G", "kind": "edge_eigen", "edge_id": "e_rho_1", "character": "G"},
            {"name": "e_rho_1.a_T", "kind": "edge_eigen", "edge_id": "e_rho_1", "character": "T"},
            {"name": "e_u_p.a_G", "kind": "edge_eigen", "edge_id": "e_u_p", "character": "G"},
            {"name": "e_p_r2.a_C", "kind": "edge_eigen", "edge_id": "e_p_r2", "character": "C"},
            {"name": "e_p_r2.a_G", "kind": "edge_eigen", "edge_id": "e_p_r2", "character": "G"},
            {"name": "e_q_r2.a_C", "kind": "edge_eigen", "edge_id": "e_q_r2", "character": "C"},
            {"name": "e_q_r2.a_G", "kind": "edge_eigen", "edge_id": "e_q_r2", "character": "G"},
            {"name": "e_p_r3.a_C", "kind": "edge_eigen", "edge_id": "e_p_r3", "character": "C"},
            {"name": "e_p_r3.a_G", "kind": "edge_eigen", "edge_id": "e_p_r3", "character": "G"},
            {"name": "e_q_r3.a_C", "kind": "edge_eigen", "edge_id": "e_q_r3", "character": "C"},
            {"name": "e_q_r3.a_G", "kind": "edge_eigen", "edge_id": "e_q_r3", "character": "G"},
            {"name": "e_r2_2.a_T", "kind": "edge_eigen", "edge_id": "e_r2_2", "character": "T"},
            {"name": "e_r3_3.a_T", "kind": "edge_eigen", "edge_id": "e_r3_3", "character": "T"},
            {"name": "delta_3(p)", "kind": "inheritance", "reticulation": "r3", "parent_choice": "p"},
        ]
        require_equal(columns, expected_columns, "canonical Jacobian descriptor order")

        matrix = [[self.jacobian_entry(row, col) for col in columns] for row in expected_rows]
        stored_matrix = [[parse_alg(x) for x in row] for row in jac["matrix"]]
        require_equal(matrix, stored_matrix, "reconstructed Jacobian matrix")
        determinant = det_field(matrix)
        stored_det = parse_alg(jac["determinant"])
        require_equal(determinant, stored_det, "Jacobian determinant")
        denominator = 2 ** 61 * 3 ** 4 * 5 ** 14
        claimed = Alg((Fraction(0), Fraction(1, denominator),
                       Fraction(0), Fraction(10, denominator)))
        require_equal(determinant, claimed,
                      "det J = h(10 h^2+1)/(2^61 3^4 5^14)")
        require_positive(determinant, self.lo, self.hi, "Jacobian determinant")
        require_equal(jac["rank"], 15, "certified Jacobian rank")

        # The first three selected columns vary one of the two rooted factors
        # of the effective leaf-1 edge.  Multiplication by the fixed positive
        # K eigenvalues is an invertible diagonal coordinate change, so the
        # same rank holds for the 29-parameter semi-directed theta map.
        fixed_root_factor = self.edge_eigen["e_rho_u"]
        for symbol, value in zip(self.symbols[1:], fixed_root_factor[1:]):
            require_positive(value, self.lo, self.hi,
                             f"invertible root-suppression coordinate factor K_{symbol}")

        # Independently reconstruct a 9 x 9 tree-model rank witness.
        tree_witness = jac["tree_rank_witness"]
        require(isinstance(tree_witness, Mapping), "tree rank witness")
        expected_tree_rows: List[str] = []
        expected_tree_columns: List[str] = []
        tree_matrix = [[Alg.zero() for _ in range(9)] for _ in range(9)]
        leaf_vectors = self.cert["comparison_tree"]["leaf_edge_vectors"]
        alpha = parse_vector(leaf_vectors["1"]["eigen"])
        beta = parse_vector(leaf_vectors["2"]["eigen"])
        gamma = parse_vector(leaf_vectors["3"]["eigen"])
        for block, symbol in enumerate(("C", "G", "T")):
            idx = self.index[symbol]
            a, b, g = alpha[idx], beta[idx], gamma[idx]
            expected_tree_rows.extend([symbol + symbol + "A",
                                       symbol + "A" + symbol,
                                       "A" + symbol + symbol])
            expected_tree_columns.extend([f"alpha_{symbol}", f"beta_{symbol}",
                                          f"gamma_{symbol}"])
            block_matrix = [[b, a, Alg.zero()],
                            [g, Alg.zero(), a],
                            [Alg.zero(), g, b]]
            for rr in range(3):
                for cc in range(3):
                    tree_matrix[3 * block + rr][3 * block + cc] = block_matrix[rr][cc]
        require_equal(tree_witness["row_order"], expected_tree_rows,
                      "tree rank row order")
        require_equal(tree_witness["column_order"], expected_tree_columns,
                      "tree rank column order")
        require_equal([[parse_alg(x) for x in row] for row in tree_witness["matrix"]],
                      tree_matrix, "tree rank matrix")
        tree_det = det_field(tree_matrix)
        require_equal(tree_det, parse_alg(tree_witness["determinant"]),
                      "tree rank determinant")
        require_positive(-tree_det, self.lo, self.hi,
                         "negative nonzero tree rank determinant")
        require_equal(tree_witness["rank"], 9, "tree model rank")

        semi_edge_count = len(self.cert["root_suppression"]["effective_semi_directed_edges"])
        reticulation_count = len(self.retic_rows)
        semi_parameter_dimension = 3 * semi_edge_count + reticulation_count
        local_fixed_output_fiber_dimension = semi_parameter_dimension - 15
        tree_dimension = 9
        tree_codimension = 15 - tree_dimension
        local_collision_dimension = semi_parameter_dimension - tree_codimension
        require_equal(semi_edge_count, 9, "semi-directed edge count")
        require_equal(reticulation_count, 2, "reticulation count")
        require_equal(jac["semi_directed_parameter_dimension"], semi_parameter_dimension,
                      "semi-directed parameter dimension")
        require_equal(local_fixed_output_fiber_dimension, 14,
                      "local fixed-output K3P fiber dimension")
        require_equal(jac["tree_model_dimension"], tree_dimension,
                      "tree model dimension")
        require_equal(jac["tree_codimension_in_ambient"], tree_codimension,
                      "tree codimension")
        require_equal(jac["local_collision_locus_dimension"], local_collision_dimension,
                      "local collision-locus dimension")
        require_equal(jac["generic_rank"], 15, "generic theta rank")
        require_equal(jac["dominant_to_ambient_space"], True,
                      "dominance to ambient group-based Fourier space")

        print("[Jacobian] PASS  specified 15 x 15 minor reconstructed by exact differentiation")
        print("[Jacobian] PASS  det J = h(10 h^2+1)/(2^61 3^4 5^14) > 0")
        print("[Jacobian] PASS  fixed semi-directed theta map has rank 15; the nonzero-minor locus is Zariski open")
        print("[Jacobian] PASS  local fixed-output theta fiber has dimension 14 (29-15)")
        print("[Jacobian] PASS  tree model has rank 9; local network preimage of the tree model has dimension 23 (codimension 6)")
        return expected_rows, columns, matrix

    # ---- Edgewise strictly continuous-time extension ------------------------

    def verify_continuous_time(self, rows: Sequence[Tuple[int, int, int]],
                               columns: Sequence[Mapping[str, object]],
                               jacobian: Sequence[Sequence[Alg]]) -> None:
        ct = self.cert["continuous_time"]
        require(isinstance(ct, Mapping), "continuous-time certificate")
        require_equal(ct["strict_rate_inequalities"],
                      ["a_C>a_G*a_T", "a_G>a_C*a_T", "a_T>a_C*a_G"],
                      "strict positive-rate inequalities")

        vectors = self.cert["parameter_vectors"]
        require(isinstance(vectors, Mapping), "parameter vectors")
        network_vectors = {name: parse_vector(row["eigen"]) for name, row in vectors.items()}
        # U and V have exactly the stated saturated margins; every other
        # continuous-time margin of every effective network edge is strict.
        network_margin_status: Dict[Tuple[str, str], Alg] = {}
        for name in ("K", "K_odot_K", "U", "V", "S", "T"):
            margins = ct_margins(network_vectors[name])
            for margin_name, value in margins.items():
                network_margin_status[(name, margin_name)] = value
        require_zero(network_margin_status[("U", "C_minus_G_T")], "U_C-U_G U_T")
        require_zero(network_margin_status[("V", "G_minus_C_T")], "V_G-V_C V_T")
        for key, value in network_margin_status.items():
            if key in {("U", "C_minus_G_T"), ("V", "G_minus_C_T")}:
                continue
            require_positive(value, self.lo, self.hi,
                             f"edgewise strict continuous-time margin {key[0]}.{key[1]}")

        tree = self.cert["comparison_tree"]
        require(isinstance(tree, Mapping), "comparison tree")
        for leaf, row in tree["leaf_edge_vectors"].items():
            for margin_name, value in ct_margins(parse_vector(row["eigen"])).items():
                require_positive(value, self.lo, self.hi,
                                 f"tree leaf {leaf} continuous-time margin {margin_name}")

        free_columns = ct["free_direction"]
        expected_free_columns = [
            {"name": "e_u_p.a_C", "kind": "edge_eigen", "edge_id": "e_u_p",
             "character": "C", "derivative": ["1", "0", "0", "0"]},
            {"name": "e_u_q.a_G", "kind": "edge_eigen", "edge_id": "e_u_q",
             "character": "G", "derivative": ["1", "0", "0", "0"]},
        ]
        require_equal(free_columns, expected_free_columns,
                      "canonical continuous-time free-direction descriptors")

        g_direction = [
            sum((self.jacobian_entry(row, col) for col in free_columns), Alg.zero())
            for row in rows
        ]
        require_equal(g_direction,
                      [parse_alg(x) for x in ct["fixed_output_direction_before_pivot_correction"]],
                      "free-direction output derivative")

        pivot_rows = ct["pivot_derivatives"]
        require(isinstance(pivot_rows, list) and len(pivot_rows) == 15,
                "fifteen pivot derivatives")
        for entry in pivot_rows:
            require_equal(set(entry), {"parameter", "value"},
                          f"pivot derivative schema for {entry.get('parameter')}")
        require_equal([str(x["parameter"]) for x in pivot_rows],
                      [str(c["name"]) for c in columns], "pivot-derivative parameter order")
        pivot = [parse_alg(x["value"]) for x in pivot_rows]
        for i, row in enumerate(jacobian):
            residual = g_direction[i]
            for a, b in zip(row, pivot):
                residual = residual + a * b
            require_zero(residual, f"linearized fixed-output identity in row {i}")

        edge_directions: Dict[Tuple[str, str], Alg] = {}
        for column, value in zip(columns, pivot):
            if column["kind"] != "edge_eigen":
                continue
            key = (str(column["edge_id"]), str(column["character"]))
            require(key not in edge_directions, f"duplicate pivot direction {key}")
            edge_directions[key] = value
        for column in free_columns:
            key = (str(column["edge_id"]), str(column["character"]))
            require(key not in edge_directions, f"free direction duplicates pivot {key}")
            edge_directions[key] = parse_alg(column["derivative"])

        def edge_direction(edge_id: str) -> List[Alg]:
            return [Alg.zero()] + [
                edge_directions.get((edge_id, character), Alg.zero())
                for character in self.symbols[1:]
            ]

        u_margin_derivative = ct_margin_derivatives(
            self.edge_eigen["e_u_p"], edge_direction("e_u_p")
        )["C_minus_G_T"]
        v_margin_derivative = ct_margin_derivatives(
            self.edge_eigen["e_u_q"], edge_direction("e_u_q")
        )["G_minus_C_T"]
        stored_derivatives = ct["formerly_saturated_margin_derivatives"]
        require_equal(u_margin_derivative, parse_alg(stored_derivatives["U_C-U_G*U_T"]),
                      "U saturated-margin derivative")
        require_equal(v_margin_derivative, parse_alg(stored_derivatives["V_G-V_C*V_T"]),
                      "V saturated-margin derivative")
        expected_u = Alg((Fraction(21, 19), Fraction(0), Fraction(-20, 19), Fraction(0)))
        require_equal(u_margin_derivative, expected_u,
                      "(10 h^2-1)/(1+10 h^2)=(21-20 h^2)/19")
        require_positive(u_margin_derivative, self.lo, self.hi, "U margin derivative")
        require_positive(v_margin_derivative, self.lo, self.hi, "V margin derivative")

        # Exact IFT certificate: the output map is polynomial, the pivot
        # Jacobian is invertible, and the two zero margins have positive
        # right derivatives. All other rate inequalities, all Theta_0^circ and
        # transition-probability inequalities, and both mixing inequalities
        # have strict slack at epsilon=0, so they persist for sufficiently
        # small positive epsilon by continuity.
        require_equal(ct["strict_continuous_time_extension"], True,
                      "edgewise strict continuous-time extension flag")
        print("[edgewise continuous time] PASS  U and V are the only saturated positive-rate margins")
        print("[edgewise continuous time] PASS  exact tangent identity for the fixed-output IFT branch verified")
        print("[edgewise continuous time] PASS  saturated-margin derivatives are positive")
        print("[edgewise continuous time] PASS  algebraic hypotheses for the analytic IFT corollary verified")


def verify_sidecars(certificate_path: Path, data: Mapping[str, object]) -> None:
    """Check that the two human-sized sidecars mirror embedded certificate data."""
    for section, filename in (
        ("jacobian", "jacobian_certificate_k3p.json"),
        ("continuous_time", "continuous_time_certificate_k3p.json"),
    ):
        sidecar_path = certificate_path.parent / filename
        require(sidecar_path.is_file(), f"missing K3P sidecar {filename}")
        sidecar = load_canonical_certificate(sidecar_path)
        require(sidecar == data[section],
                f"{filename} must equal embedded {section} section")
    print("[sidecars] PASS  transport copies equal their embedded certificate sections")


def verify(certificate_path: Path) -> None:
    data = load_canonical_certificate(certificate_path)
    require_equal(
        set(data),
        {
            "schema_version", "title", "field", "group", "rooted_network",
            "root_suppression", "parameter_vectors", "comparison_tree",
            "construction_ansatz", "core_factorization", "fourier_coordinates",
            "leaf_pattern_probabilities", "jacobian", "continuous_time",
        },
        "closed top-level K3P certificate schema",
    )
    require_equal(data["schema_version"], "3.0", "certificate schema version")
    verify_sidecars(certificate_path, data)
    verification = Verification(data)
    verification.verify_field()
    verification.verify_topology()
    verification.verify_construction_ansatz()
    verification.verify_parameters()
    q_network, q_tree = verification.verify_collision()
    verification.verify_direct_state_space(q_network, q_tree)
    verification.verify_k2p_specialization_scope(q_network, q_tree)
    rows, columns, jacobian = verification.verify_jacobian()
    verification.verify_continuous_time(rows, columns, jacobian)
    print()
    print("ALL K3P CHECKS PASSED")


def main() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10 or newer is required")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "certificate_k3p.json",
        help="path to certificate.json (default: next to verify.py)",
    )
    args = parser.parse_args()
    try:
        verify(args.certificate)
    except Exception as exc:  # concise failure report with nonzero exit status
        print(f"EXACT VERIFICATION FAILED: {exc}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
