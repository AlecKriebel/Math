#!/usr/bin/env python3
"""Check audit byte identities and correction application; not a proof checker."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import sys

here = Path(__file__).resolve().parent
frozen = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else here.parent / 'rank572-2303022' / 'public'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def entries(path):
    for line in path.read_text().splitlines():
        digest, name = line.split('  ', 1)
        yield digest, name
assert sha(frozen / 'SHA256SUMS') == 'b5ab673a48038729e817852896c54a8467857461d280acc703f8df7c2bcd2903'
for digest, name in entries(frozen / 'SHA256SUMS'):
    assert sha(frozen / name) == digest, name
for digest, name in entries(here / 'SHA256SUMS'):
    assert sha(here / name) == digest, name
assert (here / 'replayed-verification.json').read_bytes() == (frozen / 'controls/verification_results.json').read_bytes()
assert (here / 'replayed-two-arcs.json').read_bytes() == (frozen / 'controls/two_arcs_results.json').read_bytes()
assert json.loads((here / 'replayed-verification.json').read_text())['checks_count'] == 27
with tempfile.TemporaryDirectory(prefix='radial-obstacle-audit-') as d:
    p = Path(d)
    (p / 'proof.md').write_bytes((frozen / 'proof.md').read_bytes())
    subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(here / 'corrections.patch')], cwd=p, check=True, capture_output=True)
    assert (p / 'proof.md').read_bytes() == (here / 'corrected-proof.md').read_bytes()
for digest, name in entries(here / 'corrected-public-SHA256SUMS'):
    source = here / 'corrected-proof.md' if name == './proof.md' else frozen / name
    assert sha(source) == digest, name
r = json.loads((here / 'audit_results.json').read_text())
assert r['frozen_manifest_sha256'] == sha(frozen / 'SHA256SUMS')
assert r['original_proof_sha256'] == sha(frozen / 'proof.md')
assert r['corrected_proof_sha256'] == sha(here / 'corrected-proof.md')
assert r['corrections_patch_sha256'] == sha(here / 'corrections.patch')
assert r['corrected_public_manifest_sha256'] == sha(here / 'corrected-public-SHA256SUMS')
assert r['report_sha256'] == sha(here / 'AUDIT.md')
assert r['frozen_verdict'] == 'CORRECTION_REQUIRED'
assert r['corrected_bundle_verdict'] == 'PASS_UNRESOLVED_CHECKPOINT'
print('PASS: frozen identities; audit manifest; 27-check replay identity; PDE replay identity; exact patch application; corrected bundle manifest; audit metadata. No analytical or continuum certification is implied.')
