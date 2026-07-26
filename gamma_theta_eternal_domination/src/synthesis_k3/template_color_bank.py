"""Exact template-compatible three-coloring banks and proof runs.

This module is an isolated alternative to the one-cut-at-a-time CEGAR loop.
Importing it has no side effects.  Generation and solving both require an
explicit validation gate and refuse to overwrite any output directory.

The only imported synthesis semantics are the frozen base encoding and its
same-color clause constructor.  Pinned-tool verification, strict DIMACS/model
parsing, and the campaign-global bounded-child runner are reused from
``synthesis_k3.cegar`` as low-level controls; no CEGAR search state or
transition logic is reused.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
from dataclasses import asdict
from itertools import product
from pathlib import Path
from typing import Mapping, Sequence

from .cegar import (
    CADICAL_BINARY_SHA256,
    DRAT_TRIM_BINARY_SHA256,
    ChildResult,
    parse_dimacs_bytes,
    parse_solver_result_file,
    run_bounded_child,
    validate_model_satisfies_cnf,
    verify_pinned_tools,
)
from .encoding import N, build_k3_encoding, same_color_cut, validate_decoded_candidate


SCHEMA_VERSION = 1
BANK_TEMPLATES = ("hole5", "hole7", "hole9")
EXPECTED_BANK_COUNTS: Mapping[str, int] = {
    "hole5": 3_645,
    "hole7": 1_701,
    "hole9": 765,
}
EXPECTED_CNF_COUNTS: Mapping[str, tuple[int, int, int]] = {
    # variable count, clause count, literal count
    "hole5": (6_886, 23_653, 188_959),
    "hole7": (6_886, 21_718, 148_551),
    "hole9": (6_886, 20_795, 129_559),
}
EXPECTED_BASE_CNF_COUNTS: Mapping[str, tuple[int, int, int]] = {
    # variable count, clause count, literal count
    "hole5": (6_886, 20_008, 114_601),
    "hole7": (6_886, 20_017, 114_612),
    "hole9": (6_886, 20_030, 114_619),
}
BANK_NAME = "coloring_bank.json"
CNF_NAME = "instance.cnf"
MANIFEST_NAME = "manifest.json"
RUN_CONFIG_NAME = "run_config.json"
OUTCOME_NAME = "outcome.json"
RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/synthesis_k3/__init__.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/cegar.py",
    "src/synthesis_k3/template_color_bank.py",
    "math/synthesis_k3_cegar_design.md",
    "math/synthesis_k3_cegar_protocol.md",
    "math/lemmas/template_coloring_bank.md",
)


def campaign_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
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


def _reject_constant(value: str) -> object:
    raise ValueError(f"non-finite JSON constant {value!r}")


def _object_without_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def strict_json_bytes(payload: bytes) -> object:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("JSON artifact is not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as error:
        raise ValueError("malformed JSON artifact") from error


def _require_gate(validation_gate: object) -> None:
    if validation_gate is not True:
        raise PermissionError("explicit validation gate is required")


def _positive_exact_int(value: object, role: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{role} must be a positive exact integer")
    return value


def _nonnegative_exact_int(value: object, role: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{role} must be a nonnegative exact integer")
    return value


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


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
        raise ValueError(f"{role} has {information.st_nlink} hard links: {path}")


def _path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(directory.resolve(strict=False))
    except ValueError:
        return False
    return True


def _validate_new_output_directory(path: Path) -> Path:
    """Resolve a nonexisting output below a real, nonsymlinked parent."""

    if not isinstance(path, Path):
        raise ValueError("output directory must be a pathlib.Path")
    _assert_no_symlink_components(path)
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"output directory already exists: {path}")
    parent = path.parent
    _assert_no_symlink_components(parent)
    try:
        parent_information = os.lstat(parent)
    except FileNotFoundError as error:
        raise ValueError(f"output parent is missing: {parent}") from error
    if not stat.S_ISDIR(parent_information.st_mode):
        raise ValueError(f"output parent is not a directory: {parent}")
    resolved = path.resolve(strict=False)
    root = campaign_root().resolve()
    forbidden_exact = {
        Path(resolved.anchor),
        Path.home().resolve(),
        root,
    }
    if resolved in forbidden_exact:
        raise ValueError(f"unsafe output directory: {resolved}")
    if _path_is_within(root, resolved):
        raise ValueError(f"output directory contains campaign root: {resolved}")
    for protected in (
        root / "src",
        root / "math",
        root / "tests",
        root / "tools",
        root / "literature",
    ):
        if resolved == protected or _path_is_within(resolved, protected):
            raise ValueError(f"output lies in protected tree {protected}")
    return resolved


def _validate_readonly_package_directory(path: Path) -> Path:
    _assert_no_symlink_components(path)
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise ValueError(f"package directory is missing: {path}") from error
    if not stat.S_ISDIR(information.st_mode):
        raise ValueError(f"package path is not a directory: {path}")
    resolved = path.resolve(strict=True)
    names = {entry.name for entry in resolved.iterdir()}
    expected = {BANK_NAME, CNF_NAME, MANIFEST_NAME}
    if names != expected:
        raise ValueError(
            f"package entries differ: found {sorted(names)}, expected {sorted(expected)}"
        )
    for name in expected:
        _assert_regular_single_link(resolved / name, f"package artifact {name}")
    return resolved


def _write_new_file(path: Path, payload: bytes) -> None:
    _assert_no_symlink_components(path.parent)
    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def _artifact_record(path: Path) -> dict[str, object]:
    _assert_regular_single_link(path, path.name)
    return {
        "path": path.name,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _require_exact_keys(
    value: object,
    expected: set[str],
    role: str,
) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ValueError(f"{role} has an unexpected object shape")
    return value


def template_length(template: str) -> int:
    if template not in BANK_TEMPLATES:
        raise ValueError(f"unsupported coloring-bank template {template!r}")
    return int(template[4:])


def positive_template_edges(template: str) -> tuple[tuple[int, int], ...]:
    """Return exactly the forced-true H-edges relevant to coloring."""

    length = template_length(template)
    edges = {
        tuple(sorted((vertex, (vertex + 1) % length)))
        for vertex in range(length)
    }
    edges.add((0, length))
    edges.add((1, length))
    return tuple(sorted(edges))


def first_use_canonical(row: Sequence[int]) -> tuple[int, ...]:
    """Validate and return a three-color restricted-growth string."""

    if len(row) != N:
        raise ValueError(f"expected a {N}-vertex coloring row")
    result: list[int] = []
    maximum = -1
    for index, color in enumerate(row):
        if type(color) is not int or color not in (0, 1, 2):
            raise ValueError(f"row color {index} is not an exact integer in 0..2")
        if color > maximum + 1:
            raise ValueError("row is not first-use canonical")
        result.append(color)
        maximum = max(maximum, color)
    return tuple(result)


def canonicalize_color_names(row: Sequence[int]) -> tuple[int, ...]:
    if len(row) != N or any(
        type(color) is not int or color not in (0, 1, 2) for color in row
    ):
        raise ValueError("malformed labeled three-color row")
    names: dict[int, int] = {}
    result: list[int] = []
    for color in row:
        if color not in names:
            names[color] = len(names)
        result.append(names[color])
    return tuple(result)


def row_is_template_proper(template: str, row: Sequence[int]) -> bool:
    if len(row) != N:
        raise ValueError(f"expected a {N}-vertex coloring row")
    if any(type(color) is not int or color not in (0, 1, 2) for color in row):
        raise ValueError("malformed coloring row")
    return all(row[first] != row[second] for first, second in positive_template_edges(template))


def enumerate_bank(template: str) -> tuple[tuple[int, ...], ...]:
    """Enumerate all compatible restricted-growth strings in lexical order."""

    neighbors_before: list[list[int]] = [[] for _ in range(N)]
    for first, second in positive_template_edges(template):
        neighbors_before[second].append(first)
    rows: list[tuple[int, ...]] = []
    partial: list[int] = []

    def visit(vertex: int, maximum: int) -> None:
        if vertex == N:
            rows.append(tuple(partial))
            return
        upper = min(2, maximum + 1)
        for color in range(upper + 1):
            if any(partial[neighbor] == color for neighbor in neighbors_before[vertex]):
                continue
            partial.append(color)
            visit(vertex + 1, max(maximum, color))
            partial.pop()

    visit(0, -1)
    result = tuple(rows)
    expected = EXPECTED_BANK_COUNTS[template]
    if len(result) != expected:
        raise AssertionError(
            f"{template} bank count {len(result)} differs from proved {expected}"
        )
    return result


def _bank_bytes(rows: Sequence[Sequence[int]]) -> bytes:
    return canonical_json_bytes([list(row) for row in rows])


def load_bank_bytes(payload: bytes) -> tuple[tuple[int, ...], ...]:
    parsed = strict_json_bytes(payload)
    if not isinstance(parsed, list):
        raise ValueError("coloring bank must be a JSON list")
    rows: list[tuple[int, ...]] = []
    for index, raw in enumerate(parsed):
        if not isinstance(raw, list):
            raise ValueError(f"bank row {index} is not a list")
        try:
            row = first_use_canonical(raw)
        except ValueError as error:
            raise ValueError(f"invalid bank row {index}: {error}") from error
        rows.append(row)
    return tuple(rows)


def validate_bank(
    template: str,
    rows: Sequence[Sequence[int]],
    *,
    exhaustive: bool,
) -> tuple[tuple[int, ...], ...]:
    """Validate order, uniqueness, compatibility, and optionally full coverage."""

    template_length(template)
    normalized = tuple(first_use_canonical(row) for row in rows)
    if normalized != tuple(sorted(normalized)):
        raise ValueError("bank rows are not in strict lexicographic order")
    if len(set(normalized)) != len(normalized):
        raise ValueError("bank contains a duplicate row")
    if any(not row_is_template_proper(template, row) for row in normalized):
        raise ValueError("bank contains a row improper on a forced template edge")
    expected_count = EXPECTED_BANK_COUNTS[template]
    if len(normalized) != expected_count:
        raise ValueError(
            f"bank has {len(normalized)} rows; exact count is {expected_count}"
        )
    if exhaustive:
        oracle = {
            canonicalize_color_names(row)
            for row in product(range(3), repeat=N)
            if row_is_template_proper(template, row)
        }
        if set(normalized) != oracle:
            missing = sorted(oracle - set(normalized))
            extra = sorted(set(normalized) - oracle)
            raise ValueError(
                f"bank coverage differs from labeled oracle: "
                f"{len(missing)} missing, {len(extra)} extra"
            )
    return normalized


def build_exact_cnf(
    template: str,
    rows: Sequence[Sequence[int]],
) -> tuple[bytes, int, int, int]:
    normalized = validate_bank(template, rows, exhaustive=False)
    encoding = build_k3_encoding(template)
    for row in normalized:
        encoding.cnf.add_clause(same_color_cut(encoding, row))
    variable_count = encoding.cnf.variable_count
    clause_count = len(encoding.cnf.clauses)
    literal_count = sum(map(len, encoding.cnf.clauses))
    counts = (variable_count, clause_count, literal_count)
    if counts != EXPECTED_CNF_COUNTS[template]:
        raise AssertionError(
            f"{template} CNF counts {counts} differ from frozen {EXPECTED_CNF_COUNTS[template]}"
        )
    return (
        encoding.cnf.dimacs().encode("ascii"),
        variable_count,
        clause_count,
        literal_count,
    )


def bank_clause_stream_bytes(
    template: str,
    rows: Sequence[Sequence[int]],
) -> bytes:
    """Return appended bank clauses as header-free DIMACS lines."""

    normalized = validate_bank(template, rows, exhaustive=False)
    encoding = build_k3_encoding(template)
    return b"".join(
        (
            " ".join(map(str, same_color_cut(encoding, row))) + " 0\n"
        ).encode("ascii")
        for row in normalized
    )


def runtime_source_manifest() -> tuple[tuple[str, str], ...]:
    root = campaign_root()
    records: list[tuple[str, str]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        path = root / relative
        _assert_regular_single_link(path, f"runtime source {relative}")
        records.append((relative, sha256_file(path)))
    return tuple(records)


def source_set_sha256(records: Sequence[tuple[str, str]]) -> str:
    return sha256_bytes(
        "".join(f"{relative} {digest}\n" for relative, digest in records).encode(
            "ascii"
        )
    )


def _git_command(arguments: Sequence[str]) -> subprocess.CompletedProcess[bytes]:
    executable = shutil.which("git")
    if executable is None:
        raise ValueError("git executable is unavailable for source provenance")
    return subprocess.run(
        [executable, "--no-pager", "-C", str(campaign_root()), *arguments],
        env={
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "LC_ALL": "C",
            "PATH": str(Path(executable).parent),
        },
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=30,
        check=False,
    )


def _git_head() -> str:
    completed = _git_command(("rev-parse", "--verify", "HEAD"))
    if completed.returncode != 0:
        raise ValueError("cannot resolve repository HEAD")
    try:
        head = completed.stdout.decode("ascii").strip()
    except UnicodeDecodeError as error:
        raise ValueError("repository HEAD is not ASCII") from error
    if len(head) not in (40, 64):
        raise ValueError("repository HEAD has an unexpected object-id length")
    try:
        bytes.fromhex(head)
    except ValueError as error:
        raise ValueError("repository HEAD is not hexadecimal") from error
    return head


def _repository_root() -> Path:
    completed = _git_command(("rev-parse", "--show-toplevel"))
    if completed.returncode != 0:
        raise ValueError("cannot resolve repository root")
    try:
        root = Path(completed.stdout.decode("utf-8").strip()).resolve(strict=True)
    except UnicodeDecodeError as error:
        raise ValueError("repository root is not UTF-8") from error
    if not _path_is_within(campaign_root(), root):
        raise ValueError("campaign root is not within the reported repository")
    return root


def git_source_binding(
    sources: Sequence[tuple[str, str]],
    *,
    head: str | None = None,
) -> dict[str, object]:
    """Bind a commit without requiring unrelated worktree cleanliness."""

    selected_head = _git_head() if head is None else head
    if type(selected_head) is not str or len(selected_head) not in (40, 64):
        raise ValueError("source commit is malformed")
    try:
        bytes.fromhex(selected_head)
    except ValueError as error:
        raise ValueError("source commit is not hexadecimal") from error
    repository = _repository_root()
    root = campaign_root().resolve()
    campaign_relative = root.relative_to(repository).as_posix()
    mismatches: list[str] = []
    for relative, digest in sources:
        repository_relative = (
            Path(campaign_relative) / relative
        ).as_posix()
        completed = _git_command(
            ("show", f"{selected_head}:{repository_relative}")
        )
        if (
            completed.returncode != 0
            or sha256_bytes(completed.stdout) != digest
        ):
            mismatches.append(relative)
    return {
        "head_commit": selected_head,
        "repository_relative_campaign_path": campaign_relative,
        "runtime_sources_match_head": not mismatches,
        "runtime_source_mismatches": mismatches,
        "global_worktree_cleanliness_required": False,
    }


def _generation_manifest_payload(
    *,
    template: str,
    bank_path: Path,
    cnf_path: Path,
    variable_count: int,
    clause_count: int,
    literal_count: int,
    sources: Sequence[tuple[str, str]],
    git_binding: Mapping[str, object],
) -> dict[str, object]:
    length = template_length(template)
    base_encoding = build_k3_encoding(template)
    base_counts = (
        base_encoding.cnf.variable_count,
        len(base_encoding.cnf.clauses),
        sum(map(len, base_encoding.cnf.clauses)),
    )
    if base_counts != EXPECTED_BASE_CNF_COUNTS[template]:
        raise AssertionError(
            f"{template} base counts {base_counts} differ from frozen "
            f"{EXPECTED_BASE_CNF_COUNTS[template]}"
        )
    rows = enumerate_bank(template)
    clause_stream = bank_clause_stream_bytes(template, rows)
    return {
        "schema": "gamma-theta-k3-template-color-bank-v1",
        "schema_version": SCHEMA_VERSION,
        "template": template,
        "order": N,
        "canonicalization": "restricted-growth-string-first-use",
        "forced_positive_h_edges": [
            list(edge) for edge in positive_template_edges(template)
        ],
        "count_identity": {
            "cycle_length": length,
            "labeled_cycle_colorings": 2**length - 2,
            "free_vertices": 11 - length,
            "color_permutation_orbit_size": 6,
            "expected_bank_count": EXPECTED_BANK_COUNTS[template],
        },
        "bank_count": EXPECTED_BANK_COUNTS[template],
        "variable_count": variable_count,
        "clause_count": clause_count,
        "literal_count": literal_count,
        "clause_layout": {
            "base_clause_count": base_counts[1],
            "base_literal_count": base_counts[2],
            "base_cnf_sha256": sha256_bytes(
                base_encoding.cnf.dimacs().encode("ascii")
            ),
            "bank_clause_first_index_zero_based": base_counts[1],
            "bank_clause_end_index_exclusive": clause_count,
            "bank_clause_order": "coloring-bank-row-order",
            "bank_clause_stream_format": (
                "header-free-DIMACS-lines-terminal-zero-LF"
            ),
            "bank_clause_stream_sha256": sha256_bytes(clause_stream),
            "bank_clause_stream_size_bytes": len(clause_stream),
        },
        "artifacts": {
            "coloring_bank": _artifact_record(bank_path),
            "cnf": _artifact_record(cnf_path),
        },
        "runtime_source_manifest": [
            [relative, digest] for relative, digest in sources
        ],
        "runtime_source_set_sha256": source_set_sha256(sources),
        "git_source_binding": dict(git_binding),
        "generation_recipe": {
            "module": "synthesis_k3.template_color_bank",
            "subcommand": "generate",
            "validation_gate": True,
        },
    }


def generate_package(
    *,
    template: str,
    output_directory: Path,
    validation_gate: object,
) -> dict[str, object]:
    """Generate a complete bank package without overwriting any path."""

    _require_gate(validation_gate)
    template_length(template)
    destination = _validate_new_output_directory(output_directory)
    sources = runtime_source_manifest()
    git_binding = git_source_binding(sources)
    rows = enumerate_bank(template)
    validate_bank(template, rows, exhaustive=True)
    bank_payload = _bank_bytes(rows)
    cnf_payload, variables, clauses, literals = build_exact_cnf(template, rows)

    temporary = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.partial.",
            dir=destination.parent,
        )
    )
    installed = False
    try:
        bank_path = temporary / BANK_NAME
        cnf_path = temporary / CNF_NAME
        manifest_path = temporary / MANIFEST_NAME
        _write_new_file(bank_path, bank_payload)
        _write_new_file(cnf_path, cnf_payload)
        manifest = _generation_manifest_payload(
            template=template,
            bank_path=bank_path,
            cnf_path=cnf_path,
            variable_count=variables,
            clause_count=clauses,
            literal_count=literals,
            sources=sources,
            git_binding=git_binding,
        )
        _write_new_file(manifest_path, canonical_json_bytes(manifest))
        _fsync_directory(temporary)
        audit_package(temporary, exhaustive=True)
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"output appeared during generation: {destination}")
        os.rename(temporary, destination)
        installed = True
        _fsync_directory(destination.parent)
        audit = audit_package(destination, exhaustive=False)
        return {
            "status": "generated",
            "package_directory": str(destination),
            **audit,
        }
    finally:
        if not installed and temporary.exists():
            shutil.rmtree(temporary)


def _parse_source_manifest(value: object) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, list):
        raise ValueError("runtime source manifest is not a list")
    result: list[tuple[str, str]] = []
    for index, row in enumerate(value):
        if (
            not isinstance(row, list)
            or len(row) != 2
            or type(row[0]) is not str
            or type(row[1]) is not str
            or len(row[1]) != 64
        ):
            raise ValueError(f"runtime source record {index} is malformed")
        try:
            bytes.fromhex(row[1])
        except ValueError as error:
            raise ValueError(f"runtime source hash {index} is malformed") from error
        result.append((row[0], row[1]))
    return tuple(result)


def _validate_artifact_record(
    package: Path,
    value: object,
    *,
    expected_name: str,
    role: str,
) -> Path:
    record = _require_exact_keys(value, {"path", "sha256", "size_bytes"}, role)
    if (
        record["path"] != expected_name
        or type(record["sha256"]) is not str
        or len(record["sha256"]) != 64
        or type(record["size_bytes"]) is not int
        or record["size_bytes"] < 0
    ):
        raise ValueError(f"{role} binding is malformed")
    try:
        bytes.fromhex(record["sha256"])
    except ValueError as error:
        raise ValueError(f"{role} hash is malformed") from error
    path = package / expected_name
    _assert_regular_single_link(path, role)
    if path.stat().st_size != record["size_bytes"]:
        raise ValueError(f"{role} size mismatch")
    if sha256_file(path) != record["sha256"]:
        raise ValueError(f"{role} SHA-256 mismatch")
    return path


def audit_package(
    package_directory: Path,
    *,
    exhaustive: bool,
) -> dict[str, object]:
    """Strictly reconstruct and validate a complete generated package."""

    if type(exhaustive) is not bool:
        raise ValueError("exhaustive flag must be boolean")
    package = _validate_readonly_package_directory(package_directory)
    manifest_path = package / MANIFEST_NAME
    manifest_payload = manifest_path.read_bytes()
    manifest = _require_exact_keys(
        strict_json_bytes(manifest_payload),
        {
            "schema",
            "schema_version",
            "template",
            "order",
            "canonicalization",
            "forced_positive_h_edges",
            "count_identity",
            "bank_count",
            "variable_count",
            "clause_count",
            "literal_count",
            "clause_layout",
            "artifacts",
            "runtime_source_manifest",
            "runtime_source_set_sha256",
            "git_source_binding",
            "generation_recipe",
        },
        "generation manifest",
    )
    if (
        manifest["schema"] != "gamma-theta-k3-template-color-bank-v1"
        or manifest["schema_version"] != SCHEMA_VERSION
        or manifest["order"] != N
        or manifest["canonicalization"] != "restricted-growth-string-first-use"
    ):
        raise ValueError("generation manifest identity is wrong")
    template = manifest["template"]
    if type(template) is not str:
        raise ValueError("manifest template is malformed")
    length = template_length(template)
    expected_edges = [list(edge) for edge in positive_template_edges(template)]
    if manifest["forced_positive_h_edges"] != expected_edges:
        raise ValueError("manifest forced-edge list is wrong")
    count_identity = _require_exact_keys(
        manifest["count_identity"],
        {
            "cycle_length",
            "labeled_cycle_colorings",
            "free_vertices",
            "color_permutation_orbit_size",
            "expected_bank_count",
        },
        "count identity",
    )
    expected_count = EXPECTED_BANK_COUNTS[template]
    if dict(count_identity) != {
        "cycle_length": length,
        "labeled_cycle_colorings": 2**length - 2,
        "free_vertices": 11 - length,
        "color_permutation_orbit_size": 6,
        "expected_bank_count": expected_count,
    }:
        raise ValueError("manifest count identity is wrong")
    artifacts = _require_exact_keys(
        manifest["artifacts"], {"coloring_bank", "cnf"}, "artifact map"
    )
    bank_path = _validate_artifact_record(
        package,
        artifacts["coloring_bank"],
        expected_name=BANK_NAME,
        role="coloring bank",
    )
    cnf_path = _validate_artifact_record(
        package,
        artifacts["cnf"],
        expected_name=CNF_NAME,
        role="CNF",
    )
    rows = load_bank_bytes(bank_path.read_bytes())
    validate_bank(template, rows, exhaustive=exhaustive)
    if bank_path.read_bytes() != _bank_bytes(rows):
        raise ValueError("coloring bank bytes are not canonical")
    expected_cnf, variables, clauses, literals = build_exact_cnf(template, rows)
    if cnf_path.read_bytes() != expected_cnf:
        raise ValueError("CNF bytes differ from exact reconstruction")
    if (
        manifest["bank_count"],
        manifest["variable_count"],
        manifest["clause_count"],
        manifest["literal_count"],
    ) != (expected_count, variables, clauses, literals):
        raise ValueError("manifest formula counts are wrong")
    base_encoding = build_k3_encoding(template)
    base_counts = EXPECTED_BASE_CNF_COUNTS[template]
    clause_stream = bank_clause_stream_bytes(template, rows)
    clause_layout = _require_exact_keys(
        manifest["clause_layout"],
        {
            "base_clause_count",
            "base_literal_count",
            "base_cnf_sha256",
            "bank_clause_first_index_zero_based",
            "bank_clause_end_index_exclusive",
            "bank_clause_order",
            "bank_clause_stream_format",
            "bank_clause_stream_sha256",
            "bank_clause_stream_size_bytes",
        },
        "clause layout",
    )
    if dict(clause_layout) != {
        "base_clause_count": base_counts[1],
        "base_literal_count": base_counts[2],
        "base_cnf_sha256": sha256_bytes(
            base_encoding.cnf.dimacs().encode("ascii")
        ),
        "bank_clause_first_index_zero_based": base_counts[1],
        "bank_clause_end_index_exclusive": clauses,
        "bank_clause_order": "coloring-bank-row-order",
        "bank_clause_stream_format": (
            "header-free-DIMACS-lines-terminal-zero-LF"
        ),
        "bank_clause_stream_sha256": sha256_bytes(clause_stream),
        "bank_clause_stream_size_bytes": len(clause_stream),
    }:
        raise ValueError("manifest clause layout is wrong")
    recipe = _require_exact_keys(
        manifest["generation_recipe"],
        {"module", "subcommand", "validation_gate"},
        "generation recipe",
    )
    if dict(recipe) != {
        "module": "synthesis_k3.template_color_bank",
        "subcommand": "generate",
        "validation_gate": True,
    }:
        raise ValueError("generation recipe is wrong")
    recorded_sources = _parse_source_manifest(manifest["runtime_source_manifest"])
    current_sources = runtime_source_manifest()
    if recorded_sources != current_sources:
        raise ValueError("runtime source binding changed")
    if (
        manifest["runtime_source_set_sha256"]
        != source_set_sha256(recorded_sources)
    ):
        raise ValueError("runtime source-set hash is wrong")
    recorded_git = _require_exact_keys(
        manifest["git_source_binding"],
        {
            "head_commit",
            "repository_relative_campaign_path",
            "runtime_sources_match_head",
            "runtime_source_mismatches",
            "global_worktree_cleanliness_required",
        },
        "git source binding",
    )
    head = recorded_git["head_commit"]
    if type(head) is not str:
        raise ValueError("recorded source commit is malformed")
    expected_git = git_source_binding(recorded_sources, head=head)
    if canonical_json_bytes(dict(recorded_git)) != canonical_json_bytes(expected_git):
        raise ValueError("git source binding differs from repository objects")
    expected_manifest = _generation_manifest_payload(
        template=template,
        bank_path=bank_path,
        cnf_path=cnf_path,
        variable_count=variables,
        clause_count=clauses,
        literal_count=literals,
        sources=current_sources,
        git_binding=expected_git,
    )
    if manifest_payload != canonical_json_bytes(expected_manifest):
        raise ValueError("generation manifest bytes differ from reconstruction")
    return {
        "template": template,
        "bank_count": expected_count,
        "variable_count": variables,
        "clause_count": clauses,
        "literal_count": literals,
        "bank_sha256": sha256_file(bank_path),
        "cnf_sha256": sha256_file(cnf_path),
        "manifest_sha256": sha256_bytes(manifest_payload),
        "exhaustive_oracle_checked": exhaustive,
    }


def _physical_memory_bytes() -> int:
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
    except (OSError, ValueError) as error:
        raise ValueError("cannot determine physical memory") from error
    if (
        type(pages) is not int
        or type(page_size) is not int
        or pages <= 0
        or page_size <= 0
    ):
        raise ValueError("invalid physical memory report")
    return pages * page_size


def _resource_preflight(
    *,
    output_directory: Path,
    solver_wall_seconds: int,
    checker_wall_seconds: int,
    solver_memory_mib: int,
    checker_memory_mib: int,
    file_limit_mib: int,
    disk_reserve_mib: int,
) -> dict[str, object]:
    solver_wall_seconds = _positive_exact_int(
        solver_wall_seconds, "solver wall limit"
    )
    checker_wall_seconds = _positive_exact_int(
        checker_wall_seconds, "checker wall limit"
    )
    solver_memory_mib = _positive_exact_int(
        solver_memory_mib, "solver memory limit"
    )
    checker_memory_mib = _positive_exact_int(
        checker_memory_mib, "checker memory limit"
    )
    file_limit_mib = _positive_exact_int(file_limit_mib, "child file limit")
    disk_reserve_mib = _positive_exact_int(disk_reserve_mib, "disk reserve")
    if solver_memory_mib < 64 or checker_memory_mib < 64:
        raise ValueError("child memory limits must be at least 64 MiB")
    physical = _physical_memory_bytes()
    safe_memory_mib = math.floor(physical * 0.75 / (1 << 20))
    if solver_memory_mib > safe_memory_mib:
        raise ValueError("solver memory limit exceeds 75% physical RAM")
    if checker_memory_mib > safe_memory_mib:
        raise ValueError("checker memory limit exceeds 75% physical RAM")
    usage = shutil.disk_usage(output_directory.parent)
    required = (disk_reserve_mib + 7 * file_limit_mib + 16) << 20
    if usage.free < required:
        raise RuntimeError(
            f"disk preflight failed: {usage.free} bytes free, {required} required"
        )
    return {
        "physical_memory_bytes": physical,
        "maximum_safe_child_memory_mib": safe_memory_mib,
        "free_disk_bytes_before": usage.free,
        "required_free_disk_bytes": required,
        "solver_wall_seconds": solver_wall_seconds,
        "checker_wall_seconds": checker_wall_seconds,
        "solver_memory_mib": solver_memory_mib,
        "checker_memory_mib": checker_memory_mib,
        "file_limit_mib": file_limit_mib,
        "disk_reserve_mib": disk_reserve_mib,
    }


def _checker_verified(stdout_path: Path, stderr_path: Path) -> None:
    try:
        stdout = stdout_path.read_text(encoding="ascii")
        stderr = stderr_path.read_text(encoding="ascii")
    except UnicodeDecodeError as error:
        raise ValueError("DRAT-trim logs are not ASCII") from error
    combined = stdout + "\n" + stderr
    if "warning" in combined.lower():
        raise ValueError("DRAT-trim emitted a warning")
    if [line.strip() for line in stdout.splitlines()].count("s VERIFIED") != 1:
        raise ValueError("DRAT-trim did not emit exactly one s VERIFIED")


def _child_record(child: ChildResult) -> dict[str, object]:
    return asdict(child)


def _existing_artifact_map(directory: Path) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for path in sorted(directory.iterdir()):
        if path.name in {RUN_CONFIG_NAME, OUTCOME_NAME}:
            continue
        if path.is_file() and not path.is_symlink():
            _assert_regular_single_link(path, f"solve artifact {path.name}")
            result[path.name] = _artifact_record(path)
    return result


def _tool_payload(binding: object) -> dict[str, object]:
    return asdict(binding)  # ToolBinding is a frozen dataclass.


def _solver_command(
    cadical: Path,
    *,
    seed: int,
    wall_seconds: int,
    result_path: Path,
    cnf_path: Path,
    proof_path: Path,
) -> tuple[str, ...]:
    return (
        str(cadical.resolve()),
        f"--seed={seed}",
        "--no-binary",
        "--no-colors",
        "-q",
        "-t",
        str(wall_seconds),
        "-w",
        str(result_path.resolve()),
        str(cnf_path.resolve()),
        str(proof_path.resolve()),
    )


def _checker_command(
    drat_trim: Path,
    *,
    cnf_path: Path,
    proof_path: Path,
    wall_seconds: int,
) -> tuple[str, ...]:
    return (
        str(drat_trim.resolve()),
        str(cnf_path.resolve()),
        str(proof_path.resolve()),
        "-I",
        "-f",
        "-W",
        "-t",
        str(wall_seconds),
    )


def solve_package(
    *,
    package_directory: Path,
    output_directory: Path,
    cadical_path: Path,
    drat_trim_path: Path,
    seed: int,
    solver_wall_seconds: int,
    checker_wall_seconds: int,
    solver_memory_mib: int,
    checker_memory_mib: int,
    file_limit_mib: int,
    disk_reserve_mib: int,
    validation_gate: object,
) -> dict[str, object]:
    """Run one bounded proof-producing solve of an audited complete package."""

    _require_gate(validation_gate)
    seed = _nonnegative_exact_int(seed, "solver seed")
    if seed > 2_000_000_000:
        raise ValueError("solver seed exceeds 2e9")
    package = _validate_readonly_package_directory(package_directory)
    destination = _validate_new_output_directory(output_directory)
    if _path_is_within(destination, package) or _path_is_within(package, destination):
        raise ValueError("solve output and input package trees overlap")
    package_audit = audit_package(package, exhaustive=True)
    resources = _resource_preflight(
        output_directory=destination,
        solver_wall_seconds=solver_wall_seconds,
        checker_wall_seconds=checker_wall_seconds,
        solver_memory_mib=solver_memory_mib,
        checker_memory_mib=checker_memory_mib,
        file_limit_mib=file_limit_mib,
        disk_reserve_mib=disk_reserve_mib,
    )
    cadical, drat_trim = verify_pinned_tools(cadical_path, drat_trim_path)
    destination.mkdir(mode=0o700)
    _fsync_directory(destination.parent)
    cnf_path = package / CNF_NAME
    cnf_hash_before = sha256_file(cnf_path)
    source_records = runtime_source_manifest()
    run_config = {
        "schema": "gamma-theta-k3-template-color-bank-solve-config-v1",
        "schema_version": SCHEMA_VERSION,
        "package": {
            "path": str(package),
            "manifest_sha256": package_audit["manifest_sha256"],
            "cnf_sha256": package_audit["cnf_sha256"],
            "bank_sha256": package_audit["bank_sha256"],
        },
        "seed": seed,
        "resources": resources,
        "tools": {
            "cadical": _tool_payload(cadical),
            "drat_trim": _tool_payload(drat_trim),
        },
        "runtime_source_manifest": [
            [relative, digest] for relative, digest in source_records
        ],
        "runtime_source_set_sha256": source_set_sha256(source_records),
        "git_source_binding": git_source_binding(source_records),
        "python": {
            "executable": str(Path(sys.executable).resolve()),
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
        },
    }
    _write_new_file(destination / RUN_CONFIG_NAME, canonical_json_bytes(run_config))

    result_path = destination / "solver.result"
    proof_path = destination / "proof.drat"
    solver_stdout = destination / "solver.stdout"
    solver_stderr = destination / "solver.stderr"
    command = _solver_command(
        Path(cadical.path),
        seed=seed,
        wall_seconds=solver_wall_seconds,
        result_path=result_path,
        cnf_path=cnf_path,
        proof_path=proof_path,
    )
    solver: ChildResult | None = None
    checker: ChildResult | None = None
    status = "INCONCLUSIVE_SOLVER_CONTROL_FAILURE"
    claim_status = "NO_MATHEMATICAL_CLAIM"
    semantic_checks: dict[str, object] = {}
    failures: list[dict[str, str]] = []
    parsed_cnf = parse_dimacs_bytes(cnf_path.read_bytes())

    def record_failure(error: BaseException) -> None:
        failures.append(
            {
                "exception_type": type(error).__name__,
                "message": str(error),
            }
        )

    try:
        solver = run_bounded_child(
            command=command,
            cwd=destination,
            stdout_path=solver_stdout,
            stderr_path=solver_stderr,
            wall_limit_seconds=solver_wall_seconds,
            memory_limit_mib=solver_memory_mib,
            file_limit_mib=file_limit_mib,
            readonly_paths={"CNF": cnf_path},
        )
    except Exception as error:
        record_failure(error)
    else:
        if solver.timed_out:
            status = "INCONCLUSIVE_SOLVER_TIMEOUT"
        elif solver.memory_limit_exceeded:
            status = "INCONCLUSIVE_SOLVER_MEMORY_LIMIT"
        elif solver.termination_signal == int(signal.SIGXFSZ):
            status = "INCONCLUSIVE_SOLVER_FILE_LIMIT"
        elif solver.exit_code == 10:
            try:
                parsed = parse_solver_result_file(
                    result_path, parsed_cnf.variable_count
                )
                if parsed.status != "SAT" or parsed.model is None:
                    raise RuntimeError(
                        "CaDiCaL SAT exit contradicts result artifact"
                    )
                validate_model_satisfies_cnf(parsed_cnf, parsed.model)
                encoding = build_k3_encoding(str(package_audit["template"]))
                edges = encoding.decode_edges(parsed.model)
                family = encoding.decode_family(parsed.model)
                validate_decoded_candidate(encoding, edges, family)
                candidate = {
                    "status": (
                        "candidate_requires_independent_parameter_verification"
                    ),
                    "h_edges": [list(edge) for edge in edges],
                    "eternal_family": [list(triple) for triple in family],
                }
                _write_new_file(
                    destination / "candidate.json",
                    canonical_json_bytes(candidate),
                )
            except Exception as error:
                status = "INVALID_SAT_ARTIFACT_NONCLAIM"
                record_failure(error)
            else:
                status = "SAT_CANDIDATE"
                claim_status = "CANDIDATE_ONLY"
                semantic_checks = {
                    "complete_model": True,
                    "model_satisfies_exact_cnf": True,
                    "decoded_base_semantics_valid": True,
                }
        elif solver.exit_code == 20:
            proof_hash_before: str | None = None
            try:
                parsed = parse_solver_result_file(
                    result_path, parsed_cnf.variable_count
                )
                if parsed.status != "UNSAT":
                    raise RuntimeError(
                        "CaDiCaL UNSAT exit contradicts result artifact"
                    )
                _assert_regular_single_link(proof_path, "DRAT proof")
                if proof_path.stat().st_size == 0:
                    raise RuntimeError(
                        "CaDiCaL returned UNSAT with an empty proof"
                    )
                proof_hash_before = sha256_file(proof_path)
            except Exception as error:
                status = "INVALID_UNSAT_ARTIFACT_NONCLAIM"
                record_failure(error)
            else:
                checker_stdout = destination / "checker.stdout"
                checker_stderr = destination / "checker.stderr"
                try:
                    checker = run_bounded_child(
                        command=_checker_command(
                            Path(drat_trim.path),
                            cnf_path=cnf_path,
                            proof_path=proof_path,
                            wall_seconds=checker_wall_seconds,
                        ),
                        cwd=destination,
                        stdout_path=checker_stdout,
                        stderr_path=checker_stderr,
                        wall_limit_seconds=checker_wall_seconds,
                        memory_limit_mib=checker_memory_mib,
                        file_limit_mib=file_limit_mib,
                        readonly_paths={
                            "CNF": cnf_path,
                            "DRAT proof": proof_path,
                        },
                    )
                except Exception as error:
                    status = "UNSAT_UNVERIFIED_CHECKER_CONTROL_FAILURE"
                    record_failure(error)
                else:
                    if checker.timed_out:
                        status = "UNSAT_UNVERIFIED_CHECKER_TIMEOUT"
                    elif checker.memory_limit_exceeded:
                        status = "UNSAT_UNVERIFIED_CHECKER_MEMORY_LIMIT"
                    elif checker.termination_signal == int(signal.SIGXFSZ):
                        status = "UNSAT_UNVERIFIED_CHECKER_FILE_LIMIT"
                    elif checker.exit_code != 0:
                        status = "UNSAT_UNVERIFIED_CHECKER_EXIT"
                    else:
                        try:
                            _checker_verified(
                                checker_stdout, checker_stderr
                            )
                            if sha256_file(proof_path) != proof_hash_before:
                                raise RuntimeError(
                                    "proof changed during verification"
                                )
                        except Exception as error:
                            status = "UNSAT_UNVERIFIED_CHECKER_ARTIFACT"
                            record_failure(error)
                        else:
                            status = "UNSAT_VERIFIED"
                            claim_status = "VERIFIED_FINITE_CERTIFICATE"
                            semantic_checks = {
                                "result_status_unsat": True,
                                "proof_nonempty": True,
                                "drat_trim_exact_verified_line": True,
                                "drat_trim_warning_free": True,
                                "proof_unchanged_during_check": True,
                            }
        elif solver.exit_code == 0:
            status = "INCONCLUSIVE_SOLVER_UNKNOWN"
        else:
            status = "INCONCLUSIVE_SOLVER_EXIT"

    try:
        if sha256_file(cnf_path) != cnf_hash_before:
            raise RuntimeError("input CNF changed during solve")
    except Exception as error:
        status = "INPUT_CNF_MUTATION_NONCLAIM"
        claim_status = "NO_MATHEMATICAL_CLAIM"
        semantic_checks = {}
        record_failure(error)
    try:
        artifacts = _existing_artifact_map(destination)
    except Exception as error:
        status = "OUTPUT_ARTIFACT_BINDING_NONCLAIM"
        claim_status = "NO_MATHEMATICAL_CLAIM"
        semantic_checks = {}
        record_failure(error)
        artifacts = {}
    outcome = {
        "schema": "gamma-theta-k3-template-color-bank-solve-outcome-v1",
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "claim_status": claim_status,
        "package_manifest_sha256": package_audit["manifest_sha256"],
        "cnf_sha256": cnf_hash_before,
        "run_config_sha256": sha256_file(destination / RUN_CONFIG_NAME),
        "solver": _child_record(solver) if solver is not None else None,
        "checker": _child_record(checker) if checker is not None else None,
        "semantic_checks": semantic_checks,
        "failures": failures,
        "artifacts": artifacts,
    }
    _write_new_file(destination / OUTCOME_NAME, canonical_json_bytes(outcome))
    _fsync_directory(destination)
    return outcome


def _live_tool_smoke_impl(
    *,
    output_directory: Path,
    cadical_path: Path,
    drat_trim_path: Path,
    validation_gate: object,
) -> dict[str, object]:
    """Exercise pinned tools on tiny SAT and proof-checked UNSAT formulas."""

    _require_gate(validation_gate)
    destination = _validate_new_output_directory(output_directory)
    cadical, drat_trim = verify_pinned_tools(cadical_path, drat_trim_path)
    _resource_preflight(
        output_directory=destination,
        solver_wall_seconds=10,
        checker_wall_seconds=10,
        solver_memory_mib=64,
        checker_memory_mib=64,
        file_limit_mib=8,
        disk_reserve_mib=1,
    )
    destination.mkdir(mode=0o700)
    _fsync_directory(destination.parent)
    sat_cnf = destination / "smoke-sat.cnf"
    unsat_cnf = destination / "smoke-unsat.cnf"
    _write_new_file(sat_cnf, b"p cnf 1 1\n1 0\n")
    _write_new_file(unsat_cnf, b"p cnf 1 2\n1 0\n-1 0\n")

    sat_result = destination / "smoke-sat.result"
    sat_stdout = destination / "smoke-sat.stdout"
    sat_stderr = destination / "smoke-sat.stderr"
    sat_child = run_bounded_child(
        command=(
            cadical.path,
            "--seed=0",
            "--no-binary",
            "--no-colors",
            "-q",
            "-t",
            "10",
            "-w",
            str(sat_result.resolve()),
            str(sat_cnf.resolve()),
        ),
        cwd=destination,
        stdout_path=sat_stdout,
        stderr_path=sat_stderr,
        wall_limit_seconds=10,
        memory_limit_mib=64,
        file_limit_mib=8,
        readonly_paths={"SAT CNF": sat_cnf},
    )
    if sat_child.exit_code != 10 or sat_child.timed_out:
        raise RuntimeError("tiny pinned CaDiCaL SAT smoke failed")
    sat_formula = parse_dimacs_bytes(sat_cnf.read_bytes())
    sat_parsed = parse_solver_result_file(sat_result, sat_formula.variable_count)
    if sat_parsed.status != "SAT" or sat_parsed.model is None:
        raise RuntimeError("tiny SAT result artifact is inconsistent")
    validate_model_satisfies_cnf(sat_formula, sat_parsed.model)

    unsat_result = destination / "smoke-unsat.result"
    unsat_proof = destination / "smoke-unsat.drat"
    unsat_stdout = destination / "smoke-unsat.stdout"
    unsat_stderr = destination / "smoke-unsat.stderr"
    unsat_child = run_bounded_child(
        command=_solver_command(
            Path(cadical.path),
            seed=0,
            wall_seconds=10,
            result_path=unsat_result,
            cnf_path=unsat_cnf,
            proof_path=unsat_proof,
        ),
        cwd=destination,
        stdout_path=unsat_stdout,
        stderr_path=unsat_stderr,
        wall_limit_seconds=10,
        memory_limit_mib=64,
        file_limit_mib=8,
        readonly_paths={"UNSAT CNF": unsat_cnf},
    )
    if unsat_child.exit_code != 20 or unsat_child.timed_out:
        raise RuntimeError("tiny pinned CaDiCaL UNSAT smoke failed")
    parsed_unsat = parse_solver_result_file(unsat_result, 1)
    if parsed_unsat.status != "UNSAT":
        raise RuntimeError("tiny UNSAT result artifact is inconsistent")
    _assert_regular_single_link(unsat_proof, "tiny DRAT proof")
    if unsat_proof.stat().st_size == 0:
        raise RuntimeError("tiny UNSAT proof is empty")

    checker_stdout = destination / "smoke-checker.stdout"
    checker_stderr = destination / "smoke-checker.stderr"
    checker = run_bounded_child(
        command=_checker_command(
            Path(drat_trim.path),
            cnf_path=unsat_cnf,
            proof_path=unsat_proof,
            wall_seconds=10,
        ),
        cwd=destination,
        stdout_path=checker_stdout,
        stderr_path=checker_stderr,
        wall_limit_seconds=10,
        memory_limit_mib=64,
        file_limit_mib=8,
        readonly_paths={"UNSAT CNF": unsat_cnf, "DRAT proof": unsat_proof},
    )
    if checker.exit_code != 0 or checker.timed_out:
        raise RuntimeError("tiny pinned DRAT-trim smoke failed")
    _checker_verified(checker_stdout, checker_stderr)
    report = {
        "schema": "gamma-theta-k3-template-color-bank-tool-smoke-v1",
        "status": "PASSED_TOOL_SMOKE",
        "claim_status": "NO_MATHEMATICAL_CLAIM",
        "cadical_sha256": cadical.sha256,
        "drat_trim_sha256": drat_trim.sha256,
        "sat_model_checked": True,
        "unsat_proof_checked": True,
        "sat_child": _child_record(sat_child),
        "unsat_child": _child_record(unsat_child),
        "checker_child": _child_record(checker),
        "artifacts": _existing_artifact_map(destination),
    }
    _write_new_file(destination / "smoke.json", canonical_json_bytes(report))
    _fsync_directory(destination)
    return report


def live_tool_smoke(
    *,
    output_directory: Path,
    cadical_path: Path,
    drat_trim_path: Path,
    validation_gate: object,
) -> dict[str, object]:
    """Run the smoke test and leave an explicit nonclaim record on failure."""

    existed_before = output_directory.exists() or output_directory.is_symlink()
    try:
        return _live_tool_smoke_impl(
            output_directory=output_directory,
            cadical_path=cadical_path,
            drat_trim_path=drat_trim_path,
            validation_gate=validation_gate,
        )
    except Exception as error:
        destination = output_directory.resolve(strict=False)
        failure_path = destination / "smoke.json"
        if (
            not existed_before
            and destination.is_dir()
            and not destination.is_symlink()
            and not failure_path.exists()
            and not failure_path.is_symlink()
        ):
            failure = {
                "schema": "gamma-theta-k3-template-color-bank-tool-smoke-v1",
                "status": "FAILED_NONCLAIM",
                "claim_status": "NO_MATHEMATICAL_CLAIM",
                "failure": {
                    "exception_type": type(error).__name__,
                    "message": str(error),
                },
                "artifacts": _existing_artifact_map(destination),
            }
            _write_new_file(failure_path, canonical_json_bytes(failure))
            _fsync_directory(destination)
        raise


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--validation-gate-open", action="store_true")
    generate_parser.add_argument(
        "--template", choices=BANK_TEMPLATES, required=True
    )
    generate_parser.add_argument("--output-dir", type=Path, required=True)

    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--package-dir", type=Path, required=True)
    audit_parser.add_argument("--exhaustive", action="store_true")

    solve_parser = subparsers.add_parser("solve")
    solve_parser.add_argument("--validation-gate-open", action="store_true")
    solve_parser.add_argument("--package-dir", type=Path, required=True)
    solve_parser.add_argument("--output-dir", type=Path, required=True)
    solve_parser.add_argument("--cadical", type=Path, required=True)
    solve_parser.add_argument("--drat-trim", type=Path, required=True)
    solve_parser.add_argument("--seed", type=int, default=0)
    solve_parser.add_argument("--solver-wall-seconds", type=int, default=3_600)
    solve_parser.add_argument("--checker-wall-seconds", type=int, default=3_600)
    solve_parser.add_argument("--solver-memory-mib", type=int, default=2_048)
    solve_parser.add_argument("--checker-memory-mib", type=int, default=2_048)
    solve_parser.add_argument("--file-limit-mib", type=int, default=256)
    solve_parser.add_argument("--disk-reserve-mib", type=int, default=4_096)

    smoke_parser = subparsers.add_parser("smoke")
    smoke_parser.add_argument("--validation-gate-open", action="store_true")
    smoke_parser.add_argument("--output-dir", type=Path, required=True)
    smoke_parser.add_argument("--cadical", type=Path, required=True)
    smoke_parser.add_argument("--drat-trim", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command == "generate":
        result = generate_package(
            template=arguments.template,
            output_directory=arguments.output_dir,
            validation_gate=arguments.validation_gate_open,
        )
    elif arguments.command == "audit":
        result = audit_package(
            arguments.package_dir,
            exhaustive=arguments.exhaustive,
        )
    elif arguments.command == "solve":
        result = solve_package(
            package_directory=arguments.package_dir,
            output_directory=arguments.output_dir,
            cadical_path=arguments.cadical,
            drat_trim_path=arguments.drat_trim,
            seed=arguments.seed,
            solver_wall_seconds=arguments.solver_wall_seconds,
            checker_wall_seconds=arguments.checker_wall_seconds,
            solver_memory_mib=arguments.solver_memory_mib,
            checker_memory_mib=arguments.checker_memory_mib,
            file_limit_mib=arguments.file_limit_mib,
            disk_reserve_mib=arguments.disk_reserve_mib,
            validation_gate=arguments.validation_gate_open,
        )
    elif arguments.command == "smoke":
        result = live_tool_smoke(
            output_directory=arguments.output_dir,
            cadical_path=arguments.cadical,
            drat_trim_path=arguments.drat_trim,
            validation_gate=arguments.validation_gate_open,
        )
    else:
        raise AssertionError("argparse accepted an unknown command")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
