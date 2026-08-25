#!/usr/bin/env python3
"""Regression test for relocatable, source-preserving quartet mutations."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import test_quartet_semantics_mutations as semantics_mutations
import test_quartet_terminal_binding_mutations as terminal_mutations


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
MUTATION_RUNNER = Path("work/quartet_separation_closure/test_quartet_semantics_mutations.py")
TERMINAL_MUTATION_RUNNER = Path(
    "work/quartet_separation_closure/test_quartet_terminal_binding_mutations.py"
)
TERMINAL_VERIFIER = Path(
    "work/quartet_separation_closure/verify_quartet_terminal_bindings.py"
)
SOURCE_FILES = (
    MUTATION_RUNNER,
    Path("work/quartet_separation_closure/verify_quartet_logic.py"),
    Path("work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json"),
    Path("work/quartet_separation_closure/quartet_semantics_mutation_certificate.json"),
    Path("work/quartet_separation_closure/PROOF.md"),
    Path("proof_compression_submission/article/main.tex"),
    Path("work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md"),
    Path("work/global_theorem_closure/GLOBAL_PROOF.md"),
    Path("work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md"),
    TERMINAL_MUTATION_RUNNER,
    TERMINAL_VERIFIER,
    Path(
        "work/quartet_separation_closure/"
        "quartet_terminal_binding_mutation_certificate.json"
    ),
)
COLLISION_FILES = (
    MUTATION_RUNNER,
    Path("work/quartet_separation_closure/verify_quartet_logic.py"),
    Path("work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json"),
    Path("proof_compression_submission/article/main.tex"),
)
AUTHORITATIVE_OUTPUT = Path(
    "work/quartet_separation_closure/quartet_semantics_mutation_certificate.json"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def copy_minimal_project(destination: Path) -> None:
    for relative in SOURCE_FILES:
        source = PROJECT / relative
        require(source.is_file(), f"missing regression input:{relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def snapshot(project: Path) -> dict[str, str]:
    return {
        str(path.relative_to(project)): sha(path.read_bytes())
        for path in sorted(project.rglob("*"))
        if path.is_file()
    }


def run_suite(project: Path, output: Path) -> tuple[bytes, str]:
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(project / MUTATION_RUNNER),
            "--output",
            str(output),
        ],
        cwd=project,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    require(completed.returncode == 0, f"relocated suite failed:{completed.stdout}")
    require(
        "K2P_QUARTET_SEMANTICS_MUTATIONS_PASS" in completed.stdout,
        f"relocated suite omitted PASS marker:{completed.stdout}",
    )
    require(output.is_file(), "relocated suite omitted caller-owned output")
    return output.read_bytes(), completed.stdout


def require_output_policy_rejection(
    project: Path, output: Path, *, allow_authoritative_output: bool = False
) -> None:
    command = [
        sys.executable,
        "-B",
        str(project / MUTATION_RUNNER),
        "--output",
        str(output),
    ]
    if allow_authoritative_output:
        command.append("--allow-authoritative-output")
    completed = subprocess.run(
        command,
        cwd=project,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    require(
        completed.returncode != 0
        and "QUARTET_MUTATION_OUTPUT_POLICY_FAIL" in completed.stdout,
        f"unsafe output was not rejected:{output}:{completed.stdout}",
    )


def require_terminal_output_policy_rejection(project: Path, output: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(project / TERMINAL_MUTATION_RUNNER),
            "--output",
            str(output),
        ],
        cwd=project,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    require(
        completed.returncode != 0
        and "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL" in completed.stdout,
        f"unsafe terminal output was not rejected:{output}:{completed.stdout}",
    )


def main() -> None:
    if not __debug__:
        raise SystemExit("QUARTET_RELOCATION_TEST_OPTIMIZED_MODE_FORBIDDEN")
    with tempfile.TemporaryDirectory(prefix="k2p-quartet-relocation-") as directory:
        root = Path(directory)
        projects = (
            root / "extraction_alpha",
            root / "extraction_beta_with_a_deliberately_different_length",
        )
        outputs = (root / "outputs/alpha.json", root / "outputs/beta.json")
        for project in projects:
            copy_minimal_project(project)

        no_output = subprocess.run(
            [sys.executable, "-B", str(projects[0] / MUTATION_RUNNER)],
            cwd=projects[0],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(
            no_output.returncode != 0
            and "--output" in no_output.stdout
            and "required" in no_output.stdout,
            "mutation runner did not require caller-owned output",
        )
        terminal_no_output = subprocess.run(
            [sys.executable, "-B", str(projects[0] / TERMINAL_MUTATION_RUNNER)],
            cwd=projects[0],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(
            terminal_no_output.returncode != 0
            and "--output" in terminal_no_output.stdout
            and "required" in terminal_no_output.stdout,
            "terminal mutation runner did not require caller-owned output",
        )

        collision_before = snapshot(projects[0])
        require_output_policy_rejection(
            projects[0], projects[0] / "ordinary-in-project-output.json"
        )
        require_output_policy_rejection(
            projects[0], projects[0] / AUTHORITATIVE_OUTPUT
        )
        for relative in COLLISION_FILES:
            require_output_policy_rejection(projects[0], projects[0] / relative)

        symlink = root / "outside-name-resolving-to-project-source.json"
        symlink.symlink_to(projects[0] / COLLISION_FILES[2])
        require_output_policy_rejection(projects[0], symlink)
        require_output_policy_rejection(
            projects[0], outputs[0], allow_authoritative_output=True
        )

        terminal_authoritative = projects[0] / Path(
            "work/quartet_separation_closure/"
            "quartet_terminal_binding_mutation_certificate.json"
        )
        require_terminal_output_policy_rejection(
            projects[0], projects[0] / "ordinary-terminal-output.json"
        )
        require_terminal_output_policy_rejection(
            projects[0], projects[0] / TERMINAL_MUTATION_RUNNER
        )
        require_terminal_output_policy_rejection(
            projects[0], projects[0] / TERMINAL_VERIFIER
        )
        require_terminal_output_policy_rejection(projects[0], terminal_authoritative)
        terminal_symlink = root / "terminal-outside-name-to-project-source.json"
        terminal_symlink.symlink_to(projects[0] / TERMINAL_VERIFIER)
        require_terminal_output_policy_rejection(projects[0], terminal_symlink)

        require(
            terminal_mutations.validate_output_path(
                terminal_mutations.AUTHORITATIVE_OUTPUT, True
            )
            == terminal_mutations.AUTHORITATIVE_OUTPUT.resolve(),
            "terminal canonical authoritative override rejected",
        )
        try:
            terminal_mutations.validate_output_path(outputs[0], True)
        except SystemExit as error:
            require(
                "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL" in str(error),
                f"wrong terminal override diagnostic:{error}",
            )
        else:
            raise RuntimeError("terminal override licensed a noncanonical path")
        require(
            collision_before == snapshot(projects[0]),
            "rejected output collisions changed source-project bytes",
        )

        copied_spec = projects[0] / COLLISION_FILES[2]
        copied_spec_hash = sha(copied_spec.read_bytes())
        copied_spec_inode = copied_spec.stat().st_ino
        hardlink_output = root / "outside-hardlink-to-project-spec.json"
        os.link(copied_spec, hardlink_output)
        hardlink_report = run_suite(projects[0], hardlink_output)[0]
        require(
            sha(copied_spec.read_bytes()) == copied_spec_hash
            and copied_spec.stat().st_ino == copied_spec_inode
            and hardlink_output.stat().st_ino != copied_spec_inode,
            "atomic report write truncated a hardlinked project source",
        )

        late_swap_output = root / "late-symlink-swap.json"
        validated_late_output = semantics_mutations.validate_output_path(
            late_swap_output, False
        )
        late_swap_output.symlink_to(copied_spec)
        semantics_mutations.atomic_write_text(
            validated_late_output, "atomic-symlink-replacement\n"
        )
        require(
            not late_swap_output.is_symlink()
            and late_swap_output.read_text(encoding="utf-8")
            == "atomic-symlink-replacement\n"
            and sha(copied_spec.read_bytes()) == copied_spec_hash,
            "late semantic output symlink clobbered its source target",
        )

        terminal_late_swap = root / "terminal-late-symlink-swap.json"
        terminal_validated_late_output = terminal_mutations.validate_output_path(
            terminal_late_swap, False
        )
        terminal_late_swap.symlink_to(copied_spec)
        terminal_mutations.atomic_write_text(
            terminal_validated_late_output, "terminal-atomic-replacement\n"
        )
        require(
            not terminal_late_swap.is_symlink()
            and terminal_late_swap.read_text(encoding="utf-8")
            == "terminal-atomic-replacement\n"
            and sha(copied_spec.read_bytes()) == copied_spec_hash,
            "late terminal output symlink clobbered its source target",
        )

        before = [snapshot(project) for project in projects]
        reports = [
            run_suite(project, output)[0]
            for project, output in zip(projects, outputs, strict=True)
        ]
        after = [snapshot(project) for project in projects]
        require(before == after, "relocated suite changed source-project bytes")
        require(reports[0] == reports[1], "relocated reports differ by extraction path")
        require(
            hardlink_report == reports[0],
            "hardlink-safe report differs from ordinary disposable report",
        )

        report = json.loads(reports[0])
        require(
            report.get("schema") == "k2p-quartet-semantics-mutations-v3",
            "relocated report schema drift",
        )
        require(report.get("status") == "PASS", "relocated report is not PASS")
        require(report.get("case_count") == 8, "relocated report case-count drift")
        require(
            all(
                row.get("observed_marker") == row.get("expected_marker")
                and row.get("observed_returncode") == 1
                and row.get("failed_mutation_certificate_written") is False
                and "stdout_sha256" not in row
                for row in report.get("cases", [])
            ),
            "relocated report diagnostic contract drift",
        )

        override_project = root / "explicit_authoritative_reseal"
        copy_minimal_project(override_project)
        override_before = snapshot(override_project)
        authoritative = override_project / AUTHORITATIVE_OUTPUT
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(override_project / MUTATION_RUNNER),
                "--output",
                str(authoritative),
                "--allow-authoritative-output",
            ],
            cwd=override_project,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(
            completed.returncode == 0
            and "K2P_QUARTET_SEMANTICS_MUTATIONS_PASS" in completed.stdout,
            f"explicit authoritative reseal failed:{completed.stdout}",
        )
        override_after = snapshot(override_project)
        changed = sorted(
            path
            for path in set(override_before) | set(override_after)
            if override_before.get(path) != override_after.get(path)
        )
        require(
            changed == [str(AUTHORITATIVE_OUTPUT)],
            f"authoritative override changed non-certificate sources:{changed}",
        )
        require(
            authoritative.read_bytes() == reports[0],
            "authoritative override report differs from disposable report",
        )

        for runner, authoritative_relative, marker in (
            (
                MUTATION_RUNNER,
                AUTHORITATIVE_OUTPUT,
                "QUARTET_MUTATION_OUTPUT_POLICY_FAIL",
            ),
            (
                TERMINAL_MUTATION_RUNNER,
                Path(
                    "work/quartet_separation_closure/"
                    "quartet_terminal_binding_mutation_certificate.json"
                ),
                "QUARTET_TERMINAL_MUTATION_OUTPUT_POLICY_FAIL",
            ),
        ):
            symlink_project = root / f"canonical_symlink_{runner.name}"
            copy_minimal_project(symlink_project)
            canonical_path = symlink_project / authoritative_relative
            canonical_path.unlink()
            canonical_path.symlink_to(root / "noncanonical-certificate-target.json")
            rejected = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(symlink_project / runner),
                    "--output",
                    str(canonical_path),
                    "--allow-authoritative-output",
                ],
                cwd=symlink_project,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            require(
                rejected.returncode != 0 and marker in rejected.stdout,
                f"authoritative override followed canonical symlink:{rejected.stdout}",
            )

    print("K2P_QUARTET_SEMANTICS_RELOCATION_PASS")
    print(
        json.dumps(
            {
                "case_count": 8,
                "report_sha256": sha(reports[0]),
                "source_bytes_unchanged": True,
                "two_extraction_reports_identical": True,
                "collision_and_symlink_guards": True,
                "authoritative_override_exact": True,
                "terminal_output_policy": True,
                "hardlink_and_late_symlink_safe": True,
                "canonical_symlink_override_rejected": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
