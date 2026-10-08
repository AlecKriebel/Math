# Reproduce the arithmetic audit

This bundle contains authored analysis, code, and public verification metadata only. Scholarly source documents are cited, not included. The full mathematical problem is not solved.

Run with Python 3.10 or later; the standard library is sufficient:

```
python audit.py
python -O audit.py
python audit.py --slope-json '{"p":12,"q":5}'
python audit.py --slope-json '{"p":15,"q":4}'
```

The last example is deliberately unresolved by the published-input tests. A positive conditional-preprint flag has the additional dependencies explained in REPORT.md. “Unresolved by this audit” is not a literature-wide open-status assertion.

Use an externally obtained SHA-256 of MANIFEST.json:

```
python verify.py . --manifest-sha256 EXPECTED_SHA256
```

Do not replace the external pin with a freshly calculated hash of an untrusted manifest. The verifier's own hash should also be checked against a trusted external receipt before executing it. The integrity tool detects changes to a pinned bundle, not whether the pinned mathematics is true. Both scripts operate read-only and write results to stdout. Do not run a modified script merely because its accompanying manifest was also modified.

The slope CLI rejects noninteger, zero, unreduced, malformed, duplicate-key, and unknown-field inputs. The arithmetic script uses explicit checks instead of Python assertions; optimization does not disable them. Boundaries: |p|,q≤100000 for CLI inputs; the fixed self-test grid has |p|≤120,1≤q≤40, p≠0 and gcd(p,q)=1. Grid coverage is never a universal knot proof.

To reproduce the malformed-input and tampering controls, run as a nonroot user:

```
python controls.py . --manifest-sha256 EXPECTED_SHA256
```

This harness writes only temporary copies, makes one copy read-only, and removes its temporary directory when done. It does not edit the input bundle.
