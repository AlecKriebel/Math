"""Own-folder inert templates/documentation only. No prepare or native calls."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,datetime,hashlib
import v3_guards as g
import prepare_review_bundle as h
D=Path(__file__).resolve().parent;A=D.parent.parent;C=A.parents[2]
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,obj):(D/name).write_bytes(g.canonical(obj))
def pin(path):
    data=path.read_bytes();return {'path':str(path.relative_to(C)),'bytes':len(data),'sha256':g.sha(data)}
programs=[pin(D/name) for name in g.PROGRAMS]
effective={name:None for name in g.CHOICES}
effective.update(execution_mode='review_bundle_only',scoped_rank_interpretation='preserve_baseline_labels_and_positions_not_global_rerank',
    package={'root':None,'manifest':None},publication={'receipt':None},google_sheet={'receipt':None,'row_index':None,'values':[None,'',None,None],'existing_chat_authorized':False},
    original_authentication_pins={'blob_manifest':None,'queue_projection':None,'sourcepair':None,'selected_prior':None,'original_files':[]},
    effective_diagnostics_pins=[],native_baseline_pins=[],raw_source_pins={'problems.json':None,'research_results.json':None},
    runtime={'python_executable':None,'python_version':None,'python_binary':None,'git_executable':None,'git_binary':None,'gh_executable':None,'gh_binary':None},
    process_policy={'max_process_count':64,'retain_bytes_per_stream':4096,'max_stdout_bytes':32*1024*1024,'max_stderr_bytes':65536,'deadline_seconds':30,'terminate_grace_seconds':1},
    worker_policy={'deadline_seconds':120,'cpu_seconds':90,'address_space_bytes':512*1024*1024,'file_size_bytes':32*1024*1024,'open_files':32,'memory_limit_mode':'advisory_no_hard_memory_claim'},
    environment_policy={'schema':'pr108-reviewed-process-environment/v3','ambient_inheritance':False,
        'python':{'argv_prefix':g.PYTHON_PREFIX,'environment':g.COMMON_ENV},
        'initial_launcher':{'program':'launch_review_bundle.sh','shell':'/bin/sh','environment':g.COMMON_ENV},
        'git':{'environment':g.GIT_ENV,'repository_directory':str(C),'repository_location_pins':[],'repository_config_pins':[{'path':None,'bytes':None,'sha256':None}]},
        'gh':{'environment':{**g.GH_ENV_FIXED,'GH_CONFIG_DIR':None},'config_pins':[{'path':None,'bytes':None,'sha256':None}],'expected_login':None},
        'credentials_in_environment_or_receipts':False},
    capacity_policy={'headroom_bytes':32*1024*1024,'max_artifact_count':512,'max_materialized_bytes':160*1024*1024,
        'wrapper_bytes_cap':65536,'receipt_json_bytes_cap':128*1024,'per_native_growth_bytes':512*1024,'max_package_files':64,
        'future_commit_overhead_bytes':8*1024*1024,'runtime_overhead_bytes':8*1024*1024})
execution={'schema':'pr108-immutable-execution-inputs/v3','template_only':True,'effective':effective,'program_files':programs,'input_files':[]}
write('EXECUTION_INPUTS_TEMPLATE_DO_NOT_RUN.json',execution)
write('CONFIG_TEMPLATE_DO_NOT_RUN.json',{'schema':'pr108-native-publication-integration-config/v3','template_only':True,
    'commissioned_after_independent_review':False,'execution_inputs':pin(D/'EXECUTION_INPUTS_TEMPLATE_DO_NOT_RUN.json'),
    'gates':{role:{'path':None,'bytes':None,'sha256':None} for role in g.GATE_ROLES}})
fields={'mathematics':['mathematical_clearance'],'priority':['priority_clearance','bounded_substantive_resolution_note_clearance','attribution_checked','no_concrete_antecedent_in_recorded_search'],
    'package':['package_clearance','metadata_and_attribution_checked'],'whole_package_R1':['independent_whole_package_review','zero_blocking_findings'],
    'whole_package_R2':['independent_whole_package_review','zero_blocking_findings'],'pre_execution_adversary':['native_scope_and_invariants_checked'],
    'final':['mathematical_clearance','priority_clearance','package_clearance','whole_package_R1_clearance','whole_package_R2_clearance','native_integration_clearance',
        'pre_execution_adversary_clearance','actual_Zenodo_service_authenticated','actual_Google_Sheet_service_authenticated']}
gates={}
for role in g.GATE_ROLES:
    gates[role]={'schema':'pr108-publication-root-gate/v3','role':role,'PR':108,'problem_id':30003996,'UTC':None,
        'main_parent':None,'original_head':h.HEAD,'review_hash':h.REVIEW,'statement_hash':h.STATEMENT,'effective_proof_sha256':h.PROOF,
        'package_manifest_sha256':None,'execution_inputs_sha256':None,'actual_root_review':False,'clearance':False,
        'new_central_proof_search_turns':0,'original_budget':'2/5','exact_claim':None,'checked_artifacts':[],
        'fixture':True,'simulated':False,'dry_run':False,**{x:False for x in fields[role]}}
    if role in ['whole_package_R1','whole_package_R2']:gates[role]['reviewer_run_id']=None
    if role in ['pre_execution_adversary','final']:
        gates[role].update(reviewed_program_sha256={x:None for x in g.PROGRAMS},scoped_rank_interpretation='preserve_baseline_labels_and_positions_not_global_rerank')
    if role=='final':gates[role].update(gate_sha256={x:None for x in g.GATE_ROLES if x!='final'},publication_receipt_sha256=None,google_sheet_receipt_sha256=None)
write('ROOT_GATE_TEMPLATES_DO_NOT_USE_AS_EVIDENCE.json',{'draft_created_UTC':now,'template_only':True,'gates':gates})
write('GOOGLE_SHEET_RECEIPT_TEMPLATE_DO_NOT_USE_AS_EVIDENCE.json',{'schema':'pr108-actual-gws-sheet-service-receipt/v3',
    'actual_receipt':False,'fixture':True,'spreadsheet_id':g.SHEET,'sheet_id':g.GID,'sheet_title':g.TITLE,'columns':g.COLUMNS,
    'problem_id':30003996,'problem_code':g.CODE,'DOI':None,'row_index':None,'range':None,'independent_service_authentication_required':True,
    'processes':{role:{'actual_process_record':False,'fixture':True,'PID':None,'exit_code':None,'argv':[],
        'UTC_start':None,'UTC_end':None,'params_bytes':None,'params_sha256':None,'stdout_pin':None,'stderr_pin':None,'response_body_pin':None,
        **({'request_body_pin':None} if role=='write' else {})} for role in ['metadata','headers','write','readback','independent_readback']}})
write('PUBLICATION_RECEIPT_TEMPLATE_DO_NOT_USE_AS_EVIDENCE.json',{'schema':'pr108-actual-publication-receipt/v2','actual_receipt':False,'fixture':True,
    'PR':108,'problem_id':30003996,'published':False,'DOI':None,'original_head':h.HEAD,'effective_proof_sha256':h.PROOF,'package_manifest_sha256':None,
    'PID':None,'exit_code':None,'HTTP_method':'GET','status_code':None,'URL':None,'UTC_start':None,'UTC_end':None,'metadata_response':None,'payload_readbacks':[]})
write('AFFECTED_PATH_RULES.json',{'schema':'pr108-v3-exact-affected-path-rules/v1','template_only':True,'global_candidates':[h.P+x for x in h.EXPORT],
    'global_selection':'Offer only a byte-different verified private output relative to the exact pinned main-parent blob. Never recursively export a native root.',
    'attempt_prefix':h.N,'attempt_paths':'Exact materialization inventory only: preserved original fifteen, effective diagnostics, two source/prior copies, import/assessment/evidence wrappers, gates, logical package, immutable manifest, every reviewed nongate input archived by its exact A-relative name.',
    'no_native_status_or_turns_json':'No submitted status.json or turns.jsonl exists; do not create a purported original copy.',
    'excluded_global_paths':['queue.py','manifest.json','policy.json','review_v2/*','cache/*','last_update.json','update_history.jsonl'],
    'unrelated_catalog':'Exact baseline values, ranks and positions retained, including explained stale projections; target only replaced.',
    'unrelated_ranking_csv':'Every unrelated physical record byte span, header, ID order and count must match.',
    'unrelated_campaign':'Every unrelated physical line byte string and all untouched target cells must match.',
    'state_assessment':'All non-target dictionary entries equal baseline; two history prefixes exact bytes and each append exactly one target event.',
    'export_install_merge_commit_service_writes_by_helper':False})
corrections=[
{'finding':'F01','before':'Local Git tracker readback was sufficient; no required Google Sheet service custody.',
 'corrected_fields':['google_sheet.receipt','google_sheet.row_index','google_sheet.values','final.google_sheet_receipt_sha256','final.actual_Google_Sheet_service_authenticated'],
 'mechanism':'Mandatory actual GWS metadata/header/append/readback/independent-readback after actual Zenodo; exact spreadsheet/gid/tab/columns, target note, source URL, DOI, row/range, argv/params/body pins/PIDs/UTC/exit; final gate after independent service readback. Local tracker auxiliary only.',
 'code':['v3_guards.py:process_receipt','v3_guards.py:validate_sheet','prepare_review_bundle.py:prepare'],
 'tests':['SheetFixtures.test_synthetic_shape_and_wrong_row_doi_time_or_fixture','SheetFixtures.test_local_tracker_or_missing_service_readback_rejects']},
{'finding':'F02','before':'Helper SHA was bound, but editable effective configuration was not.',
 'corrected_fields':['execution_inputs','effective.*','program_files','input_files','gates.*.execution_inputs_sha256','reviewed_program_sha256'],
 'mechanism':'Canonical immutable all-choice execution-input manifest, exact field sets and runtime/source/receipt/program pins; all declared nongate input bytes consumed once with no unused entries. Gate pins excluded to avoid cycles. Every gate binds manifest, main parent, source/proof/package; final and adversary bind five-file code family; final binds antecedent gate bytes and service receipts. Worker independently checks manifest/code/final gate.',
 'code':['v3_guards.py:validate_execution_manifest','v3_guards.py:ReviewedInputs','prepare_review_bundle.py:validate_gate','native_assess_worker.py:execute'],
 'tests':['BindingFixtures.test_all_effective_fields_and_canonical_bytes_required','BindingFixtures.test_gate_exact_input_and_entire_program_binding','BindingFixtures.test_pinned_capture_once_and_no_unused_inputs']},
{'finding':'F03','before':'str.splitlines treated non-CR/LF controls as physical CSV line endings.',
 'corrected_fields':['CSV physical span selection','CSV replacement quoting and ending','unrelated record byte checks'],
 'mechanism':'Only physical CR/LF/CRLF partition input; csv.reader line_num maps to these spans. Reparse output, preserve header/count/ID order and every unrelated record exact bytes. Standard CRLF quoting then exact original target ending preserves EOF and internal quoted CR/LF.',
 'code':['v3_guards.py:physical_lines','v3_guards.py:csv_records','v3_guards.py:csv_overlay'],
 'tests':['CSVFixtures (eight Unicode/control separators, CR-only/LF/CRLF, original/new quoted multiline, target EOF without newline, duplicate/malformed input)']},
{'finding':'F04','before':'Capacity estimate omitted artifacts/overhead; child output and native assess were unbounded.',
 'corrected_fields':['capacity_policy.*','process_policy.*','worker_policy.*','CAPACITY_PLAN entries','WORKER_RESULT/PROCESS_JOURNAL/PREPARE_FAILURE receipts'],
 'mechanism':'Enumerate every exact/generated/process artifact plus exclusive native atomic slot; <=512 files including slot, <=64 logical packet files, per-file/aggregate caps, 32 MiB headroom and separate >=8 MiB runtime and future-commit reserves. Bounded retained/read subprocess streams, deadlines, TERM/KILL/reaping custody. Source-pinned assess worker requires CPU/file/open-file limit setup/readbacks; Darwin memory policy is explicitly advisory with no hard memory claim and parent tree/deadline watch. Failure receipts retained and no export.',
 'code':['v3_guards.py:capacity_inventory','bounded_process.py:BoundedRunner','native_assess_worker.py:execute','prepare_review_bundle.py:watch'],
 'tests':['ResourceFixtures.test_capacity_full_entries_counts_and_reserve','ResourceFixtures.test_bounded_tiny_subprocess_actual_custody_fixture','ResourceFixtures.test_worker_policy_only_no_native_invocation','ResourceFixtures.test_actual_harmless_worker_resource_setup_and_file_cap','ResourceFixtures.test_published_archive_requires_exact_manifest_and_inventory']},
{'finding':'F05','before':'Original relative names could swap, selected QUEUE SHA was not recomputed, prior {} was re-read.',
 'corrected_fields':['original_authentication_pins.*','original file path/name/mode/tree map','QUEUE selected_row_sha256/target/status/2/5 parse','captured prior bytes'],
 'mechanism':'Reviewed exact auth paths and fifteen regular100644 names; entry.path must equal native prefix+relative_path; live original-head NUL tree/blob map and every body checked. Whole queue pin/Git blob and selected row SHA recomputed, unique row parsed target+literalclaimed_solved+2/5. Empty selected prior captured once/reused; sourcepair absence of submitted prior kept. SQL/raw source hashes cross-bind original auth and immutable revision.',
 'code':['v3_guards.py:validate_original_map','v3_guards.py:validate_original_queue','v3_guards.py:ReviewedInputs','prepare_review_bundle.py:prepare'],
 'tests':['OriginalFixtures.test_exact_names_maps_and_modes','OriginalFixtures.test_queue_sha_parse_status_and_count','BindingFixtures.test_pinned_capture_once_and_no_unused_inputs']},
{'finding':'F06','before':'Eligibility-only regeneration changes could be accepted without a native-policy explanation.',
 'corrected_fields':['unrelated eligible/local_status/turns_used explanation','native policy turn_limit and default status','baseline catalog copy'],
 'mechanism':'Derive exact default/local status and turns from native policy/assessment/state, holds unchanged and present/turn budget gates; regenerated eligibility must equal exact predicate or abort. Preserve original unrelated full rows/ranks/positions regardless of explained drift.',
 'code':['v3_guards.py:native_status_turns','v3_guards.py:expected_eligible','v3_guards.py:scoped_catalog'],
 'tests':['EligibilityFixtures.test_eligibility_only_false_drift_rejects','EligibilityFixtures.test_exact_held_and_budget_projection_preserved','EligibilityFixtures.test_score_or_hold_drift_rejects']},
{'finding':'F07','before':'Every Sheet cell was required nonempty, rejecting the actually authorized blank chat cell.',
 'corrected_fields':['google_sheet.values[1]','google_sheet.existing_chat_authorized','exact four strings'],
 'mechanism':'Original/DOI/notes remain authenticated nonempty strings. Blank chat is accepted with existing_chat_authorized=false; a nonempty existing chat requires explicit prior authorization plus valid HTTPS without credentials, whitespace/control or malformed host/port. Actual immutable V2 service envelope is accepted without changing its body. No chat share or invented URL.',
 'code':['v3_guards.py:valid_https','v3_guards.py:validate_sheet','prepare_review_bundle.py:prepare'],
 'tests':['SheetFixtures.test_blank_chat_accepts_without_share_and_bad_existing_links_reject']},
{'finding':'F08','before':'Python site startup and arbitrary inherited Python/Git/GH environment could affect execution before guards.',
 'corrected_fields':['effective.environment_policy','initial launch -E -S -B','worker launch -E -S -B','Git config/location pins','GH existing auth/config metadata pins','expected GH login','process effective environment receipt'],
 'mechanism':'Reviewed shell launcher clears environment before Python -E -S -B. Every child gets one exact nonsecret role environment, never os.environ inheritance. Darwin UID-derived CF encoding is explicit. Exact effective Git config/location files and existing GH file-backed config/auth are bounded privately hash-checked; no credential bodies or tokens in inventory/receipts. Disable system/global Git configs, prompts/hooks/fsmonitor/credential helper; reject executable config and GH external aliases/socket. Parent binds exact environment, all binary pins and five-file code family in immutable input manifest and fresh adversary/final gates. GH expected login is checked through pinned CLI with reviewed auth, no credential dump.',
 'code':['launch_review_bundle.sh','bounded_process.py:BoundedRunner','v3_guards.py:validate_environment_policy','v3_guards.py:verify_private_runtime_configuration','prepare_review_bundle.py:prepare','native_assess_worker.py:execute'],
 'tests':['StartupFixtures.test_clean_python_and_initial_launcher_ignore_injected_startup','StartupFixtures.test_missing_startup_flags_and_ambient_policy_reject_before_spawn','StartupFixtures.test_private_config_pins_exact_locations_and_no_credential_copy']}
]
write('FIELD_SPECIFIC_CORRECTION_LEDGER.json',{'schema':'pr108-native-helper-v3-correction-ledger/v1','UTC':now,'V1_modified':False,'V2_modified':False,
    'predecessor_pin_manifest':'PREDECESSOR_UNCHANGED_INPUT_PINS.json',
    'static_adversary_input':'A/native_helper_corrected_v2_adversary_20261006 (complete REPORT/VERDICT/code/results read; exact byte pins retained)',
    'all_F01_through_F08_addressed_in_draft':True,'independent_V3_adversary_clearance':False,
    'actual_native_prepare_assess_export_executions':0,'new_central_proof_search_turns':0,'program_pins':programs,'corrections':corrections})
print(json.dumps({'templates_and_ledger_written':True,'UTC':now,'actual_runtime_configuration_prepared':False,'actual_native_calls':0}))
