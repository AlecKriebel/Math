"""Accept exact clean source05 only after root has read and reproduced its evidence."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
from accept_final_reviews import seal,sha,load,save,canonical
D=Path(__file__).resolve().parent;S=D/'release_helpers_adversary_05'
O=D/'root_reproduction/source05_sealed_replay'
expected='9f6801cce90d309829fc85d3fbe22d723dfe06a72b0685ec8e2e0850b21ffc8a'
sealed=seal(S,expected)
assert sealed['payloads']==30
assert load(O/'ROOT_REPLAY_COMPLETION.json')['all_four_jobs_passed'] is True
assert sha(S/'independent_source05_probes.py')=='3f1c699f508ba9829e9b8072dc497c115000581d241ee3b7ba754bcdf83c8841'
def normalize(value,folder):
    if isinstance(value,dict):return {k:normalize(v,folder) for k,v in value.items()}
    if isinstance(value,list):return [normalize(v,folder) for v in value]
    if isinstance(value,str):
        value=value.replace(str(folder),'{probe-root}')
        return re.sub(r'(source05-|primitive-fixture-|fixture-|fsync-fixture-|binding-copy-)[A-Za-z0-9_]+',r'\1{temporary-id}',value)
    return value
comparisons=[]
for name,count in [('MOCKED_WORKFLOW_RESULTS.json',42),('REGRESSION_TRANSITION_RESULTS.json',42),('INDEPENDENT_SOURCE05_RESULTS.json',134)]:
    a=load(S/name);b=load(O/name)
    assert len(a['tests'])==len(b['tests'])==count
    assert all(x['passed'] is True for x in b['tests'])
    a.pop('utc');b.pop('utc')
    assert canonical(normalize(a,S))==canonical(normalize(b,O)),name
    comparisons.append(dict(path=name,root_sha256=sha(O/name),tests=count,
        exact_equal_except_utc_and_documented_temporary_paths=True))
a=load(S/'LOCAL_INTEGRITY_SOURCE05_RESULTS.json');b=load(O/'LOCAL_INTEGRITY_SOURCE05_RESULTS.json')
a.pop('utc');b.pop('utc');assert canonical(a)==canonical(b)
assert b['initial_archive_payloads_verified']==14 and b['current_original_evidence_files_unchanged']==7
assert b['unique_safe_zip_entries']==181 and b['native_source_zip_equalities']==42
assert b['original_twenty_three_copy_checks']==60 and b['native_and_reconciliation_intents_absent'] is True
findings=load(S/'FINDINGS.json')
assert findings['mandatory_findings']==findings['optional_findings']==[]
assert [x['id'] for x in findings['source04_findings_verified_fixed']]==['R4-F1','R4-F2','R4-F3']
assert all(x['status']=='fixed' for x in findings['source04_findings_verified_fixed'])
helpers=[];supplement=None
for row in findings['reviewed_sources']:
    source=Path(row['source']);assert source.stat().st_size==row['bytes'] and sha(source)==row['sha256']
    pin=dict(path=source.name,bytes=row['bytes'],sha256=row['sha256'])
    if source.parent==D.parent/'publication':helpers.append(pin)
    else:
        assert source==D/'reconcile_published_release_readonly.py';supplement=pin
helpers.sort(key=lambda x:x['path'])
assert len(helpers)==6 and supplement is not None
candidate=load(D/'RENEWED_CLEARANCE_CANDIDATE.json')
assert candidate['release_cleared'] is False and candidate['candidate_only'] is True
assert findings['candidate_sha256']==sha(D/'RENEWED_CLEARANCE_CANDIDATE.json')
assert helpers==candidate['release_helpers'] and supplement==candidate['supplemental_readonly_reconciliation']
for name in ['regression_workflow_probes.py','regression_transition_probes.py','independent_source05_probes.py','local_integrity_source05.py']:
    assert (O/(name+'.stderr.txt')).stat().st_size==0
result=dict(utc=datetime.now(timezone.utc).isoformat(),case_completion_percent=90,
    clean_version_bound_acceptance=True,supporting_source_only=True,whole_manuscript_review=False,
    manifest_sha256=expected,report_sha256=sha(S/'REPORT.md'),all30sealed_payloads_verified=True,
    full_report_all_source_programs_failure_disclosures_and_harness_deltas_read=True,
    reviewed_helpers=helpers,reviewed_supplemental_reconciler=supplement,
    candidate_sha256=sha(D/'RENEWED_CLEARANCE_CANDIDATE.json'),candidate_release_cleared=False,
    independently_authored_reviewer_controls_root_reproduced=134,
    reused_reviewer_regression_controls_root_reproduced=84,total_controls_root_reproduced=218,
    exact_result_comparisons=comparisons,
    comparison_exclusions=['top-level utc','exact own fixture-root prefix','random temporary directory identifier'],
    local_integrity_root_reproduced_exactly_except_utc=True,
    all_three_source04_findings_resolved=True,mandatory_findings=[],optional_findings=[],
    scientific_submission_and_metadata_unchanged=True,actual_provider_network_or_native_actions_by_tests=0,
    genuine_renewed_clearance_not_yet_created=True,actual_native_merge_pending=True,goal_active_incomplete=True)
save(D/'ROOT_RELEASE_HELPER_REVIEW05_ACCEPTANCE.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['reviewed_helpers','exact_result_comparisons']},indent=2))
