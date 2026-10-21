#!/usr/bin/env python3
"""Fresh reviewer-written offline controls. Generated fixtures remain private.

The preparer's Fixture is used only as a disclosed filesystem constructor.
Every expectation and mocked service below is reviewer-written. Real service
boundaries are denied. These are finite operational checks, not certification.
"""
import argparse
import base64
import copy
import datetime
import hashlib
import importlib.util
import io
import contextlib
import json
import socket
import sys
import tempfile
import zipfile
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
REPO = AUDIT.parents[2]
sys.path.insert(0, str(AUDIT / 'operations'))
import common as c
import zenodo_pr464 as z
import register_pr464_tracker as t
import integrate_pr464_publication as integ
import check_operations as prepared

kit_spec = importlib.util.spec_from_file_location('reviewed_kit', REPO / 'zenodo_deposit_tool/zenodo.py')
kit = importlib.util.module_from_spec(kit_spec)
kit_spec.loader.exec_module(kit)
build_spec = importlib.util.spec_from_file_location('reviewed_builder', AUDIT / 'build_preprint_package.py')
builder = importlib.util.module_from_spec(build_spec)
build_spec.loader.exec_module(builder)
CASES = []
REAL_CALLS = []
ATTACK_OBSERVATIONS = []


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(c.json_bytes(obj))


def forbidden(*args, **kwargs):
    REAL_CALLS.append('unmocked service boundary')
    raise RuntimeError('OFFLINE BOUNDARY DENIED')


def rejection(fn, text=None):
    try:
        fn()
    except (RuntimeError, kit.DepositError) as error:
        if text is not None:
            require(text in str(error), 'Incidental/wrong rejection: ' + str(error))
        return str(error)
    raise RuntimeError('Required rejection was absent')


@contextmanager
def fixture_context():
    private = HERE / 'private_cases'
    private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ops2_', dir=private) as directory:
        f = prepared.Fixture(Path(directory))
        with patch.multiple(c, AUDIT=f.audit, PACKAGE=f.package, REPOSITORY=f.repo), \
             patch.object(t, 'AUDIT', f.audit), \
             patch.object(c, 'github', forbidden), patch.object(c, 'gws', forbidden), \
             patch.object(c.subprocess, 'run', forbidden), \
             patch.object(socket, 'create_connection', forbidden), \
             patch.object(z, 'build_opener', forbidden):
            yield f


def case(name, fn):
    before = len(REAL_CALLS)
    try:
        with fixture_context() as f:
            fn(f)
        require(len(REAL_CALLS) == before, 'An unmocked service call occurred')
        CASES.append({'case': name, 'passed': True, 'real_external_calls': 0})
    except Exception as error:
        CASES.append({'case': name, 'passed': False, 'error_type': type(error).__name__,
                      'error': str(error), 'real_external_calls': len(REAL_CALLS) - before})


def gate_attack(f, operation):
    c.validate_gate()
    operation(f)
    f.save_gate()
    rejection(c.validate_gate)


def update_freeze_hash(f):
    f.gate['review_input_manifest_sha256'] = c.sha((f.audit / f.manifest_name).read_bytes())
    for r in f.gate['complete_package_reviews']:
        r['input_manifest_sha256'] = f.gate['review_input_manifest_sha256']
    f.save_gate()


def freeze_cross(f, field):
    c.validate_gate()
    file = {'source_receipt_sha256': 'SOURCE_RECEIPT.json',
            'mathematical_acceptance_gate_sha256': 'MATHEMATICAL_ACCEPTANCE_GATE.json',
            'branch_install_plan_sha256': 'BRANCH_INSTALL_PLAN.json'}[field]
    value = json.loads((f.audit / file).read_text())
    value['fresh_review_unperformed_annotation'] = 'benign changed bytes'
    write_json(f.audit / file, value)
    f.gate[field] = c.sha((f.audit / file).read_bytes())
    f.save_gate()
    rejection(c.validate_gate, 'Reviewed freeze cross-binding differs')


def archive_attack(f, kind):
    c.validate_gate()
    path = f.package / c.ZIP_NAME
    if kind == 'local_payload_drift':
        (f.package / 'verification/README.md').write_bytes(b'changed independently')
    else:
        with zipfile.ZipFile(path, 'a') as archive:
            info = zipfile.ZipInfo('verification/added.txt' if kind == 'unplanned' else
                                   '../escape' if kind == 'traversal' else
                                   'private_cases/secret.txt' if kind == 'private' else
                                   'venv/secret.txt' if kind == 'environment' else
                                   'manuscript.pdf' if kind == 'circular' else
                                   'symlink.txt' if kind == 'symlink' else 'README.md')
            info.external_attr = (0o120777 if kind == 'symlink' else 0o100644) << 16
            archive.writestr(info, b'generated private counterexample fixture')
        f.top[c.ZIP_NAME] = {'sha256': c.sha(path.read_bytes()), 'bytes': path.stat().st_size}
        f.gate['final_files'] = f.top
        freeze = json.loads((f.audit / f.manifest_name).read_text())
        freeze['files'] = f.top
        write_json(f.audit / f.manifest_name, freeze)
        for e in f.plan['entries']:
            if e['repository_destination'] == c.PREPRINT + c.ZIP_NAME:
                e.update(f.top[c.ZIP_NAME])
        f.save_plan()
    rejection(c.validate_gate)


def tracker_scenario(f, state, apply=True):
    context, pub = f.publication()
    values = c.tracker_values(context['metadata'], pub['doi_url'])
    require(values[0][1] == '', 'Chat cell is not intentionally blank')
    header = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
    rows = [header, ['unrelated', '', 'https://doi.org/10.0/keep', 'preserve exact unrelated row']]
    writes = []
    if state in {'existing_exact', 'existing_changed', 'duplicate_alias', 'prior_exact'}:
        rows.append(copy.deepcopy(values[0]))
    if state == 'existing_changed':
        rows[-1][3] += ' conflicting note'
    if state == 'duplicate_alias':
        alias = copy.deepcopy(values[0]); alias[2] = pub['doi']; rows.append(alias)
    op = {'state': 'verified_registration' if state in {'prior_verified_removed', 'prior_exact'} else 'outcome_unconfirmed',
          'doi': pub['doi_url'], 'values': values}
    receipt = {'verified': True, 'spreadsheet_id': c.SHEET, 'sheet_id': c.TAB_ID, 'tab': c.TAB,
               'values': values, 'doi': pub['doi_url'], 'updated_range': "'Math Puzzles'!A3:D3",
               'unique_doi_row_at_final_snapshot': True}
    if state in {'prior_verified_removed', 'prior_uncertain_removed', 'prior_exact'}:
        write_json(f.audit / 'TRACKER_APPEND_OPERATION.json', op)
    if state in {'prior_verified_removed', 'receipt_removed', 'prior_exact'}:
        write_json(f.audit / 'TRACKER_APPEND_RECEIPT.json', receipt)
    saved = {p.name: p.read_bytes() for p in f.audit.glob('TRACKER_APPEND_*.json')}
    reads = 0
    def get(range_name):
        nonlocal reads
        reads += 1
        if range_name.endswith('A:D'):
            if state == 'concurrent_before_append' and reads > 1 and len(rows) == 2:
                rows.append(copy.deepcopy(values[0]))
            return {'values': copy.deepcopy(rows)}
        import re
        match = re.fullmatch(r"'Math Puzzles'!A([0-9]+):D\1", range_name)
        require(match is not None, 'Unexpected mocked range')
        n = int(match[1]); return {'values': copy.deepcopy(rows[n-1:n])}
    def append(action, params, body):
        require(action == 'append' and params['spreadsheetId'] == c.SHEET
                and params['range'] == "'Math Puzzles'!A:D" and params['valueInputOption'] == 'RAW'
                and body == {'majorDimension': 'ROWS', 'values': values}, 'Native append bytes differ')
        require(json.loads((f.audit / 'TRACKER_APPEND_OPERATION.json').read_text())['state'] == 'append_attempted_once',
                'Append was dispatched before durable write guard')
        writes.append('append')
        rows.append(copy.deepcopy(values[0]))
        if state == 'lost_success':
            raise RuntimeError('mock response lost after successful append')
        if state == 'lost_failure':
            rows.pop(); raise RuntimeError('mock append outcome remains absent')
        if state == 'duplicate_after_append':
            rows.append(copy.deepcopy(values[0]))
        return {'updates': {'updatedRows': 1, 'updatedColumns': 4,
                            'updatedCells': False if state == 'wrong_count_type' else 4,
                            'updatedRange': "'Math Puzzles'!A3:D4" if state == 'wrong_range' else "'Math Puzzles'!A3:D3"}}
    with patch.multiple(t, validate_gate=lambda: context, confirm_live_publication=lambda ctx: pub,
                        live_eligibility=lambda: None, check_sheet=lambda: None, sheet_get=get, gws=append):
        bad = {'existing_changed', 'duplicate_alias', 'prior_verified_removed', 'receipt_removed',
               'prior_uncertain_removed', 'concurrent_before_append', 'duplicate_after_append',
               'lost_failure', 'wrong_count_type', 'wrong_range'}
        if state in bad:
            rejection(lambda: t.run(apply))
            if state in {'prior_verified_removed', 'receipt_removed', 'prior_uncertain_removed'}:
                require({p.name: p.read_bytes() for p in f.audit.glob('TRACKER_APPEND_*.json')} == saved,
                        'Rejected reconciliation destroyed durable prior evidence')
            require(len(writes) == (1 if state in {'duplicate_after_append', 'lost_failure', 'wrong_count_type', 'wrong_range'} else 0),
                    'Unexpected append count for failed workflow')
            if writes:
                if state in {'wrong_count_type', 'wrong_range'}:
                    recovered = t.run(True)
                    require(recovered['verified'] is True, 'Exact existing row recovery rejected')
                else:
                    rejection(lambda: t.run(True))
                require(len(writes) == 1, 'Failed write was repeated')
        else:
            result = t.run(apply)
            expected = 0 if not apply or state in {'existing_exact', 'prior_exact'} else 1
            require(len(writes) == expected, 'Unexpected accepted append count')
            if apply:
                require(result['verified'] is True, 'Exact registration was not confirmed')
                t.run(True); require(len(writes) == expected, 'Successful registration was repeated')
        require(rows[1] == ['unrelated', '', 'https://doi.org/10.0/keep', 'preserve exact unrelated row'],
                'Unrelated tracker row was altered')


def public_readback_case(f, kind):
    context = c.validate_gate()
    pub = {'id': 123456, 'state': 'published', 'doi': '10.5281/zenodo.123456',
           'record_url': 'https://zenodo.org/records/123456'}
    content = {name: (f.package / local).read_bytes() for name, local in c.UPLOADS.items()}
    record = {'id': pub['id'], 'doi': pub['doi'], 'metadata': {'title': context['metadata']['title']},
              'files': [{'key': name} for name in content]}
    if kind == 'wrong_id': record['id'] += 1
    if kind == 'wrong_title': record['metadata']['title'] += ' drift'
    if kind == 'extra_file': record['files'].append({'key': 'unexpected'})
    if kind == 'file_drift': content[next(iter(content))] += b'x'
    if kind == 'same_length_drift':
        n = next(iter(content)); content[n] = b'X' + content[n][1:]
    calls = []
    class Response(io.BytesIO):
        status = 200
    class Opener:
        def open(self, request, timeout):
            require(not any(k.lower() == 'authorization' for k, _ in request.header_items()), 'Public read leaked authentication')
            require(request.full_url.startswith('https://zenodo.org/'), 'Public read used incorrect host')
            calls.append(request.full_url)
            if '/api/records/' in request.full_url:
                return Response(json.dumps(record).encode())
            for name, data in content.items():
                if '/files/' + name + '?download=1' in request.full_url:
                    return Response(data)
            raise RuntimeError('Unexpected public read URL')
    with patch.object(z, 'build_opener', lambda *args: Opener()):
        if kind == 'valid':
            receipt = z.public_readback(context, pub)
            require(receipt['authenticated'] is False and len(calls) == 3 and receipt['public_bytes_downloaded_and_hashed'] is True,
                    'Public readback did not hash both actual streams')
        else:
            rejection(lambda: z.public_readback(context, pub))
            require(not (f.audit / 'ZENODO_PUBLIC_FILE_READBACK.json').exists(), 'Failed public verification emitted acceptance')


def wrapper_flow(f, state):
    context = c.validate_gate()
    calls = []
    service = {'state': 'absent'}
    def summary():
        out = {'environment': 'production', 'title': context['metadata']['title'], 'id': 123456,
               'state': service['state'], 'metadata_normalizations': [],
               'files': list(c.expected_public_files(context).values()),
               'canonical_metadata_sha256': c.sha((f.package / 'metadata.json').read_bytes()),
               'accepted_input_manifest_sha256': context['gate']['review_input_manifest_sha256']}
        if service['state'] == 'published':
            out.update(doi='10.5281/zenodo.123456', doi_url='https://doi.org/10.5281/zenodo.123456',
                       record_url='https://zenodo.org/records/123456')
        return out
    def cli(ctx, mode, confirm_id=None):
        calls.append(mode)
        if mode in {'stage', 'publish'}:
            require(json.loads((f.audit / ('ZENODO_' + mode.upper() + '_OPERATION.json')).read_text())['state'] == mode + '_attempted_once',
                    'Zenodo durable state absent before dispatch')
            if mode == 'publish': require(confirm_id == 123456, 'Wrong confirmed ID was dispatched')
            service['state'] = 'ready_to_publish' if mode == 'stage' else 'published'
            if state == 'lost_' + mode:
                raise RuntimeError('simulated uncertain ' + mode)
        return summary()
    def public(ctx, pub):
        write_json(f.audit / 'ZENODO_PUBLIC_FILE_READBACK.json', {'verified': True, 'authenticated': False,
                   'id': pub['id'], 'doi': pub['doi'], 'files': list(c.expected_public_files(ctx).values())})
    with patch.object(c, 'live_eligibility', lambda: None), patch.object(z, 'kit_cli', cli), patch.object(z, 'public_readback', public):
        if state == 'default':
            z.run(); require(calls == ['check'], 'Default wrapper performed a write'); return
        if state == 'lost_stage':
            rejection(lambda: z.run('stage', True), 'uncertain stage')
            z.run('inspect'); rejection(lambda: z.run('stage', True), 'prior Zenodo write')
            require(calls.count('stage') == 1 and calls.count('publish') == 0, 'Uncertain stage repeated'); return
        z.run('stage', True)
        if state == 'wrong_id':
            rejection(lambda: z.run('publish', True, 654321), 'confirmed production draft')
            require('publish' not in calls, 'Wrong draft was published'); return
        if state == 'lost_publish':
            rejection(lambda: z.run('publish', True, 123456), 'uncertain publish')
            z.run('inspect')
        else:
            z.run('publish', True, 123456)
        c.validate_publication(context)
        rejection(lambda: z.run('publish', True, 123456), 'prior Zenodo write')
        require(calls.count('stage') == calls.count('publish') == 1, 'Publication POST repeated')


def real_kit_case(f, state):
    # Execute the unchanged kit's real logic with a reviewer-owned fake client.
    metadata = {'title': 'Offline exact canonical title', 'description': '<p>Exact simple description.</p>',
                'upload_type': 'publication', 'publication_type': 'preprint',
                'creators': [{'name': 'Offline tester', 'affiliation': 'Offline'}]}
    deposit = f.package / 'kit_probe.json'
    write_json(deposit, {'metadata': metadata, 'files': [{'path': 'manuscript.pdf'}, {'path': c.ZIP_NAME}]})
    _, local = kit.load_manifest(deposit)
    remote = {'id': 42, 'submitted': False, 'metadata': copy.deepcopy(metadata), 'files': [],
              'links': {'bucket': 'https://zenodo.org/api/files/offline'}}
    calls = []
    class Client:
        def create(self, wanted):
            require(wanted == metadata, 'Stage canonical metadata changed'); calls.append('create'); return copy.deepcopy(remote)
        def get(self, record_id):
            require(record_id == 42, 'Kit requested another deposition'); calls.append('get')
            value = copy.deepcopy(remote)
            if state == 'wrong_remote_id': value['id'] = 43
            if state == 'wrong_submitted_type': value['submitted'] = 0
            return value
        def upload(self, bucket, entry):
            require(bucket == remote['links']['bucket'], 'Wrong bucket'); calls.append('upload')
            remote['files'].append({'filename': entry['name'], 'checksum': 'md5:' + entry['md5'], 'filesize': entry['size']})
        def update(self, record_id, wanted):
            require(record_id == 42 and wanted == metadata, 'Update exact metadata/ID changed'); calls.append('update')
        def publish(self, record_id):
            require(record_id == 42, 'Wrong publish ID'); calls.append('publish')
            remote.update(submitted=True, doi='10.5281/zenodo.42')
            if state == 'lost_publish': raise kit.DepositError('simulated lost POST response')
    state_dir = f.repo / '.zenodo-state'
    args = argparse.Namespace(command='stage', manifest=deposit, sandbox=False, confirm_id=None, check_doi=False)
    with patch.object(kit, 'STATE_DIR', state_dir), patch.object(kit, 'doi_status', lambda doi: {'status': 'offline_mock'}):
        if state in {'wrong_remote_id', 'wrong_submitted_type'}:
            rejection(lambda: kit.run(args, Client())); require(calls.count('publish') == 0, 'Rejected stage published'); return
        staged = kit.run(args, Client()); require(staged['state'] == 'ready_to_publish' and staged['metadata_normalizations'] == [], 'Exact stage rejected')
        args.command = 'publish'; args.confirm_id = 41 if state == 'wrong_confirm' else 42
        if state == 'wrong_confirm':
            rejection(lambda: kit.run(args, Client()), 'confirm-id'); require('publish' not in calls, 'Wrong ID reached publish'); return
        if state == 'metadata_drift':
            remote['metadata']['description'] += 'changed'
            rejection(lambda: kit.run(args, Client()), 'metadata differs'); require('publish' not in calls, 'Bad metadata published'); return
        if state == 'file_md5_drift':
            remote['files'][0]['checksum'] = 'md5:' + '0' * 32
            rejection(lambda: kit.run(args, Client()), 'checksum/size differs'); require('publish' not in calls, 'Bad upload published'); return
        result = kit.run(args, Client()); require(result['state'] == 'published', 'Publication not confirmed')
        require(calls.count('publish') == 1, 'Kit retried unknown POST')
        again = kit.run(args, Client()); require(again['already_published'] is True and calls.count('publish') == 1, 'Already published kit retried')


def integration_flow(f, kind):
    original = (prepared.HEADER + f.receipt['selected_queue_row'] + '\n').encode()
    f.receipt['queue_sha256'] = c.sha(original)
    write_json(f.audit / 'SOURCE_RECEIPT.json', f.receipt); f.seal()
    context, pub = f.publication()
    write_json(f.audit / 'TRACKER_APPEND_RECEIPT.json', {'verified': True, 'spreadsheet_id': c.SHEET,
               'sheet_id': c.TAB_ID, 'tab': c.TAB, 'values': c.tracker_values(context['metadata'], pub['doi_url']),
               'doi': pub['doi_url'], 'updated_range': "'Math Puzzles'!A3:D3",
               'unique_doi_row_at_final_snapshot': True})
    rows, index, cells, columns = c.queue_row(original)
    cells[columns.index('Status')] = ' queued '
    cells[columns.index('Turns')] = ' 0/5 '
    if kind.startswith('main_status_'):
        cells[columns.index('Status')] = ' ' + kind.removeprefix('main_status_') + ' '
    if kind == 'main_different_doi': cells[columns.index('DOI')] = ' https://doi.org/10.5281/zenodo.999 '
    rows[index] = '|' + '|'.join(cells) + '|\n'
    unrelated_row = f.receipt['selected_queue_row'].replace('30004807 /', '99999999 /') + '\n'
    main_queue = (''.join(rows) + unrelated_row).encode()
    original_files = {x['path']: (f.audit / 'source_snapshot' / x['path']).read_bytes() for x in f.receipt['files']}
    original_files[c.QUEUE] = original
    main = 'a' * 40; commit = 'b' * 40; tree = 'c' * 40
    main_files = {c.QUEUE: main_queue, 'unrelated.bin': b'preserve latest main\x00\xff exact binary bytes'}
    state = {'branch': c.ORIGINAL, 'main_reads': 0, 'files': {main: main_files, c.ORIGINAL: original_files},
             'blobs': {}, 'writes': [], 'patches': 0, 'commit_obj': None}
    target = None
    conflicts = {'history': c.PREFIX + 'release/PROOF.md', 'paper': c.PREPRINT + 'manuscript.pdf',
                 'receipt': c.PREPRINT + 'publication_receipts/SOURCE_RECEIPT.json',
                 'math_receipt': c.PREPRINT + 'publication_receipts/MATHEMATICAL_ACCEPTANCE_GATE.json',
                 'acceptance_receipt': c.PREPRINT + 'publication_receipts/FINAL_ACCEPTANCE_GATE.json',
                 'review_receipt': c.PREPRINT + 'publication_receipts/reviews/package_round2/REPORT.md',
                 'ops_receipt': c.PREPRINT + 'publication_receipts/reviews/operations/REPORT.md',
                 'manifest': c.PREFIX + 'PUBLICATION_MANIFEST.json',
                 'landing': c.PREFIX + 'PUBLICATION_NOTES.md'}
    if kind.startswith('conflict_'):
        target = conflicts[kind.removeprefix('conflict_')]; main_files[target] = b'conflicting current-main independent bytes'
    if kind == 'frozen_landing_allowed': main_files[c.PREFIX + 'PUBLICATION_NOTES.md'] = original_files[c.PREFIX + 'PUBLICATION_NOTES.md']
    class Reader:
        def commit(self, revision):
            if revision == main: return {'sha': main, 'tree': {'sha': 'd' * 40}}
            require(revision == commit, 'Unexpected immutable mocked revision')
            return state['commit_obj']
        def entry(self, path, revision):
            data = state['files'][revision].get(path)
            return None if data is None else {'type': 'blob', 'mode': '100644', 'sha': c.git_sha(data)}
        def read(self, path, revision):
            data = state['files'][revision][path]
            if kind == 'binary_drift' and revision == commit and path == c.PREPRINT + 'manuscript.pdf':
                return b'X' + data[1:]
            return data
    reader = Reader()
    def api(endpoint, payload=None, method=None):
        if payload is not None: state['writes'].append(endpoint)
        if endpoint == 'pulls/464':
            return {'number': 464, 'state': 'open', 'draft': True, 'changed_files': 14,
                    'head': {'sha': state['branch'], 'ref': c.BRANCH, 'repo': {'full_name': c.REPO}},
                    'base': {'ref': 'main', 'repo': {'full_name': c.REPO}}}
        if endpoint.startswith('pulls/464/files'):
            return [{'filename': p, 'status': 'modified' if p == c.QUEUE else 'added'} for p in original_files]
        if endpoint == 'git/ref/heads/' + c.BRANCH: return {'object': {'sha': state['branch']}}
        if endpoint == 'git/ref/heads/main':
            state['main_reads'] += 1
            return {'object': {'sha': 'f' * 40 if kind == 'main_advanced' and state['main_reads'] > 1 else main}}
        if endpoint == 'git/blobs':
            require(payload['encoding'] == 'base64', 'Binary blob used incorrect encoding')
            data = base64.b64decode(payload['content']); digest = c.git_sha(data); state['blobs'][digest] = data
            if kind == 'head_advanced': state['branch'] = 'e' * 40
            return {'sha': digest}
        if endpoint == 'git/trees':
            require(payload['base_tree'] == 'd' * 40, 'Git tree not based on captured latest main')
            installed = dict(main_files)
            for item in payload['tree']:
                require(item['mode'] == '100644' and item['type'] == 'blob', 'Unsafe installed Git mode/type')
                installed[item['path']] = state['blobs'][item['sha']]
            state['files'][commit] = installed; return {'sha': tree}
        if endpoint == 'git/commits':
            require(payload['parents'] == [c.ORIGINAL, main] and payload['tree'] == tree, 'Incorrect exact integration ancestry')
            state['commit_obj'] = {'sha': commit, 'tree': {'sha': tree}, 'parents': [{'sha': x} for x in payload['parents']]}
            if kind == 'wrong_parents': state['commit_obj']['parents'].reverse()
            return {'sha': commit}
        if endpoint.startswith('compare/'):
            changed = [{'filename': p, 'status': 'modified' if p in main_files else 'added'}
                       for p, data in state['files'][commit].items() if main_files.get(p) != data]
            if kind == 'unrelated_compare': changed.append({'filename': 'foreign.txt', 'status': 'added'})
            if kind == 'duplicate_compare': changed.append(copy.deepcopy(changed[0]))
            if kind == 'renamed_compare': changed[0].update(status='renamed', previous_filename='foreign.txt')
            return {'base_commit': {'sha': main}, 'merge_base_commit': {'sha': 'e' * 40 if kind == 'wrong_compare_base' else main}, 'files': changed}
        if endpoint == 'git/refs/heads/' + c.BRANCH:
            require(method == 'PATCH' and payload == {'sha': commit, 'force': False}, 'Forced/wrong branch write')
            saved = json.loads((f.audit / 'BRANCH_INTEGRATION_OPERATION.json').read_text())
            require(saved['state'] == 'ref_update_attempted_once' and saved['commit_sha'] == commit, 'Missing durable ref write guard')
            state['patches'] += 1; state['branch'] = commit
            if kind == 'lost_ref_response': raise RuntimeError('simulated lost ref response')
            return {'object': {'sha': commit}}
        raise RuntimeError('Unexpected mocked Git endpoint: ' + endpoint)
    with patch.object(c, 'GitReader', lambda: reader), patch.object(c, 'github', api), \
         patch.object(c, 'confirm_live_publication', lambda ctx: pub), patch.object(c, 'confirm_live_tracker', lambda ctx, p: None):
        if kind in {'identical_manifest_allowed', 'identical_receipt_allowed', 'current_landing_allowed'}:
            _, installed, _, _, _ = integ.prepare()
            target = c.PREFIX + ('PUBLICATION_NOTES.md' if kind == 'current_landing_allowed' else 'PUBLICATION_MANIFEST.json')
            if kind == 'identical_receipt_allowed': target = conflicts['receipt']
            main_files[target] = installed[target]
        early_bad = kind.startswith('conflict_') or kind.startswith('main_status_') or kind == 'main_different_doi'
        later_bad = kind in {'head_advanced', 'main_advanced', 'binary_drift', 'wrong_parents', 'unrelated_compare',
                             'duplicate_compare', 'renamed_compare', 'wrong_compare_base'}
        if kind == 'readonly':
            result = integ.run(False)
            require(result['state'] == 'read_only_preflight' and not state['writes'], 'Default integration mutated')
        elif early_bad or later_bad:
            needle = ('installation destination conflicts' if kind.startswith('conflict_') else
                      'selected disposition changed' if kind.startswith('main_status_') else
                      'different DOI' if kind == 'main_different_doi' else
                      'PR identity' if kind == 'head_advanced' else
                      'Main advanced' if kind == 'main_advanced' else
                      'whole-file readback differs' if kind == 'binary_drift' else
                      'parents differ' if kind == 'wrong_parents' else
                      'compare base/merge base' if kind == 'wrong_compare_base' else 'changed-file set differs')
            rejection(lambda: integ.run(True), needle); require(state['patches'] == 0, 'Rejected integration updated the branch')
            if early_bad: require(not state['writes'], 'Current-main conflict reached remote object creation')
            else:
                rejection(lambda: integ.run(True), 'Prior integration write exists')
                require(state['patches'] == 0, 'Rejected integration blindly retried')
        else:
            result = integ.run(True)
            require(result['state'] == 'branch_updated_verified' and state['patches'] == 1, 'Integration failed exact single update')
            require(state['files'][commit]['unrelated.bin'] == main_files['unrelated.bin'], 'Unrelated latest-main bytes lost')
            before = main_queue.splitlines(keepends=True); after = state['files'][commit][c.QUEUE].splitlines(keepends=True)
            require(len(before) == len(after) and [i for i, pair in enumerate(zip(before, after)) if pair[0] != pair[1]] == [index],
                    'QUEUE mutation was not exactly the selected row')
            require(before[-1] == after[-1], 'Other QUEUE row lost')
            for item in f.receipt['files']:
                original_bytes = original_files[item['path']]
                history = c.PREPRINT + 'verification/frozen_history/' + item['path'].removeprefix(c.PREFIX)
                require(state['files'][commit][history] == original_bytes, 'Frozen original source lost')
            rejection(lambda: integ.run(True), 'Prior integration write exists')
            integ.reconcile(); require(state['patches'] == 1, 'Read-only reconcile repeated ref mutation')


def builder_case(f, name):
    for forbidden_dir in builder.FORBIDDEN:
        payload = f.package / forbidden_dir / 'payload.txt'
        payload.parent.mkdir(exist_ok=True); payload.write_bytes(b'fabricated private test payload')
    (f.package / 'README.md.pyc').write_bytes(b'fabricated bytecode exclusion test')
    (f.package / 'folder').mkdir(exist_ok=True)
    with patch.object(builder, 'PACKAGE', f.package):
        if name == 'valid': require(builder.selected_path('README.md') == f.package / 'README.md', 'Builder rejected canonical file'); return
        needle = 'Excluded selected' if any(part in builder.FORBIDDEN for part in name.split('/')) or name.endswith('.pyc') else (
                 'Invalid selected' if not name or '\\' in name or any(ord(x) < 32 for x in name) else 'Noncanonical selected')
        rejection(lambda: builder.selected_path(name), needle)


def eligibility_attack(f, kind):
    queue = (prepared.HEADER + f.receipt['selected_queue_row'] + '\n').encode()
    f.receipt['queue_sha256'] = c.sha(queue); write_json(f.audit / 'SOURCE_RECEIPT.json', f.receipt)
    files = {x['path']: (f.audit / 'source_snapshot' / x['path']).read_bytes() for x in f.receipt['files']}
    files[c.QUEUE] = queue
    pr = {'number': 464, 'state': 'open', 'draft': True, 'changed_files': 14,
          'head': {'sha': c.ORIGINAL, 'ref': c.BRANCH, 'repo': {'full_name': c.REPO}},
          'base': {'ref': 'main', 'repo': {'full_name': c.REPO}}}
    changes = [{'filename': p, 'status': 'modified' if p == c.QUEUE else 'added'} for p in files]
    ref = c.ORIGINAL
    if kind.startswith('status_'): files[c.QUEUE] = queue.replace(b'claimed_solved', kind.removeprefix('status_').encode())
    if kind == 'turns': files[c.QUEUE] = queue.replace(b'1/5', b'2/5')
    if kind == 'source': files[next(p for p in files if p != c.QUEUE)] += b'changed'
    if kind == 'closed': pr['state'] = 'closed'
    if kind == 'not_draft': pr['draft'] = False
    if kind == 'head': pr['head']['sha'] = 'f' * 40
    if kind == 'ref': ref = 'f' * 40
    if kind == 'branch': pr['head']['ref'] = 'other-branch'
    if kind == 'base': pr['base']['ref'] = 'other-base'
    if kind == 'repo': pr['head']['repo']['full_name'] = 'other/repo'
    if kind == 'base_repo': pr['base']['repo']['full_name'] = 'other/repo'
    if kind == 'truncated': changes.pop()
    if kind == 'rename': changes[0]['previous_filename'] = 'other.txt'
    if kind == 'unrelated': changes[0]['filename'] = 'unrelated.txt'
    class Reader:
        def read(self, path, revision):
            require(revision == c.ORIGINAL, 'Live check did not use immutable eligible original'); return files[path]
    def api(endpoint):
        if endpoint == 'pulls/464': return pr
        if endpoint == 'git/ref/heads/' + c.BRANCH: return {'object': {'sha': ref}}
        if endpoint.startswith('pulls/464/files'): return changes
        raise RuntimeError('Unexpected eligibility API path')
    with patch.object(c, 'github', api):
        if kind == 'valid': c.live_eligibility(Reader()); return
        needle = ('problem is excluded' if kind.startswith('status_') or kind == 'turns' else
                  'source bytes differ' if kind == 'source' else 'branch ref moved' if kind == 'ref' else
                  'list is truncated' if kind == 'truncated' else 'rename semantics' if kind == 'rename' else
                  'changed-file set differs' if kind == 'unrelated' else 'PR identity')
        rejection(lambda: c.live_eligibility(Reader()), needle)


def sheet_schema_case(f, kind):
    response = {'spreadsheetId': c.SHEET, 'sheets': [{'properties': {'sheetId': c.TAB_ID, 'title': c.TAB}}]}
    header = [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']]
    if kind == 'sheet': response['spreadsheetId'] = 'another-sheet'
    if kind == 'gid': response['sheets'][0]['properties']['sheetId'] += 1
    if kind == 'tab': response['sheets'][0]['properties']['title'] = 'Other tab'
    if kind == 'duplicate_gid': response['sheets'].append(copy.deepcopy(response['sheets'][0]))
    if kind == 'header': header[0][-1] = 'Wrong notes'
    calls = []
    def gws(action, params, body=None, resource='values'):
        calls.append((action, params, body, resource))
        require(action == 'get' and body is None and params['spreadsheetId'] == c.SHEET, 'Schema check mutated service')
        return copy.deepcopy(response) if resource == 'spreadsheets' else {'values': copy.deepcopy(header)}
    with patch.object(c, 'gws', gws):
        if kind == 'valid': c.check_sheet()
        else: rejection(c.check_sheet, 'spreadsheet' if kind == 'sheet' else 'header' if kind == 'header' else 'gid')


def kit_cli_case(f, kind):
    context = c.validate_gate()
    response = {'environment': 'production', 'title': context['metadata']['title'], 'metadata_normalizations': [],
                'files': list(c.expected_public_files(context).values()), 'state': 'ready_to_publish', 'id': 123456}
    if kind == 'sandbox': response['environment'] = 'sandbox'
    if kind == 'title': response['title'] += ' changed'
    if kind == 'file_sha': response['files'][0]['sha256'] = '0' * 64
    if kind == 'normalization': response['metadata_normalizations'] = [{'field': 'description'}]
    def run(args, **kwargs):
        require(args[:4] == [sys.executable, str(context['kit']), 'inspect', str(f.package / 'deposit.json')]
                and args[4:] == ['--check-doi'] and '--sandbox' not in args, 'Kit invoked wrong file/environment/operation')
        return argparse.Namespace(returncode=0, stdout=json.dumps(response))
    with patch.object(z.subprocess, 'run', run):
        if kind == 'valid':
            out = z.kit_cli(context, 'inspect')
            require(out['canonical_metadata_sha256'] == c.sha((f.package / 'metadata.json').read_bytes()), 'Canonical metadata not bound')
        else:
            rejection(lambda: z.kit_cli(context, 'inspect'), 'metadata changed' if kind == 'normalization' else 'files differ' if kind == 'file_sha' else 'production/title')


def builder_write_boundary(f, name):
    # Generated output paths are a different boundary from selected payloads.
    # No real accepted source/package is used: this entire fixture is private.
    (f.package / 'CURRENT_PUBLICATION_NOTES.md').write_bytes(b'valid offline current note')
    write_json(f.package / 'verification/PUBLIC_OUTPUT_WHITELIST.json', {'positive_whitelist_only': True, 'public_files': []})
    write_json(f.package / 'REVIEW_EVIDENCE_SELECTION.json', {'positive_explicit_selection': True, 'entries': []})
    target = f.audit / 'outside_package_sentinel.txt'
    sentinel = b'preserve unrelated local target exactly\n'; target.write_bytes(sentinel)
    if name == 'existing_freeze':
        arguments = ['builder', '--freeze', '2']
        before = {p.relative_to(f.audit).as_posix(): p.read_bytes() for p in f.audit.rglob('*') if p.is_file()}
    else:
        output = f.audit / 'BRANCH_INSTALL_PLAN.json' if name == 'BRANCH_INSTALL_PLAN.json' else f.package / name
        if output.exists(): output.unlink()
        output.symlink_to(target)
        arguments = ['builder']
    with patch.multiple(builder, ROOT=f.audit, PACKAGE=f.package), patch.object(sys, 'argv', arguments), \
         contextlib.redirect_stdout(io.StringIO()):
        try:
            builder.main()
        except RuntimeError as error:
            rejected = True; message = str(error)
        else:
            rejected = False; message = None
    if name == 'existing_freeze':
        after = {p.relative_to(f.audit).as_posix(): p.read_bytes() for p in f.audit.rglob('*') if p.is_file()}
        changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
        ATTACK_OBSERVATIONS.append({'case': 'builder_write_boundary_' + name, 'builder_rejected': rejected,
                                   'rejection': message, 'current_output_changed_paths': changed,
                                   'existing_frozen_review_unchanged': before[f.manifest_name] == after[f.manifest_name],
                                   'private_fixture_only': True, 'real_external_calls': 0})
        require(before == after, 'Existing immutable freeze rejection occurs after builder changed current outputs')
    else:
        ATTACK_OBSERVATIONS.append({'case': 'builder_write_boundary_' + name, 'builder_rejected': rejected,
                                   'rejection': message, 'unrelated_local_target_bytes_changed': target.read_bytes() != sentinel,
                                   'private_fixture_only': True, 'real_external_calls': 0})
        require(target.read_bytes() == sentinel, 'Builder followed generated-output symlink and clobbered unrelated local bytes before rejection')
        require(rejected, 'Generated-output symlink was not rejected')


def main():
    case('fully_bound_positive_baseline', lambda f: require(len(c.validate_gate()['installs']) >= 13, 'Positive baseline rejected'))
    for field in ('source_receipt_sha256', 'mathematical_acceptance_gate_sha256', 'branch_install_plan_sha256'):
        case('freeze_kept_constant_current_' + field + '_changed', lambda f, field=field: freeze_cross(f, field))
    for field, wrong in [('pr', 466), ('problem', '30000999'), ('original_head', 'f' * 40)]:
        def mutate(f, field=field, wrong=wrong):
            freeze = json.loads((f.audit / f.manifest_name).read_text()); freeze[field] = wrong
            write_json(f.audit / f.manifest_name, freeze); update_freeze_hash(f)
            rejection(c.validate_gate, 'freeze PR/problem/original-head identity')
        case('freeze_identity_' + field, mutate)
    for number in (False, True, 0.0, '0', None, -1, 1):
        for target in ('blocking_issue_count', 'required_correction_count'):
            case('review_count_' + target + '_' + repr(number), lambda f, number=number, target=target:
                 gate_attack(f, lambda g: g.gate['complete_package_reviews'][-1].__setitem__(target, number)))
    for state in ('not_pass', 'duplicate_identity', 'gap', 'wrong_manifest', 'one_review', 'bad_round_type'):
        def change(f, state=state):
            last = f.gate['complete_package_reviews'][-1]
            if state == 'not_pass': last['verdict'] = 'REQUEST_CHANGES'
            if state == 'duplicate_identity': last['identity'] = 'offline_mock_1'
            if state == 'gap': last['round'] = 4
            if state == 'wrong_manifest': last['input_manifest_sha256'] = '0' * 64
            if state == 'one_review': f.gate['complete_package_reviews'].pop()
            if state == 'bad_round_type': last['round'] = True
        case('successive_fresh_gate_' + state, lambda f, change=change: gate_attack(f, change))
    for state in ('local_payload_drift', 'unplanned', 'traversal', 'private', 'environment', 'circular', 'symlink', 'duplicate'):
        case('archive_' + state, lambda f, state=state: archive_attack(f, state))
    for name in ('operations/common.py', 'operations/zenodo_pr464.py', 'operations/register_pr464_tracker.py',
                 'operations/integrate_pr464_publication.py'):
        case('reviewed_helper_drift_' + name, lambda f, name=name: gate_attack(f, lambda g: (g.audit / name).write_bytes(b'drift')))
    for state in ('existing_exact', 'existing_changed', 'duplicate_alias', 'prior_verified_removed', 'receipt_removed',
                  'prior_uncertain_removed', 'prior_exact', 'concurrent_before_append', 'duplicate_after_append',
                  'lost_success', 'lost_failure', 'wrong_count_type', 'wrong_range', 'new'):
        case('tracker_' + state, lambda f, state=state: tracker_scenario(f, state))
    for state in ('new', 'prior_verified_removed', 'receipt_removed', 'prior_uncertain_removed', 'prior_exact'):
        case('tracker_readonly_' + state, lambda f, state=state: tracker_scenario(f, state, False))
    for state in ('valid', 'wrong_id', 'wrong_title', 'extra_file', 'file_drift', 'same_length_drift'):
        case('public_download_' + state, lambda f, state=state: public_readback_case(f, state))
    for state in ('default', 'publish', 'lost_stage', 'lost_publish', 'wrong_id'):
        case('zenodo_wrapper_' + state, lambda f, state=state: wrapper_flow(f, state))
    for state in ('valid', 'lost_publish', 'wrong_confirm', 'metadata_drift', 'file_md5_drift', 'wrong_remote_id', 'wrong_submitted_type'):
        case('unchanged_real_kit_' + state, lambda f, state=state: real_kit_case(f, state))
    for state in ('readonly', 'valid', 'lost_ref_response', 'head_advanced', 'main_advanced', 'binary_drift', 'wrong_parents',
                  'unrelated_compare', 'duplicate_compare', 'renamed_compare', 'wrong_compare_base', 'main_different_doi',
                  'main_status_unsolved', 'main_status_already_solved', 'main_status_in_progress', 'main_status_',
                  'conflict_history', 'conflict_paper', 'conflict_receipt', 'conflict_math_receipt', 'conflict_acceptance_receipt',
                  'conflict_review_receipt', 'conflict_ops_receipt', 'conflict_manifest', 'conflict_landing',
                  'frozen_landing_allowed', 'identical_manifest_allowed', 'identical_receipt_allowed', 'current_landing_allowed'):
        case('integration_' + state, lambda f, state=state: integration_flow(f, state))
    for name in ('valid', 'venv/payload.txt', '.venv/payload.txt', 'private_cases/payload.txt', 'private_sources/payload.txt',
                 'mutation_fixtures/payload.txt', '.secrets/payload.txt', '.zenodo-state/payload.txt', '__pycache__/payload.txt',
                 'README.md.pyc', './README.md', 'folder/../README.md', 'folder//README.md', 'folder/./README.md', '../README.md',
                 '/absolute', 'a\\b', 'a\x00b', 'a\nb', ''):
        case('builder_selected_path_' + repr(name), lambda f, name=name: builder_case(f, name))
    for state in ('valid', 'status_unsolved', 'status_already_solved', 'status_claimed_partial', 'status_', 'turns', 'source',
                  'closed', 'not_draft', 'head', 'ref', 'branch', 'base', 'repo', 'base_repo', 'truncated', 'rename', 'unrelated'):
        case('live_eligibility_' + state, lambda f, state=state: eligibility_attack(f, state))
    for state in ('valid', 'sheet', 'gid', 'tab', 'duplicate_gid', 'header'):
        case('native_tracker_schema_' + state, lambda f, state=state: sheet_schema_case(f, state))
    for state in ('valid', 'sandbox', 'title', 'file_sha', 'normalization'):
        case('actual_kit_cli_' + state, lambda f, state=state: kit_cli_case(f, state))
    for name in ('SHA256SUMS.json', c.ZIP_NAME, 'ARCHIVE_RECEIPT.json', 'deposit.json', 'BRANCH_INSTALL_PLAN.json', 'existing_freeze'):
        case('builder_write_boundary_' + name, lambda f, name=name: builder_write_boundary(f, name))
    result = {'scope': 'Fresh reviewer-written offline adversarial controls; all service data are mocks, not production evidence.',
              'case_count': len(CASES), 'all_passed': all(x['passed'] for x in CASES),
              'passed_count': sum(x['passed'] for x in CASES), 'real_external_calls': len(REAL_CALLS), 'cases': CASES,
              'independent_failure_observations': ATTACK_OBSERVATIONS,
              'limits': 'Finite controls; no mathematical/full-paper acceptance or global atomic concurrency guarantee.'}
    suffix = 'OPTIMIZED' if not __debug__ else 'NORMAL'
    (HERE / ('INDEPENDENT_CONTROLS_' + suffix + '.json')).write_bytes(c.json_bytes(result))
    print(json.dumps({k: result[k] for k in ('case_count', 'all_passed', 'passed_count', 'real_external_calls')}, sort_keys=True))
    if not result['all_passed'] or result['real_external_calls'] != 0:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
