#!/usr/bin/env python3
"""Reproduce frozen finite checks without writing to the source snapshot."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
SOURCE = AUDIT / "source_snapshot/unsolved_math_prioritization/attempts/30003656"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def check_manifests():
    records = []
    receipt = json.loads((AUDIT / "SOURCE_RECEIPT.json").read_text())
    for row in receipt["files"]:
        p = AUDIT / "source_snapshot" / row["path"]
        records.append({"origin":"SOURCE_RECEIPT", "path":str(p.relative_to(AUDIT)),
                        "hash_match":sha(p)==row["sha256"], "size_match":p.stat().st_size==row["size"]})
    for manifest_path in [SOURCE/"FROZEN_AUTHOR_MANIFEST.json",SOURCE/"audit/FROZEN_INPUTS.json"]:
        manifest = json.loads(manifest_path.read_text())
        for name, digest in manifest["files"].items():
            records.append({"origin":str(manifest_path.relative_to(SOURCE)),"path":name,
                            "hash_match":sha(SOURCE/name)==digest})
        if "manifest_sha256" in manifest:
            records.append({"origin":str(manifest_path.relative_to(SOURCE)),"path":"FROZEN_AUTHOR_MANIFEST.json",
                            "hash_match":sha(SOURCE/"FROZEN_AUTHOR_MANIFEST.json")==manifest["manifest_sha256"]})
    audit_manifest = json.loads((SOURCE/"audit/AUDIT_MANIFEST.json").read_text())
    for name, row in audit_manifest["portable_files"].items():
        p = SOURCE/"audit"/name
        records.append({"origin":"audit/AUDIT_MANIFEST.json","path":"audit/"+name,
                        "hash_match":sha(p)==row["sha256"],"size_match":p.stat().st_size==row["bytes"]})
    if not all(x["hash_match"] and x.get("size_match",True) for x in records):
        raise RuntimeError("Frozen manifest mismatch")
    return records

def run(label, program, optimized=False):
    cmd = [sys.executable,"-B"] + (["-O"] if optimized else []) + [str(program)]
    start = utc()
    begin = time.monotonic()
    result = subprocess.run(cmd,cwd=program.parent,capture_output=True,timeout=120)
    elapsed = time.monotonic()-begin
    stdout = HERE/(label+".stdout.txt")
    stderr = HERE/(label+".stderr.txt")
    stdout.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    return {"label":label,"command":cmd,"cwd":str(program.parent),"started_utc":start,
            "finished_utc":utc(),"elapsed_seconds":elapsed,"returncode":result.returncode,
            "program_sha256":sha(program),"stdout_sha256":sha(stdout),"stderr_sha256":sha(stderr),
            "stdout_path":str(stdout.relative_to(HERE)),"stderr_path":str(stderr.relative_to(HERE))}

def main():
    before = check_manifests()
    runs = []
    comparisons = []
    for mode in ["normal","optimized"]:
        target = HERE/"runs"/mode
        (target/"audit").mkdir(parents=True,exist_ok=True)
        for relative, output in [("check_exact.py","exact_results.json"),
                                 ("audit/audit_controls.py","audit/audit_controls.json")]:
            program = target/relative
            shutil.copyfile(SOURCE/relative,program)
            runs.append(run(mode+"_"+program.stem,program,mode=="optimized"))
            result_file = target/output
            expected = SOURCE/output
            comparisons.append({"mode":mode,"path":output,"actual_sha256":sha(result_file),
                                "expected_sha256":sha(expected),
                                "byte_equal":result_file.read_bytes()==expected.read_bytes()})
    after = check_manifests()
    receipt = {"started_scope":"PR480/problem30003656 finite verification only",
               "head_sha":json.loads((AUDIT/"SOURCE_RECEIPT.json").read_text())["head_sha"],
               "finished_utc":utc(),"completion_estimate_percent":55,
               "python_executable":sys.executable,"python_version":sys.version,
               "platform":platform.platform(),"PYTHONOPTIMIZE_environment":os.getenv("PYTHONOPTIMIZE"),
               "before_manifest_checks":before,"after_manifest_checks":after,
               "runs":runs,"comparisons":comparisons,
               "all_runs_exit_zero":all(x["returncode"]==0 for x in runs),
               "all_outputs_byte_equal":all(x["byte_equal"] for x in comparisons)}
    (HERE/"replay_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"finished_utc":receipt["finished_utc"],"runs":len(runs),
                      "manifest_checks_per_pass":len(before),
                      "all_runs_exit_zero":receipt["all_runs_exit_zero"],
                      "all_outputs_byte_equal":receipt["all_outputs_byte_equal"]},indent=2))

if __name__=="__main__": main()
