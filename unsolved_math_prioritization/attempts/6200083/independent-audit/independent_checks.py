#!/usr/bin/env python3
"""Independently implemented exact finite controls; no author code is imported."""
from fractions import Fraction as Q
import json


def run():
    checks = 0
    def require(ok, label):
        nonlocal checks
        checks += 1
        if not ok:
            raise AssertionError(label)

    # Parabolic bound for positive powers; signed distance must use abs(n).
    ratios = [Q(2*(k+1), 2**k) for k in range(1, 161)]
    for k in range(1, 160):
        require(ratios[k] < ratios[k-1], 'strict decay')
    require(ratios[79] < Q(1, 10**20), 'author endpoint')
    require(ratios[159] < Q(1, 10**40), 'extended endpoint')
    for n in range(-30, 31):
        require(Q(n*n, 2)+1 == Q(abs(n)**2, 2)+1, 'signed cosh identity')
    # At n = -1, 2*asinh(n/2) is negative and cannot be a distance.
    require(Q(-1, 2) < 0 < Q(abs(-1), 2), 'signed formula negative control')

    # A disjoint-set implementation independent of the author BFS.
    def count_components(vertices, edges):
        parent = {v: v for v in vertices}
        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for a,b in edges:
            if a in parent and b in parent:
                parent[find(a)] = find(b)
        return len({find(v) for v in vertices})

    comb_cases = 0
    for n in range(1, 101):
        xs = [Q(0)] + [Q(1,k) for k in range(n, 0, -1)]
        ys = [Q(0), Q(1,4), Q(1,2), Q(1)]
        vertices = {(x,y) for x in xs for y in ys}
        edges = [((x,a),(x,b)) for x in xs for a,b in zip(ys,ys[1:])]
        edges += [((a,Q(0)),(b,Q(0))) for a,b in zip(xs,xs[1:])]
        upper = {v for v in vertices if v[1] > Q(1,4)}
        require(count_components(vertices, edges) == 1, 'connected comb')
        require(count_components(upper, edges) == n+1, 'disconnected upper comb')
        repaired = edges + [((a,Q(1,2)),(b,Q(1,2))) for a,b in zip(xs,xs[1:])]
        require(count_components(upper, repaired) == 1, 'horizontal repair')
        require(Q(1,n+1) <= Q(1,n), 'Hausdorff bound monotonicity')
        for omitted in range(n+1, n+11):
            require(Q(1,omitted) <= Q(1,n+1), 'omitted tooth estimate')
        comb_cases += 1

    # Normalized distances a=d(z,x)/D, b=d(z,y)/D, d=d(x,y)/D.
    # Test unequal base distances and heights, including degenerate triangles.
    grid = [Q(k,4) for k in range(5)]
    heights = [Q(1,2**k) for k in range(6)]
    cone_cases = 0
    def exp_distance(d,u,v):
        return (d+max(u,v))**2/(u*v)
    for a in grid:
        for b in grid:
            for d in grid:
                if not abs(a-b) <= d <= a+b:
                    continue
                for u in heights:
                    for v in heights:
                        lhs = ((1+a)**2/u)*((1+b)**2/v)/exp_distance(d,u,v)
                        rhs = ((1+a)*(1+b)/(d+max(u,v)))**2
                        require(lhs == rhs, 'basepoint Gromov product')
                        require(exp_distance(d,u,v) == exp_distance(d,v,u), 'symmetry')
                        require(exp_distance(d,u,u) <= (1+1/u)**2, 'bounded fixed height')
                        if d > 0:
                            require(exp_distance(d,u/2,u/2) > exp_distance(d,u,u), 'height shift changes distance')
                        else:
                            require(exp_distance(d,u/2,u/2) == 1, 'zero horizontal separation')
                        require(exp_distance(Q(0),u,v) == max(u/v,v/u), 'vertical distance')
                        cone_cases += 1
    return {
        'all_passed': True,
        'assertions': checks,
        'author_code_imported': False,
        'parabolic_positive_powers': 160,
        'signed_displacement_negative_control': True,
        'finite_comb_cases': comb_cases,
        'cone_cases': cone_cases,
        'scope': 'Independent exact finite controls only; not a proof of infinite topology, source theorems, or the full target.'
    }

if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
