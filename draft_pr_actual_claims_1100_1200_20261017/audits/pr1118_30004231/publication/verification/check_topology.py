"""Independent exact verifier for PR1118; standard library only.

Enumerates exposed supports from coordinate height patterns, deduplicates by
actual sum-point sets, reconstructs all inclusions, builds every order-complex
chain and its signed rational boundary, and runs adverse controls. No candidate
checker or historical audit was used. Run with Python normally and with -O.
Validation uses explicit exceptions, never removable assertions.
"""
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, product, permutations
import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(matrix):
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    ncols, row = len(a[0]), 0
    for col in range(ncols):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        v = a[row][col]
        a[row] = [x / v for x in a[row]]
        for i in range(row + 1, len(a)):
            if a[i][col]:
                v = a[i][col]
                a[i] = [x - v * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def affine_dimension(points):
    points = sorted(points)
    if not points:
        return -1
    return rank([[x - y for x, y in zip(p, points[0])] for p in points[1:]])


def simplex(m):
    return [tuple(0 for _ in range(m))] + [
        tuple(int(i == j) for j in range(m)) for i in range(m)]


def enumerate_faces(m, prism):
    v = simplex(m)
    faces = {}
    # Every disjoint nonempty maximum/minimum pair has a representative using
    # just three heights; all equal heights also include the whole base face.
    for heights in product((-1, 0, 1), repeat=m + 1):
        a = frozenset(i for i, x in enumerate(heights) if x == max(heights))
        b = frozenset(i for i, x in enumerate(heights) if x == min(heights))
        for t in ((-1, 0, 1) if prism else (None,)):
            interval = (0,) if t == -1 else ((1,) if t == 1 else (0, 1))
            if prism:
                p = {v[i] + (z,) for i in a for z in interval}
                q = {tuple(-x for x in v[j]) + (z,) for j in b for z in interval}
            else:
                p = {v[i] for i in a}
                q = {tuple(-x for x in v[j]) for j in b}
            sums = frozenset(tuple(x + y for x, y in zip(p1, p2))
                             for p1 in p for p2 in q)
            dims = (affine_dimension(p), affine_dimension(q), affine_dimension(sums))
            item = {"A": a, "B": b, "t": t, "points": sums, "dims": dims,
                    "eligible": dims[0] > 0 and dims[1] > 0
                                and dims[2] == dims[0] + dims[1]}
            if sums in faces:
                old = faces[sums]
                require((old["A"], old["B"], old["t"], old["dims"])
                        == (a, b, t, dims), "inconsistent canonical indexing")
            else:
                faces[sums] = item
    selected = sorted((r for r in faces.values() if r["eligible"]),
                      key=lambda r: (r["dims"][2], tuple(sorted(r["points"]))))
    # This comparison independently checks every pair, including all negatives.
    less = set()
    for i, x in enumerate(selected):
        for j, y in enumerate(selected):
            geometric = x["points"] < y["points"]
            predicted = (i != j and x["A"] <= y["A"] and x["B"] <= y["B"]
                         and x["t"] == y["t"])
            require(geometric == predicted, "geometric/index inclusion disagreement")
            if geometric:
                less.add((i, j))
    return faces, selected, less


def order_complex(n, less):
    levels = [[(i,) for i in range(n)]]
    while levels[-1]:
        nxt = sorted(c + (j,) for c in levels[-1] for j in range(n)
                     if (c[-1], j) in less)
        if not nxt:
            break
        levels.append(nxt)
    return levels


def boundary_matrices(levels):
    matrices = [[[1 for _ in levels[0]]]]  # augmentation C0 -> Q
    for k in range(1, len(levels)):
        row_index = {c: i for i, c in enumerate(levels[k - 1])}
        a = [[0 for _ in levels[k]] for _ in levels[k - 1]]
        for j, c in enumerate(levels[k]):
            for i in range(k + 1):
                a[row_index[c[:i] + c[i + 1:]]][j] = (-1) ** i
        matrices.append(a)
    for k in range(1, len(matrices)):
        a, b = matrices[k - 1], matrices[k]
        for i in range(len(a)):
            for j in range(len(b[0]) if b else 0):
                require(sum(a[i][r] * b[r][j] for r in range(len(b))) == 0,
                        "boundary squared is nonzero")
    return matrices


def topology(n, less):
    levels = order_complex(n, less)
    mats = boundary_matrices(levels)
    ranks = [rank(a) for a in mats]
    ordinary = [n - (ranks[1] if len(ranks) > 1 else 0)]
    for k in range(1, len(levels)):
        ordinary.append(len(levels[k]) - ranks[k]
                        - (ranks[k + 1] if k + 1 < len(ranks) else 0))
    graph = [set() for _ in range(n)]
    for i, j in less:
        graph[i].add(j)
        graph[j].add(i)
    components, remaining = [], set(range(n))
    while remaining:
        reached, todo = set(), [min(remaining)]
        while todo:
            i = todo.pop()
            if i not in reached:
                reached.add(i)
                todo.extend(graph[i] - reached)
        remaining -= reached
        components.append(reached)
    require(ordinary[0] == len(components), "rank/connectivity disagreement")
    facets = [c for level in levels for c in level if not any(
        set(c) < set(d) for upper in levels[len(c):] for d in upper)]
    result = {"f_vector": [len(c) for c in levels],
              "boundary_ranks_from_augmentation": ranks,
              "ordinary_betti": ordinary, "reduced_beta_0": ordinary[0] - 1,
              "component_vertices": sorted(map(len, components)),
              "facet_dimensions": dict(sorted(Counter(len(c) - 1 for c in facets).items())),
              "boundary_squared_zero": True}
    return result, levels, components


def shelling_valid(facets):
    previous = set()
    for k, f in enumerate(facets):
        all_faces = {frozenset(c) for r in range(len(f) + 1)
                     for c in combinations(f, r)}
        intersection = previous & all_faces
        if k:
            maximal = [a for a in intersection if not any(a < b for b in intersection)]
            if not maximal or any(len(a) != len(f) - 1 for a in maximal):
                return False
        previous |= all_faces
    return True


def graph_shelling(edges):
    todo, order, used = set(edges), [], set()
    while todo:
        edge = next((e for e in sorted(todo) if not used or set(e) & used), None)
        if edge is None:
            return None
        todo.remove(edge)
        order.append(edge)
        used.update(edge)
    require(shelling_valid(order), "constructed graph shelling is invalid")
    return order


summary = {}
cases = {}
for name, m, prism in [("R4_base", 4, False), ("R5_prism", 4, True),
                        ("R3_tetrahedron", 3, False)]:
    faces, selected, less = enumerate_faces(m, prism)
    topo, levels, components = topology(len(selected), less)
    topo.update({"all_nonempty_exposed_faces": len(faces),
                 "eligible_faces": len(selected), "comparisons": len(less),
                 "eligible_dimension_counts": dict(sorted(Counter(
                     r["dims"][2] for r in selected).items())),
                 "all_inclusions_checked": len(selected) ** 2,
                 "full_sum_eligible": any(r["eligible"] for r in faces.values()
                                          if r["dims"][2] == m + int(prism)),
                 "eligible_interval_types": dict(sorted(Counter(
                     str(r["t"]) for r in selected).items()))})
    if len(levels) == 2:
        edges = levels[1]
        topo["component_edge_counts"] = sorted(sum(i in c and j in c for i, j in edges)
                                                 for c in components)
        topo["vertex_degree_counts"] = dict(sorted(Counter(
            sum(i in e for e in edges) for i in range(len(selected))).items()))
        topo["component_shellings_verified"] = all(graph_shelling(
            [e for e in edges if e[0] in c]) is not None for c in components)
        topo["entire_graph_shelling_constructible"] = graph_shelling(edges) is not None
    cases[name] = (selected, less, levels)
    summary[name] = topo

require(summary["R4_base"]["f_vector"] == [50, 60], "wrong base f-vector")
require(summary["R4_base"]["ordinary_betti"] == [1, 11], "wrong base homology")
require(summary["R5_prism"]["f_vector"] == [100, 120], "wrong prism f-vector")
require(summary["R5_prism"]["ordinary_betti"] == [2, 22], "wrong prism homology")
require(summary["R5_prism"]["component_vertices"] == [50, 50], "wrong components")
require(summary["R5_prism"]["component_edge_counts"] == [60, 60], "wrong component edges")
require(summary["R5_prism"]["boundary_ranks_from_augmentation"] == [1, 98], "wrong rank")
require(summary["R3_tetrahedron"]["f_vector"] == [6], "wrong small control")
require(summary["R3_tetrahedron"]["ordinary_betti"] == [6], "wrong small homology")
require(shelling_valid([(i,) for i in range(6)]), "discrete 0-complex shelling failed")

# Adversarial controls: a wrong empty-intersection convention, boundary signs,
# and appending a maximum must produce detected differences.
two_edges = [(0, 1), (2, 3)]
require(not any(shelling_valid(p) for p in permutations(two_edges)),
        "disconnected two-edge complex incorrectly accepted")
require(shelling_valid([(0, 1), (1, 2), (0, 2)]), "triangle graph should shell")
selected, less, levels = cases["R5_prism"]
cone_less = less | {(i, len(selected)) for i in range(len(selected))}
cone, cone_levels, _ = topology(len(selected) + 1, cone_less)
require(cone["f_vector"] == [101, 220, 120], "wrong cone control f-vector")
require(cone["ordinary_betti"] == [1, 0, 0], "cone must be contractible")
# A full 2-simplex tests nonvacuous d1*d2=0, and detects a sign mutation.
triangle_levels = [[(0,), (1,), (2,)], [(0, 1), (0, 2), (1, 2)], [(0, 1, 2)]]
triangle_mats = boundary_matrices(triangle_levels)
mutated_column = [1, 1, 1]
require(any(sum(triangle_mats[1][i][j] * mutated_column[j] for j in range(3))
            for i in range(3)), "boundary-sign mutation not detected")
summary["controls"] = {"six_points_shellable": True,
    "two_disjoint_edges_rejected_all_orders": True,
    "triangle_graph_shellable": True,
    "filled_triangle_boundary_squared_zero": True,
    "unsigned_triangle_boundary_mutation_detected": True,
    "artificial_maximum_cone": cone,
    "normal_and_optimized_safe_explicit_exceptions": True}
serialized = json.dumps(summary, sort_keys=True, separators=(",", ":"))
print(json.dumps({"result": "PASS", "data": summary,
    "semantic_sha256": hashlib.sha256(serialized.encode()).hexdigest()}, indent=2, sort_keys=True))
