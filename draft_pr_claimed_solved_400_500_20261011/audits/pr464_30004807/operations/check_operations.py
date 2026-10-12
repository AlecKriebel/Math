#!/usr/bin/env python3
"""Offline guard probes. All fabricated inputs stay under private_cases/.

No credentials, network, Git index, or external writes are used. Fake service
responses are test fixtures, never production evidence. Run normally and -O.
"""
import copy
import json
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch
import common as c
import integrate_pr464_publication as integration
import register_pr464_tracker as tracker
import zenodo_pr464 as zenodo

REAL_AUDIT = c.AUDIT
REAL_REPOSITORY = c.REPOSITORY
OPERATIONS = Path(__file__).resolve().parent
RESULTS = []
HEADER = '| Rank | ID / code | Problem | EV | Impact (/10) | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI |\n'


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def jwrite(path, value):
    write(path, c.json_bytes(value))


def failure(function, needle):
    try:
        function()
    except RuntimeError as error:
        c.require(needle in str(error), 'Wrong rejection: ' + str(error))
    else:
        raise RuntimeError('Expected rejection was not raised: ' + needle)


class Fixture:
    def __init__(self, directory):
        self.repo = directory / 'repository'
        self.audit = self.repo / 'draft_pr_claimed_solved_400_500_20261011/audits/pr464_30004807'
        self.package = self.audit / 'package'
        self.receipt = json.loads((REAL_AUDIT / 'SOURCE_RECEIPT.json').read_text())
        jwrite(self.audit / 'SOURCE_RECEIPT.json', self.receipt)
        self.payloads = {'README.md': b'OFFLINE FIXTURE ONLY\n', 'manuscript.tex': b'OFFLINE FIXTURE ONLY\n',
                         'metadata.json': c.json_bytes({'title': 'OFFLINE FIXTURE ONLY'}),
                         'SHA256SUMS.json': b'{}\n', 'verification/README.md': b'OFFLINE FIXTURE ONLY\n'}
        for item in self.receipt['files']:
            data = (REAL_AUDIT / 'source_snapshot' / item['path']).read_bytes()
            write(self.audit / 'source_snapshot' / item['path'], data)
            self.payloads['verification/frozen_history/' + item['path'].removeprefix(c.PREFIX)] = data
        for name, data in self.payloads.items():
            write(self.package / name, data)
        write(self.package / 'manuscript.pdf', b'OFFLINE FIXTURE ONLY; not a PDF\n')
        write(self.package / 'ARCHIVE_RECEIPT.json', b'{"offline_fixture_only":true}\n')
        jwrite(self.package / 'deposit.json', {'metadata': {'title': 'OFFLINE FIXTURE ONLY'}, 'files': [
            {'path': 'manuscript.pdf', 'name': 'regular_zas_bianchi_defect.pdf'}, {'path': c.ZIP_NAME}]})
        self.math = json.loads((REAL_AUDIT / 'MATHEMATICAL_ACCEPTANCE_GATE.json').read_text())
        for item in self.math['mathematical_families'] + [self.math['bounded_priority']]:
            for filename in ('REPORT.md', 'PUBLIC_OUTPUT_WHITELIST.json'):
                source = REAL_AUDIT / 'reviews' / item['family'] / filename
                write(self.audit / 'reviews' / item['family'] / filename, source.read_bytes())
        whole = self.math['whole_candidate_report']
        write(self.audit / whole['path'], (REAL_AUDIT / whole['path']).read_bytes())
        jwrite(self.audit / 'MATHEMATICAL_ACCEPTANCE_GATE.json', self.math)
        self.manifest_name = 'PACKAGE_REVIEW_INPUT_2.json'
        reviews = []
        for round_number in (1, 2):
            name = f'reviews/package_round{round_number}/REPORT.md'
            data = b'OFFLINE FIXTURE ONLY\n'
            write(self.audit / name, data)
            reviews.append({'round': round_number, 'identity': 'offline_mock_' + str(round_number),
                            'path': name, 'sha256': c.sha(data), 'verdict': 'PASS',
                            'blocking_issue_count': 0, 'required_correction_count': 0})
        write(self.audit / 'reviews/operations/REPORT.md', b'OFFLINE FIXTURE ONLY\n')
        for name in c.HELPERS:
            write(self.audit / name, (REAL_AUDIT / name).read_bytes())
        write(self.repo / 'zenodo_deposit_tool/zenodo.py', (REAL_REPOSITORY / 'zenodo_deposit_tool/zenodo.py').read_bytes())
        self.gate = {'verdict': 'ACCEPTED_FOR_PREPRINT_PUBLICATION', 'pr': c.PR, 'problem_id': c.PROBLEM,
                     'original_pr_head': c.ORIGINAL, 'status_gate': 'claimed_solved', 'remaining_package_issues': 0,
                     'root_read_entire_final_report': True, 'review_input_manifest': self.manifest_name,
                     'complete_package_reviews': reviews, 'operations_review': {
                         'path': 'reviews/operations/REPORT.md', 'sha256': c.sha(b'OFFLINE FIXTURE ONLY\n'),
                         'verdict': 'PASS', 'blocking_issue_count': 0, 'required_correction_count': 0,
                         'helpers': {n: c.sha((self.audit / n).read_bytes()) for n in c.HELPERS}},
                     'zenodo_kit_sha256': c.sha((self.repo / 'zenodo_deposit_tool/zenodo.py').read_bytes())}
        self.seal()

    def seal(self):
        with zipfile.ZipFile(self.package / c.ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name in sorted(self.payloads):
                archive.writestr(name, (self.package / name).read_bytes())
        self.top = {name: {'sha256': c.sha((self.package / name).read_bytes()), 'bytes': (self.package / name).stat().st_size}
                    for name in ['README.md', 'manuscript.tex', 'manuscript.pdf', 'metadata.json', 'deposit.json',
                                 'SHA256SUMS.json', c.ZIP_NAME, 'ARCHIVE_RECEIPT.json']}
        jwrite(self.audit / self.manifest_name, {'files': self.top})
        self.plan = {'entries': [
            {'local_program_path': (self.package / name).relative_to(self.repo).as_posix(),
             'repository_destination': c.PREPRINT + name,
             'sha256': c.sha((self.package / name).read_bytes()), 'bytes': (self.package / name).stat().st_size}
            for name in sorted(set(self.top) | set(self.payloads))]}
        jwrite(self.audit / 'BRANCH_INSTALL_PLAN.json', self.plan)
        self.gate.update(source_receipt_sha256=c.sha((self.audit / 'SOURCE_RECEIPT.json').read_bytes()),
                         mathematical_acceptance_gate_sha256=c.sha((self.audit / 'MATHEMATICAL_ACCEPTANCE_GATE.json').read_bytes()),
                         review_input_manifest_sha256=c.sha((self.audit / self.manifest_name).read_bytes()),
                         branch_install_plan_sha256=c.sha((self.audit / 'BRANCH_INSTALL_PLAN.json').read_bytes()),
                         final_files=self.top)
        for review in self.gate['complete_package_reviews']:
            review['input_manifest_sha256'] = self.gate['review_input_manifest_sha256']
        self.save_gate()

    def save_gate(self):
        jwrite(self.audit / 'FINAL_ACCEPTANCE_GATE.json', self.gate)

    def save_plan(self):
        jwrite(self.audit / 'BRANCH_INSTALL_PLAN.json', self.plan)
        self.gate['branch_install_plan_sha256'] = c.sha((self.audit / 'BRANCH_INSTALL_PLAN.json').read_bytes())
        self.save_gate()

    def publication(self):
        context = c.validate_gate()
        pub = {'environment': 'production', 'state': 'published', 'id': 123456,
               'doi': '10.5281/zenodo.123456', 'doi_url': 'https://doi.org/10.5281/zenodo.123456',
               'record_url': 'https://zenodo.org/records/123456', 'title': context['metadata']['title'],
               'metadata_normalizations': [], 'files': list(c.expected_public_files(context).values()),
               'canonical_metadata_sha256': c.sha((self.package / 'metadata.json').read_bytes()),
               'accepted_input_manifest_sha256': self.gate['review_input_manifest_sha256']}
        jwrite(self.audit / 'ZENODO_PUBLISH_RECEIPT.json', pub)
        jwrite(self.audit / 'ZENODO_PUBLIC_FILE_READBACK.json', {'verified': True, 'authenticated': False,
               'id': pub['id'], 'doi': pub['doi'], 'files': list(c.expected_public_files(context).values())})
        return context, pub


def case(name, function):
    private = OPERATIONS / 'private_cases'
    private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=name + '_', dir=private) as directory:
        fixture = Fixture(Path(directory))
        calls = []
        def no_service(*args, **kwargs):
            calls.append({'endpoint': args[0] if args else None, 'mutation': bool(kwargs.get('payload'))})
            raise RuntimeError('Offline test attempted an unmocked service')
        with patch.multiple(c, AUDIT=fixture.audit, PACKAGE=fixture.package, REPOSITORY=fixture.repo), \
             patch.object(c, 'github', no_service), patch.object(c, 'gws', no_service), \
             patch.object(c.subprocess, 'run', side_effect=no_service):
            function(fixture)
            c.require(not calls, 'Offline test escaped mock isolation')
    RESULTS.append({'case': name, 'passed': True, 'real_external_calls': 0})


def gate_case(name, mutate, needle):
    def probe(fixture):
        mutate(fixture)
        fixture.save_gate()
        failure(c.validate_gate, needle)
    case(name, probe)


def tracker_case(kind):
    def probe(fixture):
        context, pub = fixture.publication()
        values = c.tracker_values(context['metadata'], pub['doi_url'])
        rows = [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']]
        writes = []
        if kind in {'existing', 'existing_differs', 'duplicate'}:
            rows.append(values[0].copy())
        if kind == 'existing_differs':
            rows[1][3] += ' changed'
        if kind == 'duplicate':
            rows.append(values[0].copy())
        if kind == 'prior_unconfirmed':
            jwrite(fixture.audit / 'TRACKER_APPEND_OPERATION.json', {'state': 'outcome_unconfirmed',
                   'doi': pub['doi_url'], 'values': values})
        def read(range_name):
            if range_name.endswith('A:D'):
                return {'values': copy.deepcopy(rows)}
            if range_name == "'Math Puzzles'!A1:D1":
                return {'values': [rows[0]]}
            return {'values': [copy.deepcopy(rows[1])]}
        def write_row(action, params, body):
            c.require(action == 'append' and body['values'] == values, 'Wrong simulated append')
            c.require(json.loads((fixture.audit / 'TRACKER_APPEND_OPERATION.json').read_text())['state'] == 'append_attempted_once',
                      'Operation was not saved before append')
            writes.append(action)
            rows.append(values[0].copy())
            if kind == 'lost_response':
                raise RuntimeError('Simulated lost response')
            if kind == 'concurrent_duplicate':
                rows.append(values[0].copy())
            return {'updates': {'updatedRows': 2 if kind == 'wrong_size' else 1,
                                'updatedColumns': 4, 'updatedCells': 4,
                                'updatedRange': "'Math Puzzles'!A2:D2"}}
        with patch.multiple(tracker, AUDIT=fixture.audit, validate_gate=lambda: context,
                            validate_publication=lambda ctx: pub, confirm_live_publication=lambda ctx: pub, live_eligibility=lambda: None,
                            check_sheet=lambda: None, sheet_get=read, gws=write_row):
            if kind == 'default_readonly':
                result = tracker.run(False)
                c.require(result['state'] == 'read_only_preflight' and not writes, 'Default tracker mutated')
            elif kind in {'duplicate', 'existing_differs', 'prior_unconfirmed', 'wrong_size', 'concurrent_duplicate'}:
                needles = {'duplicate': 'Duplicate DOI', 'existing_differs': 'not unique and exact',
                           'prior_unconfirmed': 'unconfirmed', 'wrong_size': 'Unexpected append size',
                           'concurrent_duplicate': 'not unique and exact'}
                failure(lambda: tracker.run(True), needles[kind])
                expected = 1 if kind in {'wrong_size', 'concurrent_duplicate'} else 0
                c.require(len(writes) == expected, 'Unexpected simulated append count')
            else:
                result = tracker.run(True)
                c.require(result['verified'] is True and len(writes) == (0 if kind == 'existing' else 1),
                          'Simulated tracker operation not verified')
                tracker.run(True)
                c.require(len(writes) == (0 if kind == 'existing' else 1), 'Repeated append occurred')
    case('tracker_' + kind, probe)


def publication_case(name, mutate, needle):
    def probe(fixture):
        context, pub = fixture.publication()
        mutate(fixture, pub)
        jwrite(fixture.audit / 'ZENODO_PUBLISH_RECEIPT.json', pub)
        failure(lambda: c.validate_publication(context), needle)
    case(name, probe)


def git_reader_case(kind):
    def probe(fixture):
        reader = c.GitReader()
        revision = 'a' * 40
        data = b'Binary\0payload\xff\n'
        blob = c.git_sha(data)
        reader.commits[revision] = {'sha': revision, 'tree': {'sha': 'b' * 40}}
        reader.trees['b' * 40] = [{'path': 'payload.bin', 'sha': blob, 'type': 'blob', 'mode': '100644'}]
        import base64
        result = {'sha': blob, 'encoding': 'base64', 'size': len(data), 'content': base64.b64encode(data).decode()}
        if kind == 'mode_symlink':
            reader.trees['b' * 40][0]['mode'] = '120000'
        if kind == 'hash_drift':
            result['content'] = base64.b64encode(b'wrong').decode()
            result['size'] = 5
        if kind == 'size_drift':
            result['size'] += 1
        with patch.object(c, 'github', lambda endpoint: result):
            if kind == 'valid':
                c.require(reader.read('payload.bin', revision) == data, 'Binary immutable readback failed')
            else:
                failure(lambda: reader.read('payload.bin', revision), 'Git blob' if kind != 'mode_symlink' else 'symlinked Git blob')
    case('git_reader_' + kind, probe)


def eligibility_case(kind):
    def probe(fixture):
        queue = (HEADER + fixture.receipt['selected_queue_row'] + '\n').encode()
        fixture.receipt['queue_sha256'] = c.sha(queue)
        jwrite(fixture.audit / 'SOURCE_RECEIPT.json', fixture.receipt)
        files = {x['path']: (fixture.audit / 'source_snapshot' / x['path']).read_bytes() for x in fixture.receipt['files']}
        observed = dict(files)
        observed[c.QUEUE] = queue
        pr = {'number': 464, 'state': 'open', 'draft': True, 'changed_files': 14,
              'head': {'sha': c.ORIGINAL, 'ref': c.BRANCH, 'repo': {'full_name': c.REPO}},
              'base': {'ref': 'main', 'repo': {'full_name': c.REPO}}}
        changed = [{'filename': x, 'status': 'modified' if x == c.QUEUE else 'added'} for x in sorted(set(files) | {c.QUEUE})]
        ref = c.ORIGINAL
        if kind == 'excluded_status':
            observed[c.QUEUE] = queue.replace(b'claimed_solved', b'unsolved')
        if kind == 'attempt_count_changed':
            observed[c.QUEUE] = queue.replace(b'1/5', b'2/5')
        if kind == 'changed_source':
            observed[next(iter(files))] = b'changed source'
        if kind == 'not_draft':
            pr['draft'] = False
        if kind == 'closed':
            pr['state'] = 'closed'
        if kind == 'wrong_head':
            pr['head']['sha'] = 'f' * 40
        if kind == 'wrong_branch':
            pr['head']['ref'] = 'another-branch'
        if kind == 'wrong_base':
            pr['base']['ref'] = 'development'
        if kind == 'wrong_repo':
            pr['head']['repo']['full_name'] = 'different/repo'
        if kind == 'moved_ref':
            ref = 'f' * 40
        if kind == 'truncated_diff':
            changed.pop()
        if kind == 'unrelated_diff':
            changed[-1]['filename'] = 'unrelated.txt'
        class Reader:
            def read(self, path, revision):
                c.require(revision == c.ORIGINAL, 'Unexpected fixture revision')
                return observed[path]
        def api(endpoint):
            if endpoint == 'pulls/464':
                return pr
            if endpoint.startswith('git/ref/'):
                return {'object': {'sha': ref}}
            if endpoint.startswith('pulls/464/files'):
                return changed
            raise RuntimeError('Unexpected mocked API path')
        with patch.object(c, 'github', api):
            if kind == 'valid':
                c.live_eligibility(Reader())
            else:
                needles = {'excluded_status': 'problem is excluded', 'attempt_count_changed': 'problem is excluded',
                           'changed_source': 'Original source bytes differ', 'moved_ref': 'branch ref moved',
                           'truncated_diff': 'list is truncated', 'unrelated_diff': 'changed-file set differs'}
                failure(lambda: c.live_eligibility(Reader()), needles.get(kind, 'PR identity'))
    case('live_eligibility_' + kind, probe)


def integration_readback_case(kind):
    def probe(fixture):
        doi = 'https://doi.org/10.5281/zenodo.123456'
        queue = (HEADER + fixture.receipt['selected_queue_row'] + '\n').encode()
        lines, i, cells, columns = c.queue_row(queue)
        cells[columns.index('DOI')] = ' ' + doi + ' '
        lines[i] = '|' + '|'.join(cells) + '|\n'
        queue = ''.join(lines).encode()
        files = {c.QUEUE: queue, c.PREPRINT + 'manuscript.pdf': b'Binary\0PDF fixture\xff'}
        commit = 'b' * 40
        main = 'a' * 40
        summary = {'commit_sha': commit, 'parent_main_sha': main, 'doi_url': doi,
                   'expected_changed_paths': sorted(files),
                   'files': {p: {'sha256': c.sha(b), 'bytes': len(b), 'git_blob_sha': c.git_sha(b)} for p, b in files.items()}}
        comparison = {'base_commit': {'sha': main}, 'merge_base_commit': {'sha': main},
                      'files': [{'filename': p, 'status': 'added'} for p in files]}
        parents = [c.ORIGINAL, main]
        reads = []
        if kind == 'unrelated_diff':
            comparison['files'].append({'filename': 'unrelated.txt', 'status': 'added'})
        if kind == 'missing_diff':
            comparison['files'].pop()
        if kind == 'renamed_diff':
            comparison['files'][0]['status'] = 'renamed'
        if kind == 'duplicate_diff':
            comparison['files'].append(comparison['files'][0])
        if kind == 'wrong_merge_base':
            comparison['merge_base_commit']['sha'] = 'c' * 40
        if kind == 'wrong_parents':
            parents.reverse()
        if kind == 'binary_byte_drift':
            files[c.PREPRINT + 'manuscript.pdf'] += b'drift'
        class Reader:
            def commit(self, revision):
                return {'sha': revision, 'parents': [{'sha': p} for p in parents]}
            def read(self, path, revision):
                reads.append(path)
                return files[path]
        with patch.object(c, 'github', lambda endpoint: comparison):
            if kind == 'valid':
                integration.verify_commit(summary, Reader())
                c.require(set(reads) == set(files), 'Not every installed target was read back')
            else:
                needle = {'wrong_parents': 'parents differ', 'wrong_merge_base': 'compare base/merge base',
                          'binary_byte_drift': 'whole-file readback differs'}.get(kind, 'changed-file set differs')
                failure(lambda: integration.verify_commit(summary, Reader()), needle)
    case('integration_readback_' + kind, probe)


def zenodo_guard_case(kind):
    def probe(fixture):
        context = c.validate_gate()
        if kind in {'prior_stage', 'prior_publish'}:
            mode = 'stage' if kind == 'prior_stage' else 'publish'
            jwrite(fixture.audit / ('ZENODO_' + mode.upper() + '_OPERATION.json'), {'state': 'outcome_unconfirmed'})
        else:
            mode = 'publish' if kind in {'missing_stage', 'wrong_draft_id'} else 'stage'
        if kind == 'wrong_draft_id':
            jwrite(fixture.audit / 'ZENODO_STAGE_RECEIPT.json', {'state': 'ready_to_publish', 'id': 123})
        kit_calls = []
        with patch.object(zenodo.c, 'validate_gate', lambda: context), \
             patch.object(zenodo.c, 'live_eligibility', lambda: None), \
             patch.object(zenodo, 'kit_cli', lambda *args: kit_calls.append(args)):
            needle = {'prior_stage': 'prior Zenodo write', 'prior_publish': 'prior Zenodo write',
                      'missing_stage': 'Missing or escaping file', 'wrong_draft_id': 'confirmed production draft',
                      'apply_absent': 'Explicit --apply required'}[kind]
            failure(lambda: zenodo.run(mode, apply=kind != 'apply_absent', confirm_id=456), needle)
            c.require(not kit_calls, 'Rejected Zenodo operation reached kit dispatch')
    case('zenodo_guard_' + kind, probe)


def integration_flow_case(kind):
    def probe(fixture):
        original_queue = (HEADER + fixture.receipt['selected_queue_row'] + '\n').encode()
        fixture.receipt['queue_sha256'] = c.sha(original_queue)
        jwrite(fixture.audit / 'SOURCE_RECEIPT.json', fixture.receipt)
        fixture.seal()
        context, pub = fixture.publication()
        values = c.tracker_values(context['metadata'], pub['doi_url'])
        jwrite(fixture.audit / 'TRACKER_APPEND_RECEIPT.json', {'verified': True, 'spreadsheet_id': c.SHEET,
               'sheet_id': c.TAB_ID, 'tab': c.TAB, 'values': values, 'doi': pub['doi_url'],
               'updated_range': "'Math Puzzles'!A2:D2", 'unique_doi_row_at_final_snapshot': True})
        source_files = {x['path']: (fixture.audit / 'source_snapshot' / x['path']).read_bytes() for x in fixture.receipt['files']}
        source_files[c.QUEUE] = original_queue
        main = 'a' * 40
        candidate = 'b' * 40
        lines, index, cells, columns = c.queue_row(original_queue)
        cells[columns.index('Status')] = ' queued '
        cells[columns.index('Turns')] = ' 0/5 '
        if kind == 'main_excluded':
            cells[columns.index('Status')] = ' unsolved '
        if kind == 'different_main_doi':
            cells[columns.index('DOI')] = ' https://doi.org/10.5281/zenodo.999 '
        lines[index] = '|' + '|'.join(cells) + '|\n'
        other = fixture.receipt['selected_queue_row'].replace('30004807 /', '99999999 /')
        main_files = {c.QUEUE: (''.join(lines) + other + '\n').encode(), 'unrelated_anchor.txt': b'preserve latest main\n'}
        if kind == 'package_conflict':
            main_files[c.PREPRINT + 'manuscript.pdf'] = b'new unrelated revision'
        if kind == 'historical_conflict':
            main_files[c.PREFIX + 'release/PROOF.md'] = b'new unrelated revision'
        state = {'branch': c.ORIGINAL, 'main_reads': 0, 'blobs': {}, 'files': {main: main_files, c.ORIGINAL: source_files},
                 'commit': None, 'patches': [], 'mutations': []}
        changed_original = [{'filename': p, 'status': 'modified' if p == c.QUEUE else 'added'} for p in source_files]
        class Reader:
            def commit(self, revision):
                if revision == main:
                    return {'sha': main, 'tree': {'sha': 'd' * 40}}
                return state['commit']
            def entry(self, path, revision):
                data = state['files'][revision].get(path)
                return None if data is None else {'type': 'blob', 'mode': '100644', 'sha': c.git_sha(data)}
            def read(self, path, revision):
                return state['files'][revision][path]
        reader = Reader()
        def api(endpoint, payload=None, method=None):
            if payload is not None:
                state['mutations'].append(endpoint)
            if endpoint == 'pulls/464':
                return {'number': 464, 'state': 'open', 'draft': True, 'changed_files': 14,
                        'head': {'sha': state['branch'], 'ref': c.BRANCH, 'repo': {'full_name': c.REPO}},
                        'base': {'ref': 'main', 'repo': {'full_name': c.REPO}}}
            if endpoint.startswith('pulls/464/files'):
                return changed_original
            if endpoint == 'git/ref/heads/' + c.BRANCH:
                return {'object': {'sha': state['branch']}}
            if endpoint == 'git/ref/heads/main':
                state['main_reads'] += 1
                return {'object': {'sha': 'f' * 40 if kind == 'main_moves' and state['main_reads'] > 1 else main}}
            if endpoint == 'git/blobs':
                import base64
                data = base64.b64decode(payload['content'])
                digest = c.git_sha(data)
                state['blobs'][digest] = data
                if kind == 'head_moves':
                    state['branch'] = 'e' * 40
                return {'sha': digest}
            if endpoint == 'git/trees':
                c.require(payload['base_tree'] == 'd' * 40, 'Wrong mocked base tree')
                new_files = dict(main_files)
                new_files.update({x['path']: state['blobs'][x['sha']] for x in payload['tree']})
                state['files'][candidate] = new_files
                return {'sha': 'c' * 40}
            if endpoint == 'git/commits':
                state['commit'] = {'sha': candidate, 'parents': [{'sha': p} for p in payload['parents']], 'tree': {'sha': payload['tree']}}
                return {'sha': candidate}
            if endpoint.startswith('compare/'):
                differences = [{'filename': p, 'status': 'modified' if p in main_files else 'added'}
                               for p, b in state['files'][candidate].items() if main_files.get(p) != b]
                if kind == 'wrong_compare':
                    differences.append({'filename': 'unexpected.txt', 'status': 'added'})
                return {'base_commit': {'sha': main}, 'merge_base_commit': {'sha': main}, 'files': differences}
            if endpoint == 'git/refs/heads/' + c.BRANCH:
                operation = json.loads((fixture.audit / 'BRANCH_INTEGRATION_OPERATION.json').read_text())
                c.require(operation['state'] == 'ref_update_attempted_once' and operation['commit_sha'] == candidate,
                          'Branch operation was not saved before PATCH')
                c.require(payload == {'sha': candidate, 'force': False} and method == 'PATCH', 'Forced or wrong branch update')
                state['patches'].append(payload)
                state['branch'] = candidate
                if kind == 'lost_patch_response':
                    raise RuntimeError('Simulated lost PATCH response')
                return {'object': {'sha': candidate}}
            raise RuntimeError('Unexpected mock API endpoint: ' + endpoint)
        with patch.object(c, 'GitReader', lambda: reader), patch.object(c, 'github', api), \
             patch.object(c, 'confirm_live_publication', lambda ctx: pub), \
             patch.object(c, 'confirm_live_tracker', lambda ctx, published: None):
            if kind == 'readonly':
                result = integration.run(False)
                c.require(result['state'] == 'read_only_preflight' and not state['mutations'], 'Default integration mutated')
            elif kind in {'main_excluded', 'different_main_doi', 'package_conflict', 'historical_conflict',
                          'wrong_compare', 'main_moves', 'head_moves'}:
                needles = {'main_excluded': 'selected disposition changed', 'different_main_doi': 'different DOI',
                           'package_conflict': 'accepted-package path conflicts', 'historical_conflict': 'historical source conflicts',
                           'wrong_compare': 'changed-file set differs', 'main_moves': 'Main advanced', 'head_moves': 'PR identity'}
                failure(lambda: integration.run(True), needles[kind])
                c.require(not state['patches'], 'Rejected integration updated branch')
            else:
                result = integration.run(True)
                c.require(result['state'] == 'branch_updated_verified' and len(state['patches']) == 1, 'Integration not verified once')
                c.require(state['files'][candidate]['unrelated_anchor.txt'] == main_files['unrelated_anchor.txt'], 'Latest-main unrelated file lost')
                before_rows = main_files[c.QUEUE].decode().splitlines()
                after_rows = state['files'][candidate][c.QUEUE].decode().splitlines()
                c.require(before_rows[-1] == after_rows[-1], 'Other QUEUE row changed')
                failure(lambda: integration.run(True), 'Prior integration write exists')
                integration.reconcile()
                c.require(len(state['patches']) == 1, 'Reconciliation repeated branch write')
    case('integration_flow_' + kind, probe)


def zenodo_flow_case(kind):
    def probe(fixture):
        context = c.validate_gate()
        service = {'state': 'absent', 'stage_writes': 0, 'publish_writes': 0, 'inspections': 0}
        base = {'environment': 'production', 'title': context['metadata']['title'],
                'files': list(c.expected_public_files(context).values()), 'metadata_normalizations': [], 'id': 123456,
                'canonical_metadata_sha256': c.sha((fixture.package / 'metadata.json').read_bytes()),
                'accepted_input_manifest_sha256': context['gate']['review_input_manifest_sha256']}
        def fake_kit(ctx, mode, confirm_id=None):
            if mode == 'check':
                return copy.deepcopy(base)
            if mode == 'stage':
                operation = json.loads((fixture.audit / 'ZENODO_STAGE_OPERATION.json').read_text())
                c.require(operation['state'] == 'stage_attempted_once', 'Stage operation was not saved before dispatch')
                service['stage_writes'] += 1
                service['state'] = 'ready_to_publish'
                if kind == 'lost_stage':
                    raise RuntimeError('Simulated lost stage response')
            if mode == 'publish':
                operation = json.loads((fixture.audit / 'ZENODO_PUBLISH_OPERATION.json').read_text())
                c.require(operation['state'] == 'publish_attempted_once' and confirm_id == 123456,
                          'Publish operation/ID not saved before dispatch')
                service['publish_writes'] += 1
                service['state'] = 'published'
                if kind == 'lost_publish':
                    raise RuntimeError('Simulated lost publish response')
            if mode == 'inspect':
                service['inspections'] += 1
            result = copy.deepcopy(base)
            result['state'] = service['state']
            if result['state'] == 'published':
                result.update(doi='10.5281/zenodo.123456', doi_url='https://doi.org/10.5281/zenodo.123456',
                              record_url='https://zenodo.org/records/123456')
            return result
        def fake_public(ctx, pub):
            jwrite(fixture.audit / 'ZENODO_PUBLIC_FILE_READBACK.json', {'verified': True, 'authenticated': False,
                   'id': pub['id'], 'doi': pub['doi'], 'files': list(c.expected_public_files(context).values())})
        with patch.object(c, 'live_eligibility', lambda: None), patch.object(zenodo, 'kit_cli', fake_kit), \
             patch.object(zenodo, 'public_readback', fake_public):
            if kind == 'default_readonly':
                zenodo.run()
                c.require(service['stage_writes'] == service['publish_writes'] == 0, 'Default Zenodo helper mutated')
                return
            if kind == 'lost_stage':
                failure(lambda: zenodo.run('stage', True), 'Simulated lost stage')
                zenodo.run('inspect')
                failure(lambda: zenodo.run('stage', True), 'prior Zenodo write')
                c.require(service['stage_writes'] == 1 and service['publish_writes'] == 0, 'Stage retry occurred')
                return
            zenodo.run('stage', True)
            if kind == 'lost_publish':
                failure(lambda: zenodo.run('publish', True, 123456), 'Simulated lost publish')
                zenodo.run('inspect')
            else:
                zenodo.run('publish', True, 123456)
            failure(lambda: zenodo.run('publish', True, 123456), 'prior Zenodo write')
            c.require(service['stage_writes'] == service['publish_writes'] == 1, 'Publication retry occurred')
            c.validate_publication(context)
    case('zenodo_flow_' + kind, probe)


def kit_serialization_case(kind):
    def probe(fixture):
        context = c.validate_gate()
        response = {'environment': 'production', 'title': context['metadata']['title'],
                    'files': list(c.expected_public_files(context).values()), 'metadata_normalizations': [],
                    'state': 'ready_to_publish', 'id': 123456}
        if kind == 'wrong_environment':
            response['environment'] = 'sandbox'
        if kind == 'wrong_title':
            response['title'] = 'another title'
        if kind == 'file_drift':
            response['files'][0]['sha256'] = '0' * 64
        if kind == 'metadata_normalization':
            response['metadata_normalizations'] = [{'field': 'description'}]
        class Run:
            returncode = 0
            stdout = json.dumps(response)
        with patch.object(zenodo.subprocess, 'run', lambda *args, **kwargs: Run()):
            if kind == 'valid':
                result = zenodo.kit_cli(context, 'inspect')
                c.require(result['canonical_metadata_sha256'] == c.sha((fixture.package / 'metadata.json').read_bytes()),
                          'Canonical metadata was not bound')
            else:
                needle = {'wrong_environment': 'production/title', 'wrong_title': 'production/title',
                          'file_drift': 'files differ', 'metadata_normalization': 'metadata changed'}[kind]
                failure(lambda: zenodo.kit_cli(context, 'inspect'), needle)
    case('kit_serialization_' + kind, probe)


def main():
    case('valid_final_gate', lambda fixture: c.require(c.validate_gate()['gate']['pr'] == 464, 'Valid gate rejected'))
    invalid_counts = [('missing', None), ('bool_false', False), ('bool_true', True), ('string_zero', '0'),
                      ('float_zero', 0.0), ('negative', -1), ('positive', 1)]
    for label, value in invalid_counts:
        for field in ('blocking_issue_count', 'required_correction_count'):
            gate_case('review_' + field + '_' + label,
                      lambda f, field=field, value=value: f.gate['complete_package_reviews'][-1].__setitem__(field, value), field)
        gate_case('remaining_' + label, lambda f, value=value: f.gate.__setitem__('remaining_package_issues', value), 'remaining_package_issues')
        gate_case('operations_' + label, lambda f, value=value: f.gate['operations_review'].__setitem__('required_correction_count', value),
                  'operations required_correction_count')
    gate_case('review_duplicate_identity', lambda f: f.gate['complete_package_reviews'][1].__setitem__('identity', 'offline_mock_1'), 'fresh and distinct')
    gate_case('review_wrong_final_manifest', lambda f: f.gate['complete_package_reviews'][1].__setitem__('input_manifest_sha256', 'f' * 64), 'exact accepted package')
    gate_case('review_non_successive_rounds', lambda f: f.gate['complete_package_reviews'][1].__setitem__('round', 3), 'successive distinct rounds')
    gate_case('wrong_pr', lambda f: f.gate.__setitem__('pr', 466), 'Final PR464 publication acceptance')
    gate_case('excluded_gate_status', lambda f: f.gate.__setitem__('status_gate', 'already_solved'), 'Final PR464 publication acceptance')
    gate_case('root_read_absent', lambda f: f.gate.__setitem__('root_read_entire_final_report', False), 'Root full final report')
    gate_case('source_receipt_drift', lambda f: write(f.audit / 'SOURCE_RECEIPT.json', b'{}\n'), 'Bound file changed')
    gate_case('math_report_drift', lambda f: write(f.audit / 'reviews/curvature_flux/REPORT.md', b'drift'), 'Bound file changed')
    gate_case('paper_drift', lambda f: write(f.package / 'manuscript.pdf', b'drift'), 'Frozen bytes changed')
    gate_case('metadata_drift', lambda f: write(f.package / 'metadata.json', b'{}\n'), 'Frozen bytes changed')
    gate_case('helper_drift', lambda f: write(f.audit / 'operations/common.py', b'drift'), 'Bound file changed')
    gate_case('kit_drift', lambda f: write(f.repo / 'zenodo_deposit_tool/zenodo.py', b'drift'), 'Bound file changed')
    def altered_source(f):
        item = f.receipt['files'][0]
        write(f.audit / 'source_snapshot' / item['path'], b'drift')
    gate_case('historical_source_drift', altered_source, 'Frozen bytes changed')
    def source_status(f):
        f.receipt['selected_queue_row'] = f.receipt['selected_queue_row'].replace('claimed_solved', 'already_solved')
        jwrite(f.audit / 'SOURCE_RECEIPT.json', f.receipt)
        f.gate['source_receipt_sha256'] = c.sha((f.audit / 'SOURCE_RECEIPT.json').read_bytes())
    gate_case('excluded_source_status', source_status, 'Historical selected row')
    def alter_plan(f, transformation):
        transformation(f.plan['entries'][0])
        f.save_plan()
    gate_case('install_path_traversal', lambda f: alter_plan(f, lambda i: i.__setitem__('local_program_path', '../outside')), 'canonical safe relative')
    gate_case('install_private_case', lambda f: alter_plan(f, lambda i: i.__setitem__('local_program_path', 'private_cases/x')), 'Private or generated path')
    gate_case('install_unsafe_destination', lambda f: alter_plan(f, lambda i: i.__setitem__('repository_destination', c.PREFIX + '../outside')), 'canonical safe relative')
    gate_case('install_byte_drift', lambda f: alter_plan(f, lambda i: i.__setitem__('sha256', '0' * 64)), 'Frozen bytes changed')
    def duplicate_plan(f):
        f.plan['entries'].append(copy.deepcopy(f.plan['entries'][0]))
        f.save_plan()
    gate_case('install_duplicate_destination', duplicate_plan, 'duplicate install destination')
    def direct_symlink(f):
        path = f.package / 'manuscript.pdf'
        target = f.package / 'duplicate.pdf'
        target.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(target.name)
    gate_case('install_direct_symlink', direct_symlink, 'Symlink excluded')
    def parent_symlink(f):
        source = f.package / 'verification'
        target = f.package / 'verification_real'
        source.rename(target)
        source.symlink_to(target.name, target_is_directory=True)
    gate_case('install_ancestor_symlink', parent_symlink, 'Symlink excluded')
    def extra_install(f):
        path = f.package / 'extra.txt'
        path.write_bytes(b'not selected')
        f.plan['entries'].append({'local_program_path': path.relative_to(f.repo).as_posix(),
                                  'repository_destination': c.PREPRINT + 'extra.txt', 'sha256': c.sha(path.read_bytes()), 'bytes': path.stat().st_size})
        f.save_plan()
    gate_case('install_extra_unreviewed', extra_install, 'exactly ZIP payloads')
    for kind in ('default_readonly', 'append', 'existing', 'existing_differs', 'duplicate', 'prior_unconfirmed',
                 'lost_response', 'wrong_size', 'concurrent_duplicate'):
        tracker_case(kind)
    publication_case('publication_unconfirmed', lambda f, p: p.__setitem__('state', 'ready_to_publish'), 'Confirmed production publication')
    publication_case('publication_sandbox', lambda f, p: p.__setitem__('environment', 'sandbox'), 'Confirmed production publication')
    publication_case('publication_wrong_doi', lambda f, p: p.__setitem__('doi_url', 'https://doi.org/10.5281/zenodo.999'), 'record/DOI identity')
    publication_case('publication_metadata_drift', lambda f, p: p.__setitem__('canonical_metadata_sha256', '0' * 64), 'canonical metadata/package')
    publication_case('publication_normalization', lambda f, p: p.__setitem__('metadata_normalizations', [{}]), 'Canonical publication metadata drift')
    publication_case('publication_wrong_file', lambda f, p: p['files'][0].__setitem__('sha256', '0' * 64), 'Published files differ')
    publication_case('publication_missing_public_readback', lambda f, p: (f.audit / 'ZENODO_PUBLIC_FILE_READBACK.json').unlink(), 'Missing or escaping file')
    for kind in ('valid', 'mode_symlink', 'hash_drift', 'size_drift'):
        git_reader_case(kind)
    for kind in ('valid', 'excluded_status', 'attempt_count_changed', 'changed_source', 'not_draft', 'closed',
                 'wrong_head', 'wrong_branch', 'wrong_base', 'wrong_repo', 'moved_ref', 'truncated_diff', 'unrelated_diff'):
        eligibility_case(kind)
    for kind in ('valid', 'unrelated_diff', 'missing_diff', 'renamed_diff', 'duplicate_diff', 'wrong_merge_base',
                 'wrong_parents', 'binary_byte_drift'):
        integration_readback_case(kind)
    for kind in ('prior_stage', 'prior_publish', 'missing_stage', 'wrong_draft_id', 'apply_absent'):
        zenodo_guard_case(kind)
    for kind in ('readonly', 'apply', 'lost_patch_response', 'main_excluded', 'different_main_doi', 'package_conflict',
                 'historical_conflict', 'wrong_compare', 'main_moves', 'head_moves'):
        integration_flow_case(kind)
    for kind in ('default_readonly', 'publish', 'lost_stage', 'lost_publish'):
        zenodo_flow_case(kind)
    for kind in ('valid', 'wrong_environment', 'wrong_title', 'file_drift', 'metadata_normalization'):
        kit_serialization_case(kind)
    # Explicit safe path checks are independent of gate fixture details.
    for name in ('../escape', '/absolute', 'a//b', 'a/./b', 'a/../b', 'private_sources/x',
                 'private_cases/x', '.secrets/x', '.zenodo-state/x', '__pycache__/x.pyc', 'a\\b'):
        case('unsafe_path_' + str(len(RESULTS)), lambda f, name=name: failure(lambda: c.relative(name),
             'Private or generated path' if any(x in name for x in c.FORBIDDEN) else 'path'))
    result = {'scope': 'Offline operational guard probes; fabricated fixtures are private, never production receipts.',
              'all_passed': True, 'case_count': len(RESULTS), 'real_external_calls': 0,
              'cases': RESULTS, 'finite_control_limit': 'These tests do not prove math or guarantee atomic multi-runner behavior.'}
    suffix = 'optimized' if not __debug__ else 'normal'
    (OPERATIONS / ('OFFLINE_CONTROLS_' + suffix.upper() + '.json')).write_bytes(c.json_bytes(result))
    print(json.dumps({'all_passed': True, 'case_count': len(RESULTS), 'real_external_calls': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
