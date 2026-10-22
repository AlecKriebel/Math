#!/usr/bin/env python3
"""Run the exact private helper/dependency copies with every service mocked.

This program never invokes the original ledger helper. subprocess, urllib,
HTTPSConnection, and sockets are disabled/replaced before any project import.
Each invocation is one independent fixture and prints a checkable JSON receipt.
"""
import argparse
import copy
import datetime as dt
import hashlib
import http.client
import importlib.util
import io
import json
import marshal
import os
from pathlib import Path
import shutil
import socket
import stat
import struct
import subprocess
import sys
import types
import urllib.parse
import urllib.request

D = Path(__file__).resolve().parent
A = D.parent
R = A.parents[1]
DEPENDENCIES = ['publication_check.py', 'sweep_io.py', 'checkpoint.py',
                'audits/pr0399_30001179/ops_binding.py',
                'audits/pr0399_30001179/prepublication_check.py',
                '../zenodo_deposit_tool/zenodo.py']
HELPER_SHA = '75dd23fad8e65c87fb19267d168a26d05997a1e03a694d751bd85407bfa799da'
PLAN_SHA = '83df78463704c63ea3969a87325f18ab21c21893d6e1b8b49c5b16a6b4e3b2e1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ensure(value, reason):
    if not value:
        raise RuntimeError(reason)


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case')
    args = parser.parse_args()
    case = args.case
    ensure(sha(A / 'reconcile_external_ledger_v2.py') == HELPER_SHA, 'Original helper changed')
    ensure(sha(A / 'LEDGER_RECONCILIATION_PLAN.json') == PLAN_SHA, 'Original plan changed')
    fixture = D / 'private' / 'fixtures_final' / str(sys.flags.optimize) / case
    ensure(not fixture.exists(), 'Each fixture must be fresh')
    root = fixture / 'effort'
    audit = root / 'audits/pr1156_30003650'
    audit.mkdir(parents=True)
    for rel in DEPENDENCIES:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(R / rel, target)
    for name in ['reconcile_external_ledger_v2.py', 'LEDGER_RECONCILIATION_PLAN.json']:
        shutil.copyfile(A / name, audit / name)
    shutil.copytree(R / 'raw/pr1156', root / 'raw/pr1156')
    inventory = json.loads((R / 'rest_inventory.json').read_text())
    baseline_pr = copy.deepcopy(next(p for p in inventory['pull_requests'] if p['number'] == 1156))
    dump(root / 'rest_inventory.json', {'pull_requests': [baseline_pr]})
    plan = json.loads((audit / 'LEDGER_RECONCILIATION_PLAN.json').read_text())
    row = plan['proposed_row']
    adoption = {'ready_for_existing_publication_record': True,
                'helper_sha256': HELPER_SHA, 'plan_sha256': PLAN_SHA,
                'dependency_pins': {p: sha(root / p) for p in DEPENDENCIES},
                'review_pins': []}
    # This is deliberately a local synthetic review adoption, never a live grant.
    adoption_path = audit / 'ROOT_LEDGER_REVIEW02_ACCEPTANCE.json'
    if case == 'adoption_false': adoption['ready_for_existing_publication_record'] = False
    if case == 'wrong_helper_pin': adoption['helper_sha256'] = '0' * 64
    if case == 'wrong_plan_pin': adoption['plan_sha256'] = '0' * 64
    if case == 'missing_dependency_pin': adoption['dependency_pins'].pop('checkpoint.py')
    if case == 'dependency_changed':
        with (root / 'sweep_io.py').open('a') as f: f.write('\nraise RuntimeError("UNREVIEWED DEPENDENCY EXECUTED")\n')
    dump(adoption_path, adoption)
    adoption_sha = sha(adoption_path)
    if case == 'acceptance_sha_wrong': adoption_sha = '0' * 64
    if case == 'acceptance_missing': adoption_path.unlink()
    if case == 'prior_intent_absent': dump(audit / 'LEDGER_RECONCILIATION_INTENT.json', {'outcome': 'unknown'})
    if case == 'plan_changed_after_adoption':
        plan['proposed_row'][3] += ' CHANGED'
        dump(audit / 'LEDGER_RECONCILIATION_PLAN.json', plan)
    shadow_marker = audit / 'UNPINNED_IMPORT_EXECUTED'
    unpinned = "from pathlib import Path\nPath(" + repr(str(shadow_marker)) + ").write_text('executed')\nraise RuntimeError('UNPINNED IMPORT EXECUTED')\n"
    if case == 'shadow_publication_check':
        (root / 'audits/pr0399_30001179/publication_check.py').write_text(unpinned)
    if case == 'poison_timestamp_bytecode':
        target = root / 'publication_check.py'
        cache = Path(importlib.util.cache_from_source(str(target)))
        cache.parent.mkdir(parents=True, exist_ok=True)
        header = importlib.util.MAGIC_NUMBER + struct.pack('<III', 0, int(target.stat().st_mtime), target.stat().st_size)
        cache.write_bytes(header + marshal.dumps(compile(unpinned, str(target), 'exec')))
    sources = [root / p for p in DEPENDENCIES] + [audit / 'reconcile_external_ledger_v2.py', audit / 'LEDGER_RECONCILIATION_PLAN.json']
    before_sources = {str(p.relative_to(fixture)): sha(p) for p in sources}
    pinned_paths_still_match = all(sha(root / p) == digest for p, digest in adoption['dependency_pins'].items())
    service_events = []
    external_attempts = []
    reads = {'pr': 0, 'ledger': 0, 'account': 0}
    appends = []
    fsync_kinds = []
    ledger = [plan['schema_columns'], ['source unrelated', '', 'https://doi.org/10.5281/zenodo.12345678', 'unrelated existing row']]
    if case in {'exact_present', 'exact_present_with_intent'}:
        ledger.append(copy.deepcopy(row))
        if case.endswith('with_intent'): dump(audit / 'LEDGER_RECONCILIATION_INTENT.json', {'outcome': 'unknown'})
    if case == 'duplicate_exact': ledger += [copy.deepcopy(row), copy.deepcopy(row)]
    if case == 'existing_other_row': ledger.append(['different source', '', row[2], 'needs review'])
    identity_cells = {
        'concept_doi_existing': 'https://doi.org/10.5281/zenodo.23350363',
        'encoded_doi_existing': 'https://doi.org/10.5281%2fzenodo.%32%33%33%35%30%33%36%34',
        'nested_encoded_doi_existing': 'https://doi.org/10.5281%252fzenodo.23350363',
        'record_uri_existing': 'https://zenodo.org/records/23350364/files/main.pdf',
        'shortdoi_ambiguous': 'https://doi.org/abcde',
        'deep_encoding_ambiguous': 'https://doi.org/10.5281' + '%25' * 9 + '2fzenodo.23350364',
    }
    if case in identity_cells: ledger.append(['other source', '', identity_cells[case], 'existing identity lead'])
    if case == 'schema_wide_row': ledger[1].append('fifth column')
    if case == 'schema_wrong_header': ledger[0][3] = 'different notes'
    if case == 'schema_nonstring': ledger[1][1] = 27
    record = json.loads((root / 'raw/pr1156/zenodo_23350364.json').read_text())
    if case == 'provider_metadata_changed': record['metadata']['version'] = '1.1'
    if case == 'provider_concept_changed': record['conceptrecid'] = '23350362'
    if case == 'provider_file_extra': record['files'].append({'key': 'extra.txt', 'size': 1, 'checksum': 'md5:x'})
    if case == 'provider_unpublished': record['submitted'] = False
    live = {'number': 1156, 'head': {'sha': plan['head']}, 'base': {'sha': plan['base']},
            'body': baseline_pr['body'], 'state': 'open', 'merged': False, 'draft': False}
    if case == 'initial_pr_head_changed': live['head']['sha'] = '0' * 40
    if case == 'initial_pr_base_changed': live['base']['sha'] = '0' * 40
    if case == 'initial_pr_body_changed': live['body'] += 'changed'
    account = [{'id': 90000000 + i, 'metadata': {'title': 'Unrelated numbered note ' + str(i)}, 'files': []} for i in range(195)]
    account += [{'id': 23408971, 'metadata': {'title': 'Known owned note'}, 'files': []},
                {'id': 23174283, 'metadata': {'title': 'Known Fibonacci note'}, 'files': []}]
    if case == 'empty_wrong_account': account = []
    if case == 'wrong_account_same_count':
        account[-2]['id'] = 99000001
        account[-1]['id'] = 99000002
    if case == 'account_title_lead': account[0]['metadata']['title'] = 'The Maximal Finite CP-Plus-Rank Equals the Maximal CP-Rank'
    if case == 'account_alias_lead': account[0]['metadata']['title'] = 'OWR-15957-003'
    if case == 'account_md5_lead': account[0]['files'] = [{'checksum': plan['existing_publication']['files'][0]['checksum']}]
    if case == 'account_record_id_lead': account[0]['id'] = 23350364
    if case == 'account_concept_parent_lead': account[0]['parent'] = {'id': '23350363'}
    if case == 'account_top_level_doi_lead': account[0]['pids'] = {'doi': {'identifier': '10.5281/zenodo.23350364'}}
    if case == 'account_encoding_alias_lead': account[0]['metadata']['identifier'] = 'https://doi.org/10.5281%2fzenodo.%32%33%33%35%30%33%36%34'
    if case == 'account_partial': account = account[:-1]
    clock = {'elapsed_seconds': 0}
    actual_datetime = dt.datetime

    class SimulatedDatetime(actual_datetime):
        @classmethod
        def now(cls, tz=None):
            return actual_datetime.now(tz) + dt.timedelta(seconds=clock['elapsed_seconds'])

    def audit_hook(event, arguments):
        if event in {'subprocess.Popen', 'os.system', 'socket.connect', 'socket.connect_ex', 'socket.getaddrinfo'}:
            external_attempts.append(event)
            raise RuntimeError('FORBIDDEN EXTERNAL EFFECT: ' + event)

    sys.addaudithook(audit_hook)
    os.environ['ZENODO_TOKEN'] = 'OFFLINE-ONLY-NON-SECRET'
    os.environ['ZENODO_SANDBOX_TOKEN'] = 'OFFLINE-ONLY-NON-SECRET'
    sys.dont_write_bytecode = True
    real_fsync = os.fsync

    def observed_fsync(fd):
        fsync_kinds.append('directory' if stat.S_ISDIR(os.fstat(fd).st_mode) else 'regular_file')
        return real_fsync(fd)

    os.fsync = observed_fsync

    def fail_socket(*args, **kwargs):
        external_attempts.append('socket constructed')
        raise RuntimeError('Socket disabled in offline test')

    socket.socket = fail_socket

    def wrapped_range():
        return {'majorDimension': 'ROWS', 'range': "'Math Puzzles'!A1:AQ" + str(len(ledger)), 'values': copy.deepcopy(ledger)}

    def fake_run(arguments, *positional, **kwargs):
        service_events.append({'kind': 'process_mock', 'args': arguments})
        if arguments[0] == 'git':
            ensure('remote' in arguments and 'get-url' in arguments, 'Unexpected git operation')
            return subprocess.CompletedProcess(arguments, 0, stdout=b'https://github.com/AlecKriebel/Math.git\n', stderr=b'')
        if arguments[:3] == ['gh', 'api', 'repos/AlecKriebel/Math/pulls/1156']:
            reads['pr'] += 1
            value = copy.deepcopy(live)
            if reads['pr'] > 1:
                if case == 'immediate_pr_head_changed': value['head']['sha'] = '1' * 40
                if case == 'immediate_pr_base_changed': value['base']['sha'] = '1' * 40
                if case == 'immediate_pr_body_changed': value['body'] += 'changed'
                if case == 'delayed_preflight': clock['elapsed_seconds'] = 3600
        elif arguments[:3] == ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main']:
            value = {'object': {'sha': 'e' * 40}}
        elif arguments[:5] == ['gws', 'sheets', 'spreadsheets', 'values', 'get']:
            reads['ledger'] += 1
            if case == 'concurrent_before_append' and reads['ledger'] == 2:
                ledger.append(['unrelated concurrent row', '', '', 'concurrent'])
            if case == 'prefix_changed_after_append' and appends:
                ledger[1][3] = 'changed old notes'
            value = wrapped_range()
            if case == 'partial_range': value['range'] = "'Math Puzzles'!A1:D2"
            if case == 'wrong_major_dimension': value['majorDimension'] = 'COLUMNS'
        elif arguments[:4] == ['gws', 'sheets', 'spreadsheets', 'get']:
            title = 'Other' if case == 'wrong_title' else 'Math Puzzles'
            gid = 1254632078 if case == 'wrong_gid' else 1254632077
            value = {'spreadsheetId': plan['spreadsheet_id'], 'sheets': [{'properties': {'sheetId': gid, 'title': title}}]}
        elif arguments[:5] == ['gws', 'sheets', 'spreadsheets', 'values', 'append']:
            params = json.loads(arguments[arguments.index('--params') + 1])
            payload = json.loads(arguments[arguments.index('--json') + 1])
            ensure(params['spreadsheetId'] == plan['spreadsheet_id'] and params['range'] == "'Math Puzzles'!A:D", 'Wrong mocked mutation destination')
            ensure(payload == {'majorDimension': 'ROWS', 'values': [row]}, 'Append is not exact one intended row')
            appends.append({'params': params, 'payload': payload})
            if case == 'unknown_before_commit': raise subprocess.CalledProcessError(1, arguments, stderr='lost outcome')
            ledger.append(copy.deepcopy(row))
            if case == 'unknown_after_commit': raise subprocess.CalledProcessError(1, arguments, stderr='lost outcome')
            if case == 'extra_unrelated_tail': ledger.append(['unexpected tail', '', '', 'unrelated'])
            update_range = "'Math Puzzles'!A3:D3"
            value = {'spreadsheetId': plan['spreadsheet_id'], 'tableRange': "'Math Puzzles'!A1:D2",
                     'updates': {'spreadsheetId': plan['spreadsheet_id'], 'updatedRange': update_range,
                                 'updatedRows': 1, 'updatedColumns': 4, 'updatedCells': 4,
                                 'updatedData': {'range': update_range, 'majorDimension': 'ROWS', 'values': [row]}}}
            if case == 'bad_append_response': value['updates']['updatedRows'] = 2
            if case == 'response_wrong_spreadsheet': value['spreadsheetId'] = 'WRONG-SPREADSHEET'
            if case == 'response_wrong_range': value['updates']['updatedRange'] = "'Other Tab'!A3:D3"
            if case == 'response_wrong_cell_count': value['updates']['updatedCells'] = 8
            if case == 'response_wrong_echo_range': value['updates']['updatedData']['range'] = "'Other Tab'!A3:D3"
        else:
            raise RuntimeError('Unrecognized process request in offline test: ' + repr(arguments))
        return subprocess.CompletedProcess(arguments, 0, stdout=json.dumps(value), stderr='')

    def fake_check_output(arguments, *positional, **kwargs):
        ensure(arguments == ['git', 'branch', '--show-current'], 'Unexpected check_output request')
        service_events.append({'kind': 'branch_mock'})
        return 'main\n'

    subprocess.run = fake_run
    subprocess.check_output = fake_check_output

    class FakeHTTPResponse:
        status = 200

        def __init__(self, data, url=None): self.data, self.url = data, url
        def read(self, *args): return self.data
        def __enter__(self): return self
        def __exit__(self, *args): return False

    def fake_urlopen(request, *args, **kwargs):
        url = request.full_url
        service_events.append({'kind': 'http_get_mock', 'url': url})
        if url == 'https://zenodo.org/api/records/23350364': return FakeHTTPResponse(json.dumps(record).encode(), url)
        if url == row[2]:
            target = 'https://zenodo.org/records/23350365' if case == 'doi_wrong_destination' else 'https://zenodo.org/records/23350364'
            return FakeHTTPResponse(b'landing', target)
        for item in record['files']:
            if item.get('links', {}).get('self') == url:
                expected = next(f for f in plan['existing_publication']['files'] if f['name'] == item['key'])
                data = (root / 'raw/pr1156' / ('payload_' + expected['sha256'] + '.bin')).read_bytes()
                if case == 'provider_payload_changed': data = b'X' + data[1:]
                return FakeHTTPResponse(data, url)
        raise RuntimeError('Unrecognized mocked public GET')

    urllib.request.urlopen = fake_urlopen

    class FakeHTTPSConnection:
        def __init__(self, host, *args, **kwargs): ensure(host == 'zenodo.org', 'Unexpected authenticated host')
        def putrequest(self, method, target):
            ensure(method == 'GET', 'Authenticated mutation is forbidden')
            self.target = target
            service_events.append({'kind': 'account_get_mock', 'target': target})
        def putheader(self, *args): pass
        def endheaders(self): pass
        def close(self): pass
        def getresponse(self):
            reads['account'] += 1
            query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.target).query)
            page = int(query.get('page', ['1'])[0])
            total = 197 if case == 'account_partial' else len(account)
            hits = copy.deepcopy(account[(page-1)*25:page*25])
            if case == 'account_pagination_duplicate' and page == 2: hits[0]['id'] = account[0]['id']
            next_url = 'https://zenodo.org/api/user/records?size=25&page=' + str(page + 1) if page*25 < len(account) else None
            value = {'hits': {'total': {'value': total, 'relation': 'eq'}, 'hits': hits}, 'links': {'next': next_url}}
            if case == 'account_inexact_total': value['hits']['total']['relation'] = 'gte'
            if case == 'account_bad_page_host': value['links']['next'] = 'https://example.invalid/api/user/records?page=2'
            return FakeHTTPResponse(json.dumps(value).encode())

    http.client.HTTPSConnection = FakeHTTPSConnection
    dt.datetime = SimulatedDatetime
    module = types.ModuleType('offline_private_helper')
    module.__file__ = str(audit / 'reconcile_external_ledger_v2.py')
    module.__name__ = 'offline_private_helper'
    exec(compile(Path(module.__file__).read_bytes(), module.__file__, 'exec'), module.__dict__)
    sys.argv = [module.__file__, '--acceptance-sha256', adoption_sha]
    output = io.StringIO()
    saved_stdout = sys.stdout
    error = None
    try:
        sys.stdout = output
        module.main()
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    finally:
        sys.stdout = saved_stdout
    first_count = len(appends)
    retry_error = None
    if case in {'unknown_before_commit', 'unknown_after_commit'}:
        try:
            sys.stdout = output
            module.main()
        except Exception as exc:
            retry_error = type(exc).__name__ + ': ' + str(exc)
        finally:
            sys.stdout = saved_stdout
    after_sources = {str(p.relative_to(fixture)): sha(p) for p in sources}
    receipt = {'case': case, 'optimize': sys.flags.optimize, 'accepted': error is None,
               'error': error, 'mock_append_calls': len(appends), 'first_run_append_calls': first_count,
               'retry_error': retry_error, 'retry_accepted': case in {'unknown_before_commit', 'unknown_after_commit'} and retry_error is None,
               'external_effect_attempts': external_attempts, 'zero_real_external_mutations': not external_attempts,
               'all_expected_dependency_source_pins_match': pinned_paths_still_match,
               'unpinned_code_executed': shadow_marker.exists(), 'fsync_kinds': fsync_kinds,
               'source_copies_unchanged': before_sources == after_sources,
               'source_copy_sha256': before_sources, 'service_event_count': len(service_events),
               'read_counts': reads, 'modeled_elapsed_seconds': clock['elapsed_seconds'],
               'ledger_final_rows': len(ledger), 'intent_exists': (audit / 'LEDGER_RECONCILIATION_INTENT.json').exists()}
    if output.getvalue():
        dump(fixture / 'captured_stdout.json', {'stdout': output.getvalue()})
    dump(fixture / 'receipt.json', receipt)
    dump(fixture / 'service_events.json', service_events)
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
