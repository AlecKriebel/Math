#!/usr/bin/env python3
"""Generate every rigid support, support-plus-one, and support-plus-two source."""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
import hashlib
import json
from pathlib import Path

from completion_universe import build_graph, core_rows, source_and_sinks
from graph_model import canonical_mixed, mixed_local_strong, rooted_validation, sd0


HERE = Path(__file__).resolve().parent
OUT = HERE / "certificates" / "support_universe.json"


def source_records():
    records = {}
    raw = 0
    for core in core_rows():
        arcs = core["arcs"]
        _, sinks = source_and_sinks(arcs)
        for repair_index, repair in enumerate(core["repairs"]):
            # Cycle has two equivalent minimum repairs; retaining both is useful
            # provenance, while the labelled graph canonicalizer removes exact
            # duplicates only after the support role is fixed.
            repair_labels = {arc_index: f"Q_REPAIR_{position}" for position, arc_index in enumerate(repair)}
            sink_labels = {sink: f"Q_SINK_{position}" for position, sink in enumerate(sinks)}
            support_size = len(repair) + len(sinks)
            for extras in range(3):
                for assignments in product(range(len(arcs)), repeat=extras):
                    letters = {index: [] for index in range(len(arcs))}
                    for arc_index, label in repair_labels.items():
                        letters[arc_index].append(label)
                    for extra_index, arc_index in enumerate(assignments):
                        letters[arc_index].append(f"P_{extra_index}")
                    order_choices = [tuple(permutations(values)) if values else ((),) for values in letters.values()]
                    for ordered in product(*order_choices):
                        raw += 1
                        words = tuple(tuple(row) for row in ordered)
                        graph = build_graph(arcs, words, sink_labels)
                        valid, problems = rooted_validation(graph)
                        if not valid:
                            raise AssertionError(problems)
                        mixed = sd0(graph)
                        if not mixed_local_strong(mixed):
                            raise AssertionError("support source is not standard strong")
                        code, transport = canonical_mixed(mixed)
                        key = (core["id"], support_size, extras, code)
                        records.setdefault(key, {
                            "core_id": core["id"],
                            "repair_index": repair_index,
                            "repair_segments": repair,
                            "support_size": support_size,
                            "extra_count": extras,
                            "outgoing_count": support_size + extras,
                            "words": words,
                            "sink_labels": sink_labels,
                            "root": graph.root,
                            "labels": graph.labels,
                            "arcs": graph.arcs,
                            "mixed_code": code,
                            "raw_to_canonical": transport,
                        })
    return raw, tuple(records[key] for key in sorted(records, key=repr))


def main() -> None:
    raw, records = source_records()
    by_outgoing = Counter(row["outgoing_count"] for row in records)
    by_core = Counter(row["core_id"] for row in records)
    # Rigid supports have trivial pointwise stabilizer if no two distinct
    # canonical mixed graphs arise by fixing every Q-labelled port.  This is
    # checked more directly in the relation compiler; record only the finite
    # universe here.
    payload = {
        "schema": 1,
        "raw_presentations": raw,
        "canonical_decorated_support_presentations": len(records),
        "by_outgoing_count": dict(sorted(by_outgoing.items())),
        "by_core": dict(sorted(by_core.items())),
        "records": records,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256_without_hash"] = hashlib.sha256(canonical.encode()).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "output": str(OUT), "raw": raw, "canonical": len(records),
        "by_outgoing": dict(sorted(by_outgoing.items())),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
