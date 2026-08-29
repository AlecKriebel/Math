#!/usr/bin/env python3
"""Focused control and mutation for sealed JSON output modes."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile


sys.dont_write_bytecode = True


class ModeFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ModeFailure(message)


HERE = Path(__file__).resolve().parent
PACKAGED_PROOF = HERE.parent / "proof_package"
DEFAULT_PROJECT = PACKAGED_PROOF if PACKAGED_PROOF.is_dir() else HERE.parents[1]


def load_module(name: str, path: Path, search_path: Path | None = None):
    if search_path is not None:
        sys.path.insert(0, str(search_path))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        require(spec is not None and spec.loader is not None,
                ("cannot load mode-preservation target", path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if search_path is not None:
            sys.path.pop(0)


def atomic_writer_control(project: Path) -> dict[str, object]:
    targets = [
        ("primary", project / "reproducibility/verify_primary.py",
         project / "reproducibility"),
        ("cut_topology", project /
         "cut_recovery/strong_crossbridge/topology_regeneration/verify_cut_topology_regeneration.py",
         project / "cut_recovery/strong_crossbridge/topology_regeneration"),
        ("strong_cut_transfer", project /
         "reproducibility/strong_cut_transfer_gate.py",
         project / "reproducibility"),
    ]
    observed: dict[str, str] = {}
    with tempfile.TemporaryDirectory(
        prefix=".k3p-atomic-mode-control-", dir=project / "reproducibility",
    ) as directory:
        root = Path(directory)
        for name, source, search_path in targets:
            module = load_module(f"k3p_mode_control_{name}", source, search_path)
            for state in ("existing", "new"):
                path = root / f"{name}-{state}.json"
                if state == "existing":
                    path.write_text("{}\n", encoding="utf-8")
                    path.chmod(0o644)
                module.atomic_json(path, {"writer": name, "state": state})
                mode = stat.S_IMODE(path.stat().st_mode)
                require(mode == 0o644,
                        ("atomic JSON writer changed canonical mode", name, state,
                         format(mode, "04o")))
                observed[f"{name}_{state}"] = format(mode, "04o")
    return {"name": "public_atomic_json_mode_preservation",
            "status": "PASS", "modes": observed}


def primary_report_restore_control(project: Path) -> dict[str, object]:
    runner = load_module(
        "k3p_mode_control_runner",
        HERE / "run_active_verifiers.py",
    )
    canonical = {
        "project_root": "/canonical/project",
        "python": {"executable": "/canonical/python"},
        "bound_path": "/canonical/project/evidence.json",
    }
    regenerated = {
        "project_root": "/copied/workspace",
        "python": {"executable": "/copied/venv/python"},
        "bound_path": "/copied/workspace/evidence.json",
    }
    canonical_bytes = (json.dumps(canonical, sort_keys=True) + "\n").encode()
    regenerated_bytes = (json.dumps(regenerated, sort_keys=True) + "\n").encode()
    with tempfile.TemporaryDirectory(prefix="k3p-primary-mode-restore-") as directory:
        package = Path(directory)
        workspace = package / "workspace"
        phase = package / "phase"
        path = workspace / "reproducibility/primary_gate_report.json"
        path.parent.mkdir(parents=True)
        phase.mkdir()
        path.write_bytes(regenerated_bytes)
        path.chmod(0o600)
        record = runner.preserve_and_restore_primary_report(
            workspace=workspace, phase_root=phase, package_root=package,
            canonical_bytes=canonical_bytes, canonical_mode=0o644,
            label="location_dependent_primary_report",
        )
        evidence = package / record["path"]
        require(path.read_bytes() == canonical_bytes and
                stat.S_IMODE(path.stat().st_mode) == 0o644,
                "primary report canonical bytes and mode were not restored")
        require(evidence.read_bytes() == regenerated_bytes and
                stat.S_IMODE(evidence.stat().st_mode) == 0o600,
                "regenerated primary report bytes and mode were not preserved")
    return {"name": "location_dependent_primary_report_mode_restore",
            "status": "PASS", "restored_mode": "0644",
            "preserved_regenerated_mode": "0600"}


def unsafe_replacement_mutation() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="k3p-unsafe-atomic-mode-") as directory:
        root = Path(directory)
        path = root / "sealed.json"
        path.write_text("{}\n", encoding="utf-8")
        path.chmod(0o644)
        before = stat.S_IMODE(path.stat().st_mode)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=root, delete=False,
        ) as handle:
            handle.write('{"mutated": true}\n')
            temporary = Path(handle.name)
        os.replace(temporary, path)
        after = stat.S_IMODE(path.stat().st_mode)
        require((before, after) == (0o644, 0o600),
                ("unsafe atomic replacement fixture", before, after))
        return {"name": "unsafe_atomic_mode_replacement",
                "status": "REJECTED", "before": "0644", "after": "0600",
                "detected_failure": "atomic output mode drift"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT)
    args = parser.parse_args(argv)
    project = args.project_root.resolve()
    try:
        controls = [
            atomic_writer_control(project),
            primary_report_restore_control(project),
        ]
        mutation = unsafe_replacement_mutation()
        report = {
            "schema": "k3p-output-mode-preservation-control-v1",
            "status": "PASS",
            "controls": controls,
            "mutation": mutation,
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        print("K3P_OUTPUT_MODE_PRESERVATION_PASS")
        return 0
    except (ModeFailure, OSError, ValueError, TypeError) as error:
        print(f"K3P_OUTPUT_MODE_PRESERVATION_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
