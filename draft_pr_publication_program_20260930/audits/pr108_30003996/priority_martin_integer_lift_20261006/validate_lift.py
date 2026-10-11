"""Exact audit check: integer correspondence and fractional whole-lift obstruction.

This checks the existing reduction on one unsatisfiable formula. It does not
introduce a new hardness reduction or claim historical priority.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json

V = ['t', 'f', 'x', 'y', 'q0', 'q1', 'q2', 'q3']
signs = [(1, 1), (1, 0), (0, 1), (0, 0)]
E = [('t', 'f'), ('t', 'x'), ('f', 'x'), ('t', 'y'), ('f', 'y')]
E += [(q, v) for q in V[4:] for v in ['x', 'y']]
A = [(u, v) for e in E for u, v in [e, e[::-1]]]

def orient(T, r):
    adjacency = {v: [] for v in V}
    for u, v in T:
        adjacency[u].append(v); adjacency[v].append(u)
    seen = {r}; stack = [r]; arcs = set()
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v); stack.append(v); arcs.add((u, v))
    return arcs if len(seen) == len(V) else None

def structured(truths, choice):
    return [('t', 'f')] + [(('t' if truths[i] else 'f'), v) for i, v in enumerate(['x', 'y'])] + [(q, ['x', 'y'][choice]) for q in V[4:]]

def cost(r, a, B=2):
    u, v = a
    if r == 't':
        if {u, v} == {'t', 'f'}: return 0
        return B if u.startswith('q') or v.startswith('q') else 1
    if r.startswith('q') and u in ['x', 'y'] and v in ['t', 'f']:
        i = ['x', 'y'].index(u)
        return int((v == 't') != bool(signs[int(r[1:])][i]))
    return 0

def objective(T, B=2, shift=0):
    return sum(cost(r, a, B) + shift for r in V for a in orient(T, r))

def exact_lift():
    z = {}
    for r in V:
        s = signs[int(r[1:])] if r.startswith('q') else (1, 1)
        trees = [structured((s[0], 1-s[1]), 0), structured((1-s[0], s[1]), 1)]
        for a in A:
            z[r, a] = sum(Q(int(a in orient(T, r)), 2) for T in trees)
    x = {e: Q(1) if e == ('t', 'f') else Q(1, 2) for e in E}
    checks = 0
    for r in V:
        for u, v in E:
            if z[r, (u, v)] + z[r, (v, u)] != x[u, v]:
                raise RuntimeError('common edge equality failed')
            checks += 1
        for v in V:
            if sum(z[r, a] for a in A if a[1] == v) != int(v != r):
                raise RuntimeError('outward indegree equality failed')
            if sum(z[r, a[::-1]] for a in A if a[0] == v) != int(v != r):
                raise RuntimeError('transposed inward outdegree equality failed')
            checks += 2
    if sum(x.values()) != len(V)-1: raise RuntimeError('cardinality failed')
    value = sum(Q(cost(r, a)) * z[r, a] for r in V for a in A)
    if value != 10: raise RuntimeError('fractional objective failed')
    return x, z, checks, value

def main():
    x, z, checks, fractional = exact_lift()
    count = 0; best = None; best_B3 = None; histogram = {}
    for indices in combinations(range(len(E)), len(V)-1):
        T = [E[i] for i in indices]
        if orient(T, 't') is None: continue
        count += 1
        F = objective(T); F3 = objective(T, 3)
        if objective(T, shift=1) != F + 56:
            raise RuntimeError('positive shift failed')
        p = sum(e[1] in ['x', 'y'] and e[0] in ['t', 'f'] for e in T)
        q = sum(e[0].startswith('q') for e in T)
        h = int(('t', 'f') in T)
        if p + 2*q != 10 + (1-h) + (q-4):
            raise RuntimeError('B2 structural identity failed')
        best = F if best is None else min(best, F)
        best_B3 = F3 if best_B3 is None else min(best_B3, F3)
        histogram[F] = histogram.get(F, 0) + 1
    if best != 11 or best_B3 != 15: raise RuntimeError('integer minimum failed')
    data = dict(vertices=V, edges=E, root_count=len(V), dense_cost_entries=len(V)*len(A), candidate_B2_threshold=10, candidate_B3_threshold=14, enumerated_trees=count, integer_min_B2=best, integer_min_B3=best_B3, fractional_feasible_objective_B2=str(fractional), full_lift_not_convex_hull_of_integer_points=True, positive_shift=56, constraint_checks=checks, histogram=histogram, witness_x=[dict(edge=e,value=str(x[e])) for e in E], witness_z=[dict(root=r,arc=a,value=str(z[r,a])) for r in V for a in A])
    target = Path(__file__).with_name('LIFT_VALIDATION.json')
    target.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if not k.startswith('witness')}))

if __name__ == '__main__': main()
