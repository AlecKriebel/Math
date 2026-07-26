#!/usr/bin/env python3
"""Standalone read-only auditor for the retained hole5 binary-proof run.

This auditor uses only the Python standard library.  It imports no synthesis,
solver-wrapper, proof-parser, or certificate code.  It never writes inside the
audited run directory.  Its optional output is installed outside that
directory with no-overwrite semantics.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from itertools import product
from pathlib import Path
from typing import Mapping, Sequence


SCHEMA = "gamma-theta-hole5-binary-run-package-audit-v1"
ROOT = Path(__file__).resolve().parents[1]
RUN_RELATIVE = Path(
    "results/synthesis_k3_hole5_signature_seed0_600s_binary"
)
RUN = ROOT / RUN_RELATIVE
DERIVED_RELATIVE = Path("results/synthesis_k3_hole5_signature_package")
DERIVED = ROOT / DERIVED_RELATIVE
SOURCE_RELATIVE = Path(
    "results/synthesis_k3_template_bank_packages/hole5"
)
SOURCE = ROOT / SOURCE_RELATIVE
EXPECTED_SOURCE_COMMIT = "6f3ef0a0970b7214c34018fe32ea1ceeb5764d17"
EXPECTED_PACKAGE_COMMIT = "dff45f4239e4acabc461533a0a213beec18ec56d"
EXPECTED_RUN_SUBTREE_OID = "aaef13bba428f8722ad167158360da831a7d1998"
EXPECTED_RUN_CONFIG_SHA256 = (
    "6d899e212d2f349b48eefad5037ea007981a331b7e581966165ae861c741221b"
)
EXPECTED_OUTCOME_SHA256 = (
    "ea2ea36321a786aa40aff1e68587474bbdba5402abc800b1a0816d65b6df8df4"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "f54d7bf8a50f24e3a5084442d84f07548a60401faca8ec18bfd07f24f0e337e8"
)
EXPECTED_CNF_SHA256 = (
    "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104"
)
EXPECTED_PACKAGE_MANIFEST_SHA256 = (
    "da33bc1708f7d21b92ceedc68710d5433a1aacbe6e32b8a7432bbab45d8cc788"
)
EXPECTED_BREAKER_SHA256 = (
    "62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a"
)
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402"
)
EXPECTED_SOURCE_CNF_SHA256 = (
    "76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7"
)
EXPECTED_SOURCE_BANK_SHA256 = (
    "b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00"
)
EXPECTED_RAW_PROOF_SHA256 = (
    "c17ed1ee2782270ed861462ae7bdd94420a2079edf419a7d778d7096a67d1be4"
)
EXPECTED_ADDITION_PROOF_SHA256 = (
    "c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3"
)
EXPECTED_CADICAL_SHA256 = (
    "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
)
EXPECTED_CADICAL_ARCHIVE_SHA256 = (
    "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e"
)
EXPECTED_DRAT_TRIM_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
EXPECTED_DRAT_TRIM_ARCHIVE_SHA256 = (
    "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
)
EXPECTED_PARSER_SHA256 = (
    "02c3c00faf7afb91a3217f5b738d0dacf7699875928162d01ce2df97e600007d"
)
EXPECTED_RUNTIME_PATHS = (
    "src/synthesis_k3/__init__.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/coloring.py",
    "src/synthesis_k3/generate.py",
    "src/synthesis_k3/cegar.py",
    "src/synthesis_k3/template_color_bank.py",
    "src/synthesis_k3/hole5_signature_breaker.py",
    "src/synthesis_k3/hole5_binary_production.py",
    "math/lemmas/hole5_signature_symmetry.md",
    "reviews/hole5_signature_symmetry_hostile_probe.py",
    "reviews/hole5_signature_symmetry_hostile_probe_log.json",
    "reviews/hole5_signature_symmetry_hostile_review.md",
    "reviews/hole5_signature_package_hostile_probe.py",
    "reviews/hole5_signature_package_hostile_probe_log.json",
    "reviews/hole5_signature_package_hostile_review.md",
    "reviews/hole5_binary_drat_hostile_probe.py",
    "reviews/hole5_binary_drat_hostile_probe_log.json",
    "reviews/hole5_binary_drat_hostile_review.md",
    "reviews/hole5_binary_production_hostile_probe.py",
    "reviews/hole5_binary_production_hostile_probe_log.json",
    "reviews/hole5_binary_production_hostile_review.md",
    "tests/test_hole5_signature_breaker.py",
    "tests/test_hole5_binary_production.py",
)
OUTPUT_NAMES = (
    "certificate.json",
    "checker.stderr",
    "checker.stdout",
    "outcome.json",
    "parser.stderr",
    "parser.stdout",
    "proof.additions.bdrat",
    "proof.raw.bdrat",
    "run_config.json",
    "solver.result",
    "solver.stderr",
    "solver.stdout",
)
TRANSIENT_PATTERNS = (
    re.compile(r".*\.partial(?:\..*)?\Z"),
    re.compile(r"\..*\.partial(?:\..*)?\Z"),
    re.compile(r".*\.tmp\Z"),
    re.compile(r".*\.lock\Z"),
)
RUN_KEYS = {
    "claim_boundary",
    "commands",
    "expected_head_commit",
    "gates",
    "git_source_binding",
    "immutable_input_bindings",
    "package",
    "resources",
    "runtime_source_manifest",
    "runtime_source_set_sha256",
    "schema",
    "schema_version",
    "seed",
    "source_package_path",
    "tools",
}
OUTCOME_KEYS = {
    "artifacts",
    "checker",
    "claim_status",
    "cnf_sha256",
    "disk_gates",
    "failures",
    "package_manifest_sha256",
    "parser",
    "parser_report",
    "run_config_sha256",
    "schema",
    "schema_version",
    "semantic_checks",
    "solver",
    "status",
}
CERTIFICATE_KEYS = {
    "activation_condition",
    "addition_only_binary_proof",
    "checker_command",
    "claim_boundary",
    "claim_status",
    "cnf_sha256",
    "package_manifest_sha256",
    "parser_command",
    "parser_report",
    "raw_binary_proof",
    "schema",
    "schema_version",
    "scope",
    "status",
    "strict_checker_requirements",
}
CHILD_KEYS = {
    "available_memory_before_bytes",
    "command",
    "command_sha256",
    "executable_sha256_after",
    "executable_sha256_before",
    "exit_code",
    "file_limit_mib",
    "finished_unix_ns",
    "maximum_resident_set_size_mib",
    "maximum_resident_set_size_raw",
    "maximum_resident_set_size_raw_unit",
    "memory_limit_exceeded",
    "memory_limit_mib",
    "peak_polled_resident_set_size_mib",
    "started_unix_ns",
    "stderr_path",
    "stderr_sha256",
    "stdout_path",
    "stdout_sha256",
    "system_cpu_seconds",
    "termination_signal",
    "timed_out",
    "user_cpu_seconds",
    "wall_limit_seconds",
    "wall_seconds",
}
PROOF_STAT_KEYS = {
    "addition_count",
    "addition_literal_count",
    "addition_stream_sha256",
    "addition_stream_size_bytes",
    "byte_count",
    "deletion_count",
    "deletion_literal_count",
    "deletion_stream_sha256",
    "deletion_stream_size_bytes",
    "empty_addition_count",
    "final_empty_record",
    "first_deletion_record",
    "maximum_clause_length",
    "maximum_variable",
    "proof_sha256",
    "record_count",
}
CHECKER_TIME = re.compile(
    rb"(?m)^c verification time: ([0-9]+(?:\.[0-9]+)?) seconds$"
)


class AuditFailure(ValueError):
    """A deterministic package-audit failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: object, *, pretty: bool = True) -> bytes:
    if pretty:
        encoded = json.dumps(
            value,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
    else:
        encoded = json.dumps(
            value,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    return (encoded + "\n").encode("utf-8")


def _reject_constant(value: str) -> object:
    raise AuditFailure(f"non-finite JSON constant {value!r}")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def strict_json_file(path: Path) -> object:
    payload = path.read_bytes()
    try:
        value = json.loads(
            payload.decode("utf-8"),
            parse_constant=_reject_constant,
            object_pairs_hook=_unique_object,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditFailure(f"malformed JSON: {path}") from error
    require(
        canonical_json_bytes(value) == payload,
        f"JSON is not canonical: {path}",
    )
    return value


def exact_mapping(
    value: object,
    keys: set[str],
    role: str,
) -> Mapping[str, object]:
    require(
        isinstance(value, Mapping) and set(value) == keys,
        f"{role} has the wrong key set",
    )
    return value


def assert_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            information = os.lstat(current)
        except FileNotFoundError:
            break
        require(
            not stat.S_ISLNK(information.st_mode),
            f"symlinked path component: {current}",
        )


def assert_regular_single_link(path: Path, role: str) -> os.stat_result:
    assert_no_symlink_components(path)
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise AuditFailure(f"missing {role}: {path}") from error
    require(stat.S_ISREG(information.st_mode), f"{role} is not regular")
    require(information.st_nlink == 1, f"{role} has multiple links")
    return information


def file_record(path: Path, *, relative: str) -> dict[str, object]:
    information = assert_regular_single_link(path, relative)
    return {
        "path": relative,
        "mode": f"{stat.S_IMODE(information.st_mode):04o}",
        "owner_writable": bool(information.st_mode & stat.S_IWUSR),
        "size_bytes": information.st_size,
        "sha256": sha256_file(path),
    }


def output_snapshot() -> dict[str, object]:
    assert_no_symlink_components(RUN)
    information = os.lstat(RUN)
    require(stat.S_ISDIR(information.st_mode), "run path is not a directory")
    names = tuple(sorted(path.name for path in RUN.iterdir()))
    require(names == OUTPUT_NAMES, "run directory entry set differs")
    transient = [
        name
        for name in names
        if any(pattern.fullmatch(name) for pattern in TRANSIENT_PATTERNS)
    ]
    require(not transient, "transient run entries remain")
    entries = [
        file_record(RUN / name, relative=name)
        for name in names
    ]
    return {
        "directory_mode": f"{stat.S_IMODE(information.st_mode):04o}",
        "directory_owner_writable": bool(
            information.st_mode & stat.S_IWUSR
        ),
        "entry_count": len(entries),
        "entries": entries,
        "transient_entries": transient,
    }


def tree_sha256(records: Sequence[Mapping[str, object]]) -> str:
    digest = hashlib.sha256()
    for record in records:
        relative = str(record["path"])
        path = relative.encode("utf-8")
        payload_path = RUN / relative
        payload = payload_path.read_bytes()
        digest.update(len(path).to_bytes(8, "big"))
        digest.update(path)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def binding_tree_sha256(
    records: Sequence[Mapping[str, object]],
) -> str:
    digest = hashlib.sha256()
    for record in records:
        role = str(record["role"]).encode("utf-8")
        payload = Path(str(record["absolute_path"])).read_bytes()
        digest.update(len(role).to_bytes(8, "big"))
        digest.update(role)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def git_command(arguments: Sequence[str]) -> subprocess.CompletedProcess[bytes]:
    executable = shutil.which("git")
    require(executable is not None, "git executable is unavailable")
    repository = ROOT.parent
    return subprocess.run(
        [
            str(executable),
            "--no-pager",
            "-C",
            str(repository),
            *arguments,
        ],
        env={
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "LC_ALL": "C",
            "PATH": str(Path(str(executable)).parent),
        },
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=30,
        check=False,
    )


def audit_runtime_sources(
    run_config: Mapping[str, object],
) -> tuple[list[dict[str, object]], str]:
    raw_rows = run_config["runtime_source_manifest"]
    require(isinstance(raw_rows, list), "runtime source manifest is not a list")
    require(len(raw_rows) == 23, "runtime source manifest is not 23 files")
    records: list[dict[str, object]] = []
    parsed_rows: list[tuple[str, str]] = []
    for index, row in enumerate(raw_rows):
        require(
            isinstance(row, list)
            and len(row) == 2
            and all(isinstance(value, str) for value in row),
            f"runtime source row {index} is malformed",
        )
        relative, expected_hash = row
        require(relative == EXPECTED_RUNTIME_PATHS[index], "source order differs")
        require(
            len(expected_hash) == 64,
            f"runtime source {relative} digest is malformed",
        )
        path = ROOT / relative
        information = assert_regular_single_link(path, relative)
        worktree_hash = sha256_file(path)
        require(
            worktree_hash == expected_hash,
            f"worktree source hash differs: {relative}",
        )
        git_path = f"gamma_theta_eternal_domination/{relative}"
        completed = git_command(
            ("show", f"{EXPECTED_SOURCE_COMMIT}:{git_path}")
        )
        require(
            completed.returncode == 0 and not completed.stderr,
            f"cannot read committed source: {relative}",
        )
        git_hash = sha256_bytes(completed.stdout)
        require(
            git_hash == expected_hash,
            f"Git-object source hash differs: {relative}",
        )
        records.append(
            {
                "path": relative,
                "size_bytes": information.st_size,
                "sha256": expected_hash,
                "worktree_matches": True,
                "git_object_matches": True,
            }
        )
        parsed_rows.append((relative, expected_hash))
    source_set = sha256_bytes(
        "".join(
            f"{relative} {digest}\n"
            for relative, digest in parsed_rows
        ).encode("ascii")
    )
    require(
        source_set == run_config["runtime_source_set_sha256"],
        "runtime source-set SHA-256 differs",
    )
    return records, source_set


def audit_binding(
    role: str,
    raw: object,
    expected_path: Path,
    expected_hash: str | None = None,
) -> dict[str, object]:
    binding = exact_mapping(
        raw,
        {"path", "sha256", "size_bytes"},
        f"binding {role}",
    )
    path = Path(str(binding["path"]))
    require(path == expected_path.resolve(), f"{role} path differs")
    information = assert_regular_single_link(path, role)
    actual_hash = sha256_file(path)
    require(
        binding["size_bytes"] == information.st_size
        and binding["sha256"] == actual_hash,
        f"{role} binding differs from bytes",
    )
    if expected_hash is not None:
        require(actual_hash == expected_hash, f"{role} anchor hash differs")
    return {
        "role": role,
        "path": (
            str(path.relative_to(ROOT))
            if path.is_relative_to(ROOT)
            else str(path)
        ),
        "absolute_path": str(path),
        "size_bytes": information.st_size,
        "sha256": actual_hash,
    }


def parse_dimacs_summary(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditFailure("CNF is not ASCII") from error
    require("\r" not in text and text.endswith("\n"), "CNF line form differs")
    lines = text.splitlines()
    header = re.fullmatch(r"p cnf ([1-9][0-9]*) ([1-9][0-9]*)", lines[0])
    require(header is not None, "CNF header is malformed")
    variables = int(header.group(1))
    declared = int(header.group(2))
    literals = 0
    for line in lines[1:]:
        tokens = line.split(" ")
        require(tokens and tokens[-1] == "0", "CNF clause terminator differs")
        values = [int(token) for token in tokens]
        require(0 not in values[:-1], "CNF contains an internal zero")
        require(
            all(0 < abs(value) <= variables for value in values[:-1]),
            "CNF literal exceeds variable range",
        )
        literals += len(values) - 1
    require(len(lines) - 1 == declared, "CNF clause count differs")
    return {
        "variables": variables,
        "clauses": declared,
        "literals": literals,
        "size_bytes": len(payload),
        "sha256": sha256_bytes(payload),
    }


def independent_signature_suffix() -> bytes:
    edge_variables = {
        (first, second): index
        for index, (first, second) in enumerate(
            (
                (first, second)
                for first in range(12)
                for second in range(first + 1, 12)
            ),
            start=1,
        )
    }
    signatures = {
        vertex: tuple(
            edge_variables[(core, vertex)] for core in range(6)
        )
        for vertex in range(6, 12)
    }
    clauses: list[tuple[int, ...]] = []
    for left_vertex, right_vertex in zip(range(6, 11), range(7, 12)):
        left = signatures[left_vertex]
        right = signatures[right_vertex]
        for first_difference in range(6):
            for prefix in product((False, True), repeat=first_difference):
                clause: list[int] = []
                for index, bit in enumerate(prefix):
                    if bit:
                        clause.extend((-left[index], -right[index]))
                    else:
                        clause.extend((left[index], right[index]))
                clause.extend(
                    (-left[first_difference], right[first_difference])
                )
                clauses.append(tuple(clause))
    require(
        len(clauses) == 315
        and sum(map(len, clauses)) == 3210
        and len(set(clauses)) == 315,
        "independent signature suffix counts differ",
    )
    payload = b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in clauses
    )
    require(
        len(payload) == 11424
        and sha256_bytes(payload)
        == "ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6",
        "independent signature suffix bytes differ",
    )
    return payload


def audit_package_identity(
    run_config: Mapping[str, object],
) -> dict[str, object]:
    require(
        tuple(sorted(path.name for path in DERIVED.iterdir()))
        == ("instance.cnf", "manifest.json", "signature_breaker.json"),
        "derived package entry set differs",
    )
    require(
        tuple(sorted(path.name for path in SOURCE.iterdir()))
        == ("coloring_bank.json", "instance.cnf", "manifest.json"),
        "source package entry set differs",
    )
    package = exact_mapping(
        run_config["package"],
        {
            "breaker_clause_stream_sha256",
            "breaker_sha256",
            "clause_count",
            "cnf_sha256",
            "literal_count",
            "manifest_sha256",
            "path",
            "variable_count",
        },
        "package record",
    )
    require(
        package
        == {
            "path": str(DERIVED.resolve()),
            "manifest_sha256": EXPECTED_PACKAGE_MANIFEST_SHA256,
            "cnf_sha256": EXPECTED_CNF_SHA256,
            "breaker_sha256": EXPECTED_BREAKER_SHA256,
            "variable_count": 6886,
            "clause_count": 23968,
            "literal_count": 192169,
            "breaker_clause_stream_sha256": (
                "ddd32969558030c22b7b4f182dfd9f96"
                "b65bb572a7e240957d202fb32b0158c6"
            ),
        },
        "package record differs from exact retained identity",
    )
    derived = {
        "instance.cnf": EXPECTED_CNF_SHA256,
        "manifest.json": EXPECTED_PACKAGE_MANIFEST_SHA256,
        "signature_breaker.json": EXPECTED_BREAKER_SHA256,
    }
    source = {
        "coloring_bank.json": EXPECTED_SOURCE_BANK_SHA256,
        "instance.cnf": EXPECTED_SOURCE_CNF_SHA256,
        "manifest.json": EXPECTED_SOURCE_MANIFEST_SHA256,
    }
    for directory, records, role in (
        (DERIVED, derived, "derived"),
        (SOURCE, source, "source"),
    ):
        for name, digest in records.items():
            assert_regular_single_link(directory / name, f"{role} {name}")
            require(
                sha256_file(directory / name) == digest,
                f"{role} package hash differs: {name}",
            )
    summary = parse_dimacs_summary(DERIVED / "instance.cnf")
    require(
        summary
        == {
            "variables": 6886,
            "clauses": 23968,
            "literals": 192169,
            "size_bytes": 754323,
            "sha256": EXPECTED_CNF_SHA256,
        },
        "derived CNF summary differs",
    )
    source_payload = (SOURCE / "instance.cnf").read_bytes()
    derived_payload = (DERIVED / "instance.cnf").read_bytes()
    source_lines = source_payload.splitlines(keepends=True)
    derived_lines = derived_payload.splitlines(keepends=True)
    require(
        source_lines[0] == b"p cnf 6886 23653\n"
        and derived_lines[0] == b"p cnf 6886 23968\n",
        "source/derived DIMACS headers differ",
    )
    require(
        derived_lines[1:23654] == source_lines[1:],
        "derived CNF does not preserve the exact source body",
    )
    suffix = independent_signature_suffix()
    require(
        b"".join(derived_lines[23654:]) == suffix,
        "derived CNF suffix differs from independent reconstruction",
    )
    reconstructed = (
        b"p cnf 6886 23968\n"
        + b"".join(source_lines[1:])
        + suffix
    )
    require(
        reconstructed == derived_payload,
        "full derived CNF reconstruction differs",
    )
    return {
        "derived_path": str(DERIVED_RELATIVE),
        "derived_files": derived,
        "source_path": str(SOURCE_RELATIVE),
        "source_files": source,
        "cnf_summary": summary,
        "independent_reconstruction": {
            "source_clause_body_preserved": True,
            "signature_clause_count": 315,
            "signature_literal_count": 3210,
            "signature_suffix_size_bytes": len(suffix),
            "signature_suffix_sha256": sha256_bytes(suffix),
            "full_byte_reconstruction": True,
        },
    }


def audit_committed_output(
    snapshot: Mapping[str, object],
) -> dict[str, object]:
    prefix = (
        "gamma_theta_eternal_domination/"
        f"{RUN_RELATIVE.as_posix()}"
    )
    subtree = git_command(
        (
            "ls-tree",
            "--full-tree",
            EXPECTED_PACKAGE_COMMIT,
            prefix,
        )
    )
    require(
        subtree.returncode == 0
        and not subtree.stderr
        and subtree.stdout
        == (
            f"040000 tree {EXPECTED_RUN_SUBTREE_OID}\t{prefix}\n"
        ).encode("ascii"),
        "committed run subtree identity differs",
    )
    listed = git_command(
        (
            "ls-tree",
            f"{EXPECTED_PACKAGE_COMMIT}:{prefix}",
        )
    )
    require(
        listed.returncode == 0 and not listed.stderr,
        "cannot enumerate committed run blobs",
    )
    parsed: list[tuple[str, str, str, str]] = []
    for line in listed.stdout.decode("utf-8").splitlines():
        match = re.fullmatch(
            r"([0-7]{6}) (blob|tree) ([0-9a-f]{40,64})\t(.+)",
            line,
        )
        require(match is not None, "committed run tree line is malformed")
        parsed.append(
            (
                match.group(1),
                match.group(2),
                match.group(3),
                match.group(4),
            )
        )
    parsed.sort(key=lambda row: row[3])
    committed_names = tuple(row[3] for row in parsed)
    require(committed_names == OUTPUT_NAMES, "committed run entry set differs")
    by_name = {
        str(record["path"]): record
        for record in snapshot["entries"]
    }
    records: list[dict[str, object]] = []
    for mode, object_type, object_id, name in parsed:
        require(
            mode == "100644" and object_type == "blob",
            f"committed output mode/type differs: {name}",
        )
        completed = git_command(
            (
                "show",
                f"{EXPECTED_PACKAGE_COMMIT}:{prefix}/{name}",
            )
        )
        require(
            completed.returncode == 0 and not completed.stderr,
            f"cannot read committed output: {name}",
        )
        digest = sha256_bytes(completed.stdout)
        require(
            digest == by_name[name]["sha256"]
            and len(completed.stdout) == by_name[name]["size_bytes"],
            f"committed output differs from worktree: {name}",
        )
        records.append(
            {
                "path": name,
                "git_mode": mode,
                "git_type": object_type,
                "git_blob_oid": object_id,
                "size_bytes": len(completed.stdout),
                "sha256": digest,
            }
        )
    return {
        "commit": EXPECTED_PACKAGE_COMMIT,
        "subtree_mode": "040000",
        "subtree_type": "tree",
        "subtree_oid": EXPECTED_RUN_SUBTREE_OID,
        "entry_count": len(records),
        "worktree_matches_commit": True,
        "records": records,
    }


def command_sha256(command: Sequence[str]) -> str:
    return sha256_bytes(canonical_json_bytes(list(command), pretty=False))


def audit_child(
    role: str,
    raw: object,
    *,
    expected_command: Sequence[str],
    expected_exit: int,
    expected_memory_mib: int,
    expected_wall_seconds: int,
    expected_executable_hash: str,
) -> dict[str, object]:
    child = exact_mapping(raw, CHILD_KEYS, f"{role} child")
    require(child["command"] == list(expected_command), f"{role} command differs")
    require(
        child["command_sha256"] == command_sha256(expected_command),
        f"{role} command hash differs",
    )
    require(child["exit_code"] == expected_exit, f"{role} exit code differs")
    require(
        child["termination_signal"] is None
        and child["timed_out"] is False
        and child["memory_limit_exceeded"] is False,
        f"{role} did not terminate cleanly",
    )
    require(
        child["memory_limit_mib"] == expected_memory_mib
        and child["wall_limit_seconds"] == expected_wall_seconds
        and child["file_limit_mib"] == 512,
        f"{role} resource record differs",
    )
    require(
        child["executable_sha256_before"] == expected_executable_hash
        and child["executable_sha256_after"] == expected_executable_hash,
        f"{role} executable binding differs",
    )
    require(
        type(child["started_unix_ns"]) is int
        and type(child["finished_unix_ns"]) is int
        and child["started_unix_ns"] < child["finished_unix_ns"],
        f"{role} timestamps differ",
    )
    require(
        isinstance(child["wall_seconds"], (int, float))
        and 0 <= child["wall_seconds"] <= expected_wall_seconds,
        f"{role} wall duration differs",
    )
    require(
        isinstance(child["maximum_resident_set_size_mib"], (int, float))
        and 0
        <= child["maximum_resident_set_size_mib"]
        <= expected_memory_mib,
        f"{role} memory record differs",
    )
    require(
        child["available_memory_before_bytes"]
        >= (expected_memory_mib + 512) << 20,
        f"{role} available-memory gate differs",
    )
    for stream in ("stdout", "stderr"):
        path = RUN / f"{role}.{stream}"
        require(
            child[f"{stream}_path"] == str(path.resolve())
            and child[f"{stream}_sha256"] == sha256_file(path),
            f"{role} {stream} binding differs",
        )
    return {
        "exit_code": expected_exit,
        "command_sha256": child["command_sha256"],
        "wall_seconds": child["wall_seconds"],
        "user_cpu_seconds": child["user_cpu_seconds"],
        "system_cpu_seconds": child["system_cpu_seconds"],
        "maximum_resident_set_size_mib": child[
            "maximum_resident_set_size_mib"
        ],
        "memory_limit_mib": expected_memory_mib,
        "wall_limit_seconds": expected_wall_seconds,
        "file_limit_mib": 512,
    }


def encode_uvarint(value: int) -> bytes:
    require(type(value) is int and value >= 0, "uvarint value is invalid")
    result = bytearray()
    while True:
        low = value & 0x7F
        value >>= 7
        if value:
            result.append(low | 0x80)
        else:
            result.append(low)
            return bytes(result)


def parse_binary_drat_independent(
    path: Path,
    *,
    allow_deletions: bool,
    exact_addition_stream: bytes | None = None,
) -> dict[str, object]:
    payload = path.read_bytes()
    index = 0
    record_count = 0
    addition_count = 0
    deletion_count = 0
    addition_literals = 0
    deletion_literals = 0
    maximum_variable = 0
    maximum_clause_length = 0
    empty_additions = 0
    final_empty_record = 0
    first_deletion: int | None = None
    seen_empty = False
    addition_digest = hashlib.sha256()
    deletion_digest = hashlib.sha256()
    addition_bytes = 0
    deletion_bytes = 0
    addition_cursor = 0
    while index < len(payload):
        require(not seen_empty, "binary proof continues after empty addition")
        start = index
        prefix = payload[index]
        index += 1
        require(prefix in (ord("a"), ord("d")), "binary proof prefix differs")
        deletion = prefix == ord("d")
        require(allow_deletions or not deletion, "unexpected proof deletion")
        record_count += 1
        literals: list[int] = []
        literal_set: set[int] = set()
        while True:
            encoded = 0
            shift = 0
            raw_varint = bytearray()
            for _ in range(9):
                require(index < len(payload), "binary proof varint is truncated")
                byte = payload[index]
                index += 1
                raw_varint.append(byte)
                encoded |= (byte & 0x7F) << shift
                if byte < 0x80:
                    break
                shift += 7
            else:
                raise AuditFailure("binary proof varint exceeds nine bytes")
            require(
                bytes(raw_varint) == encode_uvarint(encoded),
                "binary proof varint is noncanonical",
            )
            if encoded == 0:
                break
            require(encoded != 1, "binary proof contains negative zero")
            variable = encoded >> 1
            require(
                1 <= variable <= 6886,
                "binary proof variable exceeds 6886",
            )
            literal = -variable if encoded & 1 else variable
            require(
                literal not in literal_set,
                "binary proof repeats a signed literal",
            )
            require(
                -literal not in literal_set,
                "binary proof contains a tautological record",
            )
            literal_set.add(literal)
            literals.append(literal)
        require(not deletion or literals, "binary proof deletes empty clause")
        record = payload[start:index]
        maximum_clause_length = max(
            maximum_clause_length, len(literals)
        )
        if literals:
            maximum_variable = max(
                maximum_variable,
                max(abs(literal) for literal in literals),
            )
        if deletion:
            deletion_count += 1
            deletion_literals += len(literals)
            deletion_digest.update(record)
            deletion_bytes += len(record)
            if first_deletion is None:
                first_deletion = record_count
        else:
            addition_count += 1
            addition_literals += len(literals)
            addition_digest.update(record)
            addition_bytes += len(record)
            if exact_addition_stream is not None:
                require(
                    exact_addition_stream[
                        addition_cursor:addition_cursor + len(record)
                    ]
                    == record,
                    "raw proof addition differs from retained addition stream",
                )
                addition_cursor += len(record)
            if not literals:
                empty_additions += 1
                final_empty_record = record_count
                seen_empty = True
    require(payload, "binary proof is empty")
    require(
        empty_additions == 1 and final_empty_record == record_count,
        "binary proof lacks its unique final empty addition",
    )
    if exact_addition_stream is not None:
        require(
            addition_cursor == len(exact_addition_stream),
            "retained addition stream has unmatched trailing bytes",
        )
    return {
        "byte_count": len(payload),
        "record_count": record_count,
        "addition_count": addition_count,
        "deletion_count": deletion_count,
        "addition_literal_count": addition_literals,
        "deletion_literal_count": deletion_literals,
        "maximum_variable": maximum_variable,
        "maximum_clause_length": maximum_clause_length,
        "empty_addition_count": empty_additions,
        "final_empty_record": final_empty_record,
        "first_deletion_record": first_deletion,
        "proof_sha256": sha256_bytes(payload),
        "addition_stream_sha256": addition_digest.hexdigest(),
        "deletion_stream_sha256": deletion_digest.hexdigest(),
        "addition_stream_size_bytes": addition_bytes,
        "deletion_stream_size_bytes": deletion_bytes,
    }


def proof_stat(raw: object, role: str) -> Mapping[str, object]:
    record = exact_mapping(raw, PROOF_STAT_KEYS, role)
    integer_keys = PROOF_STAT_KEYS - {
        "addition_stream_sha256",
        "deletion_stream_sha256",
        "proof_sha256",
        "first_deletion_record",
    }
    require(
        all(type(record[key]) is int and record[key] >= 0 for key in integer_keys),
        f"{role} has malformed integer statistics",
    )
    require(
        record["record_count"]
        == record["addition_count"] + record["deletion_count"],
        f"{role} record counts differ",
    )
    require(
        record["byte_count"]
        == (
            record["addition_stream_size_bytes"]
            + record["deletion_stream_size_bytes"]
        ),
        f"{role} byte counts differ",
    )
    require(
        record["maximum_variable"] <= 6886,
        f"{role} maximum variable differs",
    )
    return record


def audit_parser_report(
    raw: object,
    snapshot: Mapping[str, Mapping[str, object]],
) -> dict[str, object]:
    report = exact_mapping(
        raw,
        {
            "addition_only",
            "all_addition_bytes_preserved_in_order",
            "source",
        },
        "parser report",
    )
    require(
        report["all_addition_bytes_preserved_in_order"] is True,
        "parser preservation flag differs",
    )
    source = proof_stat(report["source"], "source proof")
    addition = proof_stat(report["addition_only"], "addition-only proof")
    raw_file = snapshot["proof.raw.bdrat"]
    addition_file = snapshot["proof.additions.bdrat"]
    require(
        source["proof_sha256"] == raw_file["sha256"]
        == EXPECTED_RAW_PROOF_SHA256
        and source["byte_count"] == raw_file["size_bytes"] == 12524020,
        "raw proof report differs",
    )
    require(
        addition["proof_sha256"] == addition_file["sha256"]
        == EXPECTED_ADDITION_PROOF_SHA256
        and addition["byte_count"] == addition_file["size_bytes"] == 6337621,
        "addition proof report differs",
    )
    require(
        source["addition_stream_sha256"] == addition["proof_sha256"]
        and source["addition_stream_size_bytes"] == addition["byte_count"]
        and source["addition_count"] == addition["addition_count"]
        and source["addition_literal_count"]
        == addition["addition_literal_count"],
        "source additions differ from stripped proof",
    )
    require(
        addition["deletion_count"] == 0
        and addition["deletion_literal_count"] == 0
        and addition["deletion_stream_size_bytes"] == 0
        and addition["empty_addition_count"] == 1
        and addition["final_empty_record"] == addition["record_count"],
        "addition-only proof invariants differ",
    )
    require(
        source["deletion_count"] == 245439
        and source["first_deletion_record"] == 96
        and source["empty_addition_count"] == 1
        and source["final_empty_record"] == source["record_count"],
        "raw proof deletion/final invariants differ",
    )
    return {
        "raw": dict(source),
        "addition_only": dict(addition),
        "all_addition_bytes_preserved_in_order": True,
    }


def normalize_checker_stdout(payload: bytes) -> tuple[bytes, str]:
    normalized = payload.replace(b"\r", b"")
    matches = CHECKER_TIME.findall(normalized)
    require(len(matches) == 1, "checker output lacks one timing line")
    elapsed = matches[0].decode("ascii")
    stable = CHECKER_TIME.sub(
        b"c verification time: <nondeterministic-seconds> seconds",
        normalized,
    )
    return stable, elapsed


class HeavyChildLock:
    def __init__(self) -> None:
        root_digest = sha256_bytes(str(ROOT.resolve()).encode("utf-8"))[:20]
        self.path = (
            Path(tempfile.gettempdir())
            / f"gamma-theta-k3-heavy-child-{root_digest}.lock"
        )
        self.descriptor: int | None = None

    def __enter__(self) -> "HeavyChildLock":
        descriptor = os.open(self.path, os.O_CREAT | os.O_RDWR, 0o600)
        information = os.fstat(descriptor)
        require(
            stat.S_ISREG(information.st_mode)
            and information.st_nlink == 1,
            "campaign heavy-child lock is unsafe",
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise AuditFailure("another campaign heavy child is active") from error
        self.descriptor = descriptor
        return self

    def __exit__(self, *ignored: object) -> None:
        require(self.descriptor is not None, "heavy-child lock was not held")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


def run_readonly(
    command: Sequence[str],
    *,
    timeout: int,
) -> subprocess.CompletedProcess[bytes]:
    with HeavyChildLock():
        return subprocess.run(
            list(command),
            cwd=ROOT,
            env={},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=timeout,
            check=False,
        )


def replay_proof(
    run_config: Mapping[str, object],
    retained_report: Mapping[str, object],
) -> dict[str, object]:
    tools = exact_mapping(
        run_config["tools"],
        {"cadical", "clean_room_parser", "drat_trim", "python"},
        "tools",
    )
    python = exact_mapping(
        tools["python"],
        {"implementation", "path", "sha256", "version"},
        "Python tool",
    )
    parser = exact_mapping(
        tools["clean_room_parser"],
        {"path", "sha256"},
        "parser tool",
    )
    checker = exact_mapping(
        tools["drat_trim"],
        {
            "commit",
            "path",
            "role",
            "sha256",
            "source_archive_path",
            "source_archive_sha256",
            "version",
        },
        "checker tool",
    )
    with tempfile.TemporaryDirectory(
        prefix=".hole5-binary-package-audit-",
        dir=ROOT / "results/logs",
    ) as temporary_name:
        temporary = Path(temporary_name)
        addition = temporary / "proof.additions.bdrat"
        parser_command = (
            str(python["path"]),
            "-I",
            "-B",
            str(parser["path"]),
            "strip",
            "--proof",
            str((RUN / "proof.raw.bdrat").resolve()),
            "--output",
            str(addition),
            "--max-var",
            "6886",
        )
        parsed = run_readonly(parser_command, timeout=180)
        require(parsed.returncode == 0, "clean-room parser replay failed")
        require(not parsed.stderr, "clean-room parser replay emitted stderr")
        require(
            parsed.stdout == (RUN / "parser.stdout").read_bytes(),
            "clean-room parser replay report differs",
        )
        require(
            sha256_file(addition) == EXPECTED_ADDITION_PROOF_SHA256
            and addition.stat().st_size == 6337621,
            "clean-room parser replay proof differs",
        )
        replay_report = json.loads(parsed.stdout.decode("utf-8"))
        require(
            replay_report == dict(retained_report),
            "clean-room parser replay object differs",
        )
        checker_command = (
            str(checker["path"]),
            str((DERIVED / "instance.cnf").resolve()),
            str(addition),
            "-i",
            "-f",
            "-W",
            "-U",
            "-t",
            "1200",
        )
        checked = run_readonly(checker_command, timeout=180)
        require(checked.returncode == 0, "strict checker replay failed")
        require(not checked.stderr, "strict checker replay emitted stderr")
        stable_replay, _ = normalize_checker_stdout(
            checked.stdout
        )
        stable_retained, _ = normalize_checker_stdout(
            (RUN / "checker.stdout").read_bytes()
        )
        require(
            stable_replay == stable_retained,
            "strict checker normalized replay differs",
        )
        text = stable_replay.decode("ascii")
        require(
            text.splitlines().count("s VERIFIED") == 1
            and text.count("RAT lemmas in core") == 1
            and "c 0 RAT lemmas in core;" in text
            and "warning" not in text.lower(),
            "strict checker replay boundary differs",
        )
        return {
            "solver_replayed": False,
            "solver_replay_reason": (
                "The solver need not be rerun; the retained proof is "
                "independently parsed and strictly replayed."
            ),
            "parser": {
                "exit_code": parsed.returncode,
                "stderr_sha256": sha256_bytes(parsed.stderr),
                "stdout_sha256": sha256_bytes(parsed.stdout),
                "addition_proof_sha256": sha256_file(addition),
                "addition_proof_size_bytes": addition.stat().st_size,
                "exact_retained_report_match": True,
            },
            "checker": {
                "exit_code": checked.returncode,
                "stderr_sha256": sha256_bytes(checked.stderr),
                "normalized_stdout_sha256": sha256_bytes(stable_replay),
                "normalized_retained_match": True,
                "verified_status_count": 1,
                "rat_lemmas_in_core": 0,
                "timing_line_present": True,
                "warning_free": True,
            },
        }


def audit_tools(
    run_config: Mapping[str, object],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    tools = exact_mapping(
        run_config["tools"],
        {"cadical", "clean_room_parser", "drat_trim", "python"},
        "tools",
    )
    expected = {
        "cadical": (
            ROOT / "tools/cadical_3_0_1/build/cadical",
            EXPECTED_CADICAL_SHA256,
            ROOT / "tools/cadical_3_0_1.tar.gz",
            EXPECTED_CADICAL_ARCHIVE_SHA256,
            "c60730422e758ef1cebe7aeddf2dda31c996bf04",
            "3.0.1",
        ),
        "drat_trim": (
            ROOT / "tools/drat_trim_2023_05_22/drat-trim",
            EXPECTED_DRAT_TRIM_SHA256,
            ROOT / "tools/drat_trim_2023_05_22.tar.gz",
            EXPECTED_DRAT_TRIM_ARCHIVE_SHA256,
            "2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
            None,
        ),
    }
    bindings: list[dict[str, object]] = []
    result: dict[str, object] = {}
    for name, role in (("cadical", "cadical"), ("drat_trim", "drat-trim")):
        record = exact_mapping(
            tools[name],
            {
                "commit",
                "path",
                "role",
                "sha256",
                "source_archive_path",
                "source_archive_sha256",
                "version",
            },
            f"tool {name}",
        )
        path, digest, archive, archive_digest, commit, version = expected[name]
        require(
            record
            == {
                "role": role,
                "path": str(path.resolve()),
                "sha256": digest,
                "source_archive_path": str(archive.resolve()),
                "source_archive_sha256": archive_digest,
                "commit": commit,
                "version": version,
            },
            f"tool record differs: {name}",
        )
        for binding_role, binding_path, binding_hash in (
            (f"tool:{name}", path, digest),
            (f"tool:{name}:source", archive, archive_digest),
        ):
            information = assert_regular_single_link(
                binding_path, binding_role
            )
            require(
                sha256_file(binding_path) == binding_hash,
                f"tool bytes differ: {binding_role}",
            )
            bindings.append(
                {
                    "role": binding_role,
                    "path": str(binding_path.relative_to(ROOT)),
                    "absolute_path": str(binding_path.resolve()),
                    "size_bytes": information.st_size,
                    "sha256": binding_hash,
                }
            )
        result[name] = {
            "version": version,
            "commit": commit,
            "binary_sha256": digest,
            "source_archive_sha256": archive_digest,
        }
    parser = exact_mapping(
        tools["clean_room_parser"],
        {"path", "sha256"},
        "parser tool",
    )
    require(
        parser
        == {
            "path": str(
                (ROOT / "reviews/hole5_binary_drat_hostile_probe.py").resolve()
            ),
            "sha256": EXPECTED_PARSER_SHA256,
        },
        "clean-room parser record differs",
    )
    python = exact_mapping(
        tools["python"],
        {"implementation", "path", "sha256", "version"},
        "Python tool",
    )
    python_path = Path(str(python["path"]))
    require(
        python["implementation"] == "CPython"
        and python["version"] == "3.14.6"
        and sha256_file(python_path) == python["sha256"],
        "Python tool record differs",
    )
    version = subprocess.run(
        [str(python_path), "--version"],
        env={},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=10,
        check=False,
    )
    require(
        version.returncode == 0
        and version.stdout == b"Python 3.14.6\n"
        and not version.stderr,
        "Python version output differs",
    )
    cadical_version = subprocess.run(
        [str(expected["cadical"][0]), "--version"],
        env={},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=10,
        check=False,
    )
    require(
        cadical_version.returncode == 0
        and cadical_version.stdout == b"3.0.1\n"
        and not cadical_version.stderr,
        "CaDiCaL version output differs",
    )
    result["clean_room_parser"] = {
        "sha256": EXPECTED_PARSER_SHA256,
    }
    result["python"] = {
        "implementation": "CPython",
        "version": "3.14.6",
        "sha256": python["sha256"],
    }
    return result, bindings


def audit() -> dict[str, object]:
    first_snapshot = output_snapshot()
    first_by_name = {
        str(record["path"]): record
        for record in first_snapshot["entries"]
    }
    require(
        first_by_name["run_config.json"]["sha256"]
        == EXPECTED_RUN_CONFIG_SHA256,
        "run-config anchor differs",
    )
    require(
        first_by_name["outcome.json"]["sha256"]
        == EXPECTED_OUTCOME_SHA256,
        "outcome anchor differs",
    )
    require(
        first_by_name["certificate.json"]["sha256"]
        == EXPECTED_CERTIFICATE_SHA256,
        "certificate anchor differs",
    )
    run_config = exact_mapping(
        strict_json_file(RUN / "run_config.json"),
        RUN_KEYS,
        "run config",
    )
    outcome = exact_mapping(
        strict_json_file(RUN / "outcome.json"),
        OUTCOME_KEYS,
        "outcome",
    )
    certificate = exact_mapping(
        strict_json_file(RUN / "certificate.json"),
        CERTIFICATE_KEYS,
        "certificate",
    )
    require(
        run_config["schema"]
        == "gamma-theta-hole5-binary-production-config-v1"
        and run_config["schema_version"] == 1
        and run_config["expected_head_commit"] == EXPECTED_SOURCE_COMMIT
        and run_config["seed"] == 0,
        "run-config identity differs",
    )
    require(
        outcome["schema"]
        == "gamma-theta-hole5-binary-production-outcome-v1"
        and outcome["schema_version"] == 1
        and outcome["status"] == "UNSAT_VERIFIED_FINITE_CERTIFICATE"
        and outcome["claim_status"] == "VERIFIED_FINITE_CERTIFICATE"
        and outcome["failures"] == [],
        "outcome status/schema differs",
    )
    require(
        certificate["schema"]
        == "gamma-theta-hole5-binary-certificate-v1"
        and certificate["schema_version"] == 1
        and certificate["status"] == "UNSAT_REPLAY_ARTIFACT"
        and certificate["claim_status"]
        == "NO_STANDALONE_MATHEMATICAL_CLAIM",
        "certificate status/schema differs",
    )
    require(
        outcome["run_config_sha256"] == EXPECTED_RUN_CONFIG_SHA256
        and outcome["cnf_sha256"] == EXPECTED_CNF_SHA256
        and certificate["cnf_sha256"] == EXPECTED_CNF_SHA256
        and outcome["package_manifest_sha256"]
        == EXPECTED_PACKAGE_MANIFEST_SHA256
        and certificate["package_manifest_sha256"]
        == EXPECTED_PACKAGE_MANIFEST_SHA256,
        "cross-artifact anchors differ",
    )
    require(
        certificate["activation_condition"]
        == {
            "required_claim_status": "VERIFIED_FINITE_CERTIFICATE",
            "required_file": "outcome.json",
            "required_self_hash_binding": (
                "outcome.artifacts.certificate.json.sha256"
            ),
            "required_status": "UNSAT_VERIFIED_FINITE_CERTIFICATE",
        },
        "certificate activation condition differs",
    )
    require(
        certificate["raw_binary_proof"]
        == {
            "path": "proof.raw.bdrat",
            "preserved": True,
            "sha256": EXPECTED_RAW_PROOF_SHA256,
            "size_bytes": 12524020,
        }
        and certificate["addition_only_binary_proof"]
        == {
            "path": "proof.additions.bdrat",
            "sha256": EXPECTED_ADDITION_PROOF_SHA256,
            "size_bytes": 6337621,
        },
        "certificate proof bindings differ",
    )
    require(
        certificate["strict_checker_requirements"]
        == {
            "binary_input": True,
            "exactly_one_verified_line": True,
            "forward": True,
            "rup_only": True,
            "warning_fatal": True,
            "zero_rat_lemmas": True,
        },
        "certificate checker requirements differ",
    )
    artifacts = outcome["artifacts"]
    require(isinstance(artifacts, Mapping), "outcome artifacts are malformed")
    expected_artifacts = set(OUTPUT_NAMES) - {"outcome.json"}
    require(set(artifacts) == expected_artifacts, "artifact coverage differs")
    for name, record in artifacts.items():
        bound = exact_mapping(
            record,
            {"sha256", "size_bytes"},
            f"output artifact {name}",
        )
        observed = first_by_name[name]
        require(
            bound["sha256"] == observed["sha256"]
            and bound["size_bytes"] == observed["size_bytes"],
            f"outcome artifact binding differs: {name}",
        )
    require(
        artifacts["certificate.json"]["sha256"]
        == EXPECTED_CERTIFICATE_SHA256,
        "outcome does not activate exact certificate",
    )
    source_records, source_set = audit_runtime_sources(run_config)
    git_binding = run_config["git_source_binding"]
    require(
        git_binding
        == {
            "global_worktree_cleanliness_required": False,
            "head_commit": EXPECTED_SOURCE_COMMIT,
            "repository_relative_campaign_path": (
                "gamma_theta_eternal_domination"
            ),
            "runtime_source_mismatches": [],
            "runtime_sources_match_head": True,
        },
        "Git source binding differs",
    )
    source_ancestry = git_command(
        (
            "merge-base",
            "--is-ancestor",
            EXPECTED_SOURCE_COMMIT,
            EXPECTED_PACKAGE_COMMIT,
        )
    )
    require(
        source_ancestry.returncode == 0,
        "package commit does not descend from source commit",
    )
    for revision in ("HEAD", "origin/main"):
        ancestry = git_command(
            (
                "merge-base",
                "--is-ancestor",
                EXPECTED_PACKAGE_COMMIT,
                revision,
            )
        )
        require(
            ancestry.returncode == 0,
            f"{revision} does not contain the package commit",
        )
    committed_output = audit_committed_output(first_snapshot)
    package = audit_package_identity(run_config)
    tools, tool_bindings = audit_tools(run_config)
    immutable = run_config["immutable_input_bindings"]
    require(
        isinstance(immutable, Mapping) and len(immutable) == 35,
        "immutable binding count differs",
    )
    expected_binding_keys = {
        *(f"runtime:{relative}" for relative in EXPECTED_RUNTIME_PATHS),
        "derived:instance.cnf",
        "derived:manifest.json",
        "derived:signature_breaker.json",
        "source:coloring_bank.json",
        "source:instance.cnf",
        "source:manifest.json",
        "tool:cadical",
        "tool:cadical:source",
        "tool:drat_trim",
        "tool:drat_trim:source",
        "tool:parser",
        "tool:python",
    }
    require(
        set(immutable) == expected_binding_keys,
        "immutable binding role set differs",
    )
    external_records: list[dict[str, object]] = []
    runtime_hashes = {
        record["path"]: record["sha256"] for record in source_records
    }
    for relative in EXPECTED_RUNTIME_PATHS:
        external_records.append(
            audit_binding(
                f"runtime:{relative}",
                immutable[f"runtime:{relative}"],
                ROOT / relative,
                str(runtime_hashes[relative]),
            )
        )
    fixed_bindings = (
        (
            "derived:instance.cnf",
            DERIVED / "instance.cnf",
            EXPECTED_CNF_SHA256,
        ),
        (
            "derived:manifest.json",
            DERIVED / "manifest.json",
            EXPECTED_PACKAGE_MANIFEST_SHA256,
        ),
        (
            "derived:signature_breaker.json",
            DERIVED / "signature_breaker.json",
            EXPECTED_BREAKER_SHA256,
        ),
        (
            "source:coloring_bank.json",
            SOURCE / "coloring_bank.json",
            EXPECTED_SOURCE_BANK_SHA256,
        ),
        (
            "source:instance.cnf",
            SOURCE / "instance.cnf",
            EXPECTED_SOURCE_CNF_SHA256,
        ),
        (
            "source:manifest.json",
            SOURCE / "manifest.json",
            EXPECTED_SOURCE_MANIFEST_SHA256,
        ),
        (
            "tool:parser",
            ROOT / "reviews/hole5_binary_drat_hostile_probe.py",
            EXPECTED_PARSER_SHA256,
        ),
    )
    for role, path, digest in fixed_bindings:
        external_records.append(
            audit_binding(role, immutable[role], path, digest)
        )
    tool_by_role = {record["role"]: record for record in tool_bindings}
    for role in (
        "tool:cadical",
        "tool:cadical:source",
        "tool:drat_trim",
        "tool:drat_trim:source",
    ):
        expected = tool_by_role[role]
        external_records.append(
            audit_binding(
                role,
                immutable[role],
                Path(str(expected["absolute_path"])),
                str(expected["sha256"]),
            )
        )
    python_path = Path(str(run_config["tools"]["python"]["path"]))
    external_records.append(
        audit_binding(
            "tool:python",
            immutable["tool:python"],
            python_path,
            str(run_config["tools"]["python"]["sha256"]),
        )
    )
    external_records.sort(key=lambda record: str(record["role"]))
    commands = exact_mapping(
        run_config["commands"],
        {"checker", "parser", "solver"},
        "commands",
    )
    expected_solver = (
        str((ROOT / "tools/cadical_3_0_1/build/cadical").resolve()),
        "--seed=0",
        "--binary",
        "--no-colors",
        "-q",
        "-t",
        "600",
        "-w",
        str((RUN / "solver.result").resolve()),
        str((DERIVED / "instance.cnf").resolve()),
        str((RUN / "proof.raw.bdrat").resolve()),
    )
    expected_parser = (
        str(run_config["tools"]["python"]["path"]),
        "-I",
        "-B",
        str(
            (ROOT / "reviews/hole5_binary_drat_hostile_probe.py").resolve()
        ),
        "strip",
        "--proof",
        str((RUN / "proof.raw.bdrat").resolve()),
        "--output",
        str((RUN / "proof.additions.bdrat").resolve()),
        "--max-var",
        "6886",
    )
    expected_checker = (
        str((ROOT / "tools/drat_trim_2023_05_22/drat-trim").resolve()),
        str((DERIVED / "instance.cnf").resolve()),
        str((RUN / "proof.additions.bdrat").resolve()),
        "-i",
        "-f",
        "-W",
        "-U",
        "-t",
        "1200",
    )
    require(
        commands
        == {
            "solver": list(expected_solver),
            "parser": list(expected_parser),
            "checker": list(expected_checker),
        },
        "run commands differ",
    )
    require(
        certificate["parser_command"] == list(expected_parser)
        and certificate["checker_command"] == list(expected_checker),
        "certificate commands differ",
    )
    resources = run_config["resources"]
    require(
        run_config["gates"]
        == {
            "atomic_new_output": True,
            "hostile_audit_gate": True,
            "raw_binary_proof_preserved": True,
            "source_to_head_gate": True,
            "validation_gate": True,
        },
        "run gates differ",
    )
    require(
        resources
        == {
            "physical_memory_bytes": 17179869184,
            "maximum_responsive_child_memory_mib": 4096,
            "solver_internal_seconds": 600,
            "solver_supervisor_seconds": 615,
            "parser_supervisor_seconds": 615,
            "checker_internal_seconds": 1200,
            "checker_supervisor_seconds": 1215,
            "solver_memory_mib": 1024,
            "parser_memory_mib": 512,
            "checker_memory_mib": 2048,
            "file_limit_mib": 512,
            "disk_reserve_mib": 4096,
            "initial_disk_gate": resources["initial_disk_gate"],
        },
        "run resource record differs",
    )
    initial_disk = resources["initial_disk_gate"]
    require(
        initial_disk["remaining_file_slots"] == 9
        and initial_disk["required_bytes"] == 9160359936
        and initial_disk["free_bytes"] >= initial_disk["required_bytes"],
        "initial disk gate differs",
    )
    for role, slots, required in (
        ("before_parser", 5, 7012876288),
        ("before_checker", 2, 5402263552),
    ):
        disk = outcome["disk_gates"][role]
        require(
            disk["remaining_file_slots"] == slots
            and disk["required_bytes"] == required
            and disk["free_bytes"] >= required,
            f"{role} disk gate differs",
        )
    require(
        set(outcome["disk_gates"]) == {"before_checker", "before_parser"},
        "outcome disk-gate role set differs",
    )
    children = {
        "solver": audit_child(
            "solver",
            outcome["solver"],
            expected_command=expected_solver,
            expected_exit=20,
            expected_memory_mib=1024,
            expected_wall_seconds=615,
            expected_executable_hash=EXPECTED_CADICAL_SHA256,
        ),
        "parser": audit_child(
            "parser",
            outcome["parser"],
            expected_command=expected_parser,
            expected_exit=0,
            expected_memory_mib=512,
            expected_wall_seconds=615,
            expected_executable_hash=str(
                run_config["tools"]["python"]["sha256"]
            ),
        ),
        "checker": audit_child(
            "checker",
            outcome["checker"],
            expected_command=expected_checker,
            expected_exit=0,
            expected_memory_mib=2048,
            expected_wall_seconds=1215,
            expected_executable_hash=EXPECTED_DRAT_TRIM_SHA256,
        ),
    }
    require(
        (RUN / "solver.result").read_bytes() == b"s UNSATISFIABLE\n"
        and not (RUN / "solver.stdout").read_bytes()
        and not (RUN / "solver.stderr").read_bytes(),
        "solver terminal artifacts differ",
    )
    parser_object = strict_json_file(RUN / "parser.stdout")
    require(not (RUN / "parser.stderr").read_bytes(), "parser stderr is nonempty")
    parser_report = audit_parser_report(
        outcome["parser_report"], first_by_name
    )
    require(
        parser_object == outcome["parser_report"]
        and certificate["parser_report"] == outcome["parser_report"],
        "parser reports differ across artifacts",
    )
    retained_addition_bytes = (
        RUN / "proof.additions.bdrat"
    ).read_bytes()
    independent_raw_stats = parse_binary_drat_independent(
        RUN / "proof.raw.bdrat",
        allow_deletions=True,
        exact_addition_stream=retained_addition_bytes,
    )
    independent_addition_stats = parse_binary_drat_independent(
        RUN / "proof.additions.bdrat",
        allow_deletions=False,
    )
    require(
        independent_raw_stats == outcome["parser_report"]["source"]
        and independent_addition_stats
        == outcome["parser_report"]["addition_only"],
        "independent binary-proof statistics differ",
    )
    stable_checker, retained_checker_seconds = normalize_checker_stdout(
        (RUN / "checker.stdout").read_bytes()
    )
    checker_text = stable_checker.decode("ascii")
    require(
        not (RUN / "checker.stderr").read_bytes()
        and checker_text.splitlines().count("s VERIFIED") == 1
        and checker_text.count("RAT lemmas in core") == 1
        and "c 0 RAT lemmas in core;" in checker_text
        and "warning" not in checker_text.lower(),
        "retained checker boundary differs",
    )
    require(
        outcome["semantic_checks"]
        == {
            "addition_only_reparsed": True,
            "all_deletions_removed": True,
            "checker_warning_free": True,
            "checker_zero_rat_lemmas": True,
            "clean_room_parser_max_var": 6886,
            "raw_binary_proof_preserved": True,
            "solver_result_unsat": True,
            "strict_binary_forward_rup_replay": True,
        },
        "semantic-check record differs",
    )
    replay = replay_proof(run_config, outcome["parser_report"])
    second_snapshot = output_snapshot()
    require(first_snapshot == second_snapshot, "run tree changed during audit")
    second_external = [
        {
            **record,
            "size_bytes": Path(str(record["absolute_path"])).stat().st_size,
            "sha256": sha256_file(Path(str(record["absolute_path"]))),
        }
        for record in external_records
    ]
    require(
        [
            (record["role"], record["size_bytes"], record["sha256"])
            for record in external_records
        ]
        == [
            (record["role"], record["size_bytes"], record["sha256"])
            for record in second_external
        ],
        "immutable input changed during audit",
    )
    owner_writable = [
        str(record["path"])
        for record in first_snapshot["entries"]
        if record["owner_writable"] is True
    ]
    return {
        "schema": SCHEMA,
        "audit_status": "PASS",
        "claim_status": "NO_NEW_MATHEMATICAL_CLAIM",
        "audited_run_status": outcome["status"],
        "audited_run_claim_status": outcome["claim_status"],
        "scope": (
            "Exact retained hole5 S6-signature-broken finite CNF and its "
            "binary proof package only."
        ),
        "source_commit": {
            "commit": EXPECTED_SOURCE_COMMIT,
            "runtime_source_count": len(source_records),
            "runtime_source_set_sha256": source_set,
            "records": source_records,
        },
        "package_commit": {
            **committed_output,
            "contained_in_current_head": True,
            "contained_in_origin_main": True,
        },
        "package_identity": package,
        "tools": tools,
        "commands_and_resources": {
            "seed": 0,
            "physical_memory_bytes": resources["physical_memory_bytes"],
            "maximum_responsive_child_memory_mib": resources[
                "maximum_responsive_child_memory_mib"
            ],
            "file_limit_mib": resources["file_limit_mib"],
            "disk_reserve_mib": resources["disk_reserve_mib"],
            "children": children,
        },
        "schemas_and_cross_bindings": {
            "run_config_schema": run_config["schema"],
            "outcome_schema": outcome["schema"],
            "certificate_schema": certificate["schema"],
            "run_config_sha256": EXPECTED_RUN_CONFIG_SHA256,
            "outcome_sha256": EXPECTED_OUTCOME_SHA256,
            "certificate_sha256": EXPECTED_CERTIFICATE_SHA256,
            "certificate_activated_by_outcome": True,
            "artifact_coverage_complete": True,
        },
        "proof_evidence": {
            "retained_checker_seconds": retained_checker_seconds,
            "retained_checker_normalized_sha256": sha256_bytes(
                stable_checker
            ),
            "parser_report": parser_report,
            "independent_binary_parse": {
                "raw_stats_exact_match": True,
                "addition_only_stats_exact_match": True,
                "raw_addition_subsequence_exact_byte_match": True,
                "binary_grammar": (
                    "canonical base-128 varints; exact a/d records; "
                    "variables 1..6886; no duplicate/tautological records; "
                    "one final empty addition"
                ),
            },
            "readonly_replay": replay,
        },
        "immutable_input_manifest": {
            "entry_count": len(external_records),
            "tree_convention": (
                "sorted role; uint64be role length; UTF-8 role; "
                "uint64be payload length; exact payload"
            ),
            "tree_sha256": binding_tree_sha256(external_records),
            "entries": [
                {
                    key: value
                    for key, value in record.items()
                    if key != "absolute_path"
                }
                for record in external_records
            ],
        },
        "output_tree_manifest": {
            **first_snapshot,
            "tree_convention": (
                "sorted relative path; uint64be path length; UTF-8 path; "
                "uint64be payload length; exact payload"
            ),
            "tree_sha256": tree_sha256(first_snapshot["entries"]),
            "two_snapshot_stable": True,
            "unbound_entries": [],
        },
        "mutability_audit": {
            "transient_entries": [],
            "unbound_output_entries": [],
            "content_hash_coverage_complete": True,
            "two_snapshot_stable": True,
            "physical_write_protection": False,
            "durable_git_content_anchor": True,
            "durable_git_commit": EXPECTED_PACKAGE_COMMIT,
            "remaining_hash_binding_gaps": [],
            "directory_owner_writable": first_snapshot[
                "directory_owner_writable"
            ],
            "owner_writable_entries": owner_writable,
            "writeability_note": (
                "The working-tree copies remain owner-writable, but all "
                "twelve exact payloads are frozen in the package Git commit; "
                "later mutation is therefore detectable and cannot alter "
                "that durable content anchor."
            ),
        },
        "reproduction_boundary": {
            "production_solver_rerun_required": False,
            "proof_parser_replayed": True,
            "strict_checker_replayed": True,
            "output_directory_modified": False,
            "absolute_paths_in_original_config": True,
            "relocation_note": (
                "The original run config records absolute paths; this audit "
                "binds the exact current checkout rather than claiming a "
                "path-relocatable production invocation."
            ),
        },
        "auditor": {
            "path": "reviews/hole5_binary_run_package_auditor.py",
            "sha256": sha256_file(Path(__file__).resolve()),
            "implementation": "Python standard library only",
        },
    }


def write_new_atomic(path: Path, payload: bytes) -> None:
    require(RUN not in path.resolve(strict=False).parents, "output lies in run")
    require(path.parent.is_dir(), "audit output parent is missing")
    require(not path.exists() and not path.is_symlink(), "audit output exists")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.partial.",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    installed = False
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
        temporary.unlink()
        installed = True
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if not installed and temporary.exists():
            temporary.unlink()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="read-only audit of the retained hole5 binary run"
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    payload = canonical_json_bytes(audit())
    if arguments.output is None:
        sys.stdout.buffer.write(payload)
    else:
        write_new_atomic(arguments.output, payload)
        print(sha256_bytes(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
