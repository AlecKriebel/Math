#!/usr/bin/env python3
"""Independent exact spot checks for the 2026-08-27 mathematical review.

This script is review-owned.  It does not import the submitted classifier,
canonicalizer, graph builders, certificate readers, or expected ledgers.
"""

from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb

import sympy as sp


GROUP = {"0": 0, "C": 1, "G": 2, "T": 3}


def mixed_graph_from_rooted(arcs, reticulations, root="r"):
    children = [v for u, v in arcs if u == root]
    assert len(children) == 2
    edges = []
    for u, v in arcs:
        if u == root:
            continue
        heads = frozenset({v}) if v in reticulations else frozenset()
        edges.append((frozenset({u, v}), heads))
    merged_heads = frozenset(x for x in children if x in reticulations)
    assert len(set(children)) == 2 and len(merged_heads) < 2
    edges.append((frozenset(children), merged_heads))
    return edges


def all_directed_paths(children, source, target, prefix=()):
    if source == target:
        return [prefix + (source,)]
    answer = []
    for child in children.get(source, ()):
        if child not in prefix:
            answer.extend(all_directed_paths(children, child, target, prefix + (source,)))
    return answer


def rooting_census(mixed_edges, reticulations, leaves):
    vertices = set().union(*(ends for ends, _ in mixed_edges))
    root = "ROOT"
    admissible = []
    for root_index, (root_ends, root_heads) in enumerate(mixed_edges):
        u, v = sorted(root_ends)
        fixed = []
        ordinary = []
        # The inserted root points to both endpoints; a retained head remains.
        fixed.extend([(root, u), (root, v)])
        for index, (ends, heads) in enumerate(mixed_edges):
            if index == root_index:
                continue
            x, y = sorted(ends)
            if heads:
                head = next(iter(heads))
                tail = y if head == x else x
                fixed.append((tail, head))
            else:
                ordinary.append((x, y))
        for bits in product((0, 1), repeat=len(ordinary)):
            arcs = list(fixed)
            for bit, (x, y) in zip(bits, ordinary):
                arcs.append((x, y) if bit == 0 else (y, x))
            indeg = {x: 0 for x in vertices | {root}}
            outdeg = {x: 0 for x in vertices | {root}}
            children = {x: [] for x in vertices | {root}}
            for x, y in arcs:
                indeg[y] += 1
                outdeg[x] += 1
                children[x].append(y)
            if (indeg[root], outdeg[root]) != (0, 2):
                continue
            if any((indeg[x], outdeg[x]) != (2, 1) for x in reticulations):
                continue
            if any((indeg[x], outdeg[x]) != (1, 0) for x in leaves):
                continue
            tree_vertices = vertices - set(reticulations) - set(leaves)
            if any((indeg[x], outdeg[x]) != (1, 2) for x in tree_vertices):
                continue
            # Reachability and acyclicity.
            reached = set()
            frontier = [root]
            while frontier:
                x = frontier.pop()
                if x in reached:
                    continue
                reached.add(x)
                frontier.extend(children[x])
            if reached != vertices | {root}:
                continue
            # Every root-to-leaf path must exist, and only root is stable for
            # all labelled leaves (the lowest-stable-ancestor convention).
            path_sets = []
            acyclic = True
            for leaf in leaves:
                paths = all_directed_paths(children, root, leaf)
                if not paths:
                    acyclic = False
                    break
                path_sets.extend(map(set, paths))
            if not acyclic:
                continue
            stable = set.intersection(*path_sets)
            if stable != {root}:
                continue
            tree_child = all(
                any(child not in reticulations for child in children[x])
                for x in (vertices | {root}) - set(leaves)
            )
            admissible.append((root_index, tuple(sorted(arcs)), tree_child))
    return len(admissible), sum(x[2] for x in admissible), sum(not x[2] for x in admissible)


def mixed_signature(edges, mapping, ignored_edges=frozenset()):
    rows = []
    for ends, heads in edges:
        mapped_ends = frozenset(mapping[x] for x in ends)
        if ends in ignored_edges:
            mapped_heads = frozenset()
        else:
            mapped_heads = frozenset(mapping[x] for x in heads)
        rows.append((tuple(sorted(mapped_ends)), tuple(sorted(mapped_heads))))
    return tuple(sorted(rows))


def triangles(edges):
    vertices = sorted(set().union(*(ends for ends, _ in edges)))
    edge_sets = {ends for ends, _ in edges}
    return [frozenset(frozenset(pair) for pair in combinations(tri, 2))
            for tri in combinations(vertices, 3)
            if all(frozenset(pair) in edge_sets for pair in combinations(tri, 2))]


def graph_relation_check():
    arcs_w = [("r", "S"), ("r", "L0"), ("S", "U"), ("S", "V"),
              ("U", "X"), ("V", "Z"), ("Z", "X"), ("U", "V"),
              ("Z", "L1"), ("X", "L2")]
    arcs_wp = [("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"),
               ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V"),
               ("X0", "L1"), ("X1", "L2")]
    w = mixed_graph_from_rooted(arcs_w, {"V", "X"})
    wp = mixed_graph_from_rooted(arcs_wp, {"X0", "X1"})
    census = (rooting_census(w, {"V", "X"}, {"L0", "L1", "L2"}),
              rooting_census(wp, {"X0", "X1"}, {"L0", "L1", "L2"}))
    assert census == ((5, 2, 3), (7, 2, 5)), census

    internal_w = sorted(set().union(*(ends for ends, _ in w)) - {"L0", "L1", "L2"})
    internal_wp = sorted(set().union(*(ends for ends, _ in wp)) - {"L0", "L1", "L2"})
    identity_leaves = {f"L{i}": f"L{i}" for i in range(3)}
    target = mixed_signature(wp, {x: x for x in set(internal_wp) | set(identity_leaves)})
    isomorphisms = 0
    triangle_isomorphisms = 0
    tri_w, tri_wp = triangles(w), triangles(wp)
    assert len(tri_w) == len(tri_wp) == 1
    ignored_w, ignored_wp = tri_w[0], tri_wp[0]
    target_triangle = mixed_signature(
        wp, {x: x for x in set(internal_wp) | set(identity_leaves)}, ignored_wp
    )
    for image_order in permutations(internal_wp):
        mapping = dict(zip(internal_w, image_order))
        mapping.update(identity_leaves)
        isomorphisms += mixed_signature(w, mapping) == target
        triangle_isomorphisms += mixed_signature(w, mapping, ignored_w) == target_triangle
    assert isomorphisms == triangle_isomorphisms == 0
    return census, len(tri_w), isomorphisms, triangle_isomorphisms


def completion_count(k, incoming_selected):
    # (directed segments, path sinks, target repair tags)
    cores = [(2, 1, 1), (5, 1, 2), (5, 1, 2), (6, 2, 4), (6, 2, 2)]
    eps = int(incoming_selected)
    return sum(
        repairs
        * sum(
            comb(sinks, j) * comb(k - eps - j + segments - 1, segments - 1)
            for j in range(sinks + 1)
        )
        for segments, sinks, repairs in cores
    )


def spectrum(edge_parameters, edge, character):
    if character == 0:
        return sp.Integer(1)
    s, g = edge_parameters[edge]
    return g if character == 2 else s


def descendants(vertices, active_arcs, leaves):
    children = {v: [] for v in vertices}
    for u, v in active_arcs:
        children[u].append(v)

    memo = {}

    def visit(v):
        if v in memo:
            return memo[v]
        if v in leaves:
            ans = {leaves[v]}
        else:
            ans = set()
            for child in children[v]:
                ans.update(visit(child))
        memo[v] = ans
        return ans

    return {arc: visit(arc[1]) for arc in active_arcs}


def network_fourier(arcs, leaves, retic_choices, edge_parameters, assignment):
    """Direct displayed-tree expansion for a rooted two-reticulation graph."""
    vertices = set(sum(([u, v] for u, v in arcs), []))
    answer = sp.Integer(0)
    for selections in product(*[choices for _, choices in retic_choices]):
        selected = set(selections)
        all_retic_arcs = {arc for _, choices in retic_choices for arc, _ in choices}
        active = [arc for arc in arcs if arc not in all_retic_arcs or arc in {x[0] for x in selections}]
        weight = sp.Integer(1)
        for arc, probability in selections:
            weight *= probability
        below = descendants(vertices, active, leaves)
        term = weight
        for arc in active:
            h = 0
            for label in below[arc]:
                h ^= assignment[label]
            term *= spectrum(edge_parameters, arc, h)
        answer += term
    return sp.expand(answer)


def weak_network_check():
    delta = F(1, 2**30)
    orbit_words = ["000", "0CC", "0GG", "C0C", "CC0", "CGT", "CTG", "G0G", "GCT", "GG0"]

    cases = []
    # The probability on the first listed incoming arc is lambda; its other
    # parent has probability 1-lambda.  These are literal rooted encodings.
    arcs_w = [("r", "S"), ("r", "L0"), ("S", "U"), ("S", "V"),
              ("U", "X"), ("V", "Z"), ("Z", "X"), ("U", "V"),
              ("Z", "L1"), ("X", "L2")]
    internal_w = [("r", "S"), ("S", "U"), ("S", "V"), ("U", "X"),
                  ("V", "Z"), ("Z", "X"), ("U", "V")]
    pendant_w = {("r", "L0"): F(86779, 80) * delta,
                 ("Z", "L1"): F(320, 253) * delta,
                 ("X", "L2"): F(114373, 20240) * delta}
    order_w = [("Z", "X"), ("S", "V"), ("r", "S"), ("S", "U"),
               ("U", "V"), ("V", "Z"), ("U", "X")]
    rows_w = [1, 2, 3, 5, 4, 7, 6, 8, 9]
    cases.append((
        "W", arcs_w, internal_w, pendant_w,
        [("X", [(("Z", "X"), sp.Rational(15996, 16339)),
                 (("U", "X"), sp.Rational(343, 16339))]),
         ("V", [(("S", "V"), sp.Rational(1, 8)),
                 (("U", "V"), sp.Rational(7, 8))])],
        sp.Rational(1, 7), order_w, rows_w,
        sp.Rational(10368019213741323, 563981315074464023964442388464888915634290688),
    ))

    arcs_wp = [("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"),
               ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V"),
               ("X0", "L1"), ("X1", "L2")]
    internal_wp = [("r", "S"), ("S", "U"), ("S", "X0"), ("V", "X0"),
                   ("U", "X1"), ("V", "X1"), ("U", "V")]
    pendant_wp = {("r", "L0"): F(16, 3) * delta,
                  ("X0", "L1"): F(32, 9) * delta,
                  ("X1", "L2"): F(96, 5) * delta}
    order_wp = [("V", "X1"), ("V", "X0"), ("U", "V"), ("r", "S"),
                ("S", "X0"), ("S", "U"), ("U", "X1")]
    rows_wp = [1, 2, 3, 5, 4, 6, 7, 8, 9]
    cases.append((
        "Wprime", arcs_wp, internal_wp, pendant_wp,
        [("X0", [(("V", "X0"), sp.Rational(1, 6)),
                  (("S", "X0"), sp.Rational(5, 6))]),
         ("X1", [(("V", "X1"), sp.Rational(1, 2)),
                  (("U", "X1"), sp.Rational(1, 2))])],
        sp.Rational(1, 4), order_wp, rows_wp,
        sp.Rational(1435825, 85002596691653613846528),
    ))

    tensors = {}
    determinants = {}
    for name, arcs, internal, pendant, choices, internal_value, edge_order, rows, expected_det in cases:
        edge_parameters = {}
        symbols = {}
        for index, edge in enumerate(internal):
            symbols[edge] = (sp.Symbol(f"s{index}"), sp.Symbol(f"g{index}"))
            edge_parameters[edge] = symbols[edge]
        for edge, value in pendant.items():
            edge_parameters[edge] = (sp.Rational(value.numerator, value.denominator),) * 2

        outputs = []
        normalized_parameters = dict(edge_parameters)
        for edge in pendant:
            normalized_parameters[edge] = (sp.Integer(1), sp.Integer(1))
        normalized_outputs = []
        for word in orbit_words:
            assignment = {i: GROUP[word[i]] for i in range(3)}
            outputs.append(network_fourier(arcs, {"L0": 0, "L1": 1, "L2": 2}, choices,
                                           edge_parameters, assignment))
            normalized_outputs.append(
                network_fourier(arcs, {"L0": 0, "L1": 1, "L2": 2}, choices,
                                normalized_parameters, assignment)
            )
        substitutions = {symbol: internal_value for pair in symbols.values() for symbol in pair}
        tensor = [sp.factor(q.subs(substitutions)) for q in outputs]
        tensors[name] = tensor

        columns = []
        for edge in edge_order:
            columns.extend(symbols[edge])
        columns = columns[:9]
        jac = sp.Matrix(normalized_outputs).jacobian(columns)
        det = sp.factor(jac.extract(rows, range(9)).subs(substitutions).det())
        determinants[name] = det
        assert det == expected_det, (name, det, expected_det)

    expected_tensor = [sp.Integer(1)] + [sp.Rational(delta.numerator, delta.denominator) ** 2] * 4
    # The orbit order has six pair rows (1,2,3,4,7,9) and three triple rows.
    d = sp.Rational(delta.numerator, delta.denominator)
    expected_tensor = [sp.Integer(1)] + [None] * 9
    for i in [1, 2, 3, 4, 7, 9]:
        expected_tensor[i] = d**2
    for i in [5, 6, 8]:
        expected_tensor[i] = sp.Rational(4, 5) * d**3
    assert tensors["W"] == expected_tensor
    assert tensors["Wprime"] == expected_tensor
    return determinants


def triangle_check():
    # Exact common tensor and the two printed logarithmic Jacobian blocks.
    half = sp.Rational(1, 2)
    third = sp.Rational(1, 3)
    delta = half

    def q(x, y, z):
        def ev(h, value):
            return sp.Integer(1) if h == 0 else value
        return (
            ev(x, half) * ev(y, half) * ev(z, half)
            * (delta * ev(y, third) * ev(z, half)
               + (1 - delta) * ev(x, third) * ev(z, half))
        )

    supported = []
    for x in range(4):
        for y in range(4):
            z = x ^ y
            supported.append(q(x, y, z))
    nonzero_pair = [q(1, 1, 0), q(2, 2, 0), q(1, 0, 1), q(2, 0, 2), q(0, 1, 1), q(0, 2, 2)]
    triple = [q(1, 2, 3), q(1, 3, 2), q(2, 1, 3)]
    assert set(nonzero_pair) == {sp.Rational(1, 12)}
    assert set(triple) == {sp.Rational(1, 48)}

    j0 = sp.Matrix([[1, 1, 0, 1], [1, 0, 1, sp.Rational(1, 4)],
                    [0, 1, 1, sp.Rational(1, 4)], [1, 1, 1, 1]])
    jp = sp.Matrix([[1, 1, 0, 0, 1], [1, 0, 1, sp.Rational(3, 4), sp.Rational(1, 4)],
                    [0, 1, 1, sp.Rational(1, 4), sp.Rational(1, 4)], [-1, 1, 0, 0, 0],
                    [-1, 0, 1, sp.Rational(1, 2), sp.Rational(-1, 2)]])
    assert j0.det() == sp.Rational(-1, 2)
    assert jp.det() == sp.Rational(-1, 4)
    return j0.det(), jp.det(), len(supported)


def sunlet_identity_check():
    a_s, a_g, b_s, b_g, c_g, f_s, f_g, d_g, e_g, delta = sp.symbols(
        "a_s a_g b_s b_g c_g f_s f_g d_g e_g delta"
    )
    # Coordinates obtained directly from the displayed map in article (4.4).
    x_s = a_s * b_s * f_s
    x_g = a_g * b_g * f_g
    y_g = a_g * c_g * (delta * d_g + (1 - delta) * f_g * e_g)
    z_g = b_g * c_g * (delta * f_g * d_g + (1 - delta) * e_g)
    v = a_s * b_s * c_g * f_s * (delta * d_g + (1 - delta) * e_g)
    lhs = sp.factor(v**2 * x_g - x_s**2 * y_g * z_g)
    rhs = -a_s**2 * b_s**2 * a_g * b_g * c_g**2 * f_s**2 * delta * (1-delta) * d_g * e_g * (1-f_g)**2
    assert sp.factor(lhs - rhs) == 0
    return sp.factor(lhs)


def cherry_inverse_check():
    """Rebuild the four-observable cherry chart and its positive inverse."""

    us, vs, ug, vg = sp.symbols("u_s v_s u_g v_g", positive=True)
    observables = sp.Matrix([us / vs, us * vs, ug / vg, ug * vg])
    variables = sp.Matrix([us, vs, ug, vg])
    determinant = sp.factor(observables.jacobian(variables).det())
    assert determinant == 4 * us * ug / (vs * vg)

    point = {us: sp.Rational(2, 5), ug: sp.Rational(4, 9),
             vs: sp.Rational(3, 7), vg: sp.Rational(5, 11)}
    assert 0 < point[us] < 1 and point[us] ** 2 < point[ug] < 1
    assert 0 < point[vs] < 1 and point[vs] ** 2 < point[vg] < 1
    observed = [sp.factor(value.subs(point)) for value in observables]
    assert observed == [sp.Rational(14, 15), sp.Rational(6, 35),
                        sp.Rational(44, 45), sp.Rational(20, 99)]
    assert determinant.subs(point) == sp.Rational(2464, 675)

    rs, ps, rg, pg = sp.symbols("R_s P_s R_g P_g", positive=True)
    recovered = [sp.sqrt(rs * ps), sp.sqrt(ps / rs),
                 sp.sqrt(rg * pg), sp.sqrt(pg / rg)]
    forward_recovered = [
        sp.factor(recovered[0] / recovered[1]),
        sp.factor(recovered[0] * recovered[1]),
        sp.factor(recovered[2] / recovered[3]),
        sp.factor(recovered[2] * recovered[3]),
    ]
    assert forward_recovered == [rs, ps, rg, pg]
    recovered_at_point = [
        sp.factor(value.subs(dict(zip((rs, ps, rg, pg), observed))))
        for value in recovered
    ]
    assert recovered_at_point == [point[us], point[vs], point[ug], point[vg]]
    return determinant, determinant.subs(point), tuple(observed), tuple(recovered_at_point)


def main():
    counts = {(k, eps): completion_count(k, eps) for k, eps in [(4, True), (4, False), (5, True), (5, False)]}
    assert counts == {(4, True): 831, (4, False): 1983, (5, True): 1983, (5, False): 4155}
    assert 6 * (counts[(4, True)] + counts[(4, False)]) * 24 == 405216
    assert 4 * (counts[(5, True)] + counts[(5, False)]) * 120 == 2946240
    print("completion_counts", counts)
    print("triangle", triangle_check())
    print("sunlet_identity", sunlet_identity_check())
    print("weak_graphs", graph_relation_check())
    print("weak_determinants", weak_network_check())
    print("cherry_inverse", cherry_inverse_check())
    print("PASS")


if __name__ == "__main__":
    main()
