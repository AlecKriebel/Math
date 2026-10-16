"""Read-only integrity diagnostics. All failures use explicit exceptions, even under -O."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import stat
import sys

BASE = Path(__file__).resolve().parent
PINS = {
    'FIRST_ASSESSMENT.md': (3135, 'ec366206ff4772b0e309320de2837a0a077cd32acdba065309b416680377c788'),
    'RESEARCH_LOG_FIRST.md': (507, '556cd9a18b00f2fbbddf2f1b9811409968eeb6fd6a40383baac875afa6ca637c'),
    'FIRST_INVENTORY.json': (1434, '627842dded43a1afb9aef6c2bf8873206256de18586ee4420a693e4f5a23057e'),
    'FIRST_SUBSTANTIVE_PRIORITY_ASSESSMENT.md': (7526, '0dd356803441b325f95f9829fa9e8c694ad5d8bef31b10eb74e708a83f04c047'),
    'FIRST_SUBSTANTIVE_PRIORITY_INVENTORY.json': (30510, 'a865f4694d4464e05fedd6640345ad1def785621be654dfe990c2350c90834f5'),
    'FIRST_INPUTS_MANIFEST.json': (2177, 'bb344fa56f97a6d0cfa9ed7d3e930b2fc2f981af6e89982e63edc68a378b12c6'),
    'FIRST_INPUT_CANDIDATE.md': (9292, 'c7254c0997b49fa3d44b7ae3ef9b82b81753395057ad528ff385c49772e4a3ad'),
    'FIRST_INPUT_source_record.json': (2607, 'c1737503f7c403ad90e3556dc5c5ecc8c127c38ee6299336719f2c00b95e9beb'),
    'FIRST_INPUT_source_manifest.json': (774, 'b16a8d87a1d3b60a5f4b1790a0143941b1ab1c3628e5ac6d39078c9d7834a7dd'),
    'AD20261012T1619Z_independent_old_generation_verification.md': (15929, '6fb264638baef57ebd242e3fd8b6ddd28209f91a5e089b816d16df86e6eba8df'),
    'FINAL_PRIORITY_SOURCE_LINEAGE_REPORT.md': (17068, '654dd30da688c7b3de2b85705e8fc4cfbb82afd4ac66a7903f430ba20bcf35e4'),
}


def fail_if(condition, message):
    if condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_path(name):
    path = BASE / name
    fail_if(not path.resolve().is_relative_to(BASE), f'Path escapes audit: {name}')
    fail_if(path.is_symlink(), f'Symlink not permitted: {name}')
    return path


def check_file(name, count, sha):
    path = local_path(name)
    fail_if(not path.is_file(), f'Missing file: {name}')
    fail_if(path.stat().st_size != count, f'Byte-count mismatch: {name}')
    fail_if(digest(path) != sha, f'SHA256 mismatch: {name}')
    fail_if(stat.S_IMODE(path.stat().st_mode) != 0o444, f'Mode mismatch: {name}')


def verify_rows(rows):
    names = set()
    for row in rows:
        name = row['file']
        fail_if(name in names, f'Duplicate inventory row: {name}')
        names.add(name)
        check_file(name, row['bytes'], row['sha256'])
        fail_if(row['mode'] not in ('0o444', '0444'), f'Inventory mode incorrect: {name}')
    return names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory')
    args = parser.parse_args()
    for name, (count, sha) in PINS.items():
        check_file(name, count, sha)
    frozen_rows = 0
    for name in ('FIRST_INVENTORY.json', 'FIRST_SUBSTANTIVE_PRIORITY_INVENTORY.json'):
        rows = json.loads(local_path(name).read_text())['files']
        verify_rows(rows)
        frozen_rows += len(rows)
    original_count = 0
    for row in json.loads(local_path('FIRST_INPUTS_MANIFEST.json').read_text())['inputs']:
        src = Path(row['source'])
        fail_if(src.stat().st_size != row['bytes'] or digest(src) != row['sha256'], 'Original input changed')
        check_file(str(Path(row['retained']).relative_to(BASE)), row['bytes'], row['sha256'])
        original_count += 1
    all_files = [f for f in BASE.rglob('*') if f.is_file()]
    for f in all_files:
        fail_if(f.is_symlink(), f'Symlink: {f.relative_to(BASE)}')
        fail_if(stat.S_IMODE(f.stat().st_mode) != 0o444, f'Unsealed file: {f.relative_to(BASE)}')
    capture_count = 0
    unavailable_count = 0
    mismatched_pdf_names = []
    for record_path in (BASE / 'private_sources').glob('*.access.json'):
        row = json.loads(record_path.read_text())
        body = BASE / 'private_sources' / row['name']
        if 'retained' in row:
            fail_if(Path(row['retained']) != body, f'Capture path mismatch: {row["name"]}')
            check_file(str(body.relative_to(BASE)), row['bytes'], row['sha256'])
            capture_count += 1
            if body.suffix == '.pdf' and not body.read_bytes().startswith(b'%PDF'):
                fail_if(body.name != 'ng_stanford_cambridge.pdf', f'Unexpected nonPDF capture: {body.name}')
                fail_if('html' not in row.get('content_type', '').lower(), 'Known nonPDF MIME changed')
                mismatched_pdf_names.append(body.name)
        else:
            fail_if(row.get('outcome') != 'unavailable', f'Incomplete access outcome: {record_path.name}')
            fail_if(body.exists(), f'Failed fetch unexpectedly has a body: {body.name}')
            unavailable_count += 1
    inventory_result = None
    if args.inventory:
        inventory = json.loads(local_path(args.inventory).read_text())
        names = verify_rows(inventory['files'])
        excluded = set(inventory['recursive_hash_exclusions'])
        actual = {str(f.relative_to(BASE)) for f in all_files}
        fail_if(actual - excluded != names, 'Final inventory coverage mismatch')
        allowed = set(inventory['safe_public_allowlist'])
        fail_if(len(allowed) != len(inventory['safe_public_allowlist']), 'Duplicate allowlist name')
        fail_if(not allowed <= names | excluded, 'Unknown allowlist member')
        for name in allowed:
            fail_if(name.startswith('private_sources/') or name.startswith('FIRST_INPUT') or name.startswith('FIRST_WEB') or name == 'FIRST_RUNTIME_METADATA.json', f'Unsafe allowlist member: {name}')
        for row in inventory['files']:
            fail_if(row['safe_public'] != (row['file'] in allowed), f'Allowlist flag mismatch: {row["file"]}')
        inventory_result = {'rows_verified': len(names), 'recursive_hash_exclusions': sorted(excluded), 'public_allowlist_entries': len(allowed)}
    print(json.dumps({'utc': datetime.now(timezone.utc).isoformat(), 'ok': True, 'optimization_level': sys.flags.optimize, 'exception_checks_active': True, 'pinned_files_verified': len(PINS), 'frozen_first_inventory_rows_verified': frozen_rows, 'original_inputs_verified': original_count, 'all_retained_files_mode0444': len(all_files), 'fetched_bodies_verified': capture_count, 'unavailable_access_records_verified': unavailable_count, 'known_html_not_pdf': mismatched_pdf_names, 'final_inventory': inventory_result, 'limits': ['Integrity only; not mathematical proof automation or priority absence guarantee.', 'Some relevant complete published bodies were unavailable; raw capture limitation separately disclosed.']}, indent=2))


if __name__ == '__main__':
    main()
