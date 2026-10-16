from pathlib import Path
import json, hashlib, subprocess, tempfile, shutil, datetime
A=Path(__file__).resolve().parent
R=A/'root_reproduction';R.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
pins=load(A/'SUBMITTED_PINS.json')
for x in pins['files']:
    b=(A/x['snapshot_path']).read_bytes()
    g=subprocess.run(['git','show',pins['head_oid']+':'+x['repository_path']],capture_output=True,check=True).stdout
    if b!=g or len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError('Original Git mismatch')
counts={};receipts=[]
for family in ['modular_encoding_01','dynamics_membership_01']:
    base=A/'reviews'/family;d=load(base/'OUTPUT_PINS.json');rows=d.get('records',d.get('files'))
    for x in rows:
        p=base/x.get('path_relative_to_review',x.get('path'));b=p.read_bytes()
        if len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError(str(p))
    counts[family]=len(rows)
    specs=[('check_modular_encoding.py','FRESH_CHECKS_NORMAL.json',False)] if family.startswith('modular') else [('check_dynamics_membership.py','CHECK_RESULTS_NORMAL_RESUMED.json',True),('check_semantic_addendum.py','SEMANTIC_ADDENDUM_NORMAL_RESUMED.json',True)]
    with tempfile.TemporaryDirectory(prefix=family+'-',dir=R) as td:
        td=Path(td)
        for script,ref,hasdest in specs:
            shutil.copy2(base/script,td/script)
            for opt in [False,True]:
                dest=td/(script+('-O.json' if opt else '.json'))
                # The semantic addendum imports its sibling implementation;
                # normal script-local imports must remain available.
                argv=['python3','-B']+(['-O'] if opt else [])+[str(td/script)]+([str(dest)] if hasdest else [])
                p=subprocess.run(argv,capture_output=True,check=True,cwd=td)
                data=json.loads(dest.read_bytes() if hasdest else p.stdout)
                if data!=load(base/ref):raise RuntimeError('Whole result differs: '+script)
                resultname=script+('-O.json' if opt else '.json');(R/resultname).write_text(json.dumps(data,indent=2)+'\n')
                receipts.append({'family':family,'script':script,'optimized':opt,'exit_code':p.returncode,'full_JSON_equals_saved_review_result':True,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'result':resultname})
                if hasdest:
                    bad=subprocess.run(argv[:-1]+['--self-test-invalid'],capture_output=True,cwd=td)
                    if bad.returncode==0:raise RuntimeError('Invalid runtime guard accepted')
                    receipts.append({'family':family,'script':script,'optimized':opt,'invalid_guard_exit':bad.returncode,'stderr_sha256':sha(bad.stderr)})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ROOT_FRESH_MATHEMATICAL_CONTROLS','actual_git_originals_authenticated':len(pins['files']),'complete_review_output_records_rehashed':counts,'actual_commands':receipts,'complete_normal_and_optimized_result_comparisons':6,'historical_omitted_programs_replayed':False,'scope':'Fresh independent family diagnostics on isolated copies; universal correctness rests on root-read written proofs and primary interfaces.'}
(A/'ROOT_MATH_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='actual_commands'}))
