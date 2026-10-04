#!/usr/bin/env python3
"""Bounded convention/graph controls. This is not a proof of JKS's theorem."""
import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def normalize(values):
    d = math.gcd(*values)
    if d == 0:
        raise ValueError('zero character is outside admissible HNN scope')
    return tuple(v // d for v in values), d

def schreier_component(modulus, offsets):
    """Component of 0 in the cyclic Schreier graph, with a BFS spanning tree."""
    seen = {0}
    queue = deque([0])
    tree_edges = 0
    while queue:
        u = queue.popleft()
        for a in offsets:
            for v in ((u + a) % modulus, (u - a) % modulus):
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
                    tree_edges += 1
    positive_edges = [(u, i, (u + a) % modulus)
                      for u in sorted(seen) for i, a in enumerate(offsets)]
    assert all(v in seen for _, _, v in positive_edges)
    assert tree_edges == len(seen) - 1
    return len(seen), len(positive_edges), len(positive_edges) - tree_edges

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sources', type=Path,
                    help='Explicitly require/hash the four independently downloaded PDFs')
    args = ap.parse_args()
    counts = Counter()
    for n in range(1, 5):
        for Q in range(1, 7):
            for residues in itertools.product(range(Q), repeat=n):
                for sign in (-1, 1):
                    q = sign * Q
                    prim, d = normalize((*residues, q))
                    assert math.gcd(*prim) == 1
                    V, E, rank = schreier_component(Q, residues)
                    m = Q // d
                    assert V == m
                    assert E == n * m
                    assert rank == 1 + m * (n - 1)
                    assert E - V == rank - 1 == m * (n - 1)
                    assert abs(prim[-1]) == m
                    counts['schreier_characters'] += 1
                    counts['primitive_characters' if d == 1 else 'nonprimitive_characters'] += 1
                    for scale in (2, 3, 5):
                        scaled = tuple(scale * x for x in (*residues, q))
                        norm2, d2 = normalize(scaled)
                        assert norm2 == prim and d2 == scale * d
                        sv, se, sr = schreier_component(scale * Q,
                                                        tuple(scale * x for x in residues))
                        assert (sv, se, sr) == (V, E, rank)
                        counts['scaling_graph_checks'] += 1
    for n in range(1, 9):
        # A=F_(n-1) x Z has 1 vertex, n 1-cells, n-1 2-cells.
        chi_A = 1 - n + (n - 1)
        chi_B = 1 - 1  # Edge Z.
        assert chi_A == chi_B == 0
        assert chi_A - chi_B == 0  # HNN Euler additivity.
        counts['zero_stable_coefficient_cell_checks'] += 1
    for q in list(range(-6, 0)) + list(range(1, 7)):
        # n=0: ker(nonzero multiplication Z->Z)=1.
        _, d = normalize((q,))
        assert d == abs(q)
        b0, b1 = 1, 0
        assert -(b0-b1) == -1
        assert b1 != -(b0-b1)
        counts['rank_zero_negative_controls'] += 1
    for n in range(0, 9):
        try:
            normalize((0,) * (n + 1))
        except ValueError:
            counts['zero_character_rejections'] += 1
        else:
            raise AssertionError('zero character accepted')
    for k, a, b in itertools.product(range(9), repeat=3):
        if k <= a <= b and k == b:
            assert a == k
            counts['squeeze_checks'] += 1
    status = json.loads((ROOT/'STATUS.json').read_text())
    assert status['proposed_status'] == 'already_solved'
    assert status['turns_used'] == 1 and status['turn_limit'] == 5
    assert status['novel_general_solution_claim'] is False
    assert status['publication_status_of_dependency'] == 'preprint'
    assert status['remote_writes_performed'] is False
    sources = json.loads((ROOT/'SOURCE_PROVENANCE.json').read_text())
    source_count = 0
    if args.sources:
        for record in sources['source_pdfs']:
            data = (args.sources / record['filename']).read_bytes()
            assert data.startswith(b'%PDF')
            assert len(data) == record['bytes']
            assert hashlib.sha256(data).hexdigest() == record['sha256']
            source_count += 1
    manifest = ROOT/'MANIFEST.sha256'
    manifest_count = 0
    if manifest.exists():
        actual = {p.name for p in ROOT.iterdir() if p.is_file() and p.name != manifest.name}
        listed = set()
        for line in manifest.read_text().splitlines():
            digest, name = line.split('  ', 1)
            assert Path(name).name == name
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
            listed.add(name)
            manifest_count += 1
        assert actual == listed, (actual-listed, listed-actual)
    print(json.dumps({'result':'PASS','integer_controls':dict(sorted(counts.items())),
                      'source_hashes_checked':source_count,
                      'manifest_payload_files_checked':manifest_count,
                      'limits':['Finite bounded controls only; no general-theorem verification.',
                                'Source-free mode checks no PDF bytes.',
                                'Literature applicability uses cited theorems, not computation.']},
                     indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
