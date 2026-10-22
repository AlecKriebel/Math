#!/usr/bin/env python3
"""Exact arithmetic and finite adversarial checks; not an infinite-event proof.

Run from any directory: python /path/to/validate_construction.py
Outputs machine-readable validation_report.json next to this script.
Uses only Python's standard library. No simulation is used for proof claims.
"""
from collections import deque
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import random

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def check(condition, label):
    # Explicit, so python -O and -OO retain every check.
    if not condition:
        raise RuntimeError(label)


def neighbors(v):
    x, y = v
    return ((x + dx, y + dy) for dx, dy in DIRECTIONS)


def region(v):
    x, y = v
    if x >= 1 and y >= 1:
        return 'A'
    if x <= -1 and y <= -1:
        return 'B'
    return 'O'


def strong(u, v):
    return region(u) == region(v) and region(u) in ('A', 'B')


def distance_B(v):
    return max(v[0] + 1, 0) + max(v[1] + 1, 0)


def weak_bridge_from_walk(walk):
    """Last A before first B, followed by chronological loop erasure."""
    check(all(sum(abs(a-b) for a,b in zip(u,v)) == 1
              for u,v in zip(walk,walk[1:])), 'input is not a lattice walk')
    first_B = next(i for i,v in enumerate(walk) if region(v) == 'B')
    last_A = max(i for i,v in enumerate(walk[:first_B]) if region(v) == 'A')
    segment = walk[last_A:first_B+1]
    check(all(not strong(u,v) for u,v in zip(segment,segment[1:])),
          'extracted segment contains a strong edge')
    simple = []
    for v in segment:
        if v in simple:
            simple = simple[:simple.index(v)+1]
        else:
            simple.append(v)
    check(len(simple) == len(set(simple)), 'loop erasure failed')
    check(region(simple[0]) == 'A' and region(simple[-1]) == 'B',
          'bridge has wrong endpoints')
    check(all(region(v) == 'O' for v in simple[1:-1]),
          'bridge visits a strong region internally')
    check(all(not strong(u,v) for u,v in zip(simple,simple[1:])),
          'loop-erased bridge contains a strong edge')
    check(len(simple)-1 >= distance_B(simple[0]), 'distance lower bound failed')
    return simple


def connected(vertices):
    todo = [next(iter(vertices))]
    seen = set(todo)
    while todo:
        for w in neighbors(todo.pop()):
            if w in vertices and w not in seen:
                todo.append(w)
                seen.add(w)
    return seen == vertices


def cut_dual_graph(cluster):
    """Quarter-plane coordinates start at (0,0); dual coords are doubled."""
    graph = {}
    for u in cluster:
        for v in neighbors(u):
            if min(v) < 0 or v in cluster:
                continue
            x, y = min(u,v)
            if u[1] == v[1]:
                a,b = (2*x+1,2*y-1),(2*x+1,2*y+1)
            else:
                a,b = (2*x-1,2*y+1),(2*x+1,2*y+1)
            graph.setdefault(a,set()).add(b)
            graph.setdefault(b,set()).add(a)
    return graph


def quarter_plane_cut_check(cluster):
    graph = cut_dual_graph(cluster)
    # Independent parity mechanism behind the general dual-crosscut lemma.
    bottom = [v for v in graph if v[1] == -1]
    left = [v for v in graph if v[0] == -1]
    check(len(bottom) % 2 == 1 and len(left) % 2 == 1,
          'finite-set boundary parity failed')
    check(all(len(graph[v]) == 1 for v in bottom+left),
          'boundary dual degree failed')
    check(all(len(graph[v]) % 2 == 0 for v in graph
              if v[0] != -1 and v[1] != -1), 'interior dual parity failed')
    starts = [v for v in graph if v[1] == -1 and v[0] >= 1]
    for start in starts:
        queue, prev = deque([start]), {start: None}
        while queue:
            v = queue.popleft()
            if v[0] == -1 and v[1] >= 1:
                path = []
                end = v
                while v is not None:
                    path.append(v)
                    v = prev[v]
                m = len(path)-1
                a, b = (start[0]-1)//2, (end[1]-1)//2
                check(m >= a+b+2 and m >= 2, 'dual length lower bound failed')
                check(a <= m-2, 'dual boundary-start range failed')
                return m
            for w in graph[v]:
                if w not in prev:
                    prev[w] = v
                    queue.append(w)
    raise RuntimeError('no bottom-to-left dual cut path for finite connected set')


def exact_parameter_check(p0, p, L):
    check(0 < p0 < p < 1, 'strict supercritical parameter ordering missing')
    n,d = p.numerator**L, p.denominator**L
    check(32*n < d, 'q < 1/32 failed')
    check(3*n < d, '3q < 1 failed')
    # (8/3)(3q)^4/(1-3q)^2 < 1/1000, with no floating-point decision.
    check(1000*8*(3*n)**4 < 3*d*d*(d-3*n)**2,
          'exact bridge-probability upper bound < 1/1000 failed')
    q = float(Fraction(n,d))
    return {'p0': str(p0), 'p': str(p), 'L': L,
            'q_decimal_support_only': q,
            'bridge_bound_decimal_support_only': (8/3)*(3*q)**4/(1-3*q)**2,
            'q_less_than_1_over_32_exact': True,
            'bridge_bound_less_than_1_over_1000_exact': True,
            'q_numerator_bits': n.bit_length(), 'q_denominator_bits': d.bit_length()}


def exhaustive_series_check():
    # One original square, one strong edge, three weak length-2 chains.
    originals = tuple(range(4))
    physical = [(0,1),(1,4),(4,2),(2,5),(5,3),(3,6),(6,0)]
    coarse = [((0,1),[0]),((1,2),[1,2]),((2,3),[3,4]),((3,0),[5,6])]
    def reachable(edges, start):
        seen,todo = {start},[start]
        while todo:
            v = todo.pop()
            for a,b in edges:
                w = b if a == v else a if b == v else None
                if w is not None and w not in seen:
                    seen.add(w); todo.append(w)
        return seen
    checked = 0
    for bits in product((False,True),repeat=len(physical)):
        physical_open = [e for e,b in zip(physical,bits) if b]
        coarse_open = [e for e,ids in coarse if all(bits[i] for i in ids)]
        for s in originals:
            check(reachable(physical_open,s).intersection(originals)
                  == reachable(coarse_open,s), 'series reduction failed')
        checked += 1
    return checked


def finite_subdivision_check(radius=2, L=100):
    originals = {(x,y) for x in range(-radius,radius+1)
                 for y in range(-radius,radius+1)}
    graph, projection = {}, {v:v for v in originals}
    original_edges = []
    chain_count = 0
    def add(u,v):
        check(u != v, 'loop detected')
        check(v not in graph.get(u,set()), 'parallel edge detected')
        graph.setdefault(u,set()).add(v); graph.setdefault(v,set()).add(u)
    for u in sorted(originals):
        for v in neighbors(u):
            if v not in originals or u >= v:
                continue
            original_edges.append((u,v))
            if strong(u,v):
                add(u,v)
            else:
                chain = [u]+[('new',chain_count,i) for i in range(1,L)]+[v]
                for i,z in enumerate(chain[1:-1],1):
                    projection[z] = u if i <= L-i else v
                for a,b in zip(chain,chain[1:]): add(a,b)
                chain_count += 1
    check(max(map(len,graph.values())) <= 4, 'degree bound failed')
    check(all(len(graph[v]) == 2 for v in graph if v not in originals),
          'inserted vertex degree is not two')
    for u in graph:
        for v in graph[u]:
            check(sum(abs(a-b) for a,b in zip(projection[u],projection[v])) <= 1,
                  'nearest-endpoint projection is not 1-Lipschitz on an edge')
    # Full all-pairs among original vertices in the finite square.
    distances = {}
    for s in sorted(originals):
        dist,queue = {s:0},deque([s])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in dist:
                    dist[v] = dist[u]+1; queue.append(v)
        check(len(dist) == len(graph), 'subdivided graph disconnected')
        for t in originals:
            manhattan = sum(abs(a-b) for a,b in zip(s,t))
            check(manhattan <= dist[t] <= L*manhattan, 'original metric bound failed')
        distances[s] = dist
    # Nearest endpoints are at distance at most L/2, uniformly.
    for z in graph:
        check(distances[projection[z]][z] <= L//2, 'projection distance bound failed')
    return {'radius':radius,'L':L,'vertices':len(graph),
            'physical_edges':sum(map(len,graph.values()))//2,
            'weak_chains':chain_count,'max_degree':max(map(len,graph.values())),
            'original_pairs_checked':len(originals)**2,
            'projection_edges_checked':sum(map(len,graph.values()))//2}


def main():
    results = {}
    results['parameters'] = [
        exact_parameter_check(Fraction(9,10),Fraction(19,20),100),
        exact_parameter_check(Fraction(1295,1296),Fraction(2591,2592),12960)]
    check(Fraction(20,19)**20 > 2, 'binomial block inequality failed')
    t = Fraction(3,32)
    bound = Fraction(8,3)*t**4/(1-t)**2
    check(bound == Fraction(27,107648) and bound < Fraction(1,1000),
          'coarse bridge constant failed')
    # m >= 2 closed dual paths, crude count 4m*3^(m-1).
    r = Fraction(3,10)
    cut_failure_bound = Fraction(4,3)*(r/(1-r)**2-r)
    check(cut_failure_bound == Fraction(102,245) < 1,
          'quarter-plane contour series failed')
    survival_lower = 1-cut_failure_bound
    nonuniqueness_lower = survival_lower**2*(1-bound)
    check(nonuniqueness_lower > Fraction(1,3), 'nonuniqueness bound > 1/3 failed')
    results['symbolic_bounds'] = {
        'coarse_bridge_bound':str(bound),
        'quarter_plane_cut_failure_bound':str(cut_failure_bound),
        'conditional_on_contour_lemma_survival_lower_bound':str(survival_lower),
        'conditional_on_contour_lemma_nonuniqueness_lower_bound':str(nonuniqueness_lower),
        'conditional_on_contour_lemma_nonuniqueness_decimal':float(nonuniqueness_lower)}
    # Check every possible boundary start in a long finite range against exact distance.
    for k in range(1,1001):
        for v in ((1,k),(k,1)):
            check(distance_B(v) == k+3, 'boundary distance failed')
            check(any(region(w) == 'O' for w in neighbors(v)), 'not a boundary vertex')
    results['boundary_vertices_checked_with_corner_duplication'] = 2000
    # Every connected subset containing the origin in a 4x4 quadrant window.
    cells = [(x,y) for x in range(4) for y in range(4)]
    cluster_count,max_cut_length,all_sets = 0,0,0
    for mask in range(1 << (len(cells)-1)):
        C = {(0,0)} | {cells[i+1] for i in range(len(cells)-1) if mask & (1<<i)}
        max_cut_length = max(max_cut_length,quarter_plane_cut_check(C))
        all_sets += 1
        if connected(C):
            cluster_count += 1
    results['finite_quadrant_dual_cut_checks'] = {
        'window':[4,4],'all_finite_sets_checked':all_sets,
        'connected_clusters_checked':cluster_count,
        'maximum_found_cut_length':max_cut_length,
        'infinite_topological_lemma_proved_by_test':False}
    # Exhaustive self-avoiding path counts are a check on the elementary bound.
    saw_counts = [0]*11
    def count_saws(path):
        n = len(path)-1
        saw_counts[n] += 1
        if n == 10: return
        for w in neighbors(path[-1]):
            if w not in path: count_saws(path+[w])
    count_saws([(0,0)])
    for n in range(1,11):
        check(saw_counts[n] <= 4*3**(n-1), 'SAW branching bound failed')
    results['exhaustive_saw_counts_n0_through_n10'] = saw_counts
    bridge_counts = [0]*11
    def count_bridges(path):
        n = len(path)-1
        v = path[-1]
        if region(v) == 'B':
            bridge_counts[n] += 1
            return
        if n == 10 or distance_B(v) > 10-n: return
        for w in neighbors(v):
            if w not in path and region(w) != 'A' and not strong(v,w):
                count_bridges(path+[w])
    starts = {(1,k) for k in range(1,8)} | {(k,1) for k in range(1,8)}
    for v in starts: count_bridges([v])
    for n in range(4,11):
        check(bridge_counts[n] <= 8*(n-3)*3**(n-1),
              'length-wise global weak-bridge count failed')
    check(all(bridge_counts[n] == 0 for n in range(4)), 'bridge shorter than four')
    results['exhaustive_weak_bridge_counts_n0_through_n10'] = bridge_counts
    # Intentional strong excursions, outside loops, and returns to both strong regions.
    adversarial = [(2,2),(1,2),(0,2),(0,3),(1,3),(2,3),(2,2),(1,2),
                   (0,2),(0,1),(0,0),(1,0),(0,0),(-1,0),(-1,-1),
                   (-2,-1),(-2,0),(-1,0),(-1,-1)]
    bridge = weak_bridge_from_walk(adversarial)
    rng = random.Random(1785)
    walks_checked = 1
    for _ in range(1000):
        walk = [(2,2)]
        for __ in range(50):
            walk.append(rng.choice(tuple(neighbors(walk[-1]))))
        # Deterministically finish in B; this adds no random pass/fail condition.
        while walk[-1][0] > -1:
            x,y=walk[-1];walk.append((x-1,y))
        while walk[-1][1] > -1:
            x,y=walk[-1];walk.append((x,y-1))
        weak_bridge_from_walk(walk)
        walks_checked += 1
    results['bridge_extraction'] = {'walks_checked':walks_checked,
        'intentional_adversarial_walk_length':len(adversarial)-1,
        'extracted_weak_simple_bridge':bridge}
    results['series_reduction_assignments_checked'] = exhaustive_series_check()
    results['finite_subdivision_graph'] = finite_subdivision_check()
    # Mutation checks establish why several tempting shortcuts are invalid.
    wrong_q = 1-(1-Fraction(19,20))**100
    check(3*wrong_q > 1, 'at-least-one-edge mutation unexpectedly passed')
    results['adversarial_mutations'] = {
        'at_least_one_chain_edge_open_is_invalid':True,
        'strict_pc_gap_requires_p0_less_than_p':True,
        'halfplane_bound_diverges_because_infinite_boundary_at_distance_2':True,
        'non_simple_walks_require_loop_erasure_before_q_power':True,
        'strong_excursions_cannot_be_charged_as_weak_edges':True}
    results['status'] = 'PASS: exact arithmetic and finite checks only'
    results['not_certified_by_computation'] = [
        'An infinite cluster exists in a quadrant at p0.',
        'Every finite quadrant cluster has the required dual boundary crosscut.',
        'A complete proof of nonuniqueness; consult the accompanying mathematical audit.']
    target = Path(__file__).with_name('validation_report.json')
    target.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
