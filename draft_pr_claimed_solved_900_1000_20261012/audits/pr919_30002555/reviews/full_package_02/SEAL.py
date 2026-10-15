#!/usr/bin/env python3
"""Curate only explicit authored review artifacts; exclude raw/private evidence."""
import hashlib,json,stat
from pathlib import Path
D=Path(__file__).resolve().parent
ROOT_FILES=['.gitignore','AUDIT.md','AUTHENTICATE.py','AUTHENTICATION_END.json','AUTHENTICATION_START.json','CHECK_PRIOR_REPAIRS.py','CODE_INSPECTION.json','COPY_GUARDS.json','CURRENT_GUARDS.json','DISPOSITION_TEST.json','HELPER_CONTROLS.py','HELPER_CONTROL_RESULTS.json','HELPER_INSPECTION.json','INDEPENDENT_CONTROLS.py','INDEPENDENT_RESULTS.json','INITIAL_RECONSTRUCTION.md','LIVE_PR_INSPECTION.json','LIVE_TARGET_INSPECTION.json','PDF_INSPECTION.json','PRIORITY_ASSESSMENT.json','PRIOR_ISSUE_RESOLUTION.json','README.md','RECEIPT_LINK_EXTENDED_TEST.json','RECEIPT_LINK_TEST.json','REPLAY.py','REPLAY_RECEIPT.json','REPRODUCE.py','REPRODUCTION_RECEIPT.json','RESEARCH_LOG.md','RESULT.json','SOURCE_BODY_PINS.json','SOURCE_INSPECTION.json','VERIFY.py','SEAL.py']
HELPERS=['merge_pr919.py','run_pr919_zenodo.py','append_pr919_tracker.py','update_pr919_publication_ledger.py','finalize_pr919_and_gate_next.py','verify_pr919_disposition_repair.py','verify_pr919_receipt_links.py']
def main():
 allowed=sorted(ROOT_FILES+['reviewed_helpers/'+x for x in HELPERS]+['reviewed_code/package_guard_challenges.py','reviewed_code/copy_guard_challenge.py']);records={}
 for n in allowed:
  p=D/n
  if not stat.S_ISREG(p.lstat().st_mode):raise RuntimeError('nonregular '+n)
  b=p.read_bytes();records[n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 m={'schema':'pr919-full-package-review02-v1','pr':919,'problem_id':'30002555','candidate_revision':2,'candidate_freeze_sha256':'c2c04a478b9f865655fb71b2b87945f01a2f4e41b4a78140e2eea42157f422cd','self_excluded':'MANIFEST.json','explicit_public_allowlist':allowed,'files':records,'private_excluded':['tmp/','__pycache__/','reviewed_code/tmp/','reviewed_helpers/audits/'],'raw_third_party_bodies_extractions_source_renders_credentials_included':False}
 b=(json.dumps(m,indent=2,ensure_ascii=False)+'\n').encode();(D/'MANIFEST.json').write_bytes(b);print(json.dumps({'manifest_sha256':hashlib.sha256(b).hexdigest(),'public_files':len(records)},indent=2))
if __name__=='__main__':main()
