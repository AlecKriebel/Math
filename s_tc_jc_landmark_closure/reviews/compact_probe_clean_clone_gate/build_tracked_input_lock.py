#!/usr/bin/env python3
"""Generate the exact git-tracked input closure of the compact-only gate."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
REPO = PROJECT.parent
sys.path.insert(0, str(HERE))
import semantic_gate as gate  # noqa: E402


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()


def main():
    paths = {
        PROJECT / "primary" / "seventh_invariant.json",
        PROJECT / "reviews" / "compact_probe_format" /
            "final_n4_cleanroom" / "engine.py",
        PROJECT / "reviews" / "compact_probe_format" /
            "final_n3_cleanroom" / "engine_n3.py",
    }
    for family in gate.FAMILIES.values():
        for shard in range(4):
            summary_path = gate.CERT / family.summary_pattern.format(shard=shard)
            paths.add(summary_path)
            summary = json.loads(summary_path.read_text())
            paths.add(gate.resolve(summary["bit_cache"]["path"], summary_path))
            for metadata in summary["streams"].values():
                paths.add(gate.resolve(metadata["path"], summary_path))
            for base in summary["base_summaries"]:
                base_path = gate.resolve(base, summary_path)
                paths.add(base_path)
                base_summary = json.loads(base_path.read_text())
                for run in base_summary["runs"]:
                    cover = run["hard_cover"]
                    paths.add(gate.resolve(cover["relation_path"], base_path))
                    paths.add(gate.resolve(cover["graph_library_path"], base_path))

    rows = []
    for path in sorted(paths):
        relative = path.resolve().relative_to(REPO.resolve())
        relative_text = str(relative)
        git("ls-files", "--error-unmatch", relative_text)
        rows.append({
            "path": relative_text,
            "sha256": gate.file_sha256(path),
            "bytes": path.stat().st_size,
        })
    payload = {
        "schema": "compact-probe-clean-clone-input-lock-v1",
        "status": "VERIFIED",
        "git_commit": git("rev-parse", "HEAD"),
        "proof_method": (
            "Every external runtime input was resolved from the eight compact "
            "summaries and two hard-cover summaries, then accepted only if "
            "git ls-files --error-unmatch succeeded.  Exact bytes are locked "
            "below and are rechecked without git in an archive checkout.  "
            "The gate's own files are covered separately by MANIFEST.sha256 "
            "and by their presence in the committed package."),
        "input_count": len(rows),
        "inputs": rows,
        "forbidden_verbose_probe_extension_inputs": [],
    }
    output = HERE / "TRACKED_INPUTS.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": "VERIFIED", "inputs": len(rows),
                      "output": str(output.relative_to(PROJECT)),
                      "sha256": gate.file_sha256(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
