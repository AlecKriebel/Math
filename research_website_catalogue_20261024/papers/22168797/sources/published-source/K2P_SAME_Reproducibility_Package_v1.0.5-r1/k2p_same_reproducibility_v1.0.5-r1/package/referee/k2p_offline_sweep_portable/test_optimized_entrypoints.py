#!/usr/bin/env python3
"""Qualify optimized-mode guards and assertion-independent atlas failures."""
from __future__ import annotations

if not __debug__:
    raise SystemExit("K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN")

import ast
import hashlib
import os
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PORTABLE_MARKER = "K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN"


@dataclass(frozen=True)
class EntryPoint:
    name: str
    relative_path: str
    arguments: tuple[str, ...]
    diagnostic: str
    shell: bool = False


def package_fingerprint() -> str:
    digest = hashlib.sha256()
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = path.relative_to(ROOT).as_posix().encode("utf-8")
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def entry_points(scratch: Path) -> tuple[EntryPoint, ...]:
    return (
        EntryPoint(
            "verify_package",
            "verify_package.py",
            ("--skip-smoke", "--skip-mutations", "--skip-prepared-audit"),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "guarded_run",
            "guarded_run.py",
            (
                str(scratch / "guarded-output"),
                "--skip-package-verify",
                "--min-start-free-gib", "0",
                "--min-runtime-free-gib", "0",
            ),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "resumable_driver",
            "resumable_four_port_driver.py",
            (
                "--package-root", str(ROOT),
                "--output-root", str(scratch / "driver-output"),
                "--source-index", "0", "--start", "0", "--end", "1",
            ),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "merge_manifests",
            "merge_manifests.py",
            (
                "--package-root", str(ROOT),
                "--run-root", str(scratch / "merge-output"),
            ),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "compare_semantic_runs",
            "compare_semantic_runs.py",
            (str(scratch / "baseline"), str(scratch / "candidate")),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "verify_direct_closure",
            "verify_direct_closure_release.py",
            ("--quick",),
            "DIRECT_CLOSURE_OPTIMIZED_MODE_FORBIDDEN: invoke Python without -O",
        ),
        EntryPoint(
            "direct_closure_mutations",
            "test_direct_closure_release_mutations.py",
            ("--output", str(scratch / "direct-closure-mutations.json")),
            "DIRECT_CLOSURE_MUTATION_OPTIMIZED_MODE_FORBIDDEN",
        ),
        EntryPoint(
            "build_direct_closure_lock",
            "build_direct_closure_lock.py",
            ("--check",),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "exact_kernel_test",
            "test_exact_kernels.py",
            (),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "portable_mutations",
            "test_mutations.py",
            ("--package-root", str(ROOT)),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "optimized_entrypoint_test",
            "test_optimized_entrypoints.py",
            (),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "atlas_developer_census",
            "atlas/k2p_atlas_core.py",
            (),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "direct_residual_replay",
            "proofs/verify_four_port_direct_residual_closure.py",
            (),
            PORTABLE_MARKER,
        ),
        EntryPoint(
            "theta_modular_probe",
            "proofs/theta_modular_invariant_probe.py",
            (),
            "candidate replay requires assertions; do not use python -O",
        ),
        EntryPoint(
            "theta0_quintic_replay",
            "proofs/verify_theta0_quintic_orbit.py",
            (),
            "exact replay requires assertions; do not use python -O",
        ),
        EntryPoint(
            "theta_quartic_replay",
            "proofs/verify_theta_quartic_obstructions.py",
            (),
            "exact replay requires assertions; do not use python -O",
        ),
        EntryPoint(
            "theta_quartic_independent_replay",
            "proofs/verify_theta_quartic_obstructions_independent.py",
            (),
            "exact replay requires assertions; do not use python -O",
        ),
        EntryPoint(
            "run_all_sources",
            "run_all_sources.sh",
            (str(scratch / "shell-output"),),
            PORTABLE_MARKER,
            shell=True,
        ),
    )


def invoke(case: EntryPoint, mode: str, scratch: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    path = ROOT / case.relative_path
    if case.shell:
        if mode == "dash_O":
            # Shell entry points receive their Python runtime through the
            # documented PYTHON_BIN interface, so a wrapper supplies -O.
            wrapper = scratch / "python-O"
            wrapper.write_text(
                "#!/usr/bin/env bash\n"
                f'exec {shlex.quote(sys.executable)} -O "$@"\n',
                encoding="utf-8",
            )
            wrapper.chmod(0o700)
            environment["PYTHON_BIN"] = str(wrapper)
        else:
            environment["PYTHON_BIN"] = sys.executable
            environment["PYTHONOPTIMIZE"] = "1"
        command = ["bash", str(path), *case.arguments]
    else:
        if mode == "dash_O":
            command = [sys.executable, "-O", "-B", str(path), *case.arguments]
        else:
            environment["PYTHONOPTIMIZE"] = "1"
            command = [sys.executable, "-B", str(path), *case.arguments]
    return subprocess.run(
        command,
        cwd=scratch,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=20,
        check=False,
    )


def verify_entrypoint_guards() -> None:
    before = package_fingerprint()
    case_count = len(entry_points(ROOT))
    for mode in ("dash_O", "environment"):
        for index in range(case_count):
            with tempfile.TemporaryDirectory(prefix="k2p_portable_optimized_") as raw:
                scratch = Path(raw)
                case = entry_points(scratch)[index]
                result = invoke(case, mode, scratch)
                observed = result.stdout.strip()
                if result.returncode != 1 or observed != case.diagnostic:
                    raise RuntimeError(
                        "K2P_OPTIMIZED_ENTRYPOINT_GUARD_FAIL "
                        f"mode={mode} case={case.name} exit={result.returncode} "
                        f"output={observed!r}"
                    )
                residuals = sorted(
                    path.relative_to(scratch).as_posix()
                    for path in scratch.rglob("*")
                    if path.name != "python-O"
                )
                if residuals:
                    raise RuntimeError(
                        "K2P_OPTIMIZED_ENTRYPOINT_RESIDUAL_OUTPUT "
                        f"mode={mode} case={case.name} paths={residuals!r}"
                    )
    after = package_fingerprint()
    if after != before:
        raise RuntimeError(
            f"K2P_OPTIMIZED_ENTRYPOINT_SOURCE_DRIFT before={before} after={after}"
        )


SEMANTIC_PROBE = r'''
import importlib.util
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("k2p_atlas_assert_probe", path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
constant = (((), ((0, 1),)),)
outputs = tuple(constant for _ in module.orbit_assignments(4))
descriptor = module.MapDescriptor(4, 0, 0, outputs, ())
module.kernel_sparse_columns_fast = lambda columns: (
    (1,) + (0,) * (len(columns) - 1),
)
try:
    module.quadratic_separator_fast(descriptor, descriptor)
except module.AtlasInvariantError as exc:
    if str(exc) != "ATLAS_TARGET_PULLBACK_NONZERO degree=2 engine=fast":
        raise
    print(str(exc))
    raise SystemExit(23)
raise SystemExit("K2P_FALSE_SEPARATOR_ACCEPTED")
'''


def verify_assertion_independence() -> None:
    atlas_path = ROOT / "atlas" / "k2p_atlas_core.py"
    parsed = ast.parse(atlas_path.read_text(encoding="utf-8"), filename=str(atlas_path))
    assert_nodes = [node for node in ast.walk(parsed) if isinstance(node, ast.Assert)]
    if assert_nodes:
        lines = [node.lineno for node in assert_nodes]
        raise RuntimeError(f"K2P_ATLAS_ASSERT_STATEMENTS_REMAIN lines={lines!r}")
    expected = "ATLAS_TARGET_PULLBACK_NONZERO degree=2 engine=fast"
    for mode in ("normal", "dash_O", "environment"):
        environment = os.environ.copy()
        environment.pop("PYTHONOPTIMIZE", None)
        command = [sys.executable, "-B", "-c", SEMANTIC_PROBE, str(atlas_path)]
        if mode == "dash_O":
            command.insert(1, "-O")
        elif mode == "environment":
            environment["PYTHONOPTIMIZE"] = "1"
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
            check=False,
        )
        if result.returncode != 23 or result.stdout.strip() != expected:
            raise RuntimeError(
                "K2P_ATLAS_ASSERTION_INDEPENDENCE_FAIL "
                f"mode={mode} exit={result.returncode} output={result.stdout.strip()!r}"
            )


def main() -> None:
    verify_entrypoint_guards()
    verify_assertion_independence()
    print("K2P_PORTABLE_OPTIMIZED_ENTRYPOINT_MATRIX_PASS")


if __name__ == "__main__":
    main()
