#!/usr/bin/env python3
"""Read-only retained evidence checks plus unchanged isolated legacy replays."""
from pathlib import Path
import hashlib
import json
import shutil
import sqlite3
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def sha(b): return hashlib.sha256(b).hexdigest()
manifest=json.loads((HERE/"MANIFEST.json").read_text())
for item in manifest["files"]:
    data=(HERE/item["path"]).read_bytes()
    assert sha(data)==item["sha256"] and len(data)==item["bytes"],item["path"]
receipt=json.loads((HERE/"ORIGINAL_FILE_RECEIPT.json").read_text())
for item in receipt["files"]:
    data=subprocess.check_output(["git","show",receipt["head"]+":"+item["path"]],cwd=ROOT)
    assert sha(data)==item["sha256"] and len(data)==item["bytes"],item["path"]
cache=ROOT/"unsolved_math_prioritization/cache"
db=sqlite3.connect("file:"+str(cache/"catalog.sqlite")+"?mode=ro",uri=True)
raw=db.execute("select payload,report from records where key=?",("30004186",)).fetchone()
assert isinstance(raw[1],str) and raw[1]=="{}"
assert sha(json.dumps([json.loads(raw[0]),json.loads(raw[1])],sort_keys=True).encode())=="759ed8f6518e7a61a2356296cdc080f951f41bc93ca448182f1ce2143cda5a7b"
db.close()
controls=subprocess.run(["/usr/bin/python3",str(HERE/"independent_source_controls.py"),"--no-write"],text=True,capture_output=True,check=True)
controls=json.loads(controls.stdout)
assert controls["check_count"]==16 and controls["rejected_mutants"]==12
(HERE/"ignoredtmp").mkdir(exist_ok=True)
runs=[]
with tempfile.TemporaryDirectory(prefix="read_only_repro_",dir=HERE/"ignoredtmp") as tmp:
    dest=Path(tmp)
    prefix="unsolved_math_prioritization/attempts/30004186/"
    for item in receipt["files"]:
        if item["path"].startswith(prefix):
            path=dest/item["path"][len(prefix):]
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(subprocess.check_output(["git","show",receipt["head"]+":"+item["path"]],cwd=ROOT))
    for script in ["check_identities.py","independent_review/submitted_check_identities.py","independent_review/independent_checks.py"]:
        before=sha((dest/script).read_bytes())
        result=subprocess.run(["/usr/bin/python3",str(dest/script)],cwd=dest,text=True,capture_output=True,check=True)
        assert sha((dest/script).read_bytes())==before
        result=json.loads(result.stdout)
        runs.append({"script":script,"count":result.get("passed",result.get("assertions")),"sympy":result["sympy_version"]})
assert [x["count"] for x in runs]==[20,20,135]
print(json.dumps({"status":"PASS","manifest_files":len(manifest["files"]),"original_git_blobs":len(receipt["files"]),"context_sha256":"759ed8f6518e7a61a2356296cdc080f951f41bc93ca448182f1ce2143cda5a7b","fresh_controls":16,"rejected_mutants":12,"legacy":runs,"limits":"No PDE, historical model/query absence or novelty certification."},indent=2))
