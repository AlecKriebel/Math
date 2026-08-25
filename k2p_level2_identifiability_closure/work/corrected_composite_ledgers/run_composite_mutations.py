#!/usr/bin/env python3
"""Verifier-facing mutations for the corrected primitive-composite ledgers.

Every semantic case streams a complete deterministic gzip ledger into scratch,
changes only the declared row occurrence, and invokes the production independent
verifier on that disposable ledger. Optimized-mode refusal and aggregate source
immutability are retained as separate non-ledger gates.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from composite_support import ARTIFACTS, HERE, PROJECT, canonical_bytes, sha_file, sha_object


TOTALS = {"raw4": 405_216, "theta2": 2_946_240}
EXPECTED_TEST_COUNTS = {"raw4": 14, "theta2": 12}


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise RuntimeError(code if detail is None else f"{code}:{detail}")


def source_fingerprints(paths: dict[str, Path]) -> dict[str, str]:
    return {role: sha_file(path) for role, path in sorted(paths.items())}


def diagnostic_line(output: str, marker: str) -> str:
    lines = [line.strip() for line in output.splitlines() if marker in line]
    return lines[-1] if lines else ""


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    """Replace one lexical output entry without following its final link."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.tmp-",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fchmod(handle.fileno(), 0o644)
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory_fd = os.open(path.parent, flags)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def registry_degree_map(path: Path) -> dict[str, int]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        registry = json.load(handle)
    result: dict[str, int] = {}
    for item in registry["rows"]:
        certificate = item["terminal_certificate"]
        if certificate.get("kind") == "exact_direct_polynomial_separator":
            result[item["certificate_binding_sha256"]] = int(certificate["degree"])
    require({3, 4, 5} <= set(result.values()), "DIRECT_DEGREE_REGISTRY_INCOMPLETE")
    return result


def load_exemplars(family: str, ledger: Path) -> dict[str, Any]:
    """Read the frozen stream once and choose deterministic valid alternatives."""

    first: dict[str, tuple[int, dict[str, Any]]] = {}
    quartet_rows: list[tuple[int, dict[str, Any]]] = []
    restoration_rows: list[tuple[int, dict[str, Any]]] = []
    restoration_parent_alternative: tuple[int, dict[str, Any]] | None = None
    restoration_transport_alternative: tuple[int, dict[str, Any]] | None = None
    quadratic_rows: list[tuple[int, dict[str, Any]]] = []
    isomorphism_rows: list[tuple[int, dict[str, Any]]] = []
    direct_by_degree: dict[int, tuple[int, dict[str, Any]]] = {}
    degree_map = (
        registry_degree_map(ARTIFACTS / "raw4_terminal_certificate_registry.json.gz")
        if family == "raw4"
        else {}
    )

    with gzip.open(ledger, "rt", encoding="utf-8") as handle:
        for ordinal, line in enumerate(handle):
            row = json.loads(line)
            require(row.get("raw_id") == ordinal, "SOURCE_RAW_ID_ORDER", ordinal)
            category = row["corrected_category"]
            first.setdefault(category, (ordinal, row))
            if category == "displayed_quartet_exclusion":
                if (
                    len(quartet_rows) < 2
                    and (
                        not quartet_rows
                        or row["evidence_binding"]
                        != quartet_rows[0][1]["evidence_binding"]
                    )
                ):
                    quartet_rows.append((ordinal, row))
            elif category == "restoration_member_presentation":
                if not restoration_rows:
                    restoration_rows.append((ordinal, row))
                else:
                    base_evidence = restoration_rows[0][1]["evidence_binding"]
                    if (
                        restoration_parent_alternative is None
                        and row["evidence_binding"]["restoration_parent_id"]
                        != base_evidence["restoration_parent_id"]
                    ):
                        restoration_parent_alternative = (ordinal, row)
                    if (
                        restoration_transport_alternative is None
                        and row["evidence_binding"]["presentation_transport_sha256"]
                        != base_evidence["presentation_transport_sha256"]
                    ):
                        restoration_transport_alternative = (ordinal, row)
            elif category == "direct_terminal_presentation":
                binding = row["evidence_binding"][
                    "terminal_certificate_binding_sha256"
                ]
                degree = degree_map.get(binding)
                if degree is not None:
                    direct_by_degree.setdefault(degree, (ordinal, row))
            elif category == "direct_quadratic_separator":
                if (
                    len(quadratic_rows) < 2
                    and (
                        not quadratic_rows
                        or row["evidence_binding"]["certificate_id"]
                        != quadratic_rows[0][1]["evidence_binding"]["certificate_id"]
                    )
                ):
                    quadratic_rows.append((ordinal, row))
            elif category == "labelled_isomorphism":
                evidence = row["evidence_binding"]
                if (
                    len(isomorphism_rows) < 2
                    and (
                        not isomorphism_rows
                        or evidence["mixed_vertex_mapping_sha256"]
                        != isomorphism_rows[0][1]["evidence_binding"][
                            "mixed_vertex_mapping_sha256"
                        ]
                    )
                ):
                    isomorphism_rows.append((ordinal, row))

            if family == "raw4":
                complete = (
                    len(first) == 5
                    and len(quartet_rows) == 2
                    and len(restoration_rows) == 1
                    and restoration_parent_alternative is not None
                    and restoration_transport_alternative is not None
                    and {3, 4, 5} <= set(direct_by_degree)
                )
            else:
                complete = (
                    len(first) == 5
                    and len(quartet_rows) == 2
                    and len(quadratic_rows) == 2
                    and len(isomorphism_rows) == 2
                    and any(
                        "physical_restoration_descendants"
                        in item["evidence_binding"]
                        for _, item in isomorphism_rows
                    )
                )
            if complete:
                break

    require(len(first) == 5, "SAMPLE_CATEGORY_CENSUS", len(first))
    require(len(quartet_rows) >= 2, "QUARTET_ALTERNATIVE_MISSING")
    if family == "raw4":
        require(len(restoration_rows) == 1, "RESTORATION_EXEMPLAR_MISSING")
        require(
            restoration_parent_alternative is not None,
            "RESTORATION_PARENT_ALTERNATIVE_MISSING",
        )
        require(
            restoration_transport_alternative is not None,
            "RESTORATION_TRANSPORT_ALTERNATIVE_MISSING",
        )
        require(
            {3, 4, 5} <= set(direct_by_degree),
            "DIRECT_DEGREE_EXEMPLAR_MISSING",
        )
    else:
        require(len(quadratic_rows) >= 2, "QUADRATIC_ALTERNATIVE_MISSING")
        require(
            len(isomorphism_rows) >= 2,
            "ISOMORPHISM_TRANSPORT_ALTERNATIVE_MISSING",
        )
        require(
            any(
                "physical_restoration_descendants" in row["evidence_binding"]
                for _, row in isomorphism_rows
            ),
            "RESTORATION_DESCENDANT_BINDING_MISSING",
        )
    return {
        "first": first,
        "quartet_rows": quartet_rows,
        "restoration_rows": restoration_rows,
        "restoration_parent_alternative": restoration_parent_alternative,
        "restoration_transport_alternative": restoration_transport_alternative,
        "direct_by_degree": direct_by_degree,
        "quadratic_rows": quadratic_rows,
        "isomorphism_rows": isomorphism_rows,
    }


RowAction = Callable[[dict[str, Any]], dict[str, Any]]


def rewrite_complete_mutant(
    source: Path,
    destination: Path,
    *,
    expected_total: int,
    target_raw_id: int,
    mode: str,
    action: RowAction | None = None,
) -> dict[str, int]:
    """Stream the entire source into one deterministic disposable mutant."""

    require(mode in {"change", "omit", "duplicate"}, "MUTATION_MODE", mode)
    input_rows = output_rows = changed_rows = deleted_rows = inserted_rows = 0
    found = False
    with gzip.open(source, "rb") as incoming:
        with destination.open("wb") as raw_output:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                fileobj=raw_output,
                mtime=0,
                compresslevel=6,
            ) as outgoing:
                for ordinal, line in enumerate(incoming):
                    input_rows += 1
                    if ordinal != target_raw_id:
                        outgoing.write(line)
                        output_rows += 1
                        continue
                    found = True
                    require(line.endswith(b"\n"), "SOURCE_LINE_ENDING", ordinal)
                    if mode == "omit":
                        deleted_rows += 1
                        continue
                    if mode == "duplicate":
                        outgoing.write(line)
                        outgoing.write(line)
                        output_rows += 2
                        inserted_rows += 1
                        continue
                    require(action is not None, "CHANGE_ACTION_MISSING")
                    row = json.loads(line)
                    candidate = action(copy.deepcopy(row))
                    require(candidate != row, "MUTATION_NO_OP", target_raw_id)
                    outgoing.write(canonical_bytes(candidate) + b"\n")
                    output_rows += 1
                    changed_rows += 1
    require(found, "MUTATION_TARGET_NOT_FOUND", target_raw_id)
    require(input_rows == expected_total, "SOURCE_ROW_CENSUS", input_rows)
    return {
        "input_rows": input_rows,
        "output_rows": output_rows,
        "changed_rows": changed_rows,
        "deleted_rows": deleted_rows,
        "inserted_rows": inserted_rows,
    }


def changed(action: Callable[[dict[str, Any]], None]) -> RowAction:
    def transform(row: dict[str, Any]) -> dict[str, Any]:
        action(row)
        return row

    return transform


def semantic_specs(family: str, exemplars: dict[str, Any]) -> list[dict[str, Any]]:
    first = exemplars["first"]
    quartet, alternate_quartet = exemplars["quartet_rows"][:2]
    rank = first["exact_rank_exclusion"]
    specs: list[dict[str, Any]] = [
        {
            "name": "omitted_raw_row",
            "gate": "dense_raw_id_count",
            "raw_id": 0,
            "mode": "omit",
            "expected": "RAW_ID_ORDER:0",
        },
        {
            "name": "duplicate_raw_id",
            "gate": "raw_id_uniqueness",
            "raw_id": 0,
            "mode": "duplicate",
            "expected": "RAW_ID_ORDER:1",
        },
        {
            "name": "wrong_port_permutation",
            "gate": "physical_port_permutation",
            "raw_id": quartet[0],
            "mode": "change",
            "action": changed(
                lambda row: row["port_permutation"].__setitem__(
                    slice(0, 2),
                    [row["port_permutation"][1], row["port_permutation"][0]],
                )
            ),
            "expected": f"PORT_PERMUTATION:{quartet[0]}",
        },
        {
            "name": "reassigned_category",
            "gate": "category_partition",
            "raw_id": quartet[0],
            "mode": "change",
            "action": changed(
                lambda row: row.__setitem__(
                    "corrected_category", "exact_rank_exclusion"
                )
            ),
            "expected": f"QUARTET_CATEGORY:{quartet[0]}",
        },
        {
            "name": "reassigned_evidence_binding",
            "gate": "exact_evidence_binding",
            "raw_id": quartet[0],
            "mode": "change",
            "action": changed(
                lambda row, evidence=alternate_quartet[1][
                    "evidence_binding"
                ]: row.__setitem__("evidence_binding", copy.deepcopy(evidence))
            ),
            "expected": f"QUARTET_WITNESS:{quartet[0]}",
        },
        {
            "name": "false_rank_exclusion",
            "gate": "directed_source_lower_target_upper_rank",
            "raw_id": rank[0],
            "mode": "change",
            "action": changed(
                lambda row: row["evidence_binding"].__setitem__(
                    "source_exact_rank",
                    row["evidence_binding"]["target_exact_rank"],
                )
            ),
            "expected": (
                f"{'RAW4' if family == 'raw4' else 'THETA2'}_RANK_EVIDENCE:"
                f"{rank[0]}"
            ),
        },
        {
            "name": "rooted_restriction_reintroduction",
            "gate": "forbidden_rooted_token",
            "raw_id": quartet[0],
            "mode": "change",
            "action": changed(
                lambda row: row.__setitem__(
                    "tree_sunlet", "tree_sunlet_REVOKED"
                )
            ),
            "expected": f"FORBIDDEN_ROOTED_TOKEN:{quartet[0]}",
        },
    ]

    if family == "raw4":
        restoration = exemplars["restoration_rows"][0]
        alternate_parent = exemplars["restoration_parent_alternative"]
        alternate_transport = exemplars["restoration_transport_alternative"]
        require(alternate_parent is not None, "RESTORATION_PARENT_ALTERNATIVE_MISSING")
        require(
            alternate_transport is not None,
            "RESTORATION_TRANSPORT_ALTERNATIVE_MISSING",
        )
        specs.extend(
            [
                {
                    "name": "wrong_restoration_parent",
                    "gate": "restoration_parent_identity",
                    "raw_id": restoration[0],
                    "mode": "change",
                    "action": changed(
                        lambda row, parent=alternate_parent[1][
                            "evidence_binding"
                        ]["restoration_parent_id"]: row["evidence_binding"].__setitem__(
                            "restoration_parent_id", parent
                        )
                    ),
                    "expected": f"RAW4_RESTORATION_EVIDENCE:{restoration[0]}",
                },
                {
                    "name": "broken_transport",
                    "gate": "physical_transport_binding",
                    "raw_id": restoration[0],
                    "mode": "change",
                    "action": changed(
                        lambda row, transport=alternate_transport[1][
                            "evidence_binding"
                        ]["presentation_transport_sha256"]: row[
                            "evidence_binding"
                        ].__setitem__("presentation_transport_sha256", transport)
                    ),
                    "expected": f"RAW4_RESTORATION_EVIDENCE:{restoration[0]}",
                },
            ]
        )
        cycle = {3: 4, 4: 5, 5: 3}
        labels = {3: "cubic", 4: "quartic", 5: "quintic"}
        for degree, replacement_degree in cycle.items():
            source = exemplars["direct_by_degree"][degree]
            replacement = exemplars["direct_by_degree"][replacement_degree]
            specs.append(
                {
                    "name": f"reassigned_{labels[degree]}_certificate",
                    "gate": f"direct_{labels[degree]}_certificate_identity",
                    "raw_id": source[0],
                    "mode": "change",
                    "action": changed(
                        lambda row, binding=replacement[1]["evidence_binding"][
                            "terminal_certificate_binding_sha256"
                        ]: row["evidence_binding"].__setitem__(
                            "terminal_certificate_binding_sha256", binding
                        )
                    ),
                    "expected": f"RAW4_TERMINAL_EVIDENCE:{source[0]}",
                }
            )
    else:
        quadratic, alternate_quadratic = exemplars["quadratic_rows"][:2]
        isomorphism, alternate_isomorphism = exemplars["isomorphism_rows"][:2]
        descendant = next(
            row
            for row in exemplars["isomorphism_rows"]
            if "physical_restoration_descendants" in row[1]["evidence_binding"]
        )
        specs.extend(
            [
                {
                    "name": "missing_restoration_child",
                    "gate": "restoration_child_edge_census",
                    "raw_id": descendant[0],
                    "mode": "change",
                    "action": changed(
                        lambda row: row["evidence_binding"][
                            "physical_restoration_descendants"
                        ].__setitem__(
                            "first_child_count",
                            row["evidence_binding"][
                                "physical_restoration_descendants"
                            ]["first_child_count"]
                            - 1,
                        )
                    ),
                    "expected": f"THETA2_ISOMORPHISM_EVIDENCE:{descendant[0]}",
                },
                {
                    "name": "reassigned_quadratic_certificate",
                    "gate": "quadratic_certificate_identity",
                    "raw_id": quadratic[0],
                    "mode": "change",
                    "action": changed(
                        lambda row, certificate_id=alternate_quadratic[1][
                            "evidence_binding"
                        ]["certificate_id"]: row["evidence_binding"].__setitem__(
                            "certificate_id", certificate_id
                        )
                    ),
                    "expected": f"THETA2_QUADRATIC_EVIDENCE:{quadratic[0]}",
                },
                {
                    "name": "broken_transport",
                    "gate": "labelled_transport_identity",
                    "raw_id": isomorphism[0],
                    "mode": "change",
                    "action": changed(
                        lambda row, mapping=alternate_isomorphism[1][
                            "evidence_binding"
                        ]["mixed_vertex_mapping_sha256"]: row[
                            "evidence_binding"
                        ].__setitem__("mixed_vertex_mapping_sha256", mapping)
                    ),
                    "expected": f"THETA2_ISOMORPHISM_EVIDENCE:{isomorphism[0]}",
                },
            ]
        )
    return specs


def invoke_verifier(
    family: str,
    verifier: Path,
    ledger: Path,
    summary: Path,
    report: Path,
    timeout: float,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(verifier),
            "--family",
            family,
            "--ledger",
            str(ledger),
            "--summary",
            str(summary),
            "--report",
            str(report),
            "--skip-heavy-full-map",
        ],
        cwd=PROJECT,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def run_semantic_case(
    family: str,
    spec: dict[str, Any],
    source: Path,
    summary: Path,
    verifier: Path,
    scratch: Path,
    timeout: float,
) -> dict[str, Any]:
    mutant = scratch / "mutant-ledger.jsonl.gz"
    verifier_report = scratch / "unexpected-verifier-report.json"
    mutant.unlink(missing_ok=True)
    verifier_report.unlink(missing_ok=True)
    try:
        diff = rewrite_complete_mutant(
            source,
            mutant,
            expected_total=TOTALS[family],
            target_raw_id=int(spec["raw_id"]),
            mode=str(spec["mode"]),
            action=spec.get("action"),
        )
        mutant_sha256 = sha_file(mutant)
        mutant_bytes = mutant.stat().st_size
        result = invoke_verifier(
            family, verifier, mutant, summary, verifier_report, timeout
        )
        combined = result.stdout + result.stderr
        observed = diagnostic_line(combined, str(spec["expected"]))
        rejected = (
            result.returncode != 0
            and bool(observed)
            and not verifier_report.exists()
        )
        row = {
            "name": spec["name"],
            "gate": spec["gate"],
            "test_type": "complete_disposable_ledger_attack",
            "mutated_raw_ids": [int(spec["raw_id"])],
            "mutation_mode": spec["mode"],
            "mutation_diff": diff,
            "complete_mutant_ledger_created": True,
            "mutated_ledger_bytes": mutant_bytes,
            "mutated_ledger_sha256": mutant_sha256,
            "production_verifier_invoked": True,
            "production_verifier_sha256": sha_file(verifier),
            "verifier_exit_code": result.returncode,
            "expected_semantic_diagnostic": spec["expected"],
            "observed_semantic_diagnostic": observed,
            "semantic_diagnostic_matched": bool(observed),
            "verifier_report_created": verifier_report.exists(),
            "rejected": rejected,
        }
        require(rejected, "SEMANTIC_MUTATION_NOT_REJECTED", spec["name"])
        return row
    finally:
        mutant.unlink(missing_ok=True)
        verifier_report.unlink(missing_ok=True)


def optimized_mode_case(family: str, verifier: Path, timeout: float) -> dict[str, Any]:
    marker = "OPTIMIZED_MODE_FORBIDDEN"
    result = subprocess.run(
        [sys.executable, "-O", "-B", str(verifier), "--family", family],
        cwd=PROJECT,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    observed = diagnostic_line(result.stdout + result.stderr, marker)
    rejected = result.returncode != 0 and bool(observed)
    require(rejected, "OPTIMIZED_MODE_MUTATION_NOT_REJECTED", family)
    return {
        "name": "python_optimized_mode",
        "gate": "optimized_mode_guard",
        "test_type": "optimized_mode_guard",
        "complete_mutant_ledger_created": False,
        "production_verifier_invoked": True,
        "production_verifier_sha256": sha_file(verifier),
        "verifier_exit_code": result.returncode,
        "expected_semantic_diagnostic": marker,
        "observed_semantic_diagnostic": observed,
        "semantic_diagnostic_matched": bool(observed),
        "rejected": rejected,
    }


def source_immutability_case(
    before: dict[str, str], after: dict[str, str]
) -> dict[str, Any]:
    unchanged = before == after
    require(unchanged, "MUTATION_SOURCE_TREE_FINGERPRINT_DRIFT")
    return {
        "name": "source_tree_immutability",
        "gate": "source_fingerprint_immutability",
        "test_type": "aggregate_source_immutability_guard",
        "complete_mutant_ledger_created": False,
        "production_verifier_invoked": False,
        "source_fingerprints_unchanged": unchanged,
        "rejected": unchanged,
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("COMPOSITE_MUTATION_RUNNER_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("raw4", "theta2"), required=True)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    args = parser.parse_args()
    require(args.timeout_seconds > 0, "INVALID_TIMEOUT")
    family = args.family
    ledger = (
        args.ledger
        or ARTIFACTS / f"{family}_corrected_composite_ledger.jsonl.gz"
    ).resolve()
    summary = (
        args.summary
        or ARTIFACTS / f"{family}_corrected_composite_summary.json"
    ).resolve()
    output = Path(os.path.abspath(args.output.expanduser()))
    resolved_output = output.resolve()
    verifier = HERE / "verify_corrected_composites_independent.py"
    source_paths = {
        "ledger": ledger,
        "mutation_runner": Path(__file__).resolve(),
        "summary": summary,
        "verifier": verifier,
    }
    if family == "raw4":
        source_paths["terminal_registry"] = (
            ARTIFACTS / "raw4_terminal_certificate_registry.json.gz"
        )
    require(
        resolved_output not in {path.resolve() for path in source_paths.values()},
        "OUTPUT_COLLIDES_WITH_SOURCE_INPUT",
        output,
    )
    if output.exists():
        require(
            not any(
                os.path.samefile(output, source)
                for source in source_paths.values()
            ),
            "OUTPUT_HARDLINK_COLLIDES_WITH_SOURCE_INPUT",
            output,
        )
    project_root = PROJECT.resolve()
    if output.is_relative_to(PROJECT) or resolved_output.is_relative_to(project_root):
        expected_authoritative = Path(
            os.path.abspath(
                ARTIFACTS / f"{family}_corrected_composite_mutations.json"
            )
        )
        require(
            args.allow_authoritative_output
            and output == expected_authoritative
            and resolved_output == expected_authoritative.resolve()
            and not expected_authoritative.is_symlink(),
            "OUTPUT_MUST_BE_CALLER_OWNED_DISPOSABLE",
            output,
        )
        ancestor = expected_authoritative.parent
        while True:
            require(
                not ancestor.is_symlink(),
                "AUTHORITATIVE_OUTPUT_ANCESTOR_SYMLINK_FORBIDDEN",
                ancestor,
            )
            if ancestor == PROJECT:
                break
            require(
                ancestor != ancestor.parent,
                "AUTHORITATIVE_OUTPUT_PROJECT_ANCESTOR_MISSING",
            )
            ancestor = ancestor.parent
    before = source_fingerprints(source_paths)
    exemplars = load_exemplars(family, ledger)
    specs = semantic_specs(family, exemplars)
    tests: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(
        prefix=f"k2p-{family}-composite-mutations-"
    ) as directory:
        scratch = Path(directory)
        for spec in specs:
            tests.append(
                run_semantic_case(
                    family,
                    spec,
                    ledger,
                    summary,
                    verifier,
                    scratch,
                    args.timeout_seconds,
                )
            )
            print(
                json.dumps(
                    {
                        "family": family,
                        "mutation": spec["name"],
                        "semantic_diagnostic": tests[-1][
                            "observed_semantic_diagnostic"
                        ],
                        "status": "REJECTED",
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        tests.append(optimized_mode_case(family, verifier, args.timeout_seconds))
    after = source_fingerprints(source_paths)
    tests.append(source_immutability_case(before, after))
    survivors = sum(not row["rejected"] for row in tests)
    require(
        len(tests) == EXPECTED_TEST_COUNTS[family],
        "MUTATION_TEST_CENSUS",
        len(tests),
    )
    report = {
        "schema": f"k2p-{family}-corrected-composite-mutations-v2",
        "status": "PASS" if survivors == 0 and before == after else "FAIL",
        "summary_sha256": sha_file(summary),
        "source_ledger_sha256": sha_file(ledger),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "production_verifier_sha256": sha_file(verifier),
        "execution_contract": {
            "semantic_cases_use_complete_disposable_ledgers": True,
            "semantic_cases_invoke_production_verifier": True,
            "semantic_cases_require_nonzero_exit": True,
            "semantic_cases_require_intended_diagnostic": True,
            "scratch_ledgers_deleted_after_each_case": True,
            "absolute_paths_recorded": False,
            "runtime_fields_recorded": False,
        },
        "tests": tests,
        "test_count": len(tests),
        "semantic_ledger_attack_count": len(specs),
        "survivors": survivors,
        "source_tree_drift": 0 if before == after else 1,
        "temporary_copies_only": True,
    }
    report["payload_sha256"] = sha_object(report)
    atomic_write_bytes(
        output,
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    if report["status"] != "PASS":
        raise SystemExit(
            f"COMPOSITE_MUTATION_FAILURE:{family}:{survivors}:{before == after}"
        )
    print(
        json.dumps(
            {
                "family": family,
                "payload_sha256": report["payload_sha256"],
                "semantic_ledger_attacks": len(specs),
                "status": "PASS",
                "tests": len(tests),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
