#!/usr/bin/env python3
"""Prove that the theta2 composite reseal changes exactly 2,528 evidence leaves."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ARTIFACTS = PROJECT / "work/corrected_composite_ledgers/artifacts"
TRUTH = PROJECT / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json"
LEDGER = ARTIFACTS / "theta2_corrected_composite_ledger.jsonl.gz"
SUMMARY = ARTIFACTS / "theta2_corrected_composite_summary.json"
RAW4_LEDGER = ARTIFACTS / "raw4_corrected_composite_ledger.jsonl.gz"
DEFAULT_OUTPUT = HERE / "composite_reseal_diff_audit.json"
LEGACY_DOMAIN = "0<every edge-sector and inheritance variable<1 (hence D_plus)"
EXPECTED_RAW4_SHA256 = "431dac8898ad2a724d12c200687de1b377723e302214a79a11a03524a4084b96"
EXPECTED_CURRENT_THETA2_SHA256 = "805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659"
EXPECTED_LEGACY_THETA2_SHA256 = "4cbd7b774adccaafc81338ce9093e33f4abcae8d75664c9d4c9ecc582a80cc58"
EXPECTED_LEGACY_STREAM_SHA256 = "230392ee6f2bfb7844246f5700942259142c4b4981827cacd14abbd8bcd1ea39"


class CompositeResealFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        suffix = "" if detail is None else f":{detail}"
        raise CompositeResealFailure(f"{code}{suffix}")


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def pretty_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def legacy_seal_map(truth: dict[str, Any]) -> dict[str, str]:
    records = truth.get("sign_certificates")
    require(isinstance(records, dict) and len(records) == 85, "SIGN_CENSUS_FAIL")
    result: dict[str, str] = {}
    for key in sorted(records):
        sign = records[key].get("sign")
        require(isinstance(sign, dict), "SIGN_PAYLOAD_FAIL", key)
        current = sign.get("certificate_sha256")
        body = {name: value for name, value in sign.items() if name != "certificate_sha256"}
        require(current == sha_object(body), "CURRENT_SIGN_SEAL_FAIL", key)
        legacy = copy.deepcopy(body)
        legacy["domain"] = LEGACY_DOMAIN
        legacy_seal = sha_object(legacy)
        require(isinstance(current, str) and current not in result, "SIGN_SEAL_COLLISION")
        result[current] = legacy_seal
    require(len(set(result.values())) == 85, "LEGACY_SIGN_SEAL_COLLISION")
    return result


def main() -> int:
    if not __debug__:
        raise CompositeResealFailure("COMPOSITE_RESEAL_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    require(sha_file(RAW4_LEDGER) == EXPECTED_RAW4_SHA256, "RAW4_LEDGER_BYTE_DRIFT")
    require(
        sha_file(LEDGER) == EXPECTED_CURRENT_THETA2_SHA256,
        "CURRENT_THETA2_LEDGER_BYTE_DRIFT",
    )
    truth = json.loads(TRUTH.read_text(encoding="utf-8"))
    mapping = legacy_seal_map(truth)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    require(summary.get("ledger_sha256") == EXPECTED_CURRENT_THETA2_SHA256, "SUMMARY_LEDGER_BINDING_FAIL")

    current_stream = hashlib.sha256()
    legacy_stream = hashlib.sha256()
    changed_raw_ids: list[int] = []
    row_count = 0
    with tempfile.TemporaryDirectory(prefix="k2p-composite-reseal-") as directory:
        reconstructed = Path(directory) / "legacy_theta2_composite.jsonl.gz"
        with gzip.open(LEDGER, "rb") as source, reconstructed.open("wb") as raw_output:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                fileobj=raw_output,
                mtime=0,
                compresslevel=6,
            ) as encoded:
                for row_count, line in enumerate(source, 1):
                    current_stream.update(line)
                    legacy_line = line
                    if b'"corrected_category":"full_map_Ti_strict_sign"' in line:
                        row = json.loads(line)
                        evidence = row.get("evidence_binding")
                        require(isinstance(evidence, dict), "EVIDENCE_BINDING_FAIL", row_count)
                        current_seal = evidence.get("coefficient_certificate_sha256")
                        require(current_seal in mapping, "CURRENT_SIGN_SEAL_UNKNOWN", row_count)
                        evidence["coefficient_certificate_sha256"] = mapping[current_seal]
                        legacy_line = canonical_bytes(row) + b"\n"
                        changed_raw_ids.append(row["raw_id"])
                    legacy_stream.update(legacy_line)
                    encoded.write(legacy_line)
        reconstructed_sha256 = sha_file(reconstructed)

    require(row_count == 2_946_240, "ROW_CENSUS_FAIL", row_count)
    require(len(changed_raw_ids) == 2_528, "CHANGED_ROW_CENSUS_FAIL", len(changed_raw_ids))
    require(
        current_stream.hexdigest() == summary.get("uncompressed_stream_sha256"),
        "CURRENT_STREAM_BINDING_FAIL",
    )
    require(
        legacy_stream.hexdigest() == EXPECTED_LEGACY_STREAM_SHA256,
        "LEGACY_STREAM_RECONSTRUCTION_FAIL",
    )
    require(
        reconstructed_sha256 == EXPECTED_LEGACY_THETA2_SHA256,
        "LEGACY_GZIP_RECONSTRUCTION_FAIL",
    )

    report: dict[str, Any] = {
        "schema": "k2p-composite-domain-reseal-diff-audit-v1",
        "status": "PASS",
        "raw4_ledger": {
            "changed_rows": 0,
            "file_sha256": EXPECTED_RAW4_SHA256,
        },
        "theta2_ledger": {
            "total_rows": row_count,
            "changed_rows": len(changed_raw_ids),
            "unchanged_rows": row_count - len(changed_raw_ids),
            "changed_category": "full_map_Ti_strict_sign",
            "changed_leaf_path": "evidence_binding.coefficient_certificate_sha256",
            "changed_raw_id_root": sha_object(changed_raw_ids),
            "current_file_sha256": EXPECTED_CURRENT_THETA2_SHA256,
            "legacy_file_sha256": EXPECTED_LEGACY_THETA2_SHA256,
            "legacy_file_reconstructed_exactly": True,
            "legacy_uncompressed_stream_sha256": EXPECTED_LEGACY_STREAM_SHA256,
        },
        "unresolved": 0,
    }
    report["payload_sha256"] = sha_object(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pretty_bytes(report))
    print(
        json.dumps(
            {
                "status": "PASS",
                "changed_rows": len(changed_raw_ids),
                "payload_sha256": report["payload_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CompositeResealFailure as error:
        raise SystemExit(f"COMPOSITE_RESEAL_FAIL:{error}") from error
