#!/usr/bin/env python3
"""Verify frozen inputs/family artifacts and the two exact prior spectra.

This is a read-only reproduction/priority-control check. It does not prove the
irrational-period or global-attractor assertions numerically; those are proved
in PRIOR_SPECIALIZATION_PROOF.md. Guards remain active under Python -O.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

D = Path(__file__).resolve().parent
A = D.parent
checks = 0


def require(condition, label):
    global checks
    if not condition:
        raise ValueError(label)
    checks += 1


def pin(path, size, sha):
    require(path.is_file() and not path.is_symlink(), str(path) + ': regular file')
    body = path.read_bytes()
    require(len(body) == size, str(path) + ': byte length')
    require(hashlib.sha256(body).hexdigest() == sha, str(path) + ': SHA256')
    return body


frozen = [
    ('repaired_diagnostics_v2/COUNTEREXAMPLE.md', 10969,
     '0e2e4e1484193c304cb2394142e24460c89a50f6ab3bb58ad838624cabb9035f'),
    ('original_head_authentication_20261006/SOURCE_STATEMENT.json', 2446,
     '0608b99bef6677de34d98e2e59e0b05651e4e3af82c14b051ac8a6d443a38688'),
    ('original_head_authentication_20261006/PRIOR_REPORT.md', 3020,
     'a92cd3d3b62e90b9e3ad1c12c60b80eb88615b210fd89101aa95298dd5538c2b'),
]
for path, size, sha in frozen:
    pin(A / path, size, sha)

families = [
    ('historical_priority_adversary_20261006', 3369,
     '8b1d7fbd3a0689f8a948fbf57b97290345d67dd7c0ce18cd4cc92c0a22fb4a63'),
    ('modern_citation_priority_adversary_20261006', 3666,
     '01e700d352ef44dd9ef53c20d95abee9c8de14ec88428dd7673bab23e9cdc7d5'),
    ('quasiperiodic_counterexample_priority_20261006', 2356,
     '4200a96d2f8a9e50609ad73baa09a479ff90f2b2f6474c722ddd0e519fb40431'),
]
family_counts = {}
for folder, size, sha in families:
    base = A / folder
    manifest = json.loads(pin(base / 'OUTPUT_MANIFEST.json', size, sha))
    seen = set()
    for item in manifest['members']:
        path = item['path']
        require(path not in seen and '/' not in path and path not in ('.', '..'),
                folder + ': unique flat member')
        seen.add(path)
        pin(base / path, item['bytes'], item['sha256'])
    family_counts[folder] = len(seen)


def dimension(rates):
    rates = sorted(map(Fraction, rates), reverse=True)
    sums = [Fraction(0)]
    for rate in rates:
        sums.append(sums[-1] + rate)
    j = max(k for k, total in enumerate(sums) if total >= 0)
    require(j < len(rates), 'negative final sum')
    return j, Fraction(j) + sums[j] / -rates[j], sums[1:]


intrinsic = dimension([0, 0, -1])
ambient = dimension([0, 0, 0, 0, -1])
require(intrinsic == (2, Fraction(2), [0, 0, -1]), 'intrinsic exact dimension')
require(ambient == (4, Fraction(4), [0, 0, 0, 0, -1]), 'ambient exact dimension')
require(sum([0, 0, -1]) == -1, 'intrinsic divergence')
require(sum([0, 0, 0, 0, -1]) == -1, 'ambient divergence')
require(intrinsic[1] != ambient[1], 'do not conflate tangent conventions')
require(Fraction(63459, 15625) - Fraction(203, 50) == Fraction(43, 31250),
        'v2 transient exceeds asymptotic maximum')

print(json.dumps({
    'status': 'PASS',
    'explicit_guards': checks,
    'original_inputs_authenticated': len(frozen),
    'family_manifest_members_authenticated': family_counts,
    'total_family_members_authenticated': sum(family_counts.values()),
    'intrinsic_spectrum': ['0', '0', '-1'],
    'intrinsic_dimension': '2',
    'ambient_spectrum': ['0', '0', '0', '0', '-1'],
    'ambient_dimension': '4',
    'priority_clearance': False,
    'new_central_proof_search': False,
    'irrationality_and_global_attractor_proved_in_text': True,
}, sort_keys=True, indent=2))
