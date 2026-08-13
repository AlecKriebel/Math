#!/usr/bin/env python3
"""Primary exact verifier for the four-leaf JC sharpness pair.

Dependencies: Python 3.10+, sympy, networkx.
No floating-point assertion is used.  Numerical decimals are printed only after
all exact checks have passed.
"""
from __future__ import annotations

import json
from itertools import product, permutations
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import networkx as nx
import sympy as sp

HERE = Path(__file__).resolve().parent
JSON_PATH = HERE / "networks.json"

# ---------------------------------------------------------------------------
# Status/output helpers
# ---------------------------------------------------------------------------
def passed(label: str) -> None:
    print(f"[EXACTLY COMPUTED] PASS: {label}")


def require_zero(expr: sp.Expr, label: str) -> None:
    z = sp.factor(sp.cancel(expr))
    if z != 0:
        raise AssertionError(f"{label}: expected zero, got {z}")


# ---------------------------------------------------------------------------
# Graph/topology checks from the machine-readable descriptions
# ---------------------------------------------------------------------------
def load_networks() -> dict:
    with JSON_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def directed_graph(common: dict, network: dict) -> nx.DiGraph:
    g = nx.DiGraph()
    for vertex, kind in common["vertices"].items():
        g.add_node(vertex, kind=kind)
    g.add_edges_from(tuple(e) for e in common["internal_arcs"])
    g.add_edges_from(tuple(e) for e in network["pendant_arcs"])
    return g


def root_is_lowest_stable_ancestor(dg: nx.DiGraph) -> bool:
    """Check that no proper vertex lies on every root-to-leaf path."""
    root = "rho"
    leaves = [v for v, d in dg.nodes(data=True) if d["kind"].startswith("leaf:")]
    for vertex in dg:
        if vertex == root:
            continue
        reduced = dg.copy()
        reduced.remove_node(vertex)
        if all(leaf not in reduced or not nx.has_path(reduced, root, leaf) for leaf in leaves):
            return False
    return True


def check_binary_rooted_class(common: dict, network: dict) -> nx.Graph:
    dg = directed_graph(common, network)
    assert nx.is_directed_acyclic_graph(dg)
    assert root_is_lowest_stable_ancestor(dg)

    roots = [v for v in dg if dg.in_degree(v) == 0]
    assert roots == ["rho"]
    assert dg.out_degree("rho") == 2

    for v, data in dg.nodes(data=True):
        kind = data["kind"]
        indeg, outdeg = dg.in_degree(v), dg.out_degree(v)
        if kind == "root":
            assert (indeg, outdeg) == (0, 2)
        elif kind == "tree":
            assert (indeg, outdeg) == (1, 2)
        elif kind == "reticulation":
            assert (indeg, outdeg) == (2, 1)
        elif kind.startswith("leaf:"):
            assert (indeg, outdeg) == (1, 0)
        else:
            raise AssertionError(f"unknown vertex kind {kind}")

    # Tree-child condition and no reticulation child.
    for v, data in dg.nodes(data=True):
        if data["kind"].startswith("leaf:"):
            continue
        child_kinds = [dg.nodes[w]["kind"] for w in dg.successors(v)]
        assert any(k == "tree" or k.startswith("leaf:") for k in child_kinds)
        if data["kind"] == "reticulation":
            assert all(k != "reticulation" for k in child_kinds)

    ug = dg.to_undirected()
    assert ug.degree("rho") == 2
    a, c = tuple(ug.neighbors("rho"))
    ug.remove_node("rho")
    ug.add_edge(a, c)

    cycles = nx.cycle_basis(ug)
    cycle_lengths = sorted(len(c) for c in cycles)
    # Cycle rank is two; in this theta graph the three simple cycles have
    # lengths 3,5,6.  cycle_basis may return any two of the three, so enumerate.
    directed = nx.DiGraph()
    directed.add_nodes_from(ug.nodes())
    for u, v in ug.edges():
        directed.add_edge(u, v)
        directed.add_edge(v, u)
    simple_cycles = set()
    for cyc in nx.simple_cycles(directed):
        if len(cyc) < 3:
            continue
        rots = []
        for seq in (cyc, list(reversed(cyc))):
            for i in range(len(seq)):
                rots.append(tuple(seq[i:] + seq[:i]))
        simple_cycles.add(min(rots))
    lengths = sorted(len(c) for c in simple_cycles)
    assert lengths == [3, 5, 6], lengths
    assert lengths.count(3) == 1
    assert all(k >= 4 for k in lengths if k != 3)

    blobs = [set(comp) for comp in nx.biconnected_components(ug) if len(comp) >= 3]
    assert len(blobs) == 1
    blob = blobs[0]
    retics = {v for v in blob if dg.nodes[v]["kind"] == "reticulation"}
    assert retics == {"C", "F"}
    assert len(retics) <= 2
    return ug


def check_not_triangle_equivalent(ug_n: nx.Graph, ug_np: nx.Graph) -> None:
    # A leaf-labelled isomorphism fixes each Li.  In N, the neighbour of L1
    # lies on the unique triangle; in N', it does not.  This property survives
    # every permitted redirection internal to the triangle.
    def unique_triangle_nodes(g: nx.Graph) -> set[str]:
        tris = [set(c) for c in nx.enumerate_all_cliques(g) if len(c) == 3]
        tris = [s for s in tris if all(g.has_edge(u, v) for u in s for v in s if u != v)]
        # enumerate_all_cliques includes each 3-clique once here.
        assert len(tris) == 1
        return tris[0]

    tri_n = unique_triangle_nodes(ug_n)
    tri_np = unique_triangle_nodes(ug_np)
    n1 = next(ug_n.neighbors("L1"))
    np1 = next(ug_np.neighbors("L1"))
    assert n1 in tri_n
    assert np1 not in tri_np

    # Also exhaustively reject a leaf-fixing graph isomorphism.
    nm = nx.algorithms.isomorphism.categorical_node_match("label", None)
    for g in (ug_n, ug_np):
        for v in g:
            g.nodes[v]["label"] = v if v.startswith("L") else "internal"
    assert not nx.is_isomorphic(ug_n, ug_np, node_match=nm)


# ---------------------------------------------------------------------------
# Fourier parameterization
# ---------------------------------------------------------------------------
# Z2 x Z2 is encoded by {0,1,2,3} with bitwise XOR.
ORBIT_REPS: List[Tuple[int, int, int, int]] = [
    (0, 0, 1, 1),  # r34
    (0, 1, 0, 1),  # r24
    (0, 1, 1, 0),  # r23
    (0, 1, 2, 3),  # t234
    (1, 0, 0, 1),  # r14
    (1, 0, 1, 0),  # r13
    (1, 0, 2, 3),  # t134
    (1, 1, 0, 0),  # r12
    (1, 1, 1, 1),  # u1111
    (1, 1, 2, 2),  # u1122
    (1, 2, 0, 3),  # t124
    (1, 2, 1, 2),  # u1212
    (1, 2, 2, 1),  # u1221
    (1, 2, 3, 0),  # t123
]
COORD_NAMES = [
    "A", "B", "C", "D", "E", "F", "G", "H",
    "J", "K", "L", "M", "N", "O",
]

EDGE_KEYS = ["AB", "CD", "DE", "AC", "BC", "AF", "EF", "p1", "p2", "p3", "p4"]
SYMS: Dict[str, sp.Symbol] = {key: sp.symbols(key) for key in EDGE_KEYS}
SYMS["lc"], SYMS["lf"] = sp.symbols("lc lf")


def xor_all(values: Iterable[int]) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def component_leaf_labels(
    edges: Sequence[Tuple[str, str, str, sp.Expr]],
    cut_index: int,
    start: str,
) -> List[int]:
    adj: Dict[str, List[str]] = {}
    for i, (u, v, _name, _x) in enumerate(edges):
        if i == cut_index:
            continue
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in adj.get(u, []):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return [i for i in range(1, 5) if f"L{i}" in seen]


def fourier_coordinate(
    characters: Tuple[int, int, int, int],
    leaf_attachment: Mapping[str, int],
    symbols: Mapping[str, sp.Expr],
) -> sp.Expr:
    """Sparse displayed-tree sum for a zero-sum character assignment."""
    if xor_all(characters) != 0:
        return sp.Integer(0)

    base_edges: List[Tuple[str, str, str, sp.Expr]] = [
        ("A", "B", "AB", symbols["AB"]),
        ("C", "D", "CD", symbols["CD"]),
        ("D", "E", "DE", symbols["DE"]),
    ]
    for internal, label in leaf_attachment.items():
        key = f"p{label}"
        base_edges.append((internal, f"L{label}", key, symbols[key]))

    total = sp.Integer(0)
    # c_choice=0 selects effective AC; c_choice=1 selects BC.
    # f_choice=0 selects AF; f_choice=1 selects EF.
    for c_choice, f_choice in product((0, 1), repeat=2):
        edges = list(base_edges)
        if c_choice == 0:
            edges.append(("A", "C", "AC", symbols["AC"]))
            weight_c = symbols["lc"]
        else:
            edges.append(("B", "C", "BC", symbols["BC"]))
            weight_c = 1 - symbols["lc"]
        if f_choice == 0:
            edges.append(("A", "F", "AF", symbols["AF"]))
            weight_f = symbols["lf"]
        else:
            edges.append(("E", "F", "EF", symbols["EF"]))
            weight_f = 1 - symbols["lf"]

        monomial = sp.Integer(1)
        for edge_index, (u, _v, _name, x_e) in enumerate(edges):
            side = component_leaf_labels(edges, edge_index, u)
            if xor_all(characters[i - 1] for i in side) != 0:
                monomial *= x_e
        total += weight_c * weight_f * monomial
    return sp.factor(total)


def orbit_coordinates(leaf_attachment: Mapping[str, int]) -> List[sp.Expr]:
    return [fourier_coordinate(rep, leaf_attachment, SYMS) for rep in ORBIT_REPS]


def check_orbit_representatives() -> None:
    automorphisms = []
    for perm in permutations((1, 2, 3)):
        f = {0: 0, 1: perm[0], 2: perm[1], 3: perm[2]}
        if all(f[a ^ b] == (f[a] ^ f[b]) for a in range(4) for b in range(4)):
            automorphisms.append(f)
    assert len(automorphisms) == 6

    zero_sum = [g for g in product(range(4), repeat=4) if xor_all(g) == 0]
    seen = set()
    representatives = []
    for g in zero_sum:
        if g in seen:
            continue
        orb = {tuple(f[x] for x in g) for f in automorphisms}
        seen.update(orb)
        representatives.append(min(orb))
    assert representatives == [(0, 0, 0, 0)] + ORBIT_REPS


# ---------------------------------------------------------------------------
# Shared ideal and gauge Jacobians
# ---------------------------------------------------------------------------
def check_invariants(coords_n: Sequence[sp.Expr], coords_np: Sequence[sp.Expr]) -> None:
    A, B, C, D, E, F, G, H, J, K, L, M, N, O = sp.symbols(
        "A B C D E F G H J K L M N O"
    )
    variables = [A, B, C, D, E, F, G, H, J, K, L, M, N, O]
    relations = [
        J - K - M + N,
        J - A * H - B * F + C * E,
        G * L - E * N,
        L**2 - B * E * H,
        B * M - D * L - B**2 * F + B * C * E,
        B * E * O - B * G * H - C * E * L + D * E * H,
    ]
    for label, coords in (("N", coords_n), ("N_prime", coords_np)):
        sub = dict(zip(variables, coords))
        for i, relation in enumerate(relations, start=1):
            require_zero(relation.subs(sub), f"shared invariant {i} on {label}")

    # Exact reconstruction on B*E != 0.
    J_rec = A * H + B * F - C * E
    N_rec = G * L / E
    M_rec = (D * L + B**2 * F - B * C * E) / B
    K_rec = J_rec + N_rec - M_rec
    O_rec = (B * G * H + C * E * L - D * E * H) / (B * E)
    reconstructed = [J_rec, K_rec, M_rec, N_rec, O_rec]
    assert len(reconstructed) == 5
    # Smoothness of L^2-BEH on the physical locus B*E != 0 follows from
    # partial derivative d/dH = -B*E.
    assert sp.diff(L**2 - B * E * H, H) == -B * E


def source_gauge(coords_n: Sequence[sp.Expr]):
    P, s, Q, t, R, u, v, S = sp.symbols("P s Q t R u v S")
    sub = {
        SYMS["p2"]: P,
        SYMS["DE"]: s,
        SYMS["p4"]: Q,
        SYMS["EF"]: t,
        SYMS["p3"]: R,
        SYMS["CD"]: u,
        SYMS["AB"]: v,
        SYMS["p1"]: S,
        SYMS["AC"]: sp.Rational(1, 2),
        SYMS["AF"]: sp.Rational(1, 2),
        SYMS["BC"]: sp.Rational(1, 2),
        SYMS["lc"]: sp.Rational(1, 2),
        SYMS["lf"]: sp.Rational(1, 2),
    }
    gauged = [sp.factor(c.subs(sub)) for c in coords_n]
    first8_expected = [
        Q * R * (s * u * (v + 1) + 8 * t) / 16,
        P * s * Q,
        P * R * (8 * s * t + u * (v + 1)) / 16,
        P * s * Q * R * (8 * t + u * (v + 1)) / 16,
        s * Q * u * S * (v + 1) / 4,
        R * S * (s * t * u * (v + 1) + 2 * v) / 8,
        s * Q * R * u * S * (t * (v + 1) + v) / 8,
        P * u * S * (v + 1) / 4,
    ]
    for i, (actual, expected) in enumerate(zip(gauged[:8], first8_expected), start=1):
        require_zero(actual - expected, f"source gauge formula {i}")

    variables = [P, s, Q, t, R, u, v, S]
    determinant = sp.factor(sp.det(sp.Matrix(gauged[:8]).jacobian(variables)))
    expected_det = -(
        P**3 * s**3 * Q**4 * t * R**4 * u**3 * v * S**3
        * (s - 1) ** 2 * (v - 1) * (v + 1) ** 2
    ) / 16384
    require_zero(determinant - expected_det, "source Jacobian determinant")
    return variables, gauged, determinant


def target_gauge(coords_np: Sequence[sp.Expr]):
    Pp, x, y, z, Rp, w, Sp, Qp = sp.symbols("Pp x y z Rp w Sp Qp")
    sub = {
        SYMS["p2"]: Pp,
        SYMS["DE"]: x,
        SYMS["AF"]: y,
        SYMS["AB"]: z,
        SYMS["p3"]: Rp,
        SYMS["CD"]: w,
        SYMS["p1"]: Sp,
        SYMS["p4"]: Qp,
        SYMS["AC"]: sp.Rational(1, 2),
        SYMS["EF"]: sp.Rational(1, 2),
        SYMS["BC"]: sp.Rational(1, 2),
        SYMS["lc"]: sp.Rational(1, 2),
        SYMS["lf"]: sp.Rational(1, 2),
    }
    gauged = [sp.factor(c.subs(sub)) for c in coords_np]
    first8_expected = [
        Qp * Rp * (x * w * (z + 1) + 8 * y * z) / 16,
        Pp * w * Qp * (z + 1) / 4,
        Pp * Rp * (2 * x + y * w * (z + 1)) / 8,
        Pp * Rp * w * Qp * (x * (z + 1) + 4 * y * z) / 16,
        x * w * Sp * Qp * (z + 1) / 4,
        Rp * Sp * (x * y * w * (z + 1) + 2) / 8,
        x * Rp * w * Sp * Qp * (4 * y * z + z + 1) / 16,
        Pp * x * Sp,
    ]
    for i, (actual, expected) in enumerate(zip(gauged[:8], first8_expected), start=1):
        require_zero(actual - expected, f"target gauge formula {i}")

    variables = [Pp, x, y, z, Rp, w, Sp, Qp]
    determinant = sp.factor(sp.det(sp.Matrix(gauged[:8]).jacobian(variables)))
    expected_det = -(
        Pp**3 * x**2 * y**2 * z * Rp**4 * w**4 * Sp**3 * Qp**4
        * (x - 1) ** 2 * (z - 1) * (z + 1) ** 3
    ) / 32768
    require_zero(determinant - expected_det, "target Jacobian determinant")
    return variables, gauged, determinant


# ---------------------------------------------------------------------------
# Exact algebraic common point and direct equality certificate
# ---------------------------------------------------------------------------
def exact_common_point(
    source_vars: Sequence[sp.Symbol],
    source_coords: Sequence[sp.Expr],
    target_vars: Sequence[sp.Symbol],
    target_coords: Sequence[sp.Expr],
):
    P, s, Q, t, R, u, v, S = source_vars
    source_values = {
        P: sp.Rational(1, 2),
        s: sp.Rational(2, 5),
        Q: sp.Rational(3, 8),
        t: sp.Rational(1, 3),
        R: sp.Rational(1, 2),
        u: sp.Rational(9, 20),
        v: sp.Rational(3, 5),
        S: sp.Rational(1, 5),
    }
    common = [sp.factor(c.subs(source_values)) for c in source_coords]
    expected = [
        sp.Rational(277, 8000),
        sp.Rational(3, 40),
        sp.Rational(67, 2400),
        sp.Rational(127, 16000),
        sp.Rational(27, 5000),
        sp.Rational(81, 5000),
        sp.Rational(153, 160000),
        sp.Rational(9, 500),
        sp.Rational(27, 16000),
        sp.Rational(261, 320000),
        sp.Rational(27, 10000),
        sp.Rational(27, 20000),
        sp.Rational(153, 320000),
        sp.Rational(183, 80000),
    ]
    assert common == expected

    A, B, C, D, _E, F, G, H = common[:8]
    P0 = source_values[P]
    calA = sp.factor(A * P0**2 / (B * C))
    calD = sp.factor(D * P0 / (B * C))
    calF = sp.factor(F * P0**2 / (C * H))
    calG = sp.factor(G * P0**3 / (B * C * H))
    X = sp.factor((calD - calG) / (1 - calF - calD + calG))
    ell = sp.factor((X - 1) / (calD - calG))
    m = sp.factor((ell - X) / 2)
    n = sp.factor((calG * ell - 1) / 4)
    omega = sp.factor(2 * n / (calA * ell - X))
    ratio = sp.factor(n / m)

    assert (calA, calD, calF, calG) == (
        sp.Rational(277, 67),
        sp.Rational(127, 67),
        sp.Rational(540, 67),
        sp.Rational(425, 134),
    )
    assert (X, ell, m, n, omega, ratio) == (
        sp.Rational(171, 775),
        sp.Rational(80936, 132525),
        sp.Rational(10339, 53010),
        sp.Rational(4967, 21204),
        sp.Rational(4967, 24430),
        sp.Rational(24835, 20678),
    )

    beta_symbol = sp.symbols("beta")
    beta = sp.Rational(10339, 24835) - 36 * sp.sqrt(233509269) / 8667415
    minpoly = 43337075 * beta_symbol**2 - 36083110 * beta_symbol + 7336259
    require_zero(minpoly.subs(beta_symbol, beta), "minimal polynomial at beta")
    assert sp.minpoly(beta, beta_symbol) == minpoly

    lower = sp.Rational(441, 1250)
    upper = sp.Rational(3529, 10000)
    # Exact root isolation: polynomial is positive at lower, negative at upper,
    # both are below the axis of symmetry, so the smaller root lies between.
    assert minpoly.subs(beta_symbol, lower) > 0
    assert minpoly.subs(beta_symbol, upper) < 0
    midpoint = sp.Rational(36083110, 2 * 43337075)
    assert upper < midpoint
    assert lower < beta < upper

    Pp, x, y, z, Rp, w, Sp, Qp = target_vars
    k = sp.factor(beta * ratio)
    target_values = {
        Pp: P0,
        x: X,
        y: sp.factor(m / beta),
        z: sp.factor(k / (1 - k)),
        Rp: sp.factor(4 * C / (P0 * ell)),
        w: sp.factor(4 * omega),
        Sp: sp.factor(H / (P0 * X)),
        Qp: sp.factor(B / (P0 * beta)),
    }
    expected_rationals = {
        Pp: sp.Rational(1, 2),
        x: sp.Rational(171, 775),
        Rp: sp.Rational(1767, 4832),
        w: sp.Rational(9934, 12215),
        Sp: sp.Rational(31, 190),
    }
    for var, value in expected_rationals.items():
        assert target_values[var] == value
    require_zero(target_values[y] - sp.Rational(10339, 53010) / beta, "target y")
    require_zero(
        target_values[z] - sp.Rational(24835, 1) * beta / (20678 - 24835 * beta),
        "target z",
    )
    require_zero(target_values[Qp] - sp.Rational(3, 20) / beta, "target Qp")

    # Physical inequalities proved from the rational isolating interval.
    assert 0 < X < 1
    assert 0 < target_values[Rp] < 1
    assert 0 < target_values[w] < 1
    assert 0 < target_values[Sp] < 1
    assert m < lower  # beta > m gives 0 < y < 1.
    assert upper * ratio < sp.Rational(1, 2)  # 0 < k < 1/2 gives 0 < z < 1.
    assert lower > sp.Rational(3, 20)  # 0 < Qp < 1.

    for i, (target_coordinate, value) in enumerate(zip(target_coords, common), start=1):
        require_zero(target_coordinate.subs(target_values) - value, f"common orbit coordinate {i}")

    # The quadratic map and its two branches.  The physical branch has z<1;
    # the other sends z to 1/z>1.  The double-root degeneration is z=1.
    quadratic = ratio * beta_symbol**2 - beta_symbol + omega
    require_zero(quadratic.subs(beta_symbol, beta), "quadratic parameter equation")
    discriminant = sp.factor(1 - 4 * ratio * omega)
    assert discriminant == sp.Rational(587088, 25258177) > 0
    other_beta = sp.factor(1 / ratio - beta)
    k_other = sp.factor(other_beta * ratio)
    require_zero(k_other - (1 - k), "quadratic branch complement")
    require_zero(
        k_other / (1 - k_other) - 1 / target_values[z],
        "second branch gives reciprocal z",
    )

    return source_values, target_values, common, beta


def all_fourier_coordinates(
    leaf_attachment: Mapping[str, int],
    substitutions: Mapping[sp.Symbol, sp.Expr],
) -> Dict[Tuple[int, int, int, int], sp.Expr]:
    result = {}
    for chars in product(range(4), repeat=4):
        value = fourier_coordinate(chars, leaf_attachment, SYMS)
        result[chars] = sp.factor(value.subs(substitutions))
    return result


def check_direct_distribution_equality(
    source_gauge_vars: Sequence[sp.Symbol],
    source_values: Mapping[sp.Symbol, sp.Expr],
    target_gauge_vars: Sequence[sp.Symbol],
    target_values: Mapping[sp.Symbol, sp.Expr],
) -> None:
    P, s, Q, t, R, u, v, S = source_gauge_vars
    source_full_sub = {
        SYMS["p2"]: source_values[P],
        SYMS["DE"]: source_values[s],
        SYMS["p4"]: source_values[Q],
        SYMS["EF"]: source_values[t],
        SYMS["p3"]: source_values[R],
        SYMS["CD"]: source_values[u],
        SYMS["AB"]: source_values[v],
        SYMS["p1"]: source_values[S],
        SYMS["AC"]: sp.Rational(1, 2),
        SYMS["AF"]: sp.Rational(1, 2),
        SYMS["BC"]: sp.Rational(1, 2),
        SYMS["lc"]: sp.Rational(1, 2),
        SYMS["lf"]: sp.Rational(1, 2),
    }
    Pp, x, y, z, Rp, w, Sp, Qp = target_gauge_vars
    target_full_sub = {
        SYMS["p2"]: target_values[Pp],
        SYMS["DE"]: target_values[x],
        SYMS["AF"]: target_values[y],
        SYMS["AB"]: target_values[z],
        SYMS["p3"]: target_values[Rp],
        SYMS["CD"]: target_values[w],
        SYMS["p1"]: target_values[Sp],
        SYMS["p4"]: target_values[Qp],
        SYMS["AC"]: sp.Rational(1, 2),
        SYMS["EF"]: sp.Rational(1, 2),
        SYMS["BC"]: sp.Rational(1, 2),
        SYMS["lc"]: sp.Rational(1, 2),
        SYMS["lf"]: sp.Rational(1, 2),
    }
    n_attach = {"B": 1, "D": 2, "F": 3, "E": 4}
    np_attach = {"B": 4, "D": 2, "F": 3, "E": 1}
    qhat_n = all_fourier_coordinates(n_attach, source_full_sub)
    qhat_np = all_fourier_coordinates(np_attach, target_full_sub)
    assert len(qhat_n) == len(qhat_np) == 256
    for chars in qhat_n:
        require_zero(qhat_n[chars] - qhat_np[chars], f"Fourier tensor entry {chars}")

    # Verify invertibility of the one-taxon character transform exactly.
    def dot2(a: int, b: int) -> int:
        return ((a & 1) * (b & 1) + ((a >> 1) & 1) * ((b >> 1) & 1)) % 2

    hadamard = sp.Matrix([[(-1) ** dot2(g, a) for a in range(4)] for g in range(4)])
    assert hadamard * hadamard.T == 4 * sp.eye(4)
    # Hence equality of all 4^4 Fourier entries is exactly equality of all
    # 4^4 leaf-pattern probabilities under the tensor inverse transform.


def main() -> None:
    data = load_networks()
    common = data["common_internal_structure"]
    n_spec, np_spec = data["networks"]
    ug_n = check_binary_rooted_class(common, n_spec)
    ug_np = check_binary_rooted_class(common, np_spec)
    passed("both rooted DAGs are LSA-valid, binary, tree-child, and level 2")
    check_not_triangle_equivalent(ug_n, ug_np)
    passed("the two leaf-labelled semi-directed topologies are not triangle-equivalent")

    check_orbit_representatives()
    passed("the 14 listed nontrivial coordinates represent all JC Fourier orbits")

    n_attach = {"B": 1, "D": 2, "F": 3, "E": 4}
    np_attach = {"B": 4, "D": 2, "F": 3, "E": 1}
    coords_n = orbit_coordinates(n_attach)
    coords_np = orbit_coordinates(np_attach)
    check_invariants(coords_n, coords_np)
    passed("all six polynomial invariants vanish identically on both full models")

    source_vars, source_coords, source_det = source_gauge(coords_n)
    target_vars, target_coords, target_det = target_gauge(coords_np)
    passed("both eight-coordinate gauge maps and both factored Jacobians are exact")

    source_values, target_values, common_vector, beta = exact_common_point(
        source_vars, source_coords, target_vars, target_coords
    )
    passed("the algebraic target point is strictly stochastic and matches all 14 orbit coordinates")

    check_direct_distribution_equality(source_vars, source_values, target_vars, target_values)
    passed("all 256 Fourier entries, hence all 256 leaf-pattern probabilities, agree exactly")

    # Exact nonvanishing at the common physical point.
    assert source_det.subs(source_values) != 0
    assert target_det.subs(target_values) != 0
    passed("both first-eight-coordinate Jacobians are nonzero at the common distribution")

    print("\n[PROVED] CERTIFICATE COMPLETE")
    print("Common model-image dimension: 8")
    print("Common orbit vector:")
    for name, value in zip(COORD_NAMES, common_vector):
        print(f"  {name} = {value}")
    print(f"beta ≈ {sp.N(beta, 16)} (decimal shown only for readability)")
    print("Conclusion: the specified non-triangle-equivalent pair has an 8-dimensional")
    print("relatively open stochastic model overlap in the open JC parameter domain.")


if __name__ == "__main__":
    main()
