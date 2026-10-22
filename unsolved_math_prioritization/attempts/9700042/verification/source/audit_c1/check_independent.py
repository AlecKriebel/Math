#!/usr/bin/env python3
"""Fresh diagnostics; does not import the author's checker or prove a limit."""
from collections import deque, defaultdict, Counter
from fractions import Fraction
from heapq import heappush, heappop
from itertools import product
from math import comb, sqrt, log, exp, e
from pathlib import Path
from random import Random
import hashlib
import json


def primal_edges(n):
    return [((x, y), (x+dx, y+dy)) for x in range(n) for y in range(n)
            for dx, dy in ((1, 0), (0, 1)) if x+dx < n and y+dy < n]


def maxflow(n, capacities):
    """Edmonds--Karp on full primal, including all irrelevant boundary edges."""
    source, sink = n*n, n*n+1
    residual = [defaultdict(int) for _ in range(n*n+2)]
    def add(u, v, c):
        residual[u][v] += c
        residual[v][u] += 0
    def ident(v):
        return v[0]*n+v[1]
    for (u, v), c in capacities.items():
        add(ident(u), ident(v), c)
    inf = 1+sum(capacities.values())
    for x, y in product(range(n), repeat=2):
        if (x == 0 or y == 0) and x < n-1 and y < n-1:
            add(source, ident((x, y)), inf)
        if x == n-1 or y == n-1:
            add(ident((x, y)), sink, inf)
    total = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, c in residual[u].items():
                if c and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            return total
        amount, v = inf, sink
        while v != source:
            u = parent[v]
            amount = min(amount, residual[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= amount
            residual[v][u] += amount
            v = u
        total += amount


def dual(n, capacities, monotone=False):
    """Uses unreflected physical face coordinates: east/south are costly."""
    width = n-1
    start, target = (0, n-2), (n-2, 0)
    adjacency = defaultdict(list)
    for x, y in product(range(width), repeat=2):
        u = (x, y)
        if x+1 < width:
            v, edge = (x+1, y), ((x+1, y), (x+1, y+1))
            adjacency[u].append((v, capacities[edge], edge, True))
            if not monotone:
                adjacency[v].append((u, 0, edge, False))
        if y > 0:
            v, edge = (x, y-1), ((x, y), (x+1, y))
            adjacency[u].append((v, capacities[edge], edge, True))
            if not monotone:
                adjacency[v].append((u, 0, edge, False))
    distance, parent = {start: 0}, {}
    heap = [(0, start)]
    while heap:
        d, u = heappop(heap)
        if d != distance[u]:
            continue
        for v, cost, edge, forward in adjacency[u]:
            if d+cost < distance.get(v, float('inf')):
                distance[v] = d+cost
                parent[v] = (u, edge, forward)
                heappush(heap, (d+cost, v))
    v, path = target, []
    while v != start:
        u, edge, forward = parent[v]
        path.append((u, v, edge, forward))
        v = u
    path.reverse()
    forced = (((0, n-2), (0, n-1)), ((n-2, 0), (n-1, 0)))
    return sum(capacities[a] for a in forced)+distance[target], path


def coordinate_count(N, k):
    counts = {(0, 0): 1}
    for _ in range(k):
        new = defaultdict(int)
        for (last, used), multiplicity in counts.items():
            for nxt in range(N+1):
                used2 = used+max(last-nxt, 0)
                if used2 <= k:
                    new[nxt, used2] += multiplicity
        counts = new
    return sum(counts.values())  # Final increment to N has no negative part.


def coordinate_bound(N, k):
    return sum(comb(k+1, t)*comb(k, t)*comb(N+2*k-t, k-t)
               for t in range(k+1))


def main():
    output = {'diagnostic_only': True, 'seed': 9379700042}
    exact = []
    for n in (2, 3):
        edges = primal_edges(n)
        for mask in range(1 << len(edges)):
            capacities = {a: (mask >> i) & 1 for i, a in enumerate(edges)}
            assert maxflow(n, capacities) == dual(n, capacities)[0]
        exact.append({'n': n, 'all_primal_edges': len(edges), 'configurations': 1 << len(edges)})
    output['full_primal_exhaustive'] = exact
    rng = Random(output['seed'])
    random_tests = []
    for n, trials in ((4, 300), (5, 300), (8, 200), (15, 100), (30, 50)):
        edges = primal_edges(n)
        for j in range(trials):
            if j % 2:
                q = (.001, .01, .1, .5, .9)[(j//2) % 5]
                capacities = {a: int(rng.random() >= q) for a in edges}
            else:
                capacities = {a: rng.randrange(5) for a in edges}
            value, path = dual(n, capacities)
            assert value == maxflow(n, capacities)
            if j % 2:
                N = n-2
                backward = sum(not a[3] for a in path)
                forward = len(path)-backward
                assert forward == 2*N+backward
                marks = [a[0] for a in path if a[3] and capacities[a[2]] == 0]
                # In physical coordinates, east and south are the forward steps.
                sequence = [(0, 0)]+[(x, N-y) for x, y in marks]+[(N, N)]
                for i in (0, 1):
                    variation = sum(max(u[i]-v[i], 0) for u, v in zip(sequence, sequence[1:]))
                    assert variation <= backward
        random_tests.append({'n': n, 'trials': trials, 'capacities': 'alternating Bernoulli and uniform integer 0..4'})
    output['independent_flow_tests'] = random_tests

    coordinate_results = []
    for N in range(1, 13):
        for k in range(1, 19):
            actual = coordinate_count(N, k)
            bound = coordinate_bound(N, k)
            smooth = comb(N+2*k, k)*(1+sqrt(k/(N+2*k)))**(2*k+1)
            assert actual <= bound <= smooth*(1+1e-12)
            coordinate_results.append((N, k, actual, bound))
    output['coordinate_dynamic_program'] = {'cases': len(coordinate_results), 'N': [1, 12], 'k': [1, 18], 'all_passed': True}

    # For N=2, enumerate all interior dual Bernoulli configurations. Forced
    # edges are open, since D_N and its probability do not use their states.
    n, N = 4, 2
    edges = primal_edges(n)
    relevant = [a for a in edges if
                (a[0][0] == a[1][0] and 0 < a[0][0] < n-1) or
                (a[0][1] == a[1][1] and 0 < a[0][1] < n-1)]
    histogram = Counter()
    witness = None
    for mask in range(1 << len(relevant)):
        capacities = dict.fromkeys(edges, 1)
        closed = []
        for i, a in enumerate(relevant):
            if (mask >> i) & 1:
                capacities[a] = 0
                closed.append(a)
        flow, path = dual(n, capacities)
        deficit = 2*n-2-flow
        histogram[len(closed), deficit] += 1
        monotone_flow = dual(n, capacities, True)[0]
        if flow < monotone_flow and (witness is None or len(closed) < len(witness['closed_edges'])):
            witness = {'closed_edges': closed, 'flow': flow, 'monotone_flow': monotone_flow, 'unreflected_dual_path': path}
    assert len(relevant) == 12
    output['nonmonotone_witness'] = witness
    probability_tests = []
    for denominator in (1000, 1000000):
        q = Fraction(1, denominator)
        for d in range(1, 2*N+1):
            probability = sum(m*q**j*(1-q)**(len(relevant)-j)
                              for (j, deficit), m in histogram.items() if deficit >= d)
            bound = sum((2*q)**k * coordinate_bound(N, k)**2
                        for k in range(d, (N+1)**2))
            assert probability <= bound
            probability_tests.append({'q': str(q), 'd': d, 'actual': float(probability), 'finite_list_bound': float(bound)})
    output['finite_probability_checks'] = probability_tests

    # Diagnose numerical bookkeeping of the two displayed geometric bounds.
    inequalities = 0
    for eta in (.01, .1, .4):
        for epsilon in (.02, .3):
            q = 1e-12
            a = e*sqrt(2*q)*(1+2*eta)*(1+sqrt(eta))**2*(1+epsilon)
            theta = 32*e*e*q*(1/eta+2)**2
            assert a < eta and theta < 1
            for N in (100, 10000):
                for k in sorted(set([1, max(1, int(a*N)+1), max(1, int(eta*N)), int(eta*N)+1, N, 3*N])):
                    if k < a*N:
                        continue
                    logterm = k*log(2*q)+2*log(comb(N+2*k, k))+(4*k+2)*log(1+sqrt(k/(N+2*k)))
                    if k <= eta*N:
                        logbound = 2*log(1+sqrt(eta))-2*k*log(1+epsilon)
                    else:
                        logbound = log(4)+k*log(theta)
                    assert logterm <= logbound+1e-8
                    inequalities += 1
    output['two_range_inequality_samples'] = inequalities
    output['all_assertions_passed'] = True
    destination = Path(__file__).with_name('INDEPENDENT_CHECKS.json')
    destination.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
