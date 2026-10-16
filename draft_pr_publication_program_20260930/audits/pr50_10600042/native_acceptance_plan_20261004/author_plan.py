#!/usr/bin/env python3
"""Author a prospective PR50 plan from already captured read-only observations."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

OUT = Path(__file__).resolve().parent
REPO = Path('/Users/alec/Documents/Math')
EXPECTED = REPO / 'draft_pr_publication_program_20260930/audits/pr50_10600042/native_acceptance_plan_20261004'
if OUT != EXPECTED:
    raise RuntimeError('Unexpected output directory')

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def binding(path):
    body = path.read_bytes()
    return {'path': str(path), 'sha256': sha(body), 'bytes': len(body),
            'full_mode': stat.S_IMODE(path.stat().st_mode)}

def write_json(name, value):
    path = OUT / name
    if path.exists():
        raise RuntimeError('Refuse overwrite: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')

started = utc()
receipt_dir = OUT / 'actual_plan_authoring'
receipt_dir.mkdir()
source = Path(__file__).read_bytes()
(receipt_dir / 'PRELAUNCH_SOURCE.py').write_bytes(source)
write_json('actual_plan_authoring/PRELAUNCH.json', {'utc': started, 'actual_pid': os.getpid(),
    'script': binding(Path(__file__)), 'prelaunch_source': binding(receipt_dir / 'PRELAUNCH_SOURCE.py'),
    'write_boundary': str(OUT), 'no_repository_or_external_mutations': True})
obs = json.loads((OUT / 'OBSERVATIONS.json').read_text())
orig = obs['original_source_record']
current = obs['current_selected_sources']
problem = current['cache/problems.json']
report = current['cache/research_results.json']
catalog = current['catalog.json']
assessment = current['assessments.json']
dataset = json.loads((OUT / 'source_snapshots/dataset_manifest.json').read_text())
typed_hash = lambda value: sha(json.dumps(value, sort_keys=True).encode())
identity = {'dataset_revision': dataset['revision'],
    'source_record_hash': typed_hash(problem), 'source_report_hash': typed_hash(report),
    'review_hash': typed_hash([problem, report]),
    'statement_hash': sha(problem['statement'].encode()),
    'raw_problem_equals_original_typed_record': problem == orig['problem'],
    'raw_report_equals_original_typed_report': report == orig['upstream_report'],
    'hash_recipe': 'SHA256 of UTF-8 json.dumps(value, sort_keys=True) with Python defaults; statement_hash uses exact UTF-8 statement.',
    'current_catalog_and_assessment_hashes_match':
        catalog['review_hash'] == assessment['review_hash'] == typed_hash([problem, report]) and
        catalog['statement_hash'] == assessment['statement_hash'] == sha(problem['statement'].encode())}
if not all(identity[k] for k in ('raw_problem_equals_original_typed_record',
    'raw_report_equals_original_typed_report', 'current_catalog_and_assessment_hashes_match')):
    raise RuntimeError('Selected source mismatch')
for source_binding in obs['large_source_bindings_only']:
    name = Path(source_binding['path']).name
    if name in dataset['files']:
        expected = dataset['files'][name]
        if source_binding['sha256'] != expected['sha256'] or source_binding['bytes'] != expected['bytes']:
            raise RuntimeError('Raw cache no longer matches dataset manifest')
pins = {'even_strand_markov.tex': 'cd141a55da2241764d4fbbe8a145d8d4be29370803e24704e645c60cf8f2d0dc',
        'even_strand_markov.pdf': 'ea3e6f6b647de0acd71219a2840ee515fe6548f7d4dbba828558b7fb0e01624e',
        'even-strand-markov-verification-v1.zip': '2b519b4ba59ccd2e5ed9c88a79aa96d273481b45bb18b6a1ecc6fcbd0381a48d',
        'zenodo-deposit.json': '4636f8b65dc2906097967a3fa963b0ae0fc652d645e2a5bcf17558c6f7493b82'}
if {k:v['sha256'] for k,v in obs['package_bindings_dated_only'].items()} != pins:
    raise RuntimeError('Package pin mismatch')
turns = obs['original_turn_ledger']
if len(turns) != 1 or turns[0]['turn'] != 1 or turns[0]['outcome'] != 'candidate':
    raise RuntimeError('Unexpected original turn ledger')
if obs['original_status']['turns_used'] != 1 or obs['original_status']['turn_limit'] != 5:
    raise RuntimeError('Original budget mismatch')
minimal = ['unsolved_math_prioritization/QUEUE.md', 'unsolved_math_prioritization/state.json',
    'unsolved_math_prioritization/history.jsonl',
    'unsolved_math_prioritization/attempts/10600042/acceptance.json',
    'unsolved_math_prioritization/attempts/10600042/CURRENT_RESULT.md']
scope = 'Explicit four classical and eight virtual reversible algebraic scheme families classify ordinary oriented unframed link closures using only even-strand braid states, with arbitrary finite word blocks and the stated syntactic supports.'
plan = {'schema': 'pr50-small-prospective-native-acceptance-plan/v1',
    'created_utc': utc(), 'created_by_pid': os.getpid(), 'pr': 50, 'problem_id': '10600042',
    'problem_code': 'AMR-105-0042', 'status': 'PROPOSED_READONLY_NO_ACCEPTANCE_CONFERRED',
    'submitted_head': obs['original_head'], 'submitted_status': 'claimed_solved',
    'original_budget': '1/5', 'exact_claim_for_future_records': scope,
    'plan_preparation_percent': 100, 'actual_native_acceptance_percent': 0,
    'new_mathematical_or_priority_approval': False, 'actual_DOI': None,
    'actual_tracker_range': None, 'actual_original_integration_merge_commit': None,
    'actual_native_acceptance_commit': None, 'actual_remote_PR_disposition_receipt': None,
    'observations': binding(OUT / 'OBSERVATIONS.json'), 'current_selected_identity': identity,
    'package_bindings_dated_only': obs['package_bindings_dated_only'],
    'original_scientific_files_to_preserve_exactly': obs['original_files'],
    'minimal_prospective_administrative_paths': minimal,
    'original_merge_paths': [x['canonical_path'] for x in obs['original_files']] + [minimal[0]],
    'QUEUE_only_authorized_target_cells': ['Status', 'Turns', 'Findings', 'DOI'],
    'QUEUE_future_status': 'preprint_published', 'QUEUE_future_turns': '1/5',
    'QUEUE_future_findings': 'Use an actual publication date and concise final-paper scope, credited unrestricted inputs, bounded diagnostics, priority limits, actual review references, and final package pointer; remove operative wording identifying the result as merely a draft PR.',
    'preserve_other_QUEUE_cells_rows_and_header': True,
    'state_and_history_schema_recommendation': {
        'schema_example': 'Existing eligible PR16 / 30000439 acceptance_mirror_import record; structure only, with no copied PR16 statuses, evidence or content.',
        'key': '10600042', 'event': 'acceptance_mirror_import', 'status': 'preprint_published',
        'turns_used': 1, 'turn_limit': 5,
        'source_identity_fields': ['source_record_hash', 'source_report_hash', 'statement_hash', 'review_hash'],
        'actual_at_required': True, 'actual_DOI_required': True,
        'event_id': 'Unique hash of the final actual event payload, consistently defined and recomputed; never reuse another event_id.',
        'append_same_event_to_history': True,
        'evidence_fields': ['accepted_source path/SHA256', 'final manuscript/PDF/ZIP and deposit-manifest path/SHA256',
            'canonical_acceptance path/SHA256', 'original_budget_ledger path/SHA256',
            'reviewed_head', 'exact_claim', 'priority and final clean reviews path/SHA256',
            'publication record/DOI/public-file readback path/SHA256',
            'tracker range/row readback path/SHA256', 'actual original integration merge_commit',
            'authorization from the user goal', 'import_is_present_day_mirror=true',
            'historical_transitions_asserted=false', 'queue_explicit_budget=1/5'],
        'no_synthetic_ready_candidate_independent_verification_or_proof_attempt_events': True,
        'preserve_all_other_state_records_and_history_prefix': True,
        'baseline_counts_dated_only': {'state_entries': obs['native_state_entries'], 'turns': obs['native_total_turns']},
        'actual_execution_delta': {'new_target_entries': 1, 'imported_original_turns': 1, 'new_history_events': 1}},
    'canonical_acceptance_recommendation': {
        'schema': 'pr50-published-native-acceptance/v1',
        'historical_original': {'head': obs['original_head'], 'files': 'Exact 15-file table pinned by ORIGINAL_MANIFEST.json',
            'candidate_sha256': '749f55ab651476c5f3c7868fed2b9f06809a38518057e33414966cb6f4f253bc',
            'role': 'Historical 2026-09-30 candidate and review, preserved unchanged; never relabeled as final submitted source.'},
        'accepted_final': {'source': 'draft_pr_publication_program_20260930/audits/pr50_10600042/publication_package_v1/even_strand_markov.tex',
            'PDF': 'draft_pr_publication_program_20260930/audits/pr50_10600042/publication_package_v1/even_strand_markov.pdf',
            'ZIP': 'draft_pr_publication_program_20260930/audits/pr50_10600042/publication_package_v1/even-strand-markov-verification-v1.zip',
            'deposit_manifest': 'draft_pr_publication_program_20260930/audits/pr50_10600042/publication_package_v1/zenodo-deposit.json',
            'sha256': pins, 'actual_final_clean_review_receipts_required': True,
            'actual_DOI_public_files_tracker_and_original_merge_receipts_required': True},
        'limits': ['Credited unrestricted Alexander/Markov inputs are imported.',
            'No first discovery, current openness, minimality, uniform geometric locality, or certificate-search complexity claim.',
            'No plat, framed, transverse or welded classification.',
            'Finite diagnostics supplement the universal proof.',
            'Extensive AI use; unrefereed; no conventional human peer review or formal proof certification.'],
        'avoid_self_referential_commit_or_hash': 'Acceptance references the already created original integration merge; post-acceptance receipt outside these native files may later bind the native administrative commit. Do not embed the commit that contains acceptance.json in that file.'},
    'CURRENT_RESULT_recommendation': 'Short human-readable pointer to actual final package and DOI, canonical acceptance, tracker readback and reviews; explicitly identify original CANDIDATE/README/status/turns/review as historical 2026-09-30 bodies.',
    'required_execution_gates': ['Fresh exact claimed_solved PR50 gate with exact head unchanged.',
        'ROOT completes fresh independent whole-package review/repair closure on the exact final bytes.',
        'Actual successful Zenodo publication with real DOI and public file/metadata verification.',
        'Exactly one checked tracker row for that DOI; no duplicate.',
        'Authorized exclusive shared-chat Git-writer window on main; fresh native/index/foreign-body/source baseline.'],
    'preferred_future_integration': [
        'Within an exclusive writer window, perform the normal two-parent no-ff local merge of exact original head into fresh current main with --no-commit, preserving all 15 original scientific blobs/modes.',
        'Reconcile only the selected QUEUE Status/Turns/Findings/DOI cells into the fresh current queue body, using the actual final publication. Preserve all unrelated bytes; inspect the complete real staged domain.',
        'Create the original integration merge commit first. Its first parent is the fresh premerge main, second parent the exact original head. This supplies an actual merge hash for the native acceptance evidence.',
        'In a separate small administrative commit, add acceptance.json/CURRENT_RESULT.md and one actual target state/history import event referencing that real merge and completed publication. This avoids hash/commit circularity. Do not add an extra proof turn.',
        'Verify both commits and the original 15 bodies before ordinary non-force push; independently read back remote main/tree/parents, real PR disposition, target queue/state/history, DOI/public files and tracker row.'],
    'shared_writer_and_race_rules': ['Preserve foreign dirty bodies/modes and all unrelated state/queue/history.',
        'If foreign staged entries exist, defer until the owner has completed them and the index is clean; never reset, stash, unstage or commit foreign entries.',
        'Do not hold Git standard index.lock across its merge/add/commit operations; Git needs the lock itself.',
        'On an unexpected source conflict, source identity change, wider stage, remote race or new reviewed bytes, stop that mutation phase and recapture/review.',
        'Do not claim merged until actual GitHub metadata confirms disposition; preserve genuine failures and partial receipts.'],
    'merge_base_dated': obs['actual_merge_base'],
    'conflict_observation': 'GitHub reports CONFLICTING/DIRTY. QUEUE is the only original PR path changed on main since the actual merge base; source conflict is not expected from this dated selected-path observation.',
    'historical_baseRefOid_not_current_main_authority': obs['pr50']['baseRefOid'],
    'no_large_general_acceptance_machinery_needed': True,
    'no_queue_status_turn_rank_sync_command_proposed': 'queue.py status/turn would reconstruct lifecycle or add a turn and rank rewrites broad generated artifacts; use the narrow documented present-day import schema.',
    'no_dependency_on_excluded_PR48_or_PR49': True,
    'no_historical_inventory_rewrite': True,
    'no_prior_family_source_edits_or_external_individual_contact': True,
    'ROOT_owns_all_future_mutations': True}
write_json('PLAN.json', plan)
table = ['| Historical relative path | Git mode | Git blob SHA-1 | SHA-256 | Bytes |',
         '|---|---|---|---|---:|']
for row in obs['original_files']:
    rel = row['canonical_path'].split('/10600042/', 1)[1]
    table.append(f"| `{rel}` | `{row['git_mode']}` | `{row['git_blob']}` | `{row['sha256']}` | {row['bytes']} |")
(OUT / 'ORIGINAL_BLOBS.md').write_text('# Exact original PR50 scientific body mapping\n\n'
    'Each path below maps to `unsolved_math_prioritization/attempts/10600042/`. All 15 bodies match the exact original head and existing `A50/original` custody. Custody copies are mode 0444; Git mode is 100644 and is the native integration authority. No body edits are proposed.\n\n'
    + '\n'.join(table) + '\n')
report_text = f'''# PR50 prospective native acceptance plan

This is an administrative read-only plan for eligible PR50, numeric target 10600042 / AMR-105-0042. It confers no mathematical, priority, publication or merge approval. The exact submitted head is `{obs['original_head']}`; its exact queue row is `claimed_solved`, 1/5. At the genuine {obs['ended_utc']} observation, GitHub reports OPEN draft, CONFLICTING/DIRTY. Local HEAD/main/origin-main and remote main were `{obs['refs_before'][0]}`. The index was empty; unrelated unstaged work exists. ROOT owns every future mutation.

## Verified source and budget custody

All fifteen original scientific bodies were fully read and byte-checked against the exact Git tree, `ORIGINAL_MANIFEST.json` and `A50/original`. Their native path/blob/mode/SHA-256/byte mapping is in `ORIGINAL_BLOBS.md` and `PLAN.json`. All fifteen native target paths are absent. The original candidate SHA-256 is `749f55ab651476c5f3c7868fed2b9f06809a38518057e33414966cb6f4f253bc`; it is a historical candidate, not the final source. Keep original CANDIDATE, README, status, research log, turn ledger and review bodies unchanged, including dated claims and historical execution metadata.

The current raw problem and prior report exactly equal the original typed source record. Dataset revision is `{identity['dataset_revision']}`. Current catalog and assessment agree on review hash `{identity['review_hash']}` and exact statement hash `{identity['statement_hash']}`. Their current selected assessment has no holds; no selected assessment-history event or related-target group exists. Typed problem/report hashes and raw-file manifest matches are recorded in `PLAN.json`; only selected source rows were extracted, with bindings for the complete large files.

The original `turns.jsonl` contains exactly one real candidate response, at 2026-09-30T06:14:00Z. Its SHA-256 is `8019c12dbf63f2b3651d48e20a46320b2381683ca6f8b312a7b2d94ae831c058`. Historical status agrees: one turn used, limit five. Current native QUEUE says queued 0/5; state has no 10600042 key and history has no event for it. This dated baseline has {obs['native_state_entries']} state entries and {obs['native_total_turns']} total imported turns. At actual execution use a fresh baseline and add exactly one target, its one original turn, and one present-day `acceptance_mirror_import` event. Never fabricate ready/candidate/verification transitions or append a fresh proof-attempt event.

## Small prospective native scope

The original merge imports the fifteen exact scientific blobs and reconciles QUEUE. The only additional administrative paths are:

''' + '\n'.join('- `' + path + '`' for path in minimal) + f'''

After actual clean whole-package review, actual Zenodo publication/public readback and a checked nonduplicate tracker row, change only target Status/Turns/Findings/DOI cells: `preprint_published`, `1/5`, concise final result and qualification pointers, and the real DOI. Preserve every other target cell, every other row, queue header, all other state entries and the full history prefix. Broad regeneration or lifecycle commands are unnecessary for this bounded import and could rewrite unrelated findings/scores.

Canonical `acceptance.json` and `CURRENT_RESULT.md` must explicitly distinguish the historical 2026-09-30 original files from accepted final `publication_package_v1` source/PDF/ZIP. The dated final pins agree exactly with ROOT's task: source `{pins['even_strand_markov.tex']}`; PDF `{pins['even_strand_markov.pdf']}`; ZIP `{pins['even-strand-markov-verification-v1.zip']}`; deposit manifest `{pins['zenodo-deposit.json']}`. These bindings alone do not establish review completion or publication. Actual DOI, tracker row, fresh clean review evidence and merge receipts remain null in this proposal.

Use the existing eligible PR16 present-day import record as a field-shape example. Bind the original source and turn ledger, actual final artifacts/manifest, scope, credited inputs and priority limits, actual clean reviews, public DOI/files, tracker readback, canonical acceptance and actual original integration merge. State and history should contain the same single real event, with an actual timestamp and fresh event identity. Do not copy PR16 evidence or any old PR18 scientific detail. The final scope is ordinary oriented unframed classical/virtual closures with arbitrary finite word blocks and stated supports; preserve no-first-priority/current-openness, locality/minimality, imported-theorem and AI/unrefereed qualifications.

## Proposed integration mechanism

1. ROOT first completes the fresh final whole-package review/repair gate, publishes the exact intended manifest using the repository Zenodo kit, verifies the actual DOI and public bytes/metadata, and appends/readbacks one authorized tracker row. A failed or incomplete phase does not become PASS. This plan has no dependency on excluded PR48/49; the earlier dated ROOT decision's scheduling qualifier is not an operative gate here.
2. Within an authorized exclusive shared-chat writer window on main, recapture current local/remote main, exact PR50 head/eligibility, target source and native baselines, owned-path cleanliness, foreign dirty bodies/modes and the full actual index. If foreign entries are staged, preserve them and wait for their owner to finish; do not reset, stash, unstage or commit them. Do not hold Git's standard index lock across Git operations.
3. Perform the normal local `git merge --no-ff --no-commit {obs['original_head']}` into fresh main. This is a proposed command, never executed here. Actual common base is `{obs['actual_merge_base']}`; GitHub's historical baseRefOid `{obs['pr50']['baseRefOid']}` is not current-main authority. QUEUE is the only overlapping original changed path. Reconcile the selected final-publication cells into the fresh current QUEUE body; never take the full old queue. Preserve all fifteen original bodies/modes exactly. An unexpected scientific conflict or wider stage stops the phase for inspection.
4. Create the true two-parent original integration merge first, with current premerge main as first parent and exact original head as second parent. Then create a small native administrative commit containing the canonical records and the one state/history event, now referencing the actual known merge hash. This ordering avoids trying to embed a commit's own hash in its files. A post-acceptance receipt outside those native files can later bind the administrative commit. Verify the complete authorized stage and unrelated preservation before an ordinary non-force push of the completed result. A remote race requires fresh reconciliation.
5. Independently read back remote tree/parents, actual GitHub disposition, original fifteen hashes/modes, final canonical pointers, four target queue cells, one state/history import, 1/5 budget, DOI/public bytes and tracker row. The server currently reports conflict; a server merge is an alternative only after fresh mergeability/head checks and still requires separate native reconciliation. Do not claim GitHub marked merged until metadata confirms it.

The preparation helper's actual PID is {obs['actual_pid']}; all 28 read-only command streams, child PIDs, timestamps and source snapshots are retained in `actual_readonly_observation`. The authoring helper writes this plan folder only. No native, Git index/ref, PR, Zenodo, Sheets or prior-family mutation was performed. Plan preparation 100%; actual native acceptance 0%; new mathematical/priority approval 0%.
'''
(OUT / 'REPORT.md').write_text(report_text)
(OUT / 'RESEARCH_LOG.md').write_text(f'''# PR50 native acceptance preparation log

- {obs['started_utc']}: Read-only selected observation started. Scope limited to prospective PR50 acceptance. Current goal's exact claimed_solved filter and both AGENTS files read. Plan preparation estimate 30%; actual native acceptance 0%; new scientific approval 0%.
- {obs['ended_utc']}: Genuine capture completed under PID {obs['actual_pid']}, with all 28 command streams retained. Exact fifteen original bodies, one-turn ledger, current source identity and native absence verified. GitHub reports QUEUE-related conflict; index empty at observation, foreign unstaged work preserved. Plan preparation estimate 70%; actual native acceptance 0%; new scientific approval 0%.
- {utc()}: Authored minimal five-path administrative plan, exact original blob table and source/schema recommendations. Publication/review/DOI/tracker gates remain prospective; no fabricated lifecycle or merge hash. Two-commit ordering supplies real original merge evidence without circular hashes. Plan preparation estimate 100%; actual native acceptance 0%; new scientific approval 0%.
''')
outputs = ['PLAN.json', 'REPORT.md', 'ORIGINAL_BLOBS.md', 'RESEARCH_LOG.md']
write_json('READY.json', {'schema': 'pr50-native-acceptance-plan-ready/v1', 'created_utc': utc(),
    'actual_author_pid': os.getpid(), 'status': 'PROPOSED_READONLY_PLAN_ONLY',
    'outputs': [binding(OUT / name) for name in outputs], 'plan_preparation_percent': 100,
    'actual_acceptance_percent': 0, 'math_or_priority_approval': False,
    'source_identity_checked': identity, 'only_written_directory': str(OUT)})
write_json('actual_plan_authoring/RECEIPT.json', {'actual_pid': os.getpid(),
    'started_utc': started, 'ended_utc': utc(), 'source': binding(Path(__file__)),
    'prelaunch_source': binding(receipt_dir / 'PRELAUNCH_SOURCE.py'),
    'outputs': [binding(OUT / name) for name in outputs + ['READY.json']],
    'repository_mutations': [], 'external_mutations': []})
print(json.dumps({'status': 'PROPOSED_READONLY_PLAN_COMPLETE', 'pid': os.getpid(),
                 'outputs': outputs, 'plan_preparation_percent': 100, 'actual_acceptance_percent': 0}))
