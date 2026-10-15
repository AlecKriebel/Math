"""Normalize current PR190 campaign facts, preserving retired historical values."""
import copy,datetime
CASE='audits/pr190_5000007/'
def require(x,msg):
 if not x:raise RuntimeError(msg)
def normalize(j,phase):
 require(phase in [95,100] and j['current_PR']==190,'Wrong campaign phase/case')
 expected=(38,22,184) if phase==95 else (39,23,190)
 require((j['fully_completed_count'],j['published_count'],j['last_completed_PR'])==expected,'Campaign factual census drift')
 retired=['actual_factual_checkpoint_accepted','active_checkpoint_commit','last_completed_writer_operation_finished','read_only_next_case','next_intake_requires_actual_completion_receipt_and_explicit_writer_release']
 if 'retired_stale_live_aliases_20261015' not in j:
  j['retired_stale_live_aliases_20261015']={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'reason':'Historical values retained here; these aliases had ceased to describe current campaign authority. No exclusive writer window or self-referential future commit is invented.','values':{k:copy.deepcopy(j[k]) for k in retired if k in j}}
 for k in retired:j.pop(k,None)
 total=j['dated_eligible_total'];require(total==99,'Dated denominator changed; reassess fraction')
 j['fully_completed_fraction_percent']=round(100*j['fully_completed_count']/total,2)
 j['workflow_estimate_percent']=j['fully_completed_fraction_percent']
 j['workflow_estimate_definition']=str(j['fully_completed_count'])+'/dated99 completed,'+str(j['published_count'])+' published; dated denominator is not a fresh eligibility census.'
 j['last_completed_actual_final_receipt']=('audits/pr184_10300044/' if phase==95 else CASE)+'ROOT_FINAL_FACTUAL_ACCEPTANCE.json'
 j['last_actual_intake_checkpoint_commit']='4c81b9a4eb4308842311e2658db41d9a961ab0d5'
 j['last_actual_intake_checkpoint_release']=CASE+'INTAKE_CHECKPOINT_ACCEPTANCE.json'
 j['latest_ordered_intake_record']='status_intakes_after_pr184/PR190_ORIGINAL_STATUS_INTAKE.json'
 j['latest_ordered_intake_records']=['status_intakes_after_pr184/PR'+str(n)+'_ORIGINAL_STATUS_INTAKE.json' for n in range(185,191)]
 j['next_intake_requires_actual_completion_receipt']=True
 j['next_intake_requires_explicit_writer_release']=False
 j['peer_pause_or_exclusive_writer_window_assumed']=False
 j['next_eligible_PR_after_current_completion']=None
 j['next_eligible_order_requires_fresh_status_check']=True
 j['current_mathematical_result_valid']=True
 j['current_mathematical_scope']='Imported bare-angle distance-two exclusion FALSE by exactly two proper face diagonals; explicitly adopted parity-selected unbounded endpoint exclusion PROVED.'
 j['current_source_formulation_issue']=True
 j['current_source_disambiguation_not_author_authenticated']=True
 j['current_source_author_authenticated_erratum']=False
 j['current_source_unique_intent_certified']=False
 j['current_current_primary_overlap_verified']=True
 j['current_DOI_file_identity_verified']=True
 j['current_publication_gate']=CASE+'ROOT_PUBLICATION_GATE.json'
 j['current_frozen_packet_pending_flags_describe_assembly_time']=True
 if phase==95:
  j['remaining_current_step']='PR190 original-head two-parent MAIN integration, full current-tree acceptance and factual completion; only then original-status-only intake191.'
  j['next_step']=j['remaining_current_step']
  j['program_snapshot_authority_condition']=CASE+'ROOT_ACTUAL_MERGE_ACCEPTANCE.json must authenticate the original-head two-parent merge and every selected identity at observed MAIN; then factual completion acceptance is required. Counts remain38/22 until factual acceptance.'
  j['active_checkpoint_acceptance_receipt']=CASE+'ROOT_ACTUAL_MERGE_ACCEPTANCE.json'
  j['completion_metadata_checkpoint_pending_at_snapshot']=True
 else:
  j['remaining_current_step']='None for PR190 after actual factual MAIN acceptance; original-status-only intake191 next.'
  j['next_step']=j['remaining_current_step']
  j['program_snapshot_authority_condition']=CASE+'ROOT_FINAL_FACTUAL_ACCEPTANCE.json authenticates actual MAIN, factual parent/full scope and combined selected current identities. This prepared postimage is effective only after that acceptance.'
  j['active_checkpoint_acceptance_receipt']=CASE+'ROOT_FINAL_FACTUAL_ACCEPTANCE.json'
  j['completion_metadata_checkpoint_pending_at_snapshot']=False
  j['last_completed_source_author_authenticated_erratum']=False
  j['last_completed_source_unique_intent_certified']=False
  j['last_completed_DOI_file_identity_verified']=True
 return j
