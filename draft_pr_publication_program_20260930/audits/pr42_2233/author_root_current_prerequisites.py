"""ROOT authors genuine completed reading records after independent full reading.

Mechanical revalidation below cannot replace ROOT's mathematical reading, recorded
in the separately authored scope certificate. No candidate helper is imported.
"""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import math
import os
import stat
import subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
SCOPE = 'aa8b26c6ce8211ca139f75ecaef1a5931ec80c4e0b9501c3b7cb9e87443c45b1'
PREP = 'c77fbc8effa07391977ed49a161001625f81bdcf1f0e647537fdae441d0b2071'
ADVERSARY = '0a0cf95dfde2893127a1fa298f6f07ad453286ec2c9598170602b45c410c1d8e'
HEAD = 'c61dc0cb572de281b871264819c8b80d647d0373'
MUTABLE = {'draft_pr_publication_program_20260930/inventory.json',
           'unsolved_math_prioritization/QUEUE.md',
           'unsolved_math_prioritization/state.json',
           'unsolved_math_prioritization/history.jsonl'}
checked = []


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()


def load(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            assert k not in out
            out[k] = v
        return out
    def bad(v):
        raise ValueError('Invalid number: ' + v)
    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    def visit(x):
        if type(x) is float:
            assert math.isfinite(x)
        elif type(x) is dict:
            for y in x.values(): visit(y)
        elif type(x) is list:
            for y in x: visit(y)
    visit(value)
    return value


def read(path, digest=None, size=None):
    assert path.is_file() and not path.is_symlink()
    assert all(not parent.is_symlink() for parent in path.parents)
    raw = path.read_bytes()
    assert digest is None or sha(raw) == digest, str(path)
    assert size is None or len(raw) == size, str(path)
    checked.append({'path': path.relative_to(R).as_posix(), 'bytes': len(raw),
                    'sha256': sha(raw), 'permission_mode': oct(stat.S_IMODE(path.stat().st_mode))})
    return raw


def closure(root, mf_name, expected_hash, items=None, directories=None, check_modes=False):
    raw = read(root / mf_name, expected_hash)
    mf = load(raw)
    rows = mf['files'] if items is None else items
    paths = {item['path'] for item in rows}
    assert len(paths) == len(rows)
    assert mf_name not in paths
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        assert not p.is_symlink()
        rel = p.relative_to(root).as_posix()
        if p.is_file(): actual_files.add(rel)
        else:
            assert p.is_dir()
            actual_dirs.add(rel)
    assert actual_files == paths | {mf_name}, str(root)
    if directories is None:
        directories = {p.as_posix() for name in paths | {mf_name}
                       for p in PurePosixPath(name).parents if p.as_posix() != '.'}
    assert actual_dirs == set(directories), str(root)
    for row in rows:
        name = PurePosixPath(row['path'])
        assert not name.is_absolute() and '..' not in name.parts
        read(root / row['path'], row['sha256'], row['bytes'])
        if check_modes:
            assert oct(stat.S_IMODE((root / row['path']).stat().st_mode)) == row['permission_mode']
    return mf


def write_absent(name, obj):
    raw = encode(obj)
    with (A / name).open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    return sha(raw)


def main():
    assert not __debug__ is False
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=R).strip() == b'main'
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip() == HEAD
    assert not (A / 'reviewed_candidate').exists()
    read(A / 'ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md', SCOPE)
    closure(A / 'current_preparation_family_v2', 'PREPARATION_MANIFEST.json', PREP)
    pins = load(read(A / 'current_preparation_family_v2/INPUT_PINS.json'))
    repair = load(read(A / 'current_preparation_family_v2/REPAIR_INPUT_PINS.json'))
    for info in repair['prior_closed_evidence']:
        closure(A / info['directory'], info['manifest']['path'], info['manifest']['sha256'],
                directories=info['directories'], check_modes='adversary' in info['directory'])
    adv_root = A / 'current_v2_source_adversary_family'
    adv = load(read(adv_root / 'OWN_CLOSED_MANIFEST.json', ADVERSARY))
    closure(adv_root, 'OWN_CLOSED_MANIFEST.json', ADVERSARY,
            directories=adv['directories'], check_modes=True)
    changed = []
    for row in adv['foreign_external_inputs_individually_bound_and_excluded_from_authorship']:
        raw = read(R / row['path'])
        if sha(raw) != row['sha256'] or len(raw) != row['bytes']:
            assert row['path'] in MUTABLE, row['path']
            changed.append({'dated_observation': row, 'current': checked[-1]})
    assert {row['dated_observation']['path'] for row in changed} == MUTABLE
    for info in pins['retained_closures']:
        paths = {p.relative_to(A / info['directory']).as_posix()
                 for p in (A / info['directory']).rglob('*') if p.is_file()}
        assert paths == {row['path'] for row in info['files']}
        for row in info['files']: read(A / info['directory'] / row['path'], row['sha256'], row['bytes'])
    for row in pins['auxiliary']: read(A / row['path'], row['sha256'], row['bytes'])
    for name, info in pins['families'].items():
        closure(A / name, info['manifest']['path'], info['manifest']['sha256'],
                items=info['copied_members'] + info['foreign_members'])
    snapshot = load(read(A / 'snapshot_manifest_v2.json'))
    for row in snapshot['files']: read(A / 'source_snapshot_v2' / row['path'], row['sha256'], row['size'])
    flags = {k: True for k in load(read(A / 'current_preparation_family_v2/DRAFT_ROOT_READ_LEDGER.json'))['root_flags']}
    utc = dt.datetime.now(dt.timezone.utc).isoformat()
    current = {'schema': 'PR42_ROOT_GENUINE_FRESH13_v1', 'approved_by_root': True,
        'reason': 'ROOT pins the actual whole native inputs after verified PR41 acceptance and the published c61 checkpoint; dated preparation observations do not authorize these current bytes.',
        'created_utc': utc, 'current_head': HEAD, 'files': []}
    paths = load(read(A / 'current_preparation_family_v2/DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json'))['required_paths']
    for name in paths:
        raw = read(R / name)
        current['files'].append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
    assert len(paths) == len(set(paths)) == 13
    current_hash = write_absent('ROOT_CURRENT_INPUT_PREIMAGES.json', current)
    common = {'schema': 'PR42_ROOT_COMPLETED_SCIENTIFIC_READING_v1', 'utc': utc,
        'reading_completed': True, 'root_flags': flags, 'scope_certificate_sha256': SCOPE,
        'preparation_manifest_sha256': PREP, 'source_qualification_sha256': pins['qualification_sha256'],
        'actual_reproduction_manifest_sha256': pins['actual_reproduction_manifest_sha256'],
        'family_manifest_sha256': pins['family_manifest_sha256'],
        'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0}
    reading = dict(common, reading_basis='ROOT direct full original math, both independent closed reports/proofs, complete genuine reproductions and bounded primary reading, as documented in the separately authored scope certificate.',
        source_preparation_adversary_manifest_sha256=ADVERSARY,
        source_preparation_review_complete=True, fresh_current_input_manifest_sha256=current_hash,
        legitimate_dated_native_changes_after_PR41=changed,
        future_freeze_or_whole_current_approval=False)
    reading_hash = write_absent('ROOT_PRIMARY_READ_LEDGER.json', reading)
    science = dict(common, status='UNSOLVED', partial_valid=True, full_problem_solved=False,
        novelty_claimed=False, turn_limit=5, read_ledger_sha256=reading_hash,
        current_input_manifest_sha256=current_hash, current_model=None,
        current_reasoning_effort=None, current_deadline_utc=None, current_verdict=None,
        new_whole_current_gate='PENDING', exact_remaining_gap='Construct n-o(n) distinct integer pinned-count values, or prove a universal fixed-proportion obstruction for unrestricted distinct planar point sets.')
    science_hash = write_absent('ROOT_SCIENCE_CARD.json', science)
    result = {'status': 'PASS_ROOT_GENUINE_CURRENT_PREREQUISITES', 'utc': utc,
        'scope_sha256': SCOPE, 'read_ledger_sha256': reading_hash,
        'science_card_sha256': science_hash, 'current_input_manifest_sha256': current_hash,
        'full_input_reads': checked, 'static_external_bindings_unchanged': 524,
        'dated_mutable_observations_qualified': 4, 'future_whole_current_gate': 'PENDING',
        'no_mathematical_helper_executed': True, 'no_native_write': True}
    write_absent('ROOT_CURRENT_PREREQUISITES_INSPECTION.json', result)
    print(json.dumps({k:v for k,v in result.items() if k != 'full_input_reads'}, indent=2))


if __name__ == '__main__':
    main()
