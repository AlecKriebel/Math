"""Read-only evidence authentication; writes one root adoption record only."""
from pathlib import Path
import hashlib
import json
import stat
from datetime import datetime, timezone

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
base = P / 'verification/checkpoint-gram-pass142-stage-20261117'
sha = lambda b: hashlib.sha256(b).hexdigest()
expected_final = 'c39241b933331ae4cc1729ad9be0ae5dcfd895daffe3456100741127bf9c47f4'
expected_manifest = 'c5c3600ba65f4cec5308be5fe97cadd79338422e75a5faf7106535a9aa6da8e3'
assert sha((base / 'FINAL.json').read_bytes()) == expected_final
assert sha((base / 'MANIFEST.json').read_bytes()) == expected_manifest
final = json.loads((base / 'FINAL.json').read_bytes())
manifest = json.loads((base / 'MANIFEST.json').read_bytes())
assert final['commit'] == '674c6b9f9b296dd7a18dac4eec87b4ace840ccd5'
assert final['parent'] == 'a4267dc5366bb693dd565421271276677a060320'
assert final['tree'] == '19377d2d555dddb5024a2960a1f60d6e5757f09b'
leaves = {x.relative_to(base).as_posix(): x for x in base.rglob('*')}
assert len(leaves) == 48 and all(x.is_file() and not x.is_symlink() for x in leaves.values())
expected = {x['path']: x for x in manifest['payload_files']}
assert set(expected) | {'MANIFEST.json', 'FINAL.json'} == set(leaves)
assert stat.S_IMODE(base.stat().st_mode) == 0o755
for name, row in expected.items():
    f = leaves[name]
    b = f.read_bytes()
    assert len(b) == row['bytes'] and sha(b) == row['SHA256'], name
    assert f'{stat.S_IMODE(f.stat().st_mode):04o}' == row['mode'], name
checks = json.loads((base / 'FINAL_CHECKS.json').read_bytes())
assert checks['all_159_untargeted_root_siblings_and_docs_exact']
assert checks['all_changed_blob_whole_bytes_and_git_modes_verified']
assert checks['whole_public_bytes_modes_topology_exact']
assert checks['dry_push_exits'] == [0, 0]
assert all(x['exit_code'] == 0 for x in checks['all_wrapper_runs'])
result = {'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'ACCEPTED_FINITE_CHECKPOINT',
          'commit': final['commit'], 'parent': final['parent'], 'tree': final['tree'],
          'authenticated_files': 48, 'child_directories': 0,
          'root_read_actual': ['FINAL.json', 'REPORT.md', 'FINAL_CHECKS.json', 'RUNS.json'],
          'final_SHA256': expected_final, 'manifest_SHA256': expected_manifest,
          'scope': 'Checkpoint custody and recorded preservation evidence; no new scientific or UI certification.',
          'native_tracker_at_snapshot': 141, 'scientific_reviewed': 142, 'goal_active_incomplete': True}
out = P / 'verification/root-checkpoint-674c-adoption-20261117.json'
with out.open('x') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
print(json.dumps(result))
