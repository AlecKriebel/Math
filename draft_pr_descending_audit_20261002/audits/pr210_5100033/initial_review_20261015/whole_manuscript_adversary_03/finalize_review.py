from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile,shutil
C=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr210_5100033');D=C/'initial_review_20261015';B=C/'preprint';P=C/'publication';O=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
# This is a later read-only external snapshot, never a relabelled acceptance.
helper=P/'integrate_reviewed_pr.py';code=helper.read_text();assert "'parents': [OLD, main]" in code and "actual_commit['parents']]==[OLD,main]" in code
original_source_receipt=load(O/'SOURCE_AND_RELEASE_RECEIPT.json')
(O/'EXTERNAL_HELPER_SCOPE_UPDATE.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'parent_reported_after_initial_readonly_snapshot':'Second supporting helper review found late ready guard and file-only fsync; fixes occurred outside ZIP, and a different THIRD NEW supporting source adversary is reviewing all six fixed helpers. This is parent-reported operational status, not this reviewer accepting helper safety.','earlier_readonly_integrator_sha256':original_source_receipt['release_plan']['helper_readonly_sha256'],'later_readonly_integrator_sha256':sha(helper),'earlier_source_receipt_sha256':sha(O/'SOURCE_AND_RELEASE_RECEIPT.json'),'current_two_parent_strategy_observed':True,'publication_or_helper_execution_by_this_review':False,'helper_acceptance_separate_pending':True,'frozen_package_changed':False},indent=2)+'\n')
report=O/'REPORT.md';t=report.read_text();t=t.replace('coefficient2iR² instead of zero','coefficient2i r_1² instead of zero')
t=t.replace('The second NEW helper-source adversary is a separate review and is not counted as this whole-manuscript review.','The supporting helper-source reviews are separate and are not counted as this whole-manuscript review. After the earlier read-only observation, the parent reported two helper-only findings (late ready guard and file-only fsync), fixes outside the ZIP, and a DIFFERENT third NEW supporting source adversary now reviewing all six helpers. That acceptance remains a separate pending operational gate. EXTERNAL_HELPER_SCOPE_UPDATE.json distinguishes the earlier and later observed helper hashes; neither is labelled an accepted helper version by this report.')
report.write_text(t)
inputs=load(O/'INPUT_SNAPSHOT.json')['files'];after={s:{'bytes':(B/s).stat().st_size,'sha256':sha(B/s)} for s in inputs};assert after==inputs
sm=load(B/'SOURCE_MANIFEST.json');assert len(sm['files'])==180
for r in sm['files']:assert (B/r['path']).stat().st_size==r['bytes'] and sha(B/r['path'])==r['sha256']
with zipfile.ZipFile(B/'k605a-source-verification.zip') as z:
 assert len(z.namelist())==181 and z.testzip() is None
 for i in z.infolist():assert z.read(i)==(B/i.filename.split('/',1)[1]).read_bytes()
for name,n in [('PORTABLE_REPLAY_RECEIPT.json',10),('GENUINE_PRIMARY_REPLAY_RECEIPT.json',1)]:
 r=load(O/name);assert len(r['jobs'])==n and r['all_selected_jobs_passed'] and r['all_scientific_fields_compared_exactly'] and r['integrity_before']==r['integrity_after']
assert load(O/'HARNESS_MUTANT_RESULTS.json')['all_passed']
assert load(O/'FRESH_CONTROL_RESULTS.json')['universal_proof_from_finite_checks'] is False
(O/'FINAL_INPUT_INTEGRITY.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'inputs':after,'all_fixed_input_bytes_unchanged':True,'source_payload_rows':len(sm['files']),'zip_entries':181,'zip_crc_test':None,'all_zip_entries_equal_fixed_disk':True,'all_scientific_replays_complete_and_passed':True,'mandatory_findings':[],'optional_findings':[],'helper_source_acceptance_is_separate_pending_gate':True},indent=2)+'\n')
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+datetime.now(timezone.utc).isoformat()+' — Final fixed-input/hash/ZIP checks PASS; all181 entries and180 source rows unchanged. Report complete: mandatory findings NONE, optional findings NONE. Mathematics/manuscript/package review completion100%. Historical/public priority remains undetermined; third NEW supporting helper-source review is separately pending after outside-ZIP fixes. No helper/provider/Git/tracker/native action executed. Review report and authored manifest sealed after removing only own disposable extracted/temp copies. Parent broader publication completion not reassessed.\n')
# Own extracted package and cleaned scratch folders are not authored public findings.
for name in ['extracted','replay_temp']:
 p=O/name
 if p.exists():shutil.rmtree(p)
# Self-exclusion is explicit; every remaining own file is a public authored payload.
rs=[]
for p in sorted(O.rglob('*')):
 assert not p.is_symlink() and '__pycache__' not in p.parts
 if p.is_file() and p.name!='AUTHORED_MANIFEST.json':rs.append({'path':p.relative_to(O).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
(O/'AUTHORED_MANIFEST.json').write_text(json.dumps({'schema':'pr210-whole-manuscript-adversary03-authored-sha256-v1','utc':datetime.now(timezone.utc).isoformat(),'self_excluded':True,'excluded_non_authored_disposable_copies':'Own extracted package and empty replay temporary directories removed after successful replay; no reading/source PDFs, text or images copied.','files':rs},indent=2)+'\n')
print(json.dumps({'report_sha256':sha(report),'manifest_sha256':sha(O/'AUTHORED_MANIFEST.json'),'authored_payloads':len(rs),'mandatory_findings':0,'optional_findings':0,'fixed_inputs_unchanged':True},indent=2))
