"""Static PR39 root-only guards. No import-time mutation or execution.

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
C = A / 'reviewed_candidate'
K = R / 'unsolved_math_prioritization/attempts/9500008'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '9500008', 'AMR-094-0008', 39
HEAD = '652b8115080e5e97b2274cb602de3faf8c551f20'
ORIGINAL_BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
CURRENT_SHA = '67488fa9fe6ae87a52e9fa41512e962c4b180b601c9770d5cab6c144d6f544be'
DEPENDENCIES_SHA = '6717a13acf5b869b8b4b308660351027cf6efadedccf17a9a9102e9f29b77f81'
SNAPSHOT_SHA = 'debd6fd2621f401ec927c441da3b54a13ca60ee917698898299ad24faf67616e'
LEDGER_SHA = '015e5bce1a752e1d666d8afdd1637a884438c4e0497eec2c156c5a16e2f3b476'
SOURCE_SHA = 'af675ce90417c3815e68da206334d4a91abdd0ce5ca7a9ea3b96c4b9722b6301'
PARTIAL_SHA = '3ad42fdecc5a30ef00d6fec6c18d1f2b8299be999d609711459bb67823af9bc1'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
WRITER_SHA = 'b72afa148d034818cc90fd25b6b084fd94e42604d433a64e09a4ee01ae6e5271'
PREVIOUS = B / 'audits/pr38_2765/state_mirror_bindings.json'
PRIOR_SHA = '029de46674fc07aa5f9817bac8595192ede3fe7ad18a66b043e98586e6121b96'
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
    temporary = path.with_name(path.name + '.pr39-tmp')
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if exclusive:
        # Atomic absent-only publication. A collision retains the complete,
        # fsynced temporary for inspection; do not unlink it on link failure.
        os.link(temporary, path, follow_symlinks=False)
        temporary.unlink()
    else:
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
    require(value['number'] == PR and value['url'] == 'https://github.com/AlecKriebel/Math/pull/39', 'Wrong remote PR')
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


def exact_closure(base, expected, empty_directories=()):
    expected = set(expected)
    actual, directories = inventory(base)
    require(actual == expected, 'Complete recursive file membership differs: ' + str(sorted(actual ^ expected)))
    parents = {str(parent) for name in expected for parent in PurePosixPath(name).parents if str(parent) != '.'}
    for name in empty_directories:
        relative(name)
        path = Path(base) / name
        require(path.is_dir() and not path.is_symlink() and not any(path.iterdir()), 'Qualified exact directory must remain empty')
        parents.add(name)
    require(directories == parents, 'Extra/missing recursive directories: ' + str(sorted(directories ^ parents)))


def manifest(base, path, expected=None, count=None, scope=None):
    """Strict complete closure; only six exact current malformed inputs qualified."""
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
    return json.loads(raw, object_pairs_hook=unique, parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON: ' + value)))


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
    require(path.resolve().is_relative_to(A.resolve()), 'Final evidence must belong to exact PR39 audit')
    raw = path.read_bytes()
    require(type(pin['bytes']) is int and len(raw) == pin['bytes'] and sha(raw) == digest(pin['sha256']), 'Final evidence binding changed: ' + pin['path'])
    return raw


def repo_pin(path):
    raw = Path(path).read_bytes()
    return {'path': str(Path(path).relative_to(R)), 'bytes': len(raw), 'sha256': sha(raw)}


def source_and_ledger(base):
    source = regular(base, 'source_record.json').read_bytes()
    prior = regular(base, 'prior_report.json').read_bytes()
    require(sha(source) == SOURCE_SHA and sha(prior) == PRIOR_SHA, 'Exact complete source/nonempty prior bytes changed')
    obj, report = parse(source), parse(prior)
    require(strict_equal(obj, load(A / 'pinned_problem.json')) and strict_equal(report, load(A / 'pinned_prior_report.json')), 'Entire actual source/prior object differs; no fallback')
    require(type(report) is dict and bool(report), 'Actual prior report must be present and nonempty')
    provenance = load(A / 'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json')['provenance']
    require(strict_equal(provenance['complete_flat_problem'], obj) and strict_equal(provenance['complete_actual_prior_report'], report), 'Full root/raw/SQL source/prior differs')
    required_values(provenance, {'prior_raw_key_present': True, 'prior_fallback_used': False}, 'Genuine retrieved prior')
    raw = regular(base, 'turns.json').read_bytes()
    require(sha(raw) == LEDGER_SHA, 'Entire original two-attempt object ledger changed')
    ledger = parse(raw)
    required_values(ledger, {'id': int(ID), 'count': 2}, 'Original authored budget')
    require(type(ledger['attempts']) is list and [z['number'] for z in ledger['attempts']] == [1, 2] and strict_equal(ledger, load(C / 'original_archive/turns.json')), 'Entire original attempts[1,2] required')
    require(ledger['attempts'][1]['artifact'] == 'PARTIAL.md' and ledger['attempts'][1]['sha256'] == PARTIAL_SHA, 'Original scientific artifact binding differs')


def exact_declared_closure(base, names, exclusions, empty_directories):
    """Only one pinned original private-tree declaration, no new holes."""
    if not exclusions:
        require(not empty_directories or (base == A / 'uniform_error_scaling_family' and strict_equal(empty_directories, ['manifest_control_fixtures/missing/nested'])), 'Only exact source-bound missing-file negative empty directory qualified')
        exact_closure(base, names, empty_directories)
        return
    require(not empty_directories, 'No private-tree empty-directory holes')
    require(base == A / 'rotation_concatenation_family' and strict_equal(exclusions, ['tmp']), 'No arbitrary private/foreign exclusion')
    require((base / 'tmp').is_dir() and not (base / 'tmp').is_symlink(), 'Exact original private root required')
    files, dirs = set(), set()
    for path in base.rglob('*'):
        name = path.relative_to(base).as_posix()
        relative(name)
        require(not path.is_symlink() and (path.is_file() or path.is_dir()), 'Even excluded private trees cannot hide symlink/special entries')
        if PurePosixPath(name).parts[0] == 'tmp':
            continue
        (dirs if path.is_dir() else files).add(name)
    require(files == set(names), 'Complete declared original authored closure differs')
    expected_dirs = {p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    require(dirs == expected_dirs, 'Extra/missing original authored directory')


def parse_bound_members(base, members):
    exceptions = {z['path']: z for z in load(HERE / 'INPUT_BINDINGS.json')['qualified_JSON_negative_inputs']}
    for row in members:
        path = regular(base, row['path'])
        if path.suffix not in {'.json', '.jsonl'}:
            continue
        data = path.read_bytes()
        name = path.relative_to(R).as_posix()
        if name in exceptions:
            pin = exceptions[name]
            require(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'Exact named negative input changed')
            try:
                parse(data)
            except (json.JSONDecodeError, ValueError) as error:
                expected = pin['parse_failure']
                require(str(error) == expected or (expected == 'duplicate key status' and str(error) == 'Duplicate JSON key: status'), 'Named negative parse failure differs')
            else:
                raise ValueError('Named negative input now parses')
        elif path.suffix == '.json':
            parse(data)
        else:
            require(not data or data.endswith(b'\n'), 'Full newline-complete JSONL required')
            for line in data.splitlines():
                parse(line)


def revision_basis():
    basis = load(HERE / 'REVISION_BASIS.json')
    for value in [basis['original_preparation_manifest'], basis['fresh_static_audit_manifest']]:
        path = regular(R, value['path'])
        require(path.resolve().is_relative_to(A.resolve()), 'Exact PR39 origin/audit root required')
        require(len(path.read_bytes()) == value['bytes'], 'Origin/audit manifest byte count differs')
        manifest(path.parent, path, value['sha256'], value['authored_count'])
    verdict = load(A / 'acceptance_static_adversary_family/FAMILY_VERDICT.json')
    require(sha((A / 'acceptance_static_adversary_family/FAMILY_VERDICT.json').read_bytes()) == basis['fresh_static_verdict_sha256'] and
            verdict['verdict'] == 'REPAIR_REQUIRED_BEFORE_ACTUAL_EXECUTION' and len(verdict['mandatory_corrections']) == 3,
            'Full exact original static repair report required')


def immutable_basis():
    """Complete byte/typed-object checks through compact immutable references."""
    revision_basis()
    inputs = load(HERE / 'INPUT_BINDINGS.json')
    references = []
    for value in inputs['pins'].values():
        bound_repository(value)
        references.append(value)
    for closure in inputs['closures']:
        pin = closure['manifest']
        path = R / pin['path']
        obj = parse(bound_repository(pin))
        members = normalize_rows(obj[closure['member_field']])
        require(len(members) == closure['authored_count'], 'Exact entire advertised closure count differs')
        check_rows(path.parent, members + closure['qualified_extra_members'])
        exact_declared_closure(path.parent, {z['path'] for z in members + closure['qualified_extra_members']} | {path.name}, closure['excluded_root_private_trees'], closure['qualified_empty_directories'])
        parse_bound_members(path.parent, members)
        references.append(pin)
    frozen = manifest(C, C / 'MANIFEST.json', CURRENT_SHA, 2901)
    dependency = load(C / 'CURRENT_PROOF_DEPENDENCIES.json')
    require(sha((C / 'CURRENT_PROOF_DEPENDENCIES.json').read_bytes()) == DEPENDENCIES_SHA and dependency['dependency_anchor_repository_relative'] == str(A.relative_to(R)) and len(dependency['files']) == 2797, 'All2797 exact audit-relative dependencies required')
    check_rows(A, normalize_rows(dependency['files']))
    parse_bound_members(A, normalize_rows(dependency['files']))
    require(sha((C / 'PARTIAL.md').read_bytes()) == PARTIAL_SHA and (C / 'PARTIAL.md').read_bytes() == (C / 'original_archive/PARTIAL.md').read_bytes(), 'PARTIAL theorem changed')
    source_and_ledger(C)
    repair = load(C / 'CURRENT_REVIEW_CORRECTION_RECEIPT.json')
    original = (C / 'original_archive/review/REVIEW.md').read_bytes()
    current = (C / 'review/REVIEW.md').read_bytes()
    required_values(repair, {'only_body_sentence_replaced': True, 'archival_notice_and_appendix_added': True, 'original_review_preserved': True, 'PARTIAL_code_source_receipts_turns_unchanged': True}, 'Current precision-only review repair')
    require(sha(original) == repair['original_review_sha256'] and sha(current) == repair['current_review_sha256'] and original.count(repair['exact_old_sentence'].encode()) == 1 and repair['exact_old_sentence'].encode() not in current and repair['exact_current_sentence'].encode() in current, 'Exact stopped-pair sentence repair differs')
    for item in inputs['outer_typed_captures']:
        pin = item['capture']
        cap = parse(bound_repository(pin))
        required_values(cap, {'actual_execution': True, 'completed': True, 'pid': item['expected_pid'], 'exit_code': item['expected_exit_code'], 'status': 'FAIL' if item['expected_exit_code'] else 'PASS'}, 'Actual failed/successful typed outer capture')
        root = (R / pin['path']).parent
        check_rows(root, item['files'])
        exact_closure(root, {z['path'] for z in item['files']})
        require(sha((root / 'prelaunch_source.py').read_bytes()) == cap['source_sha256'], 'Actual typed wrapper prelaunch source differs')
        for channel in ['stdout', 'stderr']:
            check_rows(root, normalize_rows([cap[channel]]))
        references.append(pin)
    for folder, expected in [('root_typed_entry_actual_capture', 'FAIL'), ('root_typed_entry_actual_capture_v2', 'TYPED_ADMINISTRATIVE_ENTRY_COMPLETED_NEW_WHOLE_GATE_PENDING')]:
        base = A / folder
        receipt = load(base / 'TYPED_ENTRY_RECEIPT.json')
        required_values(receipt, {'status': expected, 'builder_invoked': True, 'new_substantive_attempts': 0, 'audit_turns': 0}, 'Entire typed administrative attempt')
        runs = receipt['actual_runs']
        require(strict_equal(runs, load(base / 'RUNS.json')) and len(runs) == 20 and runs[0]['label'] == 'typed_baseline' and runs[-1]['label'] == 'unchanged_builder', 'Full20-run typed ledger differs')
        require(runs[0]['exit_code'] == 0 and runs[-2]['exit_code'] == 0 and all(z['exit_code'] == 1 for z in runs[1:18]) and runs[-1]['exit_code'] == (1 if folder == 'root_typed_entry_actual_capture' else 0), 'Exact baseline/17negative/prebuild/builder return codes required')
        for run in runs:
            require(run['stdin_supplied'] is False, 'Typed runs have no supplied stdin')
            require(run['actual_execution'] is True and run['completed'] is True and type(run['exit_code']) is int, 'Actual complete typed run required')
            for key in ['source', 'stdout', 'stderr']:
                pin = normalize_rows([run[key]])[0]
                bound_repository({**pin, 'path': str((A / pin['path']).relative_to(R))})
        fixture = (base / 'controls/duplicate_JSON_key.input.json').read_bytes()
        require(len(fixture) == 1545 and sha(fixture) == '8229604f25ce4cf93ac9b7f4bf5e4a05905b14f5cdd2afb28618727665977f2b', 'Only exact duplicate-key negative input qualified')
        try:
            parse(fixture)
        except ValueError:
            pass
        else:
            raise ValueError('Exact duplicate-key negative fixture now parses')
    old = load(A / 'root_typed_entry_preparation_family/frozen_type_schema.json')
    revised = load(A / 'root_typed_entry_execution_revision/frozen_type_schema.json')
    expected = parse(encode(old))
    expected['status'] = 'ROOT_REVIEWED_ADJACENT_EXECUTION_REVISION_SOURCE_ONLY'
    expected['builder']['path'] = 'current_execution_revision/prepare_current_packet.py'
    expected['builder']['sha256'] = 'f62d5f3010bdf09a795df083254d60c0902253eb57a451c3a0f4a2bf6cdf0154'
    expected['execution_revision_manifest_sha256'] = '62f744aa17e5844ce5c7422a71120e8e777cd5ef9f8b2db5abbb301ac2c22f09'
    expected['prior_failed_typed_capture_preserved'] = True
    require(strict_equal(revised, expected), 'Only exact five-field typed schema diff permitted')
    for name in ['typed_guard.py', 'run_typed_entry.py', 'control_cases.json']:
        require((A / 'root_typed_entry_preparation_family' / name).read_bytes() == (A / 'root_typed_entry_execution_revision' / name).read_bytes(), 'Guard/wrapper/17controls changed')
    exception = load(A / 'current_execution_revision/RETAINED_CAPABILITY_EXCEPTIONS.json')
    required_values(exception, {'schema': 'pr39-exact-historical-run1-capability-exceptions/v1', 'root_support_manifest_sha256': '0ef3c26646ff99ebb67cb165baaa09463218ec7fa33aa2bcbdec254b70267eb0'}, 'Exact historical capability revision')
    ex = normalize_rows(exception['files'])
    require(len(ex) == 8 and all(z['path'].endswith('.run1') for z in ex), 'Exactly eight .run1 paths required, no suffix wildcard')
    support = load(A / 'root_closed_families_actual_reproduction_support/ROOT_SUPPORT_MANIFEST.json')
    advertised = {z['path']: z for z in normalize_rows(support['files'])}
    require(all(strict_equal(advertised[z['path']], z) for z in ex), 'Exact exception path/bytes/hash row differs from support')
    check_rows(A / 'root_closed_families_actual_reproduction_support', ex)
    for z in ex:
        if z['path'].endswith('.json.run1'):
            parse(regular(A / 'root_closed_families_actual_reproduction_support', z['path']).read_bytes())
    root = load(A / 'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json')
    required_values(root, {'status': 'PASS', 'setup_completed': True, 'head': HEAD, 'base': ORIGINAL_BASE, 'original_substantive_turns': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'exact_original_file_count': 16, 'changed_diff_path_count': 17, 'closed_family_count': 3, 'full_problem_solved': False}, 'Full actual scientific replay preserved')
    require(len(root['actual_outer_program_runs']) == 14 and len(root['actual_nested_program_runs']) == 88 and len(root['actual_administrative_command_runs']) == 2 and root['retention_errors'] == [], 'Actual14/88/2 complete replay differs')
    root_whole = load(A / 'ROOT_WHOLE_CURRENT_REVIEW.json')
    required_values(root_whole, {'status': 'PASS', 'independent_family_manifest_sha256': 'bc71916b6b1a5496716e86839df784e3ce2db8883319fae8379c52f24f939f86', 'authored_members': 45, 'separately_bound_foreign_members': 8, 'root_semantic_whole_report_mathematical_reconstruction_operative_control_source_and_qualifications_read': True, 'new_substantive_attempts': 0, 'audit_turns': 0, 'partial_valid': True, 'full_problem_solved_by_project': False}, 'Root actual entire independent whole reading')
    current_inspection = load(A / 'ROOT_CURRENT_PACKET_INSPECTION.json')
    required_values(current_inspection, {'status': 'PASS', 'current_manifest_sha256': CURRENT_SHA, 'current_members': 2901, 'dependency_manifest_sha256': DEPENDENCIES_SHA, 'dependencies': 2797, 'root_full_current_scientific_read_completed': True, 'full_problem_solved': False, 'partial_valid': True, 'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0}, 'Root complete current source inspection')
    verdict = load(A / 'whole_current_source_first_family/FAMILY_VERDICT.json')
    required_values(verdict, {'verdict': 'PASS_SCOPED_PARTIAL_CURRENT_PACKET', 'full_target_status': 'UNSOLVED', 'full_problem_solved': False, 'novelty_claimed': False, 'historical_verdict_transferred': False, 'mandatory_corrections': [], 'original_substantive_attempts': 2, 'substantive_attempt_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'root_science_not_rerun': True}, 'Complete independent whole-current scope')
    require(strict_equal(root_whole['whole_independent_verdict'], verdict), 'Root read complete exact independent verdict object')
    for key in ['pins', 'own_evidence']:
        for pin in normalize_rows(verdict[key]):
            bound_repository({**pin, 'path': str((A / pin['path']).relative_to(R))})
    whole = next(z for z in inputs['closures'] if z['role'] == 'whole_review')
    foreign = load(A / 'whole_current_source_first_family/FOREIGN_CACHE_MANIFEST.json')
    require(strict_equal(sorted([{k: z[k] for k in ['path', 'bytes', 'sha256']} for z in normalize_rows(foreign['files'])], key=lambda z: z['path']), sorted(whole['qualified_extra_members'], key=lambda z: z['path'])), 'Exactly eight separate whole foreign members required')
    by_path = {}
    for pin in references:
        require(pin['path'] not in by_path or strict_equal(pin, by_path[pin['path']]), 'Conflicting immutable complete reference')
        by_path[pin['path']] = pin
    return [by_path[n] for n in sorted(by_path)]


def final_scope(scope):
    required_values(scope, {'schema': 'pr39-root-reviewed-final-evidence-plan/v1', 'plan_status': 'ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION', 'pr': PR, 'problem_id': int(ID), 'original_head': HEAD, 'original_base': ORIGINAL_BASE,
        'reviewed_candidate_manifest_sha256': CURRENT_SHA, 'current_proof_dependencies_sha256': DEPENDENCIES_SHA,
        'root_full_current_read_completed': True, 'root_full_whole_scope_read_completed': True, 'independent_whole_current_pass': True,
        'mandatory_corrections': [], 'science_reexecution_of_current': False, 'original_actual_closed_family_replay_bound': True,
        'queue_status': 'unsolved', 'full_problem_solved': False, 'positive_novelty_claim': False, 'original_substantive_attempts': 2,
        'new_substantive_attempts': 0, 'audit_turns': 0, 'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None,
        'separate_prior_report_present': True, 'prior_fallback_used': False, 'paper_or_new_doi_or_tracker': False}, 'Explicit genuine root current/whole source scope')
    require(strict_equal(scope['scientific_scope'], load(HERE / 'SCIENTIFIC_SCOPE.json')), 'Entire exact scientific scope differs')
    references = immutable_basis()
    require(strict_equal(scope['immutable_evidence_references'], references), 'Every complete actual manifest/record reference must remain exact')
    whole = next(z for z in load(HERE / 'INPUT_BINDINGS.json')['closures'] if z['role'] == 'whole_review')['manifest']
    require(scope['whole_manifest'] == whole['path'] and scope['whole_manifest_sha256'] == whole['sha256'], 'Actual completed whole manifest required')
    draft = load(HERE / 'DRAFT_FINAL_PLAN.json')
    expected = parse(encode(draft))
    expected.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION', root_full_current_read_completed=True, root_full_whole_scope_read_completed=True,
                    independent_whole_current_pass=True, preparation_manifest_sha256=sha((HERE / 'PREPARATION_MANIFEST.json').read_bytes()))
    require(strict_equal(scope, expected), 'Root plan may change only three review flags/status and exact preparation pin; complete objects otherwise identical')
    return references


def add_gate_args(parser):
    parser.add_argument('--execute', action='store_true', help='Future actual root-only explicit execution')
    parser.add_argument('--preparation-manifest-sha256', required=True)
    parser.add_argument('--previous-mirror-sha256', required=True, help='Fresh actual completed PR38 mirror proposal SHA; no fabricated predecessor')
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
        require(path.resolve().is_relative_to(A.resolve()) and not path.resolve().is_relative_to(C.resolve()), 'Actual finalized gate must belong to selected audit outside frozen current')
        require(sha(path.read_bytes()) == digest(getattr(args, name + '_sha256')), 'Explicit actual final gate changed: ' + name)
        paths[name] = path
    scope = load(paths['whole_scope_contract'])
    require(scope['whole_manifest'] == args.whole_manifest and scope['whole_manifest_sha256'] == args.whole_manifest_sha256 and scope['preparation_manifest_sha256'] == args.preparation_manifest_sha256, 'Exact final whole/preparation pins differ')
    bindings = final_scope(scope)
    root = load(paths['root_final_receipt'])
    required_values(root, {'schema': 'pr39-actual-final-evidence-reconciliation/v1', 'status': 'PASS', 'pr': PR, 'problem_id': int(ID),
        'actual_root_reconciliation': True, 'science_reexecution_of_current': False, 'original_actual_closed_family_replay_bound': True,
        'whole_scope_contract_sha256': args.whole_scope_contract_sha256,
        'whole_manifest_sha256': args.whole_manifest_sha256, 'preparation_manifest_sha256': args.preparation_manifest_sha256,
        'bindings_before': bindings, 'bindings_after': bindings, 'entire_scope': scope}, 'Actual root final reconciliation receipt')
    final_manifest_path = paths['root_final_manifest']
    require(final_manifest_path.parent == paths['root_final_receipt'].parent == paths['whole_scope_contract'].parent and final_manifest_path.name == 'FINAL_MANIFEST.json', 'Actual final root receipt/scope closure must be literal and complete')
    final_members = manifest(final_manifest_path.parent, final_manifest_path, args.root_final_manifest_sha256, 2)
    require(strict_equal(final_members, sorted([{'path': paths['root_final_receipt'].name, 'bytes': len(paths['root_final_receipt'].read_bytes()), 'sha256': args.root_final_receipt_sha256}, {'path': paths['whole_scope_contract'].name, 'bytes': len(paths['whole_scope_contract'].read_bytes()), 'sha256': args.whole_scope_contract_sha256}], key=lambda row: row['path'])), 'Actual final two-member receipt/scope closure differs')
    capture = load(paths['reconciliation_capture'])
    required_values(capture, {'actual_execution': True, 'completed': True, 'exit_code': 0, 'status': 'PASS', 'source_sha256': sha((HERE / 'seal_final_evidence.py').read_bytes()), 'stdin_supplied': False}, 'Actual root final reconciliation child capture')
    require(type(capture['pid']) is int and capture['pid'] > 0 and type(capture['argv']) is list and str(HERE / 'seal_final_evidence.py') in capture['argv'], 'Actual final child source/argv/pid required')
    require(type(capture['started_utc']) is str and type(capture['finished_utc']) is str, 'Actual final ISO UTC clock strings required')
    started = dt.datetime.fromisoformat(capture['started_utc'])
    finished = dt.datetime.fromisoformat(capture['finished_utc'])
    require(started.tzinfo is not None and finished.tzinfo is not None and
            started.utcoffset() == dt.timedelta(0) and finished.utcoffset() == dt.timedelta(0) and
            started <= finished, 'Actual final clocks must be aware UTC and ordered')
    require(capture['cwd'] == str(A), 'Actual final reconciliation audit cwd required')
    argv = capture['argv']
    for flag, expected in [('--preparation-manifest-sha256', args.preparation_manifest_sha256), ('--plan', root['root_reviewed_plan']['path']), ('--plan-sha256', root['root_reviewed_plan']['sha256'])]:
        require(argv.count(flag) == 1 and argv.index(flag) + 1 < len(argv) and argv[argv.index(flag) + 1] == expected, 'Actual final argv pin differs: ' + flag)
    require(argv.count('--execute') == 1, 'Actual final explicit execution flag required')
    bound_repository(root['root_reviewed_plan'])
    require(strict_equal(root['reconciliation_source'], repo_pin(HERE / 'seal_final_evidence.py')), 'Exact final reconciliation source binding differs')
    cap_base = paths['reconciliation_capture'].parent
    require(paths['reconciliation_capture'].name == 'CAPTURE.json', 'Actual capture must have the literal root CAPTURE.json name')
    capture_names = ['CAPTURE.json', 'prelaunch_source.py', capture['stdout']['path'], capture['stderr']['path']]
    for name in capture_names:
        relative(name)
        require(PurePosixPath(name).name == name, 'Each capture member must be a canonical root basename')
    require(len(set(capture_names)) == 4, 'Exactly four distinct capture members; no channel/reserved-name aliases')
    require(sha(regular(cap_base, 'prelaunch_source.py').read_bytes()) == capture['source_sha256'], 'Actual final prelaunch source differs')
    for key in ['stdout', 'stderr']:
        row = normalize_rows([capture[key]])[0]
        check_rows(cap_base, [row])
    parsed_stdout = parse(regular(cap_base, capture['stdout']['path']).read_bytes())
    required_values(parsed_stdout, {'status': 'PASS', 'root_final_receipt_sha256': args.root_final_receipt_sha256, 'whole_scope_contract_sha256': args.whole_scope_contract_sha256, 'final_manifest_sha256': args.root_final_manifest_sha256}, 'Full actual final child stdout')
    exact_closure(cap_base, capture_names)
    frozen = manifest(C, C / 'MANIFEST.json', CURRENT_SHA, 2901)
    snapshot = load(A / 'snapshot_manifest.json')
    require(sha((A / 'snapshot_manifest.json').read_bytes()) == SNAPSHOT_SHA and snapshot['head'] == HEAD and snapshot['base'] == ORIGINAL_BASE and len(snapshot['files']) == 16 and len(snapshot['changed_paths']) == 17, 'Exact original16/17diff snapshot differs')
    actual_diff = git_bytes('diff', ORIGINAL_BASE, HEAD)
    require(git_bytes('diff', '--name-only', ORIGINAL_BASE, HEAD).decode().splitlines() == snapshot['changed_paths'] and len(actual_diff) == snapshot['diff_bytes'] and sha(actual_diff) == snapshot['diff_sha256'] and actual_diff == (A / 'pr_input/diff.patch').read_bytes(), 'Entire original17-path real Git diff differs')
    for row in snapshot['files']:
        raw = regular(C / 'original_archive', row['path']).read_bytes()
        require(len(raw) == row['size'] and sha(raw) == row['sha256'] and raw == git_bytes('show', HEAD + ':unsolved_math_prioritization/attempts/' + ID + '/' + row['path']), 'Exact original Git/archive artifact differs')
    for revision in [ORIGINAL_BASE, HEAD]:
        data = git_bytes('show', revision + ':unsolved_math_prioritization/state.json')
        require(data == (C / 'historical_native_state' / (revision + '.json')).read_bytes() and ID not in parse(data), 'Original base/head selected state must be absent with exact historical bytes')
        history = optional_git_file(revision, 'unsolved_math_prioritization/history.jsonl')
        require(not any(str(z.get('id', z.get('problem_id', ''))) == ID for z in map(parse, history.splitlines())), 'Original selected native history must remain absent')
    require(sha(PREVIOUS.read_bytes()) == digest(args.previous_mirror_sha256), 'Fresh completed PR38 mirror proposal pin required')
    return frozen, {'reviewed_candidate_manifest_sha256': CURRENT_SHA, 'current_proof_dependencies_sha256': DEPENDENCIES_SHA,
        'preparation_manifest_sha256': args.preparation_manifest_sha256, 'previous_mirror_sha256': args.previous_mirror_sha256,
        **{key: getattr(args, key) for key in ['whole_manifest', 'whole_manifest_sha256', 'root_final_receipt', 'root_final_receipt_sha256', 'whole_scope_contract', 'whole_scope_contract_sha256', 'root_final_manifest', 'root_final_manifest_sha256', 'reconciliation_capture', 'reconciliation_capture_sha256']},
        'scientific_scope': scope['scientific_scope'], 'science_reexecution_of_current': False, 'original_actual_closed_family_replay_bound': True}


def acceptance_invariants(acceptance, pins, pre):
    required = {'schema': 'pr39-accepted-current-partial/v1', 'pr': PR, 'id': int(ID), 'problem_id': int(ID), 'problem_number': CODE,
        'outcome': 'unsolved_accepted_partial_merged', 'queue_status': 'unsolved', 'full_problem_solved': False, 'positive_novelty_claim': False,
        'original_head': HEAD, 'original_base': ORIGINAL_BASE, 'merge_parents': [pre['main_before'], HEAD], 'remote_state': 'MERGED', 'remote_isDraft': False,
        'canonical_scientific_artifact_sha256': PARTIAL_SHA, 'original_partial_sha256': PARTIAL_SHA,
        'source_record_sha256': SOURCE_SHA, 'original_ledger_sha256': LEDGER_SHA,
        'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'substantive_attempts_used': 2, 'substantive_attempt_limit': 5, 'verification_attempts_added': 0,
        'paper_or_new_doi_or_tracker': False, 'human_peer_review_asserted': False, 'workflow_completion_estimate_percent': 100, 'full_resolution_completion_estimate_percent': 0,
        'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'historical_metadata_archival_only': True,
        'separate_prior_report_present': True, 'prior_fallback_used': False, 'prior_report_sha256': PRIOR_SHA, 'accepted_source_for_mirror': 'source_record.json',
        'historical_worker_transcript': 'not_verified',
        'current_mirror': 'One present acceptance, no reconstructed original native transition or extra proof turn.'}
    required_values(acceptance, {**required, **pins}, 'Accepted PR39 invariant')
    for key in ['merge_commit', 'merge_tree']:
        require(type(acceptance.get(key)) is str and re.fullmatch(r'[0-9a-f]{40}', acceptance[key]), 'Actual accepted merge binding absent')
    require(type(acceptance.get('merged_at')) is str and acceptance['merged_at'], 'Actual merge date absent')
    source_and_ledger(K)
    for name in ['readiness.json', 'status.json', 'attempt.json']:
        value = load(K / name)
        required_values(value, {'id': ID, 'problem_number': CODE, 'pr': PR, 'status': 'unsolved_accepted_partial_merged', 'queue_status': 'unsolved',
            'current_gate': 'PASS_current_source_first_and_bound_original_actual_replay', 'merge_commit': acceptance['merge_commit'], 'merge_tree': acceptance['merge_tree'],
            'remote_merged_at': acceptance['merged_at'], 'current_workflow_completion_estimate_percent': 100, 'full_resolution_completion_estimate_percent': 0,
            'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'full_problem_solved': False, 'positive_novelty_claim': False,
            'full_resolution_claimed': False, 'novelty_claimed': False, 'paper_or_new_doi_or_tracker': False,
            'source_record_sha256': SOURCE_SHA, 'original_turns_sha256': LEDGER_SHA, 'current_partial_sha256': PARTIAL_SHA,
            'canonical_historical_events_inferred': False, 'later_acceptance_is_present_only': True,
            'separate_prior_report_present': True, 'prior_fallback_used': False, 'prior_report_sha256': PRIOR_SHA,
            'original_substantive_attempts': 2, 'substantive_attempt_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
            'original_authored_runtime_metadata': load(C / 'original_archive/readiness.json'), **pins}, 'Accepted administration ' + name)
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
    require(all(strict_equal(new[number], old[number]) for number in old if number != PR), 'Unselected inventory item changed')
    administrative = {'updated_at_utc', 'last_checkpoint_utc', 'completed_count', 'program_completion_estimate_percent', 'completion_estimate_percent', 'current_pr', 'items'}
    require(strict_equal({k: v for k, v in before.items() if k not in administrative}, {k: v for k, v in after.items() if k not in administrative}), 'Unrelated top-level inventory metadata changed')
    selected_changes = {'stage', 'outcome', 'queue_status', 'audited_head', 'merge_commit', 'merged_at', 'workflow_completion_estimate_percent', 'original_attempts', 'new_substantive_attempts', 'cumulative_attempts', 'paper_or_new_doi_or_tracker'}
    require(strict_equal({k: v for k, v in old[PR].items() if k not in selected_changes}, {k: v for k, v in new[PR].items() if k not in selected_changes}), 'Unrelated selected inventory attributes changed')


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
        require((K / 'original_archive' / row['path']).read_bytes() == (C / 'original_archive' / row['path']).read_bytes(), 'Original16 archive changed')
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
    spec = importlib.util.spec_from_file_location('pr39_bound_mirror', path)
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
            old_path = B / 'audits/pr38_2765/reviewed_candidate_v2/turns.json'
            mirror.require(sha(data) == 'b04b008cb90eb04c0586f32eaf2ef59d608ffc8e10f2721acfb70e91584e5737' and strict_equal(obj, load(old_path)) and used == 2 and limit == 5, 'Preserve exact PR38 two-row list ledger')
        elif kind == 'pr39_exact_original_attempt_object':
            obj = parse(data)
            mirror.require(sha(data) == LEDGER_SHA and strict_equal(obj, load(C / 'turns.json')) and obj['id'] == int(ID) and obj['count'] == 2 and [z['number'] for z in obj['attempts']] == [1, 2] and type(used) is int and used == 2 and type(limit) is int and limit == 5, 'Exact PR39 original attempt object required')
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
