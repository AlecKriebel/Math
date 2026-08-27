#!/usr/bin/env python3
"""Fail-closed verifier for a freshly graph-derived cut-topology certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import generate_cut_topology as producer


if not __debug__ or sys.flags.optimize:
    raise SystemExit("optimized Python (-O/-OO) is forbidden for exact verification")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REFERENCE = ROOT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
PRODUCER = HERE / "generate_cut_topology.py"
VERIFIER = HERE / "verify_cut_topology_regeneration.py"
MUTATION_RUNNER = HERE / "test_cut_topology_regeneration_mutations.py"
WRAPPER = HERE / "verify_all.sh"
DEFAULT_REPORT = HERE / "CUT_TOPOLOGY_REGENERATION_REPORT.json"

EXPECTED_CORES = [
    {"name": "cycle", "source": "S", "sinks": ["X"],
     "arcs": [["S", "X"], ["S", "X"]]},
    {"name": "theta_TR_nested", "source": "P", "sinks": ["Q"],
     "arcs": [["U", "V"], ["U", "V"], ["P", "U"], ["P", "Q"], ["V", "Q"]]},
    {"name": "theta_TR_separated", "source": "P", "sinks": ["Q"],
     "arcs": [["U", "V"], ["P", "U"], ["P", "V"], ["U", "Q"], ["V", "Q"]]},
    {"name": "theta_TT_nested", "source": "P", "sinks": ["Q", "R"],
     "arcs": [["U", "V"], ["P", "U"], ["P", "Q"], ["V", "Q"], ["U", "R"], ["V", "R"]]},
    {"name": "theta_TT_separated", "source": "P", "sinks": ["Q", "R"],
     "arcs": [["P", "U"], ["P", "V"], ["U", "Q"], ["V", "Q"], ["U", "R"], ["V", "R"]]},
]


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def signatures_of(record: dict) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(int(value) for value in row) for row in record["signatures"])


def verify_graph_record(witness: dict, signatures: tuple[tuple[int, ...], ...]) -> None:
    network = producer.Network(
        str(witness["core"]),
        str(witness["role"]),
        str(witness["root"]),
        tuple(tuple(edge) for edge in witness["arcs"]),
        tuple(sorted((str(key), int(value)) for key, value in witness["selected"].items())),
        tuple(sorted((str(key), int(value)) for key, value in witness["full_labels"].items())),
    )
    rebuilt = producer.graph_record(network, witness["transport"], signatures)
    require(rebuilt == witness, "witness graph does not reproduce its stored masks and compilation")


def verify_record_hash(record: dict) -> tuple[tuple[int, ...], ...]:

    signatures = signatures_of(record)
    expected = producer.tensor_hash(signatures, int(record["reticulation_count"]))
    require(record["tensor_sha256"] == expected, "tensor hash does not bind signatures")
    return signatures


def verify_semantics(data: dict) -> None:
    require(data.get("status") == "EXACTLY COMPUTED", "top-level status is not exact")
    require(data.get("primitive_cores") == EXPECTED_CORES, "primitive core topology table changed")
    orientation = data.get("primitive_orientation_derivation", {})
    require(orientation == {
        "cycle_orientation_classes": 1,
        "cycle_raw_orientations": 12,
        "status": "EXACTLY COMPUTED",
        "template_match": True,
        "theta_class_multiplicities": [6, 24, 24, 48],
        "theta_orientation_classes": 4,
        "theta_raw_orientations": 102,
    }, "primitive orientation derivation census changed")

    endpoint = data.get("three_port_endpoint_dichotomy", {})
    endpoint_records = endpoint.get("records", [])
    require(endpoint.get("status") == "EXACTLY COMPUTED", "endpoint dichotomy failed")
    require(endpoint.get("tensor_count") == 77 and len(endpoint_records) == 77,
            "endpoint tensor census is not 77")
    require(endpoint.get("failures") == [], "endpoint dichotomy has failures")
    require([row.get("id") for row in endpoint_records] == list(range(77)),
            "endpoint record ids are not contiguous")
    ordinary_endpoint_count = 0
    for row in endpoint_records:
        signatures = verify_record_hash(row)
        witness = row.get("witness_graph")
        if witness.get("core") == "ordinary_trivalent_component":
            ordinary_endpoint_count += 1
            require(int(row["reticulation_count"]) == 0 and signatures == (),
                    "ordinary trivalent endpoint has a nonempty local signature")
            require(witness == {
                "core": "ordinary_trivalent_component",
                "ports": 3,
                "role": "projective_component",
                "signatures": [],
                "transport_reproduces_tensor": True,
            }, "ordinary trivalent endpoint record changed")
        else:
            verify_graph_record(witness, signatures)
    require(ordinary_endpoint_count == 1, "ordinary endpoint multiplicity is not one")

    active = data.get("one_active_wrong_split", {})
    active_records = active.get("records", [])
    require(active.get("status") == "EXACTLY COMPUTED", "one-active theorem failed")
    require(active.get("tensor_count") == 72 and len(active_records) == 72,
            "four-port tensor census is not 72")
    require(active.get("strict_wrong_split_certificates") == 204,
            "strict wrong-split certificate census is not 204")
    require(active.get("common_displayed_splits_skipped") == 12,
            "common displayed-split census is not 12")
    require(active.get("failures") == [], "one-active theorem has failures")
    require([row.get("id") for row in active_records] == list(range(72)),
            "one-active record ids are not contiguous")
    ordinary_tree = tuple((mask,) for mask in (1, 2, 3, 4, 8, 12))
    ordinary_tree_count = 0
    checked = skipped = 0
    for row in active_records:
        signatures = verify_record_hash(row)
        witness = row.get("witness_graph")
        if witness is None:
            ordinary_tree_count += 1
            require(int(row["reticulation_count"]) == 0 and signatures == ordinary_tree,
                    "ordinary four-leaf tree signature changed")
        else:
            verify_graph_record(witness, signatures)
        splits = row.get("splits", [])
        require([tuple(item.get("split", ())) for item in splits] == list(producer.BALANCED_SPLITS),
                "balanced split list changed")
        for item in splits:
            displayed = all(producer.displayed_split_status(signatures, tuple(item["split"])))
            require(item.get("displayed_by_all") is displayed,
                    "displayed-by-all flag disagrees with regenerated masks")
            if displayed:
                skipped += 1
                require("strict_minor" not in item, "common split incorrectly carries a strict minor")
            else:
                checked += 1
                require(isinstance(item.get("strict_minor"), dict),
                        "wrong split lacks its exact strict-minor certificate")
    require(ordinary_tree_count == 1, "ordinary four-leaf tree multiplicity is not one")
    require((checked, skipped) == (204, 12), "recomputed split census changed")

    two_active = data.get("two_active_crossing", {})
    require(two_active.get("status") == "EXACTLY COMPUTED", "two-active identity failed")
    require(all(two_active.get("required_minor_membership", {}).values()),
            "two-active required minor membership failed")
    require(set(two_active.get("identity_remainders", {}).values()) == {"0"},
            "two-active identity has a nonzero remainder")
    switching = data.get("switching_compression", {})
    require(switching.get("status") == "EXACTLY COMPUTED", "switching compression failed")
    require(switching.get("survivor_count") == 0 and switching.get("failures") == [],
            "switching compression has survivors")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent,
        prefix=path.name + ".", delete=False,
    ) as handle:
        handle.write(encoded)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def binding_report(candidate_path: Path, reference_path: Path, data: dict) -> dict:
    endpoint = data["three_port_endpoint_dichotomy"]
    active = data["one_active_wrong_split"]
    report = {
        "schema": "k3p-cut-topology-graph-regeneration-report-v1",
        "status": "PASS",
        "census": {
            "primitive_cores": len(data["primitive_cores"]),
            "endpoint_tensors": endpoint["tensor_count"],
            "four_port_tensors": active["tensor_count"],
            "strict_wrong_split_certificates": active["strict_wrong_split_certificates"],
            "endpoint_failures": len(endpoint["failures"]),
            "one_active_failures": len(active["failures"]),
            "switching_compression_survivors": data["switching_compression"]["survivor_count"],
        },
        "fresh_candidate": {
            "bytes": candidate_path.stat().st_size,
            "sha256": sha256(candidate_path),
        },
        "bound_downstream_input": {
            "path": str(reference_path.relative_to(ROOT)),
            "bytes": reference_path.stat().st_size,
            "sha256": sha256(reference_path),
            "byte_identical_to_fresh_candidate": candidate_path.read_bytes() == reference_path.read_bytes(),
        },
        "active_programs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (PRODUCER, VERIFIER, MUTATION_RUNNER, WRAPPER)
        },
        "claim_boundary": (
            "The graph-derived producer reconstructs the finite cut-topology input; "
            "the downstream K3P algebra and global cut-transfer claims are verified "
            "by their separate active gates."
        ),
    }
    report["payload_sha256"] = sha_object(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--reference", type=Path, default=REFERENCE)
    parser.add_argument("--semantic-only", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        candidate = json.loads(args.candidate.read_text())
        verify_semantics(candidate)
        if not args.semantic_only:
            require(args.candidate.read_bytes() == args.reference.read_bytes(),
                    "fresh graph-derived certificate differs byte-for-byte from the bound K3P input")
        report = None
        if args.report is not None:
            require(not args.semantic_only,
                    "a sealed regeneration report requires the bound reference comparison")
            report = binding_report(args.candidate, args.reference, candidate)
            atomic_json(args.report, report)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError,
            AssertionError, VerificationError) as exc:
        print(f"CUT_TOPOLOGY_GRAPH_REGENERATION_FAIL: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "candidate_sha256": sha256(args.candidate),
        "reference_sha256": None if args.semantic_only else sha256(args.reference),
        "semantic_only": args.semantic_only,
        "status": "PASS",
        "payload_sha256": None if report is None else report["payload_sha256"],
    }, indent=2, sort_keys=True))
    print("CUT_TOPOLOGY_GRAPH_REGENERATION_COMPARE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
