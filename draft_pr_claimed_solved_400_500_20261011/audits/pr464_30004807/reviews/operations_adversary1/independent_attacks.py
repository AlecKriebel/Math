#!/usr/bin/env python3
"""Offline independent adversary probes; fabricated data remain private.

The preparer's Fixture is reused solely as a synthetic filesystem constructor.
The attacks, asserted expectations, mock services, and classifications below
are independently written. No real service or subprocess is dispatched.
"""
import base64
import copy
import hashlib
import importlib.util
import json
import socket
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
OPERATIONS = AUDIT / 'operations'
sys.path.insert(0, str(OPERATIONS))
import common as c
import check_operations as preparer
import integrate_pr464_publication as integration
import register_pr464_tracker as tracker
import zenodo_pr464 as zenodo
spec = importlib.util.spec_from_file_location('reviewed_builder', AUDIT / 'build_preprint_package.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
RESULTS = []
REAL_CALLS = []


def deny(*args, **kwargs):
    REAL_CALLS.append('blocked unexpected service')
    raise RuntimeError('Offline isolation rejected an unmocked service')


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(c.json_bytes(value) if isinstance(value, dict) else value)


def observe(fn):
    try:
        value = fn()
    except RuntimeError as error:
        return False, str(error)
    return True, value


def record(name, expected, observed, detail=''):
    RESULTS.append({'case': name, 'expected': expected, 'observed': observed,
                    'expectation_met': expected == observed, 'detail': detail,
                    'real_external_calls': 0})


def isolated(name, fn):
    private = HERE / 'private_cases'
    private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=name + '_', dir=private) as directory:
        f = preparer.Fixture(Path(directory))
        with patch.multiple(c, AUDIT=f.audit, PACKAGE=f.package, REPOSITORY=f.repo), \
             patch.object(c, 'github', deny), patch.object(c, 'gws', deny), \
             patch.object(c.subprocess, 'run', side_effect=deny), \
             patch.object(socket, 'socket', side_effect=deny):
            fn(f)


def bind_freeze(f):
    freeze = json.loads((f.audit / f.manifest_name).read_text())
    freeze.update(pr=c.PR, problem=c.PROBLEM, original_head=c.ORIGINAL,
                  source_receipt_sha256=f.gate['source_receipt_sha256'],
                  mathematical_acceptance_gate_sha256=f.gate['mathematical_acceptance_gate_sha256'],
                  branch_install_plan_sha256=f.gate['branch_install_plan_sha256'],
                  archive_contains_explicit_payload_manifest=True,
                  publication_not_yet_authorized_by_review_gate=True)
    write(f.audit / f.manifest_name, freeze)
    f.gate['review_input_manifest_sha256'] = c.sha((f.audit / f.manifest_name).read_bytes())
    for item in f.gate['complete_package_reviews']:
        item['input_manifest_sha256'] = f.gate['review_input_manifest_sha256']
    f.save_gate()


def freeze_attack(kind):
    def probe(f):
        bind_freeze(f)
        baseline, _ = observe(c.validate_gate)
        c.require(baseline, 'Synthetic fully bound baseline rejected')
        if kind in {'source_receipt', 'mathematical_acceptance_gate', 'branch_install_plan'}:
            filename = {'source_receipt': 'SOURCE_RECEIPT.json',
                        'mathematical_acceptance_gate': 'MATHEMATICAL_ACCEPTANCE_GATE.json',
                        'branch_install_plan': 'BRANCH_INSTALL_PLAN.json'}[kind]
            path = f.audit / filename
            obj = json.loads(path.read_text())
            obj['new_unreviewed_annotation'] = 'changed after the two accepted reviews'
            write(path, obj)
            f.gate[kind + '_sha256'] = c.sha(path.read_bytes())
            f.save_gate()
        else:
            freeze = json.loads((f.audit / f.manifest_name).read_text())
            freeze[kind] = {'pr': 466, 'problem': '30000999', 'original_head': 'f' * 40}[kind]
            write(f.audit / f.manifest_name, freeze)
            f.gate['review_input_manifest_sha256'] = c.sha((f.audit / f.manifest_name).read_bytes())
            for item in f.gate['complete_package_reviews']:
                item['input_manifest_sha256'] = f.gate['review_input_manifest_sha256']
            f.save_gate()
        accepted, detail = observe(c.validate_gate)
        record('freeze_' + kind + '_cross_binding', 'rejected', 'accepted' if accepted else 'rejected',
               'Reviewed freeze and current gate disagree; acceptance reproduced.' if accepted else detail)
    isolated('freeze_' + kind, probe)


def removed_registration(kind):
    def probe(f):
        ctx, pub = f.publication()
        values = c.tracker_values(ctx['metadata'], pub['doi_url'])
        rows = [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']]
        state = {'writes': 0}
        operation = {'state': 'verified_registration', 'doi': pub['doi_url'], 'values': values,
                     'updated_range': "'Math Puzzles'!A2:D2"}
        if kind == 'uncertain':
            operation['state'] = 'outcome_unconfirmed'
        if kind != 'receipt_only':
            write(f.audit / 'TRACKER_APPEND_OPERATION.json', operation)
        if kind in {'verified', 'receipt_only'}:
            write(f.audit / 'TRACKER_APPEND_RECEIPT.json', {'verified': True,
                  'spreadsheet_id': c.SHEET, 'sheet_id': c.TAB_ID, 'tab': c.TAB,
                  'values': values, 'doi': pub['doi_url'], 'updated_range': "'Math Puzzles'!A2:D2",
                  'unique_doi_row_at_final_snapshot': True})
        def read(range_name):
            return {'values': copy.deepcopy(rows if range_name.endswith('A:D') else rows[1:2])}
        def append(action, params, body):
            c.require(action == 'append' and body['values'] == values, 'Unexpected mock operation')
            state['writes'] += 1
            rows.append(values[0].copy())
            return {'updates': {'updatedRows': 1, 'updatedColumns': 4, 'updatedCells': 4,
                                'updatedRange': "'Math Puzzles'!A2:D2"}}
        with patch.multiple(tracker, AUDIT=f.audit, validate_gate=lambda: ctx,
                            confirm_live_publication=lambda unused: pub, live_eligibility=lambda: None,
                            check_sheet=lambda: None, sheet_get=read, gws=append):
            accepted, detail = observe(lambda: tracker.run(True))
        record('tracker_removed_row_' + kind, 'zero_appends',
               'zero_appends' if state['writes'] == 0 else 'one_repeated_append',
               ('Mock append count: ' + str(state['writes']) + '; run accepted: ' + str(accepted)))
    isolated('tracker_removed_' + kind, probe)


def main_conflict(kind):
    def probe(f):
        ctx, pub = f.publication()
        write(f.audit / 'TRACKER_APPEND_RECEIPT.json', {'verified': True,
              'spreadsheet_id': c.SHEET, 'sheet_id': c.TAB_ID, 'tab': c.TAB,
              'values': c.tracker_values(ctx['metadata'], pub['doi_url']),
              'doi': pub['doi_url'], 'updated_range': "'Math Puzzles'!A2:D2",
              'unique_doi_row_at_final_snapshot': True})
        queue = (preparer.HEADER + f.receipt['selected_queue_row'] + '\n').encode()
        lines, index, cells, columns = c.queue_row(queue)
        cells[columns.index('Status')] = ' queued '
        cells[columns.index('Turns')] = ' 0/5 '
        lines[index] = '|' + '|'.join(cells) + '|\n'
        original = {x['path']: (f.audit / 'source_snapshot' / x['path']).read_bytes()
                    for x in f.receipt['files']}
        main_sha = 'a' * 40
        path = {'receipt': c.PREPRINT + 'publication_receipts/SOURCE_RECEIPT.json',
                'manifest': c.PREFIX + 'PUBLICATION_MANIFEST.json',
                'installed_paper': c.PREPRINT + 'manuscript.pdf',
                'historical': c.PREFIX + 'release/PROOF.md'}[kind]
        unrelated = b'An existing different current-main resource; preserve or reject.\n'
        main_files = {c.QUEUE: ''.join(lines).encode(), path: unrelated,
                      'unrelated_control.txt': b'unrelated control\n'}
        class Reader:
            def commit(self, revision):
                c.require(revision == main_sha, 'Wrong mock commit')
                return {'sha': main_sha, 'tree': {'sha': 'b' * 40}}
            def entry(self, name, revision):
                data = main_files.get(name)
                return None if data is None else {'type': 'blob', 'mode': '100644', 'sha': c.git_sha(data)}
            def read(self, name, revision):
                return main_files[name]
        def git_read(endpoint):
            c.require(endpoint == 'git/ref/heads/main', 'Unexpected mock Git read')
            return {'object': {'sha': main_sha}}
        with patch.object(c, 'confirm_live_publication', lambda unused: pub), \
             patch.object(c, 'confirm_live_tracker', lambda unused, unused_pub: None), \
             patch.object(c, 'live_eligibility', lambda: ({'head': {'ref': c.BRANCH}}, queue, Reader())), \
             patch.object(c, 'github', git_read):
            accepted, result = observe(integration.prepare)
        overwritten = accepted and result[1].get(path) != unrelated
        record('current_main_conflict_' + kind, 'rejected',
               'accepted_overwrite' if overwritten else 'rejected',
               'Different existing target would enter the install tree.' if overwritten else str(result))
    isolated('main_conflict_' + kind, probe)


def builder_exclusion(kind):
    def probe(f):
        path = {'venv': 'venv/environment.txt', 'dot_venv': '.venv/environment.txt',
                'private_sources': 'private_sources/environment.txt',
                'noncanonical': 'notes/./same.txt'}[kind]
        write(f.package / path, b'OFFLINE fabricated content; no secrets\n')
        with patch.object(builder, 'PACKAGE', f.package):
            accepted, detail = observe(lambda: builder.selected_path(path))
        record('builder_selected_path_' + kind, 'rejected', 'accepted' if accepted else 'rejected',
               'A manually selected private environment/noncanonical payload is accepted.' if accepted else detail)
    isolated('builder_' + kind, probe)


def normal_rejections():
    for value in [None, False, True, '0', 0.0, -1, 1]:
        ok, detail = observe(lambda value=value: c.zero_count(value, 'independent_zero'))
        record('integer_zero_' + type(value).__name__ + '_' + str(value), 'rejected',
               'accepted' if ok else 'rejected', str(detail))
    ok, _ = observe(lambda: c.zero_count(0, 'independent_zero'))
    record('integer_zero_real_zero', 'accepted', 'accepted' if ok else 'rejected')
    for value in ['../outside', '/absolute', 'a//b', 'a/./b', 'a/../b', 'a\\b',
                  'private_cases/f.json', '.zenodo-state/file', '.secrets/file',
                  'venv/site_packages.py', '.venv/site_packages.py', '__pycache__/x.pyc']:
        ok, detail = observe(lambda value=value: c.relative(value))
        record('common_relative_' + value, 'rejected', 'accepted' if ok else 'rejected', str(detail))


def actual_missing_gate():
    c.require(not (AUDIT / 'FINAL_ACCEPTANCE_GATE.json').exists(),
              'Actual acceptance gate now exists; inspect before continuing')
    actions = {'gate': c.validate_gate, 'zenodo_stage': lambda: zenodo.run('stage', True),
               'zenodo_publish': lambda: zenodo.run('publish', True, 123456),
               'tracker': lambda: tracker.run(True), 'integration': lambda: integration.run(True)}
    with patch.object(c, 'github', deny), patch.object(c, 'gws', deny), \
         patch.object(c.subprocess, 'run', side_effect=deny), patch.object(socket, 'socket', side_effect=deny):
        for name, fn in actions.items():
            ok, detail = observe(fn)
            record('actual_missing_gate_' + name, 'rejected_before_service',
                   'accepted' if ok else 'rejected_before_service', str(detail))


def main():
    actual_missing_gate()
    normal_rejections()
    for kind in ('source_receipt', 'mathematical_acceptance_gate', 'branch_install_plan', 'pr', 'problem', 'original_head'):
        freeze_attack(kind)
    for kind in ('verified', 'uncertain', 'receipt_only'):
        removed_registration(kind)
    for kind in ('receipt', 'manifest', 'installed_paper', 'historical'):
        main_conflict(kind)
    for kind in ('venv', 'dot_venv', 'private_sources', 'noncanonical'):
        builder_exclusion(kind)
    c.require(not REAL_CALLS, 'Unexpected real service escape was attempted')
    outcome = {'scope': 'Independent offline adversary; private fabricated inputs never become production evidence.',
               'probe_count': len(RESULTS), 'all_probes_executed': True,
               'expectation_met_count': sum(x['expectation_met'] for x in RESULTS),
               'unsafe_behavior_reproduction_count': sum(not x['expectation_met'] for x in RESULTS),
               'real_external_calls': 0, 'cases': RESULTS,
               'limit': 'Finite controls and source reading; no formal operational or concurrency guarantee.'}
    suffix = 'NORMAL' if __debug__ else 'OPTIMIZED'
    (HERE / ('INDEPENDENT_ATTACKS_' + suffix + '.json')).write_bytes(c.json_bytes(outcome))
    print(json.dumps({k: v for k, v in outcome.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
