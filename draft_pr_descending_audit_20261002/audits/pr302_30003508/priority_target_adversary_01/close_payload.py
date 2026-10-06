"""Private audit closure payload; actual exit/streams are observed by close_launcher.py."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
EXPECTED = Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr302_30003508/priority_target_adversary_01')
assert BASE == EXPECTED
START = datetime.datetime.now(datetime.timezone.utc).isoformat()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def pin(path):
    p = Path(path)
    raw = p.read_bytes()
    return {'path': str(p), 'resolved_path': str(p.resolve()), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest(),
            'mode_observed': oct(p.stat().st_mode & 0o7777)}


def write_json(path, body):
    Path(path).write_text(json.dumps(body, indent=2, sort_keys=True) + '\n')


def check_pin(record):
    p = Path(record['path'])
    actual = pin(p)
    assert actual['bytes'] == record['bytes'], str(p) + ': size differs'
    assert actual['sha256'] == record['sha256'], str(p) + ': whole SHA differs'
    assert actual['resolved_path'] == record['resolved_path'], str(p) + ': resolution differs'
    return {'path': str(p), 'sha256': actual['sha256'],
            'historical_mode': record['mode'], 'control_observed_mode': actual['mode_observed']}


def main():
    print('Actual closure payload PID', os.getpid(), 'started UTC', START, flush=True)
    all_paths = list(BASE.rglob('*'))
    assert not any(p.is_symlink() for p in all_paths), 'Own scope contains a symlink'
    rows = []
    immutable_runtime_checks = {}
    failed = {}
    captures = sorted((BASE / 'native_captures').glob('*/execution.json'))
    assert len(captures) == 36, 'Unexpected capture count'
    for path in captures:
        record = json.loads(path.read_text())
        assert record['capture_version'] == 1
        assert record['actual_child_pid'] > 0 and record['launcher_pid'] > 0
        assert record['cwd'] == str(BASE)
        assert record['argv'] and isinstance(record['exit_code'], int)
        t0 = datetime.datetime.fromisoformat(record['started_utc'])
        t1 = datetime.datetime.fromisoformat(record['completed_utc'])
        assert t0.tzinfo is not None and t1 >= t0
        mode_checks = []
        for key, basename in [('stdout', 'stdout.bin'), ('stderr', 'stderr.bin'),
                              ('retained_launcher_source', 'launcher_source.py')]:
            assert Path(record[key]['path']) == path.parent / basename
            mode_checks.append(check_pin(record[key]))
        mode_checks.append(check_pin(record['launcher_source']))
        assert record['retained_launcher_source']['sha256'] == record['launcher_source']['sha256']
        for item in [record['launcher_python'], record['child_executable'],
                     *record['runtime']['stdlib_modules']]:
            if item['path'] not in immutable_runtime_checks:
                immutable_runtime_checks[item['path']] = check_pin(item)
            checked = immutable_runtime_checks[item['path']]
            assert checked['sha256'] == item['sha256']
        if record['exit_code']:
            failed[path.parent.name] = record['exit_code']
        rows.append({'label': path.parent.name, 'receipt': pin(path),
                     'actual_child_pid': record['actual_child_pid'],
                     'argv': record['argv'], 'cwd': record['cwd'],
                     'started_utc': record['started_utc'], 'completed_utc': record['completed_utc'],
                     'observed_exit': record['exit_code'], 'historical_mode_checks': mode_checks})
    assert failed == {'chen2009_fetch': 22, 'cv2011_publisher_fetch': 56, 'ren_fetch': 22}, failed
    pdf_checks = []
    for p in sorted((BASE / 'private_sources').glob('*.pdf')):
        raw = p.read_bytes()
        assert raw.startswith(b'%PDF-') and b'%%EOF' in raw[-4096:], str(p) + ': PDF framing incomplete'
        pdf_checks.append(pin(p))
    assert len(pdf_checks) == 15, 'Unexpected whole primary PDF count'
    author_sha = pin(BASE / 'private_sources/cv2011.pdf')['sha256']
    assert author_sha == 'be0ffdb11f8e522b0f7925f62ac553f091239f8717eae3109a6077c61ae696fa'
    criteria = BASE / 'PRIORITY_CRITERIA.md'
    assert (criteria.stat().st_mode & 0o777) == 0o444
    correction = json.loads((BASE / 'timestamp_corrections/CORRECTIONS.json').read_text())
    correction_rows = []
    for item in correction['changes']:
        original = (BASE / 'timestamp_corrections/INITIAL_SOURCE_ASSESSMENT.original.md'
                    if item['path'].endswith('/INITIAL_SOURCE_ASSESSMENT.md')
                    else BASE / 'timestamp_corrections' / Path(item['path']).name)
        assert pin(original)['sha256'] == item['original_sha256'], str(original)
        correction_rows.append({'preserved_original': pin(original),
                                'corrected_current': pin(Path(item['path']))})
    verdict = json.loads((BASE / 'VERDICT.json').read_text())
    assert verdict['status'] == 'NO_EXACT_PRIOR_RESOLUTION_FOUND_CONDITIONAL_CLEARANCE_WITH_VERSION_GAP'
    assert not verdict['universal_novelty_certificate'] and not verdict['publication_or_merge_authority']
    assert verdict['class_A_or_B_blockers_found'] == []
    with (BASE / 'RESEARCH_LOG.md').open('a') as f:
        f.write('\n' + now() + '. Native custody control verified all 36 retained scientific source executions, including the three preserved failures, all full streams and named source/runtime pins; 15 private primary PDF versions and timestamp correction originals checked. This bounded family audit is complete. No exact prior resolution found in its inspected scope; publisher-final CV2011 remains uninspected, so historical clearance is conditional. Family completion estimate: 100%; this is completion of the assigned audit, not a universal novelty proof or publication-readiness percentage. Final inventories and readonly seal are being emitted by the observed closure execution.\n')
    write_json(BASE / 'CONTROL_CHECK.json', {
        'kind': 'actual_native_control_payload', 'actual_pid': os.getpid(), 'argv': sys.argv,
        'cwd': os.getcwd(), 'started_utc': START, 'checks_completed_utc': now(),
        'checks_passed': True, 'native_captures_count': 36,
        'successful_child_executions': 33, 'preserved_failed_child_executions': failed,
        'captures': rows, 'current_whole_runtime_checks': list(immutable_runtime_checks.values()),
        'whole_primary_pdf_checks': pdf_checks, 'timestamp_original_checks': correction_rows,
        'criteria_pin': pin(criteria),
        'limits': 'Whole bytes of named executables/launcher/selected stdlib are checked; no complete dynamic-library/OS/import/environment closure is asserted. This payload does not assign its own observed exit; its parent records the actual exit and full streams.'})
    excluded = {'OUTPUT_INVENTORY.json', 'closure_capture/stdout.bin',
                'closure_capture/stderr.bin', 'closure_capture/execution.json'}
    before_modes = []
    for p in sorted(BASE.rglob('*')):
        if p.is_file() and str(p.relative_to(BASE)) not in excluded:
            before_modes.append({'path': str(p), 'before': oct(p.stat().st_mode & 0o7777)})
            p.chmod(0o444)
    attempt = BASE.parent / 'snapshot/unsolved_math_prioritization/attempts/30003508'
    external = [attempt / 'TURN_1.md', attempt / 'TURN_2.md', attempt / 'SOURCE_GATE.md',
                attempt / 'review/PRIOR_SOURCE_COMPARISON.md',
                BASE.parent / 'ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json',
                BASE.parent / 'math_scope_adversary_01/OWR_2017_24.pdf']
    write_json(BASE / 'INPUT_INVENTORY.json', {
        'generated_utc': now(), 'original_pr_head': verdict['original_pr_head'],
        'external_readonly_inputs': [pin(p) for p in external],
        'local_frozen_criteria': pin(criteria),
        'local_primary_sources_and_captures': [pin(p) for p in sorted((BASE / 'private_sources').glob('*')) if p.is_file()],
        'source_privacy': 'Third-party whole PDFs, extracts and renders are private research custody, not public supplemental material.',
        'root_acceptance_scope': 'Only the bounded mathematical acceptance statement was interpreted; whole JSON is pinned without inheriting priority conclusions.',
        'time_basis': 'Actual control-time whole bytes and observed modes; this does not retroactively claim these inventories existed at source execution time.'})
    (BASE / 'INPUT_INVENTORY.json').chmod(0o444)
    for d in sorted([p for p in BASE.rglob('*') if p.is_dir()], key=lambda p: len(p.parts), reverse=True):
        if d != BASE / 'closure_capture':
            d.chmod(0o555)
    files = [pin(p) for p in sorted(BASE.rglob('*'))
             if p.is_file() and str(p.relative_to(BASE)) not in excluded]
    assert all(x['mode_observed'] == '0o444' for x in files)
    write_json(BASE / 'OUTPUT_INVENTORY.json', {
        'generated_utc': now(), 'kind': 'noncircular_private_payload_inventory',
        'payload_file_count': len(files), 'payload_files': files,
        'excluded_relative_paths': sorted(excluded),
        'exclusion_reason': 'Self hash is circular; final child streams and parent execution receipt are still being closed. Parent receipt binds the inventory and complete streams; ROOT can independently hash receipt bytes.',
        'payload_mode_changes_observed': before_modes,
        'directory_modes_current': [{'path': str(d), 'mode_observed': oct(d.stat().st_mode & 0o7777)}
                                    for d in [BASE, *sorted(p for p in BASE.rglob('*') if p.is_dir())]],
        'pending_final_mode_seal': 'Parent observes child exit, closes streams, then verifies all files0444/dirs0555. Pending root/closure directory modes are not falsely recorded as sealed here.'})
    (BASE / 'OUTPUT_INVENTORY.json').chmod(0o444)
    print(json.dumps({'checks_passed': True, 'actual_pid': os.getpid(), 'completed_utc': now(),
                      'captures': len(captures), 'private_primary_pdfs': len(pdf_checks),
                      'preserved_failure_exits': failed, 'output_inventory': pin(BASE / 'OUTPUT_INVENTORY.json')}), flush=True)


if __name__ == '__main__':
    main()
