from pathlib import Path
import json,hashlib,subprocess,datetime
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_02'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json')
require(s['terminal'] is True,'not terminal')
require(sha((R/'INPUT_PINS.json').read_bytes())==s['input_pins_sha256'],'input seal')
require(sha((R/'OUTPUT_PINS.json').read_bytes())==s['output_pins_sha256'],'output seal')
counts={}
for filename,base in [('INPUT_PINS.json',A),('OUTPUT_PINS.json',R)]:
    rows=load(R/filename)['files']
    for row in rows:check(base/row['path'],row)
    counts[filename]=len(rows)
results=[]
for optimized in [False,True]:
    prefix=['python3','-B']+(['-O'] if optimized else [])
    argv=prefix+[str(R/'check_independent_forms.py')]
    p=subprocess.run(argv,capture_output=True)
    require(p.returncode==0,p.stderr.decode(errors='replace'))
    data=json.loads(p.stdout)
    # NEW_MATH_RESULT contains direct ordinary/optimized result objects.
    expected=load(R/'NEW_MATH_RESULT.json')
    require(data==expected,'new full JSON differs from reviewed result')
    results.append({'optimized':optimized,'result':data,'stdout_sha256':sha(p.stdout),'faults':[]})
    for fault in ['Fourier_trace_sign','mass_exponent','normal_sign','area_lost','old_theta','Hardy_m2','flat_sign']:
        q=subprocess.run(argv+['--fault',fault],capture_output=True)
        require(q.returncode!=0,'fault accepted: '+fault)
        results[-1]['faults'].append({'fault':fault,'exit_code':q.returncode,'stderr_sha256':sha(q.stderr)})
require(results[0]['result']==results[1]['result'],'full normal/O result differs')
verdict=load(R/'VERDICT.json')
require(verdict['severity_counts']=={'P0':0,'P1':0,'P2':0,'P3':0} and verdict['actionable_findings']==[],'findings present')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN','complete_REPORT_SOURCE_INTERFACE_and_frozen_derivation_read':True,'root_prior_full_paper_all6currentcode_native_metadata_and_7actualpages':'ROOT_PREPRINT_REVIEW_01.json','rehash_counts':counts,'root_actual_new_exact_control_replays':results,'normal_optimized_complete_JSON_equal':True,'output_pins_sha256':s['output_pins_sha256'],'whole_reviews_completed':2,'minimum_whole_reviews':2,'actionable_P0_P1_P2_P3':0,'priority':'UNKNOWN_WITH_REQUIRED_PRIOR_COROLLARY_AND_MECHANISM_CREDIT','publication_ready':False,'published':False,'services_held_after_pr':1032,'reviewer_real_compile_and_pages':'Both actual clean Tectonic builds reproduce canonical PDF and all seven freshly rendered pages actually viewed in complete whole02; unchanged since prior root actual page inspection.'}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_02.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS','rehash_counts':counts,'new_diagnostics':sum(results[0]['result']['counts'].values()),'fault_rejections':14,'whole_reviews_completed':2}))
