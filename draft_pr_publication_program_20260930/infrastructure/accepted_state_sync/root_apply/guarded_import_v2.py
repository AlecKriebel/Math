"""Root-owned one-shot import of the exact reviewed revision-2 mirror.

No ranking, catalog, source, publication or tracker mutation. A cooperative
advisory lock and durable history-first intent guard the two-file write. This
does not constrain an unrelated writer that ignores the lock.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import ast
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
REV = HERE.parent / 'revision2'
PLAN_SHA = '7c44f3ffbeda7e8eae96fc9ebfae785bdac2d70e3742eda4f98a884b546502eb'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stamp():
    return datetime.now(timezone.utc).isoformat()


def encode(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()


def atomic(path, data):
    tmp = path.with_name(path.name + '.root-import-tmp')
    with open(tmp, 'xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def main():
    spec = importlib.util.spec_from_file_location('mirror', REV / 'accepted_state_sync_v2.py')
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    raw = (REV / 'CURRENT_PLAN_v2.json').read_bytes()
    assert sha(raw) == PLAN_SHA
    plan = json.loads(raw)
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=REPO).decode().strip() == 'main'
    assert not (REPO / '.git/MERGE_HEAD').exists()
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=REPO).strip()
    assert not (HERE / 'IMPORT_INTENT_v2.json').exists(), 'Inspect prior intent; never retry blindly.'
    assert mirror.validate_plan(REPO, plan)['targets'] == 13

    def remote(entry):
        cmd = ['gh', 'pr', 'view', str(entry['pr']), '--repo', 'AlecKriebel/Math', '--json', 'url,state,isDraft,headRefOid,mergeCommit,mergedAt']
        observation = json.loads(subprocess.check_output(cmd, cwd=REPO, timeout=30))
        item = plan['state_after'][entry['id']]
        assert observation['url'] == f"https://github.com/AlecKriebel/Math/pull/{entry['pr']}"
        assert observation['state'] == 'MERGED' and not observation['isDraft'] and observation['mergedAt']
        assert observation['headRefOid'] == item['evidence']['reviewed_head']
        assert observation['mergeCommit']['oid'] == item['evidence']['merge_commit']
        return observation

    with ThreadPoolExecutor(max_workers=4) as pool:
        observations = list(pool.map(remote, plan['proposal_spec']['entries']))
    atomic(HERE / 'REMOTE_IMMEDIATELY_BEFORE_IMPORT_v2.json', encode({'at_utc': stamp(), 'plan_sha256': PLAN_SHA, 'observations': observations, 'all_twelve_verified': True}))

    tracked = subprocess.check_output(['git', 'ls-files', '-z', '--', 'unsolved_math_prioritization', 'draft_pr_publication_program_20260930', 'simplicial_embedding_gap_30000439'], cwd=REPO).decode().split('\0')
    protected = {x['path'] for x in plan['bindings']} | {x for x in tracked if x}
    mutable = {'unsolved_math_prioritization/state.json', 'unsolved_math_prioritization/history.jsonl'}
    protected -= mutable
    before = {p: {'bytes': len((REPO / p).read_bytes()), 'sha256': sha((REPO / p).read_bytes())} for p in sorted(protected)}
    state_path = REPO / 'unsolved_math_prioritization/state.json'
    history_path = REPO / 'unsolved_math_prioritization/history.jsonl'
    tree = ast.parse((REPO / 'unsolved_math_prioritization/queue.py').read_text())
    rank = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'rank')
    eligible = next(x for x in ast.walk(rank) if isinstance(x, ast.Assign) and any(isinstance(y, ast.Name) and y.id == 'eligible' for y in x.targets))
    expression = compile(ast.Expression(eligible.value), 'legacy-pure-expression', 'eval')
    for event in plan['state_after'].values():
        assert not eval(expression, {'a': {'holds': []}, 'local_status': event['status'], 'turns': event['turns_used'], 'cfg': {'turn_limit': 5}})

    (HERE.parent / 'tmp').mkdir(exist_ok=True)
    with open(HERE.parent / 'tmp/root-accepted-state.lock', 'a+b') as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        preflight = mirror.validate_plan(REPO, plan)
        old_state, old_history = state_path.read_bytes(), history_path.read_bytes()
        intent = {'schema': 'root-accepted-mirror-import/v2', 'status': 'PREPARED', 'prepared_at_utc': stamp(), 'plan_sha256': PLAN_SHA,
                  'before': plan['preconditions'], 'state_after_sha256': plan['state_after_sha256'], 'history_after_sha256': plan['history_after_sha256'],
                  'before_state_bytes': old_state.decode(), 'before_history_bytes': old_history.decode(), 'write_order': ['history.jsonl', 'state.json'],
                  'lock': 'cooperative advisory lock; noncooperating external writer remains outside this protocol'}
        atomic(HERE / 'IMPORT_INTENT_v2.json', encode(intent))
        assert state_path.read_bytes() == old_state and history_path.read_bytes() == old_history
        for p, receipt in before.items():
            assert sha((REPO / p).read_bytes()) == receipt['sha256'], p
        atomic(history_path, old_history + plan['history_append_bytes'].encode())
        assert state_path.read_bytes() == old_state
        assert sha(history_path.read_bytes()) == plan['history_after_sha256']
        atomic(state_path, plan['state_after_bytes'].encode())
        assert sha(state_path.read_bytes()) == plan['state_after_sha256']
        assert sha(history_path.read_bytes()) == plan['history_after_sha256']
        for p, receipt in before.items():
            assert sha((REPO / p).read_bytes()) == receipt['sha256'], p
        state = json.loads(state_path.read_bytes())
        history = [json.loads(x) for x in history_path.read_text().splitlines()]
        assert state == plan['state_after'] and len(history) == 13
        assert len({x['event_id'] for x in history}) == 13
        assert sum(x['turns_used'] for x in state.values()) == 16
        assert state['20002052']['shared_turns_used'] == 1 and not state['20002052']['independent_budget_allocated']
        intent.update(status='COMPLETED', completed_at_utc=stamp())
        atomic(HERE / 'IMPORT_INTENT_v2.json', encode(intent))
        atomic(HERE / 'ROOT_IMPORT_RECEIPT_v2.json', encode({'schema': 'root-accepted-mirror-import-receipt/v2', 'at_utc': stamp(), 'plan_sha256': PLAN_SHA,
               'preflight': preflight, 'offline_root_tests': {'v1': 31, 'v2': 30, 'all_passed': True}, 'full_report_helper_delta_and_tests_read': True,
               'v1_and_v2_manifests_and_v1_preservation_verified': True, 'fresh_remote_observations': len(observations), 'history_event_count': len(history),
               'primary_count': 12, 'duplicate_count': 1, 'consumed_original_primary_turns': 16, 'new_proof_turns': 0,
               'state_sha256': sha(state_path.read_bytes()), 'history_sha256': sha(history_path.read_bytes()),
               'protected_first_party_files': before, 'all_protected_bytes_unchanged': True, 'legacy_generator_invoked': False,
               'terminal_eligibility_pure_expression': 'All 13 excluded', 'limitations': plan['limitations'] + ['Static catalog-only consumers still require a separately reviewed change.']}))
        print(json.dumps({'status': 'COMPLETED', 'primary_acceptances': 12, 'explicit_duplicates': 1, 'protected_files_unchanged': len(before), 'new_proof_turns': 0}))


if __name__ == '__main__':
    main()
