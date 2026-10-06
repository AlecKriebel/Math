"""Persist ROOT's personally reviewed scientific decision; no native actions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,sys
A=Path(__file__).resolve().parent;R=A.parents[2]
def pin(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_bytes())
def main():
 assert sys.flags.ignore_environment and sys.flags.optimize==0 and sys.flags.dont_write_bytecode
 final=A/'final_partial_whole_record_adversary_20261004';prep=A/'native_integration_preparation_20261004'
 v=load(final/'VERDICT.json');assert v['verdict']=='CLEAN' and not v['essential_repairs'] and v['current_scientific_status']=='partial'
 assert v['historical_novelty_certified'] is False and v['intended_original_target_historically_already_solved_certified'] is False
 assert load(A/'ROOT_final_whole_record_closure_readback_20261004/READBACK.json')['status']=='PASS'
 assert load(A/'ROOT_completed_native_preparation_readback_20261004/READBACK.json')['status']=='PASS'
 scope={'id':'PR73-complete-connected-theorem-attributed-partial-priority-unestablished-v1',
 'text':'Accept the complete prescribed connected genus-three symplectic counterexample as a verified attributed partial research record. Partial describes incomplete historical novelty/target-priority determination, not an incomplete proof. The disconnected-surface version has prior negative evidence; no prior historical resolution of the intended connected target and no novel open-problem resolution are certified.',
 'excluded_scopes':['CP2 specialization','Existence of a different suitable degree-one representative','Effective high-degree existence bounds','Certification of novelty or firstness','Historical already-solved classification of the intended connected target','Processing PRs ineligible at literal claimed_solved intake']}
 auth=A/'original_source_authentication_20261004'
 evidence=[auth/n for n in ['ORIGINAL_AUTHENTICATION.md','ORIGINAL_AUTHENTICATION.json','ORIGINAL_BLOB_MANIFEST.json','SOURCEPAIR_AUTHENTICATION.json']]
 evidence += [auth/'original/unsolved_math_prioritization/attempts/2985'/n for n in ['CANDIDATE.md','source_record.json','readiness.json','turns.jsonl']]
 evidence += [R/'unsolved_math_prioritization'/n for n in ['manifest.json','catalog.json','queue.py','policy.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite']]
 local=['ROOT_MATHEMATICAL_GATE_20261004.json','ROOT_FINAL_MATHEMATICAL_GATE_SUPPLEMENT_20261004.json',
 'ROOT_custody_and_original_replay_v2_20261004/READBACK_AND_REPLAY.json','ROOT_final_mathematical_family_readback_v3_20261004/READBACK.json',
 'ROOT_BOUNDED_PRIORITY_AUDIT_20261004.json','ROOT_completed_priority_family_readback_20261004/READBACK.json',
 'ROOT_repaired_disposition_readback_v2_20261004/READBACK.json','ROOT_final_whole_record_closure_readback_20261004/READBACK.json',
 'ROOT_completed_native_preparation_readback_20261004/READBACK.json',
 'geometric_smoothing_adversary_20261004/ADVERSARIAL_REPORT.md','covering_homology_adversary_20261004/REPORT_v2.md','covering_homology_adversary_20261004/HOMOLOGY_DERIVATION_v2.md',
 'exact_target_priority_20261004/REPORT.md','exact_target_priority_20261004/VERDICT.json','exact_target_priority_20261004/FINAL_SEAL.json',
 'quotient_mechanism_priority_20261004/REPORT.md','quotient_mechanism_priority_20261004/FINAL_SEAL.json',
 'fresh_disposition_adversary_20261004/REPORT.md','fresh_disposition_adversary_20261004/VERDICT.json','fresh_disposition_adversary_20261004/FINAL_SEAL.json',
 'final_partial_whole_record_adversary_20261004/REPORT.md','final_partial_whole_record_adversary_20261004/VERDICT.json','final_partial_whole_record_adversary_20261004/FINAL_SEAL.json',
 'final_partial_whole_record_adversary_20261004/FINAL_MANIFEST.json','final_partial_whole_record_adversary_20261004/TAIL_READBACK.json',
 'native_integration_preparation_20261004/PREPARATION_REPORT_V2.md','native_integration_preparation_20261004/PREPARATION_REPORT_V2.json',
 'native_integration_preparation_20261004/PREPARATION_MANIFEST_V2.json','native_integration_preparation_20261004/PREPARATION_SEAL_RECEIPT_V2.json',
 'native_integration_preparation_20261004/FINAL_MANIFEST_READBACK.json','native_integration_preparation_20261004/independent_structural_review/FINAL_V2_REVIEW.json']
 evidence += [A/n for n in local]
 operators=[prep/n for n in ['native_common_v2.py','ROOT_native_integration_v2.py','ROOT_native_readback_v2.py','ROOT_GATE_SCHEMA_V2.json','FROZEN_PLAN_SCHEMA_V2.json','EXECUTION_README_V2.md']]
 operators += [A/'ROOT_prepare_frozen_native_execution_20261004.py']
 packet=[pin(Path(x['path'])) for x in v['reviewed_V3_packet'] if Path(x['path']).name in ['CURRENT_RESULT.md','CURRENT_PRIORITY.md','PR_BODY.md','DISPOSITION_PROPOSAL.json']]
 assert len(packet)==4
 output=A/'ROOT_FINAL_SCIENTIFIC_PARTIAL_DISPOSITION_20261004.json';assert not output.exists()
 public=[A/n for n in local if n not in ['ROOT_custody_and_original_replay_v2_20261004/READBACK_AND_REPLAY.json']]
 public += [A/'attributed_result_preparation_v3_20261004'/n for n in ['CURRENT_RESULT.md','CURRENT_PRIORITY.md','PR_BODY.md','DISPOSITION_PROPOSAL.json','README.md','MANIFEST.json']]
 public += operators+[output,A/'ROOT_operational_ACK_transition_finding_20261004.md',A/'ROOT_verify_final_whole_record_closure_20261004.py',A/'ROOT_verify_completed_native_preparation_20261004.py',Path(__file__),A/'RESEARCH_LOG.md']
 public += [prep/'independent_structural_review'/n for n in ['FINAL_V2_REVIEW.md','ACK_HANDOFF_SUPPLEMENT.md','PENDING_ASSEMBLER_REVIEW.md','PENDING_ASSEMBLER_REVIEW.json']]
 # Immutable reviewer originals may be read-only. Preserve their modes and
 # publish byte-identical 0644 copies rather than changing sealed evidence.
 published=[];copies=[];copydir=A/'ROOT_PUBLIC_READONLY_REPORT_COPIES_20261004'
 for p in dict.fromkeys(public):
  if p==output:published.append(p);continue
  assert p.is_file() and not p.is_symlink(),str(p)
  mode=stat.S_IMODE(p.stat().st_mode)
  assert mode in [0o644,0o444],str(p)
  if mode==0o644:published.append(p);continue
  if not copies:copydir.mkdir(exist_ok=False)
  q=copydir/str(p.relative_to(A)).replace('/','_');b=p.read_bytes();q.write_bytes(b);q.chmod(0o644)
  assert q.read_bytes()==b
  copies.append({'immutable_source':pin(p),'source_mode':oct(mode),'public_copy':pin(q),'public_mode':'0o644'})
  published.append(q)
 if copies:
  cm=copydir/'COPY_MANIFEST.json'
  cm.write_text(json.dumps({'purpose':'Byte-identical public copies of immutable read-only reviewer analysis; original source modes and bytes remain untouched.','copies':copies},indent=2)+'\n')
  published.append(cm);evidence.append(cm)
 paths=list(dict.fromkeys(str(p.relative_to(R)) for p in published))
 decision={'schema':'pr73-final-root-attributed-partial-disposition/v1','status':'PASS','UTC':datetime.now(timezone.utc).isoformat(),
  'authorizer':'ROOT','actual_PID':os.getpid(),'actual_cwd':os.getcwd(),'actual_argv':sys.argv,'PR':73,'problem_id':'2985',
  'reviewed_head':'6f82e81631fd43abc0140a831acfb43c150f4210','eligible_intake_literal_status':'claimed_solved','native_current_status':'partial',
  'ROOT_certified_attributed_partial_disposition':True,'ROOT_personally_read_final_reports':True,'final_fresh_adversarial_review_clean':True,
  'mathematics_validated':True,'accepted_as':'verified_attributed_partial_result','scope_interpretation':scope,
  'novelty_clearance':False,'no_prior_target_resolution_inferred':True,'new_paper':False,'publication_DOI':None,'tracker_append':False,
  'frozen_packet':packet,'bound_evidence':[pin(p) for p in evidence],'bound_operators':[pin(p) for p in operators],
  'scientific_claims':{'full_prescribed_connected_theorem_verified':True,'genus':3,'square':4,'primitive_integral_divisor_lift_verified':True,
   'cover_H3':'Z','base_H3':'0','deck_H3_action':-1,'disconnected_surface_version_prior_verified':True,
   'connected4D_novelty':'unestablished','bounded_priority_audit_complete':True,'original_target_historical_already_solved_certified':False,
   'new_open_problem_resolution_certified':False,'remaining_gap':'Historical novelty of the connected4D extension and intended original connectedness convention; no mathematical proof gap.'},
  'original_readiness_preserved':True,'original_budget':'1/5','original_turn_events':1,'new_original_proof_turns':0,
  'native_wrapper_prior_report':'PRESENT_JSON_NULL','raw_prior_report':'ABSENT','SQL_prior_report':{},
  'superseded_proposals':['attributed_result_preparation_v1_20261004','ROOT_BOUNDED_PRIORITY_AUDIT_20261004.json: dated already_solved proposal only'],
  'scope_authority_interpretation':'ROOT applies the later literal claimed_solved restriction to immutable intake and preserves the original human instruction to accept valid partial findings without a paper. This is an explicit combined-scope interpretation, not a quotation from the narrowed goal file. No excluded PR is processed; no PR50 publication exception is extended.',
  'public_safe_files':paths,'ROOT_certifies_listed_complete_public_contents':True,
  'human_peer_review':False,'formal_proof_certification':False,'AI_tools_used_extensively':True,
  'scientific_review_percent':100,'bounded_priority_audit_percent':100,'PR_workflow_estimate_percent':70,
  'merge_or_native_acceptance_performed':False,'operational_authorization_requires_separate_exact_plan_gate_and_actual_ACK':True}
 output.write_text(json.dumps(decision,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':'PASS_SCIENTIFIC_ONLY','decision':pin(output),'bound_evidence':len(evidence),'public_safe_paths':len(paths),'native_or_PR_mutation':False}))
if __name__=='__main__':main()
