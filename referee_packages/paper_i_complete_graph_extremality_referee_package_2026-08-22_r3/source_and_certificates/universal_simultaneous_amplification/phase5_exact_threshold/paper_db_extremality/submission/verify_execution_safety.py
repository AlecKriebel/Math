#!/usr/bin/env python3
"""Fail-closed runtime, dependency, and source checks for Paper I replay."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import importlib.metadata as metadata
import importlib.util
import os
from pathlib import Path, PurePosixPath
import re
import stat
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
HEX64 = re.compile(r"[0-9a-f]{64}")


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


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def parse_manifest(path: Path) -> dict[PurePosixPath, str]:
    expected: dict[PurePosixPath, str] = {}
    for number, line in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        try:
            claimed, raw_name = line.split("  ", 1)
        except ValueError as exc:
            raise CertificateFailure(
                f"{path.name}:{number}: malformed manifest line"
            ) from exc
        name = PurePosixPath(raw_name)
        require(
            HEX64.fullmatch(claimed) is not None,
            f"{path.name}:{number}: malformed SHA-256",
        )
        require(
            not name.is_absolute()
            and ".." not in name.parts
            and name.as_posix() == raw_name,
            f"{path.name}:{number}: unsafe or noncanonical path",
        )
        require(name not in expected, f"{path.name}:{number}: duplicate path")
        require(
            name != PurePosixPath("MANIFEST.sha256"),
            "the internal manifest must not list itself",
        )
        expected[name] = claimed
    require(expected, f"{path.name}: empty manifest")
    return expected


def implied_directories(files: set[PurePosixPath]) -> set[PurePosixPath]:
    directories: set[PurePosixPath] = set()
    for name in files:
        parent = name.parent
        while parent != PurePosixPath("."):
            directories.add(parent)
            parent = parent.parent
    return directories


def inspect_tree(root: Path) -> tuple[set[PurePosixPath], set[PurePosixPath]]:
    require(root.is_absolute(), f"bundle root must be absolute: {root}")
    root_stat = root.lstat()
    require(stat.S_ISDIR(root_stat.st_mode), f"bundle root is not a directory: {root}")

    files: set[PurePosixPath] = set()
    directories: set[PurePosixPath] = set()

    def visit(directory: Path, relative_directory: PurePosixPath) -> None:
        with os.scandir(directory) as entries:
            for entry in entries:
                relative = (
                    PurePosixPath(entry.name)
                    if relative_directory == PurePosixPath(".")
                    else relative_directory / entry.name
                )
                details = entry.stat(follow_symlinks=False)
                mode = details.st_mode
                require(
                    not stat.S_ISLNK(mode),
                    f"bundle tree contains a symlink: {relative}",
                )
                if stat.S_ISDIR(mode):
                    require(
                        entry.name.casefold() != "__pycache__",
                        f"bundle tree contains a forbidden bytecode/cache directory: {relative}",
                    )
                    directories.add(relative)
                    visit(Path(entry.path), relative)
                elif stat.S_ISREG(mode):
                    require(
                        relative.suffix.casefold() not in {".pyc", ".pyo"},
                        f"bundle tree contains forbidden bytecode: {relative}",
                    )
                    files.add(relative)
                else:
                    raise CertificateFailure(
                        f"bundle tree contains a special node: {relative}"
                    )

    visit(root, PurePosixPath("."))
    return files, directories


def check_bundle_tree(root: Path) -> dict[PurePosixPath, str]:
    root = root.absolute()
    root_details = root.lstat()
    require(
        stat.S_ISDIR(root_details.st_mode),
        f"bundle root is not a regular directory: {root}",
    )
    root = root.resolve(strict=True)
    actual_files, actual_directories = inspect_tree(root)
    manifest_path = root / "MANIFEST.sha256"
    require(manifest_path.is_file(), f"missing internal manifest: {manifest_path}")
    expected = parse_manifest(manifest_path)
    expected_files = set(expected) | {PurePosixPath("MANIFEST.sha256")}
    expected_directories = implied_directories(expected_files)
    missing_files = sorted(str(path) for path in expected_files - actual_files)
    unexpected_files = sorted(str(path) for path in actual_files - expected_files)
    missing_directories = sorted(
        str(path) for path in expected_directories - actual_directories
    )
    unexpected_directories = sorted(
        str(path) for path in actual_directories - expected_directories
    )
    require(
        actual_files == expected_files and actual_directories == expected_directories,
        "bundle tree node-set mismatch; "
        f"missing_files={missing_files}, unexpected_files={unexpected_files}, "
        f"missing_directories={missing_directories}, "
        f"unexpected_directories={unexpected_directories}",
    )
    for name, claimed in expected.items():
        require(digest(root / name) == claimed, f"bundle tree hash mismatch: {name}")
    print(
        f"PASS: exact bundle tree contains {len(actual_files)} regular files, "
        f"{len(actual_directories)} implied directories, no links/special nodes, "
        "and no bytecode/cache entries"
    )
    return expected


def check_cache_prefix(expected: Path) -> None:
    expected = expected.resolve(strict=True)
    actual_text = sys.pycache_prefix
    require(actual_text is not None, "controlled bytecode-cache prefix is not active")
    require(
        Path(actual_text).resolve() == expected,
        f"wrong bytecode-cache prefix: expected {expected}; found {actual_text}",
    )
    require(
        sys.flags.dont_write_bytecode == 1,
        "certificate interpreter must disable bytecode writes",
    )
    require(not any(expected.iterdir()), f"controlled cache is not empty: {expected}")
    print(f"PASS: fresh private bytecode-cache prefix is active and empty: {expected}")


def load_bundle_manifest():
    source = PAPER / "bundle_manifest.py"
    spec = importlib.util.spec_from_file_location("paper1_bundle_manifest", source)
    require(spec is not None and spec.loader is not None, "cannot load bundle manifest")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_sources(
    verified_manifest: dict[PurePosixPath, str] | None = None,
    bundle_root: Path = REPO,
) -> None:
    if verified_manifest is None:
        manifest = load_bundle_manifest()
        candidates = manifest.collect(REPO)
    else:
        candidates = [
            (relative, bundle_root / relative)
            for relative in sorted(
                verified_manifest,
                key=lambda path: path.as_posix(),
            )
        ]
    python_files = 0
    explicit_checks = 0
    scientific_checks: dict[str, int] = {}
    forbidden: list[str] = []
    for relative, path in candidates:
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
    parser.add_argument("--bundle-root", type=Path)
    parser.add_argument("--expected-cache-prefix", type=Path)
    args = parser.parse_args()
    require(
        any(vars(args).values()),
        "select at least one safety check",
    )
    if args.runtime:
        check_runtime()
    if args.expected_cache_prefix:
        check_cache_prefix(args.expected_cache_prefix)
    verified_manifest = None
    bundle_root = REPO
    if args.bundle_root:
        bundle_root = args.bundle_root.resolve(strict=True)
        verified_manifest = check_bundle_tree(bundle_root)
    if args.dependencies:
        check_dependencies()
    if args.audit_sources:
        check_sources(verified_manifest, bundle_root)
    if args.intentional_failure:
        require(False, "INTENTIONAL_NEGATIVE_CONTROL: explicit false check")
    if args.expected_cache_prefix:
        check_cache_prefix(args.expected_cache_prefix)
    print("PASS: Paper I execution-safety checks completed")


if __name__ == "__main__":
    main()
