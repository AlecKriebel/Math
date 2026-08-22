#!/usr/bin/env python3
"""Deterministically summarize the corrected K2P restoration forest.

This analyzer is deliberately conservative.  It groups canonical restoration
parents only when their source support, label-free target presentation,
restored roles, source insertion sites, terminal proof mechanisms, exact
algebra-certificate identifiers, and continuation profiles agree.  The groups
are descriptive archetypes; they do not replace the exact parent/child
transport ledger.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
FOREST = PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json"
ATLAS = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RESULTS = PROJECT / "package/referee/k2p_offline_sweep_portable/results/four_port_release_v4"
OUTPUT = HERE / "RESTORATION_ARCHETYPES.json"

EXPECTED_FOREST_SHA256 = "43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8"
EXPECTED_FOREST_PAYLOAD = "0a3df52751ba38d7e6d4d118ee7068a98b7be7897d0aa732e96a74d7523a88bf"
EXPECTED_ATLAS_SHA256 = "5b9e03653cc6960bf341fcbe7e63ffd10226d0f6a56441012212c6e3b2a26483"

ROOT_RE = re.compile(r"s(\d+):c(\d+):t(\d+):p(\d{4})")
ALGEBRA_PROOFS = {
    "exact_multihomogeneous_quadratic",
    "inherited_exact_F_2_112_quartic",
}


class Failure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def object_sha256(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def ordered_hash_root(rows) -> str:
    root = object_sha256([])
    for row in rows:
        root = object_sha256({"previous": root, "row_sha256": object_sha256(row)})
    return root


def import_atlas():
    spec = importlib.util.spec_from_file_location("compression_restoration_atlas", ATLAS)
    require(spec is not None and spec.loader is not None, "cannot import frozen atlas")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def selected_pattern(words) -> list[list[str]]:
    return [
        ["selected" if isinstance(value, int) else str(value) for value in word]
        for word in words
    ]


def target_profile(record) -> dict:
    return {
        "core": record.core_id,
        "incoming_selected": record.incoming_selected,
        "repair_index": record.repair_index,
        "selected_sink_mask": record.selected_sink_mask,
        "segment_words": selected_pattern(record.words),
        "dummy_roles": list(record.dummy_labels),
    }


def load_inputs():
    require(file_sha256(FOREST) == EXPECTED_FOREST_SHA256, "corrected forest file drift")
    require(file_sha256(ATLAS) == EXPECTED_ATLAS_SHA256, "atlas file drift")
    forest = json.loads(FOREST.read_text())
    unhashed = dict(forest)
    payload = unhashed.pop("payload_sha256")
    require(payload == EXPECTED_FOREST_PAYLOAD, "corrected forest payload identity")
    require(object_sha256(unhashed) == payload, "corrected forest payload replay")
    require(forest["status"] == "PASS", "corrected forest status")

    manifests = {}
    expected_manifest_hashes = forest["inputs"]["manifest_sha256"]
    for source_index in range(6):
        relative = f"results/four_port_release_v4/source_{source_index}/residual_manifest.json"
        path = RESULTS / f"source_{source_index}/residual_manifest.json"
        require(file_sha256(path) == expected_manifest_hashes[relative], f"manifest drift:{source_index}")
        manifest = json.loads(path.read_text())
        # ``unresolved`` in these source manifests is the pre-restoration raw
        # stratum, not a failure of the corrected forest consumed here.
        require(manifest["complete"], f"manifest incomplete:{source_index}")
        restoration_ids = set(manifest["restoration_candidates"])
        for record in manifest["records"]:
            if record["canonical_class_id"] in restoration_ids:
                require(record["status"] == "restoration_parent", "manifest restoration status")
                key = (source_index, record["canonical_class_id"])
                require(key not in manifests, f"duplicate canonical parent:{key}")
                manifests[key] = record
    require(len(manifests) == 997, "canonical restoration parent census")
    return forest, manifests


def request_locator(record: dict, target_index: int, port_match: tuple[int, ...]) -> dict:
    locator = {}
    for request in record["child_requests"]:
        for attachment in request["target_dummy_attachments"]:
            if (
                attachment["target_index"] == target_index
                and tuple(attachment["port_match"]) == port_match
            ):
                role = request["omitted_role"]
                prior = locator.get(role)
                if prior is not None:
                    require(prior == request, f"ambiguous restoration request:{role}")
                locator[role] = request
    require(locator, f"missing restoration request:{target_index}:{port_match}")
    return locator


def build_summary() -> dict:
    forest, manifests = load_inputs()
    atlas = import_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    require(len(sources) == 6, "source support census")

    first_by_root = collections.defaultdict(list)
    roots_by_parent = collections.defaultdict(set)
    for row in forest["first_coverage"]:
        match = ROOT_RE.fullmatch(row["root_id"])
        require(match is not None, f"bad root id:{row['root_id']}")
        source_index, class_id = map(int, match.group(1, 2))
        key = (source_index, class_id)
        require(key in manifests, f"row outside manifest universe:{key}")
        first_by_root[row["root_id"]].append(row)
        roots_by_parent[key].add(row["root_id"])

    second_by_root = collections.defaultdict(list)
    for row in forest["second_coverage"]:
        require(row["root_id"] in first_by_root, f"orphan second row:{row['root_id']}")
        second_by_root[row["root_id"]].append(row)

    algebra = forest["algebra_certificates"]
    quadratic_literal_bodies = set()
    for certificate in algebra.values():
        if certificate["proof"] == "exact_multihomogeneous_quadratic":
            body = {
                key: certificate[key]
                for key in ("degree", "coordinate_pairs", "coefficients", "weight")
            }
            quadratic_literal_bodies.add(object_sha256(body))

    member_profiles = {}
    member_summaries = {}
    for root_id in sorted(first_by_root):
        match = ROOT_RE.fullmatch(root_id)
        require(match is not None, f"bad root id:{root_id}")
        source_index, class_id, target_index = map(int, match.group(1, 2, 3))
        port_match = tuple(int(value) for value in match.group(4))
        requests = request_locator(manifests[(source_index, class_id)], target_index, port_match)
        rows = sorted(
            first_by_root[root_id],
            key=lambda row: (row["restored_role"], row["source_insertion_index"]),
        )
        outcomes = []
        first_proofs = collections.Counter()
        algebra_ids = set()
        for row in rows:
            role = row["restored_role"]
            require(role in requests, f"role/request mismatch:{root_id}:{role}")
            candidates = requests[role]["source_insertion_edge_candidates"]
            insertion = row["source_insertion_index"]
            require(0 <= insertion < len(candidates), f"source insertion bound:{root_id}")
            site = candidates[insertion]
            outcome = {
                "restored_role": role,
                "source_site": {
                    "edge_role": site["edge_role"],
                    "tail": site["tail"],
                    "head": site["head"],
                },
                "proof": row["proof"],
                "status": row["status"],
                "remaining_roles": list(row["remaining_roles"]),
            }
            if row["proof"] in ALGEBRA_PROOFS:
                certificate_id = row["certificate_sha256"]
                require(certificate_id in algebra, f"missing algebra certificate:{certificate_id}")
                require(algebra[certificate_id]["proof"] == row["proof"], "algebra proof reassignment")
                outcome["algebra_certificate_sha256"] = certificate_id
                algebra_ids.add(certificate_id)
            outcomes.append(outcome)
            first_proofs[row["proof"]] += 1

        second_rows = sorted(
            second_by_root.get(root_id, []),
            key=lambda row: (
                row["first_restored_role"],
                row["first_source_insertion_index"],
                row["second_source_insertion_index"],
            ),
        )
        continuation_profile = [
            {
                "first_restored_role": row["first_restored_role"],
                "first_source_insertion_index": row["first_source_insertion_index"],
                "second_restored_role": row["second_restored_role"],
                "second_source_insertion_index": row["second_source_insertion_index"],
                "proof": row["proof"],
                "status": row["status"],
            }
            for row in second_rows
        ]
        profile = {
            "target": target_profile(targets[target_index]),
            "restoration_roles": sorted(requests),
            "first_outcomes": outcomes,
            "second_outcomes": continuation_profile,
        }
        profile_id = object_sha256(profile)
        member_profiles[root_id] = profile_id
        member_summaries[root_id] = {
            "profile_sha256": profile_id,
            "first_children": len(rows),
            "second_children": len(second_rows),
            "first_proofs": dict(sorted(first_proofs.items())),
            "second_proofs": dict(sorted(collections.Counter(row["proof"] for row in second_rows).items())),
            "target_core": targets[target_index].core_id,
            "restoration_roles": sorted(requests),
            "algebra_certificate_sha256": sorted(algebra_ids),
        }

    archetype_groups = collections.defaultdict(list)
    parent_signatures = {}
    for parent in sorted(manifests):
        source_index, class_id = parent
        profile_multiset = collections.Counter(
            member_profiles[root_id] for root_id in roots_by_parent[parent]
        )
        signature = {
            "source_support": {
                "core": sources[source_index].core_id,
                "repair_index": sources[source_index].repair_index,
            },
            "member_profile_multiset": sorted(profile_multiset.items()),
        }
        signature_id = object_sha256(signature)
        parent_signatures[parent] = signature_id
        archetype_groups[signature_id].append(parent)

    require(len(archetype_groups) == 297, f"bounded archetype census drift:{len(archetype_groups)}")
    signature_order = sorted(archetype_groups)
    archetypes = []
    parent_assignment = []
    for number, signature_id in enumerate(signature_order):
        archetype_id = f"RA-{number:03d}"
        parents = sorted(archetype_groups[signature_id])
        roots = sorted(root_id for parent in parents for root_id in roots_by_parent[parent])
        first_rows = [row for root_id in roots for row in first_by_root[root_id]]
        second_rows = [row for root_id in roots for row in second_by_root.get(root_id, [])]
        source_supports = sorted({
            f"{sources[source_index].core_id}:repair{sources[source_index].repair_index}"
            for source_index, _ in parents
        })
        require(len(source_supports) == 1, f"mixed source support archetype:{archetype_id}")
        proof_first = collections.Counter(row["proof"] for row in first_rows)
        proof_second = collections.Counter(row["proof"] for row in second_rows)
        target_cores = collections.Counter(member_summaries[root_id]["target_core"] for root_id in roots)
        roles = collections.Counter(
            role for root_id in roots for role in member_summaries[root_id]["restoration_roles"]
        )
        algebra_ids = sorted({
            certificate_id
            for root_id in roots
            for certificate_id in member_summaries[root_id]["algebra_certificate_sha256"]
        })
        canonical_parents = [
            {"source_index": source_index, "canonical_class_id": class_id}
            for source_index, class_id in parents
        ]
        parent_assignment.extend(
            {**parent, "archetype_id": archetype_id} for parent in canonical_parents
        )
        archetypes.append({
            "archetype_id": archetype_id,
            "signature_sha256": signature_id,
            "source_support": source_supports[0],
            "canonical_parents": canonical_parents,
            "canonical_parent_count": len(parents),
            "member_roots": len(roots),
            "member_profile_classes": len({member_profiles[root_id] for root_id in roots}),
            "first_children": len(first_rows),
            "second_children": len(second_rows),
            "final_leaves": len(first_rows) - sum(row["status"] == "continuation" for row in first_rows) + len(second_rows),
            "max_depth": 2 if second_rows else 1,
            "target_core_census": dict(sorted(target_cores.items())),
            "restoration_role_census": dict(sorted(roles.items())),
            "first_proof_census": dict(sorted(proof_first.items())),
            "second_proof_census": dict(sorted(proof_second.items())),
            "algebra_certificate_sha256": algebra_ids,
            "ordered_member_profile_hash_root": ordered_hash_root(
                [{"root_id": root_id, "profile_sha256": member_profiles[root_id]} for root_id in roots]
            ),
        })

    parent_assignment.sort(key=lambda row: (row["source_index"], row["canonical_class_id"]))
    multiplicities = collections.Counter(item["canonical_parent_count"] for item in archetypes)
    first_proofs = collections.Counter(row["proof"] for row in forest["first_coverage"])
    second_proofs = collections.Counter(row["proof"] for row in forest["second_coverage"])
    result = {
        "schema": "k2p-restoration-descriptive-archetypes-v1",
        "status": "PC-PARTIAL",
        "source": {
            "corrected_forest_sha256": EXPECTED_FOREST_SHA256,
            "corrected_forest_payload_sha256": EXPECTED_FOREST_PAYLOAD,
            "atlas_sha256": EXPECTED_ATLAS_SHA256,
            "manifest_sha256": forest["inputs"]["manifest_sha256"],
        },
        "definition": {
            "kind": "descriptive structural/outcome fingerprint",
            "parent_signature": "source core and repair plus the multiset of member fingerprints",
            "member_signature": "label-free target core presentation, restoration roles, exact source insertion sites, ordered proof/status outcomes, exact algebra certificate IDs, and relative continuation outcomes",
            "safe_use": "compresses exposition and repeated outcome patterns only",
            "not_proved": "no cross-parent labelled mixed-graph transport quotient is asserted; the corrected forest remains the exact assignment authority",
        },
        "census": {
            "canonical_parents": len(manifests),
            "member_roots": len(first_by_root),
            "descriptive_archetypes": len(archetypes),
            "first_children": len(forest["first_coverage"]),
            "second_children": len(forest["second_coverage"]),
            "forest_edges": len(forest["first_coverage"]) + len(forest["second_coverage"]),
            "final_leaves": forest["census"]["final_leaves"],
            "max_depth": forest["census"]["max_depth"],
            "unresolved": forest["census"]["unresolved"],
            "archetype_parent_multiplicity": {str(key): value for key, value in sorted(multiplicities.items())},
        },
        "proof_mechanisms": {
            "first_layer": dict(sorted(first_proofs.items())),
            "second_layer": dict(sorted(second_proofs.items())),
            "terminal_mechanisms": [
                "displayed_quartet_mismatch",
                "full_map_Ti_zero_strict_sign",
                "exact_multihomogeneous_quadratic",
                "inherited_exact_F_2_112_quartic",
            ],
            "continuation_mechanism": "restore_remaining_physical_role",
            "quadratic_certificate_classes": sum(
                certificate["proof"] == "exact_multihomogeneous_quadratic"
                for certificate in algebra.values()
            ),
            "quadratic_literal_bodies": len(quadratic_literal_bodies),
            "quartic_transport_certificate_classes": sum(
                certificate["proof"] == "inherited_exact_F_2_112_quartic"
                for certificate in algebra.values()
            ),
            "quartic_underlying_families": 1,
            "whole_map_sign_polynomial_classes": len(forest["sign_certificates"]),
            "quartet_certificate_classes": len(forest["quartet_certificates"]),
            "bridge_torus_multihomogeneity": forest["bridge_torus"]["conclusion"],
        },
        "coverage": {
            "canonical_parent_assignment": parent_assignment,
            "canonical_parent_assignment_sha256": object_sha256(parent_assignment),
            "ordered_member_root_profile_hash_root": ordered_hash_root(
                [{"root_id": root_id, "profile_sha256": member_profiles[root_id]} for root_id in sorted(member_profiles)]
            ),
            "ordered_first_row_hash_root": ordered_hash_root(forest["first_coverage"]),
            "ordered_second_row_hash_root": ordered_hash_root(forest["second_coverage"]),
            "every_parent_exactly_once": len(parent_assignment) == len({
                (row["source_index"], row["canonical_class_id"]) for row in parent_assignment
            }) == 997,
            "every_member_root_exactly_once": len(member_profiles) == 2540,
            "every_child_edge_counted": len(forest["first_coverage"]) + len(forest["second_coverage"]) == 36824,
        },
        "archetypes": archetypes,
        "compression_verdict": {
            "outcome": "honest descriptive compression with irreducible exact residue",
            "parent_count_before": 997,
            "descriptive_archetype_count": len(archetypes),
            "exact_transport_quotient_count": None,
            "exact_residue": {
                "canonical_parent_assignments": 997,
                "member_root_presentations": 2540,
                "parent_child_edges": 36824,
                "algebra_transport_certificate_classes": len(algebra),
            },
            "reason": "The bounded pass found repeated structural/outcome fingerprints, but did not construct cross-parent labelled transports proving that one representative implies every member.  Exact row assignments and transports therefore remain load-bearing.",
        },
    }
    result["payload_sha256"] = object_sha256(result)
    return result


def main() -> None:
    if not __debug__:
        raise Failure("RESTORATION_COMPRESSION_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--emit", action="store_true", help="print the deterministic JSON artifact")
    group.add_argument("--check", type=Path, nargs="?", const=OUTPUT, help="compare with an existing artifact")
    args = parser.parse_args()
    generated = build_summary()
    if args.emit:
        print(json.dumps(generated, indent=2, sort_keys=True))
        return
    target = args.check or OUTPUT
    require(target.exists(), f"missing archetype artifact:{target}")
    recorded = json.loads(target.read_text())
    require(recorded == generated, "restoration archetype artifact drift")
    print(json.dumps({
        "status": "PASS",
        "artifact_sha256": file_sha256(target),
        "payload_sha256": generated["payload_sha256"],
        "descriptive_archetypes": generated["census"]["descriptive_archetypes"],
        "canonical_parents": generated["census"]["canonical_parents"],
        "member_roots": generated["census"]["member_roots"],
        "forest_edges": generated["census"]["forest_edges"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
