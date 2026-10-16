#!/usr/bin/env python3
"""Independent byte/topology/type inspection. Reviewed sources are AST data only."""
import ast
import copy
import datetime as dt
import difflib
import hashlib
import json
import math
import re
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
A = HERE.parent
R = A.parents[2]
S = A / 'acceptance_execution_preparation_family/integration_source_revision'
O = A / 'acceptance_preparation_family'
PIN = '65e71adae289b4243036f50be90b28bdeadca3dbd3fd99c5dfc605a72e053c0e'
SEEN = {}
PARSED = {}


def insist(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(items):
        out = {}
        for k, value in items:
            insist(k not in out, 'Duplicate JSON key ' + k)
            out[k] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError('Nonfinite JSON ' + v)))


def equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def typed(obj):
    if type(obj) is dict:
        insist(all(type(k) is str for k in obj), 'Nonstring object key')
        for value in obj.values():
            typed(value)
    elif type(obj) is list:
        for value in obj:
            typed(value)
    else:
        insist(type(obj) in {str, bool, int, float, type(None)}, 'Unexpected JSON type')
        if type(obj) is float:
            insist(math.isfinite(obj), 'Nonfinite parsed float')


def read(path):
    insist(path.is_file() and not path.is_symlink(), 'Not a regular file ' + str(path))
    for parent in path.parents:
        insist(not parent.is_symlink(), 'Symlink ancestor ' + str(parent))
        if parent == R:
            break
    raw = path.read_bytes()
    key = path.relative_to(R).as_posix()
    row = {'path': key, 'bytes': len(raw), 'sha256': sha(raw)}
    insist(key not in SEEN or equal(SEEN[key], row), 'Changed input during inspection')
    SEEN[key] = row
    if path.suffix in {'.json', '.jsonl'}:
        if path.suffix == '.jsonl':
            insist(not raw or raw.endswith(b'\n'), 'Truncated JSONL')
            value = [parse(line) for line in raw.splitlines()]
        else:
            value = parse(raw)
        typed(value)
        PARSED[key] = value
    return raw


def load(path):
    raw = read(path)
    value = parse(raw)
    typed(value)
    return value


def path_name(n):
    insist(type(n) is str and n and '\\' not in n and '\0' not in n, 'Invalid path')
    p = PurePosixPath(n)
    insist(not p.is_absolute() and '..' not in p.parts and n == p.as_posix(), 'Noncanonical path ' + n)
    return p


def rows(value):
    if type(value) is dict:
        value = [{'path': k, **v} for k, v in value.items()]
    insist(type(value) is list, 'Rows must be list or explicitly keyed object')
    result = []
    for row in value:
        insist(type(row) is dict, 'Row must be object')
        path_name(row['path'])
        insist(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'Bad digest')
        size = row['bytes'] if 'bytes' in row else row['size']
        insist(type(size) is int and size >= 0, 'Bad typed byte size')
        if 'bytes' in row and 'size' in row:
            insist(equal(row['bytes'], row['size']), 'Conflicting sizes')
        result.append({**row, 'bytes': size})
    insist(len({row['path'] for row in result}) == len(result), 'Duplicate row')
    return result


def check(base, value):
    result = rows(value)
    for row in result:
        raw = read(base / row['path'])
        insist(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Full bytes changed ' + row['path'])
    return result


def closure(base, names, excluded=()):
    insist(base.is_dir() and not base.is_symlink(), 'Unsafe closure root')
    wanted = set(names)
    files, directories = set(), set()
    for child in base.rglob('*'):
        n = child.relative_to(base).as_posix()
        p = path_name(n)
        if p.parts[0] in excluded:
            continue
        insist(not child.is_symlink() and (child.is_file() or child.is_dir()), 'Special closure member ' + n)
        (files if child.is_file() else directories).add(n)
    wanted_directories = {p.as_posix() for n in wanted for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    insist(files == wanted and directories == wanted_directories, 'Files/directories differ ' + str(base))


def manifest(base, name, pin, count, field='files', excluded=()):
    raw = read(base / name)
    insist(sha(raw) == pin, 'Wrong manifest pin ' + str(base))
    obj = parse(raw)
    rr = check(base, obj[field])
    insist(len(rr) == count and name not in {z['path'] for z in rr}, 'Wrong count/self exclusion')
    for k in ('files_count', 'member_count'):
        if k in obj:
            insist(type(obj[k]) is int and obj[k] == count, 'Declared count/type mismatch')
    closure(base, {z['path'] for z in rr} | {name}, excluded)
    return obj


def required(obj, expected):
    insist(type(obj) is dict, 'Object required')
    for k, value in expected.items():
        insist(k in obj and equal(obj[k], value), 'Wrong required typed field ' + k)


def main():
    revision = manifest(S, 'PREPARATION_MANIFEST.json', PIN, 15)
    old = manifest(O, 'PREPARATION_MANIFEST.json', 'a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b', 12)
    prior_static = manifest(A / 'acceptance_static_adversary_family', 'FIRST_PARTY_MANIFEST.json', '84b0e1c5364fac20617c1242e36c0d5b9130ea2784de81d3557ae8cbe94ab526', 22)
    sources = []
    for n in ['pr40_guards.py', 'seal_final_evidence.py', 'integrate_reviewed_partial.py', 'state_mirror_reconciliation.py', 'verify_post_acceptance.py']:
        raw = read(S / n)
        tree = ast.parse(raw, filename=str(S / n))
        insist(isinstance(tree, ast.Module), 'Not a source module')
        sources.append({'path': n, 'lines': len(raw.splitlines()), 'bytes': len(raw), 'sha256': sha(raw)})
    bindings = load(S / 'REVISION_BINDINGS.json')
    check(R, bindings['immutable_revision_inputs'])
    check(R, bindings['original13_source_rows'])
    inputs = load(S / 'INPUT_BINDINGS.json')
    insist(read(S / 'INPUT_BINDINGS.json') == read(O / 'INPUT_BINDINGS.json'), 'Immutable input bindings changed')
    for item in inputs['pins'].values():
        check(R, [item])
    closures = []
    for item in inputs['closures']:
        base = R / item['root']
        if item['manifest'] is None:
            rr = check(base, item['files'])
            closure(base, {z['path'] for z in rr})
            closures.append({'root': item['root'], 'authored_members': len(rr), 'manifest': None})
        else:
            check(R, [item['manifest']])
            obj = load(R / item['manifest']['path'])
            rr = check(base, obj[item['member_field']])
            insist(len(rr) == item['authored_count_excluding_self'], 'Closure count changed')
            name = Path(item['manifest']['path']).name
            insist(name not in {z['path'] for z in rr}, 'Nested names incorrectly self-excluded')
            closure(base, {z['path'] for z in rr} | {name}, item['excluded_root_directories'])
            closures.append({'root': item['root'], 'authored_members': len(rr), 'manifest': name,
                             'exact_declared_private_or_foreign_exclusions': item['excluded_root_directories']})
    foreign = load(A / 'current_preparation_family/INPUT_PINS.json')['foreign_inventory']
    insist(set(foreign) == {'primary_scope_family/foreign_cache', 'geodesic_geometry_family/primary'}, 'Changed original foreign roots')
    foreign_counts = []
    for n, value in foreign.items():
        rr = check(A / n, value['members'])
        closure(A / n, {z['path'] for z in rr})
        foreign_counts.append({'root': n, 'members': len(rr)})
    w = A / 'whole_current_source_first_family'
    wr = check(w, load(w / 'FOREIGN_PRIMARY_INVENTORY.json')['exact_recursive_inventory'])
    insist(len(wr) == 21 and all(PurePosixPath(z['path']).parts[0] == 'ROOTforeign_primary' for z in wr), 'Wrong whole foreign qualification')
    closure(w, {z['path'] for z in rows(load(w / 'FIRST_PARTY_MANIFEST.json')['files']) + wr} | {'FIRST_PARTY_MANIFEST.json'})
    c = A / 'reviewed_candidate'
    current = manifest(c, 'MANIFEST.json', '8de92d903edaec7471f4ecc3df443b7e779732b0ee83cdec507c22025bfae25f', 239)
    insist(all((c / z['path']).stat().st_mode & 0o777 == 0o444 for z in current['files']) and (c / 'MANIFEST.json').stat().st_mode & 0o777 == 0o444, 'Current mode changed')
    dep = load(c / 'CURRENT_PROOF_DEPENDENCIES.json')
    insist(sha(read(c / 'CURRENT_PROOF_DEPENDENCIES.json')) == 'b2c6d31f3e7230e132761322bef9d3b99e1b0f53521fbefc5a281e6682199a37', 'Dependencies changed')
    insist(len(check(A, dep['files'])) == 216, 'Dependency count changed')
    snap = load(A / 'snapshot_manifest.json')
    insist(len(snap['files']) == 13 and len(snap['changed_paths']) == 14, 'Snapshot count changed')
    for z in rows(snap['files']):
        raw = read(A / 'source_snapshot' / z['path'])
        insist(raw == read(c / z['path']) == read(c / 'original_archive' / z['path']), 'Original13 source/root/archive changed')
    required(load(c / 'turns.json'), {'id': 2814, 'count': 0, 'substantive_attempts': []})
    insist(parse(read(c / 'prior_report.json')) is None, 'Literal null original prior changed')
    insist(type(load(c / 'duplicate_prior_report.json')) is dict and bool(load(c / 'duplicate_prior_report.json')), 'Imported complete prior not present')
    pending = {'status': 'UNSOLVED', 'full_problem_solved': False, 'partial_valid': True, 'novelty_claimed': False,
               'source_hold': True, 'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0,
               'audit_attempts_added': 0, 'verification_attempts_added': 0, 'current_model': None,
               'current_reasoning_effort': None, 'current_deadline_utc': None, 'historical_verdict_transferred': False,
               'new_whole_current_gate': 'PENDING'}
    for n in ('acceptance.json', 'status.json', 'attempt.json', 'current_readiness.json'):
        required(load(c / n), pending)
    scope = load(S / 'SCIENTIFIC_SCOPE.json')
    draft = load(S / 'DRAFT_FINAL_PLAN.json')
    insist(equal(draft['scientific_scope'], scope), 'Scope/draft disagree')
    required(draft, {'plan_status': 'DRAFT_REQUIRES_GENUINE_ROOT_REVIEW', 'root_full_current_read_completed': False,
                     'root_full_whole_read_completed': False, 'independent_whole_current_pass': False,
                     'preparation_manifest_sha256': None, 'full_problem_solved': False, 'partial_valid': True,
                     'novelty_claimed': False, 'source_hold': True, 'original_substantive_attempts': 0,
                     'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'verification_attempts_added': 0,
                     'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None,
                     'paper_or_new_doi_or_tracker': False})
    refs = [inputs['pins'][n] for n in sorted(inputs['pins'])]
    insist(equal(draft['immutable_evidence_references'], refs), 'Whole immutable references differ')
    old_scope = load(O / 'SCIENTIFIC_SCOPE.json')
    insist(equal({k: v for k, v in old_scope.items() if k != 'credited_existing_coverage'},
                 {k: v for k, v in scope.items() if k != 'credited_existing_coverage'}), 'Unrequested scientific scope change')
    old_draft = load(O / 'DRAFT_FINAL_PLAN.json')
    omitted = {'scientific_scope', 'draft_prepared_utc'}
    insist(equal({k: v for k, v in old_draft.items() if k not in omitted},
                 {k: v for k, v in draft.items() if k not in omitted}), 'Unrequested full draft change')
    differences = ''.join(''.join(difflib.unified_diff(read(O / n).decode().splitlines(keepends=True),
                                                     read(S / n).decode().splitlines(keepends=True),
                                                     fromfile='original/' + n, tofile='revision/' + n))
                          for n in ['pr40_guards.py', 'integrate_reviewed_partial.py', 'state_mirror_reconciliation.py',
                                    'SCIENTIFIC_SCOPE.json', 'DRAFT_FINAL_PLAN.json', 'CONTRACT.md'])
    insist(differences.encode() == read(S / 'SOURCE_CHANGES.patch'), 'Complete patch reconstruction differs')
    for n in ('seal_final_evidence.py', 'verify_post_acceptance.py'):
        insist(read(S / n) == read(O / n), 'Unrequested unchanged source mutation')
    verdict = load(w / 'ASSESSMENT.json')
    required(verdict, {'review_disposition': 'PASS_BOUNDED_PARTIAL_SOURCE_HOLD', 'genuine_actionable_mathematical_issues': [],
                       'mandatory_frozen_SOURCE_STATUS_corrections': [], 'full_problem_solved_by_project': False,
                       'novelty_claimed': False, 'original_substantive_attempts': 0, 'turn_limit': 5,
                       'new_substantive_attempts': 0, 'audit_turns': 0, 'current_model': None,
                       'current_reasoning_effort': None, 'current_deadline_utc': None,
                       'fully_unexposed_source_first_claimed': False, 'full_recursive_standard_input_certification_claimed': False})
    root = load(A / 'ROOT_WHOLE_CURRENT_REVIEW.json')
    insist(equal(root['whole_independent_verdict'], verdict), 'Whole root verdict object differs')
    raw_native = read(R / 'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py')
    insist(sha(raw_native) == 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f', 'Bound full native driver changed')
    output = {'schema': 'pr40-fresh-revised-static-input-inspection/v1', 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'status': 'PASS_BYTE_TOPOLOGY_AND_TYPED_DATA_ONLY', 'preparation_manifest_sha256': PIN,
              'revised_members': 15, 'original_preparation_members': 12, 'old_static_members': 22,
              'current_members': 239, 'current_json_including_self': sum(k.startswith(c.relative_to(R).as_posix() + '/') for k in PARSED),
              'dependencies': 216, 'original_scientific_files': 13, 'closed_input_scopes': closures,
              'separately_exact_original_foreign_scopes': foreign_counts, 'whole_foreign_members': 21,
              'source_programs': sources, 'reviewed_source_lines': sum(z['lines'] for z in sources),
              'unique_inspected_input_members': len(SEEN), 'unique_inspected_input_bytes': sum(z['bytes'] for z in SEEN.values()),
              'complete_inputs': [SEEN[k] for k in sorted(SEEN)], 'whole_typed_JSON_objects': len(PARSED),
              'reviewed_helper_import_compile_execution': False, 'Git_SQL_native_shared_remote_writes': False,
              'actual_future_acceptance_claimed': False, 'full_problem_solved': False, 'novelty_claimed': False,
              'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0}
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
