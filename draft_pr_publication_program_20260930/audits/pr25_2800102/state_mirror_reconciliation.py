"""Root-owned incremental PR25 acceptance mirror; no legacy generator.

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
    canonical = REPO / 'unsolved_math_prioritization/attempts/2800102'

    def binding(path):
        return {'path': str(path.relative_to(REPO)), 'sha256': mirror.sha(path.read_bytes())}

    assert not (HERE / 'state_mirror_intent.json').exists(), 'Inspect prior intent before any retry.'
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=REPO, text=True).strip() == 'main'
    remote = json.loads(subprocess.check_output(['gh', 'pr', 'view', '25', '--json',
                        'number,url,state,isDraft,headRefOid,mergeCommit,mergedAt'], cwd=REPO, text=True))
    saved_remote = mirror.load(HERE / 'remote_merge_receipt.json')
    assert all(remote[k] == saved_remote[k] for k in remote)
    assert remote['state'] == 'MERGED' and remote['isDraft'] is False
    assert remote['mergeCommit']['oid'] == 'c06639f56a6e7416c70b00dddfb2688ad69b0522'
    assert remote['headRefOid'] == 'aa99d4a36eff79cbb7aae55ce3ffe4a0eb31af95'
    proposal = mirror.load(HERE.parent / 'pr24_10000062/state_mirror_bindings.json')
    proposal['created_at_utc'] = writer.stamp()
    proposal['scope'] = 'Exactly fifteen remotely accepted primary PRs9-17,19,21-25, plus accepted duplicate20002052 sharing owner20002011; original proposals and histories remain preserved.'
    for key in ['inventory', 'queue']:
        proposal[key] = binding(REPO / proposal[key]['path'])
    proposal['required_completed_prs'] = sorted(proposal['required_completed_prs'] + [25])
    entry = {'pr': 25, 'id': '2800102', 'status': 'already_solved',
             'acceptance': binding(canonical / 'acceptance.json'), 'audit_acceptance': binding(HERE / 'acceptance.json'),
             'remote': binding(HERE / 'remote_merge_receipt.json'), 'accepted_source': binding(canonical / 'source_record.json'),
             'canonical_acceptance_text': binding(canonical / 'ACCEPTANCE.md'), 'canonical_manifest': binding(canonical / 'MANIFEST.json'),
             'artifact': {**binding(canonical / 'SOURCE_AUDIT.md'), 'acceptance_hash_field': 'source_audit_sha256'},
             'budget': {'used': 0, 'limit': 5, 'kind': 'json_attempt', 'ledger': binding(canonical / 'attempt.json')}, 'duplicates': []}
    proposal['entries'].append(entry)
    original_attempt = mirror.load(canonical / 'ORIGINAL_attempt.json')
    assert original_attempt['substantive_attempts_used'] == 0 and original_attempt['substantive_attempt_limit'] == 5
    negative = []
    for label, record in [('invented original turn', {'substantive_attempts_used': 1, 'substantive_attempt_limit': 5}),
                          ('wrong limit', {'substantive_attempts_used': 0, 'substantive_attempt_limit': 4}),
                          ('negative original count', {'substantive_attempts_used': -1, 'substantive_attempt_limit': 5})]:
        try:
            ledger(json.dumps(record).encode(), 'json_attempt', 0, 5)
        except mirror.Rejected:
            negative.append(label)
        else:
            raise AssertionError('Undetected ledger mutation: ' + label)
    for field in ['substantive_attempts_used', 'substantive_attempt_limit']:
        record = {'substantive_attempts_used': 0, 'substantive_attempt_limit': 5}
        del record[field]
        try:
            ledger(json.dumps(record).encode(), 'json_attempt', 0, 5)
        except KeyError:
            negative.append('missing explicit ' + field)
        else:
            raise AssertionError('Undetected missing field: ' + field)
    plan = mirror.build_plan(REPO, proposal)
    preflight = mirror.validate_plan(REPO, plan)
    assert plan['primary_count'] == 15 and plan['duplicate_count'] == 1
    assert [x['id'] for x in plan['history_append']] == ['2800102']
    prior = mirror.load(REPO / 'unsolved_math_prioritization/state.json')
    assert len(prior) == 15 and '2800102' not in prior
    assert all(plan['state_after'][k] == v for k, v in prior.items())
    assert sum(x['turns_used'] for x in plan['state_after'].values()) == 17
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
                  'history_after_sha256': plan['history_after_sha256'], 'new_event': '2800102', 'new_proof_turns': 0}
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
                      'existing15_states_semantically_unchanged': True, 'current_targets': 16,
                      'original_consumed_turns': 17, 'new_proof_turns': 0,
                      'protected_bindings_unchanged': len(protected), 'legacy_generator_run': False,
                      'state_sha256': mirror.sha(state.read_bytes()), 'history_sha256': mirror.sha(history.read_bytes()),
                      'scope': 'Only present PR25 already-solved external-source acceptance appended after exact remote verification. Historical proposals/events unchanged; no invented proof/readiness transition. Cooperative lock limitation persists.'}))
        print(json.dumps({'status': 'COMPLETED', 'new_acceptance': '2800102',
                          'original_attempts': '0/5', 'new_proof_turns': 0, 'bindings': preflight['bindings_verified']}))


if __name__ == '__main__':
    main()
