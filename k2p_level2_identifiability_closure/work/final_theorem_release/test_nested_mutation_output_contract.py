#!/usr/bin/env python3
"""Output-safety regression for every nested mutation-report writer."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUNNERS = (
    {
        "name": "raw4_full_map",
        "path": PROJECT / "work/raw4_sign_reclassification/mutation_tests.py",
        "authoritative": PROJECT
        / "work/raw4_sign_reclassification/raw4_mutation_certificate.json",
        "marker": "RAW4_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "RAW4_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "theta2_full_map",
        "path": PROJECT / "work/theta2_sign_reclassification/mutation_tests.py",
        "authoritative": PROJECT
        / "work/theta2_sign_reclassification/theta2_mutation_certificate.json",
        "marker": "THETA2_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "THETA2_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "canonicalizer",
        "path": PROJECT
        / "work/canonicalizer_completeness/test_canonicalizer_mutations.py",
        "authoritative": PROJECT
        / "work/canonicalizer_completeness/"
        "canonicalizer_completeness_mutation_certificate.json",
        "marker": "CANONICALIZER_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_text",
        "data": "atomic-output\n",
        "optimized_marker": "CANONICALIZER_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "parameter_transport",
        "path": PROJECT
        / "work/canonicalizer_completeness/inheritance_transport/"
        "run_parameter_transport_mutations.py",
        "authoritative": PROJECT
        / "work/canonicalizer_completeness/inheritance_transport/"
        "parameter_transport_mutation_report.json",
        "marker": "PARAMETER_TRANSPORT_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "PARAMETER_TRANSPORT_MUTATION_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "restoration",
        "path": PROJECT
        / "work/restoration_sign_reclassification/"
        "mutate_corrected_restoration_forest.py",
        "authoritative": PROJECT
        / "work/restoration_sign_reclassification/"
        "corrected_restoration_mutation_certificate.json",
        "marker": "RESTORATION_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "probe",
        "path": PROJECT
        / "work/probe_coherence_corrected/run_probe_coherence_mutations.py",
        "authoritative": PROJECT
        / "work/probe_coherence_corrected/probe_coherence_mutation_certificate.json",
        "marker": "PROBE_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "PROBE_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "rank_upper",
        "path": PROJECT / "work/rank_upper_certificates/mutation_tests.py",
        "authoritative": PROJECT / "work/rank_upper_certificates/mutation_report.json",
        "marker": "K2P_RANK_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write",
        "data": b"atomic-output\n",
        "optimized_marker": "K2P_RANK_MUTATION_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "direct_closure",
        "path": PROJECT
        / "package/referee/k2p_offline_sweep_portable/"
        "test_direct_closure_release_mutations.py",
        "authoritative": PROJECT
        / "package/referee/k2p_offline_sweep_portable/"
        "direct_closure_mutation_report.json",
        "marker": "DIRECT_CLOSURE_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "DIRECT_CLOSURE_MUTATION_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "weak_sharpness",
        "path": PROJECT / "work/weak_sharpness_audit/test_mutations.py",
        "authoritative": PROJECT / "work/weak_sharpness_audit/mutation_report.json",
        "marker": "WEAK_SHARPNESS_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "WEAK_SHARPNESS_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN",
        "support_files": ("audit_weak_sharpness.py",),
    },
    {
        "name": "corrected_universe",
        "path": PROJECT
        / "work/final_theorem_release/run_corrected_universe_mutations.py",
        "authoritative": PROJECT
        / "work/final_theorem_release/corrected_universe_mutation_report.json",
        "marker": "CORRECTED_UNIVERSE_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "CORRECTED_UNIVERSE_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN",
        "support_files": ("release_common.py",),
    },
    {
        "name": "full_map_reseal",
        "path": PROJECT / "work/final_theorem_release/verify_full_map_reseal.py",
        "authoritative": PROJECT
        / "work/final_theorem_release/full_map_reseal_audit.json",
        "marker": "FULL_MAP_RESEAL_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "FULL_MAP_RESEAL_OPTIMIZED_MODE_FORBIDDEN",
    },
    {
        "name": "probe_input",
        "path": PROJECT
        / "work/adversarial_proof_review/test_probe_input_mutations.py",
        "authoritative": PROJECT
        / "work/adversarial_proof_review/probe_input_mutation_certificate.json",
        "marker": "PROBE_INPUT_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_bytes",
        "data": b"atomic-output\n",
        "optimized_marker": "PROBE_INPUT_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN",
    },
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_runner(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(
        f"k2p_nested_output_{name}", path
    )
    require(
        specification is not None and specification.loader is not None,
        f"cannot import:{path}",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    local_import_root = str(path.parent)
    sys.path.insert(0, local_import_root)
    try:
        specification.loader.exec_module(module)
    finally:
        require(
            sys.path[0] == local_import_root,
            f"nested runner changed import precedence while loading:{path}",
        )
        sys.path.pop(0)
    return module


def expect_policy_failure(module, output: Path, marker: str, allow: bool = False):
    try:
        module.validate_output_path(output, allow)
    except (RuntimeError, SystemExit) as error:
        require(marker in str(error), f"wrong output diagnostic:{error}")
        return
    raise RuntimeError(f"unsafe nested output accepted:{output}")


def main() -> None:
    if not __debug__:
        raise SystemExit("NESTED_MUTATION_OUTPUT_TEST_OPTIMIZED_MODE_FORBIDDEN")
    with tempfile.TemporaryDirectory(
        prefix="k2p-nested-mutation-output-contract-"
    ) as directory:
        root = Path(directory)
        for specification in RUNNERS:
            name = specification["name"]
            runner = specification["path"]
            authoritative = specification["authoritative"]
            marker = specification["marker"]
            module = load_runner(name, runner)
            hashes = {path: sha(path) for path in (runner, authoritative)}

            missing_output = subprocess.run(
                [sys.executable, "-B", str(runner)],
                cwd=PROJECT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            require(
                missing_output.returncode != 0
                and "--output" in missing_output.stdout
                and "required" in missing_output.stdout,
                f"nested runner did not require output:{name}",
            )
            expect_policy_failure(module, runner, marker)
            expect_policy_failure(module, authoritative, marker)
            require(
                module.validate_output_path(authoritative, True)
                == authoritative.parent.resolve() / authoritative.name,
                f"canonical override rejected:{name}",
            )
            expect_policy_failure(module, root / f"{name}-external.json", marker, True)

            optimized_marker = specification["optimized_marker"]
            if optimized_marker is not None:
                optimized_output = root / f"{name}-optimized-stale-pass.json"
                optimized_output.write_text('{"status":"PASS","stale":true}\n')
                optimized = subprocess.run(
                    [
                        sys.executable,
                        "-O",
                        "-B",
                        str(runner),
                        "--output",
                        str(optimized_output),
                    ],
                    cwd=PROJECT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False,
                )
                require(
                    optimized.returncode != 0
                    and optimized_marker in optimized.stdout
                    and not optimized_output.exists(),
                    f"optimized nested run retained stale PASS:{name}:{optimized.stdout}",
                )

            outside_symlink = root / f"{name}-outside-symlink.json"
            outside_symlink.symlink_to(runner)
            expect_policy_failure(module, outside_symlink, marker)

            copied_source = root / f"{name}-copied-source.py"
            shutil.copy2(runner, copied_source)
            copied_hash = sha(copied_source)
            copied_inode = copied_source.stat().st_ino
            hardlink = root / f"{name}-hardlink-output.json"
            os.link(copied_source, hardlink)
            validated_hardlink = module.validate_output_path(hardlink, False)
            getattr(module, specification["writer"])(
                validated_hardlink, specification["data"]
            )
            require(
                sha(copied_source) == copied_hash
                and copied_source.stat().st_ino == copied_inode
                and hardlink.stat().st_ino != copied_inode,
                f"nested writer truncated a hardlinked source:{name}",
            )

            late_swap = root / f"{name}-late-symlink.json"
            validated_swap = module.validate_output_path(late_swap, False)
            late_swap.symlink_to(copied_source)
            getattr(module, specification["writer"])(
                validated_swap, specification["data"]
            )
            require(
                not late_swap.is_symlink() and sha(copied_source) == copied_hash,
                f"nested writer followed a late symlink:{name}",
            )

            copied_project = root / f"{name}-canonical-symlink-project"
            copied_runner = copied_project / runner.relative_to(PROJECT)
            copied_authoritative = copied_project / authoritative.relative_to(PROJECT)
            copied_runner.parent.mkdir(parents=True, exist_ok=True)
            copied_authoritative.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(runner, copied_runner)
            copied_strict = (
                copied_project / "work/final_theorem_release/strict_json.py"
            )
            copied_strict.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                PROJECT / "work/final_theorem_release/strict_json.py",
                copied_strict,
            )
            for support_name in specification.get("support_files", ()):
                shutil.copy2(runner.parent / support_name, copied_runner.parent / support_name)
            copied_authoritative.symlink_to(root / f"{name}-noncanonical.json")
            rejected = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(copied_runner),
                    "--output",
                    str(copied_authoritative),
                    "--allow-authoritative-output",
                ],
                cwd=copied_project,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            require(
                rejected.returncode != 0 and marker in rejected.stdout,
                f"canonical symlink override accepted:{name}:{rejected.stdout}",
            )
            require(
                all(sha(path) == digest for path, digest in hashes.items()),
                f"nested output regression changed release sources:{name}",
            )

        audit_runner = (
            PROJECT
            / "work/global_proof_adversary/probe_full_audit/"
            "independent_probe_graph_audit.py"
        )
        audit_output = audit_runner.parent / "independent_probe_graph_audit_certificate.json"
        audit_mutations = audit_runner.parent / "independent_probe_mutation_report.json"
        audit = load_runner("independent_probe_audit", audit_runner)
        audit_hashes = {
            path: sha(path) for path in (audit_runner, audit_output, audit_mutations)
        }
        accepted = audit.validate_output_paths(
            audit_output, audit_mutations, True
        )
        require(
            accepted
            == (
                audit_output.parent.resolve() / audit_output.name,
                audit_mutations.parent.resolve() / audit_mutations.name,
            ),
            "probe-audit canonical override rejected",
        )
        try:
            audit.validate_output_paths(audit_output, audit_mutations, False)
        except RuntimeError as error:
            require(
                "PROBE_AUDIT_OUTPUT_POLICY_FAIL" in str(error),
                f"probe-audit wrong project-output failure:{error}",
            )
        else:
            raise RuntimeError("probe-audit accepted project-tree routine outputs")
        external_audit = root / "probe-audit-external.json"
        external_mutations = root / "probe-audit-mutations-external.json"
        try:
            audit.validate_output_paths(external_audit, external_mutations, True)
        except RuntimeError as error:
            require(
                "PROBE_AUDIT_OUTPUT_POLICY_FAIL" in str(error),
                f"probe-audit wrong override failure:{error}",
            )
        else:
            raise RuntimeError("probe-audit accepted noncanonical override")
        external_audit.write_text('{"status":"PASS","stale":true}\n')
        external_mutations.write_text('{"status":"PASS","stale":true}\n')
        optimized = subprocess.run(
            [
                sys.executable,
                "-O",
                "-B",
                str(audit_runner),
                "--output",
                str(external_audit),
                "--mutations-output",
                str(external_mutations),
            ],
            cwd=PROJECT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(
            optimized.returncode != 0
            and "assertions optimized away" in optimized.stdout
            and not external_audit.exists()
            and not external_mutations.exists(),
            f"probe-audit optimized run retained stale PASS:{optimized.stdout}",
        )
        audit_symlink = root / "probe-audit-symlink.json"
        audit_symlink.symlink_to(audit_runner)
        try:
            audit.validate_output_paths(audit_symlink, external_mutations, False)
        except RuntimeError as error:
            require(
                "PROBE_AUDIT_OUTPUT_POLICY_FAIL" in str(error),
                f"probe-audit wrong symlink failure:{error}",
            )
        else:
            raise RuntimeError("probe-audit accepted symlink output")
        audit_hardlink = root / "probe-audit-hardlink.json"
        os.link(audit_runner, audit_hardlink)
        try:
            audit.validate_output_paths(audit_hardlink, external_mutations, False)
        except RuntimeError as error:
            require(
                "PROBE_AUDIT_OUTPUT_POLICY_FAIL" in str(error),
                f"probe-audit wrong hardlink failure:{error}",
            )
        else:
            raise RuntimeError("probe-audit accepted hardlink output")
        require(
            all(sha(path) == digest for path, digest in audit_hashes.items()),
            "probe-audit output regression changed release sources",
        )

    print("K2P_NESTED_MUTATION_OUTPUT_CONTRACT_PASS")
    print(
        json.dumps(
            {
                "writers": len(RUNNERS) + 1,
                "required_external_outputs": True,
                "direct_and_symlink_collisions_rejected": True,
                "hardlink_and_late_symlink_safe": True,
                "canonical_symlink_override_rejected": True,
                "source_bytes_unchanged": True,
                "optimized_rejections_remove_stale_reports": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
