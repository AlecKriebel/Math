"""Record a revalidated third consecutive essential-source access blocker."""
from pathlib import Path
import datetime, hashlib, json, os

D = Path(__file__).resolve().parent
A = D.parent
P = A.parents[1]
C = P.parent
D.mkdir(exist_ok=True)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
gate = json.loads((A / 'ROOT_PRIORITY_HOLD_GATE_20261006.json').read_text())
prior = json.loads((A / 'root_final_access_followup_20261006/RESULT.json').read_text())
progress_path = P / 'CURRENT_PROGRESS.json'
progress = json.loads(progress_path.read_text())
assert progress['current_PR'] == 110
assert progress['current_access_blocker_goal_turns_recorded'] == 2
assert gate['decision'] == 'HOLD_FOR_M1_FINAL_JOURNAL_COMPARISON'
assert not gate['novelty_established_for_publication']
assert not gate['already_solved_disposition_supported']
op = A / 'actual_operations/root_blocked_revalidation_pr110_head_20261006'
execution = json.loads((op / 'execution.json').read_text())
live = json.loads((op / 'stdout.bin').read_text())
assert execution['exit_code'] == 0
assert live['state'] == 'OPEN' and live['isDraft'] and live['mergedAt'] is None
assert live['headRefOid'] == progress['current_original_head']
pins = []
for pin in prior['private_source_pins']:
    p = A / 'root_final_access_followup_20261006' / pin['path']
    b = p.read_bytes()
    assert len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256']
    pins.append({'path': str(p.relative_to(A)), 'bytes': len(b), 'sha256': pin['sha256']})
candidate = A / 'priority_modern_invariant_mechanism_20261006/private_sources/GKR_spatial_final.pdf'
b = candidate.read_bytes()
assert not b.startswith(b'%PDF-')
assert hashlib.sha256(b).hexdigest() == '7194e38a4706e3b3e140aaa2dbbdc47cc25a9e414794a79da3bc2bb04d7caf43'
names = ['elliptic', 'billiard', 'spatial', '09608', 'garcia', 'koiller', 'reznik']
download_matches = [str(p) for p in Path('/Users/alec/Downloads').rglob('*')
                    if p.is_file() and p.suffix.lower() == '.pdf'
                    and any(x in p.name.lower() for x in names)]
assert not download_matches
last = json.loads((P / 'audits/pr108_30003996/actual_checkpoints/PR110_access_followup_20261006/RECEIPT.json').read_text())
assert last['commit'] == '1ae4c844f014a8d2c5d7357506f1a794793a624c' and last['remote_verified']
record = {
    'schema': 'pr110-third-consecutive-essential-access-blocked-audit/v1',
    'UTC': now, 'actual_operator_PID': os.getpid(), 'PR': 110,
    'previous_goal_turn_classification': 'progress',
    'previous_goal_turn_evidence': 'Completed new bounded access checks and pushed their 51 full-body-verified files at 1ae4c844f014a8d2c5d7357506f1a794793a624c; required M1 remained unresolved.',
    'current_goal_turn_classification': 'no_progress_on_required_M1',
    'same_blocking_condition_consecutive_goal_turns': 3,
    'third_turn_revalidation': {
        'PR_actual_child_PID': execution['child_PID'], 'PR_live': live,
        'prior_private_access_sources_unchanged': pins,
        'existing_final_named_candidate_is_not_PDF': True,
        'existing_final_named_candidate_bytes': len(b),
        'existing_final_named_candidate_sha256': hashlib.sha256(b).hexdigest(),
        'relevant_named_download_PDF_matches': download_matches,
        'live_PR110_review_agents': [],
        'live_review_agents_source': 'Actual collaboration.list_agents /root/pr110 returned empty in this turn.',
        'no_new_human_source_or_access_reply': True,
    },
    'required_source': gate['required_findings'][0],
    'meaningful_safe_next_action_without_user_or_external_state_change': None,
    'reason': 'Source/math and fresh bounded priority adjudication are complete. The full later journal body is the one essential candidate comparison. Available publisher/repository/index/browser routes supplied previews or no body. No live process is obtaining it. Repeated unchanged searches or redoing verified math cannot satisfy this requirement. Publication and ordered advance remain gated.',
    'blocked_audit_passed': True,
    'goal_tool_status_at_last_read': 'active',
    'required_next_goal_tool_transition': 'blocked',
    'goal_transition_not_yet_executed_at_this_snapshot': True,
    'persistent_goal_complete': False, 'already_solved_supported': False,
    'PR_merge_close_publish_action_performed': False,
    'source_math_percent': 100, 'priority_work_percent': 90,
    'current_workflow_percent': 30, 'publication_percent': 0,
    'full_program_completed': 17, 'dated_eligible_total': 99,
    'full_program_completion_percent': 100 * 17 / 99,
    'published_count': 10, 'new_central_proof_search_turns': 0,
}
(D / 'RESULT.json').write_text(json.dumps(record, indent=2) + '\n')
(D / 'REPORT.md').write_text(
    '# PR110 blocked audit\n\n'
    'The same M1 final-journal-body access gap has persisted across three consecutive goal turns. '
    'The first completed fresh combined priority adjudication and pushed the specific hold; '
    'the second completed further legitimate access checks and pushed their full-body-verified checkpoint. '
    'This third turn revalidates the unchanged open draft, unchanged access-source hashes, the non-PDF publisher-preview file misleadingly named final, '
    'the absence of relevant named PDF arrivals in Downloads, and no live PR110 review agents. '
    'No human source/access reply has arrived. The previous turn was progress through completed access work; the same genuine blocker remained.\n\n'
    'Required: Garcia–Koiller–Reznik, *Estimating Elliptic Billiard Invariants with Spatial Integrals*, '
    'Journal of Dynamical and Control Systems29:757–767(2023), online2022, '
    'DOI10.1007/s10883-022-09608-y. The full nine-page2021 preprint is read. The complete eleven-page later journal body is needed '
    'to compare the actual governing statements and proofs with our all-period ordinary-positive antipedal norm-sum result. '
    'An accessible full journal PDF or legitimate full-text link would permit a separately sealed comparison supplement.\n\n'
    'The third-turn blocked audit passes. No meaningful safe work can satisfy this essential comparison without a new complete body or legitimate access change. '
    'There is no live retrieval process to wait for. Repeating unchanged access attempts or verified mathematical audits adds no evidence. '
    'The ordered goal does not permit bypassing PR110 before its disposition. Access failure is not evidence of already_solved; '
    'PR110 remains draft, unmerged and unpublished. Novelty is not established for publication.\n\n'
    'The goal tool still reported active at this file snapshot; the required next action is update_goal(blocked), whose returned status will be reported to the user. '
    'No tool success is anticipated as already completed here. Source/math100%, selected-candidate priority work90%, PR110 workflow30%, publication0%; '
    '17/99 full-program workflows complete (17.17%), ten published, new central proof-search turns0. All earlier science/source/priority seals remain unchanged.\n')
progress.update({
    'UTC': now, 'updated_UTC': now,
    'current_access_blocker_goal_turns_recorded': 3,
    'current_last_goal_turn_classification': 'progress',
    'current_this_goal_turn_classification': 'no_progress_on_required_M1',
    'current_blocked_audit': str((D / 'RESULT.json').relative_to(P)),
    'current_blocked_audit_passed': True,
    'persistent_goal_status_transition_due': 'blocked',
    'persistent_goal_status_transition_executed_at_snapshot': False,
    'current_access_followup_checkpoint_commit': last['commit'],
})
progress_path.write_text(json.dumps(progress, indent=2, sort_keys=True) + '\n')
entry = (now + ' — PR110 third consecutive M1 access-blocker audit passed: unchanged open draft/head, '
         'prior access-source hashes unchanged, final-named local file is HTML rather than a PDF, '
         'no relevant named journal PDF in Downloads, no live PR110 review agent and no new human source reply. '
         'Previous bounded access work/checkpoint completed at1ae4c844…; no safe work now clears the essential final-body comparison. '
         'Required next goal-tool transition blocked (not yet executed at this snapshot). '
         'Math/source100%, priority90%, workflow30%, publication0%; full program17/99=17.17%, ten published, new proof turns0. '
         'No PR110 close/merge/publication or ordered advance; no evidence supports already_solved.\n')
for p in [A / 'RESEARCH_LOG.md', P / 'RESEARCH_LOG.md', P / 'CURRENT_PROGRESS.md']:
    with p.open('a') as handle:
        handle.write('\n' + entry)
selected = [p for p in D.iterdir() if p.is_file()]
selected += [D / 'CHECKPOINT_SELECTION.json', A / 'RESEARCH_LOG.md', P / 'RESEARCH_LOG.md',
             P / 'CURRENT_PROGRESS.md', progress_path]
for label in ['root_blocked_revalidation_pr110_head_20261006', 'root_finalize_blocked_audit_20261006']:
    selected += [A / 'actual_operations' / label / name
                 for name in ['started.json', 'execution.json', 'stdout.bin', 'stderr.bin']]
(D / 'CHECKPOINT_SELECTION.json').write_text(json.dumps({'paths': sorted({str(p.relative_to(C)) for p in selected})}, indent=2) + '\n')
print(json.dumps({k: record[k] for k in ['schema', 'UTC', 'actual_operator_PID', 'same_blocking_condition_consecutive_goal_turns', 'blocked_audit_passed', 'required_next_goal_tool_transition', 'current_workflow_percent', 'publication_percent']}))
