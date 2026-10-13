from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PYTHON = "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14"
ENV = {"PATH":"/usr/bin:/bin", "LC_ALL":"C", "LANG":"C", "TZ":"UTC",
       "__CF_USER_TEXT_ENCODING":"0x1F5:0x0:0x0"}
records = []
for label, optimization in (("normal", []), ("optimized", ["-O"])):
    args = [PYTHON, "-E", "-S", "-B", "-P"] + optimization + [str(HERE/"independent_polytope_audit.py")]
    started = datetime.now(timezone.utc).isoformat()
    child = subprocess.Popen(args, cwd=HERE, env=ENV, stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = child.communicate()
    (HERE/(label+"_results.json")).write_bytes(stdout)
    (HERE/(label+"_stderr.txt")).write_bytes(stderr)
    record = {"label":label,"pid":child.pid,"returncode":child.returncode,"reaped":True,
              "started_utc":started,"completed_utc":datetime.now(timezone.utc).isoformat(),
              "args":args,"stdout_bytes":len(stdout),"stdout_sha256":hashlib.sha256(stdout).hexdigest(),
              "stderr_bytes":len(stderr),"stderr_sha256":hashlib.sha256(stderr).hexdigest()}
    records.append(record)
    if child.returncode or stderr:
        (HERE/"RUN_RECEIPT.json").write_text(json.dumps({"status":"FAIL","children":records},indent=2)+"\n")
        raise RuntimeError(label+" independent audit failed: "+stderr.decode(errors="replace"))
    parsed = json.loads(stdout)
    if parsed["status"] != "PASS" or parsed["explicit_guards"] < 100:
        raise RuntimeError("Missing successful explicit guards")
    record["explicit_guards"] = parsed["explicit_guards"]
    record["status"] = parsed["status"]
first, second = [json.loads((HERE/(r["label"]+"_results.json")).read_text()) for r in records]
first.pop("optimizations_disabled"); second.pop("optimizations_disabled")
if first != second:
    raise RuntimeError("Optimization changed exact mathematical output")
receipt = {"status":"PASS","root_pid":__import__("os").getpid(),"children":records,
           "normal_optimized_math_outputs_identical":True,
           "code_sha256":hashlib.sha256((HERE/"independent_polytope_audit.py").read_bytes()).hexdigest()}
(HERE/"RUN_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":"PASS","children":[{"pid":r["pid"],"guards":r["explicit_guards"],"returncode":r["returncode"]} for r in records]}))
