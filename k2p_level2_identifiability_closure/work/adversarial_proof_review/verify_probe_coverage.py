#!/usr/bin/env python3
"""Fail-closed audit of omitted-role terminal and coherent-probe coverage.

The four-port release calls some selected relations isomorphic or triangle-
related even though the frozen record still has omitted physical roles.  This
program independently inventories those records, checks whether the published
restoration forest binds them, and recomputes the topology deck of every first
five-port child.  It deliberately does not promote the global theorem merely
from a prose coherent-probe assertion.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RESULT_ROOT = (
    PROJECT
    / "package/referee/k2p_offline_sweep_portable/results/four_port_release_v4"
)
PARTITION = (
    PROJECT
    / "work/raw_ledger_audit/artifacts/retained_class_partition.json.gz"
)
RESTORATION_GENERATOR = PROJECT / "work/restoration_forest/enumerate_five_port.py"
TOPOLOGY_AUDIT = HERE / "verify_topology_direction.py"
GLOBAL_PROOF = PROJECT / "work/global_theorem_closure/GLOBAL_PROOF.md"
EXPECTED_PROBE_CERTIFICATE = PROJECT / "work/coherent_probe_closure/probe_certificate.json"


class ProbeAuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProbeAuditFailure(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ProbeAuditFailure(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def terminal_inventory(targets) -> tuple[list[dict], dict[str, object]]:
    roots = []
    statuses = Counter()
    strata = Counter()
    omitted_statuses = Counter()
    omitted_classes = []
    request_count = 0

    for path in sorted(RESULT_ROOT.glob("source_*/residual_manifest.json")):
        manifest = json.loads(path.read_text())
        source_index = manifest["source_index"]
        for record in manifest["records"]:
            if record["status"] not in {"isomorphic", "triangle"}:
                continue
            statuses[record["status"]] += 1
            strata[(record["status"], record["stratum"])] += 1
            if not record.get("omitted_roles"):
                continue
            omitted_statuses[record["status"]] += 1
            omitted_classes.append(
                {
                    "source_index": source_index,
                    "canonical_class_id": record["canonical_class_id"],
                    "status": record["status"],
                    "omitted_roles": record["omitted_roles"],
                }
            )
            request_count += len(record["child_requests"])
            attachments: dict[tuple[int, tuple[int, ...]], dict[str, dict]] = {}
            candidates = None
            for request in record["child_requests"]:
                if candidates is None:
                    candidates = request["source_insertion_edge_candidates"]
                require(
                    request["source_insertion_edge_candidates"] == candidates,
                    "terminal source candidate drift",
                )
                role = request["omitted_role"]
                for attachment in request["target_dummy_attachments"]:
                    key = (
                        attachment["target_index"],
                        tuple(attachment["port_match"]),
                    )
                    require(
                        role not in attachments.setdefault(key, {}),
                        "duplicate terminal role attachment",
                    )
                    attachments[key][role] = attachment
            require(candidates is not None, "omitted terminal lacks child request")
            for (target_index, permutation), by_role in sorted(attachments.items()):
                roles = tuple(sorted(by_role))
                require(
                    roles == tuple(targets[target_index].dummy_labels),
                    "terminal target dummy-role union drift",
                )
                roots.append(
                    {
                        "source_index": source_index,
                        "canonical_class_id": record["canonical_class_id"],
                        "parent_status": record["status"],
                        "target_index": target_index,
                        "permutation": permutation,
                        "roles": roles,
                        "candidates": candidates,
                    }
                )

    require(statuses == Counter({"triangle": 35, "isomorphic": 20}), "terminal census")
    require(
        omitted_statuses == Counter({"triangle": 25, "isomorphic": 10}),
        "omitted terminal census",
    )
    require(len(roots) == 54, "omitted-terminal member-root census")
    require(sum(len(root["roles"]) * 7 for root in roots) == 532, "first-child census")
    return roots, {
        "terminal_statuses": dict(sorted(statuses.items())),
        "terminal_strata": {
            f"{status}:{stratum}": count
            for (status, stratum), count in sorted(strata.items())
        },
        "omitted_terminal_statuses": dict(sorted(omitted_statuses.items())),
        "omitted_terminal_classes": omitted_classes,
        "omitted_terminal_child_requests": request_count,
        "omitted_terminal_member_roots": len(roots),
        "omitted_terminal_first_children": 532,
    }


def check_partition(omitted_classes: list[dict]) -> dict[str, object]:
    with gzip.open(PARTITION, "rt") as handle:
        partition = json.load(handle)
    rows = {
        (row["source_index"], row["canonical_class_id"]): row
        for row in partition["classes"]
    }
    for item in omitted_classes:
        row = rows[(item["source_index"], item["canonical_class_id"])]
        require(row["ledger_category"] == "retained_terminal", "terminal category drift")
        require(row["restoration_obligation_id"] is None, "unexpected obligation binding")
    examples = {}
    for key in ((0, 146), (0, 306)):
        row = rows[key]
        examples[f"s{key[0]}:c{key[1]}"] = {
            "ledger_category": row["ledger_category"],
            "restoration_obligation_id": row["restoration_obligation_id"],
            "raw_presentation_count": row["raw_presentation_count"],
            "status": row["status_before_direct_overlay"],
        }
    return {
        "status": "UNBOUND",
        "checked_classes": len(omitted_classes),
        "all_are_retained_terminal": True,
        "all_restoration_obligation_ids_are_null": True,
        "examples": examples,
    }


def check_first_child_topology(topology, grammar, roots: list[dict]) -> dict[str, object]:
    sources = grammar.source_supports()
    targets = grammar.target_completions(4, True) + grammar.target_completions(4, False)
    source_graphs = {}
    target_graphs = {}
    source_signatures = {}
    source_triples = {}
    target_signatures = {}
    target_triples = {}
    counts = Counter()
    by_parent = Counter()

    for root in roots:
        for insertion_index, candidate in enumerate(root["candidates"]):
            source_key = (root["source_index"], insertion_index)
            if source_key not in source_signatures:
                graph = topology.clean_insert_source_leaf(
                    sources[root["source_index"]].graph, candidate
                )
                source_graphs[source_key] = graph
                source_signatures[source_key] = topology.five_port_signature(graph)
                source_triples[source_key] = topology.five_port_triples(graph)
        for role in root["roles"]:
            target_key = (root["target_index"], root["permutation"], role)
            if target_key not in target_signatures:
                graph = topology.clean_promote_target(
                    targets[root["target_index"]], root["permutation"], role
                )
                target_graphs[target_key] = graph
                target_signatures[target_key] = topology.five_port_signature(graph)
                target_triples[target_key] = topology.five_port_triples(graph)

    for root in roots:
        parent = f"s{root['source_index']}:c{root['canonical_class_id']}"
        for role in root["roles"]:
            target_key = (root["target_index"], root["permutation"], role)
            for insertion_index, _ in enumerate(root["candidates"]):
                source_key = (root["source_index"], insertion_index)
                if source_signatures[source_key] != target_signatures[target_key]:
                    status = "displayed_quartet_mismatch"
                elif any(
                    {
                        source_triples[source_key][triple],
                        target_triples[target_key][triple],
                    }
                    == {"tree", "sunlet"}
                    for triple in source_triples[source_key]
                ):
                    status = "strict_tree_sunlet"
                else:
                    relation = grammar.mixed_relation_exact(
                        source_graphs[source_key], target_graphs[target_key]
                    )
                    status = (
                        relation
                        if relation in {"isomorphic", "triangle"}
                        else "equal_deck_nonterminal"
                    )
                counts[status] += 1
                if status in {"isomorphic", "triangle", "equal_deck_nonterminal"}:
                    by_parent[parent] += 1

    require(sum(counts.values()) == 532, "terminal first-child topology partition")
    require(counts["isomorphic"] == 13, "omitted terminal isomorphism census")
    require(counts["triangle"] == 0, "unexpected omitted terminal triangle child")
    require(counts["equal_deck_nonterminal"] == 0, "unresolved omitted terminal child")
    return {
        "status": "INCOMPLETE",
        "raw_first_children": 532,
        "topology_counts": dict(sorted(counts.items())),
        "nonseparated_parent_count": len(by_parent),
        "nonseparated_by_parent": dict(sorted(by_parent.items())),
        "interpretation": (
            "all 13 nonseparated first children are exact labelled isomorphisms; they are "
            "candidate five-port anchors, but no bound recursive A+p/A+p+q transport and "
            "coherence package currently starts from them"
        ),
    }


def check_published_binding() -> dict[str, object]:
    generator_text = RESTORATION_GENERATOR.read_text()
    require(
        'if record["status"] != "restoration_parent":' in generator_text,
        "restoration root filter changed",
    )
    proof_text = " ".join(GLOBAL_PROOF.read_text().split())
    prose_markers = (
        "One-port restrictions locate every omitted label relative to the rigid support",
        "Two-port restrictions determine the total order of labels on a common segment",
    )
    require(all(marker in proof_text for marker in prose_markers), "global probe prose drift")
    certificate_present = EXPECTED_PROBE_CERTIFICATE.is_file()
    certificate_status = None
    if certificate_present:
        certificate_status = json.loads(EXPECTED_PROBE_CERTIFICATE.read_text()).get("status")
    return {
        "status": "PASS" if certificate_status == "PASS" else "MISSING",
        "restoration_generator_filter": "status == restoration_parent only",
        "global_proof_has_prose_claim": True,
        "probe_certificate_path": str(EXPECTED_PROBE_CERTIFICATE.relative_to(PROJECT)),
        "probe_certificate_present": certificate_present,
        "probe_certificate_status": certificate_status,
    }


def main() -> int:
    if not __debug__:
        raise ProbeAuditFailure("verification disabled under Python -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()

    topology = load_module("probe_topology_audit", TOPOLOGY_AUDIT)
    grammar = topology.load_graph_grammar()
    targets = grammar.target_completions(4, True) + grammar.target_completions(4, False)
    roots, inventory = terminal_inventory(targets)
    partition = check_partition(inventory["omitted_terminal_classes"])
    first_children = check_first_child_topology(topology, grammar, roots)
    binding = check_published_binding()
    blockers = []
    if binding["status"] != "PASS":
        blockers.append(
            {
                "id": "COHERENT_PROBE_LEDGER_MISSING",
                "severity": "FATAL_FOR_GLOBAL_THEOREM",
                "diagnostic": (
                    "Thirty-five four-port iso/triangle terminals retain omitted roles, "
                    "but the 997-parent restoration forest excludes them. A bound one-/two-"
                    "port probe forest with exact parent transports and coherent triangle "
                    "choices is required before the local or global theorem is unconditional."
                ),
            }
        )
    report: dict[str, object] = {
        "schema": "k2p-coherent-probe-coverage-audit-v1",
        "status": "PASS" if not blockers else "BLOCKED",
        "inventory": inventory,
        "raw_partition_binding": partition,
        "first_child_topology": first_children,
        "published_probe_binding": binding,
        "blockers": blockers,
        "input_hashes": {
            "retained_partition": sha256_file(PARTITION),
            "restoration_generator": sha256_file(RESTORATION_GENERATOR),
            "global_proof": sha256_file(GLOBAL_PROOF),
            "topology_audit": sha256_file(TOPOLOGY_AUDIT),
        },
    }
    body = dict(report)
    report["payload_sha256"] = hashlib.sha256(canonical_bytes(body)).hexdigest()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 2 if args.require_pass and report["status"] != "PASS" else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProbeAuditFailure as error:
        print(f"PROBE_COVERAGE_AUDIT_FAIL: {error}")
        raise SystemExit(1)
