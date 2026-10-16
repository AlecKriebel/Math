from pathlib import Path
import json,hashlib,subprocess,datetime
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_02'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',s['output_inventory'])
require(sha((R/'FROZEN_INPUTS.json').read_bytes())==s['frozen_inputs_sha256'],'frozen seal')
counts={}
for filename,base in [('FROZEN_INPUTS.json',A),('OUTPUT_PINS.json',R)]:
    rows=load(R/filename)['files']
    for row in rows:check(base/row['path'],row)
    counts[filename]=len(rows)
check(R/'INDEPENDENT_DERIVATION_BEFORE_LABELS.md',load(R/'DERIVATION_FREEZE.json'))
results=[]
for optimized in [False,True]:
    argv=['python3','-B']+(['-O'] if optimized else [])+[str(R/'independent_checks.py')]
    p=subprocess.run(argv,capture_output=True)
    require(p.returncode==0,p.stderr.decode(errors='replace'));data=json.loads(p.stdout)
    require(data==load(R/'INDEPENDENT_RESULTS.json')==load(R/'INDEPENDENT_RESULTS_OPTIMIZED.json'),'full reviewed result differs')
    record={'optimized':optimized,'complete_JSON_equals_review':True,'stdout_sha256':sha(p.stdout),'faults':[]}
    for fault in ['conjugation','erasing','parity']:
        q=subprocess.run(argv+[fault],capture_output=True);require(q.returncode!=0,'fault accepted')
        record['faults'].append({'fault':fault,'exit_code':q.returncode,'stderr_sha256':sha(q.stderr)})
    results.append(record)
v=load(R/'VERDICT.json');require(v['findings']==[] and v['findings_by_priority']=={'P0':0,'P1':0,'P2':0,'P3':0},'findings present')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN','complete_REPORT_SOURCE_INTERFACE_and_frozen_derivation_read':True,'root_prior_full_paper_currentcode_native_metadata_and_7actualpages':'ROOT_PREPRINT_REVIEW_01.json','rehash_counts':counts,'root_actual_independent_new_controls':results,'output_pins_sha256':s['output_inventory']['sha256'],'whole_reviews_completed':2,'minimum_whole_reviews':2,'actionable_P0_P1_P2_P3':0,'exact_scope':'Fixedgenus ordered essential positive factors of one boundarytwist, repeatedletters andpairwise geometricintersection<=1; finiteconjugacy/finiteattainedM; separate arbitrarylengthclausenegative, fullhighermaximumclassificationbundlePARTIAL.','priority':'UNKNOWN_WITH_REQUIRED_PRIOR_COROLLARY_AND_METHOD_CREDITS','publication_ready':False,'published':False,'services_held_after_pr':1032,'reviewer_compile_and_page_evidence':'Original actual built-in and clean Tectonic success, all seven renderedpages exact; resumed current and compiledPDF rerenders exact and actuallyviewed. No newcompile on resumption; paper unchanged.'}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_02.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':counts,'fault_rejections':6,'whole_reviews_completed':2}))
