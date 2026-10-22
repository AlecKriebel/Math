#!/usr/bin/env python3
"""Independent finite-domain search, no author code, no colour/orbit quotient.

Read an inert 60-vertex edge list; enumerate G-0 with the explicit adjacent
normalization c(1)=0,c(6)=1. Then decide G and every one-edge deletion directly
by complete three-colour domain propagation, branching on every available
colour. No time/node cutoff, floating-point arithmetic, or SAT black box.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def solve(n, edges, omitted=None, fixed=(), collect=False):
    neighbours = [set() for _ in range(n)]
    for a, b in edges:
        if a != omitted and b != omitted:
            neighbours[a].add(b)
            neighbours[b].add(a)
    domains = [7] * n
    assigned = [-1] * n
    if omitted is not None:
        assigned[omitted] = -2
        domains[omitted] = 0
    stats = {'nodes': 0, 'leaves': 0}
    leaves = []

    def apply(ds, cs, v, c):
        if cs[v] != -1:
            return cs[v] == c
        if not ds[v] & (1 << c):
            return False
        cs[v] = c
        ds[v] = 1 << c
        for w in neighbours[v]:
            if cs[w] == c:
                return False
            if cs[w] == -1:
                ds[w] &= ~(1 << c)
                if ds[w] == 0:
                    return False
        return True

    for v, c in fixed:
        if not apply(domains, assigned, v, c):
            return stats, leaves

    def visit(ds, cs):
        stats['nodes'] += 1
        # A singleton is forced, so applying it loses no completion.
        while True:
            forced = next((v for v in range(n) if cs[v] == -1 and ds[v].bit_count() == 1), None)
            if forced is None:
                break
            if not apply(ds, cs, forced, ds[forced].bit_length() - 1):
                return False
        uncoloured = [v for v in range(n) if cs[v] == -1]
        if not uncoloured:
            require(all(cs[a] != cs[b] for a, b in edges if a != omitted and b != omitted),
                    'Completed assignment violates a raw edge')
            stats['leaves'] += 1
            leaves.append(cs)
            return not collect
        v = min(uncoloured, key=lambda w: (ds[w].bit_count(), -len(neighbours[w]), w))
        for c in range(3):
            if ds[v] & (1 << c):
                nd, nc = ds.copy(), cs.copy()
                if apply(nd, nc, v, c) and visit(nd, nc):
                    return True
        return False

    visit(domains, assigned)
    return stats, leaves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('edgelist', type=Path)
    args = ap.parse_args()
    raw = args.edgelist.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == '85914250312a4fe8d1a67d747fea2ee1772c9762796af90095efa61fb4c0400c',
            'Wrong immutable input')
    edges = [tuple(map(int, line.split())) for line in raw.decode('ascii').splitlines()]
    require(len(edges) == len(set(edges)) == 180 and all(0 <= a < b < 60 for a,b in edges),
            'Malformed graph')
    require((1, 6) in edges, 'Normalization vertices not adjacent')
    # Compare this solver to literal colour-assignment enumeration on all
    # labelled simple graphs of orders1..4, including positive/negative cases.
    tested = 0
    for n in range(1, 5):
        possible = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            es = [e for j,e in enumerate(possible) if mask & (1 << j)]
            brute = any(all(cs[a] != cs[b] for a,b in es)
                        for cs in itertools.product(range(3), repeat=n))
            _, found = solve(n, es)
            require(bool(found) == brute, 'Small graph exhaustive comparison failed')
            tested += 1
    puncture_stats, colourings = solve(60, edges, 0, ((1,0),(6,1)), True)
    require(len(colourings) == 16, 'Unexpected normalized puncture count')
    n0 = [v for u,v in edges if u == 0]
    require(n0 == [5,26,30,33,37,55], 'Wrong root neighbourhood')
    require(all(tuple(cs[v] for v in n0) == (1,1,0,2,2,0) for cs in colourings),
            'Unbalanced or inconsistent normalized puncture')
    deletions = []
    for removed in [None] + edges:
        es = edges if removed is None else [e for e in edges if e != removed]
        stats, found = solve(60, es)
        require(not found and stats['leaves'] == 0, 'Three-colouring counterexample: '+str(removed))
        deletions.append({'removed_edge': removed, **stats})
    print(json.dumps({'input_sha256':hashlib.sha256(raw).hexdigest(),
                      'small_graph_cases':tested,
                      'normalized_puncture':puncture_stats,
                      'root_neighbours':n0,
                      'normalized_colourings':colourings,
                      'direct_unsatisfiable_three_colour_instances':deletions,
                      'instances':len(deletions),
                      'nodes':sum(x['nodes'] for x in deletions),
                      'scope':'Complete finite direct check; no author code or infinite-family/formal claim.'},indent=2))


if __name__ == '__main__':
    main()
