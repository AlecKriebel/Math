#!/usr/bin/env python3
"""Finite checks for the authored audit; no dependencies or source-author code.

These checks falsify finite algebra/combinatorial mistakes. They do not replace
the infinite-dimensional C*-algebra proofs in the bound initial REPORT.md.

Revision 1 retains the initial finite algorithms while replacing all 19
optimization-sensitive validations with explicit RuntimeError checks.
Default execution writes only deterministic JSON to stdout.
Execution times are recorded separately by RUN_VALIDATION.py.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import argparse
import json

def require(condition, message):
    """Always evaluate a validation, including under Python -O and -OO."""
    if not condition:
        raise RuntimeError(message)

def zero(n):
    return [[0j for _ in range(n)] for _ in range(n)]

def eye(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = 1
    return a

def unit(n, i, j):
    a = zero(n)
    a[i][j] = 1
    return a

def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]

def scale(c, a):
    return [[c*x for x in r] for r in a]

def mul(a, b):
    n = len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]

def adj(a):
    return [[a[j][i].conjugate() for j in range(len(a))]
            for i in range(len(a))]

def total(xs, n):
    a = zero(n)
    for x in xs:
        a = add(a, x)
    return a

def conj(u, a):
    return mul(mul(u, a), adj(u))

def parity(q, g):
    return (q & g).bit_count() % 2

def equal(a, b):
    # All test entries are Gaussian dyadic rationals, exactly represented.
    return a == b

def orbit_frame_check():
    n = 4
    ident = eye(n)
    p = unit(n, 0, 0)
    ds = []
    for g in range(4):
        d = zero(n)
        for q in range(4):
            d[q][q] = (-1)**parity(q, g)
        ds.append(d)
    hadamard = [[(-1)**parity(i, j)/2 for j in range(4)]
                for i in range(4)]
    ys = []
    for j in range(4):
        y = zero(n)
        for i in range(n):
            y[i][0] = hadamard[i][j]
        ys.append(y)
    require(equal(total([mul(y, adj(y)) for y in ys], n), ident), 'initial nonhomogeneous frame fails to resolve the identity')
    # This is a genuinely nonhomogeneous frame before taking the orbit.
    xs = [scale(0.5, conj(ds[h], y)) for h in range(4) for y in ys]
    require(equal(total([mul(x, adj(x)) for x in xs], n), ident), 'orbit-averaged frame fails to resolve the identity')
    for x in xs:
        require(equal(mul(x, p), x), 'orbit-frame element is outside the right corner Ap')
    checks = 0
    for g in range(4):
        v = total([mul(mul(conj(ds[g], x), p), adj(x)) for x in xs], n)
        require(equal(v, ds[g]), 'lifted unitary differs from the expected diagonal implementer')
        require(equal(mul(v, adj(v)), ident), 'lifted unitary has nonzero right unitary defect')
        require(equal(mul(adj(v), v), ident), 'lifted unitary has nonzero left unitary defect')
        for h in range(4):
            require(equal(conj(ds[h], v), v), 'lifted implementer is not fixed by the entire group')
        for i in range(n):
            for j in range(n):
                a = unit(n, i, j)
                require(equal(conj(v, a), conj(ds[g], a)), 'lifted implementer has incorrect action on a matrix unit')
                checks += 1
    return dict(group="Z2 x Z2", algebra="M4(C)", corner_rank=1,
                initial_frame_size=4, orbit_frame_size=16,
                matrix_unit_implementation_checks=checks,
                all_arithmetic="exact Gaussian dyadic", passed=True)

EDGES = tuple((v, w) for v in range(4) for w in range(4)
              if (v < 2) != (w < 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}

def simple_cycles():
    found = set()
    for start in range(4):
        def visit(path):
            v = path[-1]
            for w in range(4):
                if (v, w) not in EDGE_INDEX:
                    continue
                if w == start:
                    pairs = [(path[i], path[(i+1) % len(path)])
                             for i in range(len(path))]
                    rotations = [tuple(pairs[i:]+pairs[:i])
                                 for i in range(len(pairs))]
                    found.add(min(rotations))
                elif w not in path:
                    visit(path+[w])
        visit([start])
    return tuple(sorted(tuple(EDGE_INDEX[e] for e in c) for c in found))

CYCLES = simple_cycles()
THETA = ((), (EDGE_INDEX[(0, 2)], EDGE_INDEX[(2, 1)]),
         (EDGE_INDEX[(0, 2)],), (EDGE_INDEX[(0, 3)],))

def xor_labels(labels, path):
    q = 0
    for i in path:
        q ^= labels[i]
    return q

def audit_labels(labels):
    t = tuple(xor_labels(labels, path) for path in THETA)
    cycle_labels = tuple(xor_labels(labels, c) for c in CYCLES)
    closed_trivial = all(q == 0 for q in cycle_labels)
    coboundary = all(q == (t[v] ^ t[w])
                     for q, (v, w) in zip(labels, EDGES))
    require(closed_trivial == coboundary, 'closed-cycle labels disagree with the normalized vertex-coboundary criterion')
    kernel = tuple(g for g in range(4)
                   if all(parity(q, g) == 0 for q in cycle_labels))
    beta_labels = tuple(q ^ t[v] ^ t[w]
                        for q, (v, w) in zip(labels, EDGES))
    for k in kernel:
        require(all((parity(q, k) == 0 for q in beta_labels)), 'twisted edge character fails to vanish on the cycle kernel')
    for g in range(4):
        for h in range(4):
            for tv in t:
                require(parity(tv, g ^ h) == parity(tv, g) ^ parity(tv, h), 'normalized vertex coefficient fails the finite group representation law')
    beta_kernel = tuple(g for g in range(4)
                        if all(parity(q, g) == 0 for q in beta_labels))
    require(beta_kernel == kernel, 'ordinary kernel of the twisted edge action differs from the cycle kernel')
    return len(kernel)

def exhaustive_graph_checks():
    edge_hist = Counter()
    for labels in product(range(4), repeat=len(EDGES)):
        edge_hist[audit_labels(labels)] += 1
    source_hist = Counter()
    for source_labels in product(range(4), repeat=4):
        labels = tuple(source_labels[v] for v, w in EDGES)
        source_hist[audit_labels(labels)] += 1
    require(dict(edge_hist) == {4: 64, 2: 5952, 1: 59520}, 'exhaustive edge-label kernel histogram differs from the expected exact count')
    require(dict(source_hist) == {4: 4, 2: 84, 1: 168}, 'exhaustive CK source-label kernel histogram differs from the expected exact count')
    adjacency = [[int((v < 2) != (w < 2)) for w in range(4)]
                 for v in range(4)]
    square = [[sum(adjacency[v][k]*adjacency[k][w] for k in range(4))
               for w in range(4)] for v in range(4)]
    require([[square[v][w] for w in range(2)] for v in range(2)] == [[2, 2], [2, 2]], 'period-two return adjacency differs from the expected primitive matrix')
    return dict(graph="bidirected K2,2", vertices=4, edges=8,
                period=2, simple_directed_cycles=len(CYCLES),
                edge_character_assignments=4**8,
                edge_inner_kernel_order_histogram=dict(edge_hist),
                source_character_assignments=4**4,
                source_inner_kernel_order_histogram=dict(source_hist),
                return_adjacency=[[2,2],[2,2]], passed=True)

def pauli_check():
    x = [[0j, 1+0j], [1+0j, 0j]]
    z = [[1+0j, 0j], [0j, -1+0j]]
    require(equal(mul(x, z), scale(-1, mul(z, x))), 'Pauli matrices fail the expected anticommutation relation')
    require(equal(conj(x, z), scale(-1, z)), 'Pauli conjugation fails to flip the other implementer')
    require(equal(conj(x, conj(z, unit(2, 0, 1))), conj(z, conj(x, unit(2, 0, 1)))), 'Pauli conjugations fail to commute as automorphisms')
    fixed_basis_count = 0
    # Compute fixed subspace within Pauli basis {I,X,Z,XZ}.
    for a in (eye(2), x, z, mul(x,z)):
        if equal(conj(x,a),a) and equal(conj(z,a),a):
            fixed_basis_count += 1
    require(fixed_basis_count == 1, 'Pauli fixed subspace has unexpected dimension')
    return dict(group="Z2 x Z2", algebra="M2(C)",
                fixed_algebra="scalar matrices", XZ_equals_minus_ZX=True,
                not_strongly_approximately_inner=True,
                diagonal_graph_hypothesis=False, passed=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="optional explicitly chosen NEW output file; existing files are refused")
    parser.add_argument("--false-sentinel", action="store_true",
                        help="intentionally fail an explicit check to verify optimization durability")
    args = parser.parse_args()
    if args.false_sentinel:
        require(False, "intentional false sentinel: explicit validation must fail in every optimization mode")
    result = dict(scope="finite falsification checks; not a formal C*-algebra verification",
                  orbit_frame=orbit_frame_check(),
                  exhaustive_graph=exhaustive_graph_checks(),
                  pauli_obstruction=pauli_check())
    result["all_passed"] = True
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        # Exclusive creation is essential: a replay cannot replace any saved seal.
        with args.output.open("x", encoding="utf-8") as output:
            output.write(payload)
    print(payload, end="")

if __name__ == "__main__":
    main()
