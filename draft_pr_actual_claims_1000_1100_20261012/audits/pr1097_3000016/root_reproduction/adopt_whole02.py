from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_02'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'FINAL_SEAL.json');check(R/'OUTPUT_PINS.json',seal['output_inventory']);outputs=load(R/'OUTPUT_PINS.json')['entries'];inputs=load(R/'INPUT_FREEZE.json')['files']
for row in outputs:check(R/row['path'],row)
for row in inputs:check(A/row['path'],row)
sources=load(R/'SOURCE_READ_LEDGER.json')['sources']
for row in sources:check(Path(row['body_path']),row['body']);check(Path(row['text_path']),row['text'])
controls=[]
for optimized in [False,True]:
    py=['python3','-B']+(['-O'] if optimized else []);argv=py+[str(R/'independent_math.py')]
    p=subprocess.run(argv,capture_output=True);need(p.returncode==0,p.stderr.decode(errors='replace'));need(json.loads(p.stdout)==load(R/'INDEPENDENT_NORMAL.json')==load(R/'INDEPENDENT_OPTIMIZED_RERUN.json'),'complete independent JSON differs')
    fault=subprocess.run(argv+['--inject-failure'],capture_output=True);need(fault.returncode!=0 and b'new unconditional failure control' in fault.stderr,'unconditional fault accepted')
    controls.append({'optimized':optimized,'exit_code':p.returncode,'full_JSON_equals_completed_review_runs':True,'stdout_sha256':sha(p.stdout),'unconditional_fault_rejection':fault.returncode})
v=load(R/'VERDICT.json');need(v['whole_proof_source_PDF_kit_review'] and v['findings']==[] and all(x==0 for x in v['finding_counts'].values()),'complete review verdict')
for row in inputs:check(A/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN','full_REPORT_frozen_independent_derivation_source_ledger_harness_events_and_new_control_source_read':True,'counts_rehashed':{'inputs':len(inputs),'outputs':len(outputs),'primary_source_bodies_and_texts':len(sources)},'root_fresh_independent_controls':controls,'root_confirmed_coverage':load(R/'INDEPENDENT_NORMAL.json')['coverage'],'initial_uncompleted_optimized_empty_output_not_used':'Completed INDEPENDENT_OPTIMIZED_RERUN.json is authoritative; initial zero-byte file and process attempt remain transparent history.','whole_reviews_completed':2,'minimum_whole_reviews':2,'actionable_P0_P1_P2_P3':0,'exact_gadget_method_priority_independent_discovery_worldwide_openness':'UNKNOWN','output_pins_sha256':seal['output_inventory']['sha256'],'terminal_administrative_reconciliation_and_root_final_integrity_required':True,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_02.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':'PASS_ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE','counts':record['counts_rehashed'],'math_modes':2,'ready':False}))
