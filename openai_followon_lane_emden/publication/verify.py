#!/usr/bin/env python3
"""Check included analytic source hashes, scaling algebra, interval diagnostics.

No PDE theorem is inferred from these finite or floating-point checks.
"""
from fractions import Fraction
from pathlib import Path
import hashlib, json, subprocess, sys

root = Path(__file__).resolve().parent
manifest = json.loads((root/'sources/SOURCE_HASHES.json').read_text())
checked = []
for rel, identity in manifest['files'].items():
    if rel in ('sources/pqs1.pdf', 'sources/pqs1.txt'):
        continue  # Research copy excluded for redistribution-rights reasons.
    path = root/rel
    assert path.is_file(), rel
    data = path.read_bytes()
    assert len(data) == identity['bytes'], rel
    assert hashlib.sha256(data).hexdigest() == identity['sha256'], rel
    checked.append(rel)

count = 0
for n in range(3, 21):
    for p in (Fraction(5,4), Fraction(3,2), Fraction(2), Fraction(3), Fraction(7), Fraction(20)):
        for q in (Fraction(6,5), Fraction(4,3), Fraction(2), Fraction(4), Fraction(9), Fraction(30)):
            alpha, beta = 2*(p+1)/(p*q-1), 2*(q+1)/(p*q-1)
            a,b = 1/(q+1), 1/(p+1)
            assert p*beta == alpha+2 and q*alpha == beta+2
            assert n*(a+b)-(n-2) == (1-a-b)*(alpha+beta+2-n)
            assert (a+b > Fraction(n-2,n)) == (alpha+beta>n-2)
            count += 1
raw = subprocess.check_output([sys.executable,str(root/'notes/upstream_interval_checks.py')],text=True)
diagnostics = json.loads(raw)
assert diagnostics['finite_case_count'] == 614
print(json.dumps({'checked_source_files':checked,'rational_scaling_cases':count,
                  'interval_diagnostics':diagnostics,
                  'interpretation':'hash/algebra checks and floating-point falsification diagnostics; not PDE formalization'},indent=2))
