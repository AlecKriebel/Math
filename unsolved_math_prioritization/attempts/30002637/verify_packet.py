#!/usr/bin/env python3
"""Verify portable inventory, frozen proof/audit binding, and algebra replays."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
expected = {x['path']: x for x in manifest['files']}
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual == set(expected) | {'MANIFEST.json'}, ('inventory', sorted(actual ^ (set(expected) | {'MANIFEST.json'})))
for name, item in expected.items():
    path = root / name
    assert not path.is_symlink(), name
    data = path.read_bytes()
    assert len(data) == item['bytes'], name
    assert hashlib.sha256(data).hexdigest() == item['sha256'], name
frozen = root / 'frozen'
frozen_manifest = frozen / 'FROZEN_MANIFEST.json'
assert hashlib.sha256(frozen_manifest.read_bytes()).hexdigest() == '316936e91c184fbc7a6c9b605cfee994a095183b00f75b3e1ca5df3356245f11'
fm = json.loads(frozen_manifest.read_text())
for item in fm['files']:
    data = (frozen / item['path']).read_bytes()
    assert len(data) == item['bytes']
    assert hashlib.sha256(data).hexdigest() == item['sha256']
audit = root / 'review' / 'INDEPENDENT_AUDIT.md'
assert hashlib.sha256(audit.read_bytes()).hexdigest() == 'aeda74884bc71b21df150b08ad278c0d39e496df37f896ab6570736623b8757f'
verdict = json.loads((root / 'review' / 'AUDIT_RESULT.json').read_text())
assert verdict['audit_report'] == 'INDEPENDENT_AUDIT.md'
assert verdict['audit_report_sha256'] == hashlib.sha256(audit.read_bytes()).hexdigest()
assert verdict['verdict'] == 'PASS_PARTIAL_RESULTS_ONLY'
assert verdict['original_target'] == 'unresolved_by_packet'
assert verdict['required_mathematical_repairs'] == []
results = {}
for name, script, receipt in [
    ('author', frozen / 'check_algebra.py', frozen / 'ALGEBRA_RECEIPT.json'),
    ('independent_audit', root / 'review' / 'audit_checks.py', root / 'review' / 'audit_checks.json'),
]:
    result = subprocess.run([sys.executable, str(script)], cwd=root, check=True, capture_output=True, text=True)
    parsed = json.loads(result.stdout)
    assert parsed == json.loads(receipt.read_text()), name
    results[name] = parsed['count']
ledger = json.loads((frozen / 'TURN_LEDGER.json').read_text())
assert ledger['turns_used'] == 5 and len(ledger['turns']) == 5
assert all(t['attempt_completed'] for t in ledger['turns'])
assert ledger['full_target_status'] == 'unresolved'
print(json.dumps({'inventory_files_verified': len(expected), 'frozen_files_verified': len(fm['files']),
    'audit_binding': 'PASS', 'algebra_checks': results, 'original_target': 'unsolved',
    'turns': '5/5', 'scope': 'Integrity and exact algebra only; mathematical audit is included separately.'}, indent=2))
