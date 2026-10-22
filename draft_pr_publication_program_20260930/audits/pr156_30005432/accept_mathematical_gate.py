#!/usr/bin/env python3
"""Authenticate sealed independent mathematical families and the immutable original submission."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent
def require(c,m):
 if not c:raise RuntimeError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
S=A/'literal_source_review'
require(digest(S/'INPUT_OUTPUT_BYTEHASH_MANIFEST.json')=='1908a55b8128192f0df4345276076819b6441ddd9c302650f8e69f5ba717456d','Source final seal differs')
require(digest(S/'REVIEW.md')=='f824147e926111293ccc242980093746f049b82df239d2bb4b2ff502f70df969','Final source review differs')
require(digest(S/'RESULT.json')=='b509c580f10971a6243444c8c384c022b5585438f60b63cea947f36acff7700d','Final source result differs')
j=json.loads((S/'INPUT_OUTPUT_BYTEHASH_MANIFEST.json').read_text())
records=[]
for kind in ('inputs','output_files'):
 for r in j[kind]:
  if 'relative_path' in r:p=S/r['relative_path']
  elif 'file' in r:p=S/'private_sources'/r['file']
  else:raise RuntimeError('Unknown source manifest record')
  b=p.read_bytes()
  require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'Source byte identity differs '+str(p))
  records.append({'kind':kind,'path':str(p),'bytes':len(b),'sha256':r['sha256']})
original=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())
require(original['original_head']=='aec31742f3f26c5b1e533404da57539d17dc94a1' and len(original['files'])==22,'Original target/count differs')
for r in original['files']:
 p=Path(r['local_path']);b=p.read_bytes()
 require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'Original byte changed')
 require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['Git_blob'],'Original Gitblob changed')
first=json.loads((A/'ROOT_ALGEBRA_HOLOMORPH_ACCEPTANCE.json').read_text())
require(first['status']=='ROOT_FIRST_TWO_MATHEMATICAL_FAMILY_MANIFESTS_ACCEPTED','First families not accepted')
for r in first['records']:
 b=Path(r['path']).read_bytes();require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'Previously accepted family body changed')
src=json.loads((S/'RESULT.json').read_text())
alg=json.loads((A/'infinite_algebra_review/RESULT.json').read_text())
hol=json.loads((A/'holomorph_review/RESULT.json').read_text())
require(src['gate_decision']=='PASS' and src['ancillary_harness_repair']['optimized_exact_controls']==3788,'Source gate/harness repair missing')
require(alg['mathematical_gate']=='PASS_FOR_SUPPLIED_PROPERTY_S_DEFINITION' and not alg['blocking_mathematical_issues'],'Algebra gate differs')
require(hol['status']=='MATHEMATICAL_PASS' and not hol['mathematical_defects'],'Holomorph gate differs')
repro=json.loads((A/'root_reproduction/RESULT.json').read_text())
require(repro['repaired_bad_eps_fails_both_modes'] and repro['repaired_checker_controls_per_mode']==33512,'ROOT reproduction differs')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rec={'UTC':now,'status':'ROOT_ACCEPTED_EXACT_SOURCE_INFINITE_BRACE_COUNTEREXAMPLE','PR':156,'problem_id':30005432,'original_head':original['original_head'],'original_QUEUE_status':'claimed_solved','original_budget':'2/5','original_files_preserved':22,'original_proof_sha256':'cb127cdc60740596a6e08bd0cb1cfb894b1d24ac8bc56a7338a885798b0a33ae','mathematical_percent':100,'mathematics_cleared':True,'exact_source':'OWR9/2023 printed543 Question1, unrestricted skew left brace; definitions confirmed published CFT2025. Finite/two-sided/global(S) assumptions do not belong to this question.','strongest_verified_result':'Valid infinite left brace on Z×Z4 with x=(0,1) property(s) indices2,2 and additive2x=(0,2) bothindicesinfinite. ExactS=Z×{0,1}, fails additiveclosure and lambda-invariance; multiplicativelynormal; nottwo-sided.','universal_evidence':'Two-bit V4 character/semidirect proof, independent regular holomorph subgroup, exact all-integer coefficient identities, subgroup kernels and distinct Z-cosets. Finite controls supplement universal proof.','families':[
 {'family':'infinite_algebra_review','mechanism':'Universal infinite semidirect group, exact H_z/K_z and all-c classification','controls_each_mode':33516,'negative_mutants_each_mode':4,'review_sha256':digest(A/'infinite_algebra_review/REVIEW.md'),'manifest_sha256':digest(A/'infinite_algebra_review/IO_BYTEHASH_MANIFEST.json')},
 {'family':'holomorph_review','mechanism':'Regular holomorph graph and exact centralizer/stabilizer intersection; torsion/finitequotient boundary','controls_each_mode':243983,'negative_mutations':6,'top_level_corruption_fails_both_modes':True,'review_sha256':digest(A/'holomorph_review/REVIEW.md'),'input_manifest_sha256':digest(A/'holomorph_review/INPUT_SHA256.json'),'output_manifest_sha256':digest(A/'holomorph_review/OUTPUT_SHA256.json')},
 {'family':'literal_source_review','mechanism':'Actual unrestricted source question, full preceding hypotheses, CFT definition and two-sided boundary; adjacent map defect distinguished from conclusion','controls_each_mode':3788,'corrupt_annihilator_claim_fails_both_modes':True,'review_sha256':digest(S/'REVIEW.md'),'manifest_sha256':digest(S/'INPUT_OUTPUT_BYTEHASH_MANIFEST.json'),'initial_scope_assessment_before_ROOT_followup':True}
 ],'ROOT_authenticated_family_records':len(first['records'])+len(records),'source_records':records,'original_normal_controls':33512,'ROOT_repaired_controls_each_mode':33512,'ancillary_repairs':['Original assert checker replaced by raised failures in repaired_diagnostics_v1; false epsilon mutation fails both modes.','Source-context wording must distinguish preceding global(S) discussion from restarted lemma statement and avoid asserting author intent.','The displayed f-map is noninjective even in finite12-element brace; no contradiction to finite quotient theorem conclusion. Global(S) finiteannihilator conclusion has a distinct checked finite-index proof.'],'remaining_mathematical_gap':None,'novelty_established':False,'priority_audit_required_next':True,'new_paper_or_publication_clearance':False,'private_source_bodies_redistributed':False,'MAIN_or_PR_or_index_or_ref_mutations':False,'case_percent':35,'fully_completed_count':30,'published_count':17,'persistent_goal_complete':False}
(A/'ROOT_MATHEMATICAL_GATE.json').write_text(json.dumps(rec,indent=2)+'\n')
status=json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
status.update({'UTC':now,'status':'MATHEMATICAL_GATE_ACCEPTED_PRIORITY_AUDIT_STARTING','case_percent':35,'mathematical_percent':100,'mathematics_cleared':True,'priority_started':True,'ROOT_mathematical_gate':'ROOT_MATHEMATICAL_GATE.json'})
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as h:h.write('\n\n'+now+' — ROOT accepted full mathematical/source gate after reading all three complete proofs/checkers and authenticating'+str(rec['ROOT_authenticated_family_records'])+' family input/output records and22 immutable originals. Counts33,516/243,983/3,788 per mode; negative controls effective. Originalchecker repaired; source-reconciliation caveats precise, finite12-map counterexample concerns certificate not theorem conclusion. Exact unrestrictedOWRQuestion1 answered negatively by universal infinitebrace/cosetproof. Mathematical100%, case35%; nextstage primary-source priority, no novelty or paper clearance. Programme30/dated99=30.30%,17published; persistent goalactive. Shared writer owned by descendingpeer; no MAIN/PR/index/ref writes for156.\n')
print(json.dumps({'status':rec['status'],'family_records_authenticated':rec['ROOT_authenticated_family_records'],'originals_preserved':22,'mathematical_percent':100,'case_percent':35}))
