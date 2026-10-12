"""Static PR37 root-only guards. No import-time mutation or execution.

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
A = HERE.parent
R = A.parents[2]
B = R / 'draft_pr_publication_program_20260930'
C = A / 'reviewed_candidate'
K = R / 'unsolved_math_prioritization/attempts/3009'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '3009', 'KP-5.2', 37
HEAD = '84bb43d21b36e4d97229806e2518fbc135bee786'
ORIGINAL_BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
CURRENT_SHA = 'ca440e7d4f378db294256e3d9a7a7b3f4e5344df562db9a2c4bb5092952dd2de'
DEPENDENCIES_SHA = '978f8e80fbccc453ec027c428414b6e7420df0c392d3d1c669df91a66f72b263'
SNAPSHOT_SHA = 'f2dbbca27d6b67cebe6eaa5563c990e54c5124de2ca2c626b9f124ca850ec10e'
LEDGER_SHA = '7bf94bf41466a40deceab668ecbb12a54b16fe16ad400bc221ff6f18e7558498'
SOURCE_SHA = 'f5624aff4127262fb0b9cad436377198c4c2953fcd18503f89fce013c4f7f042'
PINNED_SOURCE_SHA = '5d02c538258c518929d899638d28082a276958613baa93596921a5e903504b09'
PARTIAL_SHA = '11b674cee884531e4fb071babcbc442cbc17d8da9bbb93d445cd0bb0d6d9d794'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
WRITER_SHA = 'b72afa148d034818cc90fd25b6b084fd94e42604d433a64e09a4ee01ae6e5271'
PREVIOUS = B / 'audits/pr36_20001424/state_mirror_bindings.json'
PREVIOUS_SHA = '09a5bffa391fec5c49365559e5fe318d42964cb4d3e67cceb6e963e279e0a869'
ADMIN = {'README.md', 'pr_body.md', 'readiness.json', 'status.json', 'CURRENT_AUDIT_SCOPE.md', 'RESEARCH_LOG.md'}
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
FOREIGN_TRACKED_EXCLUSIONS = {
    'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/commands.tsv',
    'paper_ii_simultaneous_amplification_referee_audit_2026-08-22/logs/full_transcript.log',
}
SCRATCH = {'tmp', '__pycache__', 'private_tmp', 'private_sources', 'foreign_sources', 'foreign_downloads'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load(path):
    return json.loads(Path(path).read_bytes())


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode()


def write(path, data, exclusive=False):
    path = Path(path)
    require(path.parent.is_dir() and not path.is_symlink(), 'Unsafe output: ' + str(path))
    if exclusive:
        require(not path.exists(), 'Inspect existing receipt before retry: ' + str(path))
    temporary = path.with_name(path.name + '.pr37-tmp')
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
    require(value['number'] == PR and value['url'] == 'https://github.com/AlecKriebel/Math/pull/37', 'Wrong remote PR')
    require(value['headRefOid'] == HEAD and value['headRefName'] == 'dot/math-' + ID and value['baseRefName'] == 'main', 'Remote original-head/base mismatch')
    return value


def digest(value):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value), 'Require explicit lowercase SHA256')
    return value


def relative(name, scratch=False):
    require(isinstance(name, str) and name and '\\' not in name and '\0' not in name, 'Invalid member name')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == name, 'Unsafe/noncanonical member: ' + name)
    if not scratch:
        require(not (SCRATCH & set(path.parts)) and path.suffix not in {'.pyc', '.tmp'}, 'Scratch/foreign member rejected: ' + name)
    return path


def regular(base, name):
    relative(name)
    base = Path(base)
    path = base / name
    require(base.is_dir() and not base.is_symlink(), 'Unsafe package root')
    require(path.resolve().is_relative_to(base.resolve()), 'Member escaped package')
    require(path.is_file() and not path.is_symlink(), 'Nonregular member: ' + name)
    for parent in path.parents:
        if parent == base:
            break
        require(not parent.is_symlink(), 'Symlink parent: ' + name)
    return path


def rows(value):
    require(isinstance(value, list), 'Binding rows must be explicit ordered list')
    names = []
    for row in value:
        require(isinstance(row, dict), 'Malformed binding row')
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


def inventory(base, exclusions=()):
    """Complete recursive file/directory closure; canonical has no exclusions."""
    base = Path(base)
    require(base.is_dir() and not base.is_symlink(), 'Unsafe closure root')
    allowed = set(exclusions)
    require(allowed <= {'tmp', '__pycache__'}, 'Only exact whole-family scratch components can be qualified')
    files, directories = set(), set()
    for path in base.rglob('*'):
        name = str(path.relative_to(base))
        parts = set(PurePosixPath(name).parts)
        # Even ignored scratch may not redirect traversal through a symlink.
        require(not path.is_symlink(), 'Symlink in recursive closure: ' + name)
        if parts & allowed:
            continue
        relative(name)
        if path.is_dir():
            directories.add(name)
        else:
            require(path.is_file(), 'Nonregular closure entry: ' + name)
            files.add(name)
    return files, directories


def exact_closure(base, expected, exclusions=()):
    expected = set(expected)
    actual, directories = inventory(base, exclusions)
    require(actual == expected, 'Complete recursive file membership differs: ' + str(sorted(actual ^ expected)))
    parents = {str(parent) for name in expected for parent in PurePosixPath(name).parents if str(parent) != '.'}
    require(directories == parents, 'Extra/missing recursive directories: ' + str(sorted(directories ^ parents)))


def manifest(base, path, expected=None, count=None, scope=None):
    base, path = Path(base), Path(path)
    require(path.parent == base and path.name in {p.name for p in base.iterdir()}, 'Require literal root manifest')
    raw = regular(base, path.name).read_bytes()
    if expected is not None:
        require(sha(raw) == digest(expected), 'Pinned manifest changed')
    obj = json.loads(raw)
    value = obj['files']
    if isinstance(value, dict):
        value = [{'path': name, **pin} for name, pin in value.items()]
    value = [{**row, 'bytes': row.get('bytes', row.get('size'))} for row in value]
    rows(value)
    require(path.name not in {row['path'] for row in value}, 'Manifest must self-exclude')
    if count is not None:
        require(len(value) == count, 'Manifest count differs')
    for key in ['files_count', 'member_count']:
        if key in obj:
            require(obj[key] == len(value), 'Declared manifest count differs')
    exclusions, malformed = [], {}
    if scope is not None:
        require(base.resolve() == (A / 'whole_current_source_first_family').resolve(), 'Whole qualification restricted to exact PR37 whole family')
        require(scope['authored_members'] == [{'path': row['path'], 'bytes': row['bytes'], 'sha256': row['sha256']} for row in value], 'Reviewed first-party authored member bindings differ')
        exclusions = scope['scratch_components_excluded']
        require(isinstance(exclusions, list) and len(exclusions) == len(set(exclusions)) and set(exclusions) <= {'tmp', '__pycache__'}, 'No arbitrary whole scratch exclusion')
        require(obj.get('foreign_scratch_excluded', []) == [name + '/' for name in exclusions], 'Manifest/scope exact scratch exclusions differ')
        exceptions = rows(scope['malformed_json_exceptions'])
        malformed = {row['path']: row for row in exceptions}
        require(set(malformed) <= {row['path'] for row in value}, 'Malformed exceptions must be reviewed authored members')
        require(all(PurePosixPath(name).suffix == '.json' for name in malformed), 'Only exact malformed JSON fixtures may be qualified')
    else:
        require(obj.get('foreign_scratch_excluded', []) == [], 'Current/canonical permits zero scratch exclusions')
    check_rows(base, value)
    for row in value:
        data = (base / row['path']).read_bytes()
        suffix = PurePosixPath(row['path']).suffix
        if suffix == '.json':
            if row['path'] in malformed:
                pin = malformed[row['path']]
                require(all(row[key] == pin[key] for key in ['bytes', 'sha256']), 'Exact malformed fixture pin differs')
                require(isinstance(pin.get('qualification'), str) and pin['qualification'], 'Malformed fixture needs exact historical qualification')
                try:
                    json.loads(data)
                except json.JSONDecodeError:
                    pass
                else:
                    raise ValueError('Pinned malformed fixture now parses')
            else:
                json.loads(data)
        elif suffix == '.jsonl':
            require(not data or data.endswith(b'\n'), 'Incomplete JSONL member')
            for line in data.splitlines():
                json.loads(line)
    exact_closure(base, {row['path'] for row in value} | {path.name}, exclusions)
    return value


def add_gate_args(parser):
    parser.add_argument('--execute', action='store_true', help='Future root-only explicit execution')
    for name in ['whole-manifest', 'root-final-receipt', 'whole-scope-contract']:
        parser.add_argument('--' + name, required=True, help='Repository-relative finalized artifact')
        parser.add_argument('--' + name + '-sha256', required=True)


def bound_repository(pin):
    path = regular(R, pin['path'])
    require(path.resolve().is_relative_to(A.resolve()), 'Final replay binding must belong to PR37 audit')
    raw = path.read_bytes()
    require(len(raw) == pin['bytes'] and sha(raw) == digest(pin['sha256']), 'Final replay binding changed')
    return raw


def source_and_ledger(base):
    source, pinned = (base / 'source_record.json').read_bytes(), (base / 'pinned_problem.json').read_bytes()
    require(sha(source) == SOURCE_SHA and sha(pinned) == PINNED_SOURCE_SHA, 'Both exact source serializations must survive')
    require(source != pinned and json.loads(source) == json.loads(pinned), 'Flat full JSON semantic equality / byte inequality required')
    require(json.loads(source).get('id') == int(ID), 'Wrong numeric flat source')
    require(load(base / 'pinned_importer_prior_fallback.json') == {}, 'Pinned empty fallback is not a retrieved separate prior report')
    ledger = (base / 'turns.json').read_bytes()
    require(sha(ledger) == LEDGER_SHA, 'Entire original ledger bytes changed')
    obj = json.loads(ledger)
    require(obj['problem_id'] == int(ID) and obj['problem_number'] == CODE and obj['substantive_turns_used'] == 1 and obj['turn_limit'] == 5 and obj['outcome'] == 'unsolved', 'Native authored budget changed')
    require([z['turn'] for z in obj['responses']] == [1] and obj['responses'][0]['artifact'] == 'PARTIAL.md', 'Authored response changed')


def gates(args):
    require(args.execute, 'Prepared only: future root --execute required')
    require(git('branch', '--show-current') == 'main', 'Stay on main')
    frozen = manifest(C, C / 'MANIFEST.json', CURRENT_SHA, 96)
    require(sha((C / 'CURRENT_PROOF_DEPENDENCIES.json').read_bytes()) == DEPENDENCIES_SHA, 'Frozen443 dependency manifest changed')
    dependency = load(C / 'CURRENT_PROOF_DEPENDENCIES.json')
    require(dependency['dependency_anchor_repository_relative'] == str(A.relative_to(R)) and len(dependency['files']) == 443, 'Require exact audit anchor/all443 dependencies')
    check_rows(A, dependency['files'])
    paths = {}
    for name in ['whole_manifest', 'root_final_receipt', 'whole_scope_contract']:
        path = regular(R, getattr(args, name))
        require(path.resolve().is_relative_to(A.resolve()) and not path.resolve().is_relative_to(C.resolve()), 'Final gate belongs to PR37 audit outside frozen candidate')
        require(sha(path.read_bytes()) == digest(getattr(args, name + '_sha256')), 'Explicit final gate pin changed: ' + name)
        paths[name] = path
    scope = load(paths['whole_scope_contract'])
    require(scope['schema'] == 'pr37-root-reviewed-final-whole-scope/v1' and scope['pr'] == PR and scope['problem_id'] == int(ID), 'Wrong final whole contract')
    require(scope['whole_manifest_sha256'] == args.whole_manifest_sha256 and scope['root_final_receipt_sha256'] == args.root_final_receipt_sha256, 'Contract/final gate pins differ')
    whole = manifest(paths['whole_manifest'].parent, paths['whole_manifest'], args.whole_manifest_sha256, scope=scope)
    root = load(paths['root_final_receipt'])
    required = {'schema': 'pr37-actual-final-whole-reproduction/v1', 'status': 'PASS', 'pr': PR, 'problem_id': int(ID), 'original_head': HEAD,
                'reviewed_candidate_manifest_sha256': CURRENT_SHA, 'current_proof_dependencies_sha256': DEPENDENCIES_SHA,
                'whole_manifest_sha256': args.whole_manifest_sha256, 'entire_current_packet_checked': True, 'root_actual_reproduction': True,
                'mandatory_corrections': [], 'queue_status': 'unsolved', 'full_problem_solved': False, 'positive_novelty_claim': False,
                'original_substantive_attempts': 1, 'new_substantive_attempts': 0, 'verification_attempts_added': 0,
                'paper_or_new_doi_or_tracker': False, 'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None}
    require(all(root.get(key) == value for key, value in required.items()), 'Root final receipt scope missing; never fabricate pass fields')
    replay = rows(scope['root_replay_bindings'])
    require(replay and root['root_replay_bindings'] == replay, 'Bind every actual root replay authored source/receipt/stream')
    for row in replay:
        bound_repository(row)
    wrapper = scope['root_wrapper']
    require(wrapper in replay and root['root_wrapper'] == wrapper, 'Root actual wrapper source not explicitly pinned')
    bound_repository(wrapper)
    expected_snapshots = {'reviewed_candidate': [{'path': z['path'], 'bytes': z['bytes'], 'sha256': z['sha256']} for z in frozen] + [{'path': 'MANIFEST.json', 'bytes': len((C / 'MANIFEST.json').read_bytes()), 'sha256': CURRENT_SHA}],
                          'dependencies': dependency['files'], 'whole_authored_members': scope['authored_members']}
    require(root['bindings_before'] == expected_snapshots == root['bindings_after'], 'Require every current97/dependency443/final authored member exact before/after actual replay')
    executions = root['actual_outer_executions']
    require(isinstance(executions, list) and executions and [z['label'] for z in executions] == scope['required_outer_execution_labels'], 'All actual outer execution labels required')
    require(len({z['label'] for z in executions}) == len(executions), 'Duplicate outer execution')
    replay_by_path = {z['path']: z for z in replay}
    require(root['actual_outer_executions'] == scope['actual_outer_execution_specs'], 'Root-reviewed entire actual outer execution specs differ')
    for execution in executions:
        require(execution['actual_execution'] is True and type(execution['returncode']) is int and execution['returncode'] == 0, 'Actual outer execution must return0')
        require(isinstance(execution['argv'], list) and execution['argv'] and execution['started_at_utc'] and execution['finished_at_utc'], 'Recorded actual command/time required')
        require(execution['wrapper'] == wrapper, 'Execution wrapper source differs')
        for key in ['stdout', 'stderr', 'receipt']:
            pin = execution[key]
            require(replay_by_path.get(pin['path']) == pin, 'Execution stream/receipt omitted from final replay closure')
            bound_repository(pin)
        receipt = json.loads(bound_repository(execution['receipt']))
        require(receipt == execution['parsed_receipt'], 'Compare complete parsed actual outer receipt')
    comparisons = root['structured_comparisons']
    require(isinstance(comparisons, list) and comparisons and [z['label'] for z in comparisons] == scope['required_comparison_labels'], 'Complete required parsed comparisons missing')
    require(len({z['label'] for z in comparisons}) == len(comparisons), 'Duplicate comparison label')
    require(comparisons == scope['structured_comparison_specs'], 'Root-reviewed full comparison specifications differ')
    coverage = scope['required_comparison_coverage']
    require(set(coverage) == {'original_complete_controls31', 'independent_complete_controls8462', 'all_three_closed_families', 'whole_positive_and_mutant_receipts'}, 'Require complete original/independent/closed-family/whole comparison coverage')
    require(all(isinstance(labels, list) and labels and set(labels) <= {z['label'] for z in comparisons} for labels in coverage.values()), 'Every complete comparison coverage group needs exact labels')
    require(root['comparison_coverage'] == coverage, 'Actual complete comparison coverage differs')
    reviewed_bindings = dict(replay_by_path)
    for base, values in [(C, frozen), (A, dependency['files']), (paths['whole_manifest'].parent, whole)]:
        for pin in values:
            name = str((base / pin['path']).relative_to(R))
            reviewed_bindings[name] = {'path': name, 'bytes': pin['bytes'], 'sha256': pin['sha256']}
    for comparison in comparisons:
        actual_pin, expected_pin = comparison['actual'], comparison['expected']
        require(actual_pin['path'] != expected_pin['path'], 'Comparison cannot use the same file as actual and expected')
        require(replay_by_path.get(actual_pin['path']) == actual_pin, 'Actual comparison omitted from root replay closure')
        require(reviewed_bindings.get(expected_pin['path']) == expected_pin, 'Expected complete output must be first-party reviewed/dependency/root-replay member')
        actual, expected = bound_repository(actual_pin), bound_repository(expected_pin)
        kind = comparison['kind']
        if kind == 'full_parsed_json':
            require(json.loads(actual) == json.loads(expected), 'Complete JSON differs: ' + comparison['label'])
        elif kind == 'full_parsed_jsonl':
            require([json.loads(x) for x in actual.splitlines()] == [json.loads(x) for x in expected.splitlines()], 'Complete JSONL differs')
        elif kind == 'byte_exact':
            require(actual == expected, 'Complete byte comparison differs')
        else:
            raise ValueError('No projection/PASS-label-only comparison allowed')
    require(sha((A / 'snapshot_manifest.json').read_bytes()) == SNAPSHOT_SHA, 'Original13 snapshot changed')
    snapshot = load(A / 'snapshot_manifest.json')
    require(snapshot['head'] == HEAD and snapshot['base'] == ORIGINAL_BASE and len(snapshot['files']) == 13 and len(snapshot['changed_paths']) == 14, 'Original13/14diff scope changed')
    actual_changed = git_bytes('diff', '--name-only', ORIGINAL_BASE, HEAD).decode().splitlines()
    original_diff = git_bytes('diff', ORIGINAL_BASE, HEAD)
    require(actual_changed == snapshot['changed_paths'] and len(original_diff) == snapshot['diff_bytes'] and sha(original_diff) == snapshot['diff_sha256'], 'Entire actual original14-path Git diff changed')
    require(original_diff == (A / 'pr_input/diff.patch').read_bytes(), 'Exact archived original diff differs from actual Git diff')
    for row in snapshot['files']:
        raw = regular(C / 'original_archive', row['path']).read_bytes()
        require(len(raw) == row['size'] and sha(raw) == row['sha256'] and raw == git_bytes('show', HEAD + ':unsolved_math_prioritization/attempts/' + ID + '/' + row['path']), 'Exact original Git/archive artifact differs')
    source_and_ledger(C)
    patch = load(C / 'CURRENT_PARTIAL_SOURCE_PATCH_RECEIPT.json')
    original = (C / 'original_archive/PARTIAL.md').read_bytes()
    updated = original
    require(patch['replacement_count'] == len(patch['replacements']) == 3, 'Exactly three source-only replacements')
    for replacement in reversed(patch['replacements']):
        old, new, offset = replacement['before'].encode(), replacement['after'].encode(), replacement['original_byte_offset']
        require(original[offset:offset + len(old)] == old and len(old) == replacement['before_bytes'] and len(new) == replacement['after_bytes'] and sha(old) == replacement['before_sha256'] and sha(new) == replacement['after_sha256'], 'Source-only replacement binding differs')
        updated = updated[:offset] + new + updated[offset + len(old):]
    require(updated == (C / 'PARTIAL.md').read_bytes() and sha(updated) == PARTIAL_SHA, 'PARTIAL science changed outside three reviewed replacements')
    historical = load(C / 'CURRENT_NATIVE_HISTORICAL_STATE.json')
    for revision in [ORIGINAL_BASE, HEAD]:
        data = git_bytes('show', revision + ':unsolved_math_prioritization/state.json')
        record = historical['states'][revision]
        require(len(data) == record['bytes'] and sha(data) == record['sha256'] and json.loads(data) == record['entire_object'] and ID not in json.loads(data), 'No original native target state may be invented')
        history = optional_git_file(revision, 'unsolved_math_prioritization/history.jsonl')
        require(not any(str(z.get('id', z.get('problem_id', ''))) == ID for z in map(json.loads, history.splitlines())), 'Original native target history unexpectedly present')
    return frozen, {'reviewed_candidate_manifest_sha256': CURRENT_SHA, 'current_proof_dependencies_sha256': DEPENDENCIES_SHA,
                    **{key: getattr(args, key) for key in ['whole_manifest', 'whole_manifest_sha256', 'root_final_receipt', 'root_final_receipt_sha256', 'whole_scope_contract', 'whole_scope_contract_sha256']},
                    'root_wrapper': wrapper, 'whole_scratch_components_excluded': scope['scratch_components_excluded'],
                    'whole_malformed_json_exceptions': scope['malformed_json_exceptions']}


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
        records.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw), 'head_sha256': sha(git_bytes('show', 'HEAD:' + name)), 'dirty_at_preflight': name in dirty, 'integration_and_checkpoint_excluded': True})
    foreign_tracked_unchanged({'foreign_tracked_exclusions': records})
    return records


def foreign_tracked_unchanged(pre):
    records = pre['foreign_tracked_exclusions']
    require(len(records) == len(FOREIGN_TRACKED_EXCLUSIONS) and {z['path'] for z in records} == FOREIGN_TRACKED_EXCLUSIONS, 'No broad/untracked exception scope')
    for row in records:
        raw = regular(R, row['path']).read_bytes()
        require(row['integration_and_checkpoint_excluded'] is True and len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Foreign writer changed bytes; inspect, never checkpoint or overwrite')
        require(sha(git_bytes('show', 'HEAD:' + row['path'])) == row['head_sha256'], 'Foreign HEAD bytes accidentally committed')
        stages = [z for z in git_bytes('ls-files', '--stage', '-z', '--', row['path']).decode().split('\0') if z]
        require(len(stages) == 1, 'Foreign index conflicted/ambiguous')
        fields, name = stages[0].split('\t', 1)
        mode, blob, stage = fields.split()
        require(name == row['path'] and stage == '0' and mode in {'100644', '100755'} and sha(git_bytes('show', ':' + name)) == row['head_sha256'], 'Foreign dirty bytes staged/index mode changed')


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
    # A full-tree diff whitelist prevents unrelated tracked or untracked files
    # being swept into this merge by broad staging, even outside canonical scope.
    changed = set(git_bytes('diff-tree', '-r', '--no-commit-id', '--name-only', '-z', pre['main_before'], merge).decode().split('\0')) - {''}
    require(changed <= {prefix + z['path'] for z in value} | {'unsolved_math_prioritization/QUEUE.md'}, 'Unrelated path entered real merge tree')
    return actual_tree


def load_mirror():
    path = BASE / 'revision2/accepted_state_sync_v2.py'
    require(sha(path.read_bytes()) == MIRROR_SHA and sha((BASE / 'root_apply/guarded_import_v2.py').read_bytes()) == WRITER_SHA, 'Reviewed mirror/writer sources changed')
    spec = importlib.util.spec_from_file_location('pr37_bound_mirror', path)
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
            obj = json.loads(data)
            mirror.require(sha(data) == LEDGER_SHA and obj == load(C / 'turns.json') and used == 1 and limit == 5, 'PR37 original complete ledger must remain byte exact')
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
