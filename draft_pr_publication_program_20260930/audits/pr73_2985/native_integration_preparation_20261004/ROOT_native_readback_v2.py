#!/usr/bin/env python3
"""Fresh sequential readback. This never merges, edits a PR, or accepts a result."""
from native_common_v2 import *
import argparse

def preserved_single_insertion(before, after):
    """Recover all prior object bytes by removing one added member, independently."""
    require(len(after) > len(before), 'State object did not gain one member')
    left = 0
    while left < len(before) and before[left] == after[left]: left += 1
    right = 0
    while right < len(before) - left and before[-right-1] == after[-right-1]: right += 1
    require(left + right == len(before), 'Foreign state bytes were rewritten')
    added = after[left:len(after)-right if right else len(after)]
    require(after[:left] + after[len(after)-right if right else len(after):] == before, 'Prior state byte recovery differs')
    member = added.strip()
    if member.startswith(b','): member = member[1:].lstrip()
    require(type(json.loads(b'{' + member + b'}')) is dict and set(json.loads(b'{' + member + b'}')) == {ID}, 'State insertion contains foreign keys')

def verify_acceptance(s, g, plan, packet, science, gp, merge, current, files, identity):
    require(s.git('show', '-s', '--format=%P', current).decode().split() == [merge], 'Acceptance must be a separate single-parent commit after merge')
    require(names0(s.git('diff', '--name-only', '-z', merge, current)) == ACCEPT_PATHS, 'Acceptance must change exact five native paths')
    for rel in ACCEPT_PATHS:
        b = safe_path(rel).read_bytes()
        require(b == s.git('show', current + ':' + rel), 'Native acceptance body differs from committed current body')
        require(stat.S_IMODE(safe_path(rel).stat().st_mode) == 0o644, 'Native acceptance filesystem mode differs')
        require(s.git('ls-tree', current, '--', rel).decode().split()[:3] == ['100644', 'blob', git_blob(b)], 'Native acceptance committed Git mode/blob differs')
    for name in ('CURRENT_RESULT.md', 'CURRENT_PRIORITY.md'):
        require(safe_path(PREFIX + '/' + name).read_bytes() == packet[name], 'Native current report differs from reviewed exact packet')
    a = load(safe_path(PREFIX + '/acceptance.json'))
    fields(a, ('schema', 'at', 'actual_controller_PID', 'PR', 'problem_id', 'reviewed_head', 'merge_commit', 'merged_at', 'science',
               'final_ROOT_gate', 'frozen_exact_plan', 'current_source_identity', 'current_readiness_evidence', 'original_attempt_file_count', 'original_status_json',
               'original_readiness_status', 'original_substantive_attempts', 'original_attempt_limit', 'original_turn_event_count', 'original_turns',
               'new_original_proof_turns', 'historical_transitions_reconstructed', 'present_day_import_event_id', 'frozen_packet', 'whole_original_attempt_preserved'))
    require(a['schema'] == 'pr73-current-native-acceptance/v2' and a['PR'] == PR and a['problem_id'] == ID and a['reviewed_head'] == HEAD and a['merge_commit'] == merge, 'Native acceptance identity differs')
    require(a['final_ROOT_gate'] == gp and a['frozen_exact_plan'] == g['exact_plan'] and a['current_readiness_evidence'] == g['current_readiness_evidence'] and same(a['science'], science) and same(a['frozen_packet'], plan['packet']) and same(a['current_source_identity'], identity), 'Native scientific/evidence/source/readiness provenance differs')
    require(type(a['actual_controller_PID']) is int and a['actual_controller_PID'] > 0 and timestamp(a['at']) >= timestamp(g['UTC']), 'Actual author provenance/timestamp differs')
    require(a['original_attempt_file_count'] == 19 and a['original_status_json'] == 'ABSENT' and a['original_readiness_status'] == 'candidate_independently_reviewed' and type(a['original_substantive_attempts']) is int and a['original_substantive_attempts'] == 1 and type(a['original_attempt_limit']) is int and a['original_attempt_limit'] == 5 and type(a['original_turn_event_count']) is int and a['original_turn_event_count'] == 1 and a['original_turns'] == [1] and type(a['new_original_proof_turns']) is int and a['new_original_proof_turns'] == 0 and a['historical_transitions_reconstructed'] is False and a['whole_original_attempt_preserved'] is True, 'Original budget/history/provenance differs')
    before_state = s.git('show', merge + ':' + STATE)
    before_history = s.git('show', merge + ':' + HISTORY)
    for rel, b in ((STATE, before_state), (HISTORY, before_history)):
        require(s.git('ls-tree', merge, '--', rel).decode().split()[:3] == ['100644', 'blob', git_blob(b)], 'Pre-acceptance current global Git mode/blob differs')
    after_state = safe_path(STATE).read_bytes()
    after_history = safe_path(HISTORY).read_bytes()
    bs, ns = json.loads(before_state), json.loads(after_state)
    require(type(bs) is dict and ID not in bs and same({k: v for k, v in ns.items() if k != ID}, bs), 'Foreign current native state entries differ')
    preserved_single_insertion(before_state, after_state)
    require(after_history.startswith(before_history), 'Foreign history prefix differs byte-for-byte')
    added = after_history[len(before_history):]
    require(added.endswith(b'\n') and len(added.splitlines()) == 1, 'Expected exactly one actual current import event')
    event = json.loads(added)
    fields(event, ('schema', 'event', 'event_id', 'at', 'id', 'pr', 'status', 'turns_used', 'turn_limit', 'review_hash', 'readiness_review_hash',
                   'source_record_hash', 'source_report_hash', 'statement_hash', 'note', 'evidence'))
    require(same(ns[ID], event) and event['schema'] == 'pr73-present-day-native-import/v2' and event['event'] == 'acceptance_mirror_import' and event['id'] == ID and event['pr'] == PR and event['status'] == g['audited_outcome'], 'Current native state/event identity differs')
    require(type(event['turns_used']) is int and event['turns_used'] == 1 and type(event['turn_limit']) is int and event['turn_limit'] == 5 and event['at'] == a['at'], 'Current event accounting/time differs')
    eid = event_identity(gp, g['exact_plan'], merge, g['audited_outcome'])
    require(event['event_id'] == a['present_day_import_event_id'] == eid, 'Deterministic current import id differs')
    require(event['review_hash'] == event['readiness_review_hash'] == identity['review_hash_SQL_normalized_only'] and event['source_record_hash'] == identity['native_problem_hash'] and event['source_report_hash'] == identity['native_report_hash'] and event['statement_hash'] == identity['statement_hash'], 'Current event typed source/readiness fingerprints differ')
    require(event['note'] == target_row(safe_path(QUEUE).read_bytes()).decode().split('|')[11].strip(), 'Current event target-row note differs')
    expected_evidence = {'canonical_acceptance': pin(safe_path(PREFIX + '/acceptance.json')), 'final_ROOT_gate': gp,
                         'frozen_exact_plan': g['exact_plan'], 'reviewed_head': HEAD, 'merge_commit': merge,
                         'current_readiness_evidence': g['current_readiness_evidence'],
                         'original_budget': '1/5', 'original_turn_event_count': 1, 'new_original_proof_turns': 0,
                         'historical_transitions_asserted': False, 'native_prior_present_null': True, 'raw_prior_absent': True, 'SQL_prior_empty_object': True}
    require(same(event['evidence'], expected_evidence), 'Current import canonical acceptance/gate/accounting provenance differs')
    require(all(str(json.loads(x).get('id')) != ID for x in before_history.splitlines()), 'A historical target event was fabricated or duplicated')
    check_original_git(s, current, files, native=True)
    return {'event_id': eid, 'acceptance': a, 'one_current_import_event': True, 'foreign_current_state_history_bytes_preserved': True}

def foreign_readback(s, prior, owned, fresh_window):
    require(fresh_window.s is s, 'Fresh acknowledgment belongs to another readback session')
    fresh_window.check()
    fresh_ack = json.loads(fresh_window.ack_bytes)
    require(fresh_ack['ack_nonce'] != prior['actual_writer_ack_nonce'] and timestamp(fresh_ack.get('UTC', fresh_ack.get('utc'))) >= timestamp(prior['UTC']), 'Interphase acknowledgment is not fresh')
    require((s.dest / 'ACKNOWLEDGED_WINDOW.json').read_bytes() == fresh_window.ack_bytes == ACK.read_bytes(), 'Fresh actual ACK differs from current phase capture')
    d = safe_path(prior['actual_directory'])
    expected = (d / 'FOREIGN_INDEX.bin').read_bytes()
    current = b'\0'.join(x for x in s.git('ls-files', '--stage', '-z').split(b'\0') if x and x.split(b'\t', 1)[1].decode() not in owned)
    require(current == expected, 'Executed phase foreign index changed')
    flags = [x for x in s.git('ls-files', '-v', '-z').split(b'\0') if x]
    require(all(x.startswith(b'H ') for x in flags), 'Readback nonordinary index flags appeared')
    require(b'\0'.join(x for x in flags if x[2:].decode() not in owned) == (d / 'FOREIGN_INDEX_FLAGS.bin').read_bytes(), 'Executed phase foreign index flags changed')
    inventory = load(d / 'FOREIGN_TRACKED_WHOLE_INVENTORY.json')
    prior_ack_bytes = (d / 'ACKNOWLEDGED_WINDOW.json').read_bytes()
    require(prior['actual_writer_acknowledgment'] == pin(d / 'ACKNOWLEDGED_WINDOW.json'), 'Prior coordination acknowledgment pin differs')
    for row in inventory:
        p = safe_path(row['path'])
        if row['path'] == ACK_REL:
            require(row['exists'] and p.is_file() and not p.is_symlink() and p.lstat().st_mode == row['lstat_mode'], 'Coordination acknowledgment existence/type/mode changed between phases')
            require(len(prior_ack_bytes) == row['bytes'] and sha(prior_ack_bytes) == row['sha256'] and git_blob(prior_ack_bytes) == row['git_blob_SHA1'], 'Prior coordination ACK differs from prior whole tracked inventory')
            # Only this exact control file may receive its legitimate fresh
            # phase body. The current phase's WriterWindow independently pins
            # its actual body/mode/index/flags and checks them throughout.
            continue
        if row['exists']:
            b = p.read_bytes()
            require(not p.is_symlink() and p.is_file() and p.lstat().st_mode == row['lstat_mode'] and len(b) == row['bytes'] and sha(b) == row['sha256'] and git_blob(b) == row['git_blob_SHA1'], 'Executed phase foreign whole tracked body/mode changed, including a diff-hidden body')
        else: require(not p.exists() and not p.is_symlink(), 'Executed phase foreign tracked deletion changed')
    rows = load(d / 'FOREIGN_BODIES.json')
    require(names0(s.git('diff', '--name-only', '-z')) - set(owned) == set(rows), 'Executed phase foreign dirty scope changed')
    for rel, row in rows.items():
        p = safe_path(rel)
        if rel == ACK_REL:
            retained = safe_path(row['private_path']).read_bytes()
            require(row['exists'] and p.is_file() and not p.is_symlink() and p.lstat().st_mode == row['lstat_mode'] and retained == prior_ack_bytes and len(retained) == row['bytes'] and sha(retained) == row['sha256'], 'Prior/fresh coordination ACK custody or preserved mode differs')
            continue
        if row['exists']:
            require(p.is_file() and not p.is_symlink() and p.lstat().st_mode == row['lstat_mode'], 'Executed phase foreign dirty mode/type differs')
            retained = safe_path(row['private_path']).read_bytes()
            require(len(retained) == row['bytes'] and sha(retained) == row['sha256'] and p.read_bytes() == retained, 'Executed phase foreign dirty whole bytes differ')
        else:
            require(not p.exists() and not p.is_symlink(), 'Executed phase deleted foreign body recreated')
    return {'control_path': ACK_REL, 'prior_ack': prior['actual_writer_acknowledgment'],
            'fresh_ack': pin(s.dest / 'ACKNOWLEDGED_WINDOW.json'),
            'only_control_body_equality_excepted_between_phases': True,
            'prior_and_fresh_ack_separately_authenticated': True,
            'control_mode_index_flags_preserved': True,
            'all_other_foreign_body_mode_equality_preserved': True}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase', choices=('merge-readback', 'acceptance-readback', 'checkpoint-readback'))
    ap.add_argument('--gate', required=True)
    ap.add_argument('--predecessor', required=True)
    ap.add_argument('--writer-ack-nonce', required=True)
    args = ap.parse_args()
    g, plan, packet, science, gp = validate_gate(args.gate)
    m, files, source = originals()
    previous_phase = {'merge-readback': 'merge', 'acceptance-readback': 'accept', 'checkpoint-readback': 'checkpoint'}[args.phase]
    prior = read_receipt(pin(Path(args.predecessor).resolve()), previous_phase, gp)
    s = Session(args.phase, gp)
    current = current_baseline(s)
    require(current == prior['current_commit'], 'Main changed before independent readback')
    owned = ({QUEUE} | {x['path'] for x in files}) if args.phase == 'merge-readback' else (ACCEPT_PATHS if args.phase == 'acceptance-readback' else {r['pin']['path'] for r in plan['checkpoint_files']})
    w = WriterWindow(s, g, current, owned, prior['UTC'], args.writer_ack_nonce)
    identity = verify_current_source(s, source)
    pr = s.pr()
    require(pr['state'] == 'MERGED' and pr['mergedAt'] and pr['title'] == plan['pr_title'] and pr['body'].encode() == packet['PR_BODY.md'], 'Exact PR merged metadata differs')
    merge = prior.get('merge_commit')
    if args.phase == 'checkpoint-readback':
        accepted = load(safe_path(PREFIX + '/acceptance.json'))
        merge = accepted['merge_commit']
    require(pr['mergeCommit']['oid'] == merge and s.git('show', '-s', '--format=%P', merge).decode().split() == [plan['expected_base_main'], HEAD], 'Exact head/current-base two-parent merge differs')
    require(names0(s.git('diff', '--name-only', '-z', plan['expected_base_main'], merge)) == {QUEUE} | {x['path'] for x in files}, 'Merged incoming20 domain differs')
    check_original_git(s, current, files, native=True)
    before = s.git('show', plan['expected_base_main'] + ':' + QUEUE)
    after = s.git('show', merge + ':' + QUEUE)
    check_queue_plan(before, after, plan)
    require(safe_path(QUEUE).read_bytes() == after == s.git('show', current + ':' + QUEUE), 'Current native QUEUE differs from exact accepted merge')
    require(stat.S_IMODE(safe_path(QUEUE).stat().st_mode) == 0o644 and s.git('ls-tree', current, '--', QUEUE).decode().split()[:3] == ['100644', 'blob', git_blob(after)], 'Current native QUEUE worktree/Git mode/blob differs')
    remote_source = json.loads(s.run(['gh', 'api', 'repos/' + REPO + '/contents/' + QUEUE + '?ref=' + HEAD])[0])
    original_queue = (AUTH / 'original' / QUEUE).read_bytes()
    require(base64.b64decode(remote_source['content']) == original_queue and remote_source['sha'] == git_blob(original_queue), 'Fresh remote immutable original QUEUE differs')
    ack_handoff = foreign_readback(s, prior, owned, w)
    result = {'current_commit': current, 'merge_commit': merge, 'exact_plan': g['exact_plan'], 'predecessor': pin(Path(args.predecessor).resolve()),
              'GitHub_exact_head_merged_title_body_verified': True, 'exact_two_parent_merge_verified': True,
              'original19_bytes_modes_blobs_preserved': True, 'original_budget': '1/5', 'original_ledger_events': 1,
              'original_status_json': 'ABSENT', 'raw_SQL_native_typed_source_pair_verified': True,
              'unrelated_foreign_tracked_bytes_modes_index_preserved': True,
              'within_current_phase_all_foreign_bytes_modes_index_preserved': True,
              'coordination_ack_handoff': ack_handoff}
    if args.phase == 'merge-readback':
        require(current == merge and not safe_path(PREFIX + '/acceptance.json').exists(), 'Merge readback must precede separate acceptance')
        result['native_acceptance_pending'] = True
    elif args.phase == 'acceptance-readback':
        v = verify_acceptance(s, g, plan, packet, science, gp, merge, current, files, identity)
        require(v['acceptance']['merged_at'] == pr['mergedAt'] and v['event_id'] == prior['event_id'], 'Native merged provenance/event differs')
        result.update({'acceptance_commit': current, 'event_id': v['event_id'], 'native_acceptance_verified': True,
                       'one_current_import_event': True, 'foreign_current_state_history_bytes_preserved': True})
    else:
        accept_commit = s.git('rev-parse', current + '^').decode().strip()
        v = verify_acceptance(s, g, plan, packet, science, gp, merge, accept_commit, files, identity)
        paths = names0(s.git('diff', '--name-only', '-z', accept_commit, current))
        require(paths == set(prior['public_safe_paths']) and paths <= {r['pin']['path'] for r in plan['checkpoint_files']}, 'Public-safe checkpoint scope differs')
        checkpoint_rows = {r['pin']['path']: r for r in plan['checkpoint_files']}
        for rel in paths:
            public_safe(rel); row = checkpoint_rows[rel]; b = s.git('show', current + ':' + rel)
            require(len(b) == row['pin']['bytes'] and sha(b) == row['pin']['sha256'] and s.git('ls-tree', current, '--', rel).decode().split()[:3] == [row['git_mode'], 'blob', git_blob(b)], 'Readback checkpoint body/mode/blob differs from frozen ROOT pin')
        result.update({'checkpoint_commit': current, 'public_safe_checkpoint_verified': True, 'private_raw_copyright_data_excluded': True,
                       'native_acceptance_preserved': True, 'event_id': v['event_id']})
    w.check()
    require(validate_gate(args.gate)[4] == gp, 'Final ROOT gate/packet drifted during readback')
    for row in identity['whole_current_source_pins']: check_pin(row)
    s.finish(result)

if __name__ == '__main__':
    main()
