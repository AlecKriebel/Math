#!/usr/bin/env python3
"""Regenerate the complete fixed-full K3P restoration certificate.

Only graph, parentage, repair-role, ordering, and exact transport metadata are
read from the frozen corrected K2P restoration forest.  Every graph and every
K3P algebraic separator is rebuilt from the primitive K3P atlas.  The producer
is deterministic and checkpoint-resumable; the independent verifier does not
import this file or :mod:`restoration_build_support`.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import itertools
import json
import os
import sys
from fractions import Fraction
from pathlib import Path

import restoration_build_support as support


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
FOREST_PATH = support.FOREST_PATH
ATLAS_PATH = support.ATLAS_PATH
SUPPORT_PATH = HERE / "restoration_build_support.py"
SEPARATOR_PATH = PROJECT / "three_port/literal_separator_v2/K3P_TREE_SUNLET_LITERAL_SEPARATOR_V2.json"
THREE_PORT_PATH = PROJECT / "three_port/primary_exact_evidence.json"
MARGINAL_PATH = PROJECT / "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json"
LEDGER_PATH = HERE / "restoration_ledger.jsonl.gz"
REGISTRY_PATH = HERE / "restoration_proof_registry.json.gz"
MANIFEST_PATH = HERE / "RESTORATION_MANIFEST.json"
REPORT_PATH = HERE / "K3P_RESTORATION_THEOREM_REPORT.md"
CHECKPOINT_PATH = HERE / ".producer_checkpoint.json"


class RestorationFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise RestorationFailure(message)


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


def logical_payload(value):
    result = dict(value)
    result.pop("payload_sha256", None)
    return sha(result)


def graph_payload(graph):
    nodes = []
    for node, data in sorted(graph.nodes(data=True), key=lambda row: repr(row[0])):
        nodes.append({
            "id": repr(node),
            "role": data.get("role"),
            "label": data.get("label"),
            "dummy": bool(data.get("dummy", False)),
            "dummy_name": data.get("dummy_name"),
        })
    arcs = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        arcs.append({
            "tail": repr(tail),
            "head": repr(head),
            "edge_role": data.get("edge_role"),
        })
    return {"nodes": nodes, "arcs": arcs}


def descriptor_payload(descriptor):
    return {
        "k": descriptor.k,
        "retic_count": descriptor.retic_count,
        "edge_class_count": descriptor.edge_class_count,
        "outputs": descriptor.outputs,
        "edge_signatures": descriptor.edge_signatures,
    }


def sparse_payload(poly):
    return [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(poly.items())
    ]


def sparse_hash(poly):
    return sha(sparse_payload(poly))


def evaluate_sparse(poly, point):
    result = Fraction(0)
    for exponent, coefficient in poly.items():
        term = Fraction(coefficient)
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        result += term
    return result


def strict_witness(atlas, descriptor, poly):
    require(bool(poly), "strict witness requested for zero polynomial")
    for salt in range(32):
        edges, inheritance = atlas.default_exact_point(descriptor, salt)
        point = tuple(value for edge in edges for value in edge) + tuple(inheritance)
        value = evaluate_sparse(poly, point)
        if value:
            return {
                "salt": salt,
                "edge_triples": [list(map(str, edge)) for edge in edges],
                "inheritance": list(map(str, inheritance)),
                "evaluation": str(value),
                "domain": "strict continuous-time K3P",
            }
    raise RestorationFailure("nonzero source pullback missed strict witness grid")


def split_payload(value):
    rows = []
    for item in sorted(value, key=repr):
        if item == ("star",):
            rows.append(["star"])
        else:
            rows.append([list(item[0]), list(item[1])])
    return rows


def quartet_separator(atlas, source, target):
    labels = support.labels_of(source)
    require(labels == support.labels_of(target), "quartet label mismatch")
    for quartet in itertools.combinations(labels, 4):
        source_splits = atlas.quartet_splits(source, quartet)
        target_splits = atlas.quartet_splits(target, quartet)
        if source_splits != target_splits:
            certificate = {
                "method": "exact displayed-quartet split mismatch",
                "quartet": list(quartet),
                "source_splits": split_payload(source_splits),
                "target_splits": split_payload(target_splits),
            }
            return "Q:" + sha(certificate), certificate
    return None


def tree_sunlet_separator(atlas, source, target):
    labels = support.labels_of(source)
    require(labels == support.labels_of(target), "tree-sunlet label mismatch")
    for triple in itertools.combinations(labels, 3):
        source_type = atlas.triple_type(source, triple)
        target_type = atlas.triple_type(target, triple)
        if {source_type, target_type} != {"tree", "sunlet"}:
            continue
        source_restricted, source_normalized = support.normalized_restriction(
            atlas, source, triple
        )
        target_restricted, target_normalized = support.normalized_restriction(
            atlas, target, triple
        )
        source_descriptor = atlas.model_descriptor(source_normalized)
        target_descriptor = atlas.model_descriptor(target_normalized)
        source_circuits = support.circuit_pullbacks(atlas, source_descriptor)
        target_circuits = support.circuit_pullbacks(atlas, target_descriptor)
        if source_type == "tree":
            tree_on, sunlet_on = "source", "target"
            tree_descriptor, sunlet_descriptor = source_descriptor, target_descriptor
            tree_circuits, sunlet_circuits = source_circuits, target_circuits
            sunlet_graph = target_normalized
        else:
            tree_on, sunlet_on = "target", "source"
            tree_descriptor, sunlet_descriptor = target_descriptor, source_descriptor
            tree_circuits, sunlet_circuits = target_circuits, source_circuits
            sunlet_graph = source_normalized
        # The rooted reticulation count is only a finder.  Literal map and
        # ordinary mixed-graph checks are the certificate.
        if tree_descriptor.retic_count != 0 or sunlet_descriptor.retic_count != 1:
            continue
        if not support.is_exact_ordinary_sunlet(atlas, sunlet_graph):
            continue
        if any(tree_circuits) or not any(sunlet_circuits):
            continue
        certificate = {
            "method": "literal restricted K3P maps plus six-circuit SOS",
            "triple": list(triple),
            "normalized_label_map": {
                str(old): new for new, old in enumerate(sorted(triple))
            },
            "tree_on": tree_on,
            "sunlet_on": sunlet_on,
            "source_restricted_graph_sha256": sha(graph_payload(source_restricted)),
            "target_restricted_graph_sha256": sha(graph_payload(target_restricted)),
            "source_descriptor_sha256": sha(descriptor_payload(source_descriptor)),
            "target_descriptor_sha256": sha(descriptor_payload(target_descriptor)),
            "tree_circuit_pullback_sha256": [sparse_hash(poly) for poly in tree_circuits],
            "sunlet_circuit_pullback_sha256": [sparse_hash(poly) for poly in sunlet_circuits],
            "sunlet_nonzero_circuit_count": sum(bool(poly) for poly in sunlet_circuits),
            "separator_certificate_sha256": sha_file(SEPARATOR_PATH),
            "separator": "sum_{j=1}^6 I_j^2",
            "three_sector_independence": "C, G, and T compiled independently",
            "physical_domain": "D_{3,+}",
        }
        return "K3P-TS:" + sha(certificate), certificate
    return None


def coordinate_multidegree(atlas, k, monomial):
    weights = atlas.coordinate_weights(k)
    return tuple(
        sum(weights[index][slot] for index in monomial)
        for slot in range(3 * k)
    )


def quadratic_separator(atlas, source, target_full):
    source_descriptor = atlas.model_descriptor_fast2(source)
    target_descriptor = atlas.model_descriptor_fast2(target_full)
    separator = atlas.quadratic_separator_fast(
        source_descriptor, target_descriptor, max_block_size=64
    )
    if separator is None:
        return None
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    source_outputs = atlas.output_sparse_polynomials(source_descriptor)
    pairs = tuple(tuple(pair) for pair in separator["coordinate_pairs"])
    coefficients = tuple(map(int, separator["coefficients"]))
    target_pullback = atlas.sparse_lincomb(
        [atlas.sparse_mul(target_outputs[i], target_outputs[j]) for i, j in pairs],
        coefficients,
    )
    source_pullback = atlas.sparse_lincomb(
        [atlas.sparse_mul(source_outputs[i], source_outputs[j]) for i, j in pairs],
        coefficients,
    )
    require(not target_pullback, "regenerated K3P quadratic target pullback nonzero")
    require(bool(source_pullback), "regenerated K3P quadratic source pullback zero")
    degrees = {
        coordinate_multidegree(atlas, source_descriptor.k, pair)
        for pair, coefficient in zip(pairs, coefficients)
        if coefficient
    }
    require(len(degrees) == 1, "K3P quadratic is not three-sector multihomogeneous")
    certificate = {
        "method": "exact K3P multihomogeneous target quadratic",
        "degree": 2,
        "k": source_descriptor.k,
        "source_descriptor_sha256": sha(descriptor_payload(source_descriptor)),
        "target_descriptor_sha256": sha(descriptor_payload(target_descriptor)),
        "coordinate_pairs": [list(pair) for pair in pairs],
        "coefficients": list(coefficients),
        "boundary_multidegree_C_G_T": list(next(iter(degrees))),
        "target_pullback_term_count": 0,
        "source_pullback_term_count": len(source_pullback),
        "source_pullback_sha256": sparse_hash(source_pullback),
        "strict_source_witness": strict_witness(
            atlas, source_descriptor, source_pullback
        ),
        "uses_k2p_sector_equality": False,
    }
    return "K3P-Q2:" + sha(certificate), certificate


def normalize_restriction(atlas, graph, subset):
    restricted = atlas.restrict_rooted(graph, set(subset))
    label_map = {old: new for new, old in enumerate(sorted(subset))}
    normalized = restricted.copy()
    for _, data in normalized.nodes(data=True):
        label = data.get("label")
        if label in label_map:
            data["label"] = label_map[label]
    return restricted, normalized, label_map


def marginal_quartic_separator(atlas, source, target, templates):
    labels = support.labels_of(source)
    require(labels == support.labels_of(target), "quartic marginal label mismatch")
    for subset in itertools.combinations(labels, 4):
        source_restricted, source_normalized, label_map = normalize_restriction(
            atlas, source, subset
        )
        target_restricted, target_normalized, target_map = normalize_restriction(
            atlas, target, subset
        )
        require(label_map == target_map, "quartic marginal label transport")
        source_descriptor = atlas.model_descriptor_fast2(source_normalized)
        target_descriptor = atlas.model_descriptor_fast2(target_normalized)
        for template in templates:
            for permutation in itertools.permutations(range(4)):
                terms = support.transported_terms(atlas, template["terms"], permutation)
                target_pullback = support.polynomial_pullback(
                    atlas, target_descriptor, terms
                )
                if target_pullback:
                    continue
                source_pullback = support.polynomial_pullback(
                    atlas, source_descriptor, terms
                )
                if not source_pullback:
                    continue
                degrees = {
                    coordinate_multidegree(
                        atlas, 4, tuple(term["coordinate_indices"])
                    )
                    for term in terms
                    if term["coefficient"]
                }
                require(
                    len(degrees) == 1,
                    "transported K3P quartic is not three-sector multihomogeneous",
                )
                certificate = {
                    "method": "direct four-port marginal and transported active K3P quartic",
                    "degree": 4,
                    "marginal_labels": list(subset),
                    "normalized_label_map": {
                        str(old): new for old, new in sorted(label_map.items())
                    },
                    "source_restricted_graph_sha256": sha(
                        graph_payload(source_restricted)
                    ),
                    "target_restricted_graph_sha256": sha(
                        graph_payload(target_restricted)
                    ),
                    "source_descriptor_sha256": sha(
                        descriptor_payload(source_descriptor)
                    ),
                    "target_descriptor_sha256": sha(
                        descriptor_payload(target_descriptor)
                    ),
                    "template_file": template["filename"],
                    "template_file_sha256": template["file_sha256"],
                    "template_orbit_id": template["orbit_id"],
                    "port_permutation": list(permutation),
                    "terms": terms,
                    "boundary_multidegree_C_G_T": list(next(iter(degrees))),
                    "target_pullback_term_count": 0,
                    "source_pullback_term_count": len(source_pullback),
                    "source_pullback_sha256": sparse_hash(source_pullback),
                    "strict_source_witness": strict_witness(
                        atlas, source_descriptor, source_pullback
                    ),
                    "direct_marginal_of_original_containment": True,
                    "target_marginal_openness_used": False,
                    "uses_k2p_sector_equality": False,
                }
                return "K3P-M4:" + sha(certificate), certificate
    return None


def load_templates():
    templates = []
    # Only active, independently replayed K3P polynomial files enter the
    # restoration search.  The historical K2P F_(2,112) quartic is forbidden.
    for path in support.POLYNOMIAL_PATHS[:2]:
        payload = json.loads(path.read_text())
        for record in payload["records"]:
            templates.append({
                "filename": path.name,
                "file_sha256": sha_file(path),
                "orbit_id": record["orbit_id"],
                "terms": record["terms"],
            })
    return templates


def register(registries, kind, result):
    proof_id, certificate = result
    previous = registries[kind].setdefault(proof_id, certificate)
    require(previous == certificate, f"proof identifier collision:{proof_id}")
    return proof_id


def classify_pair(atlas, source, target_full, target_selected, templates, registries):
    result = quartet_separator(atlas, source, target_selected)
    if result is not None:
        return "displayed_quartet_mismatch", register(
            registries, "displayed_quartet_mismatch", result
        )
    result = tree_sunlet_separator(atlas, source, target_selected)
    if result is not None:
        return "k3p_tree_sunlet_sos", register(
            registries, "k3p_tree_sunlet_sos", result
        )
    result = quadratic_separator(atlas, source, target_full)
    if result is not None:
        return "k3p_exact_multihomogeneous_quadratic", register(
            registries, "k3p_exact_multihomogeneous_quadratic", result
        )
    result = marginal_quartic_separator(
        atlas, source, target_selected, templates
    )
    if result is not None:
        return "k3p_direct_marginal_quartic", register(
            registries, "k3p_direct_marginal_quartic", result
        )
    raise RestorationFailure("unresolved physical restoration child")


def forest_identity(layer, row):
    if layer == "first":
        return {
            "layer": 1,
            "legacy_row_sha256": row["row_sha256"],
            "root_id": row["root_id"],
            "restored_role": row["restored_role"],
            "restored_label": row["restored_label"],
            "source_insertion_index": row["source_insertion_index"],
        }
    return {
        "layer": 2,
        "legacy_row_sha256": row["row_sha256"],
        "parent_first_row_sha256": row["parent_first_row_sha256"],
        "root_id": row["root_id"],
        "restored_role": row["second_restored_role"],
        "restored_label": row["second_restored_label"],
        "source_insertion_index": row["second_source_insertion_index"],
    }


def validate_topology_and_transport(atlas, forest, rows):
    require(len(forest["first_coverage"]) == 36_568, "first frozen edge census")
    require(len(forest["second_coverage"]) == 256, "second frozen edge census")
    require(len(rows) == 36_824, "full frozen edge census")
    require(
        [row["ordinal"] for row in forest["first_coverage"]] == list(range(36_568)),
        "first row order/ordinal coverage",
    )
    first_hashes = [row["row_sha256"] for row in forest["first_coverage"]]
    second_hashes = [row["row_sha256"] for row in forest["second_coverage"]]
    require(len(set(first_hashes)) == len(first_hashes), "duplicate first forest row")
    require(len(set(second_hashes)) == len(second_hashes), "duplicate second forest row")
    continuations = [row for row in forest["first_coverage"] if row["status"] == "continuation"]
    require(len(continuations) == 32, "legacy continuation census")
    continuation_hashes = {row["row_sha256"] for row in continuations}
    children = collections.Counter(
        row["parent_first_row_sha256"] for row in forest["second_coverage"]
    )
    require(set(children) == continuation_hashes, "second parent coverage")
    require(set(children.values()) == {8}, "second children per continuation")
    seen_identity = set()
    transport_failures = []
    for layer, row, source, target_full, target_selected in rows:
        identity = tuple(sorted(forest_identity(layer, row).items()))
        require(identity not in seen_identity, "duplicate restoration child identity")
        seen_identity.add(identity)
        require(
            support.labels_of(source) == support.labels_of(target_selected),
            "source/target selected labels",
        )
        if layer == "first":
            source_transport = forest["first_source_transport_certificates"][
                row["source_parent_transport_id"]
            ]
            target_transport = forest["first_target_transport_certificates"][
                row["target_parent_transport_id"]
            ]
            source_parent = atlas.restrict_rooted(source, set(range(4)))
            target_parent = atlas.restrict_rooted(target_full, set(range(4)))
            source_hash = sha(support.exact_labelled_mixed_payload(atlas, source_parent))
            target_hash = sha(support.exact_labelled_mixed_payload(atlas, target_parent))
            if source_hash != source_transport["parent_mixed_graph_sha256"]:
                transport_failures.append((row["row_sha256"], "source"))
            if target_hash != target_transport["parent_mixed_graph_sha256"]:
                transport_failures.append((row["row_sha256"], "target"))
        else:
            source_parent = atlas.restrict_rooted(source, set(range(5)))
            target_parent = atlas.restrict_rooted(target_full, set(range(5)))
            if sha(support.exact_labelled_mixed_payload(atlas, source_parent)) != row[
                "source_parent_mixed_graph_sha256"
            ]:
                transport_failures.append((row["row_sha256"], "second_source"))
            if sha(support.exact_labelled_mixed_payload(atlas, target_parent)) != row[
                "target_parent_mixed_graph_sha256"
            ]:
                transport_failures.append((row["row_sha256"], "second_target"))
    require(not transport_failures, f"broken exact parent transports:{transport_failures[:3]}")
    legacy_first_terminal = sum(
        row["status"] == "separated" for row in forest["first_coverage"]
    )
    require(legacy_first_terminal == 36_536, "legacy first terminal census")
    require(legacy_first_terminal + len(forest["second_coverage"]) == 36_792,
            "legacy/full-forest leaf census")
    return {
        "forest_edges": len(rows),
        "first_edges": len(forest["first_coverage"]),
        "second_edges": len(forest["second_coverage"]),
        "legacy_structural_continuations": len(continuations),
        "legacy_full_forest_leaves": 36_792,
        "duplicate_children": 0,
        "missing_children": 0,
        "cycles": 0,
        "broken_parent_transports": 0,
        "max_depth": 2,
    }


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def deterministic_gzip_bytes(payload):
    import io
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as handle:
        handle.write(payload)
    return buffer.getvalue()


def write_gzip_json(path, value):
    path.write_bytes(deterministic_gzip_bytes(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    ))


def write_gzip_jsonl(path, rows):
    payload = b"".join(canonical_bytes(row) + b"\n" for row in rows)
    path.write_bytes(deterministic_gzip_bytes(payload))


def load_checkpoint(input_binding):
    if not CHECKPOINT_PATH.exists():
        return None
    checkpoint = json.loads(CHECKPOINT_PATH.read_text())
    require(checkpoint["schema"] == "k3p-restoration-producer-checkpoint-v1",
            "checkpoint schema")
    require(checkpoint["input_binding"] == input_binding, "checkpoint input drift")
    require(checkpoint["payload_sha256"] == logical_payload(checkpoint),
            "checkpoint payload")
    return checkpoint


def save_checkpoint(input_binding, records, registries):
    checkpoint = {
        "schema": "k3p-restoration-producer-checkpoint-v1",
        "input_binding": input_binding,
        "next_edge_index": len(records),
        "records": records,
        "registries": registries,
    }
    checkpoint["payload_sha256"] = logical_payload(checkpoint)
    atomic_json(CHECKPOINT_PATH, checkpoint)


def theorem_report(manifest):
    census = manifest["census"]
    proofs = census["all_edge_proof_counts"]
    return f"""# K3P fixed-full restoration theorem

Status: **PASS**.

## Theorem

For every fixed-full restoration obligation represented by the frozen corrected
restoration forest, the corresponding physical K3P source child is excluded
from the target child by an exact observable certificate.  The K3P proof
terminates all {census['minimal_k3p_terminal_rows']:,} first-layer rows.  In
particular, the 32 nodes that were structural continuations in the imported
K2P forest are already separated in K3P by direct four-port marginal quartics.

The complete imported graph forest is nevertheless replayed: it has
{census['forest_edges']:,} edges, 32 structural continuation nodes,
{census['redundant_depth2_edges']:,} depth-two edges, and
{census['legacy_full_forest_leaves']:,} legacy/full-forest leaves.  The last
256 edges are redundant for the minimal K3P proof but each is independently
reconstructed and separated.

## Exact K3P proof census over all forest edges

* displayed-quartet mismatch: {proofs.get('displayed_quartet_mismatch', 0):,}
* three-sector tree--ordinary-sunlet SOS: {proofs.get('k3p_tree_sunlet_sos', 0):,}
* regenerated K3P multihomogeneous quadratics: {proofs.get('k3p_exact_multihomogeneous_quadratic', 0):,}
* transported active K3P marginal quartics: {proofs.get('k3p_direct_marginal_quartic', 0):,}

The 614 old `T_i` rows are replaced by literal three-sector K3P maps and the
six-circuit sum-of-squares theorem.  The 148 old quadratic rows are regenerated
with independent C, G, and T variables.  The 24 old transported K2P quartic
rows, together with the 32 former continuation nodes, use exact active K3P
L20-01/H21-01 quartics.  No K2P equality such as C=T is imposed.

## Why the direct marginal is legitimate

The argument marginalizes the original fixed-full containment; it never lifts
an abstract selected relation.  Deleting the restored leaf and suppressing its
subdivision replaces each serial K3P edge chain by

`((c_i,g_i,t_i)) -> (product c_i, product g_i, product t_i)`.

Its Jacobian has three disjoint positive rows and rank three.  Since the strict
principal domain is open, the source restriction has a relative open image;
the target marginal only needs to be physical, not open.  Thus a target
identity with nonzero source pullback on the selected marginal excludes the
original full containment.  Every concrete graph restriction and parent
transport is replayed exactly in the machine ledger.

## Reproduction

```bash
cd {HERE}
../.venv/bin/python regenerate_k3p_restoration.py --resume
../.venv/bin/python verify_k3p_restoration.py
../.venv/bin/python test_k3p_restoration_mutations.py
```
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="resume a bound checkpoint")
    parser.add_argument("--fresh", action="store_true", help="discard only this producer's checkpoint")
    parser.add_argument("--checkpoint-interval", type=int, default=5_000)
    args = parser.parse_args()
    require(not (args.resume and args.fresh), "choose either --resume or --fresh")
    require(__debug__ and not sys.flags.optimize, "optimized Python forbidden")
    if args.fresh and CHECKPOINT_PATH.exists():
        CHECKPOINT_PATH.unlink()

    atlas, forest, rows = support.reconstruct_rows()
    structural = validate_topology_and_transport(atlas, forest, rows)
    templates = load_templates()
    input_binding = {
        "k3p_atlas_sha256": sha_file(ATLAS_PATH),
        "frozen_restoration_forest_sha256": sha_file(FOREST_PATH),
        "tree_sunlet_separator_sha256": sha_file(SEPARATOR_PATH),
        "three_port_primary_sha256": sha_file(THREE_PORT_PATH),
        "marginal_submersion_sha256": sha_file(MARGINAL_PATH),
        **{
            f"{path.name}_sha256": sha_file(path)
            for path in support.POLYNOMIAL_PATHS[:2]
        },
    }
    empty_registries = {
        "displayed_quartet_mismatch": {},
        "k3p_tree_sunlet_sos": {},
        "k3p_exact_multihomogeneous_quadratic": {},
        "k3p_direct_marginal_quartic": {},
    }
    checkpoint = load_checkpoint(input_binding) if args.resume else None
    if checkpoint is None:
        records = []
        registries = empty_registries
    else:
        records = checkpoint["records"]
        registries = checkpoint["registries"]
        require(len(records) <= len(rows), "checkpoint edge overflow")
        for number, record in enumerate(records):
            require(
                {key: record[key] for key in forest_identity(rows[number][0], rows[number][1])}
                == forest_identity(rows[number][0], rows[number][1]),
                f"checkpoint row identity drift:{number}",
            )

    proof_counts = collections.Counter(record["proof_kind"] for record in records)
    minimal_counts = collections.Counter(
        record["proof_kind"] for record in records if record["layer"] == 1
    )
    for edge_index in range(len(records), len(rows)):
        layer, frozen_row, source, target_full, target_selected = rows[edge_index]
        proof_kind, proof_id = classify_pair(
            atlas, source, target_full, target_selected, templates, registries
        )
        identity = forest_identity(layer, frozen_row)
        record = {
            "edge_index": edge_index,
            **identity,
            "source_graph_sha256": sha(graph_payload(source)),
            "target_full_graph_sha256": sha(graph_payload(target_full)),
            "target_selected_graph_sha256": sha(graph_payload(target_selected)),
            "legacy_structural_status": frozen_row["status"],
            "active_k3p_status": "separated" if layer == "first" else "redundant_verified",
            "proof_kind": proof_kind,
            "proof_id": proof_id,
            "uses_frozen_algebra": False,
        }
        if layer == "first":
            record["remaining_roles"] = frozen_row["remaining_roles"]
            record["source_parent_transport_id"] = frozen_row[
                "source_parent_transport_id"
            ]
            record["target_parent_transport_id"] = frozen_row[
                "target_parent_transport_id"
            ]
            if frozen_row["status"] == "continuation":
                record["k3p_refinement"] = "early_termination_before_redundant_depth2"
        else:
            record["legacy_full_forest_only"] = True
        record["row_sha256"] = sha(record)
        records.append(record)
        proof_counts[proof_kind] += 1
        if layer == "first":
            minimal_counts[proof_kind] += 1
        if args.checkpoint_interval > 0 and len(records) % args.checkpoint_interval == 0:
            save_checkpoint(input_binding, records, registries)
            print(f"K3P restoration edges:{len(records)}/{len(rows)}", flush=True)

    expected_all = {
        "displayed_quartet_mismatch": 36_006,
        "k3p_tree_sunlet_sos": 614,
        "k3p_exact_multihomogeneous_quadratic": 148,
        "k3p_direct_marginal_quartic": 56,
    }
    expected_minimal = {
        "displayed_quartet_mismatch": 35_758,
        "k3p_tree_sunlet_sos": 606,
        "k3p_exact_multihomogeneous_quadratic": 148,
        "k3p_direct_marginal_quartic": 56,
    }
    require(dict(sorted(proof_counts.items())) == expected_all,
            f"all-edge K3P proof census:{proof_counts}")
    require(dict(sorted(minimal_counts.items())) == expected_minimal,
            f"minimal K3P proof census:{minimal_counts}")
    require(len(records) == 36_824, "complete ledger")
    require(len({row["row_sha256"] for row in records}) == len(records),
            "duplicate active K3P row hash")

    registry_payload = {
        "schema": "k3p-restoration-proof-registry-v1",
        "status": "PASS",
        "inputs": input_binding,
        "proofs": registries,
        "counts": {key: len(value) for key, value in registries.items()},
        "uses_k2p_sector_equality": False,
        "uses_historical_k2p_algebra": False,
    }
    registry_payload["payload_sha256"] = logical_payload(registry_payload)
    write_gzip_json(REGISTRY_PATH, registry_payload)
    write_gzip_jsonl(LEDGER_PATH, records)

    manifest = {
        "schema": "k3p-fixed-full-restoration-manifest-v1",
        "status": "PASS",
        "claim_boundary": (
            "Complete exact K3P separation of every fixed-full restoration child. "
            "The active minimal proof terminates all first-layer rows; depth two is "
            "retained and verified solely as a redundant replay of the frozen forest."
        ),
        "inputs": input_binding,
        "producer": {
            "path": "restoration/regenerate_k3p_restoration.py",
            "sha256": sha_file(Path(__file__).resolve()),
            "support_path": "restoration/restoration_build_support.py",
            "support_sha256": sha_file(SUPPORT_PATH),
            "resumable_checkpoint_schema": "k3p-restoration-producer-checkpoint-v1",
            "optimized_mode_forbidden": True,
        },
        "frozen_field_policy": {
            "used": [
                "graph parentage and layer order",
                "root/source/target/permutation identities",
                "dummy repair roles and restored labels",
                "source insertion indices",
                "exact parent transport identifiers and hashes",
            ],
            "ignored": [
                "proof",
                "certificate",
                "certificate_sha256",
                "quartet_certificates",
                "sign_certificates",
                "algebra_certificates",
                "bridge_torus conclusions",
            ],
        },
        "census": {
            **structural,
            "minimal_k3p_terminal_rows": 36_568,
            "active_k3p_continuations": 0,
            "redundant_depth2_edges": 256,
            "all_edge_proof_counts": expected_all,
            "minimal_first_layer_proof_counts": expected_minimal,
            "old_Ti_rows_replaced": 614,
            "old_quadratic_rows_replaced": 148,
            "old_k2p_quartic_rows_replaced": 24,
            "former_continuations_early_terminated_by_k3p_quartic": 32,
            "unresolved": 0,
        },
        "ledger": {
            "path": "restoration/restoration_ledger.jsonl.gz",
            "sha256": sha_file(LEDGER_PATH),
            "rows": len(records),
            "ordered_row_hash_root": sha([row["row_sha256"] for row in records]),
        },
        "proof_registry": {
            "path": "restoration/restoration_proof_registry.json.gz",
            "sha256": sha_file(REGISTRY_PATH),
            "payload_sha256": registry_payload["payload_sha256"],
            "certificate_counts": registry_payload["counts"],
        },
        "direct_marginal_open_image": {
            "original_containment_is_marginalized_directly": True,
            "target_marginal_openness_used": False,
            "serial_map": "((c_i,g_i,t_i)) -> (prod c_i, prod g_i, prod t_i)",
            "jacobian_rank": 3,
            "selected_minor": "diag(prod_{i>1} c_i, prod_{i>1} g_i, prod_{i>1} t_i)",
            "source_relative_local_openness": True,
            "physical_section": "isotropic near-identity prefix factors and strict residual",
            "inheritance_transport": "lambda or 1-lambda, derivative +1 or -1",
            "marginal_certificate_sha256": sha_file(MARGINAL_PATH),
        },
        "uses_k2p_sector_equality": False,
        "uses_historical_k2p_algebra": False,
    }
    manifest["payload_sha256"] = logical_payload(manifest)
    atomic_json(MANIFEST_PATH, manifest)
    REPORT_PATH.write_text(theorem_report(manifest))
    if CHECKPOINT_PATH.exists():
        CHECKPOINT_PATH.unlink()
    print(json.dumps({
        "status": "PASS",
        "forest_edges": 36_824,
        "minimal_k3p_terminal_rows": 36_568,
        "legacy_full_forest_leaves": 36_792,
        "redundant_depth2_edges": 256,
        "proof_counts": expected_all,
        "payload_sha256": manifest["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (RestorationFailure, AssertionError, KeyError, IndexError, ValueError, OSError) as error:
        raise SystemExit(f"K3P_RESTORATION_BUILD_FAIL:{error}") from error
