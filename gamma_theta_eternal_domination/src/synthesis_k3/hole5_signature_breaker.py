"""Audited S6 signature breaker for the retained complete ``hole5`` CNF.

This module derives a new package from the frozen full coloring-bank package.
It does not regenerate, replace, or mutate that package.  The derived DIMACS
file retains every source clause in byte-identical order (apart from the
updated header count) and appends exactly 315 auxiliary-free clauses sorting
vertices 6..11 by their six-bit H-adjacency signatures to vertices 0..5.

There is deliberately no production solve subcommand yet.  A proof-producing
runner remains disabled until hostile review accepts the semantic symmetry
argument, package audit, and binary-proof/checker protocol.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import tempfile
from collections import Counter
from itertools import product
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .cegar import ParsedCNF, parse_dimacs_bytes
from .encoding import K3Encoding, N, build_k3_encoding
from .template_color_bank import (
    BANK_NAME as SOURCE_BANK_NAME,
    CNF_NAME,
    MANIFEST_NAME,
    _assert_no_symlink_components,
    _assert_regular_single_link,
    _fsync_directory,
    _validate_new_output_directory,
    _write_new_file,
    audit_package as audit_source_package,
    campaign_root,
    canonical_json_bytes,
    git_source_binding,
    sha256_bytes,
    sha256_file,
    source_set_sha256,
    strict_json_bytes,
)


SCHEMA_VERSION = 1
TEMPLATE = "hole5"
CORE_VERTICES = tuple(range(6))
FREE_VERTICES = tuple(range(6, 12))
ADJACENT_FREE_PAIRS = tuple(zip(FREE_VERTICES, FREE_VERTICES[1:]))
COMPARATOR_CLAUSES_PER_PAIR = 63
COMPARATOR_LITERAL_COUNT_PER_PAIR = 642
EXPECTED_BREAKER_CLAUSE_COUNT = 315
EXPECTED_BREAKER_LITERAL_COUNT = 3_210
EXPECTED_SOURCE_VARIABLE_COUNT = 6_886
EXPECTED_SOURCE_CLAUSE_COUNT = 23_653
EXPECTED_SOURCE_LITERAL_COUNT = 188_959
EXPECTED_DERIVED_VARIABLE_COUNT = 6_886
EXPECTED_DERIVED_CLAUSE_COUNT = 23_968
EXPECTED_DERIVED_LITERAL_COUNT = 192_169
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402"
)
EXPECTED_SOURCE_CNF_SHA256 = (
    "76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7"
)
EXPECTED_SOURCE_BANK_SHA256 = (
    "b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00"
)
EXPECTED_DERIVED_CNF_SHA256 = (
    "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104"
)
EXPECTED_BREAKER_SHA256 = (
    "62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a"
)
BREAKER_NAME = "signature_breaker.json"
THEOREM_RELATIVE_PATH = "math/lemmas/hole5_signature_symmetry.md"
RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/synthesis_k3/__init__.py",
    "src/synthesis_k3/encoding.py",
    "src/synthesis_k3/cegar.py",
    "src/synthesis_k3/template_color_bank.py",
    "src/synthesis_k3/hole5_signature_breaker.py",
    THEOREM_RELATIVE_PATH,
)


def _require_gate(validation_gate: object) -> None:
    if validation_gate is not True:
        raise PermissionError("explicit validation gate is required")


def _require_bool(value: object, role: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{role} must be boolean")
    return value


def _require_exact_keys(
    value: object,
    expected: set[str],
    role: str,
) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ValueError(f"{role} has an unexpected object shape")
    return value


def _artifact_record(path: Path) -> dict[str, object]:
    _assert_regular_single_link(path, path.name)
    return {
        "path": path.name,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _input_artifact_record(path: Path) -> dict[str, object]:
    _assert_regular_single_link(path, f"source artifact {path.name}")
    return {
        "path": path.name,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def runtime_source_manifest() -> tuple[tuple[str, str], ...]:
    root = campaign_root()
    result: list[tuple[str, str]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        path = root / relative
        _assert_regular_single_link(path, f"runtime source {relative}")
        result.append((relative, sha256_file(path)))
    return tuple(result)


def signature_variables(
    encoding: K3Encoding,
    vertex: int,
) -> tuple[int, ...]:
    if type(vertex) is not int or vertex not in FREE_VERTICES:
        raise ValueError("signature vertex must be an exact integer in 6..11")
    return tuple(encoding.edge(core, vertex) for core in CORE_VERTICES)


def lexicographic_leq_clauses(
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    """Encode one six-bit ``left <=lex right`` relation without auxiliaries."""

    if (
        len(left) != 6
        or len(right) != 6
        or any(type(variable) is not int or variable <= 0 for variable in left)
        or any(type(variable) is not int or variable <= 0 for variable in right)
        or len(set(left) | set(right)) != 12
    ):
        raise ValueError("comparator needs twelve distinct positive variables")
    clauses: list[tuple[int, ...]] = []
    for first_difference in range(6):
        for prefix in product((False, True), repeat=first_difference):
            clause: list[int] = []
            for index, bit in enumerate(prefix):
                if bit:
                    clause.extend((-left[index], -right[index]))
                else:
                    clause.extend((left[index], right[index]))
            clause.extend((-left[first_difference], right[first_difference]))
            clauses.append(tuple(clause))
    result = tuple(clauses)
    if (
        len(result) != COMPARATOR_CLAUSES_PER_PAIR
        or sum(map(len, result)) != COMPARATOR_LITERAL_COUNT_PER_PAIR
        or len(set(result)) != len(result)
    ):
        raise AssertionError("comparator construction count invariant failed")
    return result


def signature_breaker_clauses(
    encoding: K3Encoding | None = None,
) -> tuple[tuple[int, ...], ...]:
    selected = build_k3_encoding(TEMPLATE) if encoding is None else encoding
    if selected.template != TEMPLATE:
        raise ValueError("signature breaker requires the hole5 encoding")
    clauses = tuple(
        clause
        for left_vertex, right_vertex in ADJACENT_FREE_PAIRS
        for clause in lexicographic_leq_clauses(
            signature_variables(selected, left_vertex),
            signature_variables(selected, right_vertex),
        )
    )
    if (
        len(clauses) != EXPECTED_BREAKER_CLAUSE_COUNT
        or sum(map(len, clauses)) != EXPECTED_BREAKER_LITERAL_COUNT
        or len(set(clauses)) != len(clauses)
    ):
        raise AssertionError("signature-breaker count invariant failed")
    return clauses


def _clause_truth(
    clause: Sequence[int],
    assignment: Mapping[int, bool],
) -> bool:
    return any(
        assignment[abs(literal)] == (literal > 0) for literal in clause
    )


def exhaustive_comparator_audit(
    encoding: K3Encoding | None = None,
) -> dict[str, object]:
    """Check all 4,096 signature pairs for each of five comparators."""

    selected = build_k3_encoding(TEMPLATE) if encoding is None else encoding
    checked = 0
    for left_vertex, right_vertex in ADJACENT_FREE_PAIRS:
        left_variables = signature_variables(selected, left_vertex)
        right_variables = signature_variables(selected, right_vertex)
        clauses = lexicographic_leq_clauses(left_variables, right_variables)
        for left_bits in product((False, True), repeat=6):
            for right_bits in product((False, True), repeat=6):
                assignment = {
                    **dict(zip(left_variables, left_bits)),
                    **dict(zip(right_variables, right_bits)),
                }
                cnf_truth = all(
                    _clause_truth(clause, assignment) for clause in clauses
                )
                expected = left_bits <= right_bits
                if cnf_truth != expected:
                    raise AssertionError(
                        "comparator truth table differs from lexicographic order"
                    )
                checked += 1
    if checked != len(ADJACENT_FREE_PAIRS) * 4_096:
        raise AssertionError("comparator audit assignment count is wrong")
    return {
        "adjacent_comparators_checked": len(ADJACENT_FREE_PAIRS),
        "assignments_per_comparator": 4_096,
        "total_assignments_checked": checked,
        "truth_relation": "six-bit-lexicographic-nondecreasing",
    }


def _validate_vertex_permutation(
    permutation: Sequence[int],
) -> tuple[int, ...]:
    if (
        len(permutation) != N
        or any(type(vertex) is not int for vertex in permutation)
        or set(permutation) != set(range(N))
    ):
        raise ValueError("vertex permutation is malformed")
    normalized = tuple(permutation)
    if normalized[:6] != CORE_VERTICES:
        raise ValueError("signature symmetry must fix vertices 0..5")
    return normalized


def variable_relabeling(
    encoding: K3Encoding,
    permutation: Sequence[int],
) -> dict[int, int]:
    """Return the induced variable permutation for every encoding variable."""

    pi = _validate_vertex_permutation(permutation)
    result: dict[int, int] = {}

    def pair(first: int, second: int) -> tuple[int, int]:
        mapped = (pi[first], pi[second])
        return tuple(sorted(mapped))  # type: ignore[return-value]

    for (first, second), variable in encoding.edge_variables.items():
        result[variable] = encoding.edge_variables[pair(first, second)]
    for (first, second, witness), variable in encoding.witness_variables.items():
        mapped_first, mapped_second = pair(first, second)
        result[variable] = encoding.witness_variables[
            (mapped_first, mapped_second, pi[witness])
        ]
    for triple, variable in encoding.family_variables.items():
        mapped_triple = tuple(sorted(pi[vertex] for vertex in triple))
        result[variable] = encoding.family_variables[mapped_triple]  # type: ignore[index]
    for (triple, attacked, guard), variable in encoding.move_variables.items():
        mapped_triple = tuple(sorted(pi[vertex] for vertex in triple))
        result[variable] = encoding.move_variables[
            (mapped_triple, pi[attacked], pi[guard])  # type: ignore[arg-type]
        ]
    expected = set(range(1, encoding.cnf.variable_count + 1))
    if set(result) != expected or set(result.values()) != expected:
        raise AssertionError("induced variable map is not a bijection")
    return result


def relabel_clause(
    clause: Sequence[int],
    variable_map: Mapping[int, int],
) -> tuple[int, ...]:
    mapped = tuple(
        variable_map[abs(literal)] if literal > 0 else -variable_map[-literal]
        for literal in clause
    )
    if len(set(mapped)) != len(mapped) or any(-literal in mapped for literal in mapped):
        raise AssertionError("variable relabeling corrupted a clause")
    return mapped


def _normalized_clause(clause: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(clause))


def _clause_multiset_digest(clauses: Iterable[Sequence[int]]) -> str:
    normalized = Counter(_normalized_clause(clause) for clause in clauses)
    digest = hashlib.sha256()
    for clause, multiplicity in sorted(normalized.items()):
        line = " ".join(map(str, clause)).encode("ascii") + b" 0\n"
        for _ in range(multiplicity):
            digest.update(line)
    return digest.hexdigest()


def covariance_audit(
    source_cnf: ParsedCNF,
    encoding: K3Encoding | None = None,
) -> dict[str, object]:
    """Check the five adjacent transpositions generating the outside S6."""

    selected = build_k3_encoding(TEMPLATE) if encoding is None else encoding
    if source_cnf.variable_count != selected.cnf.variable_count:
        raise ValueError("source CNF variable count differs from the encoding")
    original = Counter(
        _normalized_clause(clause) for clause in source_cnf.clauses
    )
    generators: list[list[int]] = []
    for left, right in ADJACENT_FREE_PAIRS:
        permutation = list(range(N))
        permutation[left], permutation[right] = (
            permutation[right],
            permutation[left],
        )
        variable_map = variable_relabeling(selected, permutation)
        transformed = Counter(
            _normalized_clause(relabel_clause(clause, variable_map))
            for clause in source_cnf.clauses
        )
        if transformed != original:
            missing = original - transformed
            extra = transformed - original
            raise ValueError(
                f"source CNF is not invariant under swap {left},{right}: "
                f"{sum(missing.values())} missing, {sum(extra.values())} extra"
            )
        generators.append([left, right])
    return {
        "group": "S6-on-vertices-6-through-11-fixing-0-through-5",
        "generator_transpositions_checked": generators,
        "generator_count": len(generators),
        "source_clause_multiset_sha256": _clause_multiset_digest(
            source_cnf.clauses
        ),
        "source_clause_count": len(source_cnf.clauses),
    }


def breaker_clause_stream_bytes(
    clauses: Sequence[Sequence[int]] | None = None,
) -> bytes:
    selected = signature_breaker_clauses() if clauses is None else tuple(
        tuple(clause) for clause in clauses
    )
    if (
        len(selected) != EXPECTED_BREAKER_CLAUSE_COUNT
        or sum(map(len, selected)) != EXPECTED_BREAKER_LITERAL_COUNT
    ):
        raise ValueError("breaker clause stream has wrong counts")
    return b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in selected
    )


def breaker_payload_bytes(
    encoding: K3Encoding | None = None,
) -> bytes:
    selected = build_k3_encoding(TEMPLATE) if encoding is None else encoding
    clauses = signature_breaker_clauses(selected)
    payload = {
        "schema": "gamma-theta-hole5-signature-breaker-clauses-v1",
        "schema_version": SCHEMA_VERSION,
        "template": TEMPLATE,
        "order": N,
        "core_vertices": list(CORE_VERTICES),
        "free_vertices": list(FREE_VERTICES),
        "signature_bit_order": list(CORE_VERTICES),
        "signature_edge_variables": {
            str(vertex): list(signature_variables(selected, vertex))
            for vertex in FREE_VERTICES
        },
        "ordered_adjacent_pairs": [
            list(pair) for pair in ADJACENT_FREE_PAIRS
        ],
        "comparison": "lexicographic-nondecreasing-with-0-before-1",
        "encoding": (
            "forbid-each-common-prefix-followed-by-first-difference-1-0"
        ),
        "auxiliary_variables": 0,
        "clause_count": len(clauses),
        "literal_count": sum(map(len, clauses)),
        "clauses": [list(clause) for clause in clauses],
    }
    result = canonical_json_bytes(payload)
    if sha256_bytes(result) != EXPECTED_BREAKER_SHA256:
        raise AssertionError("signature-breaker artifact hash invariant failed")
    return result


def _derive_cnf_bytes(
    source_payload: bytes,
    clauses: Sequence[Sequence[int]],
) -> bytes:
    parsed = parse_dimacs_bytes(source_payload)
    if (
        parsed.variable_count != EXPECTED_SOURCE_VARIABLE_COUNT
        or len(parsed.clauses) != EXPECTED_SOURCE_CLAUSE_COUNT
        or sum(map(len, parsed.clauses)) != EXPECTED_SOURCE_LITERAL_COUNT
    ):
        raise ValueError("source CNF counts differ from the retained formula")
    header, body = source_payload.split(b"\n", 1)
    expected_header = (
        f"p cnf {EXPECTED_SOURCE_VARIABLE_COUNT} "
        f"{EXPECTED_SOURCE_CLAUSE_COUNT}"
    ).encode("ascii")
    if header != expected_header:
        raise ValueError("source CNF header is not canonical")
    stream = breaker_clause_stream_bytes(clauses)
    derived = (
        f"p cnf {EXPECTED_DERIVED_VARIABLE_COUNT} "
        f"{EXPECTED_DERIVED_CLAUSE_COUNT}\n"
    ).encode("ascii") + body + stream
    parsed_derived = parse_dimacs_bytes(derived)
    if (
        parsed_derived.variable_count != EXPECTED_DERIVED_VARIABLE_COUNT
        or parsed_derived.clauses
        != parsed.clauses + tuple(tuple(clause) for clause in clauses)
        or sum(map(len, parsed_derived.clauses))
        != EXPECTED_DERIVED_LITERAL_COUNT
    ):
        raise AssertionError("derived CNF is not source clauses plus breaker")
    if sha256_bytes(source_payload) == EXPECTED_SOURCE_CNF_SHA256:
        if sha256_bytes(derived) != EXPECTED_DERIVED_CNF_SHA256:
            raise AssertionError("derived CNF hash invariant failed")
    return derived


def _validate_source_identity(
    source_package: Path,
    *,
    exhaustive: bool,
) -> tuple[Path, dict[str, object], ParsedCNF]:
    report = audit_source_package(source_package, exhaustive=exhaustive)
    resolved = source_package.resolve(strict=True)
    identities = {
        "manifest_sha256": (
            sha256_file(resolved / MANIFEST_NAME),
            EXPECTED_SOURCE_MANIFEST_SHA256,
        ),
        "cnf_sha256": (
            sha256_file(resolved / CNF_NAME),
            EXPECTED_SOURCE_CNF_SHA256,
        ),
        "bank_sha256": (
            sha256_file(resolved / SOURCE_BANK_NAME),
            EXPECTED_SOURCE_BANK_SHA256,
        ),
    }
    for role, (actual, expected) in identities.items():
        if actual != expected:
            raise ValueError(f"retained source {role} differs from {expected}")
    if (
        report["template"] != TEMPLATE
        or report["variable_count"] != EXPECTED_SOURCE_VARIABLE_COUNT
        or report["clause_count"] != EXPECTED_SOURCE_CLAUSE_COUNT
        or report["literal_count"] != EXPECTED_SOURCE_LITERAL_COUNT
    ):
        raise ValueError("retained source package identity is wrong")
    parsed = parse_dimacs_bytes((resolved / CNF_NAME).read_bytes())
    return resolved, report, parsed


def _source_artifact_map(source: Path) -> dict[str, dict[str, object]]:
    return {
        "coloring_bank": _input_artifact_record(source / SOURCE_BANK_NAME),
        "cnf": _input_artifact_record(source / CNF_NAME),
        "manifest": _input_artifact_record(source / MANIFEST_NAME),
    }


def _manifest_payload(
    *,
    source: Path,
    source_report: Mapping[str, object],
    cnf_path: Path,
    breaker_path: Path,
    sources: Sequence[tuple[str, str]],
    git_binding: Mapping[str, object],
    comparator_audit: Mapping[str, object],
    covariance_report: Mapping[str, object],
) -> dict[str, object]:
    clauses = signature_breaker_clauses()
    stream = breaker_clause_stream_bytes(clauses)
    theorem_path = campaign_root() / THEOREM_RELATIVE_PATH
    return {
        "schema": "gamma-theta-hole5-signature-broken-package-v1",
        "schema_version": SCHEMA_VERSION,
        "template": TEMPLATE,
        "order": N,
        "source_package": {
            "required_identity": {
                "manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
                "cnf_sha256": EXPECTED_SOURCE_CNF_SHA256,
                "bank_sha256": EXPECTED_SOURCE_BANK_SHA256,
            },
            "artifacts": _source_artifact_map(source),
            "audited_counts": {
                "variables": source_report["variable_count"],
                "clauses": source_report["clause_count"],
                "literals": source_report["literal_count"],
                "bank_rows": source_report["bank_count"],
            },
        },
        "symmetry": {
            "group": "S6-on-vertices-6-through-11-fixing-0-through-5",
            "core_vertices": list(CORE_VERTICES),
            "free_vertices": list(FREE_VERTICES),
            "signature_bit_order": list(CORE_VERTICES),
            "ordered_adjacent_pairs": [
                list(pair) for pair in ADJACENT_FREE_PAIRS
            ],
            "theorem": {
                "path": THEOREM_RELATIVE_PATH,
                "sha256": sha256_file(theorem_path),
            },
            "comparator_audit": dict(comparator_audit),
            "covariance_audit": dict(covariance_report),
        },
        "formula_counts": {
            "source": {
                "variables": EXPECTED_SOURCE_VARIABLE_COUNT,
                "clauses": EXPECTED_SOURCE_CLAUSE_COUNT,
                "literals": EXPECTED_SOURCE_LITERAL_COUNT,
            },
            "appended": {
                "variables": 0,
                "clauses": EXPECTED_BREAKER_CLAUSE_COUNT,
                "literals": EXPECTED_BREAKER_LITERAL_COUNT,
            },
            "derived": {
                "variables": EXPECTED_DERIVED_VARIABLE_COUNT,
                "clauses": EXPECTED_DERIVED_CLAUSE_COUNT,
                "literals": EXPECTED_DERIVED_LITERAL_COUNT,
            },
        },
        "clause_layout": {
            "source_clause_first_index_zero_based": 0,
            "source_clause_end_index_exclusive": (
                EXPECTED_SOURCE_CLAUSE_COUNT
            ),
            "breaker_clause_first_index_zero_based": (
                EXPECTED_SOURCE_CLAUSE_COUNT
            ),
            "breaker_clause_end_index_exclusive": (
                EXPECTED_DERIVED_CLAUSE_COUNT
            ),
            "source_clause_order": "byte-identical-source-body",
            "breaker_clause_order": (
                "adjacent-pair-then-first-difference-then-prefix-lexicographic"
            ),
            "breaker_clause_stream_format": (
                "header-free-DIMACS-lines-terminal-zero-LF"
            ),
            "breaker_clause_stream_sha256": sha256_bytes(stream),
            "breaker_clause_stream_size_bytes": len(stream),
        },
        "artifacts": {
            "cnf": _artifact_record(cnf_path),
            "signature_breaker": _artifact_record(breaker_path),
        },
        "runtime_source_manifest": [
            [relative, digest] for relative, digest in sources
        ],
        "runtime_source_set_sha256": source_set_sha256(sources),
        "git_source_binding": dict(git_binding),
        "generation_recipe": {
            "module": "synthesis_k3.hole5_signature_breaker",
            "subcommand": "generate",
            "validation_gate": True,
            "source_to_head_gate": True,
        },
        "production_solve_gate": {
            "enabled": False,
            "claim_status": "NO_MATHEMATICAL_CLAIM",
            "reason": (
                "binary proof filtering/checking awaits hostile audit; "
                "this package is formula infrastructure only"
            ),
        },
    }


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
            raise ValueError(
                f"runtime source hash {index} is malformed"
            ) from error
        result.append((row[0], row[1]))
    return tuple(result)


def _validate_local_artifact(
    package: Path,
    value: object,
    *,
    expected_name: str,
    role: str,
) -> Path:
    record = _require_exact_keys(
        value, {"path", "sha256", "size_bytes"}, role
    )
    if (
        record["path"] != expected_name
        or type(record["sha256"]) is not str
        or len(record["sha256"]) != 64
        or type(record["size_bytes"]) is not int
        or record["size_bytes"] < 0
    ):
        raise ValueError(f"{role} record is malformed")
    path = package / expected_name
    _assert_regular_single_link(path, role)
    if (
        path.stat().st_size != record["size_bytes"]
        or sha256_file(path) != record["sha256"]
    ):
        raise ValueError(f"{role} binding differs")
    return path


def _validate_derived_directory(path: Path) -> Path:
    if not isinstance(path, Path):
        raise ValueError("package directory must be a pathlib.Path")
    _assert_no_symlink_components(path)
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise ValueError(f"derived package is missing: {path}") from error
    if not stat.S_ISDIR(information.st_mode):
        raise ValueError("derived package path is not a directory")
    resolved = path.resolve(strict=True)
    expected = {CNF_NAME, BREAKER_NAME, MANIFEST_NAME}
    names = {entry.name for entry in resolved.iterdir()}
    if names != expected:
        raise ValueError(
            f"derived package entries differ: {sorted(names)}"
        )
    for name in expected:
        _assert_regular_single_link(
            resolved / name, f"derived package artifact {name}"
        )
    return resolved


def audit_derived_package(
    package_directory: Path,
    *,
    source_package: Path,
    exhaustive_covariance: bool,
) -> dict[str, object]:
    """Reconstruct and check every byte of one derived package."""

    exhaustive = _require_bool(
        exhaustive_covariance, "exhaustive covariance flag"
    )
    package = _validate_derived_directory(package_directory)
    source, source_report, parsed_source = _validate_source_identity(
        source_package, exhaustive=exhaustive
    )
    manifest_path = package / MANIFEST_NAME
    manifest_payload = manifest_path.read_bytes()
    manifest = _require_exact_keys(
        strict_json_bytes(manifest_payload),
        {
            "schema",
            "schema_version",
            "template",
            "order",
            "source_package",
            "symmetry",
            "formula_counts",
            "clause_layout",
            "artifacts",
            "runtime_source_manifest",
            "runtime_source_set_sha256",
            "git_source_binding",
            "generation_recipe",
            "production_solve_gate",
        },
        "derived package manifest",
    )
    if (
        manifest["schema"]
        != "gamma-theta-hole5-signature-broken-package-v1"
        or manifest["schema_version"] != SCHEMA_VERSION
        or manifest["template"] != TEMPLATE
        or manifest["order"] != N
    ):
        raise ValueError("derived package manifest identity is wrong")
    artifacts = _require_exact_keys(
        manifest["artifacts"], {"cnf", "signature_breaker"}, "artifact map"
    )
    cnf_path = _validate_local_artifact(
        package,
        artifacts["cnf"],
        expected_name=CNF_NAME,
        role="derived CNF",
    )
    breaker_path = _validate_local_artifact(
        package,
        artifacts["signature_breaker"],
        expected_name=BREAKER_NAME,
        role="signature breaker",
    )
    expected_breaker = breaker_payload_bytes()
    if breaker_path.read_bytes() != expected_breaker:
        raise ValueError("signature-breaker artifact differs from reconstruction")
    clauses = signature_breaker_clauses()
    expected_cnf = _derive_cnf_bytes(
        (source / CNF_NAME).read_bytes(), clauses
    )
    if cnf_path.read_bytes() != expected_cnf:
        raise ValueError("derived CNF differs from exact reconstruction")
    comparator_report = exhaustive_comparator_audit()
    covariance_report = covariance_audit(parsed_source)
    recorded_sources = _parse_source_manifest(
        manifest["runtime_source_manifest"]
    )
    current_sources = runtime_source_manifest()
    if recorded_sources != current_sources:
        raise ValueError("runtime source binding changed")
    if (
        manifest["runtime_source_set_sha256"]
        != source_set_sha256(recorded_sources)
    ):
        raise ValueError("runtime source-set digest is wrong")
    recorded_git = manifest["git_source_binding"]
    if not isinstance(recorded_git, Mapping):
        raise ValueError("git source binding is malformed")
    head = recorded_git.get("head_commit")
    if type(head) is not str:
        raise ValueError("recorded git head is malformed")
    expected_git = git_source_binding(recorded_sources, head=head)
    if dict(recorded_git) != expected_git:
        raise ValueError("git source binding differs from repository objects")
    expected_manifest = _manifest_payload(
        source=source,
        source_report=source_report,
        cnf_path=cnf_path,
        breaker_path=breaker_path,
        sources=current_sources,
        git_binding=expected_git,
        comparator_audit=comparator_report,
        covariance_report=covariance_report,
    )
    if manifest_payload != canonical_json_bytes(expected_manifest):
        raise ValueError("derived manifest differs from exact reconstruction")
    parsed_derived = parse_dimacs_bytes(cnf_path.read_bytes())
    return {
        "status": "AUDITED_DERIVED_FORMULA_NONCLAIM",
        "claim_status": "NO_MATHEMATICAL_CLAIM",
        "template": TEMPLATE,
        "variable_count": parsed_derived.variable_count,
        "clause_count": len(parsed_derived.clauses),
        "literal_count": sum(map(len, parsed_derived.clauses)),
        "cnf_sha256": sha256_file(cnf_path),
        "breaker_sha256": sha256_file(breaker_path),
        "manifest_sha256": sha256_bytes(manifest_payload),
        "comparator_assignments_checked": comparator_report[
            "total_assignments_checked"
        ],
        "covariance_generators_checked": covariance_report[
            "generator_count"
        ],
        "source_exhaustive_oracle_checked": exhaustive,
    }


def generate_derived_package(
    *,
    source_package: Path,
    output_directory: Path,
    validation_gate: object,
) -> dict[str, object]:
    """Atomically generate a source-bound, no-overwrite derived package."""

    _require_gate(validation_gate)
    destination = _validate_new_output_directory(output_directory)
    source, source_report, parsed_source = _validate_source_identity(
        source_package, exhaustive=True
    )
    if destination == source or source in destination.parents:
        raise ValueError("derived output must not contain the source package")
    sources = runtime_source_manifest()
    git_binding = git_source_binding(sources)
    if git_binding.get("runtime_sources_match_head") is not True:
        raise RuntimeError(
            "production generation requires every runtime source to match HEAD"
        )
    comparator_report = exhaustive_comparator_audit()
    covariance_report = covariance_audit(parsed_source)
    clauses = signature_breaker_clauses()
    breaker_payload = breaker_payload_bytes()
    source_cnf_path = source / CNF_NAME
    source_hash_before = sha256_file(source_cnf_path)
    cnf_payload = _derive_cnf_bytes(source_cnf_path.read_bytes(), clauses)

    temporary = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.partial.",
            dir=destination.parent,
        )
    )
    installed = False
    try:
        cnf_path = temporary / CNF_NAME
        breaker_path = temporary / BREAKER_NAME
        manifest_path = temporary / MANIFEST_NAME
        _write_new_file(cnf_path, cnf_payload)
        _write_new_file(breaker_path, breaker_payload)
        manifest = _manifest_payload(
            source=source,
            source_report=source_report,
            cnf_path=cnf_path,
            breaker_path=breaker_path,
            sources=sources,
            git_binding=git_binding,
            comparator_audit=comparator_report,
            covariance_report=covariance_report,
        )
        _write_new_file(manifest_path, canonical_json_bytes(manifest))
        _fsync_directory(temporary)
        if sha256_file(source_cnf_path) != source_hash_before:
            raise RuntimeError("source CNF changed during derivation")
        audit_derived_package(
            temporary,
            source_package=source,
            exhaustive_covariance=True,
        )
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(
                f"output appeared during generation: {destination}"
            )
        os.rename(temporary, destination)
        installed = True
        _fsync_directory(destination.parent)
        return audit_derived_package(
            destination,
            source_package=source,
            exhaustive_covariance=False,
        )
    finally:
        if not installed and temporary.exists():
            shutil.rmtree(temporary)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="derive and audit the hole5 S6 signature-broken CNF"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser("generate")
    generate.add_argument("--source-package", type=Path, required=True)
    generate.add_argument("--output-dir", type=Path, required=True)
    generate.add_argument("--validation-gate", action="store_true")
    audit = subparsers.add_parser("audit")
    audit.add_argument("--source-package", type=Path, required=True)
    audit.add_argument("--package", type=Path, required=True)
    audit.add_argument("--exhaustive-covariance", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _build_parser().parse_args(argv)
    if arguments.command == "generate":
        report = generate_derived_package(
            source_package=arguments.source_package,
            output_directory=arguments.output_dir,
            validation_gate=arguments.validation_gate,
        )
    elif arguments.command == "audit":
        report = audit_derived_package(
            arguments.package,
            source_package=arguments.source_package,
            exhaustive_covariance=arguments.exhaustive_covariance,
        )
    else:
        raise AssertionError("argparse returned an unknown command")
    print(json.dumps(report, allow_nan=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
