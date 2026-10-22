#!/usr/bin/env python3
"""Independent exact H-polytope audit; no import of the submitted algorithms.

Enumerate vertices from every full-rank active-inequality subsystem. Obtain
edges as finite vertex sets cut out by all but one of the tight inequalities
at a simple extremal vertex. Label extremal vertices through weight images,
not through chain diagrams. Test face inclusion by complete vertex sets, using
the source's explicit codimension-one meaning of 'precedes' (Section 2.3).
Also record the stronger all-strict-predecessor condition as a stress test;
it is not the definition in the source and need not give the same Borel list.
"""
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json


def solve_unique(a, b):
    d = len(b)
    a = [[Fraction(x) for x in r] + [Fraction(y)] for r, y in zip(a, b)]
    for i in range(d):
        pivot = next((j for j in range(i, d) if a[j][i]), None)
        if pivot is None:
            return None
        a[i], a[pivot] = a[pivot], a[i]
        c = a[i][i]
        a[i] = [x / c for x in a[i]]
        for j in range(d):
            if j != i:
                c = a[j][i]
                a[j] = [x - c*y for x, y in zip(a[j], a[i])]
    return tuple(r[-1] for r in a)


def dot(a, x):
    return sum(v*w for v, w in zip(a, x))


def composition(a, b):
    return tuple(a[i-1] for i in b)


def length(w):
    return sum(w[i] > w[j] for i in range(len(w)) for j in range(i+1, len(w)))


def below(u, w):
    n = len(u)
    return all(sum(x <= q for x in u[:p]) >= sum(x <= q for x in w[:p])
               for p in range(1, n+1) for q in range(1, n+1))


def build(top):
    n = len(top)
    coords = [(r, k) for r in range(1, n) for k in range(n-r)]
    d = len(coords)
    inequalities = []
    # Every inequality is a*x >= c. Save its two endpoints only for
    # checking the independently supplied certificate's equation labels.
    for r, k in coords:
        for j, sign in ((k, 1), (k+1, -1)):
            a = [0]*d
            a[coords.index((r, k))] = sign
            c = sign*top[j] if r == 1 else 0
            if r > 1:
                a[coords.index((r-1, j))] = -sign
            inequalities.append((a, c, ((r, k), (r-1, j))))
    vertex_set = set()
    for subset in combinations(range(len(inequalities)), d):
        x = solve_unique([inequalities[i][0] for i in subset],
                         [inequalities[i][1] for i in subset])
        if x is not None and all(dot(a, x) >= c for a, c, _ in inequalities):
            vertex_set.add(x)
    vertices = sorted(vertex_set)
    tight = [{i for i, (a, c, _) in enumerate(inequalities) if dot(a, v) == c}
             for v in vertices]

    def weight(x):
        sums = [sum(top)] + [sum(x[j] for j, (s, _) in enumerate(coords) if s == r)
                                  for r in range(1, n)] + [0]
        return tuple(sums[i+1]-sums[i] for i in range(n))

    weights = [weight(v) for v in vertices]
    extremal = {}
    ps = list(permutations(range(1, n+1)))
    edges = {}
    for p in ps:
        wt = [None]*n
        for i, place in enumerate(p):
            wt[place-1] = -top[i]
        candidates = [i for i, w in enumerate(weights) if w == tuple(wt)]
        assert len(candidates) == 1
        vi = candidates[0]
        extremal[p] = vi
        assert len(tight[vi]) == d
        edges[p] = []
        for omitted in tight[vi]:
            retained = tight[vi] - {omitted}
            endpoints = [j for j in range(len(vertices)) if retained <= tight[j]]
            assert len(endpoints) == 2 and vi in endpoints
            other = next(j for j in endpoints if j != vi)
            delta = [a-b for a, b in zip(weights[other], weights[vi])]
            positive = [j for j, a in enumerate(delta) if a > 0]
            negative = [j for j, a in enumerate(delta) if a < 0]
            assert len(positive) == len(negative) == 1
            i, j = positive[0], negative[0]
            assert delta[i] == -delta[j]
            edges[p].append((omitted, i+1, j+1, other))

    def face(p, b):
        vi = extremal[p]
        omitted = {edge for edge, i, j, _ in edges[p] if b.index(i) < b.index(j)}
        retained = tight[vi] - omitted
        vs = {j for j in range(len(vertices)) if retained <= tight[j]}
        return retained, vs

    return ps, coords, inequalities, vertices, tight, extremal, face


def run(top, cert):
    ps, coords, inequalities, vertices, tight, extremal, face = build(top)
    n = len(top)
    nonrepresentable = []
    all_admissible = {}
    stronger_borels = {}
    target_faces = {}
    for w in ps:
        good = []
        strong_good = []
        predecessors = [u for u in ps if u != w and below(u, w)]
        covers = [u for u in predecessors if length(u)+1 == length(w)]
        for b in ps:
            s = composition(b, w)
            eqs, vs = face(s, b)
            assert len(coords)-len(eqs) == length(w)
            if all(face(composition(b, u), b)[1] <= vs for u in covers):
                good.append(b)
            if all(face(composition(b, u), b)[1] <= vs for u in predecessors):
                strong_good.append(b)
            if n == 4 and w == (2, 4, 1, 3):
                target_faces[b] = (eqs, vs)
        all_admissible[''.join(map(str, w))] = [''.join(map(str, b)) for b in good]
        stronger_borels[''.join(map(str, w))] = [''.join(map(str, b)) for b in strong_good]
        if not good:
            nonrepresentable.append(''.join(map(str, w)))

    certificate_checks = 0
    if n == 4:
        w = (2, 4, 1, 3)
        assert len(cert) == 24 and {tuple(z['b']) for z in cert} == set(ps)
        for z in cert:
            b = tuple(z['b'])
            u = tuple(z['predecessor'])
            assert tuple(z['sigma']) == composition(b, w)
            assert tuple(z['sigma_predecessor']) == composition(b, u)
            assert below(u, w) and length(u)+1 == length(w)
            eqs, vs = target_faces[b]
            pred = extremal[composition(b, u)]
            eq = tuple(tuple(x) for x in z['equality'])
            idx = next(i for i, (_, _, e) in enumerate(inequalities) if e == eq)
            assert idx in eqs and idx not in tight[pred] and pred not in vs
            def coord_label(c):
                r, k = c
                v = top[k] if r == 0 else vertices[pred][coords.index(c)]
                return top.index(v)+1
            assert list(map(coord_label, eq)) == z['top_labels_at_predecessor']
            certificate_checks += 1

        # The rank-incidence equality is tested against the entire Weyl group,
        # independently of the enumeration of downward position transpositions.
        interval = {u for u in ps if below(u, w)}
        incidence = {u for u in ps if u[0] <= 2 and {1, 2} <= set(u[:3])}
        assert interval == incidence and len(interval) == 8
        assert sorted(''.join(map(str, u)) for u in interval if length(u) == 2) == ['1423', '2143', '2314']

    expected = {2: [], 3: [], 4: ['2413', '3412', '4231']}
    assert nonrepresentable == expected[n]
    return {
        'n': n, 'top_row': list(top), 'all_polytope_vertices': len(vertices),
        'extremal_vertices': len(extremal), 'nonrepresentable': nonrepresentable,
        'certificate_rows_verified': certificate_checks,
        'admissible_borels_by_class': all_admissible,
        'stronger_all_predecessor_borels_by_class': stronger_borels,
        'source_admissibility_uses_covers': True,
        'all_strict_Bruhat_predecessors_tested': True,
        'face_inclusion_method': 'Complete enumerated vertex sets',
        'arithmetic': 'Exact rational',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = args.certificate.read_bytes()
    cert = json.loads(data)
    cases = [(1, 2), (1, 2, 3), (1, 2, 3, 4), (0, 2, 7, 19), (-17, -2, 3, 31)]
    results = [run(top, cert) for top in cases]
    output = {'certificate_sha256': hashlib.sha256(data).hexdigest(), 'cases': results}
    args.output.write_text(json.dumps(output, indent=2)+'\n')
    for r in results:
        print(json.dumps({k: v for k, v in r.items() if not k.endswith('borels_by_class')}, sort_keys=True))


if __name__ == '__main__':
    main()
