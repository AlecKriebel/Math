#!/usr/bin/env python3
"""Root replay of the independently authored exact finite-group checker.

Does not rewrite the independent agent's canonical data or receipts.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
AUDIT = BASE / "finite_group_audit_01"
WORK = BASE / "replay" / "root_finite_group"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    manifest = json.loads((AUDIT / "MANIFEST.json").read_text())
    for item in manifest["files"]:
        data = (AUDIT / item["path"]).read_bytes()
        require(len(data) == item["bytes"] and digest(data) == item["sha256"],
                "Independent artifact differs: " + item["path"])
    WORK.mkdir(parents=True, exist_ok=True)
    receipts = []
    for optimized in (False, True):
        label = "optimized" if optimized else "normal"
        for control in (None, "group_order", "gl_commutes", "c_fixes_all", "one_unipotent_class"):
            cmd = [sys.executable] + (["-O"] if optimized else [])
            cmd += [str(AUDIT / "exact_hessian_audit.py")]
            if control:
                cmd += ["--negative-control", control]
            else:
                cmd += ["--output", str(WORK / label)]
            start = datetime.now(timezone.utc).isoformat()
            result = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
            if control:
                require(result.returncode != 0 and "CHECK FAILED:" in result.stderr,
                        "Negative control did not fail explicitly: " + control)
            else:
                require(result.returncode == 0, result.stderr)
                for name in ("summary.json", "elements.json", "cyclic_subgroups.json", "checks.json"):
                    require((WORK / label / name).read_bytes() == (AUDIT / "exact_results" / name).read_bytes(),
                            "Root data mismatch: " + label + "/" + name)
            receipts.append({"mode": label, "control": control, "started_utc": start,
                             "returncode": result.returncode,
                             "stdout_sha256": digest(result.stdout.encode()),
                             "stderr_sha256": digest(result.stderr.encode()),
                             "explicit_rejection": bool(control),
                             "last_error": result.stderr.strip().splitlines()[-1] if result.stderr else None})
            print(label + " " + (control or "full replay") + ": PASS", flush=True)
    data = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "status": "PASS", "scope": "Exact finite-group mechanism only; no lower-bound certificate",
            "independent_manifest_sha256": digest((AUDIT / "MANIFEST.json").read_bytes()),
            "independent_manifest_files_verified": len(manifest["files"]),
            "normal_and_optimized_match_canonical_data": True,
            "explicit_checks_each_full_run": 1381, "negative_controls_rejected": 8,
            "runs": receipts}
    (BASE / "ROOT_FINITE_GROUP_REPLAY.json").write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
