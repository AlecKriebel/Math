from pathlib import Path
import json,hashlib,datetime,os,stat
P=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');A=P/'audits/pr948_30004549';D=A/'preprint';R=A/'reviews/full_package_06';core=P/'accept_pr948.py';raw=core.read_bytes();assert hashlib.sha256(raw).hexdigest()=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823';N={'__name__':'_final_schema_06_','__file__':str(core)};exec(compile(raw,str(core),'exec',dont_inherit=True,optimize=0),N)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,z):
 b=(json.dumps(z,indent=2,ensure_ascii=True)+'\n').encode();p=R/n;f=p.open('wb');f.write(b);f.flush();os.fsync(f.fileno());f.close();assert p.read_bytes()==b
F=json.loads((D/'FREEZE.json').read_bytes());S=json.loads((R/'AUTHENTICATION_START.json').read_bytes());E=json.loads((R/'AUTHENTICATION_END.json').read_bytes());C=json.loads((R/'COLD_REPLAY.json').read_bytes());dis=json.loads((R/'DISPOSITIONS_CHECKED.json').read_bytes());pins={'freeze':'1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c','manifest':'a25e28435f84374bf6e6705c9e5bc91952236d9f5fc5dc48e05ad29d62956b23','pdf':'14063ce9fef470a6a3875dc429a1c3d34372d60cbd73eb7e22e77b46b1639f60'}
assert len(S['live_operations'])==len(E['live_operations'])==7 and S['live_operations']==E['live_operations'];assert S['candidate_files']==E['candidate_files']==F['files']
start='2026-10-16T15:07:40+00:00';complete=now();result={'pr':948,'problem_id':'30004549','original_pr_head':'be4313efafa1af5962394e07d8a4debff2e94d92','reviewer_agent_id':'/root/pr948_full_package_06','clean_context':True,'full_reproducer_completed':True,'entire_package_review':True,'started_utc':start,'completed_utc':complete,'candidate_revision':2,'candidate_pins':pins,'inspected_helper_hashes':F['future_helpers'],'required_issues':[],'optional_issues':[],'clean_for_preprint':True,'strongest_verified_theorem':'On the closed connected smooth real four-manifold given by the smooth compact genus-two completion of y^2=z^6-1 times C/(Z+iZ), there is a jointly smooth small real family J_e equal to product J0 outside a fixed coordinate ball and converging to J0 in C-infinity, preserving three fixed independent real de Rham classes with closed J_e-anti-invariant representatives, and nonintegrable for every sufficiently small nonzero parameter of either sign. Thus h_J_e^- >=3.','mathematical_remaining_gap_for_stated_theorem':None,'prior_issue_resolution':dis['separate_prior_issue_resolution'],'inherited_finding_dispositions':{k:{'verified':v['verified'],'evidence':v['evidence']} for k,v in dis['inherited_finding_dispositions'].items()},'independence_metadata':{'actual_all7_live_preintake_authentication':True,'prior05_administrative_header_exposed':True,'prior_substantive_mathematical_or_priority_assessment_before_ownattack':False,'claim_of_blindness':False,'scope_reassessment_record':'SCOPE_REASSESSMENT.json','initial_NONCLEAN_scope_interpretation_preserved':'history/initial_NONCLEAN_interpretation_FULL_AUDIT.md','interpretation':'Parent clarified mechanical incomplete-history metadata is not a prior mathematical verdict. Independent review of exact exposure and actual7START/ownattack order satisfies substantive independence; no missing scientific check backfilled.'},'limitations':['Only the stated lower bound; no exact hminus, fixed symplectic compatibility or spatial analyticity.','Bounded primary-source audit with selected11bodies; no firstness, novelty, current-open or exhaustive-absence certificate. Unavailable final-version, full2012survey/Geiges and olderCZrealHminus gaps remain.','CPython3.14.6/SymPy1.14.0 only; trusted installed dependencies/host; no hostile-OS sandbox or formal proof/human peer review.','Cached local-main source/native check is not a fresh remote-main production action gate. Historical native count/total remain UNKNOWN; immutable4/5 is PR-declared;0new author proof responses.','Review05 incomplete history resets clean streak. This06 can be only first new clean current review; another distinct consecutive complete clean ENTIRE current review remains required before acceptance.'],'production_actions_run':False}
originals=N['original_check']();assert N['result_schema'](result) is True;a,t0=N['review_authentication'](S,pins,F,originals);b,t1=N['review_authentication'](E,pins,F,originals);c,tc=N['review_cold'](C,pins,F,D);assert a and b and c and N['utc'](start)<=t0<=tc<=t1<=N['utc'](complete);assert set(result['inherited_finding_dispositions'])==N['INHERITED_FINDING_IDS'] and len(result['inherited_finding_dispositions'])==50
for name,count in [('WORKFLOW.json',97),('HISTORY.json',58),('ROOT_FIXES.json',18),('BASE_CONTEXT.json',26),('LIVE_BASE.json',37)]:
 z=json.loads((R/name).read_bytes());assert z['status']=='PASS' and z['passed']==count and z['failed']==0
profile=json.loads((R/'profile/DEVELOPMENT_RESULTS.json').read_bytes());assert profile['event_count']==85 and len(profile['events'])==85 and not any('skip' in str(q.get('outcome','')).lower() for q in profile['events']);assert any(q['test']=='ambient_import_poison_positive_control' and q['outcome']=='controlled_poison_executed_without_isolation' for q in profile['events'])
assert json.loads((R/'INDEPENDENT_MATH.json').read_bytes())['checks']==18 and json.loads((R/'INDEPENDENT_WORKFLOW_PROBES.json').read_bytes())['passed']==37;assert json.loads((R/'PDF_VISUAL_QA.json').read_bytes())['five_pages_personally_viewed']
save('RESULT.json',result);save('SCHEMA_VALIDATION.json',{'utc':now(),'status':'PASS','actual_functions':['accept_pr948.result_schema','accept_pr948.review_authentication START','accept_pr948.review_authentication END','accept_pr948.review_cold'],'result_schema_complete':True,'authentication_START_PASS':a,'authentication_END_PASS':b,'cold_PASS':c,'absolute_review_base':str(D),'chronology_start_cold_end_completed_valid':True,'all50_individual_dispositions':True,'separate_R948_FULL01_R01_verified':True,'profile_events':85,'profile_skips':0,'suites':[97,58,18,26,37],'own_math_checks':18,'own_new_workflow_probes':37,'metadata_exposure_and_scope_reassessment_disclosed':True,'real_production_actions':0,'acceptance_claimed':False})
with (R/'FULL_AUDIT.md').open('a') as f:
 f.write('\nFinal END actually repeated all7 live sources/308frozen/440external/6helper/357workflow/353preservation/24original/all5priorseals and fresh eligiblePR metadata at '+E['utc']+'. Final production result_schema/review_authentication(START,END)/review_cold all PASS with absolute candidate path and chronological START<=cold<=END<=completed. Actual RESULT closing record time '+complete+'. All50 individual dispositions and separateR948-FULL01-R01 verified; no candidate required/optional issue. This is one new clean entire review after05, not a two-review acceptance.\n');f.flush();os.fsync(f.fileno())
with (R/'RESEARCH_LOG.md').open('a') as f:
 f.write(now()+' — 100% of this entire-review goal complete. Final actualEND PASS; strictproductionresult/auth/cold schemas and chronology PASS; no required/optional candidate issue or theorem gap. Clean-context eligibility independently reassessed under clarified substantive-independence standard with exact earliermetadataexposure/initialNONCLEANdrafts preserved. First new clean after05; no acceptance/action authorized. Sealing explicitpublicallowlist next.\n');f.flush();os.fsync(f.fileno())
# Explicit curated publication selection, not a recursive directory selection.
public='''ACTUAL_AUTH_CHECKS.json
AUTHENTICATION_START.json
AUTHENTICATION_END.json
AUTHENTICATION_END_PRE_FINALIZATION.json
BASE_CONTEXT.json
COLD_MODE_normal.json
COLD_MODE_O.json
COLD_MODE_OO.json
COLD_MODE_env2.json
COLD_REPLAY.json
DISPOSITIONS_CHECKED.json
FRESH_WEB_CHECKS.json
FULL_AUDIT.md
HISTORY.json
INDEPENDENT_MATH.json
INDEPENDENT_MATH_ATTEMPT_01_FAILURE.json
INDEPENDENT_WORKFLOW_PROBES.json
INITIAL_ATTACK_SAVE_RECEIPT.json
INITIAL_INDEPENDENT_ATTACK.md
LIVE_BASE.json
PACKAGE_BOUNDARIES.json
PDF_RENDER_RECEIPT.json
PDF_VISUAL_QA.json
PRESTART_DISPLAY_EXPOSURE.json
PRIMARY_READING_INVENTORY.json
PRIMARY_SUPPORT.json
PRIOR_HISTORY_VALIDATION.json
RESEARCH_LOG.md
RESULT.json
ROOT_FIXES.json
SCHEMA_VALIDATION.json
SCOPE_REASSESSMENT.json
SUBMITTED_STATUS.json
SUITE_ATTEMPT_01_FAILURE.json
SUITE_RUN_test_base_context.py.json
SUITE_RUN_test_live_base_context.py.json
SUITE_RUN_test_review_history.py.json
SUITE_RUN_test_root_fixes.py.json
SUITE_RUN_test_workflow.py.json
SUITE_RUN_test_workflow.py_ATTEMPT_01.json
WORKFLOW.json
WORKFLOW_HISTORY_AUTHENTICATION.json
ZIP_METADATA_BEFORE_DECOMPRESSION.json
actual_auth_checks.py
adapted_test_base_context.py
adapted_test_live_base_context.py
adapted_test_review_history.py
adapted_test_root_fixes.py
adapted_test_workflow.py
authenticate.py
cold_replay.py
finish_evidence.py
independent_math.py
independent_math_attempt_01.py
independent_workflow_probes.py
reassess_scope.py
run_suites.py
run_suites_attempt_01.py
validate_prior_histories.py
validate_and_seal.py
history/initial_NONCLEAN_interpretation_DISPOSITIONS_CHECKED.json
history/initial_NONCLEAN_interpretation_FULL_AUDIT.md
history/initial_NONCLEAN_interpretation_PRESTART_DISPLAY_EXPOSURE.json
history/initial_NONCLEAN_interpretation_RESEARCH_LOG.md
pdf_pages/page-1.png
pdf_pages/page-2.png
pdf_pages/page-3.png
pdf_pages/page-4.png
pdf_pages/page-5.png
profile/BASELINE_ISOLATED_NO_SITE.json
profile/BASELINE_OUTER_OPTIMIZED.json
profile/BASELINE_POISONED_ENVIRONMENT.json
profile/DEVELOPMENT_EVENTS.ndjson
profile/DEVELOPMENT_RESULTS.json'''.splitlines()
assert len(public)==len(set(public)) and 'MANIFEST.json' not in public
files={}
for n in public:
 assert not any(x in Path(n).parts for x in ['private','private_fixtures','cold_extract','tmp','__pycache__','venv','.secrets']);p=R/n;st=p.lstat();assert stat.S_ISREG(st.st_mode) and not p.is_symlink();b=p.read_bytes();assert b;f=p.open('rb');os.fsync(f.fileno());f.close();files[n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
# Synchronize remaining own private/derived evidence without publishing it.
for p in R.rglob('*'):
 if p.is_file():
  with p.open('rb') as f:os.fsync(f.fileno())
manifest={'schema':'pr948-full-package-review-seal-v1','sealed_utc':now(),'reviewer_agent_id':result['reviewer_agent_id'],'pr':948,'problem_id':'30004549','candidate_revision':2,'candidate_freeze_sha256':pins['freeze'],'status':'COMPLETE_CLEAN_ENTIRE_REVIEW_WITH_DISCLOSED_METADATA_SCOPE_REASSESSMENT','explicit_public_allowlist':public,'files':files,'exclusions':['private/ third-party selected source text; local only0700/0600','cold_extract/ exact publicpackage replay derivation; local only','tmp/ and profile/private_fixtures/ fixtures; no fixtures published','external runtimes/caches/credentials/rawcorpus; not selected'],'limitations':'One independent AI entire review; no humanreferee/formalproof/firstness or publicationacceptance. Earlier metadata exposure and initialstrictinterpretation preserved explicitly.'}
save('MANIFEST.json',manifest)
for n,pin in files.items():
 b=(R/n).read_bytes();assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']
fd=os.open(R,os.O_RDONLY);os.fsync(fd);os.close(fd)
print(json.dumps({'status':'SEALED','clean_for_preprint':True,'manifest_sha256':hashlib.sha256((R/'MANIFEST.json').read_bytes()).hexdigest(),'payload_count':len(files),'completed_utc':complete,'seal_utc':manifest['sealed_utc'],'mathematical_gap':None,'required_issues':0,'optional_issues':0,'acceptance':False}))
