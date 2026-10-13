"""Administrative preparation only; never executes mathematical or ROOT helpers."""
import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

FAMILY = Path(__file__).resolve().parent
ORIGINAL_PREPARER = FAMILY.parent / 'original_preparation_family'
HEAD = '4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29'


def utc(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def write(name, obj):
    (FAMILY / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')
def reference(path):
    data = path.read_bytes()
    return {'absolute_path': str(path), 'bytes': len(data), 'sha256': sha(data),
            'full_mode_07777': format(stat.S_IMODE(path.stat().st_mode), '04o')}


def main():
    auth = json.loads((ORIGINAL_PREPARER / 'ORIGINAL_AUTHENTICATION.json').read_bytes())
    accounting = json.loads((ORIGINAL_PREPARER / 'SOURCE_ACCOUNTING.json').read_bytes())
    source = json.loads((ORIGINAL_PREPARER / 'original/source_record.json').read_bytes())
    turns = json.loads((ORIGINAL_PREPARER / 'original/turns.json').read_bytes())
    assert auth['original_head'] == accounting['original_head'] == HEAD
    assert len(auth['original_science_files']) == 17
    assert accounting['raw_report_key_present'] is False
    assert accounting['SQL_selected_row']['report_is_SQL_NULL'] is False
    assert accounting['SQL_selected_row']['report_literal'] == '{}'
    assert 'upstream_report' not in source
    assert source['id'] == turns['problem_id'] == 30003354
    assert source['problem_number'] == 'OWR-15208-008'
    assert turns['budget'] == 5 and turns['substantive_proof_attempts'] == 1
    assert len(turns['turns']) == 1
    assert accounting['original_turns_used'] == 1 and accounting['original_turn_limit'] == 5
    assert accounting['original_turn_log_entry_count'] == 1
    assert accounting['original_status_file_present'] is False
    assert accounting['native_mutation'] is False
    results = json.loads((FAMILY / 'GEOMETRIC_CONTROL_RESULTS.json').read_bytes())
    assert results['control_count'] == 5 and results['finite_controls_are_not_universal_proof']
    receipts = json.loads((FAMILY / 'PRIMARY_SOURCE_RECEIPTS.json').read_bytes())
    assert len(receipts['private_reading_inputs']) == 12
    assert not receipts['private_cache_required_by_ROOT_close']
    for name in ('root_close_geometric_family.py', 'root_readback_geometric_family.py'):
        assert (FAMILY / name).is_file()  # Presence only; never import/run them.

    refs = [reference(ORIGINAL_PREPARER / p) for p in (
        'original/CANDIDATE.md', 'original/source_record.json', 'original/turns.json',
        'original/provenance.json', 'ORIGINAL_AUTHENTICATION.json', 'SOURCE_ACCOUNTING.json')]
    assert refs[0]['sha256'] == '7f358fb1aaa73dc3cfd06c798c10f6afed65ee430b622b84b90f0554dd440e62'
    assert refs[1]['sha256'] == 'db344206d49d5d187bb23f7bfc0bc71c2f512d6eff7ccefcbaae02dcd9003b36'
    write('INPLACE_SOURCE_BINDINGS.json', {
        'schema': 'pr57-geometric-inplace-original-bindings/v1', 'utc': utc(),
        'original_head': HEAD, 'bindings': refs,
        'preparer_authentication_not_our_Git_authentication_or_ROOT_custody': True,
        'historical_primary_receipt_modes_are_as_measured_at_the_recorded_read': True,
        'private_primary_bodies_needed_by_ROOT_helpers': False,
        'private_primary_whole_bodies_excluded_from_fixed_index': True})
    write('AUDIT_ACCOUNTING.json', {
        'schema': 'pr57-geometric-audit-accounting/v1', 'utc': utc(),
        'operator_pid': os.getpid(), 'original_head': HEAD,
        'problem_id': '30003354', 'source_code': 'OWR-15208-008',
        'raw_report_key_present_as_preparer_records': False,
        'raw_report_interpretation': 'ABSENT; no raw value; absence is not null',
        'SQL_report_is_NULL_as_preparer_records': False,
        'SQL_report_literal_as_preparer_records': '{}',
        'SQL_empty_text_object_is_not_a_raw_report': True,
        'flat_original_upstream_report_field_present_directly_checked': False,
        'separate_prior_report_present_as_preparer_records': False,
        'raw_SQL_corpus_reread_by_this_family': False,
        'exact_preparer_accounting_reference': refs[-1],
        'original_science_files_as_preparer_authenticated': 17,
        'original_proof_attempts_used': 1, 'original_proof_attempt_limit': 5,
        'original_turn_log_entry_count': 1,
        'original_status_json_present': False,
        'original_draft_queue_status': 'claimed_solved', 'original_draft_queue_turns': '1/5',
        'native_status_at_preparer_read': 'queued', 'native_turns_at_preparer_read': '0/5',
        'native_status_is_not_original_draft_status': True,
        'audit_substantive_proof_attempt_increment': 0,
        'audit_native_queue_mutation': False, 'audit_Git_remote_paper_DOI_actions': False,
        'prior_PR56_auditor_role_disclosed': True,
        'historical_review_or_checker_bodies_read_or_replayed': False,
        'other_fresh_family_findings_used': False,
        'fresh_exact_successful_control_count': 5,
        'failed_dependency_run_successful_control_count': 0,
        'historical_author_90_independent_136_not_fresh_evidence': True,
        'finite_controls_are_not_the_universal_proof': True,
        'universal_derivation': 'GEOMETRIC_TOPOLOGY_REPORT.md',
        'priority': 'unconfirmed', 'human_or_refereed_acceptance': False})

    entries = [
        {'source': 'owr_2017', 'printed_pages': '149', 'private_layout_physical_lines': [716, 738],
         'selected_topics': 'Exact question, marked points, uniqueness, integer expectation',
         'rendered_private_pdf_page': 17},
        {'source': 'banakh_belegradek', 'printed_pages': '3', 'private_layout_physical_lines': [90, 120],
         'selected_topics': 'One additional diffeomorphism derivative, integer limitation',
         'rendered_private_pdf_page': 3},
        {'source': 'banakh_belegradek', 'printed_pages': '4', 'private_layout_physical_lines': [149, 165],
         'selected_topics': 'Smooth objects and compact-open integer/noninteger conventions',
         'rendered_private_pdf_page': 4},
        {'source': 'banakh_belegradek', 'printed_pages': '17-18', 'private_layout_physical_lines': [707, 778],
         'selected_topics': 'Sphere normalization, exact continuous bijection, noninteger theorem',
         'rendered_private_pdf_page': 17},
        {'source': 'banakh_belegradek', 'printed_pages': '19-20', 'private_layout_physical_lines': [815, 854],
         'selected_topics': 'Plane affine gauge, marked points, completeness growth, exact map',
         'rendered_private_pdf_page': 19},
        {'source': 'belegradek_hu_erratum', 'printed_pages': '711-712', 'private_layout_physical_lines': [23, 39],
         'selected_topics': 'Entire two-page erratum read; listed locators are the corrected theorem on p711',
         'rendered_private_pdf_page': 1}]
    write('SOURCE_SCOPE_LOCATORS.json', {
        'schema': 'pr57-geometric-selected-primary-locators/v1', 'utc': utc(),
        'receipt': 'PRIMARY_SOURCE_RECEIPTS.json', 'selected_read_locators': entries,
        'full_primary_PDF_access_acquired': True,
        'all_paper_proofs_or_current_priority_comprehensively_audited': False,
        'six_selected_rendered_pages_visually_inspected': True,
        'printed_page_and_physical_newline_locators_not_python_splitlines': True,
        'private_cache_absolute_path': str(FAMILY.parent / 'private_primary_reading_cache' / FAMILY.name),
        'whole_PDF_text_PNG_redistribution': False,
        'private_cache_retained_no_deletion_authorized': True,
        'ROOT_helpers_read_private_cache': False})
    write('READY.json', {
        'schema': 'pr57-geometric-family-ready/v1', 'utc': utc(), 'prepared_by_pid': os.getpid(),
        'original_head': HEAD, 'problem_id': '30003354', 'source_code': 'OWR-15208-008',
        'status': 'READY_FOR_ROOT_CUSTODY_AND_REVIEW',
        'mathematical_audit': 'PASS_UNIVERSAL_GEOMETRIC_DERIVATION',
        'scope': 'Every finite integer r>=0; plane and sphere; smooth complete strictly positive curvature',
        'remaining_mathematical_gap_found': None,
        'priority': 'unconfirmed', 'AI_reviewed_unrefereed': True,
        'fixed_index': 'SOURCE.json', 'fixed_index_self_indexed': False,
        'fixed_files_full_mode_07777': '0444', 'fixed_directories_full_mode_07777': '0755',
        'ROOT_close_helper': 'root_close_geometric_family.py',
        'ROOT_readback_helper': 'root_readback_geometric_family.py',
        'ROOT_helpers_executed_by_family': False, 'ROOT_closed_or_readback_claimed': False,
        'native_Git_remote_publication_paper_DOI_actions': False,
        'whole_publication_primary_PDF_text_PNG_bodies_in_index': False,
        'private_primary_cache_required_by_ROOT_helpers': False,
        'prior_report_accounting': 'Raw ABSENT; SQL non-NULL TEXT {}; flat upstream_report ABSENT',
        'original_draft_proof_attempt_budget': '1/5', 'audit_proof_attempt_increment': 0,
        'fresh_exact_controls': 5, 'failed_environment_capture_preserved': True,
        'source_only_helpers_need_parent_owned_capture_if_executed': True})
    with (FAMILY / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n- 2026-10-03 14:30:34–14:30:41 UTC — Acquired all three exact primary PDFs; '
                  'selected scope passages and six private renders read. Owned operator 91565, '
                  'nine Poppler children exit 0. Private whole bodies excluded. Audit 75%.\n')
        log.write('- 2026-10-03 14:30:48 UTC — First exact controls failed before evaluation: '
                  'missing SymPy, child 91703 exit 1, full stderr retained. No mathematical '
                  'failure or successful-control count inferred. Audit 73%.\n')
        log.write('- 2026-10-03 14:33:16 UTC — Separate standard-library rational-jet operator '
                  '93651 passed five exact controls. Universal proof separate. Added uncorrected '
                  'critical negative-curvature control and fixed inverse function-jet failure. '
                  'Audit 85%.\n')
        log.write(f'- {utc()} — Final universal geometric report and typed source/budget '
                  'accounting complete; no math gap found. Historical checker bodies and other '
                  'fresh-family findings unused. Administrative source-only handoff prepared; '
                  'ROOT helpers unexecuted. Audit 95%.\n')
    print(json.dumps({'operator_pid': os.getpid(), 'utc': utc(), 'prepared': True,
                      'inplace_original_reference_count': len(refs), 'primary_cache_read': False,
                      'mathematical_operators_or_ROOT_helpers_executed': False,
                      'finite_exact_successful_controls': 5, 'proof_attempt_increment': 0}, sort_keys=True))


if __name__ == '__main__': main()
