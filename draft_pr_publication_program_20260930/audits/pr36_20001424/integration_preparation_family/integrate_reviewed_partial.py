#!/usr/bin/env python3
"""Future root-only PR36 preflight/overlay/finalize; never invoked in preparation.

Root separately edits the remote body, marks ready, performs a no-ff exact-head
merge and pushes. This helper only verifies those operations and writes guarded
administrative acceptance files. No Git mutation or remote write is implemented.
"""
import argparse
from pathlib import Path
import pr36_guards as g

BODY = '''# Accepted credited prior application: PCF descent

The full question “Are all PCF maps defined over their field of moduli?” has a
negative answer by the printed cubic i((z-1)/(z+1))^3 in Joseph H. Silverman,
The field of definition for dynamical systems on P1, Compositio Mathematica98
(1995),269–304, printed p.271 equation(1), with the odd-degree obstruction
on pp.296–297. Exact elementary verification gives critical points1 and-1
on the six-cycle1→0→-i→-1→infinity→i→1, absolute field of moduli Q, trivial
holomorphic automorphisms and no real model, hence no Q-model. The source
prints the map and descent assertions; this audit proves its PCF property.

Disposition already_solved; credited PRIOR_APPLICATION. Earliest worldwide
recognition of this PCF consequence and priority of the separately verified
original degree11 critically fixed graph are unestablished. Every original
scientific/source/ledger/review byte is preserved. The original graph proof
does not supply computed exact coefficients or an exact moduli field.

A NEW complete current-packet source-first adversary and actual final root
reproduction have passed; their exact manifests and receipt are bound in
the canonical acceptance. Earlier individual-family verdicts do not transfer.
Original substantive1/5, new0, verification0. No paper, new DOI, tracker row or
GitHub release. Extensive AI use is unrefereed; no external human peer review
or formal proof-assistant certification is claimed.

Primary source: https://www.numdam.org/item/CM_1995__98_3_269_0/
Literal question: http://aimpl.org/finitedynamics/2/
Original PR: https://github.com/AlecKriebel/Math/pull/36
'''

def unchanged(frozen, administration_archived=False):
    for z in frozen:
        prefix = 'reviewed_pending_administration' if administration_archived and z['path'] in g.ADMIN else ''
        p = g.K / prefix / z['path']
        g.require(p.read_bytes() == (g.C / z['path']).read_bytes(), 'Canonical reviewed bytes changed: ' + z['path'])

def before_guard(pre):
    for key, suffix in [('state', '.json'), ('history', '.jsonl')]:
        p = g.R / 'unsolved_math_prioritization' / (key + suffix)
        g.require(g.sha(p.read_bytes()) == pre[key + '_before_sha256'], 'Shared ' + key + ' changed since preflight')
    g.require(g.sha((g.B / 'inventory.json').read_bytes()) == pre['inventory_before_sha256'], 'Inventory changed since preflight')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['preflight', 'overlay', 'finalize'])
    parser.add_argument('--allow-named-row-rebase', action='store_true', help='Explicit root approval of a separately receipted live whole-preimage rebase when only unrelated queue bytes changed')
    parser.add_argument('--merge-queue-preimage-sha256', help='Overlay only: root-reviewed exact automatic merged working queue, captured before any manual edit')
    g.add_gate_args(parser)
    args = parser.parse_args()
    frozen, pins = g.gates(args)
    observation = g.remote()
    patch = g.load(g.C / 'CURRENT_QUEUE_PATCH.json')
    now = g.stamp()
    if args.phase == 'preflight':
        g.require(observation['state'] == 'OPEN' and observation['isDraft'] is True, 'Preflight requires actual OPEN draft')
        g.require(not g.K.exists(), 'Canonical attempt already exists')
        merge_head = Path(g.git('rev-parse', '--git-path', 'MERGE_HEAD'))
        if not merge_head.is_absolute():
            merge_head = g.R / merge_head
        g.require(not merge_head.exists() and not g.git('diff', '--cached', '--name-only'), 'Index/merge must be clean before root integration')
        g.require(not g.git('diff', '--name-only'), 'Checkpoint tracked changes before capturing preflight')
        q = g.Q.read_bytes()
        g.require(g.git_bytes('show', 'HEAD:unsolved_math_prioritization/QUEUE.md') == q, 'Captured current queue must equal clean captured main tree')
        row = g.selected_row(q)
        g.require(row == patch['row_before'] and row.split('|')[8].strip() == 'queued' and row.split('|')[9].strip() == '0/5', 'Selected current row changed; new reviewed rebase required')
        rebased = g.sha(q) != patch['whole_queue_preimage_sha256']
        g.require(not rebased or args.allow_named_row_rebase, 'Live queue differs from dated snapshot; explicit root named-row rebase required')
        state = g.load(g.R / 'unsolved_math_prioritization/state.json')
        inventory = g.load(g.B / 'inventory.json')
        g.require(len(state) == 26 and g.ID not in state and sum(x['turns_used'] for x in state.values()) == 31, 'Require post-PR35 mirror26/31')
        g.require(sum(x.get('stage') == 'complete' for x in inventory['items']) == 25, 'Require25 accepted primaries before PR36')
        g.dump(g.A / 'integration_preflight.json', {'utc': now, **pins, 'pr': observation, 'main_before': g.git('rev-parse', 'HEAD'), 'whole_queue_before_sha256': g.sha(q), 'dated_queue_before_sha256': patch['whole_queue_preimage_sha256'], 'separately_reviewed_named_row_rebase': rebased, 'selected_row_before': row, 'state_before_sha256': g.sha((g.R / 'unsolved_math_prioritization/state.json').read_bytes()), 'history_before_sha256': g.sha((g.R / 'unsolved_math_prioritization/history.jsonl').read_bytes()), 'inventory_before_sha256': g.sha((g.B / 'inventory.json').read_bytes()), 'new_substantive_attempts': 0, 'attempts': '1/5', 'remote_pending': True}, exclusive=True)
        g.write(g.A / 'integration_queue_before.md', q, exclusive=True)
        g.write(g.A / 'integration_inventory_before.json', (g.B / 'inventory.json').read_bytes(), exclusive=True)
        g.write(g.A / 'accepted_pr_body.md', BODY.encode(), exclusive=True)
        print('PREFLIGHT PASS PR36; root remote-ready/body and guarded no-ff merge remain')
        return
    pre = g.load(g.A / 'integration_preflight.json')
    g.require(all(pre[k] == v for k, v in pins.items()), 'Final gate changed since preflight')
    before_guard(pre)
    q = (g.A / 'integration_queue_before.md').read_bytes()
    g.require(g.sha(q) == pre['whole_queue_before_sha256'] and g.selected_row(q) == pre['selected_row_before'], 'Captured full current queue preimage altered')
    g.require((g.A / 'accepted_pr_body.md').read_bytes() == BODY.encode(), 'Reviewed acceptance body altered')
    if args.phase == 'overlay':
        g.require(observation['state'] == 'OPEN' and observation['isDraft'] is False and observation['body'] == BODY, 'Remote must be OPEN ready with exact reviewed body')
        g.require(g.git('rev-parse', 'MERGE_HEAD') == g.HEAD and g.git('rev-parse', 'HEAD') == pre['main_before'], 'Require original-head in-progress no-ff merge on captured main')
        conflicts = set(g.git('diff', '--name-only', '--diff-filter=U').splitlines())
        g.require(conflicts <= {'unsolved_math_prioritization/QUEUE.md'}, 'Unexpected conflict; retain and inspect')
        queue_path = 'unsolved_math_prioritization/QUEUE.md'
        g.require(g.git_bytes('show', 'HEAD:' + queue_path) == q, 'Actual captured main queue differs from full preflight preimage')
        if queue_path in conflicts:
            g.require(g.git_bytes('show', ':2:' + queue_path) == q and g.git_bytes('show', ':3:' + queue_path) == g.git_bytes('show', g.HEAD + ':' + queue_path), 'Conflicted queue stages differ from actual captured main/original head')
        else:
            g.require(g.git_bytes('show', ':' + queue_path) == g.Q.read_bytes(), 'Unconflicted working queue differs from automatic merge index')
        g.require(args.merge_queue_preimage_sha256 is not None and len(args.merge_queue_preimage_sha256) == 64 and all(x in '0123456789abcdef' for x in args.merge_queue_preimage_sha256), 'Overlay requires explicit root-reviewed automatic merged queue SHA256')
        merged_queue = g.Q.read_bytes()
        g.require(g.sha(merged_queue) == args.merge_queue_preimage_sha256, 'Automatic merged working queue changed after root preimage review')
        sm = g.load(g.A / 'snapshot_manifest.json')
        originals = {z['path'] for z in sm['files']}
        g.require({str(p.relative_to(g.K)) for p in g.K.rglob('*') if p.is_file()} == originals, 'Canonical tree must be exact merged original16 before overlay')
        for z in sm['files']:
            g.require((g.K / z['path']).read_bytes() == (g.C / 'original_archive' / z['path']).read_bytes(), 'Merged original byte mismatch')
        g.require(not (g.K / 'reviewed_pending_administration').exists(), 'Inspect existing pending archive before retry')
        g.write(g.A / 'integration_merge_queue_before.md', merged_queue, exclusive=True)
        # All output bytes are prepared before writing. Never edit source/science.
        outputs = {z['path']: (g.C / z['path']).read_bytes() for z in frozen}
        g.require(originals <= set(outputs), 'No original top-level deletion is implemented')
        for rel, raw in outputs.items():
            destination = g.K / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            g.write(destination, raw)
        unchanged(frozen)
        archive = g.K / 'reviewed_pending_administration'
        archive.mkdir()
        for rel in sorted(g.ADMIN):
            g.write(archive / rel, outputs[rel], exclusive=True)
        g.write(archive / 'MANIFEST.json', (g.C / 'MANIFEST.json').read_bytes(), exclusive=True)
        # The exact pending source/root/family scope statements remain immutable.
        g.write(g.K / 'pr_body.md', BODY.encode())
        g.write(g.K / 'README.md', (BODY + '\nThe complete current science is CURRENT_UNIVERSAL_CERTIFICATE.md. CANDIDATE.md remains the exact historical original graph. Dependency paths resolve from repository audit anchor ' + str(g.A.relative_to(g.R)) + ', including after canonical copying. Original archives and reviewed_pending_administration preserve dated pending scopes exactly. Actual canonical acceptance, merge and current mirror are separately recorded.\n').encode())
        for rel in ['readiness.json', 'status.json']:
            value = g.load(g.K / rel)
            value.update(accepted_at_utc=now, queue_status='already_solved', current_gate='PASS_NEW_complete_source_first_and_actual_root_reproduction', current_workflow_completion_estimate_percent=100, **pins)
            value['status'] = 'already_solved_accepted_partial_integration_pending_remote_verification'
            if rel == 'readiness.json':
                value['independent_review'] = 'NEW complete current-packet source-first adversary and actual final root reproduction passed; explicit receipt pins recorded.'
            g.dump(g.K / rel, value)
        g.write(g.K / 'CURRENT_AUDIT_SCOPE.md', ('# Accepted current scope\n\nPR36 ' + g.ID + ' already_solved credited PRIOR_APPLICATION. The NEW entire current-packet source-first gate and actual root reproduction passed, bound by ' + pins['whole_manifest_sha256'] + ' and ' + pins['root_final_receipt_sha256'] + '. All scientific/raw-source/prior-report/dependency/original-ledger bytes are unchanged. Exact root priority decision and earlier pending statements remain dated historical evidence. Original1/5,new0,verification0; no paper/newDOI/tracker/release. Canonical merge, acceptance and current mirror are separately verified.\n').encode())
        note = '\n## ' + now + ' — Accepted complete-gate partial integration\n\nWorkflow100% for scientific/current-gate validation; actual remote acceptance still pending. Credited PRIOR_APPLICATION already_solved; original1/5,new0,verification0. Science/source/prior/dependencies/entire original ledger unchanged, pending administration archived. No paper/newDOI/tracker/release.\n'
        g.write(g.K / 'RESEARCH_LOG.md', outputs['RESEARCH_LOG.md'] + note.encode())
        fields = pre['selected_row_before'].split('|')
        accepted = fields.copy()
        findings = now[:10] + ': Accepted credited PRIOR_APPLICATION: Silverman1995 printed cubic i((z-1)/(z+1))^3 is exactly PCF with absolute field of moduli Q and no real/Q model; full universal negative answer is a verified source consequence. Original degree11 graph valid/preserved, narrower priority unestablished. NEW entire current source-first gate and actual root reproduction passed. Original1/5,new0/verification0; no paper/newDOI/tracker. PR: https://github.com/AlecKriebel/Math/pull/36.'
        accepted[8], accepted[9], accepted[11] = ' already_solved ', ' 1/5 ', ' ' + findings + ' '
        row = '|'.join(accepted)
        g.require(len(fields) == len(accepted) == 14 and all(fields[i] == accepted[i] for i in range(14) if i not in {8, 9, 11}), 'Only named Status/Turns/Findings may change')
        g.require(q.count(pre['selected_row_before'].encode()) == 1, 'Unique full-row preimage required')
        after = q.replace(pre['selected_row_before'].encode(), row.encode(), 1)
        g.require(after.count(row.encode()) == 1 and after.replace(row.encode(), pre['selected_row_before'].encode(), 1) == q, 'All other current queue bytes must survive')
        before_guard(pre)
        g.require(g.git('rev-parse', 'HEAD') == pre['main_before'] and g.git('rev-parse', 'MERGE_HEAD') == g.HEAD and g.Q.read_bytes() == merged_queue, 'Queue/head/state preimage changed during overlay; preserve and inspect')
        g.write(g.Q, after)
        g.dump(g.K / 'ACCEPTED_QUEUE_PATCH.json', {'utc': now, 'header_names': g.HEADER, 'column_count': 12, 'named_changes': ['Status', 'Turns', 'Findings'], 'whole_before_sha256': g.sha(q), 'whole_after_sha256': g.sha(after), 'row_before': pre['selected_row_before'], 'row_after': row, 'all_other_bytes_preserved': True, 'dated_prospective_patch_unchanged': True, 'selected_chat_DOI_preserved': True}, exclusive=True)
        unchanged(frozen, True)
        before_guard(pre)
        tree_rows = [{'path': str(p.relative_to(g.K)), 'bytes': len(p.read_bytes()), 'sha256': g.sha(p.read_bytes())} for p in sorted(g.K.rglob('*')) if p.is_file()]
        g.require(not any(p.is_symlink() for p in g.K.rglob('*')), 'Canonical overlay must contain no symlinks')
        g.dump(g.A / 'integration_check.json', {'utc': now, **pins, 'pr': g.PR, 'original_head': g.HEAD, 'queue_before_sha256': g.sha(q), 'queue_after_sha256': g.sha(after), 'root_reviewed_automatic_merge_queue_preimage_sha256': g.sha(merged_queue), 'canonical_overlay_files': tree_rows, 'science_source_dependency_ledger_bytes_unchanged': True, 'reviewed_pending_administration_archived': True, 'canonical_scientific_artifact_sha256': g.sha((g.K / 'CURRENT_UNIVERSAL_CERTIFICATE.md').read_bytes()), 'new_substantive_attempts': 0, 'attempts': '1/5', 'remote_pending': True}, exclusive=True)
        print('OVERLAY PASS PR36; root must commit guarded no-ff merge and push')
        return
    g.require(observation['state'] == 'MERGED' and observation['isDraft'] is False and observation['mergedAt'] and observation['body'] == BODY, 'Actual remote MERGED/date/body required')
    merge = observation['mergeCommit']['oid']
    parents = g.git('show', '-s', '--format=%P', merge).split()
    g.require(parents == [pre['main_before'], g.HEAD], 'Require actual two-parent captured-main/original-head merge')
    g.git_bytes('merge-base', '--is-ancestor', merge, 'HEAD')
    for key, suffix in [('state', '.json'), ('history', '.jsonl')]:
        g.require(g.sha(g.git_bytes('show', merge + ':unsolved_math_prioritization/' + key + suffix)) == pre[key + '_before_sha256'], 'Merge must preserve actual old shared state/history')
    unchanged(frozen, True)
    qp = g.load(g.K / 'ACCEPTED_QUEUE_PATCH.json')
    g.require(g.Q.read_bytes() == q.replace(qp['row_before'].encode(), qp['row_after'].encode(), 1) and g.sha(g.Q.read_bytes()) == qp['whole_after_sha256'], 'Actual queue differs from exact current-preimage named patch')
    overlay = g.load(g.A / 'integration_check.json')
    g.require(all(overlay[k] == v for k, v in pins.items()), 'Committed overlay gate pins differ')
    g.merged_overlay_tree(merge, overlay, g.Q.read_bytes())
    for z in overlay['canonical_overlay_files']:
        g.require(g.sha((g.K / z['path']).read_bytes()) == z['sha256'], 'Local committed overlay changed before final acceptance: ' + z['path'])
    g.require(not (g.K / 'ACCEPTANCE.json').exists(), 'Canonical receipt is lowercase acceptance.json only')
    g.dump(g.A / 'remote_merge_receipt.json', observation, exclusive=True)
    for rel in ['readiness.json', 'status.json']:
        value = g.load(g.K / rel)
        value.update(status='already_solved_accepted_partial_merged', remote_acceptance='MERGED_exact_original_head_and_parents_verified', remote_merged_at=observation['mergedAt'], merge_commit=merge, current_workflow_completion_estimate_percent=100)
        g.dump(g.K / rel, value)
    g.write(g.K / 'RESEARCH_LOG.md', (g.K / 'RESEARCH_LOG.md').read_bytes() + ('\n## ' + now + ' — Actual remote acceptance verified\n\nWorkflow100%. GitHub MERGED/nondraft/date/body and exact two-parent no-ff merge independently verified; original1/5,new0,verification0. Present source-bound state mirror remains a separate administrative step. No paper/newDOI/tracker/release.\n').encode())
    acceptance = {'utc': now, **pins, 'pr': g.PR, 'id': int(g.ID), 'problem_id': int(g.ID), 'problem_number': g.CODE, 'outcome': 'already_solved_accepted_partial_merged', 'queue_status': 'already_solved', 'priority_classification': 'PRIOR_APPLICATION', 'original_head': g.HEAD, 'original_base': g.ORIGINAL_BASE, 'merge_commit': merge, 'merge_parents': parents, 'merged_at': observation['mergedAt'], 'remote_state': 'MERGED', 'remote_isDraft': False, 'canonical_scientific_artifact_sha256': g.sha((g.K / 'CURRENT_UNIVERSAL_CERTIFICATE.md').read_bytes()), 'original_graph_candidate_sha256': g.sha((g.K / 'CANDIDATE.md').read_bytes()), 'original_ledger_sha256': g.LEDGER_SHA, 'original_substantive_attempts': 1, 'new_substantive_attempts': 0, 'substantive_attempts_used': 1, 'substantive_attempt_limit': 5, 'verification_attempts_added': 0, 'positive_novelty_claim': False, 'narrow_degree11_priority_verified': False, 'paper_or_new_doi_or_tracker': False, 'human_peer_review_asserted': False, 'workflow_completion_estimate_percent': 100, 'accepted_source_for_mirror': 'problem.json', 'current_mirror': 'Separate present-day source-bound acceptance only; original ledger and prior history prefix preserved.'}
    g.dump(g.K / 'acceptance.json', acceptance, exclusive=True)
    text = '# Accepted ALREADY_SOLVED partial: ' + g.ID + '\n\nOriginal head ' + g.HEAD + ' merged on main as ' + merge + ' with exact parents ' + ','.join(parents) + '. Actual remote MERGED/nondraft/date/body independently checked. The full raw accepted_source is problem.json; exact nested source_record.json and complete prior_report.json remain preserved.\n\n' + BODY + '\nAll current scientific/source/prior/dependency/original ledger bytes remain exact. Reviewed pending administration and its self-excluding manifest are archived. Dependency paths resolve from repository audit anchor ' + str(g.A.relative_to(g.R)) + '. Final new whole gate ' + pins['whole_manifest_sha256'] + ', actual root receipt ' + pins['root_final_receipt_sha256'] + '. Root/family interim statements and failed controls retain their exact dates and scope. CURRENT_QUEUE_PATCH.json is the dated prospective snapshot; ACCEPTED_QUEUE_PATCH.json proves the actual named-row replacement. Current mirror is a single present acceptance, with no invented historical proof transition or research turn.\n'
    g.write(g.K / 'ACCEPTANCE.md', text.encode(), exclusive=True)
    rows = [{'path': str(p.relative_to(g.K)), 'bytes': len(p.read_bytes()), 'sha256': g.sha(p.read_bytes())} for p in sorted(g.K.rglob('*')) if p.is_file() and p != g.K / 'MANIFEST.json']
    g.dump(g.K / 'MANIFEST.json', {'utc': now, 'schema': 'strict_self_excluding_accepted_packet_v1', 'self_excluded': ['MANIFEST.json'], 'files_count': len(rows), 'files': rows, 'scope': 'Canonical accepted credited partial; all original and reviewed pending bytes retained; no scientific edit.'})
    g.manifest(g.K, g.K / 'MANIFEST.json')
    g.dump(g.A / 'acceptance.json', {**acceptance, 'canonical_manifest_sha256': g.sha((g.K / 'MANIFEST.json').read_bytes()), 'canonical_manifest_entries': len(rows)}, exclusive=True)
    inventory = g.load(g.A / 'integration_inventory_before.json')
    selected = [x for x in inventory['items'] if x['number'] == g.PR]
    g.require(len(selected) == 1 and selected[0]['headRefOid'] == g.HEAD and selected[0]['headRefName'] == 'dot/math-' + g.ID, 'Wrong current inventory PR36 binding')
    selected[0].update(stage='complete', outcome='already_solved_accepted_partial', queue_status='already_solved', audited_head=g.HEAD, merge_commit=merge, merged_at=observation['mergedAt'], workflow_completion_estimate_percent=100, original_attempts='1/5', new_substantive_attempts=0, cumulative_attempts='1/5', paper_or_new_doi_or_tracker=False)
    done = sum(x.get('stage') == 'complete' for x in inventory['items'])
    g.require(done == 26, 'Expected26 accepted primaries after PR36')
    inventory.update(updated_at_utc=now, last_checkpoint_utc=now, completed_count=done, program_completion_estimate_percent=done / 180 * 100, completion_estimate_percent=done / 180 * 100, current_pr=37)
    g.dump(g.B / 'inventory.json', inventory)
    note = '\n## ' + now + ' — PR36 accepted and remotely merged\n\nWorkflow100%: credited already_solved PRIOR_APPLICATION, original1/5,new0,verification0; no paper/newDOI/tracker/release. Exact original head ' + g.HEAD + ', actual merge ' + merge + '; NEW complete current-packet source-first gate and actual root final reproduction passed. Original/science/source/dependencies/ledger preserved. Program26/180=' + str(round(done / 180 * 100, 4)) + '%; other items and holds preserved. Present acceptance mirror follows source/remote/package verification.\n'
    for p in [g.A / 'RESEARCH_LOG.md', g.B / 'RESEARCH_LOG.md']:
        g.write(p, p.read_bytes() + note.encode())
    print('FINALIZE PASS PR36; present mirror still pending')

if __name__ == '__main__':
    g.run(main)
