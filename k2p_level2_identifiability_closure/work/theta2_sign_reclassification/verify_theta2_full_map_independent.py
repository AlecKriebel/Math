#!/usr/bin/env python3
"""Independent full-map replay of all 2,528 revoked theta2 sign rows.

The historical rooted witness table is not read.  The verifier discovers the
unique source-zero three-port restriction directly from each full five-port
K2P map, transports it through the labelled port permutation, and checks the
target sign certificate coefficientwise.
"""

from __future__ import annotations

import argparse
import collections
import fractions
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
LEDGER = PROJECT / "work/theta2_five_port_closure/artifacts/raw_directional_ledger.jsonl.gz"
PROOFS = PROJECT / "work/theta2_five_port_closure/artifacts/direct_proof_certificates.json.gz"
DEFAULT_CERTIFICATE = PROJECT / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json"
DEFAULT_REPORT = HERE / "theta2_independent_replay_certificate.json"


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


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


def sparse_payload(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def sparse_hash(polynomial):
    return sha(sparse_payload(polynomial))


def load_atlas():
    spec = importlib.util.spec_from_file_location("theta2_independent_full_map_atlas", ATLAS_PATH)
    require(spec is not None and spec.loader is not None, "atlas import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def t_pullback(atlas, descriptor, outputs, triple, orientation):
    assignments = atlas.orbit_assignments(descriptor.k)
    index = {assignment: number for number, assignment in enumerate(assignments)}
    others = sorted(set(triple) - {orientation})
    order = (others[0], others[1], orientation)

    def coordinate(characters):
        assignment = [0] * descriptor.k
        for label, character in zip(order, characters):
            assignment[label] = character
        return outputs[index[atlas.ct_orbit_rep(tuple(assignment))]]

    v_value = coordinate((1, 3, 2))
    x_s = coordinate((1, 1, 0))
    x_g = coordinate((2, 2, 0))
    y_g = coordinate((2, 0, 2))
    z_g = coordinate((0, 2, 2))
    return atlas.sparse_lincomb(
        [
            atlas.sparse_mul_many([v_value, v_value, x_g]),
            atlas.sparse_mul_many([x_s, x_s, y_g, z_g]),
        ],
        [1, -1],
    )


def bernstein_certificate(polynomial):
    require(polynomial, "empty target signed pullback")
    parameter_count = len(next(iter(polynomial)))
    monomial = tuple(
        min(exponent[index] for exponent in polynomial)
        for index in range(parameter_count)
    )
    active = tuple(
        index
        for index in range(parameter_count)
        if len({exponent[index] - monomial[index] for exponent in polynomial}) > 1
    )
    residual = {
        tuple(exponent[index] - monomial[index] for index in active): fractions.Fraction(coefficient)
        for exponent, coefficient in polynomial.items()
    }
    degree = tuple(max(exponent[index] for exponent in residual) for index in range(len(active)))
    shape = tuple(value + 1 for value in degree)
    coefficient_count = math.prod(shape)
    require(coefficient_count <= 1_000_000, f"Bernstein tensor bound:{coefficient_count}")
    strides = tuple(math.prod(shape[index + 1 :]) for index in range(len(shape)))
    values = [fractions.Fraction(0)] * coefficient_count
    for exponent, coefficient in residual.items():
        values[sum(value * stride for value, stride in zip(exponent, strides))] = coefficient
    for axis, axis_degree in enumerate(degree):
        stride = strides[axis]
        outer_count = math.prod(shape[:axis])
        block_size = (axis_degree + 1) * stride
        denominators = tuple(math.comb(axis_degree, alpha) for alpha in range(axis_degree + 1))
        converted = [fractions.Fraction(0)] * coefficient_count
        for outer in range(outer_count):
            base = outer * block_size
            for inner in range(stride):
                power = tuple(
                    values[base + alpha * stride + inner]
                    for alpha in range(axis_degree + 1)
                )
                for beta in range(axis_degree + 1):
                    total = fractions.Fraction(0)
                    for alpha in range(beta + 1):
                        if power[alpha]:
                            total += power[alpha] * fractions.Fraction(
                                math.comb(beta, alpha), denominators[alpha]
                            )
                    converted[base + beta * stride + inner] = total
        values = converted
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in values)
    require(signs[1] == 0 and signs[-1] > 0, f"target is not strictly negative:{signs}")
    result = {
        "method": "exact_tensor_Bernstein_after_positive_monomial",
        "parameter_count": parameter_count,
        "positive_monomial_exponent": list(monomial),
        "active_parameter_indices": list(active),
        "Bernstein_multidegree": list(degree),
        "Bernstein_coefficient_count": coefficient_count,
        "negative_coefficients": signs[-1],
        "zero_coefficients": signs[0],
        "positive_coefficients": signs[1],
        "minimum_coefficient": str(min(values)),
        "maximum_coefficient": str(max(values)),
        "domain": (
            "the full open unit cube in edge-sector and inheritance variables; "
            "therefore also its physical D_plus subset"
        ),
        "conclusion": "strictly_negative",
    }
    result["certificate_sha256"] = sha(result)
    return result


def main():
    if not __debug__:
        raise Failure("THETA2_FULL_MAP_REPLAY_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    started = time.monotonic()
    certificate = json.loads(args.certificate.read_text())
    claimed_payload = certificate.get("payload_sha256")
    unhashed = dict(certificate)
    unhashed.pop("payload_sha256", None)
    require(claimed_payload == sha(unhashed), "certificate payload")
    require(certificate.get("schema") == "k2p-theta2-tree-sunlet-full-map-truth-v1", "schema")
    require(certificate.get("status") == "PASS", "status")
    require(certificate["inputs"]["atlas_sha256"] == sha_file(ATLAS_PATH), "atlas input")
    require(certificate["inputs"]["raw_ledger_sha256"] == sha_file(LEDGER), "ledger input")
    require(certificate["inputs"]["legacy_proof_table_sha256"] == sha_file(PROOFS), "proof input hash")
    require(certificate["claimed_rows"] == 2_528, "claimed row count")
    require(certificate["full_map_source_zero_rows"] == 2_528, "source-zero count")
    require(certificate["full_map_strict_target_sign_rows"] == 2_528, "target-sign count")
    require(certificate["exact_full_graph_relation_census"] == {"none": 2_528}, "relation count")
    require(certificate["unresolved"] == certificate["incoherent"] == 0, "terminal status")

    rows = []
    with gzip.open(LEDGER, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("category") == "tree_sunlet_pointwise_excluded":
                rows.append(row)
    require(len(rows) == 2_528, f"primitive row census:{len(rows)}")
    truth_hashes = certificate.get("ordered_truth_row_hashes", [])
    require(len(truth_hashes) == len(rows), "truth row coverage")
    require(certificate["ordered_truth_row_hash_root"] == sha(truth_hashes), "truth hash root")

    atlas = load_atlas()
    sources = atlas.source_supports(("theta2",))
    targets = atlas.target_completions(5, True) + atlas.target_completions(5, False)
    source_descriptors = [atlas.model_descriptor_fast2(source.graph) for source in sources]
    source_outputs = [atlas.output_sparse_polynomials(descriptor) for descriptor in source_descriptors]

    # Discover the restriction algebraically.  Each repair must have exactly
    # one triple on which all three T orientations vanish coefficientwise.
    source_zero_triples = {}
    source_zero_polynomials = {}
    for source_index, (descriptor, outputs) in enumerate(zip(source_descriptors, source_outputs)):
        zero_triples = []
        for triple in itertools.combinations(range(5), 3):
            values = []
            for orientation in triple:
                polynomial = t_pullback(atlas, descriptor, outputs, triple, orientation)
                values.append(polynomial)
                source_zero_polynomials[(source_index, triple, orientation)] = polynomial
            if all(not polynomial for polynomial in values):
                zero_triples.append(triple)
        require(len(zero_triples) == 1, f"unique source-zero triple:{source_index}:{zero_triples}")
        source_zero_triples[source_index] = zero_triples[0]

    target_descriptor_cache = {}
    target_outputs_cache = {}
    target_polynomials = {}
    presentation_orientation = {}
    sign_records = certificate.get("sign_certificates", {})
    require(len(sign_records) == 85, f"sign certificate census:{len(sign_records)}")
    for polynomial_sha256, record in sorted(sign_records.items()):
        presentations = record.get("target_presentations", [])
        require(presentations, f"target presentation missing:{polynomial_sha256}")
        for target_index, public_triple, orientation in presentations:
            triple = tuple(public_triple)
            key = (target_index, triple, orientation)
            if target_index not in target_descriptor_cache:
                descriptor = atlas.model_descriptor_fast2(targets[target_index].graph)
                target_descriptor_cache[target_index] = descriptor
                target_outputs_cache[target_index] = atlas.output_sparse_polynomials(descriptor)
            if key not in target_polynomials:
                target_polynomials[key] = t_pullback(
                    atlas,
                    target_descriptor_cache[target_index],
                    target_outputs_cache[target_index],
                    triple,
                    orientation,
                )
            polynomial = target_polynomials[key]
            require(sparse_hash(polynomial) == polynomial_sha256, f"target polynomial hash:{key}")
            pair = (target_index, triple)
            require(pair not in presentation_orientation or presentation_orientation[pair] == orientation, f"incoherent target orientation:{pair}")
            presentation_orientation[pair] = orientation
        representative = presentations[0]
        representative_key = (representative[0], tuple(representative[1]), representative[2])
        polynomial = target_polynomials[representative_key]
        require(len(polynomial) == record["pullback_term_count"], "target term count")
        require(bernstein_certificate(polynomial) == record["sign"], f"target Bernstein replay:{polynomial_sha256}")

    prepared_sources = [atlas.prepare_mixed_source(source.graph) for source in sources]
    selected_cache = {}
    exact_relations = collections.Counter()
    relation_classes = collections.Counter()
    zero_sha256 = sparse_hash({})
    replayed_hashes = []
    for ordinal, row in enumerate(rows):
        permutation = tuple(row["port_permutation"])
        selected_key = (row["target_index"], permutation)
        if selected_key not in selected_cache:
            relabelled = atlas.relabel_record(targets[row["target_index"]], permutation)
            selected_cache[selected_key] = atlas.selected_graph_from_completion(relabelled)
        relation = atlas.mixed_relation_exact_prepared(
            prepared_sources[row["source_index"]], selected_cache[selected_key]
        )
        require(relation == "none", f"exact graph relation:{row['raw_id']}:{relation}")
        exact_relations[relation] += 1

        triple = source_zero_triples[row["source_index"]]
        inverse = {new: old for old, new in enumerate(permutation)}
        mapped_triple = tuple(sorted(inverse[label] for label in triple))
        pair = (row["target_index"], mapped_triple)
        require(pair in presentation_orientation, f"missing target sign presentation:{row['raw_id']}:{pair}")
        mapped_orientation = presentation_orientation[pair]
        source_orientation = permutation[mapped_orientation]
        source_polynomial = source_zero_polynomials[
            (row["source_index"], triple, source_orientation)
        ]
        require(not source_polynomial, f"source zero drift:{row['raw_id']}")
        target_polynomial = target_polynomials[
            (row["target_index"], mapped_triple, mapped_orientation)
        ]
        target_sha256 = sparse_hash(target_polynomial)
        truth_row = {
            "raw_id": row["raw_id"],
            "source_index": row["source_index"],
            "target_index": row["target_index"],
            "permutation_index": row["permutation_index"],
            "legacy_witness_triple": list(triple),
            "chosen_T_orientation_label": source_orientation,
            "source_pullback_sha256": zero_sha256,
            "target_pullback_sha256": target_sha256,
            "exact_full_graph_relation": "none",
            "result": "source_zero_strict_target_negative",
        }
        row_hash = sha(truth_row)
        require(row_hash == truth_hashes[ordinal], f"truth row hash:{ordinal}")
        replayed_hashes.append(row_hash)
        relation_classes[(zero_sha256, target_sha256)] += 1
    require(exact_relations == {"none": 2_528}, f"relation replay census:{exact_relations}")
    require(replayed_hashes == truth_hashes, "ordered truth replay")
    relation_public = {
        f"{source}:{target}": count
        for (source, target), count in sorted(relation_classes.items())
    }
    require(relation_public == certificate["canonical_relation_class_multiplicities"], "relation class multiplicities")
    require(len(relation_classes) == certificate["canonical_polynomial_relation_classes"] == 85, "relation class census")

    report = {
        "schema": "k2p-theta2-full-map-independent-replay-v1",
        "status": "PASS",
        "source_certificate_sha256": sha_file(args.certificate),
        "source_certificate_payload_sha256": claimed_payload,
        "raw_rows_replayed": len(rows),
        "algebraically_discovered_source_zero_triples": {
            str(index): list(triple) for index, triple in sorted(source_zero_triples.items())
        },
        "source_zero_rows": len(rows),
        "strict_target_negative_rows": len(rows),
        "exact_graph_relation_none_rows": exact_relations["none"],
        "sign_classes_replayed": len(relation_classes),
        "unresolved": 0,
        "runtime_seconds": time.monotonic() - started,
    }
    report["payload_sha256"] = sha(report)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Failure, KeyError, IndexError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"THETA2_FULL_MAP_REPLAY_FAIL:{error}") from error
