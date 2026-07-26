#!/usr/bin/env python3
"""Produce a source-bound proof certificate for the frozen DoubleLex CNF.

This program never invokes a SAT solver and never writes into the frozen
instance, theorem, source, test, review, or raw-result trees.  It checks the
exact frozen inputs, runs one bounded proof-processing child at a time under
the campaign-wide heavy-child lock, and publishes a certificate only after:

1. strict full-stream binary DRAT normalization to additions only;
2. warning-fatal RUP-only forward replay of the normalized stream;
3. warning-fatal RUP-only backward conversion to LRAT; and
4. fresh replay by the separately pinned lrat-check executable.

The resulting status is deliberately pending independent hostile review.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Mapping, Sequence


SCRIPT = Path(__file__).resolve()
PACKAGE = SCRIPT.parents[1]
ROOT = SCRIPT.parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from synthesis_k3.cegar import RunLock, run_bounded_child  # noqa: E402


SCHEMA_VERSION = 1
VARIABLE_COUNT = 18_381
CLAUSE_COUNT = 115_507
LITERAL_COUNT = 1_190_774
WALL_LIMIT_SECONDS = 3_600
MEMORY_LIMIT_MIB = 2_048
FILE_LIMIT_MIB = 2_048
MINIMUM_FREE_DISK_BYTES = 8 << 30

FORMULA = ROOT / "instances/order12_k4_connected_doublelex/instance.cnf"
FORMULA_MANIFEST = (
    ROOT / "instances/order12_k4_connected_doublelex/manifest.json"
)
RAW_PROOF = ROOT / "results/order12_k4_doublelex_seed0/proof.raw.bdrat"
SOLVER_RESULT = ROOT / "results/order12_k4_doublelex_seed0/solver.result"
THEOREM = ROOT / "math/lemmas/order12_k4_doublelex.md"
GENERATOR = ROOT / "src/search/k4_doublelex.py"
GENERATOR_TESTS = ROOT / "tests/test_k4_doublelex.py"
HOSTILE_REVIEW = ROOT / "reviews/order12_k4_doublelex_hostile_review.md"
HOSTILE_PROBE = ROOT / "reviews/order12_k4_doublelex_hostile_probe.py"
HOSTILE_EVIDENCE = ROOT / "reviews/order12_k4_doublelex_hostile_probe.json"
NORMALIZER = ROOT / "src/search/k4_production/normalize_bdrat.py"
CHILD_ORCHESTRATOR = ROOT / "src/synthesis_k3/cegar.py"
DRAT_TRIM = ROOT / "tools/drat_trim_2023_05_22/drat-trim"
LRAT_CHECK = ROOT / "tools/drat_trim_2023_05_22/lrat-check"
DRAT_ARCHIVE = ROOT / "tools/drat_trim_2023_05_22.tar.gz"

EXPECTED_HASHES: Mapping[Path, str] = {
    FORMULA: "14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7",
    FORMULA_MANIFEST: "4ca0b1d43c145acf35f7545b7a85e5d0aafa62e7279c120212455985312cba96",
    RAW_PROOF: "ed3975c5f0cfbe9475c607e440c0ddc012722d0fe68b797e693149fd6f7d5c51",
    SOLVER_RESULT: "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162",
    THEOREM: "d5be9b6373d7aa7c49dec32c18c6202698b35fe05a1f58b2b97dcc98d9114a76",
    GENERATOR: "e5aeb23eb3938631c62a29df45a880839fa9c8384121e0ec310d9740936baba1",
    GENERATOR_TESTS: "36282f747f971cf5a57c90e1b645fbe2cd76ab51c3413b7b2268547144322469",
    NORMALIZER: "07229fce9293a05fed3fa6ef3f96415eb48ea4b0cdd8e9a329620017d2bced99",
    CHILD_ORCHESTRATOR: "411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c",
    DRAT_TRIM: "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb",
    LRAT_CHECK: "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2",
    DRAT_ARCHIVE: "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108",
}

EXPECTED_SIZES: Mapping[Path, int] = {
    FORMULA: 4_030_657,
    FORMULA_MANIFEST: 1_051,
    RAW_PROOF: 32_987_136,
    SOLVER_RESULT: 16,
}

PROOF_DIRECTORY = PACKAGE / "proof"
LOG_DIRECTORY = PACKAGE / "logs"
RESOURCE_DIRECTORY = PACKAGE / "resources"
NORMALIZED_PROOF = PROOF_DIRECTORY / "proof.normalized.rup.bdrat"
LRAT_PROOF = PROOF_DIRECTORY / "proof.converted.lrat"
NORMALIZATION_REPORT = PROOF_DIRECTORY / "normalization-report.json"
ARTIFACT_MANIFEST = PACKAGE / "artifact-manifest.json"
CERTIFICATE = PACKAGE / "certificate.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_new(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    completed = False
    try:
        with os.fdopen(descriptor, "wb", buffering=0) as handle:
            handle.write(payload)
            os.fsync(handle.fileno())
        completed = True
        fsync_directory(path.parent)
    finally:
        if not completed:
            try:
                path.unlink()
            except FileNotFoundError:
                pass


def write_new_json(path: Path, value: object) -> None:
    write_new(path, canonical_json_bytes(value))


def assert_regular_single_link(path: Path, role: str) -> os.stat_result:
    supplied = path.absolute()
    if supplied.is_symlink():
        raise ValueError(f"{role} path is a symlink")
    metadata = path.lstat()
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
        raise ValueError(f"{role} is not a single-link regular file")
    return metadata


def binding(path: Path, role: str) -> dict[str, object]:
    metadata = assert_regular_single_link(path, role)
    return {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "size_bytes": metadata.st_size,
    }


def assert_frozen_inputs() -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for path, expected_hash in EXPECTED_HASHES.items():
        record = binding(path, f"frozen input {path.relative_to(ROOT)}")
        if record["sha256"] != expected_hash:
            raise ValueError(
                f"frozen input hash mismatch for {path}: "
                f"{record['sha256']} != {expected_hash}"
            )
        expected_size = EXPECTED_SIZES.get(path)
        if expected_size is not None and record["size_bytes"] != expected_size:
            raise ValueError(
                f"frozen input size mismatch for {path}: "
                f"{record['size_bytes']} != {expected_size}"
            )
        records[str(path.relative_to(ROOT))] = record
    for path in (HOSTILE_REVIEW, HOSTILE_PROBE, HOSTILE_EVIDENCE):
        records[str(path.relative_to(ROOT))] = binding(
            path, f"hostile-review input {path.relative_to(ROOT)}"
        )
    if SOLVER_RESULT.read_bytes() != b"s UNSATISFIABLE\n":
        raise ValueError("solver result is not the exact UNSATISFIABLE record")
    return records


def parse_exact_dimacs(path: Path) -> dict[str, int]:
    variable_bound: int | None = None
    declared_clauses: int | None = None
    clauses = 0
    literals = 0
    maximum_variable = 0
    saw_header = False
    with path.open("rb") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            try:
                line = raw_line.decode("ascii")
            except UnicodeDecodeError as error:
                raise ValueError(
                    f"DIMACS line {line_number} is not ASCII"
                ) from error
            stripped = line.strip()
            if not stripped or stripped.startswith("c"):
                continue
            fields = stripped.split()
            if fields[0] == "p":
                if saw_header or fields[:2] != ["p", "cnf"] or len(fields) != 4:
                    raise ValueError("malformed or repeated DIMACS header")
                variable_bound = int(fields[2])
                declared_clauses = int(fields[3])
                if variable_bound < 1 or declared_clauses < 1:
                    raise ValueError("nonpositive DIMACS census")
                saw_header = True
                continue
            if not saw_header or variable_bound is None:
                raise ValueError("DIMACS clause precedes its header")
            values = [int(field) for field in fields]
            if not values or values[-1] != 0 or 0 in values[:-1]:
                raise ValueError(
                    f"DIMACS line {line_number} is not one complete clause"
                )
            for literal in values[:-1]:
                variable = abs(literal)
                if variable < 1 or variable > variable_bound:
                    raise ValueError(
                        f"DIMACS line {line_number} has out-of-range literal"
                    )
                maximum_variable = max(maximum_variable, variable)
            clauses += 1
            literals += len(values) - 1
    if (
        not saw_header
        or variable_bound != VARIABLE_COUNT
        or declared_clauses != CLAUSE_COUNT
        or clauses != CLAUSE_COUNT
        or literals != LITERAL_COUNT
        or maximum_variable != VARIABLE_COUNT
    ):
        raise ValueError(
            "DIMACS census mismatch: "
            f"variables={variable_bound}, declared={declared_clauses}, "
            f"clauses={clauses}, literals={literals}, max={maximum_variable}"
        )
    return {
        "variable_count": variable_bound,
        "clause_count": clauses,
        "literal_count": literals,
        "maximum_variable_observed": maximum_variable,
    }


def child_passed(child: object) -> bool:
    return (
        getattr(child, "exit_code") == 0
        and getattr(child, "termination_signal") is None
        and getattr(child, "timed_out") is False
        and getattr(child, "memory_limit_exceeded") is False
    )


def run_phase(
    name: str,
    command: Sequence[str],
    readonly_paths: Mapping[str, Path],
) -> dict[str, object]:
    stdout_path = LOG_DIRECTORY / f"{name}.stdout"
    stderr_path = LOG_DIRECTORY / f"{name}.stderr"
    child = run_bounded_child(
        command=tuple(command),
        cwd=ROOT,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        wall_limit_seconds=WALL_LIMIT_SECONDS,
        memory_limit_mib=MEMORY_LIMIT_MIB,
        file_limit_mib=FILE_LIMIT_MIB,
        readonly_paths=readonly_paths,
    )
    record = {
        "schema": "gamma-theta-doublelex-proof-child-resource-v1",
        "schema_version": 1,
        "phase": name,
        "passed": child_passed(child),
        "child": asdict(child),
    }
    write_new_json(RESOURCE_DIRECTORY / f"resource-{name}.json", record)
    if not child_passed(child):
        raise RuntimeError(f"{name} did not exit cleanly")
    if assert_regular_single_link(stderr_path, f"{name} stderr").st_size != 0:
        raise RuntimeError(f"{name} emitted stderr")
    return record


def require_verified_output(path: Path, marker: bytes, role: str) -> None:
    payload = path.read_bytes().replace(b"\r", b"")
    if marker not in payload:
        raise RuntimeError(f"{role} lacks its verification marker")
    lowered = payload.lower()
    if b"warning" in lowered or b"error" in lowered or b"not verified" in lowered:
        raise RuntimeError(f"{role} contains a warning/error marker")


def output_bindings() -> dict[str, dict[str, object]]:
    paths = {
        "normalized_binary_rup": NORMALIZED_PROOF,
        "converted_lrat": LRAT_PROOF,
        "normalization_report": NORMALIZATION_REPORT,
    }
    for name in (
        "normalizer",
        "normalized-forward-rup",
        "backward-lrat-conversion-rup",
        "lrat-check",
    ):
        paths[f"{name}_stdout"] = LOG_DIRECTORY / f"{name}.stdout"
        paths[f"{name}_stderr"] = LOG_DIRECTORY / f"{name}.stderr"
        paths[f"{name}_resource"] = (
            RESOURCE_DIRECTORY / f"resource-{name}.json"
        )
    return {
        name: binding(path, f"certificate output {name}")
        for name, path in sorted(paths.items())
    }


def preserved_failure_bindings() -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for directory in sorted(PACKAGE.glob("failed-attempt-*")):
        if not directory.is_dir() or directory.is_symlink():
            raise ValueError(f"malformed preserved attempt: {directory}")
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                relative = str(path.relative_to(PACKAGE))
                records[relative] = binding(
                    path, f"preserved failed-attempt artifact {relative}"
                )
    return records


def main() -> int:
    if ROOT.name != "gamma_theta_eternal_domination":
        raise ValueError(f"unexpected campaign root: {ROOT}")
    PACKAGE.mkdir(parents=True, exist_ok=True)
    if PACKAGE.is_symlink():
        raise ValueError("certificate package path is a symlink")
    for directory in (PROOF_DIRECTORY, LOG_DIRECTORY, RESOURCE_DIRECTORY):
        directory.mkdir(parents=True, exist_ok=True)
        if directory.is_symlink():
            raise ValueError(f"output directory is a symlink: {directory}")
    for path in (
        NORMALIZED_PROOF,
        LRAT_PROOF,
        NORMALIZATION_REPORT,
        ARTIFACT_MANIFEST,
        CERTIFICATE,
    ):
        if path.exists() or path.is_symlink():
            raise ValueError(f"refusing to replace output: {path}")
    if shutil.disk_usage(PACKAGE).free < MINIMUM_FREE_DISK_BYTES:
        raise RuntimeError("free-disk gate failed")

    frozen_before = assert_frozen_inputs()
    dimacs_census = parse_exact_dimacs(FORMULA)
    script_binding = binding(SCRIPT, "certificate producer")
    git_head_process = subprocess.run(
        ("git", "-C", str(ROOT), "rev-parse", "HEAD"),
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={},
    )
    git_head = git_head_process.stdout.decode("ascii").strip()

    with RunLock(PACKAGE):
        normalizer_record = run_phase(
            "normalizer",
            (
                str(Path(sys.executable).resolve()),
                str(NORMALIZER.resolve()),
                "--input",
                str(RAW_PROOF.resolve()),
                "--output",
                str(NORMALIZED_PROOF.resolve()),
                "--report",
                str(NORMALIZATION_REPORT.resolve()),
                "--max-variable",
                str(VARIABLE_COUNT),
            ),
            {
                "raw proof": RAW_PROOF,
                "normalizer source": NORMALIZER,
            },
        )
        report = json.loads(NORMALIZATION_REPORT.read_text(encoding="utf-8"))
        if (
            report.get("schema")
            != "gamma-theta-order12-k4-binary-drat-normalization-v1"
            or report.get("policy")
            != "canonical-additions-only-unique-empty-full-stream-v1"
            or report.get("claim_status")
            != "TRANSFORMATION_ONLY_NO_PROOF_CLAIM"
            or report.get("max_variable_allowed") != VARIABLE_COUNT
            or report.get("input", {}).get("sha256")
            != EXPECTED_HASHES[RAW_PROOF]
            or report.get("output", {}).get("sha256")
            != sha256_file(NORMALIZED_PROOF)
            or type(report.get("empty_addition_record_index")) is not int
            or report["empty_addition_record_index"] < 1
        ):
            raise RuntimeError("strict normalization report is malformed")

        normalized_record = run_phase(
            "normalized-forward-rup",
            (
                str(DRAT_TRIM.resolve()),
                str(FORMULA.resolve()),
                str(NORMALIZED_PROOF.resolve()),
                "-i",
                "-f",
                "-W",
                "-U",
                "-t",
                str(WALL_LIMIT_SECONDS),
            ),
            {
                "formula": FORMULA,
                "normalized binary RUP": NORMALIZED_PROOF,
            },
        )
        require_verified_output(
            LOG_DIRECTORY / "normalized-forward-rup.stdout",
            b"s VERIFIED",
            "normalized forward RUP replay",
        )

        conversion_record = run_phase(
            "backward-lrat-conversion-rup",
            (
                str(DRAT_TRIM.resolve()),
                str(FORMULA.resolve()),
                str(NORMALIZED_PROOF.resolve()),
                "-i",
                "-W",
                "-U",
                "-L",
                str(LRAT_PROOF.resolve()),
                "-t",
                str(WALL_LIMIT_SECONDS),
            ),
            {
                "formula": FORMULA,
                "normalized binary RUP": NORMALIZED_PROOF,
            },
        )
        require_verified_output(
            LOG_DIRECTORY / "backward-lrat-conversion-rup.stdout",
            b"s VERIFIED",
            "backward LRAT conversion",
        )

        checker_record = run_phase(
            "lrat-check",
            (
                str(LRAT_CHECK.resolve()),
                str(FORMULA.resolve()),
                str(LRAT_PROOF.resolve()),
            ),
            {
                "formula": FORMULA,
                "converted LRAT": LRAT_PROOF,
            },
        )
        require_verified_output(
            LOG_DIRECTORY / "lrat-check.stdout",
            b"c VERIFIED",
            "fresh LRAT replay",
        )

    frozen_after = assert_frozen_inputs()
    if frozen_after != frozen_before:
        raise RuntimeError("a frozen input changed during certification")
    if shutil.disk_usage(PACKAGE).free < MINIMUM_FREE_DISK_BYTES:
        raise RuntimeError("post-run free-disk gate failed")

    outputs = output_bindings()
    failed_attempts = preserved_failure_bindings()
    artifact_manifest = {
        "schema": "gamma-theta-order12-k4-doublelex-artifact-manifest-v1",
        "schema_version": SCHEMA_VERSION,
        "status": "PIPELINE_PASSED_PENDING_INDEPENDENT_HOSTILE_REVIEW",
        "claim_boundary": (
            "Exact DoubleLex CNF proof-chain evidence only; no campaign claim "
            "until independent hostile acceptance"
        ),
        "git_head_observed": git_head,
        "producer": script_binding,
        "frozen_inputs_before_and_after": frozen_after,
        "dimacs_census": dimacs_census,
        "normalization": report,
        "outputs": outputs,
        "preserved_failed_attempts": failed_attempts,
        "limits": {
            "wall_seconds_per_child": WALL_LIMIT_SECONDS,
            "memory_mib_per_child": MEMORY_LIMIT_MIB,
            "file_mib_per_child": FILE_LIMIT_MIB,
            "minimum_free_disk_bytes": MINIMUM_FREE_DISK_BYTES,
        },
    }
    write_new_json(ARTIFACT_MANIFEST, artifact_manifest)
    manifest_binding = binding(ARTIFACT_MANIFEST, "artifact manifest")

    certificate = {
        "schema": "gamma-theta-order12-k4-doublelex-lrat-certificate-v1",
        "schema_version": SCHEMA_VERSION,
        "status": "UNSAT_LRAT_VERIFIED_PENDING_INDEPENDENT_HOSTILE_REVIEW",
        "claim_boundary": (
            "This source-bound package verifies only that the exact "
            "DoubleLex-strengthened CNF is UNSAT. The accepted DoubleLex "
            "theorem is needed to transfer this to the exact anchored parent; "
            "no universal conjecture-resolution claim is made."
        ),
        "proof_pipeline": (
            "strict-full-binary-parse-additions-only-normalization;"
            "normalized-forward-rup-warning-fatal;"
            "backward-rup-lrat-warning-fatal;"
            "fresh-independent-lrat-check"
        ),
        "formula": frozen_after[
            "instances/order12_k4_connected_doublelex/instance.cnf"
        ],
        "formula_manifest": frozen_after[
            "instances/order12_k4_connected_doublelex/manifest.json"
        ],
        "doublelex_theorem": frozen_after[
            "math/lemmas/order12_k4_doublelex.md"
        ],
        "generator_source": frozen_after["src/search/k4_doublelex.py"],
        "generator_tests": frozen_after["tests/test_k4_doublelex.py"],
        "accepted_doublelex_hostile_review": frozen_after[
            "reviews/order12_k4_doublelex_hostile_review.md"
        ],
        "accepted_doublelex_hostile_probe": frozen_after[
            "reviews/order12_k4_doublelex_hostile_probe.py"
        ],
        "accepted_doublelex_hostile_evidence": frozen_after[
            "reviews/order12_k4_doublelex_hostile_probe.json"
        ],
        "raw_solver_result": frozen_after[
            "results/order12_k4_doublelex_seed0/solver.result"
        ],
        "raw_binary_drat": frozen_after[
            "results/order12_k4_doublelex_seed0/proof.raw.bdrat"
        ],
        "normalizer_source": frozen_after[
            "src/search/k4_production/normalize_bdrat.py"
        ],
        "bounded_child_orchestrator_source": frozen_after[
            "src/synthesis_k3/cegar.py"
        ],
        "drat_trim_binary": frozen_after[
            "tools/drat_trim_2023_05_22/drat-trim"
        ],
        "lrat_check_binary": frozen_after[
            "tools/drat_trim_2023_05_22/lrat-check"
        ],
        "checker_source_archive": frozen_after[
            "tools/drat_trim_2023_05_22.tar.gz"
        ],
        "dimacs_census": dimacs_census,
        "normalization_report": outputs["normalization_report"],
        "normalized_binary_rup": outputs["normalized_binary_rup"],
        "converted_lrat": outputs["converted_lrat"],
        "phase_resources": {
            "normalizer": normalizer_record,
            "normalized_forward_rup": normalized_record,
            "backward_lrat_conversion_rup": conversion_record,
            "lrat_check": checker_record,
        },
        "artifact_manifest": manifest_binding,
        "producer": script_binding,
        "git_head_observed": git_head,
    }
    write_new_json(CERTIFICATE, certificate)
    print(
        json.dumps(
            {
                "status": certificate["status"],
                "certificate": binding(CERTIFICATE, "certificate"),
                "artifact_manifest": manifest_binding,
                "normalized_binary_rup": outputs["normalized_binary_rup"],
                "converted_lrat": outputs["converted_lrat"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
