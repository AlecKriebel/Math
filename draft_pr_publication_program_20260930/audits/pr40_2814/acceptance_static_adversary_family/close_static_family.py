#!/usr/bin/env python3
"""Compose and close only this NEW static adversary's first-party evidence."""
import datetime
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
PREP = AUDIT / 'acceptance_preparation_family'
REPO = Path('/Users/alec/Documents/Math')


def sha(raw): return hashlib.sha256(raw).hexdigest()
def load(p): return json.loads(p.read_bytes())
def row(p):
    raw = p.read_bytes()
    return {'path': p.relative_to(REPO).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}
def dump(name, value):
    p = HERE / name
    with p.open('x') as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write('\n')


def main():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    prep_sha = 'a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b'
    assert sha((PREP / 'PREPARATION_MANIFEST.json').read_bytes()) == prep_sha
    prep = load(PREP / 'PREPARATION_MANIFEST.json')
    assert len(prep['files']) == 12
    for v in prep['files']:
        raw = (PREP / v['path']).read_bytes()
        assert len(raw) == v['bytes'] and sha(raw) == v['sha256']
    inspection = load(HERE / 'inspect_static_inputs_actual_capture/stdout.bin')
    controls = load(HERE / 'independent_static_controls_actual_capture/stdout.bin')
    captures = [load(HERE / n / 'CAPTURE.json') for n in ['inspect_static_inputs_actual_capture', 'independent_static_controls_actual_capture']]
    assert all(c['actual_execution'] is True and c['exit_code'] == 0 and c['reviewed_helpers_executed'] is False for c in captures)
    findings = [
        {'id': 'S1', 'priority': 'P1', 'kind': 'scientific_attribution', 'mandatory': True,
         'summary': 'Published Kuhlmann incorrectly credited for nonorientable cusps; Xia omitted',
         'locations': ['SCIENTIFIC_SCOPE.json credited_existing_coverage[2]', 'DRAFT_FINAL_PLAN.json scientific_scope', 'pr40_guards.py:230,232,300', 'integrate_reviewed_partial.py:102'],
         'correction': 'Split Kuhlmann1.1 orientable coverage and Xia1.2/4.1 direct nonorientable coverage with retained qualifications',
         'target_counterexample': False},
        {'id': 'S2', 'priority': 'P2', 'kind': 'actual_capture_validation', 'mandatory': True,
         'summary': 'Nonempty clock strings do not validate parseability, UTC or ordering',
         'locations': ['pr40_guards.py:262'], 'correction': 'Require timezone-aware UTC clocks and finish at or after start'},
        {'id': 'S3', 'priority': 'P2', 'kind': 'actual_capture_closure', 'mandatory': True,
         'summary': 'stderr may alias prelaunch source; four claimed files collapse to three',
         'locations': ['pr40_guards.py:266-268'],
         'stdout_equals_stderr_already_rejected': True,
         'correction': 'Require distinct capture/source/stdout/stderr filenames and full bound streams'},
        {'id': 'S4', 'priority': 'P2', 'kind': 'exclusive_publication', 'mandatory': True,
         'summary': 'exists check followed by os.replace overwrites an intervening target',
         'locations': ['pr40_guards.py:156-163'],
         'correction': 'Use atomic non-overwrite publication when exclusive=True; preserve original failure/evidence'},
        {'id': 'S5', 'priority': 'P3', 'kind': 'dated_rebase_contract', 'mandatory': True,
         'summary': 'Undated reason passes a guard whose contract requires a dated reason',
         'locations': ['CONTRACT.md:21', 'pr40_guards.py:273'],
         'correction': 'Require concrete root-reviewed UTC rebase metadata and verify its required date or accurately revise the contract',
         'fresh_native_HEAD_or_prior39_bypass_claimed': False},
        {'id': 'S6', 'priority': 'P3', 'kind': 'next_target_metadata', 'mandatory': True,
         'summary': 'PR40 completion leaves current_pr at40 rather than advancing to41',
         'locations': ['integrate_reviewed_partial.py:98'], 'correction': 'Advance next-target metadata to41',
         'discovery_lead': 'Root subsequent whole-source read; independently confirmed literal assignment and PR39 convention'},
    ]
    assessment = {
        'schema': 'pr40-independent-acceptance-static-adversary/v1',
        'status': 'REQUIRES_ACCEPTANCE_SOURCE_REVISION', 'pr': 40, 'problem_id': 2814,
        'closed_utc': now, 'reviewed_preparation_manifest_sha256': prep_sha,
        'reviewed_authored_members': 12, 'reviewed_source_programs': 5, 'reviewed_source_lines': 632,
        'reviewed_package_preserved_before_and_after': True,
        'findings': findings, 'findings_count': 6,
        'genuine_new_target_counterexamples': [], 'mandatory_frozen_SOURCE_STATUS_corrections': [],
        'original_and_current_mathematical_bounded_partial_unchanged': True,
        'scientific_acceptance_scope_new_attribution_regression': True,
        'own_data_inspection': {
            'status': inspection['status'], 'current_members': 239,
            'current_including_root_manifest': 240, 'current_JSON_including_root_manifest': 110,
            'dependencies': 216, 'actual_original_family_retained_members': 42,
            'actual_current_freeze_retained_members': 4, 'original_root_archive_source_files': 13,
            'authored_closed_family_members': [97, 38, 5, 7, 25], 'whole_foreign_members_separately_bound': 21,
        },
        'own_control_capture_receipts': [row(HERE / n / 'CAPTURE.json') for n in ['inspect_static_inputs_actual_capture', 'independent_static_controls_actual_capture']],
        'own_control_results': row(HERE / 'independent_static_controls_actual_capture/stdout.bin'),
        'own_control_status': controls['status'],
        'proposed_or_old_verifier_import_compile_or_execution': False,
        'Git_SQL_native_shared_remote_writes': False, 'outside_communication': False,
        'actual_future_final_reconciliation_or_acceptance_or_prior39_or_native_mirror_claimed': False,
        'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None,
        'full_problem_solved': False, 'partial_valid': True, 'novelty_claimed': False,
        'source_hold': True, 'paper_or_new_DOI_or_tracker': False,
        'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0,
        'audit_turns': 0, 'mathematical_discovery_completion_percent': 0,
        'static_audit_completion_percent': 100,
        'science_reading_qualification': 'Prior sealed complete operative reading/reconstruction and disclosed raw-background exposure; no renewed unexposed independence or recursive foundational recertification claimed',
        'root_followup': 'New adjacent closed acceptance revision and fresh static review before actual gates; do not edit any closed scope',
    }
    dump('ASSESSMENT.json', assessment)
    prep_read = [row(PREP / v['path']) for v in prep['files']] + [row(PREP / 'PREPARATION_MANIFEST.json')]
    mirror = REPO / 'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py'
    prior39 = REPO / 'draft_pr_publication_program_20260930/audits/pr39_9500008/acceptance_preparation_family/integrate_reviewed_partial.py'
    receipt = {
        'schema': 'pr40-acceptance-static-whole-read-receipt/v1', 'utc': now,
        'all_twelve_preparation_members_and_manifest_full_read': prep_read,
        'all_five_sources_and_all_contracts_drafts_bindings_read': True,
        'source_lines': 632, 'bound_native_driver_full_source_static_read': row(mirror),
        'S6_prior39_next_target_convention_source_identity_not_execution': row(prior39),
        'full_proposed_sources_AST_data_parse_without_import_or_compile': True,
        'full_current_239_dependency216_capture42_plus4_recursive_data_inspection_result': row(HERE / 'inspect_static_inputs_actual_capture/stdout.bin'),
        'whole_current_mathematical_claims_source_proof_accounting_basis': [
            row(AUDIT / 'whole_current_source_first_family/FIRST_PARTY_MANIFEST.json'),
            row(AUDIT / 'whole_current_source_first_family/INDEPENDENT_PROOF_RECONSTRUCTION.md'),
            row(AUDIT / 'whole_current_source_first_family/PRIMARY_READING_SEAL.json'),
            row(AUDIT / 'ROOT_PARTIAL_SCOPE_CERTIFICATE.md'), row(AUDIT / 'ROOT_WHOLE_CURRENT_REVIEW.json'),
            row(AUDIT / 'source_snapshot/SOURCE_STATUS.md')],
        'genuine_old_pdf_full_reading_remains_previously_sealed_not_repeated_here': True,
        'new_foreign_PDF_or_HTML_copies': False,
        'full_retained_source_stream_JSON_topology_machine_checks_distinguished_from_new_human_PDF_reading': True,
        'source_first_independence_is_qualified_by_disclosed_old_raw_background_exposure': True,
        'S2_S3_S4_targeted_lead': 'Root requested checks after new whole-source reading; independently inspected predicates and reproduced local mechanisms',
        'no_reviewed_helper_or_old_verifier_import_compile_execution': True,
        'future_genuine_prior39_rebase_native_remote_records_remain_pending_requirements': True,
    }
    dump('READ_RECEIPT.json', receipt)
    with (HERE / 'RESEARCH_LOG.md').open('a') as stream:
        stream.write('\n' + now + ' — Static audit checkpoint100%, mathematical discovery0%. All632 lines/all12 authored preparation files read; independent whole-byte/typed/topology inspection passed current239+self,216deps,actual42+4,original13 and strict closed families. Six bounded findings: mandatory cusp attribution; capture clocks; stderr/source alias; exclusive-write absence race; dated-rebase contract; next-target metadata. Only own independent controls ran, complete actual sources/streams/receipts retained; no reviewed helper/old verifier import or execution, no Git/SQL/native/shared/remote writes, no outside communication. Original0/5,new0,audit0. New adjacent revision/review required before actual acceptance. This family now closes; follow-ups must be adjacent.\n')
    names, dirs = [], []
    for p in HERE.rglob('*'):
        assert not p.is_symlink() and (p.is_file() or p.is_dir())
        if p.is_file():
            names.append(p.relative_to(HERE).as_posix())
        else: dirs.append(p.relative_to(HERE).as_posix())
    assert 'FIRST_PARTY_MANIFEST.json' not in names
    rows = []
    for name in sorted(names):
        raw = (HERE / name).read_bytes()
        rows.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
    manifest = {'schema': 'pr40-acceptance-static-adversary-closure/v1', 'status': 'CLOSED_STATIC_REVIEW_REVISION_REQUIRED',
                'closed_utc': now, 'self_excluded_paths': ['FIRST_PARTY_MANIFEST.json'],
                'excluded_root_directories': [], 'foreign_exclusions': [], 'no_other_exclusions': True,
                'files_count': len(rows), 'files': rows, 'directories': sorted(dirs),
                'reviewed_preparation_manifest_sha256': prep_sha,
                'actual_reviewed_helpers_executed': False, 'scientific_acceptance_or_novelty_claimed': False}
    dump('FIRST_PARTY_MANIFEST.json', manifest)
    for p in HERE.rglob('*'):
        if p.is_file(): p.chmod(0o444)
    print(json.dumps({'status': manifest['status'], 'files_excluding_self': len(rows),
                      'manifest_sha256': sha((HERE / 'FIRST_PARTY_MANIFEST.json').read_bytes()),
                      'assessment_sha256': sha((HERE / 'ASSESSMENT.json').read_bytes()),
                      'report_sha256': sha((HERE / 'REPORT.md').read_bytes())}, sort_keys=True))


if __name__ == '__main__': main()
