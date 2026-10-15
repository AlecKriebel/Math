#!/usr/bin/env python3
"""Replay the selective-retry import-header count; this is not a Lean build.

The counting function below is faithfully regenerated from the ephemeral
Python command used for the original 8,529/8,530 count. Added preservation
metadata, hashes, and explicit missing-source checks do not change its parser.
Only this script's JSON result is written. Dependency sources are read-only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess


EXPECTED_PIN = "d13f23b723b8a846827a245b89c10fc7d3f11612"
DEFAULT_MATHLIB = Path(
    "/Users/alec/Documents/Math/openai_followon_bosonic_capacity/notes/"
    "formal_scope/pinned_build/.lake/packages/mathlib"
)


def header_imports(path):
    # This function preserves the original ephemeral counting implementation.
    deps = []
    depth = 0
    for raw in path.read_text().splitlines():
        # Strip nested and line comments only within the import header.
        out = []
        last = 0
        for m in re.finditer(r"/-|-/|--", raw):
            token = m[0]
            if token == "--" and depth == 0:
                out.append(raw[last:m.start()])
                last = len(raw)
                break
            if token == "/-":
                if depth == 0:
                    out.append(raw[last:m.start()])
                depth += 1
                last = m.end()
            elif token == "-/" and depth:
                depth -= 1
                last = m.end()
        if depth == 0:
            out.append(raw[last:])
        code = "".join(out).strip()
        if not code:
            continue
        if code == "module" or code.startswith("module "):
            continue
        m = re.match(r"(?:(?:public|private|meta)\s+)*import\s+(.+)$", code)
        if m:
            deps.extend(m[1].split())
            continue
        break
    return deps


def git_output(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "--no-optional-locks", "-C", str(root), *args], text=True
    ).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mathlib-dir", type=Path, default=DEFAULT_MATHLIB)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).with_suffix(".json"),
    )
    args = parser.parse_args()
    root = args.mathlib_dir.resolve()
    actual_pin = git_output(root, "rev-parse", "HEAD")
    if actual_pin != EXPECTED_PIN:
        raise SystemExit(f"Expected {EXPECTED_PIN}; found {actual_pin}")

    modules = {
        ".".join(p.relative_to(root).with_suffix("").parts): p
        for p in (root / "Mathlib").rglob("*.lean")
    }
    modules["Mathlib"] = root / "Mathlib.lean"
    if not modules["Mathlib"].is_file():
        raise SystemExit("Missing Mathlib.lean")

    # Canonical content fingerprint, without relying on absolute path names.
    source_manifest = [
        {
            "module": name,
            "relative_path": path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for name, path in sorted(modules.items())
    ]
    canonical_manifest = json.dumps(
        source_manifest, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")

    seen = set()
    outside = Counter()
    edges = 0
    stack = ["Mathlib"]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        for dependency in header_imports(modules[name]):
            edges += 1
            if dependency in modules:
                stack.append(dependency)
            else:
                outside[dependency] += 1

    direct = header_imports(modules["Mathlib"])
    direct_mathlib = [name for name in direct if name.startswith("Mathlib.")]
    missing = sorted(
        name for name in outside if name == "Mathlib" or name.startswith("Mathlib.")
    )
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "audit_kind": "source-only mathematical import-header closure replay",
        "preservation_status": "faithfully regenerated replay of ephemeral original parser",
        "original_run_saved": False,
        "mathlib_source_root": str(root),
        "expected_mathlib_pin": EXPECTED_PIN,
        "actual_mathlib_head": actual_pin,
        "tracked_mathlib_source_changes": git_output(
            root, "status", "--porcelain", "--untracked-files=no", "--",
            "Mathlib.lean", "Mathlib"
        ),
        "lean_toolchain": (root / "lean-toolchain").read_text().strip(),
        "mathlib_umbrella_sha256": hashlib.sha256(
            modules["Mathlib"].read_bytes()
        ).hexdigest(),
        "source_manifest_sha256": hashlib.sha256(canonical_manifest).hexdigest(),
        "source_manifest_digest_definition": (
            "SHA256 of UTF-8 json.dumps of the sorted list of records with module, "
            "relative_path and file sha256; sort_keys=True, separators=(',', ':')."
        ),
        "scope": (
            "Mathlib.lean and every Mathlib/**/*.lean source; excludes other "
            "packages, Archive, Counterexamples, compiler/toolchain modules and artifacts."
        ),
        "parser_mechanism": (
            "Read lines; remove nested block comments and line comments within the header; "
            "skip module declarations; recognize repeated public/private/meta qualifiers "
            "before import; split the import tail on whitespace; stop at the first "
            "nonblank non-module non-import header line."
        ),
        "parser_limitations": [
            "This is a lexical header parser, not Lean.parseImports or kernel checking.",
            "It assumes module names are on their import command's line.",
            "The original parser retains the import modifier 'all' as an extra non-Mathlib token; this cannot add a Mathlib source module to reachability.",
            "It does not infer a complete cache closure for dependency packages whose pinned sources are absent.",
        ],
        "direct_mathlib_umbrella_mathlib_imports": len(direct_mathlib),
        "unique_direct_mathlib_umbrella_mathlib_imports": len(set(direct_mathlib)),
        "mathlib_source_count_including_root": len(modules),
        "reachable_mathlib_count_including_root": len(seen),
        "import_header_tokens_traversed": edges,
        "unreachable_mathlib_source_modules": sorted(set(modules) - seen),
        "missing_mathlib_source_imports": missing,
        "source_coverage_complete": len(seen) == len(modules) and not missing,
        "current_pin_cache_bytes_measured": False,
        "kernel_build_performed": False,
        "download_performed": False,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
