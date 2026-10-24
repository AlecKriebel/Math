#!/usr/bin/env python3
"""Check the literal Pell witness with only the Python standard library.

No LP, exact solver, author verifier, or enormous array is imported or run.
The finite indexed object is checked by exact interval sweeps and signed counts.
"""
from bisect import bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import reduce
from hashlib import sha256
from math import gcd
from pathlib import Path
import json


EXPECTED_N = 95419250146190292634685757020254542
EXPECTED_PAIRS = ((3, 2), (20, 14), (119, 84))


def integer(x):
    assert type(x) is int or (type(x) is str and x and x.lstrip('-').isdigit()), x
    return int(x)


def partition(intervals, n):
    """Every integer in [0,n) is covered exactly once, not just sampled."""
    cursor = 0
    for start, length, *other in sorted(intervals):
        assert type(start) is type(length) is int
        assert length > 0 and start == cursor, (start, cursor, length)
        cursor += length
    assert cursor == n


def values_on_every_interval(intervals, blocks, left, right):
    """Check every overlap, allowing a supplied segment to cross block edges.

    On a block with coordinates (a,b,t), the value is left*a+right*b+t.
    intervals are (start,length,claimed_value), sorted by index here.
    """
    checks = 0
    ib = 0
    for start, length, label in sorted(intervals):
        end = start + length
        point = start
        while point < end:
            while blocks[ib][0] + blocks[ib][1] <= point:
                ib += 1
            bs, bl, v = blocks[ib]
            assert bs <= point < bs + bl
            assert left*v[0] + right*v[1] + v[2] == label
            point = min(end, bs + bl)
            checks += 1
    return checks


def canonical_order(segments):
    by_value = defaultdict(list)
    for s, d, length, label in segments:
        by_value[label].append((s, d, length))
    for label, pieces in by_value.items():
        last_source_end = last_destination_end = -1
        for s, d, length in sorted(pieces):
            assert s >= last_source_end and d >= last_destination_end
            last_source_end, last_destination_end = s + length, d + length
    return len(by_value)


def locate(block_starts, blocks, i):
    j = bisect_right(block_starts, i) - 1
    bs, length, triple = blocks[j]
    assert bs <= i < bs + length
    return triple


def main():
    root = Path(__file__).resolve().parents[1]
    author = root / 'root_orbit'
    cert_path = author / 'exact_multiset_certificate.json'
    permutation_path = author / 'compressed_permutations.json'
    data = json.loads(cert_path.read_text())
    permutations = json.loads(permutation_path.read_text())
    assert tuple(map(tuple, data['pairs'])) == EXPECTED_PAIRS
    assert data['symmetric_pair_count'] == len(data['support']) == 517
    triples = []
    multiplicities = []
    full_signed_triple_counts = Counter()
    for item in data['support']:
        v = tuple(item['triple'])
        assert len(v) == 3 and all(type(x) is int for x in v)
        m = integer(item['pair_multiplicity'])
        assert m > 0
        triples.append(v)
        multiplicities.append(m)
        full_signed_triple_counts[v] += m
        full_signed_triple_counts[tuple(-x for x in v)] += m
    n = 2 * sum(multiplicities)
    assert n == EXPECTED_N == integer(data['total_list_size']) == integer(permutations['N'])
    assert reduce(gcd, multiplicities) == 1
    assert any(v[0] for v in triples) and any(v[1] for v in triples)
    assert max(abs(v[0]) for v in triples) <= 6
    assert max(abs(v[1]) for v in triples) <= 9
    assert max(abs(v[2]) for v in triples) <= 40

    # Read compressed coordinate blocks and independently identify their multiset.
    blocks = []
    supplied_signed_triple_counts = Counter()
    for block in permutations['blocks']:
        start, length = (integer(block[k]) for k in ('start', 'length'))
        v = tuple(block['triple'])
        assert len(v) == 3 and all(type(x) is int for x in v)
        assert length > 0
        blocks.append((start, length, v))
        supplied_signed_triple_counts[v] += length
    assert len(blocks) == 1034
    partition(blocks, n)
    blocks.sort()
    assert supplied_signed_triple_counts == full_signed_triple_counts
    # Stronger than equality as multisets: verify the specified coordinate order.
    index = 0
    for j, (v, m) in enumerate(zip(triples, multiplicities)):
        assert blocks[2*j] == (index, m, v)
        index += m
        assert blocks[2*j + 1] == (index, m, tuple(-x for x in v))
        index += m
    assert index == n

    results = []
    interval_maps = []
    assert len(permutations['permutations']) == 3
    for (p, q), permutation in zip(EXPECTED_PAIRS, permutations['permutations']):
        assert (permutation['p'], permutation['q']) == (p, q)
        # FULL signed histograms, including every occurrence of zero.
        source = Counter()
        destination = Counter()
        for v, m in full_signed_triple_counts.items():
            source[p*v[0] + v[2]] += m
            destination[q*v[1] + v[2]] += m
        assert sum(source.values()) == sum(destination.values()) == n
        assert source == destination

        segments = [tuple(integer(x) for x in segment)
                    for segment in permutation['segments']]
        assert all(len(s) == 4 for s in segments)
        interval_maps.append(sorted(segments))
        sources = [(s, length, label) for s, d, length, label in segments]
        destinations = [(d, length, label) for s, d, length, label in segments]
        partition(sources, n)
        partition(destinations, n)
        source_checks = values_on_every_interval(sources, blocks, p, 0)
        destination_checks = values_on_every_interval(destinations, blocks, 0, q)
        labels = canonical_order(segments)
        assert labels == len(source)

        # Extra boundary checks of the literal maps and their inverses.
        # These are in addition to the exhaustive interval proof above.
        bstarts = [b[0] for b in blocks]
        boundary_checks = 0
        for s, d, length, label in segments:
            for offset in set((0, length // 2, length - 1)):
                j, image = s + offset, d + offset
                assert image + s - d == j
                u = locate(bstarts, blocks, j)
                v = locate(bstarts, blocks, image)
                assert p*u[0] + u[2] == q*v[1] + v[2] == label
                boundary_checks += 1
        results.append({'p': p, 'q': q, 'signed_projection_values': len(source),
                        'segments': len(segments), 'source_overlap_checks': source_checks,
                        'destination_overlap_checks': destination_checks,
                        'boundary_and_inverse_checks': boundary_checks,
                        'all_signed_counts_equal': True,
                        'both_interval_partitions': True, 'canonical_matching': True,
                        'orientation': 'P e_j=e_{P(j)}; equality verified as u_j=v_{P(j)}'})

    # A concrete noncommutation check, consistent with the earlier abelian
    # obstruction.  The full finite group order is unnecessary.
    def image(which, j):
        pieces = interval_maps[which]
        starts = [s for s, d, length, value in pieces]
        s, d, length, value = pieces[bisect_right(starts, j) - 1]
        assert s <= j < s + length
        return j + d - s
    p1p2 = image(0, image(1, 0))
    p2p1 = image(1, image(0, 0))
    assert p1p2 != p2p1

    # Independent exact second-moment consistency check; no floating point.
    gram = [[sum(m*v[i]*v[j] for v, m in full_signed_triple_counts.items())
             for j in range(3)] for i in range(3)]
    assert gram[0][0] > 0 and gram[1][1] > 0
    for p, q in EXPECTED_PAIRS:
        assert p*p*gram[0][0] + 2*p*gram[0][2] == q*q*gram[1][1] + 2*q*gram[1][2]
    assert gram[1][1] == 2*gram[0][0]
    assert 2*gram[0][2] == gram[0][0]
    assert gram[1][2] == gram[0][0]
    out = {'utc': datetime.now(timezone.utc).isoformat(), 'verdict': 'PASS_EXACT_FINITE_WITNESS',
           'standard_library_only': True, 'author_code_imported': False,
           'support_pairs': len(triples), 'blocks': len(blocks), 'N': str(n),
           'gcd_multiplicities': 1,
           'source_sha256': {cert_path.name: sha256(cert_path.read_bytes()).hexdigest(),
                             permutation_path.name: sha256(permutation_path.read_bytes()).hexdigest()},
           'permutations': results, 'gram_ABT': [[str(x) for x in row] for row in gram],
           'noncommutation': {'j': '0', 'P1P2j': str(p1p2), 'P2P1j': str(p2p1)},
           'vertex_injectivity': 'A and B nonzero, extra coordinate is 0 on a,b and 1 on t',
           'scope': 'positive witness for the specific Pell candidate; no full Kourovka result, no originality certification'}
    Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'verdict': out['verdict'], 'N': str(n), 'support_pairs': len(triples),
                      'permutations': results}, indent=2))


if __name__ == '__main__':
    main()
