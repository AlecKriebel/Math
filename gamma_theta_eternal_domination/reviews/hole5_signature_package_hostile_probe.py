#!/usr/bin/env python3
"""Clean-room audit of the retained hole5 signature-broken CNF package.

This standard-library program deliberately imports neither the author
``hole5_signature_breaker`` module nor any synthesis/search module.  It
reconstructs the six-bit comparator suffix, the complete derived DIMACS
bytes, both package JSON objects, and the recorded Git source binding.
It also reruns the already independent S6 covariance probe as a subprocess
and requires byte-identical output.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence


SCHEMA = "gamma-theta-hole5-signature-package-hostile-audit-v1"
SCHEMA_VERSION = 1
ORDER = 12
VARIABLE_COUNT = 6_886
SOURCE_CLAUSE_COUNT = 23_653
SOURCE_LITERAL_COUNT = 188_959
BREAKER_CLAUSE_COUNT = 315
BREAKER_LITERAL_COUNT = 3_210
DERIVED_CLAUSE_COUNT = 23_968
DERIVED_LITERAL_COUNT = 192_169
EXPECTED_HEAD = "126071c723b8b9e4276f962b40a89f3049e6b5a5"
EXPECTED_SOURCE_CNF_SHA256 = (
    "76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7"
)
EXPECTED_SOURCE_CNF_SIZE = 742_899
EXPECTED_SOURCE_BANK_SHA256 = (
    "b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00"
)
EXPECTED_SOURCE_BANK_SIZE = 335_343
EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402"
)
EXPECTED_SOURCE_MANIFEST_SIZE = 3_079
EXPECTED_DERIVED_CNF_SHA256 = (
    "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104"
)
EXPECTED_DERIVED_CNF_SIZE = 754_323
EXPECTED_BREAKER_JSON_SHA256 = (
    "62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a"
)
EXPECTED_BREAKER_JSON_SIZE = 38_296
EXPECTED_MANIFEST_SHA256 = (
    "da33bc1708f7d21b92ceedc68710d5433a1aacbe6e32b8a7432bbab45d8cc788"
)
EXPECTED_MANIFEST_SIZE = 5_530
EXPECTED_BREAKER_STREAM_SHA256 = (
    "ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6"
)
EXPECTED_BREAKER_STREAM_SIZE = 11_424
EXPECTED_SOURCE_MULTISET_SHA256 = (
    "201496666b255837ff7692ce13ef058f867a11ea7404d571429b7bf0589b1b78"
)
EXPECTED_RUNTIME_SOURCE_SET_SHA256 = (
    "770b9f8c7cfa1814716ce6d8b601e514313fb4dd7e95cd8dfefb6c58df25bdd6"
)
EXPECTED_S6_PROBE_SHA256 = (
    "3515adc846e961738b86c572a90aa0f42945cfa6794e3700986c392999c4ab66"
)
EXPECTED_S6_LOG_SHA256 = (
    "f1d8f6d8d6f85bdffadcf39e5d4c4504b9cf0d1b8a609d8e5fe540523091b9de"
)
EXPECTED_RUNTIME_SOURCES = (
    (
        "src/synthesis_k3/__init__.py",
        "fbc5ca4211eb97b498e0eecd692333596bba409c26629623f8d547a48a379e86",
    ),
    (
        "src/synthesis_k3/encoding.py",
        "fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6",
    ),
    (
        "src/synthesis_k3/cegar.py",
        "411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c",
    ),
    (
        "src/synthesis_k3/template_color_bank.py",
        "dc69687f01e85bea643b73f713b1afca51b3911b3fee4a857da3fb07cc979838",
    ),
    (
        "src/synthesis_k3/hole5_signature_breaker.py",
        "cc1dc4249dc20f78e8eff4de14ffdca632da1e9455a381000786faa28c950c77",
    ),
    (
        "math/lemmas/hole5_signature_symmetry.md",
        "8f8192774c3de65c2468115cc2d4aadd392fa7a1f73261c23fa49886d9c183e8",
    ),
)
PACKAGE_FILES = frozenset(
    {"instance.cnf", "manifest.json", "signature_breaker.json"}
)
SOURCE_PACKAGE_FILES = frozenset(
    {"instance.cnf", "manifest.json", "coloring_bank.json"}
)
FIXED_VERTICES = tuple(range(6))
OUTER_VERTICES = tuple(range(6, 12))
ADJACENT_PAIRS = tuple(zip(OUTER_VERTICES, OUTER_VERTICES[1:]))


class AuditFailure(ValueError):
    """A package, reconstruction, or binding failed closed."""


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


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def strict_json(payload: bytes, role: str) -> object:
    def reject_constant(token: str) -> object:
        raise AuditFailure(f"{role}: nonfinite JSON constant {token}")

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"{role}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AuditFailure(f"{role}: JSON is not UTF-8") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise AuditFailure(f"{role}: malformed JSON") from error


def campaign_root() -> Path:
    source = Path(__file__).resolve()
    for ancestor in source.parents:
        if (
            ancestor
            / "results/synthesis_k3_hole5_signature_package/instance.cnf"
        ).is_file() and (
            ancestor
            / "results/synthesis_k3_template_bank_packages/hole5/instance.cnf"
        ).is_file():
            return ancestor
    raise AuditFailure("cannot locate campaign root")


def _assert_no_symlink_components(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            information = os.lstat(current)
        except FileNotFoundError as error:
            raise AuditFailure(f"missing path component {current}") from error
        require(
            not stat.S_ISLNK(information.st_mode),
            f"symlinked path component {current}",
        )


def _assert_regular_single_link(path: Path, role: str) -> None:
    _assert_no_symlink_components(path)
    information = os.lstat(path)
    require(stat.S_ISREG(information.st_mode), f"{role} is not a regular file")
    require(information.st_nlink == 1, f"{role} has multiple hard links")


def audit_directory(
    path: Path,
    expected_files: frozenset[str],
    role: str,
) -> dict[str, object]:
    _assert_no_symlink_components(path)
    information = os.lstat(path)
    require(stat.S_ISDIR(information.st_mode), f"{role} is not a directory")
    entries = tuple(sorted(path.iterdir(), key=lambda item: item.name))
    require(
        {entry.name for entry in entries} == expected_files,
        f"{role} has missing or extra entries",
    )
    records: dict[str, dict[str, object]] = {}
    for entry in entries:
        _assert_regular_single_link(entry, f"{role}/{entry.name}")
        records[entry.name] = {
            "sha256": sha256_file(entry),
            "size_bytes": entry.stat().st_size,
            "mode": f"{stat.S_IMODE(entry.stat().st_mode):04o}",
            "link_count": entry.stat().st_nlink,
        }
    return {
        "directory_mode": f"{stat.S_IMODE(information.st_mode):04o}",
        "files": records,
    }


def _parse_integer(token: bytes, role: str) -> int:
    require(token, f"{role}: empty integer")
    negative = token.startswith(b"-")
    digits = token[1:] if negative else token
    require(
        digits
        and all(48 <= byte <= 57 for byte in digits)
        and (digits == b"0" or digits[0] != 48),
        f"{role}: noncanonical integer",
    )
    require(not (negative and digits == b"0"), f"{role}: negative zero")
    return int(token)


def parse_dimacs(
    payload: bytes,
    *,
    variables: int,
    clauses: int,
    literals: int,
    role: str,
) -> tuple[tuple[tuple[int, ...], ...], bytes]:
    require(
        payload.endswith(b"\n")
        and b"\r" not in payload
        and b"\x00" not in payload,
        f"{role}: invalid byte framing",
    )
    lines = payload.splitlines()
    expected_header = f"p cnf {variables} {clauses}".encode("ascii")
    require(lines and lines[0] == expected_header, f"{role}: wrong header")
    require(len(lines) == clauses + 1, f"{role}: wrong clause-line count")
    parsed: list[tuple[int, ...]] = []
    literal_count = 0
    for line_number, line in enumerate(lines[1:], 2):
        tokens = line.split(b" ")
        require(
            tokens
            and all(tokens)
            and tokens[-1] == b"0",
            f"{role}: malformed clause line {line_number}",
        )
        row = tuple(
            _parse_integer(token, f"{role} line {line_number}")
            for token in tokens[:-1]
        )
        require(row, f"{role}: empty clause at line {line_number}")
        require(
            all(1 <= abs(value) <= variables for value in row),
            f"{role}: variable out of range at line {line_number}",
        )
        require(
            len(set(row)) == len(row),
            f"{role}: duplicate literal at line {line_number}",
        )
        values = set(row)
        require(
            not any(-value in values for value in row),
            f"{role}: tautology at line {line_number}",
        )
        parsed.append(row)
        literal_count += len(row)
    require(literal_count == literals, f"{role}: wrong literal count")
    first_newline = payload.index(b"\n")
    return tuple(parsed), payload[first_newline + 1 :]


def edge_variables() -> dict[tuple[int, int], int]:
    return {
        pair: index
        for index, pair in enumerate(
            itertools.combinations(range(ORDER), 2),
            1,
        )
    }


def signature_variables(
    vertex: int,
    edge: Mapping[tuple[int, int], int],
) -> tuple[int, ...]:
    return tuple(
        edge[tuple(sorted((fixed, vertex)))]
        for fixed in FIXED_VERTICES
    )


def comparator_clauses(
    left_vertex: int,
    right_vertex: int,
    edge: Mapping[tuple[int, int], int],
) -> tuple[tuple[int, ...], ...]:
    left = signature_variables(left_vertex, edge)
    right = signature_variables(right_vertex, edge)
    result: list[tuple[int, ...]] = []
    for pivot in range(6):
        for prefix in itertools.product((0, 1), repeat=pivot):
            clause: list[int] = []
            for index, bit in enumerate(prefix):
                if bit == 0:
                    clause.extend((left[index], right[index]))
                else:
                    clause.extend((-left[index], -right[index]))
            clause.extend((-left[pivot], right[pivot]))
            require(
                len(set(clause)) == len(clause),
                "independent comparator has duplicate literal",
            )
            values = set(clause)
            require(
                not any(-literal in values for literal in clause),
                "independent comparator is tautological",
            )
            result.append(tuple(clause))
    return tuple(result)


def all_breaker_clauses() -> tuple[tuple[int, ...], ...]:
    edge = edge_variables()
    return tuple(
        clause
        for left, right in ADJACENT_PAIRS
        for clause in comparator_clauses(left, right, edge)
    )


def dimacs_clause_stream(clauses: Sequence[Sequence[int]]) -> bytes:
    return b"".join(
        (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        for clause in clauses
    )


def comparator_truth_audit(
    clauses: Sequence[Sequence[int]],
    left_vertex: int,
    right_vertex: int,
) -> dict[str, object]:
    edge = edge_variables()
    left = signature_variables(left_vertex, edge)
    right = signature_variables(right_vertex, edge)
    accepted = 0
    rejected = 0
    mismatches = 0
    uniquely_failed: set[int] = set()
    for left_value in range(64):
        left_bits = tuple(
            (left_value >> (5 - index)) & 1 for index in range(6)
        )
        for right_value in range(64):
            right_bits = tuple(
                (right_value >> (5 - index)) & 1 for index in range(6)
            )
            assignment = {
                **{
                    variable: bool(bit)
                    for variable, bit in zip(left, left_bits)
                },
                **{
                    variable: bool(bit)
                    for variable, bit in zip(right, right_bits)
                },
            }
            failed = [
                index
                for index, clause in enumerate(clauses)
                if not any(
                    assignment[abs(literal)] == (literal > 0)
                    for literal in clause
                )
            ]
            actual = not failed
            expected = left_bits <= right_bits
            mismatches += int(actual != expected)
            if actual:
                accepted += 1
            else:
                rejected += 1
                require(
                    len(failed) == 1,
                    "a forbidden signature pair does not fail uniquely",
                )
                uniquely_failed.add(failed[0])
    require(mismatches == 0, "comparator truth relation mismatch")
    require(
        uniquely_failed == set(range(63)),
        "not every comparator clause has a unique witness",
    )
    return {
        "left_vertex": left_vertex,
        "right_vertex": right_vertex,
        "assignments": 4_096,
        "accepted": accepted,
        "rejected": rejected,
        "mismatches": mismatches,
        "essential_clause_count": len(uniquely_failed),
    }


def source_multiset_digest(
    clauses: Sequence[Sequence[int]],
) -> str:
    canonical = sorted(tuple(sorted(clause)) for clause in clauses)
    return sha256_bytes(dimacs_clause_stream(canonical))


def expected_breaker_json(
    clauses: Sequence[Sequence[int]],
) -> dict[str, object]:
    edge = edge_variables()
    return {
        "auxiliary_variables": 0,
        "clause_count": BREAKER_CLAUSE_COUNT,
        "clauses": [list(clause) for clause in clauses],
        "comparison": "lexicographic-nondecreasing-with-0-before-1",
        "core_vertices": list(FIXED_VERTICES),
        "encoding": (
            "forbid-each-common-prefix-followed-by-first-difference-1-0"
        ),
        "free_vertices": list(OUTER_VERTICES),
        "literal_count": BREAKER_LITERAL_COUNT,
        "order": ORDER,
        "ordered_adjacent_pairs": [list(pair) for pair in ADJACENT_PAIRS],
        "schema": "gamma-theta-hole5-signature-breaker-clauses-v1",
        "schema_version": 1,
        "signature_bit_order": list(FIXED_VERTICES),
        "signature_edge_variables": {
            str(vertex): list(signature_variables(vertex, edge))
            for vertex in OUTER_VERTICES
        },
        "template": "hole5",
    }


def artifact_record(path: Path) -> dict[str, object]:
    return {
        "path": path.name,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def expected_manifest(
    *,
    package: Path,
    source_package: Path,
    source_multiset_sha256: str,
) -> dict[str, object]:
    runtime_rows = [list(row) for row in EXPECTED_RUNTIME_SOURCES]
    return {
        "artifacts": {
            "cnf": artifact_record(package / "instance.cnf"),
            "signature_breaker": artifact_record(
                package / "signature_breaker.json"
            ),
        },
        "clause_layout": {
            "breaker_clause_end_index_exclusive": DERIVED_CLAUSE_COUNT,
            "breaker_clause_first_index_zero_based": SOURCE_CLAUSE_COUNT,
            "breaker_clause_order": (
                "adjacent-pair-then-first-difference-then-prefix-lexicographic"
            ),
            "breaker_clause_stream_format": (
                "header-free-DIMACS-lines-terminal-zero-LF"
            ),
            "breaker_clause_stream_sha256": EXPECTED_BREAKER_STREAM_SHA256,
            "breaker_clause_stream_size_bytes": EXPECTED_BREAKER_STREAM_SIZE,
            "source_clause_end_index_exclusive": SOURCE_CLAUSE_COUNT,
            "source_clause_first_index_zero_based": 0,
            "source_clause_order": "byte-identical-source-body",
        },
        "formula_counts": {
            "appended": {
                "clauses": BREAKER_CLAUSE_COUNT,
                "literals": BREAKER_LITERAL_COUNT,
                "variables": 0,
            },
            "derived": {
                "clauses": DERIVED_CLAUSE_COUNT,
                "literals": DERIVED_LITERAL_COUNT,
                "variables": VARIABLE_COUNT,
            },
            "source": {
                "clauses": SOURCE_CLAUSE_COUNT,
                "literals": SOURCE_LITERAL_COUNT,
                "variables": VARIABLE_COUNT,
            },
        },
        "generation_recipe": {
            "module": "synthesis_k3.hole5_signature_breaker",
            "source_to_head_gate": True,
            "subcommand": "generate",
            "validation_gate": True,
        },
        "git_source_binding": {
            "global_worktree_cleanliness_required": False,
            "head_commit": EXPECTED_HEAD,
            "repository_relative_campaign_path": (
                "gamma_theta_eternal_domination"
            ),
            "runtime_source_mismatches": [],
            "runtime_sources_match_head": True,
        },
        "order": ORDER,
        "production_solve_gate": {
            "claim_status": "NO_MATHEMATICAL_CLAIM",
            "enabled": False,
            "reason": (
                "binary proof filtering/checking awaits hostile audit; "
                "this package is formula infrastructure only"
            ),
        },
        "runtime_source_manifest": runtime_rows,
        "runtime_source_set_sha256": EXPECTED_RUNTIME_SOURCE_SET_SHA256,
        "schema": "gamma-theta-hole5-signature-broken-package-v1",
        "schema_version": 1,
        "source_package": {
            "artifacts": {
                "cnf": artifact_record(source_package / "instance.cnf"),
                "coloring_bank": artifact_record(
                    source_package / "coloring_bank.json"
                ),
                "manifest": artifact_record(source_package / "manifest.json"),
            },
            "audited_counts": {
                "bank_rows": 3_645,
                "clauses": SOURCE_CLAUSE_COUNT,
                "literals": SOURCE_LITERAL_COUNT,
                "variables": VARIABLE_COUNT,
            },
            "required_identity": {
                "bank_sha256": EXPECTED_SOURCE_BANK_SHA256,
                "cnf_sha256": EXPECTED_SOURCE_CNF_SHA256,
                "manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
            },
        },
        "symmetry": {
            "comparator_audit": {
                "adjacent_comparators_checked": 5,
                "assignments_per_comparator": 4_096,
                "total_assignments_checked": 20_480,
                "truth_relation": "six-bit-lexicographic-nondecreasing",
            },
            "core_vertices": list(FIXED_VERTICES),
            "covariance_audit": {
                "generator_count": 5,
                "generator_transpositions_checked": [
                    list(pair) for pair in ADJACENT_PAIRS
                ],
                "group": "S6-on-vertices-6-through-11-fixing-0-through-5",
                "source_clause_count": SOURCE_CLAUSE_COUNT,
                "source_clause_multiset_sha256": source_multiset_sha256,
            },
            "free_vertices": list(OUTER_VERTICES),
            "group": "S6-on-vertices-6-through-11-fixing-0-through-5",
            "ordered_adjacent_pairs": [list(pair) for pair in ADJACENT_PAIRS],
            "signature_bit_order": list(FIXED_VERTICES),
            "theorem": {
                "path": "math/lemmas/hole5_signature_symmetry.md",
                "sha256": EXPECTED_RUNTIME_SOURCES[-1][1],
            },
        },
        "template": "hole5",
    }


def git_command(
    repository: Path,
    arguments: Sequence[str],
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "--no-pager", "-C", str(repository), *arguments],
        env={
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        },
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=30,
        check=False,
    )


def audit_git_binding(root: Path) -> dict[str, object]:
    repository_result = git_command(root, ["rev-parse", "--show-toplevel"])
    require(repository_result.returncode == 0, "cannot resolve Git root")
    repository = Path(
        repository_result.stdout.decode("utf-8").strip()
    ).resolve(strict=True)
    campaign_relative = root.relative_to(repository).as_posix()
    require(
        campaign_relative == "gamma_theta_eternal_domination",
        "unexpected campaign-relative path",
    )
    commit_result = git_command(
        repository,
        ["cat-file", "-e", f"{EXPECTED_HEAD}^{{commit}}"],
    )
    require(
        commit_result.returncode == 0,
        "recorded package generation commit is unavailable",
    )
    replayed: list[dict[str, object]] = []
    for relative, expected_digest in EXPECTED_RUNTIME_SOURCES:
        current = root / relative
        _assert_regular_single_link(current, f"runtime source {relative}")
        current_digest = sha256_file(current)
        shown = git_command(
            repository,
            [
                "show",
                f"{EXPECTED_HEAD}:{campaign_relative}/{relative}",
            ],
        )
        require(shown.returncode == 0, f"cannot replay Git source {relative}")
        git_digest = sha256_bytes(shown.stdout)
        require(
            current_digest == expected_digest == git_digest,
            f"runtime/Git source mismatch for {relative}",
        )
        replayed.append(
            {
                "path": relative,
                "sha256": expected_digest,
                "current_matches": True,
                "git_object_matches": True,
            }
        )
    source_set = sha256_bytes(
        "".join(
            f"{relative} {digest}\n"
            for relative, digest in EXPECTED_RUNTIME_SOURCES
        ).encode("ascii")
    )
    require(
        source_set == EXPECTED_RUNTIME_SOURCE_SET_SHA256,
        "runtime source-set digest differs",
    )
    return {
        "recorded_head": EXPECTED_HEAD,
        "recorded_commit_exists": True,
        "campaign_relative_path": campaign_relative,
        "runtime_source_set_sha256": source_set,
        "runtime_sources": replayed,
    }


def rerun_s6_probe(root: Path) -> dict[str, object]:
    probe = root / "reviews/hole5_signature_symmetry_hostile_probe.py"
    retained_log = (
        root / "reviews/hole5_signature_symmetry_hostile_probe_log.json"
    )
    _assert_regular_single_link(probe, "independent S6 probe")
    _assert_regular_single_link(retained_log, "independent S6 retained log")
    require(
        sha256_file(probe) == EXPECTED_S6_PROBE_SHA256,
        "independent S6 probe hash differs",
    )
    retained = retained_log.read_bytes()
    require(
        sha256_bytes(retained) == EXPECTED_S6_LOG_SHA256,
        "independent S6 log hash differs",
    )
    completed = subprocess.run(
        [sys.executable, str(probe.resolve())],
        cwd=root,
        env={
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        },
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=60,
        check=False,
    )
    require(completed.returncode == 0, "independent S6 probe rerun failed")
    require(completed.stderr == b"", "independent S6 probe emitted stderr")
    require(completed.stdout == retained, "independent S6 output changed")
    return {
        "probe_sha256": EXPECTED_S6_PROBE_SHA256,
        "retained_log_sha256": EXPECTED_S6_LOG_SHA256,
        "rerun_stdout_sha256": sha256_bytes(completed.stdout),
        "rerun_byte_identical": True,
        "exit_code": completed.returncode,
        "stderr_sha256": sha256_bytes(completed.stderr),
    }


def tree_digest(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    total = 0
    files = 0
    for item in sorted(
        (candidate for candidate in path.rglob("*") if candidate.is_file()),
        key=lambda candidate: candidate.relative_to(path).as_posix(),
    ):
        relative = item.relative_to(path).as_posix().encode("utf-8")
        payload = item.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
        total += len(payload)
        files += 1
    return {
        "sha256": digest.hexdigest(),
        "file_count": files,
        "size_bytes": total,
        "convention": (
            "sorted-relative-path; uint64be(path length); path; "
            "uint64be(payload length); payload"
        ),
    }


def run_audit() -> dict[str, object]:
    root = campaign_root()
    package = root / "results/synthesis_k3_hole5_signature_package"
    source_package = (
        root / "results/synthesis_k3_template_bank_packages/hole5"
    )
    package_filesystem = audit_directory(
        package, PACKAGE_FILES, "signature package"
    )
    source_filesystem = audit_directory(
        source_package, SOURCE_PACKAGE_FILES, "source package"
    )

    expected_source_records = {
        "instance.cnf": (
            EXPECTED_SOURCE_CNF_SHA256,
            EXPECTED_SOURCE_CNF_SIZE,
        ),
        "coloring_bank.json": (
            EXPECTED_SOURCE_BANK_SHA256,
            EXPECTED_SOURCE_BANK_SIZE,
        ),
        "manifest.json": (
            EXPECTED_SOURCE_MANIFEST_SHA256,
            EXPECTED_SOURCE_MANIFEST_SIZE,
        ),
    }
    for name, (digest, size) in expected_source_records.items():
        record = source_filesystem["files"][name]
        require(
            record["sha256"] == digest and record["size_bytes"] == size,
            f"source package binding differs for {name}",
        )

    source_payload = (source_package / "instance.cnf").read_bytes()
    source_clauses, source_body = parse_dimacs(
        source_payload,
        variables=VARIABLE_COUNT,
        clauses=SOURCE_CLAUSE_COUNT,
        literals=SOURCE_LITERAL_COUNT,
        role="source CNF",
    )
    source_multiset_sha256 = source_multiset_digest(source_clauses)
    require(
        source_multiset_sha256 == EXPECTED_SOURCE_MULTISET_SHA256,
        "source clause-multiset digest differs",
    )

    breaker_clauses = all_breaker_clauses()
    require(
        len(breaker_clauses) == BREAKER_CLAUSE_COUNT,
        "independent breaker clause count differs",
    )
    require(
        sum(map(len, breaker_clauses)) == BREAKER_LITERAL_COUNT,
        "independent breaker literal count differs",
    )
    breaker_stream = dimacs_clause_stream(breaker_clauses)
    require(
        len(breaker_stream) == EXPECTED_BREAKER_STREAM_SIZE
        and sha256_bytes(breaker_stream) == EXPECTED_BREAKER_STREAM_SHA256,
        "independent breaker stream differs",
    )
    length_distribution = Counter(map(len, breaker_clauses))
    require(
        length_distribution
        == Counter({2: 5, 4: 10, 6: 20, 8: 40, 10: 80, 12: 160}),
        "breaker clause-length distribution differs",
    )
    comparator_checks = [
        comparator_truth_audit(
            breaker_clauses[index * 63 : (index + 1) * 63],
            left,
            right,
        )
        for index, (left, right) in enumerate(ADJACENT_PAIRS)
    ]

    expected_breaker_payload = canonical_json_bytes(
        expected_breaker_json(breaker_clauses)
    )
    actual_breaker_payload = (package / "signature_breaker.json").read_bytes()
    strict_json(actual_breaker_payload, "signature breaker")
    require(
        actual_breaker_payload == expected_breaker_payload,
        "signature_breaker.json differs from independent reconstruction",
    )
    require(
        len(actual_breaker_payload) == EXPECTED_BREAKER_JSON_SIZE
        and sha256_bytes(actual_breaker_payload)
        == EXPECTED_BREAKER_JSON_SHA256,
        "signature breaker artifact binding differs",
    )

    expected_derived_payload = (
        f"p cnf {VARIABLE_COUNT} {DERIVED_CLAUSE_COUNT}\n".encode("ascii")
        + source_body
        + breaker_stream
    )
    derived_payload = (package / "instance.cnf").read_bytes()
    derived_clauses, derived_body = parse_dimacs(
        derived_payload,
        variables=VARIABLE_COUNT,
        clauses=DERIVED_CLAUSE_COUNT,
        literals=DERIVED_LITERAL_COUNT,
        role="derived CNF",
    )
    require(
        derived_payload == expected_derived_payload,
        "derived CNF is not exact source body plus independent suffix",
    )
    require(
        derived_body[: len(source_body)] == source_body
        and derived_body[len(source_body) :] == breaker_stream,
        "derived CNF body prefix/suffix split differs",
    )
    require(
        derived_clauses[:SOURCE_CLAUSE_COUNT] == source_clauses
        and derived_clauses[SOURCE_CLAUSE_COUNT:] == breaker_clauses,
        "derived CNF clause prefix/suffix differs",
    )
    require(
        len(derived_payload) == EXPECTED_DERIVED_CNF_SIZE
        and sha256_bytes(derived_payload) == EXPECTED_DERIVED_CNF_SHA256,
        "derived CNF binding differs",
    )

    manifest_path = package / "manifest.json"
    manifest_payload = manifest_path.read_bytes()
    strict_json(manifest_payload, "signature package manifest")
    reconstructed_manifest = expected_manifest(
        package=package,
        source_package=source_package,
        source_multiset_sha256=source_multiset_sha256,
    )
    require(
        manifest_payload == canonical_json_bytes(reconstructed_manifest),
        "manifest shape or value differs from independent reconstruction",
    )
    require(
        len(manifest_payload) == EXPECTED_MANIFEST_SIZE
        and sha256_bytes(manifest_payload) == EXPECTED_MANIFEST_SHA256,
        "manifest binding differs",
    )

    git_binding = audit_git_binding(root)
    s6_rerun = rerun_s6_probe(root)
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "status": "PASS",
        "claim_status": "NO_MATHEMATICAL_CLAIM",
        "probe_sha256": sha256_file(Path(__file__)),
        "package": {
            "relative_path": (
                "results/synthesis_k3_hole5_signature_package"
            ),
            "filesystem": package_filesystem,
            "tree": tree_digest(package),
            "manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "signature_breaker_sha256": EXPECTED_BREAKER_JSON_SHA256,
            "cnf_sha256": EXPECTED_DERIVED_CNF_SHA256,
        },
        "source_package": {
            "relative_path": (
                "results/synthesis_k3_template_bank_packages/hole5"
            ),
            "filesystem": source_filesystem,
            "cnf_sha256": EXPECTED_SOURCE_CNF_SHA256,
            "coloring_bank_sha256": EXPECTED_SOURCE_BANK_SHA256,
            "manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
            "clause_multiset_sha256": source_multiset_sha256,
        },
        "independent_reconstruction": {
            "variables": VARIABLE_COUNT,
            "source_clauses": SOURCE_CLAUSE_COUNT,
            "source_literals": SOURCE_LITERAL_COUNT,
            "breaker_clauses": BREAKER_CLAUSE_COUNT,
            "breaker_literals": BREAKER_LITERAL_COUNT,
            "derived_clauses": DERIVED_CLAUSE_COUNT,
            "derived_literals": DERIVED_LITERAL_COUNT,
            "source_body_preserved_byte_for_byte": True,
            "breaker_stream_sha256": EXPECTED_BREAKER_STREAM_SHA256,
            "breaker_stream_size_bytes": EXPECTED_BREAKER_STREAM_SIZE,
            "clause_length_distribution": {
                str(length): count
                for length, count in sorted(length_distribution.items())
            },
            "signature_edge_variables": (
                expected_breaker_json(breaker_clauses)[
                    "signature_edge_variables"
                ]
            ),
            "comparator_truth_checks": comparator_checks,
            "signature_breaker_json_byte_exact": True,
            "derived_cnf_byte_exact": True,
            "manifest_byte_exact": True,
        },
        "git_binding": git_binding,
        "independent_s6_probe_rerun": s6_rerun,
        "production_solve_enabled": False,
    }


def _assert_new_output(path: Path) -> Path:
    output = path.absolute()
    _assert_no_symlink_components(output.parent)
    require(output.parent.is_dir(), "output parent is not a directory")
    require(not output.exists(), "output already exists")
    return output


def write_new(path: Path, payload: bytes) -> None:
    output = _assert_new_output(path)
    with output.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    descriptor = os.open(output.parent, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Clean-room retained-package audit for the hole5 signature CNF"
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write canonical audit JSON to this new file",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        result = run_audit()
        payload = canonical_json_bytes(result)
        if arguments.output is None:
            sys.stdout.buffer.write(payload)
        else:
            write_new(arguments.output, payload)
            print(
                json.dumps(
                    {
                        "output": str(arguments.output.absolute()),
                        "sha256": sha256_bytes(payload),
                        "status": "PASS",
                    },
                    sort_keys=True,
                )
            )
        return 0
    except (
        AuditFailure,
        OSError,
        subprocess.SubprocessError,
        UnicodeError,
    ) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
