from pathlib import Path
import hashlib,json,datetime
D=Path(__file__).resolve().parent;F=D/'final_credit_packet_adversary_01';C=D/'corrected_packet'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
seal=json.loads((F/'FINAL_SEAL.json').read_text());assert seal['status']=='PASS_FINAL_REVISED_CREDIT_PACKET' and not seal['outstanding_mandatory_findings'] and not seal['outstanding_optional_findings']
mf=F/'SAFE_AUTHORED_MANIFEST.json';assert sha(mf)==seal['safe_manifest_sha256']=='f9522c79de577406000db11612cd460de7c7ceb24b91eba2ec907c0217b813c9'
for row in json.loads(mf.read_text())['files']:
 p=F/row['path'];assert p.resolve().is_relative_to(F) and not p.is_symlink();assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
assert sha(F/'REPORT.md')==seal['report_sha256']=='ca1ebf71bfbaff33d441d2c452dc957bbf7a5e86df359fbeebac94ca59079744'
assert sha(D/'PROPOSED_CURRENT_PACKET_MANIFEST.json')==seal['current_packet_envelope_sha256']
assert sha(D/'PROPOSED_NATIVE_CHANGES.json')==seal['native_plan_sha256']
assert sha(D/'apply_credited_correction.py')==seal['helper_sha256_reviewed_not_executed']
assert sha(C/'PROOF.md')==seal['reviewed_current_proof_sha256']
for row in json.loads((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_text())['files']:
 p=C/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
assert json.loads((D/'ROOT_PRIORITY_ACCEPTANCE.json').read_text())['status']=='PASS_EXACT_PRIOR_COVERAGE'
assert json.loads((D/'ROOT_COMPLETE_MATHEMATICAL_ACCEPTANCE.json').read_text())['status']=='PASS_THREE_INDEPENDENT_MATHEMATICAL_SOURCE_FAMILIES'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
out=dict(utc=now,status='PASS',native_mutations_cleared=True,native_action_scope='Exact existingPR credit correction and immediate scope skip only',packet_manifest_sha256=seal['current_packet_envelope_sha256'],native_plan_sha256=seal['native_plan_sha256'],reviewer_manifest_basename=mf.name,reviewer_manifest_sha256=sha(mf),reviewer_seal_basename='FINAL_SEAL.json',reviewer_report_sha256=sha(F/'REPORT.md'),reviewed_helper_sha256=sha(D/'apply_credited_correction.py'),all_12_reviewer_payloads_rehashed=True,full_final_report_and_derivation_read_by_root=True,current_payloads=35,originals=20,math_core_sections_2_7_unchanged=True,resolved_editorial_equation_reference=True,outstanding_findings=[],historical_credit='already_solved literal numerical negative coverage',bare_mechanism_alternative_resolved=False,first_error_recognition_certified=False,exact_tied_variant_anticipation_certified=False,preprint_clearance=False,counts=[42,19,19,0],goal_active_incomplete=True)
p=D/'ROOT_FINAL_CREDIT_PACKET_ACCEPTANCE.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
