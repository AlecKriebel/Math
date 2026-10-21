"""Prepared final clearance after repaired packet and a clean NEW review03.

Does not relabel the first two adverse reviews, require two fictitious clean
verdicts, or claim that their different historical packets were identical.
"""
from pathlib import Path
from datetime import datetime
import json
from root_submission_gate import (A, P, AUTHOR_NAMES, SUBMISSION_NAMES, ORIGINAL_HEAD,
                                  CLEAR_STATUS, current_clearance, inventory, load, pin, utc)

assert not (A / 'PUBLISHING_CLEARANCE.json').exists()
author = load(A / 'preprint/REVIEW_PACKET_MANIFEST.json')['author_inputs']
assert set(author) == set(AUTHOR_NAMES) and len(author) == 8
assert {name: pin(A / 'preprint' / name) for name in AUTHOR_NAMES} == author
first = load(A / 'ROOT_PREPRINT_REVIEW01_VERIFICATION.json')
second = load(A / 'ROOT_PREPRINT_REVIEW02_VERIFICATION.json')
third = load(A / 'ROOT_PREPRINT_REVIEW03_VERIFICATION.json')
assert first['mandatory_findings'] == 1 and first['status'] == 'REVIEW_COMPLETE_PUBLICATION_BLOCKER_RETAINED'
assert second['status'] == 'REVIEW_COMPLETE_SUBSTANTIVE_HELPER_BLOCKER_RETAINED'
assert [finding['id'] for finding in second['findings']] == ['F01']
assert second['generic_helper_valid'] is False and second['main_theorem_valid']
assert third['status'] == 'REVIEW_COMPLETE_NO_UNRESOLVED_MANDATORY_FINDINGS'
assert third['mandatory_findings'] == 0 and third['closed_namespace_unchanged']
assert third['whole_verifier_output_compared'] and third['source_first_and_premath_gates_preserved']
assert third['sealed_author_inputs'] == author
assert third['main_theorem_valid'] and third['classical_mechanism_valid'] and third['generic_helper_valid']
assert third['all_required_source_scopes_read'] and third['full_packet_bytes_and_metadata_verified']
assert third['root_independent_controls_reproduced'] and third['root_negative_controls_reproduced']
native_comparison = load(A / 'ROOT_PREPRINT_REVIEW03_NATIVE_COMPARISON.json')
assert native_comparison['status'] == 'PASS_FULL_NATIVE_REVIEW03_DOCUMENT_AND_ALL_COMPONENT_STREAM_COMPARISON'
assert native_comparison['mathematical_fields_or_failure_streams_normalized'] is False
assert all(row['complete_native_documents_equal_except_explicit_actual_UTC_fields']
           and row['every_fresh_subprocess_stdout_and_stderr_complete_hash_and_length_match_original_native_receipt']
           for row in native_comparison['results'])
repair = load(A / 'ROOT_PUBLIC_FORMULA_REPAIR.json')
assert repair['inputs'] == author and repair['revision'] == '04'
assert repair['two_runtime_complete_output_bytes_equal'] and repair['actual_negative_run_count'] == 6
qualification = load(A / 'ROOT_MATHEMATICAL_ACCEPTANCE_QUALIFICATION.json')
assert qualification['main_theorem_valid'] and qualification['original_generic_helper_valid'] is False
assert qualification['historical_reports_and_code_preserved']
priority = load(A / 'ROOT_PRIORITY_ACCEPTANCE.json')
assert priority['status'] == 'PRIORITY_ACCEPTED_BOUNDED_APPLICATION_NO_FIRST_PRIORITY_CERTIFICATE'
assert not priority['first_priority_certified'] and not priority['first_application_certified']
evidence = load(A / 'ROOT_FINAL_CLOSED_EVIDENCE.json')
assert evidence['status'] == 'ALL_EIGHT_CLOSED_NAMESPACES_PINNED_AFTER_CLEAN_REVIEW03'
assert len(evidence['namespaces']) == 8
for name, expected in evidence['namespaces'].items():
    assert inventory(A / name) == expected

# Chronology uses native root records and actual builder captures, rather than
# approximate prose header times in historical reviewer notes.
source = load(A / 'ROOT_PREPRINT03_SOURCE_GATE.json')
first_math = load(A / 'ROOT_PREPRINT03_FIRST_ASSESSMENT_GATE.json')
assert source['status'] == 'NEW_THIRD_REVIEW_SOURCE_ONLY_FREEZE_READ_AND_PINNED'
assert first_math['status'] == 'NEW_THIRD_PREZIP_MATHEMATICAL_ASSESSMENT_READ_AND_PINNED'
assert first_math['zip_builder_helpers_supporting_narratives_prior_verdicts_not_yet_read_declared']
parse = lambda value: datetime.fromisoformat(value.replace('Z', '+00:00'))
assert parse(first['utc']) < parse(second['utc']) < parse(source['utc']) < parse(first_math['utc']) < parse(third['utc'])
immutable_names = [
    'ROOT_MATHEMATICAL_ACCEPTANCE.json', 'ROOT_MATHEMATICAL_ACCEPTANCE_QUALIFICATION.json',
    'ROOT_PRIORITY_ACCEPTANCE.json', 'ROOT_PUBLIC_FORMULA_REPAIR.json',
    'ROOT_PREPRINT_REVIEW01_SEAL.json', 'ROOT_PREPRINT_REVIEW02_SEAL.json',
    'ROOT_PREPRINT_REVIEW03_SEAL.json', 'ROOT_PREPRINT_REVIEW01_VERIFICATION.json',
    'ROOT_PREPRINT_REVIEW02_VERIFICATION.json', 'ROOT_PREPRINT_REVIEW03_VERIFICATION.json',
    'ROOT_PREPRINT03_SOURCE_GATE.json', 'ROOT_PREPRINT03_FIRST_ASSESSMENT_GATE.json',
    'ROOT_PREPRINT02_TIMING_CORRECTION_READBACK.json', 'ROOT_FINAL_CLOSED_EVIDENCE.json',
    'ROOT_PREPRINT_REVIEW03_NATIVE_COMPARISON.json']
time = utc()
clear = dict(utc=time, status=CLEAR_STATUS, pr=344, problem_id='30005649',
             original_head=ORIGINAL_HEAD, original_status='claimed_solved', author_turns='1/5',
             revision='04', sealed_author_inputs=author,
             sealed_submission_files=[dict(path=name, **author[name]) for name in SUBMISSION_NAMES],
             upload_files=['qss-self-duality-note.pdf', 'qss-self-duality-verification.zip'],
             immutable_root_artifact_pins={name: pin(A / name) for name in immutable_names},
             successive_new_full_reviews=3, final_clean_review=3,
             unresolved_mandatory_findings=0, historical_adverse_reviews_retained=True,
             historical_findings_repaired=['B1', 'F01/root B2'],
             historical_review_packets_differed=True,
             final_third_review_of_current_eight_author_inputs=True,
             mathematical_resolution_percent=100, bounded_priority_percent=100,
             preprint_preparation_percent=100, acceptance_publication_workflow_percent=75,
             first_priority_certified=False, first_application_certified=False,
             continuing_openness_certified=False,
             exact_live_actual_merge_publication_tracker_pending=True,
             source_first_and_premath_root_records=[source['utc'], first_math['utc']],
             disclosure='Extensive AI use; unrefereed; no independent external human peer review.',
             scope='Explicit negative answer to the higher-rank question after Takao Proposition2, printed2479 of OWR42/2023, for every p>3 and n>=3 over k=F_p algebraic closure. Established mechanisms credited; bounded primary-literature and version/access gaps retained.')
(A / 'PUBLISHING_CLEARANCE.json').write_text(json.dumps(clear, indent=2) + '\n')
current_clearance()
criteria = load(A / 'acceptance_criteria.json')
criteria.update(updated_utc=time, fresh_preprint_reviews_pending=False,
                third_new_full_review_pending=False, preprint_preparation_percent=100,
                publishing_clearance=True, workflow_completion_percent=75,
                candidate_accepted=False, exact_live_root_and_whole_gates_pending=True,
                fresh_whole_exact_live_pending=True)
(A / 'acceptance_criteria.json').write_text(json.dumps(criteria, indent=2) + '\n')
(A / 'CURRENT_PREPRINT_STATUS.json').write_text(json.dumps(clear, indent=2) + '\n')
header = 'CONDITIONAL DRAFT: use only after separately recorded clean review03, root closure and publishing clearance.\n\n'
for name in ('accepted_pr_body.txt', 'merge_body.txt'):
    path = A / name
    text = path.read_text()
    assert text.startswith(header) and text.count(header) == 1
    path.write_text(text[len(header):])
line = ('\n' + time + ': PR344 repaired v04 eight-input packet cleared after third NEW full preprint adversary with zero unresolved mandatory findings, complete root read/reproduction and closed-evidence verification. Historical review01 B1 and review02 F01/root B2 remain adverse; both supporting defects were repaired globally in the current public derivative. Main theorem and deposit metadata unchanged. Mathematics/preprint100%, bounded priority100%, publication workflow75%; exact live/actual merge/production Zenodo/DOI/tracker pending. No first-priority or external human peer-review certificate.\n')
for path in (A / 'RESEARCH_LOG.md', P / 'RESEARCH_LOG.md'):
    with path.open('a') as file:
        file.write(line)
print(json.dumps({key: value for key, value in clear.items() if key != 'immutable_root_artifact_pins'}, indent=2))
