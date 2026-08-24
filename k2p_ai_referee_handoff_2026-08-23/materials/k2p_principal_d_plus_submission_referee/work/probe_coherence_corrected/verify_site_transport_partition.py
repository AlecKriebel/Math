#!/usr/bin/env python3
"""Independent audit of the exact site-map/Q/T_i partition."""

from __future__ import annotations

import collections
import gzip
import hashlib
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CONTRACT = PROJECT / "work/adversarial_proof_review/probe_input_contract.json"
OUTPUT = HERE / "site_transport_partition_verification.json"


class PartitionFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise PartitionFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def site_id(endpoints):
    return f"E:{sha(endpoints)}"


def main():
    if not __debug__:
        raise PartitionFailure("SITE_PARTITION_OPTIMIZED_MODE_FORBIDDEN")
    started = time.monotonic()
    contract = json.loads(CONTRACT.read_text())
    base_maps = {}
    for anchor in contract["anchors"]:
        mapping = {
            row["source_site_id"]: row["target_site_id"]
            for row in anchor["site_transport"]
        }
        require(len(mapping) == anchor["source_candidate_profile"]["site_count"], f"base site transport:{anchor['anchor_id']}")
        base_maps[anchor["anchor_id"]] = mapping

    one_counts = collections.Counter()
    one_compatible_status = collections.Counter()
    one_incompatible_status = collections.Counter()
    parent_transport_ids = {}
    with gzip.open(HERE / "one_port_ledger.jsonl.gz", "rt") as handle:
        for number, line in enumerate(handle):
            row = json.loads(line)
            compatible = (
                base_maps[row["parent_anchor_id"]].get(row["source_site_id"])
                == row["target_site_id"]
            )
            one_counts["compatible" if compatible else "incompatible"] += 1
            target = one_compatible_status if compatible else one_incompatible_status
            target[row["status"]] += 1
            if compatible:
                require(row["status"] in {"isomorphic", "triangle", "full_map_Ti_strict_sign"}, f"compatible one status:{number}")
            else:
                require(row["status"] == "displayed_quartet_mismatch", f"incompatible one not quartet:{number}")
            if row["status"] in {"isomorphic", "triangle"}:
                parent_id = f"P1:{row['parent_anchor_id']}:{row['source_site_index']}:{row['target_site_index']}"
                parent_transport_ids[parent_id] = row["transport_id"]
    require(one_counts == {"compatible": 2206, "incompatible": 27758}, f"one partition:{one_counts}")
    require(one_compatible_status == {
        "isomorphic": 1915, "triangle": 192, "full_map_Ti_strict_sign": 99,
    }, f"one compatible statuses:{one_compatible_status}")
    require(one_incompatible_status == {"displayed_quartet_mismatch": 27758}, f"one incompatible statuses:{one_incompatible_status}")
    require(len(parent_transport_ids) == 2107, "one equality parent transports")

    needed = set(parent_transport_ids.values())
    transport_site_maps = {}
    with gzip.open(HERE / "exact_transport_ledger.jsonl.gz", "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row["record_id"] not in needed:
                continue
            public = row["record"]
            mapping = {
                site_id(edge_row[0]): site_id(edge_row[1])
                for edge_row in public["mixed_edge_map"]
            }
            require(len(mapping) == len(public["mixed_edge_map"]), f"parent edge-map collision:{row['record_id']}")
            transport_site_maps[row["record_id"]] = mapping
    require(set(transport_site_maps) == needed, "one parent transport registry coverage")

    parent_maps = {
        parent_id: transport_site_maps[transport_id]
        for parent_id, transport_id in parent_transport_ids.items()
    }
    two_counts = collections.Counter()
    two_compatible_status = collections.Counter()
    two_incompatible_status = collections.Counter()
    with gzip.open(HERE / "two_port_ledger.jsonl.gz", "rt") as handle:
        for number, line in enumerate(handle):
            row = json.loads(line)
            compatible = (
                parent_maps[row["one_port_parent_id"]].get(row["second_source_site_id"])
                == row["second_target_site_id"]
            )
            two_counts["compatible" if compatible else "incompatible"] += 1
            target = two_compatible_status if compatible else two_incompatible_status
            target[row["status"]] += 1
            if compatible:
                require(row["status"] in {"isomorphic", "triangle", "full_map_Ti_strict_sign"}, f"compatible two status:{number}")
            else:
                require(row["status"] == "displayed_quartet_mismatch", f"incompatible two not quartet:{number}")
    require(two_counts == {"compatible": 33305, "incompatible": 511266}, f"two partition:{two_counts}")
    require(two_compatible_status == {
        "isomorphic": 30969, "triangle": 1760, "full_map_Ti_strict_sign": 576,
    }, f"two compatible statuses:{two_compatible_status}")
    require(two_incompatible_status == {"displayed_quartet_mismatch": 511266}, f"two incompatible statuses:{two_incompatible_status}")
    report = {
        "schema": "k2p-probe-site-transport-partition-verification-v1",
        "status": "PASS",
        "inputs": {
            "probe_input_contract_sha256": sha_file(CONTRACT),
            "one_port_ledger_sha256": sha_file(HERE / "one_port_ledger.jsonl.gz"),
            "two_port_ledger_sha256": sha_file(HERE / "two_port_ledger.jsonl.gz"),
            "transport_ledger_sha256": sha_file(HERE / "exact_transport_ledger.jsonl.gz"),
        },
        "one_port": {
            "site_transport_partition": dict(sorted(one_counts.items())),
            "compatible_statuses": dict(sorted(one_compatible_status.items())),
            "incompatible_statuses": dict(sorted(one_incompatible_status.items())),
        },
        "two_port": {
            "site_transport_partition": dict(sorted(two_counts.items())),
            "compatible_statuses": dict(sorted(two_compatible_status.items())),
            "incompatible_statuses": dict(sorted(two_incompatible_status.items())),
        },
        "conclusion": (
            "every unique-parent site-map mismatch is quartet-separated; every "
            "site-map-compatible pair is exactly iso/T or full-map T_i-separated"
        ),
        "unresolved": 0,
        "operational": {"runtime_seconds": time.monotonic() - started},
    }
    logical = dict(report)
    logical.pop("operational")
    report["payload_sha256"] = sha(logical)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "one": report["one_port"],
        "two": report["two_port"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (PartitionFailure, KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"SITE_PARTITION_FAIL:{error}") from error
