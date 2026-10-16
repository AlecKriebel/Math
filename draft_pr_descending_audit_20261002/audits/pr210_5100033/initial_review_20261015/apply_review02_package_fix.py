"""Correct the second new review's sole package-plan finding; preserve its input."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
D=Path(__file__).resolve().parent;B=D.parent/'preprint';H=B/'history/review02_frozen';PUB=D.parent/'publication'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not H.exists();assert sha(B/'k605a-source-verification.zip')=='53ad3f542b43ea6ac4aaaaa5224f70b0bc867abe2ccf61faaf973f4fd8d64c87'
H.mkdir(parents=True)
for name in ['manuscript.tex','manuscript.pdf','metadata.json','deposit.json','SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json','NATIVE_RELEASE_PLAN.json','k605a-source-verification.zip']:shutil.copyfile(B/name,H/name)
now=datetime.now(timezone.utc).isoformat();p=B/'NATIVE_RELEASE_PLAN.json';d=json.loads(p.read_text())
assert 'sole-parent nonforce branch update' in d['required_native_guard']
d['required_native_guard']='Fresh open draft PR210 at exact original head on dot/math-5100033 in AlecKriebel/Math and exact claimed_solved row; preserve all foreign paths/Queue rows via fresh MAIN base tree. PR reconciliation commit has exactly parents=[original_PR_head,fresh_MAIN] and updates only that existing PR branch nonforce. Sole-parent commits apply only to separate MAIN progress checkpoints. Verify actual expected-head commit tree/parents, all owned native identities/bodies, release/DOI/tracker bindings and changed-path scope before expected-head native merge.'
d['MAIN_progress_checkpoint_parent_rule']='Exactly one parent: the freshly observed MAIN commit; nonforce MAIN update, retry only a confirmed stale-parent rejection.'
d['PR_reconciliation_parent_rule']=['2180d64b648b81ac660a792f7823d0b715f9cf12','freshly observed MAIN commit']
d['review02_correction']='R2-O1: earlier sole-parent wording conflated MAIN progress checkpoints with original-PR/fresh-MAIN reconciliation. Earlier reviewed input is preserved under history/review02_frozen outside this ZIP. No scientific input, proof, result, primary-source or metadata change.'
p.write_text(json.dumps(d,indent=2)+'\n')
policy=dict(utc=now,role='Current external release policy consistent with corrected dated package plan; no provider action clearance',PR=210,original_head=d['original_head'],expected_head_branch='dot/math-5100033',expected_repository='AlecKriebel/Math',MAIN_checkpoint_parents='one fresh MAIN parent',PR_reconciliation_parents=d['PR_reconciliation_parent_rule'],only_existing_PR_branch_nonforce=True,actual_expected_head_commit_and_owned_byte_readback_required=True,exact_submission_and_cross_stage_receipt_bindings_required=True,once_only_durable_intents_and_shared_process_lock_required=True,publish_and_tracker_and_merge_performed=False)
(PUB/'CURRENT_RELEASE_POLICY.json').write_text(json.dumps(policy,indent=2)+'\n')
r=dict(utc=now,review_report_sha256=sha(D/'whole_manuscript_adversary_02/REPORT.md'),review_manifest_sha256=sha(D/'whole_manuscript_adversary_02/AUTHORED_MANIFEST.json'),reviewed_zip_sha256=sha(H/'k605a-source-verification.zip'),finding='R2-O1',status='Corrected globally in package native-release plan and matching current external release policy; different third NEW whole-package adversary still required',manuscript_TEX_PDF_metadata_and_all_scientific_verification_bytes_unchanged=True,source_plan_sha256=sha(p),publication_cleared=False)
(B/'REVIEW02_RESOLUTION.json').write_text(json.dumps(r,indent=2)+'\n');(D/'REVIEW02_RESOLUTION_PROGRESS.json').write_text(json.dumps(r,indent=2)+'\n')
p=B/'build_bundle.py';s=p.read_text();old="'REVIEW01_RESOLUTION.json'";assert s.count(old)==1;s=s.replace(old,"'REVIEW01_RESOLUTION.json', 'REVIEW02_RESOLUTION.json'");p.write_text(s)
p=D/'root_replay_portable_zip_v3.py';s=p.read_text().replace('_V3.json','_V4.json').replace('_V3.txt','_V4.txt').replace('required_new_sequential_whole_manuscript_reviews_completed=1','required_new_sequential_whole_manuscript_reviews_completed=2');(D/'root_replay_portable_zip_v4.py').write_text(s)
print(json.dumps(r,indent=2))
