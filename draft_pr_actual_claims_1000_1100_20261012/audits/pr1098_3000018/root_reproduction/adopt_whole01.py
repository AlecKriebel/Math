from pathlib import Path
import datetime, hashlib, json, subprocess
A=Path(__file__).resolve().parents[1]; R=A/'reviews/package_01'
def load(p): return json.loads(p.read_text())
def need(v,m):
    if not v: raise RuntimeError(m)
def digest(b): return hashlib.sha256(b).hexdigest()
def check(p,r):
    b=p.read_bytes(); need(len(b)==r['bytes'] and digest(b)==r['sha256'],str(p))
seal=load(R/'OUTPUT_SEAL.json'); check(R/'OUTPUT_PINS.json',seal['output_pins'])
outputs=load(R/'OUTPUT_PINS.json')['entries']; inputs=load(R/'PRIOR_AUDIT_FREEZE.json')['files']
for row in outputs: check(R/row['path'],row)
for row in inputs: check(A/row['path'],row)
sources=load(R/'SOURCE_READ_LEDGER.json')['primary_sources']; source_paths=0
for row in sources:
    for p in row.get('retained_matches',[]):
        need(digest((A/p).read_bytes())==row['sha256'],p); source_paths+=1
    for p in row.get('retained_text_matches',[]):
        need(digest((A/p).read_bytes())==row['text_sha256'],p); source_paths+=1
controls=[]
for optimized in (False,True):
    argv=['python3','-B']+(['-O'] if optimized else [])+[str(R/'independent_checks.py')]
    p=subprocess.run(argv,capture_output=True); need(p.returncode==0,p.stderr.decode(errors='replace'))
    need(json.loads(p.stdout)==load(R/'INDEPENDENT_NORMAL.json')==load(R/'INDEPENDENT_OPTIMIZED.json'),'full independent JSON')
    fault=subprocess.run(argv+['--invalid'],capture_output=True)
    need(fault.returncode!=0 and b'unconditional review guard' in fault.stderr,'unconditional fault accepted')
    controls.append({'optimized':optimized,'exit_code':p.returncode,'stdout_sha256':digest(p.stdout),'full_JSON_equals_completed_review_runs':True,'unconditional_fault_exit':fault.returncode})
v=load(R/'VERDICT.json'); need(v['terminal_handoff'] and v['findings']==[] and all(x==0 for x in v['finding_counts'].values()),'whole review verdict')
for row in inputs: check(A/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE01_ZERO_ACTIONABLE_SECOND_NEW_COMPLETE_WHOLE_REVIEW_REQUIRED','ROOT_full_REPORT_frozen_derivation_source_ledger_and_new_independent_code_read':True,'counts_rehashed':{'prior_inputs':len(inputs),'review_outputs':len(outputs),'source_identity_entries':len(sources),'source_body_text_path_pins':source_paths,'fresh_reviewer_body_interfaces':sum(bool(s.get('fresh_primary_body_read')) for s in sources)},'root_fresh_independent_controls':controls,'finite_controls':load(R/'INDEPENDENT_NORMAL.json'),'review_writer_scope':v['writer_scope'],'scope_qualification':'Reviewer positive writer runs use unchanged code with runtime ORIGINAL redirected to owned fixtures; prior ROOT preparation record separately pins actual unmodified external commands. These are distinct tests. Retained source identity is not a claim of fresh full-body reading for every entry. ROOT reviewed the complete mathematical proof independently in the adopted mathematics/preprint records.','output_pins_sha256':seal['output_pins']['sha256'],'whole_reviews_completed':1,'minimum_new_complete_whole_reviews':2,'new_independent_complete_whole02_REQUIRED_even_though_first_clean':True,'priority_full_result_physical_realization_methods_worldwide_openness':'UNKNOWN','publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':record['status'],'counts':record['counts_rehashed'],'root_commands':4,'ready':False}))
