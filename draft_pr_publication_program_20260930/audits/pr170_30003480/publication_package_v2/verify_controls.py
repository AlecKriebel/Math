"""Reproduce exact finite controls and reject deliberately false variants."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
K=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise RuntimeError(message)
def pin(p):
    b=p.read_bytes();return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def run(mode,mutation):
    args=[sys.executable,"-E","-S","-B","-P"]+(["-O"] if mode=="optimized" else [])+[str(K/"verify_exact.py"),"--mutate",mutation]
    p=subprocess.run(args,cwd=K,capture_output=True,text=True,timeout=120)
    return p
def main():
    baselines={}
    for mode in ["normal","optimized"]:
        p=run(mode,"none")
        require(p.returncode==0 and not p.stderr,"Baseline failed: "+mode)
        j=json.loads(p.stdout)
        require(j["status"]=="EXACT_FINITE_CONTROLS_PASS" and j["mutate"]=="none","Wrong baseline")
        require(j["total_checks"]==46274 and j["valid_eigenvalue_grid_cases"]==1554 and j["outside_eigenvalue_grid_cases"]==1524 and j["integer_tensor_cases"]==6560,"Exact baseline counts differ")
        require(j["all_polynomial_nonexistence_proved_by_finite_checks"] is False,"Finite controls misrepresented")
        baselines[mode]=p.stdout
        (K/("verification."+mode+".json")).write_text(p.stdout)
    require(baselines["normal"]==baselines["optimized"],"Baseline outputs differ under optimization")
    broken=[]
    for mode in ["normal","optimized"]:
        for mutation,label in [("weights","exact real parity marginals"),("reflection","polynomial-coordinate involution identity"),("normalization","normalized integer-tensor determinant bound"),("Q2","printed full-sign Q2 exact value")]:
            p=run(mode,mutation)
            require(p.returncode!=0 and not p.stdout and ("RuntimeError: "+label) in p.stderr,"False variant escaped or failed for the wrong reason: "+mode+"/"+mutation)
            broken.append({"mode":mode,"mutation":mutation,"exit_code":p.returncode,"required_error":label,"rejected":True})
    receipt={"status":"PASS_IDENTICAL_BASELINES_AND_ALL_FALSE_VARIANTS_REJECTED","ordinary_optimized_outputs_byte_identical":True,"finite_checks_per_baseline":46274,"rejections":broken,"manuscript":pin(K/"gram_locus_note.tex"),"checker":pin(K/"verify_exact.py"),"driver":pin(K/"verify_controls.py"),"Python_version":sys.version.split()[0],"resolved_executable":os.path.realpath(sys.executable),"universal_nonexistence_is_written_proof_not_finite_checks":True}
    (K/"negative_controls.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"status":receipt["status"],"checks_per_baseline":46274,"negative_rejections":len(broken),"manuscript_SHA256":receipt["manuscript"]["sha256"]}))
if __name__=="__main__":main()
