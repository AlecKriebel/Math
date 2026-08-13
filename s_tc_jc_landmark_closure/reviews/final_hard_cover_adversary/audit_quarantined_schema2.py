#!/usr/bin/env python3
"""Preserve and quantify the rooted-provenance merge in schema 2.

The input is the quarantined n=4 theta-2 stream.  This checker deliberately
does not import the primary producer.  It verifies content hashes, then asks
whether every raw coverage in a state has the state's exact fixed root case
and exact rooted source/target graph IDs.  Standard mixed-code agreement is
reported but never accepted as a substitute.
"""

from __future__ import annotations

from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
QUARANTINE = PROJECT / "quarantine/schema2_rooted_merge_failure"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def stable_hash(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path, key: str) -> dict[str, dict]:
    rows = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            identifier = row[key]
            if identifier in rows:
                raise AssertionError(("duplicate", key, identifier))
            rows[identifier] = row
    return rows


def main() -> int:
    state_path = QUARANTINE / "hard_cover_n4_candidate_theta2_full.jsonl.gz"
    graph_path = QUARANTINE / "hard_cover_graphs_n4_candidate_theta2_full.jsonl.gz"
    root_path = QUARANTINE / "hard_cover_root_cases_n4_candidate_theta2_full.jsonl.gz"
    states = load(state_path, "state_id")
    graphs = load(graph_path, "graph_id")
    roots = load(root_path, "root_case_id")

    mismatch_counts = Counter()
    examples = []
    merged_state_counts = Counter()
    for state_id, state in sorted(states.items()):
        root_ids = {coverage["root_case_id"] for coverage in state["raw_coverage"]}
        source_ids = {coverage["source_graph_id"] for coverage in state["raw_coverage"]}
        target_ids = {coverage["target_graph_id"] for coverage in state["raw_coverage"]}
        if len(root_ids) > 1:
            merged_state_counts["multiple_root_case_ids"] += 1
        if len(source_ids) > 1:
            merged_state_counts["multiple_source_graph_ids"] += 1
        if len(target_ids) > 1:
            merged_state_counts["multiple_target_graph_ids"] += 1
        for coverage in state["raw_coverage"]:
            failures = []
            # Schema 2 had no state-level fixed root ID.  A state is invalid
            # under schema 3 whenever its coverages do not all share one.
            if len(root_ids) != 1:
                failures.append("root_case_id")
                mismatch_counts["coverage_in_cross_root_state"] += 1
            if coverage["source_graph_id"] != state["source_graph_id"]:
                failures.append("source_graph_id")
                mismatch_counts["source_graph_id"] += 1
            if coverage["target_graph_id"] != state["target_graph_id"]:
                failures.append("target_graph_id")
                mismatch_counts["target_graph_id"] += 1
            if failures and len(examples) < 40:
                source_state = graphs[state["source_graph_id"]]
                source_coverage = graphs[coverage["source_graph_id"]]
                target_state = graphs[state["target_graph_id"]]
                target_coverage = graphs[coverage["target_graph_id"]]
                examples.append({
                    "state_id": state_id,
                    "path_binding_id": coverage["path_binding_id"],
                    "root_case_id": coverage["root_case_id"],
                    "mismatched_fields": failures,
                    "state_source_graph_id": state["source_graph_id"],
                    "coverage_source_graph_id": coverage["source_graph_id"],
                    "source_standard_mixed_code_equal": (
                        source_state["standard_mixed_code"]
                        == source_coverage["standard_mixed_code"]
                    ),
                    "state_target_graph_id": state["target_graph_id"],
                    "coverage_target_graph_id": coverage["target_graph_id"],
                    "target_standard_mixed_code_equal": (
                        target_state["standard_mixed_code"]
                        == target_coverage["standard_mixed_code"]
                    ),
                })

    malformed_schema2_state_ids = 0
    for state_id, state in states.items():
        source_code = graphs[state["source_graph_id"]]["standard_mixed_code"]
        target_code = graphs[state["target_graph_id"]]["standard_mixed_code"]
        expected = stable_hash({
            "selected_port_count": state["selected_port_count"],
            "source_mixed_code": source_code,
            "target_completion_mixed_code": target_code,
            "remaining_target_roles": state["remaining_target_roles"],
            "port_matching": tuple(range(state["selected_port_count"])),
        })
        malformed_schema2_state_ids += expected != state_id

    failure_count = sum(mismatch_counts.values())
    payload = {
        "schema": "quarantined-schema2-rooted-merge-audit-v1",
        "status": "FALSE",
        "classification": "FALSE AS A FIXED-ROOT DECORATED-RELATION CERTIFICATE",
        "reason": (
            "schema-2 state identity omitted the fixed root case and exact rooted "
            "source/target graph IDs; at least one raw coverage is bound to a "
            "different rooted presentation than its state"
        ),
        "required_replacement_identity": [
            "fixed_full_root_case_id",
            "source_rooted_graph_id",
            "target_rooted_graph_id",
            "selected_port_count",
            "source_mixed_code",
            "target_completion_mixed_code",
            "remaining_target_roles",
            "port_matching",
        ],
        "inputs": {
            str(path.relative_to(PROJECT)): file_sha(path)
            for path in (state_path, graph_path, root_path)
        },
        "counts": {
            "states": len(states),
            "root_cases": len(roots),
            "raw_coverages": sum(len(row["raw_coverage"]) for row in states.values()),
            "schema2_state_id_replay_failures": malformed_schema2_state_ids,
            "rooted_binding_mismatch_events": failure_count,
            "mismatches": dict(sorted(mismatch_counts.items())),
            "merged_states": dict(sorted(merged_state_counts.items())),
        },
        "examples": examples,
        "acceptance_rule": (
            "No state may merge raw coverages across a fixed root case or exact "
            "rooted source/target graph ID, even if standard mixed codes agree. "
            "Every path's child set must be independently regenerated."
        ),
    }
    if failure_count == 0:
        payload["status"] = "UNRESOLVED"
        payload["classification"] = "UNRESOLVED: EXPECTED REGRESSION NOT REPRODUCED"
    output = HERE / "quarantined_schema2_failure.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(canonical_json({
        "status": payload["status"],
        "failure_events": failure_count,
        "merged_states": payload["counts"]["merged_states"],
        "output": str(output),
        "sha256": file_sha(output),
    }))
    return 0 if failure_count else 1


if __name__ == "__main__":
    raise SystemExit(main())
