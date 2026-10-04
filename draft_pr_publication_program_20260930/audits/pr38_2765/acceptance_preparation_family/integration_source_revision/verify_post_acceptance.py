#!/usr/bin/env python3
"""Prepared root-only read-only complete PR38 post-acceptance validation.

No shared file is rewritten. Only a new audit receipt is created after all
checks pass. Preparation must never execute or import this helper.
"""
import argparse
import copy
import json
import sys
# Future root entry points preserve every sealed source closure.
sys.dont_write_bytecode = True
import pr38_guards as g


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    g.add_gate_args(parser)
    args = parser.parse_args()
    frozen, pins = g.gates(args)
    literal = {p.name for p in g.K.iterdir()}
    g.require('acceptance.json' in literal and 'ACCEPTANCE.json' not in literal, 'Require actual literal lowercase canonical acceptance.json')
    acceptance = g.load(g.K / 'acceptance.json')
    audit = g.load(g.A / 'acceptance.json')
    pre = g.load(g.A / 'integration_preflight.json')
    g.acceptance_invariants(acceptance, pins, pre)
    g.acceptance_invariants(audit, pins, pre)
    g.require(g.strict_equal({key: value for key, value in audit.items() if key not in {'canonical_manifest_sha256', 'canonical_manifest_entries'}}, acceptance), 'Complete audit/canonical acceptance value/type differ')
    members = g.manifest(g.K, g.K / 'MANIFEST.json', audit['canonical_manifest_sha256'], audit['canonical_manifest_entries'])
    g.canonical_unchanged(frozen, True)
    g.require(g.sha((g.K / 'RESULTS.md').read_bytes()) == acceptance['canonical_scientific_artifact_sha256'] == g.RESULTS_SHA, 'Reviewed current partial receipt differs')
    g.require(g.sha((g.K / 'turns.json').read_bytes()) == acceptance['original_ledger_sha256'] == g.LEDGER_SHA and (g.K / 'turns.json').read_bytes() == (g.K / 'original_archive/turns.json').read_bytes(), 'Whole authored ledger changed')
    g.require(acceptance['queue_status'] == 'unsolved' and acceptance['full_problem_solved'] is False and acceptance['positive_novelty_claim'] is False and acceptance['paper_or_new_doi_or_tracker'] is False, 'Partial improperly promoted')
    g.require(acceptance['accepted_source_for_mirror'] == 'source_record.json' and acceptance['separate_prior_report_present'] is False and acceptance['importer_empty_fallback_is_not_retrieved_report'] is True, 'Flat source/fallback improperly replaced')
    for name in ['readiness.json', 'status.json', 'attempt.json']:
        value = g.load(g.K / name)
        g.require(value['status'] == 'unsolved_accepted_partial_merged' and value['queue_status'] == 'unsolved' and value['current_gate'] == 'PASS_current_source_first_v2_alias_and_bound_original_actual_replay', 'Canonical administration pending/misclassified')
        g.require(value['merge_commit'] == acceptance['merge_commit'] and value['merge_tree'] == acceptance['merge_tree'] and value['current_workflow_completion_estimate_percent'] == 100 and value['full_resolution_completion_estimate_percent'] == 0, 'Administrative merge/estimate differs')
        budget = value['budget']
        g.require(budget['original_substantive_attempts'] == budget['used_substantive_attempts'] == 2 and budget['maximum_substantive_attempts'] == 5 and budget['new_substantive_attempts'] == budget['verification_attempts'] == 0, 'Budget metadata differs')
        g.require(value['current_model'] is None and value['current_reasoning_effort'] is None and value['current_deadline_utc'] is None and budget['current_model'] is None and budget['current_reasoning_effort'] is None and budget['current_deadline_utc'] is None and budget['historical_only'] is True, 'Historical runtime/deadline metadata promoted')
        g.require(value['full_problem_solved'] is False and value['positive_novelty_claim'] is False and value['paper_or_new_doi_or_tracker'] is False, 'Unsolved scope improperly promoted')
    remote = g.remote()
    saved_remote = g.load(g.A / 'remote_merge_receipt.json')
    g.require(remote == saved_remote and remote['state'] == 'MERGED' and remote['isDraft'] is False and remote['mergedAt'] == acceptance['merged_at'] and remote['mergeCommit']['oid'] == acceptance['merge_commit'], 'Fresh actual GitHub acceptance differs')
    g.require(remote['body'] == (g.K / 'pr_body.md').read_text() == (g.A / 'accepted_pr_body.md').read_text(), 'Full remote/canonical/reviewed body differs')
    prepush = g.load(g.A / 'integration_prepush.json')
    overlay = g.load(g.A / 'integration_check.json')
    g.require(all(prepush[key] == value == overlay[key] for key, value in pins.items()), 'Prepush/overlay pins differ')
    merge = acceptance['merge_commit']
    queue = g.Q.read_bytes()
    tree = g.tree_binding(merge, pre, overlay, queue)
    g.require(merge == prepush['merge_commit'] and tree == prepush['merge_tree'] == acceptance['merge_tree'] and acceptance['merge_parents'] == prepush['merge_parents'] == [pre['main_before'], g.HEAD], 'Actual real merge tree/parents differ from prepush')
    g.require(g.sha((g.A / 'integration_merge_queue_before.md').read_bytes()) == overlay['root_reviewed_automatic_merge_queue_preimage_sha256'], 'Automatic merged whole queue capture changed')
    old_queue = (g.A / 'integration_queue_before.md').read_bytes()
    patch = g.load(g.K / 'ACCEPTED_QUEUE_PATCH.json')
    g.require(g.sha(old_queue) == patch['whole_before_sha256'] == pre['whole_queue_before_sha256'] == pre['root_explicit_fresh_queue_preimage_sha256'] and g.sha(queue) == patch['whole_after_sha256'], 'Whole fresh queue before/after hashes differ')
    g.require(old_queue.count(patch['row_before'].encode()) == 1 and queue.count(patch['row_after'].encode()) == 1 and old_queue.replace(patch['row_before'].encode(), patch['row_after'].encode(), 1) == queue and queue.replace(patch['row_after'].encode(), patch['row_before'].encode(), 1) == old_queue, 'Whole queue is not unique exact named-row replacement')
    before_fields, after_fields = patch['row_before'].split('|'), patch['row_after'].split('|')
    g.require(g.selected_row(queue) == patch['row_after'] and len(before_fields) == len(after_fields) == 14 and all(before_fields[i] == after_fields[i] for i in range(14) if i not in {8, 9, 11}) and after_fields[8].strip() == 'unsolved' and after_fields[9].strip() == '2/5', 'Exact12-column Status/Turns/Findings-only contract broken')
    old_state_raw = g.git_bytes('show', merge + ':unsolved_math_prioritization/state.json')
    old_history_raw = g.git_bytes('show', merge + ':unsolved_math_prioritization/history.jsonl')
    g.require(g.sha(old_state_raw) == pre['state_before_sha256'] and g.sha(old_history_raw) == pre['history_before_sha256'], 'Merge changed shared state/history before present mirror')
    old_state = json.loads(old_state_raw)
    state_path = g.R / 'unsolved_math_prioritization/state.json'
    state = g.load(state_path)
    history = (g.R / 'unsolved_math_prioritization/history.jsonl').read_bytes()
    plan = g.load(g.A / 'state_mirror_plan.json')
    tail = plan['history_append_bytes'].encode()
    g.require(len(plan['history_append']) == 1 and plan['history_append'][0]['id'] == g.ID and plan['history_append'][0]['event'] == 'acceptance_mirror_import' and tail and history == old_history_raw + tail, 'Require complete history prefix plus one present acceptance')
    g.require(len(old_state) == 28 and len(state) == 29 and g.ID not in old_state and sum(z['turns_used'] for z in state.values()) == 35 and all(state[key] == value for key, value in old_state.items()) and state == plan['state_after'], 'Prior states/native29targets35turns accounting changed')
    g.require(g.sha(history) == plan['history_after_sha256'] and g.sha(state_path.read_bytes()) == plan['state_after_sha256'], 'Actual mirror output differs')
    entry = state[g.ID]
    g.require(entry['status'] == 'unsolved' and entry['turns_used'] == 2 and entry['turn_limit'] == 5 and entry['evidence']['accepted_source']['path'].endswith('/source_record.json') and entry['evidence']['historical_transitions_asserted'] is False and entry['evidence']['import_is_present_day_mirror'] is True, 'No invented historical native proof/readiness event or new turn')
    intent = g.load(g.A / 'state_mirror_intent.json')
    g.require(intent['status'] == 'COMPLETED' and intent['before_state_bytes'].encode() == old_state_raw and intent['before_history_bytes'].encode() == old_history_raw, 'Durable intent/original complete prefixes differ')
    g.require(g.sha(g.PREVIOUS.read_bytes()) == g.PREVIOUS_SHA, 'Frozen PR37 mirror base changed')
    saved = g.load(g.A / 'state_mirror_bindings.json')
    base = g.load(g.PREVIOUS)
    g.require(saved['entries'][:-1] == base['entries'] and saved.get('duplicate_mirrors') == base.get('duplicate_mirrors') and saved['required_completed_prs'] == sorted(base['required_completed_prs'] + [g.PR]), 'Prior primary/duplicate bindings changed')
    mirror = g.load_mirror()
    fresh_proposal = copy.deepcopy(saved)
    fresh_proposal['inventory'] = g.binding(g.R / fresh_proposal['inventory']['path'])
    fresh = mirror.build_plan(g.R, fresh_proposal)
    validation = mirror.validate_plan(g.R, fresh)
    g.require(not fresh['history_append'] and fresh['state_after'] == state and fresh['state_after_bytes'].encode() == state_path.read_bytes(), 'Fresh read-only proposal invents event/state rewrite')
    inventory = g.load(g.B / 'inventory.json')
    old_inventory = g.load(g.A / 'integration_inventory_before.json')
    g.unselected_inventory(old_inventory, inventory)
    g.require(sorted(g.inventory_items(inventory)) == pre['inventory_complete_ids'], 'Complete captured inventory ID set changed')
    completed = sum(z.get('stage') == 'complete' for z in inventory['items'])
    g.require(completed == inventory['completed_count'] == 28 and inventory['program_completion_estimate_percent'] == completed / 180 * 100 and fresh['primary_count'] == 28 and fresh['duplicate_count'] == 1, 'Completed28/180 and explicit duplicate accounting differ')
    current_item = g.inventory_items(inventory)[g.PR]
    g.require(current_item['stage'] == 'complete' and current_item['queue_status'] == 'unsolved' and current_item['audited_head'] == g.HEAD and current_item['merge_commit'] == merge and current_item['merged_at'] == remote['mergedAt'] and current_item['cumulative_attempts'] == '2/5' and current_item['new_substantive_attempts'] == 0 and current_item['paper_or_new_doi_or_tracker'] is False, 'Selected inventory acceptance differs')
    g.foreign_tracked_unchanged(pre)
    result = {'utc': g.stamp(), 'status': 'PASS', 'pr': g.PR, **pins, 'exact_remote_merge_parents_and_real_tree_verified': True, 'merge_commit': merge, 'merge_tree': tree,
              'canonical_manifest_sha256': audit['canonical_manifest_sha256'], 'canonical_members': len(members), 'reviewed_members_exact_science_or_archived_admin': len(frozen),
              'entire_original16_source_null_prior_two_turn_ledger_diagnostics_preserved': True, 'v2_archival_alias_only_and_original_actual_replay_bound': True,
              'named12_column_actual_queue_change_only': True, 'selected_chat_DOI_and_every_other_queue_byte_preserved': True,
              'complete_inventory_id_set_and_every_unselected_item_preserved': True, 'current_read_only_mirror_validation': validation,
              'history_exact_single_present_acceptance_append': True, 'all_prior_states_preserved': 28, 'current_targets': 29, 'consumed_original_substantive_turns': 35, 'complete_primary_prs': 28, 'explicit_duplicate_count': 1,
              'attempts': '2/5', 'new_substantive_attempts': 0, 'verification_attempts_added': 0, 'full_problem_solved': False, 'positive_novelty_claim': False,
              'program_completion_estimate_percent': completed / 180 * 100, 'paper_or_new_doi_or_tracker': False, 'shared_files_written': 0}
    g.dump(g.A / 'ROOT_POST_ACCEPTANCE_VERIFICATION.json', result, exclusive=True)
    print(json.dumps({'status': 'PASS', 'pr': g.PR, 'canonical_members': len(members), 'targets': 29, 'turns': 35, 'completed_primary_prs': 28, 'new_proof_turns': 0}))


if __name__ == '__main__':
    g.run(main)
