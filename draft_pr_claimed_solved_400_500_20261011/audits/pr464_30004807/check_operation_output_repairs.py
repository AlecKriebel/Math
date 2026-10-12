#!/usr/bin/env python3
"""Root output regressions plus unmodified sealed ops3 replay; no independent acceptance."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
ATTACKS = ROOT / 'reviews/operations_adversary3/independent_controls.py'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def unsafe_runner(m, f, runner, name, kind):
    path = f.audit / name
    path.unlink(missing_ok=True)
    sentinel = f.repo / 'unrelated_output_target.bin'
    initial = m.c.json_bytes({'state': 'read_only_preflight', 'sentinel': 'Preserve unrelated bytes.'})
    sentinel.write_bytes(initial)
    if kind == 'symlink': path.symlink_to(sentinel)
    elif kind == 'dangling': path.symlink_to(f.repo / 'nonexistent_output_target')
    elif kind == 'hardlink': os.link(sentinel, path)
    elif kind == 'directory': path.mkdir()
    elif kind == 'fifo': os.mkfifo(path)
    else: raise RuntimeError('Unknown fixture type')
    before = m.snapshot(f.repo)
    dispatches = []
    def forbidden(*args, **kwargs):
        dispatches.append('service boundary reached')
        raise RuntimeError('Unexpected service call before output guard')
    with patch.object(m.c, 'live_eligibility', forbidden), patch.object(m.z, 'kit_cli', forbidden), \
         patch.object(m.c, 'confirm_live_publication', forbidden), \
         patch.object(m.t, 'confirm_live_publication', forbidden), \
         patch.object(m.c, 'github', forbidden), patch.object(m.c, 'gws', forbidden), \
         patch.object(m.t, 'gws', forbidden):
        operations = {'stage': lambda: m.z.run('stage', True),
                      'publish': lambda: m.z.run('publish', True, 123456),
                      'inspect': lambda: m.z.run('inspect'),
                      'tracker_preflight': lambda: m.t.run(False),
                      'tracker_apply': lambda: m.t.run(True),
                      'integration_preflight': lambda: m.integ.run(False),
                      'integration_apply': lambda: m.integ.run(True),
                      'integration_reconcile': m.integ.reconcile}
        m.rejection(operations[runner], 'Unsafe receipt destination')
    require(not dispatches and m.snapshot(f.repo) == before,
            'Unsafe output reached service or changed fixture bytes')


def safe_writer(m, f, existing):
    path = f.audit / 'PR_BODY_CURRENT.md'
    if existing: path.write_bytes(b'Authorized previous body.\n')
    sentinel = f.repo / 'unrelated_safe_output_target.bin'; sentinel.write_bytes(b'Keep unrelated.')
    expected = b'Complete updated body.\n\0\xff'
    m.c.write_output(path.name, expected)
    require(path.read_bytes() == expected and sentinel.read_bytes() == b'Keep unrelated.', 'Safe output failed')
    require(not list(f.audit.glob('.pr464-output-*')), 'Temporary output remains')
    m.c.dump('OWNED_OUTPUT_RECEIPT.json', {'state': 'complete'})
    require(json.loads((f.audit / 'OWNED_OUTPUT_RECEIPT.json').read_bytes()) == {'state': 'complete'}, 'Safe JSON output failed')


def alias_writer(m, f, kind):
    if kind == 'root':
        alias = f.repo / 'audit_alias'; alias.symlink_to(f.audit, target_is_directory=True)
        patched = alias; name = 'OWNED_OUTPUT.json'
    elif kind == 'ancestor':
        alias = f.repo / 'ancestor_alias'; alias.symlink_to(f.audit.parent, target_is_directory=True)
        patched = alias / f.audit.name; name = 'OWNED_OUTPUT.json'
    elif kind == 'internal_ancestor':
        alias = f.audit / 'internal_alias'; alias.symlink_to(f.audit, target_is_directory=True)
        patched = f.audit; name = 'internal_alias/OWNED_OUTPUT.json'
    else:
        patched = f.audit / '..' / f.audit.name; name = 'OWNED_OUTPUT.json'
    before = m.snapshot(f.repo)
    with patch.object(m.c, 'AUDIT', patched):
        m.rejection(lambda: m.c.dump(name, {'state': 'complete'}), 'Unsafe receipt destination')
    require(m.snapshot(f.repo) == before, 'Root/ancestor rejection changed bytes')


def main():
    original = hashlib.sha256(ATTACKS.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location('sealed_ops3_root_replay', ATTACKS)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    private = ROOT / 'private_sources'; private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='operation_output_controls_', dir=private) as tmp:
        m.HERE = Path(tmp).resolve()
        groups = [(['stage', 'publish', 'inspect'],
                   ['ZENODO_STAGE_OPERATION.json', 'ZENODO_PUBLISH_OPERATION.json', 'ZENODO_STAGE_RECEIPT.json',
                    'ZENODO_PUBLISH_RECEIPT.json', 'ZENODO_PUBLIC_FILE_READBACK.json']),
                  (['tracker_preflight', 'tracker_apply'],
                   ['TRACKER_APPEND_OPERATION.json', 'TRACKER_APPEND_RECEIPT.json', 'ZENODO_PUBLIC_FILE_READBACK.json']),
                  (['integration_preflight', 'integration_apply', 'integration_reconcile'],
                   ['BRANCH_INTEGRATION_PREFLIGHT.json', 'BRANCH_INTEGRATION_OPERATION.json',
                    'BRANCH_INTEGRATION_RECEIPT.json', 'PR_BODY_CURRENT.md', 'ZENODO_PUBLIC_FILE_READBACK.json'])]
        for runners, names in groups:
            for runner in runners:
                for name in names:
                    for kind in ['symlink', 'dangling', 'hardlink', 'directory', 'fifo']:
                        m.case('parent_output_' + runner + '_' + name + '_' + kind,
                               lambda f, runner=runner, name=name, kind=kind: unsafe_runner(m, f, runner, name, kind))
        for existing in [False, True]:
            m.case('parent_complete_writer_existing_' + str(existing), lambda f, existing=existing: safe_writer(m, f, existing))
        for kind in ['root', 'ancestor', 'internal_ancestor', 'noncanonical']:
            m.case('parent_output_alias_' + kind, lambda f, kind=kind: alias_writer(m, f, kind))
        with contextlib.redirect_stdout(io.StringIO()): m.main()
        suffix = 'NORMAL' if __debug__ else 'OPTIMIZED'
        result = json.loads((m.HERE / ('INDEPENDENT_CONTROLS_' + suffix + '.json')).read_bytes())
        result['reviewer'] = '/root'
        result['independent_new_case_definitions'] = False
        result['sealed_round3_expectations_replayed'] = 84
        result['root_regression_expectations_added'] = 186
        result['scope'] = 'Root regression and sealed-source replay only; NEW independent review required.'
        (ROOT / ('OPERATION_OUTPUT_REPAIR_CONTROLS_' + suffix + '.json')).write_bytes(m.c.json_bytes(result))
    require(hashlib.sha256(ATTACKS.read_bytes()).hexdigest() == original, 'Sealed attack source changed')
    print(json.dumps({k: result[k] for k in ['case_count', 'passed_count', 'all_passed', 'real_external_calls']}, sort_keys=True))
    require(result['case_count'] == 270 and result['all_passed'] is True and result['real_external_calls'] == 0,
            'Output regression expectation failed')


if __name__ == '__main__': main()
