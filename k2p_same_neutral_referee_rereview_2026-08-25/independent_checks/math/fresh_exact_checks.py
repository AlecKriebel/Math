#!/usr/bin/env python3
"""Independent exact checks for the revised K2P mathematical review.

This script deliberately imports no submitted classifier or certificate code.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product

import sympy as sp
import networkx as nx


CHARS = (0, 1, 2, 3)  # 0,C,G,T with Klein addition = xor


def edge_value(h: int, s, g):
    if h == 0:
        return sp.Integer(1)
    if h == 2:
        return g
    return s


def quartet_checks() -> dict[str, object]:
    ss = sp.symbols("s1:5", positive=True)
    gi = sp.symbols("gI", positive=True)
    splits = {
        "A": ({0, 1}, {2, 3}),
        "B": ({0, 2}, {1, 3}),
        "C": ({0, 3}, {1, 2}),
    }
    words = {
        "Q0": (1, 1, 1, 1),       # CCCC
        "QA": (1, 1, 3, 3),       # CCTT
        "QB": (1, 3, 1, 3),       # CTCT
        "QC": (1, 3, 3, 1),       # CTTC
    }

    def q(topology: str, word: tuple[int, ...]):
        pendant = sp.prod(ss)
        side = splits[topology][0]
        internal_char = 0
        for i in side:
            internal_char ^= word[i]
        return sp.expand(pendant * (gi if internal_char == 2 else 1))

    table = {}
    for topology in splits:
        values = {name: q(topology, word) for name, word in words.items()}
        f_a = sp.expand(values["Q0"] - values["QA"])
        j_b = sp.expand(values["Q0"] - values["QA"] + values["QB"] - values["QC"])
        table[topology] = {"F_A": str(f_a), "J_B": str(j_b)}

    p = sp.prod(ss)
    assert sp.expand(q("A", words["Q0"]) - q("A", words["QA"])) == 0
    assert sp.expand(q("B", words["Q0"]) - q("B", words["QA"])) == sp.expand(p * (1 - gi))
    assert sp.expand(q("C", words["Q0"]) - q("C", words["QA"])) == sp.expand(p * (1 - gi))
    expected_j = {"A": 0, "B": sp.expand(2 * p * (1 - gi)), "C": 0}
    for topology in splits:
        vals = {name: q(topology, word) for name, word in words.items()}
        got = sp.expand(vals["Q0"] - vals["QA"] + vals["QB"] - vals["QC"])
        assert sp.expand(got - expected_j[topology]) == 0
    return table


def sunlet_checks() -> dict[str, object]:
    names = "a_s a_g b_s b_g c_s c_g d_s d_g e_s e_g f_s f_g delta"
    (a_s, a_g, b_s, b_g, c_s, c_g, d_s, d_g, e_s, e_g,
     f_s, f_g, delta) = sp.symbols(names)
    spectra = {
        "a": (1, a_s, a_g, a_s),
        "b": (1, b_s, b_g, b_s),
        "c": (1, c_s, c_g, c_s),
        "d": (1, d_s, d_g, d_s),
        "e": (1, e_s, e_g, e_s),
        "f": (1, f_s, f_g, f_s),
    }

    def q(x: int, y: int, z: int):
        assert x ^ y ^ z == 0
        return sp.expand(
            spectra["a"][x] * spectra["b"][y] * spectra["c"][z]
            * (delta * spectra["f"][y] * spectra["d"][z]
               + (1 - delta) * spectra["f"][x] * spectra["e"][z])
        )

    xs, xg = q(1, 1, 0), q(2, 2, 0)
    ys, yg = q(1, 0, 1), q(2, 0, 2)
    zs, zg = q(0, 1, 1), q(0, 2, 2)
    u, v, w = q(1, 2, 3), q(1, 3, 2), q(2, 1, 3)
    ti = sp.factor(v**2 * xg - xs**2 * yg * zg)
    expected = sp.factor(
        -a_s**2 * b_s**2 * a_g * b_g * c_g**2 * f_s**2
        * delta * (1 - delta) * d_g * e_g * (1 - f_g)**2
    )
    assert sp.expand(ti - expected) == 0

    witness = {
        a_s: F(1, 2), a_g: F(1, 2),
        b_s: F(1, 2), b_g: F(1, 2),
        c_s: F(1, 2), c_g: F(1, 2),
        d_s: F(1, 2), d_g: F(1, 2),
        e_s: F(1, 2), e_g: F(1, 2),
        f_s: F(1, 3), f_g: F(1, 3), delta: F(1, 2),
    }
    outputs = (xs, xg, ys, yg, zs, zg, u, v, w)
    params = (a_s, a_g, b_s, b_g, c_s, c_g, d_s, d_g, e_s, e_g, f_s, f_g, delta)
    jac = sp.Matrix(outputs).jacobian(params).subs(witness)
    assert jac.rank() == 9

    # Recreate the two displayed logarithmic blocks from explicit directions.
    z0 = (xs, ys, zs, w)
    sym_edges = ((a_s, a_g), (b_s, b_g), (c_s, c_g), (f_s, f_g))
    j0 = sp.zeros(4, 4)
    for i, out in enumerate(z0):
        for j, (ps, pg) in enumerate(sym_edges):
            derivative = ps * sp.diff(out, ps) + pg * sp.diff(out, pg)
            j0[i, j] = sp.factor((derivative / out).subs(witness))

    zperp = (xg / xs, yg / ys, zg / zs, u / w, v / w)
    anis_edges = (a_g, b_g, c_g, d_g, f_g)
    jp = sp.zeros(5, 5)
    for i, out in enumerate(zperp):
        for j, pg in enumerate(anis_edges):
            derivative = pg * sp.diff(out, pg)
            jp[i, j] = sp.factor((derivative / out).subs(witness))

    assert j0.det() == -sp.Rational(1, 2)
    assert jp.det() == -sp.Rational(1, 4)
    return {
        "Ti_factor": str(ti),
        "witness_outputs": [str(sp.factor(o.subs(witness))) for o in outputs],
        "full_jacobian_rank": jac.rank(),
        "J0": [list(map(str, row)) for row in j0.tolist()],
        "J0_det": str(j0.det()),
        "Jperp": [list(map(str, row)) for row in jp.tolist()],
        "Jperp_det": str(jp.det()),
    }


def displayed_network_map(arcs, retic_parents, internal_edges):
    """Return the ten normalized 3-leaf orbit expressions from primitive arcs."""
    edge_symbols = {}
    params = []
    for edge in internal_edges:
        tag = "_".join(edge)
        s, g = sp.symbols(f"s_{tag} g_{tag}")
        edge_symbols[edge] = (s, g)
        params.extend((s, g))
    lambdas = {r: sp.symbols(f"lambda_{r}") for r in retic_parents}
    params.extend(lambdas.values())
    patterns = (
        (0, 0, 0), (0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 1, 0),
        (1, 2, 3), (1, 3, 2), (2, 0, 2), (2, 1, 3), (2, 2, 0),
    )
    leaves = {"L0": 0, "L1": 1, "L2": 2}
    expressions = []
    retics = tuple(retic_parents)
    for pattern in patterns:
        total = 0
        for bits in product((0, 1), repeat=len(retics)):
            selected = set(arcs)
            weight = 1
            for r, bit in zip(retics, bits):
                p0, p1 = retic_parents[r]
                chosen, omitted = (p0, p1) if bit == 0 else (p1, p0)
                selected.remove((omitted, r))
                lam = lambdas[r]
                weight *= lam if bit == 0 else (1 - lam)
            children = {}
            for u, v in selected:
                children.setdefault(u, []).append(v)

            memo = {}

            def desc(v):
                if v in memo:
                    return memo[v]
                if v in leaves:
                    ans = {leaves[v]}
                else:
                    ans = set()
                    for child in children.get(v, ()):
                        ans.update(desc(child))
                memo[v] = ans
                return ans

            term = weight
            for edge in internal_edges:
                if edge not in selected:
                    continue
                h = 0
                for leaf_index in desc(edge[1]):
                    h ^= pattern[leaf_index]
                s, g = edge_symbols[edge]
                term *= edge_value(h, s, g)
            total += term
        expressions.append(sp.factor(total))
    return tuple(expressions), tuple(params), edge_symbols, lambdas


def weak_sharpness_checks() -> dict[str, object]:
    arcs_w = (
        ("r", "S"), ("r", "L0"), ("S", "U"), ("S", "V"),
        ("U", "X"), ("V", "Z"), ("Z", "X"), ("U", "V"),
        ("Z", "L1"), ("X", "L2"),
    )
    internal_w = (
        ("r", "S"), ("S", "U"), ("S", "V"), ("U", "X"),
        ("V", "Z"), ("Z", "X"), ("U", "V"),
    )
    retics_w = {"V": ("S", "U"), "X": ("Z", "U")}
    expr_w, params_w, edges_w, lams_w = displayed_network_map(arcs_w, retics_w, internal_w)

    arcs_wp = (
        ("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"),
        ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V"),
        ("X0", "L1"), ("X1", "L2"),
    )
    internal_wp = (
        ("r", "S"), ("S", "U"), ("S", "X0"), ("V", "X0"),
        ("U", "X1"), ("V", "X1"), ("U", "V"),
    )
    retics_wp = {"X1": ("V", "U"), "X0": ("V", "S")}
    expr_wp, params_wp, edges_wp, lams_wp = displayed_network_map(arcs_wp, retics_wp, internal_wp)

    witness_w = {}
    for s, g in edges_w.values():
        witness_w[s] = F(1, 7)
        witness_w[g] = F(1, 7)
    witness_w[lams_w["X"]] = F(15996, 16339)
    witness_w[lams_w["V"]] = F(1, 8)

    witness_wp = {}
    for s, g in edges_wp.values():
        witness_wp[s] = F(1, 4)
        witness_wp[g] = F(1, 4)
    witness_wp[lams_wp["X1"]] = F(1, 2)
    witness_wp[lams_wp["X0"]] = F(1, 6)

    vals_w = tuple(sp.factor(x.subs(witness_w)) for x in expr_w)
    vals_wp = tuple(sp.factor(x.subs(witness_wp)) for x in expr_wp)
    expected_w = (
        1, F(64009, 457492), F(64009, 457492), F(6400, 39229939),
        F(1, 1372), F(4048, 39229939), F(4048, 39229939),
        F(6400, 39229939), F(4048, 39229939), F(1, 1372),
    )
    expected_wp = (
        1, F(15, 1024), F(15, 1024), F(5, 512), F(27, 512),
        F(9, 4096), F(9, 4096), F(5, 512), F(9, 4096), F(27, 512),
    )
    assert vals_w == expected_w
    assert vals_wp == expected_wp

    rank_w = sp.Matrix(expr_w[1:]).jacobian(params_w).subs(witness_w).rank()
    rank_wp = sp.Matrix(expr_wp[1:]).jacobian(params_wp).subs(witness_wp).rank()
    assert rank_w == rank_wp == 9

    delta = F(1, 2**30)
    pendant_w = (F(86779, 80) * delta, F(320, 253) * delta, F(114373, 20240) * delta)
    pendant_wp = (F(16, 3) * delta, F(32, 9) * delta, F(96, 5) * delta)
    patterns = (
        (0, 0, 0), (0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 1, 0),
        (1, 2, 3), (1, 3, 2), (2, 0, 2), (2, 1, 3), (2, 2, 0),
    )

    def add_pendants(values, pendants):
        return tuple(
            sp.factor(value * sp.prod(pendants[i] for i, h in enumerate(pattern) if h != 0))
            for value, pattern in zip(values, patterns)
        )

    full_w = add_pendants(vals_w, pendant_w)
    full_wp = add_pendants(vals_wp, pendant_wp)
    assert full_w == full_wp
    expected_full = tuple(
        1 if pattern == (0, 0, 0)
        else delta**2 if sum(h != 0 for h in pattern) == 2
        else F(4, 5) * delta**3
        for pattern in patterns
    )
    assert full_w == expected_full

    for s, g in ((F(1, 7), F(1, 7)), (F(1, 4), F(1, 4))):
        assert 0 < s < 1 and s * s < g < 1
    for x in pendant_w + pendant_wp:
        assert 0 < x < 1 and x * x < x

    us, ug, vs, vg = sp.symbols("us ug vs vg", positive=True)
    obs = sp.Matrix((us / vs, us * vs, ug / vg, ug * vg))
    cherry_det = sp.factor(obs.jacobian((us, vs, ug, vg)).det())
    assert cherry_det == 4 * us * ug / (vs * vg)
    actual_det = cherry_det.subs({us: F(2, 5), ug: F(4, 9), vs: F(3, 7), vg: F(5, 11)})
    assert actual_det == F(2464, 675)
    return {
        "normalized_W": list(map(str, vals_w)),
        "normalized_Wprime": list(map(str, vals_wp)),
        "rank_W": rank_w,
        "rank_Wprime": rank_wp,
        "common_full_tensor": list(map(str, full_w)),
        "cherry_det": str(cherry_det),
        "cherry_det_witness": str(actual_det),
    }


def suppress_displayed_root(arcs, retics):
    root = "r"
    children = [v for u, v in arcs if u == root]
    assert len(children) == 2
    mixed = []
    for u, v in arcs:
        if u == root:
            continue
        mixed.append((u, v, v in retics))
    u, v = children
    # The merged edge retains any arrowhead formerly incident to a reticulation.
    if u in retics and v in retics:
        raise AssertionError("double-headed root suppression is not standard")
    if u in retics:
        mixed.append((v, u, True))
    elif v in retics:
        mixed.append((u, v, True))
    else:
        mixed.append(tuple(sorted((u, v))) + (False,))
    canonical = []
    for u, v, headed in mixed:
        if headed:
            canonical.append((u, v, True))  # tail, headed reticulation
        else:
            a, b = sorted((u, v))
            canonical.append((a, b, False))
    return tuple(canonical)


def rooting_census(mixed, retics, leaves):
    vertices = sorted({x for edge in mixed for x in edge[:2]})
    rows = []
    for root_index, root_edge in enumerate(mixed):
        u0, v0, headed0 = root_edge
        fixed = []
        ordinary = []
        for index, (u, v, headed) in enumerate(mixed):
            if index == root_index:
                continue
            if headed:
                fixed.append((u, v))
            else:
                ordinary.append((u, v))
        root_name = "ROOT"
        fixed.extend(((root_name, u0), (root_name, v0)))
        for bits in product((0, 1), repeat=len(ordinary)):
            directed = list(fixed)
            for (u, v), bit in zip(ordinary, bits):
                directed.append((u, v) if bit == 0 else (v, u))
            graph = nx.DiGraph()
            graph.add_nodes_from(vertices + [root_name])
            graph.add_edges_from(directed)
            if not nx.is_directed_acyclic_graph(graph):
                continue
            if set(nx.descendants(graph, root_name)) != set(vertices):
                continue
            valid = graph.in_degree(root_name) == 0 and graph.out_degree(root_name) == 2
            for v in vertices:
                indeg, outdeg = graph.in_degree(v), graph.out_degree(v)
                if v in leaves:
                    valid &= (indeg, outdeg) == (1, 0)
                elif v in retics:
                    valid &= (indeg, outdeg) == (2, 1)
                else:
                    valid &= (indeg, outdeg) == (1, 2)
            if not valid:
                continue
            # Enforce the paper's lowest-stable-ancestor root convention.
            root_is_lsa = True
            for candidate in vertices:
                without = graph.copy()
                without.remove_node(candidate)
                if all(leaf not in without or not nx.has_path(without, root_name, leaf)
                       for leaf in leaves):
                    root_is_lsa = False
                    break
            if not root_is_lsa:
                continue
            tree_child = all(
                any(child not in retics for child in graph.successors(v))
                for v in [root_name] + [x for x in vertices if x not in leaves]
            )
            rows.append({"root_edge": root_index, "tree_child": bool(tree_child)})
    return rows


def mixed_incidence_graph(mixed, leaves, forgotten_triangle=None):
    graph = nx.Graph()
    for vertex in {x for edge in mixed for x in edge[:2]}:
        graph.add_node(("v", vertex), kind="leaf" if vertex in leaves else "vertex",
                       label=vertex if vertex in leaves else None)
    forgotten_triangle = set(forgotten_triangle or ())
    for index, (u, v, headed) in enumerate(mixed):
        edge_key = frozenset((u, v))
        graph.add_node(("e", index), kind="forgotten_edge" if edge_key in forgotten_triangle else "edge",
                       label=None)
        graph.add_edge(("v", u), ("e", index), head=False)
        graph.add_edge(("v", v), ("e", index), head=False if edge_key in forgotten_triangle else bool(headed))
    return graph


def ordinary_triangles(mixed):
    simple = nx.Graph()
    simple.add_edges_from((u, v) for u, v, _ in mixed)
    headed_at = {}
    for u, v, headed in mixed:
        headed_at[frozenset((u, v))] = v if headed else None
    out = []
    for triple in product(simple.nodes, repeat=3):
        if len(set(triple)) != 3:
            continue
        verts = tuple(sorted(triple))
        edges = {frozenset((verts[i], verts[(i + 1) % 3])) for i in range(3)}
        if not all(len(e) == 2 and simple.has_edge(*tuple(e)) for e in edges):
            continue
        heads = [headed_at[e] for e in edges if headed_at[e] is not None]
        if len(heads) == 2 and heads[0] == heads[1]:
            out.append(frozenset(edges))
    unique = []
    for item in out:
        if item not in unique:
            unique.append(item)
    return unique


def weak_graph_checks() -> dict[str, object]:
    arcs_w = (
        ("r", "S"), ("r", "L0"), ("S", "U"), ("S", "V"),
        ("U", "X"), ("V", "Z"), ("Z", "X"), ("U", "V"),
        ("Z", "L1"), ("X", "L2"),
    )
    arcs_wp = (
        ("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"),
        ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V"),
        ("X0", "L1"), ("X1", "L2"),
    )
    ret_w, ret_wp = {"V", "X"}, {"X0", "X1"}
    leaves = {"L0", "L1", "L2"}
    mixed_w = suppress_displayed_root(arcs_w, ret_w)
    mixed_wp = suppress_displayed_root(arcs_wp, ret_wp)
    roots_w = rooting_census(mixed_w, ret_w, leaves)
    roots_wp = rooting_census(mixed_wp, ret_wp, leaves)
    assert (len(roots_w), sum(x["tree_child"] for x in roots_w)) == (5, 2)
    assert (len(roots_wp), sum(x["tree_child"] for x in roots_wp)) == (7, 2)

    node_match = nx.algorithms.isomorphism.categorical_node_match(("kind", "label"), (None, None))
    edge_match = nx.algorithms.isomorphism.categorical_edge_match("head", False)
    iso = nx.is_isomorphic(
        mixed_incidence_graph(mixed_w, leaves), mixed_incidence_graph(mixed_wp, leaves),
        node_match=node_match, edge_match=edge_match,
    )
    assert not iso
    triangles_w, triangles_wp = ordinary_triangles(mixed_w), ordinary_triangles(mixed_wp)
    assert len(triangles_w) == len(triangles_wp) == 1
    triangle_iso = False
    for tw in triangles_w:
        for twp in triangles_wp:
            if nx.is_isomorphic(
                mixed_incidence_graph(mixed_w, leaves, tw),
                mixed_incidence_graph(mixed_wp, leaves, twp),
                node_match=node_match, edge_match=edge_match,
            ):
                triangle_iso = True
    assert not triangle_iso
    return {
        "W_rooting_census": [len(roots_w), sum(x["tree_child"] for x in roots_w),
                              sum(not x["tree_child"] for x in roots_w)],
        "Wprime_rooting_census": [len(roots_wp), sum(x["tree_child"] for x in roots_wp),
                                   sum(not x["tree_child"] for x in roots_wp)],
        "labelled_isomorphic": iso,
        "ordinary_triangles": [len(triangles_w), len(triangles_wp)],
        "triangle_equivalent": triangle_iso,
    }


def completion_counts() -> dict[str, int]:
    tuples = ((2, 1, 1), (5, 1, 2), (5, 1, 2), (6, 2, 4), (6, 2, 2))

    def choose(n: int, k: int) -> int:
        return int(sp.binomial(n, k)) if 0 <= k <= n else 0

    def count(k: int, epsilon: int) -> int:
        return sum(
            r * sum(choose(q, j) * choose(k - epsilon - j + m - 1, m - 1)
                    for j in range(q + 1))
            for m, q, r in tuples
        )

    out = {"C(4,1)": count(4, 1), "C(4,0)": count(4, 0),
           "C(5,1)": count(5, 1), "C(5,0)": count(5, 0)}
    assert out == {"C(4,1)": 831, "C(4,0)": 1983, "C(5,1)": 1983, "C(5,0)": 4155}
    return out


def domain_checks() -> dict[str, object]:
    # Boundary-near exact witnesses, not floating-point samples.
    points = (
        (F(999, 1000), F(998001, 1000000) + F(1, 10**9)),
        (F(500001, 1000000), F(3, 10**6)),
        (F(1, 10**6), F(1, 10**9)),
    )
    rows = []
    for s, g in points:
        dplus = 0 < s < 1 and 0 < g < 1 and g > 2 * s - 1
        ct = 0 < s < 1 and s * s < g < 1
        assert dplus
        probs = ((1 + 2 * s + g) / 4, (1 - g) / 4, (1 - 2 * s + g) / 4, (1 - g) / 4)
        assert all(p > 0 for p in probs)
        rows.append({"s": str(s), "g": str(g), "D_plus": dplus, "CT": ct,
                     "min_transition": str(min(probs))})
    return {"boundary_rows": rows}


def main() -> None:
    report = {
        "quartet": quartet_checks(),
        "sunlet_triangle": sunlet_checks(),
        "weak_sharpness": weak_sharpness_checks(),
        "weak_graphs": weak_graph_checks(),
        "completion_counts": completion_counts(),
        "domain": domain_checks(),
    }
    import json
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
