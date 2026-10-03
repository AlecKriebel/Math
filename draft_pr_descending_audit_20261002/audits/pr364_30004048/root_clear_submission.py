"""Record readiness only after two sequential fresh complete clean reviews.

This does not merge or publish; exact-live and actual-merge gates remain.
"""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent;P=A.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
initial=load(A/'preprint/INITIAL_REVIEW_PACKAGE.json');files=[]
for name,e in initial['submission_files'].items():
 b=(A/'preprint'/name).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
 files.append({'path':name,'bytes':len(b),'sha256':sha(b)})
assert len(files)==4
reviews=[]
for n in (1,2):
 D=A/f'preprint_review_0{n}';seal=load(D/'FINAL_SEAL.json')
 root=load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json')
 assert (seal['mandatory_corrections'] if n==1 else seal['mandatory_submission_defects'])==0 and seal['workflow_completion_percent']==100
 assert root['mandatory_findings']==0 and root['closed_namespace_unchanged'] and root['whole_verifier_output_compared']
 assert root['review_seal_sha256']==sha((D/'FINAL_SEAL.json').read_bytes())
 controls=load(A/f'ROOT_PREPRINT_REVIEW0{n}_CONTROL_REPRODUCTION.json')
 assert controls['entire_stdout_identical'] and controls['closed_review_namespace_unchanged']
 assert controls['execution']['exit_code']==0 and controls['execution']['stderr_bytes']==0
 reviews.append({'review':n,'sealed_utc':seal['sealed_utc'],'seal_sha256':sha((D/'FINAL_SEAL.json').read_bytes()),'manifest_sha256':sha((D/'MANIFEST.json').read_bytes()),'mandatory_findings':0,'root_closure_verification':str(Path(f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json')),'root_new_control_reproduction':str(Path(f'ROOT_PREPRINT_REVIEW0{n}_CONTROL_REPRODUCTION.json'))})
assert reviews[0]['sealed_utc']<load(A/'preprint_review_02/ANALYTIC_SEAL.json')['sealed_utc']<reviews[1]['sealed_utc']
t=datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt={'utc':t,'status':'READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS','pr':364,'problem_id':30004048,'original_head':'0d07b06537aded3e76f5a71908f3546df574a691','original_status':'claimed_solved','sealed_submission_files':files,'fresh_reviews':reviews,'second_review_mandatory_findings':0,'all_mandatory_submission_findings_resolved':True,'submission_unchanged_during_two_reviews':True,'mathematical_resolution_percent':100,'preprint_preparation_percent':100,'acceptance_publication_workflow_percent':75,'exact_live_actual_merge_publication_tracker_pending':True,'priority_audit_workflow_percent':100,'novelty_certified':False,'priority_coverage_limits':['Inaccessible2019 Princeton senior thesis','Unpublished, unindexed or uninspected work not excluded by bounded searches'],'disclosure':'Extensive AI-assisted solving, verification, literature research, writing and adversarial review; unrefereed and no external human peer review.','scope':'Submission readiness of the exact four files only. Current live Git/API/queue and actual merge/publication/DOI/tracker are separate required gates.'}
assert not (A/'PUBLISHING_CLEARANCE.json').exists(),'Do not silently replace a cleared submission.'
(A/'PUBLISHING_CLEARANCE.json').write_text(json.dumps(receipt,indent=2)+'\n')
c=load(A/'acceptance_criteria.json');c.update(preprint_preparation_percent=100,fresh_sequential_preprint_reviews_pending=False,preprint_review_02_pending=False,preprint_review_02_mandatory_findings=0,preprint_review_02_final_seal=reviews[1]['seal_sha256'],workflow_completion_percent=75);(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
(A/'CURRENT_PREPRINT_STATUS.json').write_text(json.dumps(receipt,indent=2)+'\n')
for f in [A/'RESEARCH_LOG.md',A/'README.md',P/'RESEARCH_LOG.md']:
 with f.open('a') as h:h.write(f'\n{t}: PR364 exact four submission files passed two sequential fresh complete adversarial reviews with0 mandatory submission findings. ROOT fully read both reports/verifiers/closure programs and reproduced all new controls and closed outputs. Preprint preparation100%, mathematical resolution100%, acceptance/publication workflow75%; current exact-live/actual merge/Zenodo/DOI/tracker remain pending. Priority is a completed bounded workflow, not a global novelty certificate.\n')
print(json.dumps(receipt,indent=2))
