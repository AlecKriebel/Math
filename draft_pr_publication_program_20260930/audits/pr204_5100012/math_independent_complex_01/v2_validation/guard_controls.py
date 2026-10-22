"""Bounded real mutation controls plus full ordinary/optimized valid runs."""
import sys
sys.dont_write_bytecode = True
import pathlib,os,json,subprocess,hashlib,datetime
BASE=pathlib.Path(__file__).resolve().parent
PIN="4ca9a0a74d59acd78865252388696b7e8b71a8ed71d1c0669b0a078413ae6071"
EXPECTED=dict(symbolic_identities=5,configurations=27,phases=81,wrong_parity_configurations_enforced=6,repeated_list_phases=2)

def require(condition,message):
    if not condition:
        raise RuntimeError(message)

def parent_check():
    path=BASE.parent/"AUTHORED_MANIFEST.json"
    require(path.is_file(),"Sealed parent manifest required for these local custody controls")
    require(hashlib.sha256(path.read_bytes()).hexdigest()==PIN,"Parent manifest pin changed")
    manifest=json.loads(path.read_text())
    for item in manifest["files"]:
        current=BASE.parent/item["path"]
        require(current.stat().st_size==item["bytes"],"Parent size changed: "+item["path"])
        require(hashlib.sha256(current.read_bytes()).hexdigest()==item["sha256"],"Parent bytes changed: "+item["path"])
    return len(manifest["files"])

sealed_count=parent_check()
env=os.environ.copy()
env["PYTHONDONTWRITEBYTECODE"]="1"
outcomes=[]
valid=[]
for optimized in (False,True):
    command=[sys.executable,"-B"]+(["-O"] if optimized else [])+[str(BASE/"verify_complex_v2.py")]
    result=subprocess.run(command,env=env,text=True,capture_output=True,check=False)
    require(result.returncode==0 and result.stderr=="","Valid run failed: "+result.stderr)
    parsed=json.loads(result.stdout)
    require(parsed["mutation"]=="none" and parsed["optimized"]==optimized,"Unexpected valid-run mode")
    require(parsed["counts"]==EXPECTED,"Count mismatch")
    require(parsed["runtime"]["bytecode_disabled"],"Bytecode was enabled")
    require(parsed["parent_manifest"]["verified_if_available"],"Parent pin not checked")
    filename="valid_optimized.json" if optimized else "valid_normal.json"
    (BASE/filename).write_text(result.stdout)
    valid.append(parsed)
    outcomes.append(dict(mode="optimized" if optimized else "ordinary",mutation="none",accepted=True,counts=parsed["counts"],output=filename,sha256=hashlib.sha256(result.stdout.encode()).hexdigest()))
    for mutation,kind,name in [("false_identity","symbolic_identity","contact_minus"),("false_numeric_identity","upper_bound","first_area_identity"),("nan_residual","nonfinite","first_area_identity")]:
        result=subprocess.run(command+["--mutation",mutation],env=env,text=True,capture_output=True,check=False)
        require(result.returncode==2 and result.stdout=="","Mutation did not fail through the checker: "+mutation)
        rejected=json.loads(result.stderr)
        require(rejected.get("rejected") is True and rejected.get("mutation")==mutation,"Mutation failure not authenticated")
        require(rejected.get("kind")==kind and rejected.get("name")==name,"Mutation failed at the wrong check: "+str(rejected))
        require(rejected.get("optimized")==optimized,"Wrong optimization mode in rejection")
        outcomes.append(dict(mode="optimized" if optimized else "ordinary",mutation=mutation,accepted=False,rejection=rejected))
# Full outputs must agree apart from UTC and the optimization marker.
for item in valid:
    item.pop("utc")
    item.pop("optimized")
require(valid[0]==valid[1],"Ordinary/optimized validation results differ")
require(parent_check()==sealed_count,"Parent custody count changed")
output=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope="Bounded validation-code hardening only; no new theorem issue.",parent_manifest_sha256=PIN,sealed_parent_artifacts_verified_before_and_after=sealed_count,full_valid_runs=2,mutation_rejections=6,mutation_scope="Actual first contact target 1->2; actual first area identity coefficient doubled; NaN injected into first numerical area residual.",outcomes=outcomes,ordinary_optimized_results_match=True)
(BASE/"controls_output.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
print(json.dumps(dict(full_valid_runs=2,mutation_rejections=6,counts=EXPECTED,sealed_parent_artifacts_unchanged=sealed_count,ordinary_optimized_results_match=True),sort_keys=True))
