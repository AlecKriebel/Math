#!/usr/bin/env python3
"""Check the frozen public packet's file allowlist and SHA-256 manifest."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
expected={
 'README.md','SOURCE_GATE.md','ATTEMPT_LOG.md','DISPOSITION.json',
 'TURN_01_CHARACTER_REDUCTION.md','TURN_02_ALL_GRAPH_DEGREE_P.md',
 'TURN_03_FOREST_SUPPORTS.md','TURN_04_SMALL_MATCHING_NUMBER.md',
 'TURN_05_HIGHER_RANK_GAP.md','verify.py','verify_bundle.py','VERIFICATION.json',
 'MANIFEST.sha256'
}
actual={p.name for p in root.iterdir() if p.is_file()}
assert actual==expected,('file allowlist mismatch',actual^expected)
seen=set()
for line in (root/'MANIFEST.sha256').read_text().splitlines():
    digest,name=line.split('  ',1)
    assert name in expected-{'MANIFEST.sha256'} and name not in seen
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
    seen.add(name)
assert seen==expected-{'MANIFEST.sha256'}
print('PASS: exact public allowlist and all SHA-256 digests verified')
