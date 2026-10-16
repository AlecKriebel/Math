#!/usr/bin/env python3
"""Separate read-only verifier of this SOURCE adversary's complete self closure."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import stat
import os
import sys

assert __debug__ and sys.flags.optimize == 0
F = Path(__file__).resolve().parent
EXPECTED = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr46_30004438/acceptance_source_adversary_family')
assert F == EXPECTED and not EXPECTED.is_symlink()
SELF = 'SELF_MANIFEST.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            assert key not in result
            result[key] = value
        return result
    def invalid(value):
        raise AssertionError('nonfinite JSON ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def inventory():
    files, dirs = [], [F]
    for path in sorted(F.rglob('*')):
        mode = path.lstat().st_mode
        assert not stat.S_ISLNK(mode)
        if stat.S_ISDIR(mode):
            dirs.append(path)
        else:
            assert stat.S_ISREG(mode)
            if path.name != SELF or path.parent != F:
                files.append(path)
    assert not (F / 'PRIVATE_MODEL').exists() and not (F / 'MODE_PROBE').exists()
    assert all(p.suffix.lower() not in {'.pdf', '.png', '.sqlite', '.db'} for p in files)
    expected_dirs = {'.'} | {q.as_posix() for p in files for q in PurePosixPath(p.relative_to(F).as_posix()).parents}
    assert {'.' if p == F else p.relative_to(F).as_posix() for p in dirs} == expected_dirs
    return files, dirs


def own_ref(ref):
    p = Path(ref['path'])
    if not p.is_absolute():
        p = F / p
    assert F in p.parents and p.resolve() == p and not p.is_symlink()
    assert stat.S_ISREG(p.lstat().st_mode)
    raw = p.read_bytes()
    assert type(ref['bytes']) is int and len(raw) == ref['bytes'] and sha(raw) == ref['sha256']
    return raw


def captures():
    rows = []
    for path in sorted((F / 'captures').glob('*/CAPTURE.json')):
        cap = load(path.read_bytes())
        pre = load((path.parent / 'PRELAUNCH.json').read_bytes())
        assert cap['schema'] == 'pr46-source-adversary-real-command-capture/v1'
        assert pre['schema'] == 'pr46-source-adversary-real-prelaunch/v1'
        assert cap['argv'] == pre['argv'] and cap['cwd'] == pre['cwd']
        assert cap['operator_pid'] == pre['operator_pid'] and type(cap['operator_pid']) is int
        assert type(cap['child_pid']) is int and cap['child_pid'] > 0
        assert type(cap['exit_code']) is int and cap['expected_exit'] == pre['expected_exit']
        expected_status = 'PASS_EXPECTED_EXIT' if cap['exit_code'] == cap['expected_exit'] else 'FAIL_UNEXPECTED_EXIT'
        assert cap['status'] == expected_status
        for key in ['operator', 'prelaunch', 'stdout', 'stderr']:
            own_ref(cap[key])
        assert own_ref(cap['operator']) == (path.parent / 'prelaunch_operator.py').read_bytes()
        members = {'CAPTURE.json', 'PRELAUNCH.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}
        if cap['child_source'] is not None:
            assert cap['child_source'] == pre['child_source']
            assert own_ref(cap['child_source']) == (path.parent / 'prelaunch_child_source.py').read_bytes()
            members.add('prelaunch_child_source.py')
        assert {p.name for p in path.parent.iterdir()} == members
        clocks = [datetime.fromisoformat(pre['created_utc']), datetime.fromisoformat(cap['started_utc']),
                  datetime.fromisoformat(cap['finished_utc'])]
        assert all(d.tzinfo is not None and d.utcoffset().total_seconds() == 0 for d in clocks)
        assert clocks == sorted(clocks)
        rows.append({'path': path.relative_to(F).as_posix(), 'bytes': path.stat().st_size,
                     'sha256': sha(path.read_bytes()), 'child_pid': cap['child_pid'],
                     'exit_code': cap['exit_code'], 'status': cap['status'],
                     'complete_prelaunch_source_and_split_streams_read': True})
    assert len(rows) == 7 and sum(row['exit_code'] != 0 for row in rows) == 1
    return rows


def external_bindings():
    report = load((F / 'OWN_INPUT_READ_BINDINGS.json').read_bytes())
    assert report['normalized_external_count'] == len(report['external_bindings']) == 2611
    checked = []
    for row in report['external_bindings']:
        path = Path(row['path'])
        assert path.is_absolute() and path.resolve() == path and F not in path.parents
        assert not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode)
        for parent in path.parents:
            assert not parent.is_symlink()
        raw = path.read_bytes()
        assert type(row['bytes']) is int and len(raw) == row['bytes'] and sha(raw) == row['sha256']
        assert type(row['full_mode']) is int and stat.S_IMODE(path.stat().st_mode) == row['full_mode']
        checked.append({'path': row['path'], 'bytes': len(raw), 'sha256': sha(raw), 'full_mode': row['full_mode']})
    return checked


def check_verdict():
    verdict = load((F / 'VERDICT.json').read_bytes())
    assert verdict['schema'] == 'pr46-acceptance-source-adversary-verdict/v1'
    assert verdict['verdict'] == 'REJECT_MANDATORY_SOURCE_CORRECTION'
    assert verdict['preparation_manifest_sha256'] == 'd97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab'
    assert [row['id'] for row in verdict['mandatory_corrections']] == ['S1']
    assert verdict['production_imported_compiled_executed'] is False and verdict['future_acceptance_approved'] is False
    assert verdict['original_substantive_attempts'] == 0 and verdict['original_source_verification_responses'] == 1
    assert verdict['new_substantive_attempts'] == verdict['audit_turns'] == 0
    for row in verdict['evidence_bindings']:
        own_ref(row)
    return verdict


def verify():
    files, dirs = inventory()
    raw = (F / SELF).read_bytes()
    mf = load(raw)
    assert mf['schema'] == 'pr46-acceptance-source-adversary-self-closure/v1'
    assert mf['self_excluded'] == [SELF] and type(mf['files_count']) is int
    assert len(files) == mf['files_count'] == len(mf['files'])
    assert [p.relative_to(F).as_posix() for p in files] == [r['path'] for r in mf['files']]
    for path, row in zip(files, mf['files']):
        body = path.read_bytes()
        assert len(body) == row['bytes'] and sha(body) == row['sha256']
        assert stat.S_IMODE(path.stat().st_mode) == row['full_mode'] == 0o444
    assert stat.S_IMODE((F / SELF).stat().st_mode) == 0o444
    actual_dirs = sorted('.' if p == F else p.relative_to(F).as_posix() for p in dirs)
    assert actual_dirs == [r['path'] for r in mf['directories']]
    for row in mf['directories']:
        path = F if row['path'] == '.' else F / row['path']
        assert stat.S_IMODE(path.stat().st_mode) == row['full_mode'] == (0o755 if path == F else 0o700)
    assert check_verdict()['verdict'] == mf['verdict']
    assert captures() == mf['complete_prior_actual_captures']
    assert external_bindings() == mf['external_full_body_mode_readback']
    return {'status': 'PASS_STRICT_FROZEN_SOURCE_ADVERSARY_READBACK', 'manifest_sha256': sha(raw),
            'payload_files': len(files), 'files_with_self': len(files) + 1, 'directories_including_root': len(dirs),
            'prior_actual_captures': len(mf['complete_prior_actual_captures']),
            'individual_external_bindings_checked': len(mf['external_full_body_mode_readback']),
            'source_verdict': mf['verdict'], 'future_acceptance_approved': False}


if __name__ == '__main__':
    result = verify()
    result.update(actual_pid=os.getpid(), finished_utc=datetime.now(timezone.utc).isoformat())
    print(json.dumps(result, indent=2))
