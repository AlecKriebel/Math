#!/usr/bin/env python3
"""Portable finite controls. They do not prove the operadic-center conjecture.

Optional --external-catalog, --external-problems and --external-research paths
recompute the recorded complete-corpus hashes. These files are not distributed.
The problem and catalog inputs also check the selected identity and statement
hash; the research input checks absence of the exact problem-number key.
--manifest with --expected-manifest verifies the frozen public file set.
"""
import argparse
import hashlib
import itertools as it
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHECKS = 0


def check(value, message):
    global CHECKS
    CHECKS += 1
    if not value:
        raise AssertionError(message)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def simplices(q):
    return [[tuple(zip(levels, signs))
             for levels in it.combinations(range(q), k + 1)
             for signs in it.product(range(2), repeat=k + 1)]
            for k in range(q)]


def bd(chain):
    out = {}
    for simplex, coefficient in chain.items():
        for i in range(len(simplex)):
            face = simplex[:i] + simplex[i + 1:]
            out[face] = out.get(face, 0) + (-1)**i * coefficient
    return {s: a for s, a in out.items() if a}


def matrix(columns, rows):
    rid = {x: i for i, x in enumerate(rows)}
    a = [[0] * len(columns) for _ in rows]
    for j, s in enumerate(columns):
        for f, coefficient in bd({s: 1}).items():
            a[rid[f]][j] = coefficient
    return a


def rank(a, prime=None):
    if not a or not a[0]:
        return 0
    a = [[(x % prime if prime else Fraction(x)) for x in row] for row in a]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inverse = pow(a[r][c], -1, prime) if prime else 1/a[r][c]
        a[r] = [(x * inverse % prime if prime else x * inverse) for x in a[r]]
        for i in range(r + 1, len(a)):
            factor = a[i][c]
            if factor:
                a[i] = [((x - factor*y) % prime if prime else x - factor*y)
                        for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def poset_controls():
    records = []
    for q in range(1, 6):
        s = simplices(q)
        check(sum(map(len, s)) == 3**q - 1, 'cross-polytope face count')
        for dimension, layer in enumerate(s):
            for face in layer:
                check(len({v[0] for v in face}) == dimension + 1, 'one vertex per level')
                if dimension >= 2:
                    check(not bd(bd({face: 1})), 'boundary squared')
        boundaries = [None] + [matrix(s[k], s[k-1]) for k in range(1, q)]
        expected = [int(k == 0) + int(k == q-1) for k in range(q)]
        betti_by_field = {}
        for p in [None, 2, 3, 5]:
            ranks = [0] + [rank(a, p) for a in boundaries[1:]] + [0]
            betti = [len(s[k]) - ranks[k] - ranks[k+1] for k in range(q)]
            check(betti == expected, 'sphere homology over selected field')
            betti_by_field['Q' if p is None else 'F'+str(p)] = betti
        records.append({'levels': q, 'f_vector': list(map(len, s)), 'betti': betti_by_field})
    a, b, c, d, e = (0, 0), (0, 1), (1, 0), (1, 1), (2, 0)
    z = {(a, c): 1, (b, c): -1, (b, d): 1, (a, d): -1}
    t = {edge + (e,): n for edge, n in z.items()}
    check(not bd(z), 'displayed square is a cycle')
    check(bd(t) == z, 'integral cone boundary equals square')
    check(len(simplices(2)) == 2, 'no degree-two simplices in two-level model')
    check(records[1]['betti']['Q'][1] != records[2]['betti']['Q'][1],
          'negative control: two and three levels are not interchangeable')
    return records


def monoids(n):
    cells = [(i, j) for i in range(1, n) for j in range(1, n)]
    result = []
    for values in it.product(range(n), repeat=len(cells)):
        t = [[0]*n for _ in range(n)]
        for i in range(n):
            t[i][0] = t[0][i] = i
        for (i, j), value in zip(cells, values):
            t[i][j] = value
        if all(t[t[a][b]][c] == t[a][t[b][c]] for a, b, c in it.product(range(n), repeat=3)):
            result.append(t)
    return result


def center(t):
    return [a for a in range(len(t)) if all(t[a][b] == t[b][a] for b in range(len(t)))]


def monoid_controls():
    all_m = [(n, t) for n in range(1, 4) for t in monoids(n)]
    counts = {str(n): sum(m == n for m, _ in all_m) for n in range(1, 4)}
    for n, t in all_m:
        z = center(t)
        check(0 in z, 'center contains unit')
        for a, b in it.product(z, repeat=2):
            check(t[a][b] in z, 'center is closed')
            check(t[a][b] == t[b][a], 'center is commutative')
    surjections = 0
    for n, s in all_m:
        for m, t in all_m:
            if m > n:
                continue
            for tail in it.product(range(m), repeat=n-1):
                f = (0,) + tail
                if set(f) != set(range(m)):
                    continue
                if all(f[s[a][b]] == t[f[a]][f[b]] for a, b in it.product(range(n), repeat=2)):
                    surjections += 1
                    check(all(f[z] in center(t) for z in center(s)), 'surjective map preserves center')
    # Inclusion C2 -> S3 is an actual homomorphism; it fails on centers.
    permutations = list(it.permutations(range(3)))
    compose = lambda p, q: tuple(p[q[i]] for i in range(3))
    identity, transposition, other = (0, 1, 2), (1, 0, 2), (0, 2, 1)
    h = [identity, transposition]
    for p, q in it.product(h, repeat=2):
        check(compose(p, q) in h, 'order-two subgroup closed')
        check(compose(p, q) == compose(q, p), 'subgroup abelian')
    z_g = [p for p in permutations if all(compose(p, q) == compose(q, p) for q in permutations)]
    check(z_g == [identity], 'S3 center is trivial')
    check(transposition not in z_g, 'inclusion does not send central element to central element')
    check(compose(transposition, other) != compose(other, transposition), 'explicit noncommuting witness')
    # A commutative monoid need not be a group: {0,1} with max.
    t = [[0, 1], [1, 1]]
    check(center(t) == [0, 1], 'idempotent commutative monoid has full center')
    check(not any(t[1][x] == 0 for x in range(2)), 'noninvertible component negative control')
    return {'unital_tables_by_size': counts, 'surjective_homomorphisms_tested': surjections,
            'S3_center_size': len(z_g), 'center_covariance_counterexample': True}


def endomorphism_controls():
    result = []
    for n in [1, 2]:
        functions = [list(it.product(range(n), repeat=n**arity)) for arity in range(4)]
        inputs = [list(it.product(range(n), repeat=arity)) for arity in range(4)]
        candidates = []
        for z in functions[1]:
            central = True
            for arity in range(4):
                for p in functions[arity]:
                    for i, args in enumerate(inputs[arity]):
                        mapped = tuple(z[x] for x in args)
                        j = inputs[arity].index(mapped)
                        if z[p[i]] != p[j]:
                            central = False
                            break
                    if not central:
                        break
                if not central:
                    break
            if central:
                candidates.append(z)
        check(candidates == [tuple(range(n))], 'nullary operations force identity center')
        result.append({'set_size': n, 'arities_tested': [0, 1, 2, 3],
                       'operation_counts': list(map(len, functions)), 'central_unary_operations': candidates})
    return result


def external_controls(args):
    metadata = json.loads((ROOT/'SOURCE_VERIFICATION.json').read_text())
    records = []
    for name in ['catalog', 'problems', 'research']:
        path = getattr(args, 'external_'+name)
        if path is None:
            continue
        b = Path(path).read_bytes()
        expected = metadata['corpora'][name]
        check(len(b) == expected['bytes'], name+' complete byte count')
        check(digest(b) == expected['sha256'], name+' complete hash')
        d = json.loads(b)
        if name != 'research':
            selected = [x for x in d if str(x.get('id')) == '30006031']
            check(len(selected) == 1, name+' unique ID')
            record = selected[0]
            check(record['problem_number'] == 'OWR-14298590-001', name+' problem number')
            check(record['source_url'] == 'https://doi.org/10.4171/owr/2024/39', name+' source DOI')
            if name == 'problems':
                check(digest(record['statement'].encode()) == metadata['statement_sha256'], 'statement hash')
            else:
                check(record['statement_hash'] == metadata['statement_sha256'], 'catalog statement hash')
                check(record['rank'] == 792, 'catalog rank')
        else:
            check('OWR-14298590-001' not in d, 'exact prior research key absent')
        records.append({'input': name, 'byte_count_and_hash_match': True})
    return records


def manifest_controls(path, expected_digest):
    if expected_digest is None:
        raise ValueError('--manifest requires --expected-manifest; do not trust a substituted manifest')
    path = Path(path).resolve()
    raw = path.read_bytes()
    check(digest(raw) == expected_digest, 'manifest trusted digest')
    d = json.loads(raw)
    root = path.parent
    listed = set()
    for record in d['files']:
        rel = record['path']
        check(Path(rel).name == rel and rel not in listed, 'safe unique flat relative path')
        listed.add(rel)
        p = root/rel
        check(not p.is_symlink(), 'no symbolic link')
        b = p.read_bytes()
        check(len(b) == record['bytes'] and digest(b) == record['sha256'], 'frozen byte identity')
    actual = {p.name for p in root.iterdir() if p.is_file() and p.name != path.name}
    check(actual == listed, 'exact public file allowlist')
    check(not any(p.is_dir() for p in root.iterdir()), 'no unlisted directory')
    return {'files': len(listed), 'manifest_sha256': digest(raw), 'exact_file_set': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['catalog', 'problems', 'research']:
        parser.add_argument('--external-'+name, type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--expected-manifest')
    args = parser.parse_args()
    output = {'problem_id': 30006031, 'target_status': 'unresolved',
              'poset_homology': poset_controls(), 'finite_monoids': monoid_controls(),
              'endomorphism_operads': endomorphism_controls(), 'external_corpora': external_controls(args),
              'scope': 'Finite controls and optional hash replay only; not a proof of the target or of source theorems.'}
    if args.manifest:
        output['manifest'] = manifest_controls(args.manifest, args.expected_manifest)
    output['assertions_passed'] = CHECKS
    output['result'] = 'PASS'
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
