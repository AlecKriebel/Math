#!/usr/bin/env python3
"""New reviewer03 actual-function URL counterexamples. Only synthetic mutations.

Run with normal Python and -O. All outputs and fixtures stay in reviewer custody.
The exact seven canonical helper bodies are loaded before provider isolation.
"""
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
import copy
import hashlib
import json
import socket
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
A = Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179')
R = A / 'reviews/package_adversary_03'
S = A.parents[1] / 'private/pr0399_package03'
sys.path.insert(0, str(S / 'ops_tests'))
from controls_support import implementation
B, P, G, I, V, L, D = implementation('canonical')
PROVIDERS = []


def check(value, message):
    if not value:
        raise RuntimeError(message)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def forbidden(*args, **kwargs):
    PROVIDERS.append(True)
    raise RuntimeError('Actual provider forbidden in offline counterexample')


def pipeline(root, alias, column=3, expected_hidden=True, exempt=False):
    root.mkdir()
    repo = root / 'repo'
    repo.mkdir()
    current = [B.HEADERS, ['', '', '', '']]
    current[1][column] = alias
    before = copy.deepcopy(current)
    desired = D.desired_row(999)
    append_calls = []
    write(root / 'raw/pr0399/ledger_live.json', {'values': [B.HEADERS]})
    write(root / 'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json', {
        'pr': 399, 'root_identity_reconciliation_complete': True,
        'unresolved_leads': [], 'release_manifest_sha256': B.RELEASE_SHA,
        'account_leads': [], 'unrelated_local_state_exemptions': [],
        'ledger_leads': ([{'values_sha256': B.digest(current[1]),
                          'disposition': 'distinct_non_target'}] if exempt else [])})
    write(root / 'ZENODO_PUBLIC_FILE_VERIFICATION.json', {'synthetic': True})

    class Client:
        base = 'https://offline.invalid'

        def request(self, method, url):
            from urllib.parse import urlsplit, parse_qs
            check(method == 'GET', 'Collector must only GET')
            q = parse_qs(urlsplit(url).query).get('q', [''])[0]
            records = ([{'id': 23174283, 'metadata': {'title': 'Fibonacci'}, 'files': []}]
                       if q == 'Fibonacci' else
                       [{'id': 999, 'metadata': {'title': B.TITLE}, 'files': []}])
            return {'hits': {'total': len(records), 'hits': records}, 'links': {}}

    def read_command(args):
        if args[0] == 'gws':
            return {'values': copy.deepcopy(current)}
        if args[-1].endswith('/pulls/399'):
            return {'number': 399, 'state': 'closed', 'merged': True, 'draft': False,
                    'head': {'sha': 'a'*40, 'ref': B.BRANCH,
                             'repo': {'full_name': 'AlecKriebel/Math'}},
                    'base': {'ref': 'main', 'repo': {'full_name': 'AlecKriebel/Math'}}}
        if args[-1].endswith('/git/ref/heads/main'):
            return {'object': {'sha': 'b'*40}}
        raise RuntimeError('Unexpected synthetic read')

    def gws(action, params, body=None):
        if action == 'get':
            return {'values': copy.deepcopy(current)}
        check(action == 'append', 'Only one synthetic mutation kind')
        check((root / 'LEDGER_APPEND_INTENT.json').is_file(), 'Durable intent must precede append')
        check(body['values'] == [desired], 'Only the intended row may append')
        current.append(copy.deepcopy(desired))
        append_calls.append(body)
        return {'updates': {'updatedRows': 1, 'updatedColumns': 4,
                            'updatedData': {'values': [desired]}}}

    result = {'alias': alias, 'column': column + 1, 'root_exemption': exempt,
              'parser_leads': sorted(B.zenodo_doi_leads(alias))}
    public = {'record': 999, 'all_public_file_bytes_match_reviewed': True,
              'doi_resolution': {'status': 200}, 'release_manifest_sha256': B.RELEASE_SHA}
    with ExitStack() as guards:
        for module, key, value in [
            (P, 'ROOT', root), (P, 'PRIVATE', root / 'private'), (P, 'REPO', repo),
            (P, 'verify_destination', lambda: None), (P, 'read_command', read_command),
            (P.zenodo, 'ZenodoClient', lambda *args: Client()),
            (P.zenodo, 'token_for', lambda *args: 'unused-offline'), (G, 'AUDIT', root),
            (D, 'AUDIT', root), (D, 'PRIVATE', root / 'private'),
            (D, 'require_release_clearance', lambda: None),
            (D, 'verify_live', lambda identifier: public), (D, 'gws', gws)]:
            guards.enter_context(patch.object(module, key, value))
        gate = P.gather('before_ledger', 'a'*40, 999)
        result['collector_matching_rows'] = len(gate['ledger_matches'])
        try:
            acceptance = G.reconcile(gate, 'before_ledger', 'a'*40, 999, True)
        except RuntimeError as exc:
            result.update(gate_accepted=False, append_calls=0, returned_verified=False,
                          reason=str(exc))
        else:
            result['gate_accepted'] = True
            with patch.object(D, 'collect', lambda *args, **kwargs: (gate, acceptance)):
                receipt = D.append_verified('a'*40, 999)
            result.update(append_calls=len(append_calls), returned_verified=receipt['status']=='verified',
                          reported_unique=receipt['unique_target_and_DOI'],
                          semantic_duplicate_rows=2, helper_recognized_target_rows=sum(
                              B.target_in_row(row, 999) for row in current),
                          full_before_sha256=B.digest(before), full_after_sha256=B.digest(current))
    if expected_hidden:
        check(result.get('collector_matching_rows') == 0 and result.get('gate_accepted') and
              result.get('append_calls') == 1 and result.get('returned_verified') and
              result.get('reported_unique'), 'New mechanism did not reproduce the false uniqueness receipt')
    else:
        check(not result.get('gate_accepted') and result['append_calls'] == 0,
              'Recognized control unexpectedly passed')
    return result


def main():
    cases = []
    aliases = ['https://zenodo.org/record/999/',
               'https://zenodo.org:443/records/999',
               'https://zenodo.org/records/./999',
               'https://zenodo.org/records/999/export/json',
               'https://ZENODO.ORG:443/record/999/?download=1#details',
               'https://zenodo.org:443/records/./999?download=1#files',
               'https://zenodo.org:443/records/999/export/json?x=1#metadata',
               'https://zenodo.org/record/999/#files',
               'https://zenodo.org/records/999/export/json#metadata']
    with ExitStack() as guards:
        guards.enter_context(patch.object(socket, 'socket', forbidden))
        guards.enter_context(patch.object(subprocess, 'run', forbidden))
        guards.enter_context(patch.object(V, 'urlopen', forbidden))
        for name in ['request', 'create', 'upload', 'update', 'publish', 'get']:
            guards.enter_context(patch.object(B.zenodo.ZenodoClient, name, forbidden))
        with tempfile.TemporaryDirectory(dir=S, prefix='review03_identity_') as directory:
            work = Path(directory)
            for number, alias in enumerate(aliases):
                for column in range(4):
                    for exempt in [False, True]:
                        cases.append(pipeline(work/str(len(cases)), alias, column, True, exempt))
            for alias in ['https://zenodo.org/records/999', 'https://zenodo.org/record/999',
                          'https://zenodo.org/records/999/files/paper.pdf',
                          'https://zenodo.org/records/999?download=1#files',
                          'https://zenodo.org/api/records/999?x=1#metadata',
                          '10.5281/ZENODO.999', 'https://doi.org/10.5281/zenodo%2E999']:
                cases.append(pipeline(work/str(len(cases)), alias, 3, False))
    check(not PROVIDERS, 'Provider access attempted')
    value = {'optimization': sys.flags.optimize, 'canonical_helper_sha256': {
                 name: hashlib.sha256((A/name).read_bytes()).hexdigest() for name in sorted(B.HELPERS)},
             'new_false_uniqueness_cases': len(aliases)*8, 'recognized_rejection_controls': 7,
             'actual_provider_attempts': 0, 'cases': cases,
             'scope': 'Actual collector/reconciliation/appender/readback function bodies; synthetic provider boundaries. Clearance and public-download result are simulated prerequisites. No live mutation.'}
    write(R/('NOVEL_IDENTITY.optimized.json' if sys.flags.optimize else 'NOVEL_IDENTITY.normal.json'), value)
    print(json.dumps({key: value[key] for key in ['optimization', 'new_false_uniqueness_cases',
                                                  'recognized_rejection_controls', 'actual_provider_attempts']}))


if __name__ == '__main__':
    main()
