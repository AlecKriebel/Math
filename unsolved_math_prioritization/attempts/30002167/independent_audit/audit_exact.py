#!/usr/bin/env python3
"""Independent exact audit. No imports from the candidate packet; no network I/O.

Run with an optional candidate-packet path. All temporary mutations are made in
new temporary directories. The audited packet is never modified.
"""
import copy
import hashlib
import itertools
import json
import math
import shutil
import sys
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

EXPECTED_MANIFEST = 'e2645129ee536f33d58415f04b45323c816ffb3706ef02101e78de2172049180'
DEFAULT_INPUT = Path(__file__).resolve().parents[2] / 'hamiltonian_30002167' / 'safe'
P = ((95, 0), (96, 0), (-50, 83), (-51, 83), (-50, -83), (-51, -83))
DENOMINATOR = 100
EDGES = tuple(itertools.combinations(range(6), 2))


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def binding(root):
    """Anchor the manifest itself, not just its editable payload map."""
    root = Path(root)
    need(root.is_dir() and not root.is_symlink(), 'bad input directory')
    manifest = root / 'MANIFEST.json'
    need(manifest.is_file() and not manifest.is_symlink(), 'bad manifest entry')
    blob = manifest.read_bytes()
    need(sha(blob) == EXPECTED_MANIFEST, 'manifest anchor mismatch')
    doc = json.loads(blob)
    need(doc['schema'] == 1 and len(doc['files']) == 10, 'manifest format/count')
    names = set(doc['files']) | {'MANIFEST.json'}
    need({p.name for p in root.iterdir()} == names, 'input file set mismatch')
    for name in names:
        path = root / name
        need(path.is_file() and not path.is_symlink(), 'nonregular input entry')
        if name == 'MANIFEST.json':
            continue
        b = path.read_bytes()
        need(len(b) == doc['files'][name]['bytes'], 'payload byte count mismatch')
        need(sha(b) == doc['files'][name]['sha256'], 'payload hash mismatch')
    return {'manifest_sha256': sha(blob), 'manifest_bytes': len(blob),
            'payload_files': doc['files'], 'payload_count': 10,
            'total_payload_bytes': sum(v['bytes'] for v in doc['files'].values())}


def weights(points=P):
    return {(i, j): (points[i][0] - points[j][0]) ** 2
            + (points[i][1] - points[j][1]) ** 2 for i, j in EDGES}


def degree_vector(edges):
    result = [0] * 6
    for i, j in edges:
        result[i] += 1
        result[j] += 1
    return result


def connected(edges):
    seen = {0}
    while True:
        old = set(seen)
        for i, j in edges:
            if i in seen or j in seen:
                seen.update((i, j))
        if seen == old:
            return len(seen) == 6


def is_cycle(edges):
    return (len(edges) == 6 and len(set(edges)) == 6
            and all(e in EDGES for e in edges)
            and degree_vector(edges) == [2] * 6 and connected(edges))


def held_karp(d, start):
    """Subset dynamic programming, not permutation or edge-set enumeration."""
    state = {(1 << start, start): 0}
    for size in range(1, 6):
        for (mask, last), value in list(state.items()):
            if mask.bit_count() != size:
                continue
            for nxt in range(6):
                if mask & (1 << nxt):
                    continue
                key = (mask | (1 << nxt), nxt)
                new_value = value + d[tuple(sorted((last, nxt)))]
                if key not in state or new_value < state[key]:
                    state[key] = new_value
    terminals = {last: value for (mask, last), value in state.items() if mask == 63}
    return min(terminals.values()), min(value + d[tuple(sorted((last, start)))]
                                        for last, value in terminals.items())


def independently_compute():
    d = weights()
    norms = [x*x + y*y for x, y in P]
    need(len(set(P)) == 6 and all(v < 10000 for v in norms), 'point geometry')
    minima = {}
    for a, b in ((0, 1), (0, 2), (1, 2)):
        minima[f'{a}-{b}'] = min(v for (i, j), v in d.items()
                                  if i // 2 == a and j // 2 == b)
    need(minima == {'0-1': 27914, '0-2': 27914, '1-2': 27556}, 'cluster distances')
    cycles = []
    degree_two = 0
    crossing_hist = Counter()
    cost_hist = Counter()
    for edge_set in itertools.combinations(EDGES, 6):
        if degree_vector(edge_set) != [2] * 6:
            continue
        degree_two += 1
        if not connected(edge_set):
            continue
        need(is_cycle(edge_set), 'cycle classifier disagreement')
        crossing = sum(i // 2 != j // 2 for i, j in edge_set)
        cuts = [sum((i // 2 == k) != (j // 2 == k) for i, j in edge_set)
                for k in range(3)]
        need(all(c >= 2 and c % 2 == 0 for c in cuts), 'cluster cut argument')
        need(sum(cuts) == 2 * crossing and crossing >= 3, 'cut double counting')
        value = sum(d[e] for e in edge_set)
        need(value >= 3 * 27556 > 80000, 'tour lower bound')
        cycles.append((value, edge_set))
        crossing_hist[crossing] += 1
        cost_hist[value] += 1
    need(len(cycles) == 60 and degree_two == 70, 'edge subset exhaustiveness')
    matchings = [e for e in itertools.combinations(EDGES, 3)
                 if degree_vector(e) == [1] * 6]
    matching_values = [sum(d[e] for e in m) for m in matchings]
    need(len(matchings) == 15 and min(matching_values) == 3, 'matching enumeration')
    dp = [held_karp(d, s) for s in range(6)]
    optimum = min(c[0] for c in cycles)
    need(optimum == 83678 and all(closed == optimum for _, closed in dp),
         'independent DP crosscheck')
    witness = (0, 1, 2, 3, 5, 4)
    we = tuple(tuple(sorted((witness[i], witness[(i+1) % 6]))) for i in range(6))
    need(is_cycle(we) and sum(d[e] for e in we) == optimum, 'attaining witness')
    matching_min = min(matching_values)
    need(min(d.values()) == 1 and matching_min == 3 * min(d.values()),
         'analytic matching optimum')
    return {'arithmetic': 'integers and rational fractions only',
            'points': [list(p) for p in P], 'coordinate_denominator': 100,
            'norm_squared_numerators': norms, 'distance_squared_denominator': 10000,
            'pair_distance_squared_numerators': {f'{i}-{j}': v for (i, j), v in d.items()},
            'cluster_pair_minimum_numerators': minima,
            'intercluster_squared_minimum': str(Q(27556, 10000)),
            'analytic_tour_lower_bound': str(Q(3 * 27556, 10000)),
            'analytic_margin_over_8': str(Q(3 * 27556, 10000) - 8),
            'edge_subsets_examined': math.comb(15, 6), 'degree_two_edge_sets': degree_two,
            'disconnected_two_triangle_edge_sets_rejected': degree_two - len(cycles),
            'undirected_cycle_count': len(cycles),
            'tour_cost_numerator_histogram': dict(sorted(cost_hist.items())),
            'crossing_edge_count_histogram': dict(sorted(crossing_hist.items())),
            'tour_optimum': str(Q(optimum, 10000)),
            'optimal_undirected_cycle_count': sum(v == optimum for v, _ in cycles),
            'optimal_cycle_edge_sets': [[list(e) for e in es] for v, es in cycles if v == optimum],
            'witness': list(witness), 'witness_edge_numerators': [d[e] for e in we],
            'held_karp_closed_optimum_numerators_by_start': [c for _, c in dp],
            'open_path_minimum': str(Q(min(p for p, _ in dp), 10000)),
            'radius_half_tour_minimum': str(Q(optimum, 40000)),
            'matching_subsets_examined': math.comb(15, 3), 'perfect_matching_count': len(matchings),
            'matching_cost_numerators': sorted(matching_values),
            'matching_optimum': str(Q(matching_min, 10000))}


def check_certificate(cert, result):
    expected = {'point_numerators': [list(p) for p in P], 'coordinate_denominator': 100,
                'clusters': [[0, 1], [2, 3], [4, 5]],
                'intercluster_squared_minimum': result['intercluster_squared_minimum'],
                'analytic_tour_lower_bound': result['analytic_tour_lower_bound'],
                'undirected_tour_count': result['undirected_cycle_count'],
                'minimum_squared_tour_cost': result['tour_optimum'],
                'minimum_squared_matching_cost': result['matching_optimum']}
    for key, value in expected.items():
        need(cert[key] == value, 'incorrect certificate field: ' + key)
    witness = cert['optimal_tour']
    need(sorted(witness) == list(range(6)), 'witness not a vertex permutation')
    edges = tuple(tuple(sorted((witness[i], witness[(i+1) % 6]))) for i in range(6))
    need(is_cycle(edges) and sum(weights()[e] for e in edges) == 83678, 'bad witness')


def expect_rejection(fn, label):
    try:
        fn()
    except ValueError:
        return label
    raise RuntimeError('Negative control incorrectly passed: ' + label)


def negative_controls(root, result):
    rejected = []
    cert = json.loads((root / 'CERTIFICATE.json').read_bytes())
    for key, wrong in [('minimum_squared_tour_cost', '8'),
                       ('analytic_tour_lower_bound', '9'),
                       ('undirected_tour_count', 59),
                       ('minimum_squared_matching_cost', '5'),
                       ('coordinate_denominator', 200),
                       ('optimal_tour', [0, 1, 2, 3, 4, 4])]:
        bad = copy.deepcopy(cert)
        bad[key] = wrong
        rejected.append(expect_rejection(lambda: check_certificate(bad, result),
                                         'reject certificate ' + key))
    two_triangles = ((0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5))
    rejected.append(expect_rejection(lambda: need(is_cycle(two_triangles), 'disconnected'),
                                     'reject disconnected 2-factor'))
    open_witness = ((0, 1), (1, 2), (2, 3), (3, 5), (4, 5))
    rejected.append(expect_rejection(lambda: need(is_cycle(open_witness), 'unclosed'),
                                     'reject path without closing edge'))
    need(Q(result['open_path_minimum']) < 8 and Q(result['radius_half_tour_minimum']) < 8,
         'model-change controls did not differ')
    for mode in ('payload byte', 'extra file', 'missing file', 'payload symlink',
                 'manifest symlink', 'nested directory', 'reauthored manifest'):
        with tempfile.TemporaryDirectory(prefix='tour-audit-') as tmp:
            dest = Path(tmp) / 'packet'
            shutil.copytree(root, dest)
            proof = dest / 'PROOF.md'
            manifest = dest / 'MANIFEST.json'
            if mode == 'payload byte':
                proof.write_bytes(proof.read_bytes() + b'\n')
            elif mode == 'extra file':
                (dest / 'extra.txt').write_text('extra')
            elif mode == 'missing file':
                proof.unlink()
            elif mode == 'nested directory':
                (dest / 'nested').mkdir()
            elif mode in ('payload symlink', 'manifest symlink'):
                target = proof if mode == 'payload symlink' else manifest
                saved = Path(tmp) / 'outside-copy'
                saved.write_bytes(target.read_bytes())
                target.unlink()
                target.symlink_to(saved)
            else:
                proof.write_bytes(proof.read_bytes() + b'\n')
                doc = json.loads(manifest.read_bytes())
                b = proof.read_bytes()
                doc['files']['PROOF.md'] = {'bytes': len(b), 'sha256': sha(b)}
                manifest.write_text(json.dumps(doc))
            rejected.append(expect_rejection(lambda: binding(dest), 'reject ' + mode))
    return {'rejected_count': len(rejected), 'rejections': rejected,
            'model_change_controls': ['open paths have minimum below 8',
                                      'radius-half scaling gives minimum below 8']}


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    before = binding(root)
    computed = independently_compute()
    check_certificate(json.loads((root / 'CERTIFICATE.json').read_bytes()), computed)
    controls = negative_controls(root, computed)
    after = binding(root)
    need(before == after, 'input changed during audit')
    print(json.dumps({'binding': before, 'computed': computed, 'negative_controls': controls,
                      'input_unchanged': True, 'result': 'PASS_SCOPED_PARTIAL_COUNTEREXAMPLE'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
