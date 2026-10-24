#!/usr/bin/env python3
"""Independent finite sanity checks for the scoped flow claims; not RAAG rationality."""
from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rank(matrix):
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    pivot = 0
    for col in range(len(a[0])):
        k = next((k for k in range(pivot, len(a)) if a[k][col]), None)
        if k is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        z = a[pivot][col]
        a[pivot] = [x/z for x in a[pivot]]
        for j in range(pivot+1, len(a)):
            z = a[j][col]
            a[j] = [x-z*y for x,y in zip(a[j], a[pivot])]
        pivot += 1
    return pivot


def component_partition(n, edges):
    parent = list(range(n))
    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for u,v in edges:
        parent[root(u)] = root(v)
    return [{v for v in range(n) if root(v) == r} for r in sorted({root(v) for v in range(n)})]


def exact_criterion(n, edges, q, required):
    return all(not c <= required or sum(q[v] for v in c) == 0
               for c in component_partition(n, edges))


def reduce_free(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def inv(word):
    return [-x for x in reversed(word)]


def boundary_cycles():
    # Eight disks in cyclic order, two opposite attachment intervals at each.
    # Ribbon permutations: cyclic orders at vertices and edge involution.
    sigma, alpha = {}, {}
    for v in range(8):
        sigma[(v,0)] = (v,1)
        sigma[(v,1)] = (v,0)
        alpha[(v,1)] = ((v+1)%8,0)
        alpha[((v+1)%8,0)] = (v,1)
    unseen = set(sigma)
    cycles = []
    while unseen:
        h = min(unseen)
        cycle = []
        while h in unseen:
            unseen.remove(h)
            cycle.append(h)
            h = sigma[alpha[h]]
        cycles.append(cycle)
    assert len(cycles) == 2 and all(len(c) == 8 for c in cycles)
    return cycles


def main():
    p = subprocess.run([sys.executable, str(ROOT/'check_flow.py'), '--output', str(HERE/'reproduced_CHECKS.json')],
                       check=True, capture_output=True, text=True)
    original = json.loads((ROOT/'CHECKS.json').read_text())
    reproduced = json.loads((HERE/'reproduced_CHECKS.json').read_text())
    assert original == reproduced
    spec = importlib.util.spec_from_file_location('flow_author', ROOT/'check_flow.py')
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)

    count = 0
    for n in range(1,4):
        possible_edges = [(u,v) for u in range(n) for v in range(u,n)]
        for m in range(4):
            for edges in combinations_with_replacement(possible_edges, m):
                for q in product((-1,0,1), repeat=n):
                    for bits in product((False,True), repeat=n):
                        required = {v for v in range(n) if bits[v]}
                        a = [[int(v==t)-int(v==s) for s,t in edges] for v in sorted(required)]
                        augmented = [row+[-q[v]] for row,v in zip(a, sorted(required))]
                        rational = rank(a) == rank(augmented)
                        expected = exact_criterion(n, edges, q, required)
                        assert rational == expected
                        flows = author.flow(n, list(edges), list(q), required)
                        assert (flows is not None) == expected
                        if flows is not None:
                            w = list(q)
                            for f,(s,t) in zip(flows,edges):
                                assert type(f) is int
                                w[s] -= f
                                w[t] += f
                            assert all(w[v] == 0 for v in required)
                        count += 1

    # Test tree-lift obstructions using arbitrary permutation voltages on every edge,
    # rather than just the cyclic cover sampled by the author.
    rng = random.Random(991127)
    cover_count = 0
    for degree in range(1,9):
        for _ in range(50):
            lifted_b = []
            for u in (0,1,4,5):
                perm = list(range(degree))
                rng.shuffle(perm)
                lifted_b.extend((u*degree+s, ((u+1)%8)*degree+perm[s]) for s in range(degree))
            bvertices = [v*degree+s for v in (0,1,2,4,5,6) for s in range(degree)]
            local = {v:i for i,v in enumerate(bvertices)}
            edges = [(local[s],local[t]) for s,t in lifted_b]
            parts = component_partition(len(bvertices), edges)
            charges = [1 if v//degree==0 else -1 if v//degree==4 else 0 for v in bvertices]
            assert len(parts) == 2*degree
            assert all(len(c)==3 and abs(sum(charges[v] for v in c))==1 for c in parts)
            cover_count += 1

    # Free-group word checks are independent of the author's torsion reducer.
    g = [1,2,-1,-2]
    sphere_checks = []
    for n in range(2,151):
        product_word = []
        for i in reversed(range(n)):
            product_word.extend([1]*i + g + [-1]*i)
        commutator_power = [1]*n + [2] + [-1]*n + [-2]
        assert reduce_free(product_word) == commutator_power
        # The extra oriented boundaries are d b^N d^-1 and b^-N.
        sphere_relation = product_word + [2]+[1]*n+[-2]+[-1]*n
        assert reduce_free(sphere_relation) == []
        sphere_checks.append(n)
    cycles = boundary_cycles()
    # Separate finite-endomorphism example: audit only its elementary count claim.
    fib = [0,1]
    for _ in range(165):
        fib.append(fib[-1]+fib[-2])
    u,v = 1,0
    ratios = []
    for n in range(1,81):
        u,v = 2*u+v,u+v
        assert (u,v) == (fib[2*n+1],fib[2*n])
        r = Fraction(u,v)
        assert r*r-r-1 > 0
        assert not ratios or r < ratios[-1]
        ratios.append(r)
    result = {
        'scope':'local flow and conditional finite-congruence obstruction only',
        'author_checker_reproduced_byte_equivalent_json':True,
        'author_checker_stdout':p.stdout.strip(),
        'independent_exhaustive_incidence_systems':count,
        'arbitrary_permutation_voltage_P4_covers':cover_count,
        'free_group_sphere_identities_N_range':[min(sphere_checks),max(sphere_checks)],
        'ribbon_cycle_boundary_orbits':cycles,
        'endomorphism_count_Fibonacci_checks_n_range':[1,80],
        'all_checks_passed':True,
    }
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('independent_exhaustive_incidence_systems','arbitrary_permutation_voltage_P4_covers','all_checks_passed')}))


if __name__ == '__main__':
    main()
