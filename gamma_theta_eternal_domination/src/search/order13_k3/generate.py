"""Fail-closed package generation and read-only audit for order-13 k=3 CNFs.

This module never launches a SAT solver.  ``write_run_plan`` can freeze the
exact future solver command, resource ceilings, tool bindings, and initial
checkpoint, but it likewise executes no child process.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import stat
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path

from .encoding import (
    EXPECTED_FORMULAS,
    TEMPLATES,
    build_full_encoding,
    first_use_canonical,
    row_is_template_proper,
)


SCHEMA_VERSION = 1
INSTANCE_NAME = "instance.cnf"
BANK_NAME = "coloring-bank.json"
MANIFEST_NAME = "constructor-manifest.json"
PLAN_NAME = "run-plan.json"
CHECKPOINT_NAME = "checkpoint-000000.json"
RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/search/order13_k3/__init__.py",
    "src/search/order13_k3/__main__.py",
    "src/search/order13_k3/encoding.py",
    "src/search/order13_k3/generate.py",
)


def campaign_root() -> Path:
    return Path(__file__).resolve().parents[3]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _strict_json_bytes(payload: bytes) -> object:
    def reject_constant(value: str) -> object:
        raise ValueError(f"non-finite JSON constant {value!r}")

    def reject_duplicate_keys(
        pairs: list[tuple[str, object]],
    ) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("JSON is not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("malformed JSON") from error


def _assert_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current /= component
        try:
            information = os.lstat(current)
        except FileNotFoundError:
            break
        if stat.S_ISLNK(information.st_mode):
            raise ValueError(f"symlinked path component is forbidden: {current}")


def _assert_regular_single_link(path: Path, role: str) -> None:
    _assert_no_symlink_components(path)
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise ValueError(f"{role} is missing: {path}") from error
    if not stat.S_ISREG(information.st_mode):
        raise ValueError(f"{role} is not a regular file: {path}")
    if information.st_nlink != 1:
        raise ValueError(f"{role} has multiple hard links: {path}")


def _validate_new_directory(path: Path) -> Path:
    _assert_no_symlink_components(path)
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"output directory already exists: {path}")
    parent = path.parent
    _assert_no_symlink_components(parent)
    if not parent.is_dir():
        raise ValueError(f"output parent is not a directory: {parent}")
    resolved = path.resolve(strict=False)
    root = campaign_root().resolve()
    if resolved in {Path(resolved.anchor), Path.home().resolve(), root}:
        raise ValueError(f"unsafe output directory: {resolved}")
    protected = (root / "src", root / "math", root / "tests", root / "literature")
    for directory in protected:
        try:
            resolved.relative_to(directory)
        except ValueError:
            continue
        raise ValueError(f"output lies in protected tree: {directory}")
    return resolved


def _file_binding(path: Path) -> dict[str, object]:
    _assert_regular_single_link(path, path.name)
    return {
        "name": path.name,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _source_manifest() -> tuple[tuple[str, str, int], ...]:
    root = campaign_root()
    result: list[tuple[str, str, int]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        path = root / relative
        _assert_regular_single_link(path, f"runtime source {relative}")
        result.append((relative, sha256_file(path), path.stat().st_size))
    return tuple(result)


def _source_set_sha256(
    records: Sequence[tuple[str, str, int]],
) -> str:
    payload = "".join(
        f"{relative} {digest} {size}\n"
        for relative, digest, size in records
    ).encode("ascii")
    return sha256_bytes(payload)


def _bank_bytes(rows: Sequence[Sequence[int]]) -> bytes:
    return canonical_json_bytes([list(row) for row in rows])


def _formula_census(template: str) -> tuple[object, bytes, bytes, dict[str, object]]:
    encoding = build_full_encoding(template)
    cnf_bytes = encoding.cnf.dimacs_bytes()
    bank_bytes = _bank_bytes(encoding.coloring_bank)
    expected = EXPECTED_FORMULAS[template]
    actual = {
        "variables": encoding.cnf.variable_count,
        "base_clauses": len(encoding.cnf.clauses) - len(encoding.coloring_bank),
        "base_literals": (
            encoding.cnf.literal_count
            - encoding.cnf.family_counts["complete_coloring_obstruction"][1]
        ),
        "coloring_rows": len(encoding.coloring_bank),
        "clauses": len(encoding.cnf.clauses),
        "literals": encoding.cnf.literal_count,
        "size_bytes": len(cnf_bytes),
        "sha256": sha256_bytes(cnf_bytes),
    }
    if actual != dict(expected):
        raise AssertionError(
            f"{template} formula differs from the frozen census: {actual!r}"
        )
    family_counts = {
        name: {
            "clauses": counts[0],
            "literals": counts[1],
            "clause_stream_sha256": encoding.cnf.family_sha256[name],
        }
        for name, counts in encoding.cnf.family_counts.items()
    }
    return encoding, cnf_bytes, bank_bytes, family_counts


def generate_package(
    *,
    template: str,
    output_directory: Path,
    validation_gate: object,
) -> dict[str, object]:
    """Generate a new immutable constructor package without running a solver."""

    if validation_gate is not True:
        raise PermissionError("explicit constructor validation gate is required")
    if template not in TEMPLATES:
        raise ValueError(f"unknown template {template!r}")
    output = _validate_new_directory(output_directory)
    sources = _source_manifest()
    encoding, cnf_bytes, bank_bytes, family_counts = _formula_census(template)
    manifest: dict[str, object] = {
        "schema": "gamma-theta-order13-k3-constructor-package-v1",
        "schema_version": SCHEMA_VERSION,
        "claim_boundary": (
            "Exact formula construction only. No solver was launched and this "
            "package makes no SAT or UNSAT claim."
        ),
        "template": template,
        "order": 13,
        "parameter": 3,
        "graph_variable_semantics": "edge variables encode H=complement(G)",
        "fixed_independent_triple_in_g": [0, 1, int(template[4:])],
        "heuristic_symmetry_breakers": [],
        "variable_count": encoding.cnf.variable_count,
        "clause_count": len(encoding.cnf.clauses),
        "literal_count": encoding.cnf.literal_count,
        "base_clause_count": len(encoding.cnf.clauses)
        - len(encoding.coloring_bank),
        "base_literal_count": encoding.cnf.literal_count
        - encoding.cnf.family_counts["complete_coloring_obstruction"][1],
        "coloring_row_count": len(encoding.coloring_bank),
        "clause_families": family_counts,
        "artifacts": {
            INSTANCE_NAME: {
                "sha256": sha256_bytes(cnf_bytes),
                "size_bytes": len(cnf_bytes),
            },
            BANK_NAME: {
                "sha256": sha256_bytes(bank_bytes),
                "size_bytes": len(bank_bytes),
            },
        },
        "frozen_pilot_match": {
            "matched": True,
            "expected_sha256": EXPECTED_FORMULAS[template]["sha256"],
            "expected_size_bytes": EXPECTED_FORMULAS[template]["size_bytes"],
        },
        "runtime_sources": [
            {"path": relative, "sha256": digest, "size_bytes": size}
            for relative, digest, size in sources
        ],
        "runtime_source_set_sha256": _source_set_sha256(sources),
        "generation_environment": {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        },
        "normalized_regeneration_invocation": [
            "/usr/bin/env",
            "PYTHONPATH=src",
            sys.executable,
            "-m",
            "search.order13_k3",
            "generate",
            "--template",
            template,
            "--output-directory",
            "<NEW_PACKAGE_DIRECTORY>",
            "--validation-gate",
        ],
        "normalized_audit_invocation": [
            "/usr/bin/env",
            "PYTHONPATH=src",
            sys.executable,
            "-m",
            "search.order13_k3",
            "audit",
            "--package-directory",
            "<PACKAGE_DIRECTORY>",
            "--exhaustive",
        ],
        "production_defaults": {
            "seed": 0,
            "solver_wall_seconds": 1800,
            "solver_memory_mib": 2048,
            "proof_file_limit_mib": 2048,
            "disk_reserve_mib": 8192,
            "memory_reserve_mib": 2048,
            "maximum_parallel_solver_processes": 1,
        },
    }
    manifest_bytes = canonical_json_bytes(manifest)

    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{output.name}.partial-",
            dir=output.parent,
        )
    )
    try:
        for name, payload in (
            (INSTANCE_NAME, cnf_bytes),
            (BANK_NAME, bank_bytes),
            (MANIFEST_NAME, manifest_bytes),
        ):
            with (staging / name).open("xb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
        os.replace(staging, output)
        directory_descriptor = os.open(output.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def _validate_bank(
    template: str,
    raw: object,
    *,
    exhaustive: bool,
) -> tuple[tuple[int, ...], ...]:
    if not isinstance(raw, list):
        raise ValueError("coloring bank is not a JSON list")
    rows: list[tuple[int, ...]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, list):
            raise ValueError(f"coloring row {index} is not a list")
        row = first_use_canonical(item)
        if not row_is_template_proper(template, row):
            raise ValueError(f"coloring row {index} violates a forced H-edge")
        rows.append(row)
    result = tuple(rows)
    if result != tuple(sorted(set(result))):
        raise ValueError("coloring bank is duplicated or not in lexical order")
    expected_count = EXPECTED_FORMULAS[template]["coloring_rows"]
    if len(result) != expected_count:
        raise ValueError("coloring bank count differs")
    if exhaustive and result != build_full_encoding(template).coloring_bank:
        raise ValueError("coloring bank differs from exhaustive reconstruction")
    return result


def audit_package(
    package_directory: Path,
    *,
    exhaustive: bool,
) -> dict[str, object]:
    """Audit package shape, bindings, formula census, and optionally all bytes."""

    _assert_no_symlink_components(package_directory)
    if not package_directory.is_dir():
        raise ValueError("package directory is absent")
    entries = {entry.name for entry in package_directory.iterdir()}
    expected_entries = {INSTANCE_NAME, BANK_NAME, MANIFEST_NAME}
    if entries != expected_entries:
        raise ValueError(
            f"package entries differ: {sorted(entries)} != {sorted(expected_entries)}"
        )
    paths = {name: package_directory / name for name in expected_entries}
    for name, path in paths.items():
        _assert_regular_single_link(path, f"package artifact {name}")
    manifest = _strict_json_bytes(paths[MANIFEST_NAME].read_bytes())
    if not isinstance(manifest, dict):
        raise ValueError("constructor manifest is not an object")
    if (
        manifest.get("schema")
        != "gamma-theta-order13-k3-constructor-package-v1"
        or manifest.get("schema_version") != SCHEMA_VERSION
    ):
        raise ValueError("constructor manifest schema differs")
    template = manifest.get("template")
    if template not in TEMPLATES:
        raise ValueError("manifest template differs")
    length = int(template[4:])
    if (
        manifest.get("order") != 13
        or manifest.get("parameter") != 3
        or manifest.get("graph_variable_semantics")
        != "edge variables encode H=complement(G)"
        or manifest.get("fixed_independent_triple_in_g") != [0, 1, length]
        or manifest.get("heuristic_symmetry_breakers") != []
    ):
        raise ValueError("constructor manifest semantic boundary differs")
    sources = _source_manifest()
    expected_sources = [
        {"path": relative, "sha256": digest, "size_bytes": size}
        for relative, digest, size in sources
    ]
    if (
        manifest.get("runtime_sources") != expected_sources
        or manifest.get("runtime_source_set_sha256")
        != _source_set_sha256(sources)
    ):
        raise ValueError("runtime source binding differs")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("manifest artifact bindings are absent")
    for name in (INSTANCE_NAME, BANK_NAME):
        binding = artifacts.get(name)
        if not isinstance(binding, dict):
            raise ValueError(f"manifest binding for {name} is absent")
        actual = _file_binding(paths[name])
        if (
            binding.get("sha256") != actual["sha256"]
            or binding.get("size_bytes") != actual["size_bytes"]
        ):
            raise ValueError(f"artifact binding for {name} differs")

    rows = _validate_bank(
        template,
        _strict_json_bytes(paths[BANK_NAME].read_bytes()),
        exhaustive=exhaustive,
    )
    expected = EXPECTED_FORMULAS[template]
    instance_binding = _file_binding(paths[INSTANCE_NAME])
    if (
        instance_binding["sha256"] != expected["sha256"]
        or instance_binding["size_bytes"] != expected["size_bytes"]
        or manifest.get("variable_count") != expected["variables"]
        or manifest.get("clause_count") != expected["clauses"]
        or manifest.get("literal_count") != expected["literals"]
        or manifest.get("base_clause_count") != expected["base_clauses"]
        or manifest.get("base_literal_count") != expected["base_literals"]
        or manifest.get("coloring_row_count") != expected["coloring_rows"]
    ):
        raise ValueError("formula census differs from frozen expected values")
    if exhaustive:
        encoding, expected_cnf, expected_bank, expected_families = _formula_census(
            template
        )
        if paths[INSTANCE_NAME].read_bytes() != expected_cnf:
            raise ValueError("CNF differs from fresh exact reconstruction")
        if paths[BANK_NAME].read_bytes() != expected_bank:
            raise ValueError("bank bytes differ from fresh exact reconstruction")
        if manifest.get("clause_families") != expected_families:
            raise ValueError("clause-family census differs")
        if len(rows) != len(encoding.coloring_bank):
            raise AssertionError("exhaustive bank count changed during audit")
    return {
        "accepted": True,
        "template": template,
        "instance": instance_binding,
        "coloring_rows": len(rows),
        "exhaustive_reconstruction": exhaustive,
        "solver_launched": False,
    }


def write_run_plan(
    *,
    package_directory: Path,
    output_directory: Path,
    cadical_path: Path,
    validation_gate: object,
) -> dict[str, object]:
    """Freeze one future proof-producing command and an initial checkpoint.

    This function intentionally does not execute the stored command.  A later
    proof runner must enforce the resource values and add proof checking.
    """

    if validation_gate is not True:
        raise PermissionError("explicit run-plan validation gate is required")
    report = audit_package(package_directory, exhaustive=True)
    output = _validate_new_directory(output_directory)
    _assert_regular_single_link(cadical_path, "CaDiCaL executable")
    if not os.access(cadical_path, os.X_OK):
        raise ValueError("CaDiCaL path is not executable")
    package_instance = package_directory.resolve() / INSTANCE_NAME
    instance_binding = _file_binding(package_instance)
    tool_binding = {
        "path": str(cadical_path.resolve()),
        "sha256": sha256_file(cadical_path),
        "size_bytes": cadical_path.stat().st_size,
    }
    attempt = output / "attempt-000001"
    command = [
        str(cadical_path.resolve()),
        "--seed=0",
        "--binary",
        "--no-colors",
        "-q",
        "-t",
        "1800",
        "-w",
        str(attempt / "solver.result"),
        str(attempt / INSTANCE_NAME),
        str(attempt / "proof.raw.bdrat"),
    ]
    plan: dict[str, object] = {
        "schema": "gamma-theta-order13-k3-run-plan-v1",
        "schema_version": SCHEMA_VERSION,
        "status": "READY_NOT_RUN",
        "claim_boundary": (
            "Metadata and command plan only. The command has not run; a future "
            "UNSAT claim additionally requires proof conversion and replay."
        ),
        "template": report["template"],
        "source_package": str(package_directory.resolve()),
        "instance": instance_binding,
        "tool": tool_binding,
        "hardware_at_plan_creation": {
            "machine": platform.machine(),
            "logical_cpus": os.cpu_count(),
            "physical_memory_bytes": (
                os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
            ),
            "free_disk_bytes": shutil.disk_usage(output.parent).free,
            "load_average": list(os.getloadavg()),
        },
        "limits": {
            "solver_wall_seconds": 1800,
            "solver_memory_mib": 2048,
            "proof_file_limit_mib": 2048,
            "disk_reserve_mib": 8192,
            "memory_reserve_mib": 2048,
            "load_average_maximum": 7.5,
            "parallel_processes": 1,
        },
        "solver_command": command,
        "resume_protocol": {
            "next_attempt": 1,
            "refuse_if_attempt_directory_exists": True,
            "copy_frozen_instance_into_attempt": True,
            "rehash_instance_and_tool_before_launch": True,
            "write_resource_report_before_and_after_child": True,
            "checkpoint_after_every_attempt": True,
        },
    }
    checkpoint: dict[str, object] = {
        "schema": "gamma-theta-order13-k3-run-checkpoint-v1",
        "schema_version": SCHEMA_VERSION,
        "sequence": 0,
        "status": "READY_NOT_RUN",
        "attempts": [],
        "next_attempt": 1,
        "plan_sha256": sha256_bytes(canonical_json_bytes(plan)),
    }
    staging = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.partial-", dir=output.parent)
    )
    try:
        shutil.copyfile(package_instance, staging / INSTANCE_NAME)
        with (staging / INSTANCE_NAME).open("rb") as handle:
            os.fsync(handle.fileno())
        for name, payload in (
            (PLAN_NAME, canonical_json_bytes(plan)),
            (CHECKPOINT_NAME, canonical_json_bytes(checkpoint)),
        ):
            with (staging / name).open("xb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
        os.replace(staging, output)
        directory_descriptor = os.open(output.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return plan


def census() -> dict[str, object]:
    records: list[dict[str, object]] = []
    for template in TEMPLATES:
        encoding, cnf_bytes, bank_bytes, families = _formula_census(template)
        records.append(
            {
                "template": template,
                "variables": encoding.cnf.variable_count,
                "clauses": len(encoding.cnf.clauses),
                "literals": encoding.cnf.literal_count,
                "coloring_rows": len(encoding.coloring_bank),
                "size_bytes": len(cnf_bytes),
                "sha256": sha256_bytes(cnf_bytes),
                "coloring_bank_sha256": sha256_bytes(bank_bytes),
                "clause_families": families,
            }
        )
    return {
        "schema": "gamma-theta-order13-k3-constructor-census-v1",
        "schema_version": SCHEMA_VERSION,
        "classification": "CONSTRUCTOR_GATE_ONLY",
        "solver_launched": False,
        "templates": records,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    generate = commands.add_parser("generate")
    generate.add_argument("--template", choices=TEMPLATES, required=True)
    generate.add_argument("--output-directory", type=Path, required=True)
    generate.add_argument("--validation-gate", action="store_true")

    audit = commands.add_parser("audit")
    audit.add_argument("--package-directory", type=Path, required=True)
    audit.add_argument("--exhaustive", action="store_true")

    plan = commands.add_parser("plan")
    plan.add_argument("--package-directory", type=Path, required=True)
    plan.add_argument("--output-directory", type=Path, required=True)
    plan.add_argument("--cadical", type=Path, required=True)
    plan.add_argument("--validation-gate", action="store_true")

    commands.add_parser("census")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command == "generate":
        result = generate_package(
            template=arguments.template,
            output_directory=arguments.output_directory,
            validation_gate=arguments.validation_gate,
        )
    elif arguments.command == "audit":
        result = audit_package(
            arguments.package_directory,
            exhaustive=arguments.exhaustive,
        )
    elif arguments.command == "plan":
        result = write_run_plan(
            package_directory=arguments.package_directory,
            output_directory=arguments.output_directory,
            cadical_path=arguments.cadical,
            validation_gate=arguments.validation_gate,
        )
    elif arguments.command == "census":
        result = census()
    else:
        raise AssertionError("unreachable command")
    print(json.dumps(result, allow_nan=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
