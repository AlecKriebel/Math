#!/usr/bin/env python3
"""Isolated administrative guard tests; all network interfaces are replaced.

No gh/git command or external service is called. No assert statements are used.
Fixtures contain only administrative QUEUE and synthetic tree/status metadata.
"""
from pathlib import Path
import base64
import contextlib
import datetime
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
PRIVATE = CASE / 'private_sources/status_operations_adversary'
SOURCE = CASE / 'status_operation.py'
EXPECTED_SOURCE = '73f14bb65c29aad2643aabddb76773f86b43b01f028d43911698deb3be556cec'
ORIGINAL = (CASE / 'private_sources/status_operation/QUEUE.before.md').read_bytes()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fresh():
    require(sha(SOURCE.read_bytes()) == EXPECTED_SOURCE, 'candidate changed before test')
    spec = importlib.util.spec_from_file_location('candidate', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Remote:
    def __init__(self, module, scenario, contents):
        self.m, self.scenario, self.contents = module, scenario, contents
        self.calls, self.mutations, self.updated = [], 0, False
        self.head = module.HEAD
        if scenario == 'stale_head':
            self.head = '7' * 40
        self.checkpoint, self.tip, self.repair, self.descendant = ['d' * 40, 'f' * 40, 'c' * 40, 'e' * 40]
        self.before, self.after = ORIGINAL, module.replace_status(ORIGINAL)[0]
        self.payload_summary = None
        self.readback_error_emitted = False
        if scenario in ['already_classified_head', 'missing_gate_on_excluded_head']:
            self.head = self.repair

    def api(self, endpoint, payload=None, method=None):
        require(payload is None and method is None, 'unexpected REST mutation')
        self.calls.append(endpoint)
        m = self.m
        if endpoint == 'git/ref/heads/main':
            return {'object': {'sha': self.tip}}
        if endpoint == f'git/ref/heads/{m.BRANCH}':
            return {'object': {'sha': self.head}}
        if endpoint == f'pulls/{m.PR}':
            return {'state': 'open', 'draft': self.scenario != 'stale_draft',
                    'head': {'ref': m.BRANCH, 'sha': self.head, 'repo': {'full_name': m.REPO if self.scenario != 'wrong_repository' else 'Other/Math'}},
                    'base': {'ref': 'main' if self.scenario != 'wrong_base' else 'dev'}}
        if endpoint.startswith('contents/'):
            path, ref = endpoint[len('contents/'):].split('?ref=', 1)
            if path == m.QUEUE:
                data = self.before if ref == m.HEAD or self.head == m.HEAD else self.after
                if self.scenario == 'wrong_queue' and not self.updated:
                    data += b'\n'
                if self.scenario == 'wrong_readback_queue' and self.updated:
                    data += b'\n'
            else:
                data = self.contents[path]
                if self.scenario == 'published_gate_differs' and path.endswith('PRIORITY_GATE.json'):
                    data += b'\n'
                if self.scenario == 'published_finding_differs' and path.endswith('synthetic_priority.json'):
                    data += b'\n'
            return {'encoding': 'base64', 'type': 'file', 'content': base64.b64encode(data).decode()}
        if endpoint.startswith('git/commits/'):
            oid = endpoint.rsplit('/', 1)[1]
            if oid == self.tip:
                parents = [] if self.scenario == 'unpublished_checkpoint' else [{'sha': self.checkpoint}]
                return {'sha': oid, 'tree': {'sha': 't' * 40}, 'parents': parents}
            if oid == m.HEAD:
                return {'sha': oid, 'tree': {'sha': 'a' * 40}, 'parents': []}
            if oid == self.repair:
                if self.scenario == 'descendant_after_uncertainty' and not self.readback_error_emitted:
                    self.readback_error_emitted = True
                    raise RuntimeError('synthetic administrative readback transport loss')
                parents = [{'sha': m.HEAD if self.scenario != 'wrong_commit_parent' else '0' * 40}]
                return {'sha': oid, 'tree': {'sha': 'b' * 40}, 'parents': parents}
            if oid == self.descendant:
                return {'sha': oid, 'tree': {'sha': 'z' * 40}, 'parents': [{'sha': self.repair}]}
            raise RuntimeError('unexpected synthetic commit ' + oid)
        if endpoint.startswith('git/trees/'):
            oid = endpoint.rsplit('/', 1)[1]
            if oid in ['a' * 40, 'b' * 40, 'z' * 40]:
                child = '1' * 40 if oid == 'a' * 40 else '2' * 40
                unrelated = '4' * 40 if oid != 'z' * 40 else '5' * 40
                if self.scenario == 'unrelated_tree_change' and oid == 'b' * 40:
                    unrelated = '5' * 40
                rows = [{'path': 'unsolved_math_prioritization', 'mode': '040000', 'type': 'tree', 'sha': child},
                        {'path': 'author-file.mock', 'mode': '100644', 'type': 'blob', 'sha': unrelated}]
            elif oid in ['1' * 40, '2' * 40]:
                blob = m.git_blob(self.before if oid == '1' * 40 else self.after)
                rows = [{'path': 'QUEUE.md', 'mode': '100644', 'type': 'blob', 'sha': blob},
                        {'path': 'other-row-metadata.mock', 'mode': '100644', 'type': 'blob', 'sha': '6' * 40}]
            else:
                raise RuntimeError('unexpected synthetic tree ' + oid)
            return {'sha': oid, 'truncated': self.scenario == 'truncated_tree', 'tree': rows}
        raise RuntimeError('unexpected mock endpoint ' + endpoint)

    def run(self, cmd, input=None, text=None, capture_output=None):
        require(cmd == ['gh', 'api', 'graphql', '--input', '-'], 'unexpected subprocess')
        self.mutations += 1
        require(self.mutations == 1, 'mutation resent')
        payload = json.loads(input)
        actual = payload['variables']['input']
        sentinel = self.m.CASE / 'STATUS_OPERATION_ATTEMPT.json'
        require(sentinel.exists(), 'attempt absent before mutation')
        journal = json.loads(sentinel.read_text())
        request = (self.m.CASE / 'STATUS_ATOMIC_REQUEST.json').read_bytes()
        require(sha(request) == journal['request_sha256'], 'request custody not bound')
        require(json.loads(request) == payload, 'request differs from mutation payload')
        require(actual['expectedHeadOid'] == self.m.HEAD, 'expectedHeadOid absent/wrong')
        require(actual['branch'] == {'repositoryNameWithOwner': self.m.REPO, 'branchName': 'refs/heads/' + self.m.BRANCH}, 'branch escaped')
        require(actual['fileChanges'] == {'additions': [{'path': self.m.QUEUE, 'contents': base64.b64encode(self.after).decode()}]}, 'file scope escaped')
        require(actual['clientMutationId'] == journal['attempt_id'], 'operation id differs')
        self.payload_summary = {'expected_head': actual['expectedHeadOid'], 'branch': actual['branch'],
                                'file_paths': [x['path'] for x in actual['fileChanges']['additions']],
                                'queue_sha256': sha(self.after), 'request_sha256': sha(request), 'sentinel_present_before_call': True,
                                'api_call_count_before_mutation': len(self.calls)}
        if self.scenario in ['concurrent_ancestor', 'concurrent_sibling']:
            self.head = '9' * 40 if self.scenario == 'concurrent_ancestor' else '8' * 40
        if self.scenario == 'graphql_rejected' or self.head != self.m.HEAD:
            return SimpleNamespace(returncode=0, stdout=json.dumps({'errors': [{'message': 'expectedHeadOid mismatch'}]}), stderr='')
        self.updated, self.head = True, self.repair
        if self.scenario == 'uncertain_transport':
            return SimpleNamespace(returncode=1, stdout='', stderr='synthetic transport loss after atomic update')
        if self.scenario == 'malformed_success':
            return SimpleNamespace(returncode=0, stdout='{', stderr='')
        result = {'clientMutationId': actual['clientMutationId'],
                  'commit': {'oid': self.repair, 'tree': {'oid': 'b' * 40}, 'parents': {'nodes': [{'oid': self.m.HEAD}]}},
                  'ref': {'name': self.m.BRANCH, 'target': {'oid': self.repair}}}
        if self.scenario == 'wrong_client_id':
            result['clientMutationId'] = 'unbound'
        if self.scenario == 'wrong_response_parent':
            result['commit']['parents']['nodes'] = [{'oid': '0' * 40}]
        return SimpleNamespace(returncode=0, stdout=json.dumps({'data': {'createCommitOnBranch': result}}), stderr='')


def run_fixture(scenario):
    m = fresh()
    with tempfile.TemporaryDirectory(prefix='atomic-', dir=PRIVATE) as td:
        root = Path(td)
        m.PROGRAM = root / 'program'
        m.CASE = m.PROGRAM / 'audits/pr436_2569'
        m.CASE.mkdir(parents=True)
        changed = m.replace_status(ORIGINAL)[0]
        private = m.CASE / 'private_sources/status_operation'
        private.mkdir(parents=True)
        (private / 'QUEUE.before.md').write_bytes(ORIGINAL)
        (private / 'QUEUE.after.md').write_bytes(changed)
        plan = {'code_sha256': EXPECTED_SOURCE, 'new_sha256': sha(changed)}
        if scenario == 'bad_code_hash':
            plan['code_sha256'] = 'bad'
        if scenario == 'bad_payload_hash':
            plan['new_sha256'] = 'bad'
        plan_raw = (json.dumps(plan, indent=2) + '\n').encode()
        (m.CASE / 'STATUS_OPERATION_PLAN.json').write_bytes(plan_raw)
        ops_path = m.CASE / 'reviews/status_operations_adversary/RESULT.json'
        ops_path.parent.mkdir(parents=True)
        ops = {'accepted': scenario != 'operations_refused', 'required_repairs_remaining': 0,
               'code_sha256': EXPECTED_SOURCE, 'plan_sha256': sha(plan_raw)}
        ops_raw = (json.dumps(ops, indent=2)+'\n').encode()
        ops_path.write_bytes(ops_raw)
        priority_path = m.CASE / 'synthetic_priority.json'
        priority_raw = b'{"synthetic_priority_complete":true}\n'
        priority_path.write_bytes(priority_raw)
        ops_rel, priority_rel = [str(p.relative_to(root)) for p in [ops_path, priority_path]]
        required = {ops_rel: sha(ops_raw), priority_rel: sha(priority_raw)}
        gate = {'verdict': 'ALREADY_RESOLVED_ORIGINAL_PROBLEM', 'all_independent_priority_reviews_complete': True,
                'required_repairs_remaining': 0, 'operations_adversary_accepted': True,
                'operation_binding': {'code_sha256': EXPECTED_SOURCE, 'plan_sha256': sha(plan_raw),
                'expected_head_sha': m.HEAD, 'old_queue_sha256': m.EXPECTED_QUEUE_SHA256,
                'new_queue_sha256': plan['new_sha256'], 'operations_result_sha256': sha(ops_raw)},
                'required_final_findings_sha256': required}
        if scenario == 'incomplete_gate':
            gate['all_independent_priority_reviews_complete'] = False
        if scenario == 'wrong_plan_binding':
            gate['operation_binding']['plan_sha256'] = 'bad'
        if scenario == 'wrong_code_binding':
            gate['operation_binding']['code_sha256'] = 'bad'
        if scenario == 'missing_operations_binding':
            gate['operation_binding'].pop('operations_result_sha256')
        gate_path = m.CASE / 'PRIORITY_GATE.json'
        gate_raw = (json.dumps(gate, indent=2)+'\n').encode()
        gate_path.write_bytes(gate_raw)
        if scenario == 'missing_gate_on_excluded_head':
            gate_path.unlink()
        gate_rel = str(gate_path.relative_to(root))
        contents = {gate_rel: gate_raw, ops_rel: ops_raw, priority_rel: priority_raw}
        checkpoint = {'branch': 'main', 'commit_sha': 'd' * 40,
                      'files_sha256': {gate_rel: sha(gate_raw), **required}}
        if scenario == 'missing_checkpoint_finding':
            checkpoint['files_sha256'].pop(priority_rel)
        if scenario == 'wrong_checkpoint_gate_hash':
            checkpoint['files_sha256'][gate_rel] = 'bad'
        checkpoint_path = root / 'checkpoint.json'
        checkpoint_path.write_text(json.dumps(checkpoint))
        if scenario == 'existing_attempt':
            (m.CASE / 'STATUS_OPERATION_ATTEMPT.json').write_text('{}')
        remote = Remote(m, scenario, contents)
        m.api = remote.api
        original_run = m.subprocess.run
        m.subprocess.run = remote.run
        errors = {}
        apply_calls_end = 0
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                try:
                    m.apply(checkpoint_path)
                except Exception as exc:
                    errors['apply'] = str(exc)
                apply_calls_end = len(remote.calls)
                if remote.mutations:
                    try:
                        m.apply(checkpoint_path)
                    except Exception as exc:
                        errors['second_apply'] = str(exc)
                    require(remote.mutations == 1, 'existing attempt allowed a resend')
                if scenario in ['correct', 'uncertain_transport', 'malformed_success', 'wrong_client_id', 'wrong_response_parent', 'graphql_rejected', 'descendant_after_uncertainty', 'unrelated_tree_change']:
                    if scenario == 'descendant_after_uncertainty':
                        remote.head = remote.descendant
                    try:
                        m.reconcile()
                    except Exception as exc:
                        errors['reconcile'] = str(exc)
        finally:
            m.subprocess.run = original_run
        require(remote.mutations <= 1, 'more than one mutation call')
        return {'scenario': scenario, 'mutation_call_count': remote.mutations, 'mock_branch_updated': remote.updated,
                'errors': errors, 'receipt_exists': (m.CASE / 'STATUS_REPAIR_RECEIPT.json').exists(),
                'attempt_exists': (m.CASE / 'STATUS_OPERATION_ATTEMPT.json').exists(),
                'payload_summary': remote.payload_summary, 'api_calls': remote.calls,
                'apply_call_count': apply_calls_end}


def main():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    scenarios = [
        'correct', 'bad_code_hash', 'bad_payload_hash', 'incomplete_gate', 'wrong_plan_binding',
        'wrong_code_binding', 'missing_operations_binding', 'operations_refused', 'missing_checkpoint_finding',
        'wrong_checkpoint_gate_hash', 'published_gate_differs', 'published_finding_differs',
        'unpublished_checkpoint', 'stale_head', 'stale_draft', 'wrong_repository', 'wrong_base', 'wrong_queue',
        'existing_attempt', 'concurrent_ancestor', 'concurrent_sibling', 'graphql_rejected', 'uncertain_transport',
        'malformed_success', 'wrong_client_id', 'wrong_response_parent', 'wrong_commit_parent',
        'unrelated_tree_change', 'truncated_tree', 'wrong_readback_queue', 'descendant_after_uncertainty',
        'already_classified_head', 'missing_gate_on_excluded_head'
    ]
    before_call = set(scenarios[1:19])
    before_call.update(['already_classified_head', 'missing_gate_on_excluded_head'])
    outcomes = []
    for scenario in scenarios:
        result = run_fixture(scenario)
        if scenario in before_call:
            require(result['mutation_call_count'] == 0 and not result['mock_branch_updated'], scenario + ' reached mutation')
        else:
            require(result['mutation_call_count'] == 1, scenario + ' did not make exactly one mocked attempt')
        if scenario == 'correct':
            require('apply' not in result['errors'] and 'reconcile' not in result['errors'] and result['receipt_exists'], 'valid fixture failed')
        if scenario in ['concurrent_ancestor', 'concurrent_sibling', 'graphql_rejected']:
            require(not result['mock_branch_updated'] and not result['receipt_exists'], scenario + ' stale/refused operation applied')
        if scenario in ['uncertain_transport', 'malformed_success', 'wrong_client_id', 'wrong_response_parent']:
            require(result['mock_branch_updated'] and 'apply' in result['errors'] and 'reconcile' not in result['errors'] and result['receipt_exists'], scenario + ' could not reconcile read-only')
        if scenario in ['wrong_commit_parent', 'unrelated_tree_change', 'truncated_tree', 'wrong_readback_queue']:
            require('apply' in result['errors'] and not result['receipt_exists'], scenario + ' promoted invalid readback')
        if scenario == 'descendant_after_uncertainty':
            require('apply' in result['errors'] and 'reconcile' in result['errors'] and not result['receipt_exists'], 'descendant author-file alteration accepted by reconciliation')
        if scenario in ['stale_head', 'already_classified_head', 'missing_gate_on_excluded_head']:
            require('PR or branch metadata moved' in result['errors'].get('apply', ''), 'excluded/stale guard did not run first')
            require(not any('PRIORITY_GATE' in p for p in result['api_calls']), 'gate fetched before eligibility')
        if result['mutation_call_count']:
            require('second_apply' in result['errors'] and result['attempt_exists'], 'uncertain/complete attempt could resend')
            post = result['api_calls'][result['payload_summary']['api_call_count_before_mutation']:]
            require(all(p.startswith(('git/commits/', 'git/trees/', 'git/ref/heads/', 'pulls/')) or p.startswith('contents/unsolved_math_prioritization/QUEUE.md?ref=') for p in post), 'post-attempt source/gate read')
        outcomes.append(result)
    require(sha(SOURCE.read_bytes()) == EXPECTED_SOURCE, 'candidate changed during test')
    result = {'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'python_optimization': sys.flags.optimize, 'code_sha256': EXPECTED_SOURCE,
              'scenario_count': len(outcomes), 'status': 'PASS', 'outcomes': outcomes,
              'network_calls': 0, 'real_mutation_calls': 0, 'new_proof_attempts': 0}
    output = PRIVATE / ('atomic_results_O.json' if sys.flags.optimize else 'atomic_results.json')
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'outcomes'}, indent=2))


if __name__ == '__main__':
    main()
