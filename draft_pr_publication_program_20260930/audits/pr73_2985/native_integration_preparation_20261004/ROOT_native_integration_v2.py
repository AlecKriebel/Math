#!/usr/bin/env python3
"""Sequential ROOT-only PR73 actions. This file's presence authorizes nothing.

Only structural-preflight may run during preparation. Execution requires a
fresh final ROOT gate, exact frozen plan, phase-specific actual writer window,
and the preceding independently read-back receipt. Failure never rolls back,
resets, stashes, force pushes, or claims that an incomplete phase succeeded.
"""
from native_common_v2 import *
import argparse

def structural_preflight():
    manifest, files, source = originals()
    source_identity = sourcepair(ROOT / 'unsolved_math_prioritization', source)
    # Schema/sample parsing is structural only. Samples must fail execution.
    for name in ('ROOT_GATE_SCHEMA_V2.json', 'FROZEN_PLAN_SCHEMA_V2.json', 'ROOT_GATE_TEMPLATE_V2.json', 'FROZEN_PLAN_TEMPLATE_V2.json'):
        load(PREP / name)
    rejected = False
    try:
        validate_gate(PREP / 'ROOT_GATE_TEMPLATE_V2.json')
    except RuntimeError:
        rejected = True
    require(rejected, 'Placeholder gate was accepted')
    result = {'status': 'PASS_STRUCTURAL_ONLY', 'UTC': now(), 'PR': PR, 'reviewed_head': HEAD,
              'original_attempt_files': len(files), 'incoming_paths': 20,
              'original_status_json': 'ABSENT', 'original_readiness_status': 'candidate_independently_reviewed',
              'original_substantive_attempts': 1, 'original_attempt_limit': 5, 'original_ledger_events': 1, 'original_turns': [1],
              'source_identity': source_identity, 'placeholder_gate_rejected': True,
              'scientific_outcome_selected': False, 'scope_interpretation_selected': False,
              'fresh_scientific_gate_present': False, 'execution_authorized': False,
              'proof_checkers_executed': False, 'shared_mutation_performed': False}
    print(json.dumps(result, indent=2))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase', choices=('structural-preflight', 'pr-metadata', 'merge', 'accept', 'checkpoint'))
    ap.add_argument('--gate')
    ap.add_argument('--predecessor')
    ap.add_argument('--writer-ack-nonce')
    ap.add_argument('--execute-root-reviewed', action='store_true')
    args = ap.parse_args()
    require(not sys.flags.optimize and sys.flags.ignore_environment and sys.flags.dont_write_bytecode, 'Invoke python3 -E -B without optimization')
    if args.phase == 'structural-preflight':
        require(not args.execute_root_reviewed and args.gate is None and args.predecessor is None and args.writer_ack_nonce is None, 'Structural preflight cannot confer execution authority')
        return structural_preflight()
    require(args.execute_root_reviewed and args.gate and args.writer_ack_nonce, 'Fresh ROOT authorization, gate and actual writer nonce are mandatory')
    g, plan, packet, science, gp = validate_gate(args.gate)
    m, files, source = originals()
    s = Session(args.phase, gp)
    base = current_baseline(s)
    expected_predecessor = {'merge': 'pr-metadata', 'accept': 'merge-readback', 'checkpoint': 'acceptance-readback'}
    prior = None
    if args.phase in expected_predecessor:
        require(args.predecessor, 'Sequential predecessor receipt is mandatory')
        prior = read_receipt(pin(Path(args.predecessor).resolve()), expected_predecessor[args.phase], gp)
    else:
        require(args.predecessor is None, 'Initial metadata phase has no predecessor')
    newer = prior['UTC'] if prior else g['UTC']
    owned = ({QUEUE} | {x['path'] for x in files}) if args.phase == 'merge' else (ACCEPT_PATHS if args.phase == 'accept' else set())
    if args.phase == 'checkpoint': owned = {r['pin']['path'] for r in plan['checkpoint_files']}
    w = WriterWindow(s, g, base, owned, newer, args.writer_ack_nonce)
    if prior:
        require(args.writer_ack_nonce != prior['actual_writer_ack_nonce'], 'New operational phase cannot reuse predecessor acknowledgment nonce')
    identity = verify_current_source(s, source)
    pr = s.pr()
    require(pr['title'] == plan['pr_title'] and pr['body'].encode() == packet['PR_BODY.md'] if args.phase != 'pr-metadata' else True, 'Reviewed final PR title/body differ')
    def stable():
        w.check()
        gg, pp, pk, ss, current_gp = validate_gate(args.gate)
        require(current_gp == gp and same(pp, plan) and pk == packet and same(ss, science), 'Gate/frozen packet/plan changed during phase')
        for row in identity['whole_current_source_pins']: check_pin(row)
    stable()
    if args.phase == 'pr-metadata':
        require(base == plan['expected_base_main'] and pr['state'] == 'OPEN' and pr['isDraft'] is True, 'Fresh open draft/current frozen base required')
        already = pr['title'] == plan['pr_title'] and pr['body'].encode() == packet['PR_BODY.md']
        if not already:
            require(pr['title'] == plan['submitted_pr_title'] and sha(pr['body'].encode()) == plan['submitted_pr_body_sha256'], 'Submitted PR title/body drifted')
            body_path = safe_path(next(r['path'] for r in plan['packet'] if Path(r['path']).name == 'PR_BODY.md'))
            stable()
            s.run(['gh', 'pr', 'edit', '73', '--repo', REPO, '--title', plan['pr_title'], '--body-file', str(body_path)])
        fresh = s.pr()
        require(fresh['state'] == 'OPEN' and fresh['isDraft'] is True and fresh['title'] == plan['pr_title'] and fresh['body'].encode() == packet['PR_BODY.md'], 'PR metadata readback differs')
        stable()
        s.finish({'current_commit': base, 'exact_plan': g['exact_plan'], 'PR_metadata_verified': True, 'idempotent_noop': already, 'native_merge_or_acceptance_done': False})
        return
    if args.phase == 'merge':
        require(base == plan['expected_base_main'] == prior['current_commit'] and pr['state'] == 'OPEN' and pr['isDraft'] is True, 'Exact frozen current base/open draft differs')
        merge_paths = {x['path'] for x in files} | {QUEUE}
        incoming = json.loads(s.run(['gh', 'api', 'repos/' + REPO + '/pulls/73/files?per_page=100'])[0])
        require(type(incoming) is list and len(incoming) == 20 and {r['filename'] for r in incoming} == merge_paths, 'Fresh incoming exact20 paths differ')
        _, available = s.run(['git', '--no-optional-locks', 'cat-file', '-e', HEAD + '^{commit}'], allowed=(0, 128))
        if available:
            stable()
            s.git('fetch', '--no-tags', '--no-write-fetch-head', 'origin', 'refs/pull/73/head')
            fresh = s.pr()
            require(fresh['state'] == 'OPEN' and fresh['isDraft'] is True and fresh['headRefOid'] == HEAD, 'Head drift during exact object import')
        check_original_git(s, HEAD, files)
        common = s.git('merge-base', base, HEAD).decode().strip()
        require(names0(s.git('diff', '--name-only', '-z', common, HEAD)) == merge_paths, 'Local exact incoming domain differs')
        require(all(not safe_path(x['path']).exists() and not safe_path(x['path']).is_symlink() for x in files), 'Target original destination exists; inspect rather than overwrite')
        require(not safe_path(PREFIX).exists(), 'Native target attempt directory already exists; preserve and stop before merge')
        before = safe_path(QUEUE).read_bytes()
        require(before == s.git('show', base + ':' + QUEUE), 'Current QUEUE is dirty; preserve it and stop for ROOT')
        require(stat.S_IMODE(safe_path(QUEUE).stat().st_mode) == 0o644 and s.git('ls-tree', base, '--', QUEUE).decode().split()[:3] == ['100644', 'blob', git_blob(before)], 'Current QUEUE worktree/Git mode differs')
        original_row = target_row(before)
        require(original_row.decode().split('|')[8].strip() == 'queued' and original_row.decode().split('|')[9].strip() == '0/5', 'Frozen current target baseline is not queued0/5')
        after_row = base64.b64decode(plan['queue_after_row_base64'], validate=True)
        after = before.replace(original_row, after_row, 1)
        check_queue_plan(before, after, plan)
        (s.dest / 'QUEUE_BEFORE.bin').write_bytes(before)
        (s.dest / 'QUEUE_AFTER.bin').write_bytes(after)
        stable()
        _, merge_exit = s.run(['git', '--no-optional-locks', 'merge', '--no-ff', '--no-commit', HEAD], allowed=(0, 1))
        conflicts = names0(s.git('diff', '--name-only', '--diff-filter=U', '-z'))
        mergehead = ROOT / '.git/MERGE_HEAD'
        require(conflicts <= {QUEUE} and mergehead.is_file() and mergehead.read_text().strip() == HEAD, 'Unexpected conflict/merge state')
        # Only the exact target row from the reviewed plan replaces current QUEUE.
        # Every other current row is retained from before, not from incoming QUEUE.
        w.restore_foreign_after_merge()
        safe_path(QUEUE).write_bytes(after)
        safe_path(QUEUE).chmod(0o644)
        check_original_git(s, HEAD, files, native=True)
        s.git('add', '--', QUEUE)
        require(not s.git('diff', '--name-only', '--diff-filter=U', '-z') and names0(s.git('diff', '--cached', '--name-only', '-z')) == merge_paths, 'Merge index scope differs')
        stable()
        s.git('commit', '-m', plan['merge_commit_message'])
        commit = s.git('rev-parse', 'HEAD').decode().strip()
        w.current = commit
        require(s.git('show', '-s', '--format=%P', commit).decode().split() == [base, HEAD] and names0(s.git('diff', '--name-only', '-z', base, commit)) == merge_paths, 'Exact two-parent merge/current-base domain differs')
        require(s.git('show', commit + ':' + QUEUE) == after and safe_path(QUEUE).read_bytes() == after, 'Merged QUEUE body differs')
        require(stat.S_IMODE(safe_path(QUEUE).stat().st_mode) == 0o644 and s.git('ls-tree', commit, '--', QUEUE).decode().split()[:3] == ['100644', 'blob', git_blob(after)], 'Merged QUEUE working/committed mode/blob differs')
        check_original_git(s, commit, files, native=True)
        stable()
        s.git('push', 'origin', 'main')
        require(s.git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit, 'Merge push readback differs')
        stable()
        s.finish({'base_main': base, 'merge_commit': commit, 'current_commit': commit, 'exact_plan': g['exact_plan'], 'merge_exit': merge_exit, 'conflicts': sorted(conflicts), 'original19_bytes_modes_blobs_preserved': True, 'native_acceptance_pending': True})
        return
    if args.phase == 'accept':
        merge = prior['merge_commit']
        require(pr['state'] == 'MERGED' and pr['mergeCommit']['oid'] == merge and pr['mergedAt'], 'Exact GitHub merged PR identity absent')
        require(s.git('show', '-s', '--format=%P', merge).decode().split() == [plan['expected_base_main'], HEAD], 'Exact two-parent merged origin differs')
        check_original_git(s, base, files, native=True)
        require(safe_path(QUEUE).read_bytes() == s.git('show', merge + ':' + QUEUE) and target_row(safe_path(QUEUE).read_bytes()) == base64.b64decode(plan['queue_after_row_base64'], validate=True), 'Merged target QUEUE differs')
        sb, hb = safe_path(STATE).read_bytes(), safe_path(HISTORY).read_bytes()
        sb_mode, hb_mode = safe_path(STATE).lstat().st_mode, safe_path(HISTORY).lstat().st_mode
        require(stat.S_IMODE(sb_mode) == stat.S_IMODE(hb_mode) == 0o644, 'Fresh current global modes differ from registered native modes')
        for rel, b in ((STATE, sb), (HISTORY, hb)):
            require(s.git('ls-tree', base, '--', rel).decode().split()[:3] == ['100644', 'blob', git_blob(b)], 'Fresh current global committed mode/blob differs')
        require(sb == s.git('show', base + ':' + STATE) and hb == s.git('show', base + ':' + HISTORY), 'Current globals are dirty; retain and stop for ROOT')
        state = load(safe_path(STATE))
        require(type(state) is dict, 'Fresh global state must be an unambiguous JSON object')
        eid = event_identity(gp, g['exact_plan'], merge, g['audited_outcome'])
        if ID in state:
            # Idempotency verifies the completed whole acceptance and never appends.
            from ROOT_native_readback_v2 import verify_acceptance
            accepted = verify_acceptance(s, g, plan, packet, science, gp, merge, base, files, identity)
            require(accepted['event_id'] == eid, 'Existing current import belongs to another gate/plan')
            stable()
            s.finish({'merge_commit': merge, 'acceptance_commit': base, 'current_commit': base, 'exact_plan': g['exact_plan'], 'event_id': eid, 'idempotent_noop': True})
            return
        require(base == merge == prior['current_commit'], 'Main moved after merge readback; fresh ROOT reconciliation required')
        require(not hb or hb.endswith(b'\n'), 'Current history has incomplete last record')
        require(all(str(json.loads(x).get('id')) != ID for x in hb.splitlines()), 'Current target history exists without target state')
        require(all(not safe_path(PREFIX + '/' + x).exists() for x in ('CURRENT_RESULT.md', 'CURRENT_PRIORITY.md', 'acceptance.json')), 'Separate native acceptance destination already exists')
        (s.dest / 'STATE_BEFORE.bin').write_bytes(sb)
        (s.dest / 'HISTORY_BEFORE.bin').write_bytes(hb)
        at = now()
        acceptance = {'schema': 'pr73-current-native-acceptance/v2', 'at': at, 'actual_controller_PID': os.getpid(), 'PR': PR, 'problem_id': ID,
                      'reviewed_head': HEAD, 'merge_commit': merge, 'merged_at': pr['mergedAt'], 'science': science,
                      'final_ROOT_gate': gp, 'frozen_exact_plan': g['exact_plan'], 'current_source_identity': identity, 'current_readiness_evidence': g['current_readiness_evidence'],
                      'original_attempt_file_count': 19, 'original_status_json': 'ABSENT', 'original_readiness_status': 'candidate_independently_reviewed',
                      'original_substantive_attempts': 1, 'original_attempt_limit': 5, 'original_turn_event_count': 1, 'original_turns': [1],
                      'new_original_proof_turns': 0, 'historical_transitions_reconstructed': False, 'present_day_import_event_id': eid,
                      'frozen_packet': plan['packet'], 'whole_original_attempt_preserved': True}
        stable()
        for name in ('CURRENT_RESULT.md', 'CURRENT_PRIORITY.md'):
            safe_path(PREFIX + '/' + name).write_bytes(packet[name]); safe_path(PREFIX + '/' + name).chmod(0o644)
        safe_path(PREFIX + '/acceptance.json').write_bytes(json_bytes(acceptance)); safe_path(PREFIX + '/acceptance.json').chmod(0o644)
        event = {'schema': 'pr73-present-day-native-import/v2', 'event': 'acceptance_mirror_import', 'event_id': eid, 'at': at,
                 'id': ID, 'pr': PR, 'status': g['audited_outcome'], 'turns_used': 1, 'turn_limit': 5,
                 'review_hash': identity['review_hash_SQL_normalized_only'], 'readiness_review_hash': identity['review_hash_SQL_normalized_only'], 'source_record_hash': identity['native_problem_hash'],
                 'source_report_hash': identity['native_report_hash'], 'statement_hash': identity['statement_hash'],
                 'note': target_row(safe_path(QUEUE).read_bytes()).decode().split('|')[11].strip(),
                 'evidence': {'canonical_acceptance': pin(safe_path(PREFIX + '/acceptance.json')), 'final_ROOT_gate': gp,
                              'frozen_exact_plan': g['exact_plan'], 'reviewed_head': HEAD, 'merge_commit': merge,
                              'current_readiness_evidence': g['current_readiness_evidence'],
                              'original_budget': '1/5', 'original_turn_event_count': 1, 'new_original_proof_turns': 0,
                              'historical_transitions_asserted': False, 'native_prior_present_null': True, 'raw_prior_absent': True, 'SQL_prior_empty_object': True}}
        expected_state = insert_state_key(sb, state, event)
        expected_history = hb + canonical(event).encode() + b'\n'
        require(safe_path(STATE).read_bytes() == sb and safe_path(HISTORY).read_bytes() == hb and safe_path(STATE).lstat().st_mode == sb_mode and safe_path(HISTORY).lstat().st_mode == hb_mode, 'Current global bytes/modes drifted before insertion; preserve and stop')
        safe_path(STATE).write_bytes(expected_state)
        safe_path(HISTORY).write_bytes(expected_history)
        require(safe_path(STATE).read_bytes() == expected_state and safe_path(HISTORY).read_bytes() == expected_history and safe_path(STATE).lstat().st_mode == sb_mode and safe_path(HISTORY).lstat().st_mode == hb_mode, 'Exact native import/state/history bytes/modes mismatch')
        check_original_git(s, merge, files, native=True)
        stable()
        s.git('add', '--', *sorted(ACCEPT_PATHS))
        require(names0(s.git('diff', '--cached', '--name-only', '-z')) == ACCEPT_PATHS, 'Acceptance scope must be exact five paths')
        stable()
        s.git('commit', '-m', plan['acceptance_commit_message'])
        commit = s.git('rev-parse', 'HEAD').decode().strip(); w.current = commit
        require(s.git('show', '-s', '--format=%P', commit).decode().split() == [merge] and names0(s.git('diff', '--name-only', '-z', merge, commit)) == ACCEPT_PATHS, 'Acceptance commit parent/scope differs')
        check_original_git(s, commit, files, native=True)
        from ROOT_native_readback_v2 import verify_acceptance
        verified = verify_acceptance(s, g, plan, packet, science, gp, merge, commit, files, identity)
        require(verified['event_id'] == eid and verified['acceptance']['merged_at'] == pr['mergedAt'], 'Complete acceptance verification failed before push')
        stable(); s.git('push', 'origin', 'main')
        require(s.git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit, 'Acceptance push readback differs')
        stable()
        s.finish({'merge_commit': merge, 'acceptance_commit': commit, 'current_commit': commit, 'exact_plan': g['exact_plan'], 'event_id': eid,
                  'one_present_day_import_event': True, 'original19_bytes_modes_blobs_preserved': True, 'idempotent_noop': False})
        return
    # Audit checkpoint follows independently verified scientific acceptance.
    require(base == prior['current_commit'], 'Main changed after acceptance readback')
    check_original_git(s, base, files, native=True)
    paths = {r['pin']['path'] for r in plan['checkpoint_files']}
    require(len(paths) == len(plan['checkpoint_files']), 'Duplicate public-safe checkpoint paths')
    native_before = {rel: pin(safe_path(rel)) for rel in ({QUEUE, STATE, HISTORY} | ACCEPT_PATHS)}
    stable(); s.git('add', '--', *sorted(paths))
    staged = names0(s.git('diff', '--cached', '--name-only', '-z'))
    require(staged and staged <= paths, 'Checkpoint staged domain exceeds reviewed public-safe allowlist or is empty')
    checkpoint_rows = {r['pin']['path']: r for r in plan['checkpoint_files']}
    for rel in staged:
        row = checkpoint_rows[rel]; b = s.git('show', ':' + rel)
        require(len(b) == row['pin']['bytes'] and sha(b) == row['pin']['sha256'], 'Checkpoint staged bytes differ from ROOT-reviewed exact pin')
        require(s.git('ls-files', '--stage', '--', rel).decode().split()[:3] == [row['git_mode'], git_blob(b), '0'], 'Checkpoint staged Git mode/blob differs')
        require(stat.S_IMODE(safe_path(rel).stat().st_mode) == (0o644 if row['git_mode'] == '100644' else 0o755), 'Checkpoint frozen worktree mode differs')
    stable()
    for rel, row in native_before.items(): require(pin(safe_path(rel)) == row, 'Checkpoint changed native acceptance')
    s.git('commit', '-m', plan['checkpoint_commit_message'])
    commit = s.git('rev-parse', 'HEAD').decode().strip(); w.current = commit
    require(s.git('show', '-s', '--format=%P', commit).decode().split() == [base] and names0(s.git('diff', '--name-only', '-z', base, commit)) == staged, 'Checkpoint exact parent/scope differs')
    for rel in staged:
        row = checkpoint_rows[rel]; b = s.git('show', commit + ':' + rel)
        require(len(b) == row['pin']['bytes'] and sha(b) == row['pin']['sha256'] and s.git('ls-tree', commit, '--', rel).decode().split()[:3] == [row['git_mode'], 'blob', git_blob(b)], 'Checkpoint committed body/mode/blob differs from frozen pin')
    stable(); s.git('push', 'origin', 'main')
    require(s.git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit, 'Checkpoint push readback differs')
    for rel, row in native_before.items(): require(pin(safe_path(rel)) == row, 'Checkpoint changed native acceptance')
    stable()
    s.finish({'checkpoint_commit': commit, 'current_commit': commit, 'scientific_acceptance_predecessor': pin(Path(args.predecessor).resolve()),
              'public_safe_paths': sorted(staged), 'raw_copyright_and_private_operational_data_excluded': True, 'native_acceptance_unchanged': True})

if __name__ == '__main__':
    main()
