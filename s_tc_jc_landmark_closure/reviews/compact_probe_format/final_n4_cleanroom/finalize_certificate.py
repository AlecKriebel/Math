#!/usr/bin/env python3
"""Validate and aggregate the four independent shard certificates."""

from __future__ import annotations

from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
CERT = HERE / "certificates"
EXPECTED = [
    "9649b08315dbd5d9dca8b8e4e1892deefe4cecacd81ea6f1880d994e56bd0863",
    "ea0c7181389d4bb73a7a1332ec396f0223cf0e9746efde9f39bc79d3d3029de1",
    "ab678bcbd268ffd704fa79c45ac8a1eb89e2907132eb5e12a99a625cc606ebbd",
    "ffa5658edfaac800da9614fcaf32a576a09d26d6d1449fc89a2ac66efff551d6",
]
VERBOSE_SHA = "7e1c06223a683b888c365b4fa0fbe0568896a3c4e466be9b382f8d0fd7066c7a"


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def logical_rows(path):
    digest = hashlib.sha256(); rows = 0
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            digest.update(raw); rows += 1
    return rows, digest.hexdigest()


def normalized(path):
    return str(path.resolve().relative_to(PROJECT))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    counts = Counter(); stages = Counter(); cursor = 0
    all_bindings = set(); shard_rows = []
    for index, expected in enumerate(EXPECTED):
        path = CERT / f"independent_s{index}.json"
        payload = json.loads(path.read_text())
        require(payload["status"] == "VERIFIED", f"s{index} status")
        require(payload["summary_sha256"] == expected, f"s{index} summary")
        start, stop = map(int, payload["path_range"])
        require(start == cursor and stop >= start, f"s{index} range")
        require(payload["verbose_summary_sha256"] == VERBOSE_SHA,
                f"s{index} verbose binding")
        comparison = payload["semantic_comparison"]
        require(comparison["ordinary_T_cells"] == 0, f"s{index} T cells")
        require(comparison["strict_open_cube_cells"] == 0,
                f"s{index} strict cells")
        relation = payload["normalized_relation_stream"]
        relation_path = PROJECT / relation["path"]
        require(sha(relation_path) == relation["file_sha256"],
                f"s{index} relation file hash")
        records, logical = logical_rows(relation_path)
        require(records == int(relation["records"]), f"s{index} relation count")
        require(logical == relation["sha256"], f"s{index} relation logical hash")
        local_bindings = set()
        with gzip.open(relation_path, "rt") as handle:
            for line in handle:
                row = json.loads(line)
                binding = str(row["verbose_binding_id"])
                require(binding not in local_bindings, f"s{index} duplicate binding")
                local_bindings.add(binding)
                require(row["classification"] in {
                    "generic_polynomial_separation", "labelled_isomorphism"},
                    f"s{index} unexpected classification")
        require(len(local_bindings) == records, f"s{index} binding count")
        require(not (all_bindings & local_bindings), "cross-shard binding duplicate")
        all_bindings.update(local_bindings)
        counts.update(payload["counts"])
        stages.update(comparison["stage_counts"])
        shard_rows.append({
            "shard": f"s{index}", "summary_sha256": expected,
            "path_range": [start, stop], "certificate": normalized(path),
            "certificate_sha256": sha(path),
            "normalized_relation_stream": relation,
        })
        cursor = stop
    require(cursor == 132, "incomplete path inventory")
    require(len(all_bindings) == 168582, "aggregate binding count")
    require(dict(sorted(counts.items())) == {
        "generic_polynomial_separation": 153072,
        "labelled_isomorphism": 15510,
    }, "aggregate classification counts")
    require(dict(sorted(stages.items())) == {
        "A_plus_p": 12906,
        "A_plus_p_plus_q": 155676,
    }, "aggregate stage counts")

    verbose_summary_path = (PROJECT / "primary/certificates/"
                            "probe_extension_theta2_schema3_final_summary.json")
    require(sha(verbose_summary_path) == VERBOSE_SHA, "verbose summary hash")
    verbose_summary = json.loads(verbose_summary_path.read_text())
    require(int(verbose_summary["streams"]["bindings"]["records"]) == 168582,
            "verbose binding declaration")
    verbose_binding_path = PROJECT / verbose_summary["streams"]["bindings"]["path"]
    verbose_ids = set()
    digest = hashlib.sha256(); verbose_count = 0
    with gzip.open(verbose_binding_path, "rb") as handle:
        for raw in handle:
            digest.update(raw); verbose_count += 1
            identifier = str(json.loads(raw)["probe_path_binding_id"])
            require(identifier not in verbose_ids, "duplicate verbose binding")
            verbose_ids.add(identifier)
    require(verbose_count == 168582, "verbose binding count")
    require(digest.hexdigest() ==
            verbose_summary["streams"]["bindings"]["sha256"],
            "verbose logical binding hash")
    require(all_bindings == verbose_ids, "global compact/verbose binding bijection")

    mutation_path = CERT / "mutation_tests.json"
    merger_mutation_path = CERT / "merger_mutations.json"
    merge_path = CERT / "hardened_merge_manifest.json"
    mutation = json.loads(mutation_path.read_text())
    merger_mutation = json.loads(merger_mutation_path.read_text())
    merge = json.loads(merge_path.read_text())
    require(mutation["status"] == "VERIFIED", "semantic mutations")
    require(merger_mutation["status"] == "VERIFIED", "merger mutations")
    require(merge["status"] == "EXACTLY_VERIFIED", "hardened merger")
    require(merge["path_range"] == [0, 132], "merged range")
    require(merge["counts"] == dict(sorted(counts.items())), "merged counts")

    implementation = {}
    for name in ("engine.py", "audit_final_n4.py", "mutation_tests.py",
                 "merger_mutations.py", "finalize_certificate.py"):
        path = HERE / name
        implementation[name] = sha(path)
    payload = {
        "schema": "compact-probe-final-n4-evidence-gate-v1",
        "status": "VERIFIED",
        "scope": (
            "Evidence-format gate for the final complement-normalized n=4 "
            "compact shards; not a global identifiability theorem."
        ),
        "path_inventory_count": 132,
        "path_range": [0, 132],
        "total_relations": 168582,
        "classification_counts": dict(sorted(counts.items())),
        "stage_counts": dict(sorted(stages.items())),
        "verbose_summary": normalized(verbose_summary_path),
        "verbose_summary_sha256": VERBOSE_SHA,
        "verbose_binding_stream_sha256": digest.hexdigest(),
        "global_verbose_binding_bijection": True,
        "shards": shard_rows,
        "hardened_merge_manifest": normalized(merge_path),
        "hardened_merge_manifest_sha256": sha(merge_path),
        "semantic_mutation_certificate": normalized(mutation_path),
        "semantic_mutation_certificate_sha256": sha(mutation_path),
        "merger_mutation_certificate": normalized(merger_mutation_path),
        "merger_mutation_certificate_sha256": sha(merger_mutation_path),
        "independent_implementation_sha256": implementation,
        "limitations": [
            "All 132 n=4 base paths are triangle-free.",
            "ordinary T cells observed: 0.",
            "strict open-cube separation cells observed: 0.",
            "Therefore this gate does not exercise or certify compact encodings for T or strict cases.",
            "This gate certifies the evidence format and exact n=4 shard contents only.",
        ],
    }
    output = CERT / "final_gate_certificate.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": payload["status"],
                      "relations": payload["total_relations"],
                      "counts": payload["classification_counts"],
                      "output": normalized(output),
                      "output_sha256": sha(output)}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FALSE", "error": str(exc)}, sort_keys=True),
              file=sys.stderr)
        raise
