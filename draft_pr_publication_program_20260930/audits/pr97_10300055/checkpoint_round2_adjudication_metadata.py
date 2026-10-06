"""Adjudicate authenticated reviews without inferring novel-result publication authority."""
from pathlib import Path
import datetime, hashlib, json, os

A = Path(__file__).resolve().parent
P = A.parents[1]
C = P.parent
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

review_auth = A / 'root_whole_package_review_authentication_20261006/whole_package_round2_20261006.json'
auth = json.loads(review_auth.read_text())
verdict_path = A / 'whole_package_round2_20261006/VERDICT.json'
verdict = json.loads(verdict_path.read_text())
require(auth['all_bytes_and_inventory_authenticated'] and auth['required_issue_ids'] == [],
        'Fresh review evidence not accepted')
require(verdict['whole_package_verdict'] == 'PASS_QUALIFIED_UNPUBLISHED_PACKAGE'
        and verdict['issues'] == [] and verdict['whole_package_acceptance'], 'Fresh review verdict differs')
live_path = A / 'actual_operations/live_pr97_after_round2/stdout.bin'
live = json.loads(live_path.read_text())
head = 'fb50facb2a7389bb272bbf0b5cbd80c24c79b992'
require(live['number'] == 97 and live['headRefOid'] == head and live['state'] == 'OPEN'
        and live['isDraft'] and live['baseRefName'] == 'main', 'Original current PR changed')
D = A / 'contingent_credited_note_v2'
check_path = A / 'actual_operations/zenodo_local_check_credited_v2/stdout.bin'
check = json.loads(check_path.read_text())
deposit = json.loads((D / 'zenodo-deposit.proposed.json').read_text())
require(check['title'] == deposit['metadata']['title'] and len(check['files']) == len(deposit['files']) == 9,
        'Offline kit check differs from proposal')
by_name = {row['name']: row for row in check['files']}
for item in deposit['files']:
    path = D / item['path']
    name = item.get('name', path.name)
    row = by_name[name]
    require(path.is_file() and not path.is_symlink() and sha(path) == row['sha256']
            and path.stat().st_size == row['size'], 'Offline proposed file mismatch')

adjudication = {
    'schema': 'pr97-root-qualified-package-final-adjudication/v1',
    'UTC': now, 'operator_PID': os.getpid(), 'PR': 97, 'problem_id': 10300055,
    'original_current_head': head, 'original_literal_status': 'claimed_solved',
    'original_effort': '2/5', 'new_central_proof_search_turns': 0,
    'mathematical_clearance': True,
    'short_claim': 'Global nonzero C1 alpha defining a cooriented taut C2 no-sphere foliation on closed oriented smooth3M, and smooth contact omega with d alpha=alpha wedge omega, imply ordinary tight ker omega.',
    'extra_claim': 'Separately verified C1-omega explicit C2-disk criterion and every-near smooth tightness; other low-regularity equivalences not asserted.',
    'source_interpretation_limits': 'Actual2002 Question13.2 under ordinary-fundamental-class closed/oriented and smooth-contact interpretations; no Question13.1 existence result or2002/2003 equality claim.',
    'required_package_findings_remaining': [], 'qualified_unpublished_package_accepted': True,
    'whole_package_rounds_completed': 2,
    'round1': {'manifest_sha256': 'a92201a04ffa95ea2a64ccf6788923221ba5ed198a29f31c95effc428c0a8e42',
               'finding': 'R1 output-leaf symlink/hardlink custody flaw', 'disposition': 'Repaired in preserved v2, independently tested by new round2'},
    'round2': {'manifest_sha256': '4696051fa095f36d77a39063ea9b763148e23d8ffeab9dca48860c785f7cb265',
               'verdict_sha256': sha(verdict_path), 'ROOT_authentication_sha256': sha(review_auth),
               'own_regular_files': 1407, 'controlled_symlinks': 32, 'hardlink_groups': 20,
               'borrowed_inputs': 1676, 'required_findings': []},
    'package': {'folder': D.name, 'manifest_sha256': sha(D/'CLOSED_MANIFEST.json'),
                'paper_sha256': sha(D/'publicfiles/pr97_note.pdf'),
                'zip_sha256': sha(D/'pr97_support.zip'), 'zip_members': 93},
    'bounded_priority_audit_complete': True, 'strict_priority_clearance': False,
    'historical_priority': 'UNRESOLVED', 'firstness_established': False,
    'present_day_open_status_established': False,
    'prior_art': 'Dathe–Khoule2012 general affine criterion covers the pencil; ordinary tightness is our classical ET/finite-Gray corollary.',
    'exact_prior_printed_Q13_2_answer_authenticated': False,
    'full_original_already_solved_disposition_authenticated': False,
    'mathematical_failure_or_close_PR_cause': False,
    'paper_framing': 'Credited classical conditional research note with unresolved priority; no new construction or first historical resolution claim.',
    'offline_exact_repository_Zenodo_check': {'actual_child_PID': 52248, 'exit_code': 0,
                                            'proposed_files': 9, 'output_sha256': sha(check_path),
                                            'service_calls': False, 'files_match_reviewed_proposal': True},
    'root_checker_schema_failure': {'actual_child_PID': 53851, 'exit_code': 1,
                                    'cause': 'ROOT label absent versus manifest label dangling',
                                    'source_and_actual_failure_preserved': True,
                                    'corrected_actual_child_PID': 54217, 'corrected_exit_code': 0,
                                    'review_inputs_changed': False},
    'human_peer_review': False, 'PR95_waiver_applies': False,
    'PR97_qualified_publication_authorization': False, 'publication_ready_under_original_novel_resolution_goal': False,
    'native_acceptance': False, 'DOI': None, 'tracker_range': None,
    'next_gate': 'Obtain a PR97-specific human disposition for the concrete qualified note or accepted nonpublication finding; no service/native mutation until justified.',
    'workflow_estimate_percent': 60, 'program_completion_percent': 13/99*100,
}
adjudication_path = A / 'ROOT_WHOLE_PACKAGE_ADJUDICATION_20261006.json'
with adjudication_path.open('x') as stream:
    stream.write(json.dumps(adjudication, indent=2) + '\n')
progress_path = P / 'CURRENT_PROGRESS.json'
progress = json.loads(progress_path.read_text())
require(progress['current_PR'] == 97, 'Program cursor changed')
progress.update({
    'UTC': now, 'updated_UTC': now, 'current_PR_workflow_percent': 60, 'current_workflow_estimate_percent': 60,
    'current_whole_package_review_rounds_completed': 2, 'current_whole_package_reviews_completed': 2,
    'current_whole_package_round2_status': 'closed_pass_qualified_unpublished_package',
    'current_whole_package_round2_manifest_sha256': adjudication['round2']['manifest_sha256'],
    'current_whole_package_round2_ROOT_authentication': str(review_auth.relative_to(P)),
    'current_whole_package_ROOT_adjudication': str(adjudication_path.relative_to(P)),
    'current_qualified_unpublished_package_acceptance': True,
    'current_qualified_note_ready_for_human_disposition': True,
    'current_package_known_required_repair': False, 'current_package_known_issue': None,
    'current_priority_clearance': False, 'current_publication_authorization': False,
    'current_publication_ready': False, 'current_package_ready_for_publication': False,
    'current_DOI': None, 'current_tracker_range': None,
    'current_native_integration_started': False, 'current_native_integration_complete': False,
    'remaining_current_step': 'Mathematics and qualified unpublished package accepted after repaired R1 and fresh clean R2. Original goal novelty/open status unestablished; a PR97-specific human qualified-publication or nonpublication disposition is now needed.',
    'next_step': 'Present the exact reviewed four-page note/support proposal for human disposition; no priority waiver inferred from PR95.',
})
progress_path.write_text(json.dumps(progress, indent=2) + '\n')
with (A / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### ' + now + ' — fresh round two accepted; original novelty gate remains unresolved\n'
                 'ROOT read the final full report/verdict, initial independent assessment and corrected proof reconstruction and authenticated1407 own regular files,32 controlled symlinks (regular/directory/dangling targets),20 complete hardlink groups and1676 borrowed regular inputs. New reviewer independently reproduces6 math,28 integrity,50 custody and84 additional bounded own controls, inspects all4 PDF pages, and finds no required issue. A report-only general-n exponent omission was corrected against the actual source before closure; current n1 package was correct throughout. ROOT checker first failed on its own absent/dangling enum mismatch (actual53851exit1), preserving its exact source and failed streams; corrected54217exit0 fully authenticated unchanged evidence. Exact repo Zenodo offline check52248exit0 validates all9 proposed reviewed files with no service call. Current live PR97 remains OPENdraft at original fb50facb2a7389bb272bbf0b5cbd80c24c79b992. Qualified unpublished package accepted, but known2012 affine mechanism and unread historical gaps prevent strict novelty/current-openness clearance. No mathematical reason to close; no paper publication/merge/native/tracker action authorized forPR97, and noPR95 waiver inferred. Original2/5, extra proof-search0. Estimated PR97workflow60%; program13/99=13.13%. Next: human disposition for concrete qualified note or nonpublication result.\n')

selected = {progress_path, A/'RESEARCH_LOG.md', adjudication_path, Path(__file__).resolve(),
            A/'authenticate_whole_package_round2_review.py', A/'root_round2_authenticator_history_v1.py',
            A/'ROOT_ROUND2_AUTHENTICATOR_SCHEMA_CORRECTION_20261006.json', review_auth,
            A/'ROOT_V2_PREPARATION_CHECKPOINT_ACTUAL_READBACK_20261006.json', A/'record_v2_checkpoint_readback.py',
            A/'V2_PREPARATION_CHECKPOINT_SELECTION.json',
            A/'actual_checkpoints/corrected_preparation_v2/RECEIPT.json',
            A/'actual_checkpoints/corrected_preparation_v2/PROCESS_JOURNAL.json'}
R = A / 'whole_package_round2_20261006'
selected.update(path for path in R.iterdir() if path.is_file() and not path.is_symlink())
for path in (R/'actual_processes').rglob('*'):
    if not path.is_file() or path.is_symlink():
        continue
    relative = path.relative_to(R/'actual_processes')
    # Third-party source extracts remain private; their process metadata remains checkable.
    if relative.parts[0].startswith('extract_') and path.name != 'receipt.json':
        continue
    selected.add(path)
for folder in ['diagnostics_reproduction', 'integrity_reproduction', 'custody_reproduction', 'independent_controls']:
    selected.update(path for path in (R/folder).glob('*') if path.is_file() and not path.is_symlink())
for label in ['prepare_v2_checkpoint_metadata', 'checkpoint_v2_prepared', 'checkpoint_v2_prepared_retry',
              'record_v2_checkpoint_readback', 'zenodo_local_check_credited_v2',
              'authenticate_whole_package_round2', 'authenticate_whole_package_round2_corrected',
              'live_pr97_after_round2']:
    selected.update(path for path in (A/'actual_operations'/label).rglob('*')
                    if path.is_file() and not path.is_symlink())
rows = []
for path in sorted(selected):
    require(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(C.resolve()),
            'Unsafe checkpoint body')
    body = path.read_bytes()
    rows.append({'path': path.relative_to(C).as_posix(), 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()})
selection = {'schema': 'pr97-accepted-round2-checkpoint-selection/v1', 'UTC': now,
             'operator_PID': os.getpid(), 'expected_main': 'ad789fadf6e398fe7e2c0d243db4625e78207a8e',
             'paths': [row['path'] for row in rows], 'pins': rows,
             'third_party_extracted_bodies_and_controlled_fixture_links_private': True,
             'all_private_evidence_retained_not_deleted': True, 'publication_authorized': False,
             'new_central_proof_search_turns': 0}
destination = A/'ROUND2_ADJUDICATION_CHECKPOINT_SELECTION.json'
with destination.open('x') as stream:
    stream.write(json.dumps(selection, indent=2) + '\n')
print(json.dumps({'UTC': now, 'operator_PID': os.getpid(), 'accepted_qualified_unpublished_package': True,
                  'selected_files': len(rows), 'selected_bytes': sum(row['bytes'] for row in rows),
                  'workflow_percent': 60, 'publication_authorized': False}))
