"""Assemble genuine version-bound clearance from accepted, sealed review evidence."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,re
from accept_final_reviews import seal,sha,load,save,canonical

D=Path(__file__).resolve().parent;C=D.parent;B=C/'preprint';P=C/'publication'
stamp=datetime.now(timezone.utc).isoformat()
S=D/'release_helpers_adversary_03'
source_seal=seal(S,'a703e6b74255c85e7c0c7fab0bc210a4023620456f9ba5829893204b01f13f4a')
prior_seal=seal(D/'release_helpers_adversary_02','ecef37ef2b6416f7ed9c3c4b973eeec8f05409433878befc951294483c0a19a9')
findings=load(S/'FINDINGS.json')
assert findings['mandatory_findings']==findings['optional_findings']==[]
assert findings['prior_review02_findings_resolved']==['R2-F1','R2-O1']
assert len(findings['prior_review01_findings_resolved'])==9
helper_pins=findings['reviewed_helpers']
for row in helper_pins:
    p=P/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']

O=D/'root_reproduction/release_helpers_review03_regression'
def normalize(value,folder):
    if isinstance(value,dict):return {k:normalize(v,folder) for k,v in value.items()}
    if isinstance(value,list):return [normalize(v,folder) for v in value]
    if isinstance(value,str):
        value=value.replace(str(folder),'{probe-root}')
        return re.sub(r'(primitive-fixture-|fixture-|fsync-fixture-)[A-Za-z0-9_]+',r'\1{temporary-id}',value)
    return value
controls=[]
for filename in ['MOCKED_WORKFLOW_RESULTS.json','INDEPENDENT_TRANSITION_RESULTS.json']:
    a=load(S/filename);b=load(O/filename)
    assert len(a['tests'])==len(b['tests'])==42
    assert all(x['passed'] is True for x in b['tests'])
    a.pop('utc');b.pop('utc')
    assert canonical(normalize(a,S))==canonical(normalize(b,O))
    controls.append(dict(path=str((O/filename).relative_to(D)),sha256=sha(O/filename),tests=42,
        reviewer_results_exact_equal_except_utc_and_documented_fixture_paths=True))
assert (O/'root_regression_stderr.txt').stat().st_size==0
assert (O/'root_independent_stderr.txt').stat().st_size==0
earlier=load(D/'root_reproduction/release_helpers_review02_regression/MOCKED_WORKFLOW_RESULTS.json')
assert earlier['passing_test_count']==len(earlier['tests'])==42
assert all(x['passed'] is True for x in earlier['tests']) and earlier['reproduced_defects']==[]
assert load(D/'ROOT_RELEASE_BINDING_TEST_RESULTS.json')['all_tests_passed'] is True
durability=load(D/'ROOT_DURABLE_INTENT_TEST_RESULTS.json')
save(D/'ROOT_RELEASE_HELPER_REVIEW02_ACCEPTANCE.json',dict(
    utc=stamp,case_completion_percent=85,supporting_source_only=True,review_seal=prior_seal,
    full_report_harness_findings_and_failures_read=True,
    both_findings_accepted_and_repaired=True,repair_resolution_sha256=sha(D/'RELEASE_HELPER_REVIEW02_RESOLUTION.json'),
    historical_root31_receipt_restoration_sha256=sha(D/'ROOT_HISTORICAL_BINDING_TEST_RECEIPT_RESTORATION.json'),
    root_regression_tests_passed=42,mandatory_findings_remaining=[],optional_findings_remaining=[],
    fresh_independent_source03_required_and_now_completed=True,release_cleared_by_this_receipt=False))
save(D/'ROOT_RELEASE_HELPER_REVIEW03_ACCEPTANCE.json',dict(
    utc=stamp,case_completion_percent=85,supporting_source_only=True,review_seal=source_seal,
    report_sha256=sha(S/'REPORT.md'),full_report_programs_results_failure_disclosures_read=True,
    all17sealed_payloads_verified=True,reviewed_helpers=helper_pins,
    root_reproduction=controls,total_root_reproduced_controls=84,
    comparison_exclusions=['top-level utc','exact own fixture-root prefix','random temporary-directory identifier'],
    unchanged_independent_program_sha256=sha(O/'independent_transition_probes.py'),
    adaptation_receipt_sha256=sha(O/'ROOT_ADAPTATION_RECEIPT.json'),
    real_provider_or_network_actions=0,real_action_helper_subprocesses=0,
    power_crash_simulated=False,hardware_durability_guarantee=False,
    all9review01_and2review02_findings_resolved=True,mandatory_findings=[],optional_findings=[],
    manuscript_review=False,release_cleared_by_this_receipt=False))
math=[]
for family,expected in [
    ('whole_manuscript_adversary_01','3dd1a4495204eb8cf03efcb2bb6698c521e1c96e535ce99004df4a9dc833ad54'),
    ('whole_manuscript_adversary_02','c6eb0e365bbfe98f48cdc29be608b398731fad98a82d0d81e30d707823a22632'),
    ('whole_manuscript_adversary_03','2c2b5200baa6a43e4eec0fd8410ca11c959249b003562eedd1eecd2d9b0dbf50')]:
    math.append(dict(family=family,**seal(D/family,expected),report_sha256=sha(D/family/'REPORT.md')))
assert load(D/'ROOT_REVIEW03_ACCEPTANCE.json')['final_frozen_clean_reviews']==1
assert load(D/'ROOT_REVIEW03_ACCEPTANCE.json')['mandatory_findings']==[]
assert load(D/'ROOT_REVIEW03_ACCEPTANCE.json')['optional_findings']==[]
package=load(B/'PACKAGE_MANIFEST.json');metadata=load(B/'metadata.json')
assert load(B/'deposit.json')['metadata']==metadata
clear=dict(schema='PR210-genuine-final-version-bound-clearance-v1',utc=stamp,
    case_completion_percent=85,release_cleared=True,fresh_manuscript_reviews=3,
    final_frozen_clean_reviews=1,unresolved_mandatory_findings=[],unresolved_optional_findings=[],
    original_native_head='2180d64b648b81ac660a792f7823d0b715f9cf12',
    package_manifest_sha256=sha(B/'PACKAGE_MANIFEST.json'),
    deposit_manifest_sha256=sha(B/'deposit.json'),publication_metadata_sha256=sha(B/'metadata.json'),
    release_helpers=helper_pins,submission_files=package['submission_files'],
    source_manifest=package['source_manifest'],manuscript_source=package['manuscript_source'],
    publication_metadata=metadata,whole_manuscript_review_seals=math,
    final_supporting_source_review=dict(family=S.name,**source_seal,report_sha256=sha(S/'REPORT.md')),
    accepted_root_receipts=[dict(path=f,sha256=sha(D/f)) for f in [
        'ROOT_REVIEW01_GLOBAL_RESOLUTION_ACCEPTANCE.json','ROOT_REVIEW02_ACCEPTANCE.json',
        'ROOT_REVIEW03_ACCEPTANCE.json','ROOT_RELEASE_HELPER_REVIEW02_ACCEPTANCE.json',
        'ROOT_RELEASE_HELPER_REVIEW03_ACCEPTANCE.json','ROOT_PORTABLE_PACKAGE_ACCEPTANCE_V4.json',
        'ROOT_PRIORITY_ACCEPTANCE.json','ROOT_RELEASE_BINDING_TEST_RESULTS.json',
        'ROOT_DURABLE_INTENT_TEST_RESULTS.json']],
    science_boundary='Universal proof of the source-specific signed outer focal-pedal product for odd primitive elliptic billiards and coprime stars; explicit extensions/controls. Finite computations corroborate the proof and are not interval certification.',
    priority_boundary='Fully credited source-specific proof/application; bounded priority corpus, no historical-first or new-general-method claim; documented access gaps remain.',
    disclosure='Extensive AI assistance; unrefereed, no independent human peer review or formal proof-assistant certification.',
    actual_deposit_tracker_native_actions_not_yet_performed=True,counts_before_release=[43,20,20,0],
    goal_active_incomplete=True)
save(B/'FINAL_CLEARANCE.json',clear)
spec=importlib.util.spec_from_file_location('pr210_pure_release_binding',P/'release_binding.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ctx=g.context(B)
save(D/'ROOT_FINAL_CLEARANCE_ACCEPTANCE.json',dict(utc=stamp,case_completion_percent=85,
    final_clearance_sha256=sha(B/'FINAL_CLEARANCE.json'),binding=g.binding(ctx),
    exact_submission_files=ctx['expected_files'],all_six_current_helper_pins_verified=True,
    whole_manuscript_reviews=3,final_frozen_clean_reviews=1,supporting_source_reviews=3,
    unresolved_mandatory_findings=[],unresolved_optional_findings=[],
    release_cleared=True,actual_release_not_yet_executed=True,goal_active_incomplete=True))
state=load(D/'CURRENT_AUDIT_STATE.json')
state.update(utc=stamp,stage='final_clean_version_bound_clearance_checkpoint',current_stage='final_clean_version_bound_clearance_checkpoint',
    completion_percent=85,case_completion_percent=85,preprint_upload_cleared=True,
    whole_manuscript_reviews_completed=3,third_new_whole_manuscript_review_active=False,
    release_helper_source_review_active=False,release_helper_source_reviews_completed=3,
    final_clean_reviews=1,unresolved_review_findings=[],
    release_helper_source_review02_preliminary_findings=[],
    final_clearance='preprint/FINAL_CLEARANCE.json',final_clearance_sha256=sha(B/'FINAL_CLEARANCE.json'))
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
G=C.parents[1]
for log in [D/'RESEARCH_LOG.md',G/'RESEARCH_LOG.md']:
    with log.open('a') as f:f.write('\n- '+stamp+' — PR210 85%: third NEW whole-manuscript review clean; all31 sealed payloads verified, byte-identical fresh checker reproduced exactly exceptUTC (80 exact zeros,303 primitive pairs/10325 phases,7 families/21 phases at115digits). Current181-entry ZIP/16 source pins/6 render pins checked. Third supporting helper review clean; all17 payloads verified and84 mocked controls root-reproduced. Both prior helper findings resolved, no mandatory/optional findings remain. Genuine final clearance binds exact six helpers/PDF/ZIP/metadata/deposit. No deposit, tracker append, PR branch, ready or merge action yet. Counts43/20/20/0; overall goal active/incomplete.\n')
selection=G/'CURRENT_GOAL_SELECTION_20261013.json'
value=load(selection);value.update(utc=stamp,current_PR=210,current_case_completion_percent=85,
    stage='final_clean_version_bound_clearance_checkpoint',counts=[43,20,20,0],goal_active_incomplete=True)
selection.write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps(dict(final_clearance_sha256=sha(B/'FINAL_CLEARANCE.json'),case_completion_percent=85,
    root_source_controls_passed=84,release_cleared=True,submission_files=ctx['expected_files']),indent=2))
