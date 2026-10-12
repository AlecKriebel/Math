#!/usr/bin/env python3
"""Selected QUEUE-field repair via one expected-head atomic commit; no shared index.

prepare is read-only remotely. apply requires a separately verified priority gate
published on main. An uncertain attempt is never resent; reconcile read-only.
After the branch update, only administrative metadata and QUEUE are inspected.
"""
import argparse
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import uuid

CASE = Path(__file__).resolve().parent
PROGRAM = CASE.parents[1]
REPO = 'AlecKriebel/Math'
PR = 436
HEAD = 'c7805ab0804f50c6f4b0d1dda99e433dbb702ae2'
BRANCH = 'research/semiperfect-sl2five-2569'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
EXPECTED_QUEUE_SHA256 = '4c7debabda92cbcf1fda654ca4082cdd663a62b450ba16ce3f5257c58f64fd28'
EXPECTED_ROW = '| 466 | 2569 / KOU-21.60 | Kourovka Notebook Problem 21.60 | 0.1275 | 6.0 | 2 | 2026 | claimed_solved | 5/5 |  |  |  |'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(name, value):
    path = CASE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as f:
        f.write(json.dumps(value, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def api(endpoint, payload=None, method=None):
    cmd = ['gh', 'api', f'repos/{REPO}/{endpoint}']
    if payload is not None:
        cmd += ['--method', method or 'POST', '--input', '-']
    p = subprocess.run(cmd, input=None if payload is None else json.dumps(payload),
                       text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return json.loads(p.stdout)


def queue_at(ref):
    obj = api(f'contents/{QUEUE}?ref={ref}')
    if obj.get('encoding') != 'base64' or obj.get('type') != 'file':
        raise RuntimeError('Unsupported QUEUE content response')
    return base64.b64decode(obj['content'], validate=False)


def published_on_main(commit):
    tip = api('git/ref/heads/main')['object']['sha']
    pending, seen = [tip], set()
    while pending and len(seen) < 256:
        oid = pending.pop()
        if oid == commit:
            return {'main_tip_readback': tip, 'checkpoint_ancestor': commit,
                    'commit_objects_inspected': len(seen)}
        if oid in seen:
            continue
        obj = api(f'git/commits/{oid}')
        if obj.get('sha') != oid:
            raise RuntimeError('Commit ancestry response does not bind requested oid')
        seen.add(oid)
        pending.extend(p['sha'] for p in obj['parents'])
    raise RuntimeError('Checkpoint is not confirmed in remote main ancestry; no mutation')


def tree_entries(sha):
    obj = api(f'git/trees/{sha}')
    if obj.get('sha') != sha or obj.get('truncated'):
        raise RuntimeError('Unbound or truncated administrative tree response')
    rows = {x['path']: {k: x[k] for k in ['mode', 'type', 'sha']} for x in obj['tree']}
    if len(rows) != len(obj['tree']):
        raise RuntimeError('Duplicate administrative tree entries')
    return rows


def verify_tree_delta(old, new, parts, old_blob, new_blob):
    before, after = tree_entries(old), tree_entries(new)
    name = parts[0]
    if set(before) != set(after) or name not in before:
        raise RuntimeError('Repair changed an unexpected tree entry')
    if any(before[k] != after[k] for k in before if k != name):
        raise RuntimeError('Repair changed an unrelated file or subtree')
    if len(parts) == 1:
        if (before[name] != {'mode': '100644', 'type': 'blob', 'sha': old_blob}
                or after[name] != {'mode': '100644', 'type': 'blob', 'sha': new_blob}):
            raise RuntimeError('Repair leaf is not the exact intended QUEUE blob')
    else:
        if any(x[name]['type'] != 'tree' or x[name]['mode'] != '040000' for x in [before, after]):
            raise RuntimeError('Repair path unexpectedly traverses a non-directory')
        verify_tree_delta(before[name]['sha'], after[name]['sha'], parts[1:], old_blob, new_blob)


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def atomic_payload(changed, operation_id):
    query = '''mutation($input: CreateCommitOnBranchInput!) {
      createCommitOnBranch(input: $input) {
        clientMutationId
        commit { oid tree { oid } parents(first: 10) { nodes { oid } } }
        ref { name target { oid } }
      }
    }'''
    payload = {'query': query, 'variables': {'input': {
        'branch': {'repositoryNameWithOwner': REPO, 'branchName': 'refs/heads/' + BRANCH},
        'expectedHeadOid': HEAD, 'clientMutationId': operation_id,
        'message': {'headline': 'Correct KOU-21.60 priority status: prior confirmed negative resolution'},
        'fileChanges': {'additions': [{'path': QUEUE, 'contents': base64.b64encode(changed).decode()}]}}}}
    return payload


def atomic_commit(payload, operation_id):
    p = subprocess.run(['gh', 'api', 'graphql', '--input', '-'], input=json.dumps(payload),
                       text=True, capture_output=True)
    # Preserve the actual response before interpreting an uncertain outcome.
    save('STATUS_ATOMIC_RESPONSE.json', {'exit_code': p.returncode,
                                       'stdout': p.stdout, 'stderr': p.stderr})
    if p.returncode:
        raise RuntimeError('Atomic commit response uncertain/failed; reconcile read-only without resending')
    response = json.loads(p.stdout)
    if response.get('errors'):
        raise RuntimeError('GraphQL errors returned; reconcile read-only without resending')
    result = response['data']['createCommitOnBranch']
    if (result['clientMutationId'] != operation_id
            or result['commit']['parents']['nodes'] != [{'oid': HEAD}]
            or result['ref']['target']['oid'] != result['commit']['oid']
            or result['ref']['name'] not in [BRANCH, 'refs/heads/' + BRANCH]):
        raise RuntimeError('Atomic response binding cannot be confirmed; administrative reconciliation only')
    return result['commit']['oid'], result['commit']['tree']['oid']


def verify_final_bindings(gate, plan, checkpoint):
    binding = gate.get('operation_binding', {})
    expected = {'code_sha256': digest(Path(__file__).read_bytes()),
                'plan_sha256': digest((CASE / 'STATUS_OPERATION_PLAN.json').read_bytes()),
                'expected_head_sha': HEAD, 'old_queue_sha256': EXPECTED_QUEUE_SHA256,
                'new_queue_sha256': plan['new_sha256']}
    if any(binding.get(k) != v for k, v in expected.items()):
        raise RuntimeError('Final gate does not bind the exact reviewed operation')
    required = gate.get('required_final_findings_sha256', {})
    operations_rel = str((CASE / 'reviews/status_operations_adversary/RESULT.json').relative_to(PROGRAM.parent))
    if not required or required.get(operations_rel) != binding.get('operations_result_sha256'):
        raise RuntimeError('Final gate lacks its exact operations result binding')
    for rel, sha in required.items():
        path = PROGRAM.parent / rel
        if not path.resolve().is_relative_to(CASE.resolve()):
            raise RuntimeError('Final finding path is outside the selected case')
        raw = path.read_bytes()
        if digest(raw) != sha or checkpoint.get('files_sha256', {}).get(rel) != sha:
            raise RuntimeError('Required final finding is not bound by checkpoint')
        obj = api(f'contents/{rel}?ref={checkpoint["commit_sha"]}')
        if base64.b64decode(obj.get('content', '')) != raw:
            raise RuntimeError('Published final finding bytes differ')
    result = json.loads((PROGRAM.parent / operations_rel).read_text())
    if (result.get('accepted') is not True or result.get('required_repairs_remaining') != 0
            or result.get('code_sha256') != expected['code_sha256']
            or result.get('plan_sha256') != expected['plan_sha256']):
        raise RuntimeError('Exact operations review has not accepted this candidate')


def selected_row(data):
    header = None
    found = []
    for i, line in enumerate(data.decode('utf-8').splitlines(keepends=True)):
        raw = line.rstrip('\r\n')
        if not raw.startswith('|'):
            continue
        cells = raw.split('|')[1:-1]
        trimmed = [x.strip() for x in cells]
        if 'Status' in trimmed and 'ID / code' in trimmed:
            header = (trimmed.index('ID / code'), trimmed.index('Status'))
            continue
        if header is None or len(cells) <= max(header):
            continue
        id_col, status_col = header
        if re.match(r'^2569(?:\s*/|\s*$)', trimmed[id_col]):
            found.append((i, line, cells, status_col))
    if len(found) != 1:
        raise RuntimeError('Selected problem must occur exactly once')
    return found[0]


def replace_status(data):
    i, line, cells, col = selected_row(data)
    if line.rstrip('\r\n') != EXPECTED_ROW or cells[col].strip() != 'claimed_solved':
        raise RuntimeError('Selected head row is no longer the frozen claimed_solved row')
    new_cells = list(cells)
    new_cells[col] = new_cells[col].replace('claimed_solved', 'already_solved', 1)
    ending = line[len(line.rstrip('\r\n')):]
    new_line = '|' + '|'.join(new_cells) + '|' + ending
    lines = data.decode('utf-8').splitlines(keepends=True)
    lines[i] = new_line
    changed = ''.join(lines).encode('utf-8')
    if changed == data or sum(a != b for a, b in zip(data.decode().splitlines(), changed.decode().splitlines())) != 1:
        raise RuntimeError('Repair must change exactly one line')
    return changed, new_line.rstrip('\r\n')


def check_current_head():
    pr = api(f'pulls/{PR}')
    ref = api(f'git/ref/heads/{BRANCH}')
    if (pr['state'] != 'open' or not pr['draft'] or pr['head']['ref'] != BRANCH
            or pr['head']['sha'] != HEAD or pr['base']['ref'] != 'main'
            or pr['head']['repo']['full_name'] != REPO or ref['object']['sha'] != HEAD):
        raise RuntimeError('PR or branch metadata moved; stop without mutation')
    original = queue_at(HEAD)
    if digest(original) != EXPECTED_QUEUE_SHA256:
        raise RuntimeError('Frozen QUEUE content changed')
    selected_row(original)
    return original


def prepare():
    if (CASE / 'STATUS_OPERATION_PLAN.json').exists():
        raise RuntimeError('Plan already exists; do not overwrite')
    original = check_current_head()
    changed, new_row = replace_status(original)
    private = CASE / 'private_sources/status_operation'
    private.mkdir(parents=True, exist_ok=True)
    (private / 'QUEUE.before.md').write_bytes(original)
    (private / 'QUEUE.after.md').write_bytes(changed)
    plan = {'prepared_at_utc': now(), 'pr': PR, 'problem_id': 2569,
            'branch': BRANCH, 'expected_head_sha': HEAD, 'path': QUEUE,
            'old_sha256': digest(original), 'new_sha256': digest(changed),
            'old_row': EXPECTED_ROW, 'new_row': new_row,
            'changed_line_count': 1, 'changed_field': 'Status',
            'original_author_turns_preserved': '5/5', 'new_proof_attempts': 0,
            'code_sha256': digest(Path(__file__).read_bytes()),
            'other_problem_rows_and_all_author_files': 'preserved',
            'remote_mutations': False,
            'apply_prerequisite': 'Final priority gate and all findings confirmed in remote main ancestry; operations adversary accepted',
            'mutation_method': 'One GraphQL createCommitOnBranch with expectedHeadOid; no REST ref update',
            'uncertain_outcome_rule': 'Persistent attempt sentinel; never resend; administrative reconciliation only'}
    save('STATUS_OPERATION_PLAN.json', plan)
    print(json.dumps(plan, indent=2))


def apply(checkpoint_path):
    attempt = CASE / 'STATUS_OPERATION_ATTEMPT.json'
    if attempt.exists():
        raise RuntimeError('An attempt already exists; reconcile read-only and never resend')
    # Eligibility precedes any research/gate read; retain the second race check below.
    check_current_head()
    plan = json.loads((CASE / 'STATUS_OPERATION_PLAN.json').read_text())
    if plan['code_sha256'] != digest(Path(__file__).read_bytes()):
        raise RuntimeError('Reviewed operation code changed')
    gate_path = CASE / 'PRIORITY_GATE.json'
    gate_bytes = gate_path.read_bytes()
    gate = json.loads(gate_bytes)
    if (gate.get('verdict') != 'ALREADY_RESOLVED_ORIGINAL_PROBLEM'
            or gate.get('all_independent_priority_reviews_complete') is not True
            or gate.get('required_repairs_remaining') != 0
            or gate.get('operations_adversary_accepted') is not True):
        raise RuntimeError('Incomplete final priority/operations gate')
    checkpoint = json.loads(checkpoint_path.read_text())
    gate_rel = str(gate_path.relative_to(PROGRAM.parent))
    if checkpoint.get('branch') != 'main' or checkpoint.get('files_sha256', {}).get(gate_rel) != digest(gate_bytes):
        raise RuntimeError('Final gate is not bound by the main checkpoint')
    published = api(f'contents/{gate_rel}?ref={checkpoint["commit_sha"]}')
    if base64.b64decode(published.get('content', '')) != gate_bytes:
        raise RuntimeError('Published final gate bytes differ')
    main_binding = published_on_main(checkpoint['commit_sha'])
    verify_final_bindings(gate, plan, checkpoint)
    original = check_current_head()
    changed, new_row = replace_status(original)
    if digest(changed) != plan['new_sha256']:
        raise RuntimeError('Plan payload differs')
    # All research/gate inputs are read above while exact claimed_solved holds.
    parent = api(f'git/commits/{HEAD}')
    if parent.get('sha') != HEAD:
        raise RuntimeError('Expected original parent is unbound')
    journal = {'attempt_id': str(uuid.uuid4()), 'started_at_utc': now(),
               'expected_head_sha': HEAD, 'branch': BRANCH,
               'old_queue_sha256': digest(original), 'new_queue_sha256': digest(changed),
               'published_findings_commit': checkpoint['commit_sha'], 'main_binding': main_binding,
               'parent_tree_sha': parent['tree']['sha'],
               'mutation_attempted': True, 'phase': 'before_single_expected_head_atomic_commit'}
    payload = atomic_payload(changed, journal['attempt_id'])
    save('STATUS_ATOMIC_REQUEST.json', payload)
    journal['request_sha256'] = digest((CASE / 'STATUS_ATOMIC_REQUEST.json').read_bytes())
    with attempt.open('x') as f:
        f.write(json.dumps(journal, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())
    fd = os.open(CASE, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    commit, tree = atomic_commit(payload, journal['attempt_id'])
    # Status is now excluded. Administrative custody/read-back only.
    journal.update(blob_sha=git_blob(changed), tree_sha=tree, repair_commit_sha=commit,
                   phase='atomic_response_received')
    save('STATUS_OPERATION_ATTEMPT.json', journal)
    obj = api(f'git/commits/{commit}')
    if obj.get('sha') != commit or [p['sha'] for p in obj['parents']] != [HEAD] or obj['tree']['sha'] != tree:
        raise RuntimeError('Administrative commit binding differs; reconcile without resending')
    verify_tree_delta(parent['tree']['sha'], tree, QUEUE.split('/'), git_blob(original), git_blob(changed))
    ref = api(f'git/ref/heads/{BRANCH}')['object']['sha']
    actual = queue_at(commit)
    _, actual_line, actual_cells, status_col = selected_row(actual)
    changed_paths = [QUEUE]  # Established by full before/after subtree-entry comparison above.
    if actual != changed or actual_cells[status_col].strip() != 'already_solved':
        raise RuntimeError('Administrative receipt cannot confirm exact selected-only repair')
    pr = api(f'pulls/{PR}')
    if ref != commit or pr['head']['sha'] != commit or pr['state'] != 'open' or not pr['draft']:
        raise RuntimeError('Administrative metadata moved or is stale; reconcile read-only without resending')
    receipt = {'verified_at_utc': now(), 'pr': PR, 'problem_id': 2569,
               'repair_commit_sha': commit, 'branch_head_readback': ref,
               'pr_head_readback': pr['head']['sha'], 'queue_status': 'already_solved',
               'queue_sha256': digest(actual), 'selected_row': actual_line.rstrip('\r\n'),
               'changed_paths': changed_paths, 'original_author_turns': '5/5',
               'all_author_files_preserved': True, 'other_queue_rows_preserved': True,
               'immediately_excluded': True, 'pr_state': pr['state'], 'pr_draft': pr['draft'],
               'pr_comment_close_ready_merge_actions': 0, 'preprint_zenodo_sheet_actions': 0,
               'published_findings_commit': checkpoint['commit_sha'],
               'method': 'One GraphQL expectedHeadOid atomic commit; exact parent and QUEUE-only tree readback; shared index untouched'}
    save('STATUS_REPAIR_RECEIPT.json', receipt)
    journal.update(phase='administrative_readback_complete', completed_at_utc=now())
    save('STATUS_OPERATION_ATTEMPT.json', journal)
    print(json.dumps(receipt, indent=2))


def reconcile():
    """Only local operation custody, remote commit/tree metadata and QUEUE; no resend."""
    journal = json.loads((CASE / 'STATUS_OPERATION_ATTEMPT.json').read_text())
    request_bytes = (CASE / 'STATUS_ATOMIC_REQUEST.json').read_bytes()
    if digest(request_bytes) != journal.get('request_sha256'):
        raise RuntimeError('Request custody differs; manual read-only reconciliation required')
    private = CASE / 'private_sources/status_operation'
    original = (private / 'QUEUE.before.md').read_bytes()
    changed = (private / 'QUEUE.after.md').read_bytes()
    rebuilt, _ = replace_status(original)
    if (digest(original) != EXPECTED_QUEUE_SHA256 or changed != rebuilt
            or digest(changed) != journal.get('new_queue_sha256')
            or json.loads(request_bytes) != atomic_payload(changed, journal['attempt_id'])
            or journal.get('expected_head_sha') != HEAD or journal.get('branch') != BRANCH):
        raise RuntimeError('Administrative operation custody does not bind the intended change')
    ref = api(f'git/ref/heads/{BRANCH}')['object']['sha']
    current = queue_at(ref)
    if ref == HEAD and current == original:
        result = {'verified_at_utc': now(), 'outcome': 'NO_APPLIED_CHANGE_CONFIRMED_AT_READBACK',
                  'branch_head': ref, 'queue_sha256': digest(current),
                  'queue_status': 'claimed_solved', 'resend_authorized': False,
                  'uncertainty_boundary': 'Readback does not prove a delayed request cannot later complete; sentinel retained'}
        save('STATUS_RECONCILIATION.json', result)
        print(json.dumps(result, indent=2))
        return
    candidate = journal.get('repair_commit_sha', ref)
    if ref != candidate:
        raise RuntimeError('Branch moved after candidate; no preservation receipt or resend; manual administrative reconciliation')
    obj = api(f'git/commits/{candidate}')
    if obj.get('sha') != candidate or [p['sha'] for p in obj['parents']] != [HEAD]:
        raise RuntimeError('Candidate is not the intended direct child; no resend; manual administrative reconciliation')
    parent = api(f'git/commits/{HEAD}')
    if parent.get('sha') != HEAD or parent['tree']['sha'] != journal.get('parent_tree_sha'):
        raise RuntimeError('Original administrative parent binding differs')
    verify_tree_delta(parent['tree']['sha'], obj['tree']['sha'], QUEUE.split('/'), git_blob(original), git_blob(changed))
    pending, seen = [ref], set()
    while pending and len(seen) < 128 and candidate not in seen:
        oid = pending.pop()
        if oid in seen:
            continue
        commit = api(f'git/commits/{oid}')
        if commit.get('sha') != oid:
            raise RuntimeError('Unbound administrative ancestry response')
        seen.add(oid)
        pending.extend(p['sha'] for p in commit['parents'])
    pr = api(f'pulls/{PR}')
    _, line, cells, col = selected_row(current)
    if (candidate not in seen or current != changed or cells[col].strip() != 'already_solved'
            or pr['head']['sha'] != ref or pr['state'] != 'open' or not pr['draft']):
        raise RuntimeError('Administrative reconciliation incomplete; never resend')
    receipt = {'verified_at_utc': now(), 'pr': PR, 'problem_id': 2569,
               'repair_commit_sha': candidate, 'branch_head_readback': ref,
               'pr_head_readback': pr['head']['sha'], 'queue_status': 'already_solved',
               'queue_sha256': digest(current), 'selected_row': line.rstrip('\r\n'),
               'changed_paths': [QUEUE], 'original_author_turns': '5/5',
               'all_author_files_preserved': True, 'other_queue_rows_preserved': True,
               'immediately_excluded': True, 'pr_state': pr['state'], 'pr_draft': pr['draft'],
               'pr_comment_close_ready_merge_actions': 0, 'preprint_zenodo_sheet_actions': 0,
               'published_findings_commit': journal['published_findings_commit'],
               'method': 'Read-only reconciliation of the single expectedHeadOid request; no resend'}
    save('STATUS_REPAIR_RECEIPT.json', receipt)
    save('STATUS_RECONCILIATION.json', receipt)
    journal.update(phase='administrative_readback_complete', repair_commit_sha=candidate,
                   tree_sha=obj['tree']['sha'], completed_at_utc=now())
    save('STATUS_OPERATION_ATTEMPT.json', journal)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['prepare', 'apply', 'reconcile'])
    p.add_argument('--checkpoint', type=Path)
    args = p.parse_args()
    if args.mode == 'prepare':
        prepare()
    elif args.mode == 'reconcile':
        reconcile()
    elif args.checkpoint is None:
        p.error('apply requires --checkpoint')
    else:
        apply(args.checkpoint)
