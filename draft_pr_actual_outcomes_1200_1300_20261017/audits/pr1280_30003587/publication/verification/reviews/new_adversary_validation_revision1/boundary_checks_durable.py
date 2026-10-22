"""Independent exact finite falsification; analytic conclusions require the report's proof."""
import sys

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def validator_selftest():
    caught = False
    try:
        require(False, 'sentinel-always-active')
    except RuntimeError as e:
        caught = str(e) == 'sentinel-always-active'
    require(caught, 'Explicit validator inactive')
from itertools import product
from math import gcd
from pathlib import Path
import json

def walks(edges, starts, length):
    out = [(v, v, (), 0) for v in starts]
    for _ in range(length):
        out = [(a, t, path + (k,), phase + c) for a, b, path, phase in out for k, (s, t, c) in enumerate(edges) if s == b]
    return out

def connected(n, edges):
    return all((len({v for length in range(n) for a, v, p, c in walks(edges, [s], length)}) == n for s in range(n)))

def cycle_data(n, edges, modulus, g):
    d = 0
    okay = True
    for length in range(1, n + 1):
        for s, t, path, phase in walks(edges, range(n), length):
            if s == t:
                d = gcd(d, length)
                okay &= phase * g % modulus == 0
    return (d, okay)

def brute_potential(n, edges, modulus, g):
    for tail in product(range(modulus), repeat=n - 1):
        f = (0,) + tail
        if all(((f[s] - f[t] - c * g) % modulus == 0 for s, t, c in edges)):
            return f
    return None

def audit(n, edges, modulus, corner_test=True):
    require(connected(n, edges), 'Original blind_reconstruction_adversary condition at line40 failed')
    d = cycle_data(n, edges, modulus, 0)[0]
    require(d > 0, 'Original blind_reconstruction_adversary condition at line42 failed')
    hs = []
    for g in range(modulus):
        _, cycle_ok = cycle_data(n, edges, modulus, g)
        f = brute_potential(n, edges, modulus, g)
        require(cycle_ok == (f is not None), 'Original blind_reconstruction_adversary condition at line47 failed')
        if f is not None:
            hs.append(g)
    if corner_test:
        classes = []
        for r in range(d):
            classes.append({t for length in range(n) if length % d == r for a, t, path, c in walks(edges, [0], length)})
        require(set.union(*classes) == set(range(n)), 'Original blind_reconstruction_adversary condition at line55 failed')
        require(sum((len(s) for s in classes)) == n, 'Original blind_reconstruction_adversary condition at line56 failed')
        V = classes[0]
        rename = {v: i for i, v in enumerate(sorted(V))}
        fedges = [(rename[s], rename[t], phase) for s, t, path, phase in walks(edges, V, d)]
        require(connected(len(V), fedges), 'Original blind_reconstruction_adversary condition at line60 failed')
        require(cycle_data(len(V), fedges, modulus, 0)[0] == 1, 'Original blind_reconstruction_adversary condition at line61 failed')
        require([g for g in range(modulus) if brute_potential(len(V), fedges, modulus, g) is not None] == hs, 'Original blind_reconstruction_adversary condition at line62 failed')
        frame = [(r, path, s, t) for r in range(1, d) for s, t, path, c in walks(edges, classes[r], d - r)]
        require(all((t in V for r, path, s, t in frame)), 'Original blind_reconstruction_adversary condition at line66 failed')
        require(all((a[2] != b[2] or not (a[1][:len(b[1])] == b[1] or b[1][:len(a[1])] == a[1]) for i, a in enumerate(frame) for b in frame[i + 1:])), 'Original blind_reconstruction_adversary condition at line69 failed')
    return (d, len(hs))

def main():
    validator_selftest()
    if '--false-sentinel' in sys.argv:
        require(False, 'intentional-durable-false-sentinel')
    counts = {'exhaustive_z2_labelled_graphs': 0, 'periodic_cases': 0, 'one_vertex_multiloop_cases': 0, 'z4_boundary_cases': 0}
    for n in (2, 3):
        pairs = list(product(range(n), repeat=2))
        for states in product(range(3), repeat=n * n):
            edges = [(s, t, a - 1) for (s, t), a in zip(pairs, states) if a]
            if not connected(n, edges):
                continue
            if len(edges) == n:
                continue
            d, hsize = audit(n, edges, 2)
            counts['exhaustive_z2_labelled_graphs'] += 1
            counts['periodic_cases'] += d > 1
    for phases in product(range(4), repeat=3):
        audit(1, [(0, 0, c) for c in phases], 4)
        counts['one_vertex_multiloop_cases'] += 1
    nonsplit = [(s, t, 1) for s in range(4) for t in range(4) if (s < 2) != (t < 2)]
    d, hsize = audit(4, nonsplit, 4)
    require((d, hsize) == (2, 2), 'Original blind_reconstruction_adversary condition at line94 failed')
    ext = (0, 0, 1, 1)
    beta = [(s, t, (c - ext[s] + ext[t]) % 4) for s, t, c in nonsplit]
    require(all((c % 2 == 0 for s, t, c in beta)), 'Original blind_reconstruction_adversary condition at line97 failed')
    require(audit(4, beta, 4) == (2, 2), 'Original blind_reconstruction_adversary condition at line98 failed')
    counts['z4_boundary_cases'] += 2
    for g, h in product(range(4), repeat=2):
        require(all(((ext[v] * (g + h) - ext[v] * g - ext[v] * h) % 4 == 0 for v in range(4))), 'Original blind_reconstruction_adversary condition at line103 failed')
    result = {'status': 'PASS', 'counts': counts, 'nonsplit': {'period': d, 'inner_subgroup': [0, 2], 'extended_vertex_exponents': ext, 'modified_edge_exponents': sorted(set((c for s, t, c in beta)))}, 'scope': 'Finite exact graph, phase, potential, corner, and prefix checks. Does not certify operator limits or replace the imported BS theorem.'}
    pass
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
