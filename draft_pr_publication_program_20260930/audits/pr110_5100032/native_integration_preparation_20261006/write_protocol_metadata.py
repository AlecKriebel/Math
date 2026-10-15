#!/usr/bin/env python3
"""Write scoped machine-readable plan/templates and timestamped preparation notes."""
import datetime, hashlib, json, pathlib
import protocol as p
D=pathlib.Path(__file__).resolve().parent
def write(name,value):(D/name).write_bytes(p.canonical(value))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
context=json.loads((D/'CONTEXT_INSPECTION.json').read_bytes())
custody=json.loads((D/'FIXTURE_CUSTODY.json').read_bytes())
review=json.loads((D/'protocol_adversary_20261006/REVIEW.json').read_bytes())
write('EXECUTION_INPUTS_TEMPLATE_DO_NOT_USE_AS_EVIDENCE.json',{
 'schema':'pr110-native-integration-inputs/v1','template_only':True,'execution_mode':'offline_candidate_verification_only',
 'effective':{},'input_files':[],'program_hashes':{}})
write('INPUT_OUTPUT_PROTOCOL.json',{
 'schema':'pr110-native-preparation-interface/v1','UTC':now,'template_or_plan_only':True,
 'no_execution_or_acceptance_authority':True,'PR':110,'problem_id':5100032,'problem_code':p.CODE,
 'original_head':p.HEAD,'original_literal_status':'claimed_solved','original_turns_used':2,'new_central_proof_search_turns':0,
 'source_revision':p.REV,'source_review_hash':p.REVIEW,'statement_hash':p.STATEMENT,'exact_claim':p.CLAIM,
 'canonical_json':{'encoding':'UTF-8','sorted_keys':True,'indent':2,'terminal_newlines':1,
                   'duplicate_keys_allowed':False,'NaN_or_Infinity_allowed':False},
 'execution_document':{'schema':'pr110-native-integration-inputs/v1',
   'exact_fields':['schema','template_only','execution_mode','effective','input_files','program_hashes'],
   'template_only_required_for_actual_inputs':False,'execution_mode':'offline_candidate_verification_only',
   'effective_choice_fields':['main_parent','target','native_before','original','package','publication_receipt','sheet_receipt','runtime',
    'preflight_receipt','preflight_process_contracts','service_process_contracts','native_run_contract',
    'assessment_overlay','campaign_note','attempt_inventory','scope_policy'],
   'program_hash_names':['protocol.py','native_worker.py','native_runner.py','native_launcher.sh'],
   'all_declared_inputs_consumed':True,'gate_pins_excluded_to_avoid_hash_cycle':True},
 'file_pin':{'exact_fields':['path','bytes','sha256'],'path':'canonical relative nonescaping path',
             'bytes':'nonnegative integer, bool rejected','sha256':'64 lowercase hexadecimal characters'},
 'registry_limits':{'inputs':256,'logical_package_files':64,'published_ZIP_bytes':16777216,
                    'native_snapshot_copy_required_in_preparation':False,'raw_SQL_cache_copy_allowed':False},
 'original':{'manifest_pin':p.ORIGINAL_MANIFEST_PIN,'queue_pin':p.ORIGINAL_QUEUE_PIN,
  'sourcepair_authentication_pin':p.SOURCEPAIR_AUTH_PIN,'source_record_pin':p.SOURCE_PIN,
  'nonempty_prior_report_pin':p.PRIOR_PIN,'seventeen_original_paths':sorted(p.ORIGINAL_NAMES),
  'original_queue_row_SHA256':p.ORIGINAL_ROW_SHA,'original_author_log_SHA256':p.ORIGINAL_LOG_SHA,
  'no_recovered_structured_ledger_claim':True,'original_checksum_history_retained':True},
 'runtime':{'required_executables':['python','git','gws','gh','sh'],
  'executable_fields':['absolute_path','bytes','sha256','version'],'queue_py_sha256':p.QUEUE_SHA,
  'private_config_fields':['absolute_path','bytes','sha256','body_private'],'private_bodies_in_public_payload':False,
  'startup_policy':{'python_flags':['-E','-S','-B'],'ambient_environment_inherited':False}},
 'actual_process_envelope':{'required_fields':['actual_receipt','template_only','PID','exit_code','argv','cwd',
  'environment_sha256','UTC_start','UTC_end','stdout','stderr','reaped','termination_reason'],
  'simulated_fixture_or_dry_run_allowed':False,'successful_exit_required':True,'stdout_and_stderr_are_actual_CLI_streams':True},
 'publication_receipt':{'schema':'pr110-actual-publication-receipt/v1',
  'DOI':'genuine future 10.5281/zenodo.<record>; no value selected here',
  'metadata_GET':'one genuine CLI process; its stdout is exact actual raw Zenodo JSON metadata',
  'payload_GET':'one genuine CLI process per PDF/ZIP GET; actual stdout JSON contains response_bytes and response_sha256',
  'download_body':'separate raw pinned transport_body; never labeled stdout',
  'ZIP_member_READBACK':'reuse actual ZIP GET receipt; extracted member body has exact independently checked member bytes',
  'actual_HTTP_per_member_required':False,'batch_one_process_three_GETs_supported_without_reviewed_protocol_correction':False,
  'raw_immutable_service_outputs_must_be_preserved':True},
 'sheet_receipt':{'schema':'pr110-actual-gws-sheet-receipt/v1','spreadsheet_id':p.SHEET,'sheet_id':p.SHEET_GID,
  'sheet_title':p.SHEET_TITLE,'columns':p.COLUMNS,'row_index':None,'range':None,'DOI':None,
  'blank_existing_chat_allowed':True,'new_chat_generation_or_sharing_by_helper':False,
  'operations':['metadata','header','append','readback','independent_readback'],
  'all_actual_distinct_PID_ordered_after_Zenodo':True,'deduplication_checked_by_root_before_append':True},
 'root_gates':{'schema':'pr110-root-native-input-review/v1','roles':p.ROLES,
  'fresh_complete_manifest_binding_required':True,'all_gates_after_fresh_post_service_preflight':True,
  'final_after_all_hashed_antecedents':True,'independent_actual_service_authentication_required':True,
  'two_distinct_whole_package_reviewer_runs_required':True},
 'native_run_contract':{'actual_future_programs_not_authored_here':True,'read_complete_program_sources_before_use':True,
  'required_programs':['native_worker.py','native_runner.py','native_launcher.sh'],
  'program_staging':{'native_worker.py':'<future workspace>/worker.py','native_runner.py':'<future workspace>/runner.py',
                     'native_launcher.sh':'<future workspace>/launcher.sh'},
  'future_workspace':str(D)+'/future_candidates/<fresh one-part label>',
  'actual_limits_applied_readbacks_and_parent_watchdog_required':True,'Darwin_hard_memory_bound_certified':False,
  'future_file_count_cap':512,'allocation_cap_bytes':167772160,'free_headroom_bytes_minimum':33554432,
  'future_commit_reserve_bytes_minimum':8388608,'runtime_reserve_bytes_minimum':8388608},
 'native_inputs':p.NATIVE,'possible_global_offers':['unsolved_math_prioritization/'+n for n in p.DERIVED],
 'protected_unrelated':{'dictionaries':True,'catalog_records':True,'ranks':True,'catalog_list_order':True,
  'CSV_physical_byte_spans':True,'campaign_impact_EV_ranks':True,'historical_JSONL_prefixes':True,
  'review_v2_history':True,'sourcepair_provenance':True,'source_policy_runtime_and_cache':True},
 'functions':{
  'validate_execution':'canonical document bytes + complete authenticated registry + fresh gates + actual reviewed program hash map + genuine invocation UTC',
  'imported_baseline':'genuine dated import UTC + fixed authenticated queue-row and author-log hashes',
  'scoped_outputs':'fresh exact native before/actual after maps + exact reviewed overlay/import event/campaign note/actual DOI'},
 'outputs':{'preconditions_schema':'pr110-offline-protocol-preconditions/v1','native_execution_authorized_by_helper':False,
            'native_acceptance_executed_by_helper':False,'scope_offer':'in-memory dictionary of byte-different allowed names',
            'drift_receipt':'explained unrelated native projections restored to complete baseline records'},
 'required_after_actual_native_run':['actual control and limits receipts','full candidate DIFF','exact affected-path pins',
  'all offers read back','fresh candidate adversary and root review','explicit export boundary','post-export actual readbacks'],
 'unresolved_until_future_boundary':['genuine immutable publication receipt and Sheet range',
  'fresh current main/source/cache/runtime pins','complete actual native program family correctness and filesystem safety',
  'actual resource enforcement and capacity','actual native-assess outputs and candidate review','actual export/install acceptance'],
 'fixture_custody':custody,'independent_adversary_report':'protocol_adversary_20261006/REVIEW.json'})
write('PREPARATION_STATUS.json',{
 'schema':'pr110-offline-native-preparation-status/v1','UTC':now,'preparation_percent':100,
 'source_and_mathematics_percent':100,'bounded_priority_percent':100,'native_integration_percent':0,
 'publication_or_Sheet_done_by_this_effort':False,'native_acceptance_or_export_done':False,
 'source_HEAD':p.HEAD,'sourcepair_prior_nonempty':True,'original_status':'claimed_solved','turns_used':2,
 'new_central_proof_search_turns':0,'actual_native_assess_count':0,'actual_service_calls':0,'Git_mutations':0,
 'observed_main_parent_context':context['observed_main_parent'],'future_main_refresh_required':True,
 'normal_optimized_fixtures':36,'full_native_snapshots_retained':0,
 'only_runtime_code_private_context_bytes':context['single_runtime_code_copy']['bytes'],
 'independent_adversary_report_pin':p.pin((D/'protocol_adversary_20261006/REVIEW.json').read_bytes()),
 'concrete_future_adapter_runner_launcher_missing':True,'overall_publication_research_goal_complete':False,
 'execution_or_export_commissioned':False,'ready_for_parent_review':True})
log='''# PR110 native preparation research log

- 2026-10-06 13:49 UTC — Started scoped offline native preparation, 5% toward this preparation. Root/native policies read; branch main observed. No mathematical search, live native or service operation is part of this effort.
- 2026-10-06 13:52 UTC — Complete current native blobs and all 17 original Git bodies inspected, 30%. Target queued0/5 absent from state; campaign rank126 and catalog rank124 are separate baselines. Original prior report is nonempty and exact. No native snapshot retained; one runtime source copy is private fixture context.
- 2026-10-06 14:02 UTC — First 27 component fixtures pass after fixing a fixture assumption: the actual source URL resides in background rather than a source_url key. Early ad hoc tests are diagnostics, not the authoritative custody run. Preparation 65%; real publication, Sheet and native execution remain 0% for this effort.
- 2026-10-06 14:07 UTC — Independent adversary found protected null-key, self-consistent rewritten inventory, bool/int, process-time/runtime contract and import-provenance gaps. Repairs and labeled historical reproductions preserved. Preparation 75%; estimate decreased as validation exposed missing guards.
- 2026-10-06 14:13 UTC — Canonical manifest/sourcefamily/run-contract path and strict preservation fixtures pass, 90%. Actual normal/optimized commands now have private envelopes. They use synthetic transient services and inert future-program fixtures; no live inputs or approvals are inferred.
- 2026-10-06 14:16 UTC — Explicit source-to-staged-program mapping and launcher invocation added. Strict append-count/startup/environment types strengthened. 36 tests per mode pass; final captured source pins in FIXTURE_CUSTODY.json. Preparation 95%, pending independent current-source seal and concise public payload readback.
'''
log+='- '+now+' — Final exact-source adversarial report authenticated; machine-readable protocol/status/rejecting template completed. Preparation 100% toward a reviewable offline plan, native/publication acceptance still unexecuted. Root must supply genuine services, actual future native source family and fresh input/candidate reviews. No user-owned primary checkout was edited; only this dedicated folder received writes.\n'
(D/'RESEARCH_LOG.md').write_text(log)
print(json.dumps({'metadata_written':True,'UTC':now,'preparation_percent':100,'native_execution_count':0,'service_calls':0}))
