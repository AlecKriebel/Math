#!/usr/bin/env python3
"""Fail-closed build, statement, and axiom audit for this Lean checkpoint.

This program is an audit orchestrator, not a mathematical certificate checker.
The mathematical checking is performed by Lean's kernel.  An input targets
file lists one fully qualified principal theorem name per line; blank lines
and lines starting with # are ignored.  Every target is type-checked and its
transitive axiom dependencies are queried in Lean.  The target list must be
reviewed against the manuscript correspondence table independently.

Usage: python3 tools/audit.py --targets principal_theorems.txt [--clean]
--clean removes ONLY this project's .lake/build, never dependency caches.
Do not invoke --clean concurrently with another build of this project.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.19.0"
EXPECTED_MATHLIB = "c44e0c8ee63ca166450922a373c7409c5d26b00b"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_comments_and_strings(source: str) -> str:
    """Preserve lines while removing nested Lean comments and string literals."""
    result = []
    i = 0
    depth = 0
    in_string = False
    while i < len(source):
        if depth:
            if source.startswith("/-", i):
                depth += 1
                result.extend("  ")
                i += 2
            elif source.startswith("-/", i):
                depth -= 1
                result.extend("  ")
                i += 2
            else:
                result.append("\n" if source[i] == "\n" else " ")
                i += 1
        elif in_string:
            if source[i] == "\\":
                result.extend("  ")
                i += 2
            elif source[i] == '"':
                result.append(" ")
                i += 1
                in_string = False
            else:
                result.append("\n" if source[i] == "\n" else " ")
                i += 1
        elif source.startswith("/-", i):
            depth = 1
            result.extend("  ")
            i += 2
        elif source.startswith("--", i):
            end = source.find("\n", i)
            end = len(source) if end < 0 else end
            result.extend(" " * (end - i))
            i = end
        elif source[i] == '"':
            result.append(" ")
            i += 1
            in_string = True
        else:
            result.append(source[i])
            i += 1
    if depth or in_string:
        raise ValueError("Unterminated source comment or string")
    return "".join(result)


def source_audit(paths: list[Path]) -> list[dict]:
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|bv_decide|trustCompiler|"
        r"ofReduceBool|implemented_by|extern|unsafe)\b|"
        r"^\s*(?:axiom|constant)\s|debug\.skipKernelTC",
        re.M,
    )
    found = []
    for path in paths:
        clean = strip_comments_and_strings(path.read_text())
        for match in forbidden.finditer(clean):
            found.append({
                "file": str(path.relative_to(ROOT)),
                "line": clean[:match.start()].count("\n") + 1,
                "token": match.group().strip(),
            })
    return found


def inspect_axioms(output: str, targets: list[str]) -> list[dict]:
    results = []
    for target in targets:
        pat = re.compile(
            r"^\s*'?" + re.escape(target)
            + r"'?\s+(?:depends on axioms:\s*\[([^\]]*)\]|"
              r"does not depend on any axioms)", re.M,
        )
        matches = list(pat.finditer(output))
        if len(matches) != 1:
            raise ValueError(f"Expected one axiom report for {target}, got {len(matches)}")
        raw = matches[0].group(1)
        axioms = set() if raw is None else {x.strip() for x in raw.split(",") if x.strip()}
        if unexpected := axioms - ALLOWED_AXIOMS:
            raise ValueError(f"{target} has forbidden dependencies: {sorted(unexpected)}")
        results.append({"theorem": target, "axioms": sorted(axioms)})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--import-module", default="SymmetricSector")
    args = parser.parse_args()
    now = datetime.datetime.now(datetime.timezone.utc)
    run_id = now.strftime("%Y%m%dT%H%M%S.%fZ")
    dest = ROOT / "reports" / "audit" / run_id
    dest.mkdir(parents=True)
    report = {
        "run_id": run_id,
        "started_utc": now.isoformat(),
        "status": "in_progress",
        "lean_kernel_checked": False,
        "clean_project_build": args.clean,
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "commands": [],
        "scope_note": "Only listed theorem dependencies are audited. Interpretation and target coverage require independent human/agent review. Dependency build caches and the Lean kernel binary remain in the ordinary software trust boundary.",
    }

    def write_report() -> None:
        (dest / "report.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(command: list[str], label: str) -> str:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        output = proc.stdout + proc.stderr
        log = dest / (label + ".log")
        log.write_text(output)
        report["commands"].append({
            "argv": command, "exit_code": proc.returncode,
            "log": str(log.relative_to(ROOT)), "log_sha256": sha256(log),
        })
        write_report()
        if proc.returncode:
            raise RuntimeError(f"{label} failed with exit {proc.returncode}; see {log}")
        if re.search(r"\bdeclaration uses ['\"]sorry['\"]|\bsorryAx\b|\bPANIC\b|(?:^|\n).*\berror:", output):
            raise RuntimeError(f"{label} produced a forbidden diagnostic; see {log}")
        return output

    try:
        target_path = args.targets if args.targets.is_absolute() else ROOT / args.targets
        targets = [line.strip() for line in target_path.read_text().splitlines()
                   if line.strip() and not line.lstrip().startswith("#")]
        if not targets or len(set(targets)) != len(targets):
            raise ValueError("Targets must be nonempty and distinct")
        if any(not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*", t) for t in targets):
            raise ValueError("Unsupported theorem name syntax in audit targets")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", args.import_module):
            raise ValueError("Invalid import module")
        sources = sorted([ROOT / "SymmetricSector.lean"] + list((ROOT / "SymmetricSector").rglob("*.lean")))
        sources = [path for path in sources if path.is_file()]
        if not sources:
            raise ValueError("No production Lean sources exist")
        report["source_sha256"] = {str(path.relative_to(ROOT)): sha256(path) for path in sources}
        report["targets"] = targets
        report["targets_sha256"] = sha256(target_path)
        report["source_findings"] = source_audit(sources)
        if report["source_findings"]:
            raise ValueError("Forbidden source constructs found")
        toolchain = (ROOT / "lean-toolchain").read_text().strip()
        if toolchain != EXPECTED_TOOLCHAIN:
            raise ValueError(f"Unexpected toolchain: {toolchain}")
        manifest = json.loads((ROOT / "lake-manifest.json").read_text())
        mathlibs = [p for p in manifest["packages"] if p["name"] == "mathlib"]
        if len(mathlibs) != 1 or mathlibs[0].get("rev") != EXPECTED_MATHLIB:
            raise ValueError("Mathlib manifest revision differs from required pin")
        report["toolchain"] = toolchain
        report["mathlib_rev"] = EXPECTED_MATHLIB
        report["configuration_sha256"] = {
            name: sha256(ROOT / name)
            for name in ("lean-toolchain", "lakefile.toml", "lakefile.lean", "lake-manifest.json")
            if (ROOT / name).is_file()
        }
        version = run(["lake", "env", "lean", "--version"], "lean-version")
        if not re.search(r"\bLean \(version 4\.19\.0(?:,|\))|\bLean version 4\.19\.0(?:,|\b)", version):
            raise ValueError("Executed Lean binary reports an unexpected version")
        checked_out_rev = run(
            ["git", "-C", str(ROOT / ".lake" / "packages" / "mathlib"), "rev-parse", "HEAD"],
            "mathlib-checkout-revision",
        ).strip()
        if checked_out_rev != EXPECTED_MATHLIB:
            raise ValueError("Mathlib checkout HEAD differs from manifest pin")
        if args.clean:
            build = ROOT / ".lake" / "build"
            if build.is_symlink():
                raise ValueError("Refusing to delete symlinked project build directory")
            if build.exists():
                shutil.rmtree(build)
        run(["lake", "build"], "build")
        query = dest / "Audit.lean"
        query.write_text("import " + args.import_module + "\n"
                         + "set_option pp.width 200\n"
                         + "\n".join(f"#check {t}\n#print axioms {t}" for t in targets) + "\n")
        audit_output = run(["lake", "env", "lean", str(query)], "axioms-and-statements")
        report["theorems"] = inspect_axioms(audit_output, targets)
        changed = [str(p.relative_to(ROOT)) for p in sources
                   if sha256(p) != report["source_sha256"][str(p.relative_to(ROOT))]]
        if changed:
            raise ValueError(f"Production sources changed during audit: {changed}")
        report["status"] = "passed"
        report["lean_kernel_checked"] = True
        write_report()
        print(f"PASS: {len(targets)} theorem dependencies; standard axioms only. Report: {dest / 'report.json'}")
        return 0
    except Exception as exc:
        report["status"] = "failed"
        report["error"] = str(exc)
        write_report()
        print(f"FAIL: {exc}. Report: {dest / 'report.json'}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
