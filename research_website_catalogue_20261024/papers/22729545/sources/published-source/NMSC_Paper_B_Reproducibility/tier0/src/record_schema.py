"""Shared deterministic record construction and strict schema validation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "nmsc-local-certificate-v3"
STATUSES = {"PASS", "BLOCKING", "INCONCLUSIVE"}
REQUIRED = {
    "schema_version",
    "job",
    "case_id",
    "input_hash",
    "status",
    "exact_witness",
    "declared_quotient_orbit",
    "notes",
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def make_record(
    *,
    job: str,
    case_input: Any,
    status: str,
    exact_witness: Any,
    graph: Any = None,
    system: Any = None,
    declared_quotient_orbit: Any = None,
    notes: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if status not in STATUSES:
        raise ValueError(f"invalid status {status!r}")
    if (graph is None) == (system is None):
        raise ValueError("exactly one of graph or system must be supplied")
    input_hash = digest(case_input)
    record = {
        "schema_version": SCHEMA_VERSION,
        "job": job,
        "case_id": input_hash[:24],
        "input_hash": input_hash,
        "status": status,
        "graph": graph,
        "system": system,
        "exact_witness": exact_witness,
        "declared_quotient_orbit": declared_quotient_orbit,
        "notes": notes,
    }
    if extra:
        overlap = set(record).intersection(extra)
        if overlap:
            raise ValueError(f"extra fields overwrite schema fields: {sorted(overlap)}")
        record.update(extra)
    validate_record(record)
    return record


def validate_record(record: dict[str, Any], expected_job: str | None = None) -> None:
    missing = REQUIRED.difference(record)
    if missing:
        raise ValueError(f"record missing fields: {sorted(missing)}")
    if record["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unexpected schema {record['schema_version']!r}")
    if record["status"] not in STATUSES:
        raise ValueError(f"invalid status {record['status']!r}")
    if expected_job is not None and record["job"] != expected_job:
        raise ValueError(
            f"expected job {expected_job!r}, found {record['job']!r}"
        )
    if not isinstance(record["job"], str) or not record["job"].strip():
        raise ValueError("job must be a nonempty string")
    if not isinstance(record["notes"], str) or not record["notes"].strip():
        raise ValueError("notes must be nonempty")
    if record.get("graph") is None and record.get("system") is None:
        raise ValueError("record needs graph or system replay input")
    if record.get("graph") is not None and record.get("system") is not None:
        raise ValueError("record cannot contain both graph and system inputs")
    replay_input = record.get("graph") if record.get("graph") is not None else record.get("system")
    if not isinstance(replay_input, dict) or not replay_input:
        raise ValueError("graph/system replay input must be a nonempty object")
    if not isinstance(record["exact_witness"], dict) or not record["exact_witness"]:
        raise ValueError("exact_witness must be a nonempty object")
    if not isinstance(record["input_hash"], str) or len(record["input_hash"]) != 64:
        raise ValueError("input_hash must be one SHA-256 hex digest")
    try:
        int(record["input_hash"], 16)
    except ValueError as error:
        raise ValueError("input_hash must be hexadecimal") from error
    if not isinstance(record["case_id"], str) or len(record["case_id"]) != 24:
        raise ValueError("case_id must be a 24-character string")
    if record["case_id"] != record["input_hash"][:24]:
        raise ValueError("case_id must be the input-hash prefix")


def load_records(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    text = path.read_text()
    if path.suffix == ".jsonl":
        records = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        payload = json.loads(text)
        records = payload if isinstance(payload, list) else [payload]
    return records


def validate_output(
    path: str | Path,
    *,
    expected_job: str,
    minimum_records: int = 1,
) -> list[dict[str, Any]]:
    records = load_records(path)
    if len(records) < minimum_records:
        raise ValueError(
            f"{path} has {len(records)} records; expected at least {minimum_records}"
        )
    for record in records:
        validate_record(record, expected_job)
    if any(record["status"] != "PASS" for record in records):
        raise ValueError(f"{path} contains non-PASS records")
    return records


def write_json_record(path: str | Path, record: dict[str, Any]) -> None:
    validate_record(record)
    Path(path).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")


def write_jsonl(path: str | Path, records: Iterable[dict[str, Any]]) -> int:
    materialized = list(records)
    if not materialized:
        raise ValueError("refusing to write empty certificate stream")
    for record in materialized:
        validate_record(record)
    Path(path).write_text(
        "\n".join(json.dumps(record, sort_keys=True) for record in materialized) + "\n"
    )
    return len(materialized)
