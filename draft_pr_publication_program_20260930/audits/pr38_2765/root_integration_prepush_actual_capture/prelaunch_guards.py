"""Static PR38 root-only guards. No import-time mutation or execution.

The preparation agent must never import or execute this module. Future root
execution is gated by explicit final review, scope-contract and actual replay
pins. Git/gh calls below are read-only; root owns every Git/remote mutation.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import traceback
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
A = HERE.parents[1]
R = A.parents[2]
B = R / 'draft_pr_publication_program_20260930'
C = A / 'reviewed_candidate_v2'
K = R / 'unsolved_math_prioritization/attempts/2765'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '2765', 'KP-2.17', 38
HEAD = '980719c79e13ffbc3f5cfbf149c325ea2fb51df0'
ORIGINAL_BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
CURRENT_SHA = 'b48e3e17b884056143a7132fd519872ac5223a0ef15fa4bb3d5738e3f58bb52c'
DEPENDENCIES_SHA = '1b9d41f102cf3345777f4b77c5c5ffbf2db1084d82b6ce8b4a7fb8b5b4af2e79'
SNAPSHOT_SHA = '2c58f3aa5f73920fa62c7103648deee899db3a12f3f48c940576f99eff74dfe2'
LEDGER_SHA = 'b04b008cb90eb04c0586f32eaf2ef59d608ffc8e10f2721acfb70e91584e5737'
SOURCE_SHA = '0d6179bc1f850670535220113fb63b3f87e3cccc4223b94c6c2c3e211c2d421e'
RESULTS_SHA = 'd3c44c82d2ffb2d20080288821381c8fe4e4e79b6d632bfe5c93b94c71716115'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
WRITER_SHA = 'b72afa148d034818cc90fd25b6b084fd94e42604d433a64e09a4ee01ae6e5271'
PREVIOUS = B / 'audits/pr37_3009/state_mirror_bindings.json'
PREVIOUS_SHA = '7d83f82b51d2bede4dd03670e888e1ace53975caf64d4d3dd34b86052c8ef620'
ADMIN = {'README.md', 'pr_body.md', 'readiness.json', 'status.json', 'CURRENT_AUDIT_SCOPE.md', 'RESEARCH_LOG.md', 'attempt.json'}
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
FOREIGN_TRACKED_EXCLUSIONS = {
    'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv',
    'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_equal(actual, expected):
    """JSON equality without Python's bool/int coercion, recursively."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(strict_equal(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(strict_equal(left, right) for left, right in zip(actual, expected))
    return actual == expected


def required_values(actual, expected, context):
    require(type(actual) is dict, context + ': require JSON object')
    for key, value in expected.items():
        require(key in actual and strict_equal(actual[key], value), context + ': missing/wrong type/value for ' + key)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load(path):
    return parse(Path(path).read_bytes())


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode()


def write(path, data, exclusive=False):
    path = Path(path)
    require(path.parent.is_dir() and not path.is_symlink(), 'Unsafe output: ' + str(path))
    if exclusive:
        require(not path.exists(), 'Inspect existing receipt before retry: ' + str(path))
    temporary = path.with_name(path.name + '.pr38-tmp')
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def dump(path, value, exclusive=False):
    write(path, encode(value), exclusive)


def git_bytes(*args):
    return subprocess.check_output(['git', *args], cwd=R, timeout=30)


def git(*args):
    return git_bytes(*args).decode().strip()


def optional_git_file(revision, name):
    entries = git_bytes('ls-tree', '-z', revision, '--', name)
    if not entries:
        return b''
    fields, literal = entries.decode().rstrip('\0').split('\t', 1)
    require(literal == name and fields.split()[1] == 'blob', 'Optional historical path is not an exact blob')
    return git_bytes('show', revision + ':' + name)


def remote():
    value = json.loads(subprocess.check_output([
        'gh', 'pr', 'view', str(PR), '--repo', 'AlecKriebel/Math', '--json',
        'number,url,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,body',
    ], cwd=R, timeout=30))
    require(value['number'] == PR and value['url'] == 'https://github.com/AlecKriebel/Math/pull/38', 'Wrong remote PR')
    require(value['headRefOid'] == HEAD and value['headRefName'] == 'dot/math-' + ID and value['baseRefName'] == 'main', 'Remote original-head/base mismatch')
    return value


def digest(value):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value), 'Require explicit lowercase SHA256')
    return value


def relative(name):
    require(isinstance(name, str) and name and '\\' not in name and '\0' not in name, 'Invalid member name')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == name, 'Unsafe/noncanonical member: ' + name)
    return path


def regular(base, name):
    relative(name)
    base = Path(base)
    path = base / name
    require(base.is_dir() and not base.is_symlink(), 'Unsafe package root')
    require(path.resolve().is_relative_to(base.resolve()) and path.is_file() and not path.is_symlink(), 'Unsafe/nonregular member: ' + name)
    for parent in path.parents:
        if parent == base:
            break
        require(not parent.is_symlink(), 'Symlink ancestor: ' + name)
    return path


def rows(value):
    require(type(value) is list, 'Binding rows must be explicit ordered list')
    names = []
    for row in value:
        require(type(row) is dict, 'Malformed binding row')
        relative(row['path'])
        digest(row['sha256'])
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'Invalid byte count')
        names.append(row['path'])
    require(len(names) == len(set(names)), 'Duplicate binding path')
    return value


def check_rows(base, value):
    for row in rows(value):
        raw = regular(base, row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Bound member changed: ' + row['path'])


def inventory(base):
    base = Path(base)
    require(base.is_dir() and not base.is_symlink(), 'Unsafe closure root')
    files, directories = set(), set()
    for path in base.rglob('*'):
        name = str(path.relative_to(base))
        relative(name)
        require(not path.is_symlink(), 'Symlink in exact recursive closure: ' + name)
        require(path.is_dir() or path.is_file(), 'Nonregular closure entry: ' + name)
        (directories if path.is_dir() else files).add(name)
    return files, directories


def exact_closure(base, expected):
    expected = set(expected)
    actual, directories = inventory(base)
    require(actual == expected, 'Complete recursive file membership differs: ' + str(sorted(actual ^ expected)))
    parents = {str(parent) for name in expected for parent in PurePosixPath(name).parents if str(parent) != '.'}
    require(directories == parents, 'Extra/missing recursive directories: ' + str(sorted(directories ^ parents)))


def manifest(base, path, expected=None, count=None, scope=None):
    """Strict complete closure; only twelve exact current malformed inputs qualified."""
    base, path = Path(base), Path(path)
    require(path.parent == base, 'Require literal root manifest')
    raw = regular(base, path.name).read_bytes()
    if expected is not None:
        require(sha(raw) == digest(expected), 'Pinned manifest changed')
    obj = parse(raw)
    value = normalize_rows(obj['files'])
    require(path.name not in {z['path'] for z in value}, 'Manifest self exclusion required')
    if count is not None:
        require(len(value) == count, 'Exact manifest count differs')
    for key in ['files_count', 'member_count']:
        if key in obj:
            require(type(obj[key]) is int and obj[key] == len(value), 'Declared count/type differs')
    check_rows(base, value)
    malformed = {z['path']: z for z in load(HERE / 'INPUT_BINDINGS.json')['current_malformed_json_exceptions']} if base in {C, K} else {}
    for row in value:
        data = regular(base, row['path']).read_bytes()
        if PurePosixPath(row['path']).suffix == '.json':
            if row['path'] in malformed:
                pin = malformed[row['path']]
                require(all(strict_equal(row[k], pin[k]) for k in ['bytes', 'sha256']), 'Malformed fixture exact bytes changed')
                try:
                    parse(data)
                except json.JSONDecodeError:
                    pass
                else:
                    raise ValueError('Pinned malformed fixture now parses')
            else:
                parse(data)
        elif PurePosixPath(row['path']).suffix == '.jsonl':
            require(not data or data.endswith(b'\n'), 'Incomplete JSONL member')
            for line in data.splitlines():
                parse(line)
    exact_closure(base, {z['path'] for z in value} | {path.name})
    return value


def parse(raw):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, 'Duplicate JSON key: ' + key)
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=unique)


def normalize_rows(value):
    if type(value) is dict:
        value = [{'path': name, **pin} for name, pin in value.items()]
    require(type(value) is list, 'Require complete binding list')
    normalized = []
    for row in value:
        require(type(row) is dict, 'Require typed member binding')
        if 'bytes' in row and 'size' in row:
            require(strict_equal(row['bytes'], row['size']), 'Conflicting byte counts')
        normalized.append({**row, 'bytes': row['bytes'] if 'bytes' in row else row['size']})
    return rows(normalized)


def audit_pin(pin):
    require(type(pin) is dict and set(pin) >= {'path', 'bytes', 'sha256'}, 'Complete explicit audit pin required')
    path = regular(A, pin['path'])
    raw = path.read_bytes()
    require(type(pin['bytes']) is int and len(raw) == pin['bytes'] and sha(raw) == digest(pin['sha256']), 'Audit pin changed: ' + pin['path'])
    return raw


def bound_repository(pin):
    path = regular(R, pin['path'])
    require(path.resolve().is_relative_to(A.resolve()), 'Final evidence must belong to exact PR38 audit')
    raw = path.read_bytes()
    require(type(pin['bytes']) is int and len(raw) == pin['bytes'] and sha(raw) == digest(pin['sha256']), 'Final evidence binding changed: ' + pin['path'])
    return raw


def repo_pin(path):
    raw = Path(path).read_bytes()
    return {'path': str(Path(path).relative_to(R)), 'bytes': len(raw), 'sha256': sha(raw)}


def source_and_ledger(base):
    require(sha(regular(base, 'source_record.json').read_bytes()) == SOURCE_SHA, 'Exact complete original source serialization changed')
    source = load(base / 'source_record.json')
    required_values(source, {'id': int(ID)}, 'Complete flat numeric source')
    actual = load(A / 'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json')
    require(strict_equal(actual['provenance']['complete_flat_problem'], source), 'Complete native/raw/SQL source differs from exact original')
    require((base / 'prior_report.json').read_bytes() == b'null\n', 'Exact historical null prior changed')
    require(strict_equal(load(base / 'native_importer_prior_fallback.json'), {}), 'Empty importer fallback cannot become retrieved report')
    raw = regular(base, 'turns.json').read_bytes()
    require(sha(raw) == LEDGER_SHA, 'Entire two-row original list ledger changed')
    ledger = parse(raw)
    require(type(ledger) is list and len(ledger) == 2 and [z['turn'] for z in ledger] == [1, 2], 'Exact original two turns required')
    require(strict_equal(ledger, load(C / 'original_archive/turns.json')), 'Full original ledger contents differ')
    require([z['artifact'] for z in ledger] == ['RESULTS.md, Sections 1-4', 'RESULTS.md, Section 5'], 'Original artifact references changed')


def immutable_basis():
    """Read full pinned evidence; never replay a scientific program."""
    inputs = load(HERE / 'INPUT_BINDINGS.json')
    pins = inputs['pins']
    bound = []
    for pin in pins.values():
        audit_pin(pin)
        bound.append(repo_pin(A / pin['path']))
    for key, base, count in [('frozen_v1', A / 'reviewed_candidate', 1499), ('reviewed_v2', C, 1502)]:
        obj = load(A / pins[key]['path'])
        members = normalize_rows(obj['files'])
        require(len(members) == count, 'Frozen member count differs')
        check_rows(base, members)
        exact_closure(base, {z['path'] for z in members} | {'MANIFEST.json'})
        bound.extend(repo_pin(base / z['path']) for z in members)
    old = {z['path']: regular(A / 'reviewed_candidate', z['path']).read_bytes() for z in normalize_rows(load(A / pins['frozen_v1']['path'])['files'])}
    new = {z['path']: regular(C, z['path']).read_bytes() for z in normalize_rows(load(C / 'MANIFEST.json')['files'])}
    require(sorted(n for n in old if old[n] != new[n]) == ['CURRENT_CONTEXT.md', 'README.md'], 'v2 existing content changed outside exact presentation metadata')
    require(sorted(set(new) - set(old)) == ['V1_MANIFEST.json', 'V2_ALIAS_RECEIPT.json', 'review/REVIEW.md'], 'v2 additions differ')
    append = regular(A / 'acceptance_preparation_family/alias_source_revision', 'ARCHIVAL_NOTICE_APPEND.txt').read_bytes()
    require(all(new[n] == old[n] + append for n in ['README.md', 'CURRENT_CONTEXT.md']), 'Exact archival notice append differs')
    require(new['review/REVIEW.md'] == old['original_archive/review/REVIEW.md'] and new['V1_MANIFEST.json'] == (A / pins['frozen_v1']['path']).read_bytes(), 'Exact historical alias/v1 closure differs')
    dependency = load(C / 'CURRENT_PROOF_DEPENDENCIES.json')
    require(dependency['dependency_anchor_repository_relative'] == str(A.relative_to(R)) and len(dependency['files']) == 1472, 'All exact1472 audit-anchored dependencies required')
    check_rows(A, normalize_rows(dependency['files']))
    bound.extend(repo_pin(A / z['path']) for z in normalize_rows(dependency['files']))
    for name in ['primary_scope_family', 'current_measure_family', 'trace_geometry_family']:
        path = A / pins[name]['path']
        obj = load(path)
        value = normalize_rows(obj['authored_files'] if name == 'current_measure_family' else obj['files'])
        require(len(value) == pins[name]['authored_count'], 'Closed family authored scope differs')
        check_rows(path.parent, value)
        extras = inputs['source_family_qualified_extra_members'][name]
        check_rows(path.parent, extras)
        exact_closure(path.parent, {z['path'] for z in value + extras} | {path.name})
        bound.extend(repo_pin(path.parent / z['path']) for z in value + extras)
    for name, extras in [('root_actual_support', []), ('whole_v1', inputs['whole_v1_foreign_members']), ('alias_preparation', []), ('whole_v2_alias_followup', []), ('whole_alias_source_only', [])]:
        path = A / pins[name]['path']
        value = normalize_rows(load(path)['files'])
        require(len(value) == pins[name]['authored_count'], 'Exact authored closure count differs: ' + name)
        check_rows(path.parent, value + extras)
        exact_closure(path.parent, {z['path'] for z in value + extras} | {path.name})
        bound.extend(repo_pin(path.parent / z['path']) for z in value + extras)
    capture = load(A / pins['alias_actual_capture']['path'])
    required_values(capture, {'source_sha256': 'c30a30983e3d26f36b2ca055177a0445b26870deb0085082eb6d7f44db554210', 'actual_execution': True, 'completed': True, 'exit_code': 0, 'status': 'PASS'}, 'Actual root v2 alias capture')
    require(type(capture['pid']) is int and capture['pid'] > 0, 'Actual alias child pid required')
    capture_base = (A / pins['alias_actual_capture']['path']).parent
    exact_closure(capture_base, {'CAPTURE.json', 'prelaunch_source.py', capture['stdout']['path'], capture['stderr']['path']})
    require(sha(regular(capture_base, 'prelaunch_source.py').read_bytes()) == capture['source_sha256'], 'Actual alias prelaunch source differs')
    for key in ['stdout', 'stderr']:
        row = normalize_rows([capture[key]])[0]
        check_rows(capture_base, [row])
        bound.append(repo_pin(capture_base / row['path']))
    bound.append(repo_pin(capture_base / 'prelaunch_source.py'))
    replay = load(A / pins['actual_root_replay']['path'])
    required_values(replay, {'status': 'PASS', 'setup_completed': True, 'head': HEAD, 'base': ORIGINAL_BASE, 'original_substantive_turns': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'exact_original_file_count': 16, 'changed_diff_path_count': 17, 'closed_family_count': 3}, 'Entire original actual closed replay')
    require(len(replay['actual_outer_program_runs']) == 12 and len(replay['actual_nested_program_runs']) == 108 and len(replay['actual_administrative_command_runs']) == 2 and replay['retention_errors'] == [], 'Actual original replay complete scope differs')
    source_and_ledger(C)
    require(new['RESULTS.md'] == old['original_archive/RESULTS.md'] and sha(new['RESULTS.md']) == RESULTS_SHA, 'Original results mathematics changed')
    by_path = {}
    for pin in bound:
        require(pin['path'] not in by_path or strict_equal(by_path[pin['path']], pin), 'Conflicting full evidence binding')
        by_path[pin['path']] = pin
    return [by_path[k] for k in sorted(by_path)]


def final_scope(scope):
    required_values(scope, {'schema': 'pr38-root-reviewed-final-evidence-plan/v1', 'plan_status': 'ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION', 'pr': PR, 'problem_id': int(ID), 'original_head': HEAD, 'original_base': ORIGINAL_BASE,
        'reviewed_candidate_manifest_sha256': CURRENT_SHA, 'current_proof_dependencies_sha256': DEPENDENCIES_SHA,
        'root_full_current_read_completed': True, 'independent_v2_source_first_pass': True, 'mandatory_corrections': [],
        'science_reexecution_of_v2': False, 'original_actual_closed_family_replay_bound': True,
        'queue_status': 'unsolved', 'full_problem_solved': False, 'positive_novelty_claim': False,
        'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0,
        'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None,
        'separate_prior_report_present': False, 'importer_empty_fallback_is_not_retrieved_report': True,
        'paper_or_new_doi_or_tracker': False, 'standard_inputs_independently_recertified': False,
        'standard_input_qualification_is_mathematical_defect': False}, 'Explicit final evidence scope')
    require(strict_equal(scope['scientific_scope'], load(HERE / 'SCIENTIFIC_SCOPE.json')), 'Complete inherited scientific/source qualification differs')
    basis = immutable_basis()
    require(strict_equal(scope['immutable_basis_bindings'], basis), 'Complete actual immutable basis must be explicitly reviewed and pinned')
    inputs = load(HERE / 'INPUT_BINDINGS.json')['pins']
    whole_pin = repo_pin(A / inputs['whole_v2_alias_followup']['path'])
    require(scope['whole_manifest'] == whole_pin['path'] and scope['whole_manifest_sha256'] == whole_pin['sha256'], 'Actual closed v2 independent whole manifest required')
    assessment = load(A / 'whole_current_alias_followup_family/ASSESSMENT.json')
    required_values(assessment, {'verdict': 'VALID_UNSOLVED_PARTIAL_NO_REMAINING_MANDATORY_CORRECTIONS', 'actual_v2_manifest_sha256': CURRENT_SHA,
        'mandatory_corrections': [], 'original_v1_alias_correction_resolved': True, 'full_problem_solved': False, 'new_substantive_attempts': 0, 'audit_turns': 0}, 'Actual full independent v2 assessment')
    inspection = load(A / inputs['root_actual_v2_inspection']['path'])
    required_values(inspection, {'status': 'PASS', 'actual_v2_manifest_sha256': CURRENT_SHA, 'actual_v2_members': 1502,
        'root_full_current_read_completed': True, 'full_problem_solved': False, 'partial_valid': True,
        'original_attempts': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'mandatory_corrections_remaining': []}, 'Complete actual root v2 inspection')
    require(type(scope['final_review_records']) is list and [z['role'] for z in scope['final_review_records']] == ['independent_actual_v2_alias_followup', 'root_complete_actual_v2_inspection'], 'Both actual final source-first/whole v2 records required')
    require(strict_equal([z['binding'] for z in scope['final_review_records']], [repo_pin(A / 'whole_current_alias_followup_family/ASSESSMENT.json'), repo_pin(A / inputs['root_actual_v2_inspection']['path'])]), 'Both exact actual final review bindings required')
    final_bindings = []
    for item in scope['final_review_records']:
        pin = item['binding']
        actual = parse(bound_repository(pin))
        require(strict_equal(actual, item['entire_parsed_json']), 'Entire final review record differs: ' + item['role'])
        require(item['root_reviewed_pass'] is True and item['remaining_mandatory_corrections'] == [], 'Root must review complete actual record and clear all mandatory corrections')
        final_bindings.append(pin)
    require(type(scope['final_closures']) is list and scope['final_closures'], 'Explicit actual followup/inspection source/capture closures required')
    closure_names = []
    covered = {pin['path'] for pin in basis}
    for closure in scope['final_closures']:
        manifest_pin = closure['manifest']
        path = regular(R, manifest_pin['path'])
        require(path.resolve().is_relative_to(A.resolve()), 'Final closure root escaped selected audit')
        obj = parse(bound_repository(manifest_pin))
        require(strict_equal(obj, closure['entire_manifest']), 'Entire actual followup manifest differs')
        members = rows(closure['members'])
        advertised = normalize_rows(obj['files'])
        require(strict_equal(members, advertised), 'Complete advertised actual followup member rows differ')
        check_rows(path.parent, members)
        exact_closure(path.parent, {z['path'] for z in members} | {path.name})
        final_bindings.extend([manifest_pin] + [repo_pin(path.parent / z['path']) for z in members])
        covered.update(z['path'] for z in final_bindings)
        closure_names.append(manifest_pin['path'])
    require(len(closure_names) == len(set(closure_names)), 'Duplicate actual final closure')
    require(scope['whole_manifest'] in closure_names, 'Explicit final alias followup whole manifest must be in exact closures')
    require(all(item['binding']['path'] in covered for item in scope['final_review_records']), 'Actual final review records must be retained in complete closure')
    # No filename/suffix allowlist: exact declared ROOTstdout.bin and other raw
    # capture streams are ordinary first-party rows of the complete closure.
    by_path = {z['path']: z for z in basis}
    for pin in final_bindings:
        require(pin['path'] not in by_path or strict_equal(pin, by_path[pin['path']]), 'Conflicting final binding')
        by_path[pin['path']] = pin
    return [by_path[name] for name in sorted(by_path)]


def add_gate_args(parser):
    parser.add_argument('--execute', action='store_true', help='Future actual root-only explicit execution')
    parser.add_argument('--preparation-manifest-sha256', required=True)
    for name in ['whole-manifest', 'root-final-receipt', 'whole-scope-contract', 'root-final-manifest', 'reconciliation-capture']:
        parser.add_argument('--' + name, required=True, help='Explicit repository-relative actual finalized artifact')
        parser.add_argument('--' + name + '-sha256', required=True)


def gates(args):
    require(args.execute, 'Prepared only: actual root --execute required')
    require(git('branch', '--show-current') == 'main', 'Stay on main')
    manifest(HERE, HERE / 'PREPARATION_MANIFEST.json', args.preparation_manifest_sha256)
    paths = {}
    for name in ['whole_manifest', 'root_final_receipt', 'whole_scope_contract', 'root_final_manifest', 'reconciliation_capture']:
        path = regular(R, getattr(args, name))
        require(path.resolve().is_relative_to(A.resolve()) and not path.resolve().is_relative_to(C.resolve()), 'Actual finalized gate must belong to selected audit outside frozen v2')
        require(sha(path.read_bytes()) == digest(getattr(args, name + '_sha256')), 'Explicit actual final gate changed: ' + name)
        paths[name] = path
    scope = load(paths['whole_scope_contract'])
    require(scope['whole_manifest'] == args.whole_manifest and scope['whole_manifest_sha256'] == args.whole_manifest_sha256 and scope['preparation_manifest_sha256'] == args.preparation_manifest_sha256, 'Exact final whole/preparation pins differ')
    bindings = final_scope(scope)
    root = load(paths['root_final_receipt'])
    required_values(root, {'schema': 'pr38-actual-final-evidence-reconciliation/v1', 'status': 'PASS', 'pr': PR, 'problem_id': int(ID),
        'actual_root_reconciliation': True, 'science_reexecution_of_v2': False, 'original_actual_closed_family_replay_bound': True,
        'whole_scope_contract_sha256': args.whole_scope_contract_sha256,
        'whole_manifest_sha256': args.whole_manifest_sha256, 'preparation_manifest_sha256': args.preparation_manifest_sha256,
        'bindings_before': bindings, 'bindings_after': bindings, 'entire_scope': scope}, 'Actual root final reconciliation receipt')
    final_manifest_path = paths['root_final_manifest']
    require(final_manifest_path.parent == paths['root_final_receipt'].parent == paths['whole_scope_contract'].parent and final_manifest_path.name == 'FINAL_MANIFEST.json', 'Actual final root receipt/scope closure must be literal and complete')
    final_members = manifest(final_manifest_path.parent, final_manifest_path, args.root_final_manifest_sha256, 2)
    require(strict_equal(final_members, sorted([{'path': paths['root_final_receipt'].name, 'bytes': len(paths['root_final_receipt'].read_bytes()), 'sha256': args.root_final_receipt_sha256}, {'path': paths['whole_scope_contract'].name, 'bytes': len(paths['whole_scope_contract'].read_bytes()), 'sha256': args.whole_scope_contract_sha256}], key=lambda row: row['path'])), 'Actual final two-member receipt/scope closure differs')
    capture = load(paths['reconciliation_capture'])
    required_values(capture, {'actual_execution': True, 'completed': True, 'exit_code': 0, 'status': 'PASS', 'source_sha256': sha((HERE / 'seal_final_evidence.py').read_bytes())}, 'Actual root final reconciliation child capture')
    require(type(capture['pid']) is int and capture['pid'] > 0 and type(capture['argv']) is list and str(HERE / 'seal_final_evidence.py') in capture['argv'], 'Actual final child source/argv/pid required')
    require(type(capture['started_utc']) is str and capture['started_utc'] and type(capture['finished_utc']) is str and capture['finished_utc'], 'Actual final start/end clocks required')
    require(capture['cwd'] == str(A), 'Actual final reconciliation audit cwd required')
    argv = capture['argv']
    for flag, expected in [('--preparation-manifest-sha256', args.preparation_manifest_sha256), ('--plan', root['root_reviewed_plan']['path']), ('--plan-sha256', root['root_reviewed_plan']['sha256'])]:
        require(argv.count(flag) == 1 and argv.index(flag) + 1 < len(argv) and argv[argv.index(flag) + 1] == expected, 'Actual final argv pin differs: ' + flag)
    require(argv.count('--execute') == 1, 'Actual final explicit execution flag required')
    bound_repository(root['root_reviewed_plan'])
    require(strict_equal(root['reconciliation_source'], repo_pin(HERE / 'seal_final_evidence.py')), 'Exact final reconciliation source binding differs')
    cap_base = paths['reconciliation_capture'].parent
    require(sha(regular(cap_base, 'prelaunch_source.py').read_bytes()) == capture['source_sha256'], 'Actual final prelaunch source differs')
    for key in ['stdout', 'stderr']:
        row = normalize_rows([capture[key]])[0]
        check_rows(cap_base, [row])
    parsed_stdout = parse(regular(cap_base, capture['stdout']['path']).read_bytes())
    required_values(parsed_stdout, {'status': 'PASS', 'root_final_receipt_sha256': args.root_final_receipt_sha256, 'whole_scope_contract_sha256': args.whole_scope_contract_sha256, 'final_manifest_sha256': args.root_final_manifest_sha256}, 'Full actual final child stdout')
    exact_closure(cap_base, {paths['reconciliation_capture'].name, 'prelaunch_source.py', capture['stdout']['path'], capture['stderr']['path']})
    frozen = manifest(C, C / 'MANIFEST.json', CURRENT_SHA, 1502)
    snapshot = load(A / 'snapshot_manifest.json')
    require(sha((A / 'snapshot_manifest.json').read_bytes()) == SNAPSHOT_SHA and snapshot['head'] == HEAD and snapshot['base'] == ORIGINAL_BASE and len(snapshot['files']) == 16 and len(snapshot['changed_paths']) == 17, 'Exact original16/17diff snapshot differs')
    actual_diff = git_bytes('diff', ORIGINAL_BASE, HEAD)
    require(git_bytes('diff', '--name-only', ORIGINAL_BASE, HEAD).decode().splitlines() == snapshot['changed_paths'] and len(actual_diff) == snapshot['diff_bytes'] and sha(actual_diff) == snapshot['diff_sha256'] and actual_diff == (A / 'pr_input/diff.patch').read_bytes(), 'Entire original17-path real Git diff differs')
    for row in snapshot['files']:
        raw = regular(C / 'original_archive', row['path']).read_bytes()
        require(len(raw) == row['size'] and sha(raw) == row['sha256'] and raw == git_bytes('show', HEAD + ':unsolved_math_prioritization/attempts/' + ID + '/' + row['path']), 'Exact original Git/archive artifact differs')
    historical = load(C / 'CURRENT_NATIVE_HISTORICAL_STATE.json')
    for revision in [ORIGINAL_BASE, HEAD]:
        data = git_bytes('show', revision + ':unsolved_math_prioritization/state.json')
        record = historical['states'][revision]
        require(len(data) == record['bytes'] and sha(data) == record['sha256'] and ID not in parse(data) and record['target_entry_present'] is False, 'Original native target state cannot be invented')
        history = optional_git_file(revision, 'unsolved_math_prioritization/history.jsonl')
        require(not any(str(z.get('id', z.get('problem_id', ''))) == ID for z in map(parse, history.splitlines())), 'Original native target history unexpectedly present')
    return frozen, {'reviewed_candidate_manifest_sha256': CURRENT_SHA, 'current_proof_dependencies_sha256': DEPENDENCIES_SHA,
        'preparation_manifest_sha256': args.preparation_manifest_sha256,
        **{key: getattr(args, key) for key in ['whole_manifest', 'whole_manifest_sha256', 'root_final_receipt', 'root_final_receipt_sha256', 'whole_scope_contract', 'whole_scope_contract_sha256', 'root_final_manifest', 'root_final_manifest_sha256', 'reconciliation_capture', 'reconciliation_capture_sha256']},
        'scientific_scope': scope['scientific_scope'], 'science_reexecution_of_v2': False, 'original_actual_closed_family_replay_bound': True}


def acceptance_invariants(acceptance, pins, pre):
    required = {'schema': 'pr38-accepted-current-partial/v1', 'pr': PR, 'id': int(ID), 'problem_id': int(ID), 'problem_number': CODE,
        'outcome': 'unsolved_accepted_partial_merged', 'queue_status': 'unsolved', 'full_problem_solved': False, 'positive_novelty_claim': False,
        'original_head': HEAD, 'original_base': ORIGINAL_BASE, 'merge_parents': [pre['main_before'], HEAD], 'remote_state': 'MERGED', 'remote_isDraft': False,
        'canonical_scientific_artifact_sha256': RESULTS_SHA, 'original_results_sha256': RESULTS_SHA,
        'source_record_sha256': SOURCE_SHA, 'original_ledger_sha256': LEDGER_SHA,
        'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'substantive_attempts_used': 2, 'substantive_attempt_limit': 5, 'verification_attempts_added': 0,
        'paper_or_new_doi_or_tracker': False, 'human_peer_review_asserted': False, 'workflow_completion_estimate_percent': 100, 'full_resolution_completion_estimate_percent': 0,
        'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'historical_metadata_archival_only': True,
        'separate_prior_report_present': False, 'importer_empty_fallback_is_not_retrieved_report': True, 'accepted_source_for_mirror': 'source_record.json',
        'current_mirror': 'One present acceptance, no reconstructed original native transition or extra proof turn.'}
    required_values(acceptance, {**required, **pins}, 'Accepted PR38 invariant')
    for key in ['merge_commit', 'merge_tree']:
        require(type(acceptance.get(key)) is str and re.fullmatch(r'[0-9a-f]{40}', acceptance[key]), 'Actual accepted merge binding absent')
    require(type(acceptance.get('merged_at')) is str and acceptance['merged_at'], 'Actual merge date absent')
    source_and_ledger(K)
    for name in ['readiness.json', 'status.json', 'attempt.json']:
        value = load(K / name)
        required_values(value, {'id': ID, 'problem_number': CODE, 'pr': PR, 'status': 'unsolved_accepted_partial_merged', 'queue_status': 'unsolved',
            'current_gate': 'PASS_current_source_first_v2_alias_and_bound_original_actual_replay', 'merge_commit': acceptance['merge_commit'], 'merge_tree': acceptance['merge_tree'],
            'remote_merged_at': acceptance['merged_at'], 'current_workflow_completion_estimate_percent': 100, 'full_resolution_completion_estimate_percent': 0,
            'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'full_problem_solved': False, 'positive_novelty_claim': False,
            'full_resolution_claimed': False, 'novelty_claimed': False, 'paper_or_new_doi_or_tracker': False,
            'source_record_sha256': SOURCE_SHA, 'original_turns_sha256': LEDGER_SHA, 'current_results_sha256': RESULTS_SHA,
            'native_historical_events_inferred': False, 'later_acceptance_is_present_only': True,
            'separate_prior_report_present': False, 'importer_empty_fallback_is_not_retrieved_report': True,
            'original_substantive_attempts': 2, 'substantive_attempt_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
            'original_authored_attempt_metadata': load(C / 'original_archive/attempt.json'), **pins}, 'Accepted administration ' + name)
        required_values(value['budget'], {'original_substantive_attempts': 2, 'used_substantive_attempts': 2, 'maximum_substantive_attempts': 5,
            'cumulative_attempts': '2/5', 'new_substantive_attempts': 0, 'verification_attempts': 0,
            'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'historical_only': True}, 'Exact archival budget ' + name)


def selected_row(data):
    lines = data.decode().splitlines(keepends=True)
    headers = [line for line in lines if line.startswith('| Rank | ID / code |')]
    require(len(headers) == 1 and [x.strip() for x in headers[0].split('|')[1:-1]] == HEADER, 'Exact12-column queue required')
    found = [line for line in lines if len(line.split('|')) == 14 and line.split('|')[2].strip() == ID + ' / ' + CODE]
    require(len(found) == 1, 'Selected numeric/code row ambiguous/absent')
    return found[0]


def inventory_items(value):
    require(isinstance(value.get('items'), list), 'Inventory item array required')
    result = {z['number']: z for z in value['items']}
    require(len(result) == len(value['items']) and all(type(k) is int for k in result), 'Duplicate/noninteger inventory identity')
    return result


def unselected_inventory(before, after):
    old, new = inventory_items(before), inventory_items(after)
    require(set(old) == set(new), 'Complete inventory ID set changed')
    require([z['number'] for z in before['items']] == [z['number'] for z in after['items']], 'Inventory item order changed')
    require(all(new[number] == old[number] for number in old if number != PR), 'Unselected inventory item changed')
    administrative = {'updated_at_utc', 'last_checkpoint_utc', 'completed_count', 'program_completion_estimate_percent', 'completion_estimate_percent', 'current_pr', 'items'}
    require({k: v for k, v in before.items() if k not in administrative} == {k: v for k, v in after.items() if k not in administrative}, 'Unrelated top-level inventory metadata changed')
    selected_changes = {'stage', 'outcome', 'queue_status', 'audited_head', 'merge_commit', 'merged_at', 'workflow_completion_estimate_percent', 'original_attempts', 'new_substantive_attempts', 'cumulative_attempts', 'paper_or_new_doi_or_tracker'}
    require({k: v for k, v in old[PR].items() if k not in selected_changes} == {k: v for k, v in new[PR].items() if k not in selected_changes}, 'Unrelated selected inventory attributes changed')


def capture_foreign_tracked_exclusions():
    require(not git('diff', '--cached', '--name-only'), 'Preflight index must be entirely clean')
    dirty = set(git_bytes('diff', '--name-only', '-z').decode().split('\0')) - {''}
    require(dirty <= FOREIGN_TRACKED_EXCLUSIONS, 'Only exact two foreign tracked logs may be dirty')
    records = []
    for name in sorted(FOREIGN_TRACKED_EXCLUSIONS):
        require(git_bytes('ls-files', '--error-unmatch', '--', name).decode().strip() == name, 'Foreign exception must already be tracked')
        raw = regular(R, name).read_bytes()
        entries = [entry for entry in git_bytes('ls-tree', '-z', 'HEAD', '--', name).decode().split('\0') if entry]
        require(len(entries) == 1, 'Foreign HEAD tree entry must be unique')
        fields, literal = entries[0].split('\t', 1)
        mode, kind, blob = fields.split()
        require(literal == name and kind == 'blob' and mode in {'100644', '100755'}, 'Foreign HEAD entry must be exact regular blob')
        records.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw), 'head_sha256': sha(git_bytes('show', 'HEAD:' + name)), 'head_mode': mode, 'head_blob': blob,
                        'index_mode': mode, 'index_blob': blob, 'dirty_at_preflight': name in dirty, 'integration_and_checkpoint_excluded': True})
    foreign_tracked_unchanged({'foreign_tracked_exclusions': records})
    return records


def foreign_tracked_unchanged(pre):
    records = pre['foreign_tracked_exclusions']
    require(len(records) == len(FOREIGN_TRACKED_EXCLUSIONS) and {z['path'] for z in records} == FOREIGN_TRACKED_EXCLUSIONS, 'No broad/untracked exception scope')
    for row in records:
        raw = regular(R, row['path']).read_bytes()
        require(row['integration_and_checkpoint_excluded'] is True and len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Foreign writer changed bytes; inspect, never checkpoint or overwrite')
        require(sha(git_bytes('show', 'HEAD:' + row['path'])) == row['head_sha256'], 'Foreign HEAD bytes accidentally committed')
        head_entries = [entry for entry in git_bytes('ls-tree', '-z', 'HEAD', '--', row['path']).decode().split('\0') if entry]
        require(len(head_entries) == 1 and head_entries[0] == row['head_mode'] + ' blob ' + row['head_blob'] + '\t' + row['path'], 'Foreign exact HEAD mode/blob changed')
        stages = [z for z in git_bytes('ls-files', '--stage', '-z', '--', row['path']).decode().split('\0') if z]
        require(len(stages) == 1, 'Foreign index conflicted/ambiguous')
        fields, name = stages[0].split('\t', 1)
        mode, blob, stage = fields.split()
        require(name == row['path'] and stage == '0' and mode == row['index_mode'] == row['head_mode'] and blob == row['index_blob'] == row['head_blob'] and sha(git_bytes('show', ':' + name)) == row['head_sha256'], 'Foreign dirty bytes staged/exact index mode/blob changed')


def binding(path):
    return {'path': str(Path(path).relative_to(R)), 'sha256': sha(Path(path).read_bytes())}


def canonical_names(frozen, accepted=False):
    original = {z['path'] for z in load(A / 'snapshot_manifest.json')['files']}
    names = {z['path'] for z in frozen} | original
    names |= {'reviewed_pending_administration/' + name for name in ADMIN} | {'reviewed_pending_administration/MANIFEST.json', 'ACCEPTED_QUEUE_PATCH.json'}
    if accepted:
        names |= {'acceptance.json', 'ACCEPTANCE.md', 'MANIFEST.json'}
    return names


def canonical_unchanged(frozen, accepted=False):
    exact_closure(K, canonical_names(frozen, accepted))
    for row in frozen:
        prefix = 'reviewed_pending_administration/' if row['path'] in ADMIN else ''
        require(regular(K, prefix + row['path']).read_bytes() == (C / row['path']).read_bytes(), 'Reviewed science/source/diagnostic/archive byte changed: ' + row['path'])
    require((K / 'reviewed_pending_administration/MANIFEST.json').read_bytes() == (C / 'MANIFEST.json').read_bytes(), 'Frozen pending manifest changed')
    for row in load(A / 'snapshot_manifest.json')['files']:
        require((K / 'original_archive' / row['path']).read_bytes() == (C / 'original_archive' / row['path']).read_bytes(), 'Original13 archive changed')
        if row['path'] not in {z['path'] for z in frozen}:
            require((K / row['path']).read_bytes() == (C / 'original_archive' / row['path']).read_bytes(), 'Original-only top-level provenance changed')
    source_and_ledger(K)


def tree_binding(merge, pre, overlay, queue):
    """Bind actual two-parent real merge tree, not only the worktree."""
    parents = git('show', '-s', '--format=%P', merge).split()
    require(parents == [pre['main_before'], HEAD], 'Require original-head no-ff merge exact parents/order')
    git_bytes('merge-base', '--is-ancestor', merge, 'HEAD')
    actual_tree = git('show', '-s', '--format=%T', merge)
    require(re.fullmatch(r'[0-9a-f]{40}', actual_tree), 'Invalid real merge tree')
    prefix = 'unsolved_math_prioritization/attempts/' + ID + '/'
    value = rows(overlay['canonical_overlay_files'])
    entries = [z for z in git_bytes('ls-tree', '-r', '-z', merge, '--', prefix).decode().split('\0') if z]
    indexed = {}
    for entry in entries:
        fields, name = entry.split('\t', 1)
        mode, kind, blob = fields.split()
        require(mode in {'100644', '100755'} and kind == 'blob', 'Real canonical tree has nonregular entry')
        indexed[name] = mode
    require(set(indexed) == {prefix + z['path'] for z in value}, 'Real merge complete canonical file closure differs')
    for row in value:
        raw = git_bytes('show', merge + ':' + prefix + row['path'])
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Real merge canonical bytes differ')
    require(git_bytes('show', merge + ':unsolved_math_prioritization/QUEUE.md') == queue, 'Real merge entire queue differs')
    for key, suffix in [('state', '.json'), ('history', '.jsonl')]:
        require(sha(git_bytes('show', merge + ':unsolved_math_prioritization/' + key + suffix)) == pre[key + '_before_sha256'], 'Merge changed shared state/history before present mirror')
    require(sha(git_bytes('show', merge + ':draft_pr_publication_program_20260930/inventory.json')) == pre['inventory_before_sha256'], 'Merge changed inventory before finalization')
    foreign_tracked_unchanged(pre)
    for row in pre['foreign_tracked_exclusions']:
        require(sha(git_bytes('show', merge + ':' + row['path'])) == row['head_sha256'], 'Real merge committed foreign dirty bytes')
        entries = [entry for entry in git_bytes('ls-tree', '-z', merge, '--', row['path']).decode().split('\0') if entry]
        require(entries == [row['head_mode'] + ' blob ' + row['head_blob'] + '\t' + row['path']], 'Real merge changed exact foreign mode/blob')
    # A full-tree diff whitelist prevents unrelated tracked or untracked files
    # being swept into this merge by broad staging, even outside canonical scope.
    changed = set(git_bytes('diff-tree', '-r', '--no-commit-id', '--name-only', '-z', pre['main_before'], merge).decode().split('\0')) - {''}
    require(changed <= {prefix + z['path'] for z in value} | {'unsolved_math_prioritization/QUEUE.md'}, 'Unrelated path entered real merge tree')
    return actual_tree


def load_mirror():
    path = BASE / 'revision2/accepted_state_sync_v2.py'
    require(sha(path.read_bytes()) == MIRROR_SHA and sha((BASE / 'root_apply/guarded_import_v2.py').read_bytes()) == WRITER_SHA, 'Reviewed mirror/writer sources changed')
    spec = importlib.util.spec_from_file_location('pr38_bound_mirror', path)
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    native = mirror.ledger_budget
    def ledger(data, kind, used, limit):
        if kind == 'json_zero_source_triage':
            obj = json.loads(data)
            mirror.require(str(obj.get('problem_id')) == '30002145' and used == obj.get('used') == 0 and limit == obj.get('limit') == 5 and obj.get('substantive_proof_attempts') == [] and isinstance(obj.get('reason'), str) and obj['reason'], 'Invalid preserved zero-triage ledger')
        elif kind == 'json_substantive_responses':
            obj = json.loads(data)
            mirror.require(obj.get('problem_id') == 2744 and obj.get('problem_number') == 'KP-1.85' and type(obj.get('substantive_turns_used')) is int and used == obj['substantive_turns_used'] == 1 and limit == obj.get('turn_limit') == 5 and obj.get('outcome') == 'unsolved' and isinstance(obj.get('responses'), list) and [z.get('turn') for z in obj['responses']] == [1] and obj['responses'][0].get('outcome') == 'unsolved' and obj['responses'][0].get('artifact') == 'OBSTRUCTION.md', 'Invalid preserved PR35 ledger')
        elif kind == 'pr37_exact_json_substantive_responses':
            obj = parse(data)
            old_path = B / 'audits/pr37_3009/reviewed_candidate/turns.json'
            mirror.require(sha(data) == '7bf94bf41466a40deceab668ecbb12a54b16fe16ad400bc221ff6f18e7558498' and strict_equal(obj, load(old_path)) and used == 1 and limit == 5, 'Preserve exact PR37 original complete ledger')
        elif kind == 'pr38_exact_original_two_turn_list':
            obj = parse(data)
            mirror.require(sha(data) == LEDGER_SHA and strict_equal(obj, load(C / 'turns.json')) and type(obj) is list and [z['turn'] for z in obj] == [1, 2] and type(used) is int and used == 2 and type(limit) is int and limit == 5, 'Exact PR38 original two-row list ledger required')
        else:
            native(data, kind, used, limit)
    mirror.ledger_budget = ledger
    return mirror


def run(main):
    try:
        main()
    except Exception:
        # Future runtime receipts belong to root's audit, preserving this static
        # preparation package's self-excluding closure byte-exact.
        failure = A / ('ROOT_INTEGRATION_FAILURE_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ') + '.json')
        dump(failure, {'utc': stamp(), 'status': 'FAIL', 'scope': 'Future actual root helper failure, retained for inspection; no automatic retry', 'traceback': traceback.format_exc()}, exclusive=True)
        raise
