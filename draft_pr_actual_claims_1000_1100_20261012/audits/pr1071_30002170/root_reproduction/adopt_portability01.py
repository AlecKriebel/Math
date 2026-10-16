from pathlib import Path
import datetime,hashlib,importlib.util,io,json,subprocess,tempfile,zipfile
A=Path(__file__).resolve().parents[1];R=A/'repairs/portability01';P=A/'NEWpreprint_v1_0'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
seal=load(R/'SEAL.json');check(R/'OUTPUT_PINS.json',seal['output_pins']);outputs=load(R/'OUTPUT_PINS.json')['records']
for r in outputs:check(R/r['path'],r)
baseline=load(R/'BASELINE_INPUT_PINS.json')['rows'];befores={r['original_path']:r for r in load(R/'BEFORE_PINS.json')['rows']}
for r in baseline:check(A/befores[r['path']]['before_snapshot'] if r['path'] in befores else A/r['path'],r)
current=load(R/'CURRENT_CANDIDATE_PINS.json')['records']
for r in current:check(P/r['path'],r)
for r in load(R/'CURRENT_AUDIT_PINS.json')['records']:check(A/r['path'],r)
copies=load(P/'INPUT_COPY_MAP.json')['copies'];old=load(R/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies'];need(copies[:128]==old and len(copies)==140,'copy prefix')
for r in copies:check(A/r.get('source_snapshot',r['original_path']),r);check(P/r['package_copy'],r)
hist=load(R/'HISTORICAL_STAGE_RESOLUTION.json')['records'];newhist=load(R/'PRIOR_LATEST_INPUT_OUTPUT_PIN_RESOLUTION.json')['records']
for r in hist:check(A/r['portability_resolution_path'],r)
for r in newhist:
    p=Path(r['resolved_path']);check(p if p.is_absolute() else A/p,r)
need(len(baseline)==763 and len(befores)==9 and len(hist)==4346 and len(newhist)==3158,'repair counts')
archive=P/'PR1071_preprint_v1_0_support.zip';manifest=load(P/'PACKAGE_MANIFEST.json');names=sorted([r['path'] for r in manifest['members']]+['PACKAGE_MANIFEST.json']);b=io.BytesIO()
with zipfile.ZipFile(b,'w') as z:
    for n in names:
        i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,(P/n).read_bytes(),compress_type=zipfile.ZIP_STORED)
need(b.getvalue()==archive.read_bytes() and len(names)==182,'independent CLOSED ZIP')
guard_code=r'''
import sys,importlib.util,json,copy,math
sys.dont_write_bytecode=True
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p/'scripts'));s=importlib.util.spec_from_file_location('fresh_guard',p/'scripts/check.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
expected=json.loads((p/'checks/original_expected.json').read_text());coverage=m.result_guard(expected,expected);leaves=[]
def walk(v,path=()):
 if isinstance(v,dict):
  for k,w in v.items():
   if path or k!='utc':walk(w,path+(k,))
 elif isinstance(v,list):
  for k,w in enumerate(v):walk(w,path+(k,))
 else:leaves.append((path,v))
walk(expected);rejections=0
def parent(d,path):
 for k in path[:-1]:d=d[k]
 return d,path[-1]
def reject(d):
 global rejections
 try:m.result_guard(d,expected)
 except RuntimeError:rejections+=1;return
 raise RuntimeError('root injected fault escaped')
for path,v in leaves:
 d=copy.deepcopy(expected);q,k=parent(d,path);del q[k];reject(d)
 if type(v) is float:
  for bad in (float('nan'),float('inf'),float('-inf')):
   d=copy.deepcopy(expected);q,k=parent(d,path);q[k]=bad;reject(d)
  if m.float_policy(path)[2]=='exact_float':
   d=copy.deepcopy(expected);q,k=parent(d,path);q[k]=math.nextafter(v,math.inf);reject(d)
for key in ('exact_area_pairing','L1_f','L1_gthird'):
 d=copy.deepcopy(expected);d[key]='0';reject(d)
if sum(coverage.values())!=len(leaves) or len(leaves)!=258:raise RuntimeError('incomplete root leaf coverage')
print(json.dumps({'status':'PASS','coverage':coverage,'leaves':len(leaves),'actual_rejections':rejections,'new_candidate_code_imported_only_for_finite_guard_falsifications':True},sort_keys=True))
'''
commands=[];clean=[]
def run(argv,cwd):
    q=subprocess.run([str(x) for x in argv],cwd=cwd,capture_output=True);commands.append({'argv':[str(x) for x in argv],'cwd':str(cwd),'exit_code':q.returncode,'stdout':q.stdout.decode(errors='replace'),'stderr':q.stderr.decode(errors='replace')});need(q.returncode==0,q.stderr.decode(errors='replace'));return q
with tempfile.TemporaryDirectory(prefix='root1071-portability-',dir=A/'root_reproduction') as tmp:
    T=Path(tmp)
    for version,tag in [('3.11','py311'),('3.14','py314')]:
        for opt in (False,True):
            py=['/opt/homebrew/bin/python'+version,'-B']+(['-O'] if opt else []);mode='optimized' if opt else 'normal';out=T/(tag+'-'+mode)
            q=run(py+[P/'scripts/check.py','--out',out],T);receipt=json.loads(q.stdout)
            need(receipt['same_runtime_normal_optimized_non_utc_exact_equal'],'same-runtime results')
            for submode in ('normal','optimized'):
                actual=load(out/submode/'FINITE_CHECKS.json');reference=load(R/('RESULT_'+tag+'_'+mode+'_'+submode+'.json'))
                need({k:v for k,v in actual.items() if k!='utc'}=={k:v for k,v in reference.items() if k!='utc'},'complete runtime mathematical JSON')
            q=run(py+['-c',guard_code,str(P)],T);faults=json.loads(q.stdout);need(faults['leaves']==258 and faults['actual_rejections']==724,'root fault coverage')
            run(py+[P/'scripts/verify_package.py','--require-bindings'],T)
        run(['/opt/homebrew/bin/python'+version,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',A/'publication/zenodo-deposit.json'],T)
    for p in T.rglob('*'):
        if p.is_file():clean.append({'path':p.relative_to(T).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
for r in current:check(P/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_BOUNDED_PORTABILITY_REPAIR_REQUIRES_NEW_COMPLETE_WHOLE04','ROOT_full_REPORT_current_comparison_code_verifier_diff_readme_supplement_policy_status_source_evidence_and_complete_custody_verifier_source_read':True,'counts':{'outputs':len(outputs),'baseline':len(baseline),'changes':len(befores),'protected':len(baseline)-len(befores),'current_candidate':len(current),'copies':len(copies),'history_rows':len(hist),'newer_pin_rows':len(newhist),'archive_members':len(names)},'actual_root_commands':commands,'root_finite_guard_rejections_per_runtime_mode':724,'complete_runtime_math_JSON_equals_final_repair_outputs_excluding_only_utc':True,'own_derivatives_hashed_before_cleanup':clean,'independent_CLOSED_ZIP_byte_exact':True,'tolerance_qualification':'Complete exact schema/identities/sample H values; named finite derived-float acceptance policies, not proved numerical error bounds or interval certificates. Runtime claim narrowed to installed3.11.8/3.14.6 binary64. Other runtimes unvalidated.','original_checker_baseline_analytic_proof_PDF_metadata_path_guards_unchanged':True,'whole_reviews_completed':3,'minimum_whole_reviews':2,'NEW_complete_whole04_REQUIRED':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'output_pins_sha256':seal['output_pins']['sha256']}
(A/'ROOT_PORTABILITY_REPAIR_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'counts':record['counts'],'commands':len(commands),'ready':False}))
