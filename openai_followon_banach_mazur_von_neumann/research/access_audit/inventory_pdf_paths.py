#!/usr/bin/env python3
"""Regenerated, parameterized form of the 2026-10-07 local PDF inventory.

The original one-off script embedded two explicitly authorized research roots
and project-local ignored output paths. This version requires those arguments;
it otherwise preserves rg flags, case-insensitive PDF suffix glob, exclusions,
inventory order, per-root status, and counts. It has not rerun the original scan.
Use only roots the operator is authorized to inspect. Outputs are local derived
path metadata, not a publication supplement.
"""

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

EXCLUDED_GLOBS = [
    "!**/.git/**", "!**/node_modules/**", "!**/__pycache__/**",
    "!**/.cache/**", "!**/cache/**", "!**/build/**", "!**/_build/**",
    "!**/.build/**", "!**/build-*/**", "!**/dist/**", "!**/.venv/**",
    "!**/venv/**", "!**/target/**", "!**/tmp/**", "!**/temp/**",
    "!**/credentials/**", "!**/.credentials/**", "!**/secrets/**",
    "!**/.secrets/**", "!**/communications/**", "!**/email/**",
    "!**/emails/**", "!**/messages/**", "!**/browser-profiles/**",
    "!**/Browser Profiles/**",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", required=True,
                        help="Explicitly authorized research root; repeat for each root")
    parser.add_argument("--inventory-out", type=Path, required=True)
    parser.add_argument("--metadata-out", type=Path, required=True)
    args = parser.parse_args()
    records, pdfs = [], []
    for supplied_root in args.root:
        root = str(Path(supplied_root).resolve())
        command = ["rg", "--files", "--hidden", "--no-ignore", "-g", "*.[pP][dD][fF]"]
        for glob in EXCLUDED_GLOBS:
            command += ["-g", glob]
        command += [root]
        result = subprocess.run(command, text=True, capture_output=True)
        files = result.stdout.splitlines()
        pdfs += files
        records.append({
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "root": root,
            "method": "rg PDF filenames only; hidden and ignored files included, explicit generated/private-directory exclusions",
            "excluded_globs": EXCLUDED_GLOBS,
            "exit_code": result.returncode,
            "pdf_count": len(files),
            "stderr": result.stderr,
        })
    args.metadata_out.write_text(json.dumps(records, indent=2) + "\n")
    args.inventory_out.write_text(json.dumps(pdfs, indent=2) + "\n")
    print(json.dumps({"total_pdf_count": len(pdfs),
                      "per_root_counts": [r["pdf_count"] for r in records]}))


if __name__ == "__main__":
    main()
