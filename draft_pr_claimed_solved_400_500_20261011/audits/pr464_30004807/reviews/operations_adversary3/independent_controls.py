#!/usr/bin/env python3
"""New reviewer-3 controls, with generated fixtures confined to private_cases.

The preparer Fixture constructs synthetic files only. All cases, expectations,
service mocks and complete-builder readbacks below are newly reviewer-written.
No assertion statements or genuine service/credential access are used.
"""
import base64
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import socket
import stat
import sys
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
REPO = AUDIT.parents[2]
sys.path.insert(0, str(AUDIT / 'operations'))
import common as c
import check_operations as constructor
import zenodo_pr464 as z
import register_pr464_tracker as t
import integrate_pr464_publication as integ
NATIVE_GWS = c.gws

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

builder = load(AUDIT / 'build_preprint_package.py', 'ops3_reviewed_builder')
kit = load(REPO / 'zenodo_deposit_tool/zenodo.py', 'ops3_reviewed_kit')
CASES = []
REAL_CALLS = []

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def deny(*args, **kwargs):
    REAL_CALLS.append('unmocked service boundary')
    raise RuntimeError('REAL SERVICE BOUNDARY DENIED')

def rejection(fn, needle):
    try:
        fn()
    except (RuntimeError, kit.DepositError) as error:
        require(needle in str(error), 'Incidental guard error: ' + str(error))
        return str(error)
    raise RuntimeError('Required rejection absent: ' + needle)

def jwrite(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(c.json_bytes(value))

def snapshot(root):
    out = {}
    for path in root.rglob('*'):
        info = path.lstat()
        name = path.relative_to(root).as_posix()
        if stat.S_ISLNK(info.st_mode):
            out[name] = {'type': 'link', 'target': os.readlink(path)}
        elif stat.S_ISREG(info.st_mode):
            out[name] = {'type': 'file', 'sha256': c.sha(path.read_bytes()), 'bytes': info.st_size}
        else:
            out[name] = {'type': stat.S_IFMT(info.st_mode)}
    return out

def case(name, fn):
    before = len(REAL_CALLS)
    private = HERE / 'private_cases'
    private.mkdir(exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='ops3_', dir=private) as directory:
            fixture = constructor.Fixture(Path(directory).resolve())
            with patch.multiple(c, AUDIT=fixture.audit, PACKAGE=fixture.package, REPOSITORY=fixture.repo), \
                 patch.object(t, 'AUDIT', fixture.audit), patch.object(c, 'github', deny), \
                 patch.object(c, 'gws', deny), patch.object(c.subprocess, 'run', deny), \
                 patch.object(socket, 'create_connection', deny), patch.object(z, 'build_opener', deny):
                fn(fixture)
            require(len(REAL_CALLS) == before, 'Control escaped genuine service isolation')
        CASES.append({'case': name, 'passed': True, 'real_external_calls': 0})
    except Exception as error:
        CASES.append({'case': name, 'passed': False, 'error_type': type(error).__name__,
                      'error': str(error), 'real_external_calls': len(REAL_CALLS) - before})

def builder_setup(f):
    (f.package / 'CURRENT_PUBLICATION_NOTES.md').write_bytes(b'Synthetic authored offline note.\n')
    jwrite(f.package / 'REVIEW_EVIDENCE_SELECTION.json', {'positive_explicit_selection': True, 'entries': []})
    jwrite(f.package / 'verification/PUBLIC_OUTPUT_WHITELIST.json', {'positive_whitelist_only': True, 'public_files': []})

def build(f, args=(), root=None, package=None):
    with patch.multiple(builder, ROOT=root or f.audit, PACKAGE=package or f.package), \
         patch.object(sys, 'argv', ['builder', *args]), contextlib.redirect_stdout(io.StringIO()):
        builder.main()

def output_rejection(f, name, kind, freeze=False):
    builder_setup(f)
    path = f.audit / name if freeze or name == 'BRANCH_INSTALL_PLAN.json' else f.package / name
    path.unlink(missing_ok=True)
    sentinel = f.repo / 'unrelated_owned_sentinel.bin'
    sentinel.write_bytes(b'Leave every unrelated byte intact.\0\xff\n')
    if kind == 'symlink':
        path.symlink_to(sentinel)
    elif kind == 'dangling':
        path.symlink_to(f.repo / 'not_created.bin')
    elif kind == 'directory':
        path.mkdir()
    elif kind == 'fifo':
        os.mkfifo(path)
    elif kind == 'hardlink':
        os.link(sentinel, path)
    elif kind == 'regular':
        path.write_bytes(b'Immutable previous review input.\n')
    else:
        raise RuntimeError('Unknown fixture type')
    before = snapshot(f.repo)
    error = 'Symlink in generated output path' if kind in {'symlink', 'dangling'} else (
        'Never overwrite a frozen review input' if freeze else 'Unsafe existing output file type or hard link')
    rejection(lambda: build(f, ['--freeze', '3'] if freeze else []), error)
    require(snapshot(f.repo) == before, 'Rejected output preflight changed bytes, sentinel or path types')

def existing_or_invalid_freeze(f, number):
    builder_setup(f)
    before = snapshot(f.repo)
    rejection(lambda: build(f, ['--freeze', str(number)]),
              'Never overwrite a frozen review input' if number == 2 else 'Invalid review round')
    require(snapshot(f.repo) == before, 'Rejected immutable/invalid freeze changed current outputs')

def root_alias(f, kind):
    builder_setup(f)
    root, package = f.audit, f.package
    if kind == 'audit':
        alias = f.repo / 'audit_alias'; alias.symlink_to(f.audit, target_is_directory=True); root = alias
    elif kind == 'package':
        alias = f.audit / 'package_alias'; alias.symlink_to(f.package, target_is_directory=True); package = alias
    elif kind == 'audit_ancestor':
        alias = f.repo / 'ancestor_alias'; alias.symlink_to(f.audit.parent, target_is_directory=True); root = alias / f.audit.name
    else:
        alias = f.repo / 'ancestor_alias'; alias.symlink_to(f.audit, target_is_directory=True); package = alias / 'package'
    before = snapshot(f.repo)
    rejection(lambda: build(f, ['--freeze', '3'], root, package), 'Unsafe output root')
    require(snapshot(f.repo) == before, 'Rejected root/ancestor alias changed fixture')

def complete_builder(f, regular_existing):
    builder_setup(f)
    if regular_existing:
        for name in ['SHA256SUMS.json', c.ZIP_NAME, 'ARCHIVE_RECEIPT.json', 'deposit.json']:
            (f.package / name).write_bytes(b'Previous authorized owned output.\n')
        (f.audit / 'BRANCH_INSTALL_PLAN.json').write_bytes(b'Previous authorized owned plan.\n')
    prior_freeze = (f.audit / f.manifest_name).read_bytes()
    build(f, ['--freeze', '3'])
    require((f.audit / f.manifest_name).read_bytes() == prior_freeze, 'Successful build edited an earlier immutable freeze')
    freeze = json.loads((f.audit / 'PACKAGE_REVIEW_INPUT_3.json').read_bytes())
    manifest = json.loads((f.package / 'SHA256SUMS.json').read_bytes())['files']
    for name, spec in freeze['files'].items():
        data = (f.package / name).read_bytes()
        require(c.sha(data) == spec['sha256'] and len(data) == spec['bytes'], 'New freeze output bytes mismatch')
    with zipfile.ZipFile(f.package / c.ZIP_NAME) as archive:
        require(archive.testzip() is None and len(archive.namelist()) == len(set(archive.namelist())), 'New archive CRC or duplicate entry defect')
        require(set(archive.namelist()) == set(manifest) | {'SHA256SUMS.json'}, 'New archive exact manifest selection mismatch')
        for name, spec in manifest.items():
            data = archive.read(name)
            require(data == (f.package / name).read_bytes() and c.sha(data) == spec['sha256'] and len(data) == spec['bytes'], 'New archive whole payload mismatch')
    plan = json.loads((f.audit / 'BRANCH_INSTALL_PLAN.json').read_bytes())
    selected = set(manifest) | set(freeze['files'])
    require(len(plan['entries']) == len(selected), 'New positive install count mismatch')
    for item in plan['entries']:
        path = f.repo / item['local_program_path']; data = path.read_bytes()
        require(item['repository_destination'] == c.PREPRINT + path.relative_to(f.package).as_posix(), 'New install mapping mismatch')
        require(c.sha(data) == item['sha256'] and len(data) == item['bytes'], 'New install whole bytes mismatch')
    for field, name in [('source_receipt_sha256', 'SOURCE_RECEIPT.json'), ('mathematical_acceptance_gate_sha256', 'MATHEMATICAL_ACCEPTANCE_GATE.json'), ('branch_install_plan_sha256', 'BRANCH_INSTALL_PLAN.json')]:
        require(freeze[field] == c.sha((f.audit / name).read_bytes()), 'New freeze cross-binding mismatch')
    require(not [p for p in f.audit.rglob('.*') if p.is_file()], 'A partial output temporary file remains')

def gate_mismatch(f, field):
    c.validate_gate()
    freeze = json.loads((f.audit / f.manifest_name).read_bytes())
    if field in ['pr', 'problem', 'original_head']:
        freeze[field] = {'pr': 463, 'problem': '6000016', 'original_head': 'f' * 40}[field]
        jwrite(f.audit / f.manifest_name, freeze)
        f.gate['review_input_manifest_sha256'] = c.sha((f.audit / f.manifest_name).read_bytes())
        for review in f.gate['complete_package_reviews']:
            review['input_manifest_sha256'] = f.gate['review_input_manifest_sha256']
        diagnostic = 'Reviewed freeze PR/problem/original-head identity differs'
    else:
        name = {'source_receipt_sha256': 'SOURCE_RECEIPT.json', 'mathematical_acceptance_gate_sha256': 'MATHEMATICAL_ACCEPTANCE_GATE.json', 'branch_install_plan_sha256': 'BRANCH_INSTALL_PLAN.json'}[field]
        value = json.loads((f.audit / name).read_bytes()); value['changed_after_review'] = True
        jwrite(f.audit / name, value); f.gate[field] = c.sha((f.audit / name).read_bytes())
        diagnostic = 'Reviewed freeze cross-binding differs'
    f.save_gate()
    rejection(c.validate_gate, diagnostic)

def gate_count(f, kind, value):
    c.validate_gate()
    if kind == 'package':
        f.gate['complete_package_reviews'][1]['blocking_issue_count'] = value
        diagnostic = 'Nonzero or invalid blocking_issue_count'
    elif kind == 'operations':
        f.gate['operations_review']['required_correction_count'] = value
        diagnostic = 'Nonzero or invalid operations required_correction_count'
    else:
        f.gate['remaining_package_issues'] = value
        diagnostic = 'Nonzero or invalid remaining_package_issues'
    f.save_gate(); rejection(c.validate_gate, diagnostic)

def native_gws(f):
    calls = []
    class Reply:
        returncode = 0
        stdout = '{"offline_fixture_only":true}'
    def runner(args, **kwargs):
        calls.append((args, kwargs)); return Reply()
    with patch.object(c.subprocess, 'run', runner):
        NATIVE_GWS('append', {'spreadsheetId': c.SHEET, 'range': "'Math Puzzles'!A:D", 'valueInputOption': 'RAW'}, {'values': [['original', '', 'doi', 'notes']]})
    require(len(calls) == 1 and calls[0][0][:5] == [c.GWS, 'sheets', 'spreadsheets', 'values', 'append'], 'GWS native append invocation changed')
    params = json.loads(calls[0][0][6]); body = json.loads(calls[0][0][8])
    require(params['spreadsheetId'] == c.SHEET and body['values'][0][1] == '', 'GWS intended sheet or blank chat column changed')

def tracker_lost_history(f, kind):
    context, pub = f.publication(); values = c.tracker_values(context['metadata'], pub['doi_url'])
    rows = [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']]
    if kind != 'receipt_only':
        jwrite(f.audit / 'TRACKER_APPEND_OPERATION.json', {'state': kind, 'doi': pub['doi_url'], 'values': values})
    if kind == 'receipt_only':
        jwrite(f.audit / 'TRACKER_APPEND_RECEIPT.json', {'verified': True, 'spreadsheet_id': c.SHEET, 'sheet_id': c.TAB_ID,
             'tab': c.TAB, 'doi': pub['doi_url'], 'values': values, 'updated_range': "'Math Puzzles'!A2:D2", 'unique_doi_row_at_final_snapshot': True})
    before = {p.name: p.read_bytes() for p in f.audit.glob('TRACKER_APPEND_*.json')}; appends = []
    with patch.multiple(t, validate_gate=lambda: context, confirm_live_publication=lambda _: pub,
                        live_eligibility=lambda: None, check_sheet=lambda: None,
                        sheet_get=lambda _: {'values': copy.deepcopy(rows)}, gws=lambda *args: appends.append(args)):
        for apply in [False, True]:
            rejection(lambda: t.run(apply), 'row was removed')
            require({p.name: p.read_bytes() for p in f.audit.glob('TRACKER_APPEND_*.json')} == before, 'History-loss rejection overwrote durable guards')
    require(not appends, 'History-loss reconciliation appended a second row')

def git_blob(f, defect):
    data = b'Exact whole binary blob\0\xff\x80\n'; digest = c.git_sha(data)
    revision = 'a' * 40; tree = 'b' * 40
    responses = {'git/commits/' + revision: {'sha': revision, 'tree': {'sha': tree}},
                 'git/trees/' + tree: {'sha': tree, 'truncated': False, 'tree': [{'path': 'binary.bin', 'mode': '100644', 'type': 'blob', 'sha': digest}]},
                 'git/blobs/' + digest: {'sha': digest, 'encoding': 'base64', 'size': len(data), 'content': base64.b64encode(data).decode()}}
    if defect == 'same_size_corruption':
        responses['git/blobs/' + digest]['content'] = base64.b64encode(b'X' + data[1:]).decode()
    elif defect == 'symlink':
        responses['git/trees/' + tree]['tree'][0]['mode'] = '120000'
    elif defect == 'truncated_tree':
        responses['git/trees/' + tree]['truncated'] = True
    elif defect == 'duplicate_tree':
        responses['git/trees/' + tree]['tree'].append(copy.deepcopy(responses['git/trees/' + tree]['tree'][0]))
    reads = []
    def github(endpoint):
        reads.append(endpoint); require(endpoint in responses, 'Unexpected immutable read endpoint'); return copy.deepcopy(responses[endpoint])
    with patch.object(c, 'github', github):
        reader = c.GitReader()
        if defect == 'valid':
            require(reader.read('binary.bin', revision) == data, 'Binary immutable full readback changed bytes')
        else:
            rejection(lambda: reader.read('binary.bin', revision), {'same_size_corruption': 'does not match immutable object', 'symlink': 'symlinked Git blob', 'truncated_tree': 'Truncated or invalid Git tree', 'duplicate_tree': 'Duplicate Git tree path'}[defect])
    require(all(endpoint.startswith('git/') for endpoint in reads), 'Contents endpoint used for binary readback')

def kit_identity(f, defect):
    record = {'id': 123456, 'submitted': False}
    if defect == 'id_bool': record['id'] = True
    if defect == 'id_float': record['id'] = 123456.0
    if defect == 'wrong_id': record['id'] = 123457
    if defect == 'state_int': record['submitted'] = 0
    if defect == 'state_string': record['submitted'] = 'false'
    if defect == 'valid': kit.validate_record(record, 123456)
    else: rejection(lambda: kit.validate_record(record, 123456), 'different deposition ID' if defect.startswith('id') or defect == 'wrong_id' else 'invalid publication state')

def output_receipt_hardlink(f):
    # A fixed actual runner operation path, not an arbitrary caller path.
    sentinel = f.repo / 'unrelated_receipt_target.bin'; initial = b'Unrelated existing bytes\0\xff\n'; sentinel.write_bytes(initial)
    path = f.audit / 'ZENODO_STAGE_OPERATION.json'; os.link(sentinel, path)
    try:
        c.dump(path.name, {'operation': 'stage', 'state': 'stage_attempted_once'})
    except RuntimeError:
        require(sentinel.read_bytes() == initial, 'Rejected receipt write still changed the sentinel')
        return
    require(sentinel.read_bytes() == initial, 'Fixed Zenodo operation receipt overwrote an unrelated hard-linked file before dispatch')

def actual_stage_operation_hardlink(f):
    context = c.validate_gate()
    sentinel = f.repo / 'unrelated_preflight_record.json'
    initial = c.json_bytes({'state': 'read_only_preflight', 'unrelated_sentinel': 'Must be preserved outside the audit root.'})
    sentinel.write_bytes(initial)
    os.link(sentinel, f.audit / 'ZENODO_STAGE_OPERATION.json')
    dispatches = []
    def mock_kit(ctx, mode, confirm_id=None):
        dispatches.append(mode)
        return {'state': 'ready_to_publish', 'id': 123456, 'environment': 'production',
                'title': context['metadata']['title'], 'metadata_normalizations': [],
                'files': list(c.expected_public_files(context).values()),
                'canonical_metadata_sha256': c.sha((f.package / 'metadata.json').read_bytes()),
                'accepted_input_manifest_sha256': context['gate']['review_input_manifest_sha256']}
    with patch.object(c, 'live_eligibility', lambda: None), patch.object(z, 'kit_cli', mock_kit):
        try:
            z.run('stage', True)
        except RuntimeError:
            require(sentinel.read_bytes() == initial and not dispatches, 'Rejected unsafe stage still modified the target or dispatched')
            return
    require(sentinel.read_bytes() == initial and not dispatches,
            'The actual stage runner clobbered an unrelated hard-linked preflight file and reached one mocked stage dispatch')

def actual_integration_body_output(f, hardlink):
    # A new output-boundary attack uses the sealed prior review's complete Git
    # service model. This reuses only the service model, not its expectations.
    prior = load(AUDIT / 'reviews/operations_adversary2/independent_controls.py', 'ops3_integration_service_model')
    sentinel = f.repo / 'unrelated_body_target.md'
    initial = b'Unrelated body target must survive the integration.\n'
    sentinel.write_bytes(initial)
    output = f.audit / 'PR_BODY_CURRENT.md'
    if hardlink:
        os.link(sentinel, output)
    else:
        output.symlink_to(sentinel)
    try:
        prior.integration_flow(f, 'valid')
    except RuntimeError:
        require(sentinel.read_bytes() == initial, 'Rejected PR body output still modified unrelated bytes')
        return
    require(sentinel.read_bytes() == initial,
            'Verified integration followed an unsafe PR_BODY_CURRENT.md output and overwrote the unrelated target')

def receipt_leaf_symlink(f, dangling):
    target = f.repo / 'unrelated_receipt_target.bin'; target.write_bytes(b'Preserve unrelated target.\n')
    path = f.audit / 'ZENODO_STAGE_OPERATION.json'
    path.symlink_to(f.repo / 'not_existing.bin' if dangling else target)
    before = snapshot(f.repo)
    rejection(lambda: c.dump(path.name, {'operation': 'stage'}), 'Unsafe receipt destination')
    require(snapshot(f.repo) == before, 'Rejected receipt symlink write changed fixture')

def main():
    for name in ['SHA256SUMS.json', c.ZIP_NAME, 'ARCHIVE_RECEIPT.json', 'deposit.json', 'BRANCH_INSTALL_PLAN.json']:
        for kind in ['symlink', 'dangling', 'directory', 'fifo', 'hardlink']:
            case('whole_builder_output_' + name + '_' + kind, lambda f, name=name, kind=kind: output_rejection(f, name, kind))
    for kind in ['symlink', 'dangling', 'regular', 'directory', 'fifo', 'hardlink']:
        case('whole_builder_new_freeze_' + kind, lambda f, kind=kind: output_rejection(f, 'PACKAGE_REVIEW_INPUT_3.json', kind, True))
    for number in [2, 0, -1, -100]:
        case('whole_builder_refused_freeze_' + str(number), lambda f, number=number: existing_or_invalid_freeze(f, number))
    for kind in ['audit', 'package', 'audit_ancestor', 'package_ancestor']:
        case('whole_builder_root_alias_' + kind, lambda f, kind=kind: root_alias(f, kind))
    for regular_existing in [False, True]:
        case('whole_builder_success_existing_' + str(regular_existing), lambda f, regular_existing=regular_existing: complete_builder(f, regular_existing))
    for field in ['pr', 'problem', 'original_head', 'source_receipt_sha256', 'mathematical_acceptance_gate_sha256', 'branch_install_plan_sha256']:
        case('exact_reviewed_freeze_binding_' + field, lambda f, field=field: gate_mismatch(f, field))
    for kind in ['package', 'operations', 'remaining']:
        for label, value in [('false', False), ('float_zero', 0.0), ('string_zero', '0'), ('positive', 1), ('negative', -1)]:
            case('strict_integer_issue_count_' + kind + '_' + label, lambda f, kind=kind, value=value: gate_count(f, kind, value))
    case('native_google_workspace_cli_invocation', native_gws)
    for kind in ['append_attempted_once', 'outcome_unconfirmed', 'verified_registration', 'receipt_only']:
        case('tracker_durable_history_missing_row_' + kind, lambda f, kind=kind: tracker_lost_history(f, kind))
    for defect in ['valid', 'same_size_corruption', 'symlink', 'truncated_tree', 'duplicate_tree']:
        case('immutable_binary_git_read_' + defect, lambda f, defect=defect: git_blob(f, defect))
    for defect in ['valid', 'id_bool', 'id_float', 'wrong_id', 'state_int', 'state_string']:
        case('unchanged_kit_record_identity_' + defect, lambda f, defect=defect: kit_identity(f, defect))
    case('actual_operation_receipt_hardlink_boundary', output_receipt_hardlink)
    case('actual_stage_runner_preflight_hardlink_boundary', actual_stage_operation_hardlink)
    case('actual_operation_receipt_leaf_symlink', lambda f: receipt_leaf_symlink(f, False))
    case('actual_operation_receipt_dangling_symlink', lambda f: receipt_leaf_symlink(f, True))
    case('actual_integration_body_symlink_boundary', lambda f: actual_integration_body_output(f, False))
    case('actual_integration_body_hardlink_boundary', lambda f: actual_integration_body_output(f, True))
    result = {'reviewer': '/root/pr464_operations_adversary3', 'independent_new_case_definitions': True,
              'filesystem_constructor_reused': 'operations/check_operations.py Fixture only',
              'integration_body_attacks_reuse_prior_service_model_only': 'operations_adversary2/independent_controls.py integration_flow',
              'case_count': len(CASES), 'passed_count': sum(x['passed'] is True for x in CASES),
              'all_passed': all(x['passed'] is True for x in CASES), 'real_external_calls': len(REAL_CALLS), 'cases': CASES,
              'scope': 'Finite offline operational controls; no mathematical/human-peer certification or hostile-filesystem/group-transaction guarantee.'}
    suffix = 'NORMAL' if __debug__ else 'OPTIMIZED'
    (HERE / ('INDEPENDENT_CONTROLS_' + suffix + '.json')).write_bytes(c.json_bytes(result))
    print(json.dumps({k: result[k] for k in ['case_count', 'passed_count', 'all_passed', 'real_external_calls']}, sort_keys=True))

if __name__ == '__main__':
    main()
