"""Data-only fixed candidate snapshot diagnosis; never imports production code."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat

PROJECT = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
STAGE = PROJECT / 'verification/wreath-dyadic-stress-stage-sol-20261116'
OWNED = PROJECT / 'verification/stage3-preflight-discrepancy-audit-sol-20261117'
INVENTORY = STAGE / 'PROSPECTIVE_PUBLIC.json'
ROOT = STAGE / 'candidate/public'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def mode(path):
    return format(stat.S_IMODE(path.lstat().st_mode), '04o')

raw_inventory = INVENTORY.read_bytes()
assert len(raw_inventory) == 201514
assert digest(raw_inventory) == '8534ea8aadf124beb8e845045180b9ede9cb1bde21f24a47acf7eed8521fc0eb'
expected = json.loads(raw_inventory)
files = []
directories = []
special = []
for parent, childdirs, childfiles in os.walk(ROOT, followlinks=False):
    parent = Path(parent)
    for name in childdirs:
        path = parent / name
        if stat.S_ISDIR(path.lstat().st_mode):
            directories.append({'path': path.relative_to(ROOT).as_posix(), 'mode': mode(path)})
        else:
            special.append(str(path))
    for name in childfiles:
        path = parent / name
        if stat.S_ISREG(path.lstat().st_mode):
            before = path.stat()
            raw = path.read_bytes()
            after = path.stat()
            assert (before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) == (after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns)
            files.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'SHA256': digest(raw), 'mode': mode(path)})
        else:
            special.append(str(path))
files.sort(key=lambda row: row['path'])
directories.sort(key=lambda row: row['path'])
actual = {'root': str(ROOT), 'root_mode': mode(ROOT), 'files': files, 'directories': directories, 'regular_files': len(files), 'child_directories': len(directories)}
old = {row['path']: row for row in expected['files']}
new = {row['path']: row for row in actual['files']}
assert len(old) == len(expected['files']) and len(new) == len(files)
positions = [{'index_0based': i, 'expected_path': e['path'], 'actual_path': a['path']} for i, (e, a) in enumerate(zip(expected['files'], files)) if e != a]
result = {'schema': 'fixed-candidate-snapshot-order-diagnosis-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'expected_inventory': {'path': str(INVENTORY), 'bytes': len(raw_inventory), 'SHA256': digest(raw_inventory)}, 'special_objects': special, 'same_file_path_set': set(old) == set(new), 'file_payload_or_mode_differences': [{'path': name, 'expected': old.get(name), 'actual': new.get(name)} for name in sorted(set(old) | set(new)) if old.get(name) != new.get(name)], 'nonfile_snapshot_differences': {key: {'expected': expected[key], 'actual': actual[key]} for key in expected if key != 'files' and expected[key] != actual[key]}, 'expected_order_is_global_string_sort': expected['files'] == files, 'expected_order_is_path_component_sort': expected['files'] == sorted(expected['files'], key=lambda row: Path(row['path'])), 'expected_order_is_component_tuple_sort': expected['files'] == sorted(expected['files'], key=lambda row: Path(row['path']).parts), 'differing_list_positions': positions, 'differing_list_position_count': len(positions), 'globally_sorted_expected_equals_current': {**expected, 'files': sorted(expected['files'], key=lambda row: row['path'])} == actual, 'actual_snapshot': actual}
output = OWNED / 'DIAGNOSIS.json'
with output.open('x') as handle:
    json.dump(result, handle, indent=2)
    handle.write('\n')
os.chmod(output, 0o644)
summary = {key: value for key, value in result.items() if key != 'actual_snapshot'}
print(json.dumps(summary, indent=2))
