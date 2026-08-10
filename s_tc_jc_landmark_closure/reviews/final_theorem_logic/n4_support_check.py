#!/usr/bin/env python3
"""Exact audit of the theta-2 four-outgoing minimal-support gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SUPPORT = ROOT / "primary/certificates/support_universe.json"
CORES = ROOT / "primary/certificates/core_universe.json"
BOUNDED = ROOT / "primary/certificates/bounded_atlas_summary.json"

EXPECTED = {
    SUPPORT: "1bc8cdbf26c7db62fe3e315c529d7f3fa24f186f13a4a36060a586a4d066b778",
    CORES: "f7ebe0b0ebc93f58cfa5bc2086f55a518b0ce8774da57667fe4c1f169ff39e10",
    BOUNDED: "dd178e21e2abf84c582c291d5087d1fab090f8f909908534053581c380f0157e",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for path, expected in EXPECTED.items():
        assert digest(path) == expected, f"changed input: {path}"

    support = json.loads(SUPPORT.read_text())
    cores = json.loads(CORES.read_text())
    bounded = json.loads(BOUNDED.read_text())
    records = support["records"]
    minimal = [row for row in records if row["extra_count"] == 0]
    minimal_by_outgoing = {
        str(n): sum(row["outgoing_count"] == n for row in minimal)
        for n in sorted({row["outgoing_count"] for row in minimal})
    }
    assert len(minimal) == 9
    assert minimal_by_outgoing == {"2": 1, "3": 5, "4": 3}

    n3 = [row for row in records if row["outgoing_count"] == 3]
    assert len(n3) == 8
    assert sum(row["extra_count"] == 0 for row in n3) == 5
    assert sum(row["core_id"] == "cycle" and row["extra_count"] == 1 for row in n3) == 3

    theta2_core = next(row for row in cores["cores"] if row["id"] == "theta-2")
    repairs = [set(r) for r in theta2_core["minimum_repairs"]]
    theta2 = [row for row in minimal if row["core_id"] == "theta-2"]
    assert len(theta2) == 3
    assert all(row["outgoing_count"] == 4 and row["support_size"] == 4 for row in theta2)

    deletions = []
    for row_index, row in enumerate(theta2):
        labels = [label for _vertex, label in row["labels"] if label != "INCOMING"]
        assert sum(label.startswith("Q_SINK_") for label in labels) == 2
        assert sum(label.startswith("Q_REPAIR_") for label in labels) == 2
        label_segment = {}
        for segment, word in enumerate(row["words"]):
            for label in word:
                label_segment[label] = segment
        for removed in labels:
            remaining = set(labels) - {removed}
            sinks_complete = sum(label.startswith("Q_SINK_") for label in remaining) == 2
            occupied = {segment for label, segment in label_segment.items() if label in remaining}
            repair_complete = any(repair <= occupied for repair in repairs)
            retains_theta2_strong_core = sinks_complete and repair_complete
            assert not retains_theta2_strong_core
            deletions.append({
                "theta2_minimal_index": row_index,
                "repair_segments": row["repair_segments"],
                "removed_role": removed,
                "sinks_complete": sinks_complete,
                "minimum_repair_complete": repair_complete,
                "retains_theta2_strong_core": retains_theta2_strong_core,
            })

    runs = {run["outgoing"]: run for run in bounded["runs"]}
    run3, run4 = runs[3], runs[4]
    assert run3["source_bases"] == 8
    assert run3["strict_pairs"] == 110
    assert run4["source_bases"] == 50
    assert run4["common_signatures"] == 50
    assert run4["strict_pairs"] == 776
    assert run4["topology_audit"]["common_signatures_also_having_a_nonretaining_presentation"] == 50
    relation_streams = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.glob("primary/certificates/bounded_relations_n*.jsonl.gz")
    )
    assert relation_streams == []

    report = {
        "schema": "theta2-n4-support-gate-v1",
        "status": "EXACTLY_COMPUTED",
        "minimal_support_record_count": len(minimal),
        "minimal_supports_by_outgoing": minimal_by_outgoing,
        "n3_source_record_count": len(n3),
        "n3_minimal_support_count": sum(row["extra_count"] == 0 for row in n3),
        "n3_cycle_plus_one_count": sum(row["core_id"] == "cycle" and row["extra_count"] == 1 for row in n3),
        "theta2_n4_minimal_support_count": len(theta2),
        "theta2_single_deletion_checks": deletions,
        "bounded_n4_candidate_screen": {
            "source_bases": run4["source_bases"],
            "common_signatures": run4["common_signatures"],
            "common_signatures_with_nonretaining_target_presentation": run4["topology_audit"]["common_signatures_also_having_a_nonretaining_presentation"],
            "interpretation": "necessary-candidate screen only; not an overlap theorem"
        },
        "unequal_pair_level_gate": {
            "unequal_necessary_directed_signature_pairs": {
                "outgoing_3": run3["strict_pairs"],
                "outgoing_4": run4["strict_pairs"],
            },
            "active_bounded_relation_streams": relation_streams,
            "status": "UNRESOLVED",
            "reason": "equal-signature restoration does not classify unequal necessary directed pairs",
        },
        "verdict": "N4_FIXED_FULL_HARD_COVER_REQUIRED",
        "reason": "No three-outgoing restriction of a theta-2 minimal support retains both sinks and a minimum repair, so the n=3 fixed-full theorem precondition fails."
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    expected = json.loads((HERE / "n4_support_certificate.json").read_text())
    assert report == expected, "n4 support certificate does not regenerate"


if __name__ == "__main__":
    main()
