"""Read-only exact merge95 input checks. No API, Git, builder execution or writes.

Imports only previously owned byte-pinned helper/core copies. All source/body
validation is in memory. This is source clearance, never actual native acceptance.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).absolute().parent
D = HERE.parent
A = D.parent
C = A.parents[2]
B = A / 'native_integration_preparation_01'
CASE = 'draft_pr_publication_program_20260930/audits/pr207_5100044/'
MANIFEST_PIN = {'bytes': 159432, 'sha256': 'd636727bdb719b0d9acbc76e5ef7e7040a3d2e92e55f7f539601845c45d47861'}
HELPER_PIN = {'bytes': 31634, 'sha256': 'e850bb9adcb40db4d9949251c103677e37651f3ec3daad16219227729f7e1efc'}
CORE_PIN = {'bytes': 22049, 'sha256': '8a61aee886e7a19bba6c7369944d778614b4099cbe1a060cf7e8acf2f52ec4d5'}


def check(ok, message):
    if ok is not True:
        raise RuntimeError(message)


def pin(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def source(path, wanted=None):
    check(path.resolve() == path and path.is_file(), 'Canonical regular source')
    raw = path.read_bytes()
    if wanted is not None:
        check(pin(raw) == wanted, 'Exact pinned source ' + str(path))
    return raw


def load_owned(name, wanted):
    path = D / '_private/native207_frozen_v2' / name
    source(path, wanted)
    check(path.stat().st_mode & 0o777 == 0o444, 'Owned code seal mode')
    spec = importlib.util.spec_from_file_location('merge95_followup_' + name.replace('.', '_'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    check(sys.flags.ignore_environment == 1 and sys.flags.no_site == 1 and sys.dont_write_bytecode is True and sys.flags.safe_path is True and not sys.flags.optimize, 'Ordinary isolated Python required')
    checks = []
    def passed(name):
        checks.append(dict(control=name, result='PASS'))
    # Verify old accepted artifacts without editing their log or seal.
    prior = json.loads(source(D / 'PUBLIC_ARTIFACT_MANIFEST.json', {'bytes': 2588, 'sha256': '229c6bfcbde5c96721f15258b4f2bf7f286757e4df8af707b98802047adc2c11'}))
    source(D / 'FINAL_SEAL.json', {'bytes': 926, 'sha256': '53ffb17dd736c31c5fe3d26085baa4a5968e48672411d67c9a712004b2e479f2'})
    for row in prior['files']:
        source(D / row['path'], {k: row[k] for k in ('bytes', 'sha256')})
    passed('prior_sealed_audit_all14_public_files_unchanged')
    source(B / 'native207_v2.py', HELPER_PIN)
    source(B / 'archive206_verified_reference.py', CORE_PIN)
    helper = load_owned('native207_v2.py', HELPER_PIN)
    core = load_owned('archive206_verified_reference.py', CORE_PIN)
    # Bind source reads to the actual helper folder, but execute only owned code.
    helper.BASE, helper.C, helper.P = B, C, A.parents[1]
    helper.core = lambda: core
    _, m, overlay, pre, pins = helper.inputs(B / 'MERGE95_INPUTS_01.json', MANIFEST_PIN)
    rows = {row['path']: row for row in m['files']}
    check(len(rows) == m['total_files'] == 311 and sum(map(len, overlay.values())) == m['total_bytes'] == 2594743, 'Exact selected totals')
    check(all(row['source'] == 'phase_merge95_sources/' + path for path, row in rows.items()), 'Exact one-to-one owned source mapping')
    passed('311_selected_2594743_bytes_canonical0444_SHA256_blob_and_strict_contract')
    check(m['expected_parent'] == helper.ANCHOR == '063dd13ada2e9fc004f2fcb919f1ccefbbb895a9' and m['original_head'] == helper.HEAD and m['original_head_tree'] == helper.HEAD_TREE, 'Exact parent/original native identities')
    summary = json.loads(source(A / 'root_native_integration_execution_01/MERGE95_SOURCE_FREEZE.json', {'bytes': 716, 'sha256': 'ca67aad286fafe4cc2265adb8516722bd54528c8229b6b15ddefcf47dade02be'}))
    check(summary['parent'] == m['expected_parent'] and summary['parent_tree'] == '93b58eb49c457a1f0261d9ae6664903a544875ec' and summary['manifest'] == MANIFEST_PIN and summary['no_native_ref_or_local_current_write'] is True, 'Root GET-only freeze association')
    passed('exact_anchor_original_HEAD_tree_and_Root_GET_only_parent_tree_binding')
    builder_path = CASE + 'root_native_integration_execution_01/freeze_merge95.py'
    check(pin(overlay[builder_path]) == {'bytes': 13329, 'sha256': '2562faebc8f7c19f51344f0169b48aca2ae59b68172fa4f39f4503a3544d1381'}, 'Pinned GET-only builder')
    # Recreate the builder's explicit finite set, without executing it.
    prepared = helper.decode(overlay[CASE + 'native_integration_preparation_01/ROOT_PUBLIC_SOURCE_COPY_PREPARATION_01.json'])
    check(prepared['total_files'] == len(prepared['files']) == 276 and prepared['total_bytes'] == sum(row['bytes'] for row in prepared['files']), 'Prepared source totals')
    expected = set()
    for row in prepared['files']:
        path = row['path']
        check(pin(overlay[path]) == {k: row[k] for k in ('bytes', 'sha256')} and core.native('blob', overlay[path]) == row['git_blob'], 'Prepared public source identity')
        expected.add(path)
    expected.update(CASE + 'native_integration_adversary_01/' + row['path'] for row in prior['files'])
    expected.update(CASE + 'native_integration_adversary_01/' + name for name in ['PUBLIC_ARTIFACT_MANIFEST.json', 'FINAL_SEAL.json'])
    expected.update(CASE + name for name in ['ROOT_NATIVE_INTEGRATION_PREPARATION_ACCEPTANCE_01.json', 'ROOT_ACTUAL_PR_READY_01.json', 'root_native_integration_execution_01/freeze_merge95.py', 'native_integration_preparation_01/ROOT_PUBLIC_SOURCE_COPY_PREPARATION_01.json'])
    expected.update(CASE + 'root_pr_metadata_execution_01/' + name for name in ['PRE_UPDATE_NATIVE.json', 'UPDATE_METADATA_INTENT.json', 'UPDATE_TOOL_RESULT.json', 'POST_UPDATE_NATIVE.json', 'READY_INTENT.json', 'READY_TOOL_RESULT.json', 'READY_NATIVE_READBACK.json'])
    expected.update(CASE + name for name in ['ROOT_SCOPED_MATHEMATICAL_ASSESSMENT_01.json', 'ROOT_PUBLICATION_GATE_01.json', 'ROOT_ACTUAL_PUBLICATION_01.json', 'ROOT_ACTUAL_TRACKER_01.json'])
    expected.add(m['gate_receipt'])
    expected.update(helper.VIEWS)
    expected.add(helper.QUEUE)
    check(expected == set(rows), 'Unexpected selected file outside exact builder union')
    check(not any(any(part in {'_private', 'private_work', 'renders', 'OFFLINE_FIXTURE_', 'phase_merge95_sources'} or part.startswith('OFFLINE_FIXTURE_') for part in path.split('/')) for path in rows), 'Private/fixture source tree selected')
    passed('exact_explicit_builder_union_no_recursive_private_or_operational_fixture_selection')
    plan = helper.decode(overlay[CASE + 'publication_lifecycle_preparation_01/ROOT_CURATED_PUBLIC_ARCHIVE_PLAN_01.json'])
    check(plan['file_count'] == len(plan['files']) == 132, 'Original public plan count')
    for row in plan['files']:
        check(pin(overlay[CASE + row['case_relative_path']]) == {k: row[k] for k in ('bytes', 'sha256')}, 'Original curated public-plan row')
    for folder, filename in [('whole_package_adversary_01', 'PUBLIC_ARTIFACT_MANIFEST.json'), ('whole_package_adversary_02', 'PUBLIC_ALLOWLIST_MANIFEST.json')]:
        public = helper.decode(overlay[CASE + folder + '/' + filename])
        items = public['files']
        check(type(items) is list, 'Reviewer explicit file manifest')
        for row in items:
            name = row['path']
            check(pin(overlay[CASE + folder + '/' + name]) == {k: row[k] for k in ('bytes', 'sha256')}, 'Reviewer explicit public artifact')
    passed('132_prior_public_plan_and_both_peer_explicit_public_manifests_exact')
    for path, raw in overlay.items():
        if path not in helper.VIEWS and path != helper.QUEUE and not path.startswith(helper.ATTEMPT):
            check(source(C / path) == raw, 'Selected immutable case source differs from existing file')
        if pre[path] is not None and path not in helper.VIEWS and path != helper.QUEUE:
            check(pre[path] == ('100644', 'blob', core.native('blob', raw)), 'Existing immutable native tuple would change')
    passed('all_existing_nonview_nonQUEUE_native_preimages_match_selected_bodies')
    final = helper.decode(overlay[CASE + 'finalized_current_01/FINALIZATION_MANIFEST.json'])
    native = {path: raw for path, raw in overlay.items() if path.startswith(helper.ATTEMPT)}
    check(len(native) == 22 and sum(map(len, native.values())) == 103456, 'Final native packet totals')
    for path, raw in native.items():
        check(pin(raw) == final['files']['payload/' + path] and raw == overlay[CASE + 'finalized_current_01/payload/' + path] and pre[path] is None, 'Native packet exact accepted current bytes/new absence')
    passed('native22_103456_bytes_exact_accepted_finalized_packet_with_absent_native_preimages')
    package_pin = {'bytes': 1215, 'sha256': '35252843b8abb22d7abf3844f571f0239b23320118a802b5e9539a8be2933229'}
    proposal_pin = {'bytes': 485, 'sha256': '1aa225aa46e21f1a7b5aa391f1a18729ae37b2659bdb416f42b702c8d8a10b95'}
    check(pin(overlay[CASE + 'publication_package_v1/PACKAGE_SEAL.json']) == package_pin and pin(overlay[CASE + 'native_revision_preparation_01/SEAL.json']) == proposal_pin, 'Frozen science/proposal seals')
    check(pin(overlay[CASE + 'finalized_current_01/FINALIZATION_MANIFEST.json']) == {'bytes': 5121, 'sha256': '4bec7494322ab85caab606f6ba7db1f69adc213bf70d07624319a8fb168a3b7a'}, 'Accepted factual manifest')
    passed('frozen_helper_science_proposal_factual_packet_and_prior_audit_pins_preserved')
    helper.local_preimages(m, overlay)
    old = {path: source(C / path) for path in helper.VIEWS}
    for path in helper.VIEWS:
        check(pre[path] == ('100644', 'blob', core.native('blob', old[path])), 'Native old view tuple differs from actual local bytes')
    passed('all_five_live_local_preimages_and_native_old_blob_tuple_pins_exact')
    old_progress = helper.decode(old[helper.VIEWS[2]])
    new_progress = helper.decode(overlay[helper.VIEWS[2]])
    new_case = helper.decode(overlay[helper.VIEWS[0]])
    check(len(old_progress['fully_completed_eligible_PRs']) == 49 and new_progress['fully_completed_eligible_PRs'] == old_progress['fully_completed_eligible_PRs'], 'Prior completed IDs changed')
    check(len(old_progress['published_PRs']) == 33 and new_progress['published_PRs'] == old_progress['published_PRs'] + [207], 'Prior published IDs changed')
    check(new_progress['dated_eligible_total'] == old_progress['dated_eligible_total'] == 99 and new_progress['last_completed_DOI'] == old_progress['last_completed_DOI'], 'Denominator/last-completed DOI changed')
    passed('all_prior49_completed_and33_published_IDs_exact_only207_added_published')
    facts = helper.phase_facts('merge95')
    for obj in [new_progress, new_case]:
        helper.matches(obj, facts, 'Exact merge95 facts')
        check(obj['current_case_percent'] == 95 and obj['current_publication_ready'] is True and obj['completed'] is False and obj['goal_complete'] is False and obj['current_status'] == obj['status'] == 'published_tracked_native_merge_checkpoint_completion_pending', 'Current alias or status differs')
        check('publication_or_merge_or_new_intake_authorized' not in obj and obj['original_author_turns_and_model_effort_unverified'] is True and obj['novelty_or_firstness_or_independence_established'] is False, 'Stale combined authority or effort/novelty drift')
        for key in ['positive_theorem', 'alternative_reading_resolution', 'source_interpretation']:
            check(obj[key] == old_progress[key], 'Mathematical/source view text changed')
    passed('all_present_current_fact_status_ready_aliases_and_scientific_qualifiers_consistent')
    for path in [helper.VIEWS[1], helper.VIEWS[4]]:
        check(overlay[path].startswith(old[path]) and overlay[path].count(b'<!-- PR207_NATIVE_PHASE_FACTS ') == 1 and helper.marker(facts) in overlay[path].splitlines(), 'Historical log bytes or exact phase marker changed')
    check(helper.marker(facts) in overlay[helper.VIEWS[3]].splitlines(), 'Current progress MD marker')
    passed('three_exact_compact_phase_markers_and_both_prior_logs_byte_preserved')
    # Reconstruct the entire old native QUEUE and check the earlier Root full-body
    # digest, not merely the own-row cells or a flattened line count.
    queue_new = overlay[helper.QUEUE]
    lines = queue_new.splitlines(keepends=True)
    indices = [i for i, line in enumerate(lines) if b'| 5100044 / AMR-050-0044 |' in line]
    check(len(indices) == 1, 'Exactly one own QUEUE row')
    index = indices[0]
    queued = b'| 225 | 5100044 / AMR-050-0044 | Elliptic-billiard invariant k_{804,a} | 0.1905 | 5.0 | 3 | 2021 | queued | 0/5 |  |  |  |\n'
    old_lines = list(lines)
    old_lines[index] = queued
    queue_old = b''.join(old_lines)
    check(pin(queue_old) == {'bytes': 460099, 'sha256': 'b74ba8e66564f735e9f81dd651ebb3440de72cc2e27891b5e2f99754e2795fef'}, 'Whole fresh-MAIN QUEUE reconstruction differs')
    check(pre[helper.QUEUE] == ('100644', 'blob', core.native('blob', queue_old)) == ('100644', 'blob', '9a98632c02fd9039764f208839337194287e8830'), 'Fresh full QUEUE native preimage identity')
    helper.queue_change(queue_old, queue_new, 'merge95')
    check(b'https://doi.org/10.5281/zenodo.23428090' in lines[index] and b'10.5281/zenodo.23093706' in lines[index], 'Own publication/known-result DOI separation')
    passed('whole460099_byte_oldQUEUE_and_native_SHA_reconstructed_only_exact_own123_byte_row_changed')
    gate = helper.decode(overlay[m['gate_receipt']])
    for role, receipt in gate['receipts'].items():
        check(pin(overlay[receipt['path']]) == {k: receipt[k] for k in ('bytes', 'sha256')}, 'Actual role evidence binding')
    scientific = helper.decode(overlay[gate['receipts']['scientific']['path']])
    review_gate = helper.decode(overlay[gate['receipts']['whole_package_review']['path']])
    check(scientific['accepted_scoped_mathematics'] is True and review_gate['evidence_scope'] == 'ACTUAL_ROOT_RECEIPT' and review_gate['accepted'] is True and review_gate['required_repairs'] == [] and review_gate['new_distinct_reviewers'] == 2 and len(review_gate['whole_package_reviews']) == 2 and len({x['reviewer'] for x in review_gate['whole_package_reviews']}) == 2, 'Accepted distinct scientific/package roles')
    check(review_gate['package_seal'] == package_pin and review_gate['native_proposal_seal'] == proposal_pin and review_gate['mathematical_source_attribution_or_novelty_changes_since_reviews'] is False, 'Frozen reviewed scientific/native gate identity')
    for review in review_gate['whole_package_reviews']:
        for kind in ['event', 'report']:
            identity = review[kind]
            check(pin(overlay[CASE + identity['path']]) == {k: identity[k] for k in ('bytes', 'sha256')}, 'Actual review event/report pin')
    passed('scientific_acceptance_and_two_distinct_completed_Root_review_events_bound_to_frozen_package')
    ready_path = CASE + 'ROOT_ACTUAL_PR_READY_01.json'
    check(pin(overlay[ready_path]) == {'bytes': 2324, 'sha256': '7031be731dc4954aed2b1b68b73314f7c74eca4f980d3267905c03f186fbee84'}, 'Actual ready receipt')
    ready = helper.decode(overlay[ready_path])
    check(ready['evidence_scope'] == 'ACTUAL_ROOT_RECEIPT' and ready['accepted'] is True and ready['actual_PR_ready_for_review'] is True and ready['actual_draft'] is False and ready['actual_merged'] is False and ready['actual_state'] == 'open' and ready['actual_original_head'] == helper.HEAD and ready['actual_original_head_tree'] == helper.HEAD_TREE, 'Actual Root ready state')
    native_ready = helper.decode(overlay[CASE + 'root_pr_metadata_execution_01/READY_NATIVE_READBACK.json'])
    check(native_ready['head']['sha'] == helper.HEAD and native_ready['draft'] is False and native_ready['merged'] is False and native_ready['state'] == 'open' and native_ready['title'] == ready['actual_title'], 'Native ready readback state')
    check(native_ready['body'].encode() == overlay[CASE + 'finalized_current_01/FINAL_PR_BODY.md'] and pin(native_ready['body'].encode()) == ready['final_body_pin'], 'Exact final published PR body')
    passed('actual_role_gate_and_original_HEAD_open_ready_PR_native_readback_exact_body')
    changed_existing = sorted(path for path, raw in overlay.items() if pre[path] is not None and pre[path] != ('100644', 'blob', core.native('blob', raw)))
    check(set(changed_existing) == set(helper.VIEWS) | {helper.QUEUE}, 'Additional existing native path changed')
    passed('only_existing_native_changes_are_exact_five_views_and_ownQUEUE_blob')
    # Final fresh read-only check detects accidental own/shared changes during review.
    helper.local_preimages(m, overlay)
    source(B / 'MERGE95_INPUTS_01.json', MANIFEST_PIN)
    passed('manifest_and_five_live_preimages_still_stable_at_review_end')
    return dict(schema='pr207-independent-merge95-manifest-checks-v1', evidence_scope='READ_ONLY_EXACT_SOURCE_MANIFEST_REVIEW', status='CLEAN_SOURCE_MANIFEST_ONLY', manifest_pin=MANIFEST_PIN,
                selected_files=311, selected_bytes=2594743, check_count=len(checks), checks=checks,
                expected_parent=m['expected_parent'], Root_GET_parent_tree=summary['parent_tree'], facts=facts,
                new_selected_paths=sum(value is None for value in pre.values()), changed_existing_paths=changed_existing,
                own_QUEUE_row_index=index, old_QUEUE_pin=pin(queue_old), new_QUEUE_pin=pin(queue_new),
                prior_completed_IDs=old_progress['fully_completed_eligible_PRs'], prior_published_IDs=old_progress['published_PRs'],
                no_network_Git_native_mutation_or_local_source_write=True, actual_native_candidate_or_acceptance_verified=False)


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
