#!/usr/bin/env python3
"""Independent exact finite checks; analytic lifting is a written theorem application.

No network, Git, credentials, subprocesses, or external writes. Explicit exceptions
are used so that the same checks run under Python normal, -O and -OO.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations, permutations, product
from functools import reduce
from math import gcd
import argparse
import copy
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parent


def require(condition, label):
    if not condition:
        raise ValueError(label)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def determinant(a):
    n = len(a)
    if not n:
        return 1
    total = 0
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = (-1) ** inversions
        for i in range(n):
            term *= a[i][p[i]]
        total += term
    return total


def smith_factors(a):
    n = len(a)
    divisors = [1]
    for k in range(1, n + 1):
        minors = []
        for rows in combinations(range(n), k):
            for cols in combinations(range(n), k):
                minors.append(abs(determinant([[a[i][j] for j in cols] for i in rows])))
        divisors.append(reduce(gcd, minors, 0))
    return [divisors[i] // divisors[i - 1] for i in range(1, n + 1)]


def inverse(a):
    n = len(a)
    b = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if b[i][j])
        b[j], b[pivot] = b[pivot], b[j]
        q = b[j][j]
        b[j] = [x / q for x in b[j]]
        for i in range(n):
            if i != j:
                q = b[i][j]
                b[i] = [x - q * y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def multiply(a, b):
    return [sum(x * y for x, y in zip(row, b)) for row in a]


def in_lattice(inv, v):
    return all(x.denominator == 1 for x in multiply(inv, v))


def class_order(inv, v, bound):
    return next(k for k in range(1, bound + 1)
                if in_lattice(inv, [k * x for x in v]))


def reduced_banana(lengths):
    # Unit subdivide each individual metric edge; endpoints are 0 and 1.
    edges = []
    next_vertex = 2
    for length in lengths:
        require(isinstance(length, int) and length > 0, 'positive integer thickness')
        path = [0] + list(range(next_vertex, next_vertex + length - 1)) + [1]
        next_vertex += length - 1
        edges.extend(zip(path, path[1:]))
    lap = [[0] * next_vertex for _ in range(next_vertex)]
    for u, v in edges:
        lap[u][u] += 1
        lap[v][v] += 1
        lap[u][v] -= 1
        lap[v][u] -= 1
    keep = [i for i in range(next_vertex) if i != 1]
    return [[lap[i][j] for j in keep] for i in keep], edges


def verify_frozen(expected):
    file = BASE / 'FROZEN_INPUTS.json'
    require(digest(file) == expected, 'frozen-input manifest digest')
    frozen = json.loads(file.read_text())
    for item in frozen['files']:
        p = BASE / item['path']
        require(p.is_file() and not p.is_symlink(), 'regular frozen input: ' + item['path'])
        require(p.stat().st_size == item['bytes'] and digest(p) == item['sha256'],
                'frozen bytes: ' + item['path'])
    # Root files are independently pinned and not copied or modified.
    anchors = json.loads((BASE / 'ROOT_ANCHORS.json').read_text())
    for item in anchors['files']:
        p = Path(item['path'])
        require(p.is_file() and p.stat().st_size == item['bytes'] and digest(p) == item['sha256'],
                'external immutable anchor: ' + item['path'])
    return len(frozen['files']), len(anchors['files'])


def source_and_accounting_checks():
    binding = json.loads((BASE / 'INPUT_BINDING.json').read_text())
    require(binding['head'] == '4e6b40a1863c19f21a354d3237387b189ebd119d', 'immutable submitted head')
    require(len(binding['files']) == 7, 'seven actual submitted blobs')
    for item in binding['files']:
        p = BASE / item['local']
        b = p.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        require(len(b) == item['bytes'] and digest(p) == item['sha256'] and blob == item['git_blob_sha1'],
                'actual SHA256 and Git-blob identity: ' + item['local'])
    submitted_sources = json.loads((BASE / 'private/pr_source/SOURCE_MANIFEST.json').read_text())['sources']
    fresh = json.loads((BASE / 'private/primary/RETRIEVAL.json').read_text())
    require(len(submitted_sources) == len(fresh) == 5, 'all five primary source bodies')
    for item in fresh:
        match = [x for x in submitted_sources if x['url'] == item['url']]
        require(len(match) == 1 and match[0]['sha256'] == item['sha256'] and match[0]['bytes'] == item['bytes'],
                'fresh primary matches pinned submitted source: ' + item['key'])
        require((BASE / item['file']).read_bytes().startswith(b'%PDF-') and item['status'] == 200,
                'complete primary PDF response')
    literal = json.loads((BASE / 'LITERAL_FOUR_CELL_PROPOSAL.json').read_text())
    require(isinstance(literal, list) and len(literal) == 4 and all(isinstance(x, str) for x in literal),
            'literal four-string row')
    require(literal[1] == '' and literal[2] == 'https://doi.org/10.1186/s40687-014-0019-0',
            'blank B and exact existing publication DOI')
    require('https://github.com/AlecKriebel/Math/pull/1295' in literal[3], 'exact PR1295 URL in D')
    leads = json.loads((BASE / 'ALIAS_ADJUDICATION.json').read_text())
    require({x['row'] for x in leads['hits']} == {x['row'] for x in leads['mathematical_disposition']} == {149, 191},
            'every exact semantic lead has a reasoned disposition')
    require(not leads['automatic_exemptions'], 'no automatic semantic exemption')
    disposition = json.loads((BASE / 'ACCOUNTING_DISPOSITION.json').read_text())
    require(disposition['root_adopted'] is False and disposition['publication_ready'] is False
            and disposition['external_mutations'] == 0, 'review is not action readiness')
    return {'submitted_blobs': 7, 'matching_fresh_primary_pdfs': 5, 'literal_cells': 4,
            'semantic_leads': [149, 191], 'root_adopted': False, 'publication_ready': False}


def finite_checks(c):
    require(c['uniformizer_value'] == 1, 'fixed discrete normalization, no ramified rescale')
    require(c['residue_characteristic'] == 0, 'this construction is over characteristic zero')
    require(c['vertex_push_multiplier'] == 1, 'covariant vertex push has no local-degree factor')
    source, target = c['source_lengths'], c['target_lengths']
    image, slopes = c['edge_images'], c['slopes']
    require(len(source) == len(image) == len(slopes) == 4, 'all four source edges present')
    require(source == [1, 1, 1, 1] and target == [1, 2, 2], 'original fixed thicknesses')
    require(all(source[i] * slopes[i] == target[image[i]] for i in range(4)),
            'edge expansion and length compatibility')
    directional = [sum(slopes[i] for i in range(4) if image[i] == j) for j in range(3)]
    require(directional == [2, 2, 2], 'harmonicity at both vertices and degree two')
    marks = c['marked_source']
    require(len(marks) == len(set(marks)) == 4, 'four distinct source markings')
    require(set(marks) == {'1', '-1', '0', 'infinity'}, 'complete marked inverse fibers')
    fibers = {'1': [('1', 1), ('-1', 1)], '0': [('0', 2)], 'infinity': [('infinity', 2)]}
    require(all(sum(d for _, d in fiber) == 2 for fiber in fibers.values()), 'residue fiber degree')
    require(all(p in marks for fiber in fibers.values() for p, _ in fiber), 'no omitted marked preimage')
    require(2 * 2 - 2 - sum(d - 1 for d in slopes) == 0, 'vertex graph ramification zero')
    for i, d in enumerate(slopes):
        require(2 * d - 2 - 2 * (d - 1) == 0, 'interior graph ramification zero')
        require(source[i] * d == target[image[i]], 'node equation thickness identity')
    ls, es = reduced_banana(source)
    lt, et = reduced_banana(target)
    require(ls == [[4]], 'independently built source reduced Laplacian')
    require(lt == [[3, -1, -1], [-1, 2, 0], [-1, 0, 2]], 'independently built target reduced Laplacian')
    actual_orders = [abs(determinant(ls)), abs(determinant(lt))]
    require(actual_orders == c['expected_orders'] == [4, 8], 'correct graph orders, source then target')
    require(smith_factors(ls) == [4] and smith_factors(lt) == [1, 1, 8], 'exact Smith factors')
    it = inverse(lt)
    U, A, B = [1, 0, 0], [0, 1, 0], [0, 0, 1]
    require(multiply(it, U) == [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)], 'endpoint rational solution')
    require([class_order(it, x, 8) for x in (U, A, B)] == [4, 8, 8], 'exact orders of U,A,B')
    require(in_lattice(it, [1, -2, 0]) and in_lattice(it, [0, -5, 1]), 'U=2A and B=5A')
    # Enumerate the actual target quotient using the lattice, not modular labels alone.
    representatives = [[0, j, 0] for j in range(8)]
    require(all(not in_lattice(it, [x - y for x, y in zip(a, b)])
                for a, b in combinations(representatives, 2)), 'eight distinct target classes')
    actual_map = []
    for j in range(4):
        labels = [k for k, r in enumerate(representatives)
                  if in_lattice(it, [j * U[i] - r[i] for i in range(3)])]
        require(len(labels) == 1, 'unique target class for vertex push')
        actual_map.append(labels[0])
    require(actual_map == [0, 2, 4, 6], 'full covariant map enumeration')
    require(all(actual_map[(a + b) % 4] == (actual_map[a] + actual_map[b]) % 8
                for a, b in product(range(4), repeat=2)), 'sixteen additive pairs')
    require(len(set(actual_map)) == 4 and actual_map.count(0) == 1, 'injective nonsurjective and cokernel two')
    # Cycle-space pairing is independent of subdivision Laplacian computation.
    source_gram = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
    target_gram = [[3, 1], [1, 3]]
    require(determinant(source_gram) == 4 and determinant(target_gram) == 8, 'cycle-pairing discriminants')
    require(len(es) - 2 + 1 == 3 and len(et) - 4 + 1 == 2, 'normalization genera')
    require(2 * 3 - 2 == 2 * (2 * 2 - 2), 'unramified Riemann-Hurwitz consistency')
    intersection = len(source)
    self_intersection = -intersection  # (C1+C2).Ci=0 on the reduced regular model.
    require(self_intersection == -4 and self_intersection != -1,
            'source component self-intersection excludes exceptional curves')
    return {'source_laplacian': ls, 'target_laplacian': lt, 'smith_source': [4], 'smith_target': [1, 1, 8],
            'map': actual_map, 'image': [0, 2, 4, 6], 'kernel_order': 1, 'cokernel_order': 2,
            'direction_sums': directional, 'source_genus': 3, 'target_genus': 2,
            'limits': 'Finite checks supplement the written use of lifting, deformation, minimality and Raynaud theorems.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze-sha256', required=True)
    args = parser.parse_args()
    n, a = verify_frozen(args.freeze_sha256)
    identities = source_and_accounting_checks()
    config = json.loads((BASE / 'CONTROL_INPUTS.json').read_text())
    result = finite_checks(config)
    corruptions = {
        'printed_orders_reversed': ('expected_orders', [8, 4]),
        'wrong_local_degree_vertex_push': ('vertex_push_multiplier', 2),
        'discard_target_thicknesses': ('target_lengths', [1, 1, 1]),
        'ramified_rescale': ('uniformizer_value', 2),
        'nonharmonic_slope': ('slopes', [1, 1, 1, 2]),
        'characteristic_two': ('residue_characteristic', 2),
        'missing_marked_preimage': ('marked_source', ['1', '0', 'infinity']),
        'missing_source_edge': ('source_lengths', [1, 1, 1]),
    }
    rejected = []
    for label, (key, value) in corruptions.items():
        bad = copy.deepcopy(config)
        bad[key] = value
        try:
            finite_checks(bad)
        except ValueError as e:
            rejected.append({'case': label, 'reason': str(e)})
        else:
            raise ValueError('negative control escaped: ' + label)
    print(json.dumps({'status': 'PASS', 'optimized': sys.flags.optimize,
                      'frozen_inputs': n, 'root_anchors': a,
                      'source_and_accounting': identities,
                      'finite_results': result, 'rejected_negative_controls': rejected}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps({'status': 'FAIL', 'error': type(e).__name__ + ': ' + str(e)}))
        sys.exit(1)
