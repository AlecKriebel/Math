#!/usr/bin/env python3
"""Exact cross-model certificate for ordinary triangle redirection.

The complete three-port root census contains two unlabelled cycle records.
After all port labellings these records give nine rooted topologies and exactly
three semi-directed topologies.  This verifier checks that those three graphs
are pairwise related by the formal triangle-redirection predicate and then
extracts the common regular stochastic witnesses already certified by the JC,
K2P, and K3P three-port atlases.

The result is a local move theorem, not a claim that the complete open model
images are equal.  The algebraic parameter correspondence is the germ obtained
by fixing the recorded gauge parameters and inverting the recorded nonsingular
output Jacobian block.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

from enumerate_four_leaf_root_theta import canonical_code
from verify_jc_four_network_class import semi_directed_graph
from verify_jc_fully_labelled_support_atlas import canonical_mixed_graph
from verify_jc_root_spanning_atlas import is_triangle_redirection, triangles
from verify_jc_root_three_port_saturation import enumerate_unlabelled


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "group_based_triangle_redirection.json"
DEPENDENCIES = {
    "JC": HERE / "certificates" / "jc_root_three_port_saturation.json",
    "K2P": HERE / "certificates" / "k2p_root_three_port_saturation.json",
    "K3P": HERE / "certificates" / "k3p_root_three_port_atlas.json",
}


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def load_dependencies():
    return {
        model: {
            "path": str(path.relative_to(HERE)),
            "file_sha256": file_sha256(path),
            "certificate": json.loads(path.read_text()),
        }
        for model, path in DEPENDENCIES.items()
    }


def reticulation_port_label(graph):
    colors, edges = graph
    reticulations = [vertex for vertex, color in colors.items() if color == "R"]
    assert len(reticulations) == 1
    reticulation = reticulations[0]
    labels = []
    for _kind, left, right in edges:
        if left == reticulation and colors[right].startswith("L"):
            labels.append(colors[right])
        if right == reticulation and colors[left].startswith("L"):
            labels.append(colors[left])
    assert len(labels) == 1
    return labels[0]


def cycle_topology_certificate(records):
    cycle_records = [
        (index, record)
        for index, record in enumerate(records)
        if record["kind"] == "cycle"
    ]
    assert [index for index, _record in cycle_records] == [1, 2]

    raw_presentations = []
    rooted_codes = set()
    semi_graphs = {}
    for record_id, record in cycle_records:
        network = record["network"]
        for labels in permutations((1, 2, 3)):
            rooted_code = canonical_code(
                network["vertices"],
                network["edges"],
                dict(zip(network["leaves"], labels)),
            )
            graph = semi_directed_graph(network, labels)
            semi_code = canonical_mixed_graph(graph)
            rooted_codes.add(rooted_code)
            semi_graphs.setdefault(semi_code, graph)
            raw_presentations.append(
                {
                    "record_id": record_id,
                    "labels_in_port_order": list(labels),
                    "rooted_code_sha256": sha256(repr(rooted_code).encode()).hexdigest(),
                    "semi_directed_code_sha256": sha256(
                        repr(semi_code).encode()
                    ).hexdigest(),
                }
            )

    assert len(raw_presentations) == 12
    assert len(rooted_codes) == 9
    assert len(semi_graphs) == 3

    ordered = sorted(semi_graphs.items(), key=lambda item: repr(item[0]))
    orientation_records = []
    for code, graph in ordered:
        assert len(triangles(graph)) == 1
        orientation_records.append(
            {
                "reticulation_port_label": reticulation_port_label(graph),
                "canonical_code": repr(code),
                "canonical_code_sha256": sha256(repr(code).encode()).hexdigest(),
            }
        )
    assert {item["reticulation_port_label"] for item in orientation_records} == {
        "L1",
        "L2",
        "L3",
    }

    redirection_pairs = []
    for (first_code, first), (second_code, second) in combinations(ordered, 2):
        assert is_triangle_redirection(first, second)
        redirection_pairs.append(
            [
                sha256(repr(first_code).encode()).hexdigest(),
                sha256(repr(second_code).encode()).hexdigest(),
            ]
        )
    assert len(redirection_pairs) == 3

    return {
        "unlabelled_cycle_record_ids": [1, 2],
        "raw_record_label_presentations": len(raw_presentations),
        "distinct_rooted_topologies": len(rooted_codes),
        "distinct_semi_directed_topologies": len(semi_graphs),
        "orientation_records": orientation_records,
        "pairwise_triangle_redirection_relations": redirection_pairs,
        "all_three_pairs_pass_formal_T_predicate": True,
        "presentations": raw_presentations,
    }


def model_certificate(dependencies):
    jc = dependencies["JC"]["certificate"]
    k2p = dependencies["K2P"]["certificate"]
    k3p = dependencies["K3P"]["certificate"]

    jc_cycles = [
        record for record in jc["networks"] if record["id"] in (1, 2)
    ]
    assert len(jc_cycles) == 2
    assert all(record["kind"] == "cycle" for record in jc_cycles)
    assert all(record["generic_rank"] == 4 for record in jc_cycles)
    assert all("common_regular_witness" in record for record in jc_cycles)

    k2p_cycles = [
        record
        for record in k2p["rank_certificate"]["records"]
        if record["id"] in (1, 2)
    ]
    assert len(k2p_cycles) == 2
    assert all(record["kind"] == "cycle" for record in k2p_cycles)
    assert all(record["generic_K2P_rank"] == 9 for record in k2p_cycles)
    assert all(record["minor_roots_in_isolating_interval"] == 0 for record in k2p_cycles)

    k3p_generic = {
        record["id"]: record for record in k3p["generic_rank_certificates"]
    }
    k3p_common = {
        record["id"]: record
        for record in k3p["common_exact_algebraic_preimages"]["records"]
    }
    assert all(k3p_generic[index]["class"] == "H14" for index in (1, 2))
    assert all(k3p_generic[index]["generic_rank"] == 14 for index in (1, 2))
    assert all(k3p_common[index]["K3P_rank_block_order"] == 14 for index in (1, 2))
    assert all(k3p_common[index]["unique_real_algebraic_preimage_in_box"] for index in (1, 2))
    assert k3p["class_counts"]["H14"]["one_triangle_semi_directed_topologies"] == 3

    # The common rank blocks use every nonconstant coordinate except q321.
    # Differentiate the recorded sparse quartic directly at the recorded
    # rational target to prove that this projection is a local coordinate
    # chart on V(I), without relying on floating-point evaluation.
    assert all(
        record["K3P_rank_block_rows"] == list(range(13)) + [14]
        for record in (k3p_common[index] for index in (1, 2))
    )
    target = {
        name: Fraction(value)
        for name, value in k3p["common_target"]["all_16_coordinates"].items()
    }
    omitted = "321"
    omitted_partial = Fraction(0)
    for term in k3p["quartic"]["terms"]:
        monomial = ["".join(map(str, assignment)) for assignment in term["monomial"]]
        for occurrence, coordinate in enumerate(monomial):
            if coordinate == omitted:
                value = Fraction(term["coefficient"])
                for position, factor in enumerate(monomial):
                    if position != occurrence:
                        value *= target[factor]
                omitted_partial += value
    assert omitted_partial == Fraction(37, 10**14)

    return {
        "JC": {
            "local_model_dimension": 4,
            "common_target": jc["common_target"],
            "cycle_common_regular_witnesses": [
                record["common_regular_witness"] for record in jc_cycles
            ],
            "closure": "normalized affine 4-space",
            "correspondence": (
                "algebraic germ obtained by inverting the nonsingular "
                "(a0,a1,a2,h)-to-(r12,r13,r23,u123) section"
            ),
            "pairwise_bowtie": "PROVED",
        },
        "K2P": {
            "local_model_dimension": 9,
            "common_target": k2p["common_target"],
            "cycle_rank_records": k2p_cycles,
            "closure": "normalized affine 9-space",
            "correspondence": (
                "algebraic germ obtained by fixing omitted parameters and "
                "inverting the recorded 9x9 output Jacobian minor"
            ),
            "pairwise_bowtie": "PROVED",
        },
        "K3P": {
            "local_model_dimension": 14,
            "common_target": k3p["common_target"],
            "cycle_generic_rank_records": [k3p_generic[index] for index in (1, 2)],
            "cycle_common_preimage_records": [k3p_common[index] for index in (1, 2)],
            "closure": "the irreducible quartic hypersurface V(I), dimension 14",
            "local_coordinate_projection": {
                "omitted_coordinate": "q321",
                "quartic_partial_at_common_target": str(omitted_partial),
            },
            "correspondence": (
                "unique real-algebraic germ obtained by fixing omitted "
                "parameters and inverting the recorded 14x14 output block; "
                "the exact Krawczyk boxes select its physical branch"
            ),
            "pairwise_bowtie": "PROVED",
        },
    }


def generate_certificate():
    dependencies = load_dependencies()
    records = enumerate_unlabelled()
    topology = cycle_topology_certificate(records)
    models = model_certificate(dependencies)

    dependency_records = {
        model: {
            "path": data["path"],
            "file_sha256": data["file_sha256"],
            "deterministic_sha256": data["certificate"].get(
                "deterministic_sha256"
            ),
        }
        for model, data in dependencies.items()
    }
    certificate = {
        "status": {
            "triangle_redirection_bowtie_JC": "PROVED",
            "triangle_redirection_bowtie_K2P": "PROVED",
            "triangle_redirection_bowtie_K3P": "PROVED",
            "all_three_semi_directed_orientations_covered": "PROVED",
            "arbitrary_corresponding_port_grafting": "PROVED",
            "complete_open_stochastic_image_equality": "UNRESOLVED",
        },
        "move": {
            "name": "T",
            "definition": (
                "retain the labelled underlying three-port triangle and all "
                "arrowheads outside it, and change which triangle vertex is "
                "the reticulation"
            ),
            "semi_directed_orientation_class_size": 3,
            "pairwise_generators": 3,
            "changes_underlying_labelled_undirected_graph": False,
            "may_change_rooted_topology": True,
        },
        "topology": topology,
        "models": models,
        "grafting": {
            "statement": (
                "substituting identical positive group-based components at "
                "corresponding ports preserves each common tensor; on the "
                "certified positive-multiplier neighborhoods, characterwise "
                "tripod inversion recovers the local tensor and adds ranks"
            ),
            "JC_character_gauge_dimension_per_cut": 1,
            "K2P_character_gauge_dimension_per_cut": 2,
            "K3P_character_gauge_dimension_per_cut": 3,
            "full_dimensional_overlap_preserved": True,
        },
        "dependencies": dependency_records,
        "conclusion": (
            "Ordinary triangle redirection T is a universal local "
            "full-dimensional regular stochastic ambiguity for JC, K2P, "
            "and K3P.  The richer models separate Theta and Omega_chain but "
            "do not identify the reticulation vertex of a three-port triangle."
        ),
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    certificate["deterministic_sha256"] = sha256(payload.encode()).hexdigest()
    return certificate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(json.dumps(generate_certificate(), sort_keys=True))
    if args.write_certificate:
        CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    else:
        assert certificate == json.loads(CERTIFICATE.read_text())
    print(
        json.dumps(
            {
                "deterministic_sha256": certificate["deterministic_sha256"],
                "status": certificate["status"],
                "topology": {
                    key: certificate["topology"][key]
                    for key in (
                        "distinct_rooted_topologies",
                        "distinct_semi_directed_topologies",
                        "all_three_pairs_pass_formal_T_predicate",
                    )
                },
                "dimensions": {
                    model: data["local_model_dimension"]
                    for model, data in certificate["models"].items()
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
