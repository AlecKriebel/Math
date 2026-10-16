"""ROOT rechecks the closed NEW whole-current adversary and its exact inputs."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import os
import stat
from author_root_current_prerequisites import load, read, encode

A = Path(__file__).resolve().parent
R = A.parents[2]
F = A / 'whole_current_source_first_family'
PIN = '8cf1878a94133feb6a68d757481978630114262c0490451b54176395fc4ec0fe'


def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    raw = read(F / 'OWN_CLOSED_MANIFEST.json', PIN)
    mf = load(raw)
    assert mf['self_excluded'] == ['OWN_CLOSED_MANIFEST.json']
    assert type(mf['files_count']) is int and mf['files_count'] == len(mf['files']) == 25
    names = {row['path'] for row in mf['files']}
    assert len(names) == 25 and 'OWN_CLOSED_MANIFEST.json' not in names
    files, dirs = set(), set()
    for p in F.rglob('*'):
        assert not p.is_symlink()
        n = p.relative_to(F).as_posix()
        if p.is_file(): files.add(n)
        else:
            assert p.is_dir()
            dirs.add(n)
    assert files == names | {'OWN_CLOSED_MANIFEST.json'}
    assert dirs == {p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    total = 0
    for row in mf['files']:
        assert row['permission_mode'] == '0o444' and type(row['bytes']) is int
        data = read(F / row['path'], row['sha256'], row['bytes'])
        assert stat.S_IMODE((F / row['path']).stat().st_mode) == 0o444
        total += len(data)
        if row['path'].endswith('.json'): load(data)
    assert stat.S_IMODE((F / 'OWN_CLOSED_MANIFEST.json').stat().st_mode) == 0o444
    foreign = mf['foreign_files_individually_pinned_and_excluded']
    assert len(foreign) == len({row['path'] for row in foreign}) == 925
    for row in foreign:
        p = Path(row['path'])
        assert p.is_absolute() and R in p.parents and F not in p.parents
        assert type(row['bytes']) is int and row['bytes'] >= 0
        read(p, row['sha256'], row['bytes'])
    result = load(read(F / 'RESULT.json'))
    assert result['status'] == 'PASS_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
    assert result['whole_current_review_complete'] is True and result['scoped_mathematics_verified'] is True
    assert result['mandatory_defects'] == result['mandatory_corrections'] == []
    assert result['candidate_manifest_sha256'] == '09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de'
    assert result['full_problem_solved'] is False and result['original_problem_status'] == 'UNSOLVED'
    assert result['own_math_demands'] == 57839 and result['own_rejected_mutations'] == 4
    obj = {'schema':'pr42-root-complete-closed-whole-inspection/v1',
        'status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION',
        'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'candidate_manifest_sha256':result['candidate_manifest_sha256'],
        'closed_whole_manifest_sha256':PIN, 'first_party_members':25,
        'individually_bound_foreign_inputs':925, 'complete_RESULT_object':result,
        'personal_report_and_result_fully_read':True,
        'all_first_party_whole_bytes_and_modes_checked':True,
        'all_foreign_individual_whole_bytes_checked':True,
        'exact_self_only_recursive_closure_checked':True,
        'mandatory_defects':[],'mandatory_corrections':[],
        'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,
        'full_problem_solved':False,'future_execution_approved':False}
    with (A / 'ROOT_WHOLE_CURRENT_REVIEW.json').open('xb') as out:
        out.write(encode(obj)); out.flush(); os.fsync(out.fileno())
    print(json.dumps({'status':obj['status'], 'own_member_bytes':total,
                     'first_party_members':25,'foreign_inputs':925,
                     'ROOT_WHOLE_CURRENT_REVIEW_sha256':hashlib.sha256(encode(obj)).hexdigest()},indent=2))


if __name__ == '__main__':
    main()
