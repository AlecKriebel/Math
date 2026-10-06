#!/usr/bin/env python3
"""Finite exact diagnostics; not general additivity or manifold recognition."""
import itertools
import json
import math

CHECKS = 0


def require(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError("check failed: " + label)


def complex_from_facets(facets):
    facets = {frozenset(f) for f in facets}
    if not facets or len({len(f) for f in facets}) != 1:
        raise ValueError("nonempty pure facet list required")
    return facets


def vertices(facets):
    return set().union(*facets)


def all_faces(facets):
    d = len(next(iter(facets)))
    levels = [{frozenset()}] + [set() for _ in range(d)]
    for facet in facets:
        for size in range(1, d + 1):
            levels[size].update(frozenset(f) for f in itertools.combinations(facet, size))
    return levels


def boundary(facets):
    counts = {}
    for facet in facets:
        for vertex in facet:
            ridge = facet - {vertex}
            counts[ridge] = counts.get(ridge, 0) + 1
    require(all(c in (1, 2) for c in counts.values()), "ridge incidence")
    return {ridge for ridge, count in counts.items() if count == 1}


def components(facets):
    if not facets:
        return []
    adjacency = {v: set() for v in vertices(facets)}
    for f in facets:
        for v in f:
            adjacency[v].update(f - {v})
    unseen = set(adjacency)
    output = []
    while unseen:
        reached = {min(unseen)}
        todo = list(reached)
        while todo:
            v = todo.pop()
            new = adjacency[v] - reached
            reached.update(new)
            todo.extend(new)
        unseen.difference_update(reached)
        output.append(reached)
    return output


def h_vector(facets):
    levels = all_faces(facets)
    d = len(levels) - 1
    return [sum((-1) ** (k-j) * math.comb(d-j, d-k) * len(levels[j])
                for j in range(k+1)) for k in range(d+1)]


def gamma(facets):
    levels = all_faces(facets)
    d = len(levels) - 1
    bd = boundary(facets)
    require(bool(bd), "gamma requires boundary")
    interior = len(levels[1]) - len(vertices(bd))
    value = len(levels[2]) - (d-1)*len(levels[1]) + math.comb(d, 2) - interior
    h = h_vector(facets)
    require(value == h[2] - interior, "h2 normalization")
    require(interior == h[d-1] + d*h[d], "interior vertex identity")
    return value


def g2(facets):
    levels = all_faces(facets)
    d = len(levels)-1
    return len(levels[2])-d*len(levels[1])+math.comb(d+1, 2)


def sphere(n):
    return complex_from_facets(itertools.combinations(range(n+2), n+1))


def ball(n):
    return {frozenset(range(n+1))}


def cylinder(n):
    result = set()
    for base in itertools.combinations(range(n+1), n):
        for j in range(n):
            result.add(frozenset([2*v for v in base[:j+1]] +
                                 [2*v+1 for v in base[j:]]))
    return result


def cap_components(facets):
    result = set(facets)
    bd = boundary(facets)
    for number, comp in enumerate(components(bd), max(vertices(facets))+1):
        result.update(f | {number} for f in bd if f.issubset(comp))
    return result


def boundary_sum(left, right):
    lf = min(boundary(left), key=lambda f: tuple(sorted(f)))
    rf = min(boundary(right), key=lambda f: tuple(sorted(f)))
    mapping = dict(zip(sorted(rf), sorted(lf)))
    fresh = max(vertices(left)) + 1
    for v in sorted(vertices(right) - set(rf)):
        mapping[v] = fresh
        fresh += 1
    return set(left) | {frozenset(mapping[v] for v in f) for f in right}


def facet_sum(left, right):
    lf = min(left, key=lambda f: tuple(sorted(f)))
    rf = min(right, key=lambda f: tuple(sorted(f)))
    mapping = dict(zip(sorted(rf), sorted(lf)))
    fresh = max(vertices(left)) + 1
    for v in sorted(vertices(right)-set(rf)):
        mapping[v] = fresh
        fresh += 1
    return (left-{lf}) | {frozenset(mapping[v] for v in f) for f in right-{rf}}


def subdivide_facet(facets, selected=None):
    f = selected if selected is not None else min(facets, key=lambda x: tuple(sorted(x)))
    require(f in facets, "subdivision facet exists")
    new = max(vertices(facets))+1
    return (facets-{f}) | {(f-{v}) | {new} for v in f}, new


def gf2_rank(columns):
    pivots = {}
    for column in columns:
        while column:
            pivot = column.bit_length()-1
            if pivot in pivots:
                column ^= pivots[pivot]
            else:
                pivots[pivot] = column
                break
    return len(pivots)


def betti(facets):
    levels = all_faces(facets)
    ranks = [0]*len(levels)
    for size in range(2, len(levels)):
        indexes = {f: i for i, f in enumerate(levels[size-1])}
        columns = []
        for f in levels[size]:
            column = 0
            for v in f:
                column ^= 1 << indexes[f-{v}]
            columns.append(column)
        ranks[size] = gf2_rank(columns)
    ranks.append(0)
    return [len(levels[size])-ranks[size]-ranks[size+1]
            for size in range(1, len(levels))]


def link(facets, vertex):
    return {f-{vertex} for f in facets if vertex in f}


def check_vertex_links(facets, n, is_closed):
    for vertex in vertices(facets):
        lk = link(facets, vertex)
        expected = [1]+[0]*(n-1)
        if is_closed:
            expected[-1] = 1
        require(betti(lk) == expected, "selected vertex-link homology")


def main():
    product_rows = []
    for n in range(3, 8):
        c = cylinder(n)
        levels = all_faces(c)
        require(len(vertices(c)) == 2*(n+1), "product vertex count")
        require(len(levels[2]) == 3*math.comb(n+1, 2)+(n+1), "product edge count")
        require(len(c) == n*(n+1), "product facet count")
        require(len(components(boundary(c))) == 2, "product boundary components")
        require(gamma(c) == n+1, "cylinder complexity witness")
        require(h_vector(c) == [1]+[n+1]*n+[-1], "full product h-vector")
        capped = cap_components(c)
        require(not boundary(capped), "separate capped boundary empty")
        require(g2(capped) == 0, "separate caps g2 zero")
        require(gamma(ball(n)) == 0, "simplex ball")
        subdivided, _ = subdivide_facet(ball(n))
        require(gamma(subdivided) == 0, "interior facet subdivision gamma")
        if n <= 4:
            expected = [1]+[0]*n
            expected[n-1] = 1
            require(betti(c) == expected, "cylinder homology")
            require(betti(capped) == [1]+[0]*(n-1)+[1], "capped sphere homology")
            check_vertex_links(c, n, False)
            check_vertex_links(capped, n, True)
        product_rows.append({"dimension": n, "f_vector": [len(x) for x in levels[1:]],
                             "gamma": gamma(c), "capped_g2": g2(capped)})

    puncture_rows = []
    for n in range(3, 6):
        k = ball(n)
        for b in range(1, 6):
            require(len(components(boundary(k))) == b, "puncture boundary components")
            require(gamma(k) == (n+1)*(b-1), "punctured sphere witness")
            capped = cap_components(k)
            require(not boundary(capped), "puncture caps closed")
            require(g2(capped) == 0, "puncture caps identity")
            if n == 3:
                require(betti(k) == [1,0,b-1,0], "punctured 3-sphere homology")
            puncture_rows.append({"dimension": n, "punctures": b, "gamma": gamma(k)})
            new_k = boundary_sum(k, cylinder(n))
            require(gamma(new_k) == gamma(k)+gamma(cylinder(n)), "boundary glue identity")
            k = new_k

    separator_rows = []
    for n in range(3, 8):
        s = sphere(n-1)
        for step in range(4):
            a = max(vertices(s))+1
            b = a+1
            left = {f | {a} for f in s}
            right = {f | {b} for f in s}
            k = left | right
            capped_left, capped_right = cap_components(left), cap_components(right)
            defect = g2(s)+len(vertices(s))-(n+1)
            require(g2(capped_left)+g2(capped_right) == g2(k)+defect,
                    "separator capping defect")
            if n == 3:
                require(defect == len(vertices(s))-4, "3D exact loss")
            require(defect >= 0, "example defect nonnegative")
            separator_rows.append({"dimension": n, "separator_vertices": len(vertices(s)),
                                   "separator_g2": g2(s), "defect": defect})
            s, _ = subdivide_facet(s)

    for n in range(3, 8):
        k = sphere(n)
        original_g2 = g2(k)
        selected = min(k, key=lambda f: tuple(sorted(f)))
        original_vertices = sorted(selected)
        for v in original_vertices:
            old_selected = selected
            k, new = subdivide_facet(k, selected)
            selected = (old_selected-{v}) | {new}
            require(selected in k, "retained inner facet")
            require(g2(k) == original_g2, "g2 preserved by stacking")
        require(not (selected & set(original_vertices)), "inner facet has no original vertex")
        punctured = k-{selected}
        require(gamma(punctured) == g2(k), "single puncture normalization")
        connected = facet_sum(k, sphere(n))
        require(not boundary(connected), "facet sum closed")
        require(g2(connected) == g2(k)+g2(sphere(n)), "closed facet sum identity")

    # These intentionally incorrect alternatives must differ on actual examples.
    require(gamma(cylinder(3)) != 2*gamma(ball(3)), "reject unshifted interior ball sum")
    require(gamma(boundary_sum(ball(3), ball(3))) == 0, "distinguish boundary sum")
    require(gamma(cylinder(3)) != len(cylinder(3)), "not minimum-facet normalization")
    require(gamma(cylinder(3)) != len(vertices(cylinder(3))), "not vertex normalization")

    print(json.dumps({"result": "PASS", "checks": CHECKS,
                      "scope": "finite diagnostics only; general additivity unresolved",
                      "products": product_rows, "punctured_spheres": puncture_rows,
                      "separators": separator_rows}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
