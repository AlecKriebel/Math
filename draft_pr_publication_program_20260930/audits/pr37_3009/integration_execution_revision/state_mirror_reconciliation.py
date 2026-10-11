#!/usr/bin/env python3
"""Future root-only PR37 present acceptance append; no historical reconstruction.

Prepared only. A durable history-first intent and the existing cooperative lock
guard two shared writes. A failed or interrupted intent is retained for manual
inspection, never automatically retried. Native PR37 authored turns.json is byte unchanged; historic runtime metadata is archival.
"""
import argparse, copy, fcntl, json
from pathlib import Path
import pr37_guards as g

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    g.add_gate_args(parser)
    args = parser.parse_args()
    frozen, pins = g.gates(args)
    merge_head = Path(g.git('rev-parse', '--git-path', 'MERGE_HEAD'))
    if not merge_head.is_absolute():
        merge_head = g.R / merge_head
    g.require(not merge_head.exists(), 'Complete exact original-head merge before mirroring')
    g.require('acceptance.json' in {p.name for p in g.K.iterdir()} and 'ACCEPTANCE.json' not in {p.name for p in g.K.iterdir()}, 'Literal lowercase canonical receipt required')
    g.require(not (g.A / 'state_mirror_intent.json').exists(), 'Inspect prior intent before any retry')
    g.require(g.sha(g.PREVIOUS.read_bytes()) == g.PREVIOUS_SHA, 'Frozen PR36 base proposal changed')
    pre = g.load(g.A / 'integration_preflight.json')
    g.foreign_tracked_unchanged(pre)
    acceptance = g.load(g.K / 'acceptance.json')
    audit = g.load(g.A / 'acceptance.json')
    g.acceptance_invariants(acceptance, pins, pre)
    g.acceptance_invariants(audit, pins, pre)
    g.require(g.strict_equal({k: v for k, v in audit.items() if k not in {'canonical_manifest_sha256', 'canonical_manifest_entries'}}, acceptance), 'Audit/canonical acceptance value/type mismatch')
    g.require(g.sha((g.K / 'MANIFEST.json').read_bytes()) == audit['canonical_manifest_sha256'], 'Canonical accepted manifest changed')
    g.manifest(g.K, g.K / 'MANIFEST.json', audit['canonical_manifest_sha256'], audit['canonical_manifest_entries'])
    for z in frozen:
        path = g.K / ('reviewed_pending_administration' if z['path'] in g.ADMIN else '') / z['path']
        g.require(path.read_bytes() == (g.C / z['path']).read_bytes(), 'Frozen canonical science or archived pending administration changed before mirror: ' + z['path'])
    remote = g.remote()
    g.require(remote == g.load(g.A / 'remote_merge_receipt.json'), 'Fresh exact remote acceptance differs')
    g.require(remote['state'] == 'MERGED' and remote['isDraft'] is False and remote['mergedAt'] == acceptance['merged_at'] and remote['mergeCommit']['oid'] == acceptance['merge_commit'], 'Current actual remote is not accepted')
    g.require(g.git('show', '-s', '--format=%P', acceptance['merge_commit']).split() == [pre['main_before'], g.HEAD], 'Actual merge parents changed')
    g.git_bytes('merge-base', '--is-ancestor', acceptance['merge_commit'], 'HEAD')
    overlay = g.load(g.A / 'integration_check.json')
    g.require(all(overlay[k] == v for k, v in pins.items()), 'Actual overlay/final gate pins differ')
    tree = g.tree_binding(acceptance['merge_commit'], pre, overlay, g.Q.read_bytes())
    g.require(tree == acceptance['merge_tree'] == g.load(g.A / 'integration_prepush.json')['merge_tree'], 'Actual merged tree/prepush/acceptance differ')
    g.canonical_unchanged(frozen, True)
    g.unselected_inventory(g.load(g.A / 'integration_inventory_before.json'), g.load(g.B / 'inventory.json'))
    state_path = g.R / 'unsolved_math_prioritization/state.json'
    history_path = g.R / 'unsolved_math_prioritization/history.jsonl'
    old_state, old_history = state_path.read_bytes(), history_path.read_bytes()
    prior = json.loads(old_state)
    g.require(g.sha(old_state) == pre['state_before_sha256'] and g.sha(old_history) == pre['history_before_sha256'], 'Original post-PR36 state/history changed before mirror')
    g.require(len(prior) == 27 and g.ID not in prior and sum(x['turns_used'] for x in prior.values()) == 32, 'Require27 previous targets/32 consumed turns')
    mirror = g.load_mirror()
    proposal = copy.deepcopy(g.load(g.PREVIOUS))
    old_entries = copy.deepcopy(proposal['entries'])
    old_duplicates = copy.deepcopy(proposal.get('duplicate_mirrors'))
    proposal.update(created_at_utc=g.stamp(), scope='Incremental accepted primary PR37 and all prior bound acceptances; original ledgers and complete history prefix preserved, no reconstructed historical proof/readiness transitions.')
    for key in ['inventory', 'queue']:
        proposal[key] = g.binding(g.R / proposal[key]['path'])
    g.require(len(proposal['entries']) == 26 and g.PR not in proposal['required_completed_prs'], 'Prior completed-primary scope differs')
    proposal['required_completed_prs'] = sorted(proposal['required_completed_prs'] + [g.PR])
    proposal['entries'].append({'pr': g.PR, 'id': g.ID, 'status': 'unsolved', 'acceptance': g.binding(g.K / 'acceptance.json'), 'audit_acceptance': g.binding(g.A / 'acceptance.json'), 'remote': g.binding(g.A / 'remote_merge_receipt.json'), 'accepted_source': g.binding(g.K / 'source_record.json'), 'canonical_acceptance_text': g.binding(g.K / 'ACCEPTANCE.md'), 'canonical_manifest': g.binding(g.K / 'MANIFEST.json'), 'artifact': {**g.binding(g.K / 'PARTIAL.md'), 'acceptance_hash_field': 'canonical_scientific_artifact_sha256'}, 'budget': {'used': 1, 'limit': 5, 'kind': 'pr37_exact_json_substantive_responses', 'ledger': g.binding(g.K / 'turns.json')}, 'duplicates': []})
    g.require(proposal['entries'][:-1] == old_entries and proposal.get('duplicate_mirrors') == old_duplicates, 'Prior proposal entries or duplicate accounting changed')
    # Exact ledger bytes are already independently bound by g.gates. These controls
    # challenge native ambiguity accounting without rewriting the original record.
    original = g.load(g.K / 'turns.json')
    negatives = []
    mutations = []
    for name in ['missing original response', 'duplicate original response', 'invented second response', 'renumbered response']:
        mutant = copy.deepcopy(original)
        if name == 'missing original response':
            mutant['responses'] = []
        elif name == 'duplicate original response':
            mutant['responses'] *= 2
        elif name == 'invented second response':
            mutant['responses'].append(dict(mutant['responses'][0], turn=2))
            mutant['substantive_turns_used'] = 2
        else:
            mutant['responses'][0]['turn'] = 2
        mutations.append((name, mutant))
    for name, mutant in mutations:
        try:
            mirror.ledger_budget(g.encode(mutant), 'pr37_exact_json_substantive_responses', 1, 5)
        except mirror.Rejected:
            negatives.append(name)
        else:
            raise ValueError('Exact original ledger guard accepted mutant: ' + name)
    plan = mirror.build_plan(g.R, proposal)
    validation = mirror.validate_plan(g.R, plan)
    g.require(plan['primary_count'] == 27 and plan['duplicate_count'] == 1 and len(plan['state_after']) == 28, 'Expected27 accepted primaries plus1 duplicate')
    g.require(len(plan['history_append']) == 1 and plan['history_append'][0]['id'] == g.ID and plan['history_append'][0]['event'] == 'acceptance_mirror_import', 'Append exactly one PRESENT acceptance event')
    g.require(all(plan['state_after'][k] == v for k, v in prior.items()) and sum(x['turns_used'] for x in plan['state_after'].values()) == 33, 'Prior states or original-turn accounting changed')
    event = plan['history_append'][0]
    g.require(event['evidence']['historical_transitions_asserted'] is False and event['evidence']['import_is_present_day_mirror'] is True and event['turns_used'] == 1, 'No historical proof event/new research turn may be invented')
    g.dump(g.A / 'state_mirror_bindings.json', proposal, exclusive=True)
    g.dump(g.A / 'state_mirror_plan.json', plan, exclusive=True)
    protected = {z['path']: z['sha256'] for z in plan['bindings']}
    lock_path = g.BASE / 'tmp/root-accepted-state.lock'
    g.require(lock_path.parent.is_dir(), 'Existing cooperative lock directory required')
    with lock_path.open('a+b') as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        mirror.validate_plan(g.R, plan)
        g.foreign_tracked_unchanged(pre)
        g.require(state_path.read_bytes() == old_state and history_path.read_bytes() == old_history, 'Shared preimage changed before locked write')
        intent = {'schema': 'pr37-present-acceptance-mirror/v1', 'status': 'PREPARED', 'prepared_at_utc': g.stamp(), **pins, 'plan_sha256': g.sha(mirror.encode(plan)), 'before': plan['preconditions'], 'before_state_bytes': old_state.decode(), 'before_history_bytes': old_history.decode(), 'state_after_sha256': plan['state_after_sha256'], 'history_after_sha256': plan['history_after_sha256'], 'write_order': ['history.jsonl', 'state.json'], 'new_event': g.ID, 'new_proof_turns': 0, 'lock_limitation': 'Cooperative advisory lock; noncooperating writers remain outside protocol.'}
        g.dump(g.A / 'state_mirror_intent.json', intent, exclusive=True)
        for path, digest in protected.items():
            g.require(g.sha((g.R / path).read_bytes()) == digest, 'Protected binding changed before write: ' + path)
        g.write(history_path, old_history + plan['history_append_bytes'].encode())
        g.require(state_path.read_bytes() == old_state, 'History-first write altered state unexpectedly')
        g.require(g.sha(history_path.read_bytes()) == plan['history_after_sha256'], 'History append differs')
        g.write(state_path, plan['state_after_bytes'].encode())
        g.require(g.sha(state_path.read_bytes()) == plan['state_after_sha256'] and g.sha(history_path.read_bytes()) == plan['history_after_sha256'], 'Mirror output differs')
        for path, digest in protected.items():
            g.require(g.sha((g.R / path).read_bytes()) == digest, 'Protected binding changed by mirror: ' + path)
        g.foreign_tracked_unchanged(pre)
        intent.update(status='COMPLETED', completed_at_utc=g.stamp())
        g.dump(g.A / 'state_mirror_intent.json', intent)
        g.dump(g.A / 'state_mirror_receipt.json', {'at_utc': g.stamp(), 'preflight': validation, 'negative_ledger_controls': negatives, 'history_events_added': 1, 'prior_state_entries_semantically_unchanged': 27, 'current_targets': 28, 'consumed_substantive_turns': 33, 'complete_primary_count': 27, 'duplicate_count': 1, 'new_proof_turns_added_by_mirror': 0, 'entire_original_ledger_bytes_unchanged': True, 'protected_bindings_unchanged': len(protected), 'legacy_generator_run': False, 'state_sha256': g.sha(state_path.read_bytes()), 'history_sha256': g.sha(history_path.read_bytes()), 'scope': 'One present source-bound accepted partial; exact complete prior history prefix retained, no historical proof/readiness transition invented.'}, exclusive=True)
    print(json.dumps({'status': 'COMPLETED', 'pr': g.PR, 'targets': 28, 'consumed_turns': 33, 'primary_acceptances': 27, 'new_proof_turns': 0}))

if __name__ == '__main__':
    g.run(main)
