#!/usr/bin/env python3
"""Run valid computations and require specific intended false-claim rejection."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib, json, subprocess, sys

HERE=Path(__file__).resolve().parent
PROGRAM=HERE/"areal_metric_controls.py"
PRIVATE=HERE/"private_cases"
OUTPUT=HERE/"adversarial_diagnostics"
PRIVATE.mkdir(exist_ok=True)
OUTPUT.mkdir(exist_ok=True)

def require(condition,name):
    if not condition:
        raise RuntimeError(name)

def sha(data):
    return hashlib.sha256(data).hexdigest()

valid=[]
names=None
for optimized in (False,True):
    label="optimized" if optimized else "normal"
    path=OUTPUT/("valid_"+label+".json")
    cmd=[sys.executable]+(["-O"] if optimized else [])+[str(PROGRAM),"--output",str(path)]
    proc=subprocess.run(cmd,capture_output=True,text=True,check=False)
    (OUTPUT/("valid_"+label+".stdout.txt")).write_text(proc.stdout)
    (OUTPUT/("valid_"+label+".stderr.txt")).write_text(proc.stderr)
    require(proc.returncode==0,"valid "+label+" exit")
    obj=json.loads(path.read_text())
    require(obj["all_passed"] is True,"valid "+label+" status")
    require(obj["exact_check_count"]==67 and len(obj["checks"])==67 and all(type(v)is bool and v for v in obj["checks"].values()),"valid "+label+" explicit active count")
    names=obj["invalid_claim_names"]
    valid.append({"mode":label,"exit_code":0,"exact_checks":67,"sha256":sha(path.read_bytes())})
require(valid[0]["sha256"]==valid[1]["sha256"],"valid normal/optimized bytes differ")
require(len(names)==16 and len(set(names))==16,"sixteen distinct targeted false claims")

def run_one(item):
    name,optimized=item
    label=name+("_optimized" if optimized else "_normal")
    fixture=PRIVATE/(label+".json")
    fixture.write_text(json.dumps({"claim":name})+"\n")
    cmd=[sys.executable]+(["-O"] if optimized else [])+[str(PROGRAM),"--claim-file",str(fixture)]
    proc=subprocess.run(cmd,capture_output=True,text=True,check=False)
    (OUTPUT/(label+".stdout.txt")).write_text(proc.stdout)
    (OUTPUT/(label+".stderr.txt")).write_text(proc.stderr)
    expected="InvalidClaim:EXPECTED_FALSE_CLAIM_REJECTED:"+name+"\n"
    require(proc.returncode==4,"wrong rejection exit "+label)
    require(proc.stdout=="" and proc.stderr==expected,"wrong rejection diagnostic "+label)
    return {"claim":name,"optimized":optimized,"exit_code":4,"intended_rejection":True,"stderr_sha256":sha(proc.stderr.encode()),"unexpected_crash":False}

with ThreadPoolExecutor(max_workers=4) as pool:
    rejected=list(pool.map(run_one,[(name,optimized) for name in names for optimized in (False,True)]))
result={"valid_runs":valid,"false_claim_count":16,"actual_rejection_executions":len(rejected),"all_expected_rejections":True,"rejections":rejected,"guards_active_under_optimization":True,"private_fixture_files_not_publishable":True}
(HERE/"ADVERSARIAL_RECEIPT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"valid_runs":2,"exact_checks_per_run":67,"distinct_false_claims":16,"actual_expected_rejections":len(rejected),"normal_optimized_valid_output_identical":True},indent=2))
