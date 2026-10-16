from pathlib import Path
import json,hashlib,datetime
O=Path(__file__).resolve().parent
# Deliberate flat author-authored public selection. No recursive publication.
fixed=['RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INITIAL_ATTACK.md','PRIOR_ASSESSMENT_INTAKE.json','MECHANICAL_AUTHENTICATION_INITIAL.json','PREFLIGHT_ATTEMPT01_FAILURE.json','FAMILY_ENGINEERING_AUTHENTICATION.json','FIVE_FAMILY_AUTHENTICATION.json','HISTORICAL_CANDIDATE_AUTHENTICATION.json','PRIOR_EVIDENCE_STRUCTURAL_INTAKE.json','ORIGINAL_METADATA_INTAKE.json','HOSTILE_POSITIVE_CONTROL.json','HOSTILE_POSITIVE_CONTROL.stdout.txt','HOSTILE_POSITIVE_CONTROL.stderr.txt','REVIEWER_HARNESS_ADAPTATIONS.json','test_operations.py.REVIEWER_HARNESS.diff','test_source_gate.py.REVIEWER_HARNESS.diff','ENGINEERING_REPLAY_SUMMARY.json','FINISH_EVIDENCE_ATTEMPT01_FAILURE.json','SOURCE_INSPECTION.json','OWN_SOURCE_RETRIEVAL_METADATA.json','INHERITED_DISPOSITIONS_VERIFIED.json','OPERATIONAL_REVIEW.json','ACTUAL_PREFLIGHT_SUMMARY.json','LEGACY_REPLAY_OBSERVATION.json','PRIVATE_EVIDENCE_METADATA.json','RECORD_SCHEMA_VALIDATION.json','run_reviewer_checks.py','independent_probes.py','probe_native_recovery.py','probe_native_recovery.ATTEMPT01.py','finish_evidence_checks.py','finish_evidence_checks.ATTEMPT01.py','final_authenticate.py','write_result_and_validate.py','seal_public.py']
for stem,modes in [('COLD',['normal','O','OO','env2']),('PROFILE',['normal','O','OO']),('OBSERVATIONS',['normal','O','OO']),('OPERATIONS',['normal','O','OO']),('SOURCE_GATE',['normal','O','OO']),('INDEPENDENT_PROBES',['normal','O','OO']),('NATIVE_RECOVERY',['normal','O','OO']),('LEGACY_FULL',['normal','O','OO'])]:
 for mode in modes:
  for suffix in ['launch.json','stdout.json','stderr.txt']:fixed.append(stem+'_'+mode+'.'+suffix)
for family in ['algebra_falsifier_01','quantum_bridge_01']:
 for suffix in ['launch.json','stdout.json','stderr.txt']:fixed.append('ROUTE_'+family+'.'+suffix)
if len(fixed)!=len(set(fixed)):raise RuntimeError('duplicate allowlist')
records={}
for name in sorted(fixed):
 p=O/name
 if not p.is_file() or p.is_symlink():raise RuntimeError('missing public file '+name)
 b=p.read_bytes();records[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
mandatory={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INITIAL_ATTACK.md','PRIOR_ASSESSMENT_INTAKE.json'}
if not mandatory<=set(records) or any(records[x]['bytes']==0 for x in mandatory):raise RuntimeError('mandatory empty/missing')
manifest={'schema':'pr952-whole-package-review-seal-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer_agent_id':'/root/pr952_full_package_01','pr':952,'problem_id':'10400145','candidate_revision':2,'original_pr_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','files':records,'explicit_public_allowlist':list(records),'private_bodies_extracts_images_fixtures_excluded':True,'clean_review_credit':False,'review_outcome':'complete adverse review; permanent lost early independence; native recovery defect; optional size-one wording clarification'}
raw=(json.dumps(manifest,indent=2)+'\n').encode();(O/'MANIFEST.json').write_bytes(raw)
print(json.dumps({'manifest_sha256':hashlib.sha256(raw).hexdigest(),'files':len(records),'public_payload_bytes':sum(x['bytes'] for x in records.values()),'clean_review_credit':False,'candidate_revision':2},sort_keys=True))
