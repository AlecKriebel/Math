"""Clear the unchanged submission only after two sequential fresh closed reviews."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
A=Path(__file__).resolve().parent;P=A.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def parse(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
assert not (A/'PUBLISHING_CLEARANCE.json').exists()
files=[{'path':name,**pin} for name,pin in load(A/'ROOT_PREPRINT_PACKAGE_VERIFICATION.json')['files'].items()]
pins={e['path']:(e['bytes'],e['sha256']) for e in files};assert len(pins)==4
for name,pin in pins.items():b=(A/'preprint'/name).read_bytes();assert (len(b),sha(b))==pin
reviews=[]
for n in (1,2):
 N=A/f'preprint_review_0{n}';r=load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json');g=load(N/'source_first_gate.json');seal=load(N/r['review_seal_path'])
 assert r['mandatory_findings']==0 and r['all_mandatory_submission_findings_resolved'] and r['closed_namespace_unchanged'] and r['whole_verifier_output_compared']
 assert {e['path']:(e['bytes'],e['sha256']) for e in r['sealed_submission_files']}==pins
 assert sha((N/r['review_seal_path']).read_bytes())==r['review_seal_sha256']
 pre_path=A/('ROOT_PREPRINT01_PRECLOSURE_REPLAY.json' if n==1 else 'ROOT_PREPRINT02_PRECLOSURE_REPLAY.json');pre=load(pre_path)
 control=[e for e in pre['native_runs'] if Path(e['argv'][2]).name!='verify_review.py' and '--full' not in e['argv']]
 assert control and all(e['exit_code']==0 and e['stderr_bytes']==0 and e['whole_expected_output_compared'] for e in control)
 for e in control:
  b=Path(e['stdout_path']).read_bytes();assert len(b)==e['stdout_bytes'] and sha(b)==e['stdout_sha256'] and Path(e['stderr_path']).read_bytes()==b''
 if n==1:
  assert not g['candidate_exposure_before_baseline'] and not g['prior_review_or_priority_exposure'] and not g['prohibited_exposures_seen']
  analytic=load(N/'analytic_freeze.json');assert not any(analytic[k] for k in ['included_prior_audit_or_control_code_seen','deposit_metadata_content_seen','zip_member_content_seen'])
 else:
  assert not any(value for key,value in g['exposure_declaration'].items() if key!='procedural_assignment_and_AGENTS_and_pdf_skill')
  analytic=load(N/'analytic_freeze_gate.json');assert not analytic['zip_metadata_prior_audit_control_exposure']
 for label in ['default','full']:
  e=r['package_native_streams'][label];b=Path(e['stdout_path']).read_bytes()
  assert len(b)==e['bytes'] and sha(b)==e['sha256'] and e['exit_code']==0 and Path(e['stderr_path']).read_bytes()==b''
 closed_utc=seal.get('closed_utc',seal.get('sealed_utc',seal.get('created_utc')));assert closed_utc
 reviews.append({'review':n,'source_first_utc':g['created_utc'],'sealed_utc':closed_utc,'seal_relative_path':r['review_seal_path'],'seal_sha256':r['review_seal_sha256'],
  'mandatory_findings':0,'root_whole_verification':f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json','root_precosure_control_reproduction':pre_path.name})
assert parse(reviews[0]['source_first_utc'])<parse(reviews[0]['sealed_utc'])<parse(reviews[1]['source_first_utc'])<parse(reviews[1]['sealed_utc'])
assert load(A/'ROOT_PRIORITY_POSTCLOSURE_REPLAY.json')['status']=='PASS_EXACT_PRIORITY_NATIVE_REPLAY_POSTCLOSURE'
assert load(A/'ROOT_CLOSED_MATH_FAMILIES.json')['status']=='PASS_THREE_CLOSED_MATH_FAMILIES_FULL_AND_PUBLIC_VERIFIERS'
now=datetime.now(timezone.utc).isoformat()
r={'utc':now,'status':'READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS','pr':356,'problem_id':30001552,
 'original_head':'12fc989f8635fd202eb66b553b9599f0546d05d3','original_status':'claimed_solved','sealed_submission_files':files,'fresh_reviews':reviews,
 'second_review_mandatory_findings':0,'all_mandatory_submission_findings_resolved':True,'submission_unchanged_between_final_first_and_second_reviews':True,
 'mathematical_resolution_percent':100,'preprint_preparation_percent':100,'priority_audit_workflow_percent':100,'acceptance_publication_workflow_percent':75,
 'novelty_certified':False,'exact_live_actual_merge_publication_tracker_pending':True,
 'priority_coverage_limits':['Bounded inspected primary corpus only; recorded access/version gaps remain.','Unpublished, unindexed, uninspected or differently named work is not excluded.'],
 'disclosure':'Extensive AI use in solving, verification, literature research, writing and adversarial review. Unrefereed; no independent external human peer review.',
 'scope':'Exact original alternating antimorphic conjecture, uniform one-letter-lower obstruction only. Separate source Conjecture27 outside scope. Exact live/merge and production publication/tracker remain separate checks.'}
(A/'PUBLISHING_CLEARANCE.json').write_text(json.dumps(r,indent=2)+'\n')
(A/'CURRENT_PREPRINT_STATUS.json').write_text(json.dumps(r,indent=2)+'\n')
c=load(A/'acceptance_criteria.json');c.update(updated_utc=now,accepted_status='claimed_solved',author_turns='1/5',preprint_preparation_percent=100,
 fresh_preprint_reviews_pending=False,second_fresh_preprint_review_pending=False,workflow_completion_percent=75,acceptance_publication_workflow_percent=75,candidate_accepted=False)
(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
for f in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with f.open('a') as out:out.write('\n'+now+': PR356 exact final four files passed two sequential NEW full preprint adversaries with zero unresolved mandatory findings and root full-read, independent control reproduction and closed-evidence checks. Math100%, preprint100%, workflow75%; exact live, merge, Zenodo and tracker pending. Bounded priority only; no global novelty or external human peer-review certification.\n')
print(json.dumps(r,indent=2))
