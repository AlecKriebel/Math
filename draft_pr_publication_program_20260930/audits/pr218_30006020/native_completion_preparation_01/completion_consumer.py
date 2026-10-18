"""Pure externally pinned PR218 actual-terminal consumer. No intake or effects."""
from pathlib import Path
import hashlib,types
BASE=Path(__file__).absolute().parent
MODEL_PIN={'bytes': 40648, 'sha256': '5f6136ae4335dea22e219c7b1b9d62d416a975e9a8d590a9ca617d732627ae3d'}
def model():
 raw=(BASE/'native218_model.py').read_bytes()
 if {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}!=MODEL_PIN:raise RuntimeError('Pinned consumer model changed')
 h=types.ModuleType('pr218_pure_consumer_model');h.__file__=str(BASE/'native218_model.py');exec(compile(raw,h.__file__,'exec'),h.__dict__);return h
def completion_proof(raw,wanted):
 h=model()
 h.bytepin(wanted);h.need(h.exact(h.pin(raw),wanted),'Externally supplied exact actual218 terminal pin')
 proof=h.decode(raw)
 h.matches(proof,{'schema':'pr218-root-actual-completion-verification-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
  'PR':218,'workflow_percent':100,'fully_completed_count':55,'published_count':39,'last_completed_PR':218,
  'next_numeric_intake_cursor':219,'accepted':True,'completed':True,'completed_eligible_workflow':True,
  'publication_workflow_completed':True,'publication_ready':True,'advance_to_next_PR_authorized_now':True,
  'actual_original_PR_merged':True,'adopted_existing_publication':True,'no_new_provider_publication_or_tracker_append':True,
  'all_five_local_files_match_actual_checkpoint':True,'full_scope_verified':True,'all_selected_native_bodies_verified':True,
  'actual_Root_expected_SHA_force_false_ref_update_and_native_readback':True,'original_stable_writer_lock_held_exact':True,
  'foreign_native_tuples_preserved':True,'coherent_before_after_ref':True,'source_gates_verified':True,
  'goal_complete':False,'CAS_or_completion_inferred_from_ancestry':False,'perpetual_or_write_time_Main_equality_claimed':False,
  'numeric_advance_conditional_on_actual_Root_terminal':False,'original_eligible_status':'claimed_solved','current_status':'claimed_solved',
  'current_head':h.CURRENT,'original_merge_commit':h.MERGED,'existing_publication_DOI':h.EXISTING_DOI,
  'existing_tracker_range':h.EXISTING_TRACKER},'Exact typed actual218 terminal facts and authority boundary')
 for key in ('candidate','CAS_target','tree','CAS_target_tree','actual_MAIN_observed','actual_MAIN_tree'):h.need(h.hexid(proof.get(key)),'Native actual terminal identity')
 h.need(proof['candidate']==proof['CAS_target'] and proof['tree']==proof['CAS_target_tree'],'Canonical C/T aliases differ')
 h.need(h.exact(proof.get('old_memberships'),h.source_baseline()) and h.exact(proof.get('new_memberships'),h.completion_memberships()),'Actual exact baseline54/38 plus218 only')
 for key,value in h.completion_memberships().items():h.need(h.exact(proof.get(key),value),'Exact actual membership '+key)
 for key,lower,upper in (('selected_postimage_paths_verified',1,h.MAX_FILES),('protected_body_paths_verified',0,64)):
  h.need(type(proof.get(key)) is int and lower<=proof[key]<=upper,'Truthful bounded native body count')
 for key in ('native_final_ref_UTC','terminal_observation_boundary'):h.need(type(proof.get(key)) is str and bool(proof[key]),'Dated qualified terminal observation')
 checks=proof.get('source_gate_checks')
 h.need(type(checks) is dict and type(checks.get('refreshes_completed_before_record')) is int and checks['refreshes_completed_before_record']>=2 and checks.get('all_exact_pins_and_gates_rechecked_successfully') is True,'Repeated actual source/gate checks')
 return proof
