#!/usr/bin/env python3
"""Generate the machine-readable exact certificate for the K3P theta collision.

This script uses only the Python standard library.  It is a construction script;
the distributed verify.py independently rebuilds and checks every claimed object.
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


@dataclass(frozen=True)
class Alg:
    """c0+c1*h+c2*h^2+c3*h^3 in the basis representation of Q(h)."""

    c: Tuple[Fraction, Fraction, Fraction, Fraction]

    @staticmethod
    def zero() -> "Alg":
        return Alg((Fraction(0),) * 4)

    @staticmethod
    def one() -> "Alg":
        return Alg((Fraction(1), Fraction(0), Fraction(0), Fraction(0)))

    @staticmethod
    def q(x: int | Fraction) -> "Alg":
        return Alg((Fraction(x), Fraction(0), Fraction(0), Fraction(0)))

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
        tmp = [Fraction(0) for _ in range(7)]
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                tmp[i + j] += a * b
        for k in range(6, 3, -1):
            tmp[k - 4] += tmp[k] / 5
        return Alg(tuple(tmp[:4]))  # type: ignore[arg-type]

    def scale(self, x: int | Fraction) -> "Alg":
        x = Fraction(x)
        return Alg(tuple(x * a for a in self.c))  # type: ignore[arg-type]

    def is_zero(self) -> bool:
        return all(x == 0 for x in self.c)

    def inverse(self) -> "Alg":
        if self.is_zero():
            raise ZeroDivisionError("zero has no inverse")
        # Solve multiplication-by-self matrix times b = 1 over Q.
        basis = [Alg.one(), Alg.h(), Alg.h() * Alg.h(), Alg.h() * Alg.h() * Alg.h()]
        products = [self * b for b in basis]
        aug = [[products[j].c[i] for j in range(4)] + [Fraction(1 if i == 0 else 0)] for i in range(4)]
        for col in range(4):
            pivot = next(i for i in range(col, 4) if aug[i][col] != 0)
            aug[col], aug[pivot] = aug[pivot], aug[col]
            p = aug[col][col]
            aug[col] = [x / p for x in aug[col]]
            for i in range(4):
                if i == col:
                    continue
                f = aug[i][col]
                if f:
                    aug[i] = [a - f * b for a, b in zip(aug[i], aug[col])]
        return Alg(tuple(aug[i][4] for i in range(4)))  # type: ignore[arg-type]

    def __truediv__(self, other: "Alg") -> "Alg":
        return self * other.inverse()


def det_field(matrix: Sequence[Sequence[Alg]]) -> Alg:
    a = [list(row) for row in matrix]
    n = len(a)
    sign = 1
    det = Alg.one()
    for col in range(n):
        pivot = next((i for i in range(col, n) if not a[i][col].is_zero()), None)
        if pivot is None:
            return Alg.zero()
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign *= -1
        p = a[col][col]
        det = det * p
        for i in range(col + 1, n):
            if a[i][col].is_zero():
                continue
            f = a[i][col] / p
            for j in range(col, n):
                a[i][j] = a[i][j] - f * a[col][j]
    return det.scale(sign)


def enc(x: Alg) -> List[str]:
    return [str(v) for v in x.c]


def enc_vec(v: Sequence[Alg]) -> List[List[str]]:
    return [enc(x) for x in v]


def probs(eig: Sequence[Alg]) -> List[Alg]:
    one, c, g, t = eig
    return [
        (one + c + g + t).scale(Fraction(1, 4)),
        (one + c - g - t).scale(Fraction(1, 4)),
        (one - c + g - t).scale(Fraction(1, 4)),
        (one - c - g + t).scale(Fraction(1, 4)),
    ]


def ct_margins(eig: Sequence[Alg]) -> Dict[str, Alg]:
    _, c, g, t = eig
    return {"C_minus_G_T": c - g * t, "G_minus_C_T": g - c * t, "T_minus_C_G": t - c * g}


G = ["A", "C", "G", "T"]
IDX = {s: i for i, s in enumerate(G)}
H = Alg.h()
ONE = Alg.one()

K = [ONE, Alg.q(Fraction(1, 2)), Alg.q(Fraction(1, 2)), Alg.q(Fraction(1, 2))]
U = [ONE, H.scale(Fraction(1, 3)), H, Alg.q(Fraction(1, 3))]
V = [ONE, H, H.scale(Fraction(1, 3)), Alg.q(Fraction(1, 3))]
S = [ONE, (H * H).scale(Fraction(3, 4)), Alg.q(Fraction(1, 4)), Alg.q(Fraction(3, 10))]
T = [ONE, Alg.q(Fraction(1, 4)), (H * H).scale(Fraction(3, 4)), Alg.q(Fraction(3, 10))]
K2 = [a * b for a, b in zip(K, K)]

m = (H * H * H).scale(Fraction(5, 16)) + H.scale(Fraction(1, 16))
n = (H * H).scale(Fraction(1, 4))
ALPHA = [ONE, m, m, n]
BETA = [ONE, n, n, n]
GAMMA = BETA

P = [ONE, (H * H * H).scale(Fraction(5, 4)) + H.scale(Fraction(1, 4)),
     (H * H * H).scale(Fraction(5, 4)) + H.scale(Fraction(1, 4)), H * H]
B = [ONE, (H * H).scale(Fraction(1, 2)), (H * H).scale(Fraction(1, 2)), (H * H).scale(Fraction(1, 2))]

VECTOR_BY_NAME = {"K": K, "U": U, "V": V, "S": S, "T": T}

VERTICES = [
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

ARC_SPECS = [
    ("e_rho_1", "rho", "1", "K"),
    ("e_rho_u", "rho", "u", "K"),
    ("e_u_p", "u", "p", "U"),
    ("e_u_q", "u", "q", "V"),
    ("e_p_r2", "p", "r2", "S"),
    ("e_q_r2", "q", "r2", "T"),
    ("e_p_r3", "p", "r3", "S"),
    ("e_q_r3", "q", "r3", "T"),
    ("e_r2_2", "r2", "2", "K"),
    ("e_r3_3", "r3", "3", "K"),
]

ARCS = []
for edge_id, parent, child, vector_name in ARC_SPECS:
    eig = VECTOR_BY_NAME[vector_name]
    ARCS.append({
        "id": edge_id,
        "parent": parent,
        "child": child,
        "vector_name": vector_name,
        "eigen": enc_vec(eig),
        "transition_probabilities": enc_vec(probs(eig)),
    })

RETICS = [
    {"vertex": "r2", "incoming": [
        {"edge_id": "e_p_r2", "parent": "p", "weight": "1/2", "choice": "p"},
        {"edge_id": "e_q_r2", "parent": "q", "weight": "1/2", "choice": "q"},
    ]},
    {"vertex": "r3", "incoming": [
        {"edge_id": "e_p_r3", "parent": "p", "weight": "1/2", "choice": "p"},
        {"edge_id": "e_q_r3", "parent": "q", "weight": "1/2", "choice": "q"},
    ]},
]

EIG_BY_EDGE = {row[0]: VECTOR_BY_NAME[row[3]] for row in ARC_SPECS}
EDGE_ENDPOINTS = {row[0]: (row[1], row[2]) for row in ARC_SPECS}
LEAF_INDEX = {"1": 0, "2": 1, "3": 2}


def retained_for_choices(c2: int, c3: int) -> Tuple[List[str], Fraction]:
    retained = [e[0] for e in ARC_SPECS]
    weight = Fraction(1)
    for choice, retic in zip((c2, c3), RETICS):
        incoming = retic["incoming"]
        chosen = incoming[choice]
        deleted = incoming[1 - choice]
        retained.remove(deleted["edge_id"])
        weight *= Fraction(chosen["weight"])
    return retained, weight


def descendants(child: str, retained: Sequence[str]) -> set[str]:
    children: Dict[str, List[str]] = {v["id"]: [] for v in VERTICES}
    for edge_id in retained:
        u, v = EDGE_ENDPOINTS[edge_id]
        children[u].append(v)
    seen = {child}
    stack = [child]
    while stack:
        u = stack.pop()
        for v in children[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def edge_character(edge_id: str, labels: Tuple[int, int, int], retained: Sequence[str]) -> int:
    _, child = EDGE_ENDPOINTS[edge_id]
    below = descendants(child, retained)
    x = 0
    for leaf, pos in LEAF_INDEX.items():
        if leaf in below:
            x ^= labels[pos]
    return x


def displayed_monomial(labels: Tuple[int, int, int], choices: Tuple[int, int]) -> Alg:
    retained, _ = retained_for_choices(*choices)
    out = ONE
    for edge_id in retained:
        out = out * EIG_BY_EDGE[edge_id][edge_character(edge_id, labels, retained)]
    return out


def network_fourier(labels: Tuple[int, int, int]) -> Alg:
    if labels[0] ^ labels[1] ^ labels[2]:
        return Alg.zero()
    total = Alg.zero()
    for choices in itertools.product((0, 1), repeat=2):
        _, weight = retained_for_choices(*choices)
        total = total + displayed_monomial(labels, choices).scale(weight)
    return total


def tree_fourier(labels: Tuple[int, int, int]) -> Alg:
    x, y, z = labels
    if x ^ y ^ z:
        return Alg.zero()
    return ALPHA[x] * BETA[y] * GAMMA[z]


CHAR_TABLE = [
    [1, 1, 1, 1],
    [1, 1, -1, -1],
    [1, -1, 1, -1],
    [1, -1, -1, 1],
]


def pattern_probability(qmap: Mapping[Tuple[int, int, int], Alg], pattern: Tuple[int, int, int]) -> Alg:
    out = Alg.zero()
    a, b, c = pattern
    for x, y, z in itertools.product(range(4), repeat=3):
        sign = CHAR_TABLE[x][a] * CHAR_TABLE[y][b] * CHAR_TABLE[z][c]
        out = out + qmap[(x, y, z)].scale(Fraction(sign, 64))
    return out


def core_terms(y: int, z: int) -> List[Alg]:
    x = y ^ z
    return [
        S[y] * S[z] * U[x],
        S[y] * T[z] * U[y] * V[z],
        T[y] * S[z] * U[z] * V[y],
        T[y] * T[z] * V[x],
    ]


def core_m(y: int, z: int) -> Alg:
    total = Alg.zero()
    for term in core_terms(y, z):
        total = total + term.scale(Fraction(1, 4))
    return total


def factor_m(y: int, z: int) -> Alg:
    return P[y ^ z] * B[y] * B[z]


# Jacobian construction.
J_ROWS = [(x, y, z) for x, y, z in itertools.product(range(4), repeat=3)
          if (x ^ y ^ z) == 0 and (x, y, z) != (0, 0, 0)]
J_COLUMNS = [
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


def derivative_edge(labels: Tuple[int, int, int], edge_id: str, character: int) -> Alg:
    if labels[0] ^ labels[1] ^ labels[2]:
        return Alg.zero()
    total = Alg.zero()
    for choices in itertools.product((0, 1), repeat=2):
        retained, weight = retained_for_choices(*choices)
        if edge_id not in retained:
            continue
        char = edge_character(edge_id, labels, retained)
        if char != character:
            continue
        term = Alg.q(weight)
        for other in retained:
            if other == edge_id:
                continue
            term = term * EIG_BY_EDGE[other][edge_character(other, labels, retained)]
        total = total + term
    return total


def derivative_delta3(labels: Tuple[int, int, int]) -> Alg:
    if labels[0] ^ labels[1] ^ labels[2]:
        return Alg.zero()
    total = Alg.zero()
    for c2, c3 in itertools.product((0, 1), repeat=2):
        retained, _ = retained_for_choices(c2, c3)
        dweight = Fraction(1, 2) if c3 == 0 else Fraction(-1, 2)
        term = Alg.q(dweight)
        for edge_id in retained:
            term = term * EIG_BY_EDGE[edge_id][edge_character(edge_id, labels, retained)]
        total = total + term
    return total


def jac_entry(labels: Tuple[int, int, int], col: Mapping[str, str]) -> Alg:
    if col["kind"] == "edge_eigen":
        return derivative_edge(labels, col["edge_id"], IDX[col["character"]])
    return derivative_delta3(labels)


J = [[jac_entry(row, col) for col in J_COLUMNS] for row in J_ROWS]
JDET = det_field(J)
DEN = 2**61 * 3**4 * 5**14
JDET_CLAIM = Alg((Fraction(0), Fraction(1, DEN), Fraction(0), Fraction(10, DEN)))
if JDET != JDET_CLAIM:
    raise RuntimeError(f"Jacobian determinant mismatch: {JDET} != {JDET_CLAIM}")

# Continuous-time IFT direction.  Free parameters U_C and V_G both increase at unit speed.
FREE_COLUMNS = [
    {"name": "e_u_p.a_C", "kind": "edge_eigen", "edge_id": "e_u_p", "character": "C"},
    {"name": "e_u_q.a_G", "kind": "edge_eigen", "edge_id": "e_u_q", "character": "G"},
]
GDIR = [sum((jac_entry(row, col) for col in FREE_COLUMNS), Alg.zero()) for row in J_ROWS]
PPRIME = [
    Alg((0, Fraction(-3, 19), 0, Fraction(-375, 304))),
    Alg((0, Fraction(-621, 152), 0, Fraction(1875, 304))),
    Alg.zero(),
    Alg((Fraction(-6, 19), 0, Fraction(60, 19), 0)),
    Alg((0, Fraction(-117, 304), 0, Fraction(459, 608))),
    Alg((0, Fraction(-75, 608), 0, Fraction(-195, 304))),
    Alg((0, Fraction(-255, 608), 0, Fraction(135, 304))),
    Alg((0, Fraction(9, 304), 0, Fraction(-9, 608))),
    Alg((0, Fraction(-117, 304), 0, Fraction(459, 608))),
    Alg((0, Fraction(-75, 608), 0, Fraction(-195, 304))),
    Alg((0, Fraction(-255, 608), 0, Fraction(135, 304))),
    Alg((0, Fraction(9, 304), 0, Fraction(-9, 608))),
    Alg.zero(), Alg.zero(), Alg.zero(),
]
for i, row in enumerate(J):
    residual = GDIR[i]
    for a, b in zip(row, PPRIME):
        residual = residual + a * b
    if not residual.is_zero():
        raise RuntimeError(f"IFT tangent residual at row {i}: {residual}")

U_MARGIN_DER = ONE - PPRIME[3].scale(Fraction(1, 3))
V_MARGIN_DER = ONE

q_network = {triple: network_fourier(triple) for triple in itertools.product(range(4), repeat=3)}
q_tree = {triple: tree_fourier(triple) for triple in itertools.product(range(4), repeat=3)}
if q_network != q_tree:
    raise RuntimeError("Fourier maps do not agree")
pattern_network = {triple: pattern_probability(q_network, triple) for triple in itertools.product(range(4), repeat=3)}
pattern_tree = {triple: pattern_probability(q_tree, triple) for triple in itertools.product(range(4), repeat=3)}
if pattern_network != pattern_tree:
    raise RuntimeError("Pattern probabilities do not agree")


def label3(t: Tuple[int, int, int]) -> str:
    return "".join(G[i] for i in t)


semi_edges = [
    {"id": "e_1_u", "endpoints": ["1", "u"], "kind": "undirected", "source_edges": ["e_rho_1", "e_rho_u"],
     "vector_name": "K_odot_K", "eigen": enc_vec(K2), "transition_probabilities": enc_vec(probs(K2))},
    {"id": "e_u_p", "endpoints": ["u", "p"], "kind": "undirected", "source_edges": ["e_u_p"],
     "vector_name": "U", "eigen": enc_vec(U), "transition_probabilities": enc_vec(probs(U))},
    {"id": "e_u_q", "endpoints": ["u", "q"], "kind": "undirected", "source_edges": ["e_u_q"],
     "vector_name": "V", "eigen": enc_vec(V), "transition_probabilities": enc_vec(probs(V))},
    {"id": "e_p_r2", "endpoints": ["p", "r2"], "kind": "reticulation_arc", "direction": ["p", "r2"], "source_edges": ["e_p_r2"],
     "vector_name": "S", "eigen": enc_vec(S), "transition_probabilities": enc_vec(probs(S))},
    {"id": "e_q_r2", "endpoints": ["q", "r2"], "kind": "reticulation_arc", "direction": ["q", "r2"], "source_edges": ["e_q_r2"],
     "vector_name": "T", "eigen": enc_vec(T), "transition_probabilities": enc_vec(probs(T))},
    {"id": "e_p_r3", "endpoints": ["p", "r3"], "kind": "reticulation_arc", "direction": ["p", "r3"], "source_edges": ["e_p_r3"],
     "vector_name": "S", "eigen": enc_vec(S), "transition_probabilities": enc_vec(probs(S))},
    {"id": "e_q_r3", "endpoints": ["q", "r3"], "kind": "reticulation_arc", "direction": ["q", "r3"], "source_edges": ["e_q_r3"],
     "vector_name": "T", "eigen": enc_vec(T), "transition_probabilities": enc_vec(probs(T))},
    {"id": "e_r2_2", "endpoints": ["r2", "2"], "kind": "undirected", "source_edges": ["e_r2_2"],
     "vector_name": "K", "eigen": enc_vec(K), "transition_probabilities": enc_vec(probs(K))},
    {"id": "e_r3_3", "endpoints": ["r3", "3"], "kind": "undirected", "source_edges": ["e_r3_3"],
     "vector_name": "K", "eigen": enc_vec(K), "transition_probabilities": enc_vec(probs(K))},
]

cert = {
    "schema_version": "2.0",
    "title": "Exact full-dimensional K3P tree/theta-trinet collision",
    "field": {
        "generator": "h",
        "minimal_polynomial": "5*h^4-1",
        "relation": "h^4=1/5",
        "isolating_interval": ["2/3", "7/10"],
        "basis": ["1", "h", "h^2", "h^3"],
        "encoding": "[c0,c1,c2,c3] means c0+c1*h+c2*h^2+c3*h^3",
        "number_field": "Q(h)",
        "generator_value": "h=5^(-1/4), selected by 2/3<h<7/10",
        "representation": "basis 1,h,h^2,h^3 with h^4=1/5",
    },
    "group": {
        "symbols": G,
        "indices": IDX,
        "addition": "bitwise XOR on indices A=0,C=1,G=2,T=3",
        "character_table_rows_A_C_G_T": CHAR_TABLE,
    },
    "parameter_vectors": {
        name: {"eigen": enc_vec(vec), "transition_probabilities": enc_vec(probs(vec)),
               "continuous_time_margins": {k: enc(v) for k, v in ct_margins(vec).items()}}
        for name, vec in {**VECTOR_BY_NAME, "K_odot_K": K2}.items()
    },
    "rooted_network": {
        "vertices": VERTICES,
        "arcs": ARCS,
        "reticulations": RETICS,
        "display_choice_order": ["r2", "r3"],
        "choice_index_meaning": {"0": "incoming edge from p", "1": "incoming edge from q"},
    },
    "root_suppression": {
        "removed_vertex": "rho",
        "removed_arcs": ["e_rho_1", "e_rho_u"],
        "new_edge": "e_1_u",
        "composition_rule": "Fourier eigenvalues multiply coordinatewise",
        "effective_semi_directed_edges": semi_edges,
        "theta_core": {
            "vertices": ["u", "p", "q", "r2", "r3"],
            "edges": ["e_u_p", "e_u_q", "e_p_r2", "e_q_r2", "e_p_r3", "e_q_r3"],
            "three_p_q_paths": [["p", "u", "q"], ["p", "r2", "q"], ["p", "r3", "q"]],
            "incident_pendant_edges": ["e_1_u", "e_r2_2", "e_r3_3"],
            "incident_leaf_components": [["1"], ["2"], ["3"]],
            "reticulations": ["r2", "r3"],
            "level": 2,
        },
    },
    "comparison_tree": {
        "topology": "semi-directed three-star on leaves 1,2,3",
        "leaf_edge_vectors": {
            "1": {"name": "alpha", "eigen": enc_vec(ALPHA), "transition_probabilities": enc_vec(probs(ALPHA)),
                  "continuous_time_margins": {k: enc(v) for k, v in ct_margins(ALPHA).items()}},
            "2": {"name": "beta", "eigen": enc_vec(BETA), "transition_probabilities": enc_vec(probs(BETA)),
                  "continuous_time_margins": {k: enc(v) for k, v in ct_margins(BETA).items()}},
            "3": {"name": "gamma", "eigen": enc_vec(GAMMA), "transition_probabilities": enc_vec(probs(GAMMA)),
                  "continuous_time_margins": {k: enc(v) for k, v in ct_margins(GAMMA).items()}},
        },
    },
    "core_factorization": {
        "row_order": G,
        "column_order": G,
        "displayed_choice_order": ["p,p", "p,q", "q,p", "q,q"],
        "displayed_core_terms": [[enc(x) for x in core_terms(y, z)] for y in range(4) for z in range(4)],
        "M_entries_row_major": [enc(core_m(y, z)) for y in range(4) for z in range(4)],
        "P": enc_vec(P),
        "B": enc_vec(B),
        "factorized_entries_row_major": [enc(factor_m(y, z)) for y in range(4) for z in range(4)],
        "identity": "M[y,z]=P[y xor z]*B[y]*B[z]",
    },
    "fourier_coordinates": {
        "order": [label3(t) for t in itertools.product(range(4), repeat=3)],
        "network": [enc(q_network[t]) for t in itertools.product(range(4), repeat=3)],
        "tree": [enc(q_tree[t]) for t in itertools.product(range(4), repeat=3)],
    },
    "leaf_pattern_probabilities": {
        "order": [label3(t) for t in itertools.product(range(4), repeat=3)],
        "network": [enc(pattern_network[t]) for t in itertools.product(range(4), repeat=3)],
        "tree": [enc(pattern_tree[t]) for t in itertools.product(range(4), repeat=3)],
    },
    "jacobian": {
        "output_space": "the 15 nonconstant consistent Fourier coordinates; q_AAA is fixed at 1",
        "row_order": [label3(t) for t in J_ROWS],
        "row_indices": [list(t) for t in J_ROWS],
        "column_order": J_COLUMNS,
        "matrix": [[enc(x) for x in row] for row in J],
        "determinant": enc(JDET),
        "determinant_formula": "h*(10*h^2+1)/(2^61*3^4*5^14)",
        "determinant_denominator": str(DEN),
        "sign": "positive on 2/3<h<7/10",
        "rank": 15,
        "ambient_space": "15-dimensional affine space of consistent three-leaf group-based Fourier coordinates with q_AAA=1",
        "number_field": "Q(h), h=5^(-1/4), basis 1,h,h^2,h^3",
    },
    "continuous_time": {
        "eigenvalue_formulas": {
            "a_C": "exp(-2*(lambda_G+lambda_T))",
            "a_G": "exp(-2*(lambda_C+lambda_T))",
            "a_T": "exp(-2*(lambda_C+lambda_G))",
        },
        "strict_rate_inequalities": ["a_C>a_G*a_T", "a_G>a_C*a_T", "a_T>a_C*a_G"],
        "closed_form_witness_boundary_equalities": ["U_C=U_G*U_T", "V_G=V_C*V_T"],
        "free_direction": [{**c, "derivative": enc(ONE)} for c in FREE_COLUMNS],
        "fixed_output_direction_before_pivot_correction": [enc(x) for x in GDIR],
        "pivot_derivatives": [
            {"parameter": col["name"], "value": enc(value)} for col, value in zip(J_COLUMNS, PPRIME)
        ],
        "linearized_fixed_output_identity": "J*pivot_derivative + dF/d(e_u_p.a_C) + dF/d(e_u_q.a_G) = 0",
        "formerly_saturated_margin_derivatives": {
            "U_C-U_G*U_T": enc(U_MARGIN_DER),
            "V_G-V_C*V_T": enc(V_MARGIN_DER),
        },
        "U_margin_derivative_formula": "(10*h^2-1)/(1+10*h^2)=(21-20*h^2)/19",
        "strict_continuous_time_extension": True,
        "method": "real-analytic implicit-function theorem using the invertible 15x15 Jacobian minor",
        "certificate_scope": "exactly verifies the invertible Jacobian, fixed-output tangent identity, strict slack at epsilon=0, and positive derivatives of the two saturated margins; the nearby branch is supplied analytically by the real-analytic implicit-function theorem",
        "number_field": "Q(h), h=5^(-1/4), basis 1,h,h^2,h^3",
    },
}

out = Path(__file__).resolve().parents[1] / "certificate.json"
out.write_text(json.dumps(cert, indent=2) + "\n")

(Path(__file__).resolve().parents[1] / "jacobian_certificate.json").write_text(
    json.dumps(cert["jacobian"], indent=2) + "\n"
)
(Path(__file__).resolve().parents[1] / "continuous_time_certificate.json").write_text(
    json.dumps(cert["continuous_time"], indent=2) + "\n"
)
print(f"Wrote {out}")
