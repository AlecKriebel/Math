#!/usr/bin/env python3
"""Regression tests for fail-closed Paper II certificate execution."""

from __future__ import annotations

import ast
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


PAPER = Path(__file__).resolve().parents[1]
CERTIFIERS = (
    (
        Path("certificates/verify_leading_algebra.py"),
        "PASS exact sextic threshold, tangency, and monotonicity algebra",
    ),
    (
        Path("certificates/verify_hybrid_lumping.py"),
        "PASS exact labelled hybrid lumping",
    ),
    (
        Path("certificates/verify_hybrid_coefficients.py"),
        "PASS exact hybrid coefficient and phase-polynomial audit",
    ),
    (
        Path("verify_paper_claims.py"),
        "PASS: Paper II exact integration audit",
    ),
)
REPLAY_SENTINEL = "PASS: Paper II verifier replay complete"


class RegressionError(RuntimeError):
    """Raised when a verifier fails to fail closed."""


def require(condition: object, message: str) -> None:
    if not bool(condition):
        raise RegressionError(message)


def reject_optimized_python() -> None:
    if sys.flags.optimize != 0:
        raise SystemExit(
            "ERROR: optimized Python is unsupported because regression "
            "checks must remain active"
        )


def run(
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )


def output_of(process: subprocess.CompletedProcess[str]) -> str:
    return process.stdout or ""


def require_success(
    process: subprocess.CompletedProcess[str], sentinel: str, label: str
) -> None:
    output = output_of(process)
    require(
        process.returncode == 0,
        f"{label} unexpectedly failed with status {process.returncode}:\n{output}",
    )
    require(sentinel in output, f"{label} omitted its success sentinel:\n{output}")


def require_failure_without_sentinel(
    process: subprocess.CompletedProcess[str], sentinel: str, label: str
) -> None:
    output = output_of(process)
    require(process.returncode != 0, f"{label} unexpectedly exited successfully")
    require(
        sentinel not in output,
        f"{label} printed a false success sentinel after failure:\n{output}",
    )


def check_no_bare_assertions() -> None:
    files = [PAPER / relative for relative, _ in CERTIFIERS]
    files.extend((PAPER / "bundle_manifest.py", Path(__file__).resolve()))
    submission_verifier = PAPER / "submission/verify_submission_materials.py"
    if submission_verifier.is_file():
        files.append(submission_verifier)
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        lines = sorted(
            node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)
        )
        require(not lines, f"optimization-sensitive assertions remain in {path}: {lines}")


def check_direct_execution() -> None:
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for relative, sentinel in CERTIFIERS:
        ordinary = run(
            [sys.executable, str(PAPER / relative)],
            cwd=PAPER,
            environment=environment,
        )
        require_success(ordinary, sentinel, f"ordinary direct run of {relative}")

        optimized = run(
            [sys.executable, "-O", str(PAPER / relative)],
            cwd=PAPER,
            environment=environment,
        )
        require_failure_without_sentinel(
            optimized,
            sentinel,
            f"optimized direct run of {relative}",
        )

    submission = PAPER / "submission/verify_submission_materials.py"
    if submission.is_file():
        optimized_submission = run(
            [sys.executable, "-O", str(submission)],
            cwd=PAPER,
            environment=environment,
        )
        require_failure_without_sentinel(
            optimized_submission,
            "PASS: submission identity",
            "optimized submission verifier",
        )

    with tempfile.TemporaryDirectory(prefix="paper2-builder-optimize-") as temporary:
        archive = Path(temporary) / "must-not-exist.tar.gz"
        optimized_builder = run(
            [
                sys.executable,
                "-O",
                str(PAPER / "bundle_manifest.py"),
                "--repo-root",
                str(PAPER.parents[2]),
                "--output",
                str(archive),
            ],
            cwd=PAPER,
            environment=environment,
        )
        require_failure_without_sentinel(
            optimized_builder,
            "WROTE:",
            "optimized archive builder",
        )
        require(not archive.exists(), "optimized archive builder wrote an artifact")


def check_optimized_entry_points() -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONOPTIMIZE"] = "1"
    environment["PYTHON"] = sys.executable
    replay = run(
        [str(PAPER / "replay.sh")],
        cwd=PAPER,
        environment=environment,
    )
    require_failure_without_sentinel(
        replay,
        REPLAY_SENTINEL,
        "PYTHONOPTIMIZE=1 replay",
    )
    for _, sentinel in CERTIFIERS:
        require(
            sentinel not in output_of(replay),
            f"optimized replay printed a certificate success sentinel: {sentinel}",
        )

    environment["BOOTSTRAP_PYTHON"] = sys.executable
    bootstrap = run(
        [str(PAPER / "bootstrap_replay.sh")],
        cwd=PAPER,
        environment=environment,
    )
    require_failure_without_sentinel(
        bootstrap,
        REPLAY_SENTINEL,
        "PYTHONOPTIMIZE=1 bootstrap replay",
    )
    require(
        "PASS: Python 3.14.6" not in output_of(bootstrap),
        "optimized bootstrap printed its runtime success sentinel",
    )

    with tempfile.TemporaryDirectory(prefix="paper2-release-optimize-") as temporary:
        release_archive = Path(temporary) / "must-not-exist.tar.gz"
        optimized_release = run(
            [str(PAPER / "release_bundle.sh"), str(release_archive)],
            cwd=PAPER,
            environment=environment,
        )
        require_failure_without_sentinel(
            optimized_release,
            REPLAY_SENTINEL,
            "PYTHONOPTIMIZE=1 release",
        )
        require(
            not release_archive.exists(),
            "optimized release wrote an archive despite replay rejection",
        )


def copy_replay_tree(destination: Path) -> Path:
    paper = destination / "paper"
    paper.mkdir(parents=True)
    for name in ("main.tex", "replay.sh", "verify_paper_claims.py"):
        shutil.copy2(PAPER / name, paper / name)
    shutil.copytree(PAPER / "certificates", paper / "certificates")
    return paper


def replace_once(path: Path, old: str, new: str) -> None:
    source = path.read_text(encoding="utf-8")
    require(
        source.count(old) == 1,
        f"mutation anchor is not unique in {path}: {old!r}",
    )
    path.write_text(source.replace(old, new, 1), encoding="utf-8")


def run_copied_replay(paper: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHON"] = sys.executable
    return run([str(paper / "replay.sh")], cwd=paper, environment=environment)


def check_mutation_failure_propagation() -> None:
    with tempfile.TemporaryDirectory(prefix="paper2-fail-closed-") as temporary:
        temporary_root = Path(temporary)

        early = copy_replay_tree(temporary_root / "early")
        replace_once(
            early / "certificates/verify_leading_algebra.py",
            "39866792399",
            "39866792398",
        )
        early_result = run_copied_replay(early)
        require_failure_without_sentinel(
            early_result,
            REPLAY_SENTINEL,
            "early mathematical mutation replay",
        )
        early_output = output_of(early_result)
        for _, sentinel in CERTIFIERS:
            require(
                sentinel not in early_output,
                "early mutation did not stop before certificate success output: "
                f"{sentinel}",
            )

        late = copy_replay_tree(temporary_root / "late")
        replace_once(
            late / "verify_paper_claims.py",
            '"fitness-independent",',
            '"fitness-independent-MUTATED",',
        )
        late_result = run_copied_replay(late)
        require_failure_without_sentinel(
            late_result,
            REPLAY_SENTINEL,
            "late integration mutation replay",
        )
        late_output = output_of(late_result)
        require(
            CERTIFIERS[2][1] in late_output,
            "late mutation did not execute the preceding certifiers",
        )
        require(
            CERTIFIERS[3][1] not in late_output,
            "late mutation printed the integration-audit success sentinel",
        )


def main() -> None:
    reject_optimized_python()
    check_no_bare_assertions()
    check_direct_execution()
    check_optimized_entry_points()
    check_mutation_failure_propagation()
    print(
        "PASS: explicit checks, optimization rejection, mutations, and "
        "failure propagation"
    )


if __name__ == "__main__":
    main()
