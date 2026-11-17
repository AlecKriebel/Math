"""Data-only saved-byte correspondence; no production code execution/import."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import os
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V1 = P / 'verification/wreath-dyadic-stress-production-sol-20261117/continuation-20261117'
V2 = P / 'verification/wreath-dyadic-stress-production-root-v2-20261117'
OUT = P / 'verification/stage3-helper-v2-static-audit-sol-20261117'

def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

old = (V1 / 'release_three.py').read_bytes()
new = (V2 / 'release_three.py').read_bytes()
assert pin(V1 / 'release_three.py')['SHA256'] == '708149302f92374a4e0d20bccc238e344542851962934ba72ae5d7df5be17736'
assert pin(V2 / 'release_three.py')['SHA256'] == 'b3cd6a9f14f39d7a11005db9aac8c0cc1c7b5f86844b6514200a30085bc5dd18'
authored = json.loads((V2 / 'AUTHORED_DATA.json').read_bytes())
transformed = old
counts = []
for before, after in authored['exact_replacements']:
    assert transformed.count(before.encode()) == 1
    counts.append({'before': before, 'after': after, 'occurrences': 1})
    transformed = transformed.replace(before.encode(), after.encode())
assert len(counts) == 4 and transformed == new
reverse = new
for before, after in reversed(authored['exact_replacements']):
    assert reverse.count(after.encode()) == 1
    reverse = reverse.replace(after.encode(), before.encode())
assert reverse == old
expected_diff = ''.join(difflib.unified_diff(old.decode().splitlines(True), new.decode().splitlines(True), fromfile='frozen-v1/release_three.py', tofile='root-v2/release_three.py'))
assert expected_diff.encode() == (V2 / 'DIFF.patch').read_bytes()
old_plan = json.loads((V1 / 'PLAN.json').read_bytes())
new_plan = json.loads((V2 / 'PLAN.json').read_bytes())
changed = [key for key in sorted(set(old_plan) | set(new_plan)) if old_plan.get(key) != new_plan.get(key)]
assert changed == ['continuation_root', 'runtime_root']
old_plan_raw = (V1 / 'PLAN.json').read_bytes()
for key in changed:
    assert old_plan_raw.count(old_plan[key].encode()) == 1
    old_plan_raw = old_plan_raw.replace(old_plan[key].encode(), new_plan[key].encode())
assert old_plan_raw == (V2 / 'PLAN.json').read_bytes()
manifest = json.loads((V2 / 'MANIFEST.json').read_bytes())
entries = list(V2.iterdir())
assert len(entries) == 8 and all(stat.S_ISREG(path.lstat().st_mode) for path in entries)
assert format(stat.S_IMODE(V2.lstat().st_mode), '04o') == '0755'
assert set(path.name for path in entries) == {row['path'] for row in manifest['payload_files']} | {'FINAL.json', 'MANIFEST.json'}
assert all(pin(V2 / row['path']) == {key: row[key] for key in ('bytes', 'SHA256', 'mode')} for row in manifest['payload_files'])
controls = [{'name': name, 'exact': pin(Path(row['path'])) == {key: row[key] for key in ('bytes', 'SHA256', 'mode')}} for name, row in new_plan['controls'].items()]
assert len(controls) == 15 and all(row['exact'] for row in controls)
assert len(new_plan['immutable_input_files']) == 6
assert all(pin(Path(row['path'])) == {key: row[key] for key in ('bytes', 'SHA256', 'mode')} for row in new_plan['immutable_input_files'])
diag = json.loads((P / 'verification/stage3-preflight-discrepancy-audit-sol-20261117/DIAGNOSIS.json').read_bytes())
snap = json.loads((P / 'verification/wreath-dyadic-stress-stage-sol-20261116/PROSPECTIVE_PUBLIC.json').read_bytes())
normalized = {**snap, 'files': sorted(snap['files'], key=lambda row: row['path']), 'directories': sorted(snap['directories'], key=lambda row: row['path'])}
assert normalized == diag['actual_snapshot']
result = {'schema': 'informed-v2-saved-byte-correspondence-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'whole_helper_forward_reverse_exact': True, 'replacements': counts, 'unified_diff_hunks': sum(line.startswith('@@') for line in expected_diff.splitlines()), 'whole_PLAN_two_path_replacements_exact': True, 'PLAN_keys_changed': changed, 'producer_files': [{'path': path.name, **pin(path)} for path in sorted(entries)], 'producer_child_directories': 0, 'producer_root_mode': '0755', 'all15_control_pins_exact': controls, 'original6_input_files_exact': True, 'saved_expected_normalization_matches_prior_independent_complete_candidate_census': True, 'whole_snapshot_uses': [{'line': i, 'text': line} for i, line in enumerate(new.decode().splitlines(), 1) if 'whole_snapshot(' in line], 'production_code_import_or_execution': False}
with (OUT / 'CORRESPONDENCE.json').open('x') as handle:
    json.dump(result, handle, indent=2)
    handle.write('\n')
os.chmod(OUT / 'CORRESPONDENCE.json', 0o644)
print(json.dumps({key: value for key, value in result.items() if key not in ('producer_files', 'replacements')}, indent=2))
