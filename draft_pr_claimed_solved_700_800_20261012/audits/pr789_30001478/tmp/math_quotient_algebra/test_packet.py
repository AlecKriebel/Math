#!/usr/bin/env python3
"""Disposable custody controls; never writes the source packet or intake."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reseal(root):
    records=[]
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name!="MANIFEST.json":
            records.append({"path":path.relative_to(root).as_posix(),"bytes":path.stat().st_size,"sha256":digest(path)})
    (root/"MANIFEST.json").write_text(json.dumps({"schema":"pr789-quotient-algebra-v1","files":records},indent=2,sort_keys=True)+"\n")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--packet",required=True)
    p.add_argument("--intake-root",required=True)
    p.add_argument("--primary-root",required=True)
    p.add_argument("--expected-manifest-sha256",required=True)
    p.add_argument("--expected-checker-sha256",required=True)
    a=p.parse_args()
    original=Path(a.packet).absolute()
    cases=[]
    # macOS's default /var temporary path can contain a symlink ancestor.
    # Use the already authenticated packet parent for ordinary-path baselines.
    with tempfile.TemporaryDirectory(prefix="pr789 quotient controls ",dir=original.parent) as temporary:
        base=Path(temporary)
        for name,kind in [("normal",True),("optimized",True),("wrong_manifest_pin",False),
            ("wrong_checker_pin",False),("extra_file",False),("missing_file",False),
            ("changed_report",False),("empty_directory",False),("file_symlink",False),
            ("file_hardlink",False),("root_symlink",False),("self_symlink",False),
            ("nonregular_fifo",False),("rehashed_input_binding",False),
            ("rehashed_head_identity",False),("duplicate_manifest_key",False),
            ("nonfinite_manifest",False),("unsafe_manifest_path",False)]:
            root=base/name
            shutil.copytree(original,root)
            requested=root
            checker=root/"verify_packet.py"
            mf=a.expected_manifest_sha256
            cp=a.expected_checker_sha256
            if name=="wrong_manifest_pin": mf="0"*64
            elif name=="wrong_checker_pin": cp="0"*64
            elif name=="extra_file": (root/"EXTRA").write_text("x")
            elif name=="missing_file": (root/"REPORT.md").unlink()
            elif name=="changed_report": (root/"REPORT.md").write_text("modified")
            elif name=="empty_directory": (root/"empty").mkdir()
            elif name=="file_symlink":
                (root/"REPORT.md").unlink(); (root/"REPORT.md").symlink_to(original/"REPORT.md")
            elif name=="file_hardlink":
                (root/"REPORT.md").unlink(); os.link(original/"REPORT.md",root/"REPORT.md")
            elif name=="root_symlink":
                requested=base/(name+" alias"); requested.symlink_to(root,target_is_directory=True)
                checker=requested/"verify_packet.py"
            elif name=="self_symlink":
                checker.unlink(); checker.symlink_to(original/"verify_packet.py")
            elif name=="nonregular_fifo":
                (root/"REPORT.md").unlink(); os.mkfifo(root/"REPORT.md")
            elif name in ("rehashed_input_binding","rehashed_head_identity"):
                path=root/"SOURCE_BINDINGS.json"
                value=json.loads(path.read_text())
                if name=="rehashed_input_binding": value["inputs"][0]["sha256"]="0"*64
                else: value["reviewed_head"]="0"*40
                path.write_text(json.dumps(value,sort_keys=True)+"\n")
                reseal(root); mf=digest(root/"MANIFEST.json")
            elif name in ("duplicate_manifest_key","nonfinite_manifest","unsafe_manifest_path"):
                path=root/"MANIFEST.json"
                if name=="duplicate_manifest_key": path.write_text('{"schema":"x","schema":"y","files":[]}')
                elif name=="nonfinite_manifest": path.write_text('{"schema":"pr789-quotient-algebra-v1","files":[NaN]}')
                else:
                    value=json.loads(path.read_text()); value["files"][0]["path"]="../bad"
                    path.write_text(json.dumps(value))
                mf=digest(path)
            flags=[sys.executable,"-I","-B"]+(["-O"] if name=="optimized" else [])
            cmd=flags+[str(checker),"--packet",str(requested),"--intake-root",a.intake_root,
                "--expected-manifest-sha256",mf,"--expected-checker-sha256",cp,
                "--primary-root",a.primary_root]
            proc=subprocess.run(cmd,capture_output=True,text=True,timeout=30,cwd=base)
            observed=proc.returncode==0
            if observed!=kind:
                raise ValueError(name+": unexpected result "+proc.stderr)
            cases.append({"name":name,"expected":"PASS" if kind else "REJECT","observed":"PASS" if observed else "REJECT"})
            # A hardlink control temporarily raises the original file's link count.
            shutil.rmtree(root)
    print(json.dumps({"status":"PASS","positive_controls":2,"negative_controls":16,"controls":cases},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
