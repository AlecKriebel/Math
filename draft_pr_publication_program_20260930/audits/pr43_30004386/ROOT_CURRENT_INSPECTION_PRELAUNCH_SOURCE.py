"""ROOT whole-byte current freeze inspection; run no candidate helper."""
from pathlib import Path, PurePosixPath
import datetime as dt
import json
import os
import stat
from author_root_current_prerequisites import read, load, sha, write, git

A = Path(__file__).resolve().parent
R = A.parents[2]
C = A / 'reviewed_candidate'
MF = '4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14'
IMMUTABLE = ['SOURCE_STATUS.md','check_normalization.py','check_results.json',
    'source_record.json','source_checksums.json','turns.jsonl',
    'review/author_replay/check_normalization.py','review/author_replay/check_results.json',
    'review/independent_checks.py','review/independent_results.json']


def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    source = Path(__file__).read_bytes()
    (A / 'ROOT_CURRENT_INSPECTION_PRELAUNCH_SOURCE.py').write_bytes(source)
    mf = load(read(C / 'MANIFEST.json')); assert sha((C / 'MANIFEST.json').read_bytes()) == MF
    assert mf['self_excluded'] == ['MANIFEST.json'] and mf['files_count'] == len(mf['files']) == 347
    names = {row['path'] for row in mf['files']}
    assert len(names) == 347 and 'MANIFEST.json' not in names
    files, dirs, objects = set(), set(), {}
    for p in C.rglob('*'):
        assert not p.is_symlink()
        n = p.relative_to(C).as_posix()
        if p.is_file(): files.add(n)
        else:
            assert p.is_dir(); dirs.add(n)
    assert files == names | {'MANIFEST.json'}
    assert dirs == {p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    for row in mf['files']:
        assert type(row['bytes']) is int and row['mode'] == '0444'
        raw = read(C / row['path'],row)
        assert stat.S_IMODE((C / row['path']).stat().st_mode) == 0o444
        if row['path'].endswith('.json'): objects[row['path']] = load(raw)
    assert stat.S_IMODE((C / 'MANIFEST.json').stat().st_mode) == 0o444
    deps = objects['CURRENT_DEPENDENCIES.json']
    assert deps['anchor_repository_relative'] == A.relative_to(R).as_posix()
    assert len(deps['files']) == len({row['path']for row in deps['files']}) == 274
    for row in deps['files']: read(A / row['path'],row)
    fresh = load(read(A / 'ROOT_CURRENT_INPUT_PREIMAGES.json'))
    assert fresh['files'] == deps['current_native13'] and len(fresh['files']) == 13
    assert git('branch','--show-current') == 'main'
    assert git('rev-parse','HEAD') == fresh['current_head']
    for row in fresh['files']: read(R / row['path'],row)
    originals = objects['original_snapshot_manifest.json']['files']
    assert len(originals) == 16
    for row in originals:
        raw = read(C / 'original_archive' / row['path'],dict(path=row['path'],bytes=row['size'],sha256=row['sha256']))
        assert raw == read(A / 'source_snapshot' / row['path'])
        if row['path'] in IMMUTABLE: assert read(C / row['path']) == raw
    assert read(C / 'turns.jsonl') == b''
    for name in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']:
        obj = objects[name]
        assert obj['status'] == 'already_solved' and obj['full_target_resolved_in_prior_published_literature'] is True
        assert obj['full_problem_solved_by_project'] is False and obj['novelty_claimed'] is False
        assert all(type(obj[k]) is int and obj[k] == v for k,v in [('original_substantive_attempts',0),('substantive_attempt_limit',5),('new_substantive_attempts',0),('audit_turns',0)])
        assert all(obj[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict'])
        assert all(obj[k] is False for k in ['paper_created','new_DOI_created','tracker_row_created'])
    ref = objects['CURRENT_EXECUTION_REFERENCE.json']
    outer = A / ref['audit_relative_outer_capture']; inner = A / ref['audit_relative_inner_attempt']
    cap = load(read(outer / 'CAPTURE.json'))
    assert cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code'] == 0
    assert cap['pid'] == ref['actual_builder_pid'] == 68759 and cap['operator_pid'] == ref['outer_parent_pid'] == 68758
    assert cap['builder_unchanged_after_child'] is True and cap['operator_unchanged_after_child'] is True
    assert cap['status'] == 'ACTUAL_ADMINISTRATIVE_CAPTURE_COMPLETE_WHOLE_REVIEW_PENDING'
    assert sha(read(outer / 'PRELAUNCH_BUILDER_SOURCE.py')) == cap['builder_sha256']
    assert sha(read(outer / 'PRELAUNCH_OPERATOR.py')) == cap['operator_sha256']
    for channel in ['stdout','stderr']: read(outer / cap[channel]['path'],cap[channel])
    stdout = load(read(outer / 'stdout.bin')); assert stdout['manifest_sha256'] == MF and stdout['native_writes'] == 0
    final_commands = load(read(inner / 'GIT_COMMANDS.json'))
    prefix = objects['build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json']
    assert prefix == final_commands[:len(prefix)]
    for command in final_commands:
        assert command['actual_execution'] is True and command['completed'] is True
        assert type(command['pid']) is int and command['pid'] > 0 and type(command['exit_code']) is int and command['exit_code'] == 0
        for channel in ['stdout','stderr']: read(inner / command[channel]['path'],command[channel])
    invocation = load(read(inner / 'INVOCATION.json'))
    assert invocation['pid'] == 68759 and invocation['parent_pid'] == 68758
    assert sha(read(inner / 'PRELAUNCH_BUILDER_SOURCE.py')) == cap['builder_sha256']
    q = objects['CURRENT_QUEUE_PATCH.json']
    before = read(C / 'queue_proposal/QUEUE_PREIMAGE.md'); after = read(C / 'queue_proposal/QUEUE_PROSPECTIVE.md')
    assert sha(before) == q['whole_preimage_sha256'] and sha(after) == q['whole_prospective_sha256']
    assert before == read(R / 'unsolved_math_prioritization/QUEUE.md')
    assert before.count(q['row_before'].encode()) == 1
    assert after == before.replace(q['row_before'].encode(),q['row_prospective'].encode(),1)
    b,a = q['row_before'].split('|'),q['row_prospective'].split('|')
    assert len(b) == len(a) == 14 and all(x == y for i,(x,y)in enumerate(zip(a,b)) if i not in [8,9,11])
    result = {'status':'PASS_ROOT_ACTUAL_WHOLE_CURRENT_PACKET_INSPECTION',
        'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'pid':os.getpid(),
        'source_sha256':sha(source),'manifest_sha256':MF,'members_excluding_manifest':347,
        'dependencies':274,'full_JSON_objects_consumed':len(objects),'original16_byte_exact':True,
        'actual_builder_pid':68759,'actual_outer_operator_pid':68758,
        'final_inner_GIT_commands':len(final_commands),'prefix_GIT_commands':len(prefix),
        'complete_final_execution_artifacts_read':True,'native13_unchanged':True,
        'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,
        'full_problem_solved_by_project':False,'new_whole_adversary_gate':'PENDING',
        'scientific_helpers_executed':False}
    write('ROOT_ACTUAL_CURRENT_PACKET_INSPECTION.json',result)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
