#!/usr/bin/env python3
"""Adversarial semantic and stream mutations for the third math checker."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from edge_toggle_evaluation_checker.audit import (  # noqa: E402
    AuditPaths,
    LedgerRow,
    ThirdAuditError,
    collect_binding,
    generate_record,
    iter_ledger_rows,
    strict_json_loads,
    verify_certificate,
    verify_record,
)


def trace_sha(rounds: object) -> str:
    assert isinstance(rounds, list)
    digest = sha256()
    for round_index, round_ in enumerate(rounds):
        assert isinstance(round_, list)
        for record in round_:
            assert isinstance(record, list) and len(record) == 2
            digest.update(
                json.dumps(
                    [round_index, record[0], record[1]],
                    separators=(",", ":"),
                ).encode("ascii")
                + b"\n"
            )
    return digest.hexdigest()


def expect_rejection(label: str, function: object) -> None:
    try:
        function()  # type: ignore[operator]
    except (ThirdAuditError, ValueError):
        return
    raise AssertionError(f"mutation was accepted: {label}")


def paths() -> AuditPaths:
    return AuditPaths(
        campaign_root=ROOT,
        database=ROOT / "results/checkpoints/edge_toggles.sqlite3",
        checkpoint=ROOT / "results/checkpoints/edge_toggles.json",
        provenance_csv=ROOT / "results/edge_toggles_provenance.csv",
        unique_csv=ROOT / "results/edge_toggles_unique.csv",
        coverage_report=ROOT / "results/edge_toggle_coverage_audit.json",
        certificate=ROOT
        / "results/edge_toggle_third_evaluation_certificates.ndjson",
        report=ROOT / "results/edge_toggle_third_evaluation_audit.json",
    )


def main() -> None:
    started = time.monotonic()
    production = paths()
    binding = collect_binding(production)
    connection = sqlite3.connect(
        production.database.resolve().as_uri() + "?mode=ro&immutable=1",
        uri=True,
    )
    try:
        first_row = next(iter_ledger_rows(connection, production.unique_csv))
        with production.certificate.open("rb") as handle:
            header_line = handle.readline()
            original_line = handle.readline()
        original = json.loads(original_line)
        verify_record(first_row, original)

        missing_deletion = deepcopy(original)
        missing_deletion["deletion_rounds"][0].pop()
        missing_deletion["deletion_trace_sha256"] = trace_sha(
            missing_deletion["deletion_rounds"]
        )
        expect_rejection(
            "complete doomed set with one deletion omitted and digest repaired",
            lambda: verify_record(first_row, missing_deletion),
        )

        occupied_attack = deepcopy(original)
        state = occupied_attack["deletion_rounds"][0][0][0]
        occupied = (state & -state).bit_length() - 1
        occupied_attack["deletion_rounds"][0][0][1] = occupied
        occupied_attack["deletion_trace_sha256"] = trace_sha(
            occupied_attack["deletion_rounds"]
        )
        expect_rejection(
            "occupied attack with digest repaired",
            lambda: verify_record(first_row, occupied_attack),
        )

        nonsimultaneous = deepcopy(original)
        moved = nonsimultaneous["deletion_rounds"][0].pop()
        nonsimultaneous["deletion_rounds"][1].insert(0, moved)
        nonsimultaneous["deletion_trace_sha256"] = trace_sha(
            nonsimultaneous["deletion_rounds"]
        )
        expect_rejection(
            "deletion moved to a later round with digest repaired",
            lambda: verify_record(first_row, nonsimultaneous),
        )

        incomplete_terminal = deepcopy(original)
        incomplete_terminal["deletion_rounds"].pop()
        incomplete_terminal["deletion_trace_sha256"] = trace_sha(
            incomplete_terminal["deletion_rounds"]
        )
        expect_rejection(
            "nonempty terminal fixed point with digest repaired",
            lambda: verify_record(first_row, incomplete_terminal),
        )

        false_blocker = deepcopy(original)
        false_blocker["lower_blockers"][0][1] = (
            false_blocker["lower_blockers"][0][0] & -false_blocker["lower_blockers"][0][0]
        ).bit_length() - 1
        expect_rejection(
            "occupied lower-bound witness",
            lambda: verify_record(first_row, false_blocker),
        )

        wrong_witness = deepcopy(original)
        wrong_witness["dominating_witness_mask"] = 0
        expect_rejection(
            "false domination upper witness",
            lambda: verify_record(first_row, wrong_witness),
        )

        values = list(first_row.values)
        values[16] = "candidate_eternal"
        wrong_category = LedgerRow(first_row.index, tuple(values), first_row.graph)
        expect_rejection(
            "candidate category despite gamma below eternal",
            lambda: generate_record(wrong_category),
        )

        values = list(first_row.values)
        values[12] = values[8]
        values[13] = values[8]
        false_eternal = LedgerRow(first_row.index, tuple(values), first_row.graph)
        expect_rejection(
            "stored eternal value not above proved gamma",
            lambda: generate_record(false_eternal),
        )

        for malformed in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            expect_rejection(
                "strict JSON duplicate/nonfinite value",
                lambda malformed=malformed: strict_json_loads(malformed, "mutation"),
            )

        with tempfile.TemporaryDirectory(prefix="edge-toggle-math-hostile-") as name:
            temporary = Path(name)

            semantic_stream = temporary / "semantic.ndjson"
            semantic_stream.write_bytes(
                header_line
                + json.dumps(
                    missing_deletion,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("ascii")
                + b"\n"
            )
            expect_rejection(
                "stream with repaired-digest semantic mutation",
                lambda: verify_certificate(
                    connection,
                    production.unique_csv,
                    semantic_stream,
                    binding,
                ),
            )

            truncated_stream = temporary / "truncated.ndjson"
            truncated_stream.write_bytes(header_line + original_line)
            expect_rejection(
                "truncated stream",
                lambda: verify_certificate(
                    connection,
                    production.unique_csv,
                    truncated_stream,
                    binding,
                ),
            )

            duplicate_header = temporary / "duplicate-header.ndjson"
            duplicate_header.write_bytes(
                b'{"binding":{},"type":"header","type":"footer"}\n'
            )
            expect_rejection(
                "duplicate-key header",
                lambda: verify_certificate(
                    connection,
                    production.unique_csv,
                    duplicate_header,
                    binding,
                ),
            )

            trailing_stream = temporary / "trailing.ndjson"
            shutil.copyfile(production.certificate, trailing_stream)
            with trailing_stream.open("ab") as handle:
                handle.write(b"\x00")
            expect_rejection(
                "trailing byte after a valid footer",
                lambda: verify_certificate(
                    connection,
                    production.unique_csv,
                    trailing_stream,
                    binding,
                ),
            )
    finally:
        connection.close()

    print(
        json.dumps(
            {
                "status": "all mutations rejected",
                "mutations": 13,
                "wall_seconds": time.monotonic() - started,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
