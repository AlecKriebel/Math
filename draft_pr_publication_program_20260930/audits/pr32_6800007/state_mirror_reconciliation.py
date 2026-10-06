"""Root-owned incremental PR32 acceptance mirror; no legacy generator.

Uses the preserved v2 validator and PR23's exact zero-source ledger schema.
Original proposals, helpers, historical state events and budgets stay intact.
"""
from datetime import datetime, timezone
import fcntl
import importlib.util
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = REPO / 'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync'


def main():
    spec = importlib.util.spec_from_file_location('mirror', BASE / 'revision2/accepted_state_sync_v2.py')
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    spec = importlib.util.spec_from_file_location('writer', BASE / 'root_apply/guarded_import_v2.py')
    writer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(writer)
    original_ledger = mirror.ledger_budget

    def ledger(data, kind, used, limit):
        if kind != 'json_zero_source_triage':
            return original_ledger(data, kind, used, limit)
        obj = json.loads(data)
        mirror.require(str(obj.get('problem_id')) == '30002145', 'Wrong zero-triage ledger ID')
        mirror.require(used == obj.get('used') == 0 and limit == obj.get('limit') == 5, 'Zero-triage budget mismatch')
        mirror.require(obj.get('substantive_proof_attempts') == [] and isinstance(obj.get('reason'), str) and obj['reason'], 'Ambiguous zero-triage ledger')

    mirror.ledger_budget = ledger
    canonical = REPO / 'unsolved_math_prioritization/attempts/6800007'

    def binding(path):
        return {'path': str(path.relative_to(REPO)), 'sha256': mirror.sha(path.read_bytes())}

    assert not (HERE / 'state_mirror_intent.json').exists(), 'Inspect prior intent before any retry.'
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=REPO, text=True).strip() == 'main'
    remote = json.loads(subprocess.check_output(['gh', 'pr', 'view', '32', '--json',
                        'number,url,state,isDraft,headRefOid,mergeCommit,mergedAt'], cwd=REPO, text=True))
    saved_remote = mirror.load(HERE / 'remote_merge_receipt.json')
    assert all(remote[k] == saved_remote[k] for k in remote)
    assert remote['state'] == 'MERGED' and remote['isDraft'] is False
    assert remote['mergeCommit']['oid'] == 'b35315cbfcdfcfd63e2c6cceea1cf212944938be'
    assert remote['headRefOid'] == 'a92af24e2e6015893787e0c55cd4618f7098917e'
    proposal = mirror.load(HERE.parent / 'pr33_10000046/state_mirror_bindings.json')
    proposal['created_at_utc'] = writer.stamp()
    proposal['scope'] = 'Twenty-three remotely accepted primary PRs9-17,19,21-33, plus accepted duplicate20002052 under shared owner20002011; historical proposals and records unchanged.'
    for key in ['inventory', 'queue']:
        proposal[key] = binding(REPO / proposal[key]['path'])
    proposal['required_completed_prs'] = sorted(proposal['required_completed_prs'] + [32])
    entry = {'pr': 32, 'id': '6800007', 'status': 'already_solved',
             'acceptance': binding(canonical / 'acceptance.json'), 'audit_acceptance': binding(HERE / 'acceptance.json'),
             'remote': binding(HERE / 'remote_merge_receipt.json'), 'accepted_source': binding(canonical / 'source_record.json'),
             'canonical_acceptance_text': binding(canonical / 'ACCEPTANCE.md'), 'canonical_manifest': binding(canonical / 'MANIFEST.json'),
             'artifact': {**binding(canonical / 'CANDIDATE.md'), 'acceptance_hash_field': 'canonical_candidate_sha256'},
             'budget': {'used': 1, 'limit': 5, 'kind': 'jsonl_turns', 'ledger': binding(canonical / 'turns.jsonl')}, 'duplicates': []}
    proposal['entries'].append(entry)
    negative = []
    valid_ledger = [json.loads(line) for line in (canonical / 'turns.jsonl').read_text().splitlines()]
    fixtures = [('missing original turn', valid_ledger[:0]),
                ('duplicate original turn', [valid_ledger[0], valid_ledger[0]]),
                ('reset original budget', []),
                ('invented additional turn', valid_ledger + [dict(valid_ledger[0], turn=2)])]
    for label, mutant in fixtures:
        encoded = ('\n'.join(json.dumps(x) for x in mutant) + '\n').encode()
        try:
            ledger(encoded, 'jsonl_turns', 1, 5)
        except mirror.Rejected:
            negative.append(label)
        else:
            raise AssertionError('Undetected ledger mutation: ' + label)
    plan = mirror.build_plan(REPO, proposal)
    preflight = mirror.validate_plan(REPO, plan)
    assert plan['primary_count'] == 23 and plan['duplicate_count'] == 1
    assert [x['id'] for x in plan['history_append']] == ['6800007']
    prior = mirror.load(REPO / 'unsolved_math_prioritization/state.json')
    assert len(prior) == 23 and '6800007' not in prior
    assert all(plan['state_after'][k] == v for k, v in prior.items())
    assert sum(x['turns_used'] for x in plan['state_after'].values()) == 28
    writer.atomic(HERE / 'state_mirror_bindings.json', mirror.encode(proposal))
    writer.atomic(HERE / 'state_mirror_plan.json', mirror.encode(plan))
    protected = {b['path']: b['sha256'] for b in plan['bindings']}
    state = REPO / 'unsolved_math_prioritization/state.json'
    history = REPO / 'unsolved_math_prioritization/history.jsonl'
    with open(BASE / 'tmp/root-accepted-state.lock', 'a+b') as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        mirror.validate_plan(REPO, plan)
        intent = {'status': 'PREPARED', 'at_utc': writer.stamp(), 'plan_sha256': mirror.sha(mirror.encode(plan)),
                  'before': plan['preconditions'], 'state_after_sha256': plan['state_after_sha256'],
                  'history_after_sha256': plan['history_after_sha256'], 'new_event': '6800007', 'new_proof_turns': 0}
        writer.atomic(HERE / 'state_mirror_intent.json', mirror.encode(intent))
        old_state, old_history = state.read_bytes(), history.read_bytes()
        assert mirror.sha(old_state) == plan['preconditions']['state_sha256']
        assert mirror.sha(old_history) == plan['preconditions']['history_sha256']
        writer.atomic(history, old_history + plan['history_append_bytes'].encode())
        assert state.read_bytes() == old_state
        writer.atomic(state, plan['state_after_bytes'].encode())
        assert mirror.sha(state.read_bytes()) == plan['state_after_sha256']
        assert mirror.sha(history.read_bytes()) == plan['history_after_sha256']
        assert all(mirror.sha((REPO / p).read_bytes()) == h for p, h in protected.items())
        intent.update(status='COMPLETED', completed_at_utc=writer.stamp())
        writer.atomic(HERE / 'state_mirror_intent.json', mirror.encode(intent))
        writer.atomic(HERE / 'state_mirror_receipt.json', mirror.encode({'at_utc': writer.stamp(), 'preflight': preflight,
                      'negative_ledger_controls': negative, 'history_events_added': 1,
                      'existing23_states_semantically_unchanged': True, 'current_targets': 24,
                      'original_consumed_turns': 28, 'new_proof_turns': 0,
                      'protected_bindings_unchanged': len(protected), 'legacy_generator_run': False,
                      'state_sha256': mirror.sha(state.read_bytes()), 'history_sha256': mirror.sha(history.read_bytes()),
                      'scope': 'Only present PR32 credited already_solved acceptance appended after exact remote verification. Historical proposals/events unchanged; no invented proof/readiness transition. Cooperative lock limitation persists.'}))
        print(json.dumps({'status': 'COMPLETED', 'new_acceptance': '6800007',
                          'original_attempts': '1/5', 'new_proof_turns': 0, 'bindings': preflight['bindings_verified']}))


if __name__ == '__main__':
    main()
