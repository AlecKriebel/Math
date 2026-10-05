#!/usr/bin/env python3
"""Integrity negative controls run in disposable copies of the safe payload."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile


def run():
    source=Path(__file__).resolve().parent
    checker=source/"verify_manifest.py"
    mutations=["alter_byte","truncate","missing_file","extra_file","extra_directory",
               "symlink","wrong_size","wrong_hash","duplicate_path","parent_path",
               "wrong_schema","extra_manifest_key"]
    results={}
    with tempfile.TemporaryDirectory(prefix="dirichlet-zero-controls-") as temp:
        for label in ["intact"]+mutations:
            root=Path(temp)/label
            shutil.copytree(source,root)
            file=root/"TURN_1_RECURRENCE.md"
            if label=="alter_byte": file.write_bytes(b"!"+file.read_bytes()[1:])
            elif label=="truncate": file.write_bytes(file.read_bytes()[:-1])
            elif label=="missing_file": file.unlink()
            elif label=="extra_file": (root/"unexpected.txt").write_text("extra")
            elif label=="extra_directory": (root/"unexpected").mkdir()
            elif label=="symlink":
                file.unlink(); file.symlink_to(source/"TURN_1_RECURRENCE.md")
            elif label not in {"intact"}:
                p=root/"MANIFEST.json"
                m=json.loads(p.read_text())
                if label=="wrong_size": m["files"][0]["bytes"]+=1
                elif label=="wrong_hash": m["files"][0]["sha256"]="0"*64
                elif label=="duplicate_path": m["files"].append(m["files"][0])
                elif label=="parent_path": m["files"][0]["path"]="../outside"
                elif label=="wrong_schema": m["schema"]="wrong"
                elif label=="extra_manifest_key": m["extra"]="wrong"
                p.write_text(json.dumps(m))
            cp=subprocess.run([sys.executable,"-B","-O",str(checker),"--root",str(root)],capture_output=True,text=True)
            passed=cp.returncode==0
            if passed!=(label=="intact"):
                raise ValueError("unexpected integrity verdict for "+label+": "+cp.stdout+cp.stderr)
            results[label]="accepted" if passed else "rejected"
    return {"schema":"dirichlet-single-zero-negative-controls-v1","result":"PASS",
            "optimized_python":True,"negative_cases":len(mutations),"cases":results}


if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True,indent=2))
