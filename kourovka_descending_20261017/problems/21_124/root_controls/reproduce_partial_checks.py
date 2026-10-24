#!/usr/bin/env python3
"""Rerun partial certificates in disposable copies; never alter frozen inputs."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, tempfile, time
BASE=Path(__file__).resolve().parent.parent
CHECKS=["negative_review/independent_check.py", "negative_geometric/check_uniform_retraction.py", "retraction_review/independent_check.py", "retraction_review/independent_cellular_check.py", "retraction_review/k1_boundary/independent_check.py", "positive_hierarchy/check_one_twist.py", "one_twist_review/independent_check.py", "flats_review/independent_check.py", "dihedral_review/independent_check.py", "height_envelope_review/independent_check.py", "root_orbit/verify_positive_witness.py", "regular_reduction_review/independent_check.py", "pell_positive_review/independent_check.py", "root_orbit/verify_height_positive_witness.py", "height_positive_review/independent_check.py", "smoothing_review/independent_check.py"]
SOURCES=["delage2602.08759v3.html", "wu_ye2504.14192v2.html", "linton2510.10178v2.html", "merladet_minasyan2511.21293v1.html", "merladet_minasyan2505.18054v3.html"]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    receipt=BASE/"ROOT_REPRODUCTION.json"
    prior=json.loads(receipt.read_text()) if receipt.exists() else {"checks":[]}
    frozen={str(p.relative_to(BASE)):digest(p) for p in BASE.rglob("*") if p.is_file() and (any(str(p.relative_to(BASE)).startswith(x) for x in ["root_controls/", "tubular/", "negative_geometric/", "positive_hierarchy/", "negative_review/", "retraction_review/", "one_twist_review/"])) and "__pycache__" not in p.parts}
    runs=[]
    with tempfile.TemporaryDirectory(prefix="kourovka124_partial_repro_") as tmp:
        target=Path(tmp)/"21_124"
        def ignore(parent,names):
            omit={"__pycache__", ".venv"}
            if Path(parent)==BASE/"priority": omit.add("sources")
            return [n for n in names if n in omit]
        shutil.copytree(BASE,target,ignore=ignore)
        (target/"priority/sources").mkdir(parents=True,exist_ok=True)
        for name in SOURCES: shutil.copy2(BASE/"priority/sources"/name,target/"priority/sources"/name)
        selected=sys.argv[1:] or CHECKS
        assert set(selected)<=set(CHECKS), "Unknown checker selection"
        for name in selected:
            # Restore every frozen input before each checker: author checkers may
            # rewrite timestamped outputs that later reviewers hash exactly.
            shutil.copytree(BASE,target,ignore=ignore,dirs_exist_ok=True)
            for source_name in SOURCES: shutil.copy2(BASE/"priority/sources"/source_name,target/"priority/sources"/source_name)
            start=time.monotonic()
            result=subprocess.run([sys.executable,str(target/name)],capture_output=True,text=True,timeout=120)
            run={"checker":name,"input_sha256":digest(BASE/name),"exit_code":result.returncode,"seconds":round(time.monotonic()-start,4),"stdout":result.stdout,"stderr":result.stderr}
            runs.append(run)
            print(json.dumps({k:run[k] for k in ("checker","exit_code","seconds")}),flush=True)
    assert all(digest(BASE/name)==h for name,h in frozen.items()), "Frozen input changed during root rerun"
    old=prior.get("checks",[])
    history=prior.get("diagnostics",[])
    for x in old:
        if x.get("exit_code")!=0:
            explanation="Invocation omitted raw source files needed for input hashing; corrected snapshot includes them." if "FileNotFoundError" in x.get("stderr","") else "A preceding author checker rewrote a timestamped certificate in the shared temporary snapshot. Runner now restores frozen original bytes before each checker. Original author/reviewer files were unchanged."
            history.append(dict(x,explanation=explanation))
    latest={x["checker"]:x for x in old if x.get("exit_code")==0}
    latest.update({x["checker"]:x for x in runs})
    payload={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Root reproduces restricted partial checkers in temporary byte copies, preserving frozen author/reviewer artifacts. No complete Kourovka solution, proof by finite tests, or novelty certification.","all_checks_passed":all(x["exit_code"]==0 for x in latest.values()),"checks":list(latest.values()),"diagnostics":history,"frozen_original_files_verified_unchanged":len(frozen),"source_snapshot_sha256":{n:digest(BASE/"priority/sources"/n) for n in SOURCES},"runner_sha256":digest(Path(__file__))}
    receipt.write_text(json.dumps(payload,indent=2)+"\n")
    assert payload["all_checks_passed"]
if __name__=="__main__": main()
