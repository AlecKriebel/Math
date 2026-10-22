from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile,os,datetime
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_01';P=A/'preprint_v1_0'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r.get('bytes',r.get('size')) and sha(b)==r['sha256'],str(p))
s=load(R/'FINAL_SEAL.json');check(R/'OUTPUT_PINS.json',s['output_pins'])
inputs=load(R/'INPUT_PINS.json')['files'];outputs=load(R/'OUTPUT_PINS.json')['entries']
for r in inputs:check(A/r['path'],r)
for r in outputs:check(R/r['path'],r)
controls=[]
for optimized in [False,True]:
    argv=['python3','-B']+(['-O'] if optimized else [])+[str(R/'independent_checks.py')]
    p=subprocess.run(argv,capture_output=True);require(p.returncode==0,p.stderr.decode(errors='replace'))
    data=json.loads(p.stdout);require(data==load(R/'INDEPENDENT_NORMAL.json')==load(R/'INDEPENDENT_OPTIMIZED.json'),'complete independent math JSON differs')
    q=subprocess.run(argv+['--inject-failure'],capture_output=True);require(q.returncode!=0,'unconditional invalid guard accepted')
    controls.append({'optimized':optimized,'full_JSON_equals_review':True,'stdout_sha256':sha(p.stdout),'unconditional_invalid_exit':q.returncode})
cases=[]
with tempfile.TemporaryDirectory(prefix='root1097-case-',dir='/private/tmp') as td:
    td=Path(td);clean=td/'clean'
    with zipfile.ZipFile(P/'pr1097_support_v1_0.zip') as z:z.extractall(clean)
    alias=td/'CLEAN';require(alias.exists() and os.path.samefile(clean,alias),'actual case-insensitive parent alias required')
    protected={str(p.relative_to(clean)):sha(p.read_bytes()) for p in clean.rglob('*') if p.is_file()}
    for optimized in [False,True]:
        dest=alias/('insert-'+str(optimized)+'.zip')
        argv=['python3','-B']+(['-O'] if optimized else [])+[str(clean/'scripts/build_support.py'),'--out',str(dest)]
        p=subprocess.run(argv,capture_output=True);actual=clean/dest.name
        require(p.returncode==0 and actual.exists(),'case alias finding did not reproduce')
        require(actual.read_bytes()==(P/'pr1097_support_v1_0.zip').read_bytes(),'unexpected generated archive')
        cases.append({'optimized':optimized,'argument':str(dest),'samefile_parent':True,'exit_code':p.returncode,'fresh_archive_created_inside_kit':True,'existing_input_overwrite':False})
        actual.unlink()
    require(protected=={str(p.relative_to(clean)):sha(p.read_bytes()) for p in clean.rglob('*') if p.is_file()},'disposable extraction inputs changed')
for r in inputs:check(A/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_COMPLETE_WHOLE01_ONE_P3_PENDING_BOUNDED_PHYSICAL_PATH_REPAIR_AND_NEW_WHOLE02','full_REPORT_SOURCE_INTERFACE_REVIEW_and_frozen_derivation_read':True,'input_files_rehashed':len(inputs),'output_files_rehashed':len(outputs),'root_actual_independent_math_replays':controls,'root_actual_case_alias_reproductions':cases,'whole_reviews_completed':1,'minimum_whole_reviews':2,'findings':{'P0':0,'P1':0,'P2':0,'P3':1},'accepted_math_and_priority_framing':'Complete exact coNP theorem credited FL/BL/HKT/Toth/KT; all fullresult/gadget/methodpriority UNKNOWN, no proof change needed.','required_bounded_repair':'Check physical identity of every existing outputancestor against existing kit/original protectedroots, preserve absentroot behavior and all fresh/regular/link/no.. protections; refresh every current dependent artifact and record exact before custody; NEW complete whole02 required.','publication_ready':False,'published':False,'services_held_after_pr':1032,'output_pins_sha256':s['output_pins']['sha256']}
(A/'ROOT_WHOLE_PACKAGE_REVIEW_01.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_ADOPT_ONE_P3','inputs':len(inputs),'outputs':len(outputs),'case_alias_reproduced_both_modes':True,'ready':False}))
