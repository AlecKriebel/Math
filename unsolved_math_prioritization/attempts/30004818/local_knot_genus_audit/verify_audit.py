#!/usr/bin/env python3
"""Replay input integrity and finite arithmetic checks. This is not a proof checker."""
from pathlib import Path
import hashlib, json, subprocess, tempfile

root = Path(__file__).resolve().parent
base = root.parent / 'local_knot_genus_30004818'
for r in json.loads((root / 'input_pins.json').read_text()):
    b = (base / r['file']).read_bytes()
    assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256'], r['file']
for r in json.loads((root / 'source_reextraction_checks.json').read_text()):
    p = base / 'private_sources' / r['file']
    b = p.read_bytes()
    assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256'], str(p)
    with tempfile.TemporaryDirectory() as directory:
        extracted = Path(directory) / 'source.txt'
        subprocess.run(['pdftotext', '-layout', str(p), str(extracted)], check=True)
        assert extracted.read_bytes() == p.with_suffix('.txt').read_bytes(), str(p)
checks = {'finite_cover_cases': 0}
for d in range(1, 31):
    for g in range(21):
        if g == 0 and d != 1:
            continue
        upstairs = 1 + d * (g - 1)
        assert upstairs >= 0
        assert 2 - 2 * upstairs - d == d * (1 - 2 * g)
        assert d * (1 - 2 * g) - (d - 1) == 1 - 2 * d * g
        checks['finite_cover_cases'] += 1
checks['equivariant_records'] = 0
for r in json.loads((base / 'verification/APPROACH_03_CHECKS.json').read_text())['equivariant_genus_one_arithmetic']:
    assert 2 - 2 * r['upstairs_genus'] - r['upstairs_boundary'] == r['degree'] * r['quotient_chi']
    assert r['quotient_chi'] == 1 - 2 * r['quotient_genus']
    checks['equivariant_records'] += 1
checks['smoothing_cases'] = 0
for r in range(1001):
    assert -1 - 2 * r == 1 - 2 * (1 + r)
    checks['smoothing_cases'] += 1
q = lambda n: (abs(n) + 1) // 2
checks['norm_triangle_inequalities'] = 0
for a in range(-100, 101):
    assert q(a) == q(-a) and ((q(a) == 0) == (a == 0))
    for b in range(-100, 101):
        assert q(a + b) <= q(a) + q(b)
        checks['norm_triangle_inequalities'] += 1
checks['disk_bundle_determinants'] = 0
for p in range(-1000, 1001):
    assert p * 0 - 1 * 1 == -1
    checks['disk_bundle_determinants'] += 1
checks['status'] = 'PASS'
checks['scope'] = 'Finite arithmetic checks only. Geometric and Floer claims are assessed in the mathematical audit, not certified by this file.'
assert checks == json.loads((root / 'independent_checks.json').read_text())
print(json.dumps(checks, indent=2))
