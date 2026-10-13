#!/usr/bin/env python3
"""Independent offline operations harness. Never calls external commands or APIs.

Frozen helper/contract bytes and raw packet inputs stay outside the public output
manifest. Synthetic publication/gate/remote receipts are generated only under
private_cases, are marked mock, and are never treated as publication evidence.
Run: python3 -B test_publication_operations.py [--root REVIEW_DIRECTORY]
"""
import argparse
import base64
import contextlib
import copy
import datetime
import hashlib
import io
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import types
from unittest.mock import patch

sys.dont_write_bytecode = True
PREFIX = 'unsolved_math_prioritization/attempts/30000689/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
ORIGINAL = '8527ccdba064bca52035fc6c8d96caa750ac9c00'
MAIN = '1' * 40
TITLE = 'Missing faces and topological embeddings of sphere skeleta'
DOI = 'https://doi.org/10.0000/OFFLINE-MOCK-NOT-A-PUBLICATION'
PDF = 'missing_faces_and_sphere_skeleta.pdf'
ZIP = 'missing_faces_verification_v1.zip'
HEADER = '| Rank | ID / code | Problem | EV | Impact (/10) | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI |\n'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text())


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def forbidden(*args, **kwargs):
    raise AssertionError('External operation is forbidden in this harness')


def module(path, name):
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), m.__dict__)
    # No helper can invoke a real process, including its imported kit.
    m.subprocess = types.SimpleNamespace(run=forbidden, check_output=forbidden,
                                        TimeoutExpired=subprocess.TimeoutExpired)
    return m


class Fixture:
    def __init__(self, root, name):
        self.root = root
        self.repo = root / 'private_cases' / name / 'repository'
        self.program = self.repo / 'draft_pr_claimed_solved_400_500_20261011'
        self.audit = self.program / 'audits/pr468_30000689'
        if self.repo.parent.exists():
            shutil.rmtree(self.repo.parent)
        shutil.copytree(root / 'private_sources/context', self.audit)
        self.frozen = root / 'private_sources/frozen_helpers'
        self.gate = {'mock_fixture': True, 'verdict': 'ACCEPTED_FOR_PREPRINT_PUBLICATION',
                     'pr': 468, 'review_input_manifest': 'PACKAGE_REVIEW_INPUT_4.json',
                     'complete_package_reviews': []}
        for n in (1, 2):
            path = self.audit / f'mock_review_{n}.md'
            path.write_text('MOCK gate report; no mathematical or publication evidence.\n')
            self.gate['complete_package_reviews'].append(
                {'path': path.name, 'sha256': sha(path.read_bytes()), 'verdict': 'PASS',
                 'blocking_issue_count': 0, 'required_correction_count': 0})
        self.write_gate()
        freeze = load(self.audit / 'PACKAGE_REVIEW_INPUT_4.json')
        self.pub = {'mock_fixture': True, 'state': 'published', 'environment': 'production',
                    'title': TITLE, 'doi_url': DOI, 'doi': DOI.removeprefix('https://doi.org/'),
                    'record_url': 'https://example.invalid/OFFLINE-MOCK',
                    'files': [{'name': PDF, 'sha256': freeze['files']['manuscript.pdf']['sha256']},
                              {'name': ZIP, 'sha256': freeze['files'][ZIP]['sha256']}]}
        save(self.audit / 'ZENODO_PUBLISH_RECEIPT.json', self.pub)
        save(self.audit / 'TRACKER_APPEND_RECEIPT.json',
             {'mock_fixture': True, 'verified': True, 'values': [['mock', '', DOI, 'mock']]})
        self.row = load(self.audit / 'SOURCE_RECEIPT.json')['selected_queue_row'] + '\n'
        self.original_queue = (HEADER + self.row).encode()
        self.other = '| 999 | 999999 / OTHER | changed on latest main | 0 | 1 | 1 | 2026 | queued | 1/5 | | unrelated preserved | |\n'
        self.main_queue = (HEADER + self.other + self.row.replace('claimed_solved', 'queued').replace('3/5', '1/5')).encode()
        self.events = []
        self.writes = []
        self.mode = 'normal'

    def write_gate(self):
        save(self.audit / 'FINAL_ACCEPTANCE_GATE.json', self.gate)

    def invoke(self, m, apply=True):
        output = io.StringIO()
        error = None
        with patch.object(sys, 'argv', ['helper'] + (['--apply'] if apply else [])), contextlib.redirect_stdout(output):
            try:
                m.main()
            except Exception as exc:
                error = exc
        return error, output.getvalue()

    def integration(self):
        m = module(self.frozen / 'integrate_pr468_publication.py', 'offline_integration')
        m.PROGRAM, m.REPOSITORY, m.AUDIT = self.program, self.repo, self.audit
        self.blobs, self.entries, self.commit_files = {}, [], {}
        self.branch_head = ORIGINAL
        self.pr_reads = 0
        self.unrelated_main = {'unrelated/latest-main.txt': b'latest main content survives\n',
                               PREFIX + 'unrelated_existing.txt': b'same target folder preserved\n'}
        self.pr = {'state': 'open', 'draft': True, 'head': {'sha': ORIGINAL,
                   'repo': {'full_name': 'AlecKriebel/Math'}, 'ref': 'existing-pr468-branch'}}

        def read(path, head):
            self.events.append('read:' + head[:8] + ':' + path)
            if head == ORIGINAL:
                if path == QUEUE:
                    return self.original_queue
                data = (self.audit / 'source_snapshot' / path).read_bytes()
                return data + b'drift' if self.mode == 'source_drift' else data
            if head == MAIN and path == QUEUE:
                return self.main_queue
            if head == '3' * 40:
                data = self.commit_files[path]
                return data + b'drift' if self.mode == 'installed_drift' and path.endswith('manuscript.pdf') else data
            raise AssertionError('Unexpected mocked read: ' + path + '@' + head)

        def api(endpoint, payload=None, method=None, raw=False):
            self.events.append(endpoint)
            if payload is not None:
                self.writes.append(endpoint)
            if endpoint == 'pulls/468':
                self.pr_reads += 1
                result = copy.deepcopy(self.pr)
                if self.mode == 'pr_moves_after_blobs' and self.pr_reads > 1:
                    result['head']['sha'] = '2' * 40
                return result
            if endpoint.startswith('pulls/468/files'):
                paths = [x['path'] for x in load(self.audit / 'SOURCE_RECEIPT.json')['files']] + [QUEUE]
                if self.mode == 'unrelated_original_change':
                    paths.append('outside-target.txt')
                return [{'filename': p} for p in paths]
            if endpoint == 'git/ref/heads/main':
                return {'object': {'sha': MAIN}}
            if endpoint == 'git/commits/' + MAIN:
                return {'tree': {'sha': 'main-tree'}}
            if endpoint == 'git/blobs':
                data = base64.b64decode(payload['content'])
                key = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                self.blobs[key] = data
                return {'sha': key}
            if endpoint == 'git/trees':
                assert payload['base_tree'] == 'main-tree'
                self.entries = payload['tree']
                self.commit_files = dict(self.unrelated_main)
                self.commit_files[QUEUE] = self.main_queue
                self.commit_files.update({x['path']: self.blobs[x['sha']] for x in self.entries})
                return {'sha': 'accepted-tree'}
            if endpoint == 'git/commits':
                assert payload['parents'] == [ORIGINAL, MAIN]
                assert payload['tree'] == 'accepted-tree'
                return {'sha': '3' * 40}
            if endpoint == 'compare/' + MAIN + '...' + '3' * 40:
                paths = [x['path'] for x in self.entries]
                if self.mode == 'unrelated_commit_diff':
                    paths.append('outside-target.txt')
                return {'files': [{'filename': x} for x in paths]}
            if endpoint == 'git/refs/heads/existing-pr468-branch':
                assert method == 'PATCH' and payload == {'sha': '3' * 40, 'force': False}
                saved = load(self.audit / 'BRANCH_INTEGRATION_RECEIPT.json')
                assert saved['commit_sha'] == '3' * 40 and saved['state'] == 'commit_created_before_ref_update'
                if self.mode == 'branch_rejected':
                    self.branch_head = '2' * 40
                    raise RuntimeError('mock nonforced ref update rejected')
                self.branch_head = '3' * 40
                if self.mode == 'branch_lost_response':
                    raise RuntimeError('mock lost ref update response')
                return {'object': {'sha': self.branch_head}}
            if endpoint == 'git/ref/heads/existing-pr468-branch':
                return {'object': {'sha': self.branch_head}}
            raise AssertionError('Unimplemented API endpoint: ' + endpoint)

        m.read, m.api = read, api
        return m

    def replacement(self):
        m = module(self.frozen / 'replace_pr468_draft_archive.py', 'offline_replacement')
        m.PROGRAM, m.REPOSITORY, m.AUDIT = self.program, self.repo, self.audit
        m.MANIFEST = self.audit / 'package/deposit.json'
        kit = module(self.frozen / 'zenodo.py', 'offline_contract')
        metadata, wanted = kit.load_manifest(m.MANIFEST)
        backup = self.audit / 'references/private_sources/round3_accepted' / ZIP
        old = {'filename': ZIP, 'id': 'old-file-uuid', 'filesize': backup.stat().st_size,
               'checksum': 'md5:' + hashlib.md5(backup.read_bytes()).hexdigest()}
        pdf = {'filename': PDF, 'id': 'pdf-file-uuid', 'filesize': wanted[0]['size'], 'checksum': 'md5:' + wanted[0]['md5']}
        pdf_wanted = next(x for x in wanted if x['name'] == PDF)
        pdf.update(filesize=pdf_wanted['size'], checksum='md5:' + pdf_wanted['md5'])
        self.deposit = {'id': 23310484, 'submitted': False, 'metadata': copy.deepcopy(metadata), 'files': [pdf, old]}
        self.get_count = 0
        self.token_reads = 0
        def local_state(path, environment):
            self.events.append('mock_local_state')
            assert path == m.MANIFEST.resolve() and environment == 'production'
            return self.audit / 'mock_state.json', {'id': 1 if self.mode == 'wrong_saved_draft' else 23310484}
        def token(environment):
            self.token_reads += 1
            return 'OFFLINE-MOCK-NOT-A-CREDENTIAL'
        class Client:
            base = 'https://zenodo.org'
            def __init__(client, environment, token_value):
                assert environment == 'production' and token_value == 'OFFLINE-MOCK-NOT-A-CREDENTIAL'
            def get(client, draft):
                assert draft == 23310484
                self.get_count += 1
                self.events.append('GET draft')
                if self.mode == 'readback_lost' and self.get_count > 1:
                    raise kit.DepositError('mock readback lost')
                if self.mode == 'pdf_changes_after_delete' and self.get_count > 1:
                    self.deposit['files'][0]['checksum'] = 'md5:bad'
                return copy.deepcopy(self.deposit)
            def request(client, method, url):
                self.events.append(method + ' draft old ZIP')
                self.writes.append(method)
                assert method == 'DELETE' and url.endswith('/23310484/files/old-file-uuid')
                prior = load(self.audit / 'ZENODO_ARCHIVE_REPLACE_OPERATION.json')
                assert prior['state'] == 'delete_attempted_once'
                if self.mode != 'delete_failed_kept_zip':
                    self.deposit['files'] = [x for x in self.deposit['files'] if x['filename'] != ZIP]
                if self.mode in {'delete204', 'delete_lost_response', 'delete_failed_kept_zip'}:
                    raise kit.DepositError('mock empty HTTP204 or lost/error response')
                return {'mock': True}
        kit.local_state, kit.token_for, kit.ZenodoClient = local_state, token, Client
        class Loader:
            def exec_module(loader, target):
                target.__dict__.update(kit.__dict__)
        loader = Loader()
        m.importlib = types.SimpleNamespace(util=types.SimpleNamespace(
            spec_from_file_location=lambda *a: types.SimpleNamespace(loader=loader),
            module_from_spec=lambda *a: types.ModuleType('injected_offline_contract')))
        def check_output(cmd):
            self.events.append('mock gh read')
            return (json.dumps({'state': 'OPEN', 'isDraft': True, 'headRefOid': ORIGINAL}).encode()
                    if cmd[1] == 'pr' else self.original_queue)
        m.subprocess.check_output = check_output
        self.kit, self.wanted = kit, wanted
        return m

    def tracker(self):
        m = module(self.frozen / 'register_pr468_tracker.py', 'offline_tracker')
        m.ROOT = self.audit
        self.sheet = [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'],
                      ['unrelated row preserved', 'https://example.invalid/old', '10.0000/OTHER', 'original note']]
        self.original_unrelated = copy.deepcopy(self.sheet[1])
        self.full_reads, self.range_reads = 0, 0
        def cli(action, params, body=None):
            self.events.append(action + ':' + params['range'])
            assert params['spreadsheetId'] == m.SHEET
            if action == 'append':
                self.writes.append('append')
                assert params['valueInputOption'] == 'RAW' and params['insertDataOption'] == 'INSERT_ROWS'
                assert load(self.audit / 'TRACKER_APPEND_OPERATION.json')['state'] == 'append_attempted_once'
                self.intended = copy.deepcopy(body['values'])
                if self.mode != 'append_unconfirmed':
                    self.sheet.append(copy.deepcopy(body['values'][0]))
                if self.mode in {'append_lost', 'append_unconfirmed'}:
                    raise subprocess.TimeoutExpired('mock append', 60)
                return {'updates': {'updatedRows': 2 if self.mode == 'wrong_append_size' else 1,
                                    'updatedColumns': 4, 'updatedRange': "'Math Puzzles'!A3:D3"}}
            assert action == 'get'
            if params['range'] == "'Math Puzzles'!A1:D1":
                return {'values': [self.sheet[0]]}
            if params['range'] == "'Math Puzzles'!A:D":
                self.full_reads += 1
                return {'values': copy.deepcopy(self.sheet)}
            self.range_reads += 1
            row = int(params['range'].split('!A')[1].split(':')[0])
            if self.mode == 'row_changes_final' and self.range_reads == 2:
                self.sheet[row-1][3] = 'concurrent edit'
            value = copy.deepcopy(self.sheet[row-1])
            if self.mode == 'concurrent_duplicate' and self.range_reads == 1:
                self.sheet.append(copy.deepcopy(self.sheet[row-1]))
            return {'values': [value]}
        m.cli = cli
        return m


def assert_rejected(error, fixture, no_writes=True):
    assert isinstance(error, (RuntimeError, KeyError, ValueError, fixture.kit.DepositError if hasattr(fixture, 'kit') else RuntimeError)), repr(error)
    if no_writes:
        assert fixture.writes == [], fixture.writes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.root.resolve()
    frozen_receipt = load(root / 'SOURCE_FREEZE_RECEIPT.json')
    for name, item in frozen_receipt['files'].items():
        assert sha((root / 'private_sources/frozen_helpers' / name).read_bytes()) == item['sha256']
    results = []

    def run(name, exercise):
        f = Fixture(root, name)
        try:
            detail = exercise(f)
            results.append({'case': name, 'status': 'PASS', 'detail': detail,
                            'mock_remote_mutations': f.writes, 'mock_call_count': len(f.events)})
        except Exception as exc:
            results.append({'case': name, 'status': 'FAIL', 'error': type(exc).__name__ + ': ' + str(exc),
                            'mock_remote_mutations': f.writes, 'mock_call_count': len(f.events)})

    def guard(f, family, field, value, missing=False):
        if missing:
            del f.gate['complete_package_reviews'][0][field]
        else:
            f.gate['complete_package_reviews'][0][field] = value
        f.write_gate()
        m = getattr(f, family)()
        err, _ = f.invoke(m)
        assert_rejected(err, f)
        if family == 'replacement':
            assert f.token_reads == 0 and f.get_count == 0
        return 'Malformed/nonzero review count rejected before any remote mutation.'

    def hold(f, family):
        save(f.audit / 'FINAL_ACCEPTANCE_GATE.json', frozen_receipt['actual_gate'])
        m = getattr(f, family)()
        err, _ = f.invoke(m)
        assert_rejected(err, f)
        if family == 'replacement':
            assert f.token_reads == 0
        return 'Actual frozen HOLD gate rejects --apply; remote mutation count zero.'

    with patch.object(socket, 'create_connection', forbidden), patch.object(subprocess, 'run', forbidden), patch.object(subprocess, 'check_output', forbidden):
        for family in ('integration', 'replacement'):
            for field in ('blocking_issue_count', 'required_correction_count'):
                for tag, value, missing in [('missing',None,True),('null',None,False),('bool_false',False,False),
                                            ('bool_true',True,False),('float_zero',0.0,False),('string_zero','0',False),
                                            ('one',1,False),('negative',-1,False)]:
                    run(f'{family}_{field}_{tag}', lambda f, family=family, field=field, value=value, missing=missing: guard(f,family,field,value,missing))
            run(f'{family}_actual_hold', lambda f, family=family: hold(f,family))

        def integration_case(f, mode='normal', prepare=None, expected_reject=False, no_writes=True):
            f.mode = mode
            m = f.integration()
            if prepare:
                prepare(f)
            err, _ = f.invoke(m)
            if expected_reject:
                assert_rejected(err, f, no_writes)
                assert not (f.audit / 'PR_BODY_CURRENT.md').exists()
                return 'Rejected at guard/readback; no successful branch-verification declaration.'
            assert err is None, repr(err)
            receipt = load(f.audit / 'BRANCH_INTEGRATION_RECEIPT.json')
            assert receipt['state'] == 'branch_updated_verified' and receipt['commit_sha'] == '3'*40
            assert f.branch_head == receipt['commit_sha'] and receipt['parent_main_sha'] == MAIN
            for path,data in f.unrelated_main.items():
                assert f.commit_files[path] == data
            for item in load(f.audit / 'SOURCE_RECEIPT.json')['files']:
                path = item['path']
                data = (f.audit / 'source_snapshot' / path).read_bytes()
                if path not in {PREFIX + 'PUBLICATION_NOTES.md', PREFIX + 'PUBLICATION_MANIFEST.json'}:
                    assert f.commit_files[path] == data
                historical = PREFIX + 'preprint_20261012/verification/historical/' + path.removeprefix(PREFIX)
                assert f.commit_files[historical] == data
            lines = f.commit_files[QUEUE].decode().splitlines(keepends=True)
            assert lines[0] == HEADER and lines[1] == f.other and len(lines) == 3
            assert ' claimed_solved ' in lines[2] and ' 3/5 ' in lines[2] and DOI in lines[2]
            assert all('merge' not in x for x in f.events)
            return 'Zero-count gate succeeds; latest-main unrelated files/row preserved, exactly one target row changes; nonforced existing-branch update read back to recorded commit; no merge.'

        run('integration_zero_baseline', integration_case)
        run('integration_lost_ref_response', lambda f: integration_case(f,'branch_lost_response'))
        cases = [
            ('wrong_original_head','normal',lambda f:f.pr['head'].update(sha='2'*40),True),
            ('excluded_status','normal',lambda f:setattr(f,'original_queue',f.original_queue.replace(b'claimed_solved',b'solved')),True),
            ('duplicate_target_queue','normal',lambda f:setattr(f,'main_queue',f.main_queue+f.row.encode()),True),
            ('main_disposition_changed','normal',lambda f:setattr(f,'main_queue',f.main_queue.replace(b'queued',b'solved')),True),
            ('main_different_doi','normal',lambda f:setattr(f,'main_queue',f.main_queue[:-3]+b'other DOI |\n'),True),
            ('source_hash_drift','source_drift',None,True),
            ('accepted_hash_drift','normal',lambda f:(f.audit/'package/manuscript.pdf').write_bytes(b'drift'),True),
            ('review_hash_drift','normal',lambda f:(f.audit/'mock_review_1.md').write_text('drift'),True),
            ('install_hash_drift','normal',lambda f:mutate_install(f),True),
            ('unrelated_original_change','unrelated_original_change',None,True),
            ('pr_moves_after_blobs','pr_moves_after_blobs',None,False),
            ('unrelated_commit_diff','unrelated_commit_diff',None,False),
            ('branch_update_rejected','branch_rejected',None,False),
            ('installed_byte_drift','installed_drift',None,False),
        ]
        def mutate_install(f):
            plan=load(f.audit/'BRANCH_INSTALL_PLAN.json');plan['entries'][0]['sha256']='bad';save(f.audit/'BRANCH_INSTALL_PLAN.json',plan)
        for name,mode,prep,no_write in cases:
            run('integration_'+name,lambda f,mode=mode,prep=prep,no_write=no_write:integration_case(f,mode,prep,True,no_write))

        def replacement_case(f, mode='normal', prepare=None, reject=False, no_writes=True, apply=True):
            f.mode=mode
            m=f.replacement()
            if prepare:
                prepare(f)
            err,_=f.invoke(m,apply)
            if reject:
                assert_rejected(err,f,no_writes)
                assert not (f.audit/'ZENODO_ARCHIVE_REPLACE_RECEIPT.json').exists()
                return 'Rejected unsafe/unconfirmed replacement; no successful removal receipt.'
            assert err is None, repr(err)
            assert f.writes == (['DELETE'] if apply else [])
            if apply:
                receipt=load(f.audit/'ZENODO_ARCHIVE_REPLACE_RECEIPT.json')
                assert receipt['state']=='superseded_zip_absent_verified' and receipt['id']==23310484
                assert [x['filename'] for x in f.deposit['files']]==[PDF]
            return 'Known old ZIP only; same unpublished draft, exact metadata, reviewed PDF preserved, one DELETE at most.'

        for mode in ('normal','delete204','delete_lost_response'):
            run('replacement_'+mode,lambda f,mode=mode:replacement_case(f,mode))
        run('replacement_readonly',lambda f:replacement_case(f,apply=False))
        def prior(f):
            backup=f.audit/'references/private_sources/round3_accepted'/ZIP
            save(f.audit/'ZENODO_ARCHIVE_REPLACE_OPERATION.json',{'mock_fixture':True,'id':23310484,'state':'delete_attempted_once','old_archive_sha256':sha(backup.read_bytes()),'file_id':'old-file-uuid'})
        def resume(f):
            m=f.replacement();prior(f);f.deposit['files']=[x for x in f.deposit['files'] if x['filename']!=ZIP]
            err,_=f.invoke(m);assert err is None,repr(err);assert f.writes==[]
            assert load(f.audit/'ZENODO_ARCHIVE_REPLACE_RECEIPT.json')['state']=='superseded_zip_absent_verified'
            return 'Recorded prior removal resumes by GET only, no repeat DELETE.'
        run('replacement_resume_absent_after_prior',resume)
        def already(f):
            m=f.replacement();wanted=next(x for x in f.wanted if x['name']==ZIP)
            f.deposit['files'][1].update(filesize=wanted['size'],checksum='md5:'+wanted['md5'])
            err,_=f.invoke(m);assert err is None,repr(err);assert f.writes==[]
            assert load(f.audit/'ZENODO_ARCHIVE_REPLACE_RECEIPT.json')['state']=='accepted_archive_already_present'
            return 'Accepted ZIP already present verifies full packet without deleting.'
        run('replacement_already_accepted',already)
        replacement_cases=[
            ('wrong_saved_draft','wrong_saved_draft',None,True),
            ('wrong_remote_draft','normal',lambda f:f.deposit.update(id=23310485),True),
            ('published','normal',lambda f:f.deposit.update(submitted=True),True),
            ('metadata_drift','normal',lambda f:f.deposit['metadata'].update(version='2.0'),True),
            ('pdf_drift','normal',lambda f:f.deposit['files'][0].update(checksum='md5:bad'),True),
            ('unknown_zip','normal',lambda f:f.deposit['files'][1].update(checksum='md5:bad'),True),
            ('unsafe_file_id','normal',lambda f:f.deposit['files'][1].update(id='../other'),True),
            ('unexpected_file','normal',lambda f:f.deposit['files'].append({'filename':'extra','id':'extra'}),True),
            ('missing_without_prior','normal',lambda f:f.deposit.update(files=f.deposit['files'][:1]),True),
            ('prior_zip_still_present','normal',prior,True),
            ('delete_failed_kept_zip','delete_failed_kept_zip',None,False),
            ('readback_lost','readback_lost',None,False),
            ('pdf_changes_after_delete','pdf_changes_after_delete',None,False),
            ('source_scope_excluded','normal',lambda f:setattr(f,'original_queue',f.original_queue.replace(b'claimed_solved',b'solved')),True),
        ]
        for name,mode,prep,no_write in replacement_cases:
            run('replacement_'+name,lambda f,mode=mode,prep=prep,no_write=no_write:replacement_case(f,mode,prep,True,no_write))

        def intended(f,m):
            err,_=f.invoke(m,False);assert err is None,repr(err)
            value=load(f.audit/'TRACKER_APPEND_OPERATION.json')['values'][0]
            assert TITLE in value[3] and 'version 1.0, 12 October 2026' in value[3]
            assert 'https://ems.press/content/serial-article-files/46090 (p. 238, Conjecture 4)' in value[0]
            assert 'https://github.com/AlecKriebel/Math/pull/468' in value[3]
            assert value[1]=='' and value[2]==DOI
            f.full_reads,f.range_reads=0,0
            return value
        def tracker_case(f,mode='normal',prep=None,reject=False,no_writes=False,apply=True):
            f.mode=mode;m=f.tracker()
            if prep:prep(f,m)
            err,_=f.invoke(m,apply)
            if reject:
                assert_rejected(err,f,no_writes)
                assert not (f.audit/'TRACKER_APPEND_RECEIPT.json').exists() or load(f.audit/'TRACKER_APPEND_RECEIPT.json').get('mock_fixture') is True
                return 'Duplicate/changed/unconfirmed registration rejected; this runner never repeats append.'
            assert err is None,repr(err)
            assert f.sheet[1]==f.original_unrelated
            if apply:
                receipt=load(f.audit/'TRACKER_APPEND_RECEIPT.json')
                assert receipt['verified'] is True and receipt['unique_doi_row_at_final_snapshot'] is True
                assert receipt['updated_range']=="'Math Puzzles'!A3:D3"
                assert receipt['values']==[f.sheet[2]]
                assert 'No atomic multi-runner guarantee' in receipt['concurrency_scope']
            return 'Exact readable row verified at final scan and exact range; unrelated row preserved; at most one append.'
        run('tracker_zero_baseline',tracker_case)
        run('tracker_lost_append_response',lambda f:tracker_case(f,'append_lost'))
        run('tracker_readonly',lambda f:tracker_case(f,apply=False))
        run('tracker_identical_existing',lambda f:tracker_case(f,prep=lambda f,m:f.sheet.append(intended(f,m))))
        run('tracker_duplicate_initial',lambda f:tracker_case(f,prep=lambda f,m:f.sheet.extend([intended(f,m)]*2),reject=True,no_writes=True))
        run('tracker_same_doi_different_values',lambda f:tracker_case(f,prep=lambda f,m:f.sheet.append(['different','',DOI,'different']),reject=True,no_writes=True))
        run('tracker_token_form_existing_differs',lambda f:tracker_case(f,prep=lambda f,m:f.sheet.append(['different','',DOI.removeprefix('https://doi.org/'),'different']),reject=True,no_writes=True))
        run('tracker_concurrent_same_doi_insertion',lambda f:tracker_case(f,'concurrent_duplicate',reject=True))
        run('tracker_final_exact_range_edit',lambda f:tracker_case(f,'row_changes_final',reject=True))
        run('tracker_wrong_append_size',lambda f:tracker_case(f,'wrong_append_size',reject=True))
        def unconfirmed(f):
            f.mode='append_unconfirmed';m=f.tracker();err,_=f.invoke(m)
            assert_rejected(err,f,False);assert f.writes==['append']
            err,_=f.invoke(m);assert_rejected(err,f,False);assert f.writes==['append']
            return 'First unconfirmed timeout records attempt; rerun with no row fails before another append.'
        run('tracker_unconfirmed_append_rerun',unconfirmed)

        # The unchanged kit is exercised with its real manifest/verify/run
        # functions and a wholly synthetic client, state and DOI resolver.
        def contract_case(f, mode):
            f.mode = 'normal'
            f.replacement()
            kit = f.kit
            metadata, files = kit.load_manifest(f.audit / 'package/deposit.json')
            if mode.startswith('stage'):
                f.deposit['files'] = f.deposit['files'][:1]
            else:
                f.deposit['files'] = [{'filename':x['name'],'id':'mock-'+str(i),
                                       'filesize':x['size'],'checksum':'md5:'+x['md5']}
                                      for i,x in enumerate(files)]
            f.deposit['links'] = {'bucket':'https://zenodo.org/api/files/OFFLINE-MOCK',
                                  'html':'https://example.invalid/OFFLINE-MOCK'}
            f.deposit['doi'] = DOI.removeprefix('https://doi.org/')
            kit.save_state = lambda path,value: save(f.audit/'mock_kit_persist.json',
                                                    {'mock_fixture':True,'value':value})
            kit.doi_status = lambda value: {'status':'OFFLINE-MOCK-NOT-CHECKED'}
            class ContractClient:
                def create(client, value):
                    raise AssertionError('Stable saved manifest must never create a new deposit')
                def get(client, draft):
                    assert draft == 23310484
                    f.events.append('kit GET same draft')
                    return copy.deepcopy(f.deposit)
                def upload(client, bucket, entry):
                    assert bucket == f.deposit['links']['bucket'] and entry['name'] == ZIP
                    f.writes.append('upload accepted ZIP')
                    f.deposit['files'].append({'filename':entry['name'],'id':'mock-new-zip',
                                              'filesize':entry['size'],'checksum':'md5:'+entry['md5']})
                    if mode == 'stage_lost_upload':
                        raise kit.DepositError('mock upload committed but response lost')
                    return {'mock_fixture':True}
                def update(client, draft, value):
                    assert draft == 23310484 and value == metadata
                    f.writes.append('metadata update same draft')
                    f.deposit['metadata'] = copy.deepcopy(value)
                    return copy.deepcopy(f.deposit)
                def publish(client, draft):
                    assert draft == 23310484
                    f.writes.append('publish same draft')
                    if mode != 'publish_unconfirmed':
                        f.deposit['submitted'] = True
                    if mode == 'publish_bad_readback':
                        f.deposit['files'][0]['checksum'] = 'md5:bad'
                    if mode in {'publish_lost_response','publish_unconfirmed'}:
                        raise kit.DepositError('mock publish response lost')
                    return copy.deepcopy(f.deposit)
            client = ContractClient()
            command = 'stage' if mode.startswith('stage') else 'publish'
            args = types.SimpleNamespace(command=command, manifest=f.audit/'package/deposit.json',
                                         sandbox=False, confirm_id=23310484,check_doi=False)
            pdf_before = copy.deepcopy(f.deposit['files'][0])
            if mode == 'stage_lost_upload':
                try:
                    kit.run(args,client)
                except kit.DepositError:
                    pass
                else:
                    raise AssertionError('Lost upload must be unconfirmed on first attempt')
                assert f.writes == ['upload accepted ZIP']
                result = kit.run(args,client)
                assert result['state']=='ready_to_publish'
                assert f.writes==['upload accepted ZIP','metadata update same draft']
            elif mode in {'publish_unconfirmed','publish_bad_readback'}:
                try:
                    kit.run(args,client)
                except kit.DepositError:
                    pass
                else:
                    raise AssertionError('Unconfirmed/drifted publication must fail')
                assert f.writes == ['publish same draft']
                assert not (f.audit/'mock_kit_persist.json').exists()
                return 'One publication attempt; unconfirmed or mismatching readback fails without a verified receipt or automatic retry.'
            else:
                result = kit.run(args,client)
                assert result['state'] == ('ready_to_publish' if command=='stage' else 'published')
                if command=='stage':
                    assert f.writes==['upload accepted ZIP','metadata update same draft']
                else:
                    assert result['recovered_after_publish_error'] is True
                    repeated=kit.run(args,client)
                    assert repeated['already_published'] is True
                    assert f.writes==['publish same draft']
            assert f.deposit['files'][0] == pdf_before
            assert kit.verify(f.deposit,metadata,files)==[]
            return 'Stable saved manifest resumes same draft; real contract checks exact files; reviewed PDF untouched; no second upload/publication after committed lost response.'
        for mode in ('stage_resume','stage_lost_upload','publish_lost_response','publish_unconfirmed','publish_bad_readback'):
            run('kit_'+mode,lambda f,mode=mode:contract_case(f,mode))

        def checkpoint(f, excluded=None, alias=False, direct_link=False):
            m=module(f.frozen/'publish_checkpoint.py','offline_checkpoint')
            m.ROOT,m.REPOSITORY_ROOT=f.program,f.repo
            public=f.program/'own_review.md'
            public.write_text('Own public checkpoint report.\n')
            other=f.program/'own_harness.py'
            other.write_text('# Own public harness.\n')
            selected=[str(public.relative_to(f.repo)),str(other.relative_to(f.repo))]
            if excluded:
                private=f.program/excluded/'excluded.txt';private.parent.mkdir(parents=True,exist_ok=True)
                private.write_text('OFFLINE SYNTHETIC PRIVATE CONTENT; NOT A CREDENTIAL.\n')
                if alias:
                    link=f.program/'innocent_alias';link.symlink_to(private.parent,target_is_directory=True)
                    selected.append(str((link/private.name).relative_to(f.repo)))
                else:
                    selected.append(str(private.relative_to(f.repo)))
            if direct_link:
                link=f.program/'direct_link.md';link.symlink_to(public)
                selected.append(str(link.relative_to(f.repo)))
            listing=f.audit/'mock_checkpoint_list.json';save(listing,selected)
            def api(endpoint,payload=None):
                f.events.append(endpoint)
                if payload is not None:f.writes.append(endpoint)
                if endpoint=='git/blobs':return {'sha':sha(base64.b64decode(payload['content']))}
                if endpoint=='git/ref/heads/main':return {'object':{'sha':('3'*40 if 'git/refs/heads/main' in f.writes else MAIN)}}
                if endpoint=='git/commits/'+MAIN:return {'tree':{'sha':'main-tree'}}
                if endpoint=='git/trees':
                    assert payload['base_tree']=='main-tree' and {x['path'] for x in payload['tree']}==set(selected)
                    return {'sha':'new-tree'}
                if endpoint=='git/commits':
                    assert payload['parents']==[MAIN];return {'sha':'3'*40}
                if endpoint=='git/refs/heads/main':
                    assert payload=={'sha':'3'*40,'force':False};return {'object':{'sha':'3'*40}}
                raise AssertionError('Unexpected checkpoint endpoint: '+endpoint)
            m.api=api
            receipt=f.audit/'mock_checkpoint_receipt.json'
            err=None
            with patch.object(sys,'argv',['checkpoint','--file-list',str(listing),'--message','OFFLINE MOCK','--receipt',str(receipt)]),contextlib.redirect_stdout(io.StringIO()):
                try:m.main()
                except Exception as exc:err=exc
            if excluded or direct_link:
                assert isinstance(err,ValueError),repr(err)
                assert f.events==[] and f.writes==[] and not receipt.exists()
                return 'Mixed public-first plus excluded/symlink path rejected before ANY mocked remote call or receipt.'
            assert err is None,repr(err)
            saved=load(receipt)
            assert set(saved['files_sha256'])==set(selected)
            assert len([x for x in f.writes if x=='git/blobs'])==2
            assert saved['readback_main_sha']==saved['commit_sha']=='3'*40
            return 'Explicit own-public-file list succeeds; precisely two selected blobs, nonforced main update and exact commit readback.'
        run('checkpoint_explicit_public_list',checkpoint)
        for component in ('private_sources','mutation_fixtures','.secrets','.zenodo-state','__pycache__'):
            run('checkpoint_mixed_'+component.replace('.',''),lambda f,component=component:checkpoint(f,excluded=component))
        run('checkpoint_resolved_private_directory_alias',lambda f:checkpoint(f,excluded='private_sources',alias=True))
        run('checkpoint_direct_symlink',lambda f:checkpoint(f,direct_link=True))

    result={'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope':'OFFLINE MOCK DIAGNOSTICS ONLY; not publication/registration evidence',
            'source_hashes':{n:i['sha256'] for n,i in frozen_receipt['files'].items()},
            'total_cases':len(results),'passed':sum(x['status']=='PASS' for x in results),
            'failed':sum(x['status']=='FAIL' for x in results),'cases':results,
            'live_remote_calls':0,'credential_or_state_reads':0}
    save(root/'MOCK_DIAGNOSTICS.json',result)
    print(json.dumps({k:result[k] for k in ('total_cases','passed','failed','live_remote_calls','credential_or_state_reads')},indent=2))
    for item in results:
        if item['status']=='FAIL':print(item['case']+': '+item['error'])
    return 1 if result['failed'] else 0


if __name__=='__main__':
    raise SystemExit(main())
