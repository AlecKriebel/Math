"""ROOT checks the genuinely frozen whole current packet without its helpers."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import stat
import os
from author_root_current_prerequisites import load, read, encode, sha

A = Path(__file__).resolve().parent
R = A.parents[2]
C = A / 'reviewed_candidate'
EXPECTED = '09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de'
IMMUTABLE = ['PARTIAL.md', 'check_spectra.py', 'check_results.json', 'source_record.json',
             'source_checksums.json', 'turns.jsonl', 'review/PARTIAL.md',
             'review/independent_checks.py', 'review/independent_results.json',
             'review/submitted_check_spectra.py', 'review/submitted_results.json']


def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0')
    mf = load(read(C / 'MANIFEST.json', EXPECTED))
    assert mf['self_excluded'] == ['MANIFEST.json']
    assert type(mf['files_count']) is int and mf['files_count'] == len(mf['files']) == 385
    names = {row['path'] for row in mf['files']}
    assert len(names) == 385 and 'MANIFEST.json' not in names
    actual_names, actual_dirs = set(), set()
    for path in C.rglob('*'):
        assert not path.is_symlink()
        name = path.relative_to(C).as_posix()
        if path.is_file(): actual_names.add(name)
        else:
            assert path.is_dir()
            actual_dirs.add(name)
    assert actual_names == names | {'MANIFEST.json'}
    assert actual_dirs == {p.as_posix() for n in actual_names for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    objects = {}
    for row in mf['files']:
        assert type(row['bytes']) is int and row['bytes'] >= 0 and row['mode'] == '0444'
        raw = read(C / row['path'], row['sha256'], row['bytes'])
        assert stat.S_IMODE((C / row['path']).stat().st_mode) == 0o444
        if row['path'].endswith('.json'): objects[row['path']] = load(raw)
        if row['path'].endswith('.jsonl'):
            for line in raw.splitlines(): load(line)
    assert stat.S_IMODE((C / 'MANIFEST.json').stat().st_mode) == 0o444
    dep = objects['CURRENT_DEPENDENCIES.json']
    assert dep['anchor_repository_relative'] == A.relative_to(R).as_posix()
    assert len(dep['files']) == len({row['path'] for row in dep['files']}) == 517
    for row in dep['files']: read(A / row['path'], row['sha256'], row['bytes'])
    current = load(read(A / 'ROOT_CURRENT_INPUT_PREIMAGES.json'))
    assert dep['current_native13'] == current['files']
    for row in current['files']: read(R / row['path'], row['sha256'], row['bytes'])
    originals = objects['original_snapshot_manifest.json']['files']
    assert len(originals) == 17
    for row in originals:
        raw = read(C / 'original_archive' / row['path'], row['sha256'], row['size'])
        assert raw == read(A / 'source_snapshot_v2' / row['path'])
        if row['path'] in IMMUTABLE: assert read(C / row['path']) == raw
    ledger = [load(line) for line in read(C / 'turns.jsonl').splitlines()]
    assert [row['turn'] for row in ledger] == [1, 2] and all(type(row['turn']) is int for row in ledger)
    original_replay = objects['root_evidence/root_original_actual_reproduction_v2/RESULT.json']
    assert original_replay['whole_raw_bytes'] == 149266659 and original_replay['whole_SQL_rows'] == 15458
    assert original_replay['entire_reviewed_author_result'] == objects['check_results.json']
    assert original_replay['entire_original_independent_result'] == objects['review/independent_results.json']
    current_author = dict(objects['check_results.json'], partial_sha256=sha(read(C / 'PARTIAL.md')))
    assert original_replay['entire_current_author_result'] == current_author
    for name in ['status.json', 'readiness.json', 'review/verdict.json']:
        obj = objects[name]
        assert obj['full_problem_solved'] is False and obj['novelty_claimed'] is False
        assert obj['partial_valid_from_root_scientific_reading'] is True
        assert [obj[k] for k in ['original_substantive_attempts','substantive_attempt_limit','new_substantive_attempts','audit_turns']] == [2,5,0,0]
        assert all(obj[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict'])
        assert obj['current_gate'] == 'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
    capture = load(read(A / 'root_current_freeze_actual_capture/CAPTURE.json'))
    assert capture['status'] == 'PASS' and capture['actual_execution'] is True and capture['completed'] is True
    assert type(capture['pid']) is int and capture['pid'] == 60795 and capture['exit_code'] == 0
    assert capture['main_head_before'] == capture['main_head_after'] == current['current_head']
    assert capture['native13_before'] == capture['native13_after'] == current['files']
    assert sha(read(A / 'root_current_freeze_actual_capture/PRELAUNCH_SOURCE.py')) == capture['source_sha256']
    for channel in ['stdout','stderr']:
        row = capture[channel]
        read(A / 'root_current_freeze_actual_capture' / row['path'], row['sha256'], row['bytes'])
    stdout = load(read(A / 'root_current_freeze_actual_capture/stdout.bin'))
    assert stdout['manifest_sha256'] == EXPECTED and stdout['native_writes'] == 0
    q = objects['CURRENT_QUEUE_PATCH.json']
    before = read(C / 'queue_proposal/QUEUE_PREIMAGE.md', q['whole_preimage_sha256'])
    after = read(C / 'queue_proposal/QUEUE_PROSPECTIVE.md', q['whole_prospective_sha256'])
    assert before == read(R / 'unsolved_math_prioritization/QUEUE.md')
    assert before.count(q['row_before'].encode()) == 1
    assert after == before.replace(q['row_before'].encode(), q['row_prospective'].encode(), 1)
    b = q['row_before'].split('|'); a = q['row_prospective'].split('|')
    assert len(a) == len(b) == 14 and [i for i,(x,y) in enumerate(zip(a,b)) if x != y] == [8,9,11]
    result = {'status': 'PASS_ROOT_ACTUAL_WHOLE_CURRENT_PACKET_MECHANICAL_INSPECTION',
        'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'manifest_sha256': EXPECTED,
        'packet_members_plus_self': 386, 'dependencies': 517,
        'whole_JSON_objects_consumed': len(objects), 'original17_byte_exact': True,
        'actual_freeze_pid': capture['pid'], 'whole_native13_unchanged': True,
        'original_ledger': ledger, 'original_substantive_attempts': 2,
        'new_substantive_attempts': 0, 'audit_turns': 0,
        'full_problem_solved': False, 'new_whole_adversary_gate': 'PENDING',
        'this_inspection_executes_no_scientific_helper': True}
    with (A / 'ROOT_ACTUAL_CURRENT_PACKET_INSPECTION.json').open('xb') as f:
        f.write(encode(result)); f.flush(); os.fsync(f.fileno())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
