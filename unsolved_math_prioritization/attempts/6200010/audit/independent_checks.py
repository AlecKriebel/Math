#!/usr/bin/env python3
"""Independent finite controls, with exact rational and prime-field arithmetic.

These checks supplement the audit's proofs; they cannot settle the existence
question for arbitrary finite nerves. No author checker is imported.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
import json


class Checks:
    def __init__(self):
        self.counts = Counter()

    def require(self, test, name):
        if not test:
            raise RuntimeError("independent check failed: " + name)
        self.counts[name] += 1


def downward(facets):
    return frozenset(tuple(c) for f in facets for k in range(1, len(f) + 1)
                     for c in combinations(sorted(f), k))


def vertices(k):
    return sorted({s[0] for s in k if len(s) == 1})


def induced(k, keep):
    keep = set(keep)
    return frozenset(s for s in k if set(s) <= keep)


def link(k, face):
    f = set(face)
    return frozenset(tuple(v for v in s if v not in f)
                     for s in k if f < set(s))


def ranks(columns, prime=0):
    """Sparse column elimination; Fraction when prime is zero."""
    pivots = {}
    for original in columns:
        if prime:
            col = {i: x % prime for i, x in original.items() if x % prime}
        else:
            col = {i: Fraction(x) for i, x in original.items() if x}
        while col:
            row = min(col)
            if row not in pivots:
                z = pow(col[row], -1, prime) if prime else 1 / col[row]
                pivots[row] = {i: (x * z % prime if prime else x * z)
                               for i, x in col.items()}
                break
            factor = col[row]
            for i, x in pivots[row].items():
                value = col.get(i, 0) - factor * x
                if prime:
                    value %= prime
                if value:
                    col[i] = value
                else:
                    col.pop(i, None)
    return len(pivots)


def simplicial_chain(k):
    cells = [sorted(s for s in k if len(s) == d + 1)
             for d in range(max(map(len, k), default=0))]
    ds = []
    for d in range(1, len(cells)):
        ix = {s: i for i, s in enumerate(cells[d - 1])}
        ds.append([{ix[s[:j] + s[j + 1:]]: (-1) ** j
                    for j in range(len(s))} for s in cells[d]])
    return cells, ds


@lru_cache(maxsize=None)
def homology(k, prime=0):
    cells, ds = simplicial_chain(k)
    rr = [0] + [ranks(d, prime) for d in ds] + [0]
    return tuple(len(c) - rr[i] - rr[i + 1] for i, c in enumerate(cells))


def reduced_degree(k, prime=0):
    if not k:
        return -1
    b = list(homology(k, prime))
    b[0] -= 1
    return max((i for i, x in enumerate(b) if x), default=-2)


def puncture_max(k, prime=0):
    vs = set(vertices(k))
    return max(reduced_degree(induced(k, vs - set(s)), prime) for s in [()] + sorted(k))


def all_complexes(n):
    singleton = [(i,) for i in range(n)]
    other = [c for d in range(2, n + 1) for c in combinations(range(n), d)]
    for mask in range(1 << len(other)):
        faces = frozenset(singleton + [s for i, s in enumerate(other) if mask >> i & 1])
        if downward(faces) == faces:
            yield faces


def connected(k):
    vs = set(vertices(k))
    if not vs:
        return False
    seen = {min(vs)}
    while True:
        enlarged = seen | {v for e in k if len(e) == 2 and set(e) & seen for v in e}
        if enlarged == seen:
            return seen == vs
        seen = enlarged


def closed_surface(k, chi, ck):
    tris = [s for s in k if len(s) == 3]
    edges = Counter(e for t in tris for e in combinations(t, 2))
    ck.require(downward(tris) == k, "surface_purity")
    ck.require(set(edges.values()) == {2}, "surface_edge_incidence")
    ck.require(connected(k), "surface_connected")
    ck.require(len(vertices(k)) - len(edges) + len(tris) == chi, "surface_euler")
    for v in vertices(k):
        l = link(k, (v,))
        valences = Counter(x for e in l if len(e) == 2 for x in e)
        ck.require(connected(l) and set(valences.values()) == {2}, "surface_circle_links")


def cube_chain(k, n):
    cells = [[] for _ in range(max(map(len, k)) + 1)]
    for word in product((-1, 0, 1), repeat=n):
        active = tuple(i for i, x in enumerate(word) if x == -1)
        if not active or active in k:
            cells[len(active)].append(word)
    ds = []
    for d in range(1, len(cells)):
        ix = {w: i for i, w in enumerate(cells[d - 1])}
        columns = []
        for w in cells[d]:
            col = {}
            for j, coordinate in enumerate(i for i, x in enumerate(w) if x == -1):
                for value in (0, 1):
                    face = list(w)
                    face[coordinate] = value
                    col[ix[tuple(face)]] = (-1) ** (j + 1 - value)
            columns.append(col)
        ds.append(columns)
    return cells, ds


def chain_square(ds, ck, category):
    for a, b in zip(ds, ds[1:]):
        for col in b:
            answer = defaultdict(int)
            for j, coefficient in col.items():
                for i, x in a[j].items():
                    answer[i] += coefficient * x
            ck.require(not any(answer.values()), category)


def triangulate_cubes(cells):
    facets = []
    for word in cells[-1]:
        free = [i for i, x in enumerate(word) if x == -1]
        for ordering in permutations(free):
            bits = sum(1 << i for i, x in enumerate(word) if x == 1)
            path = [bits]
            for i in ordering:
                bits += 1 << i
                path.append(bits)
            facets.append(path)
    return downward(facets)


def barycentric(k):
    fs = sorted(k, key=lambda s: (len(s), s))
    out = []
    def visit(chain):
        out.append(tuple(chain))
        for j in range(chain[-1] + 1, len(fs)):
            if set(fs[chain[-1]]) < set(fs[j]):
                visit(chain + [j])
    for j in range(len(fs)):
        visit([j])
    return frozenset(out), fs


def run():
    ck = Checks()
    small_counts = {}
    for n in range(5):
        complexes = list(all_complexes(n))
        small_counts[str(n)] = len(complexes)
        for k in complexes:
            subsets = [s for size in range(n + 1) for s in combinations(range(n), size)]
            for p in (0, 2, 3):
                d = puncture_max(k, p)
                arbitrary = max(reduced_degree(induced(k, u), p) for u in subsets)
                ck.require(d == arbitrary, "all_small_induced_puncture_maxima")
                for v in range(n):
                    ck.require(d >= puncture_max(link(k, (v,)), p), "all_small_link_monotonicity")
    rp = downward([(0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 5),
                   (1, 2, 5), (1, 3, 4), (1, 4, 5), (2, 3, 4), (2, 3, 5)])
    closed_surface(rp, 1, ck)
    ck.require(homology(rp) == (1, 0, 0), "projective_plane_exact_Q")
    ck.require(homology(rp, 2) == (1, 1, 1), "projective_plane_F2")
    cells, ds = cube_chain(rp, 6)
    counts = list(map(len, cells))
    ck.require(counts == [64, 192, 240, 80], "independent_cubical_counts")
    chain_square(ds, ck, "cubical_integer_chain_identity")
    fields = {}
    for p in (0, 2, 3, 103):
        rr = [ranks(d, p) for d in ds]
        ck.require(rr == ([63, 129, 79] if p == 2 else [63, 129, 80]), "independent_cubical_ranks")
        pad = [0] + rr + [0]
        b = [counts[i] - pad[i] - pad[i + 1] for i in range(4)]
        fields[str(p) if p else "Q"] = {"ranks": rr, "betti": b}
    t = triangulate_cubes(cells)
    tc, td = simplicial_chain(t)
    tf = list(map(len, tc))
    ck.require(tf == [64, 512, 960, 480], "independent_triangulated_counts")
    chain_square(td, ck, "simplicial_integer_chain_identity")
    incidence = Counter(face for tet in tc[3] for face in combinations(tet, 3))
    ck.require(set(incidence.values()) == {2}, "triangles_in_two_tetrahedra")
    for v in range(64):
        l = link(t, (v,))
        closed_surface(l, 1, ck)
        ck.require(homology(l) == (1, 0, 0), "all_64_links_exact_Q")
        ck.require(homology(l, 2) == (1, 1, 1), "all_64_links_F2")
    simplex_fields = {}
    for p in (2, 103):
        rr = [ranks(d, p) for d in td]
        ck.require(rr == ([63, 449, 479] if p == 2 else [63, 449, 480]), "independent_simplicial_ranks")
        simplex_fields[str(p)] = rr
    susp = downward([f + (a,) for f in rp if len(f) == 3 for a in (6, 7)])
    ck.require(homology(susp) == (1, 0, 0, 0), "suspension_exact_Q_acyclic")
    lk = link(susp, (0,))
    closed_surface(lk, 2, ck)
    ck.require(homology(lk) == (1, 0, 1), "orientable_link_exact_Q")
    ck.require(homology(induced(susp, set(range(8)) - {0})) == (1, 0, 1, 0), "orientable_link_deleted_vertex_witness")
    sd, labels = barycentric(downward([(0, 1, 2, 3)]))
    boundary = induced(sd, [i for i, s in enumerate(labels) if len(s) < 4])
    ck.require(homology(sd) == (1, 0, 0, 0), "barycentric_ball_exact_Q")
    ck.require(homology(boundary) == (1, 0, 1), "barycentric_induced_sphere_exact_Q")
    cone = downward([f + (99,) for f in boundary if len(f) == 3])
    ck.require(homology(cone) == (1, 0, 0, 0), "cone_exact_Q_acyclic")
    ck.require(induced(cone, vertices(boundary)) == boundary, "cone_old_sphere_induced")
    # A concrete distinction between individual profiles and their maximum:
    # C4 has an induced disconnected pair, but no simplex deletion disconnects it.
    c4 = downward([(0, 1), (1, 2), (2, 3), (0, 3)])
    ck.require(reduced_degree(induced(c4, {0, 2})) == 0, "individual_profile_differs")
    ck.require(all(reduced_degree(induced(c4, set(range(4)) - set(s))) != 0
                   for s in [()] + sorted(c4)), "no_allowed_puncture_degree_zero")
    ck.require(puncture_max(c4) == 1, "maximum_still_agrees")
    return {"problem_id": 6200010, "status": "independent_finite_controls_pass",
            "checks": sum(ck.counts.values()), "categories": dict(sorted(ck.counts.items())),
            "small_complexes_by_vertex_count": small_counts,
            "cubical_counts": counts, "cubical_field_results": fields,
            "triangulated_f_vector": tf, "triangulated_modular_ranks": simplex_fields,
            "rational_arithmetic": "Exact Fraction elimination, not a modular guess",
            "author_checker_imported": False, "original_problem_resolved": False}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
