from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_04'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',s['output_inventory']);outs=load(R/'OUTPUT_PINS.json')['entries'];ins=load(R/'PREEXISTING_AUDIT_FREEZE.json')['files']
for r in outs:check(R/r['path'],r)
for r in ins:check(A/r['path'],r)
sources=[r for src in load(R/'SOURCE_LEDGER.json')['sources'] for r in src['source_files']]
for r in sources:check(A/r['path'],r)
runs=[]
for optimized in [False,True]:
    args=['python3','-B']+(['-O'] if optimized else [])+[str(R/'independent_rigorous_controls.py')]
    p=subprocess.run(args,capture_output=True);need(p.returncode==0,p.stderr.decode());need(json.loads(p.stdout)==load(R/'INDEPENDENT_NORMAL.json')==load(R/'INDEPENDENT_OPTIMIZED.json'),'full JSON differs')
    faults=[]
    for f in ['endpoint','drop-entry-mass','drop-sequential']:
        q=subprocess.run(args+['--fault',f],capture_output=True);need(q.returncode!=0,'fault accepted');faults.append({'fault':f,'exit_code':q.returncode})
    runs.append({'optimized':optimized,'exit_code':p.returncode,'full_JSON_equals_review':True,'stdout_sha256':sha(p.stdout),'faults':faults})
for r in ins:check(A/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE04_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN','full_REPORT_frozen_derivation_source_ledger_and_independent_control_source_read':True,'counts_rehashed':{'inputs':len(ins),'outputs':len(outs),'source_body_text_files':len(sources)},'root_rigorous_replays':runs,'rigorous_finite_scope':'241 rational interval scalar pairs; exact formal prime-log identities;1000 exact row-stochastic matrices. Universal proof is analytic.','historical_exceptions':'14813 exact /5 explicitly unsupported old pointers; two stale inventory copies plus3 invalid negative fixtures. No fabricated bytes or all-historical-pointer authentication. Current distribution claims appropriately limited.','whole_reviews_completed':4,'minimum_whole_reviews':2,'actionable_P0_P1_P2_P3':0,'priority_novelty_worldwide_openness':'UNKNOWN; credited prior corollary','output_pins_sha256':s['output_inventory']['sha256'],'terminal_administration_and_NEW_external_final_integrity_required':True,'old_FINAL_seals_unchanged_dated_history':True,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_04.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':'PASS_ADOPT_WHOLE04_ZERO','counts':record['counts_rehashed'],'actual_control_commands':8,'ready':False}))
