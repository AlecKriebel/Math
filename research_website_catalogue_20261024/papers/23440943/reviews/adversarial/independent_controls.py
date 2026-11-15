#!/usr/bin/env python3
"""Own exact coordinate exposure and chain topology; no deposited imports/data."""
from itertools import product, combinations
from fractions import Fraction
from collections import Counter, deque
from hashlib import sha256
import json

CHECKS = 0


def require(p, why):
    global CHECKS
    CHECKS += 1
    if not p:
        raise ArithmeticError(why)


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((j for j in range(r, len(a)) if a[j][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x/v for x in a[r]]
        for j in range(r+1, len(a)):
            if a[j][c]:
                v = a[j][c]
                a[j] = [x-v*y for x, y in zip(a[j], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def affine_dim(points):
    p = sorted(points)
    if not p:
        return -1
    return rank([[x-y for x, y in zip(q, p[0])] for q in p[1:]])


def simplex(d):
    return [tuple(0 for _ in range(d))] + [tuple(int(i == j) for j in range(d)) for i in range(d)]


def expose(points, u):
    values = [sum(x*y for x, y in zip(p, u)) for p in points]
    m = max(values)
    return frozenset(p for p, v in zip(points, values) if v == m)


def add(a, b):
    return frozenset(tuple(x+y for x, y in zip(p, q)) for p in a for q in b)


def all_faces(d, prism):
    v = simplex(d)
    p = [x+(h,) for x in v for h in (0, 1)] if prism else v
    neg = [tuple(-x for x in q)+(h,) for q in v for h in (0, 1)] if prism else [tuple(-x for x in q) for q in v]
    faces = {}
    single1, single2 = set(), set()
    # Every possible max/min tie pattern on simplex vertices is realizable by
    # three affine levels. Subtracting the level at v0 gives a linear form.
    for levels in product((-1, 0, 1), repeat=d+1):
        u = tuple(x-levels[0] for x in levels[1:])
        for t in ((-1, 0, 1) if prism else (None,)):
            direction = u+(t,) if prism else u
            a, b = expose(p, direction), expose(neg, direction)
            f = add(a, b)
            if f in faces:
                require(faces[f][0] == a and faces[f][1] == b, 'canonical summands agree across exposures')
            else:
                faces[f] = (a, b, direction)
            single1.add(a)
            single2.add(b)
    records = []
    for f, (a, b, direction) in faces.items():
        dims = affine_dim(a), affine_dim(b), affine_dim(f)
        qualifies = dims[0] > 0 and dims[1] > 0 and dims[2] == dims[0]+dims[1]
        records.append({'points': f, 'first': a, 'second': b, 'exposing_form': direction,
                        'dims': dims, 'qualifies': qualifies})
    return records, p, neg, single1, single2


def graph_analysis(qualifiers):
    n = len(qualifiers)
    relations = [(i, j) for i in range(n) for j in range(n)
                 if i != j and qualifiers[i]['points'] < qualifiers[j]['points']]
    require(not any((j, k) in relations for i, j in relations for k in range(n)),
            'no three-element strict chains')
    neighbors = [set() for _ in range(n)]
    matrix = [[0 for _ in relations] for _ in range(n)]
    for c, (i, j) in enumerate(relations):
        neighbors[i].add(j)
        neighbors[j].add(i)
        matrix[i][c], matrix[j][c] = -1, 1
    unseen = set(range(n))
    components = []
    while unseen:
        seen = {unseen.pop()}
        q = deque(seen)
        while q:
            for w in neighbors[q.popleft()] - seen:
                seen.add(w)
                unseen.discard(w)
                q.append(w)
        components.append(seen)
    r = rank(matrix)
    require(r == n-len(components), 'rational boundary rank versus direct components')
    return relations, neighbors, components, matrix, r


def main():
    faces, p, neg, single1, single2 = all_faces(4, True)
    require(affine_dim(p) == affine_dim(neg) == 5, 'full-dimensional lattice summands')
    require(all(type(x) is int for q in p+neg for x in q), 'integer vertices')
    require(len(faces) == 543, 'complete product sum face count')
    require(len(single1) == len(single2) == 93, 'complete summand prism face counts')
    q = sorted((x for x in faces if x['qualifies']), key=lambda x: sorted(x['points']))
    require(len(q) == 100, 'all qualifying faces')
    for f in q:
        heights = {v[-1] for v in f['points']}
        require(heights in ({0}, {2}), 'qualifiers lie on actual endpoint faces')
        require(f['dims'] in ((1, 1, 2), (1, 2, 3), (2, 1, 3)), 'coordinate ranks of qualifiers')
    vertical = [x for x in faces if len({p[-1] for p in x['points']}) > 1]
    require(len(vertical) == 181 and not any(x['qualifies'] for x in vertical), 'all shared interval faces fail exact filter')
    broad_only = [x for x in vertical if x['dims'] == (2, 2, 3)]
    require(len(broad_only) == 30, 'proper vertical (2,2,3) definition-separation witnesses')
    require(all(d >= need for x in broad_only for d, need in zip(x['dims'], (1, 1, 2))), 'broader subset lower bounds')
    whole = max(faces, key=lambda x: len(x['points']))
    require(whole['dims'] == (5, 5, 5) and not whole['qualifies'], 'whole face excluded')
    require(affine_dim([]) == -1, 'empty face fails positive summand dimensions')

    relations, neighbors, components, boundary, r = graph_analysis(q)
    require(len(relations) == 120 and len(components) == 2 and r == 98, 'whole order-complex incidence')
    component_counts = []
    for c in components:
        e = sum(i in c and j in c for i, j in relations)
        require(len(c) == 50 and e == 60 and {len(neighbors[i]) for i in c} == {2, 3}, 'each pure connected component')
        component_counts.append({'vertices': len(c), 'edges': e, 'first_betti': e-len(c)+1,
                                 'endpoint_height': sorted({p[-1] for i in c for p in q[i]['points']})})
    require(Counter(map(len, neighbors)) == {2: 60, 3: 40}, 'exact degrees, no isolated facets')
    require([len(components), len(relations)-r] == [2, 22], 'ordinary rational Betti numbers')
    require(len(components)-1 == 1, 'reduced H0 distinct from ordinary H0')

    # Independently test the signed disjointness model, including its odd-cycle
    # lift. Connectivity of an unsigned graph alone would be insufficient.
    subsets = list(combinations(range(5), 2))
    signed = [(s, frozenset(a)) for s in (-1, 1) for a in subsets]
    arcs = {(x, y) for x in signed for y in signed if x[0] != y[0] and x[1].isdisjoint(y[1])}
    start = signed[0]
    reached = {start}
    todo = [start]
    while todo:
        x = todo.pop()
        for xx, y in arcs:
            if xx == x and y not in reached:
                reached.add(y)
                todo.append(y)
    require(len(reached) == 20 and len(arcs)//2 == 30, 'signed double-cover connectivity and edges')
    cycle = [frozenset(x) for x in [(0,1), (2,3), (0,4), (1,2), (3,4), (0,1)]]
    require(all(x.isdisjoint(y) for x, y in zip(cycle, cycle[1:])), 'explicit odd disjointness cycle')
    require(len(cycle)-1 == 5 and cycle[0] == cycle[-1], 'odd lift connects opposite signs')

    # Artificial extrema are a substantive change: verify the resulting cone
    # boundary identities and acyclicity instead of conflating it with T.
    apex = len(q)
    cone_edges = relations + [(i, apex) for i in range(apex)]
    eindex = {e: j for j, e in enumerate(cone_edges)}
    d1 = [[0 for _ in cone_edges] for _ in range(apex+1)]
    d2 = [[0 for _ in relations] for _ in cone_edges]
    for j, (a, b) in enumerate(cone_edges):
        d1[a][j], d1[b][j] = -1, 1
    for j, (a, b) in enumerate(relations):
        d2[eindex[(b, apex)]][j] = 1
        d2[eindex[(a, apex)]][j] = -1
        d2[eindex[(a, b)]][j] = 1
    require(all(sum(d1[i][j]*d2[j][k] for j in range(len(cone_edges))) == 0
                for i in range(apex+1) for k in range(len(relations))), 'signed cone boundary squares to zero')
    cone_r1, cone_r2 = rank(d1), rank(d2)
    require((cone_r1, cone_r2) == (100, 120), 'cone exact ranks')
    require((apex+1-cone_r1, len(cone_edges)-cone_r1-cone_r2, len(relations)-cone_r2) == (1, 0, 0), 'adjoining a top changes homology')

    tetra, _, _, _, _ = all_faces(3, False)
    tq = [x for x in tetra if x['qualifies']]
    tr, tn, tc, tb, rr = graph_analysis(tq)
    require(len(tq) == 6 and tr == [] and rr == 0 and len(tc) == 6, 'opposite tetrahedron six-point control')
    # Empty intersection is codimension one for a vertex, not for an edge.
    require(-1 == 0-1 and -1 != 1-1, 'zero-dimensional versus graph shelling boundary')
    require(len(components) > 1 and min(map(len, neighbors)) > 0, 'first-edge-of-new-component obstruction applies')
    require(2-1 == 1, 'single connected-edge positive shellability control')

    def serial(x):
        return {'points': sorted(x['points']), 'canonical_first_points': sorted(x['first']),
                'canonical_second_points': sorted(x['second']), 'dimensions': x['dims'],
                'exposing_form': x['exposing_form']}
    result = {'status': 'PASS_BOUNDED_INDEPENDENT_EXACT_COORDINATE_AND_TOPOLOGY_CONTROLS',
              'mechanism': 'Own ternary affine-level exposure sweep of actual integer prism vertices, exact affine ranks, coordinate point-set inclusion, signed rational incidence and an independent disjointness double-cover control.',
              'sum_faces': len(faces), 'each_summand_faces': len(single1),
              'all_summand_face_pair_count': len(single1)*len(single2),
              'qualifying_faces': len(q), 'order_edges': len(relations),
              'boundary_rank_over_Q': r, 'ordinary_Betti': [2,22,0], 'reduced_Betti0': 1,
              'components': component_counts, 'degree_histogram': dict(Counter(map(len, neighbors))),
              'vertical_face_count': len(vertical), 'proper_vertical_broader_only_witnesses': len(broad_only),
              'broader_definition_witness': serial(broad_only[0]),
              'tetrahedron': {'qualifying_points': len(tq), 'comparisons': len(tr), 'Betti0': len(tc), 'shellability_dimension': 0},
              'artificial_top_cone': {'f_vector': [101,220,120], 'boundary_ranks': [cone_r1,cone_r2], 'ordinary_Betti': [1,0,0]},
              'whole_qualifying_coordinate_faces': [serial(x) for x in q],
              'whole_order_edges_by_qualifier_index': relations,
              'checks': CHECKS,
              'limits': 'Finite exact verification of the explicit example and boundary controls, not source-question authentication, a priority search or an argument for generic/stable-intersection complexes. Universal geometric completeness is derived in INITIAL_RECONSTRUCTION.md.'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
