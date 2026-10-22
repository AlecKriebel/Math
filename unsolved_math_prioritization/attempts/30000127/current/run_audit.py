#!/usr/bin/env python3
"""Replay exact checks and actual nonroot read-only probes; write one evidence file.

Usage: python run_audit.py --original-packet /path/to/original/authored --output /path/to/results.json
The input packet is read only. Temporary checker copies have read-only modes.
"""
import argparse
import datetime
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


EXPECTED_ORIGINAL_MANIFEST="6e5176946e05030e4ef98dd96123036e57433c080c3e7b9207bda7812a82cc31"


def require(ok,label):
    if not ok:raise ValueError(label)


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    return [{"file":p.relative_to(root).as_posix(),"bytes":p.stat().st_size,"sha256":digest(p)}
            for p in sorted(root.rglob("*")) if p.is_file()]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--original-packet",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    require(os.geteuid()!=0,"Run as an actual nonroot user; root is not a read-only permission probe")
    original=args.original_packet.resolve();here=Path(__file__).resolve().parent
    require(digest(original/"MANIFEST.json")==EXPECTED_ORIGINAL_MANIFEST,"Original manifest hash")
    original_before=snapshot(original)
    manifest=json.loads((original/"MANIFEST.json").read_text())
    for item in manifest["files"]:
        pp=original/item["file"]
        require(pp.stat().st_size==item["bytes"] and digest(pp)==item["sha256"],"Original input hash "+item["file"])
    require(digest(here/"verify_algebra.py")==digest(original/"verify_algebra.py"),"Inherited verifier preserved")
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    runs=[];probes=[]; fixture_before=None;fixture_after=None
    with tempfile.TemporaryDirectory(prefix="leroux-audit-") as temp:
        fixture=Path(temp)/"readonly";fixture.mkdir()
        for name in ["verify_algebra.py","audit_checks.py"]:
            shutil.copyfile(here/name,fixture/name);(fixture/name).chmod(0o444)
        fixture.chmod(0o555)
        try:
            fixture_before=snapshot(fixture)
            for name,operation in [("create",lambda: (fixture/"forbidden.tmp").open("xb")),
                                   ("append",lambda: (fixture/"audit_checks.py").open("ab"))]:
                try:
                    fp=operation();fp.close()
                    raise ValueError("Read-only "+name+" unexpectedly succeeded")
                except PermissionError as exc:
                    require(exc.errno in [errno.EACCES,errno.EPERM],"Unexpected probe errno")
                    probes.append({"operation":name,"outcome":"denied","errno":exc.errno})
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
            suites={"verify_algebra.py":["none","alter_collision_rate","reverse_entropy_flux","omit_mixed_derivative"],
                    "audit_checks.py":["none","wrong_face_flux","reverse_cone","drop_viscous_cross","wrong_third_jet","assume_kernel_exact"]}
            for mode in ["normal","-O","-OO"]:
                for script,mutations in suites.items():
                    for mutation in mutations:
                        command=[sys.executable,"-B"]+([] if mode=="normal" else [mode])+[script,"--mutation",mutation]
                        proc=subprocess.run(command,cwd=fixture,env=env,capture_output=True,text=True,timeout=120)
                        expected=0 if mutation=="none" else 1
                        require(proc.returncode==expected,f"Unexpected exit: {script} {mode} {mutation}")
                        if mutation!="none":require("ValueError:" in proc.stderr,"Mutation must fail on validation")
                        runs.append({"script":script,"mode":mode,"mutation":mutation,"exit_code":proc.returncode,
                                     "outcome":"passed" if mutation=="none" else "mutation_rejected",
                                     "stdout":proc.stdout.strip(),"stderr":proc.stderr.replace(str(fixture),"$READ_ONLY_FIXTURE")})
            fixture_after=snapshot(fixture)
            require(fixture_before==fixture_after,"Read-only fixture changed")
        finally:
            fixture.chmod(0o755)
            for pp in fixture.iterdir():pp.chmod(0o644)
    original_after=snapshot(original)
    require(original_before==original_after,"Original packet changed")
    evidence={"started_utc":started,"finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "python_version":sys.version,"effective_uid":os.geteuid(),"effective_gid":os.getegid(),
              "nonroot":True,"fixture_directory_mode":"0555","fixture_file_modes":"0444","permission_probes":probes,
              "fixture_before":fixture_before,"fixture_after":fixture_after,"fixture_unchanged":True,
              "original_manifest_sha256":EXPECTED_ORIGINAL_MANIFEST,"original_before":original_before,
              "original_after":original_after,"original_preserved":True,"runs":runs,
              "successful_baselines":sum(v["mutation"]=="none" for v in runs),
              "rejected_mutations":sum(v["mutation"]!="none" for v in runs),
              "runner_sha256":digest(Path(__file__)),
              "limitations":"Exact symbolic identities, finite controls, and filesystem behavior only; not formal verification of PDE or stochastic theorems."}
    args.output.write_text(json.dumps(evidence,indent=2)+"\n")
    print(json.dumps({"status":"passed","baselines":evidence["successful_baselines"],"mutation_rejections":evidence["rejected_mutations"],"nonroot":True,"original_preserved":True}))


if __name__=="__main__":main()
