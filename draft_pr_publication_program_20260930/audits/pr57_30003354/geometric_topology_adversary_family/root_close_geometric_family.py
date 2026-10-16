"""SOURCE-ONLY UNEXECUTED HELPER FOR ROOT. Reads lean evidence; executes no operator.

Usage: python root_close_geometric_family.py /absolute/output/ROOT_CLOSE.json
The output must be outside this immutable family. ROOT must own/capture the run.
No PDF, extracted fulltext, PNG, download, render, SQL or Git action is performed.
"""
import hashlib
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

FAMILY = Path(__file__).resolve().parent


def digest(data): return hashlib.sha256(data).hexdigest()
def mode(path): return format(stat.S_IMODE(path.stat().st_mode), '04o')
def load(path): return json.loads(path.read_bytes())


def validate():
    index_path = FAMILY / 'SOURCE.json'
    assert mode(index_path) == '0444' and not index_path.is_symlink()
    index_bytes = index_path.read_bytes(); index = json.loads(index_bytes)
    listed = {entry['relative_path'] for entry in index['files']}
    assert 'SOURCE.json' not in listed and len(listed) == len(index['files'])
    actual = {str(p.relative_to(FAMILY)) for p in FAMILY.rglob('*') if p.is_file()}
    assert actual == listed | {'SOURCE.json'}
    dirs = {'.'} | {str(p.relative_to(FAMILY)) for p in FAMILY.rglob('*') if p.is_dir()}
    assert dirs == {d['relative_path'] for d in index['directories']}
    for d in index['directories']:
        p = FAMILY if d['relative_path'] == '.' else FAMILY / d['relative_path']
        assert not p.is_symlink() and mode(p) == d['full_mode_07777'] == '0755'
    for entry in index['files']:
        p = FAMILY / entry['relative_path']
        assert not p.is_symlink() and mode(p) == entry['full_mode_07777'] == '0444'
        data = p.read_bytes()
        assert len(data) == entry['bytes'] and digest(data) == entry['sha256']
    bindings = load(FAMILY / 'INPLACE_SOURCE_BINDINGS.json')
    for ref in bindings['bindings']:
        p = Path(ref['absolute_path']); data = p.read_bytes()
        assert not p.is_symlink() and mode(p) == ref['full_mode_07777']
        assert len(data) == ref['bytes'] and digest(data) == ref['sha256']
    ready = load(FAMILY / 'READY.json')
    assert ready['original_head'] == index['original_head'] == bindings['original_head']
    assert ready['mathematical_audit'] == 'PASS_UNIVERSAL_GEOMETRIC_DERIVATION'
    assert ready['ROOT_helpers_executed_by_family'] is False
    assert ready['ROOT_closed_or_readback_claimed'] is False
    assert ready['private_primary_cache_required_by_ROOT_helpers'] is False
    assert ready['whole_publication_primary_PDF_text_PNG_bodies_in_index'] is False
    assert not any(p.endswith(('.pdf', '.png', '.layout.txt')) for p in listed)

    captures = []
    expected = {'primary_read': 0, 'geometric_controls': 1, 'geometric_controls_v2': 0,
                'handoff_preparation': 0}
    for tag, expected_exit in expected.items():
        folder = FAMILY / 'captures' / tag
        pre = load(folder / 'PRELAUNCH.json'); cap = load(folder / 'CAPTURE.json')
        for key, value in pre.items(): assert cap[key] == value
        assert cap['exit_code'] == expected_exit and cap['owned_child_pid'] > 0
        assert cap['collector_pid'] > 0 and cap['root_helpers_executed'] is False
        assert cap['root_closed'] is False and cap['started_utc'] <= cap['ended_utc']
        assert digest((folder / 'operator_prelaunch.py').read_bytes()) == cap['operator_sha256_prelaunch']
        assert digest((folder / 'collector_prelaunch.py').read_bytes()) == cap['collector_sha256_prelaunch']
        assert cap['operator_sha256_prelaunch'] == cap['operator_sha256_after']
        assert cap['collector_sha256_prelaunch'] == cap['collector_sha256_after']
        assert digest(Path(cap['argv'][1]).read_bytes()) == cap['operator_sha256_prelaunch']
        for stream in ('stdout', 'stderr'):
            data = (folder / (stream + '.bin')).read_bytes()
            assert len(data) == cap[stream + '_bytes'] and digest(data) == cap[stream + '_sha256']
        captures.append({'tag': tag, 'child_pid': cap['owned_child_pid'], 'exit_code': cap['exit_code']})
    failed_stderr = (FAMILY / 'captures/geometric_controls/stderr.bin').read_bytes()
    assert b"ModuleNotFoundError: No module named 'sympy'" in failed_stderr
    assert len(failed_stderr) == 277
    children = load(FAMILY / 'primary_child_captures/OWNED_RUNS.json')
    assert len(children) == 9
    for cap in children:
        stem = cap['stdout'].removesuffix('.stdout.bin')
        pre = load(FAMILY / 'primary_child_captures' / (stem + '.PRELAUNCH.json'))
        for key, value in pre.items(): assert cap[key] == value
        assert cap['owner_pid'] == 91565 and cap['owned_child_pid'] > 0 and cap['exit_code'] == 0
        for stream in ('stdout', 'stderr'):
            data = (FAMILY / 'primary_child_captures' / cap[stream]).read_bytes()
            assert len(data) == cap[stream + '_bytes'] and digest(data) == cap[stream + '_sha256']
    results = load(FAMILY / 'GEOMETRIC_CONTROL_RESULTS.json')
    assert results['control_count'] == 5 and len(results['controls']) == 5
    assert results['all_exact'] and results['finite_controls_are_not_universal_proof']
    accounting = load(FAMILY / 'AUDIT_ACCOUNTING.json')
    assert accounting['original_proof_attempts_used'] == 1 and accounting['original_proof_attempt_limit'] == 5
    assert accounting['audit_substantive_proof_attempt_increment'] == 0
    assert accounting['raw_report_key_present_as_preparer_records'] is False
    assert accounting['SQL_report_is_NULL_as_preparer_records'] is False
    assert accounting['SQL_report_literal_as_preparer_records'] == '{}'
    assert accounting['flat_original_upstream_report_field_present_directly_checked'] is False
    return {'SOURCE_sha256': digest(index_bytes), 'SOURCE_bytes': len(index_bytes),
            'fixed_indexed_file_count': len(listed), 'fixed_total_including_SOURCE': len(listed) + 1,
            'directory_count': len(dirs), 'inplace_original_bindings_read': len(bindings['bindings']),
            'owned_operator_capture_validation': captures, 'owned_primary_children': len(children),
            'fresh_exact_successful_controls': 5, 'preserved_dependency_failure_exit': 1,
            'private_primary_cache_read': False, 'operators_imported_or_executed': False,
            'mathematical_acceptance_or_publication_authority_inferred': False}


def main():
    assert len(sys.argv) == 2
    output = Path(sys.argv[1]).resolve()
    assert output.is_absolute() and FAMILY not in output.parents
    assert not output.exists()
    result = validate()
    result.update(schema='pr57-geometric-ROOT-close-read-receipt/v1',
                  executing_pid=os.getpid(), utc=datetime.now(timezone.utc).isoformat(),
                  family_absolute_path=str(FAMILY), original_head='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29',
                  validation_complete=True, receipt_is_actual_only_if_this_helper_was_owned_and_captured_by_ROOT=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as f: f.write(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__': main()
