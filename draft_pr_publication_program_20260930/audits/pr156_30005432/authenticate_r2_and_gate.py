"""Authenticate the fresh review and bind authorization to the unchanged qualified package."""
from pathlib import Path
import datetime, hashlib, json, zipfile

A = Path(__file__).resolve().parent
D = A / 'whole_package_r2'
K = A / 'publication_package_v1'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def check(pin):
    path = Path(pin['path'])
    data = path.read_bytes()
    require(len(data) == pin['size'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'Review byte pin differs: ' + str(path))

def main():
    expected = {'REVIEW.md': '4cf7b9e89095031213c583887ca662063a405aee319a525627630948f97186ce',
                'RESULT.json': 'f0a7da5f78ac2665576e67e25452b56f0fda6f6451b29e4b9de40fce6dd8a071',
                'INPUT_OUTPUT_MANIFEST.json': 'd89e61e33014fd04924a32b4f86c2463ab1b521315a5c53c5154ac252ffbde8b',
                'PUBLIC_OUTPUT_WHITELIST.json': 'f52975307dbabcfda9d0ed6e662afd9115fa4c899c0ca9a0ded33f4370697ba3',
                'FINAL_REVIEW_SEAL.json': 'c54df0f1b68549804d7aefda098acf1cb808a4f3261b128060ef5a97ced24d04',
                'FIRST_ASSESSMENT_SEAL.json': '18cb40546f1dabcdf8252e3ddda8fe36e866e6f328c91b47ac06f2b0bf7895bd'}
    for name, sha in expected.items():
        require(hashlib.sha256((D / name).read_bytes()).hexdigest() == sha, 'Final notified output changed: ' + name)
    manifest = json.loads((D / 'INPUT_OUTPUT_MANIFEST.json').read_text())
    for kind in ['inputs', 'outputs']:
        for pin in manifest[kind]:
            check(pin)
    seal = json.loads((D / 'FINAL_REVIEW_SEAL.json').read_text())
    for pin in seal['principal_outputs'] + seal['frozen_candidate_principal_bytes']:
        check(pin)
    require(set(manifest['output_self_reference_exclusions']) == {'FINAL_REVIEW_SEAL.json', 'FINAL_REVIEW_SEAL_SHA256.txt', 'INPUT_OUTPUT_MANIFEST.json'}, 'Unresolved manifest exclusions')
    require((D / 'FINAL_REVIEW_SEAL_SHA256.txt').read_text().split()[0] == expected['FINAL_REVIEW_SEAL.json'], 'Final seal digest receipt differs')
    result = json.loads((D / 'RESULT.json').read_text())
    require(result['substantive_findings'] == [] and result['mandatory_scientific_corrections'] == [] and result['seal_first_requirement_satisfied'] and result['scientific_publication_readiness'], 'Fresh clean complete-package recommendation missing')
    first = json.loads((D / 'FIRST_ASSESSMENT_SEAL.json').read_text())
    require(first['critical_order_compliant'] and first['prior_verdicts_read_before_seal'] is False, 'Initial independence ordering failed')
    for pin in first['inputs'] + first['outputs_at_seal']:
        check(pin)
    whitelist = json.loads((D / 'PUBLIC_OUTPUT_WHITELIST.json').read_text())['allowed_relative_paths']
    require(len(whitelist) == len(set(whitelist)) and all((D / name).is_file() for name in whitelist), 'Invalid public whitelist')
    require(all('scratch' not in Path(name).parts and 'private_sources' not in Path(name).parts for name in whitelist), 'Private paths whitelisted')
    preparation = json.loads((A / 'PACKAGE_V1_PREPARATION.json').read_text())
    for name, pin in preparation['files'].items():
        data = (K / name).read_bytes()
        require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'Frozen package changed: ' + name)
    archive_manifest = json.loads((K / 'MANIFEST.json').read_text())
    with zipfile.ZipFile(K / 'property_s_support.zip') as archive:
        require(archive.testzip() is None and set(archive.namelist()) == set(archive_manifest['files']) | {'MANIFEST.json'}, 'Archive integrity differs')
        for name, pin in archive_manifest['files'].items():
            data = archive.read(name)
            require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'] and data == (K / name).read_bytes(), 'Archive member changed: ' + name)
    deposit_path = A / 'zenodo-deposit.v1.json'
    deposit = json.loads(deposit_path.read_text())
    require(deposit['metadata'] == json.loads((K / 'metadata.json').read_text()), 'Deposit metadata differs')
    r1 = json.loads((A / 'ROOT_WHOLE_PACKAGE_R1_AUTHENTICATION.json').read_text())
    require(r1['substantive_findings'] == [] and not r1['publication_clearance'], 'R1 dated scientific assessment differs')
    priority = json.loads((A / 'ROOT_PRIORITY_DECISION.json').read_text())
    require(priority['qualified_note_preparation_allowed'] and not priority['novelty_first_priority_exclusive_priority_or_mutual_independence_certified'], 'Qualified scope differs')
    now = datetime.datetime.now(datetime.UTC).isoformat()
    authentication = {'UTC': now, 'status': 'ROOT_AUTHENTICATED_NEW_SEAL_FIRST_CLEAN_WHOLE_PACKAGE_R2', 'input_records_checked': len(manifest['inputs']), 'output_records_checked': len(manifest['outputs']), 'self_reference_exclusions_resolved': 3, 'public_files': len(whitelist), 'principal_hashes': expected, 'substantive_findings': [], 'initial_seal_first_independence_confirmed': True, 'universal_checks_per_mode': result['independent_universal_checks_per_mode'], 'prior_source_checks_per_mode': result['independent_prior_and_source_checks_per_mode'], 'package_native_checks_per_mode': result['extracted_and_native_checks_per_mode'], 'additional_mutant_mode_runs_rejected': result['additional_mutant_mode_runs_rejected'], 'PDF_visual_pages': result['pdf_visual_pages'], 'candidate_changed': False, 'temporary_scope_exception_disclosed_and_remedied': True}
    save(A / 'ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION.json', authentication)
    gate = {'UTC': now, 'status': 'READY_FOR_AUTHORIZED_PUBLICATION', 'PR': 156, 'problem_id': 30005432, 'title': deposit['metadata']['title'], 'package': 'publication_package_v1', 'deposit_manifest': deposit_path.name, 'deposit_manifest_sha256': hashlib.sha256(deposit_path.read_bytes()).hexdigest(), 'files': preparation['files'], 'upload_files': ['property_s_counterexample.pdf', 'property_s_support.zip'], 'mathematical_resolution_accepted': True, 'bounded_priority_audit_complete': True, 'historical_novelty_first_exclusive_priority_or_mutual_independence_certified': False, 'qualified_research_note_scope': 'Self-contained explicit negative answer with known construction ancestry, exact later overlapping note, precise disclosure timeline and material priority/access/visibility/independence limits.', 'human_authorized_qualified_publication': True, 'authorization_basis': 'User authorized qualified research-note publication with unresolved priority and instructed publication with documented earlier public GitHub chronology and contemporaneous separate discovery wording; the package defines that phrase as separate disclosures, without certifying independence or literal simultaneity.', 'fresh_whole_package_reviews_completed': 2, 'R1_sequence_limitation_disclosed': True, 'fresh_seal_first_review_clean': True, 'R2_authentication': 'ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION.json', 'mandatory_scientific_corrections_remaining': [], 'AI_assistance_disclosed': True, 'unrefereed_no_conventional_human_peer_review_disclosed': True, 'publication_performed_by_this_gate': False, 'tracker_or_merge_performed_by_this_gate': False, 'case_percent': 70, 'programme_completed': 30, 'published_count': 17, 'persistent_goal_complete': False}
    save(A / 'ROOT_PUBLICATION_GATE.json', gate)
    status = json.loads((A / 'CURRENT_CASE_STATUS.json').read_text())
    status.update({'UTC': now, 'status': 'QUALIFIED_RESEARCH_NOTE_FULL_PACKAGE_READY_FOR_AUTHORIZED_PUBLICATION', 'case_percent': 70, 'case_workflow_percent': 70, 'publication_cleared': True, 'whole_package_review_round1_ongoing': False, 'whole_package_review_round2_ongoing': False, 'whole_package_reviews_complete': True, 'whole_package_review_round': 2, 'fresh_seal_first_review_clean': True, 'ROOT_publication_gate': 'ROOT_PUBLICATION_GATE.json', 'priority_cleared': False, 'published': False, 'merged': False})
    save(A / 'CURRENT_CASE_STATUS.json', status)
    with (A / 'RESEARCH_LOG.md').open('a') as handle:
        handle.write('\n## ' + now + ' — New seal-first complete-package review accepted; qualified publication ready\n\nROOT read the complete R2 report and authenticated136 consumed inputs,109 outputs and3 self-reference exclusions, plus unchanged first seal and frozen PDF/ZIP/metadata/source. New independent universal458 and prior/source150450 controls per mode passed; all additional14 mutant-mode tests failed. Four-page visual review and all original22 native historical identities passed. R1 was scientifically clean with disclosed initial summary exposure; R2 satisfied seal-first ordering. No substantive correction remains. Qualified note ready; no historical priority, novelty, exclusivity or independence certificate. Actual publication/tracker/merge remain pending. Math100%, bounded priority100%, case70%, programme30/99=30.30%,17published,goalactive.\n')
    print(json.dumps({'status': gate['status'], 'case_percent': 70, 'R2_inputs_checked': len(manifest['inputs']), 'R2_outputs_checked': len(manifest['outputs']), 'title': gate['title'], 'historical_priority_certified': False}))

if __name__ == '__main__':
    main()
