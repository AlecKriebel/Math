#!/usr/bin/env python3
"""STATIC ROOT-ONLY sealing adapter; never execute/import in preparation.

Consume a positive actual child capture plus an explicitly root-reviewed full
comparison plan. Preserve full raw inputs, exact normalization operations and
full normalized objects. No subprocess, helper import, Git/remote/shared write.
Only fresh root audit sealing support and two final gate files are created.
"""
import argparse
import copy
import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
A = HERE.parent
R = A.parents[2]
C = A / 'reviewed_candidate'
W = A / 'whole_current_source_first_family'
OUT = A / 'root_source_first_private_reexecution'
CAP = A / 'root_final_whole_actual_capture'
SUP = A / 'root_final_whole_sealing_support'
CURRENT = 'ca440e7d4f378db294256e3d9a7a7b3f4e5344df562db9a2c4bb5092952dd2de'
DEPS = '978f8e80fbccc453ec027c428414b6e7420df0c392d3d1c669df91a66f72b263'
WHOLE = '859ee278297d08853fcdbc1eefe2d6cf675e5d89c02e756a23ca1eb959dafd48'
REPLAY = '4e51f166ba3f4a345b6cdd71b82ad866eef3f946fda540eb0cac09063e53a9b4'
WRAPPER = 'f5f4ac9504c9338d56c925102f635128fc7065beea594f27f919b699df7e63d7'
GROUPS = {'original_complete_controls31', 'independent_complete_controls8462', 'all_three_closed_families', 'whole_positive_and_mutant_receipts'}


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode()


def path(name):
    relative = PurePosixPath(name)
    require(name and '\\' not in name and not relative.is_absolute() and '..' not in relative.parts and str(relative) == name, 'Unsafe repository-relative pin')
    result = R / name
    require(result.resolve().is_relative_to(A.resolve()) and result.is_file() and not result.is_symlink() and all(not p.is_symlink() for p in result.parents), 'Require regular first-party PR37 audit file')
    return result


def pin(file):
    file = Path(file)
    data = file.read_bytes()
    return {'path': str(file.relative_to(R)), 'bytes': len(data), 'sha256': sha(data)}


def bound(value):
    require(set(value) == {'path', 'bytes', 'sha256'} and type(value['bytes']) is int and value['bytes'] >= 0 and re.fullmatch(r'[0-9a-f]{64}', value['sha256']), 'Exact raw pin schema required')
    data = path(value['path']).read_bytes()
    require(len(data) == value['bytes'] and sha(data) == value['sha256'], 'Bound raw bytes changed: ' + value['path'])
    return data


def load(file):
    return json.loads(Path(file).read_bytes())


def save(file, data):
    file = Path(file)
    require(file.parent.is_dir() and not file.exists() and not file.is_symlink(), 'Only fresh outputs; retain prior evidence')
    with file.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def same_typed(first, second):
    if type(first) is not type(second):
        return False
    if isinstance(first, dict):
        return set(first) == set(second) and all(same_typed(first[k], second[k]) for k in first)
    if isinstance(first, list):
        return len(first) == len(second) and all(same_typed(x, y) for x, y in zip(first, second))
    return first == second


def pointer_leaf(value, pointer):
    require(pointer.startswith('/') and pointer != '/', 'Explicit nonroot leaf JSON pointer required')
    names = [x.replace('~1', '/').replace('~0', '~') for x in pointer[1:].split('/')]
    parent = value
    for name in names[:-1]:
        parent = parent[int(name)] if isinstance(parent, list) else parent[name]
    key = int(names[-1]) if isinstance(parent, list) else names[-1]
    require(key in parent if isinstance(parent, dict) else 0 <= key < len(parent), 'Normalization pointer absent')
    require(not isinstance(parent[key], (dict, list)), 'No subtree deletion/projection/array reduction permitted')
    return parent, key


def normalize_json(actual, expected, operations):
    actual, expected = copy.deepcopy(actual), copy.deepcopy(expected)
    seen = set()
    for operation in operations:
        require(set(operation) == {'pointer', 'actual_before', 'expected_before', 'canonical_value', 'qualification'}, 'Explicit exact normalization schema')
        require(operation['pointer'] not in seen and isinstance(operation['qualification'], str) and operation['qualification'], 'Unique qualified normalization required')
        seen.add(operation['pointer'])
        left, key = pointer_leaf(actual, operation['pointer'])
        right, other_key = pointer_leaf(expected, operation['pointer'])
        require(same_typed(left[key], operation['actual_before']) and same_typed(right[other_key], operation['expected_before']), 'Exact raw normalization preimage differs')
        require(type(operation['canonical_value']) is type(left[key]) is type(right[other_key]), 'Normalization cannot change scalar types')
        require(type(left[key]) in {str, int}, 'No truth-value/null/proof-number normalization')
        if type(left[key]) is int:
            recorded_byte_delta = str(key) in {'actual', 'saved', 'expected'} and isinstance(left, dict) and isinstance(left.get('path'), str) and re.search(r'/(bytes|size|stdout_bytes|stderr_bytes)$', left['path'])
            require(str(key) in {'bytes', 'size', 'stdout_bytes', 'stderr_bytes'} or recorded_byte_delta, 'Only explicitly recorded byte-count metadata may normalize')
        else:
            require(str(key) not in {'status', 'outcome', 'queue_status', 'problem_number', 'label', 'reason', 'statement', 'exact_target', 'artifact'}, 'No scope/status/mathematical normalization')
            generated_name = str(key) == 'path' and re.fullmatch(r'generated_tmp__root_original_replay_20261002T\d{12}Z__(check_results.json|independent_review__independent_results.json)', left[key]) and re.fullmatch(r'generated_tmp__root_original_replay_20261002T\d{12}Z__(check_results.json|independent_review__independent_results.json)', right[other_key])
            metadata = ('/Users/alec/Documents/Math' in left[key] and '/Users/alec/Documents/Math' in right[other_key]) or (re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', left[key]) and re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', right[other_key])) or (re.fullmatch(r'2026-\d\d-\d\d[T ].*', left[key]) and re.fullmatch(r'2026-\d\d-\d\d[T ].*', right[other_key])) or ('AssertionError' in left[key] and 'AssertionError' in right[other_key]) or generated_name
            require(metadata, 'Only explicit clock/path/derived hash/retained traceback metadata may normalize')
        left[key] = copy.deepcopy(operation['canonical_value'])
        right[other_key] = copy.deepcopy(operation['canonical_value'])
    require(same_typed(actual, expected), 'Complete normalized JSON differs; no field projection or failure exclusion')
    return actual, expected


def complete_inventory(root):
    result = []
    for file in sorted(Path(root).rglob('*')):
        require(not file.is_symlink(), 'No symlink in root replay evidence closure')
        if file.is_file():
            result.append(pin(file))
    return result


def verify_capture():
    capture = load(CAP / 'ACTUAL_OUTER_CAPTURE.json')
    require(capture['schema'] == 'pr37-root-actual-outer-capture/v1' and capture['status'] == 'CAPTURE_PASS' and capture['actual_execution'] is True and type(capture['child_pid']) is int and capture['child_pid'] > 0 and type(capture['returncode']) is int and capture['returncode'] == 0, 'Positive actual root PID/return0 capture required')
    require(capture['wrapper']['sha256'] == WRAPPER and capture['closed_replay_source']['sha256'] == REPLAY and capture['whole_manifest_sha256'] == WHOLE and capture['candidate_manifest_sha256'] == CURRENT and capture['dependency_manifest_sha256'] == DEPS, 'Actual source/frozen capture pins differ')
    bound(capture['wrapper']); bound(capture['closed_replay_source'])
    require(capture['argv'] == ['/usr/bin/python3', str(W / 'replay_gate.py'), '--repository-root', str(R), '--output-root', str(OUT)], 'Actual unchanged replay argv differs')
    before = json.loads(bound(capture['bindings_before']))
    after = json.loads(bound(capture['bindings_after']))
    require(same_typed(before, after), 'Every frozen before/after member differs')
    require(len(before['reviewed_candidate']) == 97 and len(before['dependencies']) == 443 and len(before['whole_authored_members']) == 1287, 'Require complete97/443/1287+self snapshots')
    require(before['whole_manifest_self']['sha256'] == WHOLE, 'Whole manifest self before/after missing')
    require(bound(capture['shared_before']) == bound(capture['shared_after']), 'Shared complete preimage records changed')
    for base, records in [(C, before['reviewed_candidate']), (A, before['dependencies']), (W, before['whole_authored_members'] + [before['whole_manifest_self']])]:
        require(len({z['path'] for z in records}) == len(records), 'Duplicate captured member')
        for row in records:
            file = base / row['path']
            data = bound(pin(file))
            require(len(data) == row['bytes'] and sha(data) == row['sha256'], 'Captured current frozen member changed')
    result = json.loads(bound(capture['result']))
    require(capture['result'] == pin(OUT / 'RESULT.json') and result['status'] == 'PASS' and result['manifest_pin'] == CURRENT and result['dependency_pin'] == DEPS and result['original_attempts'] == '1/5' and result['new_substantive_attempts'] == result['audit_attempts_added'] == 0, 'Actual whole result incomplete')
    summary = json.loads(bound(capture['stdout']))
    require(summary == {'status': 'PASS', 'output': str(OUT), 'outer_subprocess_runs': len(result['runs']), 'checks': len(result['checks'])} and bound(capture['stderr']) == b'', 'Complete actual stdout/stderr interface differs')
    expected = load(W / 'replay_v7/RESULT.json')
    require(same_typed(result['checks'], expected['checks']) and len(result['checks']) == 17, 'Every positive/code/prose/inventory/builder control differs')
    runs = result['runs']
    require([z['label'] for z in runs] == ['live_branch', 'actual_closed_collector', 'original31', 'original8462', 'bad_embedding', 'bad_vectors', 'private_actual_builder'], 'Entire actual whole run list differs')
    for row in runs:
        require(type(row['exit']) is int and row['exit'] == (1 if row['label'] in {'bad_embedding', 'bad_vectors'} else 0), 'Actual run/expected material-mutant outcome differs')
        for channel in ['stdout', 'stderr']:
            record = row[channel]
            actual = pin(OUT / record['path'])
            require(actual['bytes'] == record['bytes'] and actual['sha256'] == record['sha256'], 'Full outer inner stream missing')
        if row['label'] in {'bad_embedding', 'bad_vectors'}:
            stderr = (OUT / row['stderr']['path']).read_bytes()
            require(b'AssertionError' in stderr and b'ModuleNotFoundError' not in stderr, 'Code mutant failed for setup instead of material mathematics')
    for name, count, receipt in [('original31', 31, 'check_results.json'), ('original8462', 8462, 'independent_review/independent_results.json')]:
        actual = (OUT / 'support' / (name + '.generated.json')).read_bytes()
        saved = (C / 'original_archive' / receipt).read_bytes()
        parsed = json.loads(actual)
        require(actual == saved and same_typed(parsed, json.loads(saved)) and parsed['passed'] == len(parsed['checks']) == count and parsed['failed'] == 0, 'Complete actual31/8462 receipt differs')
    collector = load(OUT / 'support/NEW_ACTUAL_COLLECTOR.json')
    outer = collector['actual_outer_program_runs']
    closed_bindings = collector['closed_members_and_manifest_self_bytes_unchanged']
    require(collector['status'] == 'PASS' and len(outer) == 9 and collector['authored_members_verified_before_and_after'] == 48 and isinstance(closed_bindings, list) and closed_bindings and len({z['path'] for z in closed_bindings}) == len(closed_bindings), 'Fresh actual nine-run/48 member collector incomplete')
    for row in closed_bindings:
        data = bound({'path': row['path'], 'bytes': row['size'], 'sha256': row['sha256']})
    retained = OUT / 'support/complete_closed_collector_streams'
    for row in outer:
        require(type(row['returncode']) is int and row['returncode'] == row['exit_code'] == row['exit'] == 0, 'All nine actual collector outer executions require0')
        for channel in ['stdout', 'stderr']:
            record = row[channel]
            name = Path(record['path']).relative_to('new_actual_collector_support')
            data = (retained / name).read_bytes()
            require(len(data) == record['size'] and sha(data) == record['sha256'], 'Fresh collector full stream missing')
    nested = list(retained.rglob('nested_runs.json'))
    require(sum(len(load(file)) for file in nested) == 82, 'Require every actual82 nested run record')
    for file in nested:
        for index, row in enumerate(load(file)):
            for channel in ['stdout', 'stderr']:
                data = (file.parent / ('%03d.%s' % (index, channel))).read_bytes()
                require(len(data) == row[channel]['size'] and sha(data) == row[channel]['sha256'], 'Actual nested full stream byte pin missing')
    return capture, before, result, collector


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--comparison-plan', required=True)
    parser.add_argument('--root-reviewed-plan-sha256', required=True)
    args = parser.parse_args()
    require(args.execute, 'Future root explicit execution only')
    plan_file = path(args.comparison_plan)
    require(sha(plan_file.read_bytes()) == args.root_reviewed_plan_sha256 and re.fullmatch(r'[0-9a-f]{64}', args.root_reviewed_plan_sha256), 'Exact root-reviewed full comparison plan pin required')
    plan = load(plan_file)
    require(plan['schema'] == 'pr37-root-reviewed-complete-comparison-plan/v1' and plan['root_reviewed'] is True and plan['pr'] == 37 and plan['problem_id'] == 3009 and plan['mandatory_corrections'] == [], 'Draft/unreviewed/corrected plan cannot establish a final gate')
    require(plan.get('unhandled_differences') == [], 'Every nonmetadata/structural/raw comparison gap must be resolved before sealing')
    require(plan['entire_current_packet_source_first_review_checked_by_root'] is True and plan['source_first_review'] == {'report': pin(W / 'REPORT.md'), 'summary': pin(W / 'SUMMARY.json'), 'current_manifest_sha256': CURRENT, 'current_dependencies_sha256': DEPS}, 'Independent root inspection of exact final whole source-first report/summary required')
    summary = load(W / 'SUMMARY.json')
    require(summary['mandatory_candidate_repairs'] == [] and summary['current_manifest_sha256'] == CURRENT and summary['current_dependency_sha256'] == DEPS and summary['full_resolution_completion_estimate_percent'] == 0, 'Whole source-first scope/corrections changed')
    capture, before, result, collector = verify_capture()
    require(plan['actual_capture'] == pin(CAP / 'ACTUAL_OUTER_CAPTURE.json'), 'Reviewed plan must bind positive actual capture')
    require(not SUP.exists() and not (A / 'ROOT_FINAL_WHOLE_ACTUAL_REPRODUCTION.json').exists() and not (A / 'ROOT_FINAL_WHOLE_SCOPE_CONTRACT.json').exists(), 'Final support/receipts must be fresh')
    expected_manifest = load(W / 'FIRST_PARTY_MANIFEST.json')
    require(sha((W / 'FIRST_PARTY_MANIFEST.json').read_bytes()) == WHOLE, 'Final whole closed manifest changed')
    expected_members = {str((W / z['path']).relative_to(R)): {'path': str((W / z['path']).relative_to(R)), 'bytes': z['bytes'], 'sha256': z['sha256']} for z in expected_manifest['files']}
    for root, advertised in [(C, load(C / 'MANIFEST.json')['files']), (A, load(C / 'CURRENT_PROOF_DEPENDENCIES.json')['files'])]:
        for row in advertised:
            name = str((root / row['path']).relative_to(R))
            expected_members[name] = {'path': name, 'bytes': row['bytes'], 'sha256': row['sha256']}
    pairs = plan['comparisons']
    require(pairs and len({z['label'] for z in pairs}) == len(pairs), 'Nonempty unique full comparison specifications required')
    coverage = plan['required_comparison_coverage']
    require(set(coverage) == GROUPS and all(labels and set(labels) <= {z['label'] for z in pairs} for labels in coverage.values()), 'Full31/8462/three-family/whole positive+mutant coverage required')
    SUP.mkdir()
    comparisons, ledger = [], []
    for index, pair in enumerate(pairs):
        actual, expected = bound(pair['actual']), bound(pair['expected'])
        require(path(pair['actual']['path']).resolve().is_relative_to(OUT.resolve()), 'Actual complete comparison must be retained fresh replay output')
        require(expected_members.get(pair['expected']['path']) == pair['expected'], 'Expected output must be exact closed first-party/current/dependency member')
        require(pair['actual']['path'] != pair['expected']['path'], 'No tautological same-file comparison')
        record = {'label': pair['label'], 'raw_actual': pair['actual'], 'raw_expected': pair['expected'], 'raw_BYTE_equal': actual == expected, 'normalization_operations': pair['normalizations'], 'qualification': pair['qualification']}
        kind = pair['kind']
        if kind == 'byte_exact':
            require(not pair['normalizations'] and actual == expected, 'Raw BYTE equality may not normalize clocks/paths')
            output_actual, output_expected, output_kind = actual, expected, 'byte_exact'
        elif kind == 'full_parsed_json':
            left, right = json.loads(actual), json.loads(expected)
            record['raw_full_JSON_equal'] = same_typed(left, right)
            normalized_left, normalized_right = normalize_json(left, right, pair['normalizations'])
            output_actual, output_expected, output_kind = encode(normalized_left), encode(normalized_right), 'full_parsed_json'
        elif kind == 'full_text_exact_after_literal_path_transport':
            left, right = actual.decode(), expected.decode()
            for operation in pair['normalizations']:
                require(set(operation) == {'actual_before', 'expected_before', 'canonical_value', 'qualification'}, 'Exact literal transport schema')
                old_left, old_right = operation['actual_before'], operation['expected_before']
                require(old_left and old_right and old_left in left and old_right in right and operation['qualification'], 'Literal path transport preimage missing')
                require(old_left.startswith(str(OUT)) and old_right.startswith(str(W / 'replay_v7')), 'Text normalization limited to exact recorded private output prefixes')
                left = left.replace(old_left, operation['canonical_value'])
                right = right.replace(old_right, operation['canonical_value'])
            require(left == right, 'Complete transported text differs')
            output_actual, output_expected, output_kind = left.encode(), right.encode(), 'byte_exact'
            record['normalized_BYTE_equal_only'] = True
        else:
            raise ValueError('Projection or unsupported comparison forbidden')
        actual_file = SUP / ('%03d.actual.full' % index)
        expected_file = SUP / ('%03d.expected.full' % index)
        save(actual_file, output_actual); save(expected_file, output_expected)
        comparisons.append({'label': pair['label'], 'actual': pin(actual_file), 'expected': pin(expected_file), 'kind': output_kind})
        ledger.append(record)
    limitation = {'private_builder_raw_generated_packet_retained': False, 'meaning': 'Unchanged closed replay internally checked all96 and complete JSON under recorded UTC/path-only substitutions, then deleted its private packet. Full retained BUILDER_FULL_DIFF.json, executed_private_builder.py, full stdout and RESULT are preserved and compared; deleted raw packet bytes are not reconstructed or asserted retained.'}
    save(SUP / 'NORMALIZATION_LEDGER.json', encode({'schema': 'pr37-full-object-explicit-normalization/v1', 'root_reviewed_plan': pin(plan_file), 'comparisons': ledger, 'no_projection': True, 'raw_dated_BYTE_equality_not_claimed': True, 'builder_retention_limitation': limitation}))
    save(SUP / 'ROOT_REVIEWED_COMPARISON_PLAN.json', plan_file.read_bytes())
    wrapper = capture['wrapper']
    executions = [{'label': capture['label'], 'actual_execution': True, 'returncode': 0, 'argv': capture['argv'], 'started_at_utc': capture['started_at_utc'], 'finished_at_utc': capture['finished_at_utc'], 'wrapper': wrapper, 'stdout': capture['stdout'], 'stderr': capture['stderr'], 'receipt': pin(CAP / 'ACTUAL_OUTER_CAPTURE.json'), 'parsed_receipt': capture}]
    for row in collector['actual_outer_program_runs']:
        execution = {'label': 'fresh_closed_collector/' + row['label'], 'actual_execution': True, 'returncode': row['returncode'], 'argv': row['argv'], 'started_at_utc': row['started_utc'], 'finished_at_utc': collector['finished_utc'], 'wrapper': wrapper,
                     'finished_at_utc_qualification': 'Observed collector completion upper bound; individual child finish timestamp was not recorded.',
                     'stdout': pin(OUT / 'support/complete_closed_collector_streams' / Path(row['stdout']['path']).relative_to('new_actual_collector_support')),
                     'stderr': pin(OUT / 'support/complete_closed_collector_streams' / Path(row['stderr']['path']).relative_to('new_actual_collector_support')), 'receipt': pin(OUT / 'support/NEW_ACTUAL_COLLECTOR.json'), 'parsed_receipt': collector}
        executions.append(execution)
    rows = complete_inventory(OUT) + complete_inventory(CAP) + complete_inventory(SUP) + [wrapper, pin(W / 'replay_gate.py'), pin(__file__)]
    # Include every exact original first-party executed source carried by the
    # dependency closure, in addition to retained executed transport revisions.
    rows += [pin(A / z['path']) for z in before['dependencies'] if z['path'].endswith('.py')]
    by_name = {}
    for row in rows:
        require(row['path'] not in by_name or by_name[row['path']] == row, 'Conflicting root evidence pin')
        by_name[row['path']] = row
    replay_bindings = [by_name[name] for name in sorted(by_name)]
    binding_snapshots = {key: before[key] for key in ['reviewed_candidate', 'dependencies', 'whole_authored_members']}
    receipt = {'schema': 'pr37-actual-final-whole-reproduction/v1', 'status': 'PASS', 'pr': 37, 'problem_id': 3009, 'original_head': '84bb43d21b36e4d97229806e2518fbc135bee786', 'reviewed_candidate_manifest_sha256': CURRENT, 'current_proof_dependencies_sha256': DEPS, 'whole_manifest_sha256': WHOLE,
               'entire_current_packet_checked': True, 'root_actual_reproduction': True, 'mandatory_corrections': [], 'queue_status': 'unsolved', 'full_problem_solved': False, 'positive_novelty_claim': False, 'original_substantive_attempts': 1, 'new_substantive_attempts': 0, 'verification_attempts_added': 0, 'paper_or_new_doi_or_tracker': False,
               'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'root_replay_bindings': replay_bindings, 'root_wrapper': wrapper, 'bindings_before': binding_snapshots, 'bindings_after': copy.deepcopy(binding_snapshots), 'whole_manifest_self_before_and_after': before['whole_manifest_self'],
               'actual_outer_executions': executions, 'structured_comparisons': comparisons, 'comparison_coverage': coverage, 'builder_retention_limitation': limitation, 'raw_actual_capture': pin(CAP / 'ACTUAL_OUTER_CAPTURE.json'), 'normalization_ledger': pin(SUP / 'NORMALIZATION_LEDGER.json'), 'sealed_at_utc': stamp()}
    foreign = []
    for file in sorted((W / 'primary').rglob('*')):
        require(not file.is_symlink(), 'Foreign primary symlink forbidden')
        if file.is_file():
            raw_pin = pin(file)
            foreign.append({'path': str(file.relative_to(W)), 'bytes': raw_pin['bytes'], 'sha256': raw_pin['sha256']})
    sources = [z for z in expected_manifest['files'] if z['path'] in {'SOURCE_AND_READ_COVERAGE.json', 'INITIAL_SOURCE_ACQUISITION_TOOL_BODY.txt', 'fetch_primary_supplement.py'} or z['path'].startswith('receipts/')]
    scope = {'schema': 'pr37-root-reviewed-final-whole-scope/v1', 'pr': 37, 'problem_id': 3009, 'whole_manifest_sha256': WHOLE, 'root_final_receipt_sha256': sha(encode(receipt)), 'authored_members': expected_manifest['files'], 'scratch_components_excluded': ['__pycache__'], 'malformed_json_exceptions': [],
             'foreign_excluded_prefixes': ['primary/'], 'foreign_members': foreign, 'foreign_inventory_sources': sources, 'root_replay_bindings': replay_bindings, 'root_wrapper': wrapper, 'required_outer_execution_labels': [z['label'] for z in executions], 'actual_outer_execution_specs': executions,
             'required_comparison_labels': [z['label'] for z in comparisons], 'structured_comparison_specs': comparisons, 'required_comparison_coverage': coverage, 'root_reviewed_raw_plan': pin(plan_file), 'normalization_ledger': pin(SUP / 'NORMALIZATION_LEDGER.json'), 'builder_retention_limitation': limitation}
    # Recheck all recorded live bytes immediately before producing gate files.
    verify_capture()
    for row in replay_bindings:
        bound(row)
    save(A / 'ROOT_FINAL_WHOLE_ACTUAL_REPRODUCTION.json', encode(receipt))
    save(A / 'ROOT_FINAL_WHOLE_SCOPE_CONTRACT.json', encode(scope))
    print(json.dumps({'status': 'SEALED_FROM_ACTUAL_CAPTURE_AND_ROOT_REVIEW', 'actual_receipt': pin(A / 'ROOT_FINAL_WHOLE_ACTUAL_REPRODUCTION.json'), 'scope_contract': pin(A / 'ROOT_FINAL_WHOLE_SCOPE_CONTRACT.json'), 'raw_replay_members': len(replay_bindings), 'complete_comparisons': len(comparisons), 'actual_outer_execution_records': len(executions)}))


if __name__ == '__main__':
    main()
