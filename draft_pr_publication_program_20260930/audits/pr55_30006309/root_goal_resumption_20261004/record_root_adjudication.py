"""Record ROOT's dated scientific adjudication; perform no native/Git mutation."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os

F = Path(__file__).resolve().parent
A = F.parent
def sha(data):
    return hashlib.sha256(data).hexdigest()
def read(path):
    return json.loads(path.read_bytes())

fresh = A / 'prior_implication_fresh_adversary_20261004'
manifest = read(fresh / 'SELF_MANIFEST.json')
for entry in manifest['files']:
    path = Path(entry['path'])
    assert path.parent == fresh and path.is_file() and not path.is_symlink()
    body = path.read_bytes()
    assert len(body) == entry['bytes'] and sha(body) == entry['sha256']
assert sha((fresh / 'REPORT.md').read_bytes()) == 'cbdf013ee2b37f4fdcaea11c9438ca9e4a24237a8c60a51b369168008d43d273'
assert sha((fresh / 'VERDICT.json').read_bytes()) == 'f0f5d6b37c5b304a9e4ce45ae665e8c6606fde132b1ce23cca73e2999d80d227'
controls = read(fresh / 'CONTROL_RESULTS.json')
assert controls['all_passed'] is True
assert len(controls['checks']) == controls['control_count'] == 3355
assert all(c['passed'] is True and c['actual'] == c['expected'] for c in controls['checks'])
verdict = read(fresh / 'VERDICT.json')
assert verdict['substantive_mathematical_defect_within_scope'] is False
assert verdict['target_sized_unsupported_step'] is False
eligibility = read(F / 'CURRENT_ELIGIBILITY.json')
utc = dt.datetime.now(dt.timezone.utc).isoformat()
record = {
    'schema': 'pr55-root-scientific-and-scope-adjudication/v1',
    'UTC': utc, 'actual_recorder_pid': os.getpid(), 'PR': 55,
    'expected_original_head': '85c78d0cf3959d9d492a637cb90835ebc6a0e828',
    'eligible_intake_literal_status': 'claimed_solved',
    'eligibility_record_sha256': sha((F / 'CURRENT_ELIGIBILITY.json').read_bytes()),
    'goal_objective_sha256': '1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04',
    'root_personally_read_fresh_report_and_verdict_in_full': True,
    'root_personally_rechecked_original_candidate_and_two_universal_proof_families': True,
    'root_personally_read_both_prior_derivations': True,
    'root_scientific_verdict': 'sound_scoped_comparison_already_implied_by_prior_machinery',
    'scoped_mathematics_verified': True,
    'scope': 'n>=1; smooth polarized toric variety; complete very ample embedding by all lattice points of a Delzant polytope; degree>=2; full induced face lattices and massive boundary convention',
    'full_source_solved': False,
    'full_source_solved_reason': 'Only the candidate restored smooth model-comparison regime is verified; unrestricted introductory A and the broader combinatorial bijection are not certified.',
    'prior_formula': 'Esterov arXiv:0810.4996v3 Theorems4.10/5.10 and Definition5.12, with the explicit checked specialization retained here',
    'exact_earlier_printed_hurwitz_proof_located': False,
    'candidate_method_originality': 'unestablished',
    'new_solution_priority_clearance': False,
    'audited_outcome': 'already_solved',
    'outcome_qualification': 'prior-theorem-implied smooth model comparison; valid attributed partial record',
    'root_scope_interpretation': 'The current goal narrows intake to literal claimed_solved PRs. PR55 qualifies at intake. For a newly audited priority issue, ROOT applies the original human instruction to merge valid already_solved findings as partial results without a paper. This is an explicit ROOT interpretation of the combined instructions; the goal file itself does not contain that partial-outcome clause.',
    'original_human_outcome_instruction': 'If the result was already_solved or unsolved, audit the findings, and if valid and everything checks out, merge the PR as a partial result. Do not make a paper for these.',
    'root_authorizes_guarded_partial_disposition_under_combined_scope': True,
    'never_process_initially_nonclaimed_PRs': True,
    'PR50_exception_extended': False,
    'prepare_paper': False, 'Zenodo_upload': False, 'new_DOI': None,
    'tracker_append': False, 'new_central_proof_attempts': 0,
    'preserve_original_ledger_turns_used': 1,
    'preserve_original_scientific_bodies_as_dated_inputs': True,
    'fresh_current_acceptance_required': True,
    'raw_report_absent_SQL_report_nonNULL_empty_object_wrapper_null_distinguished': True,
    'fresh_exact_head_eligibility_required_before_merge': True,
    'actual_exclusive_writer_ack_required_before_Git_mutation': True,
    'native_Git_PR_mutation_performed_by_this_record': False,
    'formal_or_human_refereed_certification': False,
    'fresh_manifest_entries_verified': len(manifest['files']),
    'fresh_bounded_controls_verified': controls['control_count'],
    'controls_are_not_universal_proof': True,
    'scientific_review_estimate_percent': 100,
    'PR55_workflow_estimate_percent': 50,
    'dated_completed_program_fraction_percent': 4.040404
}
target = F / 'ROOT_REVIEW_AND_SCOPE_BINDING.json'
assert not target.exists()
target.write_text(json.dumps(record, indent=2) + '\n')
with (F / 'RESEARCH_LOG.md').open('a') as out:
    out.write(f'\n{utc} — ROOT personally adjudicated the full fresh adversary report and both prior derivations; verified all nine retained manifest artifacts and3,355 bounded controls. Scoped comparison sound; earlier Esterov machinery sufficient. No exact earlier printed Hurwitz proof or candidate-method priority established; broader source not certified. Record ROOT intake/outcome scope interpretation explicitly. Scientific audit100%; PR55 workflow50%; dated completed program4/99=4.040404%. No native/Git/PR/publication mutation; no new proof attempts.\n')
print(json.dumps({'result': 'ROOT_SCOPED_ADJUDICATION_RECORDED', 'path': str(target), 'sha256': sha(target.read_bytes()), 'UTC': utc, 'pid': os.getpid(), 'fresh_files': len(manifest['files']), 'controls': controls['control_count'], 'native_mutation': False}))
