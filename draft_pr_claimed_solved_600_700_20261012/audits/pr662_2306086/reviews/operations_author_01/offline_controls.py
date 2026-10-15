#!/usr/bin/env python3
"""Adversarial offline controls: no live API, network, push, or append.

The real native bytes and source snapshot are read only. Synthetic publication
and service fixtures are isolated here; Git tests use a disposable toy repository.
The integration lifecycle service/replay doubles are explicitly identified below.
"""
import contextlib
import copy
import datetime
import hashlib
import importlib.util
import io
import json
import marshal
import os
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile
import types
import warnings
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
AUDIT = HERE.parents[1]
TMP = HERE / 'tmp'
TMP.mkdir(exist_ok=True)


def source_module(path, name):
    module = types.ModuleType(name); module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


M = source_module(AUDIT / 'prepare_integration.py', '_offline_integration')
T = source_module(AUDIT / 'record_tracker.py', '_offline_tracker')
ORIGINAL, SNAPSHOT, SNAPSHOT_BYTES = M.load_snapshot()
DOI = '10.5281/zenodo.999999999'
checks = []


def check(label, condition):
    if not condition:
        raise ValueError('control failed: ' + label)
    checks.append({'label': label, 'status': 'PASS'})


def rejects(label, function):
    try:
        function()
    except (ValueError, KeyError, FileNotFoundError, OSError, zipfile.BadZipFile, TypeError):
        checks.append({'label': label, 'status': 'REJECTED_AS_REQUIRED'})
    else:
        raise ValueError('negative control accepted: ' + label)


@contextlib.contextmanager
def patched(module, **values):
    old = {key: getattr(module, key) for key in values}
    for key, value in values.items(): setattr(module, key, value)
    try:
        yield
    finally:
        for key, value in old.items(): setattr(module, key, value)


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def fixture(root):
    for name, data in ORIGINAL.items(): write(root / 'native' / M.PREFIX / name, data)
    write(root / 'SCOPE_AND_SNAPSHOT.json', SNAPSHOT_BYTES)
    actual = AUDIT / 'publication'
    files = {name: (b'%PDF-1.5\nsynthetic offline fixture\n' if name.endswith('.pdf') else
                    b'\\documentclass{article}\n' if name.endswith('.tex') else
                    b'placeholder\n' if name.endswith('.zip') else
                    (actual / name).read_bytes()) for name in M.PUB_NAMES}
    files['CLAIM_SCOPE.json'] = M.json_bytes(M.EXPECTED_SCOPE)
    payload = {'native/' + M.PREFIX + name: data for name, data in ORIGINAL.items()}
    payload['SCOPE_AND_SNAPSHOT.json'] = SNAPSHOT_BYTES
    payload.update({('README.md' if name == 'PACKAGE_README.md' else name): data
                    for name, data in files.items() if not name.endswith('.zip')})
    files['real_schlicht_verification.zip'] = zip_payload(payload)
    for name, data in files.items(): write(root / 'publication' / name, data)
    rounds = []
    for index in (1, 2):
        name = f'reviews/round{index}/VERDICT.json'; data = M.json_bytes({'reviewer': f'offline-{index}', 'findings': []})
        write(root / name, data)
        rounds.append({'reviewer_id': f'offline-reviewer-{index}', 'report_path': name, 'report_sha256': M.sha(data),
                       'mandatory_findings': 0, 'optional_findings': 0})
    accepted = {'schema': 'pr662-accepted-publication-inputs-v1', 'pr': 662, 'problem_id': '2306086',
        'original_head': M.ORIGINAL, 'ready_for_publication': True, 'whole_package_review_rounds': rounds,
        'files': {name: {'bytes': len(data), 'sha256': M.sha(data)} for name, data in files.items()}}
    write(root / 'ACCEPTED_PUBLICATION_INPUTS.json', M.json_bytes(accepted))
    receipt = {'environment': 'production', 'state': 'published', 'receipt_saved': True, 'title': M.TITLE,
        'id': 999999999, 'doi': DOI, 'doi_url': 'https://doi.org/' + DOI,
        'record_url': 'https://zenodo.org/records/999999999', 'verified_utc': '2026-10-15T00:00:00+00:00',
        'doi_resolution': {'status': 'resolved', 'http_status': 200}, 'metadata_normalizations': [],
        'files': [{'name': name, 'size': len(files[name]), 'sha256': M.sha(files[name])} for name in M.UPLOAD_NAMES]}
    write(root / 'ZENODO_PUBLICATION_RECEIPT.json', M.json_bytes(receipt))
    write(root / 'ZENODO_POST_PUBLICATION_INSPECTION.json', M.json_bytes(receipt | {'verified_utc': '2026-10-15T00:01:00+00:00'}))
    return files, payload, accepted, receipt


def zip_payload(payload, mode=stat.S_IFREG | 0o644, duplicate=None, extra=None, manifest_mutator=None):
    manifest = {'schema': 1, 'problem_id': '2306086', 'original_head': M.ORIGINAL,
        'file_count': len(payload), 'raw_third_party_fulltexts_included': False,
        'files': [{'path': name, 'bytes': len(data), 'sha256': M.sha(data)} for name, data in sorted(payload.items())]}
    if manifest_mutator: manifest_mutator(manifest)
    body = dict(payload); body['PACKAGE_MANIFEST.json'] = M.json_bytes(manifest)
    if extra: body.update(extra)
    stream = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(body.items()):
                entry = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0)); entry.external_attr = mode << 16
                archive.writestr(entry, data)
            if duplicate:
                entry = zipfile.ZipInfo(duplicate); entry.external_attr = mode << 16
                archive.writestr(entry, body[duplicate])
    return stream.getvalue()


def publication_controls():
    for encoded in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}'):
        rejects('JSON duplicate/nonfinite ' + encoded.decode(), lambda data=encoded: M.parse_json(data))
    for name in ('', '.', '..', '../x', 'x/../y', '/x', 'a//b', 'a\\b', 'a:b', 'a\nb'):
        rejects('unsafe path ' + repr(name), lambda name=name: M.safe_name(name))
    meta = {'number': 662, 'state': 'OPEN', 'isDraft': True, 'baseRefName': 'main', 'headRefName': M.BRANCH,
            'headRefOid': M.ORIGINAL, 'isCrossRepository': False, 'headRepositoryOwner': {'login': 'AlecKriebel'}}
    check('original draft identity accepted', M.check_known_head(meta) == M.ORIGINAL)
    for key, value in (('number', 661), ('state', 'CLOSED'), ('isDraft', False), ('baseRefName', 'other'),
                       ('headRefName', 'other'), ('headRefOid', '0' * 40), ('isCrossRepository', True),
                       ('headRepositoryOwner', {'login': 'other'})):
        rejects('live PR drift ' + key, lambda key=key, value=value: M.check_known_head(meta | {key: value}))
    fetch_calls = []
    def raced_fetch(*args, input=None):
        fetch_calls.append(args[0])
        if args[0] == 'fetch':
            raise subprocess.CalledProcessError(1, ['git', 'fetch'], stderr=(
                b"error: cannot lock ref 'refs/remotes/origin/main': is at " + b'a' * 40 + b' but expected ' + b'b' * 40))
        if args[0] == 'ls-remote': return b'a' * 40 + b'\trefs/heads/main\n'
        return b'a' * 40 + b'\n'
    with patched(M, git=raced_fetch):
        fetched, receipt = M.fetch_main()
        check('concurrent ref CAS reconciles only exact advertised main', fetched == 'a' * 40
              and receipt['concurrent_fetch_ref_CAS_reconciled_by_exact_readback'] is True and fetch_calls.count('fetch') == 1)
    def mismatch_fetch(*args, input=None):
        if args[0] == 'rev-parse': return b'c' * 40 + b'\n'
        return raced_fetch(*args, input=input)
    with patched(M, git=mismatch_fetch): rejects('fetch CAS mismatched identity fails closed', M.fetch_main)
    def other_fetch_error(*args, input=None):
        raise subprocess.CalledProcessError(1, ['git', 'fetch'], stderr=b'network unavailable')
    with patched(M, git=other_fetch_error): rejects('unrecognized fetch failure has no cleanup or retry', M.fetch_main)
    selected = SNAPSHOT['queue_row'].encode() + b'\n'
    _, _, _, cells = M.queue_row(selected)
    cells[8], cells[9], cells[11] = b' queued ', b' 0/5 ', b'  '
    queued = b'|'.join(cells) + b'\n'
    context = b'Untouched prefix\r\n' + queued + b'Untouched suffix\n'
    after, patch = M.patch_queue(context, DOI, SNAPSHOT['queue_row'])
    check('queue only target row and three cells change', after.startswith(b'Untouched prefix\r\n')
          and after.endswith(b'Untouched suffix\n') and patch['changed_cells'] == ['Status', 'Turns', 'Findings'])
    _, _, _, accepted_cells = M.queue_row(after)
    check('queue retains reviewed claimed_solved 5/5 semantics', accepted_cells[8].strip() == b'claimed_solved'
          and accepted_cells[9].strip() == b'5/5' and all(accepted_cells[j] == cells[j] for j in range(14) if j not in (8, 9, 11)))
    for label, data in (('duplicate target', queued + queued), ('already integrated target', selected),
                        ('changed identity field', queued.replace(b'0.1050', b'0.1051')),
                        ('other status', queued.replace(b' queued ', b' unsolved '))):
        rejects('queue fail closed ' + label, lambda data=data: M.patch_queue(data, DOI, SNAPSHOT['queue_row']))
    with tempfile.TemporaryDirectory(prefix='inputs-', dir=TMP) as temporary:
        root = Path(temporary); files, payload, accepted, receipt = fixture(root)
        with patched(M, A=root, ACCEPTANCE=root / 'ACCEPTED_PUBLICATION_INPUTS.json'):
            def inputs():
                return M.publication_inputs(root / 'publication', DOI, root / 'ZENODO_PUBLICATION_RECEIPT.json',
                                            root / 'ZENODO_POST_PUBLICATION_INSPECTION.json')
            good = inputs()
            check('accepted eleven inputs and original24 bind exact archive', len(good['files']) == 11
                  and len(good['original']) == 24 and good['validation']['archive_binding']['original_candidate_files_bound'] == 24)
            for label, mutate in (
                ('not accepted', lambda gate: gate.update(ready_for_publication=False)),
                ('only one round', lambda gate: gate.update(whole_package_review_rounds=gate['whole_package_review_rounds'][:1])),
                ('same reviewer', lambda gate: gate['whole_package_review_rounds'][1].update(reviewer_id='offline-reviewer-1')),
                ('same report', lambda gate: gate['whole_package_review_rounds'][1].update(report_path=gate['whole_package_review_rounds'][0]['report_path'])),
                ('mandatory unresolved', lambda gate: gate['whole_package_review_rounds'][1].update(mandatory_findings=1)),
                ('optional unresolved', lambda gate: gate['whole_package_review_rounds'][1].update(optional_findings=1)),
                ('bool finding count', lambda gate: gate['whole_package_review_rounds'][1].update(optional_findings=False)),
                ('extra accepted file', lambda gate: gate['files'].update(extra={'bytes': 0, 'sha256': '0' * 64})),
                ('missing accepted file', lambda gate: gate['files'].pop('real_schlicht_preschwarzian.tex')),
                ('unsafe report path', lambda gate: gate['whole_package_review_rounds'][0].update(report_path='../outside')),
            ):
                changed = copy.deepcopy(accepted); mutate(changed)
                write(M.ACCEPTANCE, M.json_bytes(changed)); rejects('accepted gate ' + label, inputs)
            write(M.ACCEPTANCE, M.json_bytes(accepted))
            paper = root / 'publication/real_schlicht_preschwarzian.pdf'
            write(paper, files[paper.name] + b'changed'); rejects('unreviewed paper bytes', inputs); write(paper, files[paper.name])
            report = root / accepted['whole_package_review_rounds'][0]['report_path']
            old = report.read_bytes(); write(report, old + b'changed'); rejects('changed review report', inputs); write(report, old)
            original_path = root / 'native' / M.PREFIX / 'README.md'
            old = original_path.read_bytes(); write(original_path, old + b'changed'); rejects('changed native original', inputs); write(original_path, old)
            extra = original_path.with_name('EXTRA'); write(extra, b'bad'); rejects('extra native file', inputs); extra.unlink()
            empty = original_path.with_name('EMPTY'); empty.mkdir(); rejects('extra native empty directory', inputs); empty.rmdir()
            target = root / 'ZENODO_POST_PUBLICATION_INSPECTION.json'; original_receipt = target.read_bytes()
            for label, change in (
                ('wrong DOI', {'doi': '10.5281/zenodo.1'}), ('wrong ID', {'id': 1}),
                ('sandbox', {'environment': 'sandbox'}), ('unpublished', {'state': 'draft'}),
                ('unresolved DOI', {'doi_resolution': {'status': 'unresolved', 'http_status': 200}}),
                ('bool HTTP status', {'doi_resolution': {'status': 'resolved', 'http_status': True}}),
                ('unreviewed normalization', {'metadata_normalizations': ['changed']}),
                ('wrong file bytes', {'files': [dict(receipt['files'][0], sha256='0' * 64), receipt['files'][1]]}),
                ('duplicate upload names', {'files': [receipt['files'][0], receipt['files'][0]]}),
            ):
                write(target, M.json_bytes(receipt | change | {'verified_utc': 'different'})); rejects('receipt ' + label, inputs)
            write(target, (root / 'ZENODO_PUBLICATION_RECEIPT.json').read_bytes()); rejects('copied rather than independent inspection', inputs)
            write(target, original_receipt)
            for label, mutate in (
                ('extra scope claim', lambda scope: scope.update(extra_claim=True)),
                ('sharp radius inflation', lambda scope: scope.update(sharp_quantitative_radius=True)),
                ('zero boolean substitution', lambda scope: scope.update(source_expression_at_zero=False)),
            ):
                altered = copy.deepcopy(M.EXPECTED_SCOPE); mutate(altered)
                new_files = dict(files); new_files['CLAIM_SCOPE.json'] = M.json_bytes(altered)
                gate = copy.deepcopy(accepted); gate['files']['CLAIM_SCOPE.json'] = {'bytes': len(new_files['CLAIM_SCOPE.json']), 'sha256': M.sha(new_files['CLAIM_SCOPE.json'])}
                write(root / 'publication/CLAIM_SCOPE.json', new_files['CLAIM_SCOPE.json']); write(M.ACCEPTANCE, M.json_bytes(gate))
                rejects('scope ' + label + ' even with accepted outer pin updated', inputs)
            write(root / 'publication/CLAIM_SCOPE.json', files['CLAIM_SCOPE.json']); write(M.ACCEPTANCE, M.json_bytes(accepted))
            check('input controls leave accepted fixture unchanged', inputs()['validation'] == good['validation'])
        for label, altered in (
            ('duplicate member', zip_payload(payload, duplicate='CLAIM_SCOPE.json')),
            ('symlink members', zip_payload(payload, mode=stat.S_IFLNK | 0o777)),
            ('untyped file members', zip_payload(payload, mode=0o644)),
            ('unsafe extra member', zip_payload(payload, extra={'../escape': b'bad'})),
            ('unmanifested member', zip_payload(payload, extra={'extra': b'bad'})),
            ('wrong original head', zip_payload(payload, manifest_mutator=lambda value: value.update(original_head='0' * 40))),
            ('missing manifest entry', zip_payload(payload, manifest_mutator=lambda value: value['files'].pop())),
            ('third-party fulltexts flag', zip_payload(payload, manifest_mutator=lambda value: value.update(raw_third_party_fulltexts_included=True))),
        ):
            rejects('archive ' + label, lambda data=altered: M.archive_binding(data, ORIGINAL, files, SNAPSHOT_BYTES))
        for name in ('native/' + M.PREFIX + 'README.md', 'CURRENT_PRIORITY_AND_STATUS.md', 'real_schlicht_preschwarzian.pdf'):
            altered = dict(payload); altered[name] += b'changed'
            rejects('archive rebased manifest cannot hide changed ' + name,
                    lambda data=zip_payload(altered): M.archive_binding(data, ORIGINAL, files, SNAPSHOT_BYTES))
        altered = dict(payload); altered['native/unexpected'] = b'bad'
        rejects('archive extra native path despite rebased manifest', lambda: M.archive_binding(zip_payload(altered), ORIGINAL, files, SNAPSHOT_BYTES))


class FakeSheet:
    def __init__(self, pending, fault=None):
        self.pending = pending; self.fault = fault; self.values = [T.HEADERS[:]]; self.append_count = 0; self.calls = []

    def call(self, resource, method, params, body=None):
        self.calls.append((resource, method, params, body))
        if resource == 'spreadsheets':
            return {'sheets': [{'properties': {'sheetId': 1 if self.fault == 'wrong_gid' else T.GID, 'title': T.TAB}}]}
        if method == 'append':
            self.append_count += 1
            check('append durable intent exists before dispatch ' + str(len(checks)), self.pending.exists()
                  and json.loads(self.pending.read_bytes())['action_outcome'].startswith('unconfirmed'))
            check('append exact RAW INSERT_ROWS echo flags ' + str(len(checks)), params['valueInputOption'] == 'RAW'
                  and params['insertDataOption'] == 'INSERT_ROWS' and params['includeValuesInResponse'] is True
                  and body == {'majorDimension': 'ROWS', 'values': [T.wanted_row(DOI)]})
            if self.fault == 'uncertain_absent': raise OSError('simulated timeout before observable append')
            self.values.append(copy.deepcopy(body['values'][0])); number = len(self.values)
            if self.fault == 'uncertain_present': raise OSError('simulated timeout after append')
            target = f"'Math Puzzles'!A{number}:D{number}"
            response = {'spreadsheetId': T.ID, 'updates': {'updatedRange': target, 'updatedRows': 1,
                'updatedColumns': 4, 'updatedCells': 4, 'updatedData': {'values': copy.deepcopy(body['values'])}}}
            if self.fault == 'wrong_range': response['updates']['updatedRange'] = "'Math Puzzles'!A1:D1"
            if self.fault == 'wrong_cells': response['updates']['updatedCells'] = 3
            if self.fault == 'wrong_echo': response['updates']['updatedData']['values'] = [['wrong']]
            if self.fault == 'wrong_spreadsheet': response['spreadsheetId'] = 'wrong'
            if self.fault == 'duplicate_after': self.values.append(copy.deepcopy(body['values'][0]))
            return response
        if params['range'].endswith('A1:D1'):
            return {'values': [['wrong']] if self.fault == 'wrong_headers' else [T.HEADERS[:] ]}
        if params['range'].endswith('A:D'):
            return {'values': copy.deepcopy(self.values)}
        if self.fault == 'wrong_readback': return {'values': [['wrong']]}
        return {'values': [copy.deepcopy(self.values[int(params['range'].split('!A')[1].split(':')[0]) - 1])]}


def tracker_controls():
    row = T.wanted_row(DOI)
    check('tracker blank chat and bounded priority wording', row[1] == '' and 'Jenkins (1960)' in row[3]
          and 'unrefereed' in row[3] and 'current-openness guarantee' in row[3])
    for value in (DOI, 'https://doi.org/' + DOI, 'HTTP://DX.DOI.ORG/' + DOI.upper() + '/', 'doi: ' + DOI):
        check('DOI canonical duplicate variant ' + value, T.doi_matches([T.HEADERS, ['', '', value]], DOI) == [2])
    for fault in (None, 'wrong_gid', 'wrong_headers', 'uncertain_absent', 'uncertain_present', 'wrong_range',
                  'wrong_cells', 'wrong_echo', 'wrong_spreadsheet', 'wrong_readback', 'duplicate_after'):
        with tempfile.TemporaryDirectory(prefix='tracker-', dir=TMP) as temporary:
            root = Path(temporary); pending = root / 'TRACKER_UNCONFIRMED.json'; service = FakeSheet(pending, fault)
            ready = {'schema': 'pr662-tracker-row-receipt-v1', 'doi': DOI, 'row': row,
                     'publication_validation': {'accepted': 'offline-fixture'}}
            with patched(T, A=root, PENDING=pending, call=service.call):
                if fault is None:
                    receipt = T.append_once(ready)
                    check('one append and verified unique row', receipt['global_exact_doi_rows'] == [2] and service.append_count == 1)
                    again = T.append_once(ready)
                    check('confirmed existing row is idempotent read-only', again['already_present'] is True and service.append_count == 1)
                else:
                    rejects('tracker fail closed ' + fault, lambda: T.append_once(ready))
                    if fault not in ('wrong_gid', 'wrong_headers'):
                        check('sticky marker survives ' + fault, pending.exists()
                              and json.loads(pending.read_bytes())['action_outcome'].startswith('unconfirmed'))
                    if fault == 'uncertain_absent':
                        rejects('uncertain absent append cannot be retried', lambda: T.append_once(ready))
                        check('no second uncertain append', service.append_count == 1)
                    elif fault == 'uncertain_present':
                        service.fault = None
                        reconciled = T.append_once(ready)
                        check('uncertain present append reconciles only by reads', reconciled['already_present'] is True
                              and service.append_count == 1 and json.loads(pending.read_bytes())['action_outcome'] == 'confirmed')
    rejects('duplicate existing DOI rejected', lambda: T.exact_existing([T.HEADERS, row, row], row, DOI))
    rejects('existing DOI with conflicting notes rejected', lambda: T.exact_existing([T.HEADERS, row[:3] + ['different']], row, DOI))
    with tempfile.TemporaryDirectory(prefix='tracker-main-', dir=TMP) as temporary:
        root = Path(temporary); pending = root / 'TRACKER_UNCONFIRMED.json'; service = FakeSheet(pending)
        with patched(T, A=root, PENDING=pending, call=service.call,
                     publication_inputs=lambda *args: {'validation': {'offline': True}}), patched(T._dependency, A=root):
            before = sys.argv
            try:
                sys.argv = ['record_tracker.py', '--doi', DOI]
                with contextlib.redirect_stdout(io.StringIO()): T.main()
            finally: sys.argv = before
            check('tracker default has no append or pending intent', service.append_count == 0 and not pending.exists()
                  and (root / 'TRACKER_ROW_READY.json').is_file())
            check('tracker records exact captured dependency SHA', json.loads((root / 'TRACKER_ROW_READY.json').read_bytes())['integration_helper_sha256']
                  == hashlib.sha256((AUDIT / 'prepare_integration.py').read_bytes()).hexdigest())
        with patched(M, A=root):
            with M.action_lock('exclusive.lock'):
                rejects('exclusive operation lock rejects concurrent operator', lambda: _second_lock())
    # The loader must ignore an otherwise timestamp/size-valid malicious pyc.
    with tempfile.TemporaryDirectory(prefix='stale-pyc-', dir=TMP) as temporary:
        root = Path(temporary); dep = root / 'prepare_integration.py'; tracker = root / 'record_tracker.py'
        write(dep, (AUDIT / 'prepare_integration.py').read_bytes()); write(tracker, (AUDIT / 'record_tracker.py').read_bytes())
        stamp = dep.stat(); cache = Path(importlib.util.cache_from_source(str(dep)))
        evil = compile("raise RuntimeError('HOSTILE_STALE_PYC_WAS_LOADED')\n", str(dep), 'exec')
        write(cache, importlib.util.MAGIC_NUMBER + struct.pack('<III', 0, int(stamp.st_mtime), stamp.st_size) + marshal.dumps(evil))
        loaded = source_module(tracker, '_stale_pyc_control')
        check('hostile timestamp-valid stale pyc ignored', loaded.INTEGRATION_HELPER_SHA256 == hashlib.sha256(dep.read_bytes()).hexdigest()
              and loaded.TITLE == M.TITLE and cache.exists())


def _second_lock():
    with M.action_lock('exclusive.lock'):
        pass


def git_controls():
    with tempfile.TemporaryDirectory(prefix='git-', dir=TMP) as temporary:
        root = Path(temporary); repo = root / 'repo'; repo.mkdir()
        subprocess.run(['git', 'init', '-q', '-b', 'main', str(repo)], check=True)
        subprocess.run(['git', 'config', 'user.email', 'offline.invalid@example.invalid'], cwd=repo, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Offline control'], cwd=repo, check=True)
        with patched(M, REPO=repo):
            _, _, _, cells = M.queue_row(SNAPSHOT['queue_row'].encode() + b'\n')
            cells[8], cells[9], cells[11] = b' queued ', b' 0/5 ', b'  '
            queue = b'untouched before\n' + b'|'.join(cells) + b'\nuntouched after\n'
            base_files = {M.QPATH: queue, 'untouched/root.txt': b'root-preserved\n',
                          'unsolved_math_prioritization/attempts/other/file': b'other attempt\n',
                          'unsolved_math_prioritization/publications/other/file': b'other publication\n',
                          'script': b'#!/bin/sh\n', 'link': b'untouched/root.txt'}
            tree = M.files_tree(base_files)
            tree = M.splice(tree, 'script', b'100755 blob ' + M.git('hash-object', '-w', '--stdin', input=base_files['script']).strip())
            tree = M.splice(tree, 'link', b'120000 blob ' + M.git('hash-object', '-w', '--stdin', input=base_files['link']).strip())
            base = M.git('commit-tree', tree, input=b'offline base\n').decode().strip()
            M.git('update-ref', 'refs/heads/main', base); M.git('symbolic-ref', 'HEAD', 'refs/heads/main')
            initial = M.local_state()
            original_tree = M.splice(tree, M.PREFIX.rstrip('/'), b'040000 tree ' + M.files_tree(ORIGINAL).encode())
            original_tree = M.splice(original_tree, M.QPATH, b'100644 blob ' + M.git('hash-object', '-w', '--stdin', input=SNAPSHOT['queue_row'].encode() + b'\n').strip())
            original_commit = M.git('commit-tree', original_tree, '-p', base, input=b'offline candidate\n').decode().strip()
            M.git('update-ref', 'refs/remotes/origin/main', base)
            target, queue_patch = M.patch_queue(queue, DOI, SNAPSHOT['queue_row'])
            proposed = M.splice(tree, M.PREFIX.rstrip('/'), b'040000 tree ' + M.files_tree(ORIGINAL).encode())
            proposed = M.splice(proposed, M.PUB_PREFIX.rstrip('/'), b'040000 tree ' + M.files_tree({'PUBLICATION.md': b'fixture\n'}).encode())
            proposed = M.splice(proposed, M.QPATH, b'100644 blob ' + M.git('hash-object', '-w', '--stdin', input=target).strip())
            check('subtree splice forwards unrelated modes and blobs', M.git('ls-tree', tree, '--', 'script', 'link', 'untouched')
                  == M.git('ls-tree', proposed, '--', 'script', 'link', 'untouched'))
            check('subtree splice forwards unrelated nested attempts/publications',
                  M.git('rev-parse', tree + ':unsolved_math_prioritization/attempts/other') ==
                  M.git('rev-parse', proposed + ':unsolved_math_prioritization/attempts/other') and
                  M.git('rev-parse', tree + ':unsolved_math_prioritization/publications/other') ==
                  M.git('rev-parse', proposed + ':unsolved_math_prioritization/publications/other'))
            check('subtree splice never changes shared HEAD or creates index', M.local_state() == initial
                  and not (repo / '.git/index').exists())
            rejects('splice refuses non-tree ancestor', lambda: M.splice(tree, 'script/child', b'100644 blob ' + b'0' * 40))
            rejects('files tree rejects file-directory collision', lambda: M.files_tree({'a': b'one', 'a/b': b'two'}))
            # Lifecycle doubles replace ONLY external services and costly replay.
            # All Git tree/commit comparisons below use the real disposable repo.
            audit = repo / 'audit'; audit.mkdir()
            files, payload, accepted, receipt = fixture(audit)
            inputs = {'files': files, 'original': ORIGINAL, 'snapshot': SNAPSHOT, 'members': payload,
                      'accepted_bytes': M.json_bytes(accepted), 'review_files': {},
                      'receipt_bytes': [M.json_bytes(receipt), M.json_bytes(receipt | {'verified_utc': 'later'})],
                      'validation': {'offline_lifecycle_fixture': True}}
            actual_git = M.git; dispatched = []; meta_calls = []
            meta = {'number': 662, 'state': 'OPEN', 'isDraft': True, 'baseRefName': 'main', 'headRefName': M.BRANCH,
                    'headRefOid': original_commit, 'isCrossRepository': False, 'headRepositoryOwner': {'login': 'AlecKriebel'}}
            def fake_git(*args, input=None):
                if args[0] == 'fetch': return b''
                if args[0] == 'push':
                    check('push durable intent and prepared receipt precede dispatch', (audit / 'INTEGRATION_PUSH_INTENT.json').is_file()
                          and (audit / 'INTEGRATION_PREPARED_RECEIPT.json').is_file())
                    dispatched.append(args); return b''
                if args[0] == 'ls-remote':
                    oid = base if args[-1] == 'refs/heads/main' else dispatched[-1][2].split(':')[0]
                    return (oid + '\t' + args[-1] + '\n').encode()
                return actual_git(*args, input=input)
            def fake_meta():
                meta_calls.append(True); return copy.deepcopy(meta)  # deliberately stale after push
            before = sys.argv
            with patched(M, A=audit, ORIGINAL=original_commit, git=fake_git, pr_metadata=fake_meta,
                         PUSH_INTENT=audit / 'INTEGRATION_PUSH_INTENT.json', PUSHED_RECEIPT=audit / 'INTEGRATION_PUSHED_RECEIPT.json',
                         publication_inputs=lambda *args: inputs,
                         capture_replay=lambda *args: {'explicitly_mocked_for_lifecycle_test': True}):
                try:
                    sys.argv = ['prepare_integration.py', '--doi', DOI]
                    with contextlib.redirect_stdout(io.StringIO()): M.main()
                    prepared = json.loads((audit / 'INTEGRATION_PREPARED_RECEIPT.json').read_bytes())
                    check('default integration creates objects but never pushes', not dispatched and prepared['pushed'] is False)
                    check('actual toy proposed commit preserves all native24 bytes', all(
                        actual_git('show', prepared['integration_commit'] + ':' + M.PREFIX + name) == data for name, data in ORIGINAL.items()))
                    check('actual toy proposed commit has exact target-only paths', set(prepared['changed_paths']) ==
                          {M.QPATH} | {M.PREFIX + name for name in ORIGINAL} | {M.PUB_PREFIX + name for name in prepared['publication_sha256']})
                    check('default integration preserves HEAD/index', M.local_state() == initial)
                    sys.argv = ['prepare_integration.py', '--doi', DOI, '--push']
                    def advanced_main(*args, input=None):
                        if args[0] == 'ls-remote' and args[-1] == 'refs/heads/main':
                            return b'0' * 40 + b'\trefs/heads/main\n'
                        return fake_git(*args, input=input)
                    with patched(M, git=advanced_main):
                        rejects('main advance prevents branch push', M.main)
                    check('main advance leaves no intent or dispatch', not dispatched and not (audit / 'INTEGRATION_PUSH_INTENT.json').exists())
                    meta_sequence = []
                    def advanced_head():
                        meta_sequence.append(True)
                        return copy.deepcopy(meta) if len(meta_sequence) == 1 else dict(meta, headRefOid='0' * 40)
                    with patched(M, pr_metadata=advanced_head):
                        rejects('candidate head advance prevents branch push', M.main)
                    check('candidate advance leaves no intent or dispatch', not dispatched and not (audit / 'INTEGRATION_PUSH_INTENT.json').exists())
                    def uncertain_push(*args, input=None):
                        if args[0] == 'push':
                            check('uncertain push has durable prior intent', (audit / 'INTEGRATION_PUSH_INTENT.json').is_file())
                            dispatched.append(args)
                            raise OSError('simulated uncertain push transport')
                        return fake_git(*args, input=input)
                    with patched(M, git=uncertain_push):
                        rejects('uncertain push stops without success receipt', M.main)
                        rejects('uncertain push cannot be dispatched again', M.main)
                    check('uncertain push retains exact sticky identity', len(dispatched) == 1
                          and json.loads((audit / 'INTEGRATION_PUSH_INTENT.json').read_bytes())['outcome'].startswith('unconfirmed')
                          and not (audit / 'INTEGRATION_PUSHED_RECEIPT.json').exists())
                    # Reset only the disposable fake-service fixture for the
                    # separate success scenario, never a production journal.
                    (audit / 'INTEGRATION_PUSH_INTENT.json').unlink(); dispatched.clear()
                    with contextlib.redirect_stdout(io.StringIO()): M.main()
                    pushed = json.loads((audit / 'INTEGRATION_PUSHED_RECEIPT.json').read_bytes())
                    check('one explicit ordinary branch push with GH lag handled', len(dispatched) == 1 and dispatched[0][0:2] == ('push', 'origin')
                          and not any('force' in argument for argument in dispatched[0])
                          and pushed['remote_branch_head_verified'] is True and pushed['github_metadata_readback_pending'] is True)
                    rejects('confirmed push cannot dispatch again', lambda: M.main())
                    check('confirmed push repeat remains one dispatch', len(dispatched) == 1)
                finally: sys.argv = before
            check('all tree lifecycle tests preserve toy main/index', M.local_state() == initial)


def main():
    publication_controls(); tracker_controls(); git_controls()
    mode = 'optimized' if sys.flags.optimize else 'normal'
    report = {'status': 'PASS', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'mode': mode,
        'checks': len(checks), 'source_sha256': {name: hashlib.sha256((AUDIT / name).read_bytes()).hexdigest()
            for name in ('prepare_integration.py', 'record_tracker.py', 'ACCEPTED_PR_DESCRIPTION.template.md')},
        'no_live_api_or_network_calls': True, 'no_external_mutations': True,
        'native24_read_only': True, 'integration_lifecycle_service_and_replay_doubles_explicit': True,
        'actual_proposed_tree_replay_is_separate_required_control': True, 'results': checks}
    (HERE / ('OFFLINE_CONTROL_RESULTS.' + mode + '.json')).write_bytes(M.json_bytes(report))
    print(json.dumps({'status': 'PASS', 'checks': len(checks), 'no_live_api_or_network_calls': True}, indent=2))


if __name__ == '__main__': main()
