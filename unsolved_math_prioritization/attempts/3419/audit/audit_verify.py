#!/usr/bin/env python3
"""Replay a frozen packet and check independent finite algebra controls.

Usage: python3 audit_verify.py [public-directory]
Finite arithmetic does not certify the topological or infinite-group claims.
"""
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys

EXPECTED = 'acc47454c1010668f2edce71c227d55e0202b14e317b1960052decc1c121b88a'
public = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'public'
manifest = (public / 'SHA256SUMS').read_bytes()
assert hashlib.sha256(manifest).hexdigest() == EXPECTED
verified = []
for line in manifest.decode().splitlines():
    digest, name = line.split(maxsplit=1)
    name = name.lstrip('*')
    assert Path(name).name == name
    assert hashlib.sha256((public / name).read_bytes()).hexdigest() == digest
    verified.append(name)
replay = subprocess.run([sys.executable, 'verify.py'], cwd=public, check=True, capture_output=True).stdout
assert replay == (public / 'verification.json').read_bytes()
data = json.loads(replay)
assert data['total_assertions'] == 35453

# Independent determinant-by-permutations, with no Gaussian elimination.
def determinant(a):
    n = len(a)
    assert all(len(row) == n for row in a)
    total = 0
    for p in itertools.permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        term = -1 if inversions % 2 else 1
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total

def minor_rank(a):
    for k in range(min(len(a), len(a[0])), 0, -1):
        for rows in itertools.combinations(range(len(a)), k):
            for cols in itertools.combinations(range(len(a[0])), k):
                if determinant([[a[i][j] for j in cols] for i in rows]):
                    return k
    return 0

controls = {}
controls['gamma1_h1_difference_rank'] = minor_rank([[3,0,3,0],[0,-3,0,-3]])
assert controls['gamma1_h1_difference_rank'] == 2
controls['single_s_h1_difference_rank'] = minor_rank([[3,0],[0,-3]])
assert controls['single_s_h1_difference_rank'] == 2
controls['perfect_container_h2_difference_determinant'] = determinant([[1,1],[-1,0]])
assert controls['perfect_container_h2_difference_determinant'] == 1
chain = [2]
chain += [chain[-1] + (5-2)]
chain += [chain[-1] + 2]
chain += [chain[-1]]
chain += [chain[-1] - 3]
chain += [chain[-1] - 2]
assert chain == [2,5,7,7,4,2]
controls['frozen_b2_lower_bound_chain'] = chain

# Conditional arithmetic only: the inputs here are proved in the supplement.
delta = [0]
for edge_b1, upper_rank_h2 in [(5,0),(2,0),(3,0),(3,3),(3,2)]:
    delta.append(delta[-1] + edge_b1 - upper_rank_h2 - 1)
assert delta == [0,4,5,7,6,6]
controls['supplement_delta_lower_bound_chain'] = delta
lower = delta[-1] + 1
upper = 9 - (3-1)
assert lower == upper == 7
controls['supplement_b2_lower_and_upper'] = [lower,upper]

out = {
    'target': '3419 / OPG-37237',
    'date': '2026-10-03',
    'frozen_manifest_sha256': EXPECTED,
    'verified_artifacts': verified,
    'replay_byte_identical': True,
    'replayed_assertions': data['total_assertions'],
    'independent_finite_controls': controls,
    'audit_verdict': 'Accept as unresolved with valid partial results; no blocking mathematical error found.',
    'full_solution_certified': False,
    'scope': 'Finite controls and exact replay only. Mathematical claims depend on the written proofs and cited injective HNN constructions.'
}
print(json.dumps(out, indent=2, sort_keys=True))
