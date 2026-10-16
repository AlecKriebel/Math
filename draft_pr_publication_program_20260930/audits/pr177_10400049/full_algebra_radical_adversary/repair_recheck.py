#!/usr/bin/env python3
"""Additive independent review of narrow repaired inputs; preserve sealed records."""
import ast
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import re
import subprocess
import sys
import tempfile
import urllib.request

ROOT=Path(__file__).resolve().parent
REPAIR=ROOT.parent/"mathematical_repair_v1"
INPUTS=ROOT/"repair_inputs"
INPUTS.mkdir(exist_ok=True)

def require(ok, reason):
    if not ok: raise RuntimeError(reason)

def identity(path):
    body=path.read_bytes()
    return {"path":str(path),"bytes":len(body),"sha256":sha256(body).hexdigest()}

candidate=(REPAIR/"CANDIDATE.md").read_bytes()
verifier=(REPAIR/"verify.py").read_bytes()
require(sha256(candidate).hexdigest()=="6867df111f99ff3f0ed4be0682d110a96902903e0b1ae7ecb70dea6ff56f6dac","Repaired candidate identity mismatch")
for name,body in (("CANDIDATE.md",candidate),("verify.py",verifier)):
    (INPUTS/name).write_bytes(body)
original=ROOT.parent/"original_submission/files/unsolved_math_prioritization/attempts/10400049/CANDIDATE.md"
old=original.read_text(); new=candidate.decode(); code=verifier.decode()
start="## 2. The invariant and its actual zero set"
end="The main counterexample"
require(old[old.index(start):old.index(end)]==new[new.index(start):new.index(end)],"Mathematical proof changed")
tree=ast.parse(code)
require(not any(isinstance(node,ast.Assert) for node in ast.walk(tree)),"Repaired verifier contains assert")
ck=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=="ck")
require(any(isinstance(node,ast.Raise) for node in ast.walk(ck)),"ck lacks explicit exception")

mutations={
    "half_value":code.replace("half=F(1,2);chi_g=half**2","half=F(1,3);chi_g=half**2"),
    "kernel_factor":code.replace("chi_g*(4*chi_g-1)==0","chi_g*(4*chi_g+1)==0"),
    "orientation_sensitive_sum":code.replace("def G(v):return sum(x*x for x in v)","def G(v):return sum(x for x in v)"),
    "braid_residual_crossings":code.replace("expanded={2*n+r+e:a", "expanded={2*n+e:a"),
    "newton_denominator":code.replace("F(x-i,i+1)","F(x-i,1)"),
}
for name,text in mutations.items(): require(text!=code,"Mutation did not alter code: "+name)
guard_restore=mutations["half_value"].replace("if not t: raise RuntimeError('scientific control failed: '+g)","assert t,g")
require(guard_restore!=mutations["half_value"],"Assert restoration did not alter guard")

results=[]
def execute(label, script, optimization, expected_pass):
    with tempfile.TemporaryDirectory(prefix="repair_tmp_",dir=ROOT) as directory:
        d=Path(directory)
        (d/"CANDIDATE.md").write_bytes(candidate)
        (d/"verify.py").write_text(script)
        command=[sys.executable]+(["-O"] if optimization else [])+[str(d/"verify.py")]
        process=subprocess.run(command,capture_output=True,text=True,timeout=45,cwd=d)
        passed=process.returncode==0
        require(passed==expected_pass,"Unexpected result: "+label+" optimization="+str(optimization))
        record={"label":label,"optimization":optimization,"exit_code":process.returncode,
                "expected_pass":expected_pass,"actual_pass":passed,"script_sha256":sha256(script.encode()).hexdigest()}
        if passed:
            receipt=json.loads((d/"verification.json").read_text())
            require(receipt["status"]=="PASS","Malformed successful repaired receipt")
            record["clean_verifier_receipt"]=receipt
        else:
            match=re.search(r"scientific control failed: ([A-Za-z_]+)",process.stderr)
            if match: record["failure_category"]=match.group(1)
            elif "AssertionError" in process.stderr: record["failure_category"]="restored_assert_half_twist_character"
            else: raise RuntimeError("Failure is not a scientific guard rejection: "+label)
        # Raw stdout, stderr, tracebacks, temporary scripts and temporary bodies are not retained.
        results.append(record)

for optimization in (0,1):
    execute("repaired_baseline",code,optimization,True)
    for name,script in mutations.items(): execute(name,script,optimization,False)
execute("restored_assert_wrong_half",guard_restore,0,False)
execute("restored_assert_wrong_half",guard_restore,1,True)

sources=[]
private=ROOT/"private_sources"
for name,url in (
    ("author_archive.html","https://drorbn.net/AcademicPensieve/2001-06/"),
    ("author_question.pdf","https://katlas.math.toronto.edu/drorbn/AcademicPensieve/2001-06/one/Is_there_a_Hilbert%27s_Nullstellensatz_for_finite_type_invariants_of_linksQ.pdf"),
):
    with urllib.request.urlopen(url,timeout=45) as response:
        body=response.read(); resolved=response.geturl()
    (private/name).write_bytes(body)
    sources.append({**identity(private/name),"url_requested":url,"url_resolved":resolved,
                    "private_third_party_body":True,"actual_coverage":"complete archive listing" if name.endswith("html") else "complete one-page question; text and visual verification follows"})
now=datetime.now(timezone.utc).isoformat()
ledger={"created_utc":now,"repair_inputs_consumed":[identity(REPAIR/"CANDIDATE.md"),identity(REPAIR/"verify.py")],
        "original_candidate_comparison_input":identity(original),
        "retained_exact_input_copies":[identity(INPUTS/"CANDIDATE.md"),identity(INPUTS/"verify.py")],
        "proof_sections_2_through_integer_version_unchanged":True,
        "runtime":{"python_executable":sys.executable,"python_version":sys.version,"platform":platform.platform(),"binary_identity":identity(Path(sys.executable).resolve())},
        "acquired_primary_bodies":sources,"private_bodies_excluded_from_public_exact_allowlist":True,
        "no_priority_verdict":True,"raw_stderr_or_headers_retained":False}
(ROOT/"REPAIR_SOURCE_LEDGER.json").write_text(json.dumps(ledger,indent=2)+"\n")
receipt={"created_utc":now,"status":"pass","runs":results,"total_fresh_runs":len(results),
         "repaired_baselines":2,"guarded_wrong_science_rejections":10,
         "assert_restoration_control":{"normal_rejects":1,"optimized_falseaccepts":1},
         "guard_AST_checked":True,"script_identity":identity(Path(__file__)),
         "limits":"These are independent finite diagnostics. ROOT's reported 40-run history was not inspected or adopted. No priority finding follows."}
(ROOT/"REPAIR_EXECUTION_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":"pass","fresh_runs":len(results),"guarded_rejections":10,"primary_bodies":sources},indent=2))
