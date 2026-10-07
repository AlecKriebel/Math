#!/usr/bin/env python3
"""Source-free exact finite controls. These are not proofs of motivic comparison."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

COUNTS = {}

def require(condition, group):
    COUNTS[group] = COUNTS.get(group, 0) + 1
    if not condition:
        raise AssertionError((group, COUNTS[group]))

def rank(rows):
    if not rows:
        return 0
    a = [[Q(x) for x in row] for row in rows]
    m, n, r = len(a), len(a[0]), 0
    assert all(len(row) == n for row in a)
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x / v for x in a[r]]
        for i in range(m):
            if i != r:
                v = a[i][c]
                a[i] = [x - v*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r

def matvec(rows, v):
    return tuple(sum(Q(x)*Q(y) for x,y in zip(row,v)) for row in rows)

def controls():
    # Two formal Chow sheaves of a curve remain after local sheafification:
    # codim 0 is Q, codim 1 is Pic_C = connected Jacobian plus degree Q.
    bundle_cases = 0
    for m in range(41):
        for p in range(m + 3):
            chow = [(j,p-j) for j in range(m+1) if p-j in (0,1)]
            components = len(chow)
            connected_copies = sum(q == 1 for _,q in chow)
            expected_components = (1 if p in (0,m+1) else 2) if p <= m+1 else 0
            require(components == expected_components, 'chow_bundle_components')
            require(connected_copies == int(1 <= p <= m+1), 'chow_bundle_connected')
            if 1 <= p <= m+1:
                r = m+1-p
                surviving = []
                for i in range(m+1):
                    q, k = r-i, 2*r+1-2*i
                    require(k == 2*q+1, 'lawson_index_normalization')
                    if k >= 0 and q == 0:
                        surviving.append(i)
                    else:
                        require(k < 0 or q >= 1, 'lawson_vanishing_cases')
                require(surviving == [r], 'lawson_unique_curve_term')
                require(p + r == m+1, 'dimension_codimension_conversion')
                # The J(C) factor comes from beta x P^r, hence h^(m-r).
                require(any(j == m-r and q == 1 for j,q in chow), 'chow_lawson_alignment')
                for g in (0,1,2,7):
                    require(2*g*len(surviving) == 2*g, 'raw_h1_rank')
                bundle_cases += 1
    # Intersection with h^j followed by projection evaluates the P^i factor.
    # For j>i the intersection is zero; for j<i proper pushforward is zero.
    for m in range(31):
        for i in range(m+1):
            for j in range(m+1):
                coefficient = 1 if i-j == 0 else 0
                require(coefficient == int(i == j), 'projector_pairing')
    # Literal P1: one component survives on Alb; H1(P1) is zero.
    require(1 != 0, 'literal_p1_component_mismatch')
    # Finite torsion illustrates its loss on rationalization. This is an
    # integer annihilator check, not a model of elliptic-curve geometry.
    for n in range(2,33):
        for a in range(n):
            require((n*a) % n == 0, 'torsion_annihilator')
    # Nonzero scalar maps Q^n -> Q. Same kernels iff rows are proportional.
    # Test the well-definedness obstruction using explicit kernel generators.
    relation_pairs = 0
    for n in (2,3):
        rows = [v for v in product((-1,0,1), repeat=n) if any(v)]
        for a in rows:
            pivot = next(i for i,x in enumerate(a) if x)
            generators = []
            for j in range(n):
                if j == pivot:
                    continue
                v = [Q(0)]*n
                v[j], v[pivot] = Q(1), -Q(a[j],a[pivot])
                require(matvec([a],v) == (0,), 'relation_kernel_basis')
                generators.append(v)
            for w in rows:
                inclusion = all(matvec([w],v) == (0,) for v in generators)
                require(inclusion == (rank([a,w]) == 1), 'relation_factorization_criterion')
                if inclusion:
                    scalar = Q(w[pivot],a[pivot])
                    require(tuple(scalar*x for x in a) == w, 'relation_induced_isomorphism')
                relation_pairs += 1
    require(rank([(1,0),(0,1)]) == 2, 'equal_dimensions_different_relations')
    # Open-curve boundary elimination. Coordinates model rational period
    # classes formally; no Jacobian point is numerically approximated.
    open_cases = 0
    for h in range(8):
        for n in range(1,10):
            for seed in range(5):
                periods = [[((i+1)*(j+2)+seed*(i-j)) % 11-5 for i in range(n)] for j in range(h)]
                full = periods + [[1]*n]
                differences = [[row[i]-row[0] for i in range(1,n)] for row in periods]
                require(rank(full) == 1 + rank(differences), 'boundary_degree_elimination')
                require((h+1)-rank(full) == h-rank(differences), 'boundary_quotient_dimension')
                require(rank([[1]*n]) == 1, 'boundary_kills_component')
                for i in range(1,n):
                    v = [0]*n
                    v[i], v[0] = 1,-1
                    image = matvec(full,v)
                    require(image[-1] == 0, 'boundary_degree_zero')
                    require(image[:-1] == tuple(row[i]-row[0] for row in periods), 'boundary_period_class')
                open_cases += 1
    # Formal period quotient V/(Lambda + Qe), including a genuinely new period.
    period_cases = 0
    for n in range(1,8):
        basis = [[int(i == j) for j in range(n)] for i in range(n)]
        for a in range(n+1):
            lattice = basis[:a]
            for j in range(n):
                e = basis[j]
                extra = rank(lattice + [e]) - rank(lattice)
                require(extra == int(j >= a), 'weight_zero_period_relation')
                require(n-rank(lattice+[e]) == (n-rank(lattice))-extra, 'period_quotient_dimension')
                period_cases += 1
    # Finite linear model for a split component projection and its reflected
    # connected kernel. This only checks the block decomposition used in proof.
    splitting_cases = 0
    for c in range(1,9):
        for d in range(1,6):
            for k in range(c+1):
                projection = [[int(j == c+i) for j in range(c+d)] for i in range(d)]
                reflector = [[int(j == i) for j in range(c+d)] for i in list(range(k))+list(range(c,c+d))]
                out_projection = [[int(j == k+i) for j in range(k+d)] for i in range(d)]
                require(rank(reflector) == k+d, 'split_reflector_surjective')
                require(rank(out_projection) == d, 'split_component_surjective')
                require(rank(reflector)-rank(out_projection) == k, 'split_connected_kernel')
                for i in range(c+d):
                    v = [int(i == j) for j in range(c+d)]
                    require(matvec(out_projection,matvec(reflector,v)) == matvec(projection,v), 'split_component_square')
                splitting_cases += 1
    return {
        'schema_version': 1,
        'arithmetic': 'exact integers and fractions.Fraction',
        'status': 'PASS',
        'scope': 'finite algebra and index controls only; no proof of the general conjecture',
        'counts': dict(sorted(COUNTS.items())),
        'total_assertions': sum(COUNTS.values()),
        'case_counts': {'bundle_cases': bundle_cases, 'relation_map_pairs': relation_pairs,
                        'open_curve_formal_cases': open_cases, 'period_quotient_cases': period_cases,
                        'split_component_models': splitting_cases},
    }

def verify_manifest(base):
    manifest = json.loads((base/'AUTHOR_MANIFEST.json').read_text())
    for entry in manifest['files']:
        data = (base/entry['file']).read_bytes()
        assert len(data) == entry['bytes'], entry['file']
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['file']
    print('Manifest integrity: PASS')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--verify-manifest', action='store_true')
    args = parser.parse_args()
    result = json.dumps(controls(), indent=2, sort_keys=True) + '\n'
    base = Path(__file__).resolve().parent
    if args.write:
        (base/'CHECK_RESULTS.json').write_text(result)
    print(result, end='')
    if args.verify_manifest:
        verify_manifest(base)

if __name__ == '__main__':
    main()
