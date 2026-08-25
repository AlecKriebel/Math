#!/usr/bin/env python3
"""Audit the current package's supplemental dependency and tool binding."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import subprocess
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assigned_literal(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"assignment not found: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--git-audit", type=Path, required=True)
    parser.add_argument("--interpreter", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    builder_rel = "proof_compression_submission/crosswalk/build_revised_referee_bundle.py"
    manifest_rel = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
    builder = project / builder_rel
    manifest = json.loads((project / manifest_rel).read_text(encoding="utf-8"))
    inner = json.loads((project / "output/referee/REFEREE_BUNDLE_CONTENTS.json").read_text(encoding="utf-8"))
    code_dependencies = sorted(assigned_literal(builder, "SUPPLEMENTAL_EXECUTION_DEPENDENCIES"))
    policy_dependencies = manifest["submission_sources"]["policy"]["supplemental_execution_dependencies"]
    rows = []
    for relative in code_dependencies:
        path = project / relative
        declared = manifest["submission_sources"]["files"].get(relative)
        rows.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha(path),
                "outer_manifest_row": declared,
                "outer_manifest_exact": declared == {"bytes": path.stat().st_size, "sha256": sha(path)},
                "inside_older_inner_content_ledger": relative in inner["files"],
            }
        )

    git_audit = json.loads(args.git_audit.read_text(encoding="utf-8"))
    final_tag = next(
        row for row in git_audit["comparisons"] if row["requested_revision"] == "k2p-same-biorxiv-v1.0.0"
    )
    replay_commit = next(
        row for row in git_audit["comparisons"] if row["requested_revision"] == "1877985d20132fb186d21a5985e8c5f760a656af"
    )
    replay_mismatches = {
        row["path"]: {key: row[key] for key in ("commit_bytes", "commit_sha256", "package_bytes", "package_sha256")}
        for row in replay_commit["mismatches"]
        if row["path"] in code_dependencies
    }
    requirements = []
    for relative in (
        "work/final_theorem_release/requirements.txt",
        "package/referee/k2p_offline_sweep_portable/requirements.txt",
    ):
        path = project / relative
        requirements.append(
            {"path": relative, "bytes": path.stat().st_size, "sha256": sha(path), "text": path.read_text(encoding="utf-8").splitlines()}
        )
    version = subprocess.run(
        [str(args.interpreter.absolute()), "-c", "import json,networkx,sympy,sys; print(json.dumps({'python':platform.python_version() if False else sys.version.split()[0],'networkx':networkx.__version__,'sympy':sympy.__version__},sort_keys=True))"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
    )
    tectonic = subprocess.run(["tectonic", "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True, text=True)
    legacy_binding_paths = [str(path.relative_to(project)) for path in project.rglob("SUBMISSION_BINDING.json")]
    passes = (
        len(code_dependencies) == 3
        and code_dependencies == policy_dependencies
        and all(row["outer_manifest_exact"] for row in rows)
        and not any(row["inside_older_inner_content_ledger"] for row in rows)
        and final_tag["exact_package_match"]
        and len(requirements) == 2
        and requirements[0]["sha256"] == requirements[1]["sha256"]
        and not legacy_binding_paths
    )
    result = {
        "schema": "independent-k2p-dependency-binding-audit-v1",
        "status": "PASS_CURRENT_BINDING" if passes else "FAIL",
        "binding_schema": manifest["schema"],
        "legacy_submission_binding_paths": legacy_binding_paths,
        "note": (
            "This revised package has no SUBMISSION_BINDING.json and declares three, not five, supplemental execution dependencies. "
            "The five TeX/Bib PDF sources are a separate source-set contract."
        ),
        "builder_path": builder_rel,
        "builder_sha256": sha(builder),
        "supplemental_execution_dependencies": rows,
        "all_three_absent_from_older_inner_content_ledger": not any(row["inside_older_inner_content_ledger"] for row in rows),
        "replay_commit": replay_commit["resolved_commit"],
        "replay_commit_dependency_differences": replay_mismatches,
        "final_tag": {
            "name": final_tag["requested_revision"],
            "resolved_commit": final_tag["resolved_commit"],
            "exact_480_file_package_match": final_tag["exact_package_match"],
        },
        "requirements": requirements,
        "runtime": json.loads(version.stdout),
        "tectonic": tectonic.stdout.strip(),
        "host": {"platform": platform.platform(), "machine": platform.machine()},
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "supplemental_dependency_count": len(rows), "final_tag": result["final_tag"]}, sort_keys=True))
    return 0 if passes else 1


if __name__ == "__main__":
    raise SystemExit(main())
