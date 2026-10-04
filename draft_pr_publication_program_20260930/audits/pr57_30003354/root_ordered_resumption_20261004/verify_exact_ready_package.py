"""Revalidate the already reviewed PR57 package; never upload or recompile."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

F=Path(__file__).resolve().parent; A=F.parent; P=A.parents[1]; R=P.parent
F.mkdir(exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def binding(p): return {'path':p.relative_to(R).as_posix(),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())}
intake=P/'ordered_intake_20261004/INTAKE_56_57.json'
observation=load(intake)['observations'][1]
assert observation['PR']==57 and observation['eligible'] is True
assert observation['literal_submitted_status']=='claimed_solved' and observation['original_budget']=='1/5'
assert observation['current_GitHub_metadata']['headRefOid']=='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29'
final_path=A/'ROOT_FINAL_PREPRINT_PACKAGE_ADJUDICATION_20261003.json'
final=load(final_path)
assert final['preprint_package_ready_for_ordered_publication'] is True
assert final['mathematical_audit_percent']==final['manuscript_and_verification_package_percent']==final['independent_final_review_percent']==100
assert final['actual_external_upload_performed'] is False and final['DOI'] is None
checked=[]
def walk(v):
    if isinstance(v,dict):
        if {'path','bytes','sha256'}<=set(v):
            p=R/v['path']; p.resolve().relative_to(R)
            assert p.is_file() and not p.is_symlink()
            b=p.read_bytes()
            assert len(b)==v['bytes'] and sha(b)==v['sha256']
            if 'full_mode' in v: assert stat.S_IMODE(p.stat().st_mode)==v['full_mode']
            checked.append(v['path'])
        else:
            for x in v.values(): walk(x)
    elif isinstance(v,list):
        for x in v: walk(x)
walk(final)
priority=A/'ROOT_PRIORITY_ADJUDICATION_20261003.json'
prior=load(priority)
assert prior['disposition']=='claimed_solved' and prior['bounded_priority_audit_completion_percent']==100
assert prior['original_budget']=='1/5' and prior['worldwide_priority_guarantee'] is False
round2=load(A/'preprint_round2_wholepackage_adversary/VERDICT.json')
assert round2['verdict']=='NO_ESSENTIAL_ISSUES_FOUND'
assert round2['independent_claim_argument_saved_before_prior_reports'] is True
assert round2['universal_proof_independently_rederived'] is True
assert round2['all_six_PDF_pages_personally_inspected'] is True
for name, pin in round2['artifacts'].items():
    p=A/'publication_package_v1'/name; b=p.read_bytes()
    assert len(b)==pin['bytes'] and sha(b)==pin['sha256']
manifest_path=A/'publication_package_v1/zenodo-deposit.json'
manifest=load(manifest_path)
assert manifest['metadata']['title']=='Integer endpoint discontinuity of normalized uniformization for positively curved surfaces'
assert manifest['metadata']['creators']==[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}]
assert {f['path'] for f in manifest['files']}=={'integer_endpoint_discontinuity.pdf','integer-endpoint-discontinuity-verification-v1.zip'}
assert 'publication_date' not in manifest['metadata'] and 'doi' not in manifest['metadata']
now=dt.datetime.now(dt.timezone.utc).isoformat()
record={'schema':'pr57-ordered-exact-package-resumption/v1','UTC':now,'actual_pid':os.getpid(),
        'PR':57,'fresh_intake':binding(intake),'reviewed_head':observation['current_GitHub_metadata']['headRefOid'],
        'old_ROOT_final_adjudication':binding(final_path),'old_ROOT_priority_adjudication':binding(priority),
        'unchanged_bound_artifact_paths_verified':checked,'zenodo_manifest':binding(manifest_path),
        'operative_publication_files':final['exact_publication_files'],
        'existing_two_independent_review_rounds_retained':True,'new_independent_review_claimed':False,
        'source_or_PDF_edit_or_compile_performed':False,'existing_editor_kept_open':True,
        'mathematical_and_publication_package_review_percent':100,'bounded_priority_audit_percent':100,
        'PR57_ordered_workflow_estimate_percent':80,'dated_completed_program_fraction_percent':5/99*100,
        'actual_publication_performed':False,'native_acceptance_performed':False,'DOI':None,'tracker_row':None,
        'new_central_proof_attempts':0,'original_budget':'1/5','goal_complete':False,
        'remaining':'Repository Zenodo kit upload/publish, exact public bytes/metadata checks, GWS row/readback, exact-head merge/native acceptance and owned checkpoint.'}
with (F/'EXACT_READY_PACKAGE_READBACK.json').open('x') as out: json.dump(record,out,indent=2);out.write('\n')
(F/'RESEARCH_LOG.md').write_text(f'{now} — Ordered PR57 resumed after PR55 complete and PR56 nonclaimed skipped. Existing exact ready package, prior ROOT adjudications, final review and all{len(checked)} bound artifact references revalidated without edits or recompile. Mathematical/package reviews100%; bounded priority audit100%; ordered PR57 workflow80%; dated complete program5/99={5/99*100:.6f}%. Publication/DOI/tracker/native acceptance remain pending; original1/5, no new proof attempts.\n')
print(json.dumps({k:v for k,v in record.items() if k not in ('unchanged_bound_artifact_paths_verified','operative_publication_files')},indent=2))
