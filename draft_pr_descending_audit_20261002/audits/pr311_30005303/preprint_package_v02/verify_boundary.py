"""Exact, finite falsification checks accompanying the all-graph prose proof.

Standard library only. Run with ordinary Python (assertions enabled).
This is not a proof of the all-graph theorem. No stochastic or floating checks.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from collections import deque
import json
import sys

if sys.flags.optimize:
    raise SystemExit('Run without -O/PYTHONOPTIMIZE: assertions are required.')

def cube(n):
    return list(product((0, 1), repeat=n))

def mtp2(w):
    for x, y in product(w, repeat=2):
        lo = tuple(min(a, b) for a, b in zip(x, y))
        hi = tuple(max(a, b) for a, b in zip(x, y))
        if w[lo] * w[hi] < w[x] * w[y]:
            return False
    return True

def pow2(k):
    return Q(2**k) if k >= 0 else Q(1, 2**(-k))

def gauge(n, edges, h, j):
    """Integer network; residuals independently checked on EVERY assignment."""
    s, t = n, n+1
    c = [[0]*(n+2) for _ in range(n+2)]
    b = [-a for a in h]
    for (u, v), interaction in zip(edges, j):
        assert interaction >= 0
        c[u][v] += interaction
        b[u] -= interaction
    for i, cost in enumerate(b):
        if cost >= 0:
            c[i][t] += cost
        else:
            c[s][i] -= cost
    r = [row[:] for row in c]
    value = 0
    while True:
        parent = {s: None}; queue = deque([s])
        while queue and t not in parent:
            u = queue.popleft()
            for v in range(n+2):
                if r[u][v] > 0 and v not in parent:
                    parent[v] = u; queue.append(v)
        if t not in parent:
            break
        path = []; v = t
        while v != s:
            u = parent[v]; path.append((u, v)); v = u
        delta = min(r[u][v] for u, v in path)
        for u, v in path:
            r[u][v] -= delta; r[v][u] += delta
        value += delta
    energies = {x: -sum(a*z for a, z in zip(h, x))
                -sum(a*x[u]*x[v] for (u,v),a in zip(edges,j)) for x in cube(n)}
    minimum = min(energies.values()); cut_values = []
    for x, energy in energies.items():
        U = {s} | {i for i,z in enumerate(x) if z}
        cut = sum(c[u][v] for u in U for v in range(n+2) if v not in U)
        residual = sum(r[u][v] for u in U for v in range(n+2) if v not in U)
        cut_values.append(cut)
        assert residual == cut-value == energy-minimum
        assert residual >= 0
    assert value == min(cut_values)
    assert all(r[u][v] == 0 or u >= n or v >= n or tuple(sorted((u,v))) in edges
               for u in range(n+2) for v in range(n+2))
    weights = {x: pow2(-(energy-minimum)) for x,energy in energies.items()}
    assert max(weights.values()) == 1 and 1 <= sum(weights.values()) <= 2**n
    assert mtp2(weights)
    return len(energies)

def density(n, edges, pins, implications, h, j):
    """Reconstruct the quotient coefficients of deliberately nonattractive gauges."""
    states = cube(n)
    S = [x for x in states if all(x[i] == a for i,a in pins.items())
         and all(x[i] <= x[k] for i,k in implications)]
    def logw(x):
        return sum(a*z for a,z in zip(h,x))+sum(a*x[u]*x[v] for (u,v),a in zip(edges,j))
    w = {x: pow2(logw(x)) if x in S else Q(0) for x in states}
    assert S and mtp2(w)
    projections = {e: {(x[e[0]],x[e[1]]) for x in S} for e in edges}
    unary = [{x[i] for x in S} for i in range(n)]
    local = [x for x in states if all(x[i] in unary[i] for i in range(n))
             and all((x[u],x[v]) in projections[u,v] for u,v in edges)]
    assert local == S
    pinned = {i: next(iter(unary[i])) for i in range(n) if len(unary[i]) == 1}
    active = set(range(n))-set(pinned)
    forces = {(i,k) for i in active for k in active if all(x[i] <= x[k] for x in S)}
    classes = []; unseen = set(active)
    while unseen:
        i = min(unseen)
        K = tuple(sorted(k for k in active if (i,k) in forces and (k,i) in forces))
        classes.append(K); unseen.difference_update(K)
    owner = {i:k for k,K in enumerate(classes) for i in K}
    H = [sum(h[i] for i in K) for K in classes]
    constant = sum(h[i]*a for i,a in pinned.items()); B = {}
    for (u,v), coefficient in zip(edges,j):
        if u in pinned and v in pinned:
            constant += coefficient*pinned[u]*pinned[v]
        elif u in pinned:
            H[owner[v]] += coefficient*pinned[u]
        elif v in pinned:
            H[owner[u]] += coefficient*pinned[v]
        elif owner[u] == owner[v] or (u,v) in forces:
            H[owner[u]] += coefficient
        elif (v,u) in forces:
            H[owner[v]] += coefficient
        else:
            key = tuple(sorted((owner[u],owner[v])))
            B[key] = B.get(key,0)+coefficient
    assert all(value >= 0 for value in B.values())
    representatives = [K[0] for K in classes]
    chosen = {}
    for key in B:
        chosen[key] = next(e for e in edges if set(owner.get(i,-1) for i in e) == set(key))
    def L(x):
        return constant+sum(a*x[i] for a,i in zip(H,representatives)) + sum(a*x[chosen[k][0]]*x[chosen[k][1]] for k,a in B.items())
    active_arcs = []
    for u,v in edges:
        if u in active and v in active:
            if (1,0) not in projections[u,v]: active_arcs.append((u,v))
            if (0,1) not in projections[u,v]: active_arcs.append((v,u))
    def D(x):
        return sum(x[i] != a for i,a in pinned.items()) + sum(x[i]*(1-x[k]) for i,k in active_arcs)
    assert [x for x in states if D(x) == 0] == S
    assert all(L(x) == logw(x) for x in S)
    target_z = sum(w.values()); target = {x:w[x]/target_z for x in states}
    errors = []
    for penalty in [0,4,8,16]:
        weights = {x:pow2(L(x)-penalty*D(x)) for x in states}
        assert mtp2(weights)
        Z = sum(weights.values())
        errors.append(sum(abs(weights[x]/Z-target[x]) for x in states))
    assert all(a >= b for a,b in zip(errors,errors[1:]))
    return dict(support_size=len(S),classes=classes,aggregate_couplings={str(k):v for k,v in B.items()},
                l1_errors_exact=[str(a) for a in errors])

def main():
    networks = assignments = 0
    for n in range(5):
        all_edges = list(combinations(range(n),2))
        for mask in range(2**len(all_edges)):
            edges = [e for k,e in enumerate(all_edges) if mask >> k & 1]
            for sample in range(5):
                h = [((i+2)*(sample+1))%7-3 for i in range(n)]
                j = [(k+sample)%4 for k in range(len(edges))]
                assignments += gauge(n,edges,h,j); networks += 1
    examples = [
        density(3,[(0,1),(0,2),(1,2)],{},[(0,1),(1,0)],[-2,1,0],[0,-3,5]),
        density(4,[(0,1),(1,2),(2,3)],{0:1},[(1,2)],[-1,2,0,-2],[-4,-7,3]),
        density(5,[(0,1),(1,2),(0,3)],{3:1},[(0,1),(1,0),(2,1)],[1,-2,3,0,0],[-5,-4,2]),
        density(1,[],{0:0},[],[3],[]),
        density(0,[],{},[],[],[]),
    ]
    psi = {(0,0):1,(0,1):1,(1,0):1,(1,1):0}
    pinned = {x:Q((1-x[0])*psi[x],2) for x in cube(2)}
    assert mtp2(pinned) and psi[0,0]*psi[1,1]-psi[0,1]*psi[1,0] == -1
    eps = Q(1,10)
    smoothed = {x:(1 if x[0]==0 else eps)*(psi[x] or eps) for x in cube(2)}
    assert not mtp2(smoothed)
    print(json.dumps(dict(status='PASS_FINITE_BOUNDARY_AND_RESIDUAL_CONTROLS',
          arithmetic='integers and exact rational powers of two',graph_vertices_tested='0 through4; every simple graph; five deterministic parameter samples each',
          networks=networks,cut_assignments_checked=assignments,density_examples=examples,
          invalid_given_potential_and_naive_smoothing_shortcuts_falsified=True,
          limitation='Finite controls illustrate the proof and detect specified shortcuts; they do not prove the all-graph theorem.'),indent=2))

if __name__ == '__main__': main()
