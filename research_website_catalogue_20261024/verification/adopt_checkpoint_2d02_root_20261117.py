"""Read-only evidence authentication; writes one root adoption record only."""
from pathlib import Path
import hashlib
import json
import stat
from datetime import datetime, timezone

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
base = P / 'verification/checkpoint-thompson-pass143-20261117'
sha = lambda b: hashlib.sha256(b).hexdigest()
expected_final = 'bcdbfe4ed45a2f56e2db946137db359aace6fe068f991deb9df0cc14553b870f'
expected_manifest = 'd35cacde34d59eb5f8103bd52e63374ef51aee06f85f19e439e6be2d638ed55a'
assert sha((base / 'FINAL.json').read_bytes()) == expected_final
assert sha((base / 'MANIFEST.json').read_bytes()) == expected_manifest
final = json.loads((base / 'FINAL.json').read_bytes())
manifest = json.loads((base / 'MANIFEST.json').read_bytes())
assert final['commit'] == '2d020358e466323f2f188ee84aa2ff1a535bed8c'
assert final['parent'] == '674c6b9f9b296dd7a18dac4eec87b4ace840ccd5'
assert final['tree'] == '10c77e39a7c0a4d7b560012972e8eb1af8665002'
leaves = {x.relative_to(base).as_posix(): x for x in base.rglob('*')}
assert len(leaves) == 49 and all(x.is_file() and not x.is_symlink() for x in leaves.values())
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
          'authenticated_files': 49, 'child_directories': 0,
          'root_read_actual': ['FINAL.json', 'REPORT.md', 'FINAL_CHECKS.json', 'FINAL_CHECKS.json all_wrapper_runs'],
          'final_SHA256': expected_final, 'manifest_SHA256': expected_manifest,
          'scope': 'Checkpoint custody and recorded preservation evidence; no new scientific or UI certification.',
          'native_tracker_at_snapshot': 142, 'scientific_reviewed': 143, 'goal_active_incomplete': True}
out = P / 'verification/root-checkpoint-2d02-adoption-20261117.json'
with out.open('x') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
print(json.dumps(result))
