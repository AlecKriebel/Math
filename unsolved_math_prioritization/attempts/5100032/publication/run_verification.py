#!/usr/bin/env python3
"""Run normal/-O exact checks and mandatory failed subprocess controls locally."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def pin(body):
    return {"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()}


def main():
    operations, results = [], []
    for optimized in (False, True):
        prefix = [sys.executable]+(["-O"] if optimized else [])+[str(HERE/"verify.py")]
        for fault in (None,"coefficient","height","sign","proof-binding"):
            argv = prefix+(["--invalid-control",fault] if fault else [])
            started = now()
            process = subprocess.Popen(argv,cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout,stderr = process.communicate()
            receipt = {"argv":argv,"cwd":str(HERE),"child_PID":process.pid,
                       "UTC_start":started,"UTC_end":now(),"exit_code":process.returncode,
                       "stdout":pin(stdout),"stderr":pin(stderr),"invalid_control":fault,
                       "optimization":optimized}
            if fault:
                if process.returncode != 2:
                    raise RuntimeError("Required negative subprocess control did not fail: "+str(receipt))
                rejection = json.loads(stderr)
                expected = {"coefficient":"coboundary: correct fixed coefficient",
                            "height":"norm: independent solver and focal height",
                            "sign":"norm: positive ordinary root",
                            "proof-binding":"binding: manuscript SHA256"}[fault]
                if stdout or rejection.get("reason") != expected:
                    raise RuntimeError("Incorrect negative-control rejection: "+str(receipt))
                receipt["verified_rejection"] = rejection
            else:
                if process.returncode or stderr:
                    raise RuntimeError("Positive verification failed: "+str(receipt))
                result = json.loads(stdout)
                destination = "verification_optimized.json" if optimized else "verification_normal.json"
                (HERE/destination).write_bytes(stdout)
                receipt["stdout"]["path"] = destination
                results.append(result)
            operations.append(receipt)
    keys = ["proof_sha256","directed_chord_cases","paired_reversal_cases",
            "horizontal_directed_chords","coefficient_sign_cases","explicit_passing_guard_checks",
            "closed_cycle_controls","mandatory_invalid_controls"]
    if any(results[0][k] != results[1][k] for k in keys):
        raise RuntimeError("Normal and optimized verification summaries differ")
    envelope = {"schema":"focal-antipedal-execution-envelope/v1","actual_runner_PID":os.getpid(),
                "UTC_completed":now(),"operations":operations,"normal_optimized_agree":True,
                "positive_runs":2,"required_failed_subprocess_controls":8}
    (HERE/"execution_envelope.json").write_text(json.dumps(envelope,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"passed","positive_runs":2,"required_failed_controls":8,
                      "directed_chord_cases_per_run":results[0]["directed_chord_cases"],
                      "passing_guard_checks_per_run":results[0]["explicit_passing_guard_checks"]},indent=2))


if __name__ == "__main__":
    main()
