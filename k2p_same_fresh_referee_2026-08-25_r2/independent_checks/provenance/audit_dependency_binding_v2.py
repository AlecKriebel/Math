#!/usr/bin/env python3
"""Independent static/runtime dependency-binding audit for the new package."""

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


def literal_assignment(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise RuntimeError(f"assignment not found: {name}")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--git-audit", required=True, type=Path)
    parser.add_argument("--interpreter", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    builder_rel = "proof_compression_submission/crosswalk/build_revised_referee_bundle.py"
    manifest_rel = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
    builder = project / builder_rel
    manifest = json.loads((project / manifest_rel).read_text(encoding="utf-8"))
    portable = json.loads((project / "output/referee/REFEREE_BUNDLE_CONTENTS.json").read_text(encoding="utf-8"))
    code_dependencies = sorted(literal_assignment(builder, "SUPPLEMENTAL_EXECUTION_DEPENDENCIES"))
    policy_dependencies = manifest["submission_sources"]["policy"]["supplemental_execution_dependencies"]
    dependency_rows = []
    for relative in code_dependencies:
        path = project / relative
        actual = {"bytes": path.stat().st_size, "sha256": sha(path)}
        declared = manifest["submission_sources"]["files"].get(relative)
        dependency_rows.append({
            "path": relative,
            **actual,
            "outer_manifest_row": declared,
            "outer_manifest_exact": declared == actual,
            "inside_frozen_content_ledger": relative in portable["files"],
        })

    git_audit = json.loads(args.git_audit.read_text(encoding="utf-8"))
    final_tag = next(row for row in git_audit["comparisons"]
                     if row["requested_revision"] == "k2p-same-biorxiv-v1.0.1")
    replay_commit = next(row for row in git_audit["comparisons"]
                         if row["requested_revision"] == "83821850e02bc6b6a0383dbc9d3d42ab24a261f5")
    replay_diffs = {
        row["path"]: {key: row[key] for key in (
            "commit_bytes", "commit_sha256", "package_bytes", "package_sha256"
        )}
        for row in replay_commit["mismatches"] if row["path"] in code_dependencies
    }

    requirements = []
    for relative in (
        "work/final_theorem_release/requirements.txt",
        "package/referee/k2p_offline_sweep_portable/requirements.txt",
    ):
        path = project / relative
        requirements.append({
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha(path),
            "lines": path.read_text(encoding="utf-8").splitlines(),
        })
    version = run([
        str(args.interpreter.absolute()), "-c",
        "import json,networkx,sympy,sys; print(json.dumps({"
        "'python':sys.version.split()[0],'networkx':networkx.__version__,"
        "'sympy':sympy.__version__},sort_keys=True))",
    ])
    tectonic = run(["tectonic", "--version"])
    legacy = sorted(str(path.relative_to(project))
                    for path in project.rglob("SUBMISSION_BINDING.json"))
    mapped_names = {
        "START_HERE.md", "setup_environment.sh", "verify_handoff.py",
        "test_handoff_mutations.py", "run_all_verifiers.py", "SUBMISSION_BINDING.json",
    }
    readme = (project / "output/referee/README.md").read_text(encoding="utf-8")
    all_mapped = all(name in readme for name in mapped_names)
    passes = (
        len(code_dependencies) == 3
        and code_dependencies == policy_dependencies
        and all(row["outer_manifest_exact"] for row in dependency_rows)
        and not any(row["inside_frozen_content_ledger"] for row in dependency_rows)
        and final_tag["exact_package_match"]
        and len(requirements) == 2
        and requirements[0]["sha256"] == requirements[1]["sha256"]
        and version.returncode == 0
        and json.loads(version.stdout) == {
            "networkx": "3.5", "python": "3.14.6", "sympy": "1.14.0"
        }
        and tectonic.returncode == 0
        and not legacy
        and all_mapped
    )
    result = {
        "schema": "independent-k2p-dependency-binding-audit-v2",
        "status": "PASS" if passes else "FAIL",
        "binding_schema": manifest["schema"],
        "builder_path": builder_rel,
        "builder_sha256": sha(builder),
        "supplemental_execution_dependencies": dependency_rows,
        "code_and_policy_dependencies_identical": code_dependencies == policy_dependencies,
        "all_supplemental_dependencies_outside_frozen_ledger":
            not any(row["inside_frozen_content_ledger"] for row in dependency_rows),
        "requirements": requirements,
        "qualified_runtime": json.loads(version.stdout) if version.returncode == 0 else None,
        "runtime_probe_returncode": version.returncode,
        "runtime_probe_stderr": version.stderr,
        "tectonic": tectonic.stdout.strip(),
        "tectonic_returncode": tectonic.returncode,
        "host": {"platform": platform.platform(), "machine": platform.machine()},
        "legacy_submission_binding_paths": legacy,
        "legacy_name_mapping_complete": all_mapped,
        "replay_commit": replay_commit["resolved_commit"],
        "replay_commit_dependency_differences": replay_diffs,
        "final_tag": {
            "name": final_tag["requested_revision"],
            "resolved_commit": final_tag["resolved_commit"],
            "exact_package_match": final_tag["exact_package_match"],
        },
        "classification": (
            "Dependency/Git/hash agreement is provenance evidence only; "
            "the interpreter probe is computational-environment evidence."
        ),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "dependency_count": len(dependency_rows),
                      "final_tag": result["final_tag"]}, sort_keys=True))
    return 0 if passes else 1


if __name__ == "__main__":
    raise SystemExit(main())
