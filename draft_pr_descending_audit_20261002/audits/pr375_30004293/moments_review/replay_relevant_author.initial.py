#!/usr/bin/env python3
"""Post-verdict corroboration only; replay frozen author's relevant finite code."""
import datetime, hashlib, json, pathlib, shutil, subprocess, sys

BASE=pathlib.Path(__file__).resolve().parent
TARGET=BASE.parent/"snapshot"/"unsolved_math_prioritization"/"attempts"/"30004293"
PRIVATE=BASE/"tmp"/"author_replay"

def digest(path):
    data=path.read_bytes()
    return {"path":str(path.relative_to(TARGET)),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}

def main():
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    PRIVATE.mkdir(parents=True,exist_ok=True)
    source=TARGET/"verify_turn5.py"
    copy=PRIVATE/"verify_turn5.py"
    shutil.copyfile(source,copy)
    cmd=[sys.executable,str(copy)]
    result=subprocess.run(cmd,cwd=PRIVATE,capture_output=True,text=True)
    (BASE/"author_turn5.stdout").write_text(result.stdout)
    (BASE/"author_turn5.stderr").write_text(result.stderr)
    observed=json.loads(result.stdout) if result.returncode==0 else None
    expected=json.loads((TARGET/"TURN_5_CHECKS.json").read_text())
    target_binding=[digest(p) for p in sorted(TARGET.rglob("*")) if p.is_file()]
    out={"started_utc":start,"ended_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"purpose":"Post-independent-verdict corroboration; finite replay is not mathematical proof.","command":cmd,"cwd":str(PRIVATE),"returncode":result.returncode,"receipt_equal":observed==expected,"observed":observed,"recorded":expected,"script_identity":digest(source),"frozen_commit":"36c29bb039471f132889d577c9322d78925b62dd","target_file_count":len(target_binding),"target_binding":target_binding}
    (BASE/"AUTHOR_REPLAY_CORROBORATION.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("returncode","receipt_equal","observed","target_file_count")},indent=2))
    if result.returncode or observed!=expected or len(target_binding)!=54:
        raise RuntimeError("Author replay receipt or frozen binding count mismatch")

if __name__=="__main__":
    main()
