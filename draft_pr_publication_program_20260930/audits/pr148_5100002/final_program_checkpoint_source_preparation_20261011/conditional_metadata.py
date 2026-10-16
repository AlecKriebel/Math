"""PR148 source-only conditional renderer. Importing this module has no effects.

Only the future reviewed runner calls render(); modeled controls call the pure
path/preservation helpers, never render or substitute a synthetic native gate.
"""
import copy
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

R = Path('/Users/alec/Documents/Math')
C = R / 'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
P = 'draft_pr_publication_program_20260930'
AR = P + '/audits/pr148_5100002'
A = C / AR
SR = AR + '/final_program_checkpoint_source_preparation_20261011'
S = C / SR
PROGRAM3 = tuple(P + '/' + n for n in ('CURRENT_PROGRESS.json', 'CURRENT_PROGRESS.md', 'RESEARCH_LOG.md'))
ORIGINAL = '538fd2584f7dc7375e4eaa91d73daddde3d073cd'
MERGE = 'f6caddda8f8be2cdb3e91494325d8f7f365bc3fc'
DOI = '10.5281/zenodo.23271172'
PR147_FINAL = 'b2a0447e66c472a61b8d43251fa301e56457a679'
PR147_RECEIPT_SHA = 'd69d5b9d92422969f69156ebf2fca144eba1ca7d8dc78cb76cb2ab83e0f1f7c5'
NATIVE_ROLE = AR + '/ROOT_ACTUAL_NATIVE_ACCEPTANCE_20261011.json'
FINAL_ROLE = AR + '/ROOT_FINAL_METADATA_ACCEPTANCE_20261011.json'
FIXED_GATES = {
    AR + '/ROOT_MATHEMATICAL_GATE_20261008.json': '7c19c3bb1b1ac652360b989655c324ce6b7c241c5780bba91fa91eb073ea7883',
    AR + '/ROOT_BOUNDED_PRIORITY_GATE_20261008.json': 'f9318f06a752b8f64f43c0adcb4e49dd5aa24911ab2680b8b80c4a771d927cbd',
    AR + '/ROOT_WHOLE_PACKAGE_R3_ACCEPTANCE_20261008.json': 'a268a4a7f98fb1ba1ab2241a43da375552b03ff9a37070ec8c08a65b54643e63',
    AR + '/ROOT_CLEAN_PUBLICATION_GATE_20261008.json': 'dc0a0b87622a20c15faf470b11926dbbec3ef97e0a7ccba7049f76af23b92bc6',
    AR + '/ROOT_ACTUAL_PUBLISHED_RECORD_ACCEPTANCE_20261009.json': '9c9ef52479548a6d21845d8f534859aaec67de30604c1f793717d4f4defc0b4b',
}
SELECTED = PROGRAM3 + tuple(FIXED_GATES) + (NATIVE_ROLE,) + tuple(SR + '/' + n for n in (
    'conditional_metadata.py', 'final_checkpoint.py', 'SOURCE_CONTRACT.json', 'CONDITIONAL_CASE_SUMMARY.json'))
MATH = ('The literal Table2 k108=(A′/A)/product sin(original internal theta_i/2), N=2 mod4, '
        'fails on one continuous physical confocal ellipse family: two strict convex primitive '
        'six-period members give11664/3125 and3645/1024, with positive gap553311/3200000.')
LIMITS = ('Garcia–Reznik known six-period geometry and Stachel connected-family machinery are credited. '
          'The named-history search is bounded; exclusive/absolute priority and independent discovery '
          'are unestablished. No corrected all-period invariant is proved. Extensive AI use and '
          'unrefereed status are disclosed; conventional human peer review is not claimed.')

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def digest(body):
    return hashlib.sha256(body).hexdigest()

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')

def relative(path):
    require(isinstance(path, str) and 0 < len(path) <= 1024, 'invalid path')
    require(not path.startswith('/') and all(x not in ('', '.', '..', '.git') for x in path.split('/')), 'unsafe relative path')
    require(all(32 <= ord(ch) < 127 for ch in path) and '\\' not in path, 'nonportable path')
    return path

def list_prefix(old, new, role):
    require(isinstance(old, list) and isinstance(new, list) and new[:len(old)] == old, role + ' history not preserved')

def preserve(remote, local):
    """Pure baseline validation; no I/O, gate construction or completion inference."""
    require(set(remote) == set(PROGRAM3) == set(local), 'exact independent program3 required')
    for path in PROGRAM3[1:]:
        require(local[path].startswith(remote[path]), 'remote text prefix differs: ' + path)
        local[path].decode('utf-8')
    old, cur = json.loads(remote[PROGRAM3[0]]), json.loads(local[PROGRAM3[0]])
    require(cur['current_PR'] == 148 and cur['current_original_literal_status'] == 'claimed_solved', 'current eligible PR drift')
    require(cur['current_original_head'] == ORIGINAL and cur['current_original_budget'] == '1/5', 'original provenance drift')
    require(cur['current_original_substantive_author_approach_count'] == 1 and
            cur['current_actual_timestamped_author_chat_turn_ledger_present'] is False and
            cur['current_original_native_transition_ledger_present'] is False and
            cur['current_new_central_proof_search_turns'] == 0, 'original missing-ledger/effort provenance drift')
    require(cur['dated_eligible_total'] == 99 and cur['fully_completed_count'] == 26 and cur['published_count'] == 14, 'local counts drift')
    require(old['dated_eligible_total'] == 99 and old['fully_completed_count'] == 26 and old['published_count'] == 14, 'remote counts drift')
    for key in ('fully_completed_eligible_PRs', 'published_PRs', 'historical_completed_case_records', 'historical_preparation_snapshots',
                'accepted_partial_prior_result_PRs', 'accepted_partial_priority_unestablished_PRs', 'closed_without_publication_PRs',
                'status_only_skips_before_PR134_completion'):
        list_prefix(old[key], cur[key], key)
    require(len(cur['fully_completed_eligible_PRs']) == 26 and len(cur['published_PRs']) == 14, 'count/list inconsistency')
    require(148 not in cur['fully_completed_eligible_PRs'] and 148 not in cur['published_PRs'], 'completion replay')
    require(cur['last_completed_metadata_checkpoint_commit'] == PR147_FINAL, 'actual PR147 final lost')
    require(cur['last_completed_transaction_receipt_reference']['final_metadata_readback_sha256'] == PR147_RECEIPT_SHA, 'actual PR147 receipt lost')
    # Old remote current/last/scalar state is retained verbatim in a dated predecessor
    # record, including differences from the current local mathematical checkpoint.
    return old, cur

def actual_gate(native, goal, now):
    """Validate the ROOT-supplied genuine records, never create or infer them."""
    require(native.get('schema') == 'pr148-root-actual-native-final-acceptance/v1' and
            native.get('status') == 'ACCEPTED_NATIVE_PUBLIC_AND_LOCAL', 'genuine native acceptance required')
    require(native.get('PR') == 148 and native.get('problem_id') == 5100002 and native.get('code') == 'AMR-050-0002', 'native case mismatch')
    require(native.get('original_head') == ORIGINAL and native.get('original_merge') == MERGE, 'native original disposition mismatch')
    for field in ('full_public_body_mode_readback', 'full_local_body_mode_readback',
                  'whole_parent_tree_preserved_outside_exact_overlay', 'exact_main_compare_and_swap_observed'):
        require(native.get(field) is True, 'native acceptance incomplete: ' + field)
    for field in ('program3_changed', 'force_update_requested', 'ordinary_Git_push_used'):
        require(native.get(field) is False, 'native prohibited operation: ' + field)
    require(native.get('native_remote_changed_path_count') == 19 and native.get('native_local_installed_path_count') == 33 and
            native.get('remote_unchanged_original_path_count') == 14, 'native exact scope mismatch')
    require(native.get('original_effort') == '1/5' and native.get('new_central_proof_search_turns') == 0, 'native effort mismatch')
    for field in ('native_commit', 'native_tree', 'sole_parent'):
        require(re.fullmatch('[0-9a-f]{40}', str(native.get(field))) is not None, 'native object absent')
    require(isinstance(native.get('actual_ROOT_PID'), int) and native['actual_ROOT_PID'] > 0, 'ROOT native identity absent')
    require(goal.get('schema') == 'ROOT-actual-goal-tool-response-record/v1' and goal.get('owner') == 'ROOT', 'fresh genuine ROOT goal record required')
    require(isinstance(goal.get('actual_recorder_PID'), int) and goal['actual_recorder_PID'] > 0, 'goal recorder absent')
    native_time = dt.datetime.fromisoformat(native['UTC'].replace('Z', '+00:00'))
    goal_time = dt.datetime.fromisoformat(goal['UTC'].replace('Z', '+00:00'))
    require(native_time.tzinfo is not None and goal_time.tzinfo is not None and native_time <= goal_time <= now, 'goal/native chronology invalid')
    require((now - goal_time).total_seconds() <= 1800, 'ROOT goal observation older than30 minutes')
    response = goal['get_goal_response']
    require(isinstance(response, dict) and isinstance(response.get('goal'), dict) and response['goal'].get('status') == 'active', 'goal must remain active')
    require(response['goal'].get('objective') and isinstance(response['goal'].get('updatedAt'), (int, float)), 'full goal response absent')
    return response['goal']

def render(remote, local, native, goal, pins, now):
    """Future conditional proposal; caller supplies fully read, ROOT-reviewed inputs."""
    observed = actual_gate(native, goal, now)
    old, cur = preserve(remote, local)
    out = copy.deepcopy(cur)
    stamp = now.isoformat()
    out['historical_preparation_snapshots'].append({
        'UTC': stamp, 'status': 'PR148_SEPARATE_REMOTE_AND_LOCAL_PREIMAGES_PRESERVED',
        'remote_program_json_sha256': digest(remote[PROGRAM3[0]]),
        'local_program_json_sha256': digest(local[PROGRAM3[0]]),
        'prior_remote_fields': old, 'prior_local_fields': cur,
        'note': 'Remote predecessor and current local mathematical checkpoint are distinct; neither is silently substituted.'})
    for key in ('current_PR_workflow_percent', 'current_workflow_estimate_percent', 'current_priority_audit_percent', 'current_mathematical_audit_percent'):
        out[key] = 100
    out.update({
        'UTC': stamp, 'updated_UTC': stamp,
        'current_DOI': DOI, 'current_Zenodo_published': True,
        'current_core_disposition_complete': True,
        'current_disposition': 'published_merged_attributed_literal_k108_counterexample_conditional_final_acceptance',
        'current_native_status': 'claimed_solved',
        'current_native_export_state': 'ACTUALLY_PUBLISHED_INSTALLED_AND_FULLY_ACCEPTED',
        'current_native_completion_acceptance': NATIVE_ROLE[len(P)+1:],
        'current_native_completion_acceptance_sha256': pins['native']['sha256'],
        'current_native_disposition_checkpoint_commit': native['native_commit'],
        'current_native_public_changed_path_count': 19, 'current_native_local_installed_path_count': 33,
        'current_mathematical_scope': MATH, 'current_mathematical_scope_limits': [LIMITS],
        'current_priority_audit_scope': LIMITS, 'current_priority_clearance': True,
        'current_priority_status': 'completed_bounded_attributed_corrective_application_support',
        'current_priority_gate': 'audits/pr148_5100002/ROOT_BOUNDED_PRIORITY_GATE_20261008.json',
        'current_priority_gate_sha256': FIXED_GATES[AR + '/ROOT_BOUNDED_PRIORITY_GATE_20261008.json'],
        'current_publication_package_prepared': True, 'current_publication_package_review_clearance': True,
        'current_publication_package_review_status': 'R1_NEEDS_REPAIR_R2_NEEDS_REPAIR_R3_PASS_same_final_frozen_package',
        'current_publication_package_reviews_required': False, 'current_publication_ready': True,
        'current_publication_upload_clearance': True, 'current_tracker_updated': True,
        'current_tracker_range': "'Math Puzzles'!A58:D58",
        'current_active_checkpoint_pending': False, 'current_completion_metadata_checkpoint_pending': False,
        'current_original20_preservation_scope': 'Frozen original20 and immutable publication_package_v1 retained; accepted canonical native33 preserved.',
        'current_remaining_required_steps': 'No PR148 case step remains in the conditional accepted end state, once the separate genuine ROOT final receipt confirms exact publication/local3 full readbacks; no intake149 now.',
        'fully_completed_count': 27, 'published_count': 15, 'fully_completed_fraction_percent': 27.27,
        'workflow_estimate_percent': 27.27,
        'last_completed_PR': 148, 'last_published_PR': 148, 'last_completed_DOI': DOI, 'last_published_DOI': DOI,
        'last_completed_PR_workflow_percent': 100,
        'last_completed_mathematical_result_valid': True, 'last_completed_priority_clearance': True,
        'last_completed_publication_authorization': True, 'last_completed_original_budget': '1/5',
        'last_completed_new_central_proof_search_turns': 0,
        'last_completed_merge_commit': MERGE, 'last_completed_native_correction_commit': native['native_commit'],
        'last_completed_metadata_checkpoint_commit': None,
        'last_completed_outcome': 'published_merged_attributed_literal_k108_counterexample_conditional_final_acceptance',
        'last_completed_source_resolution_scope': MATH + ' ' + LIMITS,
        'last_completed_tracker_range': "'Math Puzzles'!A58:D58",
        'last_completed_record': NATIVE_ROLE[len(P)+1:],
        'last_completed_actual_final_gate': FINAL_ROLE[len(P)+1:],
        'last_completed_final_completion_readback': FINAL_ROLE[len(P)+1:],
        'last_completed_actual_writer_release': None,
        'actual_final_metadata_preparer_PID': None,
        'actual_active_metadata_preparer_PID': None,
        'active_checkpoint_commit': None, 'active_checkpoint_acceptance_receipt': None,
        'active_checkpoint_actual_readback_required': False, 'active_checkpoint_source_plan_review_required': False,
        'advance_to_next_PR_authorized_now': False, 'next_numeric_intake_cursor': 149,
        'next_eligible_PR_after_current_completion': None,
        'next_intake_requires_actual_completion_receipt_and_explicit_writer_release': True,
        'next_step': 'After genuine ROOT final acceptance and writer release, perform fresh ascending original-claimed_solved-only status intake starting numeric149; do not intake now.',
        'remaining_current_step': 'PR148 is complete in the conditional accepted end state after separate ROOT final acceptance. Persistent program remains active; later intake still needs the actual receipt and writer release.',
        'completion_metadata_checkpoint_pending_at_snapshot': True,
        'persistent_goal_complete': False, 'persistent_goal_status': 'active', 'persistent_goal_status_at_last_tool_read': 'active',
        'persistent_goal_API_last_observed_UTC': goal['UTC'], 'persistent_goal_API_updatedAt': observed['updatedAt'],
        'persistent_goal_status_observation_source': pins['goal']['path'],
        'persistent_goal_status_observation_sha256': pins['goal']['sha256'],
        'persistent_goal_status_observation_is_dated_ROOT_readback': True,
        'program_snapshot_semantics': 'Conditional accepted end state27/99 and15 publications; actual native/paper/tracker/merge facts already verified. Final program receipt pending.',
        'program_snapshot_UTC_semantics': 'UTC is conditional preparation only. Own future commit/PID/acceptanceUTC are unset; a separate ROOT final receipt supplies them after actual closure.',
        'program_snapshot_authority_condition': 'Authoritative only after exact scoped final publication, local3 full readbacks and separate genuine ROOT final acceptance; no current intake authorization.'})
    out['fully_completed_eligible_PRs'].append(148)
    out['published_PRs'].append(148)
    out['last_completed_transaction_receipt_reference'] = {
        'native_acceptance': NATIVE_ROLE[len(P)+1:], 'native_acceptance_sha256': pins['native']['sha256'],
        'actual_native_commit': native['native_commit'], 'actual_native_acceptance_UTC': native['UTC'],
        'metadata_commit': None, 'metadata_actual_PID': None, 'metadata_actual_UTC': None,
        'final_metadata_readback': FINAL_ROLE[len(P)+1:], 'final_metadata_readback_sha256': None,
        'separate_final_metadata_receipt_role': FINAL_ROLE[len(P)+1:]}
    for field in ('current_absolute_priority_established', 'current_exclusive_priority_established',
                  'current_independent_discovery_established', 'current_novelty_established', 'current_copying_or_collaboration_inferred',
                  'current_actual_timestamped_author_chat_turn_ledger_present', 'current_original_native_transition_ledger_present'):
        out[field] = False
    entry = ('\n\n## ' + stamp + ' — PR148 conditional final checkpoint; case100%;27/99 completed,15 publications\n\n'
             + MATH + ' ' + LIMITS + '\n\n'
             'DOI ' + DOI + ", tracker 'Math Puzzles'!A58:D58 (one append/two readbacks), and original-head merge " + MERGE +
             ' are actual prior facts and are never replayed. Genuine native acceptance binds19 public changes,33 local bodies and14 unchanged originals; native commit ' + native['native_commit'] + '. '
             'Raw paper reviews remain R1 NEEDS_REPAIR, R2 NEEDS_REPAIR, R3 PASS; no two-clean-review claim. '
             'Original effort1/5 reports one approach in turns.json; timestamped chat-turn and native-transition ledgers are absent. Zero new central proof-search turns. '
             'PR147 actual final ' + PR147_FINAL + ' and receipt SHA' + PR147_RECEIPT_SHA + ' remain historical facts. '
             'This end state becomes authoritative only after final scoped publication, separate local3 install/full readbacks and genuine ROOT final acceptance. '
             'Its own future commit/PID/acceptance time are unset. Persistent goal remains ACTIVE unfinished; numeric cursor149 is reserved, with no intake149 now.\n').encode()
    summary = {'schema': 'pr148-conditional-final-case-summary/v1', 'UTC': stamp, 'status': 'CONDITIONAL_PROPOSAL_NOT_ACTUAL_FINAL_ACCEPTANCE',
               'PR': 148, 'result': MATH, 'limits': LIMITS, 'DOI': DOI, 'original_head': ORIGINAL, 'original_merge': MERGE,
               'original_effort': '1/5', 'reported_original_approaches': 1, 'timestamped_chat_turn_ledger_present': False,
               'original_native_transition_ledger_present': False, 'new_central_proof_search_turns': 0,
               'raw_paper_reviews': ['R1_NEEDS_REPAIR', 'R2_NEEDS_REPAIR', 'R3_PASS'], 'two_clean_reviews_claimed': False,
               'native_acceptance': pins['native'], 'goal_observation': pins['goal'], 'actual_final_commit': None,
               'actual_final_PID': None, 'actual_final_acceptance_UTC': None, 'separate_ROOT_final_receipt_role': FINAL_ROLE,
               'case_percent_if_finally_accepted': 100, 'completed_if_finally_accepted': 27, 'published_if_finally_accepted': 15,
               'dated_denominator': 99, 'persistent_goal_status': 'active', 'persistent_goal_complete': False,
               'next_numeric_cursor_if_finally_accepted': 149, 'intake149_authorized_now': False,
               'remote_preimages': {k: digest(v) for k, v in remote.items()}, 'local_preimages': {k: digest(v) for k, v in local.items()}}
    return {PROGRAM3[0]: encoded(out), PROGRAM3[1]: local[PROGRAM3[1]] + entry,
            PROGRAM3[2]: local[PROGRAM3[2]] + entry, SR + '/CONDITIONAL_CASE_SUMMARY.json': encoded(summary)}
