#!/usr/bin/env python3
"""Independent exact checks for the R6 K2P-SAME mathematical review.

This script deliberately does not import any module from the submission.  It
reconstructs the small hand-checkable universes directly from the definitions
printed in the article: completion counts, repair transversals, K2P domain
inequalities, the tree--sunlet and triangle calculations, and the complete
three-leaf weak-sharpness witness (graphs, tensors, and Jacobian minors).
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


def frac(x):
    if isinstance(x, F):
        return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)
    if isinstance(x, sp.Rational):
        return f"{int(x.p)}/{int(x.q)}" if x.q != 1 else str(int(x.p))
    return x


def dplus(pair):
    s, g = pair
    return 0 < s < 1 and 0 < g < 1 and g > 2 * s - 1


def dct(pair):
    s, g = pair
    return 0 < s < 1 and s * s < g < 1


def inverse_probs(pair):
    s, g = pair
    return ((1 + 2 * s + g) / 4, (1 - g) / 4,
            (1 - 2 * s + g) / 4, (1 - g) / 4)


def completion_count(k, incoming):
    # cycle, theta0, theta1, theta2, theta3
    tuples = ((2, 1, 1), (5, 1, 2), (5, 1, 2), (6, 2, 4), (6, 2, 2))
    total = 0
    for m, q, repair_tags in tuples:
        for j in range(q + 1):
            total += repair_tags * math.comb(q, j) * math.comb(
                k - incoming - j + m - 1, m - 1
            )
    return total


def minimal_transversals(universe, clauses):
    valid = []
    for size in range(len(universe) + 1):
        for subset_tuple in itertools.combinations(universe, size):
            subset = set(subset_tuple)
            if all(subset & set(clause) for clause in clauses):
                if not any(set(old) < subset for old in valid):
                    valid.append(tuple(sorted(subset)))
    return sorted(valid)


def directed_paths(arcs, start, target):
    children = {}
    for u, v in arcs:
        children.setdefault(u, []).append(v)
    out = []

    def dfs(v, path):
        if v == target:
            out.append(tuple(path))
            return
        for w in children.get(v, []):
            if w not in path:
                dfs(w, path + [w])

    dfs(start, [start])
    return out


def is_acyclic(nodes, arcs):
    children = {v: [] for v in nodes}
    indeg = {v: 0 for v in nodes}
    for u, v in arcs:
        children[u].append(v)
        indeg[v] += 1
    queue = [v for v in nodes if indeg[v] == 0]
    seen = 0
    while queue:
        v = queue.pop()
        seen += 1
        for w in children[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                queue.append(w)
    return seen == len(nodes)


def suppress_root(rooted_arcs, retics, root="r"):
    root_children = [v for u, v in rooted_arcs if u == root]
    assert len(root_children) == 2
    mixed = []
    for u, v in rooted_arcs:
        if u == root:
            continue
        mixed.append((u, v, v if v in retics else None))
    a, b = root_children
    # The two witness root arcs are ordinary; retain general head metadata.
    head = a if a in retics else b if b in retics else None
    mixed.append((a, b, head))
    return mixed


def enumerate_rootings(rooted_arcs, retics, leaves):
    mixed = suppress_root(rooted_arcs, retics)
    base_nodes = sorted({x for e in mixed for x in e[:2]})
    internal_tree = set(base_nodes) - set(retics) - set(leaves)
    records = []
    for root_edge_index, root_edge in enumerate(mixed):
        ordinary_indices = [i for i, e in enumerate(mixed)
                            if e[2] is None and i != root_edge_index]
        for bits in itertools.product((0, 1), repeat=len(ordinary_indices)):
            arcs = []
            u0, v0, h0 = root_edge
            if h0 is None:
                arcs.extend((('rho', u0), ('rho', v0)))
            else:
                tail = v0 if h0 == u0 else u0
                arcs.extend((('rho', tail), ('rho', h0)))
            bit_map = dict(zip(ordinary_indices, bits))
            for i, (u, v, head) in enumerate(mixed):
                if i == root_edge_index:
                    continue
                if head is not None:
                    tail = v if head == u else u
                    arcs.append((tail, head))
                elif bit_map[i] == 0:
                    arcs.append((u, v))
                else:
                    arcs.append((v, u))
            nodes = base_nodes + ['rho']
            indeg = {v: 0 for v in nodes}
            outdeg = {v: 0 for v in nodes}
            for u, v in arcs:
                outdeg[u] += 1
                indeg[v] += 1
            degrees_ok = (
                indeg['rho'] == 0 and outdeg['rho'] == 2
                and all(indeg[v] == 2 and outdeg[v] == 1 for v in retics)
                and all(indeg[v] == 1 and outdeg[v] == 2 for v in internal_tree)
                and all(indeg[v] == 1 and outdeg[v] == 0 for v in leaves)
            )
            if not degrees_ok or not is_acyclic(nodes, arcs):
                continue
            # Reachability and the lowest-stable-ancestor convention.
            paths_by_leaf = [directed_paths(arcs, 'rho', leaf) for leaf in leaves]
            if any(not paths for paths in paths_by_leaf):
                continue
            stable = set(nodes)
            for paths in paths_by_leaf:
                on_every_path = set(paths[0])
                for path in paths[1:]:
                    on_every_path &= set(path)
                stable &= on_every_path
            if stable != {'rho'}:
                continue
            children = {v: [] for v in nodes}
            for u, v in arcs:
                children[u].append(v)
            tree_child = all(
                any(child not in retics for child in children[v])
                for v in set(nodes) - set(leaves)
            )
            records.append({
                "root_edge": root_edge_index,
                "arcs": sorted([list(e) for e in arcs]),
                "tree_child": tree_child,
            })
    # Degree constraints make each admissible edge rooting unique; assert that
    # the brute orientation search did not create duplicates.
    keys = {tuple(tuple(e) for e in rec["arcs"]) for rec in records}
    assert len(keys) == len(records)
    return records, mixed


def triangle_nodes(mixed):
    adj = {}
    for u, v, _ in mixed:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    tris = []
    for tri in itertools.combinations(sorted(adj), 3):
        if all(b in adj[a] for a, b in itertools.combinations(tri, 2)):
            tris.append(set(tri))
    return tris


def mixed_isomorphic(m1, m2, leaves, forget_triangle_heads=False):
    nodes1 = sorted({x for e in m1 for x in e[:2]})
    nodes2 = sorted({x for e in m2 for x in e[:2]})
    ints1 = [x for x in nodes1 if x not in leaves]
    ints2 = [x for x in nodes2 if x not in leaves]
    if len(ints1) != len(ints2):
        return False
    tri1 = triangle_nodes(m1)
    tri2 = triangle_nodes(m2)
    assert len(tri1) == len(tri2) == 1

    def edge_signature(edge, tri):
        u, v, head = edge
        if forget_triangle_heads and u in tri and v in tri:
            head = None
        if head is None:
            return frozenset((u, v)), None
        return frozenset((u, v)), head

    sig2 = {edge_signature(e, tri2[0]) for e in m2}
    for perm in itertools.permutations(ints2):
        mp = dict(zip(ints1, perm))
        mp.update({leaf: leaf for leaf in leaves})
        mapped = set()
        for u, v, head in m1:
            mh = mp[head] if head is not None else None
            if forget_triangle_heads and u in tri1[0] and v in tri1[0]:
                mh = None
            mapped.add((frozenset((mp[u], mp[v])), mh))
        if mapped == sig2:
            return True
    return False


def descendants(arcs, start, leaves):
    children = {}
    for u, v in arcs:
        children.setdefault(u, []).append(v)
    stack = [start]
    seen = set()
    out = set()
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        if v in leaves:
            out.add(v)
        stack.extend(children.get(v, []))
    return out


def eig(pair, h):
    if h == 0:
        return 1
    return pair[1] if h == 2 else pair[0]


def fourier_q(arcs, retic_parent_weights, edge_pairs, leaf_order, chars):
    assert len(leaf_order) == len(chars) and not math.prod([1]) == 0
    assert chars[0] ^ chars[1] ^ chars[2] == 0
    incoming = {}
    for u, v in arcs:
        if v in retic_parent_weights:
            incoming.setdefault(v, []).append(u)
    total = 0
    choices = [list(retic_parent_weights[r]) for r in sorted(retic_parent_weights)]
    for selected_parents in itertools.product(*choices):
        selected = dict(zip(sorted(retic_parent_weights), selected_parents))
        present = [(u, v) for u, v in arcs
                   if v not in selected or selected[v] == u]
        weight = 1
        for r, parent in selected.items():
            weight *= retic_parent_weights[r][parent]
        term = weight
        for edge in present:
            u, v = edge
            below = descendants(present, v, set(leaf_order))
            h = 0
            for leaf, char in zip(leaf_order, chars):
                if leaf in below:
                    h ^= char
            term *= eig(edge_pairs[edge], h)
        total += term
    return sp.cancel(total)


def graph_and_tensor_checks():
    W_arcs = [('r', 'S'), ('r', 'L0'), ('S', 'U'), ('S', 'V'),
              ('U', 'X'), ('V', 'Z'), ('Z', 'X'), ('U', 'V'),
              ('Z', 'L1'), ('X', 'L2')]
    Wp_arcs = [('r', 'S'), ('r', 'L0'), ('S', 'U'), ('S', 'X0'),
               ('V', 'X0'), ('U', 'X1'), ('V', 'X1'), ('U', 'V'),
               ('X0', 'L1'), ('X1', 'L2')]
    leaves = ['L0', 'L1', 'L2']
    W_rootings, W_mixed = enumerate_rootings(W_arcs, {'V', 'X'}, leaves)
    Wp_rootings, Wp_mixed = enumerate_rootings(Wp_arcs, {'X0', 'X1'}, leaves)
    assert (len(W_rootings), sum(r['tree_child'] for r in W_rootings)) == (5, 2)
    assert (len(Wp_rootings), sum(r['tree_child'] for r in Wp_rootings)) == (7, 2)
    assert not mixed_isomorphic(W_mixed, Wp_mixed, leaves)
    assert not mixed_isomorphic(W_mixed, Wp_mixed, leaves, True)

    delta = F(1, 2**30)
    W_internal = {e: (F(1, 7), F(1, 7)) for e in W_arcs
                  if e not in [('r', 'L0'), ('Z', 'L1'), ('X', 'L2')]}
    Wp_internal = {e: (F(1, 4), F(1, 4)) for e in Wp_arcs
                   if e not in [('r', 'L0'), ('X0', 'L1'), ('X1', 'L2')]}
    W_pairs = dict(W_internal)
    W_pairs.update({
        ('r', 'L0'): (F(86779, 80) * delta,) * 2,
        ('Z', 'L1'): (F(320, 253) * delta,) * 2,
        ('X', 'L2'): (F(114373, 20240) * delta,) * 2,
    })
    Wp_pairs = dict(Wp_internal)
    Wp_pairs.update({
        ('r', 'L0'): (F(16, 3) * delta,) * 2,
        ('X0', 'L1'): (F(32, 9) * delta,) * 2,
        ('X1', 'L2'): (F(96, 5) * delta,) * 2,
    })
    W_weights = {
        'X': {'Z': F(15996, 16339), 'U': F(343, 16339)},
        'V': {'S': F(1, 8), 'U': F(7, 8)},
    }
    Wp_weights = {
        'X1': {'V': F(1, 2), 'U': F(1, 2)},
        'X0': {'V': F(1, 6), 'S': F(5, 6)},
    }
    coords = [(0, 0, 0), (0, 1, 1), (0, 2, 2), (1, 0, 1),
              (1, 1, 0), (1, 2, 3), (1, 3, 2), (2, 0, 2),
              (2, 1, 3), (2, 2, 0)]
    W_tensor = [fourier_q(W_arcs, W_weights, W_pairs, leaves, c) for c in coords]
    Wp_tensor = [fourier_q(Wp_arcs, Wp_weights, Wp_pairs, leaves, c) for c in coords]
    expected = [F(1)] + [delta * delta] * 4 + [F(4, 5) * delta**3] * 2 \
        + [delta * delta] + [F(4, 5) * delta**3] + [delta * delta]
    assert W_tensor == Wp_tensor == expected
    assert all(dct(pair) for pair in W_pairs.values())
    assert all(dct(pair) for pair in Wp_pairs.values())

    def jacobian_det(arcs, weights, internal_edges, base, named_edges,
                     row_order):
        syms = {}
        pairs = {}
        for i, edge in enumerate(internal_edges):
            ss, gg = sp.symbols(f's{i} g{i}')
            syms[edge] = (ss, gg)
            pairs[edge] = (ss, gg)
        for edge in arcs:
            if edge not in pairs:
                pairs[edge] = (sp.Integer(1), sp.Integer(1))
        outputs = [fourier_q(arcs, weights, pairs, leaves, c) for c in coords]
        columns = []
        for edge in named_edges[:4]:
            columns.extend(syms[edge])
        columns.append(syms[named_edges[4]][0])
        subs = {symbol: sp.Rational(base.numerator, base.denominator)
                for pair in syms.values() for symbol in pair}
        J = sp.Matrix([[sp.diff(outputs[row], col).subs(subs)
                        for col in columns] for row in row_order])
        return sp.factor(J.det())

    W_names = [('Z', 'X'), ('S', 'V'), ('r', 'S'), ('S', 'U'),
               ('U', 'V'), ('V', 'Z'), ('U', 'X')]
    Wp_names = [('V', 'X1'), ('V', 'X0'), ('U', 'V'), ('r', 'S'),
                ('S', 'X0'), ('S', 'U'), ('U', 'X1')]
    W_det = jacobian_det(W_arcs, W_weights, list(W_internal), F(1, 7),
                         W_names, (1, 2, 3, 5, 4, 7, 6, 8, 9))
    Wp_det = jacobian_det(Wp_arcs, Wp_weights, list(Wp_internal), F(1, 4),
                          Wp_names, (1, 2, 3, 5, 4, 6, 7, 8, 9))
    expected_W_det = sp.Rational(
        10368019213741323,
        563981315074464023964442388464888915634290688,
    )
    expected_Wp_det = sp.Rational(1435825, 85002596691653613846528)
    assert W_det == expected_W_det
    assert Wp_det == expected_Wp_det
    cherry = (F(2, 5), F(4, 9), F(3, 7), F(5, 11))
    us, ug, vs, vg = cherry
    cherry_det = 4 * us * ug / (vs * vg)
    assert cherry_det == F(2464, 675)
    return {
        "W_rootings": [len(W_rootings), sum(r['tree_child'] for r in W_rootings),
                        len(W_rootings) - sum(r['tree_child'] for r in W_rootings)],
        "Wp_rootings": [len(Wp_rootings), sum(r['tree_child'] for r in Wp_rootings),
                         len(Wp_rootings) - sum(r['tree_child'] for r in Wp_rootings)],
        "mixed_isomorphic": False,
        "triangle_forgotten_isomorphic": False,
        "common_tensor": [frac(x) for x in W_tensor],
        "W_jacobian_det": frac(W_det),
        "Wp_jacobian_det": frac(Wp_det),
        "cherry_det": frac(cherry_det),
    }


def symbolic_checks():
    delta, d, e, f = sp.symbols('delta d e f')
    lhs = f * (delta * d + (1 - delta) * e)**2 \
        - (delta * d + (1 - delta) * f * e) \
        * (delta * f * d + (1 - delta) * e)
    rhs = -delta * (1 - delta) * d * e * (1 - f)**2
    assert sp.expand(lhs - rhs) == 0
    printed_J0 = sp.Matrix([[1, 1, 0, 1], [1, 0, 1, sp.Rational(1, 4)],
                            [0, 1, 1, sp.Rational(1, 4)], [1, 1, 1, 1]])
    printed_Jp = sp.Matrix([
        [1, 1, 0, 0, 1],
        [1, 0, 1, sp.Rational(3, 4), sp.Rational(1, 4)],
        [0, 1, 1, sp.Rational(1, 4), sp.Rational(1, 4)],
        [-1, 1, 0, 0, 0],
        [-1, 0, 1, sp.Rational(1, 2), sp.Rational(-1, 2)],
    ])
    # Rebuild both logarithmic blocks directly from the printed sunlet map,
    # rather than merely taking the displayed matrices' determinants.
    edge_names = ('a', 'b', 'c', 'd', 'e', 'f')
    edge_vars = {}
    for name in edge_names:
        edge_vars[name + 's'], edge_vars[name + 'g'] = sp.symbols(
            name + 's ' + name + 'g'
        )

    def spectrum(name, char):
        if char == 0:
            return sp.Integer(1)
        return edge_vars[name + ('g' if char == 2 else 's')]

    def sunlet_q(x, y, z):
        return spectrum('a', x) * spectrum('b', y) * spectrum('c', z) * (
            delta * spectrum('f', y) * spectrum('d', z)
            + (1 - delta) * spectrum('f', x) * spectrum('e', z)
        )

    Xs, Xg = sunlet_q(1, 1, 0), sunlet_q(2, 2, 0)
    Ys, Yg = sunlet_q(1, 0, 1), sunlet_q(2, 0, 2)
    Zs, Zg = sunlet_q(0, 1, 1), sunlet_q(0, 2, 2)
    U, V, W = sunlet_q(1, 2, 3), sunlet_q(1, 3, 2), sunlet_q(2, 1, 3)
    base = {delta: sp.Rational(1, 2)}
    for name in edge_names:
        value = sp.Rational(1, 3) if name == 'f' else sp.Rational(1, 2)
        base[edge_vars[name + 's']] = value
        base[edge_vars[name + 'g']] = value

    def log_derivative(expr, variables):
        return sp.simplify(
            sum(variable * sp.diff(expr, variable) for variable in variables) / expr
        ).subs(base)

    J0 = sp.Matrix([
        [log_derivative(output,
                        (edge_vars[name + 's'], edge_vars[name + 'g']))
         for name in ('a', 'b', 'c', 'f')]
        for output in (Xs, Ys, Zs, W)
    ])
    Jp = sp.Matrix([
        [log_derivative(numerator, (edge_vars[name + 'g'],))
         - log_derivative(denominator, (edge_vars[name + 'g'],))
         for name in ('a', 'b', 'c', 'd', 'f')]
        for numerator, denominator in ((Xg, Xs), (Yg, Ys), (Zg, Zs),
                                       (U, W), (V, W))
    ])
    assert J0 == printed_J0
    assert Jp == printed_Jp
    assert J0.det() == sp.Rational(-1, 2)
    assert Jp.det() == sp.Rational(-1, 4)
    return {
        "tree_sunlet_identity_remainder": "0",
        "triangle_J0_det": frac(J0.det()),
        "triangle_Jperp_det": frac(Jp.det()),
        "triangle_combined_det": frac(J0.det() * Jp.det()),
    }


def domain_checks():
    points = [
        (F(1, 10**6), F(1, 10**6 + 1)),
        (F(999, 1000), F(998001, 10**6)),
        (F(999999, 10**6), F(999999, 10**6)),
        (F(1, 2), F(1, 10**9)),
    ]
    for pair in points:
        assert dplus(pair)
        assert all(p > 0 for p in inverse_probs(pair))
    S, G = points[1]
    r = F(9999999, 10**7)
    R = r * r
    factors = [(r, r), (r, r), (S / R, G / R)]
    assert all(dplus(pair) for pair in factors)
    assert factors[0][0] * factors[1][0] * factors[2][0] == S
    assert factors[0][1] * factors[1][1] * factors[2][1] == G
    ct_points = [(F(1, 7), F(1, 7)), (F(2, 5), F(4, 9)),
                 (F(3, 7), F(5, 11))]
    assert all(dct(p) and dplus(p) for p in ct_points)
    return {
        "boundary_near_points": [[frac(x) for x in p] for p in points],
        "serial_target": [frac(S), frac(G)],
        "serial_factors": [[frac(x) for x in p] for p in factors],
        "continuous_time_points": [[frac(x) for x in p] for p in ct_points],
    }


def combinatorial_checks():
    counts = {
        "C(4,1)": completion_count(4, 1),
        "C(4,0)": completion_count(4, 0),
        "C(5,1)": completion_count(5, 1),
        "C(5,0)": completion_count(5, 0),
    }
    assert counts == {"C(4,1)": 831, "C(4,0)": 1983,
                      "C(5,1)": 1983, "C(5,0)": 4155}
    raw = {
        "raw4": 6 * (counts["C(4,1)"] + counts["C(4,0)"]) * math.factorial(4),
        "theta2": 4 * (counts["C(5,1)"] + counts["C(5,0)"]) * math.factorial(5),
        "cycle": 2 * 1120 * math.factorial(3),
    }
    assert raw == {"raw4": 405216, "theta2": 2946240, "cycle": 13440}
    clauses = {
        "cycle": ([0, 1], [{0, 1}]),
        "theta0": (list(range(5)), [{3}, {2, 4}]),
        "theta1": (list(range(5)), [{2}, {3, 4}]),
        "theta2": (list(range(6)), [{2, 4}, {3, 5}]),
        "theta3": (list(range(6)), [{2, 4}]),
    }
    transversals = {name: [list(x) for x in minimal_transversals(*datum)]
                    for name, datum in clauses.items()}
    expected = {
        "cycle": [[0], [1]],
        "theta0": [[2, 3], [3, 4]],
        "theta1": [[2, 3], [2, 4]],
        "theta2": [[2, 3], [2, 5], [3, 4], [4, 5]],
        "theta3": [[2], [4]],
    }
    assert transversals == expected
    partitions = {
        "raw4": sum((360408, 16974, 23822, 1472, 2540)),
        "theta2": sum((2942592, 2528, 800, 240, 80)),
        "cycle_base": sum((7452, 5964, 8, 16)),
        "cycle_completion": sum((535920, 300, 132, 12)),
        "restoration_first": sum((35758, 606, 148, 24, 32)),
        "restoration_second": sum((248, 8)),
        "probe_one": sum((27758, 99, 1915, 192)),
        "probe_two": sum((511266, 576, 30969, 1760)),
    }
    assert partitions == {
        "raw4": 405216, "theta2": 2946240, "cycle_base": 13440,
        "cycle_completion": 536364, "restoration_first": 36568,
        "restoration_second": 256, "probe_one": 29964,
        "probe_two": 544571,
    }
    return {"completion_counts": counts, "raw_counts": raw,
            "minimal_repairs": transversals, "partition_sums": partitions}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = {
        "schema": "k2p-r6-independent-exact-math-checks-v1",
        "status": "PASS",
        "imports_submission_code": False,
        "checks": {
            "domain": domain_checks(),
            "symbolic": symbolic_checks(),
            "combinatorics": combinatorial_checks(),
            "weak_sharpness": graph_and_tensor_checks(),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({"status": "PASS", "output": str(args.output)}, sort_keys=True))


if __name__ == '__main__':
    main()
