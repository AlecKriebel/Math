#!/usr/bin/env python3
"""Replay the historical runtime comparator; never infer a current-pin bound.

This faithfully persists the previously ephemeral measurement.  Scope consists
of regular files recursively below .lake/build/{lib/lean,ir}/Mathlib and root
files matching Mathlib.* in those same two directories.  Root Mathlib.olean is
therefore included.  Dependency libraries, binaries, native objects, sources,
and compressed cache archives are excluded.  No input file is modified.
"""

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess


DEFAULT_ROOT = Path(
    "/Users/alec/Documents/Math/universal_simultaneous_amplification/"
    "lean_formalization/.lake/packages/mathlib"
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mathlib-root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.mathlib_root.absolute()
    files = []
    root_files = []
    for directory in (root / ".lake/build/lib/lean", root / ".lake/build/ir"):
        files += [f for f in (directory / "Mathlib").rglob("*") if f.is_file()]
        selected_root_files = [f for f in directory.glob("Mathlib.*") if f.is_file()]
        files += selected_root_files
        root_files += selected_root_files
    if len(files) != len(set(files)):
        raise RuntimeError("Artifact scope selected a file twice")

    inventory = sorted(
        (str(f.relative_to(root)), f.stat().st_size, f.stat().st_blocks * 512)
        for f in files
    )
    oleans = [record for record in inventory if Path(record[0]).suffix == ".olean"]
    inventory_digest = hashlib.sha256(
        json.dumps(inventory, separators=(",", ":")).encode()
    ).hexdigest()
    result = {
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "method": "Faithfully regenerated replay of the original ephemeral comparator measurement",
        "measurement_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "path": str(root),
        "canonical_path_after_symlink_resolution": str(root.resolve()),
        "head": subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip(),
        "lean_toolchain": (root / "lean-toolchain").read_text().strip(),
        "scope": {
            "recursive_subdirectories": [".lake/build/lib/lean/Mathlib", ".lake/build/ir/Mathlib"],
            "root_file_globs": [".lake/build/lib/lean/Mathlib.*", ".lake/build/ir/Mathlib.*"],
            "includes_root_Mathlib_olean": True,
            "excludes": ["dependencies", "binaries", "native objects", "sources", "compressed cache archives"],
        },
        "selected_root_files": [
            {
                "path": str(f.relative_to(root)),
                "logical_bytes": f.stat().st_size,
                "allocated_bytes": f.stat().st_blocks * 512,
            }
            for f in sorted(root_files)
        ],
        "artifact_inventory_sha256": inventory_digest,
        "all_mathlib_lib_and_ir_artifact_count": len(inventory),
        "mathlib_olean_count": len(oleans),
        "mathlib_olean_logical_bytes": sum(r[1] for r in oleans),
        "mathlib_olean_allocated_bytes": sum(r[2] for r in oleans),
        "all_mathlib_lib_and_ir_artifact_logical_bytes": sum(r[1] for r in inventory),
        "all_mathlib_lib_and_ir_artifact_allocated_bytes": sum(r[2] for r in inventory),
        "current_pin_reusable": False,
        "interpretation": "Older-version comparator only; not a measured current-pin minimum or estimate.",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
