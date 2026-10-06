"""Prepare a scoped main checkpoint without staging active review artifacts."""
from pathlib import Path
import datetime, hashlib, json, os

A = Path(__file__).resolve().parent
P = A.parents[1]
C = P.parent
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
progress_path = P / 'CURRENT_PROGRESS.json'
progress = json.loads(progress_path.read_text())
if progress['current_PR'] != 97 or progress['last_completed_PR'] != 95:
    raise RuntimeError('Program cursor changed')
progress.update({
    'UTC': now, 'updated_UTC': now,
    'current_package': 'audits/pr97_10300055/contingent_credited_note_v2',
    'current_package_folder': 'contingent_credited_note_v2',
    'current_package_preparation_complete': True,
    'current_package_preparation_percent': 100,
    'current_package_preparation_estimate_percent': 100,
    'current_package_repair_status': 'closed_authentication_passed_fresh_review_pending',
    'current_package_closed_manifest_sha256': 'b66716a960c07d6064e0108f32dc9c41c1bb61757bbd1fdcb416bba7e42aa8d4',
    'current_package_ROOT_authentication': 'audits/pr97_10300055/ROOT_PREPARED_PACKAGE_V2_AUTHENTICATION_20261006.json',
    'current_package_baseline_preservation': 'audits/pr97_10300055/ROOT_V2_BASELINE_PRESERVATION_20261006.json',
    'current_package_known_required_repair': False,
    'current_package_known_issue': 'R1 repaired in v2 with actual controls; fresh whole-package review pending.',
    'current_whole_package_round2_agent': 'pr97_whole_package_round2_20261006',
    'current_whole_package_round2_status': 'running',
    'current_PR_workflow_percent': 45,
    'current_workflow_estimate_percent': 45,
    'current_package_ready_for_publication': False,
    'current_publication_ready': False,
    'current_publication_authorization': False,
    'current_priority_clearance': False,
    'remaining_current_step': 'New from-scratch whole-package round-two review of corrected closed v2; adjudicate and repair as required. Strict priority is unresolved and no PR97 qualification authority is inferred from PR95.',
    'next_step': 'Await fresh review, authenticate all evidence, globally repair any substantive finding and repeat with another new reviewer. No publication or native acceptance before justified PR97-specific gates.',
})
progress_path.write_text(json.dumps(progress, indent=2) + '\n')
with (A / 'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### ' + now + ' — closed custody correction and fresh round two\n'
                 'ROOT fully read the v2 report, corrected wrappers and public documentation, authenticated582 own regular files,10 private controlled symlinks,10 hardlink groups,20 borrowed original/math/priority bodies,10 static originals and metadata provenance. ZIP93 members are byte-identical to the92-file public payload plus manifest; mathematical programs/candidates, paper source/PDF and static metadata are unchanged. A separate actual ROOT check reauthenticated every231 v1 and578 R1 regular body, all8 R1 symlinks/six hardlink groups and9/19 respective borrowed inputs without updating frozen receipts. Required R1 is corrected; all actual positive/negative/custody/integrity/reuse controls passed, with preparation-only bookkeeping failures honestly preserved. NEW pr97_whole_package_round2_20261006 has been assigned the entire mathematical/source/artifact/custody audit from scratch, preserving initial independence. Closed inputs remain unchanged; private synthetic links and duplicate fixture payloads remain local, while regular original support and actual evidence are selected for the scoped checkpoint. No PR/QUEUE/publication/tracker/editor/outside-contact action. Original author2/5; zero new central proof-search turns. Strict priority and publication authority/package acceptance remain false. Estimated program13/99=13.13%; PR97workflow45%; correction preparation100%.\n')

selected = {progress_path, A / 'RESEARCH_LOG.md', A / 'authenticate_prepared_package_v2.py',
            A / 'authenticate_preserved_inputs_after_v2.py', Path(__file__).resolve(),
            A / 'ROOT_PREPARED_PACKAGE_V2_AUTHENTICATION_20261006.json',
            A / 'ROOT_V2_BASELINE_PRESERVATION_20261006.json',
            A / 'actual_checkpoints/round1_repair/RECEIPT.json',
            A / 'actual_checkpoints/round1_repair/PROCESS_JOURNAL.json'}
D = A / 'contingent_credited_note_v2'
for path in D.rglob('*'):
    if not path.is_file() or path.is_symlink():
        continue
    relative = path.relative_to(D)
    # Synthetic copy fixtures stay private; complete journals/generators retain replay evidence.
    if relative.parts[:2] == ('private', 'custody_current') and len(relative.parts) > 3:
        continue
    selected.add(path)
for label in ['live_pr97_after_round1', 'main_after_round1_snapshot',
              'authenticate_prepared_package_v2', 'authenticate_v2_baseline_preservation']:
    selected.update(path for path in (A / 'actual_operations' / label).rglob('*')
                    if path.is_file() and not path.is_symlink())
rows = []
for path in sorted(selected):
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(C.resolve()):
        raise RuntimeError('Unsafe selected checkpoint body: ' + str(path))
    data = path.read_bytes()
    rows.append({'path': path.relative_to(C).as_posix(), 'bytes': len(data),
                 'sha256': hashlib.sha256(data).hexdigest()})
selection = {'schema': 'pr97-corrected-preparation-checkpoint-selection/v1', 'UTC': now,
             'operator_PID': os.getpid(), 'expected_main': 'bf5f7a735a853855ba4f86c58e579e4ca4a47f2a',
             'paths': [row['path'] for row in rows], 'pins': rows,
             'active_round2_review_excluded': True, 'controlled_links_not_staged': True,
             'duplicate_private_custody_fixtures_not_staged': True,
             'private_retained_evidence_not_deleted': True,
             'publication_authorized': False, 'new_central_proof_search_turns': 0}
destination = A / 'V2_PREPARATION_CHECKPOINT_SELECTION.json'
with destination.open('x') as stream:
    stream.write(json.dumps(selection, indent=2) + '\n')
print(json.dumps({'UTC': now, 'operator_PID': os.getpid(), 'selected_files': len(rows),
                  'selected_bytes': sum(row['bytes'] for row in rows),
                  'workflow_percent': 45, 'program_percent': 13/99*100,
                  'selection': str(destination)}))
