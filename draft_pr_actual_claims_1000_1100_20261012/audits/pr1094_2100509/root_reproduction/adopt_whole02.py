from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_02'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',seal['output_pins'])
outputs=load(R/'OUTPUT_PINS.json')['records'];inputs=load(R/'FROZEN_INPUT_PINS.json')['files']
for row in outputs:check(R/row['path'],row)
for row in inputs:check(A/row['path'],row)
check(R/'INDEPENDENT_DERIVATION.md',load(R/'DERIVATION_FREEZE.json'))
sources=load(R/'SOURCE_READ_LEDGER.json')['source_reads']
for row in sources:check(Path(row['local_path']),row)
deps=load(R/'SUPPLEMENTAL_DEPENDENCY_PINS.json')['records']
for row in deps:check(Path(row['resolved_path']),row)
history=load(R/'FAMILY_HISTORY_PATHS.json')['rows']
for row in history:check(A/row['resolution'],row)
controls=[]
for optimized in [False,True]:
    argv=['python3','-B']+(['-O'] if optimized else [])+[str(R/'independent_controls02.py')]
    p=subprocess.run(argv,capture_output=True);need(p.returncode==0,p.stderr.decode(errors='replace'));need(json.loads(p.stdout)==load(R/'INDEPENDENT_NORMAL.json')==load(R/'INDEPENDENT_OPTIMIZED.json'),'complete new independent JSON')
    controls.append({'optimized':optimized,'exit_code':p.returncode,'full_JSON_equals_review':True,'stdout_sha256':sha(p.stdout)})
verdict=load(R/'VERDICT.json');need(verdict['complete_whole_review'] and not verdict['repair_only_review'] and verdict['actionable_findings']==[] and all(verdict[k]==0 for k in ['P0','P1','P2','P3']),'whole verdict')
for row in inputs:check(A/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN','full_report_independent_derivation_source_ledger_and_new_control_source_read':True,'full_math_scope':'Alln smooth compact-supported numerical real-Jordan realization in commuting local frame iff real spectrum; all previous qualifications unchanged.','counts_rehashed':{'inputs':len(inputs),'outputs':len(outputs),'primary_source_bodies':len(sources),'external_dependencies':len(deps),'additional_family_history_paths':len(history)},'root_new_independent_replays':controls,'whole_reviews_completed':2,'minimum_whole_reviews':2,'actionable_P0_P1_P2_P3':0,'full_result_and_method_priority_novelty_worldwide_openness':'UNKNOWN','output_pins_sha256':seal['output_pins']['sha256'],'terminal_administrative_reconciliation_and_root_final_integrity_required':True,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_02.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE','counts':record['counts_rehashed'],'independent_math_modes':2,'ready':False}))
