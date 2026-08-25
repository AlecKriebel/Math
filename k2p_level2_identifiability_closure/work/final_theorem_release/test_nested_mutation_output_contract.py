#!/usr/bin/env python3
"""Output-safety regression for canonicalizer and transport mutation writers."""

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
        "name": "canonicalizer",
        "path": PROJECT
        / "work/canonicalizer_completeness/test_canonicalizer_mutations.py",
        "authoritative": PROJECT
        / "work/canonicalizer_completeness/"
        "canonicalizer_completeness_mutation_certificate.json",
        "marker": "CANONICALIZER_MUTATION_OUTPUT_POLICY_FAIL",
        "writer": "atomic_write_text",
        "data": "atomic-output\n",
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
    specification.loader.exec_module(module)
    return module


def expect_policy_failure(module, output: Path, marker: str, allow: bool = False):
    try:
        module.validate_output_path(output, allow)
    except SystemExit as error:
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

    print("K2P_NESTED_MUTATION_OUTPUT_CONTRACT_PASS")
    print(
        json.dumps(
            {
                "writers": 2,
                "required_external_outputs": True,
                "direct_and_symlink_collisions_rejected": True,
                "hardlink_and_late_symlink_safe": True,
                "canonical_symlink_override_rejected": True,
                "source_bytes_unchanged": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
