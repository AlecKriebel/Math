#!/usr/bin/env python3
"""Independent preflight for the exact order-13, k=3, hole7 package.

This audit is read-only with respect to the repository.  It writes only under
private temporary directories, launches no SAT solver or proof checker, and
emits deterministic canonical JSON to stdout.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "instances/order13_k3_hole7"
EXPECTED_HEAD = "b9b74a38415dac6ef11bb7cbc55badf224affadd"
PYTHON = Path("/opt/homebrew/opt/python@3.14/bin/python3.14")
GIT = Path("/usr/bin/git")

EXPECTED_ARTIFACTS: dict[str, tuple[int, str]] = {
    "coloring-bank.json": (
        505_200,
        "efafa89d6096d81bc0ae5a1860be4d0ce69b56f4e4957c8bd307316c121e692d",
    ),
    "constructor-manifest.json": (
        5_409,
        "a218a21b761754bfaef520d8e98d10963c97a1178966cbfbb68054005ac53bf9",
    ),
    "instance.cnf": (
        1_372_338,
        "3e1c86ccbcfc1e04b3ec4de29ec5b7d342cf909553655f959b1c35de0a36c340",
    ),
}
EXPECTED_PACKAGE_SET_SHA256 = (
    "0f651f87b1339273776505da9eae50c1fa681623310216ea48d430ca354eb448"
)

EXPECTED_SOURCES: dict[str, tuple[int, str]] = {
    "src/search/order13_k3/__init__.py": (
        584,
        "90809fbba9e0fb06998ac910db44ff232849bd5b4ab8f9dfbc4c4e931ca96892",
    ),
    "src/search/order13_k3/__main__.py": (
        125,
        "6a1a7df4c3919e17d29bbe27ac10c6ba66e18a37bdefac0e0f05af845572b524",
    ),
    "src/search/order13_k3/encoding.py": (
        22_581,
        "da06a797a29fcefff1eadbea4aa1535fb2ef14c0c64d84236bb3bf9241e1d47d",
    ),
    "src/search/order13_k3/generate.py": (
        24_045,
        "35c78ecc4802667514c6294ac00558b83c9cfc83a37f9854533aedb9ca1bf1d0",
    ),
}
EXPECTED_SOURCE_SET_SHA256 = (
    "6dc5f770c792dfcc3ebaa8dd74485220832005e8c8026b030883356af38fcf64"
)

# These are the exact accepted C-055 mathematical and constructor review
# artifacts, including their audit sources and human review records.
EXPECTED_C055_BINDINGS: dict[str, tuple[int, str]] = {
    "math/lemmas/order13_k3_synthesis_target.md": (
        26_303,
        "7bec13620961adeaf61c60e88c8bc9366beecab7387e40c80083fe702484ab39",
    ),
    "reviews/order13_k3_constructor_acceptance/REVIEW.md": (
        6_905,
        "7d05355fdc92db4ccbb4a6254934015ddc89f216392fad341cff0bdb82f5e428",
    ),
    "reviews/order13_k3_constructor_acceptance/audit.py": (
        37_091,
        "cd421fb8c58035c2fdfad84811c2922e702c1dbe24d7d7d791242ed85721d0a6",
    ),
    "reviews/order13_k3_constructor_acceptance/evidence.json": (
        7_248,
        "8318d036867da89c2b2b7b9599bde17f50e160731d21243584609d34a515ec74",
    ),
    "reviews/order13_k3_constructor_independent/REVIEW.md": (
        6_803,
        "df128b29dd5464ec55465333d4672bc7dfbbe76538024325ab880a2a60d5bda4",
    ),
    "reviews/order13_k3_constructor_independent/evidence.json": (
        5_559,
        "784839ee925675b49a3636ab1625ef35389da2a6d418e629164c2ca5bb053e09",
    ),
    "reviews/order13_k3_constructor_independent/reconstruct.py": (
        33_886,
        "fbdce8d2bf2e605a1520da1bacda3fc49ca8f4926d91457c3d4d256335902cfc",
    ),
    "reviews/order13_k3_math_hostile/ADDENDUM.md": (
        2_415,
        "42fbc74ad916757a35df8bf5cbc6c4ab5205ae5f5d34abf915cff6bbb2203bd7",
    ),
    "reviews/order13_k3_math_hostile/REVIEW.md": (
        15_021,
        "284ec751a215e499de2adfa2f2b377d1a700a27a8b3e96964067c53f652698d8",
    ),
    "reviews/order13_k3_math_hostile/addendum_audit.py": (
        12_336,
        "51f070e3ecb653a3381603a09f78e5ce43540eac49a3d95e0ec106e789ea8cc2",
    ),
    "reviews/order13_k3_math_hostile/addendum_evidence.json": (
        3_456,
        "e45d99d880af6350034d7ee9a4b83acb30cc4706c9aa4445d97a07a272d3dc14",
    ),
    "reviews/order13_k3_math_hostile/audit.py": (
        47_177,
        "35d405424127c1a28742ade277fd5c5add0a109749ccc51ab6d622740371241b",
    ),
    "reviews/order13_k3_math_hostile/evidence.json": (
        20_660,
        "8c1f5b3fe4511a4d19efdc224a7ea6b10b38eac06275ddce615bd73949d22af1",
    ),
}

EXPECTED_COUNTS = {
    "variables": 9_802,
    "clauses": 34_903,
    "literals": 349_248,
    "base_clauses": 29_800,
    "base_literals": 227_019,
    "bank_rows": 5_103,
    "bank_literals": 122_229,
}


class AuditError(RuntimeError):
    """A fail-closed preflight rejection."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def strict_json(payload: bytes, role: str) -> object:
    def reject_constant(value: str) -> object:
        raise ValueError(f"nonfinite constant {value!r}")

    def reject_duplicate_keys(
        pairs: list[tuple[str, object]],
    ) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key {key!r}")
            result[key] = value
        return result

    try:
        text = payload.decode("utf-8")
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise AuditError(f"{role} is not strict UTF-8 JSON") from error


def directory_is_real(path: Path, role: str) -> None:
    try:
        information = os.lstat(path)
    except FileNotFoundError as error:
        raise AuditError(f"{role} is absent") from error
    require(stat.S_ISDIR(information.st_mode), f"{role} is not a real directory")


def regular_file_bytes(path: Path, role: str) -> bytes:
    """Read one single-link regular file with O_NOFOLLOW and stable metadata."""

    try:
        before = os.lstat(path)
    except FileNotFoundError as error:
        raise AuditError(f"{role} is absent") from error
    require(stat.S_ISREG(before.st_mode), f"{role} is not a regular file")
    require(before.st_nlink == 1, f"{role} has multiple hard links")

    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise AuditError(f"{role} cannot be opened safely") from error
    try:
        opened = os.fstat(descriptor)
        require(stat.S_ISREG(opened.st_mode), f"{role} changed file type")
        require(opened.st_nlink == 1, f"{role} changed link count")
        require(
            (before.st_dev, before.st_ino)
            == (opened.st_dev, opened.st_ino),
            f"{role} changed before open",
        )
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ),
            f"{role} changed while read",
        )
        payload = b"".join(chunks)
        require(len(payload) == after.st_size, f"{role} read was incomplete")
        return payload
    finally:
        os.close(descriptor)


def run_checked(
    command: Sequence[str],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
    timeout: int = 180,
) -> bytes:
    try:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            env=None if env is None else dict(env),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise AuditError("allowlisted subprocess failed to execute") from error
    require(
        completed.returncode == 0,
        "allowlisted subprocess returned nonzero",
    )
    return completed.stdout


def git_context() -> tuple[Path, str]:
    require(GIT.is_file(), "fixed git executable is absent")
    top_raw = run_checked(
        [str(GIT), "-C", str(ROOT), "rev-parse", "--show-toplevel"],
        cwd=ROOT,
        timeout=30,
    )
    try:
        top = Path(top_raw.decode("utf-8").strip()).resolve()
    except UnicodeDecodeError as error:
        raise AuditError("git top level is non-UTF-8") from error
    try:
        prefix = ROOT.resolve().relative_to(top).as_posix()
    except ValueError as error:
        raise AuditError("campaign directory lies outside git top level") from error
    require(prefix == "gamma_theta_eternal_domination", "git prefix differs")
    return top, prefix


def committed_blob(
    repo_top: Path,
    project_prefix: str,
    relative: str,
) -> bytes:
    require(
        relative
        and not relative.startswith("/")
        and ".." not in Path(relative).parts,
        "unsafe committed path",
    )
    return run_checked(
        [
            str(GIT),
            "-C",
            str(repo_top),
            "show",
            f"{EXPECTED_HEAD}:{project_prefix}/{relative}",
        ],
        cwd=ROOT,
        timeout=30,
    )


def source_set_hash(records: Sequence[dict[str, object]]) -> str:
    payload = "".join(
        f"{record['path']} {record['sha256']} {record['size_bytes']}\n"
        for record in records
    ).encode("ascii")
    return sha256(payload)


def validate_source_tree(
    source_root: Path,
    *,
    committed: Mapping[str, bytes] | None = None,
) -> tuple[list[dict[str, object]], str]:
    records: list[dict[str, object]] = []
    for relative, expected in EXPECTED_SOURCES.items():
        payload = regular_file_bytes(
            source_root / relative,
            f"constructor source {relative}",
        )
        require((len(payload), sha256(payload)) == expected, "source drift detected")
        if committed is not None:
            require(
                relative in committed and committed[relative] == payload,
                "working source differs from committed source",
            )
        records.append(
            {
                "path": relative,
                "sha256": sha256(payload),
                "size_bytes": len(payload),
            }
        )
    binding = source_set_hash(records)
    require(binding == EXPECTED_SOURCE_SET_SHA256, "source-set hash differs")
    return records, binding


def parse_dimacs(payload: bytes) -> tuple[int, list[tuple[int, ...]], int]:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise AuditError("formula is not ASCII DIMACS") from error
    require(text.endswith("\n"), "formula lacks terminal LF")
    lines = text.splitlines()
    require(bool(lines), "formula is empty")
    header = lines[0].split()
    require(
        len(header) == 4 and header[:2] == ["p", "cnf"],
        "DIMACS header differs",
    )
    try:
        variables = int(header[2])
        promised = int(header[3])
    except ValueError as error:
        raise AuditError("DIMACS header contains a noninteger") from error
    require(variables > 0 and promised > 0, "DIMACS header is nonpositive")

    clauses: list[tuple[int, ...]] = []
    literal_count = 0
    for line_number, line in enumerate(lines[1:], 2):
        fields = line.split()
        require(bool(fields), f"DIMACS line {line_number} is blank")
        require(fields[-1] == "0", f"DIMACS line {line_number} is open")
        require("0" not in fields[:-1], f"DIMACS line {line_number} embeds zero")
        try:
            clause = tuple(int(field) for field in fields[:-1])
        except ValueError as error:
            raise AuditError(
                f"DIMACS line {line_number} contains a noninteger"
            ) from error
        require(bool(clause), f"DIMACS line {line_number} is empty")
        require(
            all(0 < abs(literal) <= variables for literal in clause),
            f"DIMACS line {line_number} has an out-of-range literal",
        )
        clauses.append(clause)
        literal_count += len(clause)
    require(len(clauses) == promised, "DIMACS clause promise differs")
    return variables, clauses, literal_count


def first_use_canonical(row: Sequence[int]) -> bool:
    maximum = -1
    for color in row:
        if type(color) is not int or not 0 <= color < 3:
            return False
        if color > maximum + 1:
            return False
        maximum = max(maximum, color)
    return True


def derive_hole7_bank() -> list[tuple[int, ...]]:
    """Enumerate all first-use-canonical proper 3-colorings independently."""

    positive = {
        tuple(sorted((vertex, (vertex + 1) % 7)))
        for vertex in range(7)
    }
    positive.update({(0, 7), (1, 7)})
    prior_neighbors: list[list[int]] = [[] for _ in range(13)]
    for first, second in sorted(positive):
        prior_neighbors[second].append(first)

    row = [-1] * 13
    result: list[tuple[int, ...]] = []

    def visit(vertex: int, maximum: int) -> None:
        if vertex == 13:
            result.append(tuple(row))
            return
        for color in range(min(2, maximum + 1) + 1):
            if any(row[other] == color for other in prior_neighbors[vertex]):
                continue
            row[vertex] = color
            visit(vertex + 1, max(maximum, color))
            row[vertex] = -1

    visit(0, -1)
    require(
        result == sorted(set(result)),
        "independently derived bank is not sorted and unique",
    )
    return result


def validate_bank(payload: bytes) -> tuple[list[tuple[int, ...]], int]:
    raw = strict_json(payload, "coloring bank")
    require(type(raw) is list, "coloring bank is not a list")
    require(canonical_json(raw) == payload, "coloring bank is not canonical JSON")
    rows: list[tuple[int, ...]] = []
    for index, item in enumerate(raw):
        require(type(item) is list and len(item) == 13, f"bank row {index} differs")
        row = tuple(item)
        require(first_use_canonical(row), f"bank row {index} is noncanonical")
        rows.append(row)
    require(rows == sorted(set(rows)), "coloring bank is duplicated or unsorted")
    expected = derive_hole7_bank()
    require(rows == expected, "bank differs from independent exhaustive derivation")

    bank_literals = sum(
        1
        for row in rows
        for first, second in itertools.combinations(range(13), 2)
        if row[first] == row[second]
    )
    require(len(rows) == EXPECTED_COUNTS["bank_rows"], "bank row count differs")
    require(
        bank_literals == EXPECTED_COUNTS["bank_literals"],
        "bank literal census differs",
    )
    return rows, bank_literals


def validate_manifest(
    payload: bytes,
    *,
    artifact_records: Mapping[str, dict[str, object]],
    source_records: Sequence[dict[str, object]],
    source_set: str,
) -> dict[str, object]:
    raw = strict_json(payload, "constructor manifest")
    require(type(raw) is dict, "constructor manifest is not an object")
    require(canonical_json(raw) == payload, "manifest is not canonical JSON")
    require(
        set(raw)
        == {
            "artifacts",
            "base_clause_count",
            "base_literal_count",
            "claim_boundary",
            "clause_count",
            "clause_families",
            "coloring_row_count",
            "fixed_independent_triple_in_g",
            "frozen_pilot_match",
            "generation_environment",
            "graph_variable_semantics",
            "heuristic_symmetry_breakers",
            "literal_count",
            "normalized_audit_invocation",
            "normalized_regeneration_invocation",
            "order",
            "parameter",
            "production_defaults",
            "runtime_source_set_sha256",
            "runtime_sources",
            "schema",
            "schema_version",
            "template",
            "variable_count",
        },
        "manifest field set differs",
    )
    require(
        raw["schema"] == "gamma-theta-order13-k3-constructor-package-v1"
        and raw["schema_version"] == 1
        and raw["template"] == "hole7"
        and raw["order"] == 13
        and raw["parameter"] == 3,
        "manifest identity differs",
    )
    require(
        raw["claim_boundary"]
        == (
            "Exact formula construction only. No solver was launched and this "
            "package makes no SAT or UNSAT claim."
        ),
        "manifest claim boundary differs",
    )
    require(
        raw["graph_variable_semantics"]
        == "edge variables encode H=complement(G)"
        and raw["fixed_independent_triple_in_g"] == [0, 1, 7],
        "manifest graph semantics differ",
    )
    require(
        raw["heuristic_symmetry_breakers"] == [],
        "unsafe heuristic symmetry breaker is present",
    )
    expected_census = {
        "variable_count": EXPECTED_COUNTS["variables"],
        "clause_count": EXPECTED_COUNTS["clauses"],
        "literal_count": EXPECTED_COUNTS["literals"],
        "base_clause_count": EXPECTED_COUNTS["base_clauses"],
        "base_literal_count": EXPECTED_COUNTS["base_literals"],
        "coloring_row_count": EXPECTED_COUNTS["bank_rows"],
    }
    require(
        all(raw[key] == value for key, value in expected_census.items()),
        "manifest formula census differs",
    )
    require(
        raw["runtime_sources"] == list(source_records)
        and raw["runtime_source_set_sha256"] == source_set,
        "manifest runtime source binding differs",
    )
    require(
        raw["generation_environment"]
        == {"python_implementation": "CPython", "python_version": "3.14.6"},
        "manifest generation environment differs",
    )
    expected_regeneration = [
        "/usr/bin/env",
        "PYTHONPATH=src",
        str(PYTHON),
        "-m",
        "search.order13_k3",
        "generate",
        "--template",
        "hole7",
        "--output-directory",
        "<NEW_PACKAGE_DIRECTORY>",
        "--validation-gate",
    ]
    expected_audit = [
        "/usr/bin/env",
        "PYTHONPATH=src",
        str(PYTHON),
        "-m",
        "search.order13_k3",
        "audit",
        "--package-directory",
        "<PACKAGE_DIRECTORY>",
        "--exhaustive",
    ]
    require(
        raw["normalized_regeneration_invocation"] == expected_regeneration
        and raw["normalized_audit_invocation"] == expected_audit,
        "manifest normalized command differs",
    )
    require(
        raw["production_defaults"]
        == {
            "disk_reserve_mib": 8192,
            "maximum_parallel_solver_processes": 1,
            "memory_reserve_mib": 2048,
            "proof_file_limit_mib": 2048,
            "seed": 0,
            "solver_memory_mib": 2048,
            "solver_wall_seconds": 1800,
        },
        "manifest production defaults differ",
    )

    expected_bindings = {
        name: {
            "sha256": artifact_records[name]["sha256"],
            "size_bytes": artifact_records[name]["size_bytes"],
        }
        for name in ("coloring-bank.json", "instance.cnf")
    }
    require(raw["artifacts"] == expected_bindings, "manifest artifacts differ")
    require(
        raw["frozen_pilot_match"]
        == {
            "expected_sha256": artifact_records["instance.cnf"]["sha256"],
            "expected_size_bytes": artifact_records["instance.cnf"]["size_bytes"],
            "matched": True,
        },
        "manifest frozen-pilot binding differs",
    )

    families = raw["clause_families"]
    require(type(families) is dict and len(families) == 14, "families differ")
    for name, record in families.items():
        require(type(name) is str and type(record) is dict, "family record differs")
        require(
            set(record) == {"clause_stream_sha256", "clauses", "literals"}
            and type(record["clause_stream_sha256"]) is str
            and len(record["clause_stream_sha256"]) == 64
            and type(record["clauses"]) is int
            and type(record["literals"]) is int,
            "family record is malformed",
        )
    require(
        sum(record["clauses"] for record in families.values())
        == EXPECTED_COUNTS["clauses"]
        and sum(record["literals"] for record in families.values())
        == EXPECTED_COUNTS["literals"],
        "family totals differ",
    )
    coloring = families.get("complete_coloring_obstruction")
    require(
        coloring
        and coloring["clauses"] == EXPECTED_COUNTS["bank_rows"]
        and coloring["literals"] == EXPECTED_COUNTS["bank_literals"],
        "coloring family census differs",
    )
    return raw


def validate_package(
    package: Path,
    *,
    source_root: Path,
    committed_sources: Mapping[str, bytes] | None = None,
) -> dict[str, object]:
    directory_is_real(package, "package")
    names = sorted(entry.name for entry in package.iterdir())
    require(names == sorted(EXPECTED_ARTIFACTS), "package entries differ")

    payloads: dict[str, bytes] = {}
    records: list[dict[str, object]] = []
    for name in names:
        payload = regular_file_bytes(package / name, f"package artifact {name}")
        actual = (len(payload), sha256(payload))
        require(actual == EXPECTED_ARTIFACTS[name], f"{name} binding differs")
        payloads[name] = payload
        records.append(
            {
                "name": name,
                "sha256": actual[1],
                "size_bytes": actual[0],
            }
        )
    by_name = {record["name"]: record for record in records}
    package_binding = sha256(
        "".join(
            f"{record['name']} {record['sha256']} {record['size_bytes']}\n"
            for record in records
        ).encode("ascii")
    )
    require(
        package_binding == EXPECTED_PACKAGE_SET_SHA256,
        "package-set hash differs",
    )

    source_records, source_set = validate_source_tree(
        source_root,
        committed=committed_sources,
    )
    variables, clauses, literal_count = parse_dimacs(payloads["instance.cnf"])
    require(
        (
            variables,
            len(clauses),
            literal_count,
        )
        == (
            EXPECTED_COUNTS["variables"],
            EXPECTED_COUNTS["clauses"],
            EXPECTED_COUNTS["literals"],
        ),
        "parsed formula census differs",
    )
    rows, bank_literals = validate_bank(payloads["coloring-bank.json"])

    edge_variables = {
        edge: index
        for index, edge in enumerate(
            itertools.combinations(range(13), 2),
            start=1,
        )
    }
    expected_cuts = [
        tuple(
            edge_variables[(first, second)]
            for first, second in itertools.combinations(range(13), 2)
            if row[first] == row[second]
        )
        for row in rows
    ]
    require(
        clauses[-len(rows) :] == expected_cuts,
        "formula coloring suffix differs from independently derived bank cuts",
    )
    base_clauses = len(clauses) - len(rows)
    base_literals = literal_count - bank_literals
    require(
        (base_clauses, base_literals)
        == (
            EXPECTED_COUNTS["base_clauses"],
            EXPECTED_COUNTS["base_literals"],
        ),
        "independently derived base census differs",
    )

    manifest = validate_manifest(
        payloads["constructor-manifest.json"],
        artifact_records=by_name,
        source_records=source_records,
        source_set=source_set,
    )
    return {
        "artifacts": records,
        "base_clauses": base_clauses,
        "base_literals": base_literals,
        "bank_literals": bank_literals,
        "bank_rows": len(rows),
        "clauses": len(clauses),
        "family_count": len(manifest["clause_families"]),
        "literals": literal_count,
        "package_set_sha256": package_binding,
        "payloads": payloads,
        "source_records": source_records,
        "source_set_sha256": source_set,
        "variables": variables,
    }


def find_template_record(raw: object, key: str) -> dict[str, object]:
    require(type(raw) is list, "template record list is absent")
    matches = [
        record
        for record in raw
        if type(record) is dict and record.get("template") == key
    ]
    require(len(matches) == 1, f"accepted {key} record is not unique")
    return matches[0]


def validate_c055_audits(
    *,
    repo_top: Path,
    project_prefix: str,
) -> dict[str, object]:
    payloads: dict[str, bytes] = {}
    records: list[dict[str, object]] = []
    for relative, expected in EXPECTED_C055_BINDINGS.items():
        payload = regular_file_bytes(ROOT / relative, f"C-055 binding {relative}")
        require((len(payload), sha256(payload)) == expected, "C-055 binding differs")
        require(
            committed_blob(repo_top, project_prefix, relative) == payload,
            "C-055 binding differs from frozen baseline commit",
        )
        payloads[relative] = payload
        records.append(
            {
                "path": relative,
                "sha256": sha256(payload),
                "size_bytes": len(payload),
            }
        )

    constructor_b = strict_json(
        payloads["reviews/order13_k3_constructor_independent/evidence.json"],
        "independent constructor evidence",
    )
    require(
        type(constructor_b) is dict
        and canonical_json(constructor_b)
        == payloads["reviews/order13_k3_constructor_independent/evidence.json"]
        and constructor_b.get("verdict")
        == "ACCEPT_EXACT_CLEAN_ROOM_RECONSTRUCTION",
        "independent constructor acceptance differs",
    )
    b_hole7 = find_template_record(constructor_b.get("formulas"), "hole7")
    require(
        b_hole7.get("variables") == EXPECTED_COUNTS["variables"]
        and b_hole7.get("full_clauses") == EXPECTED_COUNTS["clauses"]
        and b_hole7.get("full_literals") == EXPECTED_COUNTS["literals"]
        and b_hole7.get("color_rows") == EXPECTED_COUNTS["bank_rows"]
        and b_hole7.get("sha256") == EXPECTED_ARTIFACTS["instance.cnf"][1]
        and b_hole7.get("no_unproved_symmetry_breaker") is True
        and b_hole7.get("only_justified_template_relabeling") is True
        and b_hole7.get("semantic_clause_multisets_exact") is True
        and b_hole7.get("coloring_bank_complete") is True,
        "independent constructor hole7 record differs",
    )

    constructor_a = strict_json(
        payloads["reviews/order13_k3_constructor_acceptance/evidence.json"],
        "constructor integration evidence",
    )
    require(
        type(constructor_a) is dict
        and canonical_json(constructor_a)
        == payloads["reviews/order13_k3_constructor_acceptance/evidence.json"]
        and constructor_a.get("verdict")
        == "ACCEPT_CONSTRUCTOR_A_FOR_PROOF_PRODUCTION_INPUTS"
        and constructor_a.get("solver_launched") is False
        and constructor_a.get("source_bindings_stable_pre_post") is True,
        "constructor integration acceptance differs",
    )
    a_hole7 = find_template_record(constructor_a.get("templates"), "hole7")
    require(
        a_hole7
        == {
            "bank_rows": 5103,
            "bank_sha256": EXPECTED_ARTIFACTS["coloring-bank.json"][1],
            "clause_family_names_counts_stream_hashes_match_b": True,
            "clauses": 34903,
            "complete_coloring_coverage": True,
            "constructor_a_exhaustive_audit": True,
            "constructor_b_byte_identical": True,
            "fixed_independent_triple": [0, 1, 7],
            "literals": 349248,
            "manifest_sha256": EXPECTED_ARTIFACTS["constructor-manifest.json"][1],
            "package_entries_exclusive": True,
            "sha256": EXPECTED_ARTIFACTS["instance.cnf"][1],
            "size_bytes": EXPECTED_ARTIFACTS["instance.cnf"][0],
            "template": "hole7",
            "variables": 9802,
        },
        "constructor integration hole7 record differs",
    )

    math_original = strict_json(
        payloads["reviews/order13_k3_math_hostile/evidence.json"],
        "mathematical audit evidence",
    )
    require(
        type(math_original) is dict
        and canonical_json(math_original)
        == payloads["reviews/order13_k3_math_hostile/evidence.json"]
        and math_original.get("verdict")
        == "ACCEPT_MATHEMATICS_WITH_NONMATHEMATICAL_WORDING_GAPS",
        "mathematical audit verdict differs",
    )
    branches = math_original.get("coloring_banks_and_clause_census", {}).get(
        "branches"
    )
    require(type(branches) is list, "mathematical branch census is absent")
    hole7_math = [
        record
        for record in branches
        if type(record) is dict and record.get("length") == 7
    ]
    require(
        len(hole7_math) == 1
        and hole7_math[0].get("variables") == 9802
        and hole7_math[0].get("base_clauses") == 29800
        and hole7_math[0].get("bank_rows") == 5103
        and hole7_math[0].get("full_clauses") == 34903
        and hole7_math[0].get("raw_labeled_rows") == 30618,
        "mathematical hole7 census differs",
    )

    addendum = strict_json(
        payloads["reviews/order13_k3_math_hostile/addendum_evidence.json"],
        "mathematical byte addendum evidence",
    )
    require(
        type(addendum) is dict
        and canonical_json(addendum)
        == payloads["reviews/order13_k3_math_hostile/addendum_evidence.json"]
        and addendum.get("verdict")
        == "ACCEPT_REVISED_BYTES_MATHEMATICS_UNCHANGED",
        "mathematical byte-addendum verdict differs",
    )
    theorem_diffs = addendum.get("exact_diff")
    require(type(theorem_diffs) is list, "theorem byte transfer is absent")
    synthesis_matches = [
        record
        for record in theorem_diffs
        if type(record) is dict
        and record.get("path") == "math/lemmas/order13_k3_synthesis_target.md"
    ]
    require(
        len(synthesis_matches) == 1
        and synthesis_matches[0].get("new")
        == {
            "bytes": EXPECTED_C055_BINDINGS[
                "math/lemmas/order13_k3_synthesis_target.md"
            ][0],
            "path": "math/lemmas/order13_k3_synthesis_target.md",
            "sha256": EXPECTED_C055_BINDINGS[
                "math/lemmas/order13_k3_synthesis_target.md"
            ][1],
        },
        "revised theorem binding differs",
    )

    return {
        "binding_count": len(records),
        "bindings": records,
        "constructor_a_verdict": constructor_a["verdict"],
        "constructor_b_verdict": constructor_b["verdict"],
        "hole7_constructor_records_exact": True,
        "math_addendum_verdict": addendum["verdict"],
        "math_original_verdict": math_original["verdict"],
        "theorem_bytes_transferred": True,
        "unsafe_symmetry_breakers_absent": True,
    }


def private_regeneration(
    *,
    committed_sources: Mapping[str, bytes],
    cleanroom_source: bytes,
    live_payloads: Mapping[str, bytes],
) -> dict[str, object]:
    require(PYTHON.is_file(), "fixed constructor Python is absent")
    with tempfile.TemporaryDirectory(
        prefix="order13-k3-hole7-preflight-",
        dir="/private/tmp",
    ) as temporary_name:
        temporary = Path(temporary_name)
        private_root = temporary / "gamma_theta_eternal_domination"
        for relative, payload in committed_sources.items():
            destination = private_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)

        cleanroom_path = (
            private_root
            / "reviews/order13_k3_constructor_independent/reconstruct.py"
        )
        cleanroom_path.parent.mkdir(parents=True, exist_ok=True)
        cleanroom_path.write_bytes(cleanroom_source)

        output = private_root / "generated-hole7"
        environment = {
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": "/opt/homebrew/bin:/usr/bin:/bin",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": str(private_root / "src"),
            "PYTHONWARNINGS": "error",
        }
        constructor_stdout = run_checked(
            [
                str(PYTHON),
                "-B",
                "-W",
                "error",
                "-m",
                "search.order13_k3",
                "generate",
                "--template",
                "hole7",
                "--output-directory",
                str(output),
                "--validation-gate",
            ],
            cwd=private_root,
            env=environment,
            timeout=180,
        )
        generated_manifest_stdout = strict_json(
            constructor_stdout,
            "private constructor stdout",
        )

        regenerated: list[dict[str, object]] = []
        for name in sorted(EXPECTED_ARTIFACTS):
            payload = regular_file_bytes(output / name, f"regenerated {name}")
            require(payload == live_payloads[name], f"regenerated {name} differs")
            regenerated.append(
                {
                    "name": name,
                    "sha256": sha256(payload),
                    "size_bytes": len(payload),
                }
            )
        private_manifest = strict_json(
            live_payloads["constructor-manifest.json"],
            "live manifest during private comparison",
        )
        require(
            generated_manifest_stdout == private_manifest,
            "constructor stdout and generated manifest differ",
        )

        cleanroom_formula = temporary / "cleanroom-hole7.cnf"
        run_checked(
            [
                str(PYTHON),
                "-I",
                "-B",
                "-W",
                "error",
                str(cleanroom_path),
                "emit",
                "--hole",
                "7",
                "--output",
                str(cleanroom_formula),
            ],
            cwd=private_root,
            env={
                "LANG": "C",
                "LC_ALL": "C",
                "PATH": "/opt/homebrew/bin:/usr/bin:/bin",
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONWARNINGS": "error",
            },
            timeout=180,
        )
        cleanroom_payload = regular_file_bytes(
            cleanroom_formula,
            "clean-room regenerated formula",
        )
        require(
            cleanroom_payload == live_payloads["instance.cnf"],
            "clean-room formula differs from live formula",
        )
        return {
            "all_three_constructor_a_files_byte_identical": True,
            "clean_committed_private_source_copy": True,
            "constructor_a_command": (
                "python -B -W error -m search.order13_k3 generate "
                "--template hole7 --validation-gate"
            ),
            "constructor_b_command": (
                "python -I -B -W error reconstruct.py emit --hole 7"
            ),
            "constructor_b_formula_byte_identical": True,
            "regenerated_artifacts": regenerated,
            "solver_or_proof_checker_launched": False,
        }


def write_package_fixture(
    parent: Path,
    name: str,
    payloads: Mapping[str, bytes],
) -> Path:
    package = parent / name
    package.mkdir()
    for artifact_name, payload in payloads.items():
        (package / artifact_name).write_bytes(payload)
    return package


def expect_rejected(action: Callable[[], object]) -> bool:
    try:
        action()
    except (AuditError, OSError, ValueError):
        return True
    return False


def mutation_suite(
    *,
    live_payloads: Mapping[str, bytes],
    committed_sources: Mapping[str, bytes],
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(
        prefix="order13-k3-hole7-mutations-",
        dir="/private/tmp",
    ) as temporary_name:
        temporary = Path(temporary_name)

        def record(name: str, action: Callable[[], object]) -> None:
            rejected = expect_rejected(action)
            require(rejected, f"mutation escaped: {name}")
            results.append({"mutation": name, "rejected": True})

        extra = write_package_fixture(temporary, "extra", live_payloads)
        (extra / "unexpected.txt").write_bytes(b"unexpected\n")
        record(
            "package_extra",
            lambda: validate_package(extra, source_root=ROOT),
        )

        for artifact_name, mutation_name in (
            ("instance.cnf", "formula_bit_flip"),
            ("coloring-bank.json", "bank_bit_flip"),
            ("constructor-manifest.json", "manifest_bit_flip"),
        ):
            fixture = write_package_fixture(
                temporary,
                mutation_name,
                live_payloads,
            )
            target = fixture / artifact_name
            mutant = bytearray(target.read_bytes())
            index = len(mutant) // 2
            mutant[index] ^= 1
            target.write_bytes(bytes(mutant))
            record(
                mutation_name,
                lambda fixture=fixture: validate_package(
                    fixture,
                    source_root=ROOT,
                ),
            )

        wrong_template = write_package_fixture(
            temporary,
            "wrong_template",
            live_payloads,
        )
        wrong_manifest = strict_json(
            (wrong_template / "constructor-manifest.json").read_bytes(),
            "wrong-template fixture manifest",
        )
        require(type(wrong_manifest) is dict, "fixture manifest differs")
        wrong_manifest["template"] = "hole9"
        wrong_manifest["fixed_independent_triple_in_g"] = [0, 1, 9]
        (wrong_template / "constructor-manifest.json").write_bytes(
            canonical_json(wrong_manifest)
        )
        record(
            "wrong_template",
            lambda: validate_package(wrong_template, source_root=ROOT),
        )

        artifact_symlink = write_package_fixture(
            temporary,
            "artifact_symlink",
            live_payloads,
        )
        symlink_target = temporary / "symlink-target.cnf"
        symlink_target.write_bytes(live_payloads["instance.cnf"])
        (artifact_symlink / "instance.cnf").unlink()
        (artifact_symlink / "instance.cnf").symlink_to(symlink_target)
        record(
            "artifact_symlink",
            lambda: validate_package(artifact_symlink, source_root=ROOT),
        )

        real_package = write_package_fixture(
            temporary,
            "real_package_for_directory_symlink",
            live_payloads,
        )
        package_symlink = temporary / "package_directory_symlink"
        package_symlink.symlink_to(real_package, target_is_directory=True)
        record(
            "package_directory_symlink",
            lambda: validate_package(package_symlink, source_root=ROOT),
        )

        source_drift_root = temporary / "source_drift_root"
        for relative, payload in committed_sources.items():
            destination = source_drift_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
        drifted = source_drift_root / "src/search/order13_k3/encoding.py"
        drifted.write_bytes(drifted.read_bytes() + b"\n")
        record(
            "source_drift",
            lambda: validate_source_tree(source_drift_root),
        )

        source_symlink_root = temporary / "source_symlink_root"
        for relative, payload in committed_sources.items():
            destination = source_symlink_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
        source_target = temporary / "source-symlink-target.py"
        source_target.write_bytes(
            committed_sources["src/search/order13_k3/encoding.py"]
        )
        linked_source = (
            source_symlink_root / "src/search/order13_k3/encoding.py"
        )
        linked_source.unlink()
        linked_source.symlink_to(source_target)
        record(
            "source_symlink",
            lambda: validate_source_tree(source_symlink_root),
        )

        hardlink_package = write_package_fixture(
            temporary,
            "hardlink_package",
            live_payloads,
        )
        hardlink_target = temporary / "hardlink-target.cnf"
        hardlink_target.write_bytes(live_payloads["instance.cnf"])
        (hardlink_package / "instance.cnf").unlink()
        os.link(hardlink_target, hardlink_package / "instance.cnf")
        record(
            "artifact_hardlink",
            lambda: validate_package(hardlink_package, source_root=ROOT),
        )

    require(len(results) == 10, "mutation count differs")
    return results


def main() -> None:
    repo_top, project_prefix = git_context()

    committed_sources = {
        relative: committed_blob(repo_top, project_prefix, relative)
        for relative in EXPECTED_SOURCES
    }
    source_records, source_set = validate_source_tree(
        ROOT,
        committed=committed_sources,
    )

    live = validate_package(
        PACKAGE,
        source_root=ROOT,
        committed_sources=committed_sources,
    )
    c055 = validate_c055_audits(
        repo_top=repo_top,
        project_prefix=project_prefix,
    )
    cleanroom_source = committed_blob(
        repo_top,
        project_prefix,
        "reviews/order13_k3_constructor_independent/reconstruct.py",
    )
    require(
        (
            len(cleanroom_source),
            sha256(cleanroom_source),
        )
        == EXPECTED_C055_BINDINGS[
            "reviews/order13_k3_constructor_independent/reconstruct.py"
        ],
        "committed clean-room constructor binding differs",
    )
    regeneration = private_regeneration(
        committed_sources=committed_sources,
        cleanroom_source=cleanroom_source,
        live_payloads=live["payloads"],
    )
    mutations = mutation_suite(
        live_payloads=live["payloads"],
        committed_sources=committed_sources,
    )

    # Re-read every live runtime source after private work, so concurrent drift
    # cannot be silently hidden by the initial snapshot.
    post_records, post_source_set = validate_source_tree(
        ROOT,
        committed=committed_sources,
    )
    require(
        post_records == source_records and post_source_set == source_set,
        "source binding changed during audit",
    )

    evidence = {
        "accepted_c055": c055,
        "claim_boundary": (
            "Exact pre-production constructor-input preflight only. No SAT "
            "solver or proof checker was launched; no SAT, UNSAT, template "
            "exclusion, finite-slice exclusion, or conjecture claim is made."
        ),
        "formula": {
            "base_clauses": live["base_clauses"],
            "base_literals": live["base_literals"],
            "clauses": live["clauses"],
            "literals": live["literals"],
            "sha256": EXPECTED_ARTIFACTS["instance.cnf"][1],
            "size_bytes": EXPECTED_ARTIFACTS["instance.cnf"][0],
            "variables": live["variables"],
        },
        "git": {
            "commit": EXPECTED_HEAD,
            "baseline_commit_available": True,
            "reviewed_files_equal_committed_blobs": True,
        },
        "manifest": {
            "clause_families": live["family_count"],
            "fixed_independent_triple_in_g": [0, 1, 7],
            "heuristic_symmetry_breakers": [],
            "sha256": EXPECTED_ARTIFACTS["constructor-manifest.json"][1],
            "size_bytes": EXPECTED_ARTIFACTS["constructor-manifest.json"][0],
            "template": "hole7",
            "unsafe_symmetry_breakers_absent": True,
        },
        "mutations": mutations,
        "package": {
            "artifacts": live["artifacts"],
            "entries_exact": True,
            "nonsymlink_single_link_regular_files": True,
            "package_set_hash_convention": (
                "SHA256 of sorted ASCII lines: "
                "name SP sha256 SP size_bytes LF"
            ),
            "package_set_sha256": live["package_set_sha256"],
            "path": "instances/order13_k3_hole7",
            "total_size_bytes": sum(
                int(record["size_bytes"]) for record in live["artifacts"]
            ),
        },
        "regeneration": regeneration,
        "schema": "gamma-theta-order13-k3-hole7-preflight-constructor-v1",
        "schema_version": 1,
        "solver_or_proof_checker_launched": False,
        "source_binding": {
            "records": source_records,
            "source_set_sha256": source_set,
            "stable_pre_post": True,
        },
        "strict_parsing": {
            "bank_canonical_json": True,
            "bank_exhaustively_rederived": True,
            "bank_literals": live["bank_literals"],
            "bank_rows": live["bank_rows"],
            "dimacs": True,
            "formula_bank_suffix_byte_semantics_exact": True,
            "manifest_canonical_json": True,
        },
        "verdict": "ACCEPT_EXACT_HOLE7_PACKAGE_PREFLIGHT",
    }
    sys.stdout.buffer.write(canonical_json(evidence))


if __name__ == "__main__":
    main()
