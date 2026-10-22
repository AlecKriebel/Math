"""Pure externally pinned PR239 actual-terminal consumer. No intake or effects."""
from pathlib import Path
import hashlib,types
BASE=Path(__file__).absolute().parent
MODEL_PIN={'bytes': 51455, 'sha256': 'b6e4ea626d0f63aa6c01c8c923d0afdcb810ef629feb2b3dfd15dc3a1613e64e'}
def model():
 raw=(BASE/'native239_model.py').read_bytes()
 if {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}!=MODEL_PIN:raise RuntimeError('Pinned consumer model changed')
 h=types.ModuleType('pr239_pure_consumer_model');h.__file__=str(BASE/'native239_model.py');exec(compile(raw,h.__file__,'exec'),h.__dict__);return h
def completion_proof(raw,wanted):
 h=model()
 h.bytepin(wanted);h.need(h.exact(h.pin(raw),wanted),'Externally supplied exact actual239 terminal pin')
 proof=h.decode(raw)
 h.matches(proof,{'schema':'pr239-root-actual-completion-verification-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
  'PR':239,'phase':'completion100','new_publication_workflow':True,'workflow_percent':100,'fully_completed_count':56,'published_count':40,'last_completed_PR':239,
  'next_numeric_intake_cursor':240,'accepted':True,'completed':True,'completed_eligible_workflow':True,
  'publication_workflow_completed':True,'publication_ready':True,'advance_to_next_PR_authorized_now':True,
  'actual_original_PR_merged':True,'adopted_existing_publication':False,'no_new_provider_publication_or_tracker_append':False,'new_publication_verified':True,'new_tracker_append_verified':True,
  'all_five_local_files_match_actual_checkpoint':True,'full_scope_verified':True,'all_selected_native_bodies_verified':True,
  'actual_Root_expected_SHA_force_false_ref_update_and_native_readback':True,'original_stable_writer_lock_held_exact':True,
  'foreign_native_tuples_preserved':True,'coherent_before_after_ref':True,'source_gates_verified':True,
  'goal_complete':False,'CAS_or_completion_inferred_from_ancestry':False,'perpetual_or_write_time_Main_equality_claimed':False,
  'numeric_advance_conditional_on_actual_Root_terminal':False,'original_eligible_status':'claimed_solved','current_status':'claimed_solved',
  'current_head':h.CURRENT},'Exact typed actual239 terminal facts and authority boundary')
 for key in ('original_merge_commit','candidate','CAS_target','tree','CAS_target_tree','actual_MAIN_observed','actual_MAIN_tree'):h.need(h.hexid(proof.get(key)),'Native actual terminal identity')
 h.need(proof['candidate']==proof['CAS_target'] and proof['tree']==proof['CAS_target_tree'],'Canonical C/T aliases differ')
 h.need(h.exact(proof.get('old_memberships'),h.source_baseline()) and h.exact(proof.get('new_memberships'),h.completion_memberships()),'Actual exact baseline55/39 plus239 only')
 for key,value in h.completion_memberships().items():h.need(h.exact(proof.get(key),value),'Exact actual membership '+key)
 for key,lower,upper in (('selected_postimage_paths_verified',1,h.MAX_FILES),('protected_body_paths_verified',0,64)):
  h.need(type(proof.get(key)) is int and lower<=proof[key]<=upper,'Truthful bounded native body count')
 for key in ('native_final_ref_UTC','terminal_observation_boundary'):h.need(type(proof.get(key)) is str and bool(proof[key]),'Dated qualified terminal observation')
 checks=proof.get('source_gate_checks')
 h.need(type(checks) is dict and type(checks.get('refreshes_completed_before_record')) is int and checks['refreshes_completed_before_record']>=2 and checks.get('all_exact_pins_and_gates_rechecked_successfully') is True,'Repeated actual source/gate checks')
 h.need(type(proof.get('publication_record_id')) is int and proof['publication_record_id']>0
  and proof.get('publication_DOI')=='10.5281/zenodo.'+str(proof['publication_record_id']),'Actual NEW DOI/id association')
 import re
 h.need(type(proof.get('tracker_range')) is str and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",proof['tracker_range']) is not None,'Actual unique tracker range')
 h.need(proof['original_merge_commit']!=proof['candidate'],'Merge95 and terminal100 commits distinct')
 return proof
