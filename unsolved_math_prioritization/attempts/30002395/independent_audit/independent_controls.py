#!/usr/bin/env python3
"""Independent exact finite controls. These do not prove infinite theorems.

Run: python independent_controls.py --frozen ../public
Only the frozen packet is read. JSON results are written to stdout.
"""
import argparse
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import time

EXPECTED_MANIFEST = '5d4700cf4699eea9443dbd40b268839f77404cb701bb15976efdb02bb1861c3a'
EXPECTED_PROOF = '3f9686c459bfdcfe0ede72ef21c102d74c9f3c6fd5f019ab263aca762cdcedb4'
C = Counter()

def require(statement, category):
    if not statement:
        raise AssertionError(category)
    C[category] += 1

def digest(data):
    return hashlib.sha256(data).hexdigest()

def validate_snapshot(files):
    """Pure validation makes destructive negative controls unnecessary."""
    if digest(files['MANIFEST.json']) != EXPECTED_MANIFEST:
        raise ValueError('manifest hash')
    manifest = json.loads(files['MANIFEST.json'])
    names = [row['path'] for row in manifest['files']]
    if len(names) != len(set(names)) or set(files) != set(names) | {'MANIFEST.json'}:
        raise ValueError('inventory mismatch')
    for row in manifest['files']:
        p = Path(row['path'])
        if p.is_absolute() or '..' in p.parts:
            raise ValueError('unsafe path')
        data = files[row['path']]
        if len(data) != row['bytes'] or digest(data) != row['sha256']:
            raise ValueError('file mismatch: ' + row['path'])
    if digest(files['PROOF.md']) != EXPECTED_PROOF:
        raise ValueError('proof hash')
    return len(names)

def rejects(fn):
    try:
        fn()
    except (ValueError, KeyError):
        return True
    return False

def transitive(rows):
    # If j belongs to the upper set of i, the upper set of j must be inside it.
    return all(not (rows[j] & ~rows[i])
               for i in range(len(rows)) for j in range(len(rows)) if rows[i] >> j & 1)

def orders(n):
    # Three choices per unordered pair enforce antisymmetry before enumeration.
    pairs = list(combinations(range(n), 2))
    for choice in product(range(3), repeat=len(pairs)):
        rows = [1 << i for i in range(n)]
        for (i, j), state in zip(pairs, choice):
            if state == 1:
                rows[i] |= 1 << j
            elif state == 2:
                rows[j] |= 1 << i
        if transitive(rows):
            yield tuple(rows)

def naive_orders(n):
    # Independent comparator: all off-diagonal directed-edge bit patterns.
    edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    for mask in range(1 << len(edges)):
        rel = {(i, i) for i in range(n)}
        rel |= {e for k, e in enumerate(edges) if mask >> k & 1}
        if any(i != j and (j, i) in rel for i, j in rel):
            continue
        if any((i, k) not in rel for i, j in rel for jj, k in rel if j == jj):
            continue
        yield tuple(sum(1 << j for ii, j in rel if ii == i) for i in range(n))

class Space:
    def __init__(self, rows):
        self.rows = rows
        self.n = len(rows)
        self.top = (1 << self.n) - 1
        self.opens = tuple(s for s in range(self.top + 1)
                           if all(not (s >> i & 1) or not (rows[i] & ~s)
                                  for i in range(self.n)))
        self.open_set = set(self.opens)
        self.closed = tuple(self.top ^ s for s in self.opens)
        self.closures = tuple(sum(1 << i for i in range(self.n) if rows[i] >> j & 1)
                              for j in range(self.n))
    def interior(self, s):
        return sum(1 << i for i in range(self.n) if not self.rows[i] & ~s)
    def relative_interior(self, u, s):
        return sum(1 << i for i in range(self.n)
                   if u >> i & 1 and not (self.rows[i] & u) & ~s)

def mask_union(xs):
    v = 0
    for x in xs:
        v |= x
    return v

def mask_intersection(xs, top):
    v = top
    for x in xs:
        v &= x
    return v

def maps(P, X, f):
    inverse = lambda u: sum(1 << p for p in range(P.n) if u >> f[p] & 1)
    continuous = all(inverse(u) in P.open_set for u in X.opens)
    if not continuous:
        return None
    image = mask_union(1 << x for x in f)
    R = {(p, q) for p in range(P.n) for q in range(P.n)
         if X.rows[f[q]] >> f[p] & 1}
    # Minimal opens of the subspace R suffice to test openness of projection.
    projection_open = True
    for p, q in R:
        projected = mask_union(1 << r for r, s in R
                               if P.rows[p] >> r & 1 and P.rows[q] >> s & 1)
        if projected not in P.open_set:
            projection_open = False
            break
    relative_opens = {u & image for u in X.opens}
    invariant_image_open = True
    for v in P.opens:
        invariant = all(not (v >> q & 1) or v >> p & 1 for p, q in R)
        if invariant:
            fv = mask_union(1 << f[p] for p in range(P.n) if v >> p & 1)
            if fv not in relative_opens:
                invariant_image_open = False
                break
    pseudo_open = projection_open and invariant_image_open
    pseudo_epi = all((u & ~v) & image for u in X.opens for v in X.opens
                     if v != u and v & u == v)
    images = tuple(inverse(u) for u in X.opens)
    # In a finite lattice, binary operations plus top and bottom handle all families.
    lattice_embedding = (len(set(images)) == len(images)
                         and inverse(0) == 0 and inverse(X.top) == P.top
                         and all(inverse(u & v) == inverse(u) & inverse(v)
                                 and inverse(u | v) == inverse(u) | inverse(v)
                                 for u in X.opens for v in X.opens))
    quotient = image == X.top and all((u in X.open_set) == (inverse(u) in P.open_set)
                                      for u in range(X.top + 1))
    return pseudo_open, pseudo_epi, lattice_embedding, quotient

# Gaussian integers represented by builtin complex are exact for these small integers.
# Fractions are not needed; no transcendental or approximate comparison is used.
def m_add(a, b): return tuple(x + y for x, y in zip(a, b))
def m_mul(a, b):
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])
def m_star(a): return (a[0].conjugate(), a[2].conjugate(), a[1].conjugate(), a[3].conjugate())
def diagonal(a, b): return (a, 0j, 0j, b)
def plus(x, y): return (tuple(m_add(a, b) for a, b in zip(x[0], y[0])), x[1]+y[1], x[2]+y[2])
def times(x, y): return (tuple(m_mul(a, b) for a, b in zip(x[0], y[0])), x[1]*y[1], x[2]*y[2])
def adjoint(x): return (tuple(m_star(a) for a in x[0]), x[1].conjugate(), x[2].conjugate())
def connect(x): return (x[0]+(diagonal(x[1], x[2]),), x[1], x[2])
def retract(x, m): return (x[0][:m], x[1], x[2])
def bad_connect(x): return (x[0]+((x[1], x[2], 0j, x[2]),), x[1], x[2])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frozen', type=Path, default=Path(__file__).resolve().parent.parent/'public')
    args = parser.parse_args()
    started = time.perf_counter()
    files = {p.name: p.read_bytes() for p in args.frozen.iterdir() if p.is_file()}
    require(validate_snapshot(files) == 13, 'frozen_inventory_hashes_and_sizes')
    mutation = dict(files); mutation['PROOF.md'] += b'!'
    require(rejects(lambda: validate_snapshot(mutation)), 'detect_one_byte_mutation')
    mutation = dict(files); mutation.pop('TURN_3.md')
    require(rejects(lambda: validate_snapshot(mutation)), 'detect_missing_file')
    mutation = dict(files); mutation['UNLISTED.txt'] = b'control'
    require(rejects(lambda: validate_snapshot(mutation)), 'detect_unlisted_file')
    mutation = dict(files); mutation['MANIFEST.json'] += b' '
    require(rejects(lambda: validate_snapshot(mutation)), 'detect_manifest_mutation')
    freeze_seconds = time.perf_counter() - started

    cached = {}
    enumeration = {}
    for n in range(6):
        t0 = time.perf_counter()
        rows_list = list(orders(n))
        elapsed = time.perf_counter() - t0
        require(len(rows_list) == [1, 1, 3, 19, 219, 4231][n], 'labeled_poset_count')
        cached[n] = [Space(rows) for rows in rows_list]
        enumeration[str(n)] = {'posets': len(rows_list), 'ternary_candidates': 3**(n*(n-1)//2),
                               'binary_candidates_avoided': 2**(n*(n-1)), 'seconds': elapsed}
        if n <= 4:
            t0 = time.perf_counter()
            baseline = set(naive_orders(n))
            baseline_seconds = time.perf_counter() - t0
            require(set(rows_list) == baseline, 'optimized_equals_independent_naive_enumerator')
            enumeration[str(n)]['naive_seconds'] = baseline_seconds
        for X in cached[n]:
            for i in range(n):
                require(X.rows[i] in X.open_set, 'minimal_neighborhood_is_open')
            for F in X.closed:
                if not F:
                    continue
                meets = [u for u in X.opens if u & F]
                irreducible = all((u & v & F) != 0 for u in meets for v in meets)
                require(not irreducible or X.closures.count(F) == 1, 'finite_sobriety_via_open_intersections')
            for u in X.opens:
                for v in X.opens:
                    require(u & v in X.open_set and u | v in X.open_set, 'binary_lattice_operations')
                for s in range(X.top + 1):
                    require(u & X.interior(s) == X.relative_interior(u, s), 'open_chart_arbitrary_subset_interior')
            if n <= 3:
                for choice in range(1 << len(X.opens)):
                    family = [u for k, u in enumerate(X.opens) if choice >> k & 1]
                    require(mask_union(family) in X.open_set and
                            mask_intersection(family, X.top) in X.open_set,
                            'all_families_including_empty')
            # Every two-open cover: actual component map plus exact image cardinality.
            for u in X.opens:
                for v in X.opens:
                    if u | v == X.top:
                        require(len({(w & u, w & v) for w in X.opens}) == len(X.opens),
                                'open_cover_injectivity')

    map_counts = Counter()
    for np in range(4):
        for nx in range(4):
            for P in cached[np]:
                for X in cached[nx]:
                    for f in product(range(nx), repeat=np):
                        result = maps(P, X, f)
                        map_counts['all_set_maps'] += 1
                        if result is None:
                            continue
                        po, pe, le, qu = result
                        map_counts['continuous_maps'] += 1
                        map_counts['pseudo_open_maps'] += po
                        map_counts['pseudo_epimorphisms'] += pe
                        map_counts['quotients'] += qu
                        require((po and pe) == le, 'finite_pseudo_map_lattice_equivalence')
                        require(pe == (len(set(f)) == nx), 'finite_pseudo_epi_surjectivity')
    D2 = Space((1, 2)); S2 = Space((3, 2))
    po, pe, le, qu = maps(D2, S2, (0, 1))
    require(po and pe and le and not qu, 'pseudo_open_surjection_need_not_be_quotient')
    # Finite T1 targets are discrete; use the analytical singleton-to-R witness
    # in AUDIT.md for the general open-onto-image correction.

    weak_counts = {}
    for np in range(1, 4):
        top = (1 << np) - 1
        good = fail = 0
        for a, b in product(range(top + 1), repeat=2):
            psi = (0, a, b, top)
            if len(set(psi)) != 4:
                continue
            if not all(psi[u & v] == psi[u] & psi[v] for u in range(4) for v in range(4)):
                continue
            good += 1
            # Every nonempty directed subfamily of this finite lattice is tested.
            for mask in range(1, 16):
                fam = [x for x in range(4) if mask >> x & 1]
                directed = all(any((u | v) & w == (u | v) for w in fam) for u in fam for v in fam)
                if directed:
                    require(psi[mask_union(fam)] == mask_union(psi[u] for u in fam),
                            'weak_map_all_directed_suprema')
            fail += a | b != top
        weak_counts[str(np)] = {'meet_embeddings': good, 'binary_join_failures': fail}
    require(weak_counts == {'1': {'meet_embeddings': 0, 'binary_join_failures': 0},
                            '2': {'meet_embeddings': 2, 'binary_join_failures': 0},
                            '3': {'meet_embeddings': 12, 'binary_join_failures': 6}},
            'minimal_weak_map_countermodel_counts')
    psi = (0, 1, 2, 7)
    require(psi[3] != psi[1] | psi[2], 'weak_map_binary_join_negative')
    require(len(set(psi) | {psi[1] | psi[2]}) == 5, 'join_closure_changes_space')
    require(len({(u & 1, u & 1) for u in range(4)}) != 4, 'missing_cover_detects_noninjectivity')
    small_psi = (0, 1)  # O(singleton) into O(two-point discrete space).
    require(all(small_psi[u & v] == (small_psi[u] & small_psi[v]) and
                small_psi[u | v] == (small_psi[u] | small_psi[v])
                for u in range(2) for v in range(2)) and small_psi[1] != 3,
            'missing_top_detected')

    samples = []
    scalars = (0j, 1+2j, -2+1j)
    for m in range(5):
        values = []
        for a, b in product(scalars, repeat=2):
            matrices = tuple((a+i, b-1j, 2j-a, b-i) for i in range(m))
            values.append((matrices, a, b))
        for x in values:
            require(connect(adjoint(x)) == adjoint(connect(x)), 'AF_complex_adjoint')
            require(retract(connect(x), m) == x, 'AF_injective_left_inverse')
            for y in values:
                require(connect(plus(x, y)) == plus(connect(x), connect(y)), 'AF_complex_addition')
                require(connect(times(x, y)) == times(connect(x), connect(y)), 'AF_complex_multiplication')
        samples.extend(values)
    require(any(bad_connect(adjoint(x)) != adjoint(bad_connect(x)) for x in samples),
            'mutated_AF_embedding_rejected_by_adjoint')
    require(any(bad_connect(times(x, x)) != times(bad_connect(x), bad_connect(x)) for x in samples),
            'mutated_AF_embedding_rejected_by_multiplication')
    # Tail truncation algebraic retractions commute with every longer embedding.
    for x in samples:
        m = len(x[0]); y = x
        for _ in range(5):
            y = connect(y)
            require(retract(y, m) == x, 'AF_all_tested_later_stages_retract')
    # Re-read original after all tests. No frozen file is ever written.
    final_files = {p.name: p.read_bytes() for p in args.frozen.iterdir() if p.is_file()}
    require(files == final_files, 'original_packet_unchanged')
    return {
        'status': 'PASS', 'independent_implementation': True,
        'scope': 'Finite exact checks and byte-integrity tests; not proofs of infinite claims.',
        'input': {'manifest_sha256': EXPECTED_MANIFEST, 'proof_sha256': EXPECTED_PROOF, 'files_checked': 13},
        'enumeration': enumeration, 'map_counts': dict(map_counts), 'weak_map_search': weak_counts,
        'checks_by_category': dict(C), 'total_checks': sum(C.values()),
        'optimization': 'Three states per unordered pair instead of independent directed-edge bits; integer bitsets; cached topologies; binary lattice checks replace all-family enumeration for n=4,5 by finite induction. Naive cross-check through n=4 remains independent.',
        'freeze_seconds': freeze_seconds, 'total_seconds': time.perf_counter() - started,
        'not_established_by_controls': ['infinite compactness', 'Polish completeness', 'infinite sobriety',
                                       'classification of infinite-algebra irreducible representations',
                                       'the Harnisch-Kirchberg external theorem', 'universal realization', 'formal proof certification']}

if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
