"""Authenticate the source-only gate and release exactly one frozen package."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat

A = Path(__file__).resolve().parent
R = A / 'preprint_review_01'
Q = A / 'preprint_package_v01'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pins = {
    'SOURCE_ONLY_CRITERIA.md': '9e11b10ce198985a65a3f0a612a66e76f9447df144e74ed51da8d12556e0a046',
    'FIRST_INDEPENDENT_CONCLUSION.md': '3d3ff048076968b5fc9ae06ffe0d6636db102156e51f8500b085283b34110f67',
    'SOURCE_ONLY_FREEZE_MANIFEST.json': 'fe8d9a79dbb2396d3ca7a750568f927ac836fce1eeae0e351d5c0152d881ce27',
}
out = A / 'ROOT_PREPRINT01_SOURCE_GATE.json'
assert not out.exists()
for name, digest in pins.items():
    p = R / name
    assert not p.is_symlink() and sha(p) == digest
    assert stat.S_IMODE(p.stat().st_mode) == 0o444
frozen = json.loads((R / 'SOURCE_ONLY_FREEZE_MANIFEST.json').read_text())
for row in frozen['files']:
    p = Path(row['path'])
    assert p.is_relative_to(R) and not p.is_symlink()
    assert p.stat().st_size == row['size_bytes'] and sha(p) == row['sha256']
    assert format(stat.S_IMODE(p.stat().st_mode), '04o') == row['mode'] == '0444'
manifest = Q / 'MANIFEST.json'
assert sha(manifest) == '9f4548310b58d667279ae8964cea55eeb79c4ddb9f44ee32fb2435bbf3468228'
assert stat.S_IMODE(manifest.stat().st_mode) == 0o444
package = json.loads(manifest.read_text())
assert len(package) == 11
assert {str(p.relative_to(Q)) for p in Q.rglob('*') if p.is_file()} == set(package) | {'MANIFEST.json'}
for rel, row in package.items():
    p = Q / rel
    assert p.is_relative_to(Q) and not p.is_symlink()
    assert p.stat().st_size == row['bytes'] and sha(p) == row['sha256']
    assert stat.S_IMODE(p.stat().st_mode) == 0o444
result = {
    'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'PASS_SOURCE_ONLY_GATE_NAMED_PACKAGE_RELEASE',
    'reviewer': '/root/pr311_preprint_01',
    'source_gate_pins': pins,
    'source_gate_frozen_files_authenticated': len(frozen['files']),
    'root_read_scope': 'Complete criteria and first conclusion read; manifest records authenticated mechanically, without claiming full primary-source or stream reads.',
    'named_package': str(Q),
    'package_manifest_sha256': sha(manifest),
    'released_relative_files': sorted(set(package) | {'MANIFEST.json'}),
    'release_scope': 'Exactly these twelve frozen package files; independent primary-source acquisition is permitted. No other root, sibling, inherited candidate or review reports are released.',
    'package_review_complete': False,
    'publication_ready': False,
    'workflow_percent': 55,
}
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
