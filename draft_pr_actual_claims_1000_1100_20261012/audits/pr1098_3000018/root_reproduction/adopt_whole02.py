from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_02'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'OUTPUT_SEAL.json');check(R/'OUTPUT_PINS.json',s['output_pins']);outputs=load(R/'OUTPUT_PINS.json')['entries'];inputs=load(R/'FREEZE.json')['regular_files']
for r in outputs:check(R/r['path'],r)
for r in inputs:check(A/r['path'],r)
ledger=load(R/'SOURCE_READ_LEDGER.json');sources=ledger['retained_identities'];source_paths=0
for r in sources:
    for p in r['retained_matching_paths']:check(A/p,r);source_paths+=1
for r in ledger['other_selective_context_scopes']:need(sha(Path(r['actual_text_path']).read_bytes())==r['text_sha256'],'selective text identity')
commands=[]
for opt in (False,True):
    py=['python3','-B']+(['-O'] if opt else [])
    for name,expected,error in [('new_controls.py','NEW_CONTROLS_normal.json','whole02 unconditional exception control'),('custody_check.py','CUSTODY_normal.json','custody control exception survives optimization')]:
        argv=py+[str(R/name)];p=subprocess.run(argv,capture_output=True);need(p.returncode==0,p.stderr.decode(errors='replace'));need(json.loads(p.stdout)==load(R/expected),'full independent JSON '+name)
        q=subprocess.run(argv+['--invalid'],capture_output=True);need(q.returncode!=0 and error.encode() in q.stderr,'fault accepted '+name)
        commands.append({'optimized':opt,'script':name,'full_JSON_equals_review_normal':True,'stdout_sha256':sha(p.stdout),'exit_code':p.returncode,'unconditional_fault_exit':q.returncode,'unconditional_fault_expected_error':error})
v=load(R/'VERDICT.json');need(v['terminal_handoff'] and v['findings']==[] and all(n==0 for n in v['finding_counts'].values()),'complete whole02 verdict')
for r in inputs:check(A/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN','ROOT_full_REPORT_frozen_derivation_source_ledger_new_independent_controls_custody_checker_and_period_deletion_addendum_read':True,'counts_rehashed':{'inputs':len(inputs),'review_outputs':len(outputs),'source_identities':len(sources),'source_body_path_pins':source_paths,'fresh_used_primary_reference_interfaces':len(ledger['fresh_used_paper_reference_scopes'])},'root_fresh_independent_math_custody_and_unconditional_fault_runs':commands,'new_finite_math_controls':load(R/'NEW_CONTROLS_normal.json'),'complete_custody_closed_ZIP_and_metadata':load(R/'CUSTODY_normal.json'),'review_actual_unmodified_external_commands':116,'review_runtime_ROOT_or_ORIGINAL_modified':False,'source_and_original_identity_scope':'All nine submitted bytes rehashed against two frozen actual-Git receipts under delegated noGit; ROOT earlier direct object checks remain distinct. All28 retained identities rehashed, ten used primary interfaces read by reviewer; no fresh full-body read implied for all remaining identities.','whole_reviews_completed':2,'minimum_whole_reviews':2,'actionable_P0_P1_P2_P3':0,'output_pins_sha256':s['output_pins']['sha256'],'terminal_administrative_reconciliation_and_root_final_integrity_required':True,'priority_full_result_simple_oriented_realization_methods_worldwide_openness':'UNKNOWN','publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_02.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'counts':record['counts_rehashed'],'actual_root_commands':8,'ready':False}))
