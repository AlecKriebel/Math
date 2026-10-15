"""Read/copy original controls only after the independent construction checkpoint."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent/"original_head_authentication_20261006"/"original_attempt"
PYTHON = "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14"
ENV = {"PATH":"/usr/bin:/bin","LC_ALL":"C","LANG":"C","TZ":"UTC",
       "__CF_USER_TEXT_ENCODING":"0x1F5:0x0:0x0"}
checkpoint = json.loads((HERE/"INDEPENDENCE_CHECKPOINT.json").read_text())
if not checkpoint["independent_proof_and_exact_controls_before_original_checker_read"]:
    raise RuntimeError("Independent checkpoint missing")
for name,pin in checkpoint["files"].items():
    body=(HERE/name).read_bytes()
    if len(body)!=pin["bytes"] or hashlib.sha256(body).hexdigest()!=pin["sha256"]:
        raise RuntimeError("Independent checkpoint changed before comparison")
pins={}
for name in ("CANDIDATE.md","verify.py","verification.json","review/REVIEW.md",
             "review/independent_checks.py","review/independent_results.json"):
    body=(ORIGINAL/name).read_bytes()
    pins[name]={"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()}

records=[]
cases=(("original_author_normal","verify.py","verification.json","verification.json"),
       ("original_review_normal","review/independent_checks.py","review/independent_results.json","independent_results.json"))
for label,code_path,expected_path,result_name in cases:
    folder=HERE/label
    folder.mkdir(exist_ok=True)
    (folder/Path(code_path).name).write_bytes((ORIGINAL/code_path).read_bytes())
    if label=="original_author_normal":
        (folder/"CANDIDATE.md").write_bytes((ORIGINAL/"CANDIDATE.md").read_bytes())
    else:
        (folder/"author_replay").mkdir(exist_ok=True)
        (folder/"author_replay"/"CANDIDATE.md").write_bytes((ORIGINAL/"CANDIDATE.md").read_bytes())
    args=[PYTHON,"-E","-S","-B","-P",str(folder/Path(code_path).name)]
    start=datetime.now(timezone.utc).isoformat()
    child=subprocess.Popen(args,cwd=folder,env=ENV,stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    (folder/"stdout.txt").write_bytes(out);(folder/"stderr.txt").write_bytes(err)
    if child.returncode or err:
        raise RuntimeError("Original comparison execution failed")
    result=(folder/result_name).read_bytes()
    expected=(ORIGINAL/expected_path).read_bytes()
    if result!=expected:
        raise RuntimeError("Original normal receipt did not reproduce byte for byte")
    record={"label":label,"pid":child.pid,"returncode":child.returncode,"reaped":True,
            "started_utc":start,"completed_utc":datetime.now(timezone.utc).isoformat(),
            "args":args,"stdout_bytes":len(out),"stdout_sha256":hashlib.sha256(out).hexdigest(),
            "stderr_bytes":len(err),"stderr_sha256":hashlib.sha256(err).hexdigest(),
            "reproduced_result_bytes":len(result),"reproduced_result_sha256":hashlib.sha256(result).hexdigest(),
            "exact_original_result_match":True,"normal_assertions":json.loads(result)["assertions"]}
    records.append(record)
for name,pin in pins.items():
    body=(ORIGINAL/name).read_bytes()
    if len(body)!=pin["bytes"] or hashlib.sha256(body).hexdigest()!=pin["sha256"]:
        raise RuntimeError("Original changed while reproducing")
receipt={"status":"PASS","comparison_utc":datetime.now(timezone.utc).isoformat(),
         "input_pins":pins,"children":records,"originals_unchanged":True,
         "limitations":"Original checkers use assert and were reproduced only in normal mode. Our own explicit exception guards also passed under -O. No original optimized-run validity claim."}
(HERE/"ORIGINAL_COMPARISON_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":"PASS","originals_unchanged":True,"children":[{"pid":r["pid"],"assertions":r["normal_assertions"],"byte_identical":r["exact_original_result_match"]} for r in records]}))
