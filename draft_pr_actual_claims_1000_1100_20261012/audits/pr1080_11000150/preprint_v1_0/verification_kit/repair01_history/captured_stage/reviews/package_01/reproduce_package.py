#!/usr/bin/env python3
"""Read-only candidate review; every injected mutation is in this review's scratch."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile

REVIEW = Path(__file__).resolve().parent
AUDIT = REVIEW.parent.parent
CANDIDATE = AUDIT / "preprint_v1_0"
SCRATCH = REVIEW / "tmp" / "reproduction"
PYTHON = sys.executable
RESULTS = []


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def execute(argv, cwd, tag, expect=None, env=None):
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=180, env=env)
    row = {"tag": tag, "argv": [str(x) for x in argv], "cwd": str(cwd),
           "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    RESULTS.append(row)
    if expect == "success":
        need(result.returncode == 0, "expected success: " + tag)
    elif expect == "failure":
        need(result.returncode != 0, "expected rejection: " + tag)
    return result


def reset():
    target = SCRATCH / "clean_check"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir()
    with zipfile.ZipFile(CANDIDATE / "verification_kit.zip") as z:
        z.extractall(target)
    return target / "verification_kit"


def main():
    SCRATCH.mkdir(parents=True, exist_ok=False)
    for name in ["preprint.pdf", "EXTERNAL_BINDING.json", "verification_kit.zip"]:
        shutil.copyfile(CANDIDATE/name, SCRATCH/name)
    target = SCRATCH / "clean_check"
    target.mkdir()
    execute(["unzip", "-q", "verification_kit.zip", "-d", "clean_check"], SCRATCH, "documented extraction", "success")
    kit = target / "verification_kit"
    before = {str(p.relative_to(kit)): sha(p) for p in kit.rglob("*") if p.is_file()}
    for optimized in [False, True]:
        prefix = [PYTHON, "-I", "-B"] + (["-O"] if optimized else [])
        mode = "optimized" if optimized else "normal"
        for script in ["verify.py", "run_checks.py", "fault_checks.py"]:
            execute(prefix+[script], kit, mode+" "+script, "success")
        execute(prefix+["build_archive.py", "--output", "../rebuilt.zip"], kit, mode+" builder", "success")
        execute(["cmp", "../../verification_kit.zip", "../rebuilt.zip"], kit, mode+" byte comparison", "success")
        execute(prefix+["verify.py", "--require-binding", "--binding", "../../EXTERNAL_BINDING.json",
                        "--pdf", "../../preprint.pdf", "--archive", "../../verification_kit.zip"],
                kit, mode+" strict external binding", "success")
    execute(["mkdir", "-p", "../compiled"], kit, "documented compile folder", "success")
    execute(["tectonic", "--outdir", "../compiled", "preprint.tex"], kit, "documented standalone compile", "success")
    compiled = target / "compiled/preprint.pdf"
    compile_receipt = {"bytes": compiled.stat().st_size, "sha256": sha(compiled),
                       "canonical_pdf_unchanged": sha(CANDIDATE/"preprint.pdf"),
                       "cross_runtime_byte_identity_not_promised": True}
    after = {str(p.relative_to(kit)): sha(p) for p in kit.rglob("*") if p.is_file()}
    need(before == after, "positive commands changed kit inputs")
    need(not any("Overfull" in x["stderr"] or "Overfull" in x["stdout"] for x in RESULTS), "overfull TeX warning")
    metadata_check = execute([PYTHON,"-B",str(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')),
                              "check",str(CANDIDATE/"deposit_metadata.json")],
                             Path('/Users/alec/Documents/Math'),"native Zenodo local manifest check","failure")
    need("Manifest must contain exactly 'metadata' and 'files'" in metadata_check.stderr,
         "unexpected native submission rejection")
    alias_results=[]
    for optimized in [False, True]:
        prefix=[PYTHON,"-I","-B"]+(["-O"] if optimized else [])
        for kind in ["direct_inside", "symlink_to_inside", "hardlink_to_inside", "symlink_to_outside", "symlink_ancestor_hardlink"]:
            kit=reset()
            source=kit/"preprint.tex"
            original=sha(source)
            output=SCRATCH/("alias-"+kind+".zip")
            if output.exists() or output.is_symlink():output.unlink()
            if kind=="direct_inside":output=source
            elif kind=="symlink_to_inside":output.symlink_to(source)
            elif kind=="hardlink_to_inside":os.link(source,output)
            elif kind=="symlink_to_outside":
                victim=SCRATCH/"external-sentinel.txt";victim.write_text("protected external sentinel\n")
                output.symlink_to(victim)
            elif kind=="symlink_ancestor_hardlink":
                directory=SCRATCH/"alias-directory"
                if directory.is_symlink():directory.unlink()
                directory.symlink_to(SCRATCH, target_is_directory=True)
                real=SCRATCH/"ancestor-target.zip"
                if real.exists():real.unlink()
                os.link(source,real)
                output=directory/real.name
            result=execute(prefix+["build_archive.py","--output",str(output)],kit,
                           kind+(" optimized" if optimized else " normal"))
            if kind in ["direct_inside","symlink_to_inside"]:
                need(result.returncode!=0 and sha(source)==original,"existing safe alias rejection regressed")
            elif kind in ["hardlink_to_inside","symlink_ancestor_hardlink"]:
                need(result.returncode==0 and sha(source)!=original,"known hardlink input corruption not reproduced")
            else:
                need(result.returncode==0 and victim.read_bytes().startswith(b"PK"),"resolved output symlink defect not reproduced")
            alias_results.append({"kind":kind,"optimized":optimized,"returncode":result.returncode,
                                  "source_before_sha256":original,"source_after_sha256":sha(source),
                                  "source_changed":sha(source)!=original,
                                  "outside_symlink_victim_overwritten":kind=="symlink_to_outside"})
            if output!=source and (output.exists() or output.is_symlink()):output.unlink()
    controls=[]
    for optimized in [False,True]:
        prefix=[PYTHON,"-I","-B"]+(["-O"] if optimized else [])
        for fault in ["extra_empty_directory","identical_manifest_symlink","identical_allowlist_symlink",
                      "blank_copy_omission_reason","blank_historical_omission_reason",
                      "coherent_metadata_changed_bound","binding_filename_escape"]:
            kit=reset();args=[]
            if fault=="extra_empty_directory":(kit/"unexpected-empty-directory").mkdir()
            elif fault.startswith("identical_"):
                n="MANIFEST.json" if "manifest" in fault else "ALLOWLIST.json"
                victim=SCRATCH/("original-"+n);shutil.copyfile(kit/n,victim);(kit/n).unlink();(kit/n).symlink_to(victim)
            elif "omission_reason" in fault:
                file=kit/"COPY_EXCLUSION_LEDGER.json";x=json.loads(file.read_text())
                rows=x["historical_pin_references"] if "historical" in fault else x["files"]
                next(q for q in rows if q["disposition"]=="omitted")["reason"]=""
                file.write_text(json.dumps(x))
                manifest=kit/"MANIFEST.json";m=json.loads(manifest.read_text());row=next(q for q in m["files"] if q["path"]==file.name)
                row["bytes"]=file.stat().st_size;row["sha256"]=sha(file);manifest.write_text(json.dumps(m))
            elif fault=="coherent_metadata_changed_bound":
                file=kit/"metadata.json";x=json.loads(file.read_text());x["title"]="Injected wrong title";file.write_text(json.dumps(x))
                manifest=kit/"MANIFEST.json";m=json.loads(manifest.read_text());row=next(q for q in m["files"] if q["path"]==file.name)
                row["bytes"]=file.stat().st_size;row["sha256"]=sha(file);manifest.write_text(json.dumps(m))
                args=["--binding",str(SCRATCH/"EXTERNAL_BINDING.json")]
            else:
                x=json.loads((SCRATCH/"EXTERNAL_BINDING.json").read_text());x["pdf"]["filename"]="../preprint.pdf"
                changed=SCRATCH/"bad-binding.json";changed.write_text(json.dumps(x));args=["--binding",str(changed)]
            result=execute(prefix+["verify.py"]+args,kit,"fresh semantic fault "+fault,"failure")
            controls.append({"fault":fault,"optimized":optimized,"detected":result.returncode!=0})
        for fault in ["conjugation","parity","erasing"]:
            result=execute(prefix+[str(REVIEW/"independent_checks.py"),"--fault",fault],REVIEW,"independent math fault "+fault,"failure")
            need("RuntimeError" in result.stderr,"math guard missing")
        execute(prefix+[str(REVIEW/"independent_checks.py")],REVIEW,"independent fresh math positive","success")
    receipt={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "all_documented_clean_commands_passed":True,"normal_and_optimized_passed":True,
             "positive_commands_preserved_all_kit_files":True,"compile":compile_receipt,
             "native_zenodo_manifest_fails":True,"alias_defects":alias_results,
             "new_semantic_negative_controls":controls,"actual_commands":RESULTS,
             "candidate_mutations":False,"scratch_mutations_only":True}
    (REVIEW/"REPRODUCTION_RECEIPTS.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"commands":len(RESULTS),"aliases":alias_results,"semantic_controls":len(controls),"compile":compile_receipt},indent=2))
    shutil.rmtree(SCRATCH)


if __name__=="__main__":
    main()
