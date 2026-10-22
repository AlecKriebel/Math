"""Independent receipt reconstruction; target errors, counts and service facts, not passed flags alone."""
from pathlib import Path
import json,hashlib,copy,gzip,types
O=Path(__file__).resolve().parent
ERRORS={'reply_extra':'Contradictory parsed reply','reply_wrongbook':'Contradictory parsed reply','reply_bool':'Contradictory parsed reply','reply_bad3':'Contradictory parsed reply','transport_not_applied':'Exact full43 typed prefix plus one ordered batch','formula_type_drift':'Complete typed VALUE/FORMULA response mismatch','old43_type':'Exact full43 typed prefix plus one ordered batch','raw_unknown':'Unknown full raw response/range key changed','metadata_unknown':'Full metadata changed','row_order':'Exact full43 typed prefix plus one ordered batch','partial_existing':'Partial existing batch','no_capacity':'Allocated grid capacity insufficient','owned_no_terminal':'Nonempty pages followed by exactly empty terminal','owned_duplicate_page':'Repeated owned record across pages','owned_http_bool':'Every raw owned page exact HTTP200','owned_pass_drift':'Full typed owned passes drift','owned_bool_id':'Strict full native owned shape/ID','owned_new_alias':'New/changed complete owned identity/scope carrier forPR1263','local_hidden_alias':'New/changed complete local identity/scope carrier forPR1270','source_unknown':'DOI/source/native/PR role or unknown observed-field drift','source_missing_role':'DOI/source/native/PR role or unknown observed-field drift','after_marker_source':'Source/input byte closure drift','after_marker_plan':'Source/input byte closure drift','after_marker_input':'Source/input byte closure drift','after_marker_authority':'Approval evidence changed','after_marker_history':'Durable exact history changed: WRITE_ATTEMPTED.json','after_marker_intent_age':'Durable intent expired','after_candidate_source':'Source/input byte closure drift','after_candidate_authority':'Approval evidence changed','after_candidate_history':'Durable exact history changed: VERIFIED.json','postwrite_new_record':'New/changed complete owned identity/scope carrier forPR1345','postwrite_authority':'Approval evidence changed','edge_native_expiry':'Native/source guard expired at actual edge'}
SUCCESS={'positive2','positive3','transport_applied','nonzero_exact_reply','reply_empty','complete_existing','unrelated_growth'}
POST={'reply_extra','reply_wrongbook','reply_bool','reply_bad3','transport_not_applied','old43_type','raw_unknown','metadata_unknown','row_order','after_candidate_source','after_candidate_authority','after_candidate_history','postwrite_new_record','postwrite_authority'}
def validate(r):
 assert r['world_count']==40 and len(r['controls'])==40 and r['all_passed']is True
 assert {x['mode']for x in r['controls']}==set(ERRORS)|SUCCESS
 for x in r['controls']:
  mode=x['mode'];assert x['passed']is True
  if mode in SUCCESS:
   assert x['error']is None
   if mode=='complete_existing':assert x['append_attempts']==0 and x['result']['status']=='EXACT_EXISTING_BATCH_NOOP'and len(x['result']['positions'])==34
   else:
    assert x['append_attempts']==1 and x['result']['new_rows']==34 and x['result']['new_publications']==0 and x['result']['after_rows']==37 and x['result']['old43_rows_preserved']==3
    assert x['result']['unknown_reply_get_reconciled']is(mode in{'transport_applied','nonzero_exact_reply','reply_empty'})
  else:
   assert x['result']is None and ERRORS[mode]in x['error']and'OWN10MiB'not in x['error']and'150MiB'not in x['error']
   assert x['append_attempts']==(1 if mode in POST else 0)
  assert x['append_attempts']<=1
  if mode in{'reply_extra','after_candidate_source'}:assert x['original_failure']['service_fact']['exact_prefix_plus_batch_observed']is True and x['original_failure']['status']=='UNKNOWN'
  if mode in{'positive2','transport_applied','reply_extra','after_candidate_source'}:assert x['reconciliation']['writes']==0 and x['reconciliation']['can_retry']is False
 return True
if __name__=='__main__':
 r=json.loads((O/'CONTROL_RESULTS05.json').read_bytes());validate(r);mutants=[]
 for mode in['wrong_new_row_count','wrong_expected_error','second_append']:
  bad=copy.deepcopy(r)
  if mode=='wrong_new_row_count':bad['controls'][0]['result']['new_rows']=33
  elif mode=='wrong_expected_error':next(x for x in bad['controls']if x['mode']=='after_candidate_authority')['error']="RuntimeError('OWN10MiB physical guard')"
  else:bad['controls'][0]['append_attempts']=2
  raw=json.dumps(bad,sort_keys=True,separators=(',',':')).encode();h=hashlib.sha256(raw).hexdigest()
  try:validate(bad)
  except AssertionError:mutants.append({'mutation':mode,'hash_consistent_object_sha256':h,'rejected':True})
  else:raise RuntimeError('False expected-output control accepted')
 b={'__name__':'_inert_bootstrap','__file__':str(O/'source/bootstrap.py')};exec(compile((O/'source/bootstrap.py').read_bytes(),b['__file__'],'exec',optimize=0),b)
 try:b['load_verified']('0'*64)
 except RuntimeError as e:assert'Caller-pinned source manifest mismatch'in str(e);badpin=True
 else:raise RuntimeError('Bad caller source pin accepted')
 out={'status':'PASS_INDEPENDENT_ACTUAL_TARGET_EXPECTATION_RECONSTRUCTION','controls':40,'all_actual_target_errors_and_counts_reconstructed':True,'hash_consistent_false_expected_output_controls':mutants,'wrong_caller_source_manifest_pin_actively_rejected':badpin,'source_manifest_sha256':hashlib.sha256((O/'source/SOURCE_MANIFEST.json').read_bytes()).hexdigest(),'source_hash_matches_controls':r['actual_source_hash']==hashlib.sha256((O/'source/SOURCE_MANIFEST.json').read_bytes()).hexdigest(),'real_service_effects':0,'action_authority':False}
 (O/'ACTIVE_CONTROL_EXPECTATION_AUDIT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out))
