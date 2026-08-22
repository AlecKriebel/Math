#!/usr/bin/env python3
"""Fail-closed runtime, dependency, and source checks for Paper I replay."""

from __future__ import annotations

import argparse
import ast
import importlib
import importlib.metadata as metadata
import importlib.util
import os
from pathlib import Path
import sys


EXPECTED_PYTHON = (3, 14, 6)
EXPECTED_DISTRIBUTIONS = {
    "sympy": ("sympy", "1.14.0"),
    "python-flint": ("flint", "0.9.0"),
    "mpmath": ("mpmath", "1.3.0"),
}
UNSAFE_ENVIRONMENT = (
    "PYTHONOPTIMIZE",
    "PYTHONPATH",
    "PYTHONHOME",
    "PYTHONPYCACHEPREFIX",
    "PYTHONCASEOK",
    "PYTHONPLATLIBDIR",
    "PYTHONUSERBASE",
    "PYTHONEXECUTABLE",
    "MAKEFLAGS",
    "MFLAGS",
    "GNUMAKEFLAGS",
    "MAKEOVERRIDES",
)
EXPECTED_SCIENTIFIC_CHECKS = {
    "universal_simultaneous_amplification/phase1_directed/verify_directed_db_strong.py": 7,
    "universal_simultaneous_amplification/phase2_n4/crosscheck_full_chain.py": 6,
    "universal_simultaneous_amplification/phase2_n4/derive_lumped_certificates.py": 14,
    "universal_simultaneous_amplification/phase2_triangle/audit/independent_triangle_audit.py": 26,
    "universal_simultaneous_amplification/phase2_triangle/crosscheck_exact_solver.py": 8,
    "universal_simultaneous_amplification/phase2_triangle/derive_certificate.py": 13,
    "universal_simultaneous_amplification/phase3_asymptotic/verify_lumping.py": 2,
    "universal_simultaneous_amplification/phase4_landmark_closure/obstruction/r2_collision_closure/verify_direct_flow_screen.py": 4,
    "universal_simultaneous_amplification/phase4_landmark_closure/obstruction/r2_collision_closure/verify_fisher_route.py": 53,
    "universal_simultaneous_amplification/phase4_landmark_closure/obstruction/r2_entropy_certificate/chi_square_channel/verify_resolvent_identities.py": 13,
    "universal_simultaneous_amplification/phase4_landmark_closure/obstruction/r2_marked_lift_v2/verify_marked_lift.py": 61,
    "universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py": 42,
    "universal_simultaneous_amplification/phase5_exact_threshold/r2_determinant/verify_antisymmetric_hessian.py": 11,
    "universal_simultaneous_amplification/phase5_exact_threshold/r2_determinant/verify_complete_refresh_forest.py": 15,
    "universal_simultaneous_amplification/phase5_exact_threshold/r2_determinant/verify_hessian_sectors.py": 9,
    "universal_simultaneous_amplification/phase5_exact_threshold/r2_determinant/verify_r2_determinant.py": 7,
    "universal_simultaneous_amplification/phase5_exact_threshold/r2_determinant/verify_true_inverse_rank_symmetric_phase.py": 26,
    "universal_simultaneous_amplification/phase5_exact_threshold/r2_regular_sector/verify_local_complete_hessian.py": 18,
    "universal_simultaneous_amplification/phase5_exact_threshold/r2_standard_physical_phase/verify_physical_standard_phase.py": 56,
    "universal_simultaneous_amplification/verification/verify_obstruction.py": 15,
}
HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = HERE.parents[3]


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate-safety check fails."""


def require(condition: object, detail: str) -> None:
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(detail)


def check_runtime() -> None:
    require(
        sys.version_info[:3] == EXPECTED_PYTHON,
        f"Python 3.14.6 is required; found {sys.version.split()[0]}",
    )
    require(
        sys.flags.optimize == 0,
        "optimized Python is forbidden for certificate replay",
    )
    require(sys.flags.isolated == 1, "runtime preflight must use Python isolated mode")
    inherited = [name for name in UNSAFE_ENVIRONMENT if os.environ.get(name)]
    require(not inherited, f"unsafe inherited environment: {', '.join(inherited)}")
    print("PASS: exact unoptimized Python runtime and sanitized environment")


def check_dependencies() -> None:
    environment_root = Path(sys.prefix).resolve()
    for distribution, (module_name, expected_version) in EXPECTED_DISTRIBUTIONS.items():
        actual_version = metadata.version(distribution)
        require(
            actual_version == expected_version,
            f"{distribution} {expected_version} is required; found {actual_version}",
        )
        module = importlib.import_module(module_name)
        origin_text = getattr(module, "__file__", None)
        require(origin_text is not None, f"cannot locate imported module {module_name}")
        origin = Path(origin_text).resolve()
        require(
            origin.is_relative_to(environment_root),
            f"{module_name} imported outside the replay environment: {origin}",
        )
    print(
        "PASS: hashed-lock environment contains SymPy 1.14.0, "
        "python-flint 0.9.0, and mpmath 1.3.0"
    )


def load_bundle_manifest():
    source = PAPER / "bundle_manifest.py"
    spec = importlib.util.spec_from_file_location("paper1_bundle_manifest", source)
    require(spec is not None and spec.loader is not None, "cannot load bundle manifest")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_sources() -> None:
    manifest = load_bundle_manifest()
    python_files = 0
    explicit_checks = 0
    scientific_checks: dict[str, int] = {}
    forbidden: list[str] = []
    for relative, path in manifest.collect(REPO):
        if path.suffix != ".py":
            continue
        python_files += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(relative))
        bare = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)]
        if bare:
            forbidden.append(f"{relative}:{','.join(map(str, bare))}")
        file_checks = sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "require"
            for node in ast.walk(tree)
        )
        explicit_checks += file_checks
        name = relative.as_posix()
        if name in EXPECTED_SCIENTIFIC_CHECKS:
            scientific_checks[name] = file_checks
    require(not forbidden, "optimization-elidable assert remains: " + "; ".join(forbidden))
    require(
        scientific_checks == EXPECTED_SCIENTIFIC_CHECKS,
        "scientific check inventory mismatch: "
        f"expected {EXPECTED_SCIENTIFIC_CHECKS}; found {scientific_checks}",
    )
    print(
        f"PASS: {python_files} bundled Python files contain no bare assert; "
        f"verified 406 exact scientific and {explicit_checks} total require calls"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", action="store_true")
    parser.add_argument("--dependencies", action="store_true")
    parser.add_argument("--audit-sources", action="store_true")
    parser.add_argument("--intentional-failure", action="store_true")
    args = parser.parse_args()
    require(
        any(vars(args).values()),
        "select at least one safety check",
    )
    if args.runtime:
        check_runtime()
    if args.dependencies:
        check_dependencies()
    if args.audit_sources:
        check_sources()
    if args.intentional_failure:
        require(False, "INTENTIONAL_NEGATIVE_CONTROL: explicit false check")
    print("PAPER1_EXECUTION_SAFETY_OK")


if __name__ == "__main__":
    main()
