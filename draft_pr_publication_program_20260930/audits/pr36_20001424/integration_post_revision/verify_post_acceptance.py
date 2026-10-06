#!/usr/bin/env python3
"""Future root-only read-only scientific/queue/state/history/remote postvalidation.

Only a new audit PASS receipt is written after all checks. No shared file is
rewritten; a fresh proposal refreshes only its current inventory binding in
memory. The actual historical proposal, event and original ledger stay exact.
"""
import argparse, copy, json
import pr36_guards as g

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    g.add_gate_args(parser)
    args = parser.parse_args()
    frozen, pins = g.gates(args)
    acceptance = g.load(g.K / 'acceptance.json')
    audit = g.load(g.A / 'acceptance.json')
    g.require({k: v for k, v in audit.items() if k not in {'canonical_manifest_sha256', 'canonical_manifest_entries'}} == acceptance, 'Audit/canonical receipts differ')
    g.require(all(acceptance[k] == v for k, v in pins.items()), 'Final gate pins differ')
    g.require('ACCEPTANCE.json' not in {p.name for p in g.K.iterdir()} and 'acceptance.json' in {p.name for p in g.K.iterdir()}, 'Canonical receipt literal filename must be lowercase acceptance.json')
    rows = g.manifest(g.K, g.K / 'MANIFEST.json', audit['canonical_manifest_sha256'], audit['canonical_manifest_entries'])
    for z in frozen:
        path = g.K / ('reviewed_pending_administration' if z['path'] in g.ADMIN else '') / z['path']
        g.require(path.read_bytes() == (g.C / z['path']).read_bytes(), 'Reviewed science or archived administration altered: ' + z['path'])
    g.require((g.K / 'reviewed_pending_administration/MANIFEST.json').read_bytes() == (g.C / 'MANIFEST.json').read_bytes(), 'Dated reviewed manifest archive altered')
    g.require((g.K / 'turns.jsonl').read_bytes() == (g.K / 'original_archive/turns.jsonl').read_bytes() and g.sha((g.K / 'turns.jsonl').read_bytes()) == g.LEDGER_SHA, 'Original whole ledger changed')
    g.require(g.load(g.K / 'source_record.json')['problem'] == g.load(g.K / 'problem.json') and g.load(g.K / 'source_record.json')['upstream_prior_report'] == g.load(g.K / 'prior_report.json'), 'Nested/raw problem or complete prior report differs')
    g.require(g.sha((g.K / 'CURRENT_UNIVERSAL_CERTIFICATE.md').read_bytes()) == acceptance['canonical_scientific_artifact_sha256'], 'Current science receipt differs')
    g.require(g.sha((g.K / 'CANDIDATE.md').read_bytes()) == acceptance['original_graph_candidate_sha256'], 'Historical original graph receipt differs')
    for rel in ['readiness.json', 'status.json']:
        value = g.load(g.K / rel)
        g.require(value['status'] == 'already_solved_accepted_partial_merged' and value['queue_status'] == 'already_solved' and value['current_gate'] == 'PASS_NEW_complete_source_first_and_actual_root_reproduction' and value['merge_commit'] == acceptance['merge_commit'] and value['current_workflow_completion_estimate_percent'] == 100, 'Canonical administration falsely pending or unbound')
        budget = value['budget']
        g.require(budget['original_substantive_attempts'] == budget['used_substantive_attempts'] == 1 and budget['maximum_substantive_attempts'] == 5 and budget['new_substantive_attempts'] == budget['verification_attempts'] == 0, 'Budget metadata differs')
        g.require(value['current_deadline_utc'] is None and value['current_model'] == 'Not independently exposed in this runtime' and value['current_reasoning_effort'] == 'Not independently exposed in this runtime', 'Historical model/deadline improperly promoted')
    remote = g.remote()
    g.require(remote == g.load(g.A / 'remote_merge_receipt.json') and remote['state'] == 'MERGED' and remote['isDraft'] is False and remote['mergedAt'] == acceptance['merged_at'] and remote['mergeCommit']['oid'] == acceptance['merge_commit'], 'Fresh actual remote acceptance differs')
    g.require(remote['body'] == (g.K / 'pr_body.md').read_text() == (g.A / 'accepted_pr_body.md').read_text(), 'Actual remote/canonical/reviewed body differs')
    pre = g.load(g.A / 'integration_preflight.json')
    g.foreign_tracked_unchanged(pre)
    merge = acceptance['merge_commit']
    parents = g.git('show', '-s', '--format=%P', merge).split()
    g.require(parents == acceptance['merge_parents'] == [pre['main_before'], g.HEAD], 'Actual exact no-ff merge parents differ')
    g.git_bytes('merge-base', '--is-ancestor', merge, 'HEAD')
    qp = g.load(g.K / 'ACCEPTED_QUEUE_PATCH.json')
    old_q = (g.A / 'integration_queue_before.md').read_bytes()
    q = g.Q.read_bytes()
    overlay = g.load(g.A / 'integration_check.json')
    g.merged_overlay_tree(merge, overlay, q)
    g.require(g.sha((g.A / 'integration_merge_queue_before.md').read_bytes()) == overlay['root_reviewed_automatic_merge_queue_preimage_sha256'], 'Root-reviewed automatic merged queue preimage archive changed')
    g.require(g.sha(old_q) == qp['whole_before_sha256'] == pre['whole_queue_before_sha256'] and g.sha(q) == qp['whole_after_sha256'], 'Current full queue preimage/after hashes differ')
    g.require(old_q.replace(qp['row_before'].encode(), qp['row_after'].encode(), 1) == q and q.count(qp['row_after'].encode()) == 1 and q.replace(qp['row_after'].encode(), qp['row_before'].encode(), 1) == old_q, 'Whole queue is not exact unique named-row replacement')
    fields, accepted = qp['row_before'].split('|'), qp['row_after'].split('|')
    g.require(g.selected_row(q) == qp['row_after'] and len(fields) == len(accepted) == 14 and all(fields[i] == accepted[i] for i in range(14) if i not in {8, 9, 11}) and accepted[8].strip() == 'already_solved' and accepted[9].strip() == '1/5', 'Exact12-column Status/Turns/Findings-only contract broken')
    old_state_raw = g.git_bytes('show', merge + ':unsolved_math_prioritization/state.json')
    old_history_raw = g.git_bytes('show', merge + ':unsolved_math_prioritization/history.jsonl')
    g.require(g.sha(old_state_raw) == pre['state_before_sha256'] and g.sha(old_history_raw) == pre['history_before_sha256'], 'Merge failed to retain previous shared state/history')
    old_state = json.loads(old_state_raw)
    state = g.load(g.R / 'unsolved_math_prioritization/state.json')
    plan = g.load(g.A / 'state_mirror_plan.json')
    history = (g.R / 'unsolved_math_prioritization/history.jsonl').read_bytes()
    tail = plan['history_append_bytes'].encode()
    g.require(len(plan['history_append']) == 1 and plan['history_append'][0]['id'] == g.ID and tail and history == old_history_raw + tail, 'Prior entire history prefix or single present event changed')
    g.require(len(old_state) == 26 and len(state) == 27 and sum(x['turns_used'] for x in state.values()) == 32 and all(state[k] == v for k, v in old_state.items()) and state == plan['state_after'], 'Prior state or27/32 accounting changed')
    g.require(g.sha(history) == plan['history_after_sha256'] and g.sha((g.R / 'unsolved_math_prioritization/state.json').read_bytes()) == plan['state_after_sha256'], 'Actual mirror output hashes differ')
    g.require(state[g.ID]['evidence']['accepted_source']['path'].endswith('/problem.json') and state[g.ID]['evidence']['historical_transitions_asserted'] is False and state[g.ID]['evidence']['import_is_present_day_mirror'] is True, 'Wrong full source binding or historical event scope')
    intent = g.load(g.A / 'state_mirror_intent.json')
    g.require(intent['status'] == 'COMPLETED' and intent['before_state_bytes'].encode() == old_state_raw and intent['before_history_bytes'].encode() == old_history_raw, 'Durable intent/original prefixes differ')
    g.require(g.sha(g.PREVIOUS.read_bytes()) == g.PREVIOUS_SHA, 'Original base proposal changed')
    mirror = g.load_mirror()
    saved_proposal = g.load(g.A / 'state_mirror_bindings.json')
    base_proposal = g.load(g.PREVIOUS)
    g.require(saved_proposal['entries'][:-1] == base_proposal['entries'] and saved_proposal.get('duplicate_mirrors') == base_proposal.get('duplicate_mirrors'), 'Earlier primary/duplicate proposal entries changed')
    fresh_proposal = copy.deepcopy(saved_proposal)
    # Only current global inventory may receive later bookkeeping. Queue and
    # every historical event binding must still be exact from actual acceptance.
    fresh_proposal['inventory'] = g.binding(g.R / fresh_proposal['inventory']['path'])
    fresh = mirror.build_plan(g.R, fresh_proposal)
    validation = mirror.validate_plan(g.R, fresh)
    g.require(not fresh['history_append'] and fresh['state_after'] == state and fresh['state_after_bytes'].encode() == (g.R / 'unsolved_math_prioritization/state.json').read_bytes(), 'Read-only fresh proposal would invent an event or rewrite state')
    inventory = g.load(g.B / 'inventory.json')
    count = sum(z.get('stage') == 'complete' for z in inventory['items'])
    g.require(count == inventory['completed_count'] == 26 and inventory['program_completion_estimate_percent'] == count / 180 * 100 and fresh['primary_count'] == 26 and fresh['duplicate_count'] == 1, 'Current completed-primary counts differ')
    old_inventory = g.load(g.A / 'integration_inventory_before.json')
    old_items = {x['number']: x for x in old_inventory['items']}
    new_items = {x['number']: x for x in inventory['items']}
    g.require(len(old_items) == len(old_inventory['items']) and len(new_items) == len(inventory['items']) and set(new_items) == set(old_items), 'Full inventory item identities/counts changed or duplicated')
    g.require(all(x == old_items[x['number']] for x in inventory['items'] if x['number'] != g.PR), 'Unselected inventory item changed during PR36 acceptance')
    for z in g.load(g.A / 'snapshot_manifest.json')['files']:
        g.require(g.git_bytes('show', g.HEAD + ':unsolved_math_prioritization/attempts/' + g.ID + '/' + z['path']) == (g.K / 'original_archive' / z['path']).read_bytes(), 'Original16 Git artifact changed')
    result = {'utc': g.stamp(), 'status': 'PASS', 'pr': g.PR, **pins, 'exact_remote_merge_and_parents_verified': True, 'canonical_manifest_sha256': audit['canonical_manifest_sha256'], 'canonical_members': len(rows), 'reviewed_members_exact_science_or_archived_admin': len(frozen), 'entire_original_candidate_source_prior_ledger_preserved': True, 'named12_column_actual_queue_change_only': True, 'selected_chat_DOI_and_other_current_queue_bytes_preserved': True, 'current_read_only_mirror_validation': validation, 'fresh_proposal_inventory_binding_only_refreshed_in_memory': True, 'history_exact_single_present_acceptance_append': True, 'all_prior_states_preserved': 26, 'current_targets': 27, 'consumed_original_substantive_turns': 32, 'complete_primary_prs': 26, 'explicit_duplicate_count': 1, 'attempts': '1/5', 'new_substantive_attempts': 0, 'verification_attempts_added': 0, 'program_completion_estimate_percent': count / 180 * 100, 'paper_or_new_doi_or_tracker': False, 'shared_files_written': 0}
    g.foreign_tracked_unchanged(pre)
    g.dump(g.A / 'ROOT_POST_ACCEPTANCE_VERIFICATION.json', result, exclusive=True)
    print(json.dumps({'status': 'PASS', 'pr': g.PR, 'canonical_members': len(rows), 'targets': 27, 'turns': 32, 'completed_primary_prs': 26, 'new_proof_turns': 0}))

if __name__ == '__main__':
    g.run(main)
