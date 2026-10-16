from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_03'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',{'bytes':s['output_pins_bytes'],'sha256':s['output_pins_sha256']})
outputs=load(R/'OUTPUT_PINS.json')['files'];inputs=load(R/'INPUT_FREEZE.json')['files']
for row in outputs:check(R/row['path'],row)
for row in inputs:check(A/row['path'],row)
sources=load(R/'SOURCE_READ_LEDGER.json')['sources']
for row in sources:check(A/row['path'],row)
receipts=load(R/'NEW_MATH_RECEIPTS.json')['commands'];expected=json.loads(next(x['stdout'] for x in receipts if x['code']==0));controls=[]
for optimized in (False,True):
    argv=['python3','-B']+(['-O'] if optimized else [])+[str(R/'check_independent.py')]
    p=subprocess.run(argv,capture_output=True);need(p.returncode==0,p.stderr.decode(errors='replace'));need(json.loads(p.stdout)==expected,'full independent math JSON')
    faults=[]
    for name,error in [('endpoint','complex polynomial Fourier square'),('surface','surface Jacobian retained'),('old_theta','published source range')]:
        q=subprocess.run(argv+['--mutation',name],capture_output=True);need(q.returncode!=0 and error.encode() in q.stderr,'meaningful mutation escaped '+name);faults.append({'mutation':name,'exit_code':q.returncode,'expected_error':error})
    controls.append({'optimized':optimized,'full_JSON_equals_review':True,'stdout_sha256':sha(p.stdout),'faults':faults})
v=load(R/'VERDICT.json');need(v['actionable_findings']==[] and all(n==0 for n in v['severity_counts'].values()) and v['scope'].startswith('NEW INDEPENDENT COMPLETE WHOLE-PACKAGE'),'whole03 verdict')
for row in inputs:check(A/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE03_ZERO_ACTIONABLE_PENDING_NEW_TERMINAL_ADMIN','full_REPORT_frozen_independent_derivation_source_ledger_and_new_independent_code_read':True,'counts_rehashed':{'prior_inputs':len(inputs),'review_outputs':len(outputs),'primary_source_interfaces':len(sources)},'root_fresh_new_mathematical_controls':controls,'finite_controls':expected,'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_whole_review':3,'actionable_P0_P1_P2_P3':0,'output_pins_sha256':s['output_pins_sha256'],'mathematical_scope':'Every connected smooth nontrivial compact halfspace perturbation binds in ambient2,3 at every beta>0; every compact W1,infinity graph in ambient>=4 has weak-beta absence; explicit R4 graph at beta1. Quantifiers, nongraph restriction, all-form domain proof and no embedded-eigenvalue exclusion are unchanged.','priority_novelty_independent_discovery_worldwide_openness':'UNKNOWN','source_scope':'Fresh selected primary interfaces, not complete reproof or byte identification of preprint with publisher. Published HHRV A6 theta1/4, distinct older version, and credited Exner-Minakov planar mechanism remain essential.','terminal_administrative_reconciliation_and_root_final_integrity_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_03.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'counts':record['counts_rehashed'],'root_commands':8,'ready':False}))
