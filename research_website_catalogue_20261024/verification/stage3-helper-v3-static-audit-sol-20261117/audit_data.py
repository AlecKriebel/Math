"""Fixed-path data-only byte correspondence; no production module is loaded."""
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
V3 = P / 'verification/wreath-dyadic-stress-production-root-v3-20261117'
OWN = P / 'verification/stage3-helper-v3-static-audit-sol-20261117'

def pin(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

def json_read(path):
    return json.loads(path.read_bytes())

sources = [root.joinpath('release_three.py').read_bytes() for root in (V1, V2, V3)]
assert [hashlib.sha256(raw).hexdigest() for raw in sources] == ['708149302f92374a4e0d20bccc238e344542851962934ba72ae5d7df5be17736', 'b3cd6a9f14f39d7a11005db9aac8c0cc1c7b5f86844b6514200a30085bc5dd18', '878df1fff183a407371f4b298c45d5560e6349d4b4f2dfd6bdc3a1ea1eb53cc7']
pairs23 = [
    (b"N = P / 'verification/wreath-dyadic-stress-production-root-v2-20261117'", b"N = P / 'verification/wreath-dyadic-stress-production-root-v3-20261117'"),
    (b"RUN = P / 'verification/wreath-dyadic-stress-runtime-root-v2-20261117'", b"RUN = P / 'verification/wreath-dyadic-stress-runtime-root-v3-20261117'"),
    (b"PLAN_SHA = '5b7d4b93cff056d20f3786d08b8a52fa5a7bad1b32d906fd86cc30072db4692c'", b"PLAN_SHA = 'b16e72c5c1d8e100b5234263b0be33e48176ccdac7071388aa9e024ae8fde713'"),
    (b'for root in (PREP, RUN, S, A)', b'for root in (PREP, N, RUN, S, A)'),
]
old_comparison = b"        need(census(Path(expected['root'])) == expected, 'whole namespace bytes/modes/topology: ' + expected['root'])"
new_comparison = b"        normalized = dict(expected)\n        normalized['files'] = sorted(expected['files'], key=lambda row: row['path'])\n        normalized['directories'] = sorted(expected['directories'], key=lambda row: row['path'])\n        need(census(Path(expected['root'])) == normalized, 'whole namespace bytes/modes/topology: ' + expected['root'])"
pairs12 = [
    (b"N = PREP / 'continuation-20261117'", pairs23[0][0]),
    (b"RUN = P / 'verification/wreath-dyadic-stress-runtime-root-20261117'", pairs23[1][0]),
    (b"PLAN_SHA = 'cbe3ec5c2dbdcf0727f837fc8dc08e77b639225e828698d30e16a3cca45f9bc1'", pairs23[2][0]),
    (old_comparison, new_comparison),
]

def correspondence(before, after, pairs):
    forward, reverse = before, after
    for old, new in pairs:
        assert before.count(old) == after.count(new) == 1
        forward = forward.replace(old, new)
        reverse = reverse.replace(new, old)
    assert forward == after and reverse == before
    return {'forward_exact': True, 'reverse_exact': True, 'replacement_categories': len(pairs)}

source12 = correspondence(sources[0], sources[1], pairs12)
source23 = correspondence(sources[1], sources[2], pairs23)
plan_raw = [root.joinpath('PLAN.json').read_bytes() for root in (V1, V2, V3)]
plans = [json.loads(raw) for raw in plan_raw]
plan_changes = []
for before, after, oldroot, newroot in zip(plans, plans[1:], (V1, V2), (V2, V3)):
    changed = sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
    assert changed == ['continuation_root', 'runtime_root']
    raw_before, raw_after = (oldroot / 'PLAN.json').read_bytes(), (newroot / 'PLAN.json').read_bytes()
    pairs = [(before[key].encode(), after[key].encode()) for key in changed]
    plan_changes.append({'keys': changed, **correspondence(raw_before, raw_after, pairs)})
patch = ''.join(difflib.unified_diff(sources[1].decode().splitlines(keepends=True), sources[2].decode().splitlines(keepends=True), fromfile='frozen-v2/release_three.py', tofile='root-v3/release_three.py')).encode()
assert patch == (V3 / 'DIFF.patch').read_bytes()
manifest = json_read(V3 / 'MANIFEST.json')
assert pin(V3 / 'FINAL.json')['SHA256'] == 'f1fae0993efd070e122257bec479fadfba642c5e406747168a8334a149d264ad'
assert pin(V3 / 'MANIFEST.json')['SHA256'] == 'a010e5219c905185019dbb76afd8c2da979c9a8dbfd84a52906fc4503a5ee5a3'
names = sorted(path.name for path in V3.iterdir())
assert names == sorted([row['path'] for row in manifest['payload_files']] + ['FINAL.json', 'MANIFEST.json'])
assert len(names) == manifest['regular_files'] == 8 and manifest['child_directories'] == 0
assert manifest['directories'] == [] and manifest['exact_terminal_exclusions'] == ['FINAL.json', 'MANIFEST.json']
assert format(stat.S_IMODE(V3.lstat().st_mode), '04o') == manifest['root_mode'] == '0755'
for path in V3.iterdir():
    assert stat.S_ISREG(path.lstat().st_mode) and not path.is_symlink() and pin(path)['mode'] == '0644'
for row in manifest['payload_files']:
    actual = pin(V3 / row['path'])
    assert {key: actual[key] for key in ('bytes', 'SHA256', 'mode')} == {key: row[key] for key in ('bytes', 'SHA256', 'mode')}
controls = []
for name, row in plans[2]['controls'].items():
    actual = pin(Path(row['path']))
    assert actual == row
    controls.append({'name': name, 'pin': actual})
immutable = []
for row in plans[2]['immutable_input_files']:
    actual = pin(Path(row['path']))
    assert actual == row
    immutable.append(actual)
snapshot = json_read(Path(plans[2]['controls']['prospective_public']['path']))
diagnosis = json_read(P / 'verification/stage3-preflight-discrepancy-audit-sol-20261117/DIAGNOSIS.json')
normalized_data = {**snapshot, 'files': sorted(snapshot['files'], key=lambda row: row['path']), 'directories': sorted(snapshot['directories'], key=lambda row: row['path'])}
assert normalized_data == diagnosis['actual_snapshot']
result = {'schema': 'informed-stage3-v3-byte-data-correspondence-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source12': source12, 'source23': source23, 'whole_source_chain_exact': True, 'source_line_counts': [len(raw.splitlines()) for raw in sources], 'plan_changes': plan_changes, 'actual_patch_hunks': sum(line.startswith('@@ ') for line in patch.decode().splitlines()), 'patch_exact': True, 'producer_extent': [8, 0], 'producer_pins': [pin(V3 / name) for name in names], 'controls': controls, 'immutable_input_files': immutable, 'normalized_frozen_data_equals_recorded_complete_candidate_census': True, 'runtime_absent': not os.path.lexists(Path(plans[2]['runtime_root'])), 'production_code_loaded_or_executed': False}
with (OWN / 'AUDIT_DATA.json').open('x') as handle:
    json.dump(result, handle, indent=2)
    handle.write('\n')
os.chmod(OWN / 'AUDIT_DATA.json', 0o644)
print(json.dumps({key: value for key, value in result.items() if key not in ('producer_pins', 'controls', 'immutable_input_files')}, indent=2))
