from pathlib import Path
import datetime,hashlib,json,subprocess,tempfile
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_03';P=A/'NEWpreprint_v1_0'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r.get('bytes',r.get('size')) and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',s['output_pins']);outs=load(R/'OUTPUT_PINS.json')['records'];ins=load(R/'FROZEN_INPUTS.json')['rows']
for r in outs:check(R/r['path'],r)
for r in ins:check(A/r['path'],r)
source_count=0
for src in load(R/'SOURCE_READ_LEDGER.json')['sources']:
    if 'path' in src:check(Path(src['path']),src);source_count+=1
    for r in src.get('retained_inputs',[]):check(Path(r['path']),r);source_count+=1
runs=[]
with tempfile.TemporaryDirectory(prefix='root1071-whole03-',dir='/private/tmp') as td:
    td=Path(td)
    for optimized in [False,True]:
        mode='optimized' if optimized else 'normal';dest=td/(mode+'.json');args=['python3','-B']+(['-O'] if optimized else [])+[str(R/'independent_math_checks.py'),str(dest)]
        p=subprocess.run(args,capture_output=True);need(p.returncode==0,p.stderr.decode());need(load(dest)==load(R/'INDEPENDENT_CHECKS_NORMAL.json')==load(R/'INDEPENDENT_CHECKS_OPTIMIZED.json'),'full new math JSON differs')
        target=td/('python311-'+mode);args=['/opt/homebrew/bin/python3.11','-B']+(['-O'] if optimized else [])+[str(P/'scripts/check.py'),'--out',str(target)]
        q=subprocess.run(args,capture_output=True);need(q.returncode!=0 and b'Original checker mathematics differs from frozen original result' in q.stderr,'portability finding did not reproduce')
        actual=load(target/'normal/FINITE_CHECKS.json');review=load(R/'PYTHON311_RESULT_NORMAL.json');need({k:v for k,v in actual.items() if k!='utc'}=={k:v for k,v in review.items() if k!='utc'},'3.11 full computed result differs from reviewed failure')
        runs.append({'optimized':optimized,'new_math_exit':p.returncode,'new_math_full_JSON_equals_review':True,'actual_python311_wrapper_exit':q.returncode,'actual_python311_stderr':q.stderr.decode(),'computed_non_utc_JSON_equals_reviewed311':True})
for r in ins:check(A/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE03_ONE_P3_PENDING_BOUNDED_PORTABILITY_REPAIR_AND_NEW_COMPLETE_WHOLE04','full_REPORT_early_and_completed_derivation_source_ledger_current_wrapper_and_new_control_source_read':True,'counts_rehashed':{'inputs':len(ins),'outputs':len(outs),'primary_source_objects':source_count},'root_independent_math_and_actual_portability_reproductions':runs,'findings':{'P0':0,'P1':0,'P2':0,'P3':1},'finding':'WHOLE03-P3-01 Python3.9+ promise includes3.11.8 whose covariance floating results differ at rounding level, rejected by exact full-result comparison. Exact analytic/rational claims unchanged.','required_repair':'Accurately specify/test supported runtimes or a justified explicit cross-version float contract retaining every field/exact rational guard/fault detection; no silent float omission or interval-certification claim. Preserve paper/PDF/native/history. NEW COMPLETE whole04 required.','whole_reviews_completed':3,'minimum_whole_reviews':2,'publication_ready':False,'published':False,'services_held_after_pr':1032,'output_pins_sha256':s['output_pins']['sha256']}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_03.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':'PASS_ADOPT_WHOLE03_ONE_P3','counts':record['counts_rehashed'],'actual_commands':4,'ready':False}))
