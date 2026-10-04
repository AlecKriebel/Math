#!/usr/bin/env python3
"""Independent finite audit; standard library only. Does not modify the packet.

Usage: python3 verify_independent.py ../public > verification.json
The written mathematics, not these finite checks, establishes infinite claims.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product, accumulate
from math import isqrt
from pathlib import Path
import json
import subprocess
import sys

ANCHOR = '58a8e9903b32eb6a5f918fbc150194cc359c8288e96cef3b568a793e4320c1c5'
EXPECTED_NAMES = {'ATTEMPT_LOG.md', 'PROOF.md', 'README.md', 'SOURCE_GATE.md',
                  'SOURCE_HASHES.json', 'STATUS.json', 'verification.json', 'verify.py'}


def packet_integrity(root):
    raw = (root / 'SHA256SUMS').read_bytes()
    assert sha256(raw).hexdigest() == ANCHOR
    listed = []
    for line in raw.decode().splitlines():
        digest, name = line.split('  ', 1)
        assert name in EXPECTED_NAMES
        assert sha256((root / name).read_bytes()).hexdigest() == digest
        listed.append(name)
    assert len(listed) == len(set(listed)) == 8
    assert set(listed) == EXPECTED_NAMES
    assert {p.name for p in root.iterdir() if p.is_file()} == EXPECTED_NAMES | {'SHA256SUMS'}
    status = json.loads((root / 'STATUS.json').read_text())
    assert status['status'] == 'unresolved'
    assert status['substantive_attempts'] == 5
    assert status['auxiliary_propositions'] == 6
    assert status['full_resolution_claimed'] is False
    assert status['general_counterexample_claimed'] is False
    return {'manifest_sha256': ANCHOR, 'entries': 8, 'passed': True}


def records():
    total = eligible = count_good = 0
    for length in range(1, 7):
        for a in product([-2, 0, 1, 3], repeat=length):
            total += 1
            sums = [0, *accumulate(a)]
            adjusted = [Q(s) - Q(j, 2) for j, s in enumerate(sums)]
            strict = [j for j in range(1, length + 1)
                      if all(adjusted[j] > adjusted[k] for k in range(j))]
            # Enumerate all suffix inequalities directly, independently of records.
            good = [j for j in range(1, length + 1)
                    if all(sum(a[k:j]) >= Q(j-k, 2) for k in range(j))]
            assert set(strict) <= set(good)
            count_good += len(good)
            for j in strict:
                assert adjusted[j] - max(adjusted[:j]) <= Q(5, 2)
            if sum(a) >= length:
                eligible += 1
                assert len(strict) >= Q(length, 5)
                assert len(good) >= Q(length, 5)
    assert (total, eligible) == (5460, 1644)
    return {'sequences': total, 'average_eligible': eligible,
            'all_suffix_valid_indices': count_good, 'max_length': 6}


def dyadic():
    # Construct losses by powers of two instead of testing individual indices.
    a = [1] * 4096
    for exponent in range(2, 13):
        a[2**exponent-1] -= 2**(exponent-2)
    sums = list(accumulate(a))
    adjusted = [0] + [4*s - n for n, s in enumerate(sums, 1)]
    high = 0
    record_count = 0
    for n, s in enumerate(sums, 1):
        if n >= 4:
            # Sum over all spikes already encountered, directly.
            losses = sum(2**(k-2) for k in range(2, 13) if 2**k <= n)
            assert s == n - losses
            assert s == n - (2**((n.bit_length()-1)-1) - 1)
        assert Q(s, n) >= Q(1, 2)
        if adjusted[n] > high:
            assert adjusted[n] - high <= 3
            high = adjusted[n]
            record_count += 1
        assert 3*record_count >= n
    tails = {}
    for cutoff in (1, 4, 16, 64):
        tail = sum(-v for v in a if v < -cutoff)
        assert Q(tail, 4096) >= Q(1, 4) - Q(1, 4096)
        tails[str(cutoff)] = str(Q(tail, 4096))
    for k in range(2, 13):
        n = 2**k
        assert Q(a[n-1], n) == Q(1, n) - Q(1, 4)
        assert Q(sums[n-1], n) == Q(1, 2) + Q(1, n)
    assert record_count == 2736
    return {'terms': len(a), 'record_times_c_1_4': record_count,
            'negative_tail_ratios_at_4096': tails}


def direct_vertex(word):
    # Sum the prescribed post-first-one drops, rather than min/max formula.
    first = next((j for j, bit in enumerate(word, 1) if bit), None)
    if first is None:
        return Q(1)
    return Q(1) - sum((Q(1, first+1) for level in range(first+1, len(word)+1)
                       if level <= 2*first), Q(0))


def tree():
    count = 0
    for n in range(1, 11):
        for w in product([0, 1], repeat=n):
            count += 1
            difference = abs(direct_vertex(w) - direct_vertex(w[:-1]))
            assert difference <= Q(2, n+2)
            if 1 in w:
                k = w.index(1)+1
                expected = Q(1, k+1) if k < n <= 2*k else Q(0)
                assert difference == expected
    endpoint_checks = 0
    for k in range(1, 65):
        for n in range(2*k, 2*k+6):
            word = (0,)*(k-1) + (1,) + (0,)*(n-k)
            assert direct_vertex(word) == Q(1, k+1)
            endpoint_checks += 1
        assert direct_vertex((0,)*(2*k)) == 1
    assert count == 2046
    return {'edges': count, 'max_generation': 10,
            'first_one_positions': 64, 'stabilized_endpoint_tests': endpoint_checks}


def square_digits():
    count = 0
    for n in (32, 64, 128, 256, 512, 1024):
        for m in range(1, 13):
            # A one at position s affects shifts j in [s-m,s-1].
            shifts = set()
            for k in range(1, isqrt(n+m)+1):
                square = k*k
                shifts.update(range(max(0, square-m), min(n, square)))
            brute = {j for j in range(n) if any(isqrt(j+t)**2 == j+t
                                               for t in range(1, m+1))}
            assert shifts == brute
            assert len(shifts) <= m*(isqrt(n+m)+1)
            count += 1
    assert count == 72
    return {'window_tests': count, 'max_N': 1024, 'max_window': 12}


def monomials():
    count = 0
    for d in range(2, 11):
        degree = 1
        chain_coefficient = 1
        exponent = 0
        for n in range(1, 11):
            chain_coefficient *= d
            exponent += (d-1)*degree
            degree *= d
            assert exponent == degree-1
            assert chain_coefficient == degree == d**n
            assert degree > 1
            count += 1
    return {'chain_rule_controls': count}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '../public')
    integrity = packet_integrity(root)
    frozen_output = subprocess.check_output([sys.executable, str(root / 'verify.py')], text=True)
    frozen = json.loads(frozen_output)
    saved = json.loads((root / 'verification.json').read_text())
    assert frozen == saved
    independent = {'record_times': records(), 'dyadic_sequence': dyadic(),
                   'abstract_tree': tree(), 'square_digits': square_digits(),
                   'monomials': monomials()}
    # Recheck integrity after the independent replay and frozen verifier execution.
    assert packet_integrity(root) == integrity
    result = {'schema_version': 1, 'problem_id': 5300049, 'rank': 545,
              'scope': 'Finite exact controls only; no proof of the original question.',
              'packet_integrity': integrity,
              'frozen_verifier_matches_saved_output': True,
              'independent_replay': independent, 'passed': True}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
