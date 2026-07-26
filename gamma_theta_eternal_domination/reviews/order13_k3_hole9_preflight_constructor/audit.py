#!/usr/bin/env python3
"""Read-only preflight audit of the live order-13 k=3 hole9 package.

The checker launches no child process and writes no file.  It binds the
three live package artifacts, strictly parses the DIMACS and JSON, validates
the constructor manifest and current runtime sources, and compares the result
with the frozen constructor-acceptance evidence.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "instances/order13_k3_hole9"
ACCEPTANCE = ROOT / "reviews/order13_k3_constructor_acceptance/evidence.json"

EXPECTED_ARTIFACTS = {
    "coloring-bank.json": (
        227208,
        "a0f47a0aaa3be4659ce483f27a963d351f3a13424cac6a6a99ef6ac9e0c872f1",
    ),
    "constructor-manifest.json": (
        5408,
        "8f55019121df7280368528c1b7c0808d3cc06e7bd0f871be516057763c87ad5b",
    ),
    "instance.cnf": (
        1168197,
        "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
    ),
}
EXPECTED_PACKAGE_SET_SHA256 = (
    "ba05d99b67816c1f1eeac2569b694ec1fc4412a584e95f359452bdfe12eaad6a"
)
EXPECTED_ACCEPTANCE = (
    7248,
    "8318d036867da89c2b2b7b9599bde17f50e160731d21243584609d34a515ec74",
)
EXPECTED_SOURCE_SET_SHA256 = (
    "6dc5f770c792dfcc3ebaa8dd74485220832005e8c8026b030883356af38fcf64"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def strict_json(payload: bytes, role: str) -> object:
    def reject_constant(value: str) -> object:
        raise ValueError(f"nonfinite constant {value!r}")

    def reject_duplicates(
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
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"{role} is not strict UTF-8 JSON") from error


def canonical_json(payload: object) -> bytes:
    return (
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def regular_file_bytes(path: Path, role: str) -> bytes:
    information = os.lstat(path)
    require(stat.S_ISREG(information.st_mode), f"{role} is not regular")
    require(information.st_nlink == 1, f"{role} has multiple hard links")
    return path.read_bytes()


def parse_dimacs(payload: bytes) -> tuple[int, int, int]:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as error:
        raise RuntimeError("instance is not ASCII DIMACS") from error
    require(text.endswith("\n"), "instance lacks terminal LF")
    lines = text.splitlines()
    require(bool(lines), "instance is empty")
    header = lines[0].split()
    require(
        len(header) == 4 and header[:2] == ["p", "cnf"],
        "DIMACS header differs",
    )
    try:
        variables = int(header[2])
        promised_clauses = int(header[3])
    except ValueError as error:
        raise RuntimeError("DIMACS header is noninteger") from error
    clauses = 0
    literals = 0
    for index, line in enumerate(lines[1:], 2):
        fields = line.split()
        require(bool(fields) and fields[-1] == "0", f"clause {index} is open")
        require("0" not in fields[:-1], f"clause {index} has embedded zero")
        try:
            values = tuple(int(field) for field in fields[:-1])
        except ValueError as error:
            raise RuntimeError(f"clause {index} is noninteger") from error
        require(bool(values), f"clause {index} is empty")
        require(
            all(0 < abs(value) <= variables for value in values),
            f"clause {index} has an out-of-range literal",
        )
        clauses += 1
        literals += len(values)
    require(clauses == promised_clauses, "DIMACS clause promise differs")
    return variables, clauses, literals


def package_bindings() -> tuple[list[dict[str, object]], str]:
    require(PACKAGE.is_dir() and not PACKAGE.is_symlink(), "package is unsafe")
    names = sorted(entry.name for entry in PACKAGE.iterdir())
    require(
        names == sorted(EXPECTED_ARTIFACTS),
        f"package entries differ: {names}",
    )
    records: list[dict[str, object]] = []
    for name in names:
        payload = regular_file_bytes(PACKAGE / name, name)
        actual = (len(payload), sha256(payload))
        require(actual == EXPECTED_ARTIFACTS[name], f"{name} binding differs")
        records.append(
            {
                "name": name,
                "sha256": actual[1],
                "size_bytes": actual[0],
            }
        )
    binding_payload = "".join(
        f"{record['name']} {record['sha256']} {record['size_bytes']}\n"
        for record in records
    ).encode("ascii")
    binding = sha256(binding_payload)
    require(binding == EXPECTED_PACKAGE_SET_SHA256, "package-set hash differs")
    return records, binding


def validate_manifest(
    raw: bytes,
    *,
    instance_record: dict[str, object],
    bank_record: dict[str, object],
) -> dict[str, object]:
    manifest = strict_json(raw, "constructor manifest")
    require(type(manifest) is dict, "constructor manifest is not an object")
    require(canonical_json(manifest) == raw, "manifest is not canonical JSON")
    require(
        manifest.get("schema")
        == "gamma-theta-order13-k3-constructor-package-v1"
        and manifest.get("schema_version") == 1
        and manifest.get("template") == "hole9"
        and manifest.get("order") == 13
        and manifest.get("parameter") == 3,
        "manifest identity differs",
    )
    require(
        manifest.get("graph_variable_semantics")
        == "edge variables encode H=complement(G)"
        and manifest.get("fixed_independent_triple_in_g") == [0, 1, 9]
        and manifest.get("heuristic_symmetry_breakers") == [],
        "manifest semantics differ",
    )
    expected_counts = {
        "variable_count": 9802,
        "clause_count": 32108,
        "literal_count": 281028,
        "base_clause_count": 29813,
        "base_literal_count": 227028,
        "coloring_row_count": 2295,
    }
    require(
        all(manifest.get(key) == value for key, value in expected_counts.items()),
        "manifest formula census differs",
    )
    artifacts = manifest.get("artifacts")
    require(type(artifacts) is dict, "manifest artifact bindings are absent")
    require(
        artifacts.get("instance.cnf")
        == {
            "sha256": instance_record["sha256"],
            "size_bytes": instance_record["size_bytes"],
        }
        and artifacts.get("coloring-bank.json")
        == {
            "sha256": bank_record["sha256"],
            "size_bytes": bank_record["size_bytes"],
        },
        "manifest artifact bindings differ",
    )
    pilot = manifest.get("frozen_pilot_match")
    require(
        pilot
        == {
            "expected_sha256": instance_record["sha256"],
            "expected_size_bytes": instance_record["size_bytes"],
            "matched": True,
        },
        "frozen-pilot binding differs",
    )
    source_records = manifest.get("runtime_sources")
    require(type(source_records) is list, "runtime sources are absent")
    source_tuples = []
    for record in source_records:
        require(type(record) is dict, "runtime source record is malformed")
        relative = record.get("path")
        require(type(relative) is str, "runtime source path is malformed")
        payload = regular_file_bytes(ROOT / relative, f"runtime source {relative}")
        require(
            record.get("sha256") == sha256(payload)
            and record.get("size_bytes") == len(payload),
            f"runtime source differs: {relative}",
        )
        source_tuples.append((relative, sha256(payload), len(payload)))
    source_payload = "".join(
        f"{relative} {digest} {size}\n"
        for relative, digest, size in source_tuples
    ).encode("ascii")
    source_set = sha256(source_payload)
    require(
        source_set == EXPECTED_SOURCE_SET_SHA256
        and manifest.get("runtime_source_set_sha256") == source_set,
        "runtime source-set binding differs",
    )
    families = manifest.get("clause_families")
    require(type(families) is dict and len(families) == 14, "families differ")
    family_clauses = sum(record["clauses"] for record in families.values())
    family_literals = sum(record["literals"] for record in families.values())
    require(
        family_clauses == 32108 and family_literals == 281028,
        "clause-family totals differ",
    )
    return {
        "base_clauses": expected_counts["base_clause_count"],
        "base_literals": expected_counts["base_literal_count"],
        "clause_families": len(families),
        "fixed_independent_triple_in_g": [0, 1, 9],
        "runtime_source_set_sha256": source_set,
    }


def validate_acceptance(
    raw: bytes,
    *,
    records: dict[str, dict[str, object]],
) -> dict[str, object]:
    require(
        (len(raw), sha256(raw)) == EXPECTED_ACCEPTANCE,
        "frozen constructor-acceptance evidence binding differs",
    )
    evidence = strict_json(raw, "constructor acceptance evidence")
    require(type(evidence) is dict, "acceptance evidence is not an object")
    require(canonical_json(evidence) == raw, "acceptance evidence is noncanonical")
    require(
        evidence.get("verdict")
        == "ACCEPT_CONSTRUCTOR_A_FOR_PROOF_PRODUCTION_INPUTS"
        and evidence.get("solver_launched") is False
        and evidence.get("source_bindings_stable_pre_post") is True,
        "global constructor acceptance differs",
    )
    templates = evidence.get("templates")
    require(type(templates) is list, "accepted template records are absent")
    hole9 = next(
        (
            record
            for record in templates
            if type(record) is dict and record.get("template") == "hole9"
        ),
        None,
    )
    require(type(hole9) is dict, "accepted hole9 record is absent")
    expected = {
        "variables": 9802,
        "clauses": 32108,
        "literals": 281028,
        "size_bytes": records["instance.cnf"]["size_bytes"],
        "sha256": records["instance.cnf"]["sha256"],
        "bank_rows": 2295,
        "bank_sha256": records["coloring-bank.json"]["sha256"],
        "manifest_sha256": records["constructor-manifest.json"]["sha256"],
        "fixed_independent_triple": [0, 1, 9],
        "constructor_a_exhaustive_audit": True,
        "constructor_b_byte_identical": True,
        "clause_family_names_counts_stream_hashes_match_b": True,
        "complete_coloring_coverage": True,
        "package_entries_exclusive": True,
    }
    require(
        all(hole9.get(key) == value for key, value in expected.items()),
        "live package differs from accepted hole9 record",
    )
    tests = evidence.get("warnings_fatal_test_suite")
    require(
        type(tests) is dict
        and tests.get("passed") is True
        and tests.get("tests_run") == 7,
        "accepted focused-test record differs",
    )
    return {
        "evidence_sha256": EXPECTED_ACCEPTANCE[1],
        "evidence_size_bytes": EXPECTED_ACCEPTANCE[0],
        "hole9_record_exact": True,
        "verdict": evidence["verdict"],
        "warnings_fatal_tests": 7,
    }


def main() -> None:
    artifacts, package_set = package_bindings()
    by_name = {record["name"]: record for record in artifacts}

    instance_raw = regular_file_bytes(PACKAGE / "instance.cnf", "instance")
    variables, clauses, literals = parse_dimacs(instance_raw)
    require(
        (variables, clauses, literals) == (9802, 32108, 281028),
        "parsed formula census differs",
    )

    bank_raw = regular_file_bytes(PACKAGE / "coloring-bank.json", "bank")
    bank = strict_json(bank_raw, "coloring bank")
    require(type(bank) is list and len(bank) == 2295, "bank row count differs")

    manifest_raw = regular_file_bytes(
        PACKAGE / "constructor-manifest.json", "manifest"
    )
    manifest_summary = validate_manifest(
        manifest_raw,
        instance_record=by_name["instance.cnf"],
        bank_record=by_name["coloring-bank.json"],
    )
    acceptance_summary = validate_acceptance(
        regular_file_bytes(ACCEPTANCE, "acceptance evidence"),
        records=by_name,
    )

    print(
        json.dumps(
            {
                "acceptance_comparison": acceptance_summary,
                "artifacts": artifacts,
                "bank": {
                    "rows": len(bank),
                    "sha256": by_name["coloring-bank.json"]["sha256"],
                    "size_bytes": by_name["coloring-bank.json"]["size_bytes"],
                },
                "claim_boundary": (
                    "Read-only constructor preflight. No solver was launched "
                    "and no SAT, UNSAT, or finite-exclusion claim is made."
                ),
                "formula": {
                    "base_clauses": manifest_summary["base_clauses"],
                    "base_literals": manifest_summary["base_literals"],
                    "clauses": clauses,
                    "literals": literals,
                    "sha256": by_name["instance.cnf"]["sha256"],
                    "size_bytes": by_name["instance.cnf"]["size_bytes"],
                    "variables": variables,
                },
                "manifest": {
                    "clause_families": manifest_summary["clause_families"],
                    "fixed_independent_triple_in_g": (
                        manifest_summary["fixed_independent_triple_in_g"]
                    ),
                    "runtime_source_set_sha256": (
                        manifest_summary["runtime_source_set_sha256"]
                    ),
                    "sha256": by_name["constructor-manifest.json"]["sha256"],
                    "size_bytes": (
                        by_name["constructor-manifest.json"]["size_bytes"]
                    ),
                },
                "package": {
                    "entries": [record["name"] for record in artifacts],
                    "package_set_hash_convention": (
                        "SHA256 of sorted ASCII lines: "
                        "name SP sha256 SP size_bytes LF"
                    ),
                    "package_set_sha256": package_set,
                    "path": "instances/order13_k3_hole9",
                    "total_size_bytes": sum(
                        int(record["size_bytes"]) for record in artifacts
                    ),
                },
                "schema": (
                    "gamma-theta-order13-k3-hole9-live-preflight-v1"
                ),
                "solver_launched": False,
                "verdict": "ACCEPT_LIVE_HOLE9_PACKAGE_PREFLIGHT",
            },
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
