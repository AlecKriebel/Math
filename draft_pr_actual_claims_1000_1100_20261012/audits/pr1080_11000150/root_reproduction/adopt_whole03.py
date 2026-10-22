from pathlib import Path
import datetime,hashlib,json,subprocess,zipfile
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_03';P=A/'preprint_v1_0';K=P/'verification_kit'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',s['inventory']);outputs=load(R/'OUTPUT_PINS.json')['files'];inputs=load(R/'INPUT_FREEZE.json')['files']
for row in outputs:check(R/row['path'],row)
for row in inputs:check(A/row['path'],row)
sources=load(R/'SOURCE_READ_LEDGER.json')['sources']
for row in sources:check(Path(row['path']),row)
for row in load(R/'EXTERNAL_INPUT_PINS.json')['files']:check(Path(row['path']),row)
controls=[]
for optimized in (False,True):
    argv=['python3','-B']+(['-O'] if optimized else [])+[str(R/'independent_checks03.py')]
    p=subprocess.run(argv,capture_output=True);need(p.returncode==0,p.stderr.decode(errors='replace'));need(json.loads(p.stdout)==load(R/'INDEPENDENT_RESULTS.json')==load(R/'INDEPENDENT_RESULTS_O.json'),'full independent mathematical JSON')
    faults=[]
    for name,error in [('omit_conjugates','Independent insertion identity'),('wrong_parity','Independent mod-2 alternation')]:
        q=subprocess.run(argv+[name],capture_output=True);need(q.returncode!=0 and error.encode() in q.stderr,'meaningful fault escaped '+name);faults.append({'fault':name,'exit_code':q.returncode})
    controls.append({'optimized':optimized,'full_JSON_equals_both_completed_reviews':True,'stdout_sha256':sha(p.stdout),'faults':faults})
paths=['metadata_date02_history/prior_repair01/before/preprint_v1_0/verification_kit.zip','repair01_history/before/preprint_v1_0/verification_kit.zip']
with zipfile.ZipFile(P/'verification_kit.zip') as z:
    payload=[z.read('verification_kit/'+n) for n in paths]
need(payload[0]==payload[1] and len(payload[0])==607553 and sha(payload[0])=='d1c03ef097938934641907c3552f05a0687347ea7945b399fff1a365322a1a1b','duplicate historical archives not reproduced')
need('duplicate archives are not distributed' in (P/'README.md').read_text() and 'duplicate archive is included' in (K/'README.md').read_text(),'current exclusion prose differs')
v=load(R/'VERDICT.json');need(v['complete_whole_package_review'] and not v['repair_only'] and v['findings_by_priority']=={'P0':0,'P1':0,'P2':0,'P3':1},'whole03 verdict')
for row in inputs:check(A/row['path'],row)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE03_ONE_ACTIONABLE_P3_BOUNDED_DOCUMENTATION_REPAIR_THEN_NEW_WHOLE04_REQUIRED','full_REPORT_frozen_derivation_source_ledger_and_new_control_source_read':True,'counts_rehashed':{'prior_inputs':len(inputs),'review_outputs':len(outputs),'primary_source_bodies':len(sources),'external_readonly_inputs':3},'root_fresh_independent_controls':controls,'root_reproduced_P3':{'duplicate_member_paths':paths,'duplicate_bytes':len(payload[0]),'duplicate_sha256':sha(payload[0]),'both_current_README_exclusion_statements_verified':True,'historical_archive_retention_is_legitimate':True,'repair':'Qualify current distribution wording globally, preserving exact historical archives. No mathematical defect found.'},'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_actionable_counts':v['findings_by_priority'],'NEW_complete_whole04_required_after_repair':True,'output_pins_sha256':s['inventory']['sha256'],'scope':'Fixed genus restricted arbitrary-length clause negative; complete maximum/classification bundle PARTIAL. No effective upper formula or higher-genus exact maxima established.','full_result_application_priority_novelty_worldwide_openness':'UNKNOWN','earlier_unexplained_fault_cause':'UNESTABLISHED; later completed full fault suites passed, without retroactively explaining it.','publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_03.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'counts':record['counts_rehashed'],'root_commands':6,'ready':False}))
