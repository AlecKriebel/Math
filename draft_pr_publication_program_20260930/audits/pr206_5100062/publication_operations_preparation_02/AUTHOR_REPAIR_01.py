from pathlib import Path
D=Path(__file__).resolve().parent
O=D.parent/'publication_operations_preparation_01'
for n in ('ops_common206.py','publisher206.py','tracker206.py','offline_guards.py','run_offline.py'):
 with (D/n).open('xb') as f:f.write((O/n).read_bytes())
p=D/'ops_common206.py'
s=p.read_text().replace("OWN='publication_operations_preparation_01'","OWN='publication_operations_preparation_02'")
s=s.replace(" return {'gate_pin':wanted_gate,'ready_pointer_pin':wanted_ready}",""" wanted_verification=a.get('approved_actual_ready_verification_pin')
 wanted_addendum=a.get('approved_operations_contract_addendum_pin')
 dispatcher=a.get('dispatcher_pin')
 for value,label in [(wanted_verification,'actual ready verification'),(wanted_addendum,'operations contract addendum'),(dispatcher,'adopted dispatcher')]:
  require(type(value) is dict and set(value)=={'bytes','sha256'} and type(value['bytes']) is int and value['bytes']>0 and type(value['sha256']) is str and len(value['sha256'])==64 and all(x in '0123456789abcdef' for x in value['sha256']),'Exact independently adopted '+label+' pin absent')
 addendum_path=base/'ROOT_PUBLICATION_OPERATIONS_CONTRACT_ADDENDUM_01.json';sealed(addendum_path);addendum=read_pinned(addendum_path,wanted_addendum)
 require(addendum.get('schema')=='pr206-root-postready-operations-contract-addendum-v1' and addendum.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and addendum.get('PR')==PR and addendum.get('accepted') is True and addendum.get('original_head')==HEAD,'Root postready operational addendum identity/scope missing')
 require(addendum.get('publication_gate_pin')==wanted_gate and addendum.get('actual_ready_pointer_pin')==wanted_ready and addendum.get('actual_ready_verification_pin')==wanted_verification,'Addendum gate/ready/proof binding differs')
 require(addendum.get('source_family')==OWN and addendum.get('sources')==sources and addendum.get('dispatcher_pin')==dispatcher,'Addendum source/dispatcher contract differs')
 for field in ('scientific_package_metadata_uploads_unchanged','prior_native_selected_original07_files_preserved','operations_sources_approved_after_original_ready_checkpoint','not_a_new_scientific_or_priority_clearance','no_advance_or_completion_granted'):
  require(addendum.get(field) is True,'Postready contract qualifier missing: '+field)
 require(addendum.get('executed_current_sources_claimed_present_in_original_ready_map') is False,'Current operators must not be claimed in original ready map')
 return {'gate_pin':wanted_gate,'ready_pointer_pin':wanted_ready,'ready_verification_pin':wanted_verification,'operations_contract_addendum_pin':wanted_addendum}

def ready_facts(ac,g):
 # These two editorial qualifications are nested facts, not lifecycle receipt aliases.
 facts=ac.get('facts');require(type(facts) is dict and ac.get('phase')=='ready','Actual ready phase/facts missing')
 for field in ('bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','priority_clearance','publication_ready'):
  require(facts.get(field) is True,'Actual ready facts not accepted: '+field)
 require(facts.get('priority_clearance_scope')=='qualified_attributed_note_only','Actual ready qualified-priority scope changed')
 for field in ('priority_novelty_clearance','historical_firstness_independence_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged','completed','advance_to_next_PR_authorized_now','goal_complete'):
  require(facts.get(field) is False,'Unsupported actual ready fact: '+field)
 for field,value in [('case_percent',90),('fully_completed_count',48),('published_count',32),('last_completed_PR',205),('next_numeric_intake_cursor',206)]:
  require(type(facts.get(field)) is int and facts[field]==value,'Actual ready counters/phase differ: '+field)
 require(type(facts.get('NEW_whole_package_reviews_completed')) is int and facts['NEW_whole_package_reviews_completed']==len(g['whole_package_review_events']),'Actual ready review count differs')
 require(facts.get('package')==g['package'] and facts.get('package_seal')==g['package_seal'] and facts.get('Root_publication_gate_pin')==ac['Root_publication_gate_pin'],'Actual ready nested package/gate differs')
 aliases=('Root_publication_gate_pin','package','package_seal','publication_ready','NEW_whole_package_reviews_completed','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','priority_clearance','priority_novelty_clearance','historical_firstness_independence_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged','completed','fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor','advance_to_next_PR_authorized_now','goal_complete')
 for field in aliases:require(type(ac.get(field)) is type(facts.get(field)) and ac.get(field)==facts.get(field),'Actual ready fact alias differs: '+field)

def ready_verification(base,approved,r,ac,selected,mp,gp):
 vp=base/'ROOT_ACTUAL_READY_VERIFICATION_01.json';sealed(vp);v=read_pinned(vp,approved['ready_verification_pin'])
 require(v.get('schema')=='pr206-root-actual-ready-verification-v1' and v.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and type(v.get('PR')) is int and v['PR']==PR,'Independent Root actual-ready verification identity/scope differs')
 for field in ('accepted','actual_ready90_fully_accepted_synced_and_pointer_verified','ready_candidate_changed_paths_exclude_QUEUE_and_all_native_attempts','original_native_custody_retained','every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','all_three_actual_steps_and_six_alias_cleanups_verified'):
  require(v.get(field) is True,'Independent ready verification flag missing: '+field)
 for field in ('actual_original_PR_merged','actual_publication','actual_tracker','advance'):require(v.get(field) is False,'Ready verification grants unsupported action: '+field)
 for field,value in [('completed_count',48),('published_count',32),('cursor',206),('case_completion_estimate_percent',90)]:
  require(type(v.get(field)) is int and v[field]==value,'Independent ready verification counters/phase differ: '+field)
 require(v.get('actual_ready_pointer_pin')==approved['ready_pointer_pin'] and v.get('actual_acceptance_pin')==r['acceptance_pin'] and v.get('actual_selected_map_file_pin')==ac['actual_current_map_file']==pin(mp) and v.get('actual_publication_gate_pin')==approved['gate_pin']==pin(gp),'Independent ready verification pointer/acceptance/map/gate cross-binding differs')
 require(v.get('checkpoint_commit')==ac['checkpoint_commit']==r['checkpoint_commit'] and v.get('actual_main_observed')==ac['main_observed']==r['main_observed'],'Independent ready verification checkpoint/MAIN differs')
 require(type(v.get('selected_files')) is int and type(ac.get('selected_files')) is int and v['selected_files']==ac['selected_files']==len(selected) and v.get('actual_selected_map_sha256')==ac['actual_current_selected_map_sha256'],'Independent full selected-map count/digest differs')
 require(type(v.get('ready_candidate_changed_path_count')) is int and 0<v['ready_candidate_changed_path_count']<=len(selected),'Independent changed-path count missing')
 for field in ('actual_original_PR_head','actual_original_PR_is_draft','actual_original_PR_state'):
  require(type(v.get(field)) is type(ac.get(field)) and v.get(field)==ac.get(field),'Independent ready verification original PR differs: '+field)
 paths={PREFIX+'CURRENT_CASE_STATUS.json',PREFIX+'RESEARCH_LOG.md'}|{'draft_pr_publication_program_20260930/'+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
 records=v.get('all_five_local_readonly_native_postimages')
 require(type(records) is list and len(records)==5,'Exactly five independently verified native postimages required')
 seen=set()
 for record in records:
  require(type(record) is dict and set(record)=={'path','identity','mode','regular'} and type(record['path']) is str and record['path'] in paths and record['path'] not in seen and record['mode']=='0o444' and record['regular'] is True,'Malformed/duplicate/nonreadonly native postimage')
  ident=record['identity'];require(type(ident) is dict and set(ident)=={'bytes','sha256','git_blob'} and type(ident['bytes']) is int and ident['bytes']>=0 and all(type(ident[k]) is str and len(ident[k])==n and all(x in '0123456789abcdef' for x in ident[k]) for k,n in [('sha256',64),('git_blob',40)]),'Malformed native postimage identity')
  require(selected.get(record['path'])==ident,'Native postimage differs from exact accepted historical map');seen.add(record['path'])
 require(seen==paths,'Native postimage path set differs')
 return vp
""")
s=s.replace("'QUEUE_native_original_PR_unchanged','mathematical_clearance','source_contract_clearance','priority_clearance','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','publication_ready'","'original_native_custody_retained','mathematical_clearance','source_contract_clearance','priority_clearance','publication_ready'")
s=s.replace(" require(ac.get('historical_firstness_independence_established') is False,'Historical-priority qualification changed')"," ready_facts(ac,g)\n require(ac.get('historical_firstness_independence_established') is False,'Historical-priority qualification changed')")
s=s.replace(" for rel,p in inputs.items():require(selected.get(PREFIX+rel)==native_identity(p),'Actual ready map does not bind exact input: '+rel)"," ready_verification(base,approved,r,ac,selected,mp,gp)\n for rel,p in inputs.items():require(selected.get(PREFIX+rel)==native_identity(p),'Actual ready map does not bind exact input: '+rel)")
p.write_text(s)
