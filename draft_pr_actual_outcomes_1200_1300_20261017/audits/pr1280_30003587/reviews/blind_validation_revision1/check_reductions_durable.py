"""Finite falsification checks for the authored reductions; not a C*-algebra proof.

All arithmetic is exact. Run from this file's directory with Python 3.
"""

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def validator_selftest():
    caught = False
    try:
        require(False, 'durable-validation-sentinel')
    except RuntimeError as e:
        caught = str(e) == 'durable-validation-sentinel'
    require(caught, 'Explicit validation sentinel disabled')
from collections import deque
from itertools import product
from math import gcd, lcm
from pathlib import Path
import datetime
import json
import random

def add(a, b, orders):
    return tuple(((x + y) % m for x, y, m in zip(a, b, orders)))

def val(c, g, orders):
    den = lcm(*orders)
    return sum((x * y * (den // m) for x, y, m in zip(c, g, orders))) % den

def root_paths(n, edges):
    paths = {0: ()}
    queue = deque([0])
    while queue:
        v = queue.popleft()
        for i, (s, t) in enumerate(edges):
            if s == v and t not in paths:
                paths[t] = paths[v] + (i,)
                queue.append(t)
    return paths

def simple_cycles(n, edges):
    out = [[] for _ in range(n)]
    for i, (s, t) in enumerate(edges):
        out[s].append((i, t))
    result = []
    for start in range(n):

        def visit(v, seen, path):
            for i, t in out[v]:
                if t == start:
                    result.append(path + (i,))
                elif t not in seen:
                    visit(t, seen | {t}, path + (i,))
        visit(start, {start}, ())
    return result

def path_char(path, labels, orders):
    c = (0,) * len(orders)
    for e in path:
        c = add(c, labels[e], orders)
    return c

def potentials(n, edges, labels, orders, g):
    den = lcm(*orders)
    paths = root_paths(n, edges)
    f = [-val(path_char(paths[v], labels, orders), g, orders) % den for v in range(n)]
    if all((val(labels[i], g, orders) == (f[s] - f[t]) % den for i, (s, t) in enumerate(edges))):
        return f
    return None

def strongly_connected(n, edges):
    for start in range(n):
        seen = {start}
        while True:
            new = seen | {t for s, t in edges if s in seen}
            if new == seen:
                break
            seen = new
        if len(seen) != n:
            return False
    return True

def return_graph(n, edges, labels, orders, d):
    distances = {0: 0}
    queue = deque([0])
    while queue:
        v = queue.popleft()
        for s, t in edges:
            if s == v and t not in distances:
                distances[t] = distances[v] + 1
                queue.append(t)
    cls0 = sorted((v for v in range(n) if distances[v] % d == 0))
    renumber = {v: i for i, v in enumerate(cls0)}
    out_edges, out_labels = ([], [])
    for start in cls0:
        stack = [(start, ())]
        for _ in range(d):
            stack = [(t, path + (i,)) for v, path in stack for i, (s, t) in enumerate(edges) if s == v]
        for end, path in stack:
            require(end in renumber, 'Original condition at line100 failed')
            out_edges.append((renumber[start], renumber[end]))
            out_labels.append(path_char(path, labels, orders))
    return (len(cls0), out_edges, out_labels)

def check(n, edges, labels, orders):
    elements = list(product(*(range(m) for m in orders)))
    den = lcm(*orders)
    cycles = simple_cycles(n, edges)
    require(cycles, 'Original condition at line110 failed')
    d = 0
    for path in cycles:
        d = gcd(d, len(path))
    h_cycle = {g for g in elements if all((val(path_char(path, labels, orders), g, orders) == 0 for path in cycles))}
    h_potential = {g for g in elements if potentials(n, edges, labels, orders, g) is not None}
    require(h_cycle == h_potential, 'Original condition at line119 failed')
    h = h_cycle
    require(all((add(g, k, orders) in h for g in h for k in h)), 'Original condition at line121 failed')
    f_h = {g: potentials(n, edges, labels, orders, g) for g in h}
    ext = []
    for v in range(n):
        candidates = [c for c in elements if all((val(c, g, orders) == f_h[g][v] for g in h))]
        require(candidates, 'Original condition at line130 failed')
        ext.append(candidates[0])
    beta = [tuple(((c - a + b) % m for c, a, b, m in zip(labels[i], ext[s], ext[t], orders))) for i, (s, t) in enumerate(edges)]
    require(all((val(c, h0, orders) == 0 for h0 in h for c in beta)), 'Original condition at line135 failed')
    require({g for g in elements if potentials(n, edges, beta, orders, g) is not None} == h, 'Original condition at line136 failed')
    rn, re, rl = return_graph(n, edges, beta, orders, d)
    require(strongly_connected(rn, re), 'Original condition at line140 failed')
    rd = 0
    for path in simple_cycles(rn, re):
        rd = gcd(rd, len(path))
    require(rd == 1, 'Original condition at line144 failed')
    require({g for g in elements if potentials(rn, re, rl, orders, g) is not None} == h, 'Original condition at line145 failed')
    return {'vertices': n, 'edges': len(edges), 'orders': orders, 'period': d, 'inner_subgroup_size': len(h), 'return_vertices': rn, 'return_edges': len(re)}

def main():
    validator_selftest()
    seed = 3587
    rng = random.Random(seed)
    cases = []
    cases.append(check(2, [(0, 1), (0, 1), (1, 0), (1, 0)], [(1,)] * 4, (4,)))
    require(cases[0]['inner_subgroup_size'] == 2, 'Original condition at line160 failed')
    require(cases[0]['period'] == 2, 'Original condition at line161 failed')
    cases.append(check(3, [(0, 1), (0, 1), (1, 2), (2, 0), (2, 0)], [(1, 0), (0, 1), (1, 1), (0, 0), (1, 0)], (2, 2)))
    cases.append(check(2, [(0, 1), (0, 1), (1, 0), (1, 0)], [(1,), (1,), (3,), (3,)], (4,)))
    cases.append(check(2, [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0)] * 4, (2, 4)))
    for k in range(180):
        n = rng.randrange(2, 5)
        edges = [(s, t) for s in range(n) for t in range(n) if rng.random() < 0.45]
        if not strongly_connected(n, edges):
            continue
        orders = [(4,), (2, 2), (2, 4)][k % 3]
        labels = [tuple((rng.randrange(m) for m in orders)) for _ in edges]
        cases.append(check(n, edges, labels, orders))
    result = {'status': 'PASS', 'seed': seed, 'cases_checked': len(cases), 'scope': 'Exact finite graph and character checks; not analytic C*-algebra verification.', 'cases': cases}
    print(json.dumps(result, indent=2, sort_keys=True))
if __name__ == '__main__':
    main()
