from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1];D=A/'fresh_prior_disposition_adversary_20261006'
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return {'file':str(p.relative_to(C)) if p.is_relative_to(C) else str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
M=load(D/'MANIFEST.json');V=load(D/'VERDICT.json');resolution=load(D/'SUPERSEDED_INPUT_RESOLUTION.json');checked=[]
def verify(row,base=D):
 p=Path(row['path']);p=p if p.is_absolute() else base/p
 if str(p)==resolution['superseded_original_path'] and row['sha256']==resolution['superseded_pin']['sha256']:
  require(row['bytes']==resolution['superseded_pin']['bytes'],'superseded mismatch');p=Path(resolution['matching_archive']['path'])
 require(p.is_file() and not p.is_symlink(),'invalid pin path: '+str(p))
 require(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'pin mismatch: '+str(p));checked.append(pin(p))
for name in ['INPUT_MANIFEST_INITIAL.json','INPUT_MANIFEST_POST_FREEZE.json','INPUT_MANIFEST_CURRENT_V2.json','INPUT_MANIFEST_SUPPLEMENTAL_REPORTS.json']:
 for row in load(D/name)['inputs']:verify(row)
for row in M['outputs']:verify(row)
verify(load(D/'FINAL_CLOSURE_BODY_PIN.json')['current_final_input']);verify(resolution['matching_archive'])
require(V['status']=='bounded_already_solved_disposition_defensible' and V['candidate_math_sound_after_minor_repairs'] and V['entire_advertised_hardness_bundle_elementary_published_corollary'],'fresh verdict')
require(V['close_without_merging_defensible'] and V['no_DOI_or_new_paper_or_publication_tracker_row_defensible'] and not V['gate_pending_for_actual_novelty_access_or_model_gap'],'fresh service scope')
require(sha(D/'REPORT.md')==V['report_sha256'] and sha(A/'PROPOSED_CLOSURE_COMMENT_20261006.md')==V['final_closure_body_sha256'],'report/body pins')
require(sha(A/'repaired_diagnostics_v2/PROOF.md')==V['current_proof_sha256'],'current proof pin')
math=load(A/'ROOT_MATHEMATICAL_GATE_20261006.json');effective=load(A/'CURRENT_EFFECTIVE_ARTIFACTS_20261006.json');priority=load(A/'ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json')
require(math['mathematical_clearance'] and priority['three_families_final'] and effective['metadata_only_update_since_cleared_math_gate'],'root gate prerequisites')
for r in effective['pins']:verify({'path':str(A/r['file']),'bytes':r['bytes'],'sha256':r['sha256']})
O=A/'original_source_authentication_20261006/original_attempt';require(sha(O/'PROOF.md')==math['original_immutable_proof_sha256'],'original proof drift')
require([json.loads(t)['turn'] for t in (O/'turns.jsonl').read_text().splitlines()]==[1],'original effort ledger')
out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'fresh_adversary_final_report_read_by_root':True,'final_clarity_delta_read_by_root':True,'all_retained_inputs_and_outputs_authenticated':True,'superseded_comment_bytes_authenticated_from_exact_archive':True,'fresh_manifest':pin(D/'MANIFEST.json'),'checked_pins':checked,'verdict':V,'public_paths':[str((D/r['path']).relative_to(C)) for r in M['outputs']]+[str((D/'MANIFEST.json').relative_to(C))]}
(A/'ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
ready={'schema':'pr107-root-disposition-ready/v1','UTC':out['UTC'],'actual_operator_PID':os.getpid(),'PR':107,'problem_id':30003997,'original_head':math['original_head'],'original_literal_status':'claimed_solved','original_budget':'1/5','new_central_proof_search_turns':0,'mathematical_clearance':True,'three_priority_families_authenticated':True,'fresh_final_disposition_review_authenticated':True,'complete_restricted_hardness_prior_corollary_verified':True,'no_substantive_new_contribution_established':True,'native_status_correction_supported':True,'proposed_native_status':'already_solved','exact_claim':math['exact_claim'],'exact_general_3SAT_identity_verified':True,'exact_general_3SAT_identity_priority':'unresolved; no independently consequential new theorem established','earliest_priority_established':False,'prior_cost_table_theorem_printed_verbatim':False,'closing_comment_file':'PROPOSED_CLOSURE_COMMENT_20261006.md','closing_comment_sha256':sha(A/'PROPOSED_CLOSURE_COMMENT_20261006.md'),'global_queue_sha256_before':sha(C/'unsolved_math_prioritization/QUEUE.md'),'current_effective_package':'repaired_diagnostics_v2','publication_authorization':False,'DOI':None,'Zenodo_actions':False,'tracker_actions':False,'same_head_closure_pending':True,'native_commit_readback_pending':True,'PR_workflow_percent':75,'persistent_goal_status':'active'}
(A/'ROOT_DISPOSITION_READY_20261006.json').write_text(json.dumps(ready,indent=2,ensure_ascii=False)+'\n')
prog=load(P/'CURRENT_PROGRESS.json');prog.update({'UTC':out['UTC'],'updated_UTC':out['UTC'],'current_priority_audit_percent':100,'current_priority_clearance':False,'current_novelty_established':False,'current_already_solved_corollary_disposition_ready':True,'current_fresh_final_disposition_review_authenticated':True,'current_priority_gate':'audits/pr107_30003997/ROOT_DISPOSITION_READY_20261006.json','current_repaired_diagnostics':'audits/pr107_30003997/repaired_diagnostics_v2','current_mathematical_checkpoint':'a0865fd15ce0e67b0474bd54389f264376502622','current_mathematical_checkpoint_remote_verified':True,'current_PR_workflow_percent':75,'current_workflow_estimate_percent':75,'current_fresh_disposition_agent':'pr107_fresh_prior_disposition_adversary_20261006','next_step':'Release source-bound prior-corollary disposition evidence, close same-head PR107, run native assess/status and verify committed remote readback.','remaining_current_step':'Actual closure and native main release/readback; no paper, DOI or tracker.','advance_to_next_PR_authorized_now':False,'persistent_goal_complete':False,'persistent_goal_status':'active'})
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(prog,indent=2,ensure_ascii=False)+'\n')
log=out['UTC']+': PR107 mathematical100%, bounded prior-corollary priority100%, workflow75%. Three priority families and fresh final disposition adversary authenticated. Complete restricted hardness follows from Chapoullié–Szigeti2022 Theorem13 proof; no substantive novelty established. Exact optimum identity verified, exact historical priority unresolved. Effective v2 metadata/guards/actual receipts current; original1/5 preserved, new proof turns0. Same-head closure/native main release pending. No paper/DOI/tracker; goal active15/99.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+log)
selected=priority['selected_family_public_paths']+out['public_paths']
for directory in [A/'root_priority_20261006',A/'repaired_diagnostics_v2',A/'effective_prior_package_v2_validation_20261006']:
 selected += [str(p.relative_to(C)) for p in directory.iterdir() if p.is_file()]
for p in A.glob('*.py'):selected.append(str(p.relative_to(C)))
names=['CURRENT_EFFECTIVE_ARTIFACTS_20261006.json','EFFECTIVE_PRIOR_PACKAGE_V2_PROPAGATION_20261006.json','ROOT_PRIORITY_ADJUDICATION_20261006.md','ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json','ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json','ROOT_DISPOSITION_READY_20261006.json','PROPOSED_CLOSURE_COMMENT_20261006.md','RESEARCH_LOG.md']
selected += [str((A/n).relative_to(C)) for n in names]+[str((P/n).relative_to(C)) for n in ['CURRENT_PROGRESS.json','RESEARCH_LOG.md']]
for label in ['root_priority_primary','root_prior_family_check','root_prior_family_check_positive_completion','effective_prior_package_v2','effective_prior_package_v2_validation','effective_prior_package_v2_receipts','authenticate_priority_families']:
 selected += [str(p.relative_to(C)) for p in (A/'actual_operations'/label).iterdir() if p.is_file()]
for d in [A/'actual_checkpoints/math_release']:
 selected += [str((d/n).relative_to(C)) for n in ['RECEIPT.json','PROCESS_JOURNAL.json']]
selected += [str(p.relative_to(C)) for p in (A/'actual_operations/math_release').iterdir() if p.is_file()]
require(all('private_sources' not in Path(p).parts for p in selected),'private primary material selected')
(A/'PRIOR_DISPOSITION_CHECKPOINT_SELECTION_20261006.json').write_text(json.dumps({'paths':sorted(set(selected))},indent=2)+'\n')
print(json.dumps({'actual_operator_PID':os.getpid(),'authenticated_fresh_pins':len(checked),'public_selection_paths':len(set(selected)),'ready':True,'workflow_percent':75}))
