#!/usr/bin/env python3
"""Adversarial tests for the printed authority/hash semantic gate."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from audit_article_sources import (
    AuditFailure,
    audit_printed_authority_hashes,
    canonical_hash,
    require,
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> dict[str, object]:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
    with tempfile.TemporaryDirectory(prefix="k2p-printed-hash-gate-") as raw:
        project = Path(raw)
        first_relative = "evidence/first.json"
        second_relative = "submission/second.json"
        first_bytes = b'{"certificate":"first"}\n'
        second_bytes = b'{"certificate":"second"}\n'
        for relative, data in (
            (first_relative, first_bytes),
            (second_relative, second_bytes),
        ):
            path = project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

        first_hash = digest(first_bytes)
        second_hash = digest(second_bytes)
        metadata_paths = {
            first_relative: "authority",
            second_relative: "reader derivative",
        }
        frozen_anchors = {
            "first frozen row": first_relative,
            "second frozen row": second_relative,
        }
        first_metadata = (
            f"authority: \\path{{{first_relative}}}; "
            f"SHA-256: \\hashvalue{{{first_hash}}}"
        )
        second_metadata = (
            f"reader derivative: \\path{{{second_relative}}}; "
            f"SHA-256: \\hashvalue{{{second_hash}}}"
        )
        first_anchor = (
            "first frozen row\n"
            f"& \\hashvalue{{{first_hash}}}\\\\"
        )
        second_anchor = (
            "second frozen row\n"
            f"& \\hashvalue{{{second_hash}}}\\\\"
        )
        source = "\n".join(
            (
                first_metadata,
                second_metadata,
                r"\section{Frozen hash anchors}\label{sec:hashes}",
                r"\begin{longtable}{ll}",
                first_anchor,
                second_anchor,
                r"\end{longtable}",
                r"\section{Next section}",
            )
        )

        baseline = audit_printed_authority_hashes(
            project,
            source,
            metadata_paths=metadata_paths,
            frozen_anchors=frozen_anchors,
        )
        require(
            baseline["status"] == "PASS"
            and baseline["metadata_rows"] == 2
            and baseline["frozen_anchor_rows"] == 2
            and baseline["rows_checked"] == 4,
            "PRINTED_HASH_GATE_BASELINE_FAILED",
        )

        cases: list[dict[str, str]] = []

        def reject(name: str, mutant: str, expected: str) -> None:
            try:
                audit_printed_authority_hashes(
                    project,
                    mutant,
                    metadata_paths=metadata_paths,
                    frozen_anchors=frozen_anchors,
                )
            except AuditFailure as exc:
                observed = str(exc)
                require(
                    observed.startswith(expected),
                    f"MUTATION_WRONG_REJECTION:{name}:"
                    f"expected={expected}:observed={observed}",
                )
                cases.append(
                    {"name": name, "expected": expected, "observed": observed}
                )
                return
            raise AuditFailure(f"PRINTED_HASH_MUTATION_SURVIVED:{name}")

        reject(
            "stale_metadata_hash",
            source.replace(first_metadata, first_metadata.replace(first_hash, "0" * 64)),
            "PRINTED_HASH_STALE:metadata:",
        )
        reject(
            "stale_frozen_anchor_hash",
            source.replace(first_anchor, first_anchor.replace(first_hash, "0" * 64)),
            "PRINTED_HASH_STALE:frozen-anchor:",
        )
        reject(
            "missing_metadata_row",
            source.replace(first_metadata + "\n", "", 1),
            "PRINTED_METADATA_INVENTORY_DRIFT:",
        )
        reject(
            "duplicate_metadata_row",
            source.replace(
                second_metadata + "\n",
                second_metadata + "\n" + first_metadata + "\n",
                1,
            ),
            "PRINTED_METADATA_DUPLICATE_PATH:",
        )
        reject(
            "metadata_kind_reassigned",
            source.replace("authority: \\path", "reader derivative: \\path", 1),
            "PRINTED_METADATA_KIND_DRIFT:",
        )
        reject(
            "missing_frozen_anchor_row",
            source.replace(first_anchor + "\n", "", 1),
            "PRINTED_FROZEN_ANCHOR_INVENTORY_DRIFT:",
        )
        reject(
            "duplicate_frozen_anchor_row",
            source.replace(
                second_anchor + "\n",
                second_anchor + "\n" + first_anchor + "\n",
                1,
            ),
            "PRINTED_FROZEN_ANCHOR_DUPLICATE_LABEL:",
        )
        extra_anchor = "unexpected row\n" + f"& \\hashvalue{{{first_hash}}}\\\\"
        reject(
            "unexpected_frozen_anchor_row",
            source.replace(second_anchor, second_anchor + "\n" + extra_anchor, 1),
            "PRINTED_FROZEN_ANCHOR_INVENTORY_DRIFT:",
        )

        (project / second_relative).unlink()
        reject(
            "missing_hash_target",
            source,
            "PRINTED_HASH_TARGET_MISSING_OR_SYMBOLIC:",
        )

    result: dict[str, object] = {
        "schema": "k2p-printed-authority-hash-gate-mutations-v1",
        "status": "PASS",
        "baseline_rows_checked": 4,
        "case_count": len(cases),
        "survived": 0,
        "cases": cases,
    }
    result["payload_sha256"] = canonical_hash(result)
    return result


if __name__ == "__main__":
    try:
        require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
        report = main()
        print(json.dumps(report, indent=2, sort_keys=True))
    except AuditFailure as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        raise SystemExit(1) from exc
