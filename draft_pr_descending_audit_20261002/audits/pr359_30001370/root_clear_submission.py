"""Clear exact files only after two sequential, fresh, independently closed reviews."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

A=Path(__file__).resolve().parent;P=A.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
assert not (A/'PUBLISHING_CLEARANCE.json').exists(),'Never silently replace a cleared submission.'
files=load(A/'CURRENT_PREPRINT_STATUS.json')['submission_files']
assert len(files)==4 and len({r['path'] for r in files})==4
for e in files:
    b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
pins={e['path']:{'bytes':e['bytes'],'sha256':e['sha256']} for e in files}
reviews=[]
for n in (1,2):
    v=A/f'preprint_review_0{n}'
    r=load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json')
    c=load(A/f'ROOT_PREPRINT_REVIEW0{n}_CONTROL_REPRODUCTION.json')
    assert r['status']==f'PASS_ROOT_CLOSED_PREPRINT_REVIEW0{n}' and r['review_number']==n
    assert r['mandatory_findings']==0 and r['all_mandatory_submission_findings_resolved']
    assert r['closed_namespace_unchanged'] and r['whole_verifier_output_compared']
    assert c['entire_stdout_identical'] and c['closed_review_namespace_unchanged']
    assert c['execution']['exit_code']==0 and c['execution']['stderr_bytes']==0
    assert c['review_seal_sha256']==r['review_seal_sha256']==sha((v/r['review_seal_path']).read_bytes())
    assert {e['path']:{'bytes':e['bytes'],'sha256':e['sha256']} for e in r['sealed_submission_files']}==pins
    baseline=r['baseline_seal'];assert baseline['candidate_access_before_seal'] is False
    assert baseline['prior_or_current_substantive_verdict_access_before_seal'] is False
    assert sha((v/baseline['path']).read_bytes())==baseline['sha256']
    assert (v/baseline['path']).stat().st_size==baseline['bytes']
    reviews.append({'review':n,'source_first_utc':baseline['utc'],'sealed_utc':r['sealed_utc'],
                    'seal_relative_path':r['review_seal_path'],'seal_sha256':r['review_seal_sha256'],
                    'mandatory_findings':0,'root_whole_verification':f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json',
                    'root_new_control_reproduction':f'ROOT_PREPRINT_REVIEW0{n}_CONTROL_REPRODUCTION.json'})
assert parse(reviews[0]['source_first_utc'])<parse(reviews[0]['sealed_utc'])<parse(reviews[1]['source_first_utc'])<parse(reviews[1]['sealed_utc'])
assert load(A/'ROOT_PRIORITY_VERIFICATION.json')['status']=='PASS_ROOT_COMPLETE_PRIORITY_READ_AND_CLOSED_NAMESPACE'
assert load(A/'ROOT_FAMILY_CLOSURE_VERIFICATION.json')['status']=='PASS_ALL_THREE_CLOSED_FAMILIES_PARENT_VERIFIED'
t=datetime.now(timezone.utc).isoformat()
receipt={'utc':t,'status':'READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS','pr':359,
         'problem_id':30001370,'original_head':'6be98eac0ba508368218179ecf80020c037dbece',
         'original_status':'claimed_solved','sealed_submission_files':files,'fresh_reviews':reviews,
         'second_review_mandatory_findings':0,'all_mandatory_submission_findings_resolved':True,
         'submission_unchanged_between_final_first_and_second_reviews':True,
         'metadata_notation_repair_before_first_final_seal':'METADATA_REPAIR_RECEIPT.json',
         'mathematical_resolution_percent':100,'preprint_preparation_percent':100,
         'acceptance_publication_workflow_percent':75,'exact_live_actual_merge_publication_tracker_pending':True,
         'priority_audit_workflow_percent':100,'novelty_certified':False,
         'priority_coverage_limits':['Final foundational journal proof version not obtained',
                                    'Unpublished, unindexed, uninspected or renamed work not excluded by bounded corpus'],
         'disclosure':'Extensive AI use in solving, verification, literature research, writing and adversarial review. Unrefereed; no independent external human peer review.',
         'scope':'The exact four submission files passed two sequential fresh complete adversarial reviews. Current live source/head/queue, actual native merge and production publication/tracker are separate gates.'}
(A/'PUBLISHING_CLEARANCE.json').write_text(json.dumps(receipt,indent=2)+'\n')
(A/'CURRENT_PREPRINT_STATUS.json').write_text(json.dumps(receipt,indent=2)+'\n')
criteria=load(A/'acceptance_criteria.json');criteria.update(utc=t,accepted_status='claimed_solved',
        preprint_preparation_percent=100,preprint_fresh_reviews_pending=False,
        preprint_review02_pending=False,fresh_sequential_preprint_reviews_pending=False,
        preprint_review02_mandatory_findings=0,workflow_completion_percent=75,publication_workflow_percent=75)
(A/'acceptance_criteria.json').write_text(json.dumps(criteria,indent=2)+'\n')
for f in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with f.open('a') as o:o.write('\n'+t+': PR359 exact final four files passed two sequential NEW complete preprint adversaries with0 mandatory findings and full root read/reproduction/closed-custody checks. Mathematical100%, preprint100%, acceptance/publication75%; native exact-live, actual merge, Zenodo and tracker remain pending. Priority remains bounded; no global novelty or external human peer-review certification.\n')
print(json.dumps(receipt,indent=2))
