#!/usr/bin/env python3
"""Prepared PR38 root-only preflight, overlay, prepush and finalize.

Never execute/import during preparation. Root separately marks the remote
ready, edits its body, merges ORIGINAL HEAD with --no-ff --no-commit, stages
only exact canonical/queue paths, commits, checks prepush, and pushes main.
This helper performs no Git mutation or remote write.
"""
import argparse
import copy
from pathlib import Path
import sys
# Future root entry points preserve every sealed source closure.
sys.dont_write_bytecode = True
import pr38_guards as g

BODY = '''# Accepted credited partial: complete KP-2.17 remains unsolved

For connected closed oriented genus>=2 surfaces, the credited partial gives
necessary measured-lamination tests, compact convex fiber, and simple-reference
rigidity. Finite periodic-orbit support and finite convex decomposition for an
arbitrary self-intersecting closed reference remain unproved. No classification
of extreme points, full solution or positive novelty is claimed.

The scaled nonatomic Liouville example concerns complete finite-area cusp
metrics and invariant positive Radon currents on S_0,3. It is separate from
the closed-surface problem and does not settle all complete-only metric
conventions. Finite support means finitely many closed-geodesic lift
orbits/periodic components. Noncompact intersection can be infinite; the local
finite-area normalization is i(L,L)=(pi/2)area=pi^2.

The entire current source-first review and actual v2 alias inspection passed.
The original root's 12 outer/108 nested closed-family executions, all raw
streams and complete comparisons remain bound. v2 restores the byte-exact
historical review/REVIEW.md alias and adds archival qualification only; it is
not a new scientific replay. RESULTS mathematics, original16 archives, all
1472 dependencies, full source and two original ledger rows remain unchanged.
The old review is dated scoped evidence, not a whole-current verdict.

Closed-surface intersection continuity and uniformization are cited standard
theorem inputs not independently recertified by the whole-current reviewer.
This qualification is not a mathematical defect or a new certification.
Current source/date/version limitations and the exact remaining gap are retained.
Historical null prior and empty importer fallback are not a retrieved separate
prior report. Historical worker/runtime metadata is archival; current model,
reasoning and deadline remain null. No original native event is reconstructed.

Original substantive2/5,new0/audit0. One present acceptance mirror only.
No paper, new DOI, tracker row, release or external human review is claimed.
No outside individual was contacted.

Original PR: https://github.com/AlecKriebel/Math/pull/38
Research/evidence anchor: draft_pr_publication_program_20260930/audits/pr38_2765
'''


def before_guard(pre):
    g.foreign_tracked_unchanged(pre)
    for key, suffix in [('state', '.json'), ('history', '.jsonl')]:
        path = g.R / 'unsolved_math_prioritization' / (key + suffix)
        g.require(g.sha(path.read_bytes()) == pre[key + '_before_sha256'], 'Shared preimage changed: ' + key)
    g.require(g.sha((g.B / 'inventory.json').read_bytes()) == pre['inventory_before_sha256'], 'Whole inventory changed since preflight')


def accepted_queue(pre, now):
    before = (g.A / 'integration_queue_before.md').read_bytes()
    g.require(g.sha(before) == pre['whole_queue_before_sha256'] and g.selected_row(before) == pre['selected_row_before'], 'Entire fresh queue preimage archive changed')
    fields = pre['selected_row_before'].split('|')
    after_fields = fields.copy()
    findings = now[:10] + ': Accepted credited closed genus>=2 necessary ML/compact-fiber/simple-reference partial; arbitrary self-intersecting reference unresolved. Separate finite-area cusped Radon S_0,3 example does not settle complete-only metrics. NEW whole current source-first/v2 alias inspection and original actual12/108 replay bound; continuity/uniformization unrecertified standard inputs, not a defect. Original2/5,new0/audit0; no paper/newDOI/tracker. https://github.com/AlecKriebel/Math/pull/38.'
    after_fields[8], after_fields[9], after_fields[11] = ' unsolved ', ' 2/5 ', ' ' + findings + ' '
    row = '|'.join(after_fields)
    g.require(len(fields) == len(after_fields) == 14 and all(fields[i] == after_fields[i] for i in range(14) if i not in {8, 9, 11}), 'Only named Status/Turns/Findings may change')
    g.require(before.count(pre['selected_row_before'].encode()) == 1, 'Full selected row must be unique')
    after = before.replace(pre['selected_row_before'].encode(), row.encode(), 1)
    g.require(after.count(row.encode()) == 1 and after.replace(row.encode(), pre['selected_row_before'].encode(), 1) == before, 'Preserve all other queue bytes, Chat and DOI')
    return before, after, row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['preflight', 'overlay', 'prepush', 'finalize'])
    parser.add_argument('--fresh-queue-preimage-sha256', help='Preflight: explicit root-reviewed COMPLETE fresh main queue SHA256')
    parser.add_argument('--merge-queue-preimage-sha256', help='Overlay: explicit root-reviewed automatic merged complete queue SHA256 before manual edit')
    g.add_gate_args(parser)
    args = parser.parse_args()
    frozen, pins = g.gates(args)
    observation, now = g.remote(), g.stamp()
    patch = g.load(g.C / 'CURRENT_QUEUE_PATCH.json')
    if args.phase == 'preflight':
        g.require(observation['state'] == 'OPEN' and observation['isDraft'] is True, 'Actual OPEN draft required')
        g.require(not g.K.exists() and g.K.name not in {p.name for p in g.K.parent.iterdir()}, 'Canonical attempt must be absent before merge')
        merge_head = Path(g.git('rev-parse', '--git-path', 'MERGE_HEAD'))
        if not merge_head.is_absolute():
            merge_head = g.R / merge_head
        g.require(not merge_head.exists() and not g.git('diff', '--cached', '--name-only'), 'No in-progress merge or staged bytes at preflight')
        foreign = g.capture_foreign_tracked_exclusions()
        queue = g.Q.read_bytes()
        g.require(args.fresh_queue_preimage_sha256 is not None and g.sha(queue) == g.digest(args.fresh_queue_preimage_sha256), 'Root must explicitly review and pin the entire fresh queue preimage')
        g.require(queue == g.git_bytes('show', 'HEAD:unsolved_math_prioritization/QUEUE.md'), 'Fresh main queue must be clean and tree-exact')
        row = g.selected_row(queue)
        g.require(row == patch['row_before'] and row.split('|')[8].strip() == 'queued' and row.split('|')[9].strip() == '0/5', 'Selected prior row changed; new source/queue review required')
        state = g.load(g.R / 'unsolved_math_prioritization/state.json')
        inventory = g.load(g.B / 'inventory.json')
        items = g.inventory_items(inventory)
        g.require(len(state) == 28 and g.ID not in state and sum(z['turns_used'] for z in state.values()) == 33, 'Require post-PR37 native28targets/33turns')
        g.require(sum(z.get('stage') == 'complete' for z in inventory['items']) == 27 and inventory['completed_count'] == 27, 'Require27 accepted primary PRs before PR38')
        g.require(g.PR in items and items[g.PR]['headRefOid'] == g.HEAD and items[g.PR]['headRefName'] == 'dot/math-' + g.ID and items[g.PR].get('stage') != 'complete', 'Current inventory PR38 original-head binding required')
        g.require(g.sha(g.PREVIOUS.read_bytes()) == g.PREVIOUS_SHA, 'Frozen accepted PR37 mirror base changed')
        pre = {'utc': now, **pins, 'pr': observation, 'main_before': g.git('rev-parse', 'HEAD'), 'foreign_tracked_exclusions': foreign,
               'whole_queue_before_sha256': g.sha(queue), 'root_explicit_fresh_queue_preimage_sha256': args.fresh_queue_preimage_sha256,
               'dated_queue_before_sha256': patch['whole_queue_preimage_sha256'], 'separately_reviewed_whole_queue_rebase': g.sha(queue) != patch['whole_queue_preimage_sha256'],
               'selected_row_before': row, 'state_before_sha256': g.sha((g.R / 'unsolved_math_prioritization/state.json').read_bytes()),
               'history_before_sha256': g.sha((g.R / 'unsolved_math_prioritization/history.jsonl').read_bytes()), 'inventory_before_sha256': g.sha((g.B / 'inventory.json').read_bytes()),
               'inventory_complete_ids': sorted(items), 'new_substantive_attempts': 0, 'attempts': '2/5', 'remote_pending': True}
        g.dump(g.A / 'integration_preflight.json', pre, exclusive=True)
        g.write(g.A / 'integration_queue_before.md', queue, exclusive=True)
        g.write(g.A / 'integration_inventory_before.json', (g.B / 'inventory.json').read_bytes(), exclusive=True)
        g.write(g.A / 'accepted_pr_body.md', BODY.encode(), exclusive=True)
        before_guard(pre)
        g.require(g.Q.read_bytes() == queue and g.git('rev-parse', 'HEAD') == pre['main_before'], 'Whole preimage changed during preflight')
        print('PREFLIGHT PASS PR38; root ready/body/original-head no-ff merge remain')
        return
    pre = g.load(g.A / 'integration_preflight.json')
    g.require(all(pre[key] == value for key, value in pins.items()), 'Final gates changed since preflight')
    before_guard(pre)
    g.require((g.A / 'accepted_pr_body.md').read_bytes() == BODY.encode(), 'Reviewed accepted body changed')
    before = (g.A / 'integration_queue_before.md').read_bytes()
    g.require(g.sha(before) == pre['whole_queue_before_sha256'] == pre['root_explicit_fresh_queue_preimage_sha256'], 'Whole root-reviewed queue preimage changed')
    if args.phase == 'overlay':
        g.require(observation['state'] == 'OPEN' and observation['isDraft'] is False and observation['body'] == BODY, 'Actual ready remote/body required')
        g.require(g.git('rev-parse', 'HEAD') == pre['main_before'] and g.git('rev-parse', 'MERGE_HEAD') == g.HEAD, 'Require in-progress original-head no-ff merge on exact captured main')
        queue_path = 'unsolved_math_prioritization/QUEUE.md'
        conflicts = set(g.git('diff', '--name-only', '--diff-filter=U').splitlines())
        g.require(conflicts <= {queue_path}, 'Unexpected conflict; retain and inspect')
        g.require(g.git_bytes('show', 'HEAD:' + queue_path) == before, 'Complete captured main queue differs')
        if conflicts:
            g.require(g.git_bytes('show', ':2:' + queue_path) == before and g.git_bytes('show', ':3:' + queue_path) == g.git_bytes('show', g.HEAD + ':' + queue_path), 'Actual conflict stages differ from captured main/original head')
        else:
            g.require(g.git_bytes('show', ':' + queue_path) == g.Q.read_bytes(), 'Automatic merge index/worktree queue differ')
        automatic = g.Q.read_bytes()
        g.require(args.merge_queue_preimage_sha256 is not None and g.sha(automatic) == g.digest(args.merge_queue_preimage_sha256), 'Explicit full automatic merge queue review/pin required')
        original_rows = g.load(g.A / 'snapshot_manifest.json')['files']
        g.exact_closure(g.K, {z['path'] for z in original_rows})
        for z in original_rows:
            g.require((g.K / z['path']).read_bytes() == (g.C / 'original_archive' / z['path']).read_bytes(), 'Merged exact original16 differs')
        outputs = {z['path']: (g.C / z['path']).read_bytes() for z in frozen}
        before, after, row = accepted_queue(pre, now)
        g.write(g.A / 'integration_merge_queue_before.md', automatic, exclusive=True)
        for name, raw in outputs.items():
            destination = g.K / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            g.write(destination, raw)
        archive = g.K / 'reviewed_pending_administration'
        archive.mkdir()
        for name in sorted(g.ADMIN):
            g.write(archive / name, outputs[name], exclusive=True)
        g.write(archive / 'MANIFEST.json', (g.C / 'MANIFEST.json').read_bytes(), exclusive=True)
        g.write(g.K / 'pr_body.md', BODY.encode())
        notice = (g.A / 'acceptance_preparation_family/alias_source_revision/ARCHIVAL_NOTICE_APPEND.txt').read_bytes()
        g.write(g.K / 'README.md', BODY.encode() + b'\nRESULTS.md is the byte-unchanged original partial. Exact original16 archives and pending administration are retained. Dependency paths resolve from the repository audit anchor. Actual merge and present acceptance are verified separately.\n' + notice)
        for name in ['readiness.json', 'status.json', 'attempt.json']:
            value = g.load(g.K / name)
            value.update(id=g.ID, problem_number=g.CODE, pr=g.PR, status='unsolved_accepted_partial_integration_pending_remote_verification', accepted_at_utc=now, queue_status='unsolved',
                current_gate='PASS_current_source_first_v2_alias_and_bound_original_actual_replay', current_workflow_completion_estimate_percent=100, full_resolution_completion_estimate_percent=0,
                full_target_completion_estimate_percent=0, full_resolution_claimed=False, novelty_claimed=False, full_problem_solved=False, positive_novelty_claim=False,
                paper_or_new_doi_or_tracker=False, source_record_sha256=g.SOURCE_SHA, original_turns_sha256=g.LEDGER_SHA, current_results_sha256=g.RESULTS_SHA,
                separate_prior_report_present=False, importer_empty_fallback_is_not_retrieved_report=True,
                original_authored_attempt_metadata=g.load(g.C / 'original_archive/attempt.json'),
                budget={'original_substantive_attempts': 2, 'used_substantive_attempts': 2, 'maximum_substantive_attempts': 5, 'cumulative_attempts': '2/5',
                        'new_substantive_attempts': 0, 'verification_attempts': 0, 'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'historical_only': True}, **pins)
            if name == 'readiness.json':
                value['independent_review'] = 'Entire current source-first review and actual v2 alias inspection passed; original actual12/108 replay remains bound. No v2 scientific rerun or standard-input recertification claimed.'
            g.dump(g.K / name, value)
        g.write(g.K / 'CURRENT_AUDIT_SCOPE.md', BODY.encode() + b'\nAll inherited current source qualifications and exact scientific scope are bound in SCIENTIFIC_SCOPE.json within the preparation and copied in acceptance metadata. Original16 archives and dated pending administrative bytes are preserved. Current runtime fields remain null.\n' + notice)
        note = '\n## ' + now + ' — Accepted current partial integration\n\nAcceptance workflow100%; actual remote pending. Full-resolution estimate0%; complete target unsolved. Original2/5,new0,audit0; mathematics/source/code/ledger/receipts unchanged; archival v2 alias only. No paper/newDOI/tracker/release.\n'
        g.write(g.K / 'RESEARCH_LOG.md', outputs['RESEARCH_LOG.md'] + note.encode())
        before_guard(pre)
        g.require(g.git('rev-parse', 'HEAD') == pre['main_before'] and g.git('rev-parse', 'MERGE_HEAD') == g.HEAD and g.Q.read_bytes() == automatic, 'Preimage changed during overlay')
        g.write(g.Q, after)
        g.dump(g.K / 'ACCEPTED_QUEUE_PATCH.json', {'utc': now, 'header_names': g.HEADER, 'column_count': 12, 'named_changes': ['Status', 'Turns', 'Findings'], 'whole_before_sha256': g.sha(before), 'whole_after_sha256': g.sha(after), 'row_before': pre['selected_row_before'], 'row_after': row, 'all_other_bytes_preserved': True, 'selected_chat_DOI_preserved': True, 'root_explicit_fresh_queue_preimage_sha256': pre['root_explicit_fresh_queue_preimage_sha256'], 'dated_prospective_patch_unchanged': True}, exclusive=True)
        g.canonical_unchanged(frozen)
        value = [{'path': name, 'bytes': len((g.K / name).read_bytes()), 'sha256': g.sha((g.K / name).read_bytes())} for name in sorted(g.canonical_names(frozen))]
        g.dump(g.A / 'integration_check.json', {'utc': now, **pins, 'pr': g.PR, 'original_head': g.HEAD, 'canonical_overlay_files': value, 'queue_before_sha256': g.sha(before), 'queue_after_sha256': g.sha(after), 'root_reviewed_automatic_merge_queue_preimage_sha256': g.sha(automatic), 'canonical_scientific_artifact_sha256': g.RESULTS_SHA, 'new_substantive_attempts': 0, 'attempts': '2/5', 'remote_pending': True}, exclusive=True)
        before_guard(pre)
        print('OVERLAY PASS PR38; root stages exact paths/commits then runs prepush')
        return
    overlay = g.load(g.A / 'integration_check.json')
    g.require(all(overlay[key] == value for key, value in pins.items()), 'Overlay/final pins differ')
    g.canonical_unchanged(frozen)
    qp = g.load(g.K / 'ACCEPTED_QUEUE_PATCH.json')
    queue = g.Q.read_bytes()
    g.require(before.replace(qp['row_before'].encode(), qp['row_after'].encode(), 1) == queue and queue.replace(qp['row_after'].encode(), qp['row_before'].encode(), 1) == before and g.sha(queue) == qp['whole_after_sha256'], 'Exact full queue Status/Turns/Findings replacement differs')
    if args.phase == 'prepush':
        g.require(observation['state'] == 'OPEN' and observation['isDraft'] is False and observation['body'] == BODY, 'Prepush requires exact ready remote')
        g.require(not g.git('diff', '--cached', '--name-only') and not g.git('diff', '--name-only', '--', 'unsolved_math_prioritization/QUEUE.md', str(g.K.relative_to(g.R))), 'Commit exact owned overlay first')
        merge = g.git('rev-parse', 'HEAD')
        tree = g.tree_binding(merge, pre, overlay, queue)
        g.dump(g.A / 'integration_prepush.json', {'utc': now, **pins, 'pr': g.PR, 'merge_commit': merge, 'merge_parents': [pre['main_before'], g.HEAD], 'merge_tree': tree, 'canonical_overlay_files': overlay['canonical_overlay_files'], 'whole_queue_after_sha256': g.sha(queue), 'foreign_tracked_exclusions': pre['foreign_tracked_exclusions'], 'remote_before_push': observation, 'actual_push_performed_by_helper': False}, exclusive=True)
        print('PREPUSH PASS PR38; exact real merge tree captured, root pushes main')
        return
    g.require(observation['state'] == 'MERGED' and observation['isDraft'] is False and observation['mergedAt'] and observation['body'] == BODY, 'Require actual GitHub MERGED/nondraft/date/body')
    merge = observation['mergeCommit']['oid']
    prepush = g.load(g.A / 'integration_prepush.json')
    g.require(all(prepush[key] == value for key, value in pins.items()) and prepush['merge_commit'] == merge and prepush['canonical_overlay_files'] == overlay['canonical_overlay_files'], 'Remote merge differs from prepush capture')
    tree = g.tree_binding(merge, pre, overlay, queue)
    g.require(tree == prepush['merge_tree'] and prepush['merge_parents'] == [pre['main_before'], g.HEAD], 'Actual published real merge tree/parents differ')
    names = {p.name for p in g.K.iterdir()}
    g.require('ACCEPTANCE.json' not in names and 'acceptance.json' not in names, 'Receipt must be new literal lowercase acceptance.json')
    inventory_before = g.load(g.A / 'integration_inventory_before.json')
    g.require(g.sha((g.B / 'inventory.json').read_bytes()) == pre['inventory_before_sha256'] and g.load(g.B / 'inventory.json') == inventory_before, 'Fresh complete inventory differs before finalization')
    inventory = copy.deepcopy(inventory_before)
    selected = g.inventory_items(inventory)[g.PR]
    selected.update(stage='complete', outcome='unsolved_accepted_partial', queue_status='unsolved', audited_head=g.HEAD, merge_commit=merge, merged_at=observation['mergedAt'], workflow_completion_estimate_percent=100, original_attempts='2/5', new_substantive_attempts=0, cumulative_attempts='2/5', paper_or_new_doi_or_tracker=False)
    g.unselected_inventory(inventory_before, inventory)
    done = sum(z.get('stage') == 'complete' for z in inventory['items'])
    g.require(done == 28, 'Expected28 accepted primaries after PR38')
    inventory.update(updated_at_utc=now, last_checkpoint_utc=now, completed_count=done, program_completion_estimate_percent=done / 180 * 100, completion_estimate_percent=done / 180 * 100, current_pr=39)
    g.dump(g.A / 'remote_merge_receipt.json', observation, exclusive=True)
    for name in ['readiness.json', 'status.json', 'attempt.json']:
        value = g.load(g.K / name)
        value.update(status='unsolved_accepted_partial_merged', remote_acceptance='MERGED_exact_original_head_parents_and_real_tree_verified', remote_merged_at=observation['mergedAt'], merge_commit=merge, merge_tree=tree)
        g.dump(g.K / name, value)
    g.write(g.K / 'RESEARCH_LOG.md', (g.K / 'RESEARCH_LOG.md').read_bytes() + ('\n## ' + now + ' — Actual remote acceptance verified\n\nAcceptance workflow100%; full-resolution estimate0%. Actual MERGED/nondraft/date/body and exact two-parent original-head merge/real tree checked against prepush capture. Present mirror pending. Original2/5,new0,audit0; no paper/newDOI/tracker/release.\n').encode())
    acceptance = {'schema': 'pr38-accepted-current-partial/v1', 'utc': now, **pins, 'pr': g.PR, 'id': int(g.ID), 'problem_id': int(g.ID), 'problem_number': g.CODE,
        'outcome': 'unsolved_accepted_partial_merged', 'queue_status': 'unsolved', 'full_problem_solved': False, 'positive_novelty_claim': False,
        'original_head': g.HEAD, 'original_base': g.ORIGINAL_BASE, 'merge_commit': merge, 'merge_parents': [pre['main_before'], g.HEAD], 'merge_tree': tree,
        'merged_at': observation['mergedAt'], 'remote_state': 'MERGED', 'remote_isDraft': False,
        'canonical_scientific_artifact_sha256': g.RESULTS_SHA, 'original_results_sha256': g.RESULTS_SHA, 'original_ledger_sha256': g.LEDGER_SHA,
        'source_record_sha256': g.SOURCE_SHA, 'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'substantive_attempts_used': 2,
        'substantive_attempt_limit': 5, 'verification_attempts_added': 0, 'paper_or_new_doi_or_tracker': False, 'human_peer_review_asserted': False,
        'workflow_completion_estimate_percent': 100, 'full_resolution_completion_estimate_percent': 0,
        'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'historical_metadata_archival_only': True,
        'separate_prior_report_present': False, 'importer_empty_fallback_is_not_retrieved_report': True, 'accepted_source_for_mirror': 'source_record.json',
        'current_mirror': 'One present acceptance, no reconstructed original native transition or extra proof turn.'}
    g.acceptance_invariants(acceptance, pins, pre)
    g.dump(g.K / 'acceptance.json', acceptance, exclusive=True)
    g.write(g.K / 'ACCEPTANCE.md', ('# Accepted UNSOLVED partial: 2765 / KP-2.17\n\n' + BODY + '\nActual original-head merge ' + merge + ', parents ' + ','.join(acceptance['merge_parents']) + ', tree ' + tree + '. Final source-first/v2 alias whole ' + pins['whole_manifest_sha256'] + '; actual evidence reconciliation ' + pins['root_final_receipt_sha256'] + '. Original actual12/108 replay, full source/null-prior qualification and exact two-row ledger remain bound. This is one present acceptance, no historical native reconstruction.\n').encode(), exclusive=True)
    g.exact_closure(g.K, g.canonical_names(frozen, True) - {'MANIFEST.json'})
    member_rows = [{'path': name, 'bytes': len((g.K / name).read_bytes()), 'sha256': g.sha((g.K / name).read_bytes())} for name in sorted(g.canonical_names(frozen, True) - {'MANIFEST.json'})]
    g.dump(g.K / 'MANIFEST.json', {'utc': now, 'schema': 'strict_self_excluding_accepted_packet_v1', 'self_excluded': ['MANIFEST.json'], 'files_count': len(member_rows), 'files': member_rows, 'foreign_scratch_excluded': [], 'scope': 'Accepted unsolved credited partial; original and pending bytes retained; no science edit.'}, exclusive=True)
    g.manifest(g.K, g.K / 'MANIFEST.json')
    g.canonical_unchanged(frozen, True)
    g.dump(g.A / 'acceptance.json', {**acceptance, 'canonical_manifest_sha256': g.sha((g.K / 'MANIFEST.json').read_bytes()), 'canonical_manifest_entries': len(member_rows)}, exclusive=True)
    g.acceptance_invariants(g.load(g.K / 'acceptance.json'), pins, pre)
    g.acceptance_invariants(g.load(g.A / 'acceptance.json'), pins, pre)
    g.require(g.strict_equal({key: value for key, value in g.load(g.A / 'acceptance.json').items() if key not in {'canonical_manifest_sha256', 'canonical_manifest_entries'}}, g.load(g.K / 'acceptance.json')), 'Final accepted copies differ in value/type')
    before_guard(pre)
    g.dump(g.B / 'inventory.json', inventory)
    g.unselected_inventory(inventory_before, g.load(g.B / 'inventory.json'))
    note = '\n## ' + now + ' — PR38 accepted and actually remotely merged\n\nAcceptance workflow100%; complete KP-2.17 unsolved, full-resolution estimate0%. Original2/5,new0,audit0; no paper/newDOI/tracker/release. Original head ' + g.HEAD + ', real merge ' + merge + '/tree ' + tree + '. Program28/180=' + str(round(done / 180 * 100, 4)) + '%; every unselected inventory item/hold preserved. Present mirror remains separate.\n'
    for path in [g.A / 'RESEARCH_LOG.md', g.B / 'RESEARCH_LOG.md']:
        g.write(path, path.read_bytes() + note.encode())
    g.foreign_tracked_unchanged(pre)
    print('FINALIZE PASS PR38; present acceptance mirror remains pending')


if __name__ == '__main__':
    g.run(main)
