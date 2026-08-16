#!/usr/bin/env python3
"""Logical closure certificate for the complete root three-port atlas.

This verifier combines the exact JC tree-separation theorem, K2P reticulate
saturation, the two-class K3P reticulate atlas, and universal displayed-tree
containment.  It classifies bowtie and one-sided containment for every rooted
three-port generator under all three models.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from verify_jc_root_three_port_saturation import enumerate_unlabelled, topology_counts


HERE = Path(__file__).resolve().parent.parent
CERTIFICATE = HERE / "certificates" / "group_based_root_three_port_complete_atlas.json"
DEPENDENCIES = {
    "JC_reticulate": "jc_root_three_port_saturation.json",
    "JC_tree_separation": "jc_root_three_port_tree_separation.json",
    "K2P_reticulate": "k2p_root_three_port_saturation.json",
    "K3P_reticulate": "k3p_root_three_port_atlas.json",
    "displayed_tree_containment": "group_based_displayed_tree_containment.json",
}


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def load_dependencies():
    result = {}
    for key, name in DEPENDENCIES.items():
        path = HERE / "certificates" / name
        result[key] = {
            "name": name,
            "file_sha256": file_sha256(path),
            "data": json.loads(path.read_text()),
        }
    return result


def generate_certificate():
    dependencies = load_dependencies()
    records = enumerate_unlabelled()
    assert [record["kind"] for record in records] == [
        "tree",
        "cycle",
        "cycle",
        "theta",
        "theta",
        "theta",
        "theta",
        "theta",
    ]
    counts = topology_counts(records)
    assert counts["rooted_by_kind"] == {"cycle": 9, "theta": 30, "tree": 3}
    assert counts["semi_directed_total"] == 22

    jc = dependencies["JC_reticulate"]["data"]
    jc_sep = dependencies["JC_tree_separation"]["data"]
    k2p = dependencies["K2P_reticulate"]["data"]
    k3p = dependencies["K3P_reticulate"]["data"]
    containment = dependencies["displayed_tree_containment"]["data"]

    assert jc["status"]["all_reticulate_root_three_port_models_one_class"] == "PROVED"
    assert jc_sep["status"]["ordinary_tree_vs_reticulate_open_interiors"] == "PROVED DISJOINT"
    assert k2p["status"]["all_reticulate_root_three_port_models_one_K2P_bowtie_class"] == "PROVED"
    assert k3p["status"]["complete_reticulate_three_port_K3P_bowtie_atlas"] == "PROVED"
    assert containment["status"]["K2P_every_displayed_tree_complete_stochastic_containment"] == "PROVED"
    assert containment["status"]["K3P_every_displayed_tree_complete_stochastic_containment"] == "PROVED"

    k3_classes = k3p["class_counts"]
    assert k3_classes["H14"]["record_ids"] == [1, 2, 4]
    assert k3_classes["A15"]["record_ids"] == [3, 5, 6, 7]
    assert k3p["observational_relations"] == {
        "within_H14": "bowtie_K3P",
        "within_A15": "bowtie_K3P",
        "H14_to_A15": "preceq_K3P",
        "A15_to_H14": "no one-sided generic containment",
        "simultaneous_seven_model_intersection_local_dimension": 14,
    }

    classes = {
        "JC": {
            "T3": {
                "record_ids": [0],
                "dimension": 3,
                "rooted_topologies": 3,
                "semi_directed_topologies": 1,
            },
            "R4": {
                "record_ids": list(range(1, 8)),
                "dimension": 4,
                "rooted_topologies": 39,
                "semi_directed_topologies": 21,
            },
        },
        "K2P": {
            "T6": {
                "record_ids": [0],
                "dimension": 6,
                "rooted_topologies": 3,
                "semi_directed_topologies": 1,
            },
            "R9": {
                "record_ids": list(range(1, 8)),
                "dimension": 9,
                "rooted_topologies": 39,
                "semi_directed_topologies": 21,
            },
        },
        "K3P": {
            "T9": {
                "record_ids": [0],
                "dimension": 9,
                "rooted_topologies": 3,
                "semi_directed_topologies": 1,
            },
            "H14": {
                **k3_classes["H14"],
                "dimension": 14,
            },
            "A15": {
                **k3_classes["A15"],
                "dimension": 15,
            },
        },
    }

    relations = {
        "JC": {
            "T3--T3": "bowtie (isomorphic semi-directed tree; reversible root placements)",
            "R4--R4": "bowtie",
            "T3--R4": "disjoint open stochastic images; neither one-sided containment",
        },
        "K2P": {
            "T6--T6": "bowtie (equal complete tree image)",
            "R9--R9": "bowtie",
            "T6->R9": "complete open stochastic image containment",
            "R9->T6": "absent by dimension",
            "T6--R9_bowtie": "absent by unequal dimension",
        },
        "K3P": {
            "T9--T9": "bowtie (equal complete tree image)",
            "H14--H14": "bowtie",
            "A15--A15": "bowtie",
            "T9->H14": "complete open stochastic image containment",
            "T9->A15": "complete open stochastic image containment",
            "H14->A15": "one-sided generic containment on a regular 14-dimensional neighborhood",
            "A15->H14": "absent by dimension",
            "H14->T9": "absent by dimension",
            "A15->T9": "absent by dimension",
            "unequal_class_bowtie": "absent by unequal dimension",
        },
    }

    dependency_records = {
        key: {
            "name": value["name"],
            "file_sha256": value["file_sha256"],
            "deterministic_sha256": value["data"].get("deterministic_sha256"),
        }
        for key, value in dependencies.items()
    }
    certificate = {
        "status": {
            "complete_JC_root_three_port_bowtie_and_preceq_atlas": "PROVED",
            "complete_K2P_root_three_port_bowtie_and_preceq_atlas": "PROVED",
            "complete_K3P_root_three_port_bowtie_and_preceq_atlas": "PROVED",
            "complete_open_image_equality_within_reticulate_bowtie_classes": "UNRESOLVED",
        },
        "scope": (
            "all one ordinary-tree, two cycle, and five theta unlabelled "
            "three-port root generators, with every port labelling and rooted presentation"
        ),
        "unlabelled_record_order": [record["kind"] for record in records],
        "topology_counts": counts,
        "observational_classes": classes,
        "class_relations": relations,
        "simultaneous_intersections": {
            "JC_all_eight_unlabelled_models": "empty in the open stochastic domain",
            "K2P_all_eight_unlabelled_models": (
                "exactly the complete ordinary-tree image, dimension 6"
            ),
            "K3P_all_eight_unlabelled_models": (
                "exactly the complete ordinary-tree image, dimension 9"
            ),
        },
        "dependency_certificates": dependency_records,
        "conclusion": (
            "The smallest nontrivial root-generator atlas is now complete for "
            "bowtie and one-sided generic containment under JC, K2P, and K3P. "
            "The model hierarchy reverses at the tree boundary: JC separates "
            "tree from every reticulate generator, whereas K2P and K3P place "
            "the complete tree image inside every reticulate generator."
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
                "observational_classes": certificate["observational_classes"],
                "simultaneous_intersections": certificate["simultaneous_intersections"],
                "status": certificate["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
