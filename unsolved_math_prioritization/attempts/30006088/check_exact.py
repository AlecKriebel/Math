#!/usr/bin/env python3
"""Exact finite-graph and algebra checks. No source files or network are read.

The checks support elementary reductions; they do not prove a continuum limit.
Explicit exceptions keep every test active under python -O and -OO.
"""
from fractions import Fraction as F
from itertools import combinations
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def configurations(edges):
    vertices = sorted({v for e in edges for v in e})
    out = []
    for mask in range(1 << len(edges)):
        chosen = [e for i, e in enumerate(edges) if mask & (1 << i)]
        adj = {v: set() for v in vertices}
        for u, v in chosen:
            adj[u].add(v)
            adj[v].add(u)
        if any(len(a) not in (0, 2) for a in adj.values()):
            continue
        unseen = {v for v, a in adj.items() if a}
        cycles = []
        while unseen:
            todo = [min(unseen)]
            component = set()
            while todo:
                v = todo.pop()
                if v in component:
                    continue
                component.add(v)
                todo.extend(adj[v] - component)
            unseen -= component
            cycle_edges = frozenset(e for e in chosen if e[0] in component)
            require(len(cycle_edges) == len(component), "component is not a cycle")
            cycles.append(cycle_edges)
        out.append(tuple(cycles))
    return out


def vertices_of(cycle):
    return frozenset(v for e in cycle for v in e)


def check_graph(name, edges):
    edges = sorted({tuple(sorted(e)) for e in edges})
    configs = configurations(edges)
    cycles = sorted({c for conf in configs for c in conf}, key=lambda c: sorted(c))
    checks = 0
    x = F(2, 3)
    for n in (F(1, 5), F(1), F(2)):
        def weight(conf):
            return n ** len(conf) * x ** sum(len(c) for c in conf)
        z = sum((weight(conf) for conf in configs), F(0))
        def z_deleted(vs):
            return sum((weight(conf) for conf in configs
                        if all(not (vertices_of(c) & vs) for c in conf)), F(0))
        singles = {}
        for c in cycles:
            direct = sum((weight(conf) for conf in configs if c in conf), F(0)) / z
            formula = n * x ** len(c) * z_deleted(vertices_of(c)) / z
            require(direct == formula, name + ": single-loop formula")
            singles[c] = direct
            checks += 1
        for c, d in combinations(cycles, 2):
            direct = sum((weight(conf) for conf in configs if c in conf and d in conf), F(0)) / z
            vc, vd = vertices_of(c), vertices_of(d)
            if vc & vd:
                require(direct == 0, name + ": intersecting loops coexist")
            else:
                formula = n*n * x ** (len(c)+len(d)) * z_deleted(vc | vd) / z
                require(direct == formula, name + ": two-loop formula")
                ratio = z*z_deleted(vc | vd)/(z_deleted(vc)*z_deleted(vd))
                require(direct / (singles[c]*singles[d]) == ratio, name + ": ratio formula")
                def one_cycle_sum(vs):
                    return sum((x ** len(a) for a in cycles if not (vertices_of(a) & vs)), F(0))
                coeff = one_cycle_sum(frozenset()) + one_cycle_sum(vc | vd) - one_cycle_sum(vc) - one_cycle_sum(vd)
                both = sum((x ** len(a) for a in cycles if vertices_of(a) & vc and vertices_of(a) & vd), F(0))
                require(coeff == both and coeff >= 0, name + ": fugacity derivative")
            checks += 1
    return {"graph": name, "edges": len(edges), "configurations": len(configs), "simple_cycles": len(cycles), "checks": checks}


def main():
    if "--force-failure" in sys.argv:
        require(False, "intentional failure: optimization must not disable this")
    graphs = []
    for k in (3, 4, 5):
        edges = [(i, i+1) for i in range(k-1)] + [(k+i, k+i+1) for i in range(k-1)] + [(i, k+i) for i in range(k)]
        graphs.append(("ladder_"+str(k), edges))
    cube = [(v, v ^ (1 << b)) for v in range(8) for b in range(3) if v < (v ^ (1 << b))]
    graphs.append(("cube", cube))
    triangles = [(3*j+i, 3*j+(i+1)%3) for j in range(3) for i in range(3)] + [(2, 3), (5, 6)]
    graphs.append(("three_triangles_with_bridges", triangles))
    results = [check_graph(name, edges) for name, edges in graphs]
    # Algebraic identities used in the report, with exact symbolic arithmetic.
    import sympy as sp
    k, b, A, C = sp.symbols("k b A C", nonzero=True)
    c = (6-k)*(3*k-8)/(2*k)
    require(sp.simplify(c-(1-6*(1-4/k)**2/(4/k))) == 0, "central charge conversion")
    require(sp.simplify(A*C/b/(1-C/b)-A*C/(b-C)) == 0, "geometric-resolvent identity")
    require(sp.simplify(-2*sp.cos(4*sp.pi/3)-1) == 0, "Ising n=1 at kappa=3")
    require(sp.simplify(c.subs(k, sp.Rational(8, 3))) == 0, "zero central charge endpoint")
    require(sp.limit((4/k-1)/sp.sin(sp.pi*(1-k/4)), k, 4) == 1/sp.pi, "kappa=4 removable prefactor")
    t = sp.symbols("t", positive=True, real=True)
    require(sp.simplify(sp.sin(sp.I*t)/(sp.I*t)/(sp.cos(sp.I*t)-1)
                       - sp.sinh(t)/(t*(sp.cosh(t)-1))) == 0, "kappa=4 hyperbolic resolvent")
    # Rare-event counterexample: first moments vanish but second factorial moments do not.
    for m in range(2, 32):
        p = F(1, m*m)
        require(p*m == F(1, m), "first moment counterexample")
        require(p*m*(m-1) == F(m-1, m), "second moment counterexample")
    print(json.dumps({"status": "PASS", "arithmetic": "exact integer, rational and symbolic", "graphs": results,
                      "finite_graph_checks": sum(r["checks"] for r in results),
                      "symbolic_checks": 6, "rare_event_checks": 60,
                      "continuum_claim_verified": False}, indent=2))


if __name__ == "__main__":
    main()
