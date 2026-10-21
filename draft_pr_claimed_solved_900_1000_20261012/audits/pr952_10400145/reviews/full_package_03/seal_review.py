"""Explicitly select only own public reasoning/code/metadata/actual receipts."""
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent
names='''RESULT.json FULL_AUDIT.md RESEARCH_LOG.md AUTHENTICATION_START.json AUTHENTICATION_END.json COLD_REPLAY.json INITIAL_ATTACK.md PRIOR_ASSESSMENT_INTAKE.json ACTUAL_START_PREFLIGHT_SUMMARY.json ACTUAL_END_PREFLIGHT_SUMMARY.json ADDITIONAL_REPLAY.json CLOSURE_AND_PRESENTATION.json FAMILY_APPROACH_REVIEW.json GW_RETRIEVAL.json HISTORICAL_VALIDATION.json INHERITED_DISPOSITIONS_VERIFIED.json MATH_REVIEW.md NEW_RECOVERY_REPLAY.json ORIGINAL_FILE_INSPECTION.json PRIORITY_REVIEW.md PRIOR_ISSUES_VERIFIED.json PUBLICATION_REVIEW.md SOURCE_INSPECTION.json SOURCE_RETRIEVALS.json SOURCE_RETRIEVALS_ADDITIONAL.json SUITE_REPLAY.json authenticate.py format_authentication.py independent_recovery_probe.py independent_torsion_probe.py inspect_closures.py inspect_originals.py run_additional_replays.py run_cold.py run_suites.py write_review_notes.py prepare_report.py validate_report.py take_end.py seal_review.py REPLAYED_independent_boundaries_probe.py REPLAYED_independent_operations_probe.py REPLAYED_FAMILY_INDEPENDENT_CHECKS.py REPLAYED_FAMILY_independent_controls.py REPORT_VALIDATION_pre.json'''.split()
for name in ['REPORT_VALIDATION_chain.json','BOUNDARY_ATTEMPTS.json']:
 if (R/name).exists():names.append(name)
prefixes=('COLD_','SUITE_','NEW_MATH_','NEW_RECOVERY_','FLOW_REPLAYED_','LEGACY_','ORIGINAL_MUTATIONS.','ENGINEERING_FINAL_SEAL.','FAMILY_','END01_','END02_','END03_','REPORT_CHECK_')
for p in R.iterdir():
 if p.is_file() and p.name.startswith(prefixes) and p.name.endswith(('.stdout.raw','.stderr.raw','.launch.json')):names.append(p.name)
names=sorted(set(names));files={}
for name in names:
 p=R/name
 if not p.is_file() or p.is_symlink():raise RuntimeError('explicit selected file missing/nonregular: '+name)
 raw=p.read_bytes();files[name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
required={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INITIAL_ATTACK.md','PRIOR_ASSESSMENT_INTAKE.json'}
if not required<=set(files) or any(not (R/n).read_bytes().strip() for n in required):raise RuntimeError('all mandatory actual nonempty records')
doc={'schema':'pr952-full-package-review-public-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer_agent_id':'/root/pr952_full_package_03','files':files,'explicit_public_allowlist':names,'excluded_private_material':'All private primary bodies/extracts/images, download caches, mechanical raw preflight outputs, observations, fixtures and transient working trees; MANIFEST itself.','derived_code_note':'REPLAYED programs are explicitly attributed adaptations/copies, not claimed as new designs; exact sources/diffs recorded. New designs are independent_torsion_probe and independent_recovery_probe.','authority':'Independent scoped review only; no mutation or acceptance authority.'}
(R/'MANIFEST.json').write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n')
print('EXPLICIT_PUBLIC_MEMBERS',len(files),'MANIFEST_SHA256',hashlib.sha256((R/'MANIFEST.json').read_bytes()).hexdigest())
