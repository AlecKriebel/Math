from pathlib import Path
import json,os,datetime,hashlib,stat
R=Path(__file__).parent;A=R.parents[1];D=A/'preprint';P=A.parents[1];W=A/'publication/workflow'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,d):
 b=(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode() if not isinstance(d,str) else d.encode()
 with (R/n).open('wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert (R/n).read_bytes()==b
n={'__name__':'review07_final_pure_schema','__file__':str(P/'accept_pr948.py')};raw=(P/'accept_pr948.py').read_bytes();assert sha(raw)=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823';exec(compile(raw,str(P/'accept_pr948.py'),'exec',dont_inherit=True,optimize=0),n)
freeze=json.loads((D/'FREEZE.json').read_bytes());start=json.loads((R/'AUTHENTICATION_START.json').read_bytes());end=json.loads((R/'AUTHENTICATION_END.json').read_bytes());cold=json.loads((R/'COLD_REPLAY.json').read_bytes());began=json.loads((R/'SESSION_START.json').read_bytes())['started_utc'];dis=json.loads((R/'DISPOSITIONS_CHECKED.json').read_bytes());details=json.loads((R/'AUTHENTICATION_END_DETAILS.json').read_bytes());pin={'freeze':'1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c','manifest':'a25e28435f84374bf6e6705c9e5bc91952236d9f5fc5dc48e05ad29d62956b23','pdf':'14063ce9fef470a6a3875dc429a1c3d34372d60cbd73eb7e22e77b46b1639f60'}
workflow=json.loads((W/'MANIFEST.json').read_bytes());want=set(workflow['files'])|{'MANIFEST.json','MANIFEST.sha256'};actual={p.relative_to(W).as_posix() for p in W.rglob('*') if p.is_file()};assert actual==want and len(actual)==359 and not list(W.glob('private-fixture-*'))
for path,v in workflow['files'].items():assert n['fingerprint']((W/path).read_bytes())==v
source_stable=details['seven_operations']==json.loads((R/'AUTHENTICATION_START_DETAILS.json').read_bytes())['seven_operations'];assert source_stable
scope={'utc':utc(),'literal_initial_folder_confinement_met':False,'initial_stricter_NONCLEAN_interpretation_preserved':True,'parent_clarification_received':'Unique automatically removed inert scratch is distinct from missing authentication, substantive contamination or external action; preserve first source/receipt and judge actual END plus corrected evidence. No forced clean verdict.','actual_outside_scope_scratch':['One uniquely named inert TemporaryDirectory under W in firstworkflow97; exact generated basename unknown, auto removed.','Initial four cold profile.replay calls used uniquely generated normal OS temporary empty checker cwd; exact names unknown, context removed it.'],'corrected_actual_reruns':'Current workflow97 fixture under07 and current four cold TMPDIR/TMP/TEMP under07; all five suites and four exact canonical receipts actually rerun, not retrofitted.','independent_final_assessment':'No substantive mathematical/priority intake preceded completed START/own saved attack. All protected candidate/external/operations/original/prior bytes match again. W actual359files exactly357sealedpayloads+twoenvelopes, with no fixture leftovers or production-state files. No authoritative mutation, contamination, lost review evidence, missing full check or unmet frozen-contract requirement remains. The literal scratch-location deviation is real and retained, but does not itself falsify substantive independence or the entire mathematical/package verdict under the clarified protection purpose.','clean_context_under_disclosed_substantive_standard':True,'blindness_claim':False,'candidate_or_production_code_changed':False,'all_three_failed_END_attempts_preserved':True,'END_guard_refinement':'The initial additional whole-dictionary review bracket failed three times. First exact difference is unknown because not saved then; attempts02/03 actual diffs only computed mergeableUNKNOWN->MERGEABLE,mergeStateStatusUNKNOWN->CLEAN. Current extra review bracket records both statuses, requires closingMERGEABLE, and requires equality of every other observed field incl currentlivebase/associatedbase/body/files. This is a reviewer-harness correction, not any production premerge rule change or cold receipt normalization.'}
save('SCOPE_REASSESSMENT.json',scope)
result={'pr':948,'problem_id':'30004549','original_pr_head':n['HEAD'],'reviewer_agent_id':'/root/pr948_full_package_07','clean_context':True,'full_reproducer_completed':True,'entire_package_review':True,'started_utc':began,'completed_utc':utc(),'candidate_revision':2,'candidate_pins':pin,'inspected_helper_hashes':freeze['future_helpers'],'required_issues':[],'optional_issues':[],'clean_for_preprint':True,'strongest_verified_theorem':'On the closed connected product of the smooth genus-two completion of y^2=z^6-1 and C/(Z+iZ), a jointly smooth two-sided small real family J_e equals the product J0 outside a fixed coordinate ball, converges to J0 in C-infinity, retains three fixed independent real de Rham classes with closed J_e-anti-invariant representatives, and is nonintegrable for every sufficiently small nonzero real e. Thus h_J_e^- >=3. No exact dimension, fixed symplectic compatibility, analyticity or historical-priority certificate is asserted.','mathematical_remaining_gap_for_stated_theorem':None,'prior_issue_resolution':dis['separate_prior_whole_review_issue'],'inherited_finding_dispositions':{k:{'verified':v['verified'],'evidence':v['evidence']} for k,v in dis['dispositions'].items()},'procedural_deviations':{'record':'FIXTURE_SCOPE_DEVIATION.json','reassessment':'SCOPE_REASSESSMENT.json','literal_initial_folder_confinement':False,'authoritative_mutation_or_missing_scientific_check_found':False},'source_priority_limits':'11 selected primary bodies, bounded current searches; no novelty, firstness, current-openness or exhaustive-absence certificate. Fullsurvey/Geiges/finalbody/citation/olderCZrealHminus gaps persist.','new_author_proof_responses':0,'production_acceptance_performed':False}
originals=n['original_check']();assert n['result_schema'](result) is True
ap,ta=n['review_authentication'](start,pin,freeze,originals);bp,tb=n['review_authentication'](end,pin,freeze,originals);cp,tc=n['review_cold'](cold,pin,freeze,D);assert ap and bp and cp and n['utc'](began)<=ta<=tc<=tb<=n['utc'](result['completed_utc'])
assert set(result['inherited_finding_dispositions'])==n['INHERITED_FINDING_IDS'] and len(result['prior_issue_resolution'])==1
assert n['utc'](began)>n['utc']('2026-10-16T15:24:42.894075+00:00')
# Final close time is an actual later record, then all actual schema calls are repeated on saved/reread inputs.
result['completed_utc']=utc();save('RESULT.json',result)
assert n['result_schema'](json.loads((R/'RESULT.json').read_bytes())) is True
assert n['review_authentication'](json.loads((R/'AUTHENTICATION_START.json').read_bytes()),pin,freeze,originals)[0]
assert n['review_authentication'](json.loads((R/'AUTHENTICATION_END.json').read_bytes()),pin,freeze,originals)[0]
assert n['review_cold'](json.loads((R/'COLD_REPLAY.json').read_bytes()),pin,freeze,D)[0]
save('SCHEMA_VALIDATION.json',{'utc':utc(),'status':'PASS','actual_production_functions':['result_schema','review_authentication START','review_authentication END','review_cold'],'absolute_review_base':str(D),'chronology':{'started_utc':began,'START':start['utc'],'COLD':cold['utc'],'END':end['utc'],'completed_utc':result['completed_utc'],'ordered':True},'inherited_count':50,'required':39,'optional':11,'separate_prior_issue':'R948-FULL01-R01','workflow_closed359exact':True,'production_action_functions_called':[]})
with (R/'FULL_AUDIT.md').open('a') as f:
 f.write('\nActual closing END PASS at '+end['utc']+' repeated all7/308/440/6/357/353/24 and all6priorseals/payloads, with fresh OPEN/draft/exacthead/main metadata and distinct associated/live bases. All authoritative pins remain unchanged; exact W359closure has no fixture or production-state leftovers. The refined additional metadata bracket retains computed status observations and requires all other fields equal; failed attempts remain failures. The scratch-scope reassessment above finds no unmet frozen-contract check or substantive contamination. RESULT clean_for_preprint=true, no candidate required/optional issue, theorem gapnull. Actual completed_utc '+result['completed_utc']+'; exact production result/auth(START,END)/cold schemas PASS with absoluteD and START<=cold<=END<=completed. This is a completed clean ENTIRE review under the disclosed substantive standard; production acceptance remains separate.\n');f.flush();os.fsync(f.fileno())
log=(R/'RESEARCH_LOG.md').read_text()+'\n- '+utc()+' — 100% complete for assigned entire-package review. Final END passed and exact schemas/chronology validated; all50+R01 independently verified. No candidate issues or stated-theorem gap. Initial scratch-scope deviation, strict initial interpretation, parent clarification, own setup failures and three failed END attempts preserved. Final clean assessment follows actual protected-file integrity and corrected evidence; no publication action.\n';save('RESEARCH_LOG.md',log)
TOP='''ACTUAL_PR_METADATA_BRACKET_DIFFERENCE_END.json
AUTHENTICATION_ATTEMPT_01_FAILURE.json
AUTHENTICATION_ATTEMPT_02_FAILURE.json
AUTHENTICATION_END_ATTEMPT_01_FAILURE.json
AUTHENTICATION_END_ATTEMPT_02_FAILURE.json
AUTHENTICATION_END_ATTEMPT_03_FAILURE.json
AUTHENTICATION_START.json
AUTHENTICATION_START_DETAILS.json
AUTHENTICATION_END.json
AUTHENTICATION_END_DETAILS.json
FINAL_PR_BRACKET_END.json
COLD_MODE_O.json
COLD_MODE_OO.json
COLD_MODE_env2.json
COLD_MODE_normal.json
COLD_REPLAY.json
DIFF_test_base_context.py.json
DIFF_test_live_base_context.py.json
DIFF_test_review_history.py.json
DIFF_test_root_fixes.py.json
DIFF_test_workflow.py.json
DISPOSITIONS_CHECKED.json
EXECUTION_test_base_context.py.json
EXECUTION_test_live_base_context.py.json
EXECUTION_test_review_history.py.json
EXECUTION_test_root_fixes.py.json
EXECUTION_test_workflow.py.json
FAMILY_AUTHENTICATION.json
FIXTURE_SCOPE_DEVIATION.json
FRESH_WEB_CHECKS.json
FULL_AUDIT.md
GENERAL_MATRIX_ATTEMPT_01_FAILURE.json
GENERAL_MATRIX_RESULT.json
HISTORY_VALIDATION_ATTEMPT_01_FAILURE.json
HISTORY_VALIDATION_ATTEMPT_02_FAILURE.json
INDEPENDENT_MATH_RESULT.json
INDEPENDENT_PROBES.json
INERT_BASE_CONTEXT.json
INERT_LIVE_BASE_CONTEXT.json
INERT_REVIEW_HISTORY.json
INERT_ROOT_FIXES.json
INERT_SUITE_EXECUTIONS.json
INERT_WORKFLOW_01.json
INERT_WORKFLOW_02.json
INITIAL_ATTACK.md
INITIAL_ATTACK_RECEIPT.json
PACKAGE_AND_WORKFLOW_BOUNDARIES.json
PDF_VISUAL_QA.json
POST_END_ATTEMPT_IDENTITY.json
PRIMARY_INVENTORY.json
PRIMARY_SUPPORT.json
PRIOR_HISTORY_VALIDATION.json
PROFILE_EXECUTION.json
RESEARCH_LOG.md
RUNTIME.json
SESSION_START.json
ZIP_METADATA.json
RESULT.json
SCHEMA_VALIDATION.json
SCOPE_REASSESSMENT.json
PUBLIC_ALLOWLIST.json
adapted_test_base_context.py
adapted_test_live_base_context.py
adapted_test_review_history.py
adapted_test_root_fixes.py
adapted_test_workflow.py
authenticate.py
authenticate_attempt01.py
authenticate_attempt02.py
authenticate_before_final_bracket.py
authenticate_end_attempt01.py
authenticate_end_attempts02_03.py
correct_fixture_scope.py
general_matrix.py
general_matrix_attempt01.py
independent_math.py
independent_probes.py
read_primary.py
reproduce.py
run_inert.py
save_initial.py
support_evidence.py
validate_histories.py
validate_histories_attempt01.py
validate_histories_attempt02.py
write_assessment.py
close_and_seal.py'''.splitlines()
HISTORY=['history/initial_fixture_scope/'+x for x in '''COLD_MODE_OO.json
INERT_REVIEW_HISTORY.json
reproduce.py
INERT_SUITE_EXECUTIONS.json
INERT_ROOT_FIXES.json
run_inert.py
COLD_MODE_normal.json
INERT_WORKFLOW_01.json
COLD_MODE_O.json
COLD_REPLAY.json
INERT_BASE_CONTEXT.json
DIFF_test_workflow.py.json
COLD_MODE_env2.json
adapted_test_workflow.py
INERT_LIVE_BASE_CONTEXT.json'''.splitlines()]
PROFILE=['profile/'+x for x in ['DEVELOPMENT_RESULTS.json','BASELINE_OUTER_OPTIMIZED.json','BASELINE_ISOLATED_NO_SITE.json','BASELINE_POISONED_ENVIRONMENT.json','DEVELOPMENT_EVENTS.ndjson']]
allowed=sorted(TOP+HISTORY+PROFILE);assert len(allowed)==len(set(allowed)) and 'MANIFEST.json' not in allowed
exclusions=['private_primary/ retained third-party extracts (no raw bodies or HTML/PDF included)','private_cold/ and private_cold_rerun/ reproduced package copies','profile/private_fixtures/ and cold_child_tmp/ owned temporary fixtures','pdf_qa/ rendered previews (recipe, all image hashes and personal-view judgments are public)','No runtime/dependency/cache/credentials/raw private source record or recursive private evidence selection']
save('PUBLIC_ALLOWLIST.json',{'utc':utc(),'public_files':allowed,'excluded':exclusions,'selection':'Explicit static per-path public allowlist, no recursive directory selection.'})
private=(A/'source_record_private.txt').read_bytes();records={}
for name in allowed:
 path=R/name;info=path.lstat();assert stat.S_ISREG(info.st_mode) and info.st_nlink==1
 b=path.read_bytes();assert b and private not in b
 with path.open('rb') as f:os.fsync(f.fileno())
 assert path.read_bytes()==b
 records[name]={'bytes':len(b),'sha256':sha(b)}
manifest={'schema':'pr948-full-package-review-seal-v1','sealed_utc':utc(),'reviewer_agent_id':'/root/pr948_full_package_07','pr':948,'problem_id':'30004549','candidate_revision':2,'candidate_freeze_sha256':pin['freeze'],'status':'SEALED_COMPLETE_CLEAN_WITH_DISCLOSED_REVIEWER_HARNESS_HISTORY','files':records,'explicit_public_allowlist':allowed,'exclusions':exclusions,'limitations':'AI adversarial review, not human peer review, formal proof, exhaustive priority, hostile-OS sandbox or production acceptance. Initial scratch-location and reviewer harness failures preserved; authoritative bytes independently reauthenticated.'}
save('MANIFEST.json',manifest)
for name,pinrow in json.loads((R/'MANIFEST.json').read_bytes())['files'].items():assert n['fingerprint']((R/name).read_bytes())==pinrow
external=sha((R/'MANIFEST.json').read_bytes());print(json.dumps({'status':'SEALED','manifest_sha256':external,'payload_count':len(records),'clean_for_preprint':True,'required_issues':0,'optional_issues':0,'theorem_gap':None,'started_utc':began,'completed_utc':result['completed_utc'],'END':end['utc'],'production_acceptance':False}))
