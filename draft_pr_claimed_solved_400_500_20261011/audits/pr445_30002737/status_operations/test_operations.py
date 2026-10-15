#!/usr/bin/env python3
"""Executable isolated gh/API controls; fixtures are private, raw executions public."""
import copy
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).absolute().parent
CASE = HERE.parent
PRIVATE = CASE / 'private_sources/status_operations'
RUN = PRIVATE / 'controls'
HELPER = HERE / 'classify_pr445.py'
HEAD = '3242c84e06db7e99012c7fe581adde5c3f89fc89'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
receipt = json.loads((CASE / 'SOURCE_RECEIPT.json').read_text())

def sha(data): return hashlib.sha256(data).hexdigest()
def blob(data): return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
def require(value, text):
    if not value: raise RuntimeError(text)

RUN.mkdir(parents=True, exist_ok=True)
BIN = RUN / 'bin'
BIN.mkdir(exist_ok=True)
stub = BIN / 'gh'
stub.write_bytes((HERE / 'stub_gh.py').read_bytes())
stub.chmod(0o755)
source_paths = {e['path']: str(CASE / 'source_snapshot' / e['path']) for e in receipt['files']}
leaves = {path: {'mode': '100644', 'type': 'blob', 'sha': blob(Path(file).read_bytes())} for path, file in source_paths.items()}
leaves[QUEUE] = {'mode': '100644', 'type': 'blob', 'sha': blob((PRIVATE / 'frozen_QUEUE.md').read_bytes())}
leaves['unrelated.txt'] = {'mode': '100644', 'type': 'blob', 'sha': 'b' * 40}
base_state = {'head': HEAD, 'ref': HEAD, 'old_tree_sha': '0' * 40, 'old_leaves': leaves,
              'sources': source_paths, 'queue_fixture': str(PRIVATE / 'frozen_QUEUE.md'),
              'original_row': receipt['selected_queue_row'], 'calls': []}
# No synthetic gate is root approval. All such gates live below ignored private_sources.
base_gate = {'schema': 'pr445_queue_classification_gate_v1', 'repo': 'AlecKriebel/Math', 'pr': 445,
             'problem_id': '30002737', 'source_head': HEAD, 'branch': 'research/diffraction-dynamical-30002737',
             'from_status': 'claimed_solved', 'to_status': 'already_solved', 'approved': True,
             'genuine_accepted_certificate': True, 'source_receipt_sha256': sha((CASE / 'SOURCE_RECEIPT.json').read_bytes()),
             'review_bindings': []}
for role in ['root_disposition', 'priority', 'numeric_certificate_adversary']:
    p = RUN / (role + '.txt')
    p.write_text('Synthetic control binding: ' + role + '\n')
    base_gate['review_bindings'].append({'role': role, 'path': str(p.relative_to(CASE)), 'sha256': sha(p.read_bytes())})

# Each case changes a materially relevant acceptance boundary or transaction failure.
CASES = [
    ('prepare_positive', 'prepare', 'normal', 0, 0),
    ('apply_positive', 'apply', 'normal', 0, 4),
    ('extra_binding_positive', 'apply', 'normal', 0, 4),
    ('missing_gate', 'apply', 'normal', 2, 0),
    ('missing_digest', 'apply', 'normal', 2, 0),
    ('wrong_digest', 'apply', 'normal', 2, 0),
    ('gate_pr_boolean', 'apply', 'normal', 2, 0),
    ('approved_integer', 'apply', 'normal', 2, 0),
    ('accepted_integer', 'apply', 'normal', 2, 0),
    ('unapproved_gate', 'apply', 'normal', 2, 0),
    ('gate_head_mismatch', 'apply', 'normal', 2, 0),
    ('gate_receipt_mismatch', 'apply', 'normal', 2, 0),
    ('gate_duplicate_keys', 'apply', 'normal', 2, 0),
    ('duplicate_binding_role', 'apply', 'normal', 2, 0),
    ('review_hash_mismatch', 'apply', 'normal', 2, 0),
    ('review_path_escape', 'apply', 'normal', 2, 0),
    ('review_symlink', 'apply', 'normal', 2, 0),
    ('gate_symlink', 'apply', 'normal', 2, 0),
    ('other_pr_option', 'prepare', 'normal', 2, 0),
    ('changed_head', 'apply', 'changed_head', 2, 0),
    ('changed_status', 'apply', 'changed_status', 2, 0),
    ('changed_branch', 'apply', 'changed_branch', 2, 0),
    ('nonblank_doi', 'apply', 'nonblank_doi', 2, 0),
    ('changed_source', 'apply', 'changed_source', 2, 0),
    ('wrong_source_size', 'apply', 'wrong_source_size', 2, 0),
    ('closed_pr', 'apply', 'closed_pr', 2, 0),
    ('nondraft_pr', 'apply', 'nondraft_pr', 2, 0),
    ('wrong_base', 'apply', 'wrong_base', 2, 0),
    ('wrong_repo', 'apply', 'wrong_repo', 2, 0),
    ('bool_pr_remote', 'apply', 'bool_pr_remote', 2, 0),
    ('duplicate_api_keys', 'apply', 'duplicate_api_keys', 2, 0),
    ('truncated_tree', 'apply', 'truncated_tree', 2, 0),
    ('changed_head_before_patch', 'apply', 'changed_head_before_patch', 2, 3),
    ('tree_changes_other_path', 'apply', 'tree_changes_other_path', 2, 2),
    ('diff_changes_other_path', 'apply', 'diff_changes_other_path', 2, 3),
    ('malformed_blob_response', 'apply', 'malformed_blob_response', 2, 1),
    ('lost_blob_response', 'apply', 'lost_blob_response', 2, 1),
    ('malformed_tree_response', 'apply', 'malformed_tree_response', 2, 2),
    ('malformed_commit_response', 'apply', 'malformed_commit_response', 2, 3),
    ('malformed_patch_applied', 'apply', 'malformed_patch_applied', 3, 4),
    ('lost_patch_applied', 'apply', 'lost_patch_applied', 3, 4),
    ('wrong_patch_response_applied', 'apply', 'wrong_patch_response_applied', 3, 4),
    ('lost_patch_not_applied', 'apply', 'lost_patch_not_applied', 2, 4),
    ('post_queue_wrong', 'apply', 'post_queue_wrong', 2, 4),
    ('post_diff_wrong', 'apply', 'post_diff_wrong', 2, 4),
]
records = []
for optimized in [False, True]:
    for name, mode, scenario, expected_rc, expected_mutations in CASES:
        label = ('optimized_' if optimized else 'normal_') + name
        folder = RUN / label
        folder.mkdir(exist_ok=True)
        gate = copy.deepcopy(base_gate)
        if name == 'extra_binding_positive':
            item = copy.deepcopy(gate['review_bindings'][0]); item['role'] = 'producer_certificate'; gate['review_bindings'].append(item)
        if name == 'gate_pr_boolean': gate['pr'] = True
        if name == 'approved_integer': gate['approved'] = 1
        if name == 'accepted_integer': gate['genuine_accepted_certificate'] = 1
        if name == 'unapproved_gate': gate['approved'] = False
        if name == 'gate_head_mismatch': gate['source_head'] = '9' * 40
        if name == 'gate_receipt_mismatch': gate['source_receipt_sha256'] = '9' * 64
        if name == 'duplicate_binding_role': gate['review_bindings'].append(copy.deepcopy(gate['review_bindings'][0]))
        if name == 'review_hash_mismatch': gate['review_bindings'][0]['sha256'] = '9' * 64
        if name == 'review_path_escape': gate['review_bindings'][0]['path'] = '../../AGENTS.md'
        if name == 'review_symlink':
            p = folder / 'review_link'; p.unlink(missing_ok=True); p.symlink_to(RUN / 'root_disposition.txt')
            gate['review_bindings'][0]['path'] = str(p.relative_to(CASE))
        gatepath = folder / 'gate.json'
        rawgate = json.dumps(gate, sort_keys=True).encode()
        if name == 'gate_duplicate_keys': rawgate = rawgate[:-1] + b',"approved":true}'
        gatepath.write_bytes(rawgate)
        if name == 'gate_symlink':
            link = folder / 'gate_link.json'; link.unlink(missing_ok=True); link.symlink_to(gatepath); gatepath = link
        state = copy.deepcopy(base_state); state['scenario'] = scenario
        statepath = folder / 'state.json'; statepath.write_text(json.dumps(state))
        argv = [sys.executable] + (['-O'] if optimized else []) + [str(HELPER), mode]
        if mode == 'apply' and name != 'missing_gate': argv += ['--gate', str(gatepath)]
        if mode == 'apply' and name != 'missing_digest':
            argv += ['--expected-gate-sha256', '9' * 64 if name == 'wrong_digest' else sha(rawgate)]
        if name == 'other_pr_option': argv += ['--pr', '446']
        env = dict(os.environ, PATH=str(BIN) + os.pathsep + os.environ['PATH'], PR445_STUB_STATE=str(statepath), PYTHONDONTWRITEBYTECODE='1')
        result = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=40)
        state = json.loads(statepath.read_text())
        calls = state['calls']; mutations = [c for c in calls if c['method'] != 'GET']; patches = [c for c in calls if c['method'] == 'PATCH']
        checks = {'expected_exit': result.returncode == expected_rc,
                  'expected_mutation_count': len(mutations) == expected_mutations,
                  'at_most_one_patch': len(patches) <= 1,
                  'no_source_body_after_patch': True, 'no_post_patch_math_metadata': True,
                  'fixed_repository_pr': all(c['endpoint'] != 'pulls/446' for c in calls)}
        parsed = None
        try: parsed = json.loads(result.stdout)
        except ValueError: pass
        if patches:
            position = calls.index(patches[0]); post = calls[position+1:]
            checks['one_ref_queue_reconciliation'] = sum(c['endpoint'].startswith('git/ref/') for c in post) == 1 and sum(c['endpoint'].startswith('contents/') for c in post) == 1
            checks['no_source_body_after_patch'] = all(not c['endpoint'].startswith('contents/') or c['endpoint'].startswith('contents/' + QUEUE + '?') for c in post)
            checks['no_post_patch_math_metadata'] = all(c['method'] == 'GET' and c['endpoint'].startswith(('git/ref/', 'contents/' + QUEUE + '?', 'git/commits/', 'compare/')) for c in post)
            checks['nonforce_patch'] = patches[0]['body'].get('force') is False
        if name in ('apply_positive', 'extra_binding_positive'):
            before = (PRIVATE / 'frozen_QUEUE.md').read_bytes(); after = __import__('base64').b64decode(state['new_queue'])
            expected = before.replace(receipt['selected_queue_row'].encode(), receipt['selected_queue_row'].replace('claimed_solved', 'already_solved').encode(), 1)
            checks['exact_status_only_queue_bytes'] = after == expected
            checks['all_12_verified'] = len(parsed.get('originals_verified_before_change', [])) == 12
            checks['success_outcome'] = parsed.get('outcome') == 'applied_verified'
            checks['original_tree_leaf_sha_preserved'] = all(state['new_leaves'][p] == e for p,e in state['old_leaves'].items() if p != QUEUE)
        if name == 'prepare_positive': checks['prepare_success_outcome'] = parsed.get('outcome') == 'prepared_read_only'
        if name in ('malformed_patch_applied', 'lost_patch_applied', 'wrong_patch_response_applied'):
            checks['uncertainty_retained'] = parsed.get('outcome') == 'applied_reconciled_uncertain_patch' and bool(parsed.get('patch_response_error'))
        if name not in ('prepare_positive', 'apply_positive', 'extra_binding_positive', 'malformed_patch_applied', 'lost_patch_applied', 'wrong_patch_response_applied', 'other_pr_option'):
            checks['failed_check_retained'] = bool(parsed and parsed.get('error'))
        raw = {'label': label, 'argv': argv, 'returncode': result.returncode, 'stdout': result.stdout,
               'stderr': result.stderr, 'checks': checks,
               'actual_api_calls': [{k:v for k,v in c.items() if k != 'body'} for c in calls],
               'actual_mutation_count': len(mutations), 'actual_patch_count': len(patches)}
        records.append(raw)
(HERE / 'RAW_EXECUTIONS.json').write_text(json.dumps(records, indent=2, sort_keys=True) + '\n')
failures = [r['label'] + ':' + k for r in records for k,v in r['checks'].items() if not v]
summary = {'schema': 'pr445_offline_controls_v1', 'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'actual_child_executions': len(records), 'normal_child_executions': sum(not r['label'].startswith('optimized_') for r in records),
           'optimized_child_executions': sum(r['label'].startswith('optimized_') for r in records),
           'positive_child_executions': sum(r['label'].endswith(('prepare_positive','apply_positive','extra_binding_positive')) and all(r['checks'].values()) for r in records),
           'failed_checks': failures, 'all_checks_passed': not failures,
           'raw_executions_sha256': sha((HERE / 'RAW_EXECUTIONS.json').read_bytes()),
           'real_remote_mutations': 0, 'synthetic_gates_are_root_approval': False}
(HERE / 'CONTROL_RESULTS.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
print(json.dumps(summary, indent=2, sort_keys=True))
sys.exit(1 if failures else 0)
