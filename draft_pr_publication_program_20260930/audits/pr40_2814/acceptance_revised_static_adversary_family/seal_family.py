#!/usr/bin/env python3
"""Own strict final closure. No reviewed helper imports or execution."""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
R = HERE.parents[3]
SELF = 'FIRST_PARTY_MANIFEST.json'


def insist(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            insist(k not in result, 'Duplicate JSON')
            result[k] = v
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError('Nonfinite JSON ' + v)))


def typed(v):
    if type(v) is dict:
        for child in v.values():
            typed(child)
    elif type(v) is list:
        for child in v:
            typed(child)
    elif type(v) is float:
        insist(math.isfinite(v), 'Nonfinite float')
    else:
        insist(type(v) in {str, int, bool, type(None)}, 'Unknown JSON type')


def main():
    insist(not (HERE / SELF).exists(), 'Self manifest already exists; inspect, never overwrite')
    inspected = parse((HERE / 'inspect_revised_inputs_actual_capture/stdout.bin').read_bytes())
    for row in inspected['complete_inputs']:
        path = R / row['path']
        insist(path.is_file() and not path.is_symlink(), 'Changed retained input regularity')
        raw = path.read_bytes()
        insist(type(row['bytes']) is int and len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Bound input changed before sealing ' + row['path'])
    names, directories = set(), set()
    rows = []
    json_count = 0
    for p in sorted(HERE.rglob('*')):
        insist(not p.is_symlink() and (p.is_dir() or p.is_file()), 'Special first-party member')
        n = p.relative_to(HERE).as_posix()
        if p.is_dir():
            directories.add(n)
            continue
        raw = p.read_bytes()
        names.add(n)
        rows.append({'path': n, 'bytes': len(raw), 'sha256': sha(raw)})
        if p.suffix == '.json':
            typed(parse(raw))
            json_count += 1
    expected_directories = {d.as_posix() for n in names for d in PurePosixPath(n).parents if d.as_posix() != '.'}
    insist(directories == expected_directories, 'Extra empty directory in first-party closure')
    for n in ['inspect_revised_inputs_actual_capture', 'finite_guard_controls_actual_capture', 'write_review_metadata_actual_capture']:
        base = HERE / n
        cap = parse((base / 'CAPTURE.json').read_bytes())
        insist(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid'] > 0 and type(cap['exit_code']) is int and cap['exit_code'] == 0, 'Actual own completed capture required')
        insist(cap['cwd'] == str(HERE) and cap['argv'][0] == '/usr/bin/python3', 'Own actual cwd/argv')
        start, finish = [dt.datetime.fromisoformat(cap[k]) for k in ('started_utc', 'finished_utc')]
        insist(start.tzinfo is not None and finish.tzinfo is not None and start.utcoffset() == finish.utcoffset() == dt.timedelta(0) and start <= finish, 'Own actual aware UTC interval')
        insist(sha((base / 'prelaunch_source.py').read_bytes()) == cap['source_sha256'], 'Own prelaunch source')
        for key in ['stdout', 'stderr']:
            row = cap[key]
            raw = (base / row['path']).read_bytes()
            insist(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Own full stream binding')
        insist({p.name for p in base.iterdir()} == {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}, 'Own exact four-file capture')
    meta = parse((HERE / 'write_review_metadata_actual_capture/stdout.bin').read_bytes())
    for key in ['assessment', 'report', 'coverage']:
        row = meta[key]
        archive_name = {'assessment': 'ASSESSMENT.json', 'report': 'REPORT.md', 'coverage': 'READ_COVERAGE.json'}[key]
        raw = (HERE / 'historical_metadata_before_final_closure' / archive_name).read_bytes()
        insist(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Dated own metadata output not preserved')
    assessment = parse((HERE / 'ASSESSMENT.json').read_bytes())
    insist(assessment['mandatory_defects'] == [] and assessment['status'] == 'PASS_QUALIFIED_SOURCE_ONLY', 'Qualified static verdict')
    report = (HERE / 'REPORT.md').read_bytes()
    insist(sha(report) == assessment['report']['sha256'] and len(report) == assessment['report']['bytes'], 'Final complete report binding')
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    obj = {'schema': 'pr40-fresh-revised-static-first-party-closure/v1', 'closed_utc': now,
           'status': 'PASS_QUALIFIED_SOURCE_ONLY', 'self_excluded_paths': [SELF], 'files_count': len(rows),
           'files': rows, 'directories': sorted(directories), 'foreign_excluded_prefixes': [], 'scratch_exclusions': [],
           'reviewed_preparation_manifest_sha256': '65e71adae289b4243036f50be90b28bdeadca3dbd3fd99c5dfc605a72e053c0e',
           'own_complete_JSON_members_excluding_self': json_count,
           'reviewed_helper_import_compile_execution': False, 'actual_future_acceptance_claimed': False,
           'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
           'full_problem_solved': False, 'novelty_claimed': False, 'paper_or_new_DOI_or_tracker': False,
           'static_review_completion_percent': 100, 'mathematical_discovery_completion_percent': 0}
    with (HERE / SELF).open('x') as stream:
        stream.write(json.dumps(obj, sort_keys=True, indent=2) + '\n')
    for row in rows:
        raw = (HERE / row['path']).read_bytes()
        insist(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Changed authored bytes before close')
        (HERE / row['path']).chmod(0o444)
    (HERE / SELF).chmod(0o444)
    insist({p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()} == names | {SELF}, 'Final literal self closure')
    print(json.dumps({'status': obj['status'], 'closed_utc': now, 'first_party_members': len(rows), 'manifest_sha256': sha((HERE / SELF).read_bytes()), 'first_party_JSON_including_self': json_count + 1}))


if __name__ == '__main__':
    main()
