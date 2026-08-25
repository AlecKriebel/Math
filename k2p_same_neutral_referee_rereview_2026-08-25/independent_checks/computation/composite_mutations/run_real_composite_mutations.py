#!/usr/bin/env python3
"""Run real disposable mutations against the submitted composite verifier."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable


def canonical(row: object) -> bytes:
    return json.dumps(row, sort_keys=True, separators=(",", ":")).encode()


def rewrite(
    source: Path,
    destination: Path,
    transform: Callable[[int, dict], list[dict]],
) -> None:
    with gzip.open(source, "rt", encoding="utf-8") as reader:
        with destination.open("wb") as raw:
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=6
            ) as writer:
                for number, line in enumerate(reader):
                    row = json.loads(line)
                    for output in transform(number, row):
                        writer.write(canonical(output) + b"\n")


def invoke(project: Path, ledger: Path, output: Path) -> dict:
    verifier = project / "work/corrected_composite_ledgers/verify_corrected_composites_independent.py"
    summary = project / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json"
    qualified_python = project / ".venv/bin/python"
    if not qualified_python.is_file():
        qualified_python = Path(sys.executable)
    command = [
        str(qualified_python),
        "-B",
        str(verifier),
        "--family",
        "raw4",
        "--ledger",
        str(ledger),
        "--summary",
        str(summary),
        "--report",
        str(output),
        "--skip-heavy-full-map",
    ]
    started = time.monotonic()
    result = subprocess.run(
        command,
        cwd=project,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        timeout=300,
    )
    elapsed = time.monotonic() - started
    return {
        "command": command,
        "exit_code": result.returncode,
        "elapsed_seconds": round(elapsed, 6),
        "stdout": result.stdout,
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        "report_created": output.exists(),
    }


def main() -> None:
    suite_started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    root = args.output_root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    source = project / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz"

    registry_path = project / "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
    with gzip.open(registry_path, "rt", encoding="utf-8") as handle:
        registry = json.load(handle)
    semantic_by_binding: dict[str, str] = {}
    for item in registry["rows"]:
        terminal = item["terminal_certificate"]
        if terminal["kind"] == "exact_direct_polynomial_separator":
            semantic = {3: "cubic", 4: "quartic", 5: "quintic"}[terminal["degree"]]
        elif terminal["kind"] == "exact_multihomogeneous_quadratic":
            semantic = "quadratic"
        else:
            semantic = terminal["kind"]
        semantic_by_binding[item["certificate_binding_sha256"]] = semantic

    # Obtain independently valid alternate quartet evidence and direct certificate IDs.
    exemplars: dict[str, tuple[int, dict]] = {}
    quartet_rows: list[tuple[int, dict]] = []
    direct_rows: list[tuple[int, dict]] = []
    direct_by_semantic: dict[str, tuple[int, dict]] = {}
    with gzip.open(source, "rt", encoding="utf-8") as handle:
        for number, line in enumerate(handle):
            row = json.loads(line)
            exemplars.setdefault(row["corrected_category"], (number, row))
            if row["corrected_category"] == "displayed_quartet_exclusion":
                if not quartet_rows or row["evidence_binding"] != quartet_rows[0][1]["evidence_binding"]:
                    quartet_rows.append((number, row))
            if row["corrected_category"] == "direct_terminal_presentation":
                binding = row["evidence_binding"]["terminal_certificate_binding_sha256"]
                semantic = semantic_by_binding[binding]
                direct_by_semantic.setdefault(semantic, (number, row))
                if not direct_rows or binding != direct_rows[0][1]["evidence_binding"]["terminal_certificate_binding_sha256"]:
                    direct_rows.append((number, row))
            if (
                len(exemplars) == 5
                and len(quartet_rows) >= 2
                and len(direct_rows) >= 2
                and {"quadratic", "cubic", "quartic", "quintic"} <= direct_by_semantic.keys()
            ):
                break

    q0, q1 = quartet_rows[:2]
    d0, d1 = direct_rows[:2]
    r0 = exemplars["restoration_member_presentation"]
    rank0 = exemplars["exact_rank_exclusion"]

    cases: list[tuple[str, str, Callable[[int, dict], list[dict]]]] = []

    cases.append((
        "omitted_first_raw_row",
        "RAW_ID_ORDER",
        lambda number, row: [] if number == 0 else [row],
    ))
    cases.append((
        "duplicated_first_raw_row",
        "RAW_ID_ORDER",
        lambda number, row: [row, row] if number == 0 else [row],
    ))

    def wrong_port(number: int, row: dict) -> list[dict]:
        if number == 0:
            row["port_permutation"][0], row["port_permutation"][1] = row["port_permutation"][1], row["port_permutation"][0]
        return [row]

    cases.append(("wrong_physical_port_permutation", "PORT_PERMUTATION", wrong_port))

    def valid_quartet_substitution(number: int, row: dict) -> list[dict]:
        if number == q0[0]:
            row["evidence_binding"] = q1[1]["evidence_binding"]
        return [row]

    cases.append(("valid_quartet_proof_reassigned", "QUARTET_WITNESS", valid_quartet_substitution))

    def false_rank(number: int, row: dict) -> list[dict]:
        if number == rank0[0]:
            row["evidence_binding"]["source_exact_rank"] = row["evidence_binding"]["target_exact_rank"]
        return [row]

    cases.append(("false_rank_exclusion", "RAW4_RANK_EVIDENCE", false_rank))

    def direct_substitution(number: int, row: dict) -> list[dict]:
        if number == d0[0]:
            row["evidence_binding"]["terminal_certificate_binding_sha256"] = d1[1]["evidence_binding"]["terminal_certificate_binding_sha256"]
        return [row]

    cases.append(("valid_direct_certificate_reassigned", "RAW4_TERMINAL_EVIDENCE", direct_substitution))

    degree_cycle = {
        "quadratic": "cubic",
        "cubic": "quartic",
        "quartic": "quintic",
        "quintic": "quadratic",
    }
    for original_semantic, substitute_semantic in degree_cycle.items():
        original_number, _original_row = direct_by_semantic[original_semantic]
        substitute_binding = direct_by_semantic[substitute_semantic][1]["evidence_binding"]["terminal_certificate_binding_sha256"]

        def degree_substitution(
            number: int,
            row: dict,
            *,
            original_number: int = original_number,
            substitute_binding: str = substitute_binding,
        ) -> list[dict]:
            if number == original_number:
                row["evidence_binding"]["terminal_certificate_binding_sha256"] = substitute_binding
            return [row]

        cases.append((
            f"reassigned_{original_semantic}_certificate",
            "RAW4_TERMINAL_EVIDENCE",
            degree_substitution,
        ))

    def wrong_parent(number: int, row: dict) -> list[dict]:
        if number == r0[0]:
            row["evidence_binding"]["restoration_parent_id"] = "source_0:class_999999"
        return [row]

    cases.append(("wrong_restoration_parent", "RAW4_RESTORATION_EVIDENCE", wrong_parent))

    def broken_restoration_transport(number: int, row: dict) -> list[dict]:
        if number == r0[0]:
            row["evidence_binding"]["presentation_transport_sha256"] = "f" * 64
        return [row]

    cases.append(("broken_restoration_transport", "RAW4_RESTORATION_EVIDENCE", broken_restoration_transport))

    results = []
    for name, expected, transform in cases:
        ledger = root / f"{name}.jsonl.gz"
        output = root / f"{name}.report.json"
        rewrite(source, ledger, transform)
        observed = invoke(project, ledger, output)
        intended = observed["exit_code"] != 0 and expected in observed["stdout"]
        results.append({
            "case": name,
            "expected_semantic_marker": expected,
            "rejected_for_intended_reason": intended,
            "mutated_ledger_sha256": hashlib.sha256(ledger.read_bytes()).hexdigest(),
            **{key: value for key, value in observed.items() if key != "stdout"},
            "diagnostic_tail": observed["stdout"][-1200:],
        })

    payload = {
        "schema": "independent-real-composite-mutations-v1",
        "project": str(project),
        "source_ledger_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "case_count": len(results),
        "all_rejected_for_intended_semantic_reason": all(row["rejected_for_intended_reason"] for row in results),
        "cases": results,
        "elapsed_seconds": round(time.monotonic() - suite_started, 6),
    }
    payload["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
    report = root / "real_composite_mutation_report.json"
    report.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(report), "cases": len(results), "all_intended": payload["all_rejected_for_intended_semantic_reason"]}, sort_keys=True))
    if not payload["all_rejected_for_intended_semantic_reason"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
