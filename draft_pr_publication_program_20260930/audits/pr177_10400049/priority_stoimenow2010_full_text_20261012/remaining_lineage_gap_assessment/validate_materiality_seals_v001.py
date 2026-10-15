"""Read-only preservation check with explicit exceptions; supports normal and -O runs."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import stat
import sys

BASE = Path(__file__).resolve().parent
OLD = BASE.parent.parent / 'priority_source_lineage'
PINS = {
    'INPUT_PROVENANCE_FIRST.json': (6358, 'd538d3b95a560abdce0cd608cde33f053bb89d78aba29c4bfeb573be7e5b9a1c'),
    'FIRST_SUBSTANTIVE_MATERIALITY_ASSESSMENT.md': (4789, '81cd65806e62dcbe8343340685d9754859e379b78bf4281df3056926e484f14f'),
    'RESEARCH_LOG_FIRST.md': (699, 'c3cd5e3c7b4a12af88f922d40072043153b260c53c25319a7f401e6d136b2be5'),
    'FIRST_INVENTORY.json': (3410, '9b47e7f18960f3f9986f1d585cb9616e7127c564c61d2d411fce92435b1d2508'),
    'FINAL_MATERIALITY_ASSESSMENT.md': (9562, 'ab77c808c6b5f88cf409219cfb7601cf6428c4e6ac5d9a3a548964775071f898'),
    'SOURCE_EVIDENCE_QUALIFICATION_ADDENDUM_001.md': (1662, '5aa3f0840eacae6fd55683c43904a835d2dd6411a5267b3a28c0ffba5d0dcfdb'),
}


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(base, name, size, checksum):
    p = base / name
    require(p.resolve().is_relative_to(base), 'Path escapes base: ' + name)
    require(p.is_file() and not p.is_symlink(), 'Missing/nonregular file: ' + name)
    require(p.stat().st_size == size, 'Byte-count mismatch: ' + name)
    require(sha(p) == checksum, 'SHA256 mismatch: ' + name)
    require(stat.S_IMODE(p.stat().st_mode) == 0o444, 'Unsealed file: ' + name)


def rows_check(base, rows):
    names = set()
    for row in rows:
        require(row['file'] not in names, 'Duplicate row')
        names.add(row['file'])
        check(base, row['file'], row['bytes'], row['sha256'])
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inventory')
    args = ap.parse_args()
    for name, (size, checksum) in PINS.items():
        check(BASE, name, size, checksum)
    first_rows = json.loads((BASE / 'FIRST_INVENTORY.json').read_text())['files']
    rows_check(BASE, first_rows)
    original_sources = 0
    for manifest in ['INPUT_PROVENANCE_FIRST.json', 'INPUT_PROVENANCE_SUPPLEMENT_001.json']:
        data = json.loads((BASE / manifest).read_text())
        rows = data.get('inputs', data.get('additional_prior_sealed_evidence_read', []))
        for row in rows:
            check(BASE, row['retained'], row['bytes'], row['sha256'])
            p = Path(row['source'])
            require(p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'Original supplied source/report changed')
            original_sources += 1
    check(OLD, 'FINAL_ENVELOPE_v001.json', 3402, '5cd1471436e09b486324a8ead1c54fa3cd6856338e569c24a8a4d7bb56cf0150')
    check(OLD, 'FINAL_INVENTORY_v001.json', 74787, '3b007840429d6f1e36330acc24c4be900064ee89a264c7c7bf1f5d26976ecf61')
    old_inventory = json.loads((OLD / 'FINAL_INVENTORY_v001.json').read_text())
    old_envelope = json.loads((OLD / 'FINAL_ENVELOPE_v001.json').read_text())
    old_names = rows_check(OLD, old_inventory['files'])
    old_names |= rows_check(OLD, old_envelope['recursive_hash_exclusion_pins'])
    old_names.add('FINAL_ENVELOPE_v001.json')
    actual_old = {str(p.relative_to(OLD)) for p in OLD.rglob('*') if p.is_file()}
    require(old_names == actual_old and len(old_names) == 309, 'Old309-file freeze changed')
    actual = {str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}
    for name in actual:
        require(stat.S_IMODE((BASE / name).stat().st_mode) == 0o444, 'New unsealed file: ' + name)
    final = None
    if args.inventory:
        obj = json.loads((BASE / args.inventory).read_text())
        names = rows_check(BASE, obj['files'])
        require(actual - set(obj['recursive_hash_exclusions']) == names, 'New final inventory coverage mismatch')
        allow = set(obj['safe_public_allowlist'])
        require(len(allow) == len(obj['safe_public_allowlist']), 'Duplicate allowlist member')
        require(all(not n.startswith('private_inputs/') for n in allow), 'Private source/prior verdict in allowlist')
        require(allow <= names | set(obj['recursive_hash_exclusions']), 'Unknown allowlist member')
        require(all(row['safe_public'] == (row['file'] in allow) for row in obj['files']), 'Allowlist flag mismatch')
        final = {'rows': len(names), 'allowlist_entries': len(allow), 'recursive_hash_exclusions': obj['recursive_hash_exclusions']}
    print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'ok': True, 'optimization_level': sys.flags.optimize, 'explicit_exception_checks': True, 'old309files_unchanged': True, 'old_envelope_sha256': sha(OLD / 'FINAL_ENVELOPE_v001.json'), 'new_first_pins_verified': len(PINS), 'first_inventory_rows_verified': len(first_rows), 'supplied_original_sources_and_reports_verified': original_sources, 'new_files_mode0444': len(actual), 'final_inventory': final, 'case_percent': 40, 'task_type': 'post-first-seal bounded synthesis; no new complete final-body or2010reading'}, indent=2))


if __name__ == '__main__':
    main()
