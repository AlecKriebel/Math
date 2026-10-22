#!/usr/bin/env python3
"""Small deterministic offline controls; NEVER call a real external operation."""
import ast
import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
P = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012')
ROOT = P.parent
SOURCE = P / 'accept_pr946.py'
N = {'__name__': '_offline_pr946_core_', '__file__': str(SOURCE), '__package__': None}
exec(compile(SOURCE.read_bytes(), str(SOURCE), 'exec', dont_inherit=True, optimize=0), N)
RESULTS = []


def check(name, call, reject=False):
    try:
        result = call()
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        if not reject:
            raise
        RESULTS.append({'control': name, 'status': 'PASS', 'rejected': type(error).__name__, 'message': str(error)[:180]})
    else:
        if reject:
            raise RuntimeError('Guard unexpectedly accepted: ' + name)
        if result is False:
            raise RuntimeError('Positive control false: ' + name)
        RESULTS.append({'control': name, 'status': 'PASS'})


def fp(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def encode(value):
    return (json.dumps(value, sort_keys=True) + '\n').encode()


def pure_controls():
    for name in N['HELPERS']:
        tree = ast.parse((P / name).read_text())
        check('syntax_and_no_assert_' + name, lambda tree=tree: not any(isinstance(n, ast.Assert) for n in ast.walk(tree)))
        first = [x for x in tree.body if not isinstance(x, ast.Expr) or not isinstance(x.value, ast.Constant)]
        check('safe_import_guard_precedes_nonbuiltin_' + name, lambda first=first:
              isinstance(first[0], ast.Import) and first[0].names[0].name == 'sys'
              and isinstance(first[1], ast.If) and 'safe_path' in ast.unparse(first[1]))
    for value in ["'Math Puzzles'!A2:D2", "'Math Puzzles'!A108:D108"]:
        check('accepted_tracker_' + value, lambda value=value: N['valid_tracker_range'](value))
    for value in ['Math Puzzles!A2:D2', "'Math Puzzles'!A1:D1", "'Math Puzzles'!A02:D02",
                  "'Math Puzzles'!A2:D3", "'Other'!A2:D2", "'Math Puzzles'!B2:E2", None, True]:
        check('rejected_tracker_' + repr(value), lambda value=value: not N['valid_tracker_range'](value))
    for raw in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}']:
        check('strict_json_' + raw, lambda raw=raw: N['strict_json'](raw), reject=True)
    for raw in ['{}\n', '{"other":{"a": 2}, "target": 0}\n', '{\n "other" : [1,2]\n}\n']:
        changed = N['replace_entry'](raw, 'target', {'x': 4})
        check('literal_state_preservation_' + str(len(raw)), lambda changed=changed: N['strict_json'](changed)['target'] == {'x': 4})
    for specs in [['01:' + 'a' * 64], ['02:' + 'a' * 64, '03:' + 'b' * 64],
                  ['01:' + 'a' * 64, '03:' + 'b' * 64], ['01:' + 'a' * 64, '02:garbage']]:
        check('review_sequence_reject_' + str(specs), lambda specs=specs: N['validate_review_sequence'](specs), reject=True)
    check('review_sequence_accept', lambda: N['validate_review_sequence'](['01:' + 'a' * 64, '02:' + 'b' * 64]))
    for value in ['2026-10-15T00:00:00', '2026-10-15T00:00:00-07:00']:
        check('explicit_UTC_required_' + value, lambda value=value: N['utc'](value), reject=True)
    check('explicit_UTC_accepted', lambda: N['utc']('2026-10-15T00:00:00Z'))
    publication = {'id': 12, 'doi': '10.5281/zenodo.12', 'record_url': 'https://zenodo.org/records/12'}
    accepted = {'freeze_sha256': 'f' * 64}
    merge = {'mergeCommit': {'oid': 'd' * 40}}
    tracker = {'updated_range': "'Math Puzzles'!A2:D2"}
    event = N['native_event']({}, accepted, publication, merge, tracker, 'note')
    check('native_honest_declared_four_zero_audit_turns', lambda:
          event['turns_used'] == 4 and event['candidate_turn'] == 4
          and event['proof_search_turns_added_by_audit'] == 0
          and event['author_native_history_authenticated'] is False
          and event['original_total_attempt_count_known'] is False
          and event['turn_count_status'] == 'original_PR_declared_four_native_event_history_unavailable'
          and 'new_mechanism_native_receipt_sha256' not in event)
    for prior in [{'turns_used': 5}, {'turns_used': True}, {'doi': '10.5281/zenodo.13'}]:
        check('native_reconciliation_' + repr(prior), lambda prior=prior: N['native_event'](prior, accepted, publication, merge, tracker, 'note'), reject=True)
    for record in [{'number': 946, 'baseRefName': 'other', 'headRefOid': N['HEAD'], 'state': 'MERGED', 'mergeCommit': {'oid': 'd' * 40}},
                   {'number': 946, 'baseRefName': 'main', 'headRefOid': 'e' * 40, 'state': 'MERGED', 'mergeCommit': {'oid': 'd' * 40}},
                   {'number': 946, 'baseRefName': 'main', 'headRefOid': N['HEAD'], 'state': 'OPEN', 'mergeCommit': {'oid': 'd' * 40}}]:
        check('actual_merged_destination_' + repr(record), lambda record=record: N['main_destination'](record, merged=True), reject=True)


def source_gate_controls():
    real_load, real_blob = N['load'], N['blob']
    source = {'id': N['KEY'], 'review_hash': N['REVIEW'], 'statement_hash': N['STATEMENT'], 'related_target_groups': {}}
    target = {'id': N['KEY'], 'review_hash': N['REVIEW'], 'statement_hash': N['STATEMENT'], 'holds': [], 'present': True}
    groups = {'groups': []}
    try:
        N['load'] = lambda path: copy.deepcopy(source)
        N['blob'] = lambda ref, path: encode([target] if path == N['CATALOG'] else groups)
        check('fresh_source_and_empty_related_membership', lambda: N['source_gate']('p' * 40))
        target['holds'] = ['unresolved']
        check('fresh_source_hold_rejected', lambda: N['source_gate']('p' * 40), reject=True)
        target['holds'] = []
        target['statement_hash'] = 'x' * 64
        check('fresh_source_identity_rejected', lambda: N['source_gate']('p' * 40), reject=True)
        target['statement_hash'] = N['STATEMENT']
        groups['groups'] = [{'name': 'newly related', 'ids': [N['KEY'], 'other']}]
        check('fresh_related_membership_rejected', lambda: N['source_gate']('p' * 40), reject=True)
    finally:
        N['load'], N['blob'] = real_load, real_blob


def next_status_controls():
    real_run = N['run']
    calls = []
    inventory = [{'number': n, 'entries': [{'id': str(10000 + n)}]} for n in [947, 948, 949]]
    state = {'eligible_prs': [946, 947, 948, 949], 'completed_prs': [946]}
    def fake_run(args, raw=False, **kwargs):
        calls.append(args)
        if args[:3] == ['gh', 'pr', 'view']:
            number = int(args[3])
            return json.dumps({'number': number, 'state': 'OPEN', 'isDraft': True,
                               'headRefOid': str(number % 10) * 40, 'baseRefName': 'main'})
        if args[:2] == ['gh', 'api'] and '/contents/' in args[2] and N['QUEUE'] in args[2]:
            number = 947 if 'ref=' + '7' * 40 in args[2] else 948
            cells = ['', f' {10000 + number} / target ', '', '', '', '', '', '',
                     ' unsolved ' if number == 947 else ' claimed_solved ', ' 4/5 ', '', '', '', '']
            return ('|'.join(cells) + '\n').encode()
        raise RuntimeError('Offline test forbids all other commands: ' + repr(args))
    try:
        N['run'] = fake_run
        skipped, selected = N['gate_next'](inventory, state)
        check('ascending_status_only_skips_unsolved_and_selects_exact_claimed', lambda:
              len(calls) == 4 and len(skipped) == 1 and skipped[0]['pr'] == 947
              and skipped[0]['action'] == 'SKIP_STATUS_ONLY' and skipped[0]['math_source_read'] is False
              and selected['number'] == 948 and selected['math_source_read'] is False
              and selected['snapshot_not_yet_created'] is True and 947 not in state['eligible_prs'])
    finally:
        N['run'] = real_run


def publication_metadata_controls():
    real_descriptor, real_load = N['descriptor_check'], N['load']
    expected = [{'name': 'research_note.pdf', 'size': 3, 'sha256': 'a' * 64},
                {'name': 'global_hessian_verification.zip', 'size': 4, 'sha256': 'b' * 64}]
    descriptor = {'metadata': {'title': 'Global Hessian realizations of statistical manifolds'}}
    accepted = {'freeze_sha256': 'f' * 64, 'operations_inventory_sha256': 'c' * 64}
    freeze = {'files': {'zenodo-deposit.json': {'sha256': 'd' * 64}}}
    merge = {'number': 946, 'state': 'MERGED', 'baseRefName': 'main', 'headRefOid': N['HEAD'], 'mergeCommit': {'oid': 'e' * 40}}
    publication = {'id': 12, 'state': 'published', 'environment': 'production', 'title': descriptor['metadata']['title'],
                   'files': expected, 'doi': '10.5281/zenodo.12', 'record_url': 'https://zenodo.org/records/12'}
    records = {
        N['D'] / 'ZENODO_STAGE.json': {**publication, 'state': 'ready_to_publish'},
        N['D'] / 'ZENODO_PUBLISH.json': publication,
        N['D'] / 'ZENODO_INSPECT.json': copy.deepcopy(publication),
        N['A'] / 'PR_MERGE_RECEIPT.json': merge,
        N['D'] / 'ZENODO_PUBLISH_INTENT.json': {
            'pr': 946, 'action': 'publish', 'accepted_freeze_sha256': accepted['freeze_sha256'],
            'operations_inventory_sha256': accepted['operations_inventory_sha256'], 'descriptor_sha256': 'd' * 64,
            'merged_base': 'main', 'merged_commit': 'e' * 40,
            'destination_readback': {'baseRefName': 'main', 'merge_commit': 'e' * 40,
                                     'merge_commit_is_ancestor_of_observed_main': True,
                                     'observed_remote_main': '1' * 40, 'actual_PR_readback': copy.deepcopy(merge)}}}
    baseline = copy.deepcopy(records)
    try:
        N['descriptor_check'] = lambda f: (descriptor, expected)
        N['load'] = lambda path: copy.deepcopy(records[path])
        check('exact_publication_metadata_file_DOI_main_links', lambda: N['publication_links'](accepted, freeze))
        changes = [
            ('wrong_staged_ID', N['D'] / 'ZENODO_STAGE.json', 'id', 13),
            ('wrong_inspected_DOI', N['D'] / 'ZENODO_INSPECT.json', 'doi', '10.5281/zenodo.13'),
            ('wrong_published_metadata_title', N['D'] / 'ZENODO_PUBLISH.json', 'title', 'unreviewed title'),
            ('wrong_published_file_fingerprint', N['D'] / 'ZENODO_PUBLISH.json', 'files', [{'name': 'other', 'size': 1, 'sha256': 'a' * 64}]),
            ('wrong_merged_destination', N['A'] / 'PR_MERGE_RECEIPT.json', 'baseRefName', 'other'),
            ('wrong_publish_freeze_link', N['D'] / 'ZENODO_PUBLISH_INTENT.json', 'accepted_freeze_sha256', '0' * 64),
            ('wrong_publish_descriptor_link', N['D'] / 'ZENODO_PUBLISH_INTENT.json', 'descriptor_sha256', '0' * 64),
        ]
        for label, path, field, value in changes:
            records = copy.deepcopy(baseline)
            records[path][field] = value
            check('publication_reject_' + label, lambda: N['publication_links'](accepted, freeze), reject=True)
    finally:
        N['descriptor_check'], N['load'] = real_descriptor, real_load


def native_CAS_controls():
    keys = ['accepted_package', 'merged_gate', 'load', 'publication_links', 'pr_view',
            'remote_main', 'source_gate', 'blob', 'explicit_tree', 'run', 'save']
    prior_functions = {k: N[k] for k in keys}
    real_subprocess_run = subprocess.run
    accepted = {'freeze_sha256': 'f' * 64}
    publication = {'id': 12, 'doi': '10.5281/zenodo.12', 'record_url': 'https://zenodo.org/records/12'}
    merge = {'number': 946, 'state': 'MERGED', 'baseRefName': 'main', 'headRefOid': N['HEAD'], 'mergeCommit': {'oid': 'e' * 40}}
    tracker = {'updated_range': "'Math Puzzles'!A2:D2"}
    parents = iter(['1' * 40, '2' * 40, '3' * 40])
    checked_sources, built, saved, commits, pushes = [], [], [], [], []
    selected_cells = ['', ' 6000001 / target ', '', '', '', '', '', '', ' claimed_solved ', ' 4/5 ', '', ' original finding ', '', '']
    queue = ('other original row remains exactly\n' + '|'.join(selected_cells) + '\n').encode()
    state = b'{"other" : { "value": [1,2] }}\n'
    history = b'{"other_history":"unchanged"}\n'
    def fake_blob(parent, path):
        return {N['QUEUE']: queue, N['STATE']: state, N['HISTORY']: history}[path]
    def fake_tree(parent, replacements):
        built.append((parent, copy.deepcopy(replacements)))
        return 'a' * 40
    def fake_run(args, **kwargs):
        if args[:3] == ['git', 'merge-base', '--is-ancestor']:
            return ''
        if args[:3] == ['git', 'diff', '--name-only']:
            return '\n'.join(sorted([N['QUEUE'], N['STATE'], N['HISTORY']])) + '\n'
        if args[:2] == ['git', 'commit-tree']:
            commit = str(len(commits) + 4) * 40
            commits.append(commit)
            return commit + '\n'
        raise RuntimeError('Offline CAS forbids command: ' + repr(args))
    def fake_push(args, **kwargs):
        if args[:3] != ['git', 'push', 'origin']:
            raise RuntimeError('Offline CAS forbids subprocess: ' + repr(args))
        pushes.append(args)
        if len(pushes) == 1:
            return SimpleNamespace(returncode=1, stdout='', stderr='rejected non-fast-forward')
        return SimpleNamespace(returncode=0, stdout='mocked accepted', stderr='')
    try:
        N['accepted_package'] = lambda context: (accepted, {})
        N['merged_gate'] = lambda a, f: {}
        N['load'] = lambda path: tracker
        N['publication_links'] = lambda *args: (publication, merge)
        N['pr_view'] = lambda: copy.deepcopy(merge)
        N['remote_main'] = lambda: next(parents)
        N['source_gate'] = lambda parent: checked_sources.append(parent) or {'parent': parent}
        N['blob'] = fake_blob
        N['explicit_tree'] = fake_tree
        N['run'] = fake_run
        N['save'] = lambda path, value, **kwargs: saved.append((str(path), copy.deepcopy(value)))
        subprocess.run = fake_push
        with contextlib.redirect_stdout(io.StringIO()):
            N['native_write'](SimpleNamespace(), {})
        check('native_CAS_rechecks_current_source_on_each_new_parent', lambda:
              checked_sources == ['1' * 40, '2' * 40] and len(pushes) == 2 and len(built) == 2)
        for parent, replacements in built:
            new_queue = replacements[N['QUEUE']].encode()
            new_state = replacements[N['STATE']].encode()
            new_history = replacements[N['HISTORY']].encode()
            check('native_CAS_only_selected_queue_state_history_' + parent[0], lambda new_queue=new_queue,new_state=new_state,new_history=new_history:
                  set(replacements) == {N['QUEUE'], N['STATE'], N['HISTORY']}
                  and N['queue_parts'](queue)[0] == N['queue_parts'](new_queue)[0]
                  and N['strict_json'](new_state)['other'] == {'value': [1, 2]}
                  and N['raw_json_members'](new_state)['other']['literal'] == N['raw_json_members'](state)['other']['literal']
                  and new_history.startswith(history)
                  and N['strict_json'](new_state)[N['KEY']]['turns_used'] == 4
                  and N['strict_json'](new_state)[N['KEY']]['proof_search_turns_added_by_audit'] == 0)
        check('native_CAS_final_receipt_confirms_actual_observed_parent', lambda:
              saved[-1][1]['parent'] == '2' * 40 and saved[-1][1]['observed_remote_main'] == '3' * 40
              and saved[-1][1]['push_confirmed'] is True)
        parents = iter(['1' * 40])
        pushes.clear()
        def uncertain_push(args, **kwargs):
            pushes.append(args)
            return SimpleNamespace(returncode=1, stdout='', stderr='connection reset; outcome unknown')
        subprocess.run = uncertain_push
        check('native_uncertain_push_stops_without_retry', lambda: N['native_write'](SimpleNamespace(), {}), reject=True)
        check('native_uncertain_push_only_one_attempt', lambda: len(pushes) == 1)
    finally:
        N.update(prior_functions)
        subprocess.run = real_subprocess_run


def review_fixture(mutation=None):
    expected = {'example' + str(i): {'bytes': 1, 'sha256': str(i % 10) * 64,
                                   'git_blob': 'b' * 40, 'git_mode': '100644', 'disk_mode': '0644'} for i in range(33)}
    freeze = {'revision_candidate': 1, 'package_manifest_sha256': 'a' * 64, 'future_helpers': {'some.py': fp(b'code')},
              'files': {'research_note.pdf': fp(b'pdf'), 'package/verify_package.py': fp(b'verifier')},
              'archive_layout': {'verifier': 'package/verify_package.py'}, 'replay_normalization_ignored': []}
    freeze_pin = 'f' * 64
    memory = {}
    specs = []
    for number in [1, 2]:
        folder = N['A'] / 'reviews' / f'full_package_{number:02d}'
        begin, auth_begin, cold_time, auth_end, end = [f'2026-10-15T{number:02d}:00:0{i}+00:00' for i in range(5)]
        originals = {name: {**record, 'archive_mode': '100644', 'disk_and_archive_match': True} for name, record in expected.items()}
        authentication = {'status': 'PASS', 'utc': auth_begin, 'original_pr_head': N['HEAD'], 'freeze_sha256': freeze_pin,
                          'package_manifest_sha256': freeze['package_manifest_sha256'], 'future_helpers': freeze['future_helpers'],
                          'candidate_files': freeze['files'], 'payloads': 1, 'archive_members': 2, 'originals': originals}
        cold = {'status': 'PASS', 'utc': cold_time, 'cold_extraction': True, 'typed_float_policy_verified': True,
                'historical_strict_failure_preserved': True, 'package_manifest_sha256': freeze['package_manifest_sha256'],
                'externally_pinned_verifier_sha256': freeze['files']['package/verify_package.py']['sha256'],
                'normalized_fields_ignored': [], 'modes': []}
        for label, optimization in zip(['normal', 'O', 'OO', 'env2'], [0, 1, 2, 2]):
            receipt = {'status': 'PASS', 'pr': 946, 'problem_id': N['KEY'],
                       'package_manifest_sha256': freeze['package_manifest_sha256'],
                       'original_files_unchanged': 33, 'worker_optimization': 0}
            memory[N['D'] / ('PACKAGE_REPLAY_' + label + '.json')] = encode(receipt)
            cold['modes'].append({'mode': label, 'observed_outer_optimization': optimization, 'returncode': 0, 'receipt': receipt})
        result = {'pr': 946, 'problem_id': N['KEY'], 'original_pr_head': N['HEAD'], 'reviewer_agent_id': f'fresh_{number}',
                  'candidate_revision': 1, 'clean_context': True, 'full_reproducer_completed': True, 'started_utc': begin, 'completed_utc': end,
                  'candidate_pins': {'freeze': freeze_pin, 'manifest': freeze['package_manifest_sha256'], 'pdf': freeze['files']['research_note.pdf']['sha256']},
                  'inspected_helper_hashes': freeze['future_helpers'], 'required_issues': [], 'optional_issues': [],
                  'clean_for_preprint': True, 'mathematical_remaining_gap_for_stated_theorem': None,
                  'strongest_verified_theorem': 'Synthetic theorem for guard tests, no mathematical certification.', 'prior_issue_resolution': {}}
        payloads = {'AUTHENTICATION_START.json': authentication, 'AUTHENTICATION_END.json': {**authentication, 'utc': auth_end},
                    'COLD_REPLAY.json': cold, 'RESULT.json': result,
                    'FULL_AUDIT.md': 'Synthetic audit text for guard tests.', 'RESEARCH_LOG.md': 'Synthetic log text.'}
        if mutation is not None:
            mutation(number, payloads)
        for name, value in payloads.items():
            memory[folder / name] = value.encode() if type(value) is str else encode(value)
        records = {name: fp(memory[folder / name]) for name in payloads}
        manifest = encode({'files': records, 'explicit_public_allowlist': sorted(records)})
        memory[folder / 'MANIFEST.json'] = manifest
        specs.append(f'{number:02d}:' + fp(manifest)['sha256'])
    return expected, freeze, freeze_pin, memory, specs


def review_controls():
    real_read, real_load, real_archive = N['read_regular'], N['load'], N['archive_check']
    real_folders = N['existing_numbered_review_folders']
    N['existing_numbered_review_folders'] = lambda: {'full_package_01', 'full_package_02'}
    def invoke(mutation=None):
        expected, freeze, freeze_pin, memory, specs = review_fixture(mutation)
        def read(path, cap=N['MAX_FILE'], pin=None):
            raw = memory[Path(path)]
            if pin is not None and fp(raw) != pin:
                raise RuntimeError('Offline fixture fingerprint changed')
            return raw
        N['read_regular'] = read
        N['load'] = lambda path: N['strict_json'](read(path))
        N['archive_check'] = lambda *args: {'payload_files': 1, 'zip_members': 2}
        return N['review_check'](specs, freeze, freeze_pin, {}, expected)
    try:
        check('complete_two_NEW_review_evidence_accepts', lambda: invoke())
        mutations = {
            'empty_full_audit': lambda n, p: p.update({'FULL_AUDIT.md': ''}) if n == 2 else None,
            'empty_cold_json': lambda n, p: p.update({'COLD_REPLAY.json': {}}) if n == 2 else None,
            'same_reviewer': lambda n, p: p['RESULT.json'].update(reviewer_agent_id='fresh_1'),
            'overlapping_rounds': lambda n, p: p['RESULT.json'].update(started_utc='2026-10-15T00:00:00+00:00') if n == 2 else None,
            'wrong_actual_env2': lambda n, p: p['COLD_REPLAY.json']['modes'][3].update(observed_outer_optimization=0) if n == 2 else None,
            'optimized_worker': lambda n, p: p['COLD_REPLAY.json']['modes'][1]['receipt'].update(worker_optimization=1) if n == 2 else None,
            'missing_original': lambda n, p: p['AUTHENTICATION_END.json']['originals'].pop('example0') if n == 2 else None,
            'wrong_original_mode': lambda n, p: p['AUTHENTICATION_END.json']['originals']['example0'].update(git_mode='100755') if n == 2 else None,
            'cold_after_final_auth': lambda n, p: p['COLD_REPLAY.json'].update(utc='2026-10-15T09:00:00+00:00') if n == 2 else None,
            'optional_issue_remains': lambda n, p: p['RESULT.json'].update(optional_issues=[{'id': 'optional1'}]) if n == 2 else None,
            'prior_required_unresolved': lambda n, p: p['RESULT.json'].update(required_issues=[{'id': 'old1'}]) if n == 1 else None,
            'historical_failure_erased': lambda n, p: p['COLD_REPLAY.json'].update(historical_strict_failure_preserved=False) if n == 2 else None,
            'typed_policy_unchecked': lambda n, p: p['COLD_REPLAY.json'].update(typed_float_policy_verified=False) if n == 2 else None,
        }
        for label, mutation in mutations.items():
            check('review_reject_' + label, lambda mutation=mutation: invoke(mutation), reject=True)
    finally:
        N['read_regular'], N['load'], N['archive_check'] = real_read, real_load, real_archive
        N['existing_numbered_review_folders'] = real_folders


def actual_bootstrap_controls():
    fixture = HERE / 'bootstrap_fixture'
    if fixture.exists():
        shutil.rmtree(fixture)
    fixture.mkdir()
    effort = fixture / 'effort'
    audit = effort / 'audits/pr946_6000001'
    audit.mkdir(parents=True)
    kit = fixture / 'zenodo_deposit_tool/zenodo.py'
    kit.parent.mkdir()
    for name in N['HELPERS']:
        shutil.copyfile(P / name, effort / name)
    # Safe fake core: if executed, reports actual flags and creates only a marker
    # within this disposable own fixture. It has no network/Git/native function.
    fake = ("import json,sys\nfrom pathlib import Path\n"
            "def operation(action,args,context):\n"
            " Path(__file__).with_name('core_executed.marker').write_text('yes')\n"
            " print(json.dumps({'worker_optimization':sys.flags.optimize,'isolated':sys.flags.isolated,'captured':len(context['captured']),'action':action}))\n")
    (effort / 'accept_pr946.py').write_text(fake)
    kit.write_text('safe fake kit, never executed')
    records = {str(path.relative_to(fixture)): fp(path.read_bytes()) for path in [*[effort / x for x in N['HELPERS']], kit]}
    inventory = {'schema': 'pr946-operations-v1', 'pr': 946, 'problem_id': N['KEY'], 'original_pr_head': N['HEAD'], 'files': records}
    def write_inventory():
        raw = encode(inventory)
        (audit / 'OPERATIONS_INVENTORY.json').write_bytes(raw)
        return fp(raw)['sha256']
    pin = write_inventory()
    for mode, args, environment in [('normal', [], None), ('O', ['-O'], None), ('OO', ['-OO'], None), ('env2', [], '2')]:
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        if environment:
            env['PYTHONOPTIMIZE'] = environment
        command = [sys.executable, *args, '-P', '-B', str(effort / 'merge_pr946.py'), '--operations-sha256', pin]
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=10)
        check('actual_bootstrap_forces_worker0_' + mode, lambda result=result:
              result.returncode == 0 and json.loads(result.stdout) == {'worker_optimization': 0, 'isolated': 1, 'captured': 7, 'action': 'merge'})
    marker = effort / 'core_executed.marker'
    marker.unlink()
    kit.write_text('tampered final dependency')
    result = subprocess.run([sys.executable, '-P', '-B', str(effort / 'merge_pr946.py'), '--operations-sha256', pin], capture_output=True, timeout=10)
    check('entire_inventory_last_dependency_drift_prevents_core_execution', lambda:
          result.returncode != 0 and not marker.exists())
    kit.unlink()
    os.mkfifo(kit)
    started = time.monotonic()
    result = subprocess.run([sys.executable, '-P', '-B', str(effort / 'merge_pr946.py'), '--operations-sha256', pin], capture_output=True, timeout=3)
    check('actual_FIFO_rejected_nonblocking_before_core_execution', lambda:
          result.returncode != 0 and not marker.exists() and time.monotonic() - started < 3)
    kit.unlink()
    target = fixture / 'regular_target'
    target.write_text('safe fake kit, never executed')
    kit.symlink_to(target)
    result = subprocess.run([sys.executable, '-P', '-B', str(effort / 'merge_pr946.py'), '--operations-sha256', pin], capture_output=True, timeout=3)
    check('actual_symlink_rejected_before_core_execution', lambda:
          result.returncode != 0 and not marker.exists())
    shadow_marker = effort / 'stdlib_shadow_executed.marker'
    (effort / 'argparse.py').write_text("from pathlib import Path\nPath(__file__).with_name('stdlib_shadow_executed.marker').write_text('bad')\n")
    result = subprocess.run([sys.executable, '-B', str(effort / 'merge_pr946.py'), '--operations-sha256', pin], capture_output=True, timeout=3)
    check('unsafe_invocation_rejected_BEFORE_shadow_stdlib_import', lambda:
          result.returncode != 0 and b'Invoke with Python -I or -P' in result.stderr
          and not shadow_marker.exists() and not marker.exists())
    shutil.rmtree(fixture)


def main():
    pure_controls()
    source_gate_controls()
    next_status_controls()
    publication_metadata_controls()
    native_CAS_controls()
    review_controls()
    actual_bootstrap_controls()
    report = {'status': 'PASS', 'scope': 'Offline small synthetic fixtures and actual isolated/bootstrap filesystem guards; no mathematical certification or external action.',
              'external_mutations_executed': 0, 'actual_Git_GitHub_Zenodo_GWS_native_calls': 0,
              'control_count': len(RESULTS), 'controls': RESULTS,
              'helper_sha256': {name: fp((P / name).read_bytes()) for name in N['HELPERS']}}
    (HERE / 'OFFLINE_CONTROLS.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'controls': len(RESULTS), 'external_actions': 0}))


if __name__ == '__main__':
    main()
