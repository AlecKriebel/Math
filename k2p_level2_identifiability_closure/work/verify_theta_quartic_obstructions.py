#!/usr/bin/env python3
"""Independent exact replay of three sparse quartics covering twelve records.

Unlike the candidate generator, this verifier never constructs a MapDescriptor
and never invokes any separator or kernel routine.  It expands the four
displayed-tree sums directly from the bound graph presentations.  With
``--run-root`` it also binds every transported row to its production record.
"""

from __future__ import annotations

import argparse
import importlib.util
import hashlib
import json
import sys
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
SPEC = importlib.util.spec_from_file_location("k2p_theta_replay_core", CORE)
assert SPEC is not None and SPEC.loader is not None
atlas = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = atlas
SPEC.loader.exec_module(atlas)


def polynomial_add_term(polynomial, exponent, coefficient):
    polynomial[exponent] += coefficient
    if not polynomial[exponent]:
        del polynomial[exponent]


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def polynomial_multiply(left, right):
    result = defaultdict(int)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent))
            result[exponent] += left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def inheritance_polynomial(bits, edge_parameter_count):
    parameter_count = 2 * edge_parameter_count + len(bits)
    polynomial = {(0,) * parameter_count: 1}
    for index, bit in enumerate(bits):
        variable = [0] * parameter_count
        variable[2 * edge_parameter_count + index] = 1
        if bit:
            factor = {tuple(variable): 1}
        else:
            factor = {(0,) * parameter_count: 1, tuple(variable): -1}
        polynomial = polynomial_multiply(polynomial, factor)
    return polynomial


def raw_coordinate_polynomials(graph):
    arms = atlas.selected_arm_edges(graph)
    edges = tuple(edge for edge in graph.edges() if edge not in arms)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    retics = atlas.reticulation_nodes(graph)
    parents = tuple(tuple(sorted(graph.predecessors(node), key=repr)) for node in retics)
    parameter_count = 2 * len(edges) + len(retics)
    outputs = []
    for characters in atlas.orbit_assignments(4):
        output = defaultdict(int)
        for bits in product((0, 1), repeat=len(retics)):
            removed = set()
            for node, choices, bit in zip(retics, parents, bits):
                kept_parent = choices[bit]
                removed.update((parent, node) for parent in choices if parent != kept_parent)
            kept = tuple(edge for edge in graph.edges() if edge not in removed)
            masks = atlas.descendant_masks_for_switch(graph, kept)
            edge_exponent = [0] * parameter_count
            for edge in edges:
                if edge not in masks:
                    continue
                sector = atlas.sector_for_mask(masks[edge], characters)
                if sector:
                    edge_exponent[2 * edge_index[edge] + sector - 1] += 1
            for inheritance_exponent, coefficient in inheritance_polynomial(bits, len(edges)).items():
                exponent = tuple(a + b for a, b in zip(edge_exponent, inheritance_exponent))
                polynomial_add_term(output, exponent, coefficient)
        outputs.append(dict(output))
    return tuple(outputs)


def pullback(outputs, terms):
    result = defaultdict(int)
    for coefficient, indices in terms:
        polynomial = {(0,) * len(next(iter(outputs[0]))): 1}
        for index in indices:
            polynomial = polynomial_multiply(polynomial, outputs[index])
        for exponent, value in polynomial.items():
            result[exponent] += coefficient * value
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def coordinate_weight(indices):
    weights = atlas.coordinate_weights(4)
    return tuple(sum(weights[index][column] for index in indices) for column in range(8))


CERTIFICATES = {
    "source2-class112": {
        "source": 2,
        "permutation": (0, 1, 2, 3),
        "weight": (3, 0, 2, 1, 1, 1, 2, 1),
        "terms": (
            (1, (0, 15, 16, 18)),
            (1, (0, 16, 18, 23)),
            (-1, (0, 20, 22, 23)),
            (1, (1, 14, 16, 18)),
            (-2, (3, 11, 16, 18)),
            (1, (3, 11, 20, 22)),
            (-1, (4, 12, 18, 22)),
            (-1, (8, 10, 14, 16)),
            (1, (8, 12, 14, 22)),
        ),
    },
    "source2-class113": {
        "source": 2,
        "permutation": (0, 1, 3, 2),
        "weight": (2, 1, 3, 0, 1, 1, 2, 1),
        "terms": (
            (1, (0, 16, 17, 29)),
            (-1, (0, 16, 23, 29)),
            (-1, (0, 17, 22, 31)),
            (1, (0, 22, 23, 31)),
            (-1, (1, 14, 16, 29)),
            (1, (1, 14, 22, 31)),
            (2, (3, 11, 16, 29)),
            (-1, (3, 11, 22, 31)),
            (-1, (3, 14, 16, 27)),
            (-1, (5, 11, 22, 29)),
            (1, (5, 14, 22, 27)),
        ),
    },
    "source4-class8": {
        "source": 4,
        "permutation": (0, 1, 2, 3),
        "weight": (2, 1, 3, 0, 2, 1, 1, 1),
        "terms": (
            (1, (0, 15, 16, 32)),
            (1, (0, 16, 23, 32)),
            (-1, (0, 23, 24, 30)),
            (1, (1, 14, 16, 32)),
            (-2, (3, 11, 16, 32)),
            (1, (3, 11, 24, 30)),
            (-1, (4, 14, 16, 27)),
            (-1, (6, 10, 24, 32)),
            (1, (6, 14, 24, 27)),
        ),
    },
}


def transform_terms(terms, index_map):
    return tuple(
        (coefficient, tuple(index_map[index] for index in indices))
        for coefficient, indices in terms
    )


def canonical_pullback(graph, terms):
    descriptor = atlas.model_descriptor_fast2(graph)
    outputs = atlas.output_sparse_polynomials(descriptor)
    columns = [atlas.sparse_mul_many([outputs[index] for index in indices]) for _coefficient, indices in terms]
    coefficients = [coefficient for coefficient, _indices in terms]
    return atlas.sparse_lincomb(columns, coefficients)


def canonical_pullback_metadata(polynomial):
    ordered = [(list(exponent), str(coefficient)) for exponent, coefficient in sorted(polynomial.items())]
    encoded = json.dumps(ordered, separators=(",", ":")).encode()
    exponent, coefficient = ordered[0]
    return {
        "term_count": len(polynomial),
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "witness": {"exponent": exponent, "coefficient": coefficient},
    }


def evaluate_coordinate_polynomial(terms, coordinates):
    value = Fraction(0)
    for coefficient, indices in terms:
        term = Fraction(coefficient)
        for index in indices:
            term *= coordinates[index]
        value += term
    return value


def validate_record_binding(run_root, artifact):
    record_path = (
        run_root / f"source_{artifact['source_index']}" / "records" /
        f"class_{artifact['canonical_class_id']:06d}.json"
    )
    record = json.loads(record_path.read_text())
    assert record["status"] == "unresolved"
    assert record["stratum"] == "direct_no_dummy"
    for field in (
        "source_index", "canonical_class_id", "semantic_record_sha256",
        "source_graph_sha256", "target_graph_sha256", "descriptor_sha256",
        "source_rank", "target_rank",
    ):
        assert artifact[field] == record[field], (artifact["source_index"], artifact["canonical_class_id"], field)
    assert len(record["members"]) == 1
    member = record["members"][0]
    assert artifact["target_index"] == member["target_index"]
    assert artifact["port_match"] == member["port_match"]
    assert artifact["target_selected_graph_sha256"] == member["target_selected_graph_sha256"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).with_name("theta_quartic_obstruction_certificates.json"),
    )
    parser.add_argument(
        "--run-root",
        type=Path,
        help="optional completed sweep root whose 12 records must match every bound hash and port match",
    )
    args = parser.parse_args()
    certificate_path = args.certificate.resolve()
    payload = json.loads(certificate_path.read_text())
    assert payload["schema"] == "k2p-theta-quartic-obstructions-v2"
    replay = payload["replay"]
    assert sha256_file(Path(__file__).resolve()) == replay["independent_direct_switch_verifier_sha256"]
    for path_field, hash_field in (
        ("candidate_generator", "candidate_generator_sha256"),
        ("separately_authored_adversarial_verifier", "separately_authored_adversarial_verifier_sha256"),
        ("separately_authored_certificate", "separately_authored_certificate_sha256"),
    ):
        assert sha256_file(ROOT / replay[path_field]) == replay[hash_field]
    coordinate_bytes = json.dumps(
        payload["coordinate_convention"]["order"], sort_keys=True, separators=(",", ":")
    ).encode()
    assert hashlib.sha256(coordinate_bytes).hexdigest() == payload["coordinate_convention"]["canonical_json_sha256"]
    assert tuple(tuple(row) for row in payload["coordinate_convention"]["order"]) == atlas.orbit_assignments(4)
    base_rows = {
        f"source{row['source_index']}-class{row['canonical_class_id']}": row
        for row in payload["certificates"]
    }
    assert set(base_rows) == set(CERTIFICATES)
    permutations = {name: tuple(values) for name, values in payload["coordinate_permutations"].items()}
    assert permutations["identity"] == tuple(range(36))
    assignments = atlas.orbit_assignments(4)
    assignment_index = {assignment: index for index, assignment in enumerate(assignments)}
    expected_swap_01 = tuple(
        assignment_index[atlas.ct_orbit_rep((assignment[1], assignment[0], assignment[2], assignment[3]))]
        for assignment in assignments
    )
    assert permutations["swap_01"] == expected_swap_01
    for name, certificate in CERTIFICATES.items():
        artifact = base_rows[name]
        assert tuple(artifact["port_match"]) == certificate["permutation"]
        assert tuple(artifact["port_weight"]) == certificate["weight"]
        assert tuple((coefficient, tuple(indices)) for coefficient, indices in artifact["terms"]) == certificate["terms"]

    sources = atlas.source_supports()
    target_record = atlas.target_completions(4, True)[822]
    assert (target_record.core_id, target_record.repair_index, target_record.dummy_labels) == ("theta3", 1, ())
    transports = payload["transports"]
    assert len(transports) == 12
    assert {(row["source_index"], row["canonical_class_id"]) for row in transports} == {
        *((source, class_id) for source in (2, 3) for class_id in (112, 113, 114, 115)),
        *((4, class_id) for class_id in (8, 9, 10, 11)),
    }
    if args.run_root is not None:
        run_root = args.run_root.resolve()
        for artifact in transports:
            validate_record_binding(run_root, artifact)

    strict = payload["strict_D_plus_witness"]
    strict_values_bytes = json.dumps(
        strict["exact_nonzero_values"], sort_keys=True, separators=(",", ":")
    ).encode()
    assert hashlib.sha256(strict_values_bytes).hexdigest() == strict["exact_nonzero_values_sha256"]
    strict_values = {
        (row["source_index"], row["canonical_class_id"]): Fraction(row["value"])
        for row in strict["exact_nonzero_values"]
    }
    strict_edge_pairs = tuple(
        (Fraction(row["s"]), Fraction(row["g"])) for row in strict["edge_pairs"]
    )
    strict_lambdas = tuple(Fraction(value) for value in strict["inheritance_probabilities"])
    assert len(strict_edge_pairs) == 8 and len(strict_lambdas) == 2
    for s_value, g_value in strict_edge_pairs:
        assert 0 < s_value < 1 and 0 < g_value < 1 and g_value > 2 * s_value - 1
    assert all(0 < value < 1 for value in strict_lambdas)
    strict_source_coordinates = {
        source_index: atlas.eval_descriptor(
            atlas.model_descriptor_fast2(sources[source_index].graph),
            strict_edge_pairs,
            strict_lambdas,
        )
        for source_index in (2, 3, 4)
    }

    raw_source_outputs = {index: raw_coordinate_polynomials(sources[index].graph) for index in (2, 3, 4)}
    raw_target_outputs = {}
    replay_rows = []
    for artifact in transports:
        name = f"source{artifact['source_index']}-class{artifact['canonical_class_id']}"
        base = CERTIFICATES[artifact["base_certificate"]]
        terms = transform_terms(base["terms"], permutations[artifact["coordinate_permutation"]])
        observed_weights = {coordinate_weight(indices) for _coefficient, indices in terms}
        assert observed_weights == {tuple(artifact["port_weight"])}, (name, observed_weights)
        port_match = tuple(artifact["port_match"])
        target = atlas.relabel_record(target_record, port_match)
        if port_match not in raw_target_outputs:
            raw_target_outputs[port_match] = raw_coordinate_polynomials(target.graph)
        raw_target_pullback = pullback(raw_target_outputs[port_match], terms)
        raw_source_pullback = pullback(raw_source_outputs[artifact["source_index"]], terms)
        assert not raw_target_pullback, (name, "raw target pullback nonzero", len(raw_target_pullback))
        assert raw_source_pullback, (name, "raw source pullback vanished")
        assert artifact["target_pullback_term_count"] == 0
        assert artifact["source_pullback_term_count"] == len(raw_source_pullback)

        canonical_target_pullback = canonical_pullback(target.graph, terms)
        canonical_source_pullback = canonical_pullback(sources[artifact["source_index"]].graph, terms)
        assert not canonical_target_pullback
        metadata = canonical_pullback_metadata(canonical_source_pullback)
        assert metadata["term_count"] == artifact["source_pullback_term_count"]
        assert metadata["sha256"] == artifact["source_pullback_sha256"]
        assert metadata["witness"] == artifact["source_witness"]
        strict_value = evaluate_coordinate_polynomial(
            terms, strict_source_coordinates[artifact["source_index"]]
        )
        assert strict_value == strict_values[(artifact["source_index"], artifact["canonical_class_id"])]
        assert strict_value
        row = {
            "source_index": artifact["source_index"],
            "canonical_class_id": artifact["canonical_class_id"],
            "base_certificate": artifact["base_certificate"],
            "coordinate_permutation": artifact["coordinate_permutation"],
            "target_terms": 0,
            "source_terms": len(raw_source_pullback),
            "source_witness": metadata["witness"],
            "strict_D_plus_value": str(strict_value),
            "port_weight": artifact["port_weight"],
        }
        replay_rows.append(row)
        print(json.dumps(row, sort_keys=True))
    assert len(replay_rows) == 12
    print("THETA_QUARTIC_OBSTRUCTIONS_INDEPENDENT_REPLAY_PASS")


if __name__ == "__main__":
    main()
