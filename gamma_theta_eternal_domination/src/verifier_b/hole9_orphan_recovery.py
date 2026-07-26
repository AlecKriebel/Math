"""Fail-closed recovery verifier for the preserved hole9 attempt 000170.

This module is deliberately independent of ``synthesis_k3.cegar`` and of its
DIMACS reconstruction helpers.  It rebuilds the hole9 formula directly from
the mathematical encoding, validates the committed 170-cut ledger, strips
only strictly parsed DRAT deletion instructions, and checks the resulting
addition-only proof with the pinned DRAT-trim binary in forward RUP-only mode.

The recovery package is *not* a CEGAR terminal marker.  Its status remains
``verified_pending_hostile_review`` until a separate reviewer accepts it.
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
from dataclasses import asdict, dataclass
import fcntl
import gzip
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from typing import Iterable, Iterator, Mapping, Sequence


N = 12
TEMPLATE = "hole9"
ORPHAN_DIRECTORY_NAME = "000170.akmx9xl0"
SCHEMA = "gamma-theta-hole9-orphan-recovery-v1"
PACKAGE_SCHEMA = "gamma-theta-hole9-recovered-certificate-v1"

EXPECTED_RUN_MANIFEST = (
    4442,
    "73869e60bdefc547a91139ab3bfb0673ee8168acada62485089eb371a9d7c15d",
)
EXPECTED_CHECKPOINT = (
    253000,
    "9cc9cdee08fb1fcd7a8772b09cdf9ba9ced802cb0b31be35ab292244e5f286b7",
)
EXPECTED_CONFIGURATION_SHA256 = (
    "91b1257afd83f8b574229ebf9a1b8f673bd69b93ca7b72286ba90da6ee38fdd8"
)
EXPECTED_HISTORY_CHAIN_SHA256 = (
    "f174e43a531f4a1fbd857ab334d2ec4f7fa3c9b4c2cd0902eb37d887ccc51c99"
)

EXPECTED_ORPHAN_ARTIFACTS: Mapping[str, tuple[int, str]] = {
    "checker.stderr": (
        0,
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    "checker.stdout": (
        113,
        "00713579066b184feaa75783404de748da3055bc55d2871c796123a657779590",
    ),
    "cuts.json": (
        4422,
        "a3c7bd3591b71c310cfe0bd5711b8e672b75136f3598bb1505ae11cda3c2193b",
    ),
    "generator.json": (
        2536,
        "e492e06a0265f176df9a3e76f15b14a17f9873354dc9b6da4020347e1c95dbb4",
    ),
    "instance.cnf": (
        530053,
        "2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d",
    ),
    "proof-solver.stderr": (
        0,
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    "proof-solver.stdout": (
        0,
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    "proof.drat": (
        512071,
        "3cdd686fb2af82e41ff06aa13901d4706618170eb1dc4e74a870831e7fbde8ef",
    ),
    "proof.result": (
        16,
        "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162",
    ),
    "solver.result": (
        16,
        "bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162",
    ),
    "solver.stderr": (
        0,
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    "solver.stdout": (
        0,
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
}

EXPECTED_ADDITION_ONLY_PROOF = {
    "sha256": "24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab",
    "size_bytes": 65906,
    "line_count": 4705,
    "addition_count": 4705,
    "deletion_count": 11683,
    "comment_count": 0,
    "empty_addition_count": 1,
    "maximum_variable": 6886,
    "maximum_clause_size": 220,
    "original_line_count": 16388,
}

EXPECTED_RUNTIME_SOURCES: Mapping[str, str] = {
    "src/synthesis_k3/__init__.py":
        "fbc5ca4211eb97b498e0eecd692333596bba409c26629623f8d547a48a379e86",
    "src/synthesis_k3/encoding.py":
        "fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6",
    "src/synthesis_k3/coloring.py":
        "9791599aaca6b9f7ec5e6fed8cfce41a5c5bec825a350e5e493a0d1aa06d3713",
    "src/synthesis_k3/generate.py":
        "456029e08a199e3cc8d4aa6070e3209d6884901fc6c3db8486b80862614430e1",
    "src/synthesis_k3/cegar.py":
        "411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c",
    "math/synthesis_k3_cegar_design.md":
        "57d82b9dabdc9c8f66950a3f9c483f3cb58e35a11e243a8880c173b5724a09b8",
    "math/synthesis_k3_cegar_protocol.md":
        "c51db6d865557f4dcc3147772dbaa1c86d3c6c6d3544ab0090f0f89267a9de31",
}
EXPECTED_RUNTIME_SOURCE_SET_SHA256 = (
    "8c4e811bc4250c3e2b0b7edeb8afd07f7509ebda3cbae3db1b3ca82c07b35299"
)
EXPECTED_GENERATOR_SOURCE_SET_SHA256 = (
    "e48f1b430cfa5d1421bb8e7c856d70db8fc634b27d6cbd51d7d22e11f16d30bd"
)
EXPECTED_DRAT_TRIM_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
EXPECTED_DRAT_TRIM_ARCHIVE_SHA256 = (
    "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
)
EXPECTED_CADICAL_SHA256 = (
    "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
)
EXPECTED_CADICAL_ARCHIVE_SHA256 = (
    "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e"
)
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
INTEGER = re.compile(r"-?[1-9][0-9]*\Z")
ATTEMPT_DIRECTORY = re.compile(r"([0-9]{6})\.[A-Za-z0-9_]+\Z")
HEAVY_LOCK_STEM = "gamma-theta-k3-heavy-child"
HANDLED_SIGNALS = (signal.SIGTERM, signal.SIGHUP, signal.SIGINT)


class VerificationError(RuntimeError):
    """An evidence or checker condition failed closed."""


@dataclass(frozen=True)
class Formula:
    variable_count: int
    clauses: tuple[tuple[int, ...], ...]
    edge_variables: Mapping[tuple[int, int], int]

    def dimacs(self) -> bytes:
        lines = [f"p cnf {self.variable_count} {len(self.clauses)}"]
        lines.extend(
            " ".join(map(str, clause)) + " 0" for clause in self.clauses
        )
        return ("\n".join(lines) + "\n").encode("ascii")

    @property
    def literal_count(self) -> int:
        return sum(map(len, self.clauses))


@dataclass(frozen=True)
class ProofStats:
    original_line_count: int
    addition_count: int
    deletion_count: int
    comment_count: int
    empty_addition_count: int
    maximum_variable: int
    maximum_clause_size: int
    stripped_line_count: int
    stripped_size_bytes: int
    stripped_sha256: str


@dataclass(frozen=True)
class ChildRecord:
    command: tuple[str, ...]
    command_sha256: str
    executable_sha256_before: str
    executable_sha256_after: str
    exit_code: int
    termination_signal: int | None
    timed_out: bool
    memory_limit_exceeded: bool
    wall_limit_seconds: int
    memory_limit_mib: int
    file_limit_mib: int
    available_memory_before_bytes: int
    started_unix_ns: int
    finished_unix_ns: int
    wall_seconds: float
    user_cpu_seconds: float
    system_cpu_seconds: float
    maximum_resident_set_size_raw: int
    maximum_resident_set_size_raw_unit: str
    maximum_resident_set_size_mib: float
    peak_polled_resident_set_size_mib: float
    stdout_sha256: str
    stderr_sha256: str


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: object, *, pretty: bool = False) -> bytes:
    options: dict[str, object] = {
        "allow_nan": False,
        "sort_keys": True,
    }
    if pretty:
        options["indent"] = 2
    else:
        options["separators"] = (",", ":")
    return (json.dumps(value, **options) + "\n").encode("utf-8")


def _reject_constant(value: str) -> object:
    raise VerificationError(f"non-finite JSON constant {value!r}")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def strict_json_bytes(payload: bytes) -> object:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError("JSON artifact is not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as error:
        raise VerificationError("malformed JSON artifact") from error


def strict_json_file(path: Path) -> object:
    return strict_json_bytes(path.read_bytes())


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def _is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def _assert_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            raise VerificationError(f"symlinked path component: {current}")


def _regular_single_link(path: Path, role: str) -> Path:
    _assert_no_symlink_components(path)
    try:
        info = path.stat()
    except FileNotFoundError as error:
        raise VerificationError(f"missing {role}: {path}") from error
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise VerificationError(
            f"{role} is not a single-link regular file: {path}"
        )
    return path.resolve(strict=True)


def _expected_file(path: Path, role: str, expected: tuple[int, str]) -> bytes:
    resolved = _regular_single_link(path, role)
    payload = resolved.read_bytes()
    size, digest = expected
    _require(len(payload) == size, f"{role} size mismatch")
    _require(sha256_bytes(payload) == digest, f"{role} SHA-256 mismatch")
    return payload


def _source_set_sha256(records: Sequence[tuple[str, str]]) -> str:
    return sha256_bytes(
        "".join(f"{path} {digest}\n" for path, digest in records).encode(
            "ascii"
        )
    )


def _pair(first: int, second: int) -> tuple[int, int]:
    _require(first != second, "loop passed to edge-variable lookup")
    return (first, second) if first < second else (second, first)


def reconstruct_hole9_formula(
    colorings: Sequence[Sequence[int]],
) -> Formula:
    """Independently reconstruct the exact accepted hole9 DIMACS bytes."""

    variable_count = 0
    clauses: list[tuple[int, ...]] = []

    def new_variable() -> int:
        nonlocal variable_count
        variable_count += 1
        return variable_count

    def add_clause(values: Iterable[int]) -> None:
        clause = tuple(int(value) for value in values)
        _require(all(value != 0 for value in clause), "zero inside clause")
        _require(
            all(abs(value) <= variable_count for value in clause),
            "clause uses an unallocated variable",
        )
        _require(len(set(clause)) == len(clause), "duplicate clause literal")
        _require(
            not any(-value in clause for value in clause),
            "tautological clause",
        )
        clauses.append(clause)

    vertices = tuple(range(N))
    triples = tuple(combinations(vertices, 3))
    edge_variables = {
        pair: new_variable() for pair in combinations(vertices, 2)
    }
    witness_variables = {
        (first, second, witness): new_variable()
        for first, second in combinations(vertices, 2)
        for witness in vertices
        if witness not in (first, second)
    }
    family_variables = {triple: new_variable() for triple in triples}
    move_variables = {
        (triple, attacked, guard): new_variable()
        for triple in triples
        for attacked in vertices
        if attacked not in triple
        for guard in triple
    }

    def edge(first: int, second: int) -> int:
        return edge_variables[_pair(first, second)]

    # omega(H) <= 3.
    for four_set in combinations(vertices, 4):
        add_clause(
            -edge(first, second)
            for first, second in combinations(four_set, 2)
        )

    # Every pair has an external common neighbor in H.
    for first, second in combinations(vertices, 2):
        witnesses = tuple(
            vertex for vertex in vertices if vertex not in (first, second)
        )
        add_clause(
            witness_variables[(first, second, witness)]
            for witness in witnesses
        )
        for witness in witnesses:
            variable = witness_variables[(first, second, witness)]
            add_clause((-variable, edge(first, witness)))
            add_clause((-variable, edge(second, witness)))

    # Exact induced C9 on 0,...,8, no external hub, and common neighbor 9
    # fixed for rim edge 01.
    rim = tuple(range(9))
    rim_edges = {
        _pair(vertex, (vertex + 1) % len(rim)) for vertex in rim
    }
    for first, second in combinations(rim, 2):
        variable = edge(first, second)
        add_clause(
            (variable if (first, second) in rim_edges else -variable,)
        )
    for outside in range(9, N):
        add_clause(-edge(outside, rim_vertex) for rim_vertex in rim)
    add_clause((edge(0, 9),))
    add_clause((edge(1, 9),))

    # Connectedness of G: every proper cut containing vertex 0 has a
    # complement nonedge across it.
    full = (1 << N) - 1
    for mask in range(1, full):
        if not mask & 1:
            continue
        add_clause(
            -edge(first, second)
            for first in vertices
            if mask >> first & 1
            for second in vertices
            if not (mask >> second & 1)
        )

    # Selected family states dominate G.
    for triple in triples:
        family = family_variables[triple]
        for outside in vertices:
            if outside in triple:
                continue
            add_clause(
                (
                    -family,
                    -edge(outside, triple[0]),
                    -edge(outside, triple[1]),
                    -edge(outside, triple[2]),
                )
            )

    # Nonempty family and exact one-guard response witnesses.
    add_clause(family_variables.values())
    for triple in triples:
        family = family_variables[triple]
        for attacked in vertices:
            if attacked in triple:
                continue
            responses: list[int] = []
            for guard in triple:
                move = move_variables[(triple, attacked, guard)]
                successor = tuple(
                    sorted((set(triple) - {guard}) | {attacked})
                )
                responses.append(move)
                add_clause((-move, -edge(guard, attacked)))
                add_clause((-move, family_variables[successor]))
            add_clause((-family, *responses))

    # Every H-triangle belongs to the eternal family.
    for triple in triples:
        add_clause(
            (
                -edge(triple[0], triple[1]),
                -edge(triple[0], triple[2]),
                -edge(triple[1], triple[2]),
                family_variables[triple],
            )
        )

    # Globally sound same-color cuts.
    seen: set[tuple[int, ...]] = set()
    for raw in colorings:
        coloring = canonical_coloring(raw)
        _require(coloring not in seen, "duplicate coloring partition")
        seen.add(coloring)
        add_clause(
            edge(first, second)
            for first, second in combinations(vertices, 2)
            if coloring[first] == coloring[second]
        )

    return Formula(
        variable_count=variable_count,
        clauses=tuple(clauses),
        edge_variables=edge_variables,
    )


def canonical_coloring(raw: Sequence[int]) -> tuple[int, ...]:
    _require(len(raw) == N, "coloring does not have 12 entries")
    _require(
        all(type(color) is int and color in (0, 1, 2) for color in raw),
        "coloring has a noncanonical color token",
    )
    relabel: dict[int, int] = {}
    result: list[int] = []
    for color in raw:
        if color not in relabel:
            relabel[color] = len(relabel)
        result.append(relabel[color])
    canonical = tuple(result)
    _require(tuple(raw) == canonical, "coloring is not first-use canonical")
    return canonical


def _coloring_bytes(coloring: Sequence[int]) -> bytes:
    return canonical_json_bytes(list(canonical_coloring(coloring)))


def _clause_bytes(clause: Sequence[int]) -> bytes:
    _require(
        bool(clause)
        and all(type(literal) is int and literal > 0 for literal in clause),
        "coloring cut is not a positive nonempty clause",
    )
    return (" ".join(map(str, clause)) + "\n").encode("ascii")


def _cuts_payload_bytes(cuts: Sequence[Mapping[str, object]]) -> bytes:
    rows = [record["coloring"] for record in cuts]
    return canonical_json_bytes(rows)


def _cut_prefix_hashes(
    cuts: Sequence[Mapping[str, object]],
) -> tuple[str, ...]:
    result = [sha256_bytes(b"[]\n")]
    rows: list[object] = []
    for cut in cuts:
        rows.append(cut["coloring"])
        result.append(sha256_bytes(canonical_json_bytes(rows)))
    return tuple(result)


def _history_initial(
    configuration_sha256: str, run_manifest_sha256: str
) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            {
                "domain": "gamma-theta-k3-cegar-history-v1",
                "configuration_sha256": configuration_sha256,
                "run_manifest_sha256": run_manifest_sha256,
            }
        )
    )


def _history_step(
    before: str,
    reference: Mapping[str, object],
    cut: Mapping[str, object],
) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            {
                "domain": "gamma-theta-k3-cegar-history-v1",
                "before_sha256": before,
                "attempt_reference": dict(reference),
                "cut_record": dict(cut),
                "status": "running",
                "terminal": None,
            }
        )
    )


def _logical_checkpoint_digest(
    *,
    run_manifest_path: str,
    run_manifest_sha256: str,
    attempt_count: int,
    cut_count: int,
    cuts_payload_sha256: str,
    history_chain_sha256: str,
) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            {
                "domain": "gamma-theta-k3-cegar-checkpoint-state-v1",
                "schema": "gamma-theta-k3-cegar-checkpoint-v2",
                "schema_version": 2,
                "configuration_sha256": EXPECTED_CONFIGURATION_SHA256,
                "run_manifest_path": run_manifest_path,
                "run_manifest_sha256": run_manifest_sha256,
                "status": "running",
                "attempt_count": attempt_count,
                "cut_count": cut_count,
                "cuts_payload_sha256": cuts_payload_sha256,
                "history_chain_sha256": history_chain_sha256,
                "terminal": None,
            }
        )
    )


def _artifact_binding(path: Path) -> dict[str, object]:
    resolved = _regular_single_link(path, "bound artifact")
    return {
        "path": str(resolved),
        "sha256": sha256_file(resolved),
        "size_bytes": resolved.stat().st_size,
    }


def _validate_binding(
    record: object,
    *,
    run_directory: Path,
    role: str,
) -> Path:
    _require(
        isinstance(record, dict)
        and set(record) == {"path", "sha256", "size_bytes"},
        f"{role} binding has wrong schema",
    )
    raw_path = record["path"]
    _require(type(raw_path) is str, f"{role} path is not text")
    path = Path(raw_path)
    _require(path.is_absolute(), f"{role} path is not absolute")
    resolved = _regular_single_link(path, role)
    _require(
        _is_within(resolved, run_directory),
        f"{role} escapes the run directory",
    )
    _require(
        type(record["size_bytes"]) is int
        and record["size_bytes"] == resolved.stat().st_size,
        f"{role} size mismatch",
    )
    _require(
        type(record["sha256"]) is str
        and HEX64.fullmatch(record["sha256"]) is not None
        and record["sha256"] == sha256_file(resolved),
        f"{role} hash mismatch",
    )
    return resolved


def _validate_attempt_present_hashes(
    manifest: Mapping[str, object],
    *,
    run_directory: Path,
    cut_prefix_hashes: Sequence[str],
) -> int:
    checked = 0
    artifacts = manifest.get("artifacts")
    _require(isinstance(artifacts, dict), "attempt artifacts are not an object")
    artifact_paths: dict[str, Path] = {}
    for role, record in artifacts.items():
        _require(type(role) is str, "artifact role is not text")
        artifact_paths[role] = _validate_binding(
            record, run_directory=run_directory, role=f"attempt {role}"
        )
        checked += 1

    compressed = manifest.get("compressed_artifacts")
    _require(
        isinstance(compressed, dict),
        "compressed artifact ledger is not an object",
    )
    for role, record in compressed.items():
        _require(
            type(role) is str
            and isinstance(record, dict)
            and set(record)
            == {
                "format",
                "raw_path",
                "raw_sha256",
                "raw_size_bytes",
                "gzip_path",
                "gzip_sha256",
                "gzip_size_bytes",
            },
            "compressed artifact binding has wrong schema",
        )
        _require(record["format"] == "gzip", "unknown compression format")
        gzip_path = Path(str(record["gzip_path"]))
        resolved = _regular_single_link(gzip_path, f"compressed {role}")
        _require(
            _is_within(resolved, run_directory),
            "compressed artifact escapes run directory",
        )
        payload = resolved.read_bytes()
        _require(
            len(payload) == record["gzip_size_bytes"]
            and sha256_bytes(payload) == record["gzip_sha256"],
            "compressed artifact hash/size mismatch",
        )
        try:
            raw = gzip.decompress(payload)
        except (gzip.BadGzipFile, EOFError) as error:
            raise VerificationError("compressed artifact is malformed") from error
        _require(
            len(raw) == record["raw_size_bytes"]
            and sha256_bytes(raw) == record["raw_sha256"],
            "compressed artifact raw binding mismatch",
        )
        _require(
            not Path(str(record["raw_path"])).exists(),
            "compacted raw artifact unexpectedly exists",
        )
        checked += 2

    reconstructed = manifest.get("reconstructible_artifacts")
    _require(
        isinstance(reconstructed, dict)
        and set(reconstructed) == {"cnf", "cuts_input"},
        "reconstructible artifact ledger has wrong schema",
    )
    cut_count = manifest.get("cut_count_before")
    _require(
        type(cut_count) is int and 0 <= cut_count < len(cut_prefix_hashes),
        "attempt cut count is malformed",
    )
    expected_prefix = cut_prefix_hashes[cut_count]
    for role, record in reconstructed.items():
        _require(isinstance(record, dict), "reconstruction record is malformed")
        _require(
            record.get("cut_count") == cut_count
            and record.get("cut_prefix_sha256") == expected_prefix,
            "reconstruction cut-prefix binding mismatch",
        )
        raw_path = Path(str(record.get("raw_path")))
        _require(
            raw_path.is_absolute()
            and _is_within(raw_path, run_directory)
            and not raw_path.exists(),
            "reconstructed raw role is not an absent in-run path",
        )
        raw_hash = record.get("raw_sha256")
        raw_size = record.get("raw_size_bytes")
        _require(
            type(raw_hash) is str
            and HEX64.fullmatch(raw_hash) is not None
            and type(raw_size) is int
            and raw_size >= 0,
            "reconstruction raw binding is malformed",
        )
    generator_path = artifact_paths.get("generator_manifest")
    _require(generator_path is not None, "attempt lacks generator manifest")
    generator = strict_json_file(generator_path)
    _require(isinstance(generator, dict), "generator manifest is not an object")
    cnf_recipe = reconstructed["cnf"]
    cuts_recipe = reconstructed["cuts_input"]
    _require(
        generator.get("cnf_sha256") == cnf_recipe.get("raw_sha256")
        and generator.get("colorings_sha256")
        == cuts_recipe.get("raw_sha256")
        and generator.get("coloring_cut_count") == cut_count,
        "generator/reconstruction hashes disagree",
    )
    checked += 4
    return checked


def _validate_run_manifest(
    payload: object,
    *,
    campaign_root: Path,
    run_directory: Path,
) -> Mapping[str, object]:
    _require(
        isinstance(payload, dict)
        and set(payload)
        == {
            "schema",
            "schema_version",
            "configuration",
            "configuration_sha256",
            "working_directory",
            "required_environment",
            "normalized_resume_invocation",
        },
        "run manifest has wrong schema",
    )
    _require(
        payload["schema"] == "gamma-theta-k3-cegar-run-v2"
        and payload["schema_version"] == 2,
        "run manifest schema/version mismatch",
    )
    configuration = payload["configuration"]
    _require(isinstance(configuration, dict), "configuration is not an object")
    digest = sha256_bytes(canonical_json_bytes(configuration))
    _require(
        digest == payload["configuration_sha256"]
        == EXPECTED_CONFIGURATION_SHA256,
        "configuration hash mismatch",
    )
    _require(
        configuration.get("template") == TEMPLATE
        and Path(str(configuration.get("run_directory"))).resolve()
        == run_directory,
        "run manifest targets the wrong run/template",
    )
    runtime_records = configuration.get("runtime_source_manifest")
    expected_records = [[key, value] for key, value in EXPECTED_RUNTIME_SOURCES.items()]
    _require(
        runtime_records == expected_records,
        "runtime source manifest differs from frozen production sources",
    )
    for relative, expected_hash in EXPECTED_RUNTIME_SOURCES.items():
        source = _regular_single_link(
            campaign_root / relative, f"runtime source {relative}"
        )
        _require(
            sha256_file(source) == expected_hash,
            f"runtime source hash mismatch: {relative}",
        )
    records = tuple((str(a), str(b)) for a, b in runtime_records)
    _require(
        _source_set_sha256(records)
        == configuration.get("runtime_source_set_sha256")
        == EXPECTED_RUNTIME_SOURCE_SET_SHA256,
        "runtime source-set hash mismatch",
    )
    for role, expected_binary, expected_archive in (
        ("cadical", EXPECTED_CADICAL_SHA256, EXPECTED_CADICAL_ARCHIVE_SHA256),
        (
            "drat_trim",
            EXPECTED_DRAT_TRIM_SHA256,
            EXPECTED_DRAT_TRIM_ARCHIVE_SHA256,
        ),
    ):
        binding = configuration.get(role)
        _require(isinstance(binding, dict), f"{role} binding is malformed")
        binary = _regular_single_link(Path(str(binding.get("path"))), role)
        archive = _regular_single_link(
            Path(str(binding.get("source_archive_path"))),
            f"{role} source archive",
        )
        _require(
            binding.get("sha256") == expected_binary
            and sha256_file(binary) == expected_binary
            and binding.get("source_archive_sha256") == expected_archive
            and sha256_file(archive) == expected_archive,
            f"{role} tool/archive hash mismatch",
        )
    return payload


def validate_source_evidence(
    campaign_root: Path,
) -> dict[str, object]:
    """Validate every decisive source artifact without writing the run tree."""

    campaign_root = campaign_root.resolve(strict=True)
    run_directory = (
        campaign_root / "results/synthesis_k3_runs/hole9"
    ).resolve(strict=True)
    attempt_directory = (
        run_directory / "attempts" / ORPHAN_DIRECTORY_NAME
    ).resolve(strict=True)
    _require(
        attempt_directory.parent.parent == run_directory,
        "orphan attempt path is not exact",
    )

    run_manifest_path = run_directory / "run_manifest.json"
    checkpoint_path = run_directory / "checkpoint.json"
    run_manifest_bytes = _expected_file(
        run_manifest_path, "run manifest", EXPECTED_RUN_MANIFEST
    )
    checkpoint_bytes = _expected_file(
        checkpoint_path, "checkpoint", EXPECTED_CHECKPOINT
    )
    run_manifest = _validate_run_manifest(
        strict_json_bytes(run_manifest_bytes),
        campaign_root=campaign_root,
        run_directory=run_directory,
    )
    checkpoint = strict_json_bytes(checkpoint_bytes)
    _require(
        isinstance(checkpoint, dict)
        and set(checkpoint)
        == {
            "schema",
            "schema_version",
            "configuration_sha256",
            "run_manifest_path",
            "run_manifest_sha256",
            "status",
            "attempts",
            "cuts",
            "cuts_payload_sha256",
            "history_chain_sha256",
            "terminal",
        },
        "checkpoint has wrong schema",
    )
    _require(
        checkpoint["schema"] == "gamma-theta-k3-cegar-checkpoint-v2"
        and checkpoint["schema_version"] == 2
        and checkpoint["configuration_sha256"]
        == EXPECTED_CONFIGURATION_SHA256
        and checkpoint["run_manifest_path"] == str(run_manifest_path.resolve())
        and checkpoint["run_manifest_sha256"] == EXPECTED_RUN_MANIFEST[1]
        and checkpoint["status"] == "running"
        and checkpoint["terminal"] is None,
        "checkpoint provenance/status mismatch",
    )
    attempts = checkpoint["attempts"]
    cuts = checkpoint["cuts"]
    _require(
        isinstance(attempts, list)
        and isinstance(cuts, list)
        and len(attempts) == len(cuts) == 170,
        "checkpoint is not the exact 170-cut running prefix",
    )

    # Build base variables independently before validating clause IDs.
    base = reconstruct_hole9_formula(())
    _require(
        base.variable_count == 6886
        and len(base.clauses) == 20030
        and base.literal_count == 114619,
        "independent base reconstruction has wrong dimensions",
    )

    seen: set[tuple[int, ...]] = set()
    manifests: list[Mapping[str, object]] = []
    present_hash_checks = 0
    for index, (reference, record) in enumerate(zip(attempts, cuts)):
        _require(
            isinstance(reference, dict)
            and set(reference)
            == {
                "index",
                "manifest_path",
                "manifest_sha256",
                "outcome",
                "checkpoint_before_sha256",
                "history_chain_before_sha256",
            },
            "attempt reference has wrong schema",
        )
        _require(
            reference["index"] == index
            and reference["outcome"] == "coloring_cut_committed",
            "attempt reference index/outcome mismatch",
        )
        manifest_path = Path(str(reference["manifest_path"]))
        _require(
            manifest_path.is_absolute()
            and _is_within(manifest_path, run_directory)
            and manifest_path.name == "attempt.json",
            "attempt manifest path escapes or has wrong basename",
        )
        match = ATTEMPT_DIRECTORY.fullmatch(manifest_path.parent.name)
        _require(
            match is not None and int(match.group(1)) == index,
            "attempt directory index mismatch",
        )
        manifest_path = _regular_single_link(
            manifest_path, f"attempt {index} manifest"
        )
        _require(
            sha256_file(manifest_path) == reference["manifest_sha256"],
            f"attempt {index} manifest hash mismatch",
        )
        manifest = strict_json_file(manifest_path)
        _require(isinstance(manifest, dict), "attempt manifest is not an object")
        _require(
            manifest.get("schema") == "gamma-theta-k3-cegar-attempt-v2"
            and manifest.get("schema_version") == 2
            and manifest.get("attempt_index") == index
            and manifest.get("outcome") == "coloring_cut_committed"
            and manifest.get("configuration_sha256")
            == EXPECTED_CONFIGURATION_SHA256
            and manifest.get("run_manifest_sha256")
            == EXPECTED_RUN_MANIFEST[1]
            and manifest.get("checkpoint_before_sha256")
            == reference["checkpoint_before_sha256"]
            and manifest.get("history_chain_before_sha256")
            == reference["history_chain_before_sha256"]
            and manifest.get("cut_count_before") == index,
            f"attempt {index} provenance mismatch",
        )
        manifests.append(manifest)

        _require(
            isinstance(record, dict)
            and set(record)
            == {
                "index",
                "coloring",
                "coloring_sha256",
                "clause",
                "clause_sha256",
                "source_attempt_index",
                "source_attempt_manifest_path",
                "source_attempt_manifest_sha256",
            }
            and record["index"] == index
            and record["source_attempt_index"] == index
            and record["source_attempt_manifest_path"]
            == reference["manifest_path"]
            and record["source_attempt_manifest_sha256"]
            == reference["manifest_sha256"],
            f"cut {index} source binding mismatch",
        )
        raw_coloring = record["coloring"]
        _require(isinstance(raw_coloring, list), "cut coloring is not a list")
        coloring = canonical_coloring(raw_coloring)
        _require(coloring not in seen, "checkpoint repeats a coloring")
        seen.add(coloring)
        clause = tuple(
            base.edge_variables[(first, second)]
            for first, second in combinations(range(N), 2)
            if coloring[first] == coloring[second]
        )
        _require(
            record["coloring_sha256"]
            == sha256_bytes(_coloring_bytes(coloring))
            and isinstance(record["clause"], list)
            and tuple(record["clause"]) == clause
            and record["clause_sha256"]
            == sha256_bytes(_clause_bytes(clause)),
            f"cut {index} coloring/clause hash mismatch",
        )
        expected_committed = {
            key: record[key]
            for key in (
                "index",
                "coloring",
                "coloring_sha256",
                "clause",
                "clause_sha256",
            )
        }
        _require(
            manifest.get("committed_cut") == expected_committed,
            f"cut {index} differs from source attempt",
        )

    prefix_hashes = _cut_prefix_hashes(cuts)
    _require(
        checkpoint["cuts_payload_sha256"]
        == prefix_hashes[-1]
        == EXPECTED_ORPHAN_ARTIFACTS["cuts.json"][1],
        "checkpoint cut payload hash mismatch",
    )
    for manifest in manifests:
        present_hash_checks += _validate_attempt_present_hashes(
            manifest,
            run_directory=run_directory,
            cut_prefix_hashes=prefix_hashes,
        )

    # Independently replay predecessor and history-chain hashes.
    run_manifest_path_text = str(run_manifest_path.resolve())
    history = _history_initial(
        EXPECTED_CONFIGURATION_SHA256, EXPECTED_RUN_MANIFEST[1]
    )
    checkpoint_before = _logical_checkpoint_digest(
        run_manifest_path=run_manifest_path_text,
        run_manifest_sha256=EXPECTED_RUN_MANIFEST[1],
        attempt_count=0,
        cut_count=0,
        cuts_payload_sha256=prefix_hashes[0],
        history_chain_sha256=history,
    )
    for index, (reference, cut, manifest) in enumerate(
        zip(attempts, cuts, manifests)
    ):
        _require(
            reference["history_chain_before_sha256"] == history
            and manifest["history_chain_before_sha256"] == history
            and reference["checkpoint_before_sha256"] == checkpoint_before
            and manifest["checkpoint_before_sha256"] == checkpoint_before,
            f"checkpoint chronology fails at attempt {index}",
        )
        history = _history_step(history, reference, cut)
        checkpoint_before = _logical_checkpoint_digest(
            run_manifest_path=run_manifest_path_text,
            run_manifest_sha256=EXPECTED_RUN_MANIFEST[1],
            attempt_count=index + 1,
            cut_count=index + 1,
            cuts_payload_sha256=prefix_hashes[index + 1],
            history_chain_sha256=history,
        )
    _require(
        history
        == checkpoint["history_chain_sha256"]
        == EXPECTED_HISTORY_CHAIN_SHA256,
        "checkpoint history-chain head mismatch",
    )

    source_bytes: dict[str, bytes] = {}
    for name, expected in EXPECTED_ORPHAN_ARTIFACTS.items():
        source_bytes[name] = _expected_file(
            attempt_directory / name, f"orphan {name}", expected
        )
    _require(
        source_bytes["cuts.json"] == _cuts_payload_bytes(cuts),
        "orphan cuts bytes differ from checkpoint cut payload",
    )
    _require(
        source_bytes["solver.stdout"] == b""
        and source_bytes["solver.stderr"] == b""
        and source_bytes["proof-solver.stdout"] == b""
        and source_bytes["proof-solver.stderr"] == b"",
        "solver logs are not the preserved empty transcripts",
    )
    parse_exact_unsat_result(source_bytes["solver.result"], "initial result")
    parse_exact_unsat_result(source_bytes["proof.result"], "proof result")

    colorings = tuple(tuple(record["coloring"]) for record in cuts)
    formula = reconstruct_hole9_formula(colorings)
    reconstructed = formula.dimacs()
    _require(
        formula.variable_count == 6886
        and len(formula.clauses) == 20200
        and formula.literal_count == 117841,
        "complete formula dimensions mismatch",
    )
    _require(
        reconstructed == source_bytes["instance.cnf"],
        "orphan CNF is not byte-identical to independent reconstruction",
    )

    generator = strict_json_bytes(source_bytes["generator.json"])
    _require(isinstance(generator, dict), "generator manifest is not an object")
    _require(
        generator.get("schema") == "gamma-theta-k3-cnf-v2"
        and generator.get("schema_version") == 2
        and generator.get("template") == TEMPLATE
        and generator.get("order") == N
        and generator.get("variable_count") == formula.variable_count
        and generator.get("clause_count") == len(formula.clauses)
        and generator.get("literal_count") == formula.literal_count
        and generator.get("coloring_cut_count") == len(cuts)
        and generator.get("colorings_sha256")
        == EXPECTED_ORPHAN_ARTIFACTS["cuts.json"][1]
        and generator.get("cnf_sha256")
        == EXPECTED_ORPHAN_ARTIFACTS["instance.cnf"][1],
        "generator manifest dimensions/hashes mismatch",
    )
    stream = hashlib.sha256()
    for coloring in colorings:
        stream.update((" ".join(map(str, coloring)) + "\n").encode("ascii"))
    _require(
        generator.get("coloring_cut_stream_sha256") == stream.hexdigest(),
        "generator coloring stream hash mismatch",
    )
    generator_sources = generator.get("generator_source_manifest")
    _require(
        isinstance(generator_sources, list),
        "generator source manifest is not a list",
    )
    generator_records: list[tuple[str, str]] = []
    for row in generator_sources:
        _require(
            isinstance(row, list)
            and len(row) == 2
            and type(row[0]) is str
            and type(row[1]) is str,
            "generator source row is malformed",
        )
        relative, recorded_hash = row
        _require(
            EXPECTED_RUNTIME_SOURCES.get(relative) == recorded_hash
            and sha256_file(campaign_root / relative) == recorded_hash,
            f"generator source hash mismatch: {relative}",
        )
        generator_records.append((relative, recorded_hash))
    _require(
        _source_set_sha256(generator_records)
        == generator.get("generator_source_set_sha256")
        == EXPECTED_GENERATOR_SOURCE_SET_SHA256,
        "generator source-set hash mismatch",
    )

    stripped, proof_stats = strip_deletion_lines(source_bytes["proof.drat"])
    validate_expected_stripped_proof(stripped, proof_stats)

    # The failed checker transcript is provenance only and must not masquerade
    # as a verified transcript.
    _require(
        b"s VERIFIED" not in source_bytes["checker.stdout"]
        and source_bytes["checker.stderr"] == b"",
        "preserved failed checker transcript has unexpected success text",
    )

    return {
        "campaign_root": campaign_root,
        "run_directory": run_directory,
        "attempt_directory": attempt_directory,
        "run_manifest_path": run_manifest_path,
        "checkpoint_path": checkpoint_path,
        "run_manifest": run_manifest,
        "checkpoint": checkpoint,
        "source_bytes": source_bytes,
        "formula": formula,
        "reconstructed_cnf": reconstructed,
        "addition_only_proof": stripped,
        "proof_stats": proof_stats,
        "present_artifact_hash_checks": present_hash_checks,
    }


def parse_exact_unsat_result(payload: bytes, role: str) -> None:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise VerificationError(f"{role} is not ASCII") from error
    lines = text.splitlines()
    _require(
        text.endswith("\n")
        and "\r" not in text
        and lines == ["s UNSATISFIABLE"],
        f"{role} is not the exact singleton UNSAT result",
    )


def _parse_proof_clause(line: bytes, *, deletion: bool, number: int) -> tuple[int, ...]:
    prefix = b"d " if deletion else b""
    _require(
        line.startswith(prefix) and line.endswith(b"\n") and b"\r" not in line,
        f"proof line {number} has noncanonical framing",
    )
    body = line[len(prefix):-1]
    try:
        text = body.decode("ascii")
    except UnicodeDecodeError as error:
        raise VerificationError(f"proof line {number} is not ASCII") from error
    tokens = text.split(" ")
    _require(
        bool(tokens) and tokens[-1] == "0" and "" not in tokens,
        f"proof line {number} is not a canonical zero-terminated clause",
    )
    _require(
        all(INTEGER.fullmatch(token) is not None for token in tokens[:-1]),
        f"proof line {number} has an invalid literal token",
    )
    literals = tuple(int(token) for token in tokens[:-1])
    _require(
        all(abs(literal) <= 2_147_483_647 for literal in literals),
        f"proof line {number} exceeds the DRAT integer range",
    )
    _require(
        len(literals) == len(set(literals)),
        f"proof line {number} repeats a literal",
    )
    _require(
        not any(-literal in literals for literal in literals),
        f"proof line {number} is tautological",
    )
    if deletion:
        _require(bool(literals), f"proof line {number} deletes the empty clause")
    canonical = prefix + (
        (" ".join(map(str, literals)) + " 0\n").encode("ascii")
        if literals
        else b"0\n"
    )
    _require(line == canonical, f"proof line {number} is not canonical ASCII")
    return literals


def strip_deletion_lines(payload: bytes) -> tuple[bytes, ProofStats]:
    """Strictly parse ASCII DRAT and remove only valid deletion lines."""

    _require(payload != b"", "DRAT proof is empty")
    _require(payload.endswith(b"\n"), "DRAT proof lacks final LF")
    _require(b"\r" not in payload and b"\x00" not in payload, "DRAT is not LF ASCII")
    try:
        payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise VerificationError("DRAT proof is not ASCII") from error

    additions = 0
    deletions = 0
    comments = 0
    empty_additions = 0
    maximum_variable = 0
    maximum_clause_size = 0
    stripped: list[bytes] = []
    last_instruction_was_empty = False
    lines = payload.splitlines(keepends=True)
    for number, line in enumerate(lines, 1):
        _require(line not in (b"\n", b""), f"blank proof line {number}")
        if line.startswith(b"c "):
            _require(
                all(byte == 9 or 32 <= byte <= 126 for byte in line[:-1]),
                f"proof comment {number} has a control byte",
            )
            comments += 1
            stripped.append(line)
            continue
        deletion = line.startswith(b"d ")
        literals = _parse_proof_clause(
            line, deletion=deletion, number=number
        )
        maximum_clause_size = max(maximum_clause_size, len(literals))
        for literal in literals:
            maximum_variable = max(maximum_variable, abs(literal))
        if deletion:
            deletions += 1
            continue
        additions += 1
        stripped.append(line)
        last_instruction_was_empty = not literals
        if not literals:
            empty_additions += 1
            _require(
                number == len(lines),
                "empty-clause addition is not the final proof line",
            )
    _require(
        empty_additions == 1 and last_instruction_was_empty,
        "proof does not end in exactly one empty-clause addition",
    )
    stripped_payload = b"".join(stripped)
    stats = ProofStats(
        original_line_count=len(lines),
        addition_count=additions,
        deletion_count=deletions,
        comment_count=comments,
        empty_addition_count=empty_additions,
        maximum_variable=maximum_variable,
        maximum_clause_size=maximum_clause_size,
        stripped_line_count=len(stripped),
        stripped_size_bytes=len(stripped_payload),
        stripped_sha256=sha256_bytes(stripped_payload),
    )
    return stripped_payload, stats


def validate_expected_stripped_proof(
    payload: bytes, stats: ProofStats
) -> None:
    expected = EXPECTED_ADDITION_ONLY_PROOF
    _require(
        stats.original_line_count == expected["original_line_count"]
        and stats.addition_count == expected["addition_count"]
        and stats.deletion_count == expected["deletion_count"]
        and stats.comment_count == expected["comment_count"]
        and stats.empty_addition_count == expected["empty_addition_count"]
        and stats.maximum_variable == expected["maximum_variable"]
        and stats.maximum_clause_size == expected["maximum_clause_size"]
        and stats.stripped_line_count == expected["line_count"]
        and stats.stripped_size_bytes == expected["size_bytes"]
        and stats.stripped_sha256 == expected["sha256"]
        and len(payload) == expected["size_bytes"]
        and sha256_bytes(payload) == expected["sha256"],
        "addition-only proof hash or exact instruction counts differ",
    )
    # A second parse proves that the emitted proof contains no deletion line.
    reparsed, second = strip_deletion_lines(payload)
    _require(
        reparsed == payload
        and second.deletion_count == 0
        and second.addition_count == expected["addition_count"],
        "emitted proof is not addition-only under the strict parser",
    )


def validate_checker_transcript(stdout: bytes, stderr: bytes) -> None:
    try:
        out = stdout.decode("ascii")
        err = stderr.decode("ascii")
    except UnicodeDecodeError as error:
        raise VerificationError("checker transcript is not ASCII") from error
    combined = out + "\n" + err
    lowered = combined.lower()
    _require(err == "", "checker wrote to stderr")
    _require(out.endswith("\n"), "checker stdout lacks final LF")
    normalized_lines = [line.strip() for line in out.splitlines()]
    _require(
        normalized_lines.count("s VERIFIED") == 1,
        "checker did not emit exactly one exact `s VERIFIED` line",
    )
    for forbidden in (
        "warning",
        "error",
        "failed",
        "timeout",
        "not verified",
        "invalid",
    ):
        _require(forbidden not in lowered, f"checker transcript contains {forbidden!r}")
    status_lines = [
        line for line in normalized_lines if line.startswith("s ")
    ]
    _require(status_lines == ["s VERIFIED"], "checker emitted another status line")


def tree_digest(directory: Path) -> dict[str, object]:
    """Hash a regular-file tree with unambiguous path and length framing."""

    root = directory.resolve(strict=True)
    digest = hashlib.sha256()
    count = 0
    total = 0
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            continue
        _require(
            stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
            f"tree contains nonregular or multiply-linked entry: {path}",
        )
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
        count += 1
        total += len(payload)
    return {
        "algorithm": (
            "SHA256(sorted files; u64be path length; UTF-8 relative path; "
            "u64be byte length; bytes)"
        ),
        "sha256": digest.hexdigest(),
        "file_count": count,
        "total_file_bytes": total,
    }


class ExistingExclusiveLock:
    """Acquire an existing lock file without creating or changing it."""

    def __init__(self, path: Path, role: str) -> None:
        self.path = path
        self.role = role
        self.descriptor: int | None = None

    def __enter__(self) -> "ExistingExclusiveLock":
        _regular_single_link(self.path, self.role)
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(self.path, flags)
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise VerificationError(f"{self.role} is already held") from error
        self.descriptor = descriptor
        return self

    def __exit__(self, *_: object) -> None:
        _require(self.descriptor is not None, "lock exit without acquisition")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


class CampaignHeavyLock:
    """Use the exact cross-template heavy-child lock namespace."""

    def __init__(self, campaign_root: Path) -> None:
        root_hash = sha256_bytes(
            str(campaign_root.resolve()).encode("utf-8")
        )[:20]
        self.path = (
            Path(tempfile.gettempdir()).resolve()
            / f"{HEAVY_LOCK_STEM}-{root_hash}.lock"
        )
        self.descriptor: int | None = None

    def __enter__(self) -> "CampaignHeavyLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        _assert_no_symlink_components(self.path.parent)
        if self.path.exists():
            _regular_single_link(self.path, "campaign heavy-child lock")
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(self.path, flags, 0o600)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            os.close(descriptor)
            raise VerificationError("heavy-child lock is not a regular file")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise VerificationError(
                "another campaign solver/checker is active"
            ) from error
        self.descriptor = descriptor
        return self

    def __exit__(self, *_: object) -> None:
        _require(
            self.descriptor is not None,
            "heavy-child lock exit without acquisition",
        )
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


class _DarwinVMStatistics64(ctypes.Structure):
    _fields_ = (
        ("free_count", ctypes.c_uint32),
        ("active_count", ctypes.c_uint32),
        ("inactive_count", ctypes.c_uint32),
        ("wire_count", ctypes.c_uint32),
        ("zero_fill_count", ctypes.c_uint64),
        ("reactivations", ctypes.c_uint64),
        ("pageins", ctypes.c_uint64),
        ("pageouts", ctypes.c_uint64),
        ("faults", ctypes.c_uint64),
        ("cow_faults", ctypes.c_uint64),
        ("lookups", ctypes.c_uint64),
        ("hits", ctypes.c_uint64),
        ("purges", ctypes.c_uint64),
        ("purgeable_count", ctypes.c_uint32),
        ("speculative_count", ctypes.c_uint32),
        ("decompressions", ctypes.c_uint64),
        ("compressions", ctypes.c_uint64),
        ("swapins", ctypes.c_uint64),
        ("swapouts", ctypes.c_uint64),
        ("compressor_page_count", ctypes.c_uint32),
        ("throttled_count", ctypes.c_uint32),
        ("external_page_count", ctypes.c_uint32),
        ("internal_page_count", ctypes.c_uint32),
        ("total_uncompressed_pages_in_compressor", ctypes.c_uint64),
    )


class _DarwinProcTaskInfo(ctypes.Structure):
    _fields_ = (
        ("pti_virtual_size", ctypes.c_uint64),
        ("pti_resident_size", ctypes.c_uint64),
        ("pti_total_user", ctypes.c_uint64),
        ("pti_total_system", ctypes.c_uint64),
        ("pti_threads_user", ctypes.c_uint64),
        ("pti_threads_system", ctypes.c_uint64),
        ("pti_policy", ctypes.c_int32),
        ("pti_faults", ctypes.c_int32),
        ("pti_pageins", ctypes.c_int32),
        ("pti_cow_faults", ctypes.c_int32),
        ("pti_messages_sent", ctypes.c_int32),
        ("pti_messages_received", ctypes.c_int32),
        ("pti_syscalls_mach", ctypes.c_int32),
        ("pti_syscalls_unix", ctypes.c_int32),
        ("pti_csw", ctypes.c_int32),
        ("pti_threadnum", ctypes.c_int32),
        ("pti_numrunning", ctypes.c_int32),
        ("pti_priority", ctypes.c_int32),
    )


def available_memory_bytes() -> int:
    if sys.platform == "darwin":
        library = ctypes.CDLL("/usr/lib/libSystem.B.dylib")
        host = library.mach_host_self()
        page_size = ctypes.c_uint32()
        library.host_page_size.argtypes = (
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint32),
        )
        _require(
            library.host_page_size(host, ctypes.byref(page_size)) == 0,
            "host_page_size failed",
        )
        statistics = _DarwinVMStatistics64()
        count = ctypes.c_uint32(
            ctypes.sizeof(statistics) // ctypes.sizeof(ctypes.c_int32)
        )
        library.host_statistics64.argtypes = (
            ctypes.c_uint32,
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint32),
        )
        _require(
            library.host_statistics64(
                host, 4, ctypes.byref(statistics), ctypes.byref(count)
            )
            == 0,
            "host_statistics64 failed",
        )
        pages = (
            int(statistics.free_count)
            + int(statistics.inactive_count)
            + int(statistics.speculative_count)
            + int(statistics.purgeable_count)
        )
        return pages * int(page_size.value)
    if sys.platform.startswith("linux"):
        for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
            if line.startswith("MemAvailable:"):
                fields = line.split()
                _require(
                    len(fields) == 3 and fields[2] == "kB",
                    "malformed MemAvailable",
                )
                return int(fields[1]) * 1024
    raise VerificationError("available-memory probe is unsupported")


_DARWIN_PROC_PIDINFO: object | None = None


def _rss_bytes(pid: int) -> int | None:
    if sys.platform == "darwin":
        global _DARWIN_PROC_PIDINFO
        if _DARWIN_PROC_PIDINFO is None:
            library = ctypes.CDLL("/usr/lib/libproc.dylib")
            function = library.proc_pidinfo
            function.argtypes = (
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_uint64,
                ctypes.c_void_p,
                ctypes.c_int,
            )
            function.restype = ctypes.c_int
            _DARWIN_PROC_PIDINFO = function
        function = _DARWIN_PROC_PIDINFO
        information = _DarwinProcTaskInfo()
        returned = function(  # type: ignore[operator]
            pid, 4, 0, ctypes.byref(information), ctypes.sizeof(information)
        )
        if returned != ctypes.sizeof(information):
            return None
        return int(information.pti_resident_size)
    if sys.platform.startswith("linux"):
        try:
            lines = Path(f"/proc/{pid}/status").read_text(
                encoding="ascii"
            ).splitlines()
        except FileNotFoundError:
            return None
        for line in lines:
            if line.startswith("VmRSS:"):
                fields = line.split()
                if len(fields) == 3 and fields[2] == "kB":
                    return int(fields[1]) * 1024
    return None


def _child_setup(memory_bytes: int, cpu_seconds: int, file_bytes: int) -> None:
    os.setsid()
    if hasattr(signal, "pthread_sigmask"):
        signal.pthread_sigmask(signal.SIG_UNBLOCK, HANDLED_SIGNALS)
    if sys.platform != "darwin":
        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds + 1))
    resource.setrlimit(resource.RLIMIT_FSIZE, (file_bytes, file_bytes))
    os.umask(0o077)


def _kill_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    deadline = time.perf_counter() + 0.5
    while time.perf_counter() < deadline:
        try:
            waited, _, _ = os.wait4(pid, os.WNOHANG)
        except ChildProcessError:
            return
        if waited == pid:
            return
        time.sleep(0.01)
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        os.wait4(pid, 0)
    except ChildProcessError:
        pass


def _command_sha256(command: Sequence[str]) -> str:
    return sha256_bytes(canonical_json_bytes(list(command)))


def run_bounded_child(
    *,
    command: Sequence[str],
    cwd: Path,
    stdout_path: Path,
    stderr_path: Path,
    readonly_paths: Sequence[Path],
    wall_limit_seconds: int,
    memory_limit_mib: int,
    file_limit_mib: int,
    available_before: int,
) -> ChildRecord:
    """Run one process-group child with hard wall/CPU/RSS/file limits."""

    _require(
        type(wall_limit_seconds) is int and wall_limit_seconds > 0,
        "wall limit is not a positive exact integer",
    )
    _require(
        type(memory_limit_mib) is int and memory_limit_mib > 0,
        "memory limit is not a positive exact integer",
    )
    _require(
        type(file_limit_mib) is int and file_limit_mib > 0,
        "file limit is not a positive exact integer",
    )
    argv = tuple(str(value) for value in command)
    _require(bool(argv) and all(argv), "child command has an empty argument")
    executable = Path(argv[0])
    _require(executable.is_absolute(), "child executable is not absolute")
    executable = _regular_single_link(executable, "child executable")
    for index, path in enumerate(readonly_paths):
        resolved = _regular_single_link(path, f"checker input {index}")
        _require(
            resolved not in (stdout_path.resolve(), stderr_path.resolve()),
            "checker input/output roles collide",
        )
    _require(
        stdout_path != stderr_path
        and not stdout_path.exists()
        and not stderr_path.exists(),
        "checker log role exists or collides",
    )

    executable_hash_before = sha256_file(executable)
    out_handle = stdout_path.open("xb")
    err_handle = stderr_path.open("xb")
    process: subprocess.Popen[bytes] | None = None
    usage = None
    wait_status: int | None = None
    timed_out = False
    memory_exceeded = False
    peak_rss = 0
    started_ns = time.time_ns()
    started = time.perf_counter()
    previous_handlers: dict[int, object] = {}
    previous_mask: set[signal.Signals] | None = None
    if hasattr(signal, "pthread_sigmask"):
        previous_mask = signal.pthread_sigmask(
            signal.SIG_BLOCK, HANDLED_SIGNALS
        )

    def interrupted(signum: int, _: object) -> None:
        if process is not None and process.returncode is None:
            _kill_group(process.pid)
        raise KeyboardInterrupt(f"checker interrupted by signal {signum}")

    try:
        for handled in HANDLED_SIGNALS:
            previous_handlers[handled] = signal.getsignal(handled)
            signal.signal(handled, interrupted)
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env={},
            stdin=subprocess.DEVNULL,
            stdout=out_handle,
            stderr=err_handle,
            close_fds=True,
            preexec_fn=lambda: _child_setup(
                memory_limit_mib << 20,
                wall_limit_seconds + 1,
                file_limit_mib << 20,
            ),
        )
        if previous_mask is not None:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        deadline = started + wall_limit_seconds
        while True:
            waited, candidate_status, candidate_usage = os.wait4(
                process.pid, os.WNOHANG
            )
            if waited == process.pid:
                wait_status = candidate_status
                usage = candidate_usage
                break
            resident = _rss_bytes(process.pid)
            if resident is not None:
                peak_rss = max(peak_rss, resident)
                if resident > (memory_limit_mib << 20):
                    memory_exceeded = True
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    _, wait_status, usage = os.wait4(process.pid, 0)
                    break
            if time.perf_counter() >= deadline:
                timed_out = True
                _kill_group(process.pid)
                try:
                    _, wait_status, usage = os.wait4(process.pid, os.WNOHANG)
                except ChildProcessError:
                    # _kill_group already reaped it; portable resource values
                    # are unavailable only on this rejected path.
                    wait_status = 0
                    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
                break
            time.sleep(0.02)
        _require(
            wait_status is not None and usage is not None,
            "checker child lacks wait4 accounting",
        )
        process.returncode = os.waitstatus_to_exitcode(wait_status)
        out_handle.flush()
        err_handle.flush()
        os.fsync(out_handle.fileno())
        os.fsync(err_handle.fileno())
    finally:
        if process is not None and process.returncode is None:
            _kill_group(process.pid)
        out_handle.close()
        err_handle.close()
        for handled, previous in previous_handlers.items():
            signal.signal(handled, previous)
        if previous_mask is not None:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)

    finished = time.perf_counter()
    finished_ns = time.time_ns()
    _require(
        process is not None
        and process.returncode is not None
        and usage is not None,
        "checker child completion accounting is missing",
    )
    executable_hash_after = sha256_file(executable)
    _require(
        executable_hash_before == executable_hash_after,
        "checker binary changed during execution",
    )
    raw_rss = int(usage.ru_maxrss)
    if sys.platform == "darwin":
        rss_mib = raw_rss / (1 << 20)
        unit = "bytes"
    else:
        rss_mib = raw_rss / 1024.0
        unit = "KiB"
    return ChildRecord(
        command=argv,
        command_sha256=_command_sha256(argv),
        executable_sha256_before=executable_hash_before,
        executable_sha256_after=executable_hash_after,
        exit_code=process.returncode,
        termination_signal=(
            -process.returncode if process.returncode < 0 else None
        ),
        timed_out=timed_out,
        memory_limit_exceeded=memory_exceeded,
        wall_limit_seconds=wall_limit_seconds,
        memory_limit_mib=memory_limit_mib,
        file_limit_mib=file_limit_mib,
        available_memory_before_bytes=available_before,
        started_unix_ns=started_ns,
        finished_unix_ns=finished_ns,
        wall_seconds=finished - started,
        user_cpu_seconds=float(usage.ru_utime),
        system_cpu_seconds=float(usage.ru_stime),
        maximum_resident_set_size_raw=raw_rss,
        maximum_resident_set_size_raw_unit=unit,
        maximum_resident_set_size_mib=rss_mib,
        peak_polled_resident_set_size_mib=peak_rss / (1 << 20),
        stdout_sha256=sha256_file(stdout_path),
        stderr_sha256=sha256_file(stderr_path),
    )


def checker_command(
    checker: Path,
    cnf: Path,
    proof: Path,
    *,
    wall_seconds: int,
    plain: bool,
) -> tuple[str, ...]:
    flags = ["-I", "-f"]
    if plain:
        flags.append("-p")
    flags.extend(("-W", "-U", "-t", str(wall_seconds)))
    return (
        str(checker.resolve()),
        str(cnf.resolve()),
        str(proof.resolve()),
        *flags,
    )


def _run_and_validate_checker(
    *,
    checker: Path,
    cnf: Path,
    proof: Path,
    stdout_path: Path,
    stderr_path: Path,
    cwd: Path,
    wall_seconds: int,
    memory_mib: int,
    file_mib: int,
    available_before: int,
    plain: bool,
) -> ChildRecord:
    cnf_hash = sha256_file(cnf)
    proof_hash = sha256_file(proof)
    command = checker_command(
        checker, cnf, proof, wall_seconds=wall_seconds, plain=plain
    )
    record = run_bounded_child(
        command=command,
        cwd=cwd,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        readonly_paths=(cnf, proof),
        wall_limit_seconds=wall_seconds,
        memory_limit_mib=memory_mib,
        file_limit_mib=file_mib,
        available_before=available_before,
    )
    _require(
        record.exit_code == 0
        and not record.timed_out
        and not record.memory_limit_exceeded,
        "pinned checker did not complete successfully",
    )
    validate_checker_transcript(
        stdout_path.read_bytes(), stderr_path.read_bytes()
    )
    _require(
        sha256_file(cnf) == cnf_hash and sha256_file(proof) == proof_hash,
        "checker input changed during verification",
    )
    return record


def _write_new_file(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _package_bindings(root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_dir():
            continue
        _regular_single_link(path, "package artifact")
        relative = path.relative_to(root).as_posix()
        _require(relative != "certificate.json", "manifest cannot bind itself")
        records.append(
            {
                "path": relative,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return records


def _seal_tree(root: Path) -> None:
    for path in sorted(root.rglob("*"), key=lambda item: len(item.parts), reverse=True):
        if path.is_file():
            os.chmod(path, 0o444)
        elif path.is_dir():
            os.chmod(path, 0o555)
    os.chmod(root, 0o555)


def _safe_cleanup_staging(staging: Path, parent: Path) -> None:
    try:
        resolved_parent = parent.resolve(strict=True)
        resolved_staging = staging.resolve(strict=False)
    except FileNotFoundError:
        return
    if (
        resolved_staging.parent == resolved_parent
        and resolved_staging.name.startswith(".hole9-recovery.partial.")
    ):
        if resolved_staging.exists():
            for path in resolved_staging.rglob("*"):
                with contextlib.suppress(OSError):
                    os.chmod(path, 0o700 if path.is_dir() else 0o600)
            with contextlib.suppress(OSError):
                os.chmod(resolved_staging, 0o700)
            shutil.rmtree(resolved_staging)


def recover(
    *,
    campaign_root: Path,
    output_directory: Path,
    drat_trim: Path,
    soundness_note: Path,
    wall_seconds: int = 60,
    memory_mib: int = 2048,
    file_mib: int = 16,
) -> dict[str, object]:
    """Create one immutable recovery package, refusing every overwrite."""

    campaign_root = campaign_root.resolve(strict=True)
    run_directory = (
        campaign_root / "results/synthesis_k3_runs/hole9"
    ).resolve(strict=True)
    output = output_directory.resolve(strict=False)
    _assert_no_symlink_components(output.parent)
    _require(output.is_absolute(), "output directory is not absolute")
    _require(
        not output.exists()
        and not _is_within(output, run_directory)
        and not _is_within(run_directory, output),
        "output exists, overlaps, or contains the run directory",
    )
    note = _regular_single_link(soundness_note, "soundness note")
    checker = _regular_single_link(drat_trim, "pinned DRAT-trim")
    _require(
        sha256_file(checker) == EXPECTED_DRAT_TRIM_SHA256,
        "DRAT-trim is not the pinned binary",
    )
    archive = _regular_single_link(
        campaign_root / "tools/drat_trim_2023_05_22.tar.gz",
        "DRAT-trim source archive",
    )
    _require(
        sha256_file(archive) == EXPECTED_DRAT_TRIM_ARCHIVE_SHA256,
        "DRAT-trim source archive hash mismatch",
    )
    _require(
        0 < memory_mib <= 3072,
        "checker memory ceiling exceeds the laptop-safe recovery bound",
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=".hole9-recovery.partial.", dir=output.parent
        )
    ).resolve()
    installed = False
    try:
        with ExistingExclusiveLock(run_directory / "run.lock", "hole9 run lock"):
            source_tree_before = tree_digest(run_directory)
            evidence = validate_source_evidence(campaign_root)

            source_root = staging / "source"
            orphan_root = source_root / "orphan-attempt-000170"
            _write_new_file(
                source_root / "run_manifest.json",
                Path(evidence["run_manifest_path"]).read_bytes(),
            )
            _write_new_file(
                source_root / "checkpoint.json",
                Path(evidence["checkpoint_path"]).read_bytes(),
            )
            source_bytes = evidence["source_bytes"]
            _require(isinstance(source_bytes, dict), "internal source map error")
            for name in sorted(source_bytes):
                payload = source_bytes[name]
                _require(isinstance(payload, bytes), "internal source bytes error")
                _write_new_file(orphan_root / name, payload)

            _write_new_file(staging / "SOUNDNESS.md", note.read_bytes())
            _write_new_file(
                staging / "proof/addition-only.rup.drat",
                evidence["addition_only_proof"],
            )
            verifier_source = Path(__file__).resolve()
            _write_new_file(
                staging / "repro/hole9_orphan_recovery.py",
                verifier_source.read_bytes(),
            )
            test_source = (
                campaign_root / "tests/test_hole9_orphan_recovery.py"
            )
            if test_source.exists():
                _write_new_file(
                    staging / "repro/test_hole9_orphan_recovery.py",
                    _regular_single_link(test_source, "recovery tests").read_bytes(),
                )

            cnf = orphan_root / "instance.cnf"
            original_proof = orphan_root / "proof.drat"
            stripped_proof = staging / "proof/addition-only.rup.drat"
            checker_root = staging / "checker"
            checker_root.mkdir(parents=True)
            with CampaignHeavyLock(campaign_root):
                available = available_memory_bytes()
                _require(
                    available >= ((memory_mib + 512) << 20),
                    "current-memory gate failed before checker",
                )
                stripped_record = _run_and_validate_checker(
                    checker=checker,
                    cnf=cnf,
                    proof=stripped_proof,
                    stdout_path=checker_root / "addition-only-rup.stdout",
                    stderr_path=checker_root / "addition-only-rup.stderr",
                    cwd=staging,
                    wall_seconds=wall_seconds,
                    memory_mib=memory_mib,
                    file_mib=file_mib,
                    available_before=available,
                    plain=False,
                )
                # Redundant diagnostic: the original deletion-bearing proof,
                # interpreted in plain mode, must verify under the same RUP-only
                # restriction.  This is not the primary certificate premise.
                original_record = _run_and_validate_checker(
                    checker=checker,
                    cnf=cnf,
                    proof=original_proof,
                    stdout_path=checker_root / "original-plain-rup.stdout",
                    stderr_path=checker_root / "original-plain-rup.stderr",
                    cwd=staging,
                    wall_seconds=wall_seconds,
                    memory_mib=memory_mib,
                    file_mib=file_mib,
                    available_before=available,
                    plain=True,
                )

            # Recheck every source hash and the whole run tree after both
            # external checker calls.
            validate_source_evidence(campaign_root)
            source_tree_after = tree_digest(run_directory)
            _require(
                source_tree_before == source_tree_after,
                "hole9 run tree changed during read-only recovery",
            )

        proof_stats = evidence["proof_stats"]
        _require(isinstance(proof_stats, ProofStats), "internal proof stats error")
        package_artifacts = _package_bindings(staging)
        manifest = {
            "schema": PACKAGE_SCHEMA,
            "schema_version": 1,
            "status": "verified_pending_hostile_review",
            "claim_boundary": (
                "This package is not a CEGAR terminal marker and does not by "
                "itself certify the complete (12,3) slice. It may be promoted "
                "only after independent hostile review."
            ),
            "template": TEMPLATE,
            "order": 12,
            "committed_cut_count": 170,
            "source": {
                "campaign_root": str(campaign_root),
                "run_manifest_sha256": EXPECTED_RUN_MANIFEST[1],
                "checkpoint_sha256": EXPECTED_CHECKPOINT[1],
                "checkpoint_status": "running",
                "checkpoint_terminal": None,
                "orphan_directory_name": ORPHAN_DIRECTORY_NAME,
                "orphan_was_checkpoint_referenced": False,
                "original_cnf_sha256":
                    EXPECTED_ORPHAN_ARTIFACTS["instance.cnf"][1],
                "original_proof_sha256":
                    EXPECTED_ORPHAN_ARTIFACTS["proof.drat"][1],
                "initial_result_sha256":
                    EXPECTED_ORPHAN_ARTIFACTS["solver.result"][1],
                "proof_result_sha256":
                    EXPECTED_ORPHAN_ARTIFACTS["proof.result"][1],
                "run_tree_before": source_tree_before,
                "run_tree_after": source_tree_after,
            },
            "independent_reconstruction": {
                "implementation": (
                    "standalone hole9 formula builder; no import from "
                    "synthesis_k3.cegar, synthesis_k3.encoding, or "
                    "synthesis_k3.generate"
                ),
                "variable_count": 6886,
                "base_clause_count": 20030,
                "base_literal_count": 114619,
                "cut_clause_count": 170,
                "total_clause_count": 20200,
                "literal_count": 117841,
                "cnf_byte_equality": True,
                "checkpoint_history_chain_replayed": True,
                "present_attempt_artifact_hash_checks":
                    evidence["present_artifact_hash_checks"],
            },
            "proof_transformation": {
                **asdict(proof_stats),
                "original_sha256":
                    EXPECTED_ORPHAN_ARTIFACTS["proof.drat"][1],
                "original_size_bytes":
                    EXPECTED_ORPHAN_ARTIFACTS["proof.drat"][0],
                "method": (
                    "strict ASCII line parser; preserve every addition/comment "
                    "byte; remove only canonical `d <nonempty clause> 0` lines"
                ),
                "addition_only_reparse_deletion_count": 0,
            },
            "primary_checker": {
                "semantics": "forward addition-only RUP",
                "required_flags": ["-I", "-f", "-W", "-U", "-t", str(wall_seconds)],
                "exact_verified_line_count": 1,
                "warning_count": 0,
                "record": asdict(stripped_record),
            },
            "redundant_original_checker": {
                "semantics": "forward plain-mode RUP; deletions ignored",
                "required_flags": [
                    "-I", "-f", "-p", "-W", "-U", "-t", str(wall_seconds)
                ],
                "exact_verified_line_count": 1,
                "warning_count": 0,
                "record": asdict(original_record),
            },
            "tool": {
                "drat_trim_binary_sha256": EXPECTED_DRAT_TRIM_SHA256,
                "drat_trim_source_archive_sha256":
                    EXPECTED_DRAT_TRIM_ARCHIVE_SHA256,
                "commit": "2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
            },
            "validation": {
                "all_expected_source_hashes": True,
                "both_unsat_results_parsed": True,
                "cut_ledger_and_chronology": True,
                "formula_exactly_reconstructed": True,
                "original_proof_strictly_parsed": True,
                "addition_only_proof_deterministic": True,
                "addition_only_proof_rup_verified": True,
                "original_plain_mode_rup_crosscheck": True,
                "checker_warning_free": True,
                "run_tree_byte_unchanged": True,
                "package_pending_hostile_review": True,
            },
            "package_artifacts": package_artifacts,
        }
        _write_new_file(
            staging / "certificate.json",
            canonical_json_bytes(manifest, pretty=True),
        )
        _fsync_directory(staging)
        _seal_tree(staging)
        _require(not output.exists(), "output appeared before package install")
        os.rename(staging, output)
        installed = True
        _fsync_directory(output.parent)
        return manifest
    finally:
        if not installed:
            _safe_cleanup_staging(staging, output.parent)


def _load_package_manifest(package: Path) -> Mapping[str, object]:
    manifest_path = _regular_single_link(
        package / "certificate.json", "certificate manifest"
    )
    manifest = strict_json_file(manifest_path)
    _require(
        isinstance(manifest, dict)
        and manifest.get("schema") == PACKAGE_SCHEMA
        and manifest.get("schema_version") == 1
        and manifest.get("status") == "verified_pending_hostile_review",
        "certificate manifest schema/status mismatch",
    )
    return manifest


def audit_package(
    *,
    package_directory: Path,
    drat_trim: Path,
    wall_seconds: int = 60,
    memory_mib: int = 2048,
    file_mib: int = 16,
) -> dict[str, object]:
    """Read-only package audit plus fresh pinned proof replay."""

    package = package_directory.resolve(strict=True)
    before = tree_digest(package)
    manifest = _load_package_manifest(package)
    records = manifest.get("package_artifacts")
    _require(isinstance(records, list), "package artifact ledger is not a list")
    expected_paths: set[str] = {"certificate.json"}
    for record in records:
        _require(
            isinstance(record, dict)
            and set(record) == {"path", "size_bytes", "sha256"}
            and type(record["path"]) is str,
            "package artifact record is malformed",
        )
        relative = record["path"]
        _require(relative not in expected_paths, "duplicate package path")
        path = _regular_single_link(package / relative, f"package {relative}")
        _require(
            _is_within(path, package)
            and path.stat().st_size == record["size_bytes"]
            and sha256_file(path) == record["sha256"],
            f"package artifact binding mismatch: {relative}",
        )
        expected_paths.add(relative)
    actual_paths = {
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file()
    }
    _require(actual_paths == expected_paths, "package has omitted/extra files")

    checkpoint = strict_json_file(package / "source/checkpoint.json")
    _require(isinstance(checkpoint, dict), "packaged checkpoint is malformed")
    _require(
        sha256_file(package / "source/checkpoint.json") == EXPECTED_CHECKPOINT[1]
        and checkpoint.get("status") == "running"
        and checkpoint.get("terminal") is None,
        "packaged checkpoint binding/status mismatch",
    )
    cuts = checkpoint.get("cuts")
    _require(isinstance(cuts, list) and len(cuts) == 170, "packaged cut count")
    cut_bytes = _cuts_payload_bytes(cuts)
    _require(
        cut_bytes
        == (package / "source/orphan-attempt-000170/cuts.json").read_bytes()
        and sha256_bytes(cut_bytes)
        == EXPECTED_ORPHAN_ARTIFACTS["cuts.json"][1],
        "packaged cuts do not match checkpoint",
    )
    formula = reconstruct_hole9_formula(
        tuple(tuple(record["coloring"]) for record in cuts)
    )
    cnf = package / "source/orphan-attempt-000170/instance.cnf"
    _require(
        formula.dimacs() == cnf.read_bytes()
        and sha256_file(cnf)
        == EXPECTED_ORPHAN_ARTIFACTS["instance.cnf"][1],
        "packaged CNF fails independent reconstruction",
    )
    parse_exact_unsat_result(
        (package / "source/orphan-attempt-000170/solver.result").read_bytes(),
        "packaged initial result",
    )
    parse_exact_unsat_result(
        (package / "source/orphan-attempt-000170/proof.result").read_bytes(),
        "packaged proof result",
    )
    original = package / "source/orphan-attempt-000170/proof.drat"
    stripped = package / "proof/addition-only.rup.drat"
    regenerated, stats = strip_deletion_lines(original.read_bytes())
    _require(
        regenerated == stripped.read_bytes(),
        "packaged addition-only proof is not the deterministic transform",
    )
    validate_expected_stripped_proof(regenerated, stats)

    checker = _regular_single_link(drat_trim, "pinned DRAT-trim")
    _require(
        sha256_file(checker) == EXPECTED_DRAT_TRIM_SHA256,
        "audit checker is not the pinned binary",
    )
    campaign_root = Path(
        str(manifest.get("source", {}).get("campaign_root", package))
    )
    # The package is portable; its own absolute location names the lock
    # namespace when the original campaign root is unavailable.
    lock_root = package if not campaign_root.exists() else campaign_root
    with tempfile.TemporaryDirectory(prefix="hole9-package-audit.") as raw:
        temporary = Path(raw)
        with CampaignHeavyLock(lock_root):
            available = available_memory_bytes()
            _require(
                available >= ((memory_mib + 512) << 20),
                "current-memory gate failed before package audit",
            )
            primary = _run_and_validate_checker(
                checker=checker,
                cnf=cnf,
                proof=stripped,
                stdout_path=temporary / "primary.stdout",
                stderr_path=temporary / "primary.stderr",
                cwd=temporary,
                wall_seconds=wall_seconds,
                memory_mib=memory_mib,
                file_mib=file_mib,
                available_before=available,
                plain=False,
            )
    after = tree_digest(package)
    _require(before == after, "package changed during read-only audit")
    return {
        "schema": SCHEMA,
        "status": "audit_passed_pending_hostile_review",
        "package": str(package),
        "package_tree": after,
        "cnf_sha256": sha256_file(cnf),
        "addition_only_proof_sha256": sha256_file(stripped),
        "checker_exit_code": primary.exit_code,
        "checker_flags": ["-I", "-f", "-W", "-U", "-t", str(wall_seconds)],
        "exact_verified_line_count": 1,
        "warning_count": 0,
    }


def _campaign_root_from_module() -> Path:
    candidate = Path(__file__).resolve().parents[2]
    if (candidate / "src/synthesis_k3/encoding.py").is_file():
        return candidate
    raise VerificationError(
        "recover mode needs --campaign-root when run outside the source tree"
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="operation", required=True)
    recover_parser = subparsers.add_parser("recover")
    recover_parser.add_argument("--campaign-root", type=Path)
    recover_parser.add_argument("--output", type=Path, required=True)
    recover_parser.add_argument("--drat-trim", type=Path)
    recover_parser.add_argument("--soundness-note", type=Path)
    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--package", type=Path, required=True)
    audit_parser.add_argument("--drat-trim", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.operation == "recover":
            root = (
                arguments.campaign_root.resolve()
                if arguments.campaign_root is not None
                else _campaign_root_from_module()
            )
            checker = (
                arguments.drat_trim
                if arguments.drat_trim is not None
                else root / "tools/drat_trim_2023_05_22/drat-trim"
            )
            note = (
                arguments.soundness_note
                if arguments.soundness_note is not None
                else root / "math/lemmas/hole9_orphan_drat_recovery.md"
            )
            result = recover(
                campaign_root=root,
                output_directory=arguments.output,
                drat_trim=checker,
                soundness_note=note,
            )
        else:
            result = audit_package(
                package_directory=arguments.package,
                drat_trim=arguments.drat_trim,
            )
    except (OSError, VerificationError, ValueError) as error:
        print(
            json.dumps(
                {
                    "schema": SCHEMA,
                    "status": "REJECT",
                    "error": f"{type(error).__name__}: {error}",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
