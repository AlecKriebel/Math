#!/usr/bin/env python3
"""Reproducible, read-only audit of the sibling frozen bundle; no topology certification."""
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from math import ceil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / 'bundle'
EXPECTED_MANIFEST = 'ba0d7d679c1b07f93703e7f247b6761091b5435868a3a8515a7c3038666de8fb'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check_frozen():
    assert digest(BUNDLE / 'SHA256SUMS') == EXPECTED_MANIFEST
    entries = {}
    for line in (BUNDLE / 'SHA256SUMS').read_text().splitlines():
        expected, filename = line.split(maxsplit=1)
        filename = filename.removeprefix('*')
        assert Path(filename).name == filename
        actual = digest(BUNDLE / filename)
        assert actual == expected, filename
        entries[filename] = actual
    assert len(entries) == 7
    return entries

def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))

def main():
    before = check_frozen()
    rerun = subprocess.run([sys.executable, str(BUNDLE / 'controls.py')],
                           check=True, text=True, capture_output=True)
    stored = json.loads((BUNDLE / 'CONTROL_RESULTS.json').read_text())
    assert json.loads(rerun.stdout) == stored
    assert rerun.stdout == (BUNDLE / 'CONTROL_RESULTS.json').read_text()
    assert stored['tests']['same_prime_lens_sum_cases'] == 100
    assert stored['tests']['cover_normalization_grid_cases'] == 560

    # Independent presentation-nullity arithmetic, including orders not prime powers.
    lens_cases = 0
    for p in (2, 3, 5, 7, 11):
        for k in range(8):
            for ell in range(8):
                orders = [p * (j + 1) for j in range(ell)]
                nullity = sum(1 for n in orders if n % p == 0)
                assert k + nullity == k + ell
                lens_cases += 1
    mixed = {str(p): sum(n % p == 0 for n in (2, 3))
             for p in (2, 3, 5, 7, 11)}
    assert max(mixed.values()) == 1
    # Concrete noncommuting quotient independently witnesses C2*C3 nonabelian.
    identity, x, y = (0, 1, 2), (1, 0, 2), (1, 2, 0)
    assert compose(x, x) == identity
    assert compose(y, compose(y, y)) == identity
    assert compose(x, y) != compose(y, x)

    cover_cases = 0
    for r in range(1, 21):
        for d in range(1, 31):
            schreier = 1 + d * (r - 1)
            for b in range(schreier + 1):
                bound = Fraction(d + b - 1, d)
                assert bound <= r and ceil(bound) <= r
                assert d * (r - 1) + 1 >= b
                cover_cases += 1
    # Trivial group: only d=1 and b1=0 occur.
    assert Fraction(1 + 0 - 1, 1) == 0
    # Omitting the normalization fails even for the known free-group cover model.
    assert Fraction(2 + 3 - 1, 2) == 2 < 3
    # For the 0-framed Hopf link, the full relation matrix is unimodular.
    H = ((0, 1), (1, 0))
    assert H[0][0]*H[1][1] - H[0][1]*H[1][0] == -1
    assert compose(x, y) != compose(y, x)
    # First filling relation e2=0; e1 maps nontrivially to Z.
    projection = lambda pair: pair[0]
    assert projection((0, 1)) == 0 and projection((1, 0)) == 1
    # Arithmetic of the conditional amalgamation inequality, not its topology.
    amalgamation_cases = 0
    for h in range(9):
        for a in range(h, h + 9):
            for b in range(h, h + 9):
                assert a + b - h >= b
                assert (2 - 2*a) + (2 - 2*b) - (2 - 2*h) == 2 - 2*(a+b-h)
                amalgamation_cases += 1
    after = check_frozen()
    assert before == after
    return {
        'audit_status': 'pass',
        'frozen_manifest_sha256': EXPECTED_MANIFEST,
        'frozen_file_count': len(before),
        'frozen_unchanged': True,
        'original_stdout_matches_record_byte_for_byte': True,
        'original_lens_controls': 100,
        'original_cover_controls': 560,
        'independent_lens_arithmetic_cases': lens_cases,
        'independent_cover_arithmetic_cases': cover_cases,
        'independent_amalgamation_arithmetic_cases': amalgamation_cases,
        'noncommuting_S3_quotient': 'pass',
        'rank_zero_edge_case': 'pass',
        'hopf_quotient_arithmetic': 'pass',
        'limits': [
            'These are exact-arithmetic and integrity checks only.',
            'No manifold is constructed, no Heegaard genus is recognized, and no degree-one map is certified.',
            'No external theorem proof or universal conjecture is certified by computation.'
        ],
        'frozen_files': before,
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
