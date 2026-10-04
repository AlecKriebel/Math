"""Record the completed qualified package; keep the unmet priority gate explicit."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys

if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B, no -O')
A = Path(__file__).resolve().parent
P = A.parents[1]
C = P / 'audits/pr45_9900007'
F = A / 'ROOT_qualified_note_ready_gate_20261004'
F.mkdir(exist_ok=False)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def capture(name):
    folder = C / name
    row = json.loads((folder / 'CAPTURE.json').read_bytes())
    require(row['status'] == 'PASS' and row['actual_execution'] and row['completed'] and row['exit_code'] == 0 and row['pid'] > 0, 'Invalid capture')
    for stream in ('stdout', 'stderr'):
        body = (folder / row[stream]['path']).read_bytes()
        require(len(body) == row[stream]['bytes'] and sha(body) == row[stream]['sha256'], 'Capture stream drift')
    return folder, row

review = json.loads((A / 'ROOT_round2_review_readback_20261004/READBACK.json').read_bytes())
require(review['required_repairs'] == [] and review['review_members_verified'] == 81 and review['package_regular_files_verified'] == 34, 'Round2 readback not complete')
head_folder, head_capture = capture('root_pr65_ready_decision_fresh_GitHub_head_20261004_actual_capture')
head = json.loads((head_folder / 'stdout.bin').read_bytes())
require(head['number'] == 65 and head['state'] == 'open' and head['draft'] and not head['merged'] and head['head']['sha'] == '5cc1602c05d79502defb07cec7027963149494d2', 'PR head changed')
queue_folder, queue_capture = capture('root_pr65_ready_decision_fresh_HEAD_QUEUE_retry_20261004_actual_capture')
rows = []
for line in (queue_folder / 'stdout.bin').read_text().splitlines():
    if not line.startswith('|'):
        continue
    cells = [cell.strip() for cell in line.strip('|').split('|')]
    if len(cells) > 8 and cells[1].split('/')[0].strip() == '2305051':
        rows.append(cells)
require(len(rows) == 1 and rows[0][7] == 'claimed_solved' and rows[0][8] == '2/5', 'Literal eligibility changed')
progress_path = P / 'CURRENT_PROGRESS.json'
progress = json.loads(progress_path.read_bytes())
require(progress['current_PR'] == 65 and progress['fully_completed_eligible_PRs'] == [9, 16, 18, 50, 55, 57] and not progress['persistent_goal_complete'], 'Progress drift')
stamp = dt.datetime.now(dt.timezone.utc).isoformat()
gate = {
    'schema': 'qualified-note-ready-unpublished/v1', 'UTC': stamp, 'actual_writer_pid': os.getpid(),
    'PR': 65, 'problem': '2305051 / AMR-022-5051', 'immutable_science_head': head['head']['sha'],
    'last_readonly_GitHub_observation_UTC': head_capture['finished_utc'],
    'last_readonly_HEAD_QUEUE_observation_UTC': queue_capture['finished_utc'],
    'literal_HEAD_QUEUE_status': rows[0][7], 'original_proof_turns': rows[0][8],
    'title': 'An effective Blaschke construction with Bloch Cayley transform',
    'package': str(A / 'publication_package_v1'), 'current_artifact_pins': review['current_artifacts'],
    'mathematical_audit_percent': 100, 'bounded_priority_audit_percent': 100,
    'priority_clearance': False, 'historical_priority': 'unestablished',
    'affirmative_prior_overlap': 'Kahane1969 fixed absorbed unit rule; Aleksandrov-Anderson-Nicolau1999 printed Cayley/Bloch application. No novelty or first-solution certificate.',
    'material_unread_sources': [
        {'title': 'Two monotonic, singular, uniformly almost smooth functions', 'authors': 'G. Piranian', 'year': 1966, 'DOI': '10.1215/S0012-7094-66-03329-1'},
        {'title': 'Singular measures and domains not of Smirnov type', 'authors': 'P. L. Duren; H. S. Shapiro; A. L. Shields', 'year': 1966, 'DOI': '10.1215/S0012-7094-66-03328-X'},
        {'title': 'Research Problems in Function Theory', 'authors': 'W. K. Hayman; E. F. Lingham', 'year': 2019, 'DOI': '10.1007/978-3-030-25165-9', 'gap': 'relevant later-edition update unread'}
    ],
    'fresh_whole_package_round1': 'complete; sole historical-runner custody issue repaired',
    'fresh_whole_package_round2': 'complete; NEW independent agent clean; no required repairs',
    'round2_report_sha256': review['review_report_sha256'],
    'ROOT_round2_custody_record': 'ROOT_round2_review_readback_20261004/READBACK.json',
    'native_compilation_success': True, 'ROOT_visual_QA_pages': 10,
    'local_Zenodo_kit_check': 'passed for exact repaired metadata/PDF/ZIP; local-only, no API call',
    'AI_and_unrefereed_disclosures': True,
    'ready_for_qualified_publication_if_specifically_authorized': True,
    'publication_authorized': False, 'publication_decision_needed': 'PR65-specific exception to original novel-resolution priority requirement; PR50 exception does not transfer',
    'uploaded_or_staged': False, 'DOI': None, 'tracker_row': None, 'merged': False,
    'native_acceptance_changed': False, 'proof_turns_changed': False,
    'current_PR_workflow_estimate_percent': 60,
    'ordered_completed_count': 6, 'dated_eligible_total': 99,
    'ordered_completion_percent': 100 * 6 / 99, 'goal_complete': False,
    'approval_timeout_is_not_authorization': True,
    'operator_readback_note': 'The initial read-only row selector included the leading empty pipe cell and failed. The corrected selector strips the enclosing pipes, verifies the compound ID, and reads literal status/turn cells. This was an operator-format correction, not a mathematical failure or mutation.'
}
(F / 'READY_GATE.json').write_text(json.dumps(gate, indent=2) + '\n')
progress.update(UTC=stamp, current_PR_workflow_percent=60,
    remaining_current_step='PR65 qualified package is fully reviewed and ready; obtain PR65-specific human publication decision because historical priority remains unresolved. No publication/merge/advance on silence.',
    current_package_adversarial_round2_status='complete: NEW independent agent CLEAN; no required repairs',
    current_package_adversarial_round2_record='audits/pr65_2305051/whole_package_round2_20261004/REPORT.md',
    current_package_ROOT_round2_readback_record='audits/pr65_2305051/ROOT_round2_review_readback_20261004/READBACK.json',
    current_ready_gate_record='audits/pr65_2305051/ROOT_qualified_note_ready_gate_20261004/READY_GATE.json',
    current_qualified_package_ready=True, current_priority_clearance=False,
    current_publication_authorization=False, advance_to_next_PR_authorized_now=False,
    current_DOI=None, current_merge_commit=None)
progress_path.write_text(json.dumps(progress, indent=2) + '\n')
with (A / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n## ' + stamp + ' — qualified note ready; human PR65 publication decision pending\n\n')
    f.write('ROOT read the full fresh round2 report, verdict, first independent conclusion and custody-check source. Verified all81 manifested review members, seven actual outer process streams, four nested assertion-enabled unchanged-checker outputs, all34 current package files, the30-member source manifest and all32 exact archive members. The new reviewer found no required repairs after independent proof/source/code/PDF/package review. Round1’s historical-runner traceability issue is resolved without changing proof/PDF/checker/metadata bytes. Native compilation and all ten ROOT-inspected PDF pages passed; the repaired local-only Zenodo-kit check passed. The three bounded priority families remain complete with clearancefalse: strong classical overlap and named unread1966/later-edition sources prevent a novel-resolution certificate. The qualified note is concrete and ready for a PR65-specific human exception; PR50 authorization is not extended. No65 staging/upload/DOI/tracker/merge/native acceptance or additional original proof turns. Original turns2/5; math100%; bounded priority audit100% (clearancefalse); package review100%; best-guess current workflow60%; ordered completion6/99 (6.060606%).\n')
record = {'UTC': stamp, 'actual_writer_pid': os.getpid(), 'ready_gate_sha256': sha((F / 'READY_GATE.json').read_bytes()), 'current_progress_sha256': sha(progress_path.read_bytes()), 'status': 'READY_QUALIFIED_NOTE_UNPUBLISHED_PENDING_PR65_HUMAN_DECISION', 'current_PR_workflow_percent': 60, 'priority_clearance': False, 'publication_authorized': False, 'goal_complete': False}
(F / 'PROGRESS_RECEIPT.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
