#!/usr/bin/env python3
"""Root readback of the genuine fresh review; no API or Git mutations."""
import ast
import base64
import datetime
import hashlib
import json
from pathlib import Path

PROGRAM = Path(__file__).resolve().parent
CASE = PROGRAM / 'audits/pr458_20000693'
OWN = CASE / 'reviews/disposition_adversary2'
HEAD = '87a39f7b4e5ef81aacf98464f86586cc95684d7f'
REVIEWER = '/root/pr458_disposition_adversary2'
HELPER = '4f4551dade92520d049cfb385eb2eca5001fc0c16fc4510decc7176e98138303'
SYNTHESIS = 'a04186e6fd5178048edd6ec4892cebb53a1a17e7ed23d48cf6a98cab81c3eb37'


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def bind(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def read(path):
    return json.loads(path.read_text())


def check_record(base, record):
    need(type(record) is dict and type(record['bytes']) is int
         and record['bytes'] > 0, 'Typed positive record')
    relative = record['path']
    need(type(relative) is str and Path(relative).as_posix() == relative
         and not Path(relative).is_absolute() and '..' not in Path(relative).parts
         and not {'private', 'private_sources', 'private_cases', 'mutation_fixtures',
                  '__pycache__', '.venv', 'venv'}.intersection(Path(relative).parts),
         'Positive public path')
    path = base / relative
    need(path.resolve() == path and path.is_file() and path.stat().st_nlink == 1,
         'Positive topology')
    need(bind(path) == {k: record[k] for k in ('bytes', 'sha256')}, 'Record byte binding')
    return {'path': str(path.relative_to(CASE)), **bind(path)}


def main():
    manifest = read(OWN / 'PUBLIC_FILES.json')
    payloads = [check_record(OWN, item) for item in manifest['files']]
    names = [item['path'] for item in manifest['files']]
    need(len(names) == len(set(names)) and {'REPORT.md', 'RESULT.json'} <= set(names),
         'Complete genuine positive packet')
    for name in names:
        if Path(name).suffix == '.json':
            read(OWN / name)
    inputs = read(OWN / 'INPUT_BINDINGS.json')
    need(len(inputs['evidence']) == 187 and len(inputs['positive_payloads']) == 100
         and inputs['actual_action_gate_exists'] is False and inputs['draft_approval'] is False,
         'Complete independent input metadata')
    for item in inputs['evidence']:
        check_record(CASE, item)
    for item in inputs['positive_payloads']:
        check_record(CASE / 'reviews' / item['family'], item)
    inspection = read(OWN / 'SOURCE_INSPECTION.json')
    primary_names = ('source_heap.pdf', 'source_sahay.pdf', 'source_ks.pdf',
                     'source_mtb.pdf', 'source_sahay_v3.pdf')
    need(len(inspection['sources']) == len(primary_names) == 5
         and inspection['complete_primary_PDF_pages_visually_inspected'] == 15,
         'Exact primary inspection metadata')
    for name, item in zip(primary_names, inspection['sources']):
        need(bind(OWN / 'private' / name) == {k: item[k] for k in ('bytes', 'sha256')},
             'Private primary source bytes')
    need(bind(OWN / 'private/aim.html') == {
        k: inspection['direct_AIM_HTTP'][k] for k in ('bytes', 'sha256')},
        'Direct primary problem bytes')
    need(bind(PROGRAM / 'repair_pr458_status.py')['sha256'] == HELPER
         and bind(OWN / 'REVIEWED_HELPER.py')['sha256'] == HELPER
         and bind(CASE / 'DISPOSITION_SYNTHESIS.md')['sha256'] == SYNTHESIS
         and bind(OWN / 'REVIEWED_SYNTHESIS.md')['sha256'] == SYNTHESIS, 'Current exact inputs')
    result = read(OWN / 'RESULT.json')
    need(type(result['pr']) is int and result['pr'] == 458
         and result['problem_id'] == '20000693' and result['frozen_head'] == HEAD
         and result['reviewer'] == REVIEWER, 'Genuine review identity')
    for key in ('blocking_findings', 'required_repairs', 'unresolved_disposition_issues'):
        need(type(result[key]) is int and result[key] == 0, 'Actual clean result ' + key)
    need(result['operations_approved'] is True and result['current_helper_accepted'] is True
         and result['publication_accepted'] is False
         and result['status_recommendation'] == 'already_solved'
         and result['acceptance_scope'] == 'one_row_priority_correction_then_immediate_skip'
         and result['reviewed_helper_sha256'] == HELPER
         and result['reviewed_synthesis_sha256'] == SYNTHESIS, 'Narrow genuine acceptance')
    draft = read(CASE / 'DRAFT_OPERATIONS_GATE.json')
    need(draft['operations_approval'] is False and draft['not_an_action_gate'] is True
         and draft['missing_actual_final_operations_review'] is True
         and len(draft['reviews']) == 8 and len(draft['reviewed_files']) == 187,
         'Draft remained unapproved during fresh review')
    for item in draft['reviewed_files']:
        check_record(CASE, item)
    foundation = read(CASE / 'FROZEN_FOUNDATION_BINDINGS.json')
    need(bind(CASE / 'FROZEN_FOUNDATION_BINDINGS.json')['sha256'] ==
         '84281ba210adf18cf431cc4ec9ede8e32873f680852e48ef5e7ef601ca4b0303'
         and len(foundation['files']) == 158, 'Genuine frozen foundation')
    for item in foundation['files']:
        check_record(CASE, item)
    source = read(CASE / 'SOURCE_RECEIPT.json')
    need(len(source['files']) == 27, 'Frozen original count')
    for item in source['files']:
        check_record(CASE / 'source_snapshot', item)
    first = read(OWN / 'FIRST_CONTROLS.json')
    supplement = read(OWN / 'SUPPLEMENT_CONTROLS.json')
    need(len(first['runs']) == 306 and len(supplement['runs']) == 64,
         'Actual main and supplemental execution counts')
    all_rows = first['runs'] + supplement['runs']
    modes = {mode: {row['case']: row for row in all_rows if row['mode'] == mode}
             for mode in ('normal', 'optimized')}
    need(len(all_rows) == 370 and len(modes['normal']) == len(modes['optimized']) == 185
         and modes['normal'].keys() == modes['optimized'].keys(), 'Complete independent matrix')
    summary = {}
    positive = []
    for mode, rows in modes.items():
        summary[mode] = {outcome: sum(row['outcome'] == outcome for row in rows.values())
                         for outcome in ('positive_pass', 'intended_rejection',
                                         'unexpected_acceptance', 'wrong_guard_or_harness_failure')}
        need(summary[mode] == {'positive_pass': 6, 'intended_rejection': 179,
                              'unexpected_acceptance': 0, 'wrong_guard_or_harness_failure': 0},
             'Actual matrix outcomes')
    for name, normal in modes['normal'].items():
        optimized = modes['optimized'][name]
        for key in ('outcome', 'returncode', 'API_calls', 'git_writes', 'PATCH_count',
                    'ref_moved', 'operation_marker_exists', 'receipt_exists', 'last_error'):
            need(normal[key] == optimized[key], 'Mode semantics ' + name + ' ' + key)
    for packet, directory in ((first, 'first'), (supplement, 'supplement')):
        for row in packet['runs']:
            need(type(row['index']) is int and row['index'] >= 0, 'Actual case index')
            private = OWN / 'private' / directory / (row['mode'] + '_' + str(row['index']))
            need(read(private / 'RECORD.json') == row, 'Retained exact record')
            for stream in ('stdout', 'stderr'):
                need(bind(private / stream) == row[stream], 'Retained raw output digest')
            model = read(private / 'MODEL.json')
            requests = model['requests']
            writes = [request for request in requests if request['method'] != 'GET']
            patches = [request for request in requests if request['method'] == 'PATCH']
            need(len(requests) == row['API_calls'] and len(writes) == row['git_writes']
                 and len(patches) == row['PATCH_count'] and len(patches) <= 1,
                 'Independent actual dispatch count')
            if row['case'] != 'helper_drift':
                need(bind(private / 'program/repair_pr458_status.py')['sha256'] == HELPER,
                     'Actual executed current helper bytes')
            if row['outcome'] == 'intended_rejection':
                need(row['returncode'] != 0 and row['expected_guard'] in
                     (private / 'stderr').read_text(), 'Actual intended negative diagnostic')
            else:
                need(row['returncode'] == 0, 'Positive actual subprocess')
                preflight = read(private / 'program/audits/pr458_20000693/STATUS_REPAIR_PREFLIGHT.json')
                old = preflight['selected_old_row'].split('|')
                new = preflight['selected_new_row'].split('|')
                need([i for i, pair in enumerate(zip(old, new)) if pair[0] != pair[1]] == [8, 11]
                     and old[9] == new[9] and new[9].strip() == '1/5'
                     and old[12] == new[12] and new[12].strip() == '',
                     'Actual positive selected cells, Turns and DOI')
                if row['case'] == 'preflight':
                    need(not writes, 'Actual preflight is read-only')
                else:
                    need(patches == [{'endpoint': 'git/refs/heads/dot%2Fmath-20000693',
                                      'method': 'PATCH', 'payload': {'sha': 'c' * 40, 'force': False}}],
                         'Actual single nonforced PATCH')
                    need(model['new_commit']['parents'] == [HEAD]
                         and model['new_tree'] == {'base_tree': 'a' * 40, 'tree': [{
                             'path': 'unsolved_math_prioritization/QUEUE.md', 'mode': '100644',
                             'type': 'blob', 'sha': model['new_blob']}]}, 'Original parent, one QUEUE path')
                    before = base64.b64decode(model['blobs'][model['original_blob']]).splitlines(keepends=True)
                    after = base64.b64decode(model['blobs'][model['new_blob']]).splitlines(keepends=True)
                    need(len(before) == len(after)
                         and sum(a != b for a, b in zip(before, after)) == 1,
                         'Every other QUEUE row and header preserved')
                positive.append({'case': row['case'], 'mode': row['mode'],
                                 'DOI12_blank_preserved': True, 'Turns9_1_5_preserved': True,
                                 'only_Status8_Findings11_changed': True})
    need(len(positive) == 12 and len(first['repeats']) == 18 and not supplement['repeats'],
         'Actual positive and second-invocation counts')
    for repeat in first['repeats']:
        row = modes[repeat['mode']][repeat['case']]
        private = OWN / 'private/first' / (repeat['mode'] + '_' + str(row['index']))
        need(repeat['returncode'] != 0 and repeat['API_calls_added'] == repeat['PATCH_calls_added'] == 0
             and bind(private / 'repeat_stderr') == repeat['stderr']
             and 'Prior operation: no repeated mutation' in (private / 'repeat_stderr').read_text(),
             'Actual second invocation rejects before dispatch')
    for status in ('already_solved', 'unsolved', 'solved', 'out_of_scope', 'in_progress', 'pending', 'unknown'):
        for mode in modes:
            row = modes[mode]['excluded|' + status]
            need(row['git_writes'] == 0 and row['last_error'] ==
                 'RuntimeError: Excluded status: stop without processing', 'Excluded before math gate')
    need((OWN / 'MATH_NORMAL.json').read_bytes() == (OWN / 'MATH_OPTIMIZED.json').read_bytes(),
         'Exact finite controls mode agreement')
    for name in ('audit_evidence.py', 'mock_github.py', 'run_controls.py', 'run_supplement.py',
                 'seal_checks.py', 'verify_disposition_math.py', 'REVIEWED_HELPER.py'):
        need(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse((OWN / name).read_text()))),
             'Explicit non-assert controls')
    need(not (CASE / 'PRIORITY_DISPOSITION_GATE.json').exists(), 'Review precedes genuine action gate')
    output = {'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'pr': 458, 'problem_id': '20000693', 'frozen_head': HEAD, 'reviewer': REVIEWER,
              'root_read_entire_final_report_result_and_controlling_sources': True,
              'root_computationally_parsed_every_matrix_record': 370,
              'raw_stdout_stderr_digests_independently_checked': 740,
              'actual_second_invocations_checked': 18, 'total_helper_executions': 388,
              'matrix_outcomes': summary, 'mode_effects_equal': True,
              'positive_selected_cell_readbacks': positive,
              'original_source_files_unchanged': 27, 'fixed_foundation_files_unchanged': 158,
              'unapproved_draft_evidence_checked': 187, 'safe_payloads': payloads,
              'every_safe_JSON_payload_fully_parsed': True,
              'independent_input_positive_records_checked': 100,
              'private_primary_PDF_byte_bindings_checked': 5,
              'direct_primary_problem_byte_binding_checked': True,
              'positive_manifest': {'path': 'reviews/disposition_adversary2/PUBLIC_FILES.json',
                                    **bind(OWN / 'PUBLIC_FILES.json')},
              'reviewed_helper_sha256': HELPER, 'reviewed_synthesis_sha256': SYNTHESIS,
              'raw_counts': {key: result[key] for key in ('blocking_findings', 'required_repairs',
                                                        'unresolved_disposition_issues')},
              'operations_approved': True, 'current_helper_accepted': True,
              'publication_accepted': False, 'acceptance_scope': result['acceptance_scope'],
              'status_recommendation': result['status_recommendation'],
              'failed_first_review_retained_as_failed': True,
              'root_created_action_gate_or_performed_mutation_during_readback': False}
    (CASE / 'DISPOSITION_ADVERSARY2_FAMILY_READBACK.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: output[key] for key in ('at_utc', 'raw_counts', 'operations_approved',
                                                'total_helper_executions', 'matrix_outcomes')}, indent=2))


if __name__ == '__main__':
    main()
