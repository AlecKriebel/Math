#!/usr/bin/env python3
"""Capture the locked-file drift caused by an in-place release mutation run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path


RELATIVE = "work/quartet_separation_closure/quartet_semantics_mutation_certificate.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    path = args.project.resolve() / RELATIVE
    current_bytes = path.read_bytes()
    with zipfile.ZipFile(args.archive) as archive:
        sealed_bytes = archive.read("k2p_principal_d_plus_submission_referee/" + RELATIVE)
    current = json.loads(current_bytes)
    sealed = json.loads(sealed_bytes)
    differing_cases = []
    for before, after in zip(sealed["cases"], current["cases"]):
        if before != after:
            differing_cases.append(
                {
                    "case": before["case"],
                    "sealed_stdout_sha256": before["stdout_sha256"],
                    "current_stdout_sha256": after["stdout_sha256"],
                }
            )
    stat = os.stat(path)
    result = {
        "schema": "independent-k2p-locked-file-drift-capture-v1",
        "status": "DRIFT_REPRODUCED" if current_bytes != sealed_bytes else "NO_DRIFT",
        "path": str(path),
        "relative_path": RELATIVE,
        "bytes": len(current_bytes),
        "sealed_sha256": sha(sealed_bytes),
        "current_sha256": sha(current_bytes),
        "sealed_payload_sha256": sealed["payload_sha256"],
        "current_payload_sha256": current["payload_sha256"],
        "differing_case_count": len(differing_cases),
        "differing_cases": differing_cases,
        "mtime_epoch": stat.st_mtime,
        "mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "sealed_sha256", "current_sha256", "differing_case_count")}, sort_keys=True))
    return 0 if result["status"] == "DRIFT_REPRODUCED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
